#!/usr/bin/env python3
"""Authenticate and replay the qualified double-permutation publication."""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).absolute().parent
ARCHIVES = {
    'DOUBLE_PERMUTATION_30001054_SCOPE_CORRECTION_AUDIT_REBUILT.zip': ('audit', 20762, 'ad0e79032522c72ee0015336e11f53f2a58c66fa1b5be17478d72f0f4416edba', 14),
    'DOUBLE_PERMUTATION_30001054_FRESH_ADVERSARIAL_REVIEW.zip': ('review', 9942, 'a4859fd8373aceba5a980b1076502120dc75ae405b2d544397492973cd85f092', 7),
}

def require(value, message):
    if not value:
        raise ValueError(message)

def digest(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate key: ' + key)
        result[key] = value
    return result

def read_json(path):
    def reject(value):
        raise ValueError('nonfinite JSON constant: ' + value)
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=reject)

def run(root, relative, optimized):
    command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(root / relative)]
    proc = subprocess.run(command, cwd='/', text=True, capture_output=True)
    require(proc.returncode == 0, relative + ': ' + proc.stderr)
    return json.loads(proc.stdout, object_pairs_hook=unique)

def verify(root, pin):
    require(root.is_dir() and not root.is_symlink(), 'invalid root')
    manifest_path = root / 'PUBLICATION_MANIFEST.json'
    require(len(pin) == 64 and all(c in '0123456789abcdef' for c in pin), 'invalid external manifest pin')
    require(hashlib.sha256(manifest_path.read_bytes()).hexdigest() == pin, 'external manifest pin mismatch')
    manifest = read_json(manifest_path)
    require(type(manifest) is dict and set(manifest) == {'schema', 'files'}, 'invalid manifest shape')
    require(type(manifest['schema']) is int and manifest['schema'] == 1, 'invalid manifest schema')
    files = manifest['files']
    require(type(files) is dict, 'invalid file inventory')
    expected = set(files) | {'PUBLICATION_MANIFEST.json'}
    require(all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts for n in expected), 'unsafe member name')
    entries = list(root.rglob('*'))
    require(not any(p.is_symlink() for p in entries), 'symlink member')
    actual = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    require(actual == expected, 'missing or unexpected file')
    dirs = {str(p) for n in expected for p in pathlib.PurePosixPath(n).parents if str(p) != '.'}
    require({p.relative_to(root).as_posix() for p in entries if p.is_dir()} == dirs, 'unexpected directory')
    require(all(p.is_file() or p.is_dir() for p in entries), 'nonregular member')
    for name, record in files.items():
        require(type(record) is dict and set(record) == {'bytes', 'sha256'} and type(record['bytes']) is int, 'invalid file record')
        require(digest((root / name).read_bytes()) == record, 'content mismatch: ' + name)
    inventories = read_json(root / 'ARCHIVE_INVENTORY.json')
    require(set(inventories) == set(ARCHIVES), 'wrong archive inventory')
    for name, (folder, size, sha, count) in ARCHIVES.items():
        path = root / 'archives' / name
        require(digest(path.read_bytes()) == {'bytes': size, 'sha256': sha}, 'archive pin mismatch: ' + name)
        with zipfile.ZipFile(path) as z:
            members = z.infolist()
            names = [m.filename for m in members]
            require(len(members) == count and len(set(names)) == count, 'wrong or duplicate archive members')
            require(all('/' not in n and '\\' not in n and n not in ('.', '..') for n in names), 'unsafe archive member')
            require(set(names) == {p.name for p in (root / folder).iterdir()}, 'extracted inventory mismatch')
            got = {}
            for member in members:
                data = z.read(member)
                require(data == (root / folder / member.filename).read_bytes(), 'extracted bytes mismatch: ' + member.filename)
                got[member.filename] = digest(data)
            require(got == inventories[name], 'archive member receipt mismatch')
    verdict = read_json(root / 'VERDICT.json')
    require(verdict['effective_gate'] == 'ACCEPT_COUNTEREXAMPLE_WITH_SCOPE_ADDENDUM', 'wrong operative gate')
    require(verdict['status'] == 'claimed_solved' and verdict['turns'] == '1/5', 'wrong queue scope')
    require(verdict['literal_four_axiom_statement'] == 'FALSE_BY_FINITE_WITNESS', 'wrong literal scope')
    require(verdict['intended_switch_once_fibration_problem'] == 'SOLVED_IN_LITERATURE_AFFIRMATIVE', 'missing historical credit')
    require(verdict['normalized_polygonal_request'] == 'NOT_REFUTED; FULLY_SEPARATED_START_FORCES_SWITCH_ONCE', 'missing normalized restriction')
    require(verdict['mandatory_addendum'] == 'review/PUBLICATION_ADDENDUM.md', 'missing mandatory addendum')
    for key in ['original_author_archive_available', 'original_author_archive_currently_replayed', 'original_corpora_currently_recertified', 'novelty_claimed', 'independent_full_representation_proof_claimed', 'euclidean_stretchability_claimed', 'polygonal_construction_claimed', 'human_peer_review_claimed']:
        require(verdict[key] is False, 'unsupported claim: ' + key)
    review = read_json(root / 'review/REVIEW_CERTIFICATE.json')
    require(review['verdict'] == verdict['effective_gate'], 'review gate differs')
    expected_independent = read_json(root / 'review/INDEPENDENT_RESULTS.json')
    checks = []
    for optimized in (False, True):
        mode = 'optimized' if optimized else 'normal'
        witness = run(root, 'audit/witness_check.py', optimized)
        require(witness == read_json(root / 'audit/WITNESS_RESULT.json'), 'witness result differs')
        audit = run(root, 'audit/verify_audit.py', optimized)
        require(audit['result'] == 'PASS_AUDIT_INTEGRITY_AND_WITNESS' and audit['audit_gate'] == 'NEEDS_SCOPE_CORRECTION', 'audit gate rewritten')
        cli = run(root, 'audit/test_witness.py', optimized)
        require(cli['result'] == 'PASS' and cli['cli_control_count'] == 44, 'CLI controls differ')
        integrity = run(root, 'audit/test_integrity.py', optimized)
        require(integrity['result'] == 'PASS' and integrity['count'] == 24, 'integrity controls differ')
        independent = run(root, 'review/independent_check.py', optimized)
        require(independent == expected_independent, 'independent enumeration differs')
        require(independent['rooted_word_counts'] == {'primitive_weak_words':48, 'switch_once_words':16, 'non_switch_once_words':32, 'zero_separating_words':32, 'words_with_fully_separated_term':16, 'non_switch_once_with_fully_separated_term':0}, 'wrong exhaustive counts')
        checks.append({'mode': mode, 'cli_controls': 44, 'integrity_controls': 24, 'independent_half_words': 1296, 'rooted_weak_words': 48, 'switch_once_words': 16, 'non_switch_once_words': 32})
    return {'result': 'PASS', 'effective_gate': verdict['effective_gate'], 'files_verified': len(expected), 'archives_verified': 2, 'archive_member_counts': [14, 7], 'replays': checks, 'author_archive_replayed': False, 'source_PDFs_replayed_by_this_wrapper': False, 'representation_theorem_proved_by_code': False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=pathlib.Path, default=ROOT)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    try:
        result = verify(args.root.absolute(), args.manifest_sha256)
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
