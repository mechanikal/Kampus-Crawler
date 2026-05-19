import socket
import threading
# calling absolute path so import works from main as well
from client_server.common import recv_pickle, send_pickle
import time


class Server:
    def __init__(self, hostname, port_number):
        self.numberOfClients = 0
        self.clients = {}
        self.players = {}
        self.lock = threading.Lock()
        self.host = hostname
        self.port = port_number

    def handle_client(self, conn, player_id):
        try:
            while True:
                # get pickled player
                player = recv_pickle(conn)
                player.id = player_id
                if player is None:
                    # Client disconnected
                    break
                with self.lock:
                    send_pickle(conn, player_id)
                with self.lock:
                    self.players[player_id] = player
                # send player number to all players
                with self.lock:
                    send_pickle(conn, self.numberOfClients)
                # send player data to all players
                with self.lock:
                    send_pickle(conn, self.players)
                # wait a bit so the cpu isn't working at full capacity | higher value may cause lag
                time.sleep(0.005)
        finally:
            # if the connection is lost delete player from dict
            with self.lock:
                if player_id in self.clients:
                    del self.clients[player_id]
                if player_id in self.players:
                    del self.players[player_id]
                self.numberOfClients -= 1
            conn.close()

    def run_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.host, self.port))
        except OSError:
            # if socket is occupied - server is already running
            s.close()
            return
        s.listen()
        player_id = 0
        while True:
            # wait for client to connect
            conn, addr = s.accept()
            self.numberOfClients += 1
            with self.lock:
                self.clients[player_id] = conn
            threading.Thread(target=self.handle_client, args=(conn, player_id), daemon=True).start()
            player_id += 1