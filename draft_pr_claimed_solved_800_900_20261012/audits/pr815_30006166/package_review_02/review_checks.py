"""Fresh read-only artifact checks and disposable finite replay; no theorem certification."""
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sqlite3
import stat
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = AUDIT.parents[2]
PRE = AUDIT / 'preprint'
OUTER = AUDIT.parents[1] / 'work/pr815_revision_r1b'
HEAD = '5bee5139501a399da653f634147eab9433774ac7'
COMMIT = '9fed4b0d038281cd4145fdc40dbc3a8a86618b99'
MAIN = '615332755152f8ce12ece98c2b74e3e359166e9d'
PREFIX = 'unsolved_math_prioritization/attempts/30006166/'
PIN = '04575e83242d31ac08338cda2e1e810d917b54092f2cc8f32d310eb3f8d8b8d3'
OUTER_PIN = 'f1b7993fd3c2a056da0e97e38711d30f194a481c8ed29c9b50ffea954d5e8fd7'


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def unique(pairs):
    d = {}
    for k, v in pairs:
        require(k not in d, 'duplicate JSON key')
        d[k] = v
    return d


def decode(raw):
    return json.loads(raw, object_pairs_hook=unique)


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def git(*args):
    return subprocess.run(['git', *args], cwd=REPO, check=True, capture_output=True).stdout


def core():
    seal = decode((AUDIT / 'PACKAGE_SEAL_R2.json').read_bytes())
    actual = []
    for row in seal['core_files']:
        p = PRE / row['path']
        require(stat.S_ISREG(p.lstat().st_mode), 'core regular file')
        raw = p.read_bytes()
        item = dict(path=row['path'], bytes=len(raw), sha256=sha(raw))
        require(item == row, 'R2 core mismatch')
        actual.append(item)
    require(len(actual) == 10, 'ten core files')
    require(sha((OUTER / 'PUBLICATION_MANIFEST.json').read_bytes()) == OUTER_PIN,
            'outer pin')
    return actual


