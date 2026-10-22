#!/usr/bin/env python3
"""Read-only verification of this closed review and its six permitted snapshots."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent

def require(ok,message):
    if not ok: raise ValueError(message)
def identity(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def entries(rows):
    found={}
    for row in rows:
        name=row['path'];p=PurePosixPath(name)
        require(not p.is_absolute() and '\\' not in name and all(x not in ('','.','..') for x in name.split('/')),'Unsafe path')
        require(name not in found and name!='MANIFEST.json','Duplicate/self path')
        found[name]={k:row[k] for k in ('bytes','sha256')}
    return found
m=json.loads((ROOT/'MANIFEST.json').read_bytes())
authored=entries(m['authored_files']);frozen=entries(m['permitted_frozen_inputs'])
require(len(frozen)==6 and all(n.startswith('frozen/') for n in frozen),'Frozen input inventory')
require(not set(authored)&set(frozen),'Overlapping input/authored inventory')
expected={**authored,**frozen};actual={};dirs=set()
for p in ROOT.rglob('*'):
    require(not p.is_symlink(),'Symlink')
    n=p.relative_to(ROOT).as_posix()
    if p.is_dir():dirs.add(n);continue
    require(stat.S_ISREG(p.stat().st_mode),'Nonregular file')
    actual[n]=p.read_bytes()
require(set(actual)==set(expected)|{'MANIFEST.json'},'Closed file inventory mismatch')
require(dirs=={p.as_posix() for n in actual for p in Path(n).parents if p.as_posix()!='.'},'Closed directory inventory mismatch')
for name,pin in expected.items():require(identity(actual[name])==pin,'Byte mismatch: '+name)
binding=json.loads(actual['INPUT_BINDING.json'])
require(frozen=={'frozen/'+r['path']:{k:r[k] for k in ('bytes','sha256')} for r in binding['frozen_publication_files']},'Root binding mismatch')
v=json.loads(actual['VERDICT.json']);require(v['issue_count']==0 and v['repairs_required'] is False and v['verdict']=='PASS','Verdict mismatch')
require(v['publication_inputs']==binding['frozen_publication_files'],'Verdict input pins mismatch')
print(json.dumps({'result':'PASS','authored_or_bound_review_files':len(authored),'permitted_frozen_inputs':len(frozen),'closed_regular_files':len(actual),'outer_optimized':not __debug__,'scope':'Closed review bytes and permitted input pins; not a formal mathematical or priority certificate.'},indent=2))
