#!/usr/bin/env python3
"""Exact portable publication verification, effective with Python -O."""
import hashlib,json,os,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(value,message):
    if not value:raise RuntimeError('PACKAGE FAILURE: '+message)
def sha(data):return hashlib.sha256(data).hexdigest()
def safe_name(name):
    p=Path(name)
    need(not p.is_absolute() and '..' not in p.parts and p.as_posix()==name,'unsafe relative path')
def payload(root):
    paths=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'symlink in package')
        if p.is_file() and '__pycache__' not in p.parts:paths.add(p.relative_to(root).as_posix())
    return paths

def manifest(root,name):
    raw=(root/name).read_bytes();data=json.loads(raw);listed=set()
    for row in data['files']:
        path=row['path'];safe_name(path)
        need(path not in listed and path!=name,'duplicate or self-listed path');listed.add(path)
        b=(root/path).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'payload hash '+path)
    need(payload(root)-{name}==listed,'exact inventory '+name)
    return sha(raw)

def replay(path,optimized,expected):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
    p=subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(ROOT/path)],cwd=ROOT,env=env,capture_output=True)
    need(p.returncode==0,'replay exit '+path+': '+p.stderr.decode(errors='replace'))
    need(p.stdout==(ROOT/expected).read_bytes(),'replay bytes '+path)
    return {'path':path,'optimized':optimized,'expected':expected,'stdout_sha256':sha(p.stdout)}

outer=manifest(ROOT,'PUBLICATION_MANIFEST.json')
author_manifest=manifest(ROOT/'author','MANIFEST.json')
audit_manifest=manifest(ROOT/'audit','MANIFEST.json')
verdict=json.loads((ROOT/'VERDICT.json').read_text());archives=[]
for row in verdict['archives']:
    path=ROOT/row['archive'];data=path.read_bytes()
    need(len(data)==row['bytes'] and sha(data)==row['sha256'],'archive identity')
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist();need(len(names)==len(set(names))==row['members'],'archive cardinality')
        for name in names:safe_name(name)
        need(set(names)==payload(ROOT/row['directory']),'archive exact membership')
        for name in names:need(archive.read(name)==(ROOT/row['directory']/name).read_bytes(),'archive member '+name)
    archives.append({'archive':row['archive'],'sha256':sha(data),'members':len(names)})
original=(ROOT/'author/verify.py').read_bytes();fixed=(ROOT/'verify.py').read_bytes()
old=b'    assert b';new=b'    if not b:\n        raise AssertionError("verification check failed")'
need(original.count(old)==1 and original.replace(old,new)==fixed,'exact hardening derivative')
need(fixed==(ROOT/'audit/corrections/verify.py').read_bytes(),'operative audit correction identity')
need(b'--- a/verify.py\n+++ b/verify.py\n' in (ROOT/'audit/VERIFY_HARDENING.patch').read_bytes(),'supplied patch identity')
runs=[replay('author/verify.py',False,'author/results.json')]
for optimized in [False,True]:
    runs.append(replay('verify.py',optimized,'author/results.json'))
    runs.append(replay('audit/independent_verify.py',optimized,'audit/independent_results.json'))
runs.append(replay('audit/run_controls.py',False,'audit/CONTROL_RESULTS.json'))
print(json.dumps({'status':'pass','publication_manifest_sha256':outer,'author_manifest_sha256':author_manifest,'audit_manifest_sha256':audit_manifest,'archives':archives,'replays':runs,'operative_checker':'verify.py','mathematical_disposition':'unsolved_5_of_5'},sort_keys=True,indent=2))
