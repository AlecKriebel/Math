#!/usr/bin/env python3
"""Portable, exact publication verification, effective under Python -O."""
import argparse,hashlib,json,os,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).absolute().parent
PINS={'author':('MANIFEST.json','1d99dd20f9ed095b3d199b2802f0198ccab4832654e65b27d35f0643e1fa5f3c'),'audit':('MANIFEST.json','0b6b8ed792a531fb262b2b6cf536ba637e250e8d7a9519db7e712cf8dbc7ba75')}
def need(v,m):
    if not v:raise RuntimeError('PACKAGE FAILURE: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(b):return {'bytes':len(b),'sha256':sha(b)}
def safe(n):
    p=Path(n);need(bool(n) and not p.is_absolute() and '..' not in p.parts and p.as_posix()==n,'unsafe path')
def inventory(root):
    fs=set();ds=set()
    for p in [root,*root.parents]:need(not p.is_symlink(),'linked package ancestor')
    for p in root.rglob('*'):
        need(not p.is_symlink(),'linked package member')
        n=p.relative_to(root).as_posix()
        if p.is_file():fs.add(n)
        elif p.is_dir():ds.add(n)
        else:need(False,'nonregular member')
    return fs,ds
def check_manifest(root,name,expected=None):
    raw=(root/name).read_bytes();need(expected is None or sha(raw)==expected,'external manifest pin');data=json.loads(raw);files=data['files'];fs,ds=inventory(root)
    need(set(files)==fs-{name},'exact file inventory')
    derived=set()
    for n,value in files.items():
        safe(n);need(n!=name,'self-listed manifest');need(ident((root/n).read_bytes())==value,'file identity '+n)
        derived.update(p.as_posix() for p in Path(n).parents if p!=Path('.'))
    need(ds==derived,'exact directory inventory')
    return sha(raw)
def queue_check(a,b):
    before=Path(a).read_bytes();after=Path(b).read_bytes();d=json.loads((ROOT/'QUEUE_DELTA.json').read_text())
    need(ident(before)==d['before'] and ident(after)==d['after'],'queue identity')
    lines=before.splitlines(keepends=True);hits=[i for i,l in enumerate(lines) if b'| 30000432 / OWR-1194-001 |' in l];need(len(hits)==1,'queue unique target');i=hits[0];cells=lines[i].split(b'|')
    need(cells[1].strip()==b'811' and cells[8]==b' queued ' and cells[9]==b' 0/5 ','queue original cells');cells[8]=b' unsolved ';cells[9]=b' 5/5 ';lines[i]=b'|'.join(cells)
    need(b''.join(lines)==after,'exact two-cell queue patch')
    return {'only_changed_cells':['Status','Turns'],'all_other_bytes_preserved':True,'before':ident(before),'after':ident(after)}
def replay(path,opt,expected,args):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
    cmd=[sys.executable]+(['-O'] if opt else [])+[str(ROOT/path),*args]
    r=subprocess.run(cmd,cwd=ROOT.parent,env=env,capture_output=True)
    need(r.returncode==0,'replay '+path+': '+r.stderr.decode(errors='replace'));need(r.stdout==(ROOT/expected).read_bytes(),'frozen output '+path)
    return {'checker':path,'stdout':ident(r.stdout),'expected':expected}
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest');p.add_argument('--integrity-only',action='store_true');p.add_argument('--queue-base');p.add_argument('--queue-updated');args=p.parse_args();need(bool(args.queue_base)==bool(args.queue_updated),'both queue paths required')
    outer=check_manifest(ROOT,'PUBLICATION_MANIFEST.json',args.expected_manifest)
    for d,(n,pin) in PINS.items():check_manifest(ROOT/d,n,pin)
    verdict=json.loads((ROOT/'VERDICT.json').read_text());archives=[]
    for row in verdict['archives']:
        b=(ROOT/row['archive']).read_bytes();need(ident(b)=={'bytes':row['bytes'],'sha256':row['sha256']},'archive pin')
        with zipfile.ZipFile(ROOT/row['archive']) as z:
            ns=z.namelist();need(len(ns)==len(set(ns))==row['members'],'archive cardinality');need(z.testzip() is None,'archive CRC');fs,_=inventory(ROOT/row['directory']);need(set(ns)=={row['prefix']+n for n in fs},'archive exact members')
            for n in ns:safe(n);need(z.read(n)==(ROOT/row['directory']/n[len(row['prefix']):]).read_bytes(),'archive member equality')
        archives.append({'archive':row['archive'],'members':len(ns),**ident(b)})
    author_files=inventory(ROOT/'author')[0]
    need(author_files==inventory(ROOT/'audit/author')[0],'nested author inventory')
    for n in author_files:need((ROOT/'author'/n).read_bytes()==(ROOT/'audit/author'/n).read_bytes(),'nested author byte equality '+n)
    runs=[]
    if not args.integrity_only:
        opt=bool(sys.flags.optimize)
        runs.append(replay('author/verify.py',opt,'author/RESULTS.json',[]))
        runs.append(replay('audit/independent_verify.py',opt,'audit/RESULTS.json',[]))
    result={'status':'pass','problem_id':30000432,'disposition':'unsolved_5_of_5','publication_manifest_sha256':outer,'package_files':len(inventory(ROOT)[0]),'archives':archives,'replays':runs,'geometric_proof_machine_certified':False,'full_target_solved':False}
    if args.queue_base:result['queue']=queue_check(args.queue_base,args.queue_updated)
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
