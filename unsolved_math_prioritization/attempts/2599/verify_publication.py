#!/usr/bin/env python3
"""Strict, portable publication integrity and disposable replay for KOU-21.90."""
import argparse,copy,hashlib,json,os,shutil,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
# Independently pinned immutable archives: original author, original audit, accepted v2, delta.
PINS={
 'author_original':('KOUROVKA_2599_AUTHOR_SAFE_FREEZE.zip',59164,'2c4530b0d0daf358e64d8e701ee739bbe97d5a83fa87037a2a2e5d1b47643bba','AUTHOR_MANIFEST.json','7ddf656ed2dc847097cdb3134a578791021748d4cfa9d9202b8bc60c32aa4d0e',14),
 'audit_original':('KOUROVKA_2599_INDEPENDENT_AUDIT.zip',27188,'a6ff5aecfe81e64af531953837b8ce60b72bcf1a609080e5386c9f37f47dd845','AUDIT_MANIFEST.json','f113d6cce2c42e7e366d94a26f5e85261bcebb3181a35397240d27826350dc97',12),
 'author_v2':('KOUROVKA_2599_V2_AUTHOR_SAFE_FREEZE.zip',63061,'f4f6c13056b5053795c076b6a62f61930e3b757a181c4ffa0bed00f23dc4e5f5','AUTHOR_MANIFEST.json','15ce6b84aa22e1c5d217bf6fbe82e6768fbf2e27c654df6bbd7846f3360ed89c',16),
 'delta_acceptance':('KOUROVKA_2599_V2_DELTA_ACCEPTANCE_SAFE_FREEZE.zip',7681,'fe8f3ac2b8cd3d896f31799c518f9d75861f86000addd8982544cbc732b28d07','AUDIT_MANIFEST.json','f1ad4d676490490e70f28ab9553310c7759425335527d7ced3ad0e142e3db5b5',6)}
def require(ok,label):
 if not ok: raise ValueError(label)
def digest(b): return hashlib.sha256(b).hexdigest()
def pairs(items):
 d={}
 for k,v in items:
  require(k not in d,'duplicate JSON key');d[k]=v
 return d
def readjson(path): return json.loads(path.read_bytes(),object_pairs_hook=pairs)
def safe(s):
 p=PurePosixPath(s);return isinstance(s,str) and bool(s) and not p.is_absolute() and p.as_posix()==s and all(x not in ('','.','..') for x in p.parts) and '\\' not in s
def metadata(p):
 b=p.read_bytes();return len(b),digest(b)
