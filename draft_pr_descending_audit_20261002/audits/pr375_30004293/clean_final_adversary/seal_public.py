#!/usr/bin/env python3
"""Seal or verify an explicit bounded owned public artifact set."""
from pathlib import Path
import hashlib,json,datetime,sys
H=Path(__file__).resolve().parent
MEMBERS=(
 'SOURCE_FIRST_SEAL.md','PRE_CANDIDATE_CONTROLS.json','independent_controls.py',
 'research_log.md','MATHEMATICAL_CONTROLS.json','mathematical_controls.py','MATHEMATICAL_SEAL.md',
 'package_audit.initial.py','package_audit.py','INITIAL_REPLAY_FAILURE.json','PACKAGE_REPLAY_RECEIPT.json',
 'rank_extension_controls.py','RANK_EXTENSION_CONTROLS.json','POSTSEAL_RANK_EXTENSION.md',
 'final_integration.pre_body_append.py','FINAL_INTEGRATION_CERTIFICATE.pre_body_append.json',
 'final_integration.py','CHECKPOINT_90_INTEGRATION.json','FINAL_INTEGRATION_CERTIFICATE.json',
 'FINAL_REPORT.md','AUDIT_GATE.json','seal_public.py')
def digest(b):return hashlib.sha256(b).hexdigest()
def validate():
    assert len(set(MEMBERS))==22
    assert {p.name for p in H.iterdir() if p.is_file()}<=set(MEMBERS)|{'PUBLIC_MANIFEST.json'}
    for name in MEMBERS:
        assert '/' not in name and name.endswith(('.md','.json','.py'))
        assert (H/name).is_file() and (H/name).stat().st_size<200000
    final=json.loads((H/'FINAL_INTEGRATION_CERTIFICATE.json').read_text())
    for name,key in [('SOURCE_FIRST_SEAL.md','source_seal_sha256'),('MATHEMATICAL_SEAL.md','mathematical_seal_sha256')]:
        assert digest((H/name).read_bytes())==final[key]
    assert final['completion_estimate_percent']==100
    assert final['unchanged_original_target_files']==53 and len(final['all_final_git_objects'])==54
    assert final['metadata_update_mapping']['current_body_sha256']=='f02179f4389a888cb3807d7da853e28a3286ea7c2bdcd695b631d414a1663458'
if __name__=='__main__':
    validate();mf=H/'PUBLIC_MANIFEST.json'
    if '--verify' in sys.argv:
        d=json.loads(mf.read_text());assert tuple(e['path'] for e in d['files'])==MEMBERS
        for e in d['files']:
            b=(H/e['path']).read_bytes();assert len(b)==e['bytes'] and digest(b)==e['sha256']
        print(json.dumps({'owned_public_members_verified':len(MEMBERS),'source_math_seals_unchanged':True,'raw_extract_render_candidate_runtime_capture_replay_cache_members':0,'final_gate':100},sort_keys=True))
    else:
        d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'explicit owned bounded audit artifacts; no raw/extract/render/private replay/runtime/cache/capture members','completion_estimate_percent':100,'files':[{'path':name,'bytes':len((H/name).read_bytes()),'sha256':digest((H/name).read_bytes())} for name in MEMBERS]}
        mf.write_text(json.dumps(d,indent=2)+'\n')
        print(json.dumps({'sealed_public_members':len(MEMBERS),'manifest_sha256':digest(mf.read_bytes())},sort_keys=True))
