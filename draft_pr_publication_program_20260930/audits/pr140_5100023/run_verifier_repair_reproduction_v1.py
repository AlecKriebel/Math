from pathlib import Path
import contextlib,datetime,hashlib,io,json,os,runpy,shutil,sys,time
A=Path(__file__).resolve().parent;kind=sys.argv[1]
if kind not in ['author','independent']:raise RuntimeError('verifier kind')
mode='optimized' if sys.flags.optimize else 'normal'
F=A/'ROOT_reproduction_20261007'/('repaired_'+kind+'_'+mode);F.mkdir(exist_ok=False)
source=A/'repaired_candidate_v1'
if kind=='author':
 for n in ['PROOF.md','verify.py']:shutil.copyfile(source/n,F/n)
 code='verify.py'
else:
 shutil.copyfile(source/'independent_checks.py',F/'independent_checks.py');(F/'author_replay').mkdir();shutil.copyfile(source/'PROOF.md',F/'author_replay/PROOF.md');code='independent_checks.py'
os.chdir(F);start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter();capture=io.StringIO()
with contextlib.redirect_stdout(capture):runpy.run_path(code,run_name='__main__')
result=json.loads(capture.getvalue());(F/'ACTUAL_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
metadata={'actual_PID':os.getpid(),'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-t,'kind':kind,'mode':mode,'source_sha256':hashlib.sha256((F/code).read_bytes()).hexdigest(),'status':'completed'}
(F/'ACTUAL_RUN.json').write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps({**metadata,'checks':result['assertions'],'proof_sha256':result['artifact_sha256']}))