def static():
    original = decode((AUDIT / 'SOURCE_MANIFEST.json').read_bytes())
    require(original['source_head'] == HEAD and len(original['files']) == 61,
            'original exact head/count')
    for row in original['files']:
        raw = (AUDIT / row['path']).read_bytes()
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'original binding')
        require(git('show', HEAD + ':' + row['repo_path']) == raw, 'original Git bytes')
        require(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
                == row['git_blob_sha'], 'original Git blob identity')
    all_members = {}
    with zipfile.ZipFile(PRE / 'verification.zip') as z:
        require(z.testzip() is None, 'ZIP CRC')
        for i in z.infolist():
            n = PurePosixPath(i.filename)
            require(i.filename == str(n) and not n.is_absolute() and '..' not in n.parts
                    and '\\' not in i.filename and not i.is_dir()
                    and stat.S_ISREG(i.external_attr >> 16), 'safe regular ZIP member')
            require(i.filename not in all_members, 'unique ZIP member')
            raw = z.read(i)
            if i.filename.endswith('.json'):
                decode(raw)
            all_members[i.filename] = raw
    require(len(all_members) == 121, '121 closed members')
    require(sha(all_members['package_index.json']) == PIN, 'index pin')
    index = decode(all_members['package_index.json'])
    require(set(all_members) == {'package_index.json'} | {r['path'] for r in index['files']},
            'index closed')
    for row in index['files']:
        raw = all_members[row['path']]
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'indexed member')
    for row in original['files']:
        require(all_members[row['path']] == (AUDIT / row['path']).read_bytes(),
                'all frozen original files in ZIP')
    for n in ['note.tex', 'README.md', 'metadata.json', 'CURRENT_PRIORITY.md',
              'verify_package.py', 'package_index.json']:
        require(all_members[n] == (PRE / n).read_bytes(), 'current archive identity')
    require(all_members['note.pdf'] == (PRE / 'output/pdf/note.pdf').read_bytes(), 'current PDF')
    metadata = decode((PRE / 'metadata.json').read_bytes())
    kit = decode((PRE / 'zenodo-deposit.json').read_bytes())
    require(metadata == kit['metadata'] == decode(all_members['metadata.json']), 'exact metadata')
    for f in kit['files']:
        require((PRE / f['path']).is_file(), 'upload file present')
    mapping = decode((AUDIT / 'PREPARED_PR_MAPPING_R1.json').read_bytes())
    require(mapping['expected_head'] == HEAD and mapping['original_turns'] == '3/5', 'mapping gate')
    require(len(mapping['files']) == 192, 'mapping count')
    mapped = set()
    for r in mapping['files']:
        require(r['repo_path'].startswith(PREFIX), 'target-only mapping')
        require(r['repo_path'] not in mapped, 'unique mapping')
        mapped.add(r['repo_path'])
        p = Path(r['local_path'])
        require(p.is_relative_to(OUTER) and stat.S_ISREG(p.lstat().st_mode), 'r1b map input')
        raw = p.read_bytes()
        require(sha(raw) == r['sha256'] and git('show', COMMIT + ':' + r['repo_path']) == raw,
                'prepared commit mapped bytes')
    commit_paths = set(git('ls-tree', '-r', '--name-only', COMMIT, '--', PREFIX).decode().splitlines())
    require(commit_paths == mapped, 'prepared target tree closed')
    changed = git('diff', '--name-only', MAIN, COMMIT).decode().splitlines()
    require(all(p.startswith(PREFIX) or p == 'unsolved_math_prioritization/QUEUE.md'
                for p in changed), 'prepared commit changed only target and queue')
    queue_main = git('show', MAIN + ':unsolved_math_prioritization/QUEUE.md').splitlines(keepends=True)
    queue_new = git('show', COMMIT + ':unsolved_math_prioritization/QUEUE.md').splitlines(keepends=True)
    selected = lambda lines: [r for r in lines if b'30006166 / OWR-14299082-012' in r]
    require(len(selected(queue_main)) == len(selected(queue_new)) == 1, 'one queue target')
    require([r for r in queue_main if r not in selected(queue_main)]
            == [r for r in queue_new if r not in selected(queue_new)], 'non-target QUEUE bytes')
    require(b'claimed_solved' in selected(queue_new)[0] and b'3/5' in selected(queue_new)[0],
            'prepared queue exact status and budget')
    c = sqlite3.connect('file:' + str(REPO / 'unsolved_math_prioritization/cache/catalog.sqlite')
                        + '?mode=ro', uri=True)
    payload, report = c.execute('select payload,report from records where key=?', ('30006166',)).fetchone()
    p, prior = decode(payload), decode(report)
    require(prior == {}, 'empty prior report')
    statement = sha(p['statement'].encode())
    review = sha(json.dumps([p, prior], sort_keys=True).encode())
    require(statement == '33441e0172f1653aaa85c1528ce39b90030aec6726589b622a2511fbf5f0c597'
            and review == 'db8ab75699d8f143e031873e1d7326fad1d0d6fbd8b637b59a82bd2c63793f91',
            'complete target fingerprints')
    c.close()
    result = {'original_files_compared_to_frozen_git': 61, 'closed_archive_members': 121,
              'unique_json_keys_checked': True, 'exact_metadata_equality': True,
              'original_zip_members_verified_by_full_replay': 51,
              'mapping_entries': 192, 'prepared_commit': COMMIT, 'main_base': MAIN,
              'prepared_commit_target_tree_closed': True, 'all_mapped_commit_bytes_equal': True,
              'non_target_queue_bytes_preserved': True, 'statement_sha256': statement,
              'review_hash': review, 'empty_prior_report': True,
              'outer_manifest_sha256': OUTER_PIN, 'core_files': core(),
              'infinite_theorem_verified_by_program': False}
    save('STATIC_CHECKS.json', result)
    return all_members


