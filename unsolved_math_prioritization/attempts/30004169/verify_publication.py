#!/usr/bin/env python3
"""Fail-closed portable integrity checks and assertion-enabled bounded replay."""
import argparse,hashlib,json,os,re,subprocess,sys,tempfile,zipfile
from pathlib import Path
PINS={
 'milnor_witt_30004169/AUTHOR_MANIFEST.json':'fc8c3f58258b73b16b491fff45663c78d8a409bea72fd67b35b8260b366755a2',
 'milnor_witt_30004169_independent_audit/AUDIT_MANIFEST.json':'22f00a618df4a4db54b02ef322a3e17fe7816deef3cf4b841a943b50b8be6951',
 'MILNOR_WITT_30004169_AUTHOR_SAFE_FREEZE.zip':'1a31a422207531ae6a37553f5de289ce358b445f5473f70939ca3a335f992f42',
 'MILNOR_WITT_30004169_INDEPENDENT_AUDIT.zip':'7668ec058e31b044130a8a68b48a937b46e44166d4e9f9036c23f9287933cc1c'}
def need(ok,message):
 if not ok:raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def regular(p):
 need(p.is_file() and not p.is_symlink(),'Nonregular file: '+str(p));return p.read_bytes()
def bind(root,pin):
 need(re.fullmatch('[0-9a-f]{64}',pin) is not None,'Invalid external pin')
 raw=regular(root/'MANIFEST.json');need(digest(raw)==pin,'External manifest mismatch');manifest=json.loads(raw)
 need(manifest['schema']=='milnor-witt-30004169-publication-manifest-v1','Manifest schema');names=set()
 for row in manifest['files']:
  need(set(row)=={'path','bytes','sha256'},'Record schema');name=row['path'];need(isinstance(name,str),'Path type');p=Path(name)
  need(name not in names and name!='MANIFEST.json' and not p.is_absolute() and '..' not in p.parts and '\\' not in name and str(p)==name,'Unsafe/duplicate/self path')
  need(type(row['bytes']) is int and row['bytes']>=0,'Invalid size');need(isinstance(row['sha256'],str) and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'Invalid hash')
  b=regular(root/name);need(len(b)==row['bytes'] and digest(b)==row['sha256'],'File mismatch: '+name);names.add(name)
 entries=list(root.rglob('*'));need(not any(p.is_symlink() for p in entries),'Symlink in packet')
 need({p.relative_to(root).as_posix() for p in entries if p.is_file()}==names|{'MANIFEST.json'},'File inventory mismatch')
 dirs={str(p) for name in names for p in Path(name).parents if str(p)!='.'}
 need({p.relative_to(root).as_posix() for p in entries if p.is_dir()}==dirs,'Directory inventory mismatch')
 for name,expected in PINS.items():need(digest(regular(root/name))==expected,'Frozen pin mismatch: '+name)
 for folder,mname,archive,count in [
  ('milnor_witt_30004169','AUTHOR_MANIFEST.json','MILNOR_WITT_30004169_AUTHOR_SAFE_FREEZE.zip',9),
  ('milnor_witt_30004169_independent_audit','AUDIT_MANIFEST.json','MILNOR_WITT_30004169_INDEPENDENT_AUDIT.zip',8)]:
  inner=json.loads(regular(root/folder/mname))['files'];inner_names=set(inner)|{mname}
  need(len(inner_names)==count and inner_names=={p.name for p in (root/folder).iterdir()},'Inner inventory')
  for name,row in inner.items():
   need(Path(name).name==name,'Unsafe inner name');b=regular(root/folder/name);need(len(b)==row['bytes'] and digest(b)==row['sha256'],'Inner binding')
  with zipfile.ZipFile(root/archive) as z:
   members=z.infolist();need(len(members)==count and {m.filename for m in members}=={folder+'/'+n for n in inner_names},'Archive inventory')
   for m in members:
    need(not m.is_dir() and (m.external_attr>>16)&0o170000!=0o120000,'Archive nonregular');need(z.read(m)==regular(root/m.filename),'Archive bytes')
 m=json.loads(regular(root/'PUBLICATION.json'));need(m['problem_id']==30004169 and m['rank']==745 and m['status']=='unsolved' and m['turns']=='5/5' and m['substantive_approaches_used']==5,'Target/status scope')
 need(all(m[x] is False for x in ['original_problem_solved','novelty_claim','formal_verification','raw_dataset_included','source_pdfs_or_extracts_included','private_coordination_included','nonflasqueness_is_descent_counterexample','cech_defect_vanishing_proved']),'Claim boundary')
 need(m['queue']['changed_cells']==['Status','Turns'] and m['queue']['changed_indices']==[8,9],'Queue cell scope')
 v=json.loads(regular(root/'milnor_witt_30004169_independent_audit/AUDIT_VERDICT.json'));need(v['verdict']=='PASS' and v['original_problem_solved'] is False and v['mandatory_corrections']==[],'Audit verdict scope')
 return len(names)+1

