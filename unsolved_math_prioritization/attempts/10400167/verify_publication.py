#!/usr/bin/env python3
"""Portable read-only release integrity and exact-control replay."""
from pathlib import Path
import hashlib,json,runpy
ROOT=Path(__file__).resolve().parent
PUB=ROOT/'public'
EXPECTED='1bf1bf1b7bf7b1232a75bac9e742940a9fcbb52bbe27847a947a3c56226d4075'
def check(ok,message):
    if not ok:raise RuntimeError(message)
def digest():
    fs=sorted(p for p in PUB.iterdir() if p.is_file())
    return len(fs),hashlib.sha256(b''.join(p.name.encode()+b'\0'+hashlib.sha256(p.read_bytes()).digest() for p in fs)).hexdigest()
def main():
    manifest=json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_text())
    expected=set(manifest['files'])|{'PUBLICATION_MANIFEST.json'}
    found={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    check(found==expected,'Release file allowlist mismatch')
    for n,row in manifest['files'].items():
        b=(ROOT/n).read_bytes();check(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'Release hash mismatch: '+n)
    check(digest()==(15,EXPECTED),'Corrected packet digest mismatch')
    for n,row in json.loads((PUB/'MANIFEST.json').read_text())['files'].items():
        b=(PUB/n).read_bytes();check(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'Packet manifest mismatch: '+n)
    turns=[json.loads(l) for l in (PUB/'turns.jsonl').read_text().splitlines()]
    check([t['turn'] for t in turns]==list(range(1,6)),'Five-turn ledger mismatch')
    for t in turns:check(t['artifact_sha256']==hashlib.sha256((PUB/t['artifact']).read_bytes()).hexdigest(),'Turn artifact hash mismatch')
    s=json.loads((PUB/'STATUS.json').read_text());check(s['turns_used']==5 and s['status']=='exhausted' and s['full_resolution'] is False,'Disposition mismatch')
    narrow=json.loads((ROOT/'audit/NARROW_REVIEW.json').read_text());check(narrow['status']=='PASS' and narrow['corrected_packet_sha256']==EXPECTED,'Narrow review mismatch')
    check('link in S^3 with at most two components, under one common simple-label bijection' in (PUB/'TURN_5.md').read_text(),'Missing source-scope correction')
    author=runpy.run_path(str(PUB/'verify.py'),run_name='publication_author_replay')
    a={k:author[f]() for k,f in [('torus','torus_controls'),('s3','s3_control'),('abelian','abelian_controls'),('cyclic','cyclic_cocycle_controls')]}
    check(a==json.loads((PUB/'verification.json').read_text())['checks'],'Author replay mismatch')
    independent=runpy.run_path(str(ROOT/'audit/independent_controls.py'),run_name='publication_independent_replay')
    controls={k:independent[f]() for k,f in [('bar_chains','cyclic_bar_chains'),('nonreal_torus','exact_nonreal_torus'),('groupoid','groupoid_normalization'),('coboundary_lens','coboundary_lens_control')]}
    for n in ['original_audit_verification.json','independent_verification.json']:
        check(controls==json.loads((ROOT/'audit'/n).read_text())['independent_controls'],'Independent replay mismatch: '+n)
    check(digest()==(15,EXPECTED),'Packet modified by replay')
    print(json.dumps({'status':'PASS','corrected_packet_sha256':EXPECTED,'packet_files':15,'publication_files':len(expected),'author_and_independent_controls_reproduced':True,'original_problem':'unsolved','turns_used':5,'full_resolution_claim':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
