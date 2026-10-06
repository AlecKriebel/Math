"""Select only PR95 acceptance and new evidence for its private main checkpoint."""
from pathlib import Path
import hashlib,json
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise RuntimeError(message)
native=load(A/'native_acceptance_20261005/PREPARED_RECEIPT.json')
require(native['native_optimized_runs_passed'] and not native['priority_clearance'],'native qualified gate')
paths=set(native['native_paths'])
top=['ROOT_READY_FOR_PUBLICATION.json','ROOT_PUBLIC_DEPOSIT_VERIFICATION.json','ROOT_TRACKER_RECORD.json','ROOT_AUTHENTICATED_whole_qualified_package_round2_20261005.json','ROOT_REPAIRED_CANDIDATE_AUTHENTICATION_20261005.json','RESEARCH_LOG.md','PR95_ACCEPTED_BODY.md','record_cli.py','scoped_checkpoint.py','prepare_native_acceptance.py','verify_public_deposit.py','append_verified_tracker.py','UNEXECUTED_ACCEPTANCE_HELPERS.json','finalize_PR95.py','select_source_acceptance.py','actual_checkpoints/v2_authenticated_disposition/RECEIPT.json','actual_checkpoints/v2_authenticated_disposition/PROCESS_JOURNAL.json']
paths.update(str((A/n).relative_to(C)) for n in top)
paths.add(str((A/'ROOT_MAIN_COORDINATION_DISPOSITION_20261005.json').relative_to(C)))
paths.update(str((A/n).relative_to(C)) for n in ['native_acceptance_helper_initial_20261005.py','NATIVE_HELPER_PATH_REPAIR_20261005.json','resume_native_acceptance.py'])
paths.add(str((P/'CURRENT_PROGRESS.json').relative_to(C)))
D=A/'whole_qualified_package_round2_20261005';m=load(D/'CLOSED_MANIFEST.json')
require(sha(D/'CLOSED_MANIFEST.json')=='39eaf4b331e0992053f724c488784b35fb4b1cc238c6f1b2e3521e42bcff1102','fresh review pin')
for e in m['files']:
    f=D/e['file'];require(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'review evidence changed')
    paths.add(str(f.relative_to(C)))
paths.add(str((D/'CLOSED_MANIFEST.json').relative_to(C)))
labels=['root_round2_closed_integrity','readiness_head_read','zenodo_check','zenodo_stage','zenodo_staged_inspect','zenodo_publish','zenodo_published_inspect','public_byte_verification','tracker_append_verified','pr95_published_body_read','pr95_qualified_body_update','pr95_qualified_body_timing_update','pr95_qualified_body_readback','pr95_premerge_head','pr95_ready','pr95_ready_readback','pr95_merge','pr95_merged_readback','native_acceptance_prepare']
labels.append('native_acceptance_resume')
for n in labels:
    D=A/'actual_operations'/n;require(D.is_dir(),'actual operation missing '+n)
    paths.update(str(f.relative_to(C)) for f in D.iterdir() if f.is_file())
for n in ['published_download_verification_20261005','tracker_acceptance_20261005','native_acceptance_20261005']:
    paths.update(str(f.relative_to(C)) for f in (A/n).rglob('*') if f.is_file() and not f.is_symlink())
out=A/'SOURCE_ACCEPTANCE_CHECKPOINT_SELECTION.json';paths.add(str(out.relative_to(C)))
for rel in paths:
    if rel==str(out.relative_to(C)):continue
    f=C/rel;require(f.resolve().is_relative_to(C) and f.is_file() and not f.is_symlink(),'unsafe selection')
out.write_text(json.dumps({'paths':sorted(paths),'role':'Scoped PR95 accepted source and actual new closed evidence; no foreign files or recursively duplicated checkpoint streams.'},indent=2)+'\n')
print(json.dumps({'selected_paths':len(paths),'base':native['base_commit'],'merge_commit':native['merge_commit'],'priority_clearance':False}))
