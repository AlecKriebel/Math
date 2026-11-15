"""Pure closed default custody. No project imports, subprocess, network or writes."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
TERMINALS = {'MANIFEST.json', 'SEAL.json'}


def read(path):
    if not path.is_file() or path.is_symlink() or path.resolve() != path:
        raise ValueError('not a real regular file: ' + str(path))
    return path.read_bytes()


def digest(path):
    return hashlib.sha256(read(path)).hexdigest()


def main():
    if sys.argv[1:]:
        raise ValueError('pure default closure accepts no options')
    seal = json.loads(read(ROOT / 'SEAL.json'))
    if digest(ROOT / 'MANIFEST.json') != seal['MANIFEST_SHA256']:
        raise ValueError('manifest mismatch')
    manifest = json.loads(read(ROOT / 'MANIFEST.json'))
    expected = set()
    for row in manifest['files']:
        rel = PurePosixPath(row['path'])
        if rel.is_absolute() or '..' in rel.parts or str(rel) != row['path']:
            raise ValueError('unsafe owned path')
        expected.add(row['path'])
        body = read(ROOT / rel)
        if len(body) != row['bytes'] or hashlib.sha256(body).hexdigest() != row['SHA256']:
            raise ValueError('owned mismatch')
    paths = list(ROOT.rglob('*'))
    if any(p.is_symlink() or not (p.is_file() or p.is_dir()) for p in paths):
        raise ValueError('nonordinary owned namespace')
    actual = {p.relative_to(ROOT).as_posix() for p in paths if p.is_file()} - TERMINALS
    directories = sorted(p.relative_to(ROOT).as_posix() for p in paths if p.is_dir())
    if (actual != expected or len(expected) != len(manifest['files'])
            or directories != manifest['exact_relative_directories']):
        raise ValueError('closed extent mismatch')
    bindings = json.loads(read(ROOT / 'INPUT_BINDINGS.json'))
    for row in bindings['static_recheck_bindings']:
        body = read(Path(row['path']))
        if len(body) != row['bytes'] or hashlib.sha256(body).hexdigest() != row['SHA256']:
            raise ValueError('audited static input changed: ' + row['path'])
    controls = json.loads(read(ROOT / 'CONTROL_RESULTS.json'))
    if controls['status'] != 'PASS_INDEPENDENT_ISOLATED_V2_CONTROLS' or not all(controls['results'].values()):
        raise ValueError('independent controls mismatch')
    comparison = json.loads(read(ROOT / 'INDEPENDENT_COMPARISON.json'))
    if comparison['status'] != 'PASS_ACTUAL_COMPLETE_DIFF_AND_ALL_CODE_PINS':
        raise ValueError('code comparison mismatch')
    pure = json.loads(read(ROOT / 'PREPARATION_CUSTODY_RESULT.json'))
    fresh = json.loads(read(ROOT / 'FRESH_PREFLIGHT.json'))
    if (pure['status'] != 'PREPARATION_CUSTODY_PASS' or pure['owned_payload_count'] != 23
            or fresh['status'] != 'PASS_READ_ONLY_EXACT11_PREFLIGHT'
            or fresh['stage_and_website']['actual_counts'] != [605, 90, 91]
            or fresh['Git']['index_record_count'] != 58545
            or fresh['Git']['protected_record_count'] != 58543):
        raise ValueError('custody/baseline observation mismatch')
    print(json.dumps({'status': 'PASS_PURE_CLOSED_EXACT11_V2_SAFETY_AUDIT_CUSTODY',
                      'verdict': 'PASS_UNDER_STATED_STABLE_NAMESPACE_ASSUMPTIONS',
                      'owned_payloads': len(expected), 'static_bindings': len(bindings['static_recheck_bindings']),
                      'installation_or_publication_authorized': False,
                      'project_imports_network_subprocess_or_writes': False}, sort_keys=True))


if __name__ == '__main__':
    main()
