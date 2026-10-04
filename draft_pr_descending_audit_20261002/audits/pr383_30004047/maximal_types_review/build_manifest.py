#!/usr/bin/env python3
"""Seal or verify all audit artifacts; the manifest is the sole self-exclusion."""
import pathlib,hashlib,json,sys,datetime
HERE=pathlib.Path(__file__).resolve().parent
OUT=HERE/'AUDIT_MANIFEST.json'
FROZEN=HERE.parent/'snapshot_manifest.json'
HEAD='967e8e489aa4599f712d5ddcde62e591827f7e38'
def record(path):
 data=path.read_bytes()
 return {'path':path.relative_to(HERE).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
actual=[record(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=OUT]
binding={'path':'../snapshot_manifest.json','bytes':FROZEN.stat().st_size,'sha256':hashlib.sha256(FROZEN.read_bytes()).hexdigest()}
if '--verify' in sys.argv:
 saved=json.loads(OUT.read_text())
 assert saved['head']==HEAD
 assert saved['files']==actual
 assert saved['frozen_snapshot_manifest']==binding
 assert json.loads(FROZEN.read_text())['head']==HEAD
 print(json.dumps({'status':'PASS','head':HEAD,'audit_artifacts_checked':len(actual),'audit_manifest_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'frozen_snapshot_manifest_sha256':binding['sha256']},indent=2))
else:
 result={'audit':'PR383 maximal-type small-support family','head':HEAD,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_disposition':'unsolved','substantive_author_turns':'5/5','mandatory_mathematical_repairs':[],'scope':'Explicit uniform-A finite-size and structural results, not the original arbitrary-graph conjecture','frozen_snapshot_manifest':binding,'source_reconstruction_before_candidate_and_prior_verdicts':True,'prior_verdict_read_after_independent_proofs_and_new_controls':True,'files':actual,'self_exclusion':'AUDIT_MANIFEST.json; its SHA256 is reported externally by --verify'}
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'status':'SEALED','files':len(actual),'manifest_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},indent=2))
