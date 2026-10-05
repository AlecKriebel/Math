#!/usr/bin/env python3
"""Pinned recursive integrity, immutable archives, exact queue diff, normal-mode replay."""
import argparse,hashlib,json,os,re,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
MANIFEST='PUBLICATION_MANIFEST.json'
PINS={'author':('AUTHOR_MANIFEST.json','28ec0d19ba6891338c95a37f24d8842de69300cb78984a65367b465596704920'), 'audit':('AUDIT_MANIFEST.json','3850910bb6ad5112c68d6a34695bd4b408491903fef05cad1e65a1e4454110a3')}
ZIPS=[('KOUROVKA_2551_AUTHOR_SAFE_FREEZE.zip',18835,'6ba3c58803407218391afc5d045939f8c3f0e8d750756e516aa5de0c300a7e01','kourovka_2551/','author'),('KOUROVKA_2551_INDEPENDENT_AUDIT.zip',17871,'cf2b22bfcb21f1ea3c58c396e0b4e210e903a3f7b0ccae22fa2de01a89b9173b','kourovka_2551_independent_audit/','audit')]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
def pairs(items):
 d={}
 for k,v in items:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def js(b):return json.loads(b,object_pairs_hook=pairs)
def inventory(root):
 need(root.is_dir() and not root.is_symlink(),'root directory')
 files=set();dirs=set()
 for p in root.rglob('*'):
  need(not p.is_symlink(),'symlink')
  n=p.relative_to(root).as_posix()
  if p.is_dir():dirs.add(n)
  else:need(stat.S_ISREG(p.stat().st_mode),'nonregular file');files.add(n)
 return files,dirs
def manifest(root,name,expected):
 b=(root/name).read_bytes();need(sha(b)==expected,'manifest pin '+name);m=js(b);rows={}
 for row in m['files']:
  n=row['path'];p=PurePosixPath(n)
  need(re.fullmatch(r'[A-Za-z0-9_./-]+',n) and not p.is_absolute() and '..' not in p.parts and str(p)==n and n not in ('.',name) and n not in rows,'unsafe or duplicate manifest path')
  need(type(row['bytes']) is int and row['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',row['sha256']),'invalid manifest values');rows[n]=row
 actual,dirs=inventory(root)
 need(actual==set(rows)|{name},'recursive file inventory')
 need(dirs=={str(p) for n in rows for p in PurePosixPath(n).parents if str(p)!='.'},'recursive directory inventory')
 for n,row in rows.items():
  b=(root/n).read_bytes();need((len(b),sha(b))==(row['bytes'],row['sha256']),'file mismatch '+n)
 return m,actual
def queue_check(root,qpath):
 q=js((root/'QUEUE_PATCH.json').read_bytes());need(qpath.is_file() and not qpath.is_symlink(),'queue file')
 b=qpath.read_bytes();need((len(b),sha(b),blob(b))==(q['updated_bytes'],q['updated_sha256'],q['updated_blob']),'updated queue bytes')
 lines=b.splitlines(keepends=True);ix=[i for i,l in enumerate(lines) if b'| 2551 /' in l]
 need(ix==[q['line_number']-1],'queue identity');i=ix[0];new=lines[i].split(b'|');old=new[:]
 need(len(new)==14 and new[1].strip()==b'768' and new[2].strip()==b'2551 / KOU-21.42','target row')
 need(new[8]==b' already_solved ' and new[9]==b' 1/5 ','disposition')
 for j,k in [(8,'Status'),(9,'Turns'),(11,'Findings')]:
  need(new[j].decode()==q['new_values'][k],'new queue value');old[j]=q['old_values'][k].encode()
 need([j for j in range(len(new)) if new[j]!=old[j]]==q['changed_indices']==[8,9,11],'exact three-cell diff')
 need(q['changed_cells']==['Status','Turns','Findings'],'named cell diff')
 lines[i]=b'|'.join(old);base=b''.join(lines)
 need((len(base),sha(base),blob(base))==(q['base_bytes'],q['base_sha256'],q['base_blob']),'exact queue restoration')
 return {'status':'PASS','changed_cells':q['changed_cells'],'all_other_bytes_preserved':True,'stale_header_preserved':True}
