"""Bounded own controls, including isolated toy FD files; never Git or the installer."""
import sys
sys.dont_write_bytecode = True
import ast
import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import struct
import tempfile
from pathlib import Path
import exact11_lib as L
from exact11_lib import O, BASE, need, parse_index, adoption_fields, safe_rel


def fd_controls():
    results = []

    def denied(action):
        try:
            action()
        except RuntimeError:
            return
        raise RuntimeError('an isolated ownership/content control was not rejected')

    def lock_at(path):
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
        L.write_complete(fd, L.LOCK_BODY)
        L.validate_owned_buffer(path, fd, L.LOCK_BODY)
        return fd

    with tempfile.TemporaryDirectory(prefix='isolated-fd-controls-', dir=O / 'private') as directory:
        root = Path(directory)
        packet = root / 'toy-packet'; packet.mkdir()
        body = b'owned toy payload'
        (packet / 'payload').write_bytes(body)
        manifest = {'files': [{'path': 'payload', 'bytes': len(body), 'SHA256': L.sha(body)}],
                    'exact_relative_directories': []}
        manifest_body = json.dumps(manifest).encode()
        (packet / 'MANIFEST').write_bytes(manifest_body)
        seal_a = json.dumps({'manifest_SHA256': L.sha(manifest_body)}).encode()
        seal_b = json.dumps({'manifest_SHA256': '0' * 64}).encode()
        seal_path = packet / 'SEAL'; seal_path.write_bytes(seal_a)
        original_read = L.read; calls = [0]

        def changed_seal(path):
            value = original_read(path)
            if Path(path) == seal_path:
                calls[0] += 1
                seal_path.write_bytes(seal_b)
            return value

        L.read = changed_seal
        try:
            observed, _ = L.sealed_namespace(packet, 'SEAL', 'MANIFEST', L.sha(seal_a),
                                             'manifest_SHA256', 'files')
        finally:
            L.read = original_read
        need(calls[0] == 1 and observed['manifest_SHA256'] == L.sha(manifest_body)
             and seal_path.read_bytes() == seal_b, 'same authenticated seal buffer, not changed pathname bytes')
        results.append({'control': 'seal path actually changed after read', 'critical_reads': calls[0],
                        'authenticated_and_parsed_original_buffer': True})

        alternate = root / 'mutable-alternate'
        newraw = b'VALIDATED BUFFER: toy data, not a Git index'
        alternate.write_bytes(newraw)
        captured = alternate.read_bytes()
        alternate.write_bytes(b'CHANGED ALTERNATE PATH')
        destination = root / 'toy-destination'; destination.write_bytes(b'old destination')
        lock = root / 'toy-lock'; fd = lock_at(lock)
        try:
            L.publish_buffer(captured, destination, lock, fd)
            L.validate_owned_buffer(lock, fd, L.LOCK_BODY)
            need(destination.read_bytes() == newraw and destination.read_bytes() != alternate.read_bytes(),
                 'publication uses captured validated bytes despite altered alternate')
            results.append({'control': 'altered alternate cannot replace validated buffer',
                            'installed_bytes_hex': destination.read_bytes().hex(),
                            'distinct_owned_lock_retained': True})
        finally:
            try: L.unlink_owned(lock, fd)
            finally: os.close(fd)

        path = root / 'short-write'; fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
        original_write = L.os.write; writes = [0]

        def short_write(descriptor, value):
            writes[0] += 1
            if writes[0] == 1:
                raise InterruptedError('isolated interrupted write')
            return original_write(descriptor, value[:3])

        L.os.write = short_write
        try:
            L.write_complete(fd, newraw)
        finally:
            L.os.write = original_write
        try:
            L.validate_owned_buffer(path, fd, newraw)
            need(writes[0] > 2, 'actual short/interrupted writes exercised')
            results.append({'control': 'complete interrupted and short writes', 'write_attempts': writes[0],
                            'actual_bytes_equal': path.read_bytes() == newraw})
        finally:
            try: L.unlink_owned(path, fd)
            finally: os.close(fd)

        path = root / 'zero-write'; fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
        L.os.write = lambda descriptor, value: 0
        try:
            denied(lambda: L.write_complete(fd, newraw))
        finally:
            L.os.write = original_write
        try:
            need(os.fstat(fd).st_size == 0, 'zero-progress write rejected without hanging')
            results.append({'control': 'zero progress rejected', 'actual_file_bytes': 0})
        finally:
            try: L.unlink_owned(path, fd)
            finally: os.close(fd)

        path = root / 'foreign-lock'; fd = lock_at(path)
        path.unlink(); path.write_bytes(b'foreign inode')
        try:
            denied(lambda: L.unlink_owned(path, fd))
            need(path.read_bytes() == b'foreign inode', 'foreign regular entry retained')
            results.append({'control': 'foreign regular inode cleanup rejected', 'foreign_entry_retained': True})
        finally:
            os.close(fd)

        target = root / 'owned-target'; fd = lock_at(target)
        link = root / 'symlink-lock'; link.symlink_to(target)
        try:
            denied(lambda: L.unlink_owned(link, fd))
            need(link.is_symlink() and target.read_bytes() == L.LOCK_BODY, 'symlink and its target retained')
            results.append({'control': 'symlink to owned inode cleanup rejected', 'symlink_and_target_retained': True})
        finally:
            os.close(fd)

        destination.write_bytes(b'old destination')
        lock = root / 'sibling-control-lock'; fd = lock_at(lock)
        original_mkstemp = L.tempfile.mkstemp; substituted = []

        def changed_sibling(*args, **kwargs):
            sibling_fd, name = original_mkstemp(*args, **kwargs)
            path = Path(name); path.unlink(); path.write_bytes(b'foreign final sibling')
            substituted.append(path)
            return sibling_fd, name

        L.tempfile.mkstemp = changed_sibling
        try:
            denied(lambda: L.publish_buffer(newraw, destination, lock, fd))
        finally:
            L.tempfile.mkstemp = original_mkstemp
        try:
            need(destination.read_bytes() == b'old destination'
                 and substituted[0].read_bytes() == b'foreign final sibling',
                 'substituted sibling rejected before replacement and never cleaned as owned')
            results.append({'control': 'final sibling inode substitution rejected',
                            'destination_unchanged': True, 'foreign_sibling_retained': True})
        finally:
            try: L.unlink_owned(lock, fd)
            finally: os.close(fd)

        path = root / 'changed-content'; fd = lock_at(path)
        os.lseek(fd, 0, os.SEEK_SET); original_write(fd, b'changed')
        try:
            denied(lambda: L.validate_owned_buffer(path, fd, L.LOCK_BODY))
            results.append({'control': 'changed owned FD content rejected', 'actual_bytes_changed': True})
        finally:
            try: L.unlink_owned(path, fd)
            finally: os.close(fd)
    return results


