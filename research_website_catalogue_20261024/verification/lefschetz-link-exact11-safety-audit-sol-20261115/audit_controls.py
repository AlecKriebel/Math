"""Small isolated controls. Never import/run installer, invoke Git, or touch real targets."""
from pathlib import Path
import ast
import hashlib
import json
import os
import struct
import tempfile

HERE = Path(__file__).resolve().parent
PREP = HERE.parent / 'lefschetz-link-production-integration-preparation-sol-20261115'


def extracted(name, env):
    tree = ast.parse((PREP / 'exact11_lib.py').read_text())
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(body) == 1
    exec(compile(ast.Module(body=body, type_ignores=[]), str(PREP / 'exact11_lib.py'), 'exec'), env)
    return env[name]


def need(value, reason):
    if not value:
        raise RuntimeError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    results = {}
    with tempfile.TemporaryDirectory(prefix='isolated-', dir=HERE) as temporary:
        root = Path(temporary)
        source, destination = root / 'new-buffer', root / 'leaf'
        source.write_bytes(b'new')
        destination.write_bytes(b'old')
        try:
            os.link(source, destination, follow_symlinks=False)
        except FileExistsError:
            pass
        else:
            raise AssertionError('no-clobber link unexpectedly overwrote destination')
        assert destination.read_bytes() == b'old'
        results['no_clobber_leaf_preserves_existing_bytes'] = True

        # Reproduce the exact pin-then-replace window, without running the installer.
        aggregate, new = root / 'aggregate', root / 'aggregate-new'
        aggregate.write_bytes(b'baseline')
        new.write_bytes(b'approved')
        assert aggregate.read_bytes() == b'baseline'
        aggregate.write_bytes(b'concurrent-edit')
        os.replace(new, aggregate)
        assert aggregate.read_bytes() == b'approved'
        results['aggregate_concurrent_edit_overwritten_after_check'] = True

        # .approved is a mutable pathname between parse/check and replacement.
        alternate, shared = root / 'approved-copy', root / 'shared-target'
        alternate.write_bytes(b'checked-index-buffer')
        validated = alternate.read_bytes()
        assert validated == b'checked-index-buffer'
        alternate.write_bytes(b'changed-after-validation')
        with alternate.open('rb') as stream:
            os.fsync(stream.fileno())
        os.replace(alternate, shared)
        assert shared.read_bytes() != validated
        results['mutable_alternate_can_differ_from_validated_buffer'] = True

        # Path.stat follows a substituted symlink. The inode comparison alone
        # consequently does not identify the actual directory entry as the lock.
        lock, retained = root / 'index.lock', root / 'retained-own-inode'
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        try:
            owned = os.fstat(fd)
            os.link(lock, retained)
            lock.unlink()
            lock.symlink_to(retained)
            current = lock.stat()
            follows = (current.st_dev, current.st_ino) == (owned.st_dev, owned.st_ino)
            direct = lock.lstat()
            assert follows and (direct.st_dev, direct.st_ino) != (owned.st_dev, owned.st_ino)
            results['lock_stat_can_accept_substituted_symlink_to_owned_inode'] = True
        finally:
            os.close(fd)

    # Memory-only deterministic interleaving of sealed_namespace's two seal reads.
    # It proves that primitive assumes a stable packet; it is not a full installer bypass.
    authentic_seal = json.dumps({'manifest': 'original-manifest'}).encode()
    payload = b'changed-payload'
    forged_manifest = json.dumps({'payloads': [{'path': 'item', 'bytes': len(payload),
                                               'SHA256': sha(payload)}], 'directories': []}).encode()
    forged_seal = json.dumps({'manifest': sha(forged_manifest)}).encode()
    calls = {}
    packet = Path('/memory-only-not-a-real-path')

    def fake_read(path):
        key = str(path)
        calls[key] = calls.get(key, 0) + 1
        if path.name == 'SEAL.json':
            return authentic_seal if calls[key] == 1 else forged_seal
        return {'MANIFEST.json': forged_manifest, 'item': payload}[path.name]

    class EmptyRoot:
        def __truediv__(self, name):
            return packet / name

        def rglob(self, pattern):
            return []

    env = {'need': need, 'sha': sha, 'read': fake_read, 'json': json,
           'obj': lambda path: json.loads(fake_read(path)),
           'namespace': lambda root: ['SEAL.json', 'MANIFEST.json', 'item'],
           'safe_rel': lambda text: text,
           'pin': lambda path, row: need(sha(fake_read(path)) == row['SHA256'], 'pin')}
    sealed_namespace = extracted('sealed_namespace', env)
    result, rows = sealed_namespace(EmptyRoot(), 'SEAL.json', 'MANIFEST.json',
                                    sha(authentic_seal), 'manifest', 'payloads')
    assert result['manifest'] == sha(forged_manifest) and rows[0]['SHA256'] == sha(payload)
    results['seal_second_read_can_differ_from_authenticated_first_read'] = True

    # Real native bytes read-only; preserve the distinction between tuple and raw protection.
    env = {'need': need, 'sha': sha, 'struct': struct, 'hashlib': hashlib}
    parse = extracted('parse_index', env)
    capture = json.loads((PREP / 'PREFLIGHT_CAPTURE.json').read_bytes())
    stage = HERE.parent / 'lefschetz-link-private-stage-sol-20261115'
    rows = json.loads((stage / 'OVERLAY_MANIFEST.json').read_bytes())['files']
    targets = {('public/' + row['path']).encode() for row in rows}
    raw = (PREP / 'private/shared-index.before').read_bytes()
    parsed = parse(raw, targets)
    assert parsed['count'] == 58545 and parsed['protected_record_count'] == 58543
    assert parsed['protected_raw_records_SHA256'] == capture['Git']['protected_raw_records_SHA256']
    path, record = parsed['protected'][0]
    start = raw.find(record)
    assert raw.count(record) == 1
    changed = bytearray(raw)
    changed[start] ^= 1
    changed[-20:] = hashlib.sha1(changed[:-20]).digest()
    mutated = parse(bytes(changed), targets)
    assert [(p, m, o) for p, r, m, o in parsed['entries']] == [(p, m, o) for p, r, m, o in mutated['entries']]
    assert parsed['protected'] != mutated['protected']
    results['raw_index_check_detects_stat_change_invisible_to_stage_tuples'] = True
    print(json.dumps({'status': 'PASS_ISOLATED_AUDIT_CONTROLS', 'results': results,
                      'full_installer_bypass_demonstrated': False,
                      'real_repository_mutations': False, 'Git_or_installer_executed': False}, indent=2))


if __name__ == '__main__':
    main()