def verify(root,pin,qpath):
 need(not sys.flags.optimize,'normal Python mode required; do not use -O')
 m,files=manifest(root,MANIFEST,pin);need(m['problem_id']==2551 and m['schema']=='kourovka-2551-publication-v1','publication schema')
 for folder,(name,pin) in PINS.items():
  inner,names=manifest(root/folder,name,pin);need(inner['problem_id']==2551 and len(names)==8,'inner identity')
 for name,size,pin,prefix,folder in ZIPS:
  p=root/'freezes'/name;b=p.read_bytes();need((len(b),sha(b))==(size,pin),'ZIP pin')
  expected={prefix+n for n in inventory(root/folder)[0]}
  with zipfile.ZipFile(p) as z:
   need(len(z.namelist())==len(expected) and set(z.namelist())==expected,'ZIP inventory')
   for info in z.infolist():
    need(not info.is_dir() and not stat.S_ISLNK(info.external_attr>>16),'ZIP member type')
    need(z.read(info)==(root/folder/info.filename[len(prefix):]).read_bytes(),'ZIP member bytes')
 s=js((root/'PUBLICATION_STATUS.json').read_bytes())
 need(s['status']=='already_solved' and s['turns_used']==1 and s['turn_limit']==5 and s['author_controls']==4455 and s['independent_controls']==6567,'status')
 for k in ['original_2003_proof_obtained','original_2003_proof_independently_audited','human_peer_review_claimed','novelty_claimed','editorial_acceptance_claimed','finite_controls_prove_universal_result','scholarly_source_contents_bundled','raw_dataset_contents_bundled','private_coordination_bundled']:need(s[k] is False,'scope boundary '+k)
 return {'integrity':'PASS','package_files':len(files),'inner_manifests':'PASS','frozen_archives_and_all_members':'PASS','queue':queue_check(root,qpath) if qpath else 'NOT_RUN: no queue supplied'}
def run(script,*args):
 with tempfile.TemporaryDirectory(prefix='kourovka replay cwd ') as cwd:
  p=subprocess.run([sys.executable,'-I','-B',str(script),*map(str,args)],cwd=cwd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=600)
 need(p.returncode==0,'replay failure '+script.name+': '+p.stderr.decode());return p.stdout
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('expected_manifest');p.add_argument('--queue',type=Path);a=p.parse_args();r=a.root.resolve();q=a.queue.resolve() if a.queue else None
 result=verify(r,a.expected_manifest,q)
 author=run(r/'author/verify_math.py');need(author==(r/'author/CHECK_RESULTS.json').read_bytes(),'author saved result');result['author_controls']=js(author)['total_checks']
 result['author_manifest_replay']=js(run(r/'author/verify_manifest.py'))
 independent=run(r/'audit/verify_independent.py');need(independent==(r/'audit/INDEPENDENT_RESULTS.json').read_bytes(),'independent saved result');result['independent_controls']=js(independent)['total_checks']
 result['audit_replay']=js(run(r/'audit/verify_audit.py','--author-dir',r/'author','--author-zip',r/'freezes/KOUROVKA_2551_AUTHOR_SAFE_FREEZE.zip'))
 need(result['audit_replay']['status']=='PASS' and len(result['audit_replay']['freeze_mutations_rejected'])==5 and all(result['audit_replay']['freeze_mutations_rejected'].values()),'audit replay checks')
 need(result['author_controls']==4455 and result['independent_controls']==6567,'control counts')
 result['external_source_and_dataset_replay']='NOT_RUN: optional external evidence is not bundled'
 verify(r,a.expected_manifest,q);print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
