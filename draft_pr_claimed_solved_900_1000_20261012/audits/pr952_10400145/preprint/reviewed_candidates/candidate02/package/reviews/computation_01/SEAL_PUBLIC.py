#!/usr/bin/env python3
"""Explicit source-free review seal. Does not recursively select any directory."""
from pathlib import Path
import datetime,hashlib,json,stat
W=Path(__file__).resolve().parent
PUBLIC_FILES=[
 'authenticate.py','START.json','INITIAL_ATTACK.md','INITIAL_INTAKE.json',
 'RESEARCH_LOG.md','CODE_INTAKE.json','independent_math.py',
 'MATH_RESULTS_INITIAL.json','MATH_RESULTS.json','runtime_review.py',
 'RUNTIME_RESULTS.json','ORIGINAL_PAYLOAD_PINS.json','portable_profile.py',
 'math_adversary.py','MATH_ADVERSARY_RESULTS.json','REPLAY_SUMMARY.json',
 'COMPUTATION_REVIEW.md','PORTABLE_PROFILE.md','FINDINGS.json',
 'END.json','FINAL_SCOPE.json','SEAL_PUBLIC.py',
]
def need(c,m):
    if not c:raise RuntimeError(m)
def main():
    need(len(PUBLIC_FILES)==len(set(PUBLIC_FILES)),'duplicate public file')
    entries=[]
    for n in PUBLIC_FILES:
        need('/' not in n and n not in ['.','..','MANIFEST.json'],'not a flat explicit public file')
        p=W/n;s=p.lstat();need(stat.S_ISREG(s.st_mode),'nonregular public file')
        b=p.read_bytes();entries.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':f'{stat.S_IMODE(s.st_mode):04o}'})
    m={'schema':'pr952-computation-route-public-manifest-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'immutable_submitted_head':'989a532ae1d50894190d010a0a02ba8c3d71ee05','scope':'Source-free independent computational route review and separately authored portable prototype; not full-paper acceptance or a Linux/bwrap/EROFS pass.','selection':'Explicit flat files; never recursively select private or tmp.','excluded_directories':['private','tmp'],'files':entries,'file_count':len(entries),'total_payload_bytes':sum(e['bytes'] for e in entries),'manifest_self_hash':'External delivery record; manifest does not hash itself.'}
    dest=W/'MANIFEST.json';dest.write_text(json.dumps(m,indent=2)+'\n')
    # Re-read every explicitly listed payload after writing; no mutation allowed.
    for e in json.loads(dest.read_bytes())['files']:
        b=(W/e['path']).read_bytes();need(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'postseal mismatch')
    print(json.dumps({'manifest_bytes':dest.stat().st_size,'manifest_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'public_files':len(entries),'payload_bytes':m['total_payload_bytes']}))
if __name__=='__main__':main()
