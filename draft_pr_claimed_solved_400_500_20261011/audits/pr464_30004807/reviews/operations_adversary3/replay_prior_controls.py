#!/usr/bin/env python3
"""Reviewer-3 replays of unchanged prior controls, with private output roots.

These are disclosed replays, distinct from the new reviewer-written controls.
Neither original control summaries nor reviewed candidate files are written.
"""
import hashlib
import importlib.util
import json
import socket
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
REPO = AUDIT.parents[2]
sys.path.insert(0, str(AUDIT / 'operations'))

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    private = HERE / 'private_cases'
    private.mkdir(exist_ok=True)
    suffix = 'NORMAL' if __debug__ else 'OPTIMIZED'
    paths = [('PREPARER', AUDIT / 'operations/check_operations.py', 'OPERATIONS', 158),
             ('SEALED_ROUND2', AUDIT / 'reviews/operations_adversary2/independent_controls.py', 'HERE', 160)]
    records = []
    calls = []
    def denied(*args, **kwargs):
        calls.append('unmocked service boundary')
        raise RuntimeError('REAL SERVICE BOUNDARY DENIED')
    for label, path, root_name, expected in paths:
        source_sha = sha(path.read_bytes())
        mod = load(path, 'review3_replay_' + label.lower())
        with tempfile.TemporaryDirectory(prefix='replay_', dir=private) as directory:
            output_root = Path(directory).resolve()
            with patch.object(mod, root_name, output_root), patch.object(socket, 'create_connection', denied), \
                 patch.object(mod.c.subprocess, 'run', denied):
                mod.main()
            output_name = ('OFFLINE_CONTROLS_' if label == 'PREPARER' else 'INDEPENDENT_CONTROLS_') + suffix + '.json'
            data = (output_root / output_name).read_bytes()
            result = json.loads(data)
            require(result.get('case_count') == expected and result.get('all_passed') is True,
                    'Unmodified control replay failed: ' + label)
            require(result.get('real_external_calls') == 0, 'Control replay escaped isolation')
            require(sha(path.read_bytes()) == source_sha, 'Prior source was modified')
            (HERE / (label + '_REPLAY_' + suffix + '.json')).write_bytes(data)
            records.append({'source': path.relative_to(AUDIT).as_posix(), 'source_sha256': source_sha,
                            'case_count': expected, 'all_passed': True, 'result_sha256': sha(data)})
    require(not calls, 'Real service call attempted')
    summary = {'replay_only': True, 'reviewer': '/root/pr464_operations_adversary3',
               'all_passed': True, 'real_external_calls': 0, 'sources': records,
               'independent_new_controls_are_separate': True}
    (HERE / ('PRIOR_REPLAY_RECEIPT_' + suffix + '.json')).write_bytes(mod.c.json_bytes(summary))
    print(json.dumps({'all_passed': True, 'replayed_cases': sum(x['case_count'] for x in records),
                      'real_external_calls': 0}, sort_keys=True))

if __name__ == '__main__':
    main()
