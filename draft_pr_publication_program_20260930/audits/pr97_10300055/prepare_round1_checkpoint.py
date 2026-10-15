from pathlib import Path
import json

A=Path(__file__).resolve().parent;C=A.parents[2]
D=A/'whole_package_round1_20261006';paths=[]
def add(p):
    if not p.is_file() or p.is_symlink():raise RuntimeError('Invalid selected file '+str(p))
    paths.append(p.relative_to(C).as_posix())
r=json.loads((D/'CLOSED_EVIDENCE_MANIFEST.json').read_text())
private_source_prefixes=('runs/DR_','runs/KMNW_','runs/calegari_','runs/vogel2011_','runs/vogel2016_')
for row in r['own_files']:
    rel=row['path']
    if rel.startswith(private_source_prefixes) or '/package/' in rel:continue
    add(D/rel)
add(D/'CLOSED_EVIDENCE_MANIFEST.json')
for name in ['authenticate_whole_package_review.py','RESEARCH_LOG.md','prepare_round1_checkpoint.py']:
    add(A/name)
add(A/'root_whole_package_review_authentication_20261006/whole_package_round1_20261006.json')
for label in ['authenticate_whole_package_round1','checkpoint_prepared_package']:
    for p in sorted((A/'actual_operations'/label).rglob('*')):
        if p.is_file():add(p)
for name in ['RECEIPT.json','PROCESS_JOURNAL.json']:
    add(A/'actual_checkpoints/prepared_package'/name)
add(C/'draft_pr_publication_program_20260930/CURRENT_PROGRESS.json')
selection=A/'ROUND1_REPAIR_CHECKPOINT_SELECTION.json';paths.append(selection.relative_to(C).as_posix())
selection.write_text(json.dumps({'schema':'explicit-pr97-round1-repair-checkpoint-selection/v1','scope':'Closed fresh review, mathematical reconstruction, wrapper falsifications and actual receipts; third-party page extracts, controlled live link fixtures, duplicate synthetic package bodies and active v2 repair folder remain private/excluded.','paths':sorted(set(paths))},indent=2)+'\n')
print(json.dumps({'paths':len(set(paths)),'bytes':sum((C/p).stat().st_size for p in set(paths)),'review':'closed_repairs_required','publication_authorized':False}))
