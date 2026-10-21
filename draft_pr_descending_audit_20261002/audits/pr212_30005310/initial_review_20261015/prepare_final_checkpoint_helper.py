from pathlib import Path
D=Path(__file__).resolve().parent
s=(D/'publish_proposed_credit_checkpoint.py').read_text()
s=s.replace('PROPOSED_CREDIT_CHECKPOINT_PUBLICATION_RECEIPT.json','FINAL_DISPOSITION_PUBLICATION_RECEIPT.json')
a="intake=json.loads((D/'INTAKE.json').read_text());pr=api('GET','pulls/212')"
b="intake=json.loads((D/'INTAKE.json').read_text());repair=json.loads((D/'CLASSIFICATION_REPAIR_RECEIPT.json').read_text());assert repair['status']=='APPLIED_AND_VERIFIED';HEAD=repair['corrected_head'];pr=api('GET','pulls/212')"
assert a in s;s=s.replace(a,b)
s=s.replace("pr['head']['sha']==intake['head']","pr['head']['sha']==HEAD")
s=s.replace("'?ref='+intake['head']","'?ref='+HEAD")
s=s.replace("queue['sha']==intake['Queue_blob']","queue['sha']==json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text())['Queue_blob']")
s=s.replace("rows[0].split('|')[8].strip()=='claimed_solved'","rows[0].split('|')[8].strip()=='already_solved'")
pos=s.index("selection=P/'next_selection_after_pr214_20261015'")
extra='''accept=json.loads((D/'ROOT_FINAL_CREDIT_PACKET_ACCEPTANCE.json').read_text());assert accept['status']=='PASS' and accept['native_mutations_cleared']
assert json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())['completion_percent']==100
folder=D/'final_credit_packet_adversary_01';mf=folder/accept['reviewer_manifest_basename']
assert hashlib.sha256(mf.read_bytes()).hexdigest()==accept['reviewer_manifest_sha256']
manifest=json.loads(mf.read_text());paths.append(mf)
for row in manifest.get('files',manifest.get('safe_authored_files')):
    q=folder/row.get('path',row.get('relative_path'));raw=q.read_bytes()
    assert q.resolve().is_relative_to(folder.resolve()) and len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];paths.append(q)
if accept.get('reviewer_seal_basename'):paths.append(folder/accept['reviewer_seal_basename'])
'''
s=s[:pos]+extra+s[pos:]
s=s.replace('Checkpoint PR212 at65%: exact prior coverage and reviewable credit correction; fresh final adversary pending','Publish PR212 verified prior-credit correction; preserve complete evidence and skip corrected open draft')
s=s.replace('case_completion_percent=65,','case_completion_percent=100,completion_scope="Eligible-intake audit and historical credit disposition only",')
s=s.replace("original_PR_head_unchanged=intake['head']","reviewed_original_PR_head=intake['head'],corrected_PR_head_unchanged=HEAD")
(D/'publish_final_disposition.py').write_text(s)
print('Final checkpoint helper prepared only; requires completed verified correction.')
