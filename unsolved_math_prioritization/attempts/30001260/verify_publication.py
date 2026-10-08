#!/usr/bin/env python3
"""Pinned source-free integrity/replay checker; not a mathematical proof checker."""
import argparse, hashlib, json, os, pathlib, re, stat, subprocess, sys, zipfile

FROZEN = {
 'author': ('MANIFEST.json','3f689988d6844b90d70a1f3bbeb18dcbdecc769c8a98ed6c6f5f34053bc01757',21349,'80adc712a807f61e5b3daf948e356002d475cd44b5763408b05af1f70491aba0',14),
 'audit': ('AUDIT_MANIFEST.json','aebb74e42fcfeb2f3ee6a7427d98563847707ab111879305cbf1cd20cf4affbb',40467,'d6027ee9b74773b8bc5d8372a9158bb0ea55cf2ac023e6cf8f60214d836afa30',11),
}
def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def safe(name):
    return isinstance(name,str) and name and '\\' not in name and '\0' not in name and not name.startswith('/') and all(x not in ('','.','..') for x in name.split('/'))
def unique_pairs(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'duplicate JSON key');out[k]=v
    return out
def parse(raw): return json.loads(raw,object_pairs_hook=unique_pairs)
def validate(root,pin,replay=True):
    root=pathlib.Path(root).absolute()
    need(not root.is_symlink() and root.is_dir(),'unsafe packet root')
    need(isinstance(pin,str) and re.fullmatch('[0-9a-f]{64}',pin),'invalid manifest pin')
    mf=root/'PUBLIC_MANIFEST.json'
    need(not mf.is_symlink() and mf.is_file(),'unsafe manifest')
    raw=mf.read_bytes();need(sha(raw)==pin,'manifest digest mismatch')
    m=parse(raw);need(set(m)=={'schema','files'} and m['schema']==1,'manifest schema')
    need(isinstance(m['files'],list),'manifest files list')
    wanted={};dirs=set()
    for r in m['files']:
        need(isinstance(r,dict) and set(r)=={'path','bytes','sha256'},'record schema')
        n=r['path'];need(safe(n) and n!='PUBLIC_MANIFEST.json' and n not in wanted,'unsafe or duplicate path')
        need(type(r['bytes']) is int and r['bytes']>=0,'invalid byte count')
        need(isinstance(r['sha256'],str) and re.fullmatch('[0-9a-f]{64}',r['sha256']),'invalid file digest')
        wanted[n]=r
        dirs.update(str(p) for p in pathlib.PurePosixPath(n).parents if str(p)!='.')
    actual=set();founddirs=set()
    for base,ds,fs in os.walk(root,followlinks=False):
        for n in ds:
            p=pathlib.Path(base)/n;need(stat.S_ISDIR(p.lstat().st_mode) and not p.is_symlink(),'nonregular directory')
            founddirs.add(p.relative_to(root).as_posix())
        for n in fs:
            p=pathlib.Path(base)/n;need(stat.S_ISREG(p.lstat().st_mode) and not p.is_symlink(),'nonregular file')
            actual.add(p.relative_to(root).as_posix())
    need(actual==set(wanted)|{'PUBLIC_MANIFEST.json'} and founddirs==dirs,'exact inventory mismatch')
    for n,r in wanted.items():
        b=(root/n).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'file mismatch: '+n)
    for name,(manifest,mpin,size,zpin,count) in FROZEN.items():
        folder=root/name;need(sha((folder/manifest).read_bytes())==mpin,'frozen manifest pin')
        zpath=root/'archives'/f'{name}.zip';b=zpath.read_bytes()
        need(len(b)==size and sha(b)==zpin,'frozen archive pin')
        members={p.name for p in folder.iterdir()}
        need(len(members)==count and all(p.is_file() for p in folder.iterdir()),'frozen folder')
        with zipfile.ZipFile(zpath) as z:
            names=z.namelist();need(len(names)==count and len(set(names))==count and set(names)==members,'archive inventory')
            for info in z.infolist():
                need(safe(info.filename) and '/' not in info.filename and not info.is_dir(),'unsafe archive member')
                mode=info.external_attr>>16;need(not stat.S_ISLNK(mode),'archive symlink')
                need(z.read(info)==(folder/info.filename).read_bytes(),'archive member mismatch')
    need((root/'audit/AUTHOR_PACKET.zip').read_bytes()==(root/'archives/author.zip').read_bytes(),'embedded author archive')
    status=parse((root/'PUBLICATION_STATUS.json').read_bytes())
    acceptance=parse((root/'audit/ACCEPTANCE.json').read_bytes())
    need(status['problem_id']==acceptance['problem_id']==30001260,'target mismatch')
    need(status['status']==acceptance['status']=='unsolved' and status['turns']=='5/5','disposition mismatch')
    need(status['full_resolution'] is False and acceptance['full_resolution'] is False,'false resolution')
    if replay:
        for flags in ([],['-O']):
            run=subprocess.run([sys.executable,'-I',*flags,str(root/'audit/verify_audit.py'),FROZEN['audit'][1]],capture_output=True,check=True,cwd=root.parent)
            need(parse(run.stdout)['status']=='PASS','audit replay failed')
    return {'status':'PASS','manifest_sha256':pin,'file_count_including_manifest':len(actual),'frozen_expanded_files':25,'unchanged_archives':2,'archive_member_equivalence':'PASS','normal_and_optimized_replay':'PASS' if replay else 'NOT_RUN','scope':'Inventory and finite diagnostics only; not a mathematical proof, source-authenticity signature, smooth-realization certificate or CI result.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest_sha256');p.add_argument('--root',default=str(pathlib.Path(__file__).absolute().parent));p.add_argument('--integrity-only',action='store_true');a=p.parse_args()
    print(json.dumps(validate(a.root,a.manifest_sha256,not a.integrity_only),indent=2,sort_keys=True))
