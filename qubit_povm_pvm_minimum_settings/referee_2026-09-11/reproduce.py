#!/usr/bin/env python3
"""Fresh Bell source build, reusing explicitly trusted pinned dependency cache."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'bell_lean'
WORK = HERE / 'work' / 'bell_lean'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
if WORK.exists():
    raise SystemExit('Work copy already exists; preserve it and choose a new audit folder for a new run.')
WORK.mkdir(parents=True)
for name in ['Bell', 'validation', 'scripts', 'environment', 'certificates', 'source']:
    shutil.copytree(SOURCE/name, WORK/name, ignore=shutil.ignore_patterns('__pycache__'))
for name in ['Bell.lean', 'lakefile.toml', 'lake-manifest.json', 'lean-toolchain']:
    shutil.copy2(SOURCE/name, WORK/name)
(WORK/'preservation').mkdir()
for name in ['input_before_preflight.zip', 'input_before_source_completion.zip']:
    shutil.copy2(SOURCE/'preservation'/name, WORK/'preservation'/name)
(WORK/'.lake').mkdir()
(WORK/'.lake/packages').symlink_to(SOURCE/'.lake/packages', target_is_directory=True)
files = sorted([SOURCE/'Bell.lean', * (SOURCE/'Bell').glob('*.lean'), *(SOURCE/'validation').glob('*.lean'), SOURCE.parent/'paper/main.tex', SOURCE.parent/'paper/appendices.tex'])
receipt = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'git_head': subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip(), 'source_sha256': {str(p.relative_to(HERE.parent)):digest(p) for p in files}, 'dependency_policy':'Reuse pinned dependency checkouts and compiled cache; all Bell production modules freshly compiled in isolated audit copy.'}
(HERE/'evidence/input.json').write_text(json.dumps(receipt,indent=2)+'\n')
with (HERE/'evidence/build.log').open('w') as log:
    proc=subprocess.run([sys.executable,'scripts/run_lean.py','--serial'],cwd=WORK,stdout=log,stderr=subprocess.STDOUT)
receipt['exit_code']=proc.returncode
receipt['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt['original_sources_unchanged']=all(digest(HERE.parent/p)==h for p,h in receipt['source_sha256'].items())
(HERE/'evidence/reproduction.json').write_text(json.dumps(receipt,indent=2)+'\n')
for name in ['kernel_report.json','axiom_audit.json','statement_audit.json','latest_run.json','declarations.json']:
    p=WORK/'reports'/name
    if p.exists(): shutil.copy2(p,HERE/'evidence'/name)
latest=WORK/'reports/latest_run.json'
if latest.exists():
    run_dir=WORK/json.loads(latest.read_text())['directory']
    shutil.copytree(run_dir,HERE/'evidence/run',dirs_exist_ok=True)
print(json.dumps({'exit_code':proc.returncode,'original_sources_unchanged':receipt['original_sources_unchanged']}))
sys.exit(proc.returncode)
