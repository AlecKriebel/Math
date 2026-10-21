from pathlib import Path
import json
D=Path(__file__).resolve().parent;A=D.parent;P=A.parents[1];C=P.parent
paths=[p for p in D.iterdir() if p.is_file()]
paths += [p for p in (A/'m1_final_journal_adversary_20261006').iterdir() if p.is_file()]
paths += [D/'CHECKPOINT_SELECTION.json',A/'ROOT_M1_FINAL_COMPARISON_AUTHENTICATION_20261006.json',A/'ROOT_PRIORITY_CLEARANCE_AFTER_M1_20261006.json',A/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.json',P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md']
labels=['m1_supplied_source_live_PR110_20261006','m1_supplied_final_ingestion_20261006','m1_final_text_extract_20261006','m1_final_page_render_20261006','m1_precursor_text_extract_20261006','m1_independent_root_replay_normal_20261006','m1_independent_root_replay_optimized_20261006','m1_root_gate_closure_20261006']
for label in labels:paths += [p for p in (A/'actual_operations'/label).iterdir() if p.is_file()]
r=sorted({str(p.relative_to(C)) for p in paths})
if any('/private_sources/' in p or '/publication_package_v1/' in p for p in r):raise RuntimeError('scope')
(D/'CHECKPOINT_SELECTION.json').write_text(json.dumps({'paths':r,'workflow_percent':35,'publication_percent':0,'private_primary_bodies_excluded':True},indent=2)+'\n')
print(json.dumps({'selected_public_files':len(r),'workflow_percent':35,'publication_percent':0}))