def replay(members):
    # TMPDIR confines all integrity-suite transient mutations to this review.
    private = HERE / 'private_sources'
    env = dict(os.environ, TMPDIR=str(private), PYTHONDONTWRITEBYTECODE='1')
    outputs = {}
    with tempfile.TemporaryDirectory(prefix='audit replay with spaces ', dir=private) as temp:
        root = Path(temp)
        extracted = root / 'extracted package'
        extracted.mkdir()
        for n, raw in members.items():
            p = extracted / n
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
        outer = root / 'assembled repository'
        shutil.copytree(OUTER, outer)
        for kind, tree, verifier, pin in [('inner', extracted, 'verify_package.py', PIN),
                                           ('outer', outer, 'verify_publication.py', OUTER_PIN)]:
            stdout = []
            for optimized in (False, True):
                flags = ['-I', '-B'] + (['-O'] if optimized else [])
                r = subprocess.run([sys.executable, *flags, str(tree / verifier), pin, '--full'],
                                   cwd='/', env=env, capture_output=True, text=True, timeout=900)
                require(r.returncode == 0, kind + ' full replay: ' + r.stderr)
                value = decode(r.stdout)
                save(kind.upper() + ('_OPTIMIZED.json' if optimized else '_NORMAL.json'), value)
                stdout.append(r.stdout)
            require(stdout[0] == stdout[1], kind + ' optimized stdout')
            require(not list(tree.rglob('__pycache__')), kind + ' cache absent')
            outputs[kind] = decode(stdout[0])
        require(outputs['outer']['inner'] == outputs['inner'], 'inner outer semantic equality')
        cases = ['bad_pin', 'tampered_note', 'missing_file', 'extra_file', 'empty_directory',
                 'bytecode_directory', 'symlink', 'fifo']
        rows = []
        for case in cases:
            trial = root / ('trial ' + case)
            shutil.copytree(extracted, trial)
            if case == 'tampered_note':
                (trial / 'note.tex').write_bytes((trial / 'note.tex').read_bytes() + b'\n')
            elif case == 'missing_file':
                (trial / 'README.md').unlink()
            elif case == 'extra_file':
                (trial / 'extra').write_bytes(b'new')
            elif case in ['empty_directory', 'bytecode_directory']:
                (trial / ('empty' if case == 'empty_directory' else '__pycache__')).mkdir()
            elif case in ['symlink', 'fifo']:
                f = trial / 'README.md'
                f.unlink()
                if case == 'symlink':
                    f.symlink_to(extracted / 'README.md')
                else:
                    os.mkfifo(f)
            for optimized in (False, True):
                flags = ['-I', '-B'] + (['-O'] if optimized else [])
                pin = '0' * 64 if case == 'bad_pin' else PIN
                r = subprocess.run([sys.executable, *flags, str(trial / 'verify_package.py'), pin],
                                   cwd='/', env=env, capture_output=True, text=True, timeout=30)
                require(r.returncode != 0, 'fresh mutation escaped')
                rows.append({'case': case, 'optimized': optimized, 'rejected': True})
        save('FRESH_INTEGRITY_CONTROLS.json', {'rejections': len(rows), 'cases': rows})
    save('REPLAY_SUMMARY.json', {'normal_optimized_stdout_equal': True,
                               'inner_outer_results_equal': True, 'historical_rejections': 68,
                               'fresh_rejections': 16, 'source_cache_created': False,
                               'normal_inner_regular_files': outputs['inner']['regular_files'],
                               'normal_outer_regular_files': outputs['outer']['regular_files'],
                               'infinite_theorem_verified_by_program': False})


if __name__ == '__main__':
    members = static()
    print('Fresh static identity and prepared-commit checks passed.', flush=True)
    replay(members)
    core()
    print('Full inner/outer normal/optimized replay and fresh integrity controls passed.', flush=True)