def main():
    results = []

    def rejected(label, action):
        try:
            action()
        except (RuntimeError, ValueError, struct.error):
            results.append({'control': label, 'rejected': True})
        else:
            raise RuntimeError('missed control: ' + label)

    for name in ['exact11_lib.py', 'preflight.py', 'install_exact.py', 'controls.py', 'verify_preparation.py']:
        ast.parse((O / name).read_text())
    installer = ast.parse((O / 'install_exact.py').read_text())
    main_body = next(n for n in installer.body if isinstance(n, ast.FunctionDef) and n.name == 'main').body
    gate = next(i for i, n in enumerate(main_body) if isinstance(n, ast.Assign)
                and isinstance(n.value, ast.Call) and getattr(n.value.func, 'id', '') == 'root_adoption')
    dispatch = next(i for i, n in enumerate(main_body) if isinstance(n, ast.If))
    need(gate < dispatch, 'root adoption gate before mutation dispatch')
    tree = ast.parse((O / 'exact11_lib.py').read_text())
    # Only imports, literal/path assignments, and function definitions occur at library top level.
    need(not any(isinstance(n, (ast.With, ast.For, ast.While, ast.If, ast.Expr))
                 and not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)) for n in tree.body),
         'inert library top level')
    template = json.loads((O / 'ROOT_ADOPTION_TEMPLATE.json').read_bytes())
    rejected('false-authority preparation template', lambda: adoption_fields(template))
    valid = copy.deepcopy(template)
    valid['template_not_root_receipt'] = False
    flags = ['root_stage_adopted', 'independent_code_audit_adopted',
             'complete_current_helper_and_rendered_output_adopted', 'production_install_authorized']
    for key in flags:
        valid[key] = True
    adoption_fields(valid)  # Memory-only field fixture; no receipt or authority is created.
    for key in flags:
        bad = copy.deepcopy(valid); bad[key] = 1
        rejected('integer is not explicit boolean authority: ' + key, lambda bad=bad: adoption_fields(bad))
    bad = copy.deepcopy(valid); bad['commit_message'] = 'x\0y'
    rejected('invalid message rejected before mutation', lambda: adoption_fields(bad))
    for text in ['../public/file', '/public/file', 'research/../file', 'research\\file']:
        rejected('path escape ' + text, lambda text=text: safe_rel(text))

    raw = (O / 'private/shared-index.before').read_bytes()
    overlay = json.loads((O.parents[0] / 'lefschetz-link-private-stage-sol-20261115/OVERLAY_MANIFEST.json').read_bytes())['files']
    targets = {('public/' + r['path']).encode() for r in overlay}
    parsed = parse_index(raw, targets)
    need(parsed['count'] == json.loads((O / 'PREFLIGHT_CAPTURE.json').read_bytes())['Git']['index_record_count'],
         'actual fresh index extent, no inherited count')
    bad = bytearray(raw); bad[-1] ^= 1
    rejected('whole index checksum corruption', lambda: parse_index(bytes(bad), targets))

    def changed(offset, value):
        bad = bytearray(raw); bad[offset:offset + len(value)] = value
        bad[-20:] = hashlib.sha1(bad[:-20]).digest()
        return bytes(bad)

    rejected('unsupported v3 index', lambda: parse_index(changed(4, struct.pack('>I', 3)), targets))
    rejected('unmerged flags', lambda: parse_index(changed(72, b'\x10\x00'), targets))
    first_path = parsed['entries'][0][0]
    path_start = 12 + 62
    end = path_start + len(first_path)
    rejected('nonzero native padding', lambda: parse_index(changed(end, b'X'), targets))
    protected_path, protected_record = parsed['protected'][0]
    start = raw.find(protected_record)
    need(start >= 12 and raw.count(protected_record) == 1, 'unique actual protected raw record')
    for offset, label in [(0, 'stat bytes'), (24, 'mode'), (40, 'object identity')]:
        bad = bytearray(raw); bad[start + offset] ^= 1
        bad[-20:] = hashlib.sha1(bad[:-20]).digest()
        try:
            altered = parse_index(bytes(bad), targets)
        except RuntimeError:
            results.append({'control': 'protected raw ' + label, 'rejected': True})
        else:
            need(altered['protected'] != parsed['protected'], 'raw preservation fence detects ' + label)
            results.append({'control': 'protected raw ' + label, 'rejected': True})

    loader = importlib.machinery.SourceFileLoader('exact11_memory_hook', str(O / 'hooks/pre-push'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    hook = importlib.util.module_from_spec(spec); loader.exec_module(hook)
    commit = 'a' * 40; url = 'memory://explicit-origin'
    args = ['pre-push', 'origin', url]
    environment = {'EXACT11_APPROVED_COMMIT': commit,
                   'EXACT11_APPROVED_PUSH_URL_SHA256': hashlib.sha256(url.encode()).hexdigest()}
    body = (commit + ' ' + commit + ' refs/heads/master ' + BASE + '\n').encode()
    need(hook.accepted(args, environment, body), 'positive pure actual-advertisement fixture')
    bad_bodies = [b'', body + body, body.replace(BASE.encode(), b'b' * 40),
                  body.replace(b'refs/heads/master', b'refs/heads/other'),
                  body.replace(commit.encode(), b'c' * 40),
                  b'(delete) ' + commit.encode() + b' refs/heads/master ' + BASE.encode() + b'\n']
    for i, bad in enumerate(bad_bodies):
        need(not hook.accepted(args, environment, bad), 'advertisement control ' + str(i))
        results.append({'control': 'actual advertisement ' + str(i), 'rejected': True})
    need(not hook.accepted(['pre-push', 'other', url], environment, body)
         and not hook.accepted(['pre-push', 'origin', url + '/other'], environment, body),
         'wrong remote name or actual push URL rejected')
    fd_results = fd_controls()
    print(json.dumps({'status': 'PASS_BOUNDED_STATIC_MEMORY_AND_ISOLATED_FD_CONTROLS', 'controls': results,
                      'new_actual_FD_controls': fd_results,
                      'false_authority_dictionaries_only_in_memory': True, 'Git_or_installer_executed': False,
                      'network_or_subprocess': False, 'writes_only_new_private_toy_fixtures': True,
                      'actual_Git_index_or_object_or_ref_or_public_mutations': False}, indent=2))


if __name__ == '__main__':
    main()
