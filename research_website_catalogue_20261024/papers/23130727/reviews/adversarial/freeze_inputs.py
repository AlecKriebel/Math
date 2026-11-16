"""Own opaque custody capture; no source programme imports or execution."""
from pathlib import Path
import hashlib
import json
import stat
import datetime

E=Path(__file__).resolve().parent
P=E.parents[3]
S=P/'papers/23130727/sources'
C=P/'verification/supported-cycle-focal-independent-code-audit-sol-20261115/ACTUAL623_QUALIFIED_CORE.json'
def digest(b):return hashlib.sha256(b).hexdigest()
if C.stat().st_size!=13162 or digest(C.read_bytes())!='0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104':raise ValueError('core authority')
contract=json.loads(C.read_bytes())
source_files=[];source_dirs=[]
for p in sorted(S.rglob('*')):
 mode=p.lstat().st_mode
 if stat.S_ISREG(mode):source_files.append(p)
 elif stat.S_ISDIR(mode):source_dirs.append(p.relative_to(S).as_posix())
 else:raise ValueError('nonordinary source entry')
if len(source_files)!=128 or len(source_dirs)!=18:raise ValueError('source namespace')
core=[]
for row in contract['files']:
 p=Path(row['path']);b=p.read_bytes()
 if len(b)!=row['bytes'] or digest(b)!=row['SHA256']:raise ValueError('current qualified core')
 core.append(p)
if len(core)!=18:raise ValueError('17 original plus sole405b')
(E/'inputs/blobs').mkdir(parents=True,exist_ok=False)
rows=[]
for p in source_files+core:
 b=p.read_bytes();h=digest(b);dest=E/'inputs/blobs'/h
 if not dest.exists():dest.write_bytes(b)
 if dest.read_bytes()!=b:raise ValueError('opaque copy')
 rows.append({'path':str(p),'bytes':len(b),'SHA256':h,'copy':dest.relative_to(E).as_posix()})
obj={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'files':rows,'source_namespace':{'path':str(S),'files':[p.relative_to(S).as_posix() for p in source_files],'directories':source_dirs},'core_files':[str(p) for p in core],'qualified_core':'17 original plus sole separately authorized405b checkpoint; not18 original unchanged','raw_inputs_ignored_before_creation':True,'source_programmes_executed':[],'science_code_results_or_opinion_bodies_exposed_by_capture':False}
(E/'PROTECTED_INPUTS.json').write_text(json.dumps(obj,indent=2)+'\n')
(E/'QUALIFIED_CORE_AUTHORITY_BINDING.json').write_text(json.dumps({'original_by_reference':{'path':str(C),'bytes':C.stat().st_size,'SHA256':digest(C.read_bytes())},'whole_literal_contract':contract},indent=2)+'\n')
print(json.dumps({'source_files':len(source_files),'source_directories':len(source_dirs),'qualified_core_files':len(core),'protected_paths':len(rows),'opaque_only':True}))
