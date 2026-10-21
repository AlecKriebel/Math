#!/usr/bin/env python3
"""Fail-closed artifact authentication and relocated finite diagnostic replay.
Authenticate this file against an independently supplied SHA256 BEFORE execution.
This is not a formal proof checker, novelty certificate or peer review.
"""
import argparse, hashlib, json, pathlib, shutil, stat, subprocess, sys, tempfile, zipfile
PINS = {'INDEPENDENT_MATHEMATICAL_AUDIT.md': {'bytes': 21580, 'sha256': '9bc29555e72caab61dedc81c4eadc7ce1012ecac84f7740b09e5418c4bc68206'}, 'PROOF.md': {'bytes': 19961, 'sha256': '3bed7a81c5562d793bc4991fe62e1c06703818a9046495a7fe96d0b38e1ac100'}, 'RANDOM_PROPERTY_T_30006628_AUTHOR_EXTERNAL_MANIFEST.json': {'bytes': 3285, 'sha256': '46011dfd09c59dc52c561886c31b0e8ed0c823f5d5f446baf2c5aa35448fdaf0'}, 'RANDOM_PROPERTY_T_30006628_AUTHOR_SAFE_FREEZE.zip': {'bytes': 20225, 'sha256': 'f5c4e06b7c535a98aa37520ff616b4b63b4bdd7eb100e461de733f7fd7192134'}, 'RANDOM_PROPERTY_T_30006628_INDEPENDENT_AUDIT.zip': {'bytes': 14240, 'sha256': '513510dc1cced2a8dd25b2ab417a28092782159f74e56497ca156f2c4deed45e'}, 'RANDOM_PROPERTY_T_30006628_INDEPENDENT_AUDIT_MANIFEST.json': {'bytes': 2416, 'sha256': '1874f45e22c6b16a3198405a34b7deec974dca9c6d0e98097ad72cfd255bd05b'}, 'RANDOM_PROPERTY_T_30006628_SECOND_INDEPENDENT_REVIEW_EXTERNAL_MANIFEST.json': {'bytes': 2435, 'sha256': '5479ce6da0187f2d3463ea304bdf0d061b04cabaa04a37066b4fd6fa0cd4686d'}, 'RANDOM_PROPERTY_T_30006628_SECOND_INDEPENDENT_REVIEW_SAFE.zip': {'bytes': 17367, 'sha256': '2defd6a9aa5d295cdb93b3be46beeda6f0562b7eebddbd4b78d7d62405d229b3'}, 'SECOND_INDEPENDENT_MATHEMATICAL_REVIEW.md': {'bytes': 23384, 'sha256': '73015e793cc656aef605db3a76b378e7581ebd822fb2a0d0e562c7104596a806'}}
BUNDLES = [
 ('RANDOM_PROPERTY_T_30006628_AUTHOR_SAFE_FREEZE.zip', 'RANDOM_PROPERTY_T_30006628_AUTHOR_EXTERNAL_MANIFEST.json'),
 ('RANDOM_PROPERTY_T_30006628_INDEPENDENT_AUDIT.zip', 'RANDOM_PROPERTY_T_30006628_INDEPENDENT_AUDIT_MANIFEST.json'),
 ('RANDOM_PROPERTY_T_30006628_SECOND_INDEPENDENT_REVIEW_SAFE.zip', 'RANDOM_PROPERTY_T_30006628_SECOND_INDEPENDENT_REVIEW_EXTERNAL_MANIFEST.json')]

def require(ok, msg):
 if not ok: raise ValueError(msg)

def digest(raw): return hashlib.sha256(raw).hexdigest()
def authenticate(raw, expected, label):
 require(len(raw)==expected['bytes'] and digest(raw)==expected['sha256'], 'pin mismatch: '+label)

def verify(package):
 blobs={}
 for name,pin in PINS.items():
  p=package/name
  require(p.is_file() and not p.is_symlink(), 'missing or unsafe file: '+name)
  blobs[name]=p.read_bytes();authenticate(blobs[name],pin,name)
 members={}; inventories=[]
 for archive,manifest in BUNDLES:
  m=json.loads(blobs[manifest]);expected={x['path']:x for x in m['members']}
  require(len(expected)==len(m['members']), 'duplicate manifest path')
  with zipfile.ZipFile(package/archive) as z:
   names=z.namelist();require(len(names)==len(set(names)) and set(names)==set(expected),'archive member set: '+archive)
   for info in z.infolist():
    n=info.filename;p=pathlib.PurePosixPath(n)
    require(not p.is_absolute() and '..' not in p.parts and '\\' not in n and not info.is_dir() and not stat.S_ISLNK(info.external_attr>>16),'unsafe member: '+n)
    raw=z.read(n);authenticate(raw,expected[n],n);require(n not in members,'duplicate cross-archive path')
    members[n]=raw
  inventories.append({'archive':archive,'members_verified':len(names)})
 for member,loose in [('random_property_t_30006628/PROOF.md','PROOF.md'),('random_property_t_30006628_independent_audit/INDEPENDENT_MATHEMATICAL_AUDIT.md','INDEPENDENT_MATHEMATICAL_AUDIT.md'),('random_property_t_30006628_second_review/INDEPENDENT_MATHEMATICAL_REVIEW.md','SECOND_INDEPENDENT_MATHEMATICAL_REVIEW.md')]:
  require(members[member]==blobs[loose],'readable copy differs: '+loose)
 return blobs,members,inventories

