#!/usr/bin/env python3
"""Verify exact v1-to-v2 changes from separately supplied immutable archives."""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import subprocess
import tempfile
import zipfile

PINS={
 'original':(17955,'f603686a4d0a3d22cb26b6f1dbb972a8dd37a746a0738ef43165e3d9ff6d66ed'),
 'revised':(20735,'9194e9059bd3255336a66e707d490c685b2055752a987aca65f099d89aab7c82'),
 'prior_audit':(38655,'d35d483f06de1771829468e7b2e64b56567254784de0205f98e341f277d54eb7')
}
EDITS=[
 ('cover A by sets U_i of positive diameter d_i<1/(2j), with Σ_i d_i^κ arbitrarily small.',
  'cover A by sets U_i of diameters 0≤d_i<1/(2j), with Σ_i d_i^κ arbitrarily small.'),
 ('For each U_i meeting A∩E_j choose x_i in that intersection.',
  'For each positive-diameter U_i meeting A∩E_j choose x_i in that intersection.'),
 ('Singleton members can be replaced by arbitrarily small positive-diameter balls; the growth estimate rules out atoms on E_j.',
  'Any zero-diameter cover member meeting A∩E_j is a singleton {x} with x∈E_j, and ν({x})≤j r^κ for every 0<r<1/j, so ν({x})=0. There are at most countably many such members. Discard their zero-mass contribution and apply the preceding estimate to the positive-diameter members.')
]
def require(test,message):
    if not test:raise AssertionError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def meta(name,b):return {'path':name,'bytes':len(b),'sha256':sha(b)}

