"""Portable integrity regression suite; archive contents remain inert data."""
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import warnings
import zipfile

if len(sys.argv) != 4:
    raise SystemExit('Usage: TEST_VERIFY_AUTHOR.py VERIFY_AUTHOR.py AUTHOR.zip FREEZE_RECEIPT.json')
VERIFIER, AUTHOR, RECEIPT = (Path(arg).resolve() for arg in sys.argv[1:])
api = runpy.run_path(str(VERIFIER))
api['verify'](AUTHOR, RECEIPT)
original = AUTHOR.read_bytes()
with zipfile.ZipFile(io.BytesIO(original)) as z:
    entries = [(copy.copy(i), z.read(i)) for i in z.infolist()]


def require(value, message):
    if not value:
        raise RuntimeError(message)


def repack(items, comment=b''):
    out = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        with zipfile.ZipFile(out, 'w') as z:
            z.comment = comment
            for info, value in items:
                z.writestr(info, value)
    return out.getvalue()


def alter(name, change):
    items = copy.deepcopy(entries)
    for k, (info, value) in enumerate(items):
        if info.filename == name:
            items[k] = change(info, value)
            break
    return repack(items)


def rename(newname):
    def change(info, value):
        info.filename = newname
        info.orig_filename = newname
        return info, value
    return alter('README.md', change)


def mode(newmode):
    def change(info, value):
        info.external_attr = newmode << 16
        return info, value
    return alter('README.md', change)


def compression(info, value):
    info.compress_type = zipfile.ZIP_STORED
    return info, value


def origin(info, value):
    info.create_system = 0
    return info, value


def extra(info, value):
    info.extra = b'\x99\x99\x00\x00'
    return info, value


def member_comment(info, value):
    info.comment = b'not allowed'
    return info, value


mutants = {
    'extra_member': repack(entries + [(zipfile.ZipInfo('unapproved.py'), b'raise RuntimeError()')]),
    'missing_member': repack(entries[1:]),
    'duplicate_member': repack(entries + [entries[0]]),
    'traversal': rename('../README.md'),
    'absolute_name': rename('/README.md'),
    'backslash_name': rename('..\\README.md'),
    'nested_name': rename('nested/README.md'),
    'symlink_mode': mode(0o120444),
    'executable_mode': mode(0o100555),
    'writable_mode': mode(0o100644),
    'stored_compression': alter('README.md', compression),
    'origin_system': alter('README.md', origin),
    'extra_metadata': alter('README.md', extra),
    'member_comment': alter('README.md', member_comment),
    'archive_comment': repack(entries, b'not allowed'),
    'changed_content_same_size': alter('README.md', lambda i, v: (i, b'!' + v[1:])),
    'changed_content_size': alter('README.md', lambda i, v: (i, v + b'\n')),
    'malformed_json': alter('STATUS.json', lambda i, v: (i, b'x' * len(v))),
    'truncated_zip': original[:-10],
    'appended_bytes': original + b'payload',
}
items = copy.deepcopy(entries)
new_readme = entries[1][1] + b'\n'
for n, (info, value) in enumerate(items):
    if info.filename == 'README.md':
        items[n] = info, new_readme
    if info.filename == 'MANIFEST.json':
        manifest = json.loads(value)
        for row in manifest['payload_members']:
            if row['path'] == 'README.md':
                row['bytes'] = len(new_readme)
                row['sha256'] = hashlib.sha256(new_readme).hexdigest()
        items[n] = info, (json.dumps(manifest, indent=2) + '\n').encode()
mutants['self_consistent_rehashed_payload'] = repack(items)

structural_results = []
for name, value in mutants.items():
    if name == 'appended_bytes':
        continue  # Outer identity check, rather than ZIP semantics, forbids this.
    try:
        api['inspect_payload'](value)
    except Exception as error:
        structural_results.append({'case': name, 'result': 'rejected', 'reason': str(error)})
    else:
        raise RuntimeError('Structural layer accepted: ' + name)
