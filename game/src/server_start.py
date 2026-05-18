# script to run server locally
from client_server.server_udp import Server
from constants import Constants

server = Server('0.0.0.0', Constants.SERVER_PORT)
server.run_server()