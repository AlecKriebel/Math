from pathlib import Path
import json,hashlib,shutil,subprocess,datetime
D=Path(__file__).resolve().parent
py=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python')
rows=[]
for family,script,out,extra,count in [('source_scope_adversary_01','source_math_check.py','SOURCE_MATH_CHECK.json',[],'count'),('elimination_dominance_adversary_01','fresh_exact_controls.py','FRESH_EXACT_RESULTS.json',['INDEPENDENT_DERIVATION.md'],'checks_passed')]:
 src=D/family;mf=src/'SAFE_AUTHORED_MANIFEST.json';m=json.loads(mf.read_text());m=m if isinstance(m,list) else m['safe_authored_files']
 for v in m:
  q=src/v['path'];assert q.resolve().is_relative_to(src) and not q.is_symlink()
  b=q.read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
 dst=D/'root_fresh_replays'/family;dst.mkdir(parents=True,exist_ok=True)
 for name in [script]+extra:shutil.copyfile(src/name,dst/name)
 r=subprocess.run([str(py),str(dst/script)],capture_output=True,text=True,timeout=180)
 (dst/'stdout.txt').write_text(r.stdout);(dst/'stderr.txt').write_text(r.stderr);assert r.returncode==0,r.stderr
 a=json.loads((dst/out).read_text());b=json.loads((src/out).read_text())
 for x in [a,b]:x.pop('utc',None)
 assert a==b
 rows.append(dict(family=family,manifest_sha256=hashlib.sha256(mf.read_bytes()).hexdigest(),safe_manifest_files=len(m),all_safe_bytes_verified=True,independent_controls_replayed=a[count],exact_semantic_match_excluding_UTC_only=True,report_sha256=hashlib.sha256((src/'REPORT.md').read_bytes()).hexdigest()))
res={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer_families':rows,'no_original_or_sealed_reviewer_output_modified':True}
(D/'ROOT_FRESH_FAMILY_REPLAY_ACCEPTANCE.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
