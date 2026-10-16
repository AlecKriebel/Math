#!/usr/bin/env python3
"""Independent outer-package mutation checks and isolated deterministic rebuild."""
from pathlib import Path
import json,hashlib,runpy,shutil,tempfile,os,subprocess,sys,zipfile
HERE=Path(__file__).absolute().parent
ROOT=HERE/'tmp/packet'
V=runpy.run_path(str(ROOT/'verify_package.py'))
passed=[]
def need(ok,label):
 if not ok:raise ValueError(label)
def update(q,name):
 m=q/'PACKAGE_MANIFEST.json';d=json.loads(m.read_text());b=(q/name).read_bytes()
 for r in d['files']:
  if r['path']==name:r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 m.write_text(json.dumps(d))
def scope(q,key,value):
 n='CLAIM_SCOPE.json';p=q/n;d=json.loads(p.read_text());d[key]=value;p.write_text(json.dumps(d));update(q,n)
cases=['extra_rehashed','missing_tex','changed_pdf_rehashed','original_native_rehashed','changed_pinned_gate_rehashed','duplicate_manifest_key','duplicate_scope_key_rehashed','duplicate_record','manifest_parent_escape','manifest_abs','manifest_backslash','manifest_colon','manifest_nul','manifest_double_slash','manifest_self_reference','symlink_file','symlink_dir','empty_dir','scope_explicit_gap','scope_sharp_radius','scope_firstness','scope_certified_numeric','scope_human_review','scope_unexpected_field','scope_bool_int','scope_nan','manifest_count_bool','manifest_size_bool']
for case in cases:
 with tempfile.TemporaryDirectory(dir=HERE/'tmp',prefix='negative-') as tmp:
  q=Path(tmp)/'packet';shutil.copytree(ROOT,q);m=q/'PACKAGE_MANIFEST.json';d=json.loads(m.read_text())
  if case=='extra_rehashed':
   n='extra.txt';b=b'extra';(q/n).write_bytes(b);d['files'].append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()});d['file_count']+=1;m.write_text(json.dumps(d))
  elif case=='missing_tex':(q/'real_schlicht_preschwarzian.tex').unlink()
  elif case in ('changed_pdf_rehashed','original_native_rehashed','changed_pinned_gate_rehashed'):
   n={'changed_pdf_rehashed':'real_schlicht_preschwarzian.pdf','original_native_rehashed':V['NATIVE']+'/SCOPE_CLARIFICATION.md','changed_pinned_gate_rehashed':'MATH_SOURCE_GATE_ACCEPTANCE.json'}[case];p=q/n;p.write_bytes(p.read_bytes()+b'\n');update(q,n)
  elif case=='duplicate_manifest_key':m.write_text(m.read_text().replace('{','{"schema":1,',1))
  elif case=='duplicate_scope_key_rehashed':
   p=q/'CLAIM_SCOPE.json';p.write_text(p.read_text().replace('{','{"unrefereed":true,',1));update(q,'CLAIM_SCOPE.json')
  elif case=='duplicate_record':d['files'].append(d['files'][0]);d['file_count']+=1;m.write_text(json.dumps(d))
  elif case.startswith('manifest_') and case not in ('manifest_count_bool','manifest_size_bool'):
   names={'manifest_parent_escape':'../outside','manifest_abs':'/outside','manifest_backslash':'a\\b','manifest_colon':'a:b','manifest_nul':'a\0b','manifest_double_slash':'a//b','manifest_self_reference':'PACKAGE_MANIFEST.json'}
   d['files'][0]['path']=names[case];m.write_text(json.dumps(d))
  elif case=='symlink_file':
   p=q/'real_schlicht_preschwarzian.tex';p.unlink();p.symlink_to(ROOT/'real_schlicht_preschwarzian.tex')
  elif case=='symlink_dir':
   p=q/'reviews/geometry_01';shutil.rmtree(p);p.symlink_to(ROOT/'reviews/geometry_01',target_is_directory=True)
  elif case=='empty_dir':(q/'empty').mkdir()
  elif case.startswith('scope_'):
   kv={'scope_explicit_gap':('explicit_upper_gap_formula',True),'scope_sharp_radius':('sharp_quantitative_radius',True),'scope_firstness':('historical_firstness_claim',True),'scope_certified_numeric':('numerical_interval_certification',True),'scope_human_review':('AI_reviews_are_human_peer_review',True),'scope_unexpected_field':('all_quantitative_questions_solved',True),'scope_bool_int':('unrefereed',1),'scope_nan':('source_expression_at_zero',float('nan'))}[case];scope(q,*kv)
  elif case=='manifest_count_bool':d['file_count']=True;m.write_text(json.dumps(d))
  elif case=='manifest_size_bool':d['files'][0]['bytes']=True;m.write_text(json.dumps(d))
  try:V['verify'](q)
  except (ValueError,KeyError,FileNotFoundError,NotADirectoryError):passed.append(case)
  else:raise ValueError('accepted '+case)
need(len(passed)==len(cases),'all mutations rejected')
# Rebuild in the documented audit working layout, rather than overwriting frozen outputs.
with tempfile.TemporaryDirectory(dir=HERE/'tmp',prefix='rebuild-') as tmp:
 A=Path(tmp)/'audit';P=A/'publication';P.mkdir(parents=True)
 for name in V['PUBLICATION_FILES']:
  shutil.copyfile(ROOT/name,P/('PACKAGE_README.md' if name=='README.md' else name))
 for name in V['ROOT_FILES']:
  shutil.copyfile(ROOT/name,A/name)
 shutil.copytree(ROOT/'native',A/'native');shutil.copytree(ROOT/'reviews',A/'reviews')
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
 p=subprocess.run([sys.executable,'-I','-B',str(P/'build_package.py')],cwd=A,env=env,capture_output=True)
 need(p.returncode==0,p.stderr.decode())
 rebuilt=(P/'real_schlicht_verification.zip').read_bytes()
 expected='945c5e52a136bd0187d51661140b617965c064c880628bdbeff3324516b9bc04'
 need(hashlib.sha256(rebuilt).hexdigest()==expected,'deterministic rebuild SHA')
 report={'status':'PASS','rejected_count':len(passed),'rejected':passed,'isolated_rebuild_zip_sha256':expected,'original_payload_unchanged':V['verify'](ROOT),'limitations':'Checksums are integrity/provenance checks, not a signature against replacement of the complete verifier and packet.'}
print(json.dumps(report,indent=2,sort_keys=True))
