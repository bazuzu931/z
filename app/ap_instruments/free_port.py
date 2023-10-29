import socket
from contextlib import closing
from rich.console import Console

cp = Console().print

def get_free_port():
	with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
		# s.bind(('', 0))
		s.bind(('localhost', 0))
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		free_port = s.getsockname()[1]
		print('Free port: ', free_port)
		return free_port

# print(get_free_port())