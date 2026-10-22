"""Independent tiny native-object adversarial controls. No network or local Git.

Only owned byte-pinned source copies are imported. Fixtures are test evidence,
never actual receipts. Native identities are authored independently of the core.
"""
import base64
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
CORE_PIN = (22049, '8a61aee886e7a19bba6c7369944d778614b4099cbe1a060cf7e8acf2f52ec4d5')
CHECKPOINT_PIN = (22360, 'b448d2671fe27ca1bee624602cc1a8de5ef6e95126bef6a79b24fc9ce50bd256')


def check(condition, message):
    if condition is not True:
        raise RuntimeError(message)


def oid(kind, raw):
    return hashlib.sha1(kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def load_owned(name, wanted):
    path = HERE / '_private' / name
    raw = path.read_bytes()
    check((len(raw), hashlib.sha256(raw).hexdigest()) == wanted, 'Owned import pin')
    check(path.resolve() == path and path.stat().st_mode & 0o777 == 0o444, 'Owned source mode')
    spec = importlib.util.spec_from_file_location('independent_' + name.replace('.', '_'), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Objects:
    def __init__(self):
        self.trees = {}
        self.blobs = {}
        self.calls = []

    def blob(self, raw):
        sha = oid('blob', raw)
        self.blobs[sha] = raw
        return sha

    def tree(self, rows):
        rows = sorted(rows, key=lambda row: row[0].encode() + (b'/' if row[1] == '040000' else b''))
        raw = b''.join((row[1].lstrip('0') + ' ' + row[0]).encode() + b'\0' + bytes.fromhex(row[3]) for row in rows)
        sha = oid('tree', raw)
        self.trees[sha] = [dict(path=n, mode=m, type=k, sha=s) for n, m, k, s in rows]
        return sha

    def __call__(self, method, path, body=None):
        self.calls.append((method, path))
        check(method == 'GET' and body is None, 'Core fixture forbids writes')
        if path.startswith('git/trees/'):
            sha = path.rsplit('/', 1)[1]
            return dict(sha=sha, truncated=False, tree=copy.deepcopy(self.trees[sha]))
        if path.startswith('git/blobs/'):
            sha = path.rsplit('/', 1)[1]
            raw = self.blobs[sha]
            return dict(sha=sha, size=len(raw), encoding='base64', content=base64.b64encode(raw).decode())
        raise RuntimeError('Unexpected fixture endpoint ' + path)


def fixture():
    db = Objects()
    empty = db.tree([])
    deep = db.tree([('unrelated', '100644', 'blob', db.blob(b'foreign nested\n'))])
    original_rows = [
        ('empty', '040000', 'tree', empty),
        ('foreign', '040000', 'tree', deep),
        ('run', '100755', 'blob', db.blob(b'#!/bin/sh\nexit 0\n')),
        ('symlink', '120000', 'blob', db.blob(b'../foreign/unrelated')),
        ('vendor', '160000', 'commit', '1234567890abcdef1234567890abcdef12345678'),
        ('QUEUE.md', '100644', 'blob', db.blob(b'header\n| 7 | foreign |\n| 5100044 | own |\nfooter\n')),
    ]
    before = db.tree(original_rows)
    body = b'independent selected content\n'
    audit = db.tree([('selected.txt', '100644', 'blob', db.blob(body))])
    after = db.tree(original_rows + [('audit', '040000', 'tree', audit)])
    return db, before, after, body


def run():
    check(sys.flags.ignore_environment == 1 and sys.flags.no_site == 1 and sys.dont_write_bytecode is True and sys.flags.safe_path is True and sys.flags.optimize == 0, 'Use Python -E -S -B -P without optimization')
    core = load_owned('archive206_verified_reference.py', CORE_PIN)
    outcomes = []

    def passed(name, action):
        action()
        outcomes.append(dict(control=name, result='PASS'))

    def rejected(name, action):
        try:
            action()
        except (RuntimeError, ValueError, KeyError, TypeError, OSError):
            outcomes.append(dict(control=name, result='REJECTED_AS_REQUIRED'))
        else:
            raise RuntimeError('Control unexpectedly accepted: ' + name)

    historical = load_owned('checkpoint207_v3_public.py', CHECKPOINT_PIN)
    with tempfile.TemporaryDirectory(prefix='independent-lock-', dir=HERE / '_private') as name:
        historical.PROGRAM = Path(name)
        lock_path = Path(name) / 'ROOT_GLOBAL_FIVE_WRITER.lock'
        rejected('missing_existing_writer_lock', lambda: historical.WriterLock().__enter__())
        lock_path.write_bytes(historical.LOCK_BYTES)
        lock_path.chmod(0o444)
        def held_lock():
            with historical.WriterLock() as lock:
                lock.check()
                rejected('concurrent_writer_lock', lambda: historical.WriterLock().__enter__())
        passed('existing_stable_writer_lock', held_lock)
        lock_path.chmod(0o644)
        rejected('mutable_writer_lock', lambda: historical.WriterLock().__enter__())
        lock_path.write_bytes(b'wrong lock bytes')
        lock_path.chmod(0o444)
        rejected('wrong_writer_lock_payload', lambda: historical.WriterLock().__enter__())
        lock_path.chmod(0o644)
        lock_path.write_bytes(historical.LOCK_BYTES)
        lock_path.chmod(0o444)
        def replaced_lock():
            with historical.WriterLock():
                lock_path.unlink()
                lock_path.write_bytes(historical.LOCK_BYTES)
                lock_path.chmod(0o444)
        rejected('writer_lock_inode_replaced', replaced_lock)

    db, before, after, body = fixture()
    def preservation():
        reader = core.NativeTrees(db)
        wanted, missing, dirs = reader.expected(before, {'audit/selected.txt': body})
        check(wanted == after and missing == {'audit/selected.txt'} and dirs == {'audit'}, 'Independent native postimage')
        check(reader.changes(before, after) == ({'audit/selected.txt'}, {'audit'}, set()), 'Independent exact diff')
        for name in ['empty', 'foreign', 'run', 'symlink', 'vendor', 'QUEUE.md']:
            check(reader.lookup(before, name) == reader.lookup(after, name), 'Foreign tuple changed')
        check(('GET', 'git/trees/' + reader.lookup(before, 'foreign')[2]) not in db.calls, 'Equal foreign subtree was traversed')
    passed('native_modes_empty_tree_and_foreign_QUEUE_preserved', preservation)
    passed('selected_blob_native_identity_verified', lambda: core.blob_matches(db, oid('blob', body), body))
    for name, mutate in [
        ('foreign_empty_tree_deleted', lambda rows: [row for row in rows if row[0] != 'empty']),
        ('foreign_executable_mode_changed', lambda rows: [(n, '100644' if n == 'run' else m, k, s) for n, m, k, s in rows]),
        ('foreign_symlink_target_changed', lambda rows: [(n, m, k, db.blob(b'foreign-target') if n == 'symlink' else s) for n, m, k, s in rows]),
        ('foreign_gitlink_changed', lambda rows: [(n, m, k, 'f' * 40 if n == 'vendor' else s) for n, m, k, s in rows]),
        ('foreign_QUEUE_bytes_changed', lambda rows: [(n, m, k, db.blob(b'foreign line edited\n') if n == 'QUEUE.md' else s) for n, m, k, s in rows]),
    ]:
        def action(mutate=mutate):
            rows = [(x['path'], x['mode'], x['type'], x['sha']) for x in db.trees[after]]
            forged = db.tree(mutate(rows))
            core.exact_scope(dict(trees=core.NativeTrees(db), parent_tree=before, wanted=forged,
                                  missing={'audit/selected.txt'}, newdirs={'audit'}))
        rejected(name, action)
    for name, mutate in [
        ('truncated_immediate_tree', lambda j: j.update(truncated=True)),
        ('duplicate_tree_name', lambda j: j['tree'].append(copy.deepcopy(j['tree'][0]))),
        ('wrong_tree_sort', lambda j: j['tree'].reverse()),
        ('forged_tree_SHA', lambda j: j['tree'][0].update(sha='f' * 40)),
        ('invalid_mode_type_pair', lambda j: j['tree'][0].update(mode='100644', type='commit')),
    ]:
        def action(mutate=mutate):
            def bad_api(method, path, payload=None):
                result = db(method, path, payload)
                if path == 'git/trees/' + before:
                    mutate(result)
                return result
            core.NativeTrees(bad_api).get(before, 0)
        rejected(name, action)
    for raw in [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}']:
        rejected('strict_JSON_' + raw.decode(), lambda raw=raw: core.decode(raw))
    for value in ['../escape', '/absolute', 'a//b', 'a/./b', 'a\\b', 'a\0b', 'a/../b']:
        rejected('unsafe_path_' + repr(value), lambda value=value: core.rel(value))
    rejected('bool_byte_count', lambda: core.bytepin(dict(bytes=True, sha256='0' * 64)))
    rejected('leaf_ancestor_collision', lambda: core.NativeTrees(db).expected(before, {'audit': b'x', 'audit/leaf': b'y'}))
    rejected('foreign_leaf_as_overlay_ancestor', lambda: core.NativeTrees(db).expected(before, {'run/leaf': b'x'}))
    rejected('selected_native_preexisting_mismatch', lambda: core.NativeTrees(db).expected(before, {'QUEUE.md': b'replaced\n'}))
    for name, mutate in [
        ('blob_size_mismatch', lambda j: j.update(size=j['size'] + 1)),
        ('blob_bool_size', lambda j: j.update(size=True)),
        ('blob_corrupt_base64', lambda j: j.update(content='???')),
        ('blob_forged_body', lambda j: j.update(content=base64.b64encode(b'forged').decode(), size=6)),
    ]:
        def action(mutate=mutate):
            def bad_api(method, path, payload=None):
                result = db(method, path, payload)
                mutate(result)
                return result
            core.blob_matches(bad_api, oid('blob', body), body)
        rejected(name, action)
    return dict(schema='pr207-independent-native-controls-v1', evidence_scope='INDEPENDENT_IN_MEMORY_TESTS_ONLY', actual_events_created=False, control_count=len(outcomes), controls=outcomes)


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