def inspect(a,b,audit):
    original_names={'APPROACHES.md','LITERATURE.md','MANIFEST.json','PROOF.md','README.md','source_metadata.json','verification_results.json','verify.py','verify_manifest.py'}
    added={'CORRECTION_DELTA.md','REVISION_PROVENANCE.json'}
    require(set(a)==original_names and set(b)==original_names|added,'Unexpected archive member set')
    expected=a['PROOF.md'].decode()
    corrections=audit['CORRECTIONS.md'].decode()
    for old,new in EDITS:
        require(expected.count(old)==1,'Correction target is not unique')
        require(old in corrections and new in corrections,'Correction differs from original audit requirement')
        expected=expected.replace(old,new,1)
    require(expected.encode()==b['PROOF.md'],'Proof contains an unapproved delta')
    require(sha(b['PROOF.md'])=='f0baa658ae1380777ba63c8d651dfd4c71bb2b39e4c6e9f4f1be3f8d5ef2dc50','Corrected proof hash mismatch')
    unchanged=sorted(original_names-{'PROOF.md','MANIFEST.json'})
    for name in unchanged:require(a[name]==b[name],'Original file changed: '+name)
    for name,data in a.items():require(audit['author_freeze/'+name]==data,'Original audit freeze changed: '+name)
    manifest=json.loads(b['MANIFEST.json'])
    require(manifest['schema']==1 and manifest['hash_algorithm']=='sha256','Manifest schema changed')
    require(manifest['purpose']=='Frozen sanitized v2 authored payload; excludes this manifest to avoid self-reference. Archive hash is recorded separately.','Unexpected manifest purpose')
    require(manifest['files']==[meta(name,b[name]) for name in sorted(b) if name!='MANIFEST.json'],'Manifest does not describe exact v2 bytes')
    diff=''.join(difflib.unified_diff(a['PROOF.md'].decode().splitlines(True),b['PROOF.md'].decode().splitlines(True),fromfile='v1/PROOF.md',tofile='v2/PROOF.md'))
    delta=b['CORRECTION_DELTA.md'].decode()
    require(delta=='# Exact v1-to-v2 proof delta\n\nOnly the three required edits from the independent audit correction were applied. No optional prose changes, theorem changes, new proof attempts, or code changes were made.\n\n```diff\n'+diff+'```\n','Reported proof diff differs from actual complete proof diff')
    prov=json.loads(b['REVISION_PROVENANCE.json'])
    require(prov['problem_id']==5300056 and prov['revision']=='v2','Revision identity mismatch')
    require(prov['original_archive']['bytes']==PINS['original'][0] and prov['original_archive']['sha256']==PINS['original'][1],'Original archive binding mismatch')
    require(prov['correction_source']['sha256']==sha(audit['CORRECTIONS.md']),'Original correction binding mismatch')
    require(prov['correction_source']['required_edits']==3 and prov['correction_source']['optional_edits_applied'] is False,'Incorrect edit-scope metadata')
    for version,key in [('old',a),('new',b)]:
        require(prov['proof_delta'][version+'_bytes']==len(key['PROOF.md']) and prov['proof_delta'][version+'_sha256']==sha(key['PROOF.md']),'Proof binding mismatch')
    require(prov['proof_delta']['unified_diff_file_sha256']==sha(b['CORRECTION_DELTA.md']),'Proof patch binding mismatch')
    require(prov['unchanged_original_files']==[meta(name,b[name]) for name in unchanged],'Unchanged-member metadata mismatch')
    require(prov['manifest']['original_sha256']==sha(a['MANIFEST.json']),'Original manifest binding mismatch')
    require(prov['code_and_results_unchanged'] is True and prov['remote_writes_performed'] is False,'Unexpected revision claims')
    full=''
    for name in sorted(set(a)|set(b)):
        x=a.get(name,b'').decode();y=b.get(name,b'').decode()
        if x!=y:full+=''.join(difflib.unified_diff(x.splitlines(True),y.splitlines(True),fromfile='v1/'+name if x else '/dev/null',tofile='v2/'+name))
    require(full.encode()==Path(__file__).with_name('FULL_DELTA.patch').read_bytes(),'Full payload patch mismatch')
    return unchanged

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in PINS:parser.add_argument('--'+name.replace('_','-'),type=Path,required=True)
    args=parser.parse_args(); archives={}
    for name,(size,digest) in PINS.items():
        path=getattr(args,name);raw=path.read_bytes()
        require(len(raw)==size and sha(raw)==digest,'Input archive pin mismatch: '+name)
        with zipfile.ZipFile(path) as z:
            require(len(z.namelist())==len(set(z.namelist())),'Duplicate ZIP member')
            archives[name]={n:z.read(n) for n in z.namelist()}
    unchanged=inspect(archives['original'],archives['revised'],archives['prior_audit'])
    replay={}
    with tempfile.TemporaryDirectory(prefix='jacobian_delta_') as td:
        target=Path(td)/'relocated';target.mkdir()
        for name,data in archives['revised'].items():(target/name).write_bytes(data)
        for file in ['verify_manifest.py','verify.py']:
            p=subprocess.run(['python3','-B',str(target/file)],cwd=td,text=True,capture_output=True)
            require(p.returncode==0,'Relocated verifier failed: '+p.stderr)
            replay[file]=json.loads(p.stdout)
    require(replay['verify.py']['total_assertions']==21193,'Unexpected replay count')
    result={'status':'PASS','verdict':'V2_BOUNDED_DELTA_ACCEPTED','problem_id':5300056,
            'exact_required_replacements':3,'changed_original_members':['MANIFEST.json','PROOF.md'],
            'added_members':['CORRECTION_DELTA.md','REVISION_PROVENANCE.json'],
            'unchanged_original_members':unchanged,'original_archive_preserved':True,
            'prior_audit_archive_preserved':True,'corrected_proof_sha256':sha(archives['revised']['PROOF.md']),
            'full_delta_sha256':sha(Path(__file__).with_name('FULL_DELTA.patch').read_bytes()),
            'relocated_manifest':'PASS','relocated_author_checks':21193,
            'general_target':'UNSOLVED in this investigation','documented_routes':5,
            'scope':'Exact correction delta and revision metadata only; the original independent mathematical audit remains the substantive review.'}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
