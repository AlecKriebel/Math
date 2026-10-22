"""Strict audit-packet integrity and finite-arithmetic replay, standard library only."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

FILES = {'ACCEPTANCE.json','AUDIT.md','INDEPENDENT_LEMMAS.md','AUTHOR_BINDING.json',
         'AUTHOR_REPLAY.json','DATA_AUDIT.json','SOURCE_AUDIT.json','INDEPENDENT_CHECKS.py',
         'INDEPENDENT_RESULTS.json','PACKAGE_TEST_RESULTS.json','VERIFY_AUDIT.py',
         'TEST_AUDIT_PACKAGE.py','README.md'}


def require(ok,message):
    if not ok:
        raise ValueError(message)


def unique_object(pairs):
    out = {}
    for key,value in pairs:
        require(key not in out,'duplicate JSON key')
        out[key]=value
    return out


def read_json(data):
    return json.loads(data,object_pairs_hook=unique_object)


def regular_bytes(path):
    fd=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)|getattr(os,'O_NONBLOCK',0))
    with os.fdopen(fd,'rb') as f:
        require(stat.S_ISREG(os.fstat(f.fileno()).st_mode),'not a regular file')
        return f.read()


def verify(root):
    root=Path(root)
    require(not root.is_symlink() and root.is_dir(),'invalid packet root')
    entries=list(os.scandir(root))
    require(all(stat.S_ISREG(e.stat(follow_symlinks=False).st_mode) for e in entries),'nonregular member')
    require({e.name for e in entries}==FILES|{'MANIFEST.json'},'strict inventory mismatch')
    manifest_bytes=regular_bytes(root/'MANIFEST.json')
    manifest=read_json(manifest_bytes)
    require(set(manifest)=={'format','files'} and manifest['format']=='free-p-toral-independent-audit-v1','manifest format')
    require(isinstance(manifest['files'],list),'manifest files type')
    inventory={}
    for row in manifest['files']:
        require(isinstance(row,dict) and set(row)=={'name','bytes','sha256'},'manifest row')
        name=row['name']
        require(isinstance(name,str) and name in FILES and name not in inventory,'unsafe or duplicate member')
        require(type(row['bytes']) is int and row['bytes']>=0,'invalid byte count')
        require(isinstance(row['sha256'],str) and len(row['sha256'])==64 and all(c in '0123456789abcdef' for c in row['sha256']),'invalid digest')
        inventory[name]=row
    require(set(inventory)==FILES,'manifest inventory mismatch')
    payload={}
    for name,row in inventory.items():
        data=regular_bytes(root/name)
        require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'payload mismatch: '+name)
        payload[name]=data
    binding=read_json(payload['AUTHOR_BINDING.json'])
    require(binding['archive_sha256']=='66040253e0072ac532237b7cf70c513b69ae6cabdf4e99e554e96c5f703de7fa','author archive binding')
    require(binding['manifest_sha256']=='4d2d1a9b1aa2693d50697b94e2cb47a6bb1d938ad9ac66f6e1eace4042085e81','author manifest binding')
    dataset=read_json(payload['DATA_AUDIT.json'])
    require(dataset['review_sha256']=='ca5ea39f6f40b6344a17adf507993b7a3aa628f194669943f2b6acb99876e306','review binding')
    ns={'__name__':'verified_independent_checks','__builtins__':__builtins__}
    exec(compile(payload['INDEPENDENT_CHECKS.py'],'<verified independent checks>','exec'),ns)
    results=ns['run_checks']()
    require(results==read_json(payload['INDEPENDENT_RESULTS.json']),'independent results mismatch')
    return {'status':'PASS','verified_payload_files':len(payload),
            'manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(),
            'independent_results':results,
            'scope':'Integrity and finite diagnostics only. Mathematical acceptance is the separate reviewed exposition, not a program theorem.'}


if __name__=='__main__':
    try:
        print(json.dumps(verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent),sort_keys=True,indent=2))
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr)
        sys.exit(1)