def verify(root):
 root=Path(root);require(not root.is_symlink(),'symlink root')
 m=readjson(root/'PUBLICATION_MANIFEST.json');require((m['problem_id'],m['status'],m['turns'])==(2599,'unsolved','5/5'),'manifest scope')
 expected={'PUBLICATION_MANIFEST.json'}
 for e in m['files']:
  name=e['path'];require(safe(name) and name not in expected,'unsafe or duplicate path');expected.add(name)
  p=root/name;require(p.is_file() and not p.is_symlink(),'missing file or symlink');require(metadata(p)==(e['bytes'],e['sha256']),'payload integrity: '+name)
 dirs=set()
 for n in expected:
  p=PurePosixPath(n).parent
  while str(p)!='.': dirs.add(str(p));p=p.parent
 observed=set();actual_dirs=set()
 for p in root.rglob('*'):
  require(not p.is_symlink(),'symlink member');rel=p.relative_to(root).as_posix()
  if p.is_file(): observed.add(rel)
  elif p.is_dir(): actual_dirs.add(rel)
  else: raise ValueError('special file')
 require(observed==expected and actual_dirs==dirs,'strict inventory')
 b=readjson(root/'BINDING.json')
 checks={'problem_id':2599,'problem_number':'KOU-21.90','rank':770,'status':'unsolved','turns':'5/5','controlling_author_version':'v2','acceptance_verdict':'PASS_V2_DELTA_ACCEPTED','remaining_required_corrections':[],'source_explicitly_requires_connectedness':False,'connected_nondegenerate_interpretation':'inferred; authorial intent not verified','connected_nondegenerate_target_resolved':False,'permissive_crown_family_known_in_prior_literature':True,'novelty_claim':False,'global_nonexistence_proved':False,'parameter_sieve':{'range':'2 <= t <= 30','triples':959,'basic_survivors':159,'after_five_certificates':154},'standard_library_audit_checks':155035,'independent_symbolic_identities':46,'frozen_payload_files_preserved':48}
 for k,v in checks.items(): require(b[k]==v,'binding scope: '+k)
 require(len(b['freezes'])==4,'four frozen stages')
 for directory,(archive,size,pin,manifest,mpin,count) in PINS.items():
  ar=root/'archives'/archive;require(metadata(ar)==(size,pin),'archive pin')
  matches=[f for f in b['freezes'] if f['directory']==directory]
  require(len(matches)==1,'freeze binding');f=matches[0]
  require(f==dict(directory=directory,archive='archives/'+archive,bytes=size,sha256=pin,manifest=manifest,manifest_sha256=mpin,member_count=count),'freeze metadata')
  sub=root/directory;require(digest((sub/manifest).read_bytes())==mpin,'manifest pin')
  with zipfile.ZipFile(ar) as z:
   ns=z.namelist();require(len(ns)==count==len(set(ns)) and z.testzip() is None,'ZIP inventory/CRC')
   for i in z.infolist():
    require(safe(i.filename) and PurePosixPath(i.filename).name==i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16)!=stat.S_IFLNK,'unsafe archive member')
    require(z.read(i)==(sub/i.filename).read_bytes(),'archive/member bytes')
   require(set(ns)=={p.name for p in sub.iterdir()},'archive/folder inventory')
  fm=readjson(sub/manifest);seen={manifest}
  for e in fm['files']:
   name=e['name'];require(safe(name) and PurePosixPath(name).name==name and name not in seen,'frozen manifest inventory');seen.add(name)
   require(metadata(sub/name)==(e['bytes'],e['sha256']),'frozen payload hash')
  require(seen==set(ns),'frozen manifest members')
 d=readjson(root/'delta_acceptance/DELTA_ACCEPTANCE.json')
 require(d['verdict']=='PASS_V2_DELTA_ACCEPTED' and d['remaining_required_corrections']==[] and d['math_proofs_code_certificates_outputs_unchanged'] is True,'delta acceptance')
 return {'status':'PASS','problem_id':2599,'files':len(expected),'frozen_files':48,'archives':4,'archive_members':48,'status_scope':'unsolved; 5/5; connected/nondegenerate interpretation inferred'}