def main():
 p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);p.add_argument('--queue',type=Path);a=p.parse_args()
 need(__debug__ and sys.flags.optimize==0,'Python optimization is forbidden; disabled assertions are not verification')
 sys.dont_write_bytecode=True;root=Path(__file__).resolve().parent;count=bind(root,a.expected_manifest)
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 with tempfile.TemporaryDirectory(prefix='milnor-witt-replay-') as temp:
  def run(args):return subprocess.run([sys.executable,'-B']+list(map(str,args)),cwd=temp,env=env,capture_output=True)
  d=run(['-c','print(__debug__); assert False, "execution control"']);need(d.returncode!=0 and d.stdout==b'True\n' and b'AssertionError' in d.stderr,'False assertion escaped')
  author=root/'milnor_witt_30004169';audit=root/'milnor_witt_30004169_independent_audit'
  r=run([author/'controls.py']);need(r.returncode==0 and r.stdout==regular(author/'CHECK_RESULTS.json'),'Author exact replay')
  r=run([author/'verify.py']);need(r.returncode==0 and json.loads(r.stdout)['exact_replay']=='PASS','Author verifier')
  r=run([audit/'independent_verifier.py']);need(r.returncode==0,'Independent replay: '+r.stderr.decode());actual=json.loads(r.stdout);expected=json.loads(regular(audit/'INDEPENDENT_RESULTS.json'))
  need(set(actual)=={'problem_id','bounded_controls','original_problem_solved','freeze','cech','faces','weight_zero','orientation','finite_totalization'},'Offline independent result scope')
  for key,value in actual.items():need(value==expected[key],'Independent output mismatch: '+key)
  r=run([audit/'verify_audit.py']);need(r.returncode==0 and json.loads(r.stdout)['self_contained_independent_controls']=='PASS','Audit verifier')
  need(actual['cech']['integral_basis_contractions']==34992 and actual['cech']['negative_controls_detected']==2,'Cech controls')
  need(actual['faces']['facets_only_mutation_rejected_by_vertex'] and actual['weight_zero']['nonzero_splice_mutation_detected'] and actual['freeze']['one_byte_integrity_mutation_detected'],'Adverse controls')
 queue_verified=False
 if a.queue is not None:
  b=regular(a.queue);m=json.loads(regular(root/'PUBLICATION.json'))['queue']['updated'];need(len(b)==m['bytes'] and digest(b)==m['sha256'],'Queue bytes');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==m['git_blob_sha1'],'Queue Git blob');queue_verified=True
 need(bind(root,a.expected_manifest)==count,'Packet changed during replay')
 print(json.dumps({'status':'PASS within unresolved scope','queue_status':'unsolved','turns':'5/5','publication_files':count,'manifest_sha256':a.expected_manifest,'frozen_archives_verified':True,'author_replay_exact':True,'independent_offline_replay_exact':True,'independent_integral_cech_contractions':34992,'independent_adverse_controls':5,'false_assertion_rejected':True,'queue_verified':queue_verified,'original_problem_solved':False,'formal_verification':False,'external_source_dataset_catalog_checks':'Recorded by frozen audit; not replayed without optional external inputs.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
