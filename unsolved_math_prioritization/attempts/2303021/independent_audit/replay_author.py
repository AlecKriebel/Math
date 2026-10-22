#!/usr/bin/env python3
"""Independent closed-inventory replay; run with -I -S -B.
Usage: replay_author.py AUTHOR_ARTIFACT_DIRECTORY ORIGINAL_PACKET_DIRECTORY
Only pinned author code is executed. Temporary attack fixtures are never trusted.
"""
import hashlib
import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PREFIX = 'FUNCTION_THEORY_2303021_AUTHOR_'
PINS = {
    'SAFE_FREEZE.zip': (9912, 'a89e522bc8d06a249f96ab4eb0c3351325b3bab9e21876900fab919df3c12e5f'),
    'BOOTSTRAP.py': (2249, 'e50c19ff0fe418e4c61aeabdcefa50fcb59f322c26a7c735fac94d269b3cd889'),
    'EXTERNAL_MANIFEST.json': (1553, '630f2280e99538428b6f623d24cdea9c866a0f40d7f71c294c4fadec8f124fd1'),
    'VALIDATION_RECEIPT.json': (4702, '1d6003628c36d9ed4fe9b8073ff6b7281d51319399838a15e87314f1a2264cae'),
}
MANIFEST_PIN = '3770f2377bd62309dc72af56862be11ad97115964d7efab36ed2014d503ada2c'
NAMES = {'APPROACHES.md', 'CLAIMS.json', 'MANIFEST.json', 'README.md', 'RESULT.md', 'SOURCES.json', 'verify.py'}
EXPECTED_RESULT = {'authored_effort': '1/5', 'formal_proof': False, 'inventory_files': 7,
                   'result': 'PASS: static inventory and declared scope', 'status': 'already_solved'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def parse(data):
    return json.loads(data, object_pairs_hook=unique)


def regular(path):
    return stat.S_ISREG(path.lstat().st_mode) and not path.is_symlink()


def safe_root(root):
    need(root.is_dir(), 'root is not directory')
    need(not any(p.is_symlink() for p in (root, *root.parents)), 'symlink in root')


def checked_file(path, pin):
    need(regular(path), 'nonregular external input')
    data = path.read_bytes()
    need(len(data) == pin[0] and digest(data) == pin[1], 'external input pin mismatch')
    return data


def checked_packet(root, expected):
    safe_root(root)
    members = list(root.iterdir())
    need({p.name for p in members} == NAMES, 'independent closed inventory')
    for p in members:
        need(regular(p), 'nonregular packet member')
        checked_file(p, (expected[p.name]['bytes'], expected[p.name]['sha256']))
    need(digest((root / 'MANIFEST.json').read_bytes()) == MANIFEST_PIN, 'independent manifest pin')


def main():
    need(sys.flags.isolated == 1 and sys.flags.no_site == 1, 'run with -I -S')
    need(len(sys.argv) == 3, 'supply artifact directory and original packet directory')
    artifacts, original = (pathlib.Path(x).absolute() for x in sys.argv[1:])
    safe_root(artifacts)
    raw = {name: checked_file(artifacts / (PREFIX + name), pin) for name, pin in PINS.items()}
    metadata = parse(raw['EXTERNAL_MANIFEST.json'])
    need(metadata['manifest_sha256'] == MANIFEST_PIN, 'external manifest binding')
    need(set(metadata['files']) == NAMES, 'external inventory binding')
    checked_packet(original, metadata['files'])
    original_before = {p.name: digest(p.read_bytes()) for p in original.iterdir()}
    receipt = parse(raw['VALIDATION_RECEIPT.json'])
    need(receipt['positive_controls'] == 6 and receipt['negative_controls'] == 22, 'author receipt binding')
    results = []
    with tempfile.TemporaryDirectory(prefix='harmonic_measure_independent_') as temp:
        temp = pathlib.Path(temp)
        relocated = temp / 'relocated'
        relocated.mkdir()
        archive = artifacts / (PREFIX + 'SAFE_FREEZE.zip')
        with zipfile.ZipFile(archive) as z:
            infos = z.infolist()
            need(len(infos) == len(NAMES) and {i.filename for i in infos} == NAMES, 'archive exact inventory')
            for i in infos:
                need(i.filename == pathlib.PurePosixPath(i.filename).name and '\\' not in i.filename, 'unsafe archive name')
                need(not i.is_dir() and stat.S_ISREG(i.external_attr >> 16), 'archive nonregular member')
                data = z.read(i)
                record = metadata['files'][i.filename]
                need(len(data) == record['bytes'] and digest(data) == record['sha256'], 'archive member binding')
                (relocated / i.filename).write_bytes(data)
        checked_packet(relocated, metadata['files'])
        clean = temp / 'clean'
        clean.mkdir()
        boot = clean / (PREFIX + 'BOOTSTRAP.py')
        boot.write_bytes(raw['BOOTSTRAP.py'])
        shadow = temp / 'shadow'
        shadow.mkdir()
        marker = temp / 'UNTRUSTED_CODE_EXECUTED'
        attack = 'open(' + repr(str(marker)) + ', "w").write("UNTRUSTED")\nraise RuntimeError("untrusted code")\n'
        for name in ['json.py', 'hashlib.py', 'pathlib.py', 'subprocess.py', 'sitecustomize.py', 'usercustomize.py']:
            (shadow / name).write_text(attack)
        shadow_boot = shadow / boot.name
        shadow_boot.write_bytes(raw['BOOTSTRAP.py'])

        def run(name, root, optimized=False, good=False, cwd=None, entry=None, flags=None, extra=(), no_root=False):
            entry = entry or boot
            checked_file(entry, PINS['BOOTSTRAP.py'])
            args = [sys.executable, *(flags if flags is not None else ['-I', '-S', '-B'])]
            if optimized:
                args.append('-O')
            args.append(str(entry))
            if not no_root:
                args.append(str(root))
            args.extend(extra)
            env = os.environ.copy()
            if flags is None:
                env['PYTHONPATH'] = str(shadow)
            else:
                env.pop('PYTHONPATH', None)
                env.pop('PYTHONSTARTUP', None)
            proc = subprocess.run(args, cwd=cwd or clean, env=env, text=True, capture_output=True, timeout=30)
            need(not marker.exists(), 'attack code executed')
            if good:
                need(proc.returncode == 0 and not proc.stderr, 'positive control failed: ' + name)
                need(parse(proc.stdout) == EXPECTED_RESULT, 'unexpected result: ' + name)
            else:
                need(proc.returncode == 2 and not proc.stdout and proc.stderr.startswith('REJECT: '), 'negative control failed: ' + name)
            results.append({'name': name, 'optimized': optimized, 'returncode': proc.returncode,
                            'outcome': 'PASS' if good else 'REJECTED_BEFORE_PACKET_EXECUTION',
                            'attack_marker_absent': True})

        for optimized in [False, True]:
            run('original', original, optimized, good=True)
            run('archive_relocation', relocated, optimized, good=True)
            run('import_shadow_cwd_and_PYTHONPATH', relocated, optimized, good=True, cwd=shadow)
            run('import_shadow_entrypoint_directory', relocated, optimized, good=True, cwd=shadow, entry=shadow_boot)
            modes = ['changed_result', 'changed_checker', 'missing_claims', 'extra_file', 'cache_directory',
                     'sourceless_cache', 'symlink_member', 'duplicate_manifest_key', 'changed_claim_rehashed_manifest',
                     'changed_entrypoint_rehashed_manifest', 'wrong_root', 'regular_file_root', 'symlink_root',
                     'symlink_parent', 'extra_argument', 'missing_argument']
            for mode in modes:
                target = temp / ('bad_' + mode + '_' + str(optimized))
                shutil.copytree(relocated, target)
                extra = ()
                no_root = False
                if mode == 'changed_result':
                    (target / 'RESULT.md').write_text('modified mathematical assertion\n')
                elif mode == 'changed_checker':
                    (target / 'verify.py').write_text(attack)
                elif mode == 'missing_claims':
                    (target / 'CLAIMS.json').unlink()
                elif mode == 'extra_file':
                    (target / 'unexpected.py').write_text(attack)
                elif mode == 'cache_directory':
                    (target / '__pycache__').mkdir()
                    (target / '__pycache__' / 'verify.cpython-311.pyc').write_bytes(b'not trusted')
                elif mode == 'sourceless_cache':
                    (target / 'verify.pyc').write_bytes(b'not trusted')
                elif mode == 'symlink_member':
                    (target / 'verify.py').unlink()
                    (target / 'verify.py').symlink_to(relocated / 'verify.py')
                elif mode == 'duplicate_manifest_key':
                    p = target / 'MANIFEST.json'
                    p.write_text(p.read_text().replace('"schema": 1', '"schema": 1, "schema": 1'))
                elif mode in ['changed_claim_rehashed_manifest', 'changed_entrypoint_rehashed_manifest']:
                    p = target / ('CLAIMS.json' if mode.startswith('changed_claim') else 'verify.py')
                    if p.name == 'CLAIMS.json':
                        obj = parse(p.read_bytes())
                        obj['new_solution'] = True
                        p.write_text(json.dumps(obj))
                    else:
                        p.write_text(attack)
                    m = parse((target / 'MANIFEST.json').read_bytes())
                    m['files'][p.name] = {'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}
                    (target / 'MANIFEST.json').write_text(json.dumps(m))
                elif mode == 'wrong_root':
                    target = clean
                elif mode == 'regular_file_root':
                    target = relocated / 'RESULT.md'
                elif mode == 'symlink_root':
                    link = temp / ('root_link_' + str(optimized))
                    link.symlink_to(target, target_is_directory=True)
                    target = link
                elif mode == 'symlink_parent':
                    parent = temp / ('parent_link_' + str(optimized))
                    parent.symlink_to(temp, target_is_directory=True)
                    target = parent / target.name
                elif mode == 'extra_argument':
                    extra = ('unexpected_argument',)
                elif mode == 'missing_argument':
                    no_root = True
                run(mode, target, optimized, extra=extra, no_root=no_root)
            for label, flags in [('missing_I_and_S', ['-B']), ('missing_I', ['-S', '-B']), ('missing_S', ['-I', '-B'])]:
                run(label, relocated, optimized, flags=flags)
        need(not any(p.name == '__pycache__' or p.suffix == '.pyc' for p in relocated.rglob('*')), 'replay generated cache')
    checked_packet(original, metadata['files'])
    need({p.name: digest(p.read_bytes()) for p in original.iterdir()} == original_before, 'original changed')
    for name, pin in PINS.items():
        checked_file(artifacts / (PREFIX + name), pin)
    print(json.dumps({'schema': 1, 'problem_id': 2303021, 'result': 'PASS',
        'author_archive_sha256': PINS['SAFE_FREEZE.zip'][1], 'author_manifest_sha256': MANIFEST_PIN,
        'positive_controls': sum(x['outcome'] == 'PASS' for x in results),
        'negative_controls': sum(x['outcome'] != 'PASS' for x in results),
        'controls': results, 'original_preserved': True, 'all_executed_author_code_externally_pinned': True,
        'isolated_execution': '-I -S -B, additionally -O in optimized cases',
        'direct_packet_entrypoint_is_not_trusted_gate': True, 'formal_mathematical_proof': False,
        'concurrent_hostile_filesystem_writer_model': 'not claimed'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        print('REJECT: ' + str(exc), file=sys.stderr)
        sys.exit(2)
