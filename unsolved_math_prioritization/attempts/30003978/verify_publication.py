#!/usr/bin/env python3
"""Fail-closed offline publication binding and assertion-enabled exact replay."""
import argparse,hashlib,json,os,re,subprocess,sys,tempfile,zipfile
from pathlib import Path
PINS={
 'author/MANIFEST.json':'19e0257d9ade68f67a9004cc77bfa3e26b4b242ab7dc0dc3c97596763ede5e1a',
 'independent_audit/MANIFEST.json':'e4504940b5c816e9c6de3f6fb7c6285bd2328be47439c034e5d49a613708ba36',
 'SESHADRI_30003978_AUTHOR_FREEZE.zip':'601c698414044bba32dd4bb624130febf008f64422eab986233c363aa94599ed',
 'SESHADRI_30003978_INDEPENDENT_AUDIT.zip':'6ea1d4e56acf9dc0b777141de57fc2244025fdf0a5cc32614631812c618e52c7'}
def need(ok,message):
 if not ok:raise ValueError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def regular(path):
 need(path.is_file() and not path.is_symlink(),'Nonregular file: '+str(path));return path.read_bytes()
def bind(root,pin):
 need(re.fullmatch('[0-9a-f]{64}',pin) is not None,'Invalid pin')
 raw=regular(root/'MANIFEST.json');need(digest(raw)==pin,'External manifest mismatch');manifest=json.loads(raw)
 need(manifest['schema']=='seshadri-30003978-publication-manifest-v1','Manifest schema');names=set()
 for row in manifest['files']:
  need(set(row)=={'path','bytes','sha256'},'Record schema');name=row['path']
  need(isinstance(name,str) and name not in names and name!='MANIFEST.json','Duplicate/self path');p=Path(name)
  need(not p.is_absolute() and '..' not in p.parts and '\\' not in name and str(p)==name,'Unsafe path')
  need(type(row['bytes']) is int and row['bytes']>=0,'Invalid size');need(isinstance(row['sha256'],str) and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'Invalid hash')
  b=regular(root/name);need(len(b)==row['bytes'] and digest(b)==row['sha256'],'File mismatch: '+name);names.add(name)
 entries=list(root.rglob('*'));need(not any(p.is_symlink() for p in entries),'Symlink in packet')
 need({p.relative_to(root).as_posix() for p in entries if p.is_file()}==names|{'MANIFEST.json'},'File inventory mismatch')
 dirs={str(p) for name in names for p in Path(name).parents if str(p)!='.'}
 need({p.relative_to(root).as_posix() for p in entries if p.is_dir()}==dirs,'Directory inventory mismatch')
 for name,pin in PINS.items():need(digest(regular(root/name))==pin,'Frozen pin mismatch: '+name)
 for folder,prefix,archive,size in [
  ('author','author','SESHADRI_30003978_AUTHOR_FREEZE.zip',18758),
  ('independent_audit','seshadri_30003978_independent_audit','SESHADRI_30003978_INDEPENDENT_AUDIT.zip',20988)]:
  need(len(regular(root/archive))==size,'Archive size');inner=json.loads(regular(root/folder/'MANIFEST.json'))['files'];inner_names=['MANIFEST.json']+[x['path'] for x in inner]
  need(len(inner_names)==len(set(inner_names))==10,'Inner count');need(set(inner_names)=={p.name for p in (root/folder).iterdir()},'Inner inventory')
  for row in inner:
   need(Path(row['path']).name==row['path'],'Unsafe inner path');b=regular(root/folder/row['path']);need(len(b)==row['bytes'] and digest(b)==row['sha256'],'Inner binding')
  with zipfile.ZipFile(root/archive) as z:
   members=z.infolist();need(len(members)==10,'Archive count');need({m.filename for m in members}=={prefix+'/'+n for n in inner_names},'Archive names')
   for m in members:
    need(not m.is_dir() and (m.external_attr>>16)&0o170000!=0o120000,'Archive nonregular');need(z.read(m)==regular(root/folder/m.filename.split('/',1)[1]),'Archive bytes')
 m=json.loads(regular(root/'PUBLICATION.json'));need(m['status']=='already_solved' and m['turns']=='1/5' and m['target_resolved_in_prior_preprints'] is True,'Status scope')
 need(all(m[x] is False for x in ['novelty_claim','nagata_proved','formal_verification','peer_review_established','raw_dataset_included','source_text_or_source_bytes_included','private_coordination_included']),'Claim boundary')
 need(m['queue']['changed_cells']==['Status','Turns','Findings'],'Queue cell scope')
 need(m['reflection_scope']=='Globally line-bundle-marked rational blowup families; no endorsement of the broader abstract proposition without repairing its base-change shorthand.','Reflection scope')
 return len(names)+1

