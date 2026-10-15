#!/usr/bin/env python3
"""Seal the additive prepared allowlist while verifying every immutable original."""
import datetime,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).parents[2]
HERE=pathlib.Path(__file__).parent
INITIAL_SHA='6cd9683ff75d92e821b8d704bf72e908c1bcd4b087fe367fdb2045997cb11ee8'
def binding(p):
    b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    initial=ROOT/'public/PUBLIC_MANIFEST.json'
    assert binding(initial)['sha256']==INITIAL_SHA
    m=json.loads(initial.read_bytes());assert len(m['files'])==68 and len(m['explicit_public_allowlist'])==69
    for f in m['files']:assert binding(ROOT/f['path'])==f
    receipt=json.loads((HERE/'round2_prepared/final_gate_prepared_receipt.json').read_bytes())
    assert receipt['result']['status']=='PASS' and not receipt['result']['prepared_body_is_live']
    assert json.loads((HERE/'round2_prepared/final_gate_prepared.stdout').read_bytes())==receipt['result']
    assert not (HERE/'round2_prepared/final_gate_prepared.stderr').read_bytes()
    manifest=HERE/'PREPARED_PUBLIC_MANIFEST.json';assert not manifest.exists(),'Prepared manifest is immutable'
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (HERE/'initial_evidence_integrity.json').write_text(json.dumps({'checked_utc':utc,'initial_manifest_sha256':INITIAL_SHA,'initial_allowlist_members':69,'initial_bound_files':68,'all_initial_bindings_exact':True},indent=2)+'\n')
    (HERE/'seal_prepared.stderr').write_bytes(b'')
    (HERE/'seal_prepared.stdout').write_bytes(b'')
    paths=sorted(p for p in HERE.rglob('*') if p.is_file())
    assert all('__pycache__' not in p.parts and 'private' not in p.parts for p in paths)
    output={'status':'SEALED_PREPARED_PASS','initial_allowlist_members':69,'initial_bound_files':68,'additive_allowlist_members':len(paths)+1,'additive_bound_files':len(paths),'final_live_acceptance_pending':True}
    stream=json.dumps(output,sort_keys=True)+'\n';(HERE/'seal_prepared.stdout').write_text(stream)
    obj={'created_utc':utc,'phase':'round2_prepared_acceptance','status':'PASS_PREPARED_BODY_NOT_YET_LIVE','initial_manifest_sha256':INITIAL_SHA,'initial_allowlist_members':69,'initial_bound_files':68,'all_initial_bindings_exact':True,'additive_public_allowlist':[p.relative_to(ROOT).as_posix() for p in paths]+[manifest.relative_to(ROOT).as_posix()],'files':[binding(p) for p in paths],'staged_gate_sha256':binding(HERE/'final_gate_staged.py')['sha256'],'stage_descriptor_sha256':binding(HERE/'ROUND2_STAGE_DESCRIPTOR.json')['sha256'],'live_head':receipt['result']['head'],'actual_remote_main':receipt['result']['remote_main'],'proposed_body_sha256':receipt['result']['prepared_body_sha256'],'observed_body_sha256':receipt['result']['api_body_sha256'],'remaining_actions':['root unchanged prepared-gate reproduction','send exact prospective body','same-code exact-live acceptance','root unchanged exact-live reproduction','authorized merge with latest-main preservation verification'],'private_exclusions':['private/**','**/__pycache__/**'],'publication_instruction':'Publish only the immutable original allowlist plus this explicit additive allowlist. No recursive staging or private inputs.'}
    manifest.write_text(json.dumps(obj,indent=2)+'\n')
    print(stream,end='')
if __name__=='__main__':main()
