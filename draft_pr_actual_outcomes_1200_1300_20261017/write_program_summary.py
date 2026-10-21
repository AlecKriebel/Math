#!/usr/bin/env python3
"""Render this shard's own verified publication register from its explicit state."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
state=json.loads((ROOT/'PROGRAM_STATE.json').read_text())
eligible=[1205,1211,1216,1225,1241,1261,1262,1268,1271,1274,1280,1283]
if state['eligible_prs']!=eligible or len(set(state['completed_prs']))!=len(state['completed_prs']):
 raise RuntimeError('Explicit scope or completed inventory differs')
pubs={row['pr']:row for row in state['publications']}
if set(pubs)!=set(state['completed_prs']):raise RuntimeError('Publication/completion inventory differs')
for pr,row in pubs.items():
 if row.get('completion_estimate_percent')!=100 or not row.get('doi_url','').startswith('https://doi.org/10.5281/zenodo.') or not row.get('merge_commit'):
  raise RuntimeError('Incomplete publication row '+str(pr))
complete=state.get('status')=='complete'
if complete and (set(pubs)!=set(eligible) or state.get('current_pr') is not None):raise RuntimeError('Cannot report incomplete shard as complete')
text='# Actual PR outcomes: #1200–#1300\n\n'
text+='The human superseded the stale QUEUE.md gate: admission uses an explicit full solution of the original target in each actual PR outcome. Partial, unsolved, conditional-only and recorded prior-result outcomes are excluded from mathematical review and publication. Two initial readers and a fresh global eligibility adversary checked the scope; twelve claims were admitted and 89 PRs skipped.\n\n'
text+=('All twelve admitted claims are complete. Each has rigorous mathematical verification, a bounded priority audit with concrete prior credit, a submission-ready preprint and verification package, sequential distinct fresh whole-package adversaries, a published Zenodo record, an exact unique tracker row and a verified expected-head merge. The final all101-PR metadata refresh is reconciled.\n\n' if complete else str(len(pubs))+' of twelve admitted claims are complete. Current PR: '+str(state.get('current_pr'))+'. Current stage: '+state.get('current_pr_stage','')+'. Overall estimate: '+str(state['completion_estimate_percent'])+'%. The publication register below contains completed, verified cases only.\n\n')
text+='The notes give the precise mathematical conclusions and literature qualifications. They make no firstness or current-worldwide-openness claim. AI tools were used extensively; the manuscripts are unrefereed, without external human or formal certification.\n\n'
text+='| PR | Problem | Published preprint and verification package | Tracker row |\n|---|---|---|---|\n'
for pr in eligible:
 if pr not in pubs:continue
 r=pubs[pr];text+='| [#'+str(pr)+'](https://github.com/AlecKriebel/Math/pull/'+str(pr)+') | '+str(r['problem_id'])+' | ['+r['doi']+']('+r['doi_url']+') | '+r['tracker_range']+' |\n'
text+='\n[PROGRAM_STATE.json](PROGRAM_STATE.json) records dispositions and immutable merge identities; [RESEARCH_LOG.md](RESEARCH_LOG.md) records checkpoints and estimates. Each audits/pr... folder retains its own original/current editions, proofs, source/access receipts, independently sealed reviews, exact publication records and postmerge checks. The initial eligibility files remain immutable historical scope evidence.\n\n'
text+='Work stays on main. Narrow regular pushes preserve other remote root entries and leave the shared checkout/index untouched. Third-party primary bodies, extracts, renders and raw retrieval data remain private review inputs. No outside individual is contacted, no outreach is prepared, and no GitHub release is created. The earlier queue-only checkpoint is preserved as superseded historical evidence.\n'
(ROOT/'README.md').write_text(text)
print('Updated own publication register: '+str(len(pubs))+' completed; status='+state['status'])
