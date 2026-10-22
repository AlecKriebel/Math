#!/usr/bin/env python3
"""Closed-file-set, immutable-packet and exact replay verification; offline."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parent
PINS = {'author': 'e2645129ee536f33d58415f04b45323c816ffb3706ef02101e78de2172049180',
        'independent_audit': '7525f8f0203e8ca40846e8a2490eefbab944d1d100064fa3eaf4329c32772bf3'}
STATUS_PIN = 'b6481083f54016240f03fae5784a71b4f9c27da7c608e759f3761c17900c77fc'
TOP = {'README.md', 'PUBLICATION_STATUS.json', 'PUBLICATION_MANIFEST.json', 'verify_publication.py'}


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def metadata(path):
    blob = path.read_bytes()
    return {'bytes': len(blob), 'sha256': sha(blob)}


def verify_files():
    manifests = {}
    expected = set(TOP)
    for directory, pin in PINS.items():
        folder = ROOT / directory
        need(folder.is_dir() and not folder.is_symlink(), 'bad packet directory')
        path = folder / 'MANIFEST.json'
        need(path.is_file() and not path.is_symlink(), 'bad packet manifest')
        blob = path.read_bytes()
        need(sha(blob) == pin, directory + ' manifest anchor mismatch')
        doc = json.loads(blob)
        need(doc.get('schema') == 1 and isinstance(doc['files'], dict), 'manifest schema')
        expected.add(directory + '/MANIFEST.json')
        for name, entry in doc['files'].items():
            need(name == Path(name).name and name not in ('', '.', '..', 'MANIFEST.json'), 'unsafe path')
            path = folder / name
            need(path.is_file() and not path.is_symlink(), 'missing or linked payload')
            need(metadata(path) == entry, directory + '/' + name + ' metadata mismatch')
            expected.add(directory + '/' + name)
        manifests[directory] = doc
    observed = set()
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT).as_posix()
        need(not path.is_symlink(), 'symlink forbidden')
        if path.is_dir():
            need(relative in PINS, 'unexpected directory')
        else:
            need(path.is_file(), 'nonregular entry')
            observed.add(relative)
    need(observed == expected, 'publication file set mismatch')
    outer = json.loads((ROOT / 'PUBLICATION_MANIFEST.json').read_bytes())
    need(outer.get('schema') == 1, 'outer schema')
    need(set(outer['files']) == expected - {'PUBLICATION_MANIFEST.json'}, 'outer file set')
    for name, entry in outer['files'].items():
        need(metadata(ROOT / name) == entry, 'publication metadata mismatch: ' + name)
    need(sha((ROOT / 'PUBLICATION_STATUS.json').read_bytes()) == STATUS_PIN, 'status anchor mismatch')
    status = json.loads((ROOT / 'PUBLICATION_STATUS.json').read_bytes())
    need(status['queue_status'] == 'unsolved' and status['turns'] == '1/5', 'status/turns')
    need(status['whole_problem_solved'] is False and status['novelty_claimed'] is False, 'scope promotion')
    binding = json.loads((ROOT / 'independent_audit/INPUT_BINDING.json').read_bytes())
    need(binding['manifest_sha256'] == PINS['author'], 'audit manifest binding')
    need(binding['payload_files'] == manifests['author']['files'], 'audit payload binding')
    need(binding['manifest_bytes'] == (ROOT / 'author/MANIFEST.json').stat().st_size, 'manifest size binding')
    need(binding['payload_count'] == 10 and binding['total_payload_bytes'] == 23472, 'payload totals')
    return {'files': len(expected), 'author_manifest_sha256': PINS['author'],
            'audit_manifest_sha256': PINS['independent_audit']}


def run(relative, optimized=False, args=()):
    command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(ROOT / relative)] + list(args)
    env = dict(os.environ, PYTHONOPTIMIZE='0', PYTHONDONTWRITEBYTECODE='1')
    result = subprocess.run(command, env=env, capture_output=True)
    need(result.returncode == 0, relative + ': ' + result.stderr.decode('utf-8', 'replace'))
    need(not result.stderr, 'unexpected stderr')
    return result.stdout


def main():
    integrity = verify_files()
    replay = []
    expected_audit = (ROOT / 'independent_audit/EXACT_RESULTS.json').read_bytes()
    results = {}
    for script in ('verify_manifest.py', 'exact_checks.py', 'negative_controls.py'):
        outputs = [run('author/' + script, mode) for mode in (False, True)]
        need(outputs[0] == outputs[1], 'normal/optimized mismatch: ' + script)
        results[script] = json.loads(outputs[0])
        replay.append({'program': 'author/' + script, 'normal': 'passed', 'optimized': 'passed'})
    need(results['exact_checks.py'] == {'checks': 172, 'matching_optimum': '3/10000',
        'matchings_exhausted': 15, 'tour_optimum': '41839/5000', 'tours_exhausted': 60}, 'author exact result')
    need(results['negative_controls.py']['negative_controls_passed'] == 8, 'author negatives')
    outputs = [run('independent_audit/audit_exact.py', mode, (str(ROOT / 'author'),)) for mode in (False, True)]
    need(outputs[0] == outputs[1] == expected_audit, 'independent result bytes differ')
    independent = json.loads(outputs[0])
    need(independent['negative_controls']['rejected_count'] == 15, 'independent negatives')
    need(independent['input_unchanged'] and independent['result'] == 'PASS_SCOPED_PARTIAL_COUNTEREXAMPLE', 'audit verdict')
    replay.append({'program': 'independent_audit/audit_exact.py', 'normal': 'passed', 'optimized': 'passed', 'stored_result_byte_equal': True})
    need(verify_files() == integrity, 'packet changed in replay')
    print(json.dumps({'result': 'PASS_SCOPED_PARTIAL_COUNTEREXAMPLE', 'integrity': integrity,
        'queue_status': 'unsolved', 'turns': '1/5', 'whole_problem_solved': False,
        'author_checks': 172, 'author_negative_controls': 8, 'independent_negative_controls': 15,
        'tour_optimum': '41839/5000', 'matching_minimum': '3/10000', 'replay': replay}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
