#!/usr/bin/env python3
"""Verify the exact audited author artifacts. This is not a proof checker."""
import argparse
import hashlib
import json
import stat
import sys
import zipfile
from pathlib import Path

ZIP_SHA256 = '72f9afea11f77de85242d98b32b8769beafdf33599ea939a93ba923bf897f652'
ZIP_BYTES = 13913
EXTERNAL_SHA256 = '2c07eb0303f15e18f7937bc7ec554d0b2384fae38395fa8475334478288a8606'
PREFIX = 'tangle_stabilizer_2756/'
MEMBERS = {
 'APPROACH_LOG.md': (2462, 'c636273e9faf539d7834812e463f436da98047c624c858927eff65f6b87be491'),
 'MANIFEST.json': (1060, '018231d39c0491f2a50aa22942681092d57178304e32ca579755b90ed68fd712'),
 'PROOF.md': (10369, '5421fed5844469f6835649a5a6e167f7c238c729da15364afeeb59ba18357ea4'),
 'README.md': (1756, 'b6c2f12582500b083974740c76fd4c2d83f2781f9ff13d92ee75cfcafdf5ea97'),
 'REPORT.md': (5456, 'b553dc5fb28503b8b7a049e618607b641fcd5ea3bb834b421bb1325ed92ceb4c'),
 'STATUS.json': (1614, '23183df6ba7eebe9298d086c567188dd159b4e08a8bbb0eb5b102d4a5772ed8d'),
 'VERIFICATION_METADATA.json': (6498, '69d8272a9b0567301d56f5dfaeb8c5cb52e7f3d8655f3b9d0f2881afe202302f'),
}

def require(condition, message):
 if not condition:
  raise ValueError(message)

def sha(data):
 return hashlib.sha256(data).hexdigest()

def verify_members(archive):
 """Validate contents separately so mutation tests can bypass the outer pin."""
 with zipfile.ZipFile(archive) as z:
  require(z.testzip() is None, 'CRC failure')
  names=z.namelist()
  require(len(names)==len(MEMBERS) and set(names)=={PREFIX+s for s in MEMBERS}, 'member allowlist failure')
  for info in z.infolist():
   mode=info.external_attr >> 16
   require(not info.is_dir() and not stat.S_ISLNK(mode), 'directory or symlink member')
   name=info.filename[len(PREFIX):]
   data=z.read(info.filename)
   size,digest=MEMBERS[name]
   require(len(data)==size and sha(data)==digest, 'member pin failure: '+name)
   text=data.decode('utf-8')
   if name.endswith('.json'):
    json.loads(text)
  manifest=json.loads(z.read(PREFIX+'MANIFEST.json'))
  rows=manifest['files']
  require(len(rows)==len(MEMBERS)-1 and {r['path'] for r in rows}==set(MEMBERS)-{'MANIFEST.json'}, 'inner manifest coverage failure')
  for r in rows:
   require((r['bytes'],r['sha256'])==MEMBERS[r['path']], 'inner manifest pin failure')
  status=json.loads(z.read(PREFIX+'STATUS.json'))
  require(status['problem_id']==2756 and status['status']=='stalled_partial' and status['full_solution'] is False, 'scope failure')
  require(status['approaches_used']==3 and status['approach_limit']==5, 'approach count failure')
 return len(MEMBERS)

def verify(zip_path, external_path):
 data=zip_path.read_bytes()
 require(len(data)==ZIP_BYTES and sha(data)==ZIP_SHA256, 'exact author ZIP pin failure')
 ext=external_path.read_bytes()
 require(sha(ext)==EXTERNAL_SHA256, 'exact external manifest pin failure')
 m=json.loads(ext)
 require(m['problem_id']==2756 and m['bytes']==ZIP_BYTES and m['sha256']==ZIP_SHA256, 'external identity failure')
 rows=m['archive_members']
 require(len(rows)==len(MEMBERS) and {r['path'] for r in rows}=={PREFIX+s for s in MEMBERS}, 'external coverage failure')
 for r in rows:
  require((r['bytes'],r['sha256'])==MEMBERS[r['path'][len(PREFIX):]], 'external member pin failure')
 count=verify_members(zip_path)
 return {'problem_id':2756,'exact_author_artifacts_verified':True,'member_count':count,'mathematical_proof_checked_by_this_script':False}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('author_zip',type=Path)
 p.add_argument('author_external_manifest',type=Path)
 args=p.parse_args()
 try:
  result=verify(args.author_zip,args.author_external_manifest)
 except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as e:
  print('FAIL: '+str(e),file=sys.stderr)
  return 1
 print(json.dumps(result,sort_keys=True))
 return 0

if __name__=='__main__':
 raise SystemExit(main())
