#!/usr/bin/env python3
"""Strict portable publication checks; no network, dependencies or proof claims."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,re,stat,subprocess,sys,zipfile
ROOT=Path(__file__).absolute().parent
ARCHIVES={'author':('KLEINIAN_BOUNDARY_6200061_AUTHOR_SAFE_FREEZE.zip',30172,'9d404dd597724c207e50afe80f97ec7f4b66e8c957193972fe2011c8853563d8',9,'kleinian_boundary_6200061/','fc47e35e492d41ab4b1b1a49e3ed43bf4d5a275861e1f90e3028691b9d099f03'),'audit':('KLEINIAN_BOUNDARY_6200061_INDEPENDENT_AUDIT_SAFE.zip',17114,'17e47788e6aa081a98305cd4cdaac61906525e0afe1f4935a6aacaade6d8a291',7,'kleinian_boundary_6200061_independent_audit/','a3b2688fd90b2e59c768fcf6058c449e4ae1c7fe49d536376317287604ff55e0')}
def need(v,m):
 if not v:raise ValueError('PACKAGE FAILURE: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(b):return {'bytes':len(b),'sha256':sha(b)}
def unique(pairs):
 out={}
 for k,v in pairs:need(k not in out,'duplicate JSON key');out[k]=v
 return out
def read(p):return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
def safe(n):
 need(isinstance(n,str) and n and '\\' not in n,'path type');p=PurePosixPath(n);need(not p.is_absolute() and '..' not in p.parts and p.as_posix()==n and n!='.','unsafe or noncanonical path')
def inventory(root):
 for p in [root,*root.parents]:need(not p.is_symlink(),'linked ancestor')
 fs=set();ds=set()
 for p in root.rglob('*'):
  need(not p.is_symlink(),'linked member');n=p.relative_to(root).as_posix()
  if p.is_file():fs.add(n)
  elif p.is_dir():ds.add(n)
  else:need(False,'nonregular member')
 return fs,ds
def manifest(root,name,pin=None):
 fs,ds=inventory(root);raw=(root/name).read_bytes();need(pin is None or sha(raw)==pin,'manifest external pin');m=read(root/name);items=m.get('files');need(isinstance(items,(list,dict)) and items,'manifest files')
 if isinstance(items,dict):items=[{'path':n,**row} for n,row in items.items()]
 expected={};dirs=set()
 for row in items:
  need(isinstance(row,dict) and set(row)=={'path','bytes','sha256'},'entry shape');n=row['path'];safe(n);need(n!=name and n not in expected,'duplicate/self path');need(type(row['bytes']) is int and row['bytes']>=0 and isinstance(row['sha256'],str) and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'identity shape');expected[n]=row
  dirs.update(p.as_posix() for p in PurePosixPath(n).parents if p!=PurePosixPath('.'))
 need(fs==set(expected)|{name},'exact file inventory');need(ds==dirs,'exact directory inventory')
 for n,row in expected.items():need(ident((root/n).read_bytes())=={'bytes':row['bytes'],'sha256':row['sha256']},'file identity '+n)
 return sha(raw)
def queue_check(a,b):
 before=Path(a).read_bytes();after=Path(b).read_bytes();q=read(ROOT/'QUEUE_DELTA.json');need(ident(before)==q['before'] and ident(after)==q['after'],'queue identity');lines=before.splitlines(keepends=True);hits=[i for i,l in enumerate(lines) if b'| 6200061 / AMR-061-0061 |' in l];need(len(hits)==1,'queue target');i=hits[0];c=lines[i].split(b'|');need(c[1].strip()==b'810' and c[8]==b' queued ' and c[9]==b' 0/5 ','queue cells');c[8]=b' unsolved ';c[9]=b' 5/5 ';lines[i]=b'|'.join(c);need(b''.join(lines)==after,'exact two-cell delta');return {'status':'PASS','all_other_bytes_preserved':True,'changed_cells':['Status','Turns']}
def main():
 p=argparse.ArgumentParser();p.add_argument('--expected-manifest');p.add_argument('--queue-base');p.add_argument('--queue-updated');a=p.parse_args();need(bool(a.queue_base)==bool(a.queue_updated),'both queue paths required');outer=manifest(ROOT,'PUBLICATION_MANIFEST.json',a.expected_manifest)
 need(read(ROOT/'PUBLICATION_MANIFEST.json')['problem_id']==6200061,'publication identity')
 for d,(n,size,pin,count,prefix,mpin) in ARCHIVES.items():
  manifest(ROOT/d,'MANIFEST.json',mpin);zpath=ROOT/'archives'/n;need(ident(zpath.read_bytes())=={'bytes':size,'sha256':pin},'archive external pin')
  with zipfile.ZipFile(zpath) as z:
   ns=z.namelist();need(len(ns)==len(set(ns))==count,'ZIP inventory');need(z.testzip() is None,'ZIP CRC');need(set(ns)=={prefix+s for s in inventory(ROOT/d)[0]},'ZIP members')
   for info in z.infolist():
    safe(info.filename);need(not stat.S_ISLNK(info.external_attr>>16),'ZIP link');need(z.read(info.filename)==(ROOT/d/info.filename[len(prefix):]).read_bytes(),'ZIP member binding')
 v=read(ROOT/'VERDICT.json');need(v['problem_id']==6200061 and v['rank']==810 and v['status']=='unsolved' and v['turns_used']==v['turn_limit']==5 and v['general_problem_solved'] is False and v['existential_attainment_disproved'] is False and v['formal_proof'] is False and v['independent_agent_audit']=='ACCEPTED_PARTIAL_NOT_SOLVED','verdict scope')
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1';cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(ROOT/'audit/independent_checks.py'),str(ROOT/'archives'/ARCHIVES['author'][0])];r=subprocess.run(cmd,cwd='/',env=env,capture_output=True,text=True,timeout=240);need(r.returncode==0,'audit replay '+r.stderr);j=json.loads(r.stdout,object_pairs_hook=unique);need(j['audit_result']=='ACCEPTED_PARTIAL_NOT_SOLVED' and j['general_problem_solved'] is False and j['controls']['independent_rejection_runs']==44 and len(j['controls']['semantic_limit_cases'])==3,'audit scope/count')
 out={'status':'PASS','problem_id':6200061,'disposition':'unsolved_5_of_5','general_problem_solved':False,'formal_proof':False,'optimized':bool(sys.flags.optimize),'publication_manifest_sha256':outer,'package_files':len(inventory(ROOT)[0]),'strict_inventory':True,'immutable_author_and_audit':True,'algebra':j['algebra'],'independent_rejection_runs':44,'semantic_limit_cases':3,'semantic_limit_archive_rejections':6,'optional_complete_corpus_identity':'NOT_RUN','optional_source_pdf_retrieval':'NOT_RUN','queue':{'status':'NOT_RUN'}}
 if a.queue_base:out['queue']=queue_check(a.queue_base,a.queue_updated)
 print(json.dumps(out,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
