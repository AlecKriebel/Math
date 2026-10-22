import sys
def deny_network(event,args):
    if event in {'socket.connect','socket.connect_ex','socket.getaddrinfo','socket.bind'}:
        raise RuntimeError('Network access disabled for offline package replay')
sys.addaudithook(deny_network)
