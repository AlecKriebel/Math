"""Independent extracted-function toy controls; no installer/import/Git/real-target writes."""
from pathlib import Path
from types import SimpleNamespace
import ast
import hashlib
import json
import os
import stat
import tempfile

ROOT = Path(__file__).resolve().parent
PREP = ROOT.parent / 'lefschetz-link-production-integration-preparation-v2-sol-20261115'
LIB = ast.parse((PREP / 'exact11_lib.py').read_text())


def need(value, reason):
    if not value:
        raise RuntimeError(reason)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def functions(names, env):
    nodes = [node for node in LIB.body if isinstance(node, ast.FunctionDef) and node.name in names]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(PREP / 'exact11_lib.py'), 'exec'), env)


def rejected(action):
    try:
        action()
    except RuntimeError:
        return
    raise AssertionError('expected rejection')


def main():
    results = {}
    names = ['owned_entry', 'write_complete', 'validate_owned_buffer', 'unlink_owned', 'publish_buffer']
    lock_body = b'Exact11 publication lock; inspect run-state if interrupted\n'
    proxy = SimpleNamespace(**{name: getattr(os, name) for name in
                              ['write', 'fstat', 'fsync', 'lseek', 'read', 'replace', 'close', 'SEEK_SET']})
    maker = SimpleNamespace(mkstemp=tempfile.mkstemp)
    env = {'need': need, 'os': proxy, 'stat': stat, 'tempfile': maker,
           'Path': Path, 'LOCK_BODY': lock_body}
    functions(names, env)

    with tempfile.TemporaryDirectory(prefix='independent-toy-', dir=ROOT) as temporary:
        toy = Path(temporary)
        lock = toy / 'index.lock'
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
        env['write_complete'](fd, lock_body)
        env['validate_owned_buffer'](lock, fd, lock_body)
        owned_lock = os.fstat(fd)
        destination = toy / 'destination'; destination.write_bytes(b'old')
        alternate = toy / 'alternate'; alternate.write_bytes(b'checked binary\0buffer')
        checked = alternate.read_bytes()
        alternate.write_bytes(b'changed alternate')

        def observed_replace(source, target):
            direct = lock.lstat()
            assert (direct.st_dev, direct.st_ino) == (owned_lock.st_dev, owned_lock.st_ino)
            assert lock.read_bytes() == lock_body
            return os.replace(source, target)

        proxy.replace = observed_replace
        env['publish_buffer'](checked, destination, lock, fd)
        assert destination.read_bytes() == checked != alternate.read_bytes()
        env['validate_owned_buffer'](lock, fd, lock_body)
        results['checked_buffer_published_with_distinct_original_lock_retained'] = True

        calls = [0]

        def short_write(descriptor, data):
            calls[0] += 1
            if calls[0] == 1:
                raise InterruptedError('toy interruption')
            return os.write(descriptor, data[:2])

        proxy.write = short_write
        proxy.read = lambda descriptor, count: os.read(descriptor, min(count, 3))
        env['publish_buffer'](checked, destination, lock, fd)
        assert destination.read_bytes() == checked and calls[0] > 2
        proxy.write, proxy.read = os.write, os.read
        results['short_interrupted_writes_and_short_reads_complete_correctly'] = True

        destination.write_bytes(b'old-zero-progress')
        proxy.write = lambda descriptor, data: 0
        rejected(lambda: env['publish_buffer'](checked, destination, lock, fd))
        proxy.write = os.write
        assert destination.read_bytes() == b'old-zero-progress'
        assert not list(toy.glob('.exact11-index-approved-*'))
        results['zero_write_rejected_before_destination_change_and_owned_temporary_removed'] = True

        captured = []

        def foreign_sibling(*args, **kwargs):
            descriptor, name = tempfile.mkstemp(*args, **kwargs)
            path = Path(name); path.unlink(); path.write_bytes(b'foreign sibling')
            captured.append((descriptor, path))
            return descriptor, name

        maker.mkstemp = foreign_sibling
        rejected(lambda: env['publish_buffer'](checked, destination, lock, fd))
        maker.mkstemp = tempfile.mkstemp
        descriptor, path = captured[0]
        assert path.read_bytes() == b'foreign sibling'
        assert destination.read_bytes() == b'old-zero-progress'
        try:
            os.fstat(descriptor)
        except OSError:
            pass
        else:
            raise AssertionError('publication leaked sibling descriptor after ownership rejection')
        results['foreign_sibling_retained_destination_unchanged_descriptor_closed'] = True

        # Directly reproduce original v1 lock.stat weakness with the v2 cleanup.
        retained = toy / 'owned-hardlink'; os.link(lock, retained)
        lock.unlink(); lock.symlink_to(retained)
        rejected(lambda: env['unlink_owned'](lock, fd))
        assert lock.is_symlink() and retained.read_bytes() == lock_body
        lock.unlink(); os.link(retained, lock)
        results['symlink_to_retained_owned_inode_rejected_and_retained'] = True

        lock.unlink(); lock.write_bytes(b'foreign lock')
        rejected(lambda: env['unlink_owned'](lock, fd))
        assert lock.read_bytes() == b'foreign lock'
        lock.unlink(); os.link(retained, lock)
        results['foreign_regular_lock_rejected_and_retained'] = True

        # Accepted residual assumption: a hostile edit after the last identity
        # check can be detected only after replacement has already had an effect.
        def last_moment_substitution(source, target):
            source = Path(source)
            source.unlink(); source.write_bytes(b'last-moment foreign bytes')
            return os.replace(source, target)

        proxy.replace = last_moment_substitution
        rejected(lambda: env['publish_buffer'](checked, destination, lock, fd))
        assert destination.read_bytes() == b'last-moment foreign bytes'
        env['validate_owned_buffer'](lock, fd, lock_body)
        results['residual_last_check_to_rename_substitution_detected_after_side_effect'] = True
        proxy.replace = os.replace
        env['unlink_owned'](lock, fd)
        os.close(fd)

    # Same-buffer proof with an interleaving that would change a second seal read.
    manifest = json.dumps({'payloads': [{'path': 'item', 'bytes': 7, 'SHA256': sha(b'payload')}],
                           'directories': []}).encode()
    authentic = json.dumps({'manifest': sha(manifest)}).encode()
    substituted = json.dumps({'manifest': '0' * 64}).encode()
    calls = [0]

    def fake_read(path):
        if path.name == 'SEAL':
            calls[0] += 1
            return authentic if calls[0] == 1 else substituted
        return {'MANIFEST': manifest, 'item': b'payload'}[path.name]

    class EmptyRoot:
        def __truediv__(self, name):
            return Path('/memory-only-not-real') / name

        def rglob(self, pattern):
            return []

    seal_env = {'need': need, 'sha': sha, 'json': json, 'read': fake_read,
                'namespace': lambda root: ['SEAL', 'MANIFEST', 'item'],
                'safe_rel': lambda text: text,
                'pin': lambda path, row: need(sha(fake_read(path)) == row['SHA256'], 'pin')}
    functions(['sealed_namespace'], seal_env)
    observed, rows = seal_env['sealed_namespace'](EmptyRoot(), 'SEAL', 'MANIFEST', sha(authentic),
                                                'manifest', 'payloads')
    assert calls[0] == 1 and observed == json.loads(authentic)
    results['seal_authenticated_and_parsed_from_one_exact_buffer'] = True

    print(json.dumps({'status': 'PASS_INDEPENDENT_ISOLATED_V2_CONTROLS', 'results': results,
                      'residual_namespace_cooperation_required': True,
                      'real_repository_or_preparation_writes': False,
                      'Git_or_installer_or_owner_controls_executed': False}, indent=2))


if __name__ == '__main__':
    main()
