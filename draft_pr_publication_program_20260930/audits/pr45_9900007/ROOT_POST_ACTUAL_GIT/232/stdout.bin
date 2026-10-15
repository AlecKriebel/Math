#!/usr/bin/env python3
"""Seal only this family's files; manifest paired with a self-hash file."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat
root=Path(__file__).resolve().parent
manifest=root/'OWN_CLOSURE.json'
selfhash=root/'OWN_CLOSURE.sha256'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert not manifest.exists() and not selfhash.exists(), 'Never overwrite a prior seal'
inputs=json.loads((root/'INPUT_PINS.json').read_text())['inputs']
assert len(inputs)==18
for item in inputs:
 path=Path(item['path'])
 assert path.stat().st_size==item['bytes'] and digest(path)==item['sha256'],item['path']
receipt=json.loads((root/'independent_controls_run1/RECEIPT.json').read_text())
run=root/'independent_controls_run1'
assert receipt['exit_code']==0
assert digest(root/'independent_controls.py')==receipt['program_sha256_after']
assert digest(root/'capture_controls.py')==receipt['operator_sha256_after']
for item in ['stdout','stderr']:
 assert digest(run/f'{item}.bin')==receipt[f'{item}_sha256']
 assert (run/f'{item}.bin').stat().st_size==receipt[f'{item}_bytes']
x=json.loads((run/'stdout.bin').read_text())
assert x['runtime_identity']['pid']==receipt['child_pid'] and x['control_count']==13928
files=sorted(p for p in root.rglob('*') if p.is_file())
assert not any(p.is_symlink() for p in files)
records=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':digest(p),'sealed_mode':'0444'} for p in files]
data={'seal_utc':datetime.now(timezone.utc).isoformat(),'family_root':str(root),'scope':'This family only. Content records plus OWN_CLOSURE.json and paired OWN_CLOSURE.sha256 exhaust all regular files. No native acceptance/publication decision.','input_count_checked':18,'own_runtime_receipt_checked':True,'files':records,'self_pair':{'manifest':'OWN_CLOSURE.json','self_hash':'OWN_CLOSURE.sha256','mechanism':'Self-hash file pins the exact manifest bytes; manifest deliberately excludes the two self-pair files to avoid circular hashes.'},'foreign_primary_exclusions':[],'full_target_resolved':False,'novelty_certified':False}
manifest.write_text(json.dumps(data,indent=2)+'\n')
selfhash.write_text(digest(manifest)+'  OWN_CLOSURE.json\n')
for p in files+[manifest,selfhash]:p.chmod(0o444)
# Actual full-coverage verification after the writes and permission changes.
expected={r['path'] for r in records}|{'OWN_CLOSURE.json','OWN_CLOSURE.sha256'}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==expected,(actual-expected,expected-actual)
for r in records:
 p=root/r['path'];assert p.stat().st_size==r['bytes'] and digest(p)==r['sha256']
for rel in actual:assert stat.S_IMODE((root/rel).stat().st_mode)==0o444,rel
assert selfhash.read_text()==digest(manifest)+'  OWN_CLOSURE.json\n'
print(json.dumps({'verified_utc':datetime.now(timezone.utc).isoformat(),'own_only_closed':True,'actual_file_count':len(actual),'all_regular_files_mode':'0444','manifest_sha256':digest(manifest),'self_hash_sha256':digest(selfhash),'input_count_rechecked':18,'audit_completion_percent':100,'full_target_discovery_completion_percent':0,'publication_or_acceptance_claim':False},indent=2))
