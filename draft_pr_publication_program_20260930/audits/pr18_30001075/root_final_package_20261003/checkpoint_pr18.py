"""Selected-path PR18 checkpoint during a coordinated exclusive writer window."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

if sys.flags.optimize or sys.argv[1:] != ['--exclusive-window-confirmed']:
    raise RuntimeError('ROOT must first obtain the shared writer window')
own = Path(__file__).resolve().parent
a18 = own.parent
program = a18.parents[1]
repo = program.parent
def git(*args):
    return subprocess.run(['git',*args],cwd=repo,capture_output=True,check=True).stdout
def sha(body):
    return hashlib.sha256(body).hexdigest()
def ordinary(p):
    return stat.S_ISREG(p.lstat().st_mode) and not p.is_symlink()
if git('branch','--show-current').strip() != b'main':
    raise RuntimeError('Requires main')
base = git('rev-parse','HEAD').decode().strip()
selected = set()
def add(p):
    if not ordinary(p):
        raise RuntimeError('Nonregular selected path: '+str(p))
    selected.add(p.relative_to(repo).as_posix())
for p in [program/'RESEARCH_LOG.md',a18/'RESEARCH_LOG.md',
          a18/'ROOT_CURRENT_PRIORITY_ASSESSMENT_20261003.json',
          a18/'ROOT_CURRENT_PRIORITY_ASSESSMENT_20261003.md']:
    add(p)
for folder in [a18/'preprint_v1',a18/'native_acceptance_plan_20261003']:
    for p in folder.rglob('*'):
        if p.is_file():
            add(p)
family = (a18/'preprint_round1_adversary_family').relative_to(repo).as_posix()
for raw in git('ls-files','--others','--exclude-standard','-z','--',family).split(b'\0'):
    if raw:
        add(repo/raw.decode())
for folder in [own,a18/'root_priority_fulltext_20261003',
               a18/'priority_mechanism_revisit_20261003/full_article_followup_20261003']:
    for p in folder.iterdir():
        if p.is_file() and p.name != 'CHECKPOINT_RESULT.json':
            add(p)
access = a18/'priority_access_revisit_20261003'
m = json.loads((access/'SOURCE_MANIFEST.json').read_bytes())
for item in m['payloads']:
    p = access/item['path']
    if sha(p.read_bytes()) != item['sha256']:
        raise RuntimeError('Closed source payload changed: '+str(p))
    add(p)
for name in ['SOURCE_MANIFEST.json','SOURCE_READY.json','INDEX.json']:
    add(access/name)
captures = program/'audits/pr45_9900007'
for folder in captures.glob('root_pr18_*_actual_capture'):
    for p in folder.iterdir():
        if p.is_file():
            add(p)
paths = sorted(selected)
selected_bytes = {p.encode() for p in paths}
work_pins = {p:sha((repo/p).read_bytes()) for p in paths}
def foreign_index():
    return b'\0'.join(entry for entry in git('ls-files','--stage','-z').split(b'\0')
                      if entry and entry.split(b'\t',1)[1] not in selected_bytes)
before = foreign_index()
if git('rev-parse','HEAD').decode().strip() != base:
    raise RuntimeError('Main changed before staging')
git('add','--',*paths)
if foreign_index() != before or git('rev-parse','HEAD').decode().strip() != base:
    raise RuntimeError('Foreign index or main changed; stop')
git('commit','--only','-m','Prepare PR18 nullness preprint and complete priority-source audit','--',*paths)
commit = git('rev-parse','HEAD').decode().strip()
changed = set(git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0'))-{b''}
if not changed <= selected_bytes or git('rev-parse',commit+'^').decode().strip() != base:
    raise RuntimeError('Unexpected checkpoint commit scope or parent; stop before push')
if foreign_index() != before or any(sha((repo/p).read_bytes()) != h for p,h in work_pins.items()):
    raise RuntimeError('Foreign index or selected work drift; stop before push')
git('push','origin','main')
remote = git('ls-remote','--heads','origin','main').decode().split()[0]
if remote != commit or foreign_index() != before:
    raise RuntimeError('Remote/index readback mismatch')
record = {'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
          'base':base,'commit':commit,'remote_main':remote,'selected_files':len(paths),
          'changed_files':len(changed),'foreign_index_unchanged':True,
          'foreign_index_sha256':sha(before),'work_pins':work_pins,
          'workflow_percent':75,'final_review_loop_complete':False,
          'native_acceptance':False,'publication':False}
(own/'CHECKPOINT_RESULT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='work_pins'},indent=2))
