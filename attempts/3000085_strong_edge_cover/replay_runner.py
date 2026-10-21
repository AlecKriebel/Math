"""Run local regression with socket audit events rejected, without creating sockets."""
import runpy
import sys

def deny_socket(event, args):
    if event.startswith('socket.'):
        raise RuntimeError('Socket activity forbidden')

sys.addaudithook(deny_socket)
try:
    sys.audit('socket.frozen_regression_selftest')
except RuntimeError as exc:
    if str(exc) != 'Socket activity forbidden':
        raise
else:
    raise RuntimeError('Socket audit guard failed')
runpy.run_path(sys.argv[1], run_name='__main__')
