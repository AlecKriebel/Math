#!/usr/bin/env python3
"""Strict publication integrity and replay checks; Python standard library."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
MANIFEST = 'PUBLICATION_MANIFEST.json'
EXPECTED = {
    'README.md', 'PUBLICATION.json', 'verify_publication.py', 'test_integrity.py',
    'packet/CONTROL_RESULTS.json', 'packet/PROOF.md', 'packet/README.md',
    'packet/REPOSITORY_GATE.json', 'packet/RESEARCH_LOG.md',
    'packet/SHA256SUMS.json', 'packet/SOURCE_CHECK.json', 'packet/SOURCE_GATE.md',
    'packet/SOURCE_MANIFEST.json', 'packet/STATUS.json', 'packet/turns.jsonl',
    'packet/verify.py', 'packet/verify_manifest.py',
    'audit/AUDIT.md', 'audit/AUDIT_RESULT.json', 'audit/AUDIT_SHA256SUMS.json',
    'audit/AUDIT_SOURCE_METADATA.json', 'audit/CANDIDATE_MANIFEST_REPLAY.json',
    'audit/CANDIDATE_REPLAY.json', 'audit/CORRECTIONS.md',
    'audit/INDEPENDENT_RESULTS.json', 'audit/INPUT_BINDING.json',
    'audit/verify_audit.py', 'audit/verify_independent.py',
}
FROZEN_MANIFESTS = {
    'packet/SHA256SUMS.json': 'a99e4e28c91d7f51ed116f868a698e2d718fec97a4ee82cf5b94aba409100f98',
    'audit/AUDIT_SHA256SUMS.json': 'b0485e8e9a11aacfb567ad76bfb47614cebb06d4336b845939232c96427b69d3',
}

def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def integrity():
    paths = list(HERE.rglob('*'))
    require(not any(p.is_symlink() for p in paths), 'symlink in publication')
    actual = {p.relative_to(HERE).as_posix() for p in paths if p.is_file()}
    require(actual == EXPECTED | {MANIFEST}, 'publication file set mismatch')
    dirs = {p.relative_to(HERE).as_posix() for p in paths if p.is_dir()}
    require(dirs == {'packet', 'audit'}, 'publication directory set mismatch')
    m = json.loads((HERE / MANIFEST).read_text(), object_pairs_hook=unique_pairs)
    require(type(m) is dict and set(m) == {'schema', 'files'}, 'manifest schema')
    require(m['schema'] == 'math-research-publication-v1', 'manifest version')
    require(type(m['files']) is list and len(m['files']) == len(EXPECTED), 'manifest inventory count')
    names = set()
    for entry in m['files']:
        require(type(entry) is dict and set(entry) == {'path', 'bytes', 'sha256'}, 'entry schema')
        name = entry['path']
        require(type(name) is str, 'path type')
        pure = PurePosixPath(name)
        require(not pure.is_absolute() and name == pure.as_posix() and '..' not in pure.parts
                and '\\' not in name and name in EXPECTED, 'unsafe or unexpected path')
        require(name not in names, 'duplicate manifest entry')
        names.add(name)
        require(type(entry['bytes']) is int and entry['bytes'] >= 0, 'invalid byte count')
        require(type(entry['sha256']) is str and re.fullmatch('[0-9a-f]{64}', entry['sha256']), 'invalid SHA-256')
        data = (HERE / name).read_bytes()
        require(len(data) == entry['bytes'], name + ': byte count mismatch')
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], name + ': SHA-256 mismatch')
    require(names == EXPECTED, 'manifest names mismatch')
    for name, expected in FROZEN_MANIFESTS.items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, 'frozen manifest changed: ' + name)
    return {'integrity': 'PASS', 'manifested_files': len(EXPECTED), 'total_artifact_files': len(EXPECTED) + 1}


def run(script, *args):
    proc = subprocess.run([sys.executable, '-I', str(HERE / script), *args],
                          cwd=HERE, capture_output=True, check=False)
    require(proc.returncode == 0, script + ' failed: ' + proc.stderr.decode(errors='replace'))
    return proc.stdout


def main():
    require(sys.argv[1:] in [[], ['--integrity-only']], 'usage: verify_publication.py [--integrity-only]')
    result = integrity()
    if not sys.argv[1:]:
        author = run('packet/verify.py')
        independent = run('audit/verify_independent.py')
        require(author == (HERE / 'packet/CONTROL_RESULTS.json').read_bytes(), 'author replay output differs')
        require(author == (HERE / 'audit/CANDIDATE_REPLAY.json').read_bytes(), 'audit author replay differs')
        require(independent == (HERE / 'audit/INDEPENDENT_RESULTS.json').read_bytes(), 'independent replay output differs')
        packet_integrity = json.loads(run('packet/verify_manifest.py'))
        audit_integrity = json.loads(run('audit/verify_audit.py', str(HERE / 'packet')))
        result.update(author_assertions=json.loads(author)['exact_assertions'],
                      independent_assertions=json.loads(independent)['independent_assertions'],
                      byte_identical_replays=True,
                      packet_integrity=packet_integrity, audit_integrity=audit_integrity)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
