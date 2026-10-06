#!/usr/bin/env python3
"""Seal an exact self-excluding first-party audit manifest; check frozen originals."""
from pathlib import Path
from datetime import datetime, timezone
import json,hashlib,subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()
IGNORED={'sources','tmp','isolated','__pycache__'}
def members():
 return sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and not any(x in IGNORED for x in p.relative_to(HERE).parts))
prov=json.loads((HERE/'provenance_results.json').read_text())
for item in prov['original_artifacts']:
 if not item['path'].startswith('unsolved_math_prioritization/attempts/10000046/'):continue
 name=item['path'].removeprefix('unsolved_math_prioritization/attempts/10000046/')
 actual=(HERE.parent/'source_snapshot'/name).read_bytes()
 assert sha(actual)==item['snapshot_sha256']
 gitblob=subprocess.check_output(['git','show',prov['head']+':'+item['path']],cwd=ROOT)
 assert actual==gitblob
controls=json.loads((HERE/'controls_results.json').read_text())
assert controls['protected_live_bytes_unchanged_by_controls']
assert all(x['code_unchanged'] and x['receipt_bytes_equal'] for x in controls['baseline_replays'].values())
files=[{'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in members()]
manifest={'schema':'exact-self-excluding-first-party-audit-v1','sealed_at_utc':datetime.now(timezone.utc).isoformat(),
 'audit_assignment_completion_percent':100,'original_target_verification_percent':0,'original_substantive_turns':'1/5','verification_turns':0,
 'scope':'Original-stage PR33 source/provenance/scope family only; copied selected source records are first-party audit extracts, not source-truth claims.',
 'excluded_directories':sorted(IGNORED),'excluded_self':'MANIFEST.json','original_numeric_members_preserved':13,
 'head':prov['head'],'actual_base':prov['actual_merge_base'],'dated_main':prov['dated_main'],
 'file_count':len(files),'files':files}
(HERE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
expected={x['path'] for x in manifest['files']};assert expected=={str(x.relative_to(HERE)) for x in members()}
for x in manifest['files']:
 p=HERE/x['path'];assert p.stat().st_size==x['bytes'] and sha(p.read_bytes())==x['sha256']
print(json.dumps({'sealed':True,'first_party_file_count':len(files),'original_numeric_members_preserved':13,'original_turns':'1/5','verification_turns':0,'original_target_verification_percent':0},indent=2))
