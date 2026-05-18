import pygame
import threading
from client_server.client_udp import Client
from client_server.server_udp import Server
from constants import Constants
from sound.sound_type import MusicType, SoundEffectType
from map.game_map import GameMap
from player.player import Player
from player.player_state import PlayerState, PlayerCharacter
from menu.main_menu import MainMenu
from menu.pause_menu import PauseMenu
from menu.options_menu import OptionsMenu
from menu.character_menu import CharacterMenu
from intro.intro_screen import IntroScreen
from sound.sound_manager import SoundManager
from ui.UI import UI
from ui.building_info import BuildingInfo
from map.ui_map import MapViewer
from gaming.gaming import Gaming
from menu.game_over import GameOver
from menu.win_screen import WinScreen


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Constants.WINDOW_HEIGHT, Constants.WINDOW_WIDTH))
        pygame.display.set_caption("Kampus Crawler")
        pygame.display.set_icon(pygame.image.load('assets/logo/logo_icon.png'))

        self.map_data = GameMap("assets/map_data/map_all.tmx", Constants.MAP_SCALE)
        self.player = Player(PlayerState.IDLE_DOWN)

        self.client = None
        self.server = None
        self.running = True
        self.paused = False
        self.map_open = False

        self.map_viewer = MapViewer(self.screen)
        self.options_menu = OptionsMenu(self.screen, self.player)
        self.character_menu = CharacterMenu(self.screen, self.player)
        self.pause_menu = PauseMenu(self.screen)

        IntroScreen.play(self.screen)

        SoundManager.init()
        SoundManager.play_music(MusicType.Menu)

        self.msg_typing = False
        self.msg = ""
        self.ui = None
        self.game_time_seconds = 600
        self.max_game_time = 600
        self.current_objective = "C4"  # static for now
        self.game_over = False
        self.gaming = Gaming(self)
        self.building_info = BuildingInfo(self)
        self.dt = 0

        self.client = Client(Constants.SERVER_IP_ADDR, Constants.SERVER_PORT)
        
    def start_networking(self):
        # Start client
        self.client.disconnect = False
        client_thread = threading.Thread(target=Client.network_thread, args=(self.client, self.player), daemon=True)
        client_thread.start()

    def draw_game(self, dt):
        self.screen.fill((30, 30, 30))
        self.map_data.draw(self.screen, self.player.data.pos_x, self.player.data.pos_y)
        self.player.draw(
            self.screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, self.dt, 0, 0
        )
        # Draw other players
        with self.client.lock:
            for player_id, other_player_data in self.client.all_players.items():
                if other_player_data.clientID == self.player.data.clientID:
                    continue
                if player_id not in self.client.player_objects:
                    self.client.player_objects[player_id] = Player(other_player_data.state, other_player_data.character)

                if self.client.player_objects[player_id].data.state != other_player_data.state:
                    self.client.player_objects[player_id].set_animation(other_player_data.state)

                self.client.player_objects[player_id].data = other_player_data
                offset_x = other_player_data.pos_x - self.player.data.pos_x
                offset_y = other_player_data.pos_y - self.player.data.pos_y

                self.client.player_objects[player_id].draw(
                    self.screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, self.dt, offset_x, offset_y
                )

        # Msg input box
        if self.msg_typing:
            font = pygame.font.Font("assets/menu/font.ttf", 10)
            text = self.msg + "|"
            text_surface = font.render(text, True, (38, 38, 38))
            text_rect = text_surface.get_rect(center=(Constants.WINDOW_HEIGHT / 2, (Constants.WINDOW_WIDTH / 2) - (
                        self.player.player_img_info.scale_size_x / 2) - 20))
            # background
            bubble_rect = text_rect.inflate(16, 8)
            outline_rect = bubble_rect.inflate(4, 4)
            pygame.draw.rect(self.screen, (100, 100, 100), outline_rect, border_radius=10)
            pygame.draw.rect(self.screen, (207, 207, 207), bubble_rect, border_radius=8)
            self.screen.blit(text_surface, text_rect)

        self.ui.draw(self.current_objective, self.max_game_time, self.game_time_seconds)

        self.building_info.try_draw()

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return None
            # Handle chat message input
            if self.msg_typing:
                self.player.movement.stop()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.msg.strip():
                            self.player.data.chat_message = self.msg
                            self.player.data.chat_timer = 180
                        self.msg = ""
                        self.msg_typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.msg = self.msg[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.player.movement.stop()
                        self.msg_typing = False
                        self.msg = ""
                    else:
                        if len(self.msg) < 60 and event.unicode.isprintable():
                            self.msg += event.unicode
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.ui.handle_click(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.player.movement.stop()
                    self.map_viewer.run()
                if event.key == pygame.K_ESCAPE:
                    self.player.movement.stop()
                    self.paused = not self.paused

                if not self.paused:
                    self.player.movement.handle_down(event.key)

                if event.key == pygame.K_RETURN and not self.msg_typing:
                    self.msg_typing = True
                    self.msg = ""

                if event.key == pygame.K_SPACE:
                    self.gaming.check_building()

            if event.type == pygame.KEYUP:
                if not self.paused and not self.msg_typing:
                    self.player.movement.handle_up(event.key)
                else:
                    result = self.pause_menu.run()
                    if result == "resume":
                        self.paused = False
                    elif result == "options":
                        self.options_menu.run()
                        self.player.align_immediate()
                        self.player.movement.stop()
                        self.paused = False
                    elif result == "main menu":
                        self.client.disconnect = True  # disconnect client
                        self.player.align_immediate()
                        return "main_menu"
                    elif result == "quit":
                        self.running = False

        return None

    def game_loop(self):
        self.start_networking()
        SoundManager.stop_music()
        SoundManager.play_music(MusicType.Game)
        walking_sound_channel = None
        self.gaming.reset()
        self.player.align_immediate()
        self.player.movement.stop()
        while self.running:
            if self.player.data.ects >= 30:
                self.player.align_immediate()
                WinScreen(self.screen, self.player.data.character).run()
                self.player.reset(PlayerState.IDLE_DOWN, self.player.data.character, self.player.movement.base_movement_speed)
                return "main_menu"
            elif self.player.data.lives == 0:
                self.player.align_immediate()
                GameOver(self.screen, self.player.data.character).run()
                self.player.reset(PlayerState.IDLE_DOWN, self.player.data.character, self.player.movement.base_movement_speed)
                return "main_menu"
            # when server is closed become new server or join another
           #if not self.client.is_connected:
            #    print("connection lost, establishing new one")
           #     self.start_networking()
            self.dt = self.clock.tick(60) / 1000

            result = self.handle_events()
            if result == "main_menu":
                self.player.reset(PlayerState.IDLE_DOWN, self.player.data.character, self.player.movement.base_movement_speed)
                self.player.data.pos_x = self.player.data.pos_x - self.player.data.pos_x % (
                        16 * Constants.MAP_SCALE) + 16 * Constants.MAP_SCALE / 2
                self.player.data.pos_y = self.player.data.pos_y - self.player.data.pos_y % (
                        16 * Constants.MAP_SCALE) + 16 * Constants.MAP_SCALE / 2
                return "main_menu"

            # ui icon click pause menu
            if self.ui.paused:
                self.ui.paused = False
                self.paused = True
                result = self.pause_menu.run()
                if result == "resume":
                    self.paused = False
                elif result == "options":
                    self.player.align_immediate()
                    self.options_menu.run()
                    self.paused = False
                elif result == "main menu":
                    self.player.reset(PlayerState.IDLE_DOWN, self.player.data.character, self.player.data.movement.base_movement_speed)
                    self.player.data.pos_x = self.player.data.pos_x - self.player.data.pos_x % (
                            16 * Constants.MAP_SCALE) + 16 * Constants.MAP_SCALE / 2
                    self.player.data.pos_y = self.player.data.pos_y - self.player.data.pos_y % (
                            16 * Constants.MAP_SCALE) + 16 * Constants.MAP_SCALE / 2
                    return "main_menu"
                elif result == "quit":
                    self.running = False

            if not self.paused:
                # Sprint handling
                if self.player.data.is_sprinting:
                    if self.player.movement.is_moving:
                        self.player.data.stamina -= self.player.data.stamina_drain_rate * self.dt
                        if self.player.data.stamina <= 0:
                            self.player.data.stamina = 0
                            self.player.data.is_sprinting = False
                            self.player.data.movement_speed = self.player.movement.base_movement_speed
                            # self.player.movement._update_movement_changes_speed()
                            self.player.data.stamina_regen_timer = self.player.data.stamina_regen_delay
                else:
                    if self.player.data.stamina < self.player.data.max_stamina:
                        if self.player.data.stamina_regen_timer > 0:
                            self.player.data.stamina_regen_timer -= self.dt
                        else:
                            self.player.data.stamina += self.player.data.stamina_regen_rate * self.dt
                            if self.player.data.stamina > self.player.data.max_stamina:
                                self.player.data.stamina = self.player.data.max_stamina

                self.game_time_seconds -= self.dt * float(self.player.movement.base_movement_speed / 2)  # from conflict

                if self.game_time_seconds < 0:
                    self.game_time_seconds = 0  # time ran out ¯\_(ツ)_/¯
                self.player.movement.move_player(self.map_data.get_collision_rects())

                if self.player.movement.is_moving:  # is the player moving?
                    if walking_sound_channel == None:  # check for null
                        walking_sound_channel = SoundManager.play_effect(SoundEffectType.Walking)
                    elif not walking_sound_channel.get_busy():  # check if the sound is not currently played
                        walking_sound_channel = SoundManager.play_effect(SoundEffectType.Walking)

                self.gaming.update_data()
                self.draw_game(self.dt)   # from conflict

            if self.player.data.chat_timer > 0:
                self.player.data.chat_timer -= 1

        return "quit"

    def run(self):
        while True:
            self.player.reset(PlayerState.IDLE_DOWN, self.player.data.character, self.player.movement.base_movement_speed)
            self.player.movement.stop()
            choice = MainMenu(self.screen).run()
            if choice == "play":
                self.client.disconnect = True  # disconnect client
                self.player.align_immediate()
                self.character_menu.run()
                self.player.reset(PlayerState.IDLE_DOWN, self.player.data.character, self.player.movement.base_movement_speed)
                self.player.movement.stop()
                self.options_menu.player = self.player # I have to update the instance of the player in the options menu - to verify
                self.ui = UI(self.screen, self.options_menu, self.player)
                self.paused = False
                self.game_time_seconds = 600
                result = self.game_loop()
                if result == "quit":
                    break
                elif result == "main_menu":
                    self.player.align_immediate()
                    SoundManager.stop_music()
                    SoundManager.play_music(MusicType.Menu)
                    continue
            elif choice == "options":
                self.player.align_immediate()
                self.options_menu.run()
            elif choice == "quit":
                pygame.quit()
                break


if __name__ == "__main__":
    game = Game()
    game.run()
