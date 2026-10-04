#!/usr/bin/env python3
"""Replay frozen author programs only in ignored copies; preserve complete receipts."""
from pathlib import Path
import argparse, datetime, hashlib, json, shutil, subprocess, sys, time

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent
SNAPSHOT = AUDIT / 'snapshot'
PREFIX = Path('problems/30006025_geometric_chapuy')
SOURCE = SNAPSHOT / PREFIX
parser=argparse.ArgumentParser()
parser.add_argument('--run-id',default='author_replay')
args=parser.parse_args()
assert args.run_id and all(c.isalnum() or c in '_-' for c in args.run_id)
PRIVATE = ROOT / 'private' / args.run_id
PRIVATE.mkdir(parents=True, exist_ok=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = json.loads((AUDIT/'snapshot_manifest.json').read_text())
files = []
for row in manifest['files']:
    path = SNAPSHOT / row['path']
    actual = sha(path)
    files.append({'path':row['path'],'expected_sha256':row['sha256'],
                  'actual_sha256':actual,'matches':actual==row['sha256']})
assert all(row['matches'] for row in files)
binding = {'head':manifest['head'],'manifest_sha256':sha(AUDIT/'snapshot_manifest.json'),
           'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'files':files}
(ROOT/'FROZEN_BINDING.json').write_text(json.dumps(binding,indent=2)+'\n')

dest = PRIVATE/'author'
if dest.exists():
    raise RuntimeError('Preserve existing replay; choose a fresh private root for a rerun.')
shutil.copytree(SOURCE,dest)
receipts=[]
for turn in range(1,6):
    filename = f'verify_turn{turn}.py'
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    before = time.monotonic()
    proc = subprocess.run([sys.executable,str(dest/filename)],cwd=dest,
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    elapsed = time.monotonic()-before
    # stdout must remain whole, including trailing newlines; do not trim it.
    (PRIVATE/f'turn_{turn}.stdout.txt').write_text(proc.stdout)
    (PRIVATE/f'turn_{turn}.stderr.txt').write_text(proc.stderr)
    parsed=None
    parse_error=None
    try:
        parsed=json.loads(proc.stdout)
    except Exception as error:
        parse_error=repr(error)
    receipt={'turn':turn,'program':str(PREFIX/filename),
             'program_sha256':sha(dest/filename),'started_utc':started,
             'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'elapsed_seconds':elapsed,'exit_code':proc.returncode,
             'stdout':proc.stdout,'stderr':proc.stderr,
             'stdout_sha256':hashlib.sha256(proc.stdout.encode()).hexdigest(),
             'stderr_sha256':hashlib.sha256(proc.stderr.encode()).hexdigest(),
             'parsed_json':parsed,'parse_error':parse_error}
    receipts.append(receipt)
    (ROOT/'AUTHOR_REPLAY_RECEIPTS.json').write_text(json.dumps(
        {'frozen_head':manifest['head'],'python':sys.version,'python_executable':sys.executable,
         'receipts':receipts,'all_five_complete':len(receipts)==5,
         'all_exits_zero':all(r['exit_code']==0 for r in receipts)},indent=2)+'\n')
    if turn==1 and proc.returncode==0 and parsed is not None:
        # Turn 3 consumes this control output. Use the newly generated result.
        (dest/'TURN_1_CHECKS.json').write_text(proc.stdout)
    print(json.dumps({'turn':turn,'exit_code':proc.returncode,
                      'elapsed_seconds':elapsed,'assertions':None if parsed is None else parsed.get('assertions'),
                      'stderr_bytes':len(proc.stderr)}),flush=True)

assert len(receipts)==5
assert all(r['exit_code']==0 and r['parsed_json'] is not None for r in receipts)
assert all(sha(SNAPSHOT/r['path'])==r['expected_sha256'] for r in files)