for name, value in [('duplicate_json_key', b'{"a":1,"a":2}'),
                    ('nonfinite_json', b'{"a":NaN}')]:
    try:
        api['strict_json'](value)
    except Exception as error:
        structural_results.append({'case': name, 'result': 'rejected', 'reason': str(error)})
    else:
        raise RuntimeError('JSON layer accepted: ' + name)

cli_results = []
with tempfile.TemporaryDirectory(prefix='finite-radius-audit-') as tmp:
    root = Path(tmp)
    relocated = root / 'unrelated directory'
    relocated.mkdir()
    script = relocated / 'check.py'
    archive = relocated / 'input.zip'
    receipt = relocated / 'receipt.json'
    shutil.copyfile(VERIFIER, script)
    shutil.copyfile(AUTHOR, archive)
    shutil.copyfile(RECEIPT, receipt)
    (root / 'json.py').write_text('raise RuntimeError("UNSAFE_SHADOW_IMPORT")\n')
    (root / 'sitecustomize.py').write_text('raise RuntimeError("UNSAFE_SITE")\n')
    env = dict(os.environ, PYTHONPATH=str(root), PYTHONHOME='')
    for flags, mode_name in [(['-I', '-S'], 'isolated'), (['-I', '-S', '-O'], 'isolated_optimized')]:
        for scriptpath, inputpath, receiptpath, location in [
            (VERIFIER, AUTHOR, RECEIPT, 'original'),
            (script, archive, receipt, 'relocated_with_hostile_pythonpath')]:
            p = subprocess.run([sys.executable, *flags, str(scriptpath), str(inputpath), str(receiptpath)],
                               cwd=root, env=env, text=True, capture_output=True)
            require(p.returncode == 0, p.stdout + p.stderr)
            result = json.loads(p.stdout)
            require(result['verdict'] == 'PASS' and result['receipt_verified'], 'Bad positive result')
            cli_results.append({'mode': mode_name, 'case': location, 'result': 'pass'})
        for name, value in mutants.items():
            bad = root / (name + '.zip')
            bad.write_bytes(value)
            p = subprocess.run([sys.executable, *flags, str(script), str(bad)],
                               cwd=root, env=env, text=True, capture_output=True)
            require(p.returncode == 1 and json.loads(p.stdout)['verdict'] == 'FAIL',
                    'Production verifier accepted ' + name)
            cli_results.append({'mode': mode_name, 'case': name, 'result': 'rejected'})
        symlink = root / ('input-link-' + mode_name)
        symlink.symlink_to(archive)
        p = subprocess.run([sys.executable, *flags, str(script), str(symlink)],
                           cwd=root, env=env, text=True, capture_output=True)
        require(p.returncode == 1 and json.loads(p.stdout)['verdict'] == 'FAIL', 'Accepted symlink input')
        cli_results.append({'mode': mode_name, 'case': 'symlink_input', 'result': 'rejected'})
        bad_receipt = root / ('bad-receipt-' + mode_name)
        raw = RECEIPT.read_bytes()
        bad_receipt.write_bytes(b'!' + raw[1:])
        p = subprocess.run([sys.executable, *flags, str(script), str(archive), str(bad_receipt)],
                           cwd=root, env=env, text=True, capture_output=True)
        require(p.returncode == 1 and json.loads(p.stdout)['verdict'] == 'FAIL', 'Accepted bad receipt')
        cli_results.append({'mode': mode_name, 'case': 'same_size_bad_receipt', 'result': 'rejected'})

output = {
    'verdict': 'PASS',
    'python': sys.version.split()[0],
    'harness_optimized': not __debug__,
    'verifier_bytes': VERIFIER.stat().st_size,
    'verifier_sha256': hashlib.sha256(VERIFIER.read_bytes()).hexdigest(),
    'positive_cli_runs': sum(r['result'] == 'pass' for r in cli_results),
    'negative_cli_runs': sum(r['result'] == 'rejected' for r in cli_results),
    'structural_and_json_negative_runs': len(structural_results),
    'cli_results': cli_results,
    'structural_results': structural_results,
    'mathematical_scope': 'Integrity tests only; no proof or left-orderability algorithm is executed.',
}
print(json.dumps(output, indent=2, sort_keys=True))
