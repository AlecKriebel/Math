"""Privately reproduce the fresh actual-head gate without touching sealed files."""
from pathlib import Path
import datetime, hashlib, json, subprocess
A=Path(__file__).resolve().parent
D=A/'clean_corrected_final_adversary'
C=A/'tmp/root_clean_final_gate'
assert not C.exists(), 'Preserve previous runs.'
C.mkdir(parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads((D/'public_evidence_manifest.json').read_text())
assert sha((D/'public_evidence_manifest.json').read_bytes())=='160f8e62a2f17031a76a7d69af3a71077f6ba0abb796bd0fd602c744e2b90594'
before={str(D/'public_evidence_manifest.json'):sha((D/'public_evidence_manifest.json').read_bytes())}
def bind(p,e):
 b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],str(p);return b
for e in m['files']:
 assert not {'raw_sources','tmp','private'} & set(Path(e['path']).parts)
 p=D/e['path'];b=bind(p,e);before[str(p)]=sha(b)
 q=C/e['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
source=json.loads((D/'private_source_evidence_manifest.json').read_text())
for e in source['files']:
 b=bind(D/e['private_path'],e);q=C/e['private_path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
seal_instances=0
for f in ['independent_pre_candidate_seal.json','mathematical_verdict_seal.json','final_verdict_seal.json']:
 for e in json.loads((D/f).read_text())['files']:
  bind(D/e['path'],e);seal_instances+=1
src=(D/'verify_final_git_binding.py').read_text()
old='B = P.parent'
assert src.count(old)==1
# Only the immutable input root changes. P remains the private output copy;
# all object/queue/source/math/seal/runtime/live API assertions remain verbatim.
(C/'verify_final_git_binding.py').write_text(src.replace(old,'B = Path('+repr(str(A))+')'))
PY=A.parent/'pr378_30004322/sources_effective_review/private_runtime/bin/python'
r=subprocess.run([str(PY),'-B',str(C/'verify_final_git_binding.py')],capture_output=True)
(A/'root_clean_final_gate.stdout').write_bytes(r.stdout);(A/'root_clean_final_gate.stderr').write_bytes(r.stderr)
assert r.returncode==0 and not r.stderr,(r.returncode,r.stderr.decode())
j=json.loads(r.stdout);expected=json.loads((D/'final_actual_head_receipt.json').read_text())
for key in ['started_utc','completed_utc']:j.pop(key);expected.pop(key)
assert j==expected
for e in j['replays']:
 stem='final_'+e['script'].replace('/','_').removesuffix('.py')
 assert (C/(stem+'.stdout')).read_bytes()==(D/(stem+'.stdout')).read_bytes()
 assert not (C/(stem+'.stderr')).read_bytes()
assert all(sha(Path(p).read_bytes())==h for p,h in before.items())
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','workflow_percent':98,'head':j['head'],'base':j['base'],'public_files':len(m['files']),'public_manifest_sha256':sha((D/'public_evidence_manifest.json').read_bytes()),'all_seal_instances':seal_instances,'private_source_bindings':len(source['files']),'full_final_receipt_equal_except_two_utc_fields':True,'all_five_runtime_full_streams_byte_exact':True,'all26_actual_objects':True,'all25_target_files_equal_deeply_reviewed_packet':True,'queue_only_own_status_token':True,'live_API_commit_tree_parents_body_and_remote_refs':True,'sealed_reviewer_files_unchanged':True,'only_private_verifier_input_root_redirected':True,'source_first_mathematics_previously_root_reproduced':'root_clean_mathematical_reproduction_receipt.json','actual_merge_pending':True,'no_new_solution_no_paper_no_doi':True}
(A/'root_clean_final_gate_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
