#!/usr/bin/env python3
"""All-29 fixed-snapshot gate for a frozen entry point. Bootstrap via public map."""
import argparse
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).absolute().parent
SNAPSHOT_PIN = 'f05112fa43eb99a0c9cd4687b14beeef5eb4d190dcebae9b15c1d84c9acc656f'
spec = importlib.util.spec_from_file_location('packet_guard', HERE/'PACKET_GUARD.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', required=True)
    p.add_argument('--entrypoint', required=True, choices=['public/controls.py', 'public/verify_packet.py',
                   'PORTABLE_INDEPENDENT.py', 'VERIFY_PUBLICATION.py', 'TEST_MUTATIONS.py', 'audit_b/independent_controls.py'])
    p.add_argument('arguments', nargs=argparse.REMAINDER)
    args = p.parse_args()
    try:
        snapshot = g.load_snapshot(HERE/'PINNED_SNAPSHOT.json', SNAPSHOT_PIN)
        before = g.authenticate(args.packet, snapshot)
        env = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        tail = args.arguments[1:] if args.arguments[:1] == ['--'] else args.arguments
        cp = subprocess.run([sys.executable, '-I', '-B', str(Path(args.packet)/args.entrypoint), *tail],
                            cwd=Path(args.packet).parent, env=env, capture_output=True, timeout=240)
        g.need(g.typed_equal(before, g.authenticate(args.packet, snapshot)), 'packet changed during execution')
        sys.stdout.buffer.write(cp.stdout)
        sys.stderr.buffer.write(cp.stderr)
        return cp.returncode
    except (g.Rejected, OSError, subprocess.SubprocessError) as error:
        print('GUARD_REJECT: ' + str(error), file=sys.stderr)
        return 42


if __name__ == '__main__':
    raise SystemExit(main())
