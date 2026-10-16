from pathlib import Path
import hashlib,json,datetime
D=Path(__file__).resolve().parent;P=D.parents[2];C=D/'corrected_packet';m=json.loads((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_text());plan=json.loads((D/'PROPOSED_NATIVE_CHANGES.json').read_text())
assert m['archive_files']==20 and len(m['files'])==35==plan['planned_source_files']
assert hashlib.sha256((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_bytes()).hexdigest()==plan['packet_manifest_sha256']
for row in m['files']:
 q=C/row['path'];b=q.read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
for name in ['MANIFEST.json','PUBLICATION_MANIFEST.json']:
 for row in json.loads((C/name).read_text())['files']:
  b=(C/row['path']).read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
a=plan['old_row'].split('|');b=plan['new_row'].split('|');assert len(a)==len(b)
assert [i for i,(x,y) in enumerate(zip(a,b)) if x!=y]==[8,11]
assert a[8].strip()=='claimed_solved' and b[8].strip()=='already_solved' and a[9]==b[9] and b[9].strip()=='1/5'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
result=dict(utc=now,status='PASS_PROPOSED_CREDIT_PACKET',files=35,archive_files=20,Queue_columns_changed_zero_based=[8,11],author_turns=1,mathematical_core_sha256=m['mathematical_core_sha256'],current_188_assertions_replayed=True,manifest_sha256=hashlib.sha256((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_bytes()).hexdigest(),native_plan_sha256=hashlib.sha256((D/'PROPOSED_NATIVE_CHANGES.json').read_bytes()).hexdigest(),native_changes_applied=False,final_independent_review_pending=True)
(D/'ROOT_PROPOSED_CREDIT_PACKET_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
state=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text());state.update(utc=now,completion_percent=65,stage='exact_prior_coverage_accepted_credited_packet_proposed_fresh_final_adversary_pending',priority_verdict='Exact prior numerical negative coverage PASS via two independent primary routes; bare mechanisms unresolved',proposed_classification='already_solved',native_status_unchanged='claimed_solved',native_repair_cleared=False)
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
s=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text());s.update(utc=now,case_completion_percent=65,current_stage=state['stage'],priority_verdict=state['priority_verdict'],priority_classification_repairs_required=['Credited already_solved for full literal numerical question; bare mechanisms unresolved'],preprint_preparation_cleared=False,preprint_upload_cleared=False);(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(s,indent=2)+'\n')
entry='\n## '+now+': PR212 exact prior coverage and proposed credit packet —65%\n\nTwo fresh priority families sealed and root-validated against full primary proofs. Both stdlib certificates replay exactly. GS2015+BS2017 cover exact singletonK44numeric triple; same-authorHKSSept2026 independently gives a coloredC4numeric counterexample. No bareAorB or exactprior tiedvariant/firsterrorrecognition claim. Proposed35-file creditpacket preserves20 originals and mathematicalSections2–7; currentauthor188checks reproduce with actualcontextualproofSHA. Exactone-rowQueue plan changes onlystatus/note, preservingauthor1/5. Fresh finalwholepacketadversary running; no nativecreditrepair/paper/deposit/tracker/merge/comment/closure yet. Counts42/19/19/0; goalactive/incomplete.\n'
for q in [D/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with q.open('a') as f:f.write(entry)
src=(D/'publish_mathematical_checkpoint.py').read_text().replace('MATHEMATICAL_CHECKPOINT_PUBLICATION_RECEIPT.json','PROPOSED_CREDIT_CHECKPOINT_PUBLICATION_RECEIPT.json')
pos=src.index("selection=P/'next_selection_after_pr214_20261015'")
extra='''for name in ['priority_classical_01','priority_author_update_01']:
    folder=D/name;manifest=json.loads((folder/'MANIFEST.json').read_text());paths.append(folder/'MANIFEST.json')
    for row in manifest['files']:
        q=folder/row.get('path',row.get('relative_path'));raw=q.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];paths.append(q)
    paths.append(folder/('SEAL.sha256' if name=='priority_classical_01' else 'FINAL_SEAL.json'))
for row in json.loads((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_text())['files']:
    q=D/'corrected_packet'/row['path'];assert hashlib.sha256(q.read_bytes()).hexdigest()==row['sha256'];paths.append(q)
paths += [q for q in (D/'root_priority_replays').rglob('*') if q.is_file()]
'''
src=src[:pos]+extra+src[pos:]
src=src.replace('Checkpoint PR212 at35%: three independent mathematical-source families verified; priority audit in progress','Checkpoint PR212 at65%: exact prior coverage and reviewable credit correction; fresh final adversary pending').replace('case_completion_percent=35','case_completion_percent=65')
(D/'publish_proposed_credit_checkpoint.py').write_text(src)
print(json.dumps(result,indent=2))
