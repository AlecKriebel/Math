"""Final explicit public allowlist; self-excluded seal, no later payload edits."""
import hashlib,json,stat
from pathlib import Path
R=Path(__file__).resolve().parent
names=['RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','INDEPENDENT_RECONSTRUCTION.md','START.json','SOURCE_PINS.json','PIXEL_AND_SOURCE_SCOPE.json','PACKAGE_AND_METADATA.json','LIVE_GATE.json','HISTORICAL_STATIC_CHECK.json','GUARD_REPLAY.json','COPY_REPLAY.json','HELPER_MODE_SUMMARY.json','ADDITIONAL_CONTROLS.json','FINALIZER_CONTROLS.json','FINAL_METADATA_CONTROLS.json','FULL_DRIFT_CONTROLS.json','authenticate.py','live_gate.py','cold_replay.py','helper_controls.py','additional_controls.py','finalizer_controls.py','r7_controls.py','run_helper_modes.py','full_drift_controls.py','final_metadata_controls.py','package_evidence.py','source_auth.py','render_sources.py','finish_review.py','seal_review.py']+[f'HELPER_CONTROLS_{m}.json' for m in ['normal','O','OO','env2']]+[f'R7_CONTROLS_{m}.json' for m in ['normal','O','OO','env2']]
if len(names)!=len(set(names)) or (R/'MANIFEST.json').exists():raise RuntimeError('Duplicate or existing final seal')
records={}
for name in sorted(names):
 p=R/name
 if not stat.S_ISREG(p.lstat().st_mode) or '/' in name or name=='MANIFEST.json':raise RuntimeError('Unsafe public payload')
 b=p.read_bytes();records[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
v={'schema_version':1,'pr':938,'problem_id':'30003634','candidate_revision':5,'files':records,'explicit_public_allowlist':list(records),'manifest_self_excluded':True,'private_raw_source_bodies_and_scratch_excluded':True}
b=(json.dumps(v,indent=2)+'\n').encode();(R/'MANIFEST.json').write_bytes(b)
# Deliberately read-only after the final seal.
for name,want in records.items():
 raw=(R/name).read_bytes()
 if {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}!=want:raise RuntimeError('Post-seal drift')
print(json.dumps({'verdict':'COMPLETE_CLEAN','public_payloads':len(records),'manifest_sha256':hashlib.sha256(b).hexdigest(),'manifest_bytes':len(b),'no_payload_edits_after_seal':True}))
