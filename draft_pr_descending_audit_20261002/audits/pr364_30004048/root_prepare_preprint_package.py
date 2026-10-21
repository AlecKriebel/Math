"""Prepare the current submission and capture a full portable reproduction."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,zipfile
A=Path(__file__).resolve().parent;P=A/'preprint';V=P/'verification';Q=A/'priority_review'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
assert (Q/'FINAL_SEAL.json').is_file(),'Complete priority closure required first'
for n in ['PRIORITY_REPORT.md','SEARCH_COVERAGE.json','SOURCE_IDENTITIES.json','README.md','RESEARCH_LOG.md','PUBLIC_MANIFEST.json','FINAL_SEAL.json']:
 d=V/'audits/priority';d.mkdir(exist_ok=True);shutil.copyfile(Q/n,d/n)
shutil.copyfile(Q/'PRIORITY_REPORT.md',V/'PRIORITY_REPORT.md')
shutil.copyfile(P/'biconstrained_asymmetry.tex',V/'biconstrained_asymmetry.tex')
files={p.relative_to(V).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(V.rglob('*')) if p.is_file() and p!=V/'MANIFEST.json'}
(V/'MANIFEST.json').write_text(json.dumps({'schema':'Exact biconstrained portable verification v1','self_exclusion':'MANIFEST.json','files':files},indent=2)+'\n')
D=P/'private/package_001';D.mkdir(exist_ok=False)
argv=['python3','-B',str(V/'verify_package.py')];start=utc();p=subprocess.run(argv,cwd=A.parents[2],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True);end=utc()
(D/'stdout').write_bytes(p.stdout);(D/'stderr').write_bytes(p.stderr)
r={'argv':argv,'cwd':str(A.parents[2]),'environment_changes':{'PYTHONDONTWRITEBYTECODE':'1'},'started_utc':start,'finished_utc':end,'exit_code':p.returncode,'streams':{st:{'path':str(D/st),'bytes':len(b),'sha256':sha(b)} for st,b in [('stdout',p.stdout),('stderr',p.stderr)]}}
(D/'EXECUTION.json').write_text(json.dumps(r,indent=2)+'\n');assert p.returncode==0 and not p.stderr,r
result=json.loads(p.stdout);assert result['status']=='PASS' and len(result['whole_program_replays'])==6 and result['nested_manifest_instances']==135
Z=P/'biconstrained-asymmetry-verification.zip'
with zipfile.ZipFile(Z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(V.rglob('*')):
  if p.is_file():
   n='biconstrained-asymmetry-verification/'+p.relative_to(V).as_posix();i=zipfile.ZipInfo(n,date_time=(2026,10,3,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,p.read_bytes())
with zipfile.ZipFile(Z) as z:
 assert len(z.namelist())==len(files)+1 and len(set(z.namelist()))==len(z.namelist())
 for n in z.namelist():assert z.read(n)==(V/n.removeprefix('biconstrained-asymmetry-verification/')).read_bytes()
submission={}
for n in ['biconstrained_asymmetry.tex','biconstrained_asymmetry.pdf','biconstrained-asymmetry-verification.zip','zenodo-deposit.json']:
 b=(P/n).read_bytes();submission[n]={'bytes':len(b),'sha256':sha(b)}
out={'utc':utc(),'stage':'INITIAL_COMPLETE_REVIEW_PACKAGE','submission_files':submission,'verification_files':len(files)+1,'complete_zip_members_verified':True,'portable_whole_replay':result,'execution_receipt':str(D/'EXECUTION.json'),'mathematical_completion_percent':100,'preprint_workflow_percent':80,'fresh_sequential_preprint_reviews_pending':True,'priority_finding':'No equivalent earlier theorem identified in bounded primary corpus; inaccessible2019 thesis and indexing limits retained. No global novelty certification.','no_zenodo_or_tracker_write_yet':True}
(P/'INITIAL_REVIEW_PACKAGE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
