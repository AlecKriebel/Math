from pathlib import Path
import json, hashlib

A = Path(__file__).resolve().parent
C = A.parents[2]
paths = []
def add(p):
    if not p.is_file() or p.is_symlink():
        raise RuntimeError('Missing or symbolic selected file: '+str(p))
    paths.append(str(p.relative_to(C)))
def tree(rel):
    for p in sorted((A/rel).rglob('*')):
        if p.is_file(): add(p)
for rel in ['credited_verification_candidate_v2', 'root_credited_candidate_reproduction_20261006', 'root_priority_evidence_authentication_20261006']:
    tree(rel)
for rel in ['prepare_credited_candidate.py','reproduce_credited_candidate.py','authenticate_priority_family.py','record_priority_adjudication.py','ROOT_CREDITED_CANDIDATE_PREPARATION_20261006.json','ROOT_PRIORITY_ADJUDICATION_20261006.json','RESEARCH_LOG.md','prepare_priority_checkpoint.py']:
    add(A/rel)
for rel, names in {
 'priority_question_history_20261006':['CLOSED_MANIFEST.json','SOURCE_REGISTER.json','REPORT.md','VERDICT.json','RESEARCH_LOG.md','SEARCH_HYPOTHESES.md','OWN_ANALYSIS.md','SEARCH_EVENT_INDEX.json','PAGE_VISUAL_CHECK.json','CLOSURE_CHECK.json','fetch_primary_sources.py','close_audit.py'],
 'priority_linear_contact_mechanism_20261006':['REPORT.md','VERDICT.json','RESEARCH_LOG.md','INITIAL_HYPOTHESES.md','SEARCH_PROTOCOL.md','SOURCE_CATALOG.json','CLOSED_SHA256_MANIFEST.json','VALIDATION_CLOSE.json','HTTP_PROCESS_RECORDS.json','HTTP_PROCESS_RECORDS_02.json','HTTP_PROCESS_RECORDS_03.json','RENDER_PROCESS_RECORDS.json','fetch_sources.py','fetch_more_sources.py','fetch_priority_followups.py','build_source_catalog.py','render_pinned_pages.py','close_manifest.py'],
 'priority_covering_interpretation_adversary_20261006':['BORROWED_INPUT_HASHES.json','DK2012_WEB_READ_SCOPE.json','VALIDATION_CHECKS.json','MANIFEST.sha256','MANIFEST.json','RENDER_PROCESS_RECORDS.json','PRIMARY_SOURCE_READ_SCOPE.md','REPORT.md','VERDICT.json','RESEARCH_LOG.md','EXECUTION_RECORDS.json','EXACT_COVERING_TABLE.md','INITIAL_HYPOTHESES.md','OWN_ANALYSIS.md']
}.items():
    for name in names: add(A/rel/name)
for p in sorted((A/'priority_question_history_20261006/new_primary_sources').glob('*.receipt.json')):
    add(p)
for label in ['authenticate_priority_history','authenticate_priority_mechanism','authenticate_priority_mechanism_v2','authenticate_priority_covering','prepare_credited_candidate','reproduce_credited_candidate','record_priority_adjudication','checkpoint_priority_start']:
    tree('actual_operations/'+label)
for name in ['RECEIPT.json','PROCESS_JOURNAL.json']:
    add(A/'actual_checkpoints/priority_start'/name)
add(C/'draft_pr_publication_program_20260930/CURRENT_PROGRESS.json')
selection=A/'PRIORITY_ADJUDICATION_CHECKPOINT_SELECTION.json'
paths.append(str(selection.relative_to(C)))
paths=sorted(set(paths))
for rel in paths:
    if '/contingent_credited_note_v1/' in rel or rel.endswith(('.pdf','.png','.txt','.html')) or '/WEB_' in rel or '/source_pages_' in rel or '/search_' in rel:
        raise RuntimeError('Private or active evidence included: '+rel)
selection.write_text(json.dumps({'schema':'explicit-pr97-priority-checkpoint-selection/v1','scope':'Root-authenticated bounded priority, credited proof and reproduction; private copyrighted source bodies and active package excluded.','paths':paths},indent=2)+'\n')
print(json.dumps({'selection':str(selection),'paths':len(paths),'bytes':sum((C/p).stat().st_size for p in paths),'selection_sha256':hashlib.sha256(selection.read_bytes()).hexdigest()}))
