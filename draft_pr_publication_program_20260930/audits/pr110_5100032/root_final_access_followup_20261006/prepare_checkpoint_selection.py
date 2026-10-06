"""Select only this bounded access follow-up and public execution metadata."""
from pathlib import Path
import datetime, hashlib, json, os

D = Path(__file__).resolve().parent
A = D.parent
P = A.parents[1]
C = P.parent
selection = D / 'CHECKPOINT_SELECTION.json'
private_stdout = A / 'actual_operations/root_access_followup_publisher_html_diagnostic/stdout.bin'
paths = [p for p in D.iterdir() if p.is_file()]
paths += [selection, A / '.gitignore', A / 'RESEARCH_LOG.md',
          P / 'CURRENT_PROGRESS.json', P / 'CURRENT_PROGRESS.md', P / 'RESEARCH_LOG.md']
labels = [
    'root_access_followup_crossref_metadata',
    'root_access_followup_openalex_metadata',
    'root_access_followup_semanticscholar_metadata',
    'root_access_followup_crossref_fulltext_html',
    'root_access_followup_publisher_html_diagnostic',
    'root_access_followup_publisher_public_Fig6',
    'root_access_followup_finalization',
    'root_access_followup_archive_completed_checkpoint',
    'root_access_followup_prepare_checkpoint_selection',
]
for label in labels:
    for name in ['started.json', 'execution.json', 'stdout.bin', 'stderr.bin']:
        p = A / 'actual_operations' / label / name
        if p != private_stdout:
            paths.append(p)
relative = sorted({str(p.relative_to(C)) for p in paths})
assert not any('/private_sources/' in p for p in relative)
assert str(private_stdout.relative_to(C)) not in relative
assert not any('/actual_checkpoints/' in p for p in relative)
record = {
    'schema': 'pr110-bounded-access-followup-checkpoint-selection/v1',
    'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actual_operator_PID': os.getpid(),
    'paths': relative,
    'copyrighted_preview_stdout_excluded': True,
    'prior_completed_execution_envelope_preserved_as_byte_checked_zip': True,
    'priority_or_publication_clearance': False,
    'source_math_percent': 100,
    'selected_candidate_priority_work_percent': 90,
    'workflow_percent': 30,
    'publication_percent': 0,
}
selection.write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({k: v for k, v in record.items() if k != 'paths'}))
print(json.dumps({'selected_path_count': len(relative), 'selection_sha256': hashlib.sha256(selection.read_bytes()).hexdigest()}))
