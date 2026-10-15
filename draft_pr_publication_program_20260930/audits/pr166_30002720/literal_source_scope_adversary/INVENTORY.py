#!/usr/bin/env python3
"""Recompute every retained file identity, excluding only MANIFEST.json itself."""
from pathlib import Path
import datetime
import hashlib
import json

root=Path(__file__).resolve().parent
base=root.parent/'original_submission/files/unsolved_math_prioritization/attempts/30002720'
public_names=[
 'FIRST_ASSESSMENT.md','FIRST_ASSESSMENT_SEAL.json','DERIVATION.md',
 'CHECKS.py','CHECK_RESULTS.json','RESEARCH_LOG.md','REVIEW.md',
 'RESULT.json','INVENTORY.py','MANIFEST.json',
]
def ident(p):
    data=p.read_bytes()
    return {'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'mode':format(p.stat().st_mode & 0o777,'04o')}

files=[]
for p in sorted(root.rglob('*')):
    if p.is_file():
        assert not p.is_symlink(),p
        rel=p.relative_to(root).as_posix()
        if rel=='MANIFEST.json':
            continue
        item=ident(p)
        item['relative_path']=rel
        item['public_own_output']=rel in public_names
        item['handling']='private audit evidence; excluded from public output' if rel.startswith('private/') else 'own audit output'
        files.append(item)

original_inputs=[]
for name in ['COUNTEREXAMPLE.md','problem.json','source_manifest.json','SOURCE_AUDIT.md']:
    item=ident(base/name)
    item['read_phase']='post-seal' if name=='SOURCE_AUDIT.md' else 'pre-seal permitted candidate/neutral input'
    original_inputs.append(item)

instruction=Path('/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.1009.11318/skills/pdf/SKILL.md')
result={'schema_version':1,'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'audit_root':str(root),'candidate_original_head_supplied':'efc3f35a72543ad9ae76fd31a860116f1ffd4a32','self_exclusion':{'relative_path':'MANIFEST.json','reason':'A byte-level manifest cannot include its own final hash without recursion; it is the only retained-file exclusion.','external_digest_delivery':'SHA256, byte count and mode are delivered to the parent agent and in the final response, not retained as a circular sidecar.'},'public_own_output_whitelist':public_names,'private_policy':'All private/ files, including complete third-party bodies, extractions, renderings, metadata and post-seal author input, are excluded from public own outputs.','retained_files':files,'actual_original_inputs':original_inputs,'instruction_file_read':ident(instruction)}
path=root/'MANIFEST.json'
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'manifest':ident(path),'inventoried_file_count':len(files),'only_self_exclusion':True},indent=2))