def main():
 p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);p.add_argument('--queue',type=Path);a=p.parse_args()
 need(__debug__ and sys.flags.optimize==0,'Python optimization is forbidden; disabled assertions are not verification')
 sys.dont_write_bytecode=True;root=Path(__file__).resolve().parent;count=bind(root,a.expected_manifest)
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 with tempfile.TemporaryDirectory(prefix='seshadri-publication-replay-') as temp:
  def run(args):return subprocess.run([sys.executable,'-B']+list(map(str,args)),cwd=temp,env=env,capture_output=True)
  d=run(['-c','print(__debug__)']);need(d.returncode==0 and d.stdout==b'True\n','Assertions disabled')
  for folder,script,output in [('author','verify_math.py','verification.json'),('author','test_integrity.py','integrity_results.json'),('independent_audit','independent_verify.py','independent_results.json'),('independent_audit','test_packet_integrity.py','integrity_results.json')]:
   r=run([root/folder/script]);need(r.returncode==0,script+' failed: '+r.stderr.decode());need(r.stdout==regular(root/folder/output),script+' output mismatch')
  for folder,script in [('author','verify_manifest.py'),('independent_audit','verify_packet.py')]:
   r=run([root/folder/script]);need(r.returncode==0 and json.loads(r.stdout)['status']=='PASS',script+' failed')
  author=json.loads(regular(root/'author/verification.json'));audit=json.loads(regular(root/'independent_audit/independent_results.json'))
  need(author['assertions']==85787 and audit['total_assertions']==32975,'Assertion counts')
  need(len(author['negative_controls'])==5 and all(author['negative_controls'].values()),'Author adverse controls')
  need(len(audit['negative_controls'])==8 and all(audit['negative_controls'].values()),'Independent adverse controls')
  source=regular(root/'author/verify_math.py');anchor=b'assert bool(value)';need(source.count(anchor)==1,'Assertion anchor');mutant=Path(temp)/'false_assertion.py';mutant.write_bytes(source.replace(anchor,b'assert False, "synthetic execution control"',1));r=run([mutant]);need(r.returncode!=0 and b'AssertionError' in r.stderr,'False assertion escaped')
 queue_verified=False
 if a.queue is not None:
  b=regular(a.queue);m=json.loads(regular(root/'PUBLICATION.json'))['queue']['updated'];need(len(b)==m['bytes'] and digest(b)==m['sha256'],'Queue bytes');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==m['git_blob_sha1'],'Queue Git blob');queue_verified=True
 need(bind(root,a.expected_manifest)==count,'Packet changed during replay')
 print(json.dumps({'status':'PASS_FOR_SPECIFIED_VERY_GENERAL_SCOPE','queue_status':'already_solved','turns':'1/5','publication_files':count,'manifest_sha256':a.expected_manifest,'frozen_archives_verified':True,'author_replay_exact':True,'author_assertions':85787,'independent_replay_exact':True,'independent_assertions':32975,'author_arithmetic_negative_controls':5,'independent_arithmetic_negative_controls':8,'author_inventory_controls':7,'independent_inventory_controls':14,'false_assertion_rejected':True,'queue_verified':queue_verified,'nagata_proved':False,'formal_verification':False,'peer_review_established':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
