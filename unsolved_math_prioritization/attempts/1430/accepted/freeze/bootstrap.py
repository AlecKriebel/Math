#!/usr/bin/env python3
"""Authenticate this file using an external digest before running it."""
from pathlib import Path
import hashlib
import json
import math
import os
import re
import stat
import subprocess
import sys

MANIFEST_SHA256 = '14f71c06b96e52cf76c99fa546e7698266f0e3d7ba05de940a02a053733fee15'

class Rejected(Exception):
    pass

def require(ok, message):
    if not ok:
        raise Rejected(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def unique(items):
    out = {}
    for key,value in items:
        require(key not in out,'duplicate JSON key')
        out[key] = value
    return out

def bad(value):
    raise Rejected('nonfinite JSON constant')

def finite(value):
    result = float(value)
    require(math.isfinite(result),'nonfinite JSON number')
    return result

def parse(raw):
    require(len(raw)<=2000000,'JSON size limit')
    return json.loads(raw,object_pairs_hook=unique,parse_constant=bad,parse_float=finite)

def regular(path):
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode),'symlink or nonregular file')
    require(stat.S_IMODE(st.st_mode) in (0o444,0o644),'unexpected file mode')
    return st

def main():
    require(len(sys.argv)==2,'usage: bootstrap.py /path/to/packet')
    source = Path(__file__).absolute()
    regular(source)
    manifest_path = source.parent/'AUTHOR_MANIFEST.json'
    ms = regular(manifest_path)
    require(ms.st_size<=2000000,'manifest size limit')
    raw = manifest_path.read_bytes()
    require(sha(raw)==MANIFEST_SHA256,'manifest trust-anchor mismatch')
    manifest = parse(raw)
    require(type(manifest) is dict and set(manifest)=={'schema','problem_id','status','approaches_used','files'},'manifest schema')
    require(manifest['schema']=='word-representation-author-manifest-v1','manifest version')
    require(type(manifest['problem_id']) is int and manifest['problem_id']==1430,'problem identity')
    require(manifest['status']=='unsolved' and type(manifest['approaches_used']) is int and manifest['approaches_used']==5,'disposition')
    root = Path(sys.argv[1]).absolute()
    require(not root.is_symlink() and root.is_dir(),'payload root')
    for parent in [root,*root.parents]:
        require(not parent.is_symlink(),'symlink in payload root ancestry')
    require(stat.S_IMODE(root.stat().st_mode) in (0o555,0o755),'payload root mode')
    entries = manifest['files']
    require(type(entries) is list and 1<=len(entries)<=50,'manifest inventory')
    names = set()
    for entry in entries:
        require(type(entry) is dict and set(entry)=={'path','bytes','sha256'},'entry schema')
        name = entry['path']
        require(type(name) is str and re.fullmatch(r'[A-Za-z0-9_.-]+',name) is not None and name not in ('.','..'),'unsafe manifest path')
        require(name not in names,'duplicate manifest path')
        names.add(name)
        require(type(entry['bytes']) is int and 0<=entry['bytes']<=2000000,'bad byte count')
        require(type(entry['sha256']) is str and re.fullmatch(r'[0-9a-f]{64}',entry['sha256']) is not None,'bad digest')
        path = root/name
        st = regular(path)
        require(st.st_size==entry['bytes'],'payload size mismatch')
        payload = path.read_bytes()
        require(len(payload)==entry['bytes'] and sha(payload)==entry['sha256'],'payload hash mismatch: '+name)
        if name.endswith('.json'):
            parse(payload)
    require({p.name for p in root.iterdir()}==names,'extra or missing payload inventory')
    require({'verify.py','DIAGNOSTICS.json'}<=names,'missing verifier data')
    flags = [] if sys.flags.optimize==0 else (['-O'] if sys.flags.optimize==1 else ['-OO'])
    result = subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/'verify.py')],cwd=root,
                            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
    require(result.returncode==0,'pinned verifier failed: '+result.stderr.decode('utf-8','replace'))
    require(result.stdout==(root/'DIAGNOSTICS.json').read_bytes(),'diagnostic output mismatch')
    return {'schema':'word-representation-bootstrap-v1','status':'PASS','files':len(entries),
            'manifest_sha256':MANIFEST_SHA256,'diagnostics_sha256':sha(result.stdout)}

if __name__=='__main__':
    try:
        print(json.dumps(main(),sort_keys=True,separators=(',',':')))
    except (Rejected,OSError,ValueError,TypeError,KeyError,IndexError,subprocess.SubprocessError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        sys.exit(1)
