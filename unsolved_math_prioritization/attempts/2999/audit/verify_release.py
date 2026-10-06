#!/usr/bin/env python3
"""Verify an externally pinned archive and manifest, including exact membership.
Supply the expected hashes from the separate audit receipt or trusted record.
This checks integrity, not mathematical truth. It extracts nothing.
"""
import argparse,hashlib,json,pathlib,stat,sys,zipfile

def require(ok,msg):
    if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def verify(archive,manifest,archive_sha,manifest_sha):
    a=pathlib.Path(archive).read_bytes();mbytes=pathlib.Path(manifest).read_bytes()
    require(digest(a)==archive_sha,'External archive pin mismatch')
    require(digest(mbytes)==manifest_sha,'External manifest pin mismatch')
    m=json.loads(mbytes)
    require(len(a)==m['zip']['bytes'] and digest(a)==m['zip']['sha256'],'Manifest archive pin mismatch')
    entries=m['entries'];expected={e['path']:e for e in entries}
    require(len(expected)==len(entries),'Duplicate manifest members')
    with zipfile.ZipFile(archive) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        require(len(names)==len(set(names)),'Duplicate ZIP members')
        require(set(names)==set(expected),'Exact membership mismatch')
        require(z.testzip() is None,'ZIP CRC mismatch')
        for info in infos:
            p=pathlib.PurePosixPath(info.filename)
            require(not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename,'Unsafe archive path')
            require(not info.is_dir(),'Directory member forbidden')
            require(not stat.S_ISLNK(info.external_attr>>16),'Symlink member forbidden')
            b=z.read(info);e=expected[info.filename]
            require(len(b)==e['bytes'] and digest(b)==e['sha256'],'Entry pin mismatch: '+info.filename)
    return {'integrity':'PASS','members':len(entries),'archive_sha256':digest(a),'manifest_sha256':digest(mbytes)}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for x in ['archive','manifest','expected-archive-sha256','expected-manifest-sha256']:p.add_argument('--'+x,required=True)
    a=p.parse_args();print(json.dumps(verify(a.archive,a.manifest,a.expected_archive_sha256,a.expected_manifest_sha256),indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile) as e:
        print('VERIFY FAILED: '+str(e),file=sys.stderr);sys.exit(1)
