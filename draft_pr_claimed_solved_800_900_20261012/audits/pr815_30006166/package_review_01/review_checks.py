"""Read-only package inspection and replay in disposable copies; no theorem certification."""
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
PREPRINT = AUDIT / 'preprint'
TMP = HERE / 'tmp'


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def load(path):
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def static_and_extract():
    seal = load(AUDIT / 'PACKAGE_SEAL_R1.json')
    need(seal['frozen_original_head'] == '5bee5139501a399da653f634147eab9433774ac7', 'exact PR head')
    for row in seal['core_files']:
        raw = (PREPRINT / row['path']).read_bytes()
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'core seal: ' + row['path'])
    metadata = load(PREPRINT / 'metadata.json')
    deposit = load(PREPRINT / 'zenodo-deposit.json')
    need(deposit['metadata'] == metadata, 'upload metadata exactness')
    need(deposit['files'] == [
        {'path': 'output/pdf/note.pdf', 'name': 'generic-wreath-hyperfiniteness-note.pdf'},
        {'path': 'verification.zip', 'name': 'generic-wreath-hyperfiniteness-verification.zip'}], 'deposit destinations')
    source = load(AUDIT / 'SOURCE_MANIFEST.json')
    for row in source['files']:
        raw = (AUDIT / row['path']).read_bytes()
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'frozen original bytes')
        need(hashlib.sha1(('blob ' + str(len(raw)) + '\0').encode() + raw).hexdigest() == row['git_blob_sha'], 'Git blob identity')
        frozen = subprocess.run(['git', 'show', source['source_head'] + ':' + row['repo_path']],
                                cwd='/Users/alec/Documents/Math', capture_output=True, check=True).stdout
        need(frozen == raw, 'original frozen commit file identity')
    need(len(source['files']) == 61, 'original 61 files')
    index = load(PREPRINT / 'package_index.json')
    need(index['source_head'] == source['source_head'] == seal['frozen_original_head'], 'matching head')
    rows = index['files']
    names = {row['path'] for row in rows} | {'package_index.json'}
    need(len(names) == len(rows) + 1 == 121, '121 unique closed members')
    clean = TMP / 'relocated empty package with spaces'
    need(not clean.exists(), 'disposable extraction must be fresh')
    clean.mkdir(parents=True)
    scripts = []
    with zipfile.ZipFile(PREPRINT / 'verification.zip') as z:
        entries = z.infolist()
        need(len(entries) == len(names) and {i.filename for i in entries} == names, 'archive exact inventory')
        need(z.testzip() is None, 'ZIP CRC')
        for info in entries:
            p = PurePosixPath(info.filename)
            need(str(p) == info.filename and not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename,
                 'safe ZIP path')
            need(stat.S_ISREG(info.external_attr >> 16) and not info.is_dir(), 'regular ZIP member')
            need(not any(x in p.parts for x in ('private_sources', 'tmp', '__pycache__')), 'private/generated path excluded')
            raw = z.read(info)
            if info.filename == 'package_index.json':
                need(raw == (PREPRINT / 'package_index.json').read_bytes(), 'index archive identity')
            else:
                row = next(r for r in rows if r['path'] == info.filename)
                need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'indexed archive payload')
            if info.filename.startswith('source/'):
                need(raw == (AUDIT / info.filename).read_bytes(), 'original archive preservation')
            if info.filename in {'note.tex', 'README.md', 'CURRENT_PRIORITY.md', 'metadata.json', 'verify_package.py'}:
                need(raw == (PREPRINT / info.filename).read_bytes(), 'current core archive identity')
            if info.filename == 'note.pdf':
                need(raw == (PREPRINT / 'output/pdf/note.pdf').read_bytes(), 'PDF archive identity')
            if info.filename.endswith('.py'):
                tree = ast.parse(raw, filename=info.filename)
                scripts.append({'path': info.filename, 'sha256': sha(raw), 'lines': len(raw.splitlines()),
                                'assert_nodes': sum(isinstance(x, ast.Assert) for x in ast.walk(tree)),
                                'imports': sorted({x.name for n in ast.walk(tree) if isinstance(n, ast.Import) for x in n.names}
                                                  | {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)})})
            if info.filename.endswith('.json'):
                json.loads(raw, object_pairs_hook=unique)
            output = clean / p
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(raw)
    for relative in ('checks.py', 'verify.py', 'integrity_tests.py'):
        need((clean / 'source/author' / relative).read_bytes() == (clean / 'source/audit_bundle/author' / relative).read_bytes(),
             'duplicate author script identity')
    original = load(clean / 'source/PUBLICATION_METADATA.json')
    nested = 0
    for record in original['archives']:
        with zipfile.ZipFile(clean / 'source' / record['path']) as z:
            need(len(z.infolist()) == record['regular_members'], 'original ZIP count')
            for entry in z.infolist():
                need(z.read(entry) == (clean / 'source' / record['extract_root'] / entry.filename).read_bytes(), 'original extracted ZIP identity')
                nested += 1
    need(nested == 51 and len(original['archives']) == 3, '3 ZIP/51 member total')
    save('STATIC_PACKAGE_CHECKS.json', {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'core_files': seal['core_files'], 'metadata_exact': True, 'members': len(names),
        'original_files_preserved': len(source['files']), 'original_zip_count': 3, 'original_zip_members': nested,
        'git_blob_identities_checked': 61, 'frozen_commit_files_compared': 61,
        'archive_crc_ok': True, 'archive_index_identity': True,
        'current_core_archive_identity': True, 'downloaded_primary_content_distributed': False,
        'all_json_unique_keys': True, 'scripts': scripts, 'infinite_theorem_verified_by_program': False})
    return clean, sha((PREPRINT / 'package_index.json').read_bytes())


