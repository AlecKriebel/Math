"""Rerun four unchanged owned mathematical cores in an exclusive scratch folder.

No network access or private authentication replay is attempted. This driver
does not prove the universal theorem; the analytic arguments remain essential.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, subprocess, sys

ap=argparse.ArgumentParser()
ap.add_argument('--audit-root', required=True)
ap.add_argument('--library-dir', required=True, help='Explicit directory containing SymPy1.14.0 and mpmath1.3.0')
ap.add_argument('--output-dir',required=True,help='New exclusive scratch directory; do not point into a frozen audit.')
args=ap.parse_args()
B=Path(args.audit_root).resolve()
O=Path(args.output_dir).resolve()
L=Path(args.library_dir).resolve()
assert B.is_dir() and L.is_dir()
assert not (O==B or B in O.parents), 'Scratch must be outside the selected audit tree.'
O.mkdir(parents=True,exist_ok=False)
plan=[
 ('archive_algebra','priority_repository_archive/public/check_algebra.py','priority_repository_archive/public/ALGEBRA_RECEIPT.json','ALGEBRA_RECEIPT.json',[]),
 ('odd_repeat','ROOT_ODD_REPEAT_BOUNDARY.py','ROOT_ODD_REPEAT_BOUNDARY.json','OUTPUT.json',['--library-dir',str(L),'--output','OUTPUT.json']),
 ('general_reduction','priority_general_theorem/verify_reduction.py','priority_general_theorem/REDUCTION_VERIFICATION.json','REDUCTION_VERIFICATION.json',[]),
 ('general_comparison','priority_general_theorem/verify_comparison.py','priority_general_theorem/COMPARISON_VERIFICATION.json','COMPARISON_VERIFICATION.json',[]),
]
ignore={'UTC','utc','checked_utc'}
def norm(x):
 if isinstance(x,dict): return {k:norm(v) for k,v in x.items() if k not in ignore}
 if isinstance(x,list): return [norm(v) for v in x]
 return x
wrapper='''import runpy,sys
sys.path.insert(0,sys.argv[1])
import sympy,mpmath
assert sympy.__version__=="1.14.0"
assert mpmath.__version__=="1.3.0"
script=sys.argv[2]
sys.argv=sys.argv[2:]
runpy.run_path(script,run_name="__main__")
'''
rows=[]
for label,script_rel,receipt_rel,outname,tail in plan:
 D=O/label;D.mkdir()
 raw=(B/script_rel).read_bytes()
 target=D/Path(script_rel).name;target.write_bytes(raw)
 started=datetime.now(timezone.utc).isoformat()
 result=subprocess.run([sys.executable,'-I','-B','-c',wrapper,str(L),str(target),*tail],cwd=D,
                       env={**os.environ,'PYTHONHASHSEED':'0'},capture_output=True,timeout=240)
 (D/'stdout.txt').write_bytes(result.stdout);(D/'stderr.txt').write_bytes(result.stderr)
 row={'label':label,'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),
      'script_relative_path':script_rel,'script_sha256':hashlib.sha256(raw).hexdigest(),
      'expected_receipt_relative_path':receipt_rel,'expected_receipt_sha256':hashlib.sha256((B/receipt_rel).read_bytes()).hexdigest(),
      'exit_code':result.returncode,'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),
      'stderr_sha256':hashlib.sha256(result.stderr).hexdigest(),'scratch_output':str(D/outname)}
 rows.append(row)
 (O/'REPLAY_PROGRESS.json').write_text(json.dumps({'rows':rows,'completed':False},indent=2)+'\n')
 assert result.returncode==0 and result.stderr==b'',label
 actual=json.loads((D/outname).read_bytes());expected=json.loads((B/receipt_rel).read_bytes())
 row['mathematical_output_equal_excluding_UTC_only']=norm(actual)==norm(expected)
 assert row['mathematical_output_equal_excluding_UTC_only'],label
receipt={'schema':'pr259-owned-core-portable-replay-v1','utc':datetime.now(timezone.utc).isoformat(),
         'decision':'PASS_OWNED_MATHEMATICAL_CORE_REPLAYS','completed':True,'rows':rows,
         'ignored_json_keys':sorted(ignore),'private_authentication_replayed':False,
         'source_body_downloads':0,'provider_writes':0,'shared_git_writes':0,
         'limits':'Exact algebra and finite numerical comparisons supplement the analytic proof; they do not establish all-period invariance or global priority. The full historical authentication checker requires excluded private inputs and original paths.'}
(O/'VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'decision':receipt['decision'],'replays':len(rows),'output_dir':str(O)},indent=2))
