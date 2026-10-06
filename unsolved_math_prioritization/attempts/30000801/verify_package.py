#!/usr/bin/env python3
"""Integrity and finite controls for the frozen conditional result, not a PDE proof."""
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,json,shutil,stat,subprocess,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ARCHIVES=[('NAVIER_30000801_AUTHOR_SAFE_FREEZE.zip','author','navier_30000801',22361,'45ab3bf6abaa90e865cba7899a509de3a8343ab44b32bb09dbbad7ccd9f46434',11,'8588374c263f35b384d5cb2e74187c0d09198c8cdc63ebb1b60ac240a8f13626'),('NAVIER_30000801_INDEPENDENT_AUDIT_SAFE.zip','audit','navier_30000801_independent_audit',24188,'326136d76eb46725806875d906dc6bb19833f9e8de17ab45d33d8143a0dad1bf',10,'64eced9eebf31d7f080a7349b75bb5df20aee5bf07b91fcf7207fc6de741b0e0')]
def require(ok,message):
 if not ok:raise ValueError(message)
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def parse(b):
 def pairs(ps):
  d={}
  for k,v in ps:
   require(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs)
def inventory(root):
 paths=list(root.rglob('*'));require(not any(p.is_symlink() for p in paths),'symlink package member')
 files={p.relative_to(root).as_posix():p for p in paths if p.is_file()};dirs={p.relative_to(root).as_posix() for p in paths if p.is_dir()}
 require(dirs=={'archives','author','audit'},'package directory inventory')
 m=parse((root/'PACKAGE_MANIFEST.json').read_bytes());require(set(m)=={'schema','files'} and m['schema']=='sha256-byte-inventory-v1','package manifest schema')
 require(set(files)==set(m['files'])|{'PACKAGE_MANIFEST.json'},'package file inventory')
 for n,e in m['files'].items():require(digest(files[n].read_bytes())==e,'package digest: '+n)
 for name,d,prefix,size,h,count,mh in ARCHIVES:
  p=root/'archives'/name;require(digest(p.read_bytes())=={'bytes':size,'sha256':h},'external archive pin')
  require(hashlib.sha256((root/d/'MANIFEST.json').read_bytes()).hexdigest()==mh,'frozen manifest pin')
  with zipfile.ZipFile(p) as z:
   names=z.namelist();expected={prefix+'/'+p.name for p in (root/d).iterdir()}
   require(len(names)==len(set(names))==count and set(names)==expected and z.testzip() is None,'ZIP inventory/CRC')
   for info in z.infolist():
    require(not stat.S_ISLNK(info.external_attr>>16) and not info.is_dir(),'ZIP member type')
    require(z.read(info.filename)==(root/d/Path(info.filename).name).read_bytes(),'ZIP member equality')
 return {'status':'PASS','files':len(files),'archive_members':[11,10]}
def run(script,args=(),opt=False,cwd=None):
 r=subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(script)]+list(args),cwd=cwd or ROOT,capture_output=True,text=True,timeout=600)
 require(r.returncode==0,'child failed: '+Path(script).name+' '+r.stderr[:300]);d=parse(r.stdout);require(d['status']=='PASS','child status');return d
def inventory_corruptions():
 out=[]
 with tempfile.TemporaryDirectory(prefix='navier_inventory_') as t:
  t=Path(t)
  for opt in (False,True):
   for kind in ['altered_proof','missing_result','extra_file','symlink_proof','duplicate_manifest_key']:
    d=t/(str(opt)+'_'+kind);shutil.copytree(ROOT/'audit',d)
    if kind=='altered_proof':
     p=d/'MATHEMATICAL_AUDIT.md';p.write_bytes(p.read_bytes()+b'Changed.')
    elif kind=='missing_result':(d/'RESULTS.json').unlink()
    elif kind=='extra_file':(d/'unlisted.txt').write_text('x')
    elif kind=='symlink_proof':
     p=d/'MATHEMATICAL_AUDIT.md';p.unlink();p.symlink_to(d/'README.md')
    else:
     p=d/'MANIFEST.json';p.write_text(p.read_text().replace('"schema":','"schema": "sha256-byte-inventory-v1", "schema":',1))
    r=subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(d/'audit_inventory.py')],cwd=t,capture_output=True,text=True,timeout=30)
    require(r.returncode!=0 and '"status": "FAIL"' in r.stderr,'audit corruption accepted');out.append({'mode':'optimized' if opt else 'normal','case':kind,'status':'REJECTED'})
 return out
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',nargs=3);p.add_argument('--pdf-inputs',nargs=4);p.add_argument('--adversarial',action='store_true');a=p.parse_args();inv=inventory(ROOT)
 ca=['--inputs']+[str(Path(x).resolve()) for x in a.inputs] if a.inputs else [];pa=['--pdf-inputs']+[str(Path(x).resolve()) for x in a.pdf_inputs] if a.pdf_inputs else [];za=['--author-zip',str(ROOT/'archives'/ARCHIVES[0][0])]
 out={'status':'PASS','full_resolution':False,'package_inventory':inv,'replays':[],'adversarial':{'status':'NOT_REQUESTED'}}
 for opt in (False,True):
  au=run(ROOT/'author/verify.py',ca,opt);iv=run(ROOT/'audit/independent_verify.py',za+ca+pa,opt);ai=run(ROOT/'audit/audit_inventory.py',[],opt)
  require(au['exact_control_count']==17 and au['proves_full_target'] is False,'author scope/count');require(iv['independent_control_count']==26 and iv['full_resolution'] is False,'independent scope/count')
  require(iv['corpus_replay']['status']==('PASS' if a.inputs else 'NOT_REQUESTED'),'corpus status');require(iv['pdf_byte_replay']['status']==('PASS' if a.pdf_inputs else 'NOT_REQUESTED'),'PDF status')
  out['replays'].append({'mode':'optimized' if opt else 'normal','author':au,'independent':iv,'audit_inventory':ai})
 if a.adversarial:
  old=run(ROOT/'author/test_fail_closed.py');new=run(ROOT/'audit/independent_adversarial.py',za+ca+pa);ic=inventory_corruptions()
  require(old['mutation_rejections']==24 and new['additional_author_mutation_rejections']==36 and new['external_archive_corruption_rejections']==4,'mutation counts');require(new['source_corruption_rejections']==(3 if a.inputs else 0)+(4 if a.pdf_inputs else 0),'source corruption count');require(len(ic)==10,'audit inventory count')
  out['adversarial']={'status':'PASS','original':old,'independent':new,'audit_inventory_corruptions':ic,'source_corruptions_status':'PASS' if a.inputs or a.pdf_inputs else 'NOT_REQUESTED'}
 inventory(ROOT);print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:
  print(json.dumps({'status':'FAIL','error':str(e)}),file=sys.stderr);sys.exit(1)
