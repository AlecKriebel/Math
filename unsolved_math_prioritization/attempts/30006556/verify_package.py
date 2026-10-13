#!/usr/bin/env python3
"""Verify immutable inputs and replay exact controls with assertions active."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,stat,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
ARCHIVES=[('TWO_SPARSE_DISTANCES_30006556_AUTHOR_SAFE_FREEZE.zip','author',21557,'315ca399e06f5ee40f519fd841150a90342b3391325782a2cd4bead04adaf6d0',10),('TWO_SPARSE_DISTANCES_30006556_INDEPENDENT_AUDIT_SAFE.zip','audit',18338,'87d3f86cbb34d7be5debb4315ed8e28833172f8a22bf99628ed38b3607082bc6',7)]
def require(ok,message):
    if not ok:raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def inventory():
    mf=ROOT/'PUBLICATION_MANIFEST.json';require(mf.is_file() and not mf.is_symlink(),'invalid publication manifest')
    data=json.loads(mf.read_bytes());require(data['format']=='recursive-sha256-inventory-v1','unknown inventory format')
    entries=data['files'];paths=[r['path'] for r in entries]
    require(len(paths)==len(set(paths)),'duplicate manifest path')
    for name in paths:
        p=PurePosixPath(name)
        require(isinstance(name,str) and name and not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and str(p)==name and '\\' not in name and name!='PUBLICATION_MANIFEST.json','unsafe manifest path')
    expected=set(paths)|{'PUBLICATION_MANIFEST.json'}
    dirs={str(p) for name in paths for p in PurePosixPath(name).parents if str(p)!='.'}
    actual_files=set();actual_dirs=set()
    for p in ROOT.rglob('*'):
        name=p.relative_to(ROOT).as_posix();require(not p.is_symlink(),'symlink: '+name)
        if p.is_dir():actual_dirs.add(name)
        else:require(stat.S_ISREG(p.stat().st_mode),'nonregular file: '+name);actual_files.add(name)
    require(actual_files==expected,'file inventory mismatch');require(actual_dirs==dirs,'directory inventory mismatch')
    for r in entries:
        b=(ROOT/r['path']).read_bytes();require(len(b)==r['bytes'] and digest(b)==r['sha256'],'file hash mismatch: '+r['path'])
    return len(expected)
def verify_archives():
    outputs=[]
    for name,folder,size,sha,count in ARCHIVES:
        p=ROOT/'archives'/name;b=p.read_bytes();require(len(b)==size and digest(b)==sha,'frozen archive mismatch: '+name)
        with zipfile.ZipFile(p) as z:
            members=z.namelist();require(len(members)==count==len(set(members)),'archive count/duplicate mismatch')
            require(all(Path(n).name==n and n not in ('','.','..') for n in members),'unsafe archive member')
            require(set(members)=={x.name for x in (ROOT/folder).iterdir()},'extracted inventory mismatch')
            for n in members:
                require(not z.getinfo(n).is_dir(),'archive directory entry')
                require(z.read(n)==(ROOT/folder/n).read_bytes(),'archive member mismatch: '+n)
        outputs.append({'archive':name,'bytes':size,'sha256':sha,'members':count,'status':'PASS'})
    return outputs
BOOTSTRAP='import runpy,sys; assert __debug__ and sys.flags.optimize == 0; runpy.run_path(sys.argv[1],run_name="__main__")'
def run(rel,result=None):
    script=ROOT/rel
    proc=subprocess.run([sys.executable,'-I','-B','-c',BOOTSTRAP,str(script)],cwd=script.parent,check=True,capture_output=True)
    require(not proc.stderr,'unexpected checker stderr: '+rel)
    if result:require(proc.stdout==(ROOT/result).read_bytes(),'result bytes differ: '+rel)
    return {'script':rel,'assertions_active':True,'status':'PASS','stdout_bytes':len(proc.stdout),'stdout_sha256':digest(proc.stdout),'matches_frozen_results':bool(result)}
def main():
    count=inventory();archives=verify_archives()
    jobs=[run('author/verify_manifest.py'),run('audit/verify_audit_manifest.py'),run('author/verify_math.py','author/CHECK_RESULTS.json'),run('audit/independent_checks.py','audit/INDEPENDENT_RESULTS.json')]
    print(json.dumps({'status':'PASS','publication_files':count,'complete_recursive_inventory':True,'archives':archives,'checks':jobs,'mathematical_scope':'Audited partial claims only; general problem unresolved, 5/5 approaches; no novelty claim.'},indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
