"""Byte-identical isolated replay of all original checkers. Run from this folder."""
from pathlib import Path
import subprocess, sys, hashlib, json, time, datetime, platform
ROOT=Path(__file__).resolve().parent
ORIGINAL=ROOT.parent/'submitted/unsolved_math_prioritization/attempts/30001321'
DEFAULT_RUNTIME=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python')
PYTHON=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else (DEFAULT_RUNTIME if DEFAULT_RUNTIME.exists() else Path(sys.executable))
SPECS=[('turn1','check_turn1.py','turn1_receipt.json'),('turn2','check_turn2.py','turn2_receipt.json'),('turn3','check_turn3.py','turn3_receipt.json'),('old_independent','independent_review/independent_check.py','independent_review/independent_check.json')]
rows=[]
for name,script,receipt in SPECS:
    folder=ROOT/'tmp/replay'/name;folder.mkdir(parents=True,exist_ok=True)
    original=(ORIGINAL/script).read_bytes();copy=folder/Path(script).name;copy.write_bytes(original)
    start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc=subprocess.run([str(PYTHON),'-I','-B',str(copy)],cwd=folder,capture_output=True,timeout=600)
    (ROOT/(name+'_replay_stdout.json')).write_bytes(proc.stdout)
    (ROOT/(name+'_replay_stderr.txt')).write_bytes(proc.stderr)
    try: got=json.loads(proc.stdout); expected=json.loads((ORIGINAL/receipt).read_text());equal=got==expected
    except Exception as error:got=None;equal=False
    row={'name':name,'source_path':script,'source_sha256':hashlib.sha256(original).hexdigest(),'copy_sha256':hashlib.sha256(copy.read_bytes()).hexdigest(),'utc_started':utc,'elapsed_seconds':round(time.monotonic()-start,3),'returncode':proc.returncode,'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stderr_bytes':len(proc.stderr),'stdout_matches_original_receipt_json':equal,'stdout_bytes_equal_original_receipt':proc.stdout==(ORIGINAL/receipt).read_bytes(),'reported_status':None if got is None else got.get('status'),'exact_assertions':None if got is None else got.get('exact_assertions')}
    rows.append(row);print(json.dumps(row),flush=True)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':str(PYTHON),'runtime_probe':subprocess.run([str(PYTHON),'-I','-B','-c','import sys,sympy;print(sys.version);print(sympy.__version__)'],capture_output=True,text=True).stdout,'isolation':'Separate fresh working directories, unchanged script bytes, Python -I -B, no imports from original checker tree; full unmodified loops.','runs':rows,'all_pass':all(x['returncode']==0 and x['stderr_bytes']==0 and x['stdout_matches_original_receipt_json'] and x['stdout_bytes_equal_original_receipt'] and x['source_sha256']==x['copy_sha256'] for x in rows)}
(ROOT/'EXACT_REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
sys.exit(0 if result['all_pass'] else 1)
