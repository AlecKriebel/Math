"""Authenticate and replay unchanged published mathematical programs only.
Historical review acceptance files are never parsed; --full wrappers are not used.
"""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,zipfile
R=Path(__file__).resolve().parent;P=R.parents[1];S=P/'sources'
SRC=S/'published-source/generic-wreath-hyperfiniteness-verification'
CACHE=R/'cache/package'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
need(sha(S/'generic-wreath-hyperfiniteness-verification.zip')=='3d73bb07b994c619df8a7e27ed2e43c99dd4e30c9fc1e5406454ee0671d1ebdd','ZIP pin')
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
if CACHE.exists():raise RuntimeError('replay cache already exists; do not silently overwrite')
shutil.copytree(SRC,CACHE)
source_hashes={str(f.relative_to(SRC)):sha(f) for f in SRC.rglob('*') if f.is_file()}
need(source_hashes=={str(f.relative_to(CACHE)):sha(f) for f in CACHE.rglob('*') if f.is_file()},'copy bytes')
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
commands=[]
def run(args):
 proc=subprocess.run([sys.executable,'-I','-B',*args],cwd=R/'cache',env=env,capture_output=True,text=True,timeout=900)
 commands.append({'arguments':[sys.executable,'-I','-B',*args],'exit_code':proc.returncode,'stderr':proc.stderr})
 need(proc.returncode==0,'replay failed: '+proc.stderr)
 return json.loads(proc.stdout)
outer=run([str(CACHE/'verify_package.py'),sha(CACHE/'package_index.json')])
inner=run([str(CACHE/'source/verify_publication.py'),sha(CACHE/'source/PUBLICATION_MANIFEST.json')])
need(outer['status']=='PASS' and inner['status']=='PASS_PUBLICATION_INVENTORY','inventory wrappers')
(R/'published-integrity.json').write_text(json.dumps({'outer':outer,'inner':inner},indent=2)+'\n')
summary=[]
for label,program,expected in [
 ('author','source/author/checks.py','source/author/EXPECTED_RESULTS.json'),
 ('planar_nonfree','source/audit_bundle/audit/independent_checks.py','source/audit_bundle/audit/INDEPENDENT_RESULTS.json'),
 ('quotient_nonfree','source/independent_review_2/independent_diagnostics.py','source/independent_review_2/EXPECTED_RESULTS.json'),
 ('current_boundary','audits/slab/boundary_diagnostics.py','audits/slab/BOUNDARY_DIAGNOSTICS.json')]:
 actual=run(['-c',"import json,runpy,sys; d=runpy.run_path(sys.argv[1]); print(json.dumps(d['compute'](),sort_keys=True))",str(CACHE/program)])
 prior=json.loads((CACHE/expected).read_text())
 need(not({'verdict','decision','acceptance'}&set(prior)),'unexpected historical opinion in numerical file')
 need(actual==prior,'computed numerical JSON differs: '+program)
 (R/(label+'-replay.json')).write_text(json.dumps(actual,indent=2)+'\n')
 summary.append({'label':label,'program':program,'program_sha256':sha(CACHE/program),'expected_numeric_file':expected,'expected_sha256':sha(CACHE/expected),'exact_numeric_json_equal':True,'counted_conditions':sum(actual.get('counts',{}).values()),'result_sha256':sha(R/(label+'-replay.json'))})
need(source_hashes=={str(f.relative_to(CACHE)):sha(f) for f in CACHE.rglob('*') if f.is_file()},'copy changed during replay')
need(source_hashes=={str(f.relative_to(SRC)):sha(f) for f in SRC.rglob('*') if f.is_file()},'source changed during replay')
receipt={'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_SELECTED_MATHEMATICAL_REPLAY','python':sys.version,'public_zip_sha256':sha(S/'generic-wreath-hyperfiniteness-verification.zip'),'package_index_sha256':sha(SRC/'package_index.json'),'source_manifest_sha256':sha(SRC/'source/PUBLICATION_MANIFEST.json'),'programs':summary,'commands':commands,'excluded':'The --full wrappers and historical integrity-mutation suites were not run. Full wrappers explicitly parse historical ACCEPTANCE.json; those bodies and their verdicts remain unread and are not mathematical evidence.','scope':'Four unchanged mathematical diagnostic programs plus two inventory-only wrappers. No program proves the infinite theorem.','originals_and_copy_unchanged':True}
(R/'published-replay-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'programs':len(summary),'numeric_counts':[r['counted_conditions'] for r in summary],'outer_files':outer['regular_files'],'inner_files':inner['files'],'inner_zip_members':inner['archive_members_verified']}))
