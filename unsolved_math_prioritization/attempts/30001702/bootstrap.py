#!/usr/bin/env python3
"""Externally trusted gate; python -I -S -B bootstrap.py ROOT MANIFEST_SHA [ENTRY]."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: require -I -S -B before any nonbuiltin import')
import hashlib, io, json, os, stat, tempfile, zipfile
from pathlib import Path, PurePosixPath
AUTHOR={'APPROACH_LOG.md','PROOF.md','README.md','RESULTS.json','SOURCE_METADATA.json','certificate.py','verify_bundle.py'}
AUDIT={'ACCEPTANCE.json','ADVERSARIAL_AUDIT.md','AUTHOR_CONTROL_RESULTS.json','EXPANDED_LEMMAS.md','INDEPENDENT_RESULTS.json','README.md','SOURCE_AUDIT.json','audit_controls.py','independent_check.py','verify_audit.py'}
ROOT={'README.md','SCOPE_CLARIFICATION.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_TEST_RESULTS.json','PUBLICATION_MANIFEST.json','bootstrap.py','isolated_runner.py','verify_publication.py','test_publication.py'}
PINS=[('author','MINIMAL_TORUS_30001702_AUTHOR_SAFE_FREEZE.zip',14518,'6bc7b4cc916c38afbc1f7a6289e0dd9643f577d17778ecc79524c1f4646a538b','MINIMAL_TORUS_30001702_EXTERNAL_MANIFEST.json',1130,'9516d60833e6f198eea54faf502f70d151aafe39ed26504ae9be3af05b22bab4',AUTHOR),('audit','MINIMAL_TORUS_30001702_INDEPENDENT_AUDIT_SAFE.zip',24813,'9689ac97f49f3fb525d369aad47d123175cc2e31a2b457d51240900bb96817fd','MINIMAL_TORUS_30001702_AUDIT_EXTERNAL_MANIFEST.json',1616,'9bdfb9469a4f8091f1e4ddbfb3ef62f0074db65eedcc15011cfaba554a6a51fb',AUDIT)]
FILES=ROOT|{'author/'+n for n in AUTHOR}|{'audit/'+n for n in AUDIT}|{'archives/'+r[1] for r in PINS}|{'manifests/'+r[4] for r in PINS}
DIRS={'author','audit','archives','manifests'}
def need(ok,message):
    if not ok:raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
    out={}
    for k,v in pairs:need(k not in out,'duplicate JSON key');out[k]=v
    return out
def js(b):return json.loads(b,object_pairs_hook=unique)
def ordinary_path(value,directory):
    path=Path(value)
    need(path.is_absolute() and '..' not in path.parts,'absolute lexical path without traversal required')
    for p in path.parents:need(stat.S_ISDIR(p.lstat().st_mode),'symlink/non-directory ancestry')
    mode=path.lstat().st_mode
    need(stat.S_ISDIR(mode) if directory else stat.S_ISREG(mode),'nonregular entrypoint or root')
    return path
def read_regular(path):
    st=path.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'nonregular or hardlinked payload')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        actual=os.fstat(fd);need(stat.S_ISREG(actual.st_mode) and actual.st_nlink==1 and (actual.st_dev,actual.st_ino)==(st.st_dev,st.st_ino),'entry changed during read')
        with os.fdopen(fd,'rb',closefd=False) as src:data=src.read()
    finally:os.close(fd)
    return data
def snapshot(value,pin):
    root=ordinary_path(value,True);paths={};dirs=set()
    for current,ds,fs in os.walk(root,followlinks=False):
        for n in ds+fs:
            p=Path(current)/n;rel=p.relative_to(root).as_posix();mode=p.lstat().st_mode
            if stat.S_ISDIR(mode):dirs.add(rel)
            else:need(stat.S_ISREG(mode),'nonregular payload: '+rel);paths[rel]=p
    need(dirs==DIRS and set(paths)==FILES,'strict inventory mismatch')
    data={n:read_regular(p) for n,p in paths.items()}
    raw=data['PUBLICATION_MANIFEST.json'];need(digest(raw)==pin,'external publication manifest pin mismatch');m=js(raw)
    need(type(m) is dict and set(m)=={'schema','files'} and m['schema']=='minimal-torus-publication-sha256-v1','publication schema')
    need(type(m['files']) is dict and set(m['files'])==FILES-{'PUBLICATION_MANIFEST.json'},'manifest inventory')
    for n,record in m['files'].items():
        need(type(record) is dict and set(record)=={'bytes','sha256'} and type(record['bytes']) is int and record['bytes']>=0,'manifest record schema')
        need(record=={'bytes':len(data[n]),'sha256':digest(data[n])},'payload hash mismatch: '+n)
    for role,an,sz,sha,mn,msz,msha,names in PINS:
        ar=data['archives/'+an];mr=data['manifests/'+mn]
        need((len(ar),digest(ar))==(sz,sha) and (len(mr),digest(mr))==(msz,msha),'immutable archive/manifest pin mismatch')
        entries=js(mr)['files'];need({r['path'] for r in entries}==names and len(entries)==len(names),'frozen manifest inventory')
        with zipfile.ZipFile(io.BytesIO(ar)) as z:
            infos=z.infolist();need(len(infos)==len(names) and set(z.namelist())==names,'archive inventory')
            for info in infos:
                n=info.filename;p=PurePosixPath(n)
                need(p.name==n and not p.is_absolute() and stat.S_ISREG(info.external_attr>>16) and not info.is_dir(),'archive member type/path')
                b=data[role+'/'+n];need(z.read(info)==b,'archive/member byte mismatch')
            for r in entries:need(r=={'path':r['path'],'bytes':len(data[role+'/'+r['path']]),'sha256':digest(data[role+'/'+r['path']])},'external frozen manifest mismatch')
    return data

def main():
    ordinary_path(str(Path(__file__).absolute()),False)
    need(3<=len(sys.argv)<=4,'usage: ROOT EXTERNAL_MANIFEST_SHA [verify_publication.py|test_publication.py|integrity]')
    root,pin=sys.argv[1:3];entry=sys.argv[3] if len(sys.argv)==4 else 'verify_publication.py'
    need(entry in {'verify_publication.py','test_publication.py','integrity'},'unsupported entrypoint')
    data=snapshot(root,pin)
    if entry=='integrity':print(json.dumps({'status':'PASS','files':len(data),'archives':2,'archive_members':17},sort_keys=True,indent=2));return
    # Execute verified bytes in a private snapshot, never a second read from input.
    with tempfile.TemporaryDirectory(prefix='minimal torus validated ') as td:
        copied=Path(td)/'package';copied.mkdir()
        for name,b in data.items():p=copied/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        sys.argv=[str(copied/entry),'--expected-manifest',pin]
        exec(compile(data[entry],str(copied/entry),'exec'),{'__name__':'__main__','__file__':str(copied/entry)})
if __name__=='__main__':
    try:main()
    except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
