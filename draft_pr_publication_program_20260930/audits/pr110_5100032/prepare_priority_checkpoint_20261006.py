from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent;P=A.parents[1];C=A.parents[2]
selected=set()
def add(p):
    if not p.is_file() or p.is_symlink():raise RuntimeError('file '+str(p))
    relative=p.relative_to(C).as_posix()
    if any(x in p.parts for x in ['private_sources','private_review_materials','private_source_extracts','primary_sources_private','root_primary_read_private','private_operational_archive']):raise RuntimeError('private '+relative)
    selected.add(relative)
for folder,key in [('priority_classical_confocal_mechanism_20261006','payload'),('priority_exact_invariant_history_20261006','payload'),('priority_modern_invariant_mechanism_20261006','public_payload_bodies')]:
    d=A/folder;m=json.loads((d/'OUTPUT_MANIFEST.json').read_text())
    for r in m[key]:
        p=d/r['path'];b=p.read_bytes()
        if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:raise RuntimeError('manifest body changed')
        add(p)
    add(d/'OUTPUT_MANIFEST.json');add(d/'SEAL_RECEIPT.json')
    for closing in {'priority_classical_confocal_mechanism_20261006':['final_seal'],'priority_exact_invariant_history_20261006':['seal_public_audit_final','verify_public_seal_final'],'priority_modern_invariant_mechanism_20261006':['seal_public_payload']}[folder]:
        for p in (d/'actual_operations'/closing).iterdir():
            if p.is_file():add(p)
for p in A.iterdir():
    if p.is_file() and p.name!='PRIORITY_CHECKPOINT_SELECTION_20261006.json':add(p)
for p in (A/'root_priority_20261006').iterdir():
    if p.is_file():add(p)
for d in [A/'root_checkpoint_authentication_20261006',A/'priority_remote_main_reconciliation_20261006',P/'audits/pr108_30003996/actual_checkpoints/PR110_source_math_reconciled_20261006']:
    for p in d.rglob('*'):
        if p.is_file():add(p)
for d in (A/'actual_operations').iterdir():
    if d.is_dir() and (d/'execution.json').is_file():
        for p in d.iterdir():
            if p.is_file():add(p)
for name in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']:add(P/name)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
note='\n'+now+' — Priority checkpoint selection (workflow30%, priority85%): all3 sealed families514 public payloads and their closing envelopes selected; copyright bodies excluded. The earlier two-family paragraph records the preceding09:58 intermediate state; latest state is all3 root-authenticated with NEW combined adjudication running. Final journal M1 unresolved; no status/publication/native action. Remote parent b569035aa9ce654f32e13f2cf19558a94a038b69 preserved.\n'
for log in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md']:
    with log.open('a') as f:f.write(note)
selection=A/'PRIORITY_CHECKPOINT_SELECTION_20261006.json';selected.add(selection.relative_to(C).as_posix())
r={'schema':'pr110-priority-checkpoint-exact-selection/v1','UTC':now,'actual_operator_PID':os.getpid(),'expected_parent':'b569035aa9ce654f32e13f2cf19558a94a038b69','paths':sorted(selected),'all3_family_sealed_public_payloads':514,'copyright_private_bodies_excluded':True,'combined_priority_or_publication_clearance':False,'new_central_proof_search_turns':0,'workflow_estimate_percent':30,'pending_required_source_access_question':True,'pending_new_cross_family_adjudication':True}
selection.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='paths'}));print('selected_paths',len(selected))
