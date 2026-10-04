#!/usr/bin/env python3
"""Read-only exact verifier for this owned public probability-audit manifest."""
from pathlib import Path
import json,hashlib

def main():
    p=Path(__file__).resolve().parent
    m=json.loads((p/'PUBLIC_EVIDENCE_MANIFEST.json').read_text())
    seen=set()
    for e in m['files']:
        name=e['path']
        assert name not in seen;seen.add(name)
        assert Path(name).parts[0] not in ('tmp','sources','downloads')
        f=p/name;assert f.is_file() and not f.is_symlink()
        b=f.read_bytes();assert len(b)==e['bytes']
        assert hashlib.sha256(b).hexdigest()==e['sha256']
    expected={f.name for f in p.iterdir() if f.is_file()}-{'PUBLIC_EVIDENCE_MANIFEST.json','verify_public_evidence.stdout','verify_public_evidence.stderr'}
    assert seen==expected,(sorted(seen-expected),sorted(expected-seen))
    for sealname in ('independent_seal_manifest.json','candidate_verdict_seal.json'):
        s=json.loads((p/sealname).read_text())
        for e in s['files']:
            f=p.parent/e['path'];b=f.read_bytes()
            assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
    assert json.loads((p/'independent_controls.stdout').read_text())['all_passed']
    assert json.loads((p/'cross_boundary_controls.stdout').read_text())['all_passed']
    for run in json.loads((p/'candidate_replay.json').read_text())['runs']:
        assert run['exit_code']==0 and run['exact_receipt_match']
        for kind in ('stdout','stderr'):
            b=(p/f"candidate_turn{run['turn']}.{kind}").read_bytes()
            assert hashlib.sha256(b).hexdigest()==run[f'{kind}_sha256']
    print(json.dumps({'all_public_hashes_verified':True,'public_manifest_entries':len(seen),'both_independence_seals_verified':True,'raw_sources_in_public_manifest':False},sort_keys=True))

if __name__=='__main__':main()
