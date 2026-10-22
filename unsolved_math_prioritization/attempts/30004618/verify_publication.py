#!/usr/bin/env python3
"""Strict offline integrity and exact arithmetic replay, not a Kodaira computation."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
PINS = [
 ('author', 'odd_strata_30004618', 'odd_strata_30004618_frozen.zip', 18469,
  '62ee95de99e41e97f54a2f1bdad0623fab43d8317296a471145d0a764bbe169a',
  '96c5ef2a3ef324896d96c1419d37ccd695290275f4db79e9a598a027925e2b56'),
 ('independent_audit', 'odd_strata_30004618_independent_audit',
  'odd_strata_30004618_independent_audit_frozen.zip', 14643,
  '800e02f8b16faa92e20d96bb28fd711b2ef7eef163e65414c666ae395da338f3',
  '64add66350b612bb74e06a3c8882a2c6abd790bde13bdc8663e286ae39ff1e27'),
]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def safe_path(name):
    p = PurePosixPath(name)
    require(bool(name) and not p.is_absolute() and '..' not in p.parts
            and '.' not in p.parts and str(p) == name and '\\' not in name,
            'Unsafe path: ' + name)

def files(root):
    result = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symlink rejected')
        if p.is_file():
            require(stat.S_ISREG(p.stat().st_mode), 'Nonregular file rejected')
            result.add(p.relative_to(root).as_posix())
        else:
            require(p.is_dir(), 'Nonregular entry rejected')
    return result

def manifest_check(root, name):
    entries = json.loads((root/name).read_text())['files']
    names = [e['path'] for e in entries]
    require(len(names) == len(set(names)) and name not in names, 'Manifest paths invalid')
    for e in entries:
        safe_path(e['path'])
        b = (root/e['path']).read_bytes()
        require(len(b) == e['bytes'] and sha(b) == e['sha256'], 'Hash/size mismatch: '+e['path'])
    require(files(root) == set(names)|{name}, 'Closed recursive file inventory mismatch')
    expected = {str(p) for n in names for p in PurePosixPath(n).parents if str(p) != '.'}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
    require(actual == expected, 'Closed recursive directory inventory mismatch')
    return len(names)+1

def replay(root, kind):
    script, saved = ('verify.py','RESULTS.json') if kind == 'author' else ('independent_check.py','INDEPENDENT_RESULTS.json')
    before = {n: (root/n).read_bytes() for n in files(root)}
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    code = 'import runpy,sys; assert __debug__; runpy.run_path(sys.argv[1], run_name="__main__")'
    run = subprocess.run([sys.executable, '-I', '-B', '-c', code, str(root/script)],
                         cwd=root, env=env, text=True, capture_output=True, check=True)
    result = json.loads(run.stdout)
    require(result == json.loads(before[saved]), 'Replay output differs from frozen result')
    require(not result['full_problem_solved'], 'Replay scope widened')
    require(before == {n:(root/n).read_bytes() for n in files(root)}, 'Replay changed frozen bytes')
    return dict(script=script, exit_code=0, assertions_active=True,
                matches_frozen_result=True, stdout_sha256=sha(run.stdout.encode()))

def main():
    require(__debug__, 'Run without -O: assertion checks must remain active')
    count = manifest_check(ROOT, 'PUBLICATION_MANIFEST.json')
    s = json.loads((ROOT/'PUBLICATION_STATUS.json').read_text())
    require(s['problem_id']==30004618 and s['rank']==781, 'Wrong target')
    require(s['status']=='unsolved' and s['turns']=='5/5' and s['budget_exhausted'], 'Wrong disposition')
    require(s['substantive_approaches']==5 and s['duplicate_id']==30004619, 'Budget or duplicate changed')
    for k in ['full_problem_solved','full_spin_smoothing_independently_established','non_bigness_proved',
              'general_type_conjecture_refuted','human_peer_review','novelty_claim']:
        require(s[k] is False, 'Scope widened: '+k)
    require(s['raw_w_gamma_strict_improvement']=='470/9963'
            and s['lambda12_normalized_w_b_strict_improvement']=='16544/29889'
            and s['genus13_control_classes']=='W_mid and 2 BN', 'Clarification changed')
    require(s['review_hash']=='fce1058dfb86fd826a06545d85e42203a444feff1471695a483935923a2cd8c6', 'Review hash changed')
    results=[]
    with tempfile.TemporaryDirectory(prefix='odd-strata-replay-') as temp:
        for folder,prefix,archive,size,ah,mh in PINS:
            b=(ROOT/archive).read_bytes()
            require(len(b)==size and sha(b)==ah, 'Frozen ZIP changed')
            source=ROOT/folder
            require(sha((source/'MANIFEST.json').read_bytes())==mh, 'Frozen manifest changed')
            require(manifest_check(source,'MANIFEST.json')==8, 'Wrong frozen inventory')
            target=Path(temp)/folder;target.mkdir()
            with zipfile.ZipFile(ROOT/archive) as z:
                infos=z.infolist();names=[i.filename for i in infos]
                require(len(names)==len(set(names))==8, 'ZIP member count mismatch')
                require(set(names)=={prefix+'/'+n for n in files(source)}, 'ZIP membership mismatch')
                for info in infos:
                    safe_path(info.filename)
                    name=PurePosixPath(info.filename).name
                    require(info.filename==prefix+'/'+name and not info.is_dir()
                            and not stat.S_ISLNK(info.external_attr>>16), 'Unsafe ZIP member')
                    content=z.read(info)
                    require(content==(source/name).read_bytes(), 'ZIP member bytes differ')
                    (target/name).write_bytes(content)
            results.append(dict(directory=folder,archive_sha256=ah,manifest_sha256=mh,
                                normal_replay=replay(source,folder),clean_zip_replay=replay(target,folder)))
    require(manifest_check(ROOT,'PUBLICATION_MANIFEST.json')==count, 'Replay altered package')
    print(json.dumps(dict(status='PASS',problem_id=30004618,files_including_manifest=count,
                         closed_recursive_inventory=True,assertions_active=True,results=results,
                         full_problem_solved=False,
                         scope='Frozen-package integrity and exact arithmetic; no full geometry or Kodaira-dimension verification.'),
                     indent=2,sort_keys=True))

if __name__=='__main__':
    main()
