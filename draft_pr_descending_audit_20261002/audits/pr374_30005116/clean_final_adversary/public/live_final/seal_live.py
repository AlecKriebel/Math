#!/usr/bin/env python3
"""Add a final explicit allowlist without changing either earlier seal."""
import datetime,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).parents[2]
HERE=pathlib.Path(__file__).parent
SEALS={'public/PUBLIC_MANIFEST.json':'6cd9683ff75d92e821b8d704bf72e908c1bcd4b087fe367fdb2045997cb11ee8',
       'public/live_acceptance/PREPARED_PUBLIC_MANIFEST.json':'d79770b4ee472c106927ce228bfed13f133ec010131b0d57bb14ea1ec1f56875'}
def bind(p):
    b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    for name,digest in SEALS.items():
        assert bind(ROOT/name)['sha256']==digest
        m=json.loads((ROOT/name).read_bytes())
        for f in m['files']:assert bind(ROOT/f['path'])==f
    r=json.loads((HERE/'final_gate_live_receipt.json').read_bytes());o=r['result']
    assert o['status']=='PASS' and o['phase']=='exact_live_acceptance' and o['prepared_body_is_live'] and not o['draft']
    assert json.loads((HERE/'final_gate_live.stdout').read_bytes())==o and not (HERE/'final_gate_live.stderr').read_bytes()
    comparison=json.loads((HERE/'root_live_comparison_receipt.json').read_bytes())
    assert comparison['entire_result_input_Git_Merkle_objects_exact'] and comparison['every_other_command_record_exact']
    assert comparison['whole_receipts_equal_after_only_proven_differences'] and not comparison['arbitrary_receipt_normalization']
    assert json.loads((HERE/'compare_live_reproduction.stdout').read_bytes())==comparison
    assert not (HERE/'compare_live_reproduction.stderr').read_bytes()
    path=HERE/'LIVE_PUBLIC_MANIFEST.json';assert not path.exists(),'Final manifest is immutable'
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (HERE/'seal_live.stdout').write_bytes(b'');(HERE/'seal_live.stderr').write_bytes(b'')
    files=sorted(p for p in HERE.rglob('*') if p.is_file())
    assert not any('private' in p.parts or '__pycache__' in p.parts for p in files)
    summary={'status':'SEALED_EXACT_LIVE_PASS','initial_allowlist_members':69,'prepared_additive_members':68,
             'live_additive_members':len(files)+1,'live_bound_files':len(files),'both_prior_manifests_unchanged':True}
    stream=json.dumps(summary,sort_keys=True)+'\n';(HERE/'seal_live.stdout').write_text(stream)
    m={'created_utc':utc,'phase':'exact_live_acceptance_before_authorized_merge','status':'PASS',
       'prior_immutable_manifests_sha256':SEALS,'all_prior_bindings_exact':True,
       'explicit_public_allowlist':[p.relative_to(ROOT).as_posix() for p in files]+[path.relative_to(ROOT).as_posix()],
       'files':[bind(p) for p in files],'observed_live_head':o['head'],'observed_actual_main':o['remote_main'],
       'exact_live_body_sha256':o['api_body_sha256'],'complete_live_receipt_sha256':bind(HERE/'final_gate_live_receipt.json')['sha256'],
       'complete_root_live_receipt_sha256':comparison['root_receipt_sha256'],
       'whole_reproduction_explicit_differences':['observed_utc','pr_live/pr_final stdout hashes explained by exactly two raw repo/size leaves'],
       'unrestricted_status':'unsolved5/5','novelty_certification':False,
       'actual_merge_reported_by_root':'ced99fb2fa921e1f66a701efec35f5c2d61fddfe',
       'private_exclusions':['private/**','**/__pycache__/**'],
       'publication_instruction':'Publish exactly the original, prepared and live allowlists union. Preserve all earlier manifests. Do not stage private input/output trees.'}
    path.write_text(json.dumps(m,indent=2)+'\n');print(stream,end='')
if __name__=='__main__':main()
