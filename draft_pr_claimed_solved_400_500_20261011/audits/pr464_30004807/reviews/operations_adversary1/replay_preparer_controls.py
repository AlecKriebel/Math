#!/usr/bin/env python3
"""Run the existing controls while relocating every output into this review."""
import json
import socket
import sys
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'operations'))
import check_operations as controls
import common


def deny(*args, **kwargs):
    raise RuntimeError('Independent offline isolation blocked a real service')


def main():
    controls.OPERATIONS = HERE
    with patch.object(socket, 'socket', side_effect=deny), \
         patch.object(common.subprocess, 'run', side_effect=deny):
        controls.main()
    suffix = 'NORMAL' if __debug__ else 'OPTIMIZED'
    generated = HERE / ('OFFLINE_CONTROLS_' + suffix + '.json')
    obj = json.loads(generated.read_text())
    common.require(obj.get('all_passed') is True and type(obj.get('case_count')) is int
                   and obj['case_count'] == 127 and len(obj.get('cases', [])) == 127,
                   'Existing controls did not execute all 127 expected cases')
    common.require(type(obj.get('real_external_calls')) is int and obj['real_external_calls'] == 0
                   and all(x.get('passed') is True and type(x.get('real_external_calls')) is int
                           and x['real_external_calls'] == 0 for x in obj['cases']),
                   'Existing controls contain missing, false, or nonzero call evidence')
    generated.rename(HERE / ('PREPARER_REPLAY_' + suffix + '.json'))


if __name__ == '__main__':
    main()
