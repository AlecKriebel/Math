#!/usr/bin/env python3
"""Strict portable inventory, immutable bindings and scoped replay; Python -O safe."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, re, subprocess, sys, zipfile
ROOT=Path(__file__).absolute().parent
PINS={'author':('MANIFEST.json','b8f24c4403ad0c93be653da10572689ecb683741e4e387b97996ebb05a717609'), 'audit':('AUDIT_MANIFEST.json','c6015afbde76381d7f7eb2d27f00bf6a0afff22d4d163aa3d2be9c5810e312ec')}
ARCHIVES={'author':('KLEINIAN_BOUNDARY_6200010_AUTHOR_SAFE_FREEZE.zip',20470,'a2fc0e27b9bd81dca28450f20cdbbda139b2e50933126bd6b9db577662cc0dcf',10),'audit':('KLEINIAN_BOUNDARY_6200010_INDEPENDENT_AUDIT_SAFE.zip',39630,'d1f99fa9ec76e240ecb80f365c9f98a820402e5345723e34842c6a4285d6b491',19)}
def need(v,m):
    if not v: raise RuntimeError('PACKAGE FAILURE: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(b):return {'bytes':len(b),'sha256':sha(b)}
def unique(pairs):
    d={}
    for k,v in pairs: need(k not in d,'duplicate JSON key');d[k]=v
    return d
def read(p):return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=unique)
def safe(n):
    need(isinstance(n,str) and n and '\\' not in n,'path type');p=PurePosixPath(n)
    need(not p.is_absolute() and '..' not in p.parts and p.as_posix()==n and n!='.','unsafe or noncanonical path')
def inventory(root):
    for p in [root,*root.parents]:need(not p.is_symlink(),'linked package ancestor')
    fs=set();ds=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'linked member');n=p.relative_to(root).as_posix()
        if p.is_file():fs.add(n)
        elif p.is_dir():ds.add(n)
        else:need(False,'nonregular member')
    return fs,ds
def check_manifest(root,name,pin=None):
    fs,ds=inventory(root);raw=(root/name).read_bytes();need(pin is None or sha(raw)==pin,'manifest pin');m=read(root/name)
    need(type(m.get('problem_id')) is int and m['problem_id']==6200010,'manifest problem');items=m.get('files');need(isinstance(items,list) and items,'manifest files')
    expected={};derived=set()
    for row in items:
        need(isinstance(row,dict) and set(row)=={'path','bytes','sha256'},'manifest entry shape');n=row['path'];safe(n);need(n!=name and n not in expected,'duplicate or self inventory')
        need(type(row['bytes']) is int and row['bytes']>=0 and isinstance(row['sha256'],str) and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'identity shape');expected[n]=row
        derived.update(p.as_posix() for p in PurePosixPath(n).parents if p!=PurePosixPath('.'))
    need(fs==set(expected)|{name},'exact file inventory');need(ds==derived,'exact directory inventory')
    for n,row in expected.items():need(ident((root/n).read_bytes())=={'bytes':row['bytes'],'sha256':row['sha256']},'file identity '+n)
    return sha(raw)
def queue_check(a,b):
    before=Path(a).read_bytes();after=Path(b).read_bytes();d=read(ROOT/'QUEUE_DELTA.json');need(ident(before)==d['before'] and ident(after)==d['after'],'queue binding')
    lines=before.splitlines(keepends=True);hits=[i for i,l in enumerate(lines) if b'| 6200010 / AMR-061-0010 |' in l];need(len(hits)==1,'queue target');i=hits[0];cells=lines[i].split(b'|');need(cells[1].strip()==b'807' and cells[8]==b' queued ' and cells[9]==b' 0/5 ','queue cells');cells[8]=b' unsolved ';cells[9]=b' 5/5 ';lines[i]=b'|'.join(cells);need(b''.join(lines)==after,'exact two-cell queue delta');return {'all_other_bytes_preserved':True,'changed_cells':['Status','Turns']}
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest');p.add_argument('--queue-base');p.add_argument('--queue-updated');a=p.parse_args();need(bool(a.queue_base)==bool(a.queue_updated),'both queue paths required')
    outer=check_manifest(ROOT,'PUBLICATION_MANIFEST.json',a.expected_manifest)
    for d,(n,pin) in PINS.items():check_manifest(ROOT/d,n,pin)
    for d,(n,size,pin,count) in ARCHIVES.items():
        path=ROOT/'archives'/n;need(ident(path.read_bytes())=={'bytes':size,'sha256':pin},'archive pin')
        with zipfile.ZipFile(path) as z:
            ns=z.namelist();need(len(ns)==len(set(ns))==count,'zip cardinality');need(z.testzip() is None,'zip CRC');need(set(ns)==inventory(ROOT/d)[0],'zip exact members')
            for name in ns:safe(name);need(z.read(name)==(ROOT/d/name).read_bytes(),'zip member binding')
    need(inventory(ROOT/'author')[0]==inventory(ROOT/'audit/author')[0],'author duplicate inventory')
    for n in inventory(ROOT/'author')[0]:need((ROOT/'author'/n).read_bytes()==(ROOT/'audit/author'/n).read_bytes(),'author duplicate bytes')
    v=read(ROOT/'VERDICT.json');need(v['status']=='unsolved' and v['turns_used']==v['turn_limit']==5 and v['full_target_solved'] is False and v['independent_agent_audit']=='PASS_SCOPED_PARTIALS_ORIGINAL_UNRESOLVED','verdict scope')
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
    r=subprocess.run([sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(ROOT/'audit/verify_audit.py')],cwd=ROOT.parent,env=env,capture_output=True,text=True,timeout=240)
    need(r.returncode==0,'strict audit replay: '+r.stderr);result=json.loads(r.stdout,object_pairs_hook=unique);need(result['status']=='PASS' and result['author_checks']==32400 and result['independent_checks']==5055 and result['original_problem_resolved'] is False,'audit output')
    out={'status':'PASS','problem_id':6200010,'disposition':'unsolved_5_of_5','publication_manifest_sha256':outer,'package_files':len(inventory(ROOT)[0]),'optimized':bool(sys.flags.optimize),'author_checks':32400,'independent_checks':5055,'immutable_author_and_audit':True,'strict_inventory':True,'original_problem_resolved':False,'formal_proof':False}
    if a.queue_base:out['queue']=queue_check(a.queue_base,a.queue_updated)
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
