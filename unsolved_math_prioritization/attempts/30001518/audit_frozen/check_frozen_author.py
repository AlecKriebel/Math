#!/usr/bin/env python3
"""Externally anchored, optimization-safe inventory check of the author freeze."""
import argparse, hashlib, json, zipfile
from pathlib import Path, PurePosixPath

MANIFEST_SHA256='802e09153108d1ca826841748adfe751aec2fb2c1fe6718bca1083b0e56eb610'
ARCHIVE_SHA256='164e5736afdf41580386741079a6ee5b05ea5041b56036def48f379970f3042b'
SUMS_SHA256='245ddc1f04c5e6b29f34debc2e42fcc5e6d029ec92089bb3a2aedcd0c6eeb54d'

def require(ok,reason):
    if not ok: raise RuntimeError(reason)

def sha(b): return hashlib.sha256(b).hexdigest()
def unique_object(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,'duplicate JSON key')
        out[key]=value
    return out

def inspect(root, archive=None):
    require(root.is_dir() and not root.is_symlink(),'author root missing or symlinked')
    mb=(root/'AUTHOR_MANIFEST.json').read_bytes()
    require(sha(mb)==MANIFEST_SHA256,'external author manifest anchor mismatch')
    manifest=json.loads(mb,object_pairs_hook=unique_object)
    rows=manifest['files']; names=[r['path'] for r in rows]
    require(len(names)==len(set(names)),'duplicate manifest path')
    for name in names:
        p=PurePosixPath(name)
        require(not p.is_absolute() and len(p.parts)==1 and p.name not in ('','.','..'),'unsafe manifest path')
    expected=set(names)|{'AUTHOR_MANIFEST.json','SHA256SUMS'}
    found=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symlink in author packet')
        if p.is_file(): found.add(p.relative_to(root).as_posix())
        else: require(p.is_dir(),'unexpected filesystem object')
    require(found==expected,'author inventory mismatch')
    for row in rows:
        b=(root/row['path']).read_bytes()
        require(len(b)==row['bytes'],'author byte count mismatch')
        require(sha(b)==row['sha256'],'author file hash mismatch')
    require(sha((root/'SHA256SUMS').read_bytes())==SUMS_SHA256,'external sums anchor mismatch')
    expected_sums=''.join(sha((root/name).read_bytes())+'  '+name+'\n' for name in sorted(expected-{'SHA256SUMS'}))
    require((root/'SHA256SUMS').read_text()==expected_sums,'checksum list mismatch')
    result={'status':'PASS_EXTERNALLY_ANCHORED_AUTHOR_FREEZE','files':len(found),'manifest_sha256':sha(mb)}
    if archive is not None:
        b=archive.read_bytes();require(sha(b)==ARCHIVE_SHA256,'external archive anchor mismatch')
        with zipfile.ZipFile(archive) as z:
            items=z.infolist();znames=[x.filename for x in items if not x.is_dir()]
            require(len(znames)==len(set(znames)),'duplicate archive entry')
            # The author's archive has a verified packet/ prefix.
            require(set(znames)=={'packet/'+name for name in expected},'archive inventory mismatch')
            for name in expected: require(z.read('packet/'+name)==(root/name).read_bytes(),'archive member mismatch')
        result['archive_sha256']=sha(b);result['archive_bytes']=len(b)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('packet',type=Path);p.add_argument('--archive',type=Path)
    a=p.parse_args();print(json.dumps(inspect(a.packet,a.archive),sort_keys=True,indent=2))