def replay(clean, pin):
    sandbox_tmp = TMP / 'nested_test_scratch'
    sandbox_tmp.mkdir(exist_ok=True)
    environment = dict(os.environ, TMPDIR=str(sandbox_tmp), PYTHONDONTWRITEBYTECODE='1')
    outputs = []
    for optimized in (False, True):
        command = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(clean / 'verify_package.py'), pin, '--full']
        run = subprocess.run(command, cwd='/', env=environment, text=True, capture_output=True, timeout=900)
        need(run.returncode == 0, 'portable replay: ' + run.stderr)
        result = json.loads(run.stdout, object_pairs_hook=unique)
        need(result['regular_files'] == 121 and result['infinite_theorem_verified_by_program'] is False, 'replay scope')
        save('REPLAY_OPTIMIZED.json' if optimized else 'REPLAY_NORMAL.json', result)
        outputs.append(run.stdout)
    need(outputs[0] == outputs[1], 'normal and optimized exact output')
    need(not list(clean.rglob('__pycache__')), 'bytecode cache created')
    save('REPLAY_COMPARISON.json', {'normal_passed': True, 'optimized_passed': True,
        'exact_stdout_equal': True, 'sha256': sha(outputs[0].encode()), 'cwd': '/',
        'relocated_path_contains_spaces': True, 'cache_created': False,
        'infinite_theorem_verified_by_program': False})


def adversarial_inventory_controls(clean, pin):
    rows = []
    cases = ['wrong_external_pin', 'changed_note', 'missing_member', 'extra_file',
             'empty_directory', 'bytecode_directory', 'symlink_member', 'fifo_member']
    for case in cases:
        trial = TMP / ('inventory_attack_' + case)
        shutil.copytree(clean, trial)
        chosen_pin = pin
        if case == 'wrong_external_pin':
            chosen_pin = '0' * 64
        elif case == 'changed_note':
            with (trial / 'note.tex').open('a') as f:
                f.write('\n% diagnostic modification\n')
        elif case == 'missing_member':
            (trial / 'README.md').unlink()
        elif case == 'extra_file':
            (trial / 'unindexed.txt').write_text('diagnostic')
        elif case == 'empty_directory':
            (trial / 'unindexed_directory').mkdir()
        elif case == 'bytecode_directory':
            (trial / '__pycache__').mkdir()
            (trial / '__pycache__/verify_package.pyc').write_bytes(b'not executable bytecode')
        elif case == 'symlink_member':
            (trial / 'README.md').unlink()
            (trial / 'README.md').symlink_to(clean / 'README.md')
        elif case == 'fifo_member':
            (trial / 'README.md').unlink()
            os.mkfifo(trial / 'README.md')
        for optimized in (False, True):
            command = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(trial / 'verify_package.py'), chosen_pin]
            run = subprocess.run(command, cwd='/', capture_output=True, text=True, timeout=15)
            need(run.returncode != 0, 'inventory attack accepted: ' + case)
            rows.append({'case': case, 'mode': 'optimized' if optimized else 'normal',
                         'rejected': True, 'exit_code': run.returncode})
        shutil.rmtree(trial)
    save('ADVERSARIAL_INVENTORY_CONTROLS.json', {'cases': len(cases), 'rejections': len(rows),
        'rows': rows, 'mutations_only_disposable_copies': True,
        'scope': 'integrity behavior only, not mathematical or priority verification'})


if __name__ == '__main__':
    clean, pin = static_and_extract()
    print('Static package inspection passed; starting disposable replay.', flush=True)
    replay(clean, pin)
    adversarial_inventory_controls(clean, pin)
    print('Normal and optimized portable replays passed with exactly equal output.', flush=True)
