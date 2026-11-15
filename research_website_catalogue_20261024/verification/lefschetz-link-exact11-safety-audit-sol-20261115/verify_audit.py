"""Pure default audit custody: standard library, no project imports/subprocess/network/writes."""
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
        raise ValueError('default pure closure accepts no options')
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
            raise ValueError('owned bytes mismatch')
    # Root requested a later v2 review in this one exact child namespace.
    # It is a separate sealed effort, not part of the immutable original audit.
    paths = [p for p in ROOT.rglob('*') if p.relative_to(ROOT).parts[0] != 'revisions']
    if any(path.is_symlink() or not (path.is_file() or path.is_dir()) for path in paths):
        raise ValueError('nonordinary owned namespace')
    actual = {p.relative_to(ROOT).as_posix() for p in paths if p.is_file()} - TERMINALS
    if actual != expected or len(expected) != len(manifest['files']):
        raise ValueError('owned extent mismatch')
    bindings = json.loads(read(ROOT / 'INPUT_BINDINGS.json'))
    for row in bindings['static_recheck_bindings']:
        body = read(Path(row['path']))
        if len(body) != row['bytes'] or hashlib.sha256(body).hexdigest() != row['SHA256']:
            raise ValueError('audited static input changed: ' + row['path'])
    controls = json.loads(read(ROOT / 'CONTROL_RESULTS.json'))
    if controls['status'] != 'PASS_ISOLATED_AUDIT_CONTROLS' or not all(controls['results'].values()):
        raise ValueError('isolated controls did not pass')
    fresh = json.loads(read(ROOT / 'FRESH_PREFLIGHT.json'))
    if (fresh['status'] != 'PASS_READ_ONLY_EXACT11_PREFLIGHT'
            or fresh['stage_and_website']['actual_counts'] != [605, 90, 91]
            or fresh['Git']['index_record_count'] != 58545
            or fresh['Git']['protected_record_count'] != 58543):
        raise ValueError('fresh observation mismatch')
    print(json.dumps({'status': 'PASS_PURE_EXACT11_SAFETY_AUDIT_CUSTODY',
                      'verdict': 'QUALIFIED_STABLE_LOCAL_NAMESPACES_ONLY',
                      'owned_payloads': len(expected), 'static_bindings': len(bindings['static_recheck_bindings']),
                      'installation_or_publication_authorized': False,
                      'network_subprocess_project_imports_or_writes': False}, sort_keys=True))


if __name__ == '__main__':
    main()
