from pathlib import Path
import hashlib,json,datetime,re
D=Path(__file__).resolve().parent;P=D.parents[2];ROOT=P.parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
u=json.loads((D/'private_upstream/complete_record.json').read_text());p=u['record'];r=u['report']
related=ROOT/'unsolved_math_prioritization/review_v2/related_target_groups.json'
a=json.loads(related.read_text());matches=[]
def walk(v,path=''):
 if isinstance(v,dict):
  for k,x in v.items():
   if k in ('30005310','OWR-11695865-009'):matches.append(path+'/'+k)
   walk(x,path+'/'+k)
 elif isinstance(v,list):
  for i,x in enumerate(v):walk(x,path+'/'+str(i))
 elif str(v) in ('30005310','OWR-11695865-009'):matches.append(path)
walk(a)
assert not matches,matches
rec={'utc':now,'statement_hash':hashlib.sha256((p.get('statement') or '').encode()).hexdigest(),'review_hash':hashlib.sha256(json.dumps([p,r],sort_keys=True).encode()).hexdigest(),'hash_convention':'Exact queue.py score digest formulas; no module import or cache write','related_target_groups_sha256':hashlib.sha256(related.read_bytes()).hexdigest(),'exact_target_matches':matches,'upstream_report_empty_object':r=={},'submitted_prior_imported_report_null':'Historical no-prior-report marker; do not replace with fabricated earlier results'}
(D/'TARGET_PROVENANCE_HASHES.json').write_text(json.dumps(rec,indent=2)+'\n')
state=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text());state.update(utc=now,stage='original_exact_replays_complete_independent_mathematical_audit_in_progress',completion_percent=15,source_verdict='Source-first scoped numerical implication validated; bare mechanism conjecture not refuted',mathematical_verdict='Root reconstruction and 1996 submitted exact assertions pass; two independent mathematics families pending',priority_verdict='Not yet cleared; older exact bipartite theorem and September2026 same-author paper require full audit')
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
sel=P/'CURRENT_GOAL_SELECTION_20261013.json';s=json.loads(sel.read_text());s.update(utc=now,case_completion_percent=15,current_stage=state['stage'],source_verdict=state['source_verdict'],mathematical_verdict=state['mathematical_verdict'],priority_verdict=state['priority_verdict']);sel.write_text(json.dumps(s,indent=2)+'\n')
entry=f'''\n## {now}: PR212 exact replay/source checkpoint — 15%\n\nAll20 native attempt files frozen at c697b4a5cc62f3b8836d8c37d82b71a1d1c53fb7; exact current PR-head Queue claimed_solved. Full upstream record read through SQLite URI mode=ro and matched native source. Root independently reconstructed ideal dominance, full minors, open-set PD completion, one-observation likelihood ray and source-scope boundary before inherited reviews. Both programs replayed in isolated folders with byte-identical receipts:188+1808 exact assertions. Root read/rendered all four original contribution pages. New source-first adversary independently validates the scoped numerical counterexample,16 fresh exact checks, and warns that the bare SOS/intersection alternative remains unrefuted. Two materially independent mathematics reviews still pending. Primary search located a September2026 same-author preprint and an older explicit bipartite WMLT theorem; no priority or publication clearance. No paper/deposit/tracker/PR mutation. Counts42 completed/19 preprints/19 merges/0 pending rows; held293,292,280,239 unchanged. Goal active/incomplete.\n'''
with (D/'RESEARCH_LOG.md').open('a') as f:f.write(entry)
with (P/'RESEARCH_LOG.md').open('a') as f:f.write(entry)
src=(P/'audits/pr214_30005244/initial_review_20261015/publish_initial_checkpoint.py').read_text().replace('214','212').replace('30005244 / OWR-11101924-008','30005310 / OWR-11695865-009')
src=src.replace("assert json.loads((D/'ROOT_ORIGINAL_EXACT_REPLAY_ACCEPTANCE.json').read_text())['status']=='PASS'","assert all(x['semantic_exact_replay'] for x in json.loads((D/'ROOT_REPLAY_RECEIPT.json').read_text())['isolated_replays'])")
src=src.replace("selection=P/'next_selection_after_pr218_20261015'","review=D/'source_scope_adversary_01'\nmanifest=json.loads((review/'SAFE_AUTHORED_MANIFEST.json').read_text())\nfor row in manifest:\n    q=review/row['path'];raw=q.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']\n    paths.append(q)\npaths.append(review/'SAFE_AUTHORED_MANIFEST.json')\nselection=P/'next_selection_after_pr214_20261015'")
src=src.replace("old=P/'audits/pr218_30006020/initial_review_20261015'","old=P/'audits/pr214_30005244/initial_review_20261015'")
src=src.replace('counts=[41,18,18,0]','counts=[42,19,19,0]')
(D/'publish_initial_checkpoint.py').write_text(src)
print(json.dumps({'utc':now,'checkpoint_percent':15,'target_hashes':rec,'publishing_script_prepared':True},indent=2))
