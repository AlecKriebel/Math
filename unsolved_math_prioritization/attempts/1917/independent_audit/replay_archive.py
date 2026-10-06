#!/usr/bin/env python3
"""Check externally pinned archive and manifest, every member and its safe path."""
import argparse,hashlib,json,stat,zipfile
from pathlib import Path,PurePosixPath

def require(x,msg):
 if not x:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(archive,manifest,archive_sha256,manifest_sha256):
 b=Path(archive).read_bytes();mb=Path(manifest).read_bytes()
 require(sha(b)==archive_sha256,'external archive pin')
 require(sha(mb)==manifest_sha256,'external manifest pin')
 m=json.loads(mb)
 require((len(b),sha(b))==(m['archive_bytes'],m['archive_sha256']),'manifest archive identity')
 members=m['members'];require(len(members)==m['member_count'],'member count')
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();require(len(names)==len(set(names)),'duplicate archive name')
  require(sorted(names)==sorted(x['name'] for x in members),'exact member set')
  for v in members:
   name=v['name'];p=PurePosixPath(name)
   require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,'unsafe member path')
   info=z.getinfo(name);mode=info.external_attr>>16
   require(stat.S_ISREG(mode) and mode&0o222==0,'member must be read-only regular file')
   raw=z.read(name);require((len(raw),sha(raw))==(v['bytes'],v['sha256']),'member bytes/hash')
 return {'archive_sha256':sha(b),'archive_bytes':len(b),'members_checked':len(members),'status':'PASS','mathematical_proof_checked_by_this_program':False}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for key in ['archive','manifest','archive-sha256','manifest-sha256']:p.add_argument('--'+key,required=True)
 a=p.parse_args();print(json.dumps(verify(a.archive,a.manifest,a.archive_sha256,a.manifest_sha256),indent=2,sort_keys=True))
