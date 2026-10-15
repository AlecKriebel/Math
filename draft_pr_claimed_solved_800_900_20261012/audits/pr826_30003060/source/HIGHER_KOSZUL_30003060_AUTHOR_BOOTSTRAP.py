#!/usr/bin/env python3
"""Pinned external integrity gate; archive code is never loaded before full validation."""
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import zipfile

EXPECTED_MANIFEST_SHA256 = "1b54474d1e6b45c176a3ed7cb699c8837a179c9f908ed90df937c2c5c5c1404b"


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def no_duplicates(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, "duplicate JSON key")
        d[k] = v
    return d


def main():
    need(sys.flags.isolated == 1, "run bootstrap with python -I -B")
    need(sys.flags.optimize == 0, "optimized execution rejected")
    need(len(sys.argv) == 3, "usage: bootstrap.py SAFE.zip EXTERNAL_MANIFEST.json")
    archive, manifest_path = map(Path, sys.argv[1:])
    need(archive.is_file() and not archive.is_symlink(), "archive must be a regular non-symlink file")
    need(manifest_path.is_file() and not manifest_path.is_symlink(), "manifest must be a regular non-symlink file")
    mb = manifest_path.read_bytes()
    need(hashlib.sha256(mb).hexdigest() == EXPECTED_MANIFEST_SHA256, "external manifest pin mismatch")
    manifest = json.loads(mb, object_pairs_hook=no_duplicates)
    ab = archive.read_bytes()
    need(len(ab) == manifest['archive']['bytes'], "archive byte count mismatch")
    need(hashlib.sha256(ab).hexdigest() == manifest['archive']['sha256'], "archive SHA-256 mismatch")
    expected = manifest['members']
    payload = {}
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        names = [info.filename for info in infos]
        need(len(names) == len(set(names)), "duplicate ZIP members")
        need(set(names) == set(expected), "exact inventory mismatch")
        for info in infos:
            name = info.filename
            pp = PurePosixPath(name)
            need(not pp.is_absolute() and len(pp.parts) == 1 and name not in ['.', '..']
                 and '\\' not in name and pp.name == name, "unsafe ZIP path")
            need(not info.is_dir() and stat.S_ISREG(info.external_attr >> 16), "nonregular ZIP member")
            need(info.file_size == expected[name]['bytes'], "uncompressed size mismatch")
            data = z.read(info)
            need(hashlib.sha256(data).hexdigest() == expected[name]['sha256'], "member SHA-256 mismatch")
            payload[name] = data
    # AST inspection occurs after integrity, still without import/execution of archive code.
    for name, data in payload.items():
        if name.endswith('.py'):
            ast.parse(data, filename=name)
    with tempfile.TemporaryDirectory(prefix='higher-koszul-verified-') as temp:
        td = Path(temp)
        for name, data in payload.items():
            (td/name).write_bytes(data)
            (td/name).chmod(0o444)
        result = subprocess.run([sys.executable, '-I', '-B', str(td/'verify_free_algebra.py')],
                                cwd=td, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=120, check=False)
        need(result.returncode == 0, "algebra checker failed: " + result.stderr.decode())
        need(result.stdout == payload['RESULTS.json'], "algebra output differs from frozen result")
    print(json.dumps({'status':'PASS','archive_sha256':manifest['archive']['sha256'],
                      'manifest_sha256':EXPECTED_MANIFEST_SHA256,'members_verified':len(payload),
                      'isolated_execution':True,'optimized_execution':False,
                      'results_reproduced_byte_exactly':True,
                      'optional_provenance_rehash':'NOT_RUN_SOURCE_INPUTS_NOT_SUPPLIED',
                      'textual_source_inspection':'NOT_PERFORMED_BY_REPLAY',
                      'mathematical_independent_review':'NOT_PERFORMED_BY_REPLAY'},
                     sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
