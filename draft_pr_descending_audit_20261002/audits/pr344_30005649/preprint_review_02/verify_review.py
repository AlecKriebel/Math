#!/usr/bin/env python3
"""Read-only historical review verifier. Integrity/replay PASS never changes NEEDS_REPAIR.

--scope public: frozen six inputs, exact32 ZIP members/modes, duplicates, public
pins and review core bodies. Requires no external originals, network or software.
--scope full: all owned files/directories/modes, copied primary sources and original
control derivations, historical native receipts, then fresh read-only replays on
both recorded available interpreters. No builder is run; nothing is written.
The final manifest excludes its own bytes and must be pinned externally by root.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,stat,zipfile,subprocess,os,sys,datetime,shutil
R=Path(__file__).resolve().parent
P=R/'public/qss-self-duality-verification'
VERDICT='NEEDS_REPAIR'
def require(c,msg):
 if not c:raise RuntimeError(msg)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(b):return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def entry(p):
 require(not p.is_symlink(),'symlink: '+str(p))
 x=dict(type='directory' if p.is_dir() else 'file',mode=format(stat.S_IMODE(p.stat().st_mode),'04o'))
 if p.is_file():x.update(pin(p.read_bytes()))
 return x
def inventory():
 return {'.':entry(R),**{p.relative_to(R).as_posix():entry(p) for p in sorted(R.rglob('*')) if p != R/'FINAL_MANIFEST.json'}}
CORE={'REVIEW_REPORT.md','SOURCE_READING_LEDGER.json','PROVENANCE.md','ROOT_CLOSURE_PLAN.md','verify_review.py','independent_controls.py','probe_intrinsic_formula.py','REVIEW_STATUS.json'}
def public_path(s):return s=='.' or s in CORE or s in ('inputs','public','freezes') or s.startswith(('inputs/','public/','freezes/'))
def match_pin(p,w):
 require(pin(p.read_bytes())==dict(bytes=w['bytes'],sha256=w['sha256']),'pin mismatch: '+str(p))
 if 'mode' in w:require(stat.S_IMODE(p.stat().st_mode)==int(w['mode'],8),'mode mismatch: '+str(p))
def process(exe,script,args,expected=None):
 argv=[exe,'-B',str(script),*args];start=utc()
 r=subprocess.run(argv,cwd=P if script.is_relative_to(P) else R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0'),capture_output=True,timeout=60);end=utc()
 require(r.returncode==0,'replay failed: '+str(argv)+' '+r.stderr.decode(errors='replace'));require(not r.stderr,'stderr: '+str(argv))
 if expected is not None:require(r.stdout==expected,'complete output mismatch: '+str(script))
 return r.stdout,dict(argv=argv,resolved_executable=str(Path(exe).resolve()),cwd=str(P if script.is_relative_to(P) else R),start_utc=start,end_utc=end,exit_status=r.returncode,stdout=pin(r.stdout),stderr=pin(r.stderr))
def main():
 require(__debug__,'optimization disabled required')
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--scope',choices=['public','full'],default='public');a=ap.parse_args()
 start=utc();manifest=json.loads((R/'FINAL_MANIFEST.json').read_text());require(manifest['unsealed'] is True,'unexpected seal')
 require(manifest['verdict']==VERDICT,'adverse verdict changed');require(manifest['self_exclusion']==['FINAL_MANIFEST.json'],'self exclusion changed')
 before=inventory();expected=manifest['entries']
 choose=(lambda s:True) if a.scope=='full' else public_path
 require({k:v for k,v in before.items() if choose(k)}=={k:v for k,v in expected.items() if choose(k)},'owned scoped inventory/body/mode mismatch')
 status=json.loads((R/'REVIEW_STATUS.json').read_text());require(status['package_verdict']==VERDICT and status['main_theorem']=='VERIFIED_WITH_CLASSICAL_INPUTS' and status['mandatory_finding_ids']==['F01'],'scientific status changed')
 inputs=json.loads((R/'inputs/PINS.json').read_text());require(len(inputs)==6,'six inputs required')
 for x in inputs:match_pin(R/'inputs'/x['name'],x)
 rows=json.loads((R/'inputs/ZIP_INVENTORY.json').read_text());require(len(rows)==32,'ZIP member count')
 zpath=R/'inputs/qss-self-duality-verification.zip'
 with zipfile.ZipFile(zpath) as z:
  infos=z.infolist();require(len(infos)==32 and len({x.filename for x in infos})==32,'duplicate/count ZIP')
  require({x.filename for x in infos}=={x['name'] for x in rows},'ZIP inventory')
  table={x['name']:x for x in rows}
  for x in infos:
   path=PurePosixPath(x.filename);require(not path.is_absolute() and '..' not in path.parts and path.parts[0]=='qss-self-duality-verification','unsafe ZIP member')
   require(not x.is_dir() and stat.S_IMODE(x.external_attr>>16)==0o644,'ZIP mode/type')
   data=z.read(x);w=table[x.filename];require(pin(data)==dict(bytes=w['bytes'],sha256=w['sha256']),'ZIP body pin')
   require(format(x.CRC,'08x')==w['zip_crc32'],'ZIP CRC');match_pin(R/'public'/x.filename,w)
 require({x.relative_to(R/'public').as_posix() for x in (R/'public').rglob('*') if x.is_file()}=={x['name'] for x in rows},'extracted inventory')
 for src,dst in [('qss-self-duality-note.tex','manuscript.tex'),('zenodo-deposit.json','zenodo-deposit.json'),('verify_supplement.py','verify_supplement.py')]:require((R/'inputs'/src).read_bytes()==(P/dst).read_bytes(),'duplicate body mismatch')
 identity=json.loads((P/'SOURCE_IDENTITY.json').read_text())
 for name,w in identity['control_source_pins'].items():match_pin(P/name,w)
 fresh=[]
 if a.scope=='full':
  for f in ('PRIMARY_PINS.json','SUPPORT_PINS.json'):
   for x in json.loads((R/'sources'/f).read_text()):match_pin(R/'sources'/x['name'],x)
  for name,w in identity['reviewed_original_control_pins'].items():
   orig=R/'original_controls'/Path(name).name;match_pin(orig,w);body=orig.read_text()
   d=identity['control_derivations'].get(name)
   if d:
    require(d['reviewed_original']==w,'derivation original pin')
    for e in d['edits']:
     require(body.count(e['literal_old'])==e['occurrences'],'literal occurrence mismatch')
     body=body.replace(e['literal_old'],e['literal_new'])
    match_pin(P/name,d['public_derivative'])
   require(body.encode()==(P/name).read_bytes(),'literal public derivation mismatch: '+name)
  historical=0
  for directory in ('replays','adversarial'):
   summary=json.loads((R/'native'/directory/'SUMMARY.json').read_text())
   require(len(summary['runs'])==14,'native replay count')
   for x in summary['runs']:
    receipt=json.loads((R/'native'/directory/(x['name']+'.receipt.json')).read_text())
    require({k:v for k,v in x.items() if k!='name'}==receipt,'native summary differs from receipt')
    require(datetime.datetime.fromisoformat(x['start_utc'])<=datetime.datetime.fromisoformat(x['end_utc']),'native time order')
    require(x['exit_status']==x.get('expected_exit_status',0),'native status')
    for stream in ('stdout','stderr'):match_pin(R/'native'/directory/(x['name']+'.'+stream),x[stream])
    require(x['argv'][1]=='-B' and x['resolved_executable'] and x['python']['version'],'native argv/version')
    if directory=='replays':require(x['package_files_directories_modes_bodies_unchanged'] and x['six_inputs_unchanged'] and x['full_stdout_matches_expected'] is not False,'replay stability/expected')
    else:require(x['frozen_public_inventory_unchanged'] and x['six_inputs_inventory_unchanged'],'adversarial stability')
    historical+=1
  pairs={}
  for label,exe in [('system',shutil.which('python3')),('bundled','/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')]:
   require(exe is not None and Path(exe).is_file(),'required interpreter unavailable: '+label)
   vr=subprocess.run([exe,'-B','-c','import sys,json;print(json.dumps(dict(executable=sys.executable,version=sys.version)))'],cwd=R,capture_output=True);require(vr.returncode==0 and not vr.stderr,'version process')
   version=json.loads(vr.stdout)
   for name,script,args,stream in [('default',P/'verify_supplement.py',[],R/'native/replays/system_default.stdout'),('full',P/'verify_supplement.py',['--full'],R/'native/replays/system_full.stdout'),('independent',R/'independent_controls.py',[],R/'native/adversarial/system_independent.stdout'),('formula_probe',R/'probe_intrinsic_formula.py',[],R/'native/adversarial/system_formula_probe.stdout')]:
    stdout,receipt=process(exe,script,args,stream.read_bytes());fresh.append(dict(name=label+'_'+name,python=version,**receipt));pairs[(label,name)]=stdout
   found=json.loads(pairs[(label,'formula_probe')]);require(found['verdict']==VERDICT and all(w['author_invariants']['dual_kernel_formula']==0 and w['author_invariants']['dual_delta2']==1 and w['corrected_formula']==1 for w in found['witnesses']),'formula defect lost')
  require(all(pairs[('system',n)]==pairs[('bundled',n)] for n in ('default','full','independent','formula_probe')),'fresh complete streams differ')
 require(inventory()==before,'verifier wrote or changed owned namespace')
 print(json.dumps(dict(integrity_status='PASS',scope=a.scope,package_verdict=VERDICT,main_theorem='VERIFIED_WITH_CLASSICAL_INPUTS',mandatory_finding_ids=['F01'],frozen_zip_members=32,six_inputs=6,owned_namespace_unchanged=True,unsealed=True,start_utc=start,end_utc=utc(),fresh_native_replays=fresh,limitations=['PASS verifies supplied historical bindings and stated replay expectations, not universal proof, source authenticity, priority, or independent external human review.','Historical external source paths are provenance only; no live source body or Git ref is consulted.','The manifest does not hash itself. Root must bind its exact final body externally.','The adverse formula-finding verdict persists even though the author default and full replays pass.']),indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps(dict(integrity_status='FAIL',package_verdict=VERDICT,error=str(e)),indent=2));sys.exit(1)
