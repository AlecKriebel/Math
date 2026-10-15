#!/usr/bin/env python3
"""Portable byte integrity and exact replay. No assertion-based guards."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ANCHORS = {
 'frozen_v2/FROZEN_MANIFEST.json': '199dc44fdb8de8f37024d170e6246281e1a7b6b5b7e1cdd94a21f4a1b195e478',
 'audit_a/AUDIT_MANIFEST.json': '218b4dd72de1aa92ed88be04c5010b4eccea7331985dcd853a5c2465e032bf9e',
 'audit_b/AUDIT_MANIFEST.json': 'ca49b07b2dfc4c83f9d7c6f03b7185e56a662ee820eba58a5c63f905973f94c5',
}
FROZEN = {
 'frozen_v2': ['CHECK_RESULTS.json','FROZEN_MANIFEST.json','PROOF.md','README.md','SOURCE_MANIFEST.json','checks.py'],
 'audit_a': ['AUDIT.md','AUDIT_MANIFEST.json','AUTHOR_CHECK_RESULTS.json','AUTHOR_CHECK_RESULTS_OPTIMIZED.json','INDEPENDENT_CHECK_RESULTS.json','INDEPENDENT_SOURCE_RETRIEVAL.json','independent_checks.py'],
 'audit_b': ['AUDIT_MANIFEST.json','AUDIT_REPORT.md','INDEPENDENT_RESULTS.json','SOURCE_METADATA.json','independent_checks.py'],
}
PAYLOAD = {f'{d}/{n}' for d,names in FROZEN.items() for n in names} | {
 'README.md','ACCEPTANCE.md','APPROACH_LEDGER.md','RESEARCH_LOG.md','requirements.txt',
 'run_audit_a.py','verify_publication.py','mutation_tests.py',
}
EXACT = PAYLOAD | {'PACKAGE_MANIFEST.json','PACKAGE_MANIFEST.sha256'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def integrity():
    found = set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'Symlink prohibited: '+str(p.relative_to(ROOT)))
        if p.is_file():
            found.add(p.relative_to(ROOT).as_posix())
        else:
            require(p.is_dir(), 'Special file prohibited')
    require(found == EXACT, 'Exact allowlist mismatch: '+repr(sorted(found ^ EXACT)))
    raw = (ROOT/'PACKAGE_MANIFEST.json').read_bytes()
    require((ROOT/'PACKAGE_MANIFEST.sha256').read_text() == digest(raw)+'  PACKAGE_MANIFEST.json\n', 'Package manifest checksum mismatch')
    manifest = json.loads(raw)
    require(set(manifest) == {'schema','problem_id','scope','files'}, 'Manifest schema mismatch')
    require(manifest['schema']==1 and manifest['problem_id']==30001345, 'Manifest target mismatch')
    files = manifest['files']
    require(isinstance(files,list) and len(files)==len(PAYLOAD), 'Manifest item count mismatch')
    require({x['file'] for x in files} == PAYLOAD, 'Manifest payload allowlist mismatch')
    for item in files:
        require(set(item)=={'file','bytes','sha256'}, 'Invalid manifest entry')
        b=(ROOT/item['file']).read_bytes()
        require(len(b)==item['bytes'] and digest(b)==item['sha256'], 'Payload identity mismatch: '+item['file'])
    for name,sha in ANCHORS.items():
        p=ROOT/name
        require(digest(p.read_bytes())==sha, 'Frozen manifest anchor mismatch: '+name)
        child=json.loads(p.read_bytes())
        items=child['files']
        require({x['file'] for x in items} == set(FROZEN[p.parent.name])-{p.name}, 'Frozen manifest allowlist mismatch')
        for item in items:
            b=(p.parent/item['file']).read_bytes()
            require(len(b)==item['bytes'] and digest(b)==item['sha256'], 'Frozen identity mismatch: '+name+'/'+item['file'])
    return {'status':'PASS','payload_files':len(PAYLOAD),'frozen_files':18,'package_manifest_sha256':digest(raw)}

def replay():
    try:
        import sympy
        import mpmath
    except ImportError as exc:
        raise RuntimeError('Install requirements.txt before full replay') from exc
    require(sympy.__version__=='1.14.0' and mpmath.__version__=='1.3.0','Pinned dependency versions required')
    env=os.environ.copy()
    env.pop('PYTHONOPTIMIZE',None)
    env.pop('PYTHONPATH',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    cases=[
     ('author_normal',[],['frozen_v2/checks.py'],'frozen_v2/CHECK_RESULTS.json'),
     ('author_optimized',['-O'],['frozen_v2/checks.py'],'frozen_v2/CHECK_RESULTS.json'),
     ('audit_a_guarded_normal',[],['run_audit_a.py'],'audit_a/INDEPENDENT_CHECK_RESULTS.json'),
     ('audit_b_normal',[],['audit_b/independent_checks.py','frozen_v2'],'audit_b/INDEPENDENT_RESULTS.json'),
     ('audit_b_optimized',['-O'],['audit_b/independent_checks.py','frozen_v2'],'audit_b/INDEPENDENT_RESULTS.json'),
    ]
    results={}
    for label,flags,arguments,expected in cases:
        args=[sys.executable,'-I','-B',*flags,*[str(ROOT/a) for a in arguments]]
        result=subprocess.run(args,cwd=ROOT.parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
        require(result.returncode==0, label+' failed: '+result.stderr.decode(errors='replace'))
        require(result.stdout==(ROOT/expected).read_bytes(),label+' saved output mismatch')
        results[label]={'status':'PASS','output_sha256':digest(result.stdout)}
    # Never propagate the parent's optimization flags to audit A.
    for flags in (['-O'],['-OO']):
        rejected=subprocess.run([sys.executable,'-I','-B',*flags,str(ROOT/'run_audit_a.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
        require(rejected.returncode!=0 and b'REFUSED: audit A requires normal Python' in rejected.stderr, 'Audit A optimized guard failed')
    results['audit_a_optimized_invocation']='REJECTED_AS_REQUIRED'
    return results

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--integrity-only',action='store_true')
    args=parser.parse_args()
    result=integrity()
    if not args.integrity_only:
        result['replays']=replay()
        integrity()
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
