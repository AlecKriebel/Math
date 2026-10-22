"""Verify a fixed flat review packet and replay verified finite diagnostics."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

FILES = {'README.md','REVIEW.md','INPUT_BINDINGS.json','SOURCE_REVIEW.json',
         'ACCEPTANCE.json','DIAGNOSTICS.py','DIAGNOSTIC_RESULTS.json','VERIFY.py',
         'TEST_PACKAGE.py','VERIFICATION_RESULTS.json'}
PINS = {'FREE_P_TORAL_30001522_AUTHOR_SAFE_FREEZE.zip':(17871,'66040253e0072ac532237b7cf70c513b69ae6cabdf4e99e554e96c5f703de7fa'),
        'FREE_P_TORAL_30001522_INDEPENDENT_AUDIT_SAFE.zip':(22630,'9ec76657649910ba8eaa7546fb490445b826d3a354a52cb8965a2a17802a72ec')}


def require(ok,message):
    if not ok:
        raise ValueError(message)


def unique_object(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,'duplicate JSON key')
        result[k]=v
    return result


def parse(data):
    return json.loads(data,object_pairs_hook=unique_object)


def regular_bytes(path):
    fd=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)|getattr(os,'O_NONBLOCK',0))
    with os.fdopen(fd,'rb') as f:
        require(stat.S_ISREG(os.fstat(f.fileno()).st_mode),'nonregular file')
        return f.read()


def verify(root):
    root=Path(root)
    require(not root.is_symlink() and root.is_dir(),'invalid root')
    entries=list(os.scandir(root))
    require(all(stat.S_ISREG(e.stat(follow_symlinks=False).st_mode) for e in entries),'nonregular entry')
    require({e.name for e in entries}==FILES|{'MANIFEST.json'},'inventory mismatch')
    manifest_bytes=regular_bytes(root/'MANIFEST.json')
    manifest=parse(manifest_bytes)
    require(set(manifest)=={'format','files'} and manifest['format']=='free-p-toral-second-review-v1','manifest format')
    require(type(manifest['files']) is list,'files type')
    inventory={}
    for row in manifest['files']:
        require(type(row) is dict and set(row)=={'name','bytes','sha256'},'manifest row')
        name=row['name']
        require(type(name) is str and name in FILES and name not in inventory,'member name')
        require(type(row['bytes']) is int and row['bytes']>=0,'byte count')
        require(type(row['sha256']) is str and len(row['sha256'])==64 and all(c in '0123456789abcdef' for c in row['sha256']),'digest format')
        inventory[name]=row
    require(set(inventory)==FILES,'manifest inventory')
    data={}
    for name,row in inventory.items():
        b=regular_bytes(root/name)
        require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'content mismatch: '+name)
        data[name]=b
    bindings=parse(data['INPUT_BINDINGS.json'])
    require(bindings['problem_id']==30001522 and bindings['problem_number']=='OWR-4413-005','problem binding')
    archives=bindings['archives']
    require(type(archives) is list and len(archives)==2,'archive bindings')
    require({a['filename']:(a['bytes'],a['sha256']) for a in archives}==PINS,'input archive pins')
    require(bindings['freezes_modified'] is False,'freeze preservation')
    acceptance=parse(data['ACCEPTANCE.json'])
    require(acceptance['problem_id']==30001522 and acceptance['free_toral_rank']==0 and acceptance['free_2_rank']==0 and acceptance['free_p_rank_every_odd_prime']==1,'accepted ranks')
    require(acceptance['mathematical_corrections_required']==[] and acceptance['novelty_certified'] is False and acceptance['formal_proof_assistant_verified'] is False,'verdict scope')
    ns={'__name__':'verified_finite_diagnostics','__builtins__':__builtins__}
    exec(compile(data['DIAGNOSTICS.py'],'<verified DIAGNOSTICS.py>','exec'),ns)
    result=ns['run_checks']()
    require(result==parse(data['DIAGNOSTIC_RESULTS.json']),'diagnostic output')
    return {'status':'PASS','verified_payload_files':len(data),'manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(),
            'diagnostics':result,'scope':'Packet integrity and finite consistency only; mathematical acceptance is separate reviewed exposition.'}


if __name__=='__main__':
    try:
        print(json.dumps(verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent),sort_keys=True,indent=2))
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
