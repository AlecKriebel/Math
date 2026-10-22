#!/usr/bin/env python3
"""Observe optimization while executing unchanged frozen code in a copy."""
import json
import runpy
import subprocess
import sys

original_run = subprocess.run


def observed_run(command, *args, **kwargs):
    if type(command) is list and len(command) > 1 and command[1].endswith('.py'):
        probe = original_run([command[0], '-c', 'import sys;print(sys.flags.optimize)'],
                             cwd=kwargs.get('cwd'), env=kwargs.get('env'),
                             capture_output=True, text=True, timeout=5)
        print(json.dumps({'observation': 'child_optimization', 'script': command[1],
                          'optimize': int(probe.stdout.strip()), 'arguments': command[1:]}), file=sys.stderr)
    return original_run(command, *args, **kwargs)


subprocess.run = observed_run
script = sys.argv[1]
sys.argv = sys.argv[1:]
print(json.dumps({'observation': 'parent_optimization', 'optimize': sys.flags.optimize,
                  'script': script}), file=sys.stderr)
runpy.run_path(script, run_name='__main__')
