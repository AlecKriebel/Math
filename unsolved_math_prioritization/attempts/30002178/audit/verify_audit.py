#!/usr/bin/env python3
"""Verify an externally anchored audit manifest and the frozen author archive.
Usage: python verify_audit.py AUDIT_DIRECTORY AUTHOR_ZIP EXPECTED_AUDIT_MANIFEST_SHA256
No author modules or network access are used.
"""
import hashlib,json,re,stat,sys,zipfile
from pathlib import Path,PurePosixPath
ARCHIVE_SHA='24f88fd09d1f753306be377bcb96e17a0dd85d2ccb674975873a6046ddcbe02d'
AUTHOR_MANIFEST_SHA='12236b07d02cdc19409631ce6b56ae41d6509876a3c7fa200e2aafda1df329b6'

def require(value,label):
    if not value:raise ValueError(label)

def digest(b):return hashlib.sha256(b).hexdigest()

def unique_keys(pairs):
    d={}
    for k,v in pairs:
        require(k not in d,'duplicate JSON key');d[k]=v
    return d

def json_read(raw):return json.loads(raw,object_pairs_hook=unique_keys)

def entries(raw):
    obj=json_read(raw)
    require(obj['schema']=='sha256-bytes-v1','manifest schema')
    require(isinstance(obj['files'],list),'manifest file list')
    out={}
    for row in obj['files']:
        name=row['path'];q=PurePosixPath(name)
        require(isinstance(name,str) and re.fullmatch(r'[A-Za-z0-9_./-]+',name),'path characters')
        require(not q.is_absolute() and str(q)==name and not any(p in ('.','..','') for p in q.parts),'unsafe path')
        require(name!='MANIFEST.json' and name not in out,'duplicate or self manifest path')
        require(type(row['bytes']) is int and row['bytes']>=0,'byte count')
        require(isinstance(row['sha256'],str) and re.fullmatch(r'[a-f0-9]{64}',row['sha256']),'hash format')
        out[name]=row
    return out

def verify_directory(root,expected_manifest):
    root=Path(root);require(root.is_dir() and not root.is_symlink(),'audit directory')
    mf=root/'MANIFEST.json';require(mf.is_file() and not mf.is_symlink(),'manifest file')
    raw=mf.read_bytes();require(digest(raw)==expected_manifest,'external audit manifest anchor')
    expected=entries(raw);actual={}
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symlink prohibited')
        if p.is_dir():continue
        require(stat.S_ISREG(p.stat().st_mode),'nonregular payload')
        name=p.relative_to(root).as_posix()
        if name!='MANIFEST.json':actual[name]=p
    require(set(actual)==set(expected),'audit file set')
    for name,p in actual.items():
        b=p.read_bytes();row=expected[name]
        require(len(b)==row['bytes'] and digest(b)==row['sha256'],'audit bytes '+name)
    return len(actual)

def verify_author(archive):
    p=Path(archive);b=p.read_bytes()
    require(len(b)==29040 and digest(b)==ARCHIVE_SHA,'author archive anchor')
    with zipfile.ZipFile(p) as z:
        infos=z.infolist();names=[x.filename for x in infos]
        require(len(names)==13 and len(set(names))==13,'author archive file count')
        require(z.testzip() is None,'author ZIP CRC')
        for info in infos:
            require(not info.is_dir() and PurePosixPath(info.filename).name==info.filename,'author flat safe file')
            require(not stat.S_ISLNK(info.external_attr>>16),'author ZIP symlink')
        raw=z.read('MANIFEST.json');require(digest(raw)==AUTHOR_MANIFEST_SHA,'author manifest anchor')
        expected=entries(raw);require(set(names)==set(expected)|{'MANIFEST.json'},'author member set')
        for name,row in expected.items():
            data=z.read(name);require(len(data)==row['bytes'] and digest(data)==row['sha256'],'author member hash '+name)
    return len(names)

def main():
    require(len(sys.argv)==4,'arguments: AUDIT_DIRECTORY AUTHOR_ZIP EXPECTED_AUDIT_MANIFEST_SHA256')
    files=verify_directory(sys.argv[1],sys.argv[3]);members=verify_author(sys.argv[2])
    print(json.dumps({'status':'PASS','audit_payload_files':files,'author_archive_files':members,'author_archive_sha256':ARCHIVE_SHA},sort_keys=True))

if __name__=='__main__':main()