def run(root,folder,script,args=()):
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
 probe=subprocess.run([sys.executable,'-B','-c','import sys; print(int(__debug__),sys.flags.optimize)'],cwd=root/folder,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
 require(probe.returncode==0 and probe.stdout==b'1 0\n','child assertion-state sentinel')
 proc=subprocess.run([sys.executable,'-B',str(root/folder/script),*map(str,args)],cwd=root/folder,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300)
 require(proc.returncode==0,script+' failed: '+proc.stderr.decode())
 return proc.stdout

def replay(root):
 before={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
 results=[]
 with tempfile.TemporaryDirectory(prefix='kourovka-2599-replay-') as tmp:
  r=Path(tmp)/'relocated';shutil.copytree(root,r)
  for folder in ('author_original','author_v2'):
   run(r,folder,'verify_manifest.py')
   for script in ('verify_math.py','verify_triples.py','verify_symbolic.py'):
    out=run(r,folder,script);results.append({'directory':folder,'script':script,'stdout_sha256':digest(out)})
   run(r,folder,'verify_manifest.py')
  for script in ('verify_independent.py','verify_symbolic_independent.py','verify_audit_manifest.py'):
   out=run(r,'audit_original',script);results.append({'directory':'audit_original','script':script,'stdout_sha256':digest(out)})
  ar=r/'archives';args=[ar/PINS[x][0] for x in ('author_original','author_v2','audit_original')]
  out=run(r,'delta_acceptance','verify_delta.py',args)
  require(json.loads(out)==readjson(r/'delta_acceptance/DELTA_ACCEPTANCE.json'),'delta output exact')
  run(r,'delta_acceptance','verify_audit_manifest.py')
  a=readjson(r/'audit_original/AUDIT_RESULTS.json');s=readjson(r/'audit_original/SYMBOLIC_AUDIT_RESULTS.json')
  require((a['parameter_count'],a['basic_survivors'],a['post_certificate_survivors'],a['total_checks'],s['identity_count'])==(959,159,154,155035,46),'replay counts')
  provenance=readjson(r/'author_v2/VERSION_PROVENANCE.json')
  for e in provenance['mathematical_replays']:
   script=e['command'].split()[-1]
   require(all(x['stdout_sha256']==e['stdout_sha256'] for x in results if x['script']==script),'stdout provenance')
  verify(r)
  require({p.relative_to(r).as_posix():p.read_bytes() for p in r.rglob('*') if p.is_file()}==before,'generated outputs changed')
 require({p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}==before,'source modified')
 return {'all_generated_outputs_byte_exact':True,'source_unchanged':True,'child_assertions_enabled':True,'sieve_triples':959,'basic_survivors':159,'post_certificate_survivors':154,'standard_library_audit_checks':155035,'independent_symbolic_identities':46,'exact_editorial_delta_accepted':True,'runs':results}
def selftest(root):
 rejected=[]
 tests=['changed_file','missing_file','extra_file','extra_empty_directory','extra_pycache','symlink_file','symlink_directory','duplicate_entry','unsafe_path','duplicate_json_key','scope_change','archive_change','freeze_pin_change']
 for label in tests:
  with tempfile.TemporaryDirectory(prefix='kourovka-2599-negative-') as tmp:
   r=Path(tmp)/'copy';shutil.copytree(root,r);mp=r/'PUBLICATION_MANIFEST.json';m=readjson(mp)
   if label=='changed_file': (r/'README.md').write_bytes(b'changed')
   elif label=='missing_file': (r/'README.md').unlink()
   elif label=='extra_file': (r/'extra.txt').write_text('extra')
   elif label=='extra_empty_directory': (r/'empty').mkdir()
   elif label=='extra_pycache': (r/'__pycache__').mkdir()
   elif label=='symlink_file': (r/'README.md').unlink();(r/'README.md').symlink_to(root/'README.md')
   elif label=='symlink_directory': shutil.rmtree(r/'author_v2');(r/'author_v2').symlink_to(root/'author_v2',target_is_directory=True)
   elif label=='duplicate_entry': m['files'].append(m['files'][0]);mp.write_text(json.dumps(m))
   elif label=='unsafe_path': m['files'][0]['path']='../escape';mp.write_text(json.dumps(m))
   elif label=='duplicate_json_key': mp.write_text(mp.read_text().replace('"problem_id": 2599','"problem_id": 2599, "problem_id": 2599'))
   elif label in ('scope_change','freeze_pin_change'):
    bp=r/'BINDING.json';b=readjson(bp)
    if label=='scope_change': b['source_explicitly_requires_connectedness']=True
    else: b['freezes'][0]['sha256']='0'*64
    bp.write_text(json.dumps(b));n,h=metadata(bp)
    for e in m['files']:
     if e['path']=='BINDING.json': e.update(bytes=n,sha256=h)
    mp.write_text(json.dumps(m))
   elif label=='archive_change': (r/'archives'/PINS['author_v2'][0]).write_bytes(b'wrong')
   try: verify(r)
   except (ValueError,KeyError,FileNotFoundError,zipfile.BadZipFile): rejected.append(label)
   else: raise ValueError('negative control accepted: '+label)
 return rejected
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');p.add_argument('--selftest',action='store_true');a=p.parse_args()
 result=verify(ROOT)
 if a.replay: result['replay']=replay(ROOT)
 if a.selftest: result['negative_controls_rejected']=selftest(ROOT)
 print(json.dumps(result,indent=2,sort_keys=True))
