from pathlib import Path
import datetime,json,os
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1];Q=A/'qualified_publication_package_v2'
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
auth=json.loads((A/'ROOT_REPAIRED_CANDIDATE_AUTHENTICATION_20261005.json').read_text())
if not auth['verified'] or not auth['R1_repair_authenticated']:raise RuntimeError('repair gate')
pr=P/'CURRENT_PROGRESS.json';p=json.loads(pr.read_text());p.update({'UTC':utc,'current_PR_workflow_percent':65,
    'current_package':'audits/pr95_10400120/qualified_publication_package_v2',
    'current_package_preparation_percent':100,'current_whole_package_required_repairs':[],
    'current_package_R1_repair_authenticated':True,
    'current_active_whole_package_reviewer':'pr95_whole_qualified_package_round2_20261005',
    'current_publication_ready':False,'remaining_current_step':'New second whole-package adversary reviews corrected frozen v2. Qualified publication remains gated on clean final review; priority unresolved.'});dump(pr,p)
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n### '+utc+' — corrected V2 authenticated, second fresh review active; PR95 workflow65%, math100%, priority85% unresolved; program12/99 (12.12%)\nROOT read repair report/scope/exact diff and authenticated2030 V2 file bodies, four intentional hostile fixture links, immutable693-file V1, public payload and110 archive members. All mathematical checkers, manuscript/PDF and exact deposit metadata remain unchanged. Fourteen hostile component/content/manifest/AST controls reject in both modes before output creation; two clean guards pass. Initial ROOT authentication mistakenly counted16 total as14 hostile; the captured failed administrative check remains preserved, and the corrected actual partition/authentication passes without relabeling or rerunning science. New round2 adversary is independent and active; no service action or primary mutation.\n')
paths={str(pr.relative_to(C)),str((A/'RESEARCH_LOG.md').relative_to(C))}
for n in ['authenticate_repaired_candidate.py','ROOT_REPAIRED_CANDIDATE_AUTHENTICATION_20261005.json','record_v2_checkpoint.py','append_verified_tracker.py']:
    paths.add(str((A/n).relative_to(C)))
for f in (Q/'publicfiles').rglob('*'):
    if f.is_file() and not f.is_symlink():paths.add(str(f.relative_to(C)))
for f in (Q/'private_notes').iterdir():
    if f.is_file() and not f.is_symlink():paths.add(str(f.relative_to(C)))
for n in ['zenodo-deposit.json','PREPARATION_MANIFEST.json']:paths.add(str((Q/n).relative_to(C)))
# Publish concrete receipts/source snapshots without duplicating every hostile fixture tree.
for n in ['private_notes/assembled_run','private_notes/clean_archive_run','private_notes/processes']:
    for f in (Q/n).rglob('*'):
        if f.is_file() and not f.is_symlink():paths.add(str(f.relative_to(C)))
for n in ['actual_operations/root_repaired_candidate_authentication','actual_operations/root_repaired_candidate_authentication_corrected',
    'actual_operations/v2_checkpoint_remote','actual_operations/record_round1_repair_disposition','actual_operations/checkpoint_round1_repair_disposition']:
    for f in (A/n).rglob('*'):
        if f.is_file() and not f.is_symlink():paths.add(str(f.relative_to(C)))
for n in ['RECEIPT.json','PROCESS_JOURNAL.json']:paths.add(str((A/'actual_checkpoints/round1_repair_disposition'/n).relative_to(C)))
dump(A/'v2_checkpoint_selection.json',{'paths':sorted(paths),
 'private_fixture_scope':'Full2030-file preparation inventory and adversarial fixture copies remain local and authenticated; public sources/archive and actual receipts are committed. Source scripts recreate fixtures.'})
print(json.dumps({'UTC':utc,'PID':os.getpid(),'workflow_percent':65,'selected_paths':len(paths),'publication_ready':False}))
