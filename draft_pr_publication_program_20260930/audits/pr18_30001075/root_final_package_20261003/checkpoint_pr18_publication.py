"""Checkpoint only PR18 publication evidence and the exact Zenodo adapter repair."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

if sys.flags.optimize or sys.argv[1:] != ['--exclusive-window-confirmed']:
    raise RuntimeError('Requires the confirmed shared Git writer window')
own = Path(__file__).resolve().parent
a18 = own.parent
program = a18.parents[1]
repo = program.parent
def git(*args):
    return subprocess.run(['git', *args], cwd=repo, capture_output=True, check=True).stdout
def sha(body):
    return hashlib.sha256(body).hexdigest()
if git('branch', '--show-current').strip() != b'main' or git('diff', '--cached', '--name-only').strip():
    raise RuntimeError('Requires main with a clean real index; preserve foreign staging')
base = git('rev-parse', 'HEAD').decode().strip()
if git('ls-remote', '--heads', 'origin', 'main').decode().split()[0] != base:
    raise RuntimeError('Local and remote main must agree')
selected = set()
def add(p):
    if p.is_symlink() or not stat.S_ISREG(p.lstat().st_mode):
        raise RuntimeError('Nonregular selected path: '+str(p))
    selected.add(p.relative_to(repo).as_posix())
for p in [program/'RESEARCH_LOG.md', a18/'RESEARCH_LOG.md']:
    add(p)
for folder in [own, a18/'publication']:
    for p in folder.iterdir():
        if p.is_file() and p.name != 'PUBLICATION_CHECKPOINT_RESULT.json':
            add(p)
family = a18/'preprint_round2_adversary_family'
for p in family.rglob('*'):
    parts = p.relative_to(family).parts
    if p.is_file() and parts[0] not in ('tmp', 'reproduction'):
        add(p)
for name in ['README.md', 'test_zenodo.py', 'zenodo.py']:
    add(repo/'zenodo_deposit_tool'/name)
for folder in (program/'audits/pr45_9900007').glob('root_pr18_*_actual_capture'):
    for p in folder.iterdir():
        if p.is_file():
            add(p)
publication = json.loads((a18/'publication/PUBLICATION_VERIFICATION.json').read_bytes())
if publication['published'] is not True or publication['all_public_bytes_identical'] is not True or publication['DOI'] != '10.5281/zenodo.23127955':
    raise RuntimeError('Publication readback does not match')
paths = sorted(selected)
selected_bytes = {p.encode() for p in paths}
work_pins = {p:sha((repo/p).read_bytes()) for p in paths}
def foreign_index():
    return b'\0'.join(entry for entry in git('ls-files', '--stage', '-z').split(b'\0')
                      if entry and entry.split(b'\t',1)[1] not in selected_bytes)
before = foreign_index()
if git('rev-parse','HEAD').decode().strip() != base:
    raise RuntimeError('Main moved before staging')
git('add', '--', *paths)
if foreign_index() != before or git('rev-parse','HEAD').decode().strip() != base:
    raise RuntimeError('Foreign index or main changed')
git('commit', '--only', '-m', 'Publish PR18 reviewed nullness preprint and verify exact public files', '--', *paths)
commit = git('rev-parse','HEAD').decode().strip()
changed = set(git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0'))-{b''}
if not changed <= selected_bytes or git('rev-parse',commit+'^').decode().strip() != base:
    raise RuntimeError('Unexpected commit scope or parent')
if foreign_index() != before or any(sha((repo/p).read_bytes()) != h for p,h in work_pins.items()):
    raise RuntimeError('Selected work or foreign index drift')
git('push','origin','main')
remote = git('ls-remote','--heads','origin','main').decode().split()[0]
if remote != commit or foreign_index() != before:
    raise RuntimeError('Remote or foreign index readback mismatch')
record = {'UTC':dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_pid':os.getpid(),
          'base':base,'commit':commit,'remote_main':remote,'selected_files':len(paths),
          'changed_files':len(changed),'foreign_index_unchanged':True,
          'foreign_index_sha256':sha(before),'work_pins':work_pins,
          'workflow_percent':95,'final_review_loop_complete':True,
          'native_acceptance':False,'publication':True,'DOI':publication['DOI'],
          'tracker_row_written':False}
(own/'PUBLICATION_CHECKPOINT_RESULT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k != 'work_pins'},indent=2))