def replay(package, sources):
 blobs,members,inventories=verify(package)
 records=[]
 with tempfile.TemporaryDirectory(prefix='property-t-relocated-') as td:
  root=pathlib.Path(td);work=root/'unrelated working directory';work.mkdir()
  for name,raw in blobs.items(): (root/name).write_bytes(raw)
  for name,raw in members.items():
   p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
  # Original review expects this author workspace layout; bytes remain unchanged.
  p=root/'random_property_t_30006628/safe/PROOF.md';p.parent.mkdir();p.write_bytes(blobs['PROOF.md'])
  source_args=[]
  if sources:
   source_manifest=json.loads(members['random_property_t_30006628/sources.json'])
   private=root/'supplied inputs';private.mkdir()
   for key in ['catalog','problems','reports']:
    pin=source_manifest['corpus'][key];raw=sources[key].read_bytes();authenticate(raw,pin,'supplied '+key)
    target=private/pin['filename'];target.write_bytes(raw);source_args += ['--'+key,str(target)]
   pdfdir=private/'pdfs';pdfdir.mkdir()
   for pin in source_manifest['primary_sources']:
    raw=(sources['pdf_dir']/pin['filename']).read_bytes();authenticate(raw,pin,'supplied PDF '+pin['filename']);(pdfdir/pin['filename']).write_bytes(raw)
   source_args += ['--pdf-dir',str(pdfdir)]
  def execute(mode,script,extra,expected=None,reason=None):
   flags=['-I','-B']+(['-O'] if mode=='optimized' else [])
   proc=subprocess.run([sys.executable,*flags,str(root/script),*extra],cwd=work,capture_output=True,timeout=300)
   require(not proc.stderr, 'unexpected stderr: '+script)
   data=json.loads(proc.stdout)
   if reason is None:
    require(proc.returncode==0 and data.get('status')=='PASS', 'positive diagnostic failed: '+script)
    require(proc.stdout==members[expected], 'recorded output mismatch: '+script)
   else:
    require(proc.returncode==1 and data=={'status':'REJECTED','reason':reason},'wrong rejection: '+script)
   records.append({'mode':mode,'script':script,'kind':'negative' if reason else 'positive','mutant':extra[-1] if reason else None,'exit_code':proc.returncode,'stdout_bytes':len(proc.stdout),'stdout_sha256':digest(proc.stdout),'expected_output_or_reason_matched':True})
  for mode in ['normal','optimized']:
   execute(mode,'random_property_t_30006628/checker.py',[],expected='random_property_t_30006628/checker_normal.json')
   execute(mode,'random_property_t_30006628_independent_audit/independent_kernel_check.py',[],expected='random_property_t_30006628_independent_audit/independent_kernel_results.json')
   execute(mode,'random_property_t_30006628_second_review/independent_checks.py',['--workspace',str(root)],expected='random_property_t_30006628_second_review/independent_checks_normal.json')
   for mutant,reason in [('missing_edge','exact expected-link kernel mismatch'),('wrong_boundary','exact expected-link kernel mismatch'),('two_factor_strict','two-factor strict gap is false'),('critical_density','density exponent must be positive')]:
    execute(mode,'random_property_t_30006628/checker.py',['--mutant',mutant],reason=reason)
   if sources:
    execute(mode,'random_property_t_30006628/verify_sources.py',source_args,expected='random_property_t_30006628/source_verification_normal.json')
    for mutant,reason in [('source_hash','SHA256 mismatch: problems.json'),('pair_hash','complete-record pair hash mismatch')]:
     execute(mode,'random_property_t_30006628/verify_sources.py',source_args+['--mutant',mutant],reason=reason)
 return {'status':'PASS','scope':'Artifact authentication and finite diagnostics only. Not asymptotic proof certification.','inventories':inventories,'core_file_count':len(PINS),'archive_member_count':len(members),'isolated_python':True,'relocated_temporary_layout':True,'original_artifacts_changed':False,'source_replay':'PASS' if sources else 'NOT_RUN_SOURCE_BYTES_NOT_SUPPLIED','receipts':records}

def main():
 p=argparse.ArgumentParser();p.add_argument('--package',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent);p.add_argument('--verify-only',action='store_true')
 for key in ['catalog','problems','reports','pdf-dir']: p.add_argument('--'+key,type=pathlib.Path)
 a=p.parse_args();v=[a.catalog,a.problems,a.reports,a.pdf_dir];require(all(v) or not any(v),'supply all four source locations or none')
 if a.verify_only:
  _,m,i=verify(a.package);result={'status':'PASS','archive_member_count':len(m),'inventories':i}
 else: result=replay(a.package,dict(zip(['catalog','problems','reports','pdf_dir'],v)) if all(v) else None)
 print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,KeyError,zipfile.BadZipFile,subprocess.TimeoutExpired) as e:
  print(json.dumps({'status':'REJECTED','reason':str(e)},sort_keys=True));sys.exit(1)
