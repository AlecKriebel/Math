#!/usr/bin/env python3
"""Independent rebuilt-producer portability, exclusions, and path controls."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent; A=HERE.parent.parent; C=HERE/'.cache'/'producers';C.mkdir(parents=True,exist_ok=True)
expected=hashlib.sha256((A/'publication/verification_package.zip').read_bytes()).hexdigest(); rows=[]
def copy(name):
 d=C/name;shutil.copytree(A,d,ignore=shutil.ignore_patterns('.cache','qa','__pycache__','scratch','receipts','package_preflight*'));return d
def run(d):return subprocess.run([sys.executable,str(d/'publication/make_package.py')],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
def check(name,d,reason):
 p=run(d);assert p.returncode and reason in p.stderr,(name,p.returncode,p.stderr)
 rows.append({'case':name,'status':'REJECTED_AS_REQUIRED','reason':reason})
def append(d,relative,data=b'Independent exclusion control.\n'):
 p=d/'original'/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 s=d/'ORIGINAL_SNAPSHOT.json';obj=json.loads(s.read_text());obj['files'].append({'path':relative,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()});s.write_text(json.dumps(obj))
for name in ('ordinary/checkout','.cache/checkout','scratch/checkout'):
 d=copy(name);p=run(d);assert p.returncode==0,p.stderr;h=hashlib.sha256((d/'publication/verification_package.zip').read_bytes()).hexdigest();assert h==expected
 rows.append({'case':name,'status':'EXACT_BUILD','sha256':h})
for part in ('.cache','sources','scratch','qa','.secrets'):
 d=copy('direct_'+part);append(d,part+'/probe.md');check('direct_'+part,d,'Excluded source')
 for reverse in (False,True):
  tag=('allowed_to_forbidden_' if reverse else 'forbidden_to_allowed_')+part;d=copy(tag)
  real=d/'original'/ (part if reverse else 'permitted');real.mkdir();(real/'probe.md').write_bytes(b'Independent exclusion control.\n')
  alias=d/'original'/('permitted_alias' if reverse else part);alias.symlink_to(real,target_is_directory=True)
  relative=alias.name+'/probe.md';append(d,relative);check(tag,d,'Excluded source')
 # A two-hop alias cannot launder a forbidden middle target either: lexical allowed,
 # resolved forbidden path catches it regardless of the intermediate alias spelling.
 d=copy('two_hop_'+part);real=d/'original'/part;real.mkdir();(real/'probe.md').write_text('Control\n');mid=d/'original'/'mid';mid.symlink_to(real,target_is_directory=True);alias=d/'original'/'permitted_alias';alias.symlink_to(mid,target_is_directory=True);append(d,'permitted_alias/probe.md');check('two_hop_'+part,d,'Excluded source')
d=copy('leaf_symlink');p=d/'publication/weighted_centers.tex';p.unlink();p.symlink_to(d/'publication/README.md');check('leaf_symlink',d,'Invalid or duplicate source')
d=copy('parent_escape');outside=C/'outside';outside.mkdir();(outside/'probe.json').write_text('{}\n');shutil.rmtree(d/'root_reproduction');(d/'root_reproduction').symlink_to(outside,target_is_directory=True);check('parent_escape',d,'Source escapes the audit')
d=copy('private');append(d,'probe.private.md');check('private',d,'Invalid or duplicate source')
d=copy('traversal');append(d,'../probe.md');check('traversal',d,'Invalid relative path')
# unsafe archive spellings are rejected before any source access.
sys.path.insert(0,str(A/'publication'));from integrity import safe_path
bad=['../x','a/../x','/absolute','a//x','a/./x','a\\x','C:x','a/','']
for x in bad:
 try:safe_path(x)
 except RuntimeError:rows.append({'case':'archive_path_'+repr(x),'status':'REJECTED_AS_REQUIRED'})
 else:raise AssertionError(x)
result={'status':'PASS','expected_zip_sha256':expected,'cases':rows,'exact_relocated_builds':3,'required_rejections':len(rows)-3,'canonical_files_modified':False}
(HERE/'PRODUCER_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
