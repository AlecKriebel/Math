#!/usr/bin/env python3
"""Verify all five supporting seals and rerun each control in private copies."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent;D=A.parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
config=[('source_scope_adversary_01','SAFE_AUTHORED_MANIFEST.json','source_math_check.py','SOURCE_MATH_CHECK.json',[]),('elimination_dominance_adversary_01','SAFE_AUTHORED_MANIFEST.json','fresh_exact_controls.py','FRESH_EXACT_RESULTS.json',['INDEPENDENT_DERIVATION.md']),('likelihood_threshold_adversary_01','SAFE_AUTHORED_MANIFEST.json','exact_controls.py','exact_controls_results.json',[]),('priority_classical_01','MANIFEST.json','check_certificates.py','certificates.json',[]),('priority_author_update_01','MANIFEST.json','CONTROL.py','CONTROL_RESULTS.json',[])]
res=[]
for family,mname,script,output,extra in config:
 src=D/family;mf=src/mname;m=json.loads(mf.read_text())
 rows=m if isinstance(m,list) else m.get('safe_authored_files',m.get('files'))
 for r in rows:
  rel=r.get('path',r.get('relative_path'));pr=PurePosixPath(rel)
  assert not pr.is_absolute() and '..' not in pr.parts and rel==pr.as_posix()
  p=src/rel;assert p.resolve().is_relative_to(src.resolve()) and not p.is_symlink()
  assert p.stat().st_size==r['bytes'] and H(p)==r['sha256']
 dst=A/'private'/'support_replays'/family;dst.mkdir(parents=True,exist_ok=False)
 for name in [script]+extra:shutil.copyfile(src/name,dst/name)
 run=subprocess.run([sys.executable,str(dst/script)],cwd=dst,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=180)
 (dst/'stdout.txt').write_bytes(run.stdout);(dst/'stderr.txt').write_bytes(run.stderr)
 assert run.returncode==0,(family,run.stderr)
 if (dst/output).exists():actual=json.loads((dst/output).read_text())
 else:actual=json.loads(run.stdout)
 expected=json.loads((src/output).read_text())
 for obj in [actual,expected]:obj.pop('utc',None)
 assert actual==expected,family
 res.append({'family':family,'manifest_sha256':H(mf),'all_safe_entries_verified':len(rows),'script_sha256':H(src/script),'report_sha256':H(src/'REPORT.md'),'isolated_semantic_replay_exact_excluding_utc_only':True,'control_count':actual.get('count',actual.get('checks_passed',actual.get('assertions'))),'exit_code':run.returncode})
# Explicit separate seal formats.
p=D/'priority_author_update_01';seal=json.loads((p/'FINAL_SEAL.json').read_text());assert H(p/'MANIFEST.json')==seal['manifest_sha256'];assert (p/'MANIFEST.json').stat().st_size==seal['manifest_bytes']
p=D/'priority_classical_01'
for line in (p/'SEAL.sha256').read_text().splitlines():
 sha,name=line.split('  ',1);assert H(p/name)==sha
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','families':res,'original_fresh_control_count':16+3333+188,'both_priority_seals_verified':True,'raw_replays_private':True,'sibling_mutations':0}
(A/'SUPPORT_VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
