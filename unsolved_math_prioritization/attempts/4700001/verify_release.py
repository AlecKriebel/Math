#!/usr/bin/env python3
"""Strict portable integrity verifier for the exact published 4700001 packet."""
import hashlib,json,re,sys
from pathlib import Path,PurePosixPath

EXPECTED=set('''FREEZE_MANIFEST.json
RELEASE_NOTE.md
verify_release.py
PUBLICATION_MANIFEST.json
frozen/ATTEMPT_LOG.md
frozen/PROOF.md
frozen/README.md
frozen/SOURCE_GATE.md
frozen/check_numeric.py
frozen/check_symbolic.py
frozen/numerical-results.json
frozen/verification-metadata.json
audit/AUDIT.md
audit/CORRECTIONS.md
audit/README.md
audit/independent_checks.py
audit/run_audit.py
audit/input-verification.json
audit/symbolic-replay.txt
audit/numerical-replay.json
audit/independent-results.json
audit/replay-summary.json
audit/source-checks.json
audit/AUDIT_MANIFEST.json
audit/AUDIT_MANIFEST.sha256'''.splitlines())

def require(condition,message):
    if not condition: raise ValueError(message)

def no_duplicate_keys(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'duplicate JSON key')
        result[key]=value
    return result

def verify(root):
    root=Path(root).resolve()
    items=list(root.rglob('*'))
    require(not any(p.is_symlink() for p in items),'symlink forbidden')
    require({p.relative_to(root).as_posix() for p in items if p.is_dir()}=={'audit','frozen'},'unexpected directory')
    actual={p.relative_to(root).as_posix() for p in items if p.is_file()}
    require(actual==EXPECTED,'unexpected or missing file: '+repr(sorted(actual^EXPECTED)))
    manifest=json.loads((root/'PUBLICATION_MANIFEST.json').read_text(),object_pairs_hook=no_duplicate_keys)
    require(set(manifest)=={'version','target_id','status','files'},'unexpected manifest schema')
    require(type(manifest['version']) is int and manifest['version']==1 and type(manifest['target_id']) is int and manifest['target_id']==4700001 and manifest['status']=='unsolved','manifest identity mismatch')
    require(isinstance(manifest['files'],list),'entries must be a list')
    paths=[]
    for e in manifest['files']:
        require(isinstance(e,dict) and set(e)=={'path','bytes','sha256'},'unexpected entry schema')
        path=e['path']; require(isinstance(path,str),'path must be text')
        pp=PurePosixPath(path)
        require(not pp.is_absolute() and str(pp)==path and '\\' not in path and all(p not in ('','.','..') for p in path.split('/')),'unsafe path')
        require(path in EXPECTED and path!='PUBLICATION_MANIFEST.json','entry outside allowlist')
        require(type(e['bytes']) is int and e['bytes']>=0,'invalid byte count')
        require(isinstance(e['sha256'],str) and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None,'invalid hash')
        paths.append(path)
        b=(root/path).read_bytes()
        require(len(b)==e['bytes'],'byte mismatch: '+path)
        require(hashlib.sha256(b).hexdigest()==e['sha256'],'hash mismatch: '+path)
    require(len(paths)==len(set(paths)),'duplicate path')
    require(set(paths)==EXPECTED-{'PUBLICATION_MANIFEST.json'},'manifest allowlist mismatch')
    require(hashlib.sha256((root/'FREEZE_MANIFEST.json').read_bytes()).hexdigest()=='c1af53c8f215aff4236e2490d01a81d2502c82e36e6f9c36c5779b00df6972f4','original freeze manifest mismatch')
    require(hashlib.sha256((root/'audit/AUDIT_MANIFEST.json').read_bytes()).hexdigest()=='6e7b2ea7b9becb60c742dfee04218772c62cd79cff57cd1153a09450366b38b0','audit manifest mismatch')
    require((root/'audit/AUDIT_MANIFEST.sha256').read_text().strip()=='6e7b2ea7b9becb60c742dfee04218772c62cd79cff57cd1153a09450366b38b0  AUDIT_MANIFEST.json','audit manifest sidecar mismatch')
    return {'status':'PASS','file_count':len(EXPECTED),'hashed_file_count':len(paths),'target_status':'unsolved'}

if __name__=='__main__':
    try:
        print(json.dumps(verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent),sort_keys=True))
    except Exception as error:
        print('FAIL: '+str(error),file=sys.stderr)
        raise SystemExit(1)
