import socket
import time
from client_server.common_udp import recv_pickle_udp, send_pickle_udp


class Server:
    def __init__(self, hostname, port_number):
        self.players = {}
        self.last_seen = {}
        self.host = hostname
        self.port = port_number
        self.timeout = 2.0

    def run_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind((self.host, self.port))
        except OSError:
            # if socket is occupied - server is already running
            s.close()
            return

        while True:
            try:
                player, addr = recv_pickle_udp(s)
                now = time.time()

                player.id = addr
                player.clientID = addr
                self.players[addr] = player
                self.last_seen[addr] = now

                to_remove = [a for a, t in self.last_seen.items() if now - t > self.timeout]
                for inactive_addr in to_remove:
                    del self.players[inactive_addr]
                    del self.last_seen[inactive_addr]

                all_players = self.players.copy()
                send_pickle_udp(s, addr, addr)
                send_pickle_udp(s, len(all_players), addr)
                send_pickle_udp(s, all_players, addr)
            except Exception as e:
                print("UDP server error:", e)

            time.sleep(0.05)
