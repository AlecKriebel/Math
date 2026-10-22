"""Settle the explicit public map after all checks; no writes after MANIFEST."""
import hashlib,json,stat
from pathlib import Path
R=Path(__file__).resolve().parent
names=['RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','INDEPENDENT_RECONSTRUCTION.md','SOURCE_PINS.json','PIXEL_AND_SOURCE_SCOPE.json','PACKAGE_AND_METADATA.json','LIVE_GATE.json','HISTORICAL_REGRESSION_CHECK.json','GUARD_REPLAY.json','COPY_REPLAY.json','HELPER_MODE_SUMMARY.json','FINALIZER_CONTROLS.json','ADDITIONAL_CONTROLS.json','authenticate.py','live_gate.py','cold_replay.py','helper_controls.py','run_helper_modes.py','finalizer_auth_control.py','finalizer_controls.py','additional_controls.py','package_evidence.py','source_auth.py','render_sources.py','finish_review.py','seal_review.py']+[f'HELPER_CONTROLS_{m}.json' for m in ['normal','O','OO','env2']]+[f'FINALIZER_AUTH_CONTROL_{m}.json' for m in ['normal','O','OO','env2']]
if len(names)!=len(set(names)) or (R/'MANIFEST.json').exists():raise RuntimeError('Duplicate or existing final seal')
records={}
for name in sorted(names):
 p=R/name
 if not stat.S_ISREG(p.lstat().st_mode) or '/' in name or name=='MANIFEST.json':raise RuntimeError('Unsafe public payload')
 raw=p.read_bytes();records[name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
map_={'schema_version':1,'pr':938,'problem_id':'30003634','candidate_revision':4,'files':records,'explicit_public_allowlist':list(records),'manifest_self_excluded':True,'private_raw_source_bodies_and_scratch_excluded':True}
raw=(json.dumps(map_,indent=2)+'\n').encode();(R/'MANIFEST.json').write_bytes(raw)
# Read-only checks after final seal; intentionally no other writes.
for name,record in records.items():
 b=(R/name).read_bytes()
 if {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}!=record:raise RuntimeError('Post-seal drift')
print(json.dumps({'verdict':'COMPLETE_ADVERSE_R7','public_payloads':len(records),'manifest_sha256':hashlib.sha256(raw).hexdigest(),'manifest_bytes':len(raw),'no_payload_edits_after_seal':True}))
