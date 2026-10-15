#!/usr/bin/env python3
"""Inventory every retained regular file; only the manifest itself is excluded."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat
root=Path(__file__).resolve().parent
manifest=root/'FINAL_MANIFEST.json'
seal=json.loads((root/'FIRST_ASSESSMENT_SEAL.json').read_text())
for e in seal['bound_inputs_and_evidence']:
    p=root/e['path']; data=p.read_bytes()
    assert hashlib.sha256(data).hexdigest()==e['sha256']
    assert len(data)==e['size'] and oct(stat.S_IMODE(p.stat().st_mode))==e['mode']
assert stat.S_IMODE((root/'FIRST_ASSESSMENT.md').stat().st_mode)==0o444
assert stat.S_IMODE((root/'FIRST_ASSESSMENT_SEAL.json').stat().st_mode)==0o444
whitelist=json.loads((root/'PUBLIC_OUTPUT_WHITELIST.json').read_text())
entries=[]
for p in sorted(root.rglob('*')):
    if p.is_file() and p!=manifest:
        assert not p.is_symlink()
        data=p.read_bytes(); rel=str(p.relative_to(root))
        entries.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'size':len(data),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o'),'publication_eligible_own_output':rel in whitelist['paths'],'classification':'private input or primary-source body' if rel.startswith('private/') else 'own audit output'})
assert all((root/rel).is_file() or rel=='FINAL_MANIFEST.json' for rel in whitelist['paths'])
assert all(not e['publication_eligible_own_output'] for e in entries if e['path'].startswith('private/'))
x={'created_at_utc':datetime.now(timezone.utc).isoformat(),'root':str(root),'coverage':'Every retained regular file and retained input, with exact SHA256, byte size and mode.','only_inventory_self_exclusion':'FINAL_MANIFEST.json','external_digest_delivery':'Manifest SHA256 is printed by this builder and reported to the parent, not retained in a recursive digest file.','first_seals_bound':{'FIRST_ASSESSMENT.md':hashlib.sha256((root/'FIRST_ASSESSMENT.md').read_bytes()).hexdigest(),'FIRST_ASSESSMENT_SEAL.json':hashlib.sha256((root/'FIRST_ASSESSMENT_SEAL.json').read_bytes()).hexdigest()},'entries':entries,'entry_count':len(entries)}
manifest.write_text(json.dumps(x,indent=2)+'\n');os.chmod(manifest,0o444)
# Immediate full inventory verification after writing.
for e in entries:
    p=root/e['path'];data=p.read_bytes()
    assert hashlib.sha256(data).hexdigest()==e['sha256'] and len(data)==e['size']
    assert format(stat.S_IMODE(p.stat().st_mode),'04o')==e['mode']
print(json.dumps({'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'manifest_size':manifest.stat().st_size,'manifest_mode':format(stat.S_IMODE(manifest.stat().st_mode),'04o'),'inventory_entries':len(entries),'first_seal_preserved':True,'all_inventory_entries_verified':True},indent=2))
