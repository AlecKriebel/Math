#!/usr/bin/env python3
"""Verify strict envelope integrity, unchanged author identity, and exact replays."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
AUTHOR_FILES={'README.md','proof.md','certificate.py','claim.json','RESULTS.json','PUBLIC_METADATA.json','exploratory.py','EXPLORATORY_RESULTS.json','verify.py','MANIFEST.json'}
AUDIT_FILES={'AUDIT.md','DERIVATIVE_REMAINDER.md','INDEPENDENT_RESULTS.json','MUTATION_RESULTS.json','NUMERICAL_REPLAY.json','PUBLIC_SOURCE_REVIEW.json','independent_check.py','replay_mutations.py'}
ROOT_FILES={'README.md','MANIFEST.json','verify_audit.py'}
AUTHOR_MANIFEST_SHA='070eec675456682300a3bb1cf23fbed0069068bc05b32bce492226cdbeec0f27'

def require(ok,message):
    if not ok:raise ValueError(message)

def inspect(directory,files,dirs=frozenset()):
    entries=list(os.scandir(directory))
    require({e.name for e in entries}==files|dirs,'unexpected or missing inventory node: '+directory.name)
    for e in entries:
        mode=e.stat(follow_symlinks=False).st_mode
        if e.name in dirs:require(stat.S_ISDIR(mode),'nonregular directory')
        else:require(stat.S_ISREG(mode),'nonregular file')

def run_script(path):
    flags=['-I','-B']+(['-O'] if sys.flags.optimize else [])
    p=subprocess.run([sys.executable,*flags,str(path)],capture_output=True,text=True,check=True,timeout=90)
    return json.loads(p.stdout)

def main():
    inspect(ROOT,ROOT_FILES,{'author','audit'})
    inspect(ROOT/'author',AUTHOR_FILES)
    inspect(ROOT/'audit',AUDIT_FILES)
    expected=(ROOT_FILES-{'MANIFEST.json'})|{'author/'+p for p in AUTHOR_FILES}|{'audit/'+p for p in AUDIT_FILES}
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    require(manifest['schema']=='yamabe-audit-flat-sha256-v1','manifest schema')
    require(set(manifest['files'])==expected,'manifest inventory')
    for name,meta in manifest['files'].items():
        raw=(ROOT/name).read_bytes()
        require(len(raw)==meta['bytes'] and hashlib.sha256(raw).hexdigest()==meta['sha256'],'content mismatch: '+name)
    require(hashlib.sha256((ROOT/'author/MANIFEST.json').read_bytes()).hexdigest()==AUTHOR_MANIFEST_SHA,'accepted author manifest changed')
    author=run_script(ROOT/'author/verify.py')
    require(author['status']=='PASS' and author['mathematical_status']=='partial_unresolved','author replay failed')
    exact=run_script(ROOT/'audit/independent_check.py')
    require(exact==json.loads((ROOT/'audit/INDEPENDENT_RESULTS.json').read_text()),'independent replay changed')
    mutations=json.loads((ROOT/'audit/MUTATION_RESULTS.json').read_text())
    require(mutations['status']=='PASS' and mutations['author_test_count']==48,'mutation receipt invalid')
    require(mutations['accepted_author_manifest_sha256']==AUTHOR_MANIFEST_SHA,'mutation source identity mismatch')
    require(all(t['passed'] for t in mutations['author_tests']+mutations['independent_tests']),'failed mutation receipt')
    numerical=json.loads((ROOT/'audit/NUMERICAL_REPLAY.json').read_text())
    raw=(ROOT/'author/EXPLORATORY_RESULTS.json').read_bytes()
    require(numerical['bytes']==len(raw) and numerical['sha256']==hashlib.sha256(raw).hexdigest(),'numerical identity mismatch')
    require(numerical['certified_signs'] is False and numerical['coarse_positive_count']==6 and numerical['refined_positive_count']==0,'numerical scope changed')
    print(json.dumps({'status':'PASS','mathematical_status':'partial_unresolved','file_count':len(expected)+1,'optimized':bool(sys.flags.optimize),'accepted_author_manifest_sha256':AUTHOR_MANIFEST_SHA,'independent_intervals':750,'independent_exp_enclosures':13500},sort_keys=True))

if __name__=='__main__':main()
