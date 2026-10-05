from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,gzip,os,stat
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_descending_audit_20261002/audits/pr302_30003508';W=A/'publication_operations_adversary_02';D=A/'publication_preparation';F=A/'preprint_package_v02'
def pin(p):
 p=Path(p);assert p.is_file() and not p.is_symlink();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
rows=[];archive=W/'initial_full_sources';archive.mkdir()
paths=[D/n for n in ('publication_guard.py','run_zenodo_step.py','verify_public_record.py','append_tracker.py','REVISED_OPERATOR_MANIFEST.json')]+[A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json',R/'zenodo_deposit_tool/zenodo.py',R/'zenodo_deposit_tool/README.md',A/'ROOT_PUBLICATION_OPERATORS_GLOBAL_REPAIR_02.json',A/'publication_operator_version_01/ARCHIVE_MANIFEST.json',F/'SECOND_CANDIDATE_MANIFEST.json']
for i,p in enumerate(paths):
 b=p.read_bytes();q=archive/(str(i)+'_'+p.name+'.gz');q.write_bytes(gzip.compress(b,mtime=0));q.chmod(0o444);assert gzip.decompress(q.read_bytes())==b;rows.append(dict(input=pin(p),full_body_archive=pin(q)))
manifest=json.loads((F/'SECOND_CANDIDATE_MANIFEST.json').read_bytes());assert len(manifest['files'])==23
for row in manifest['files']:assert pin(row['path'])==row
science=json.loads((A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json').read_bytes())
for row in science['closed_evidence_pins']:assert pin(row['path'])==row
assert not (A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json').exists()
result=dict(UTC=datetime.now(timezone.utc).isoformat(),actual_self_recorder_PID=os.getpid(),status='INITIAL_COMPLETE_SOURCE_AND_CANDIDATE_AUTHENTICATION',sources=rows,candidate_files=manifest['files'],science_evidence_pins=science['closed_evidence_pins'],runtime_targets=[pin(Path(p).resolve()) for p in ('/opt/homebrew/bin/python3','/usr/bin/curl','/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws')],production_operations_gate_absent=True,production_OUT_absent=not (A/'publication_actual').exists(),publication_clearance=False,limits='Initializer self-recording is not independent OS/upstream launch attestation')
(W/'INITIAL_INPUTS.json').write_text(json.dumps(result,indent=2)+'\n')
(W/'RESEARCH_LOG.md').write_text('# Fresh PR302 publication operations review 02\n\n'+result['UTC']+' — Authenticated all four current programs, registry, kit, README, all23 frozen public files and14 actual science evidence pins. Independently read each entire current program before consulting prior verdict. Operational review15%, approval readiness remains unadjudicated, service execution0%. Writes are confined to this new review namespace.\n')
print(json.dumps(dict(status=result['status'],actual_self_recorder_PID=os.getpid(),sources=len(rows),public_files=23,science_evidence=len(science['closed_evidence_pins']),production_operations_gate_absent=True)))
