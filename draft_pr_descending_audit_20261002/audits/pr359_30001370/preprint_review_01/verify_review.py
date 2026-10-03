#!/usr/bin/env python3
"""Read-only, standard-library review custody verifier; never executes payloads."""
import argparse
import hashlib
import json
import pathlib
import stat
import sys

CONTAINERS = {'PUBLIC_MANIFEST.json', 'PRIVATE_MANIFEST.json', 'CLOSURE.json'}

def require(value, message):
    if not value:
        raise ValueError(message)

def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result

def read(path):
    return json.loads(path.read_bytes(), object_pairs_hook=pairs)

def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def safe_name(name):
    require(isinstance(name, str) and name != '', 'invalid path')
    path = pathlib.PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts
            and str(path) == name and '\\' not in name, 'unsafe path: ' + name)
    return name

def inventory(root):
    result = set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'symlink: ' + str(path))
        require(path.is_file() or path.is_dir(), 'nonregular payload: ' + str(path))
        if path.is_file():
            result.add(str(path.relative_to(root)))
    return result

def verify(root, public_only=False, diagnostic_fixture=False):
    root = root.resolve()
    closure = read(root / 'CLOSURE.json')
    require(closure['schema'] == 1, 'closure schema')
    if diagnostic_fixture:
        require(closure['status'] == 'DIAGNOSTIC_FIXTURE' and closure['closed'] is False,
                'fixture is not a closed review')
    else:
        require(closure['status'] == 'CLOSED' and closure['closed'] is True,
                'review is not closed')
    manifests = {}
    for name in ['PUBLIC_MANIFEST.json', 'PRIVATE_MANIFEST.json']:
        require(identity((root / name).read_bytes()) == closure['manifest_bindings'][name],
                'manifest binding: ' + name)
        obj = read(root / name)
        require(obj['schema'] == 1, 'manifest schema')
        rows = obj['files']
        names = [safe_name(row['path']) for row in rows]
        require(len(names) == len(set(names)), 'duplicate manifest path')
        require(not set(names) & CONTAINERS, 'container self inclusion')
        manifests[name] = {row['path']: row for row in rows}
    public = manifests['PUBLIC_MANIFEST.json']
    private = manifests['PRIVATE_MANIFEST.json']
    require(not public.keys() & private.keys(), 'overlapping public/private inventory')
    actual = inventory(root)
    all_names = set(public) | set(private) | CONTAINERS
    require(actual <= all_names, 'undeclared files: ' + repr(sorted(actual - all_names)))
    require(set(public) | CONTAINERS <= actual, 'missing public files/containers')
    if not public_only:
        require(actual == all_names, 'missing private files')
    for name, row in {**public, **({} if public_only else private)}.items():
        path = root / name
        require(identity(path.read_bytes()) == {k: row[k] for k in ['bytes', 'sha256']},
                'payload identity: ' + name)
        require(stat.S_IMODE(path.stat().st_mode) == row['mode'], 'payload mode: ' + name)
    plan = read(root / 'PUBLIC_PLAN.json')
    require(set(plan['public_payload_paths']) == set(public), 'public plan mismatch')
    if not diagnostic_fixture:
        require('ROOT_APPROVAL.json' in private, 'missing private root approval')
        if not public_only:
            approval = read(root / 'ROOT_APPROVAL.json')
            require(approval['authorized_one_shot_closure'] is True, 'root authorization absent')
            require(identity((root / 'ROOT_APPROVAL.json').read_bytes()) == closure['approval_binding'],
                    'approval binding')
            for name, pin in closure['current_submission_pins'].items():
                require(identity((root / 'current_submission_private/kit' / safe_name(name)).read_bytes()) == pin,
                        'final submission pin: ' + name)
            for name in sorted(private):
                if name.startswith('native_runs/') and name.endswith('/record.json'):
                    receipt_path = root / name
                    receipt = read(receipt_path)
                    for stream in ['stdout', 'stderr']:
                        require(identity((receipt_path.parent / (stream + '.bin')).read_bytes()) == receipt[stream],
                                'native stream: ' + name + '/' + stream)
                    require(isinstance(receipt['argv'], list) and bool(receipt['argv']), 'native argv')
                    require(receipt['finished_utc'] >= receipt['started_utc'], 'native time order')
            # Imported root receipts remain exact files. Their source schema and
            # Git/API contents were checked by check_captured_api.py, not replayed.
    return {'status': 'PASS', 'closed_review': not diagnostic_fixture,
            'public_payloads_checked': len(public),
            'private_payloads_checked': 0 if public_only else len(private),
            'private_payloads_declared': len(private),
            'private_scope': 'not checked' if public_only else 'full local custody checked',
            'scope': 'Byte/mode/inventory and native-stream custody; no proof evaluation, program execution, source download or publication action.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent)
    parser.add_argument('--public-only', action='store_true')
    parser.add_argument('--diagnostic-fixture', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.root, args.public_only, args.diagnostic_fixture), indent=2))
    except (ValueError, KeyError, OSError, TypeError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
