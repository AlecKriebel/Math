"""Fresh read-only resumption evidence after interrupted goal turn."""
from pathlib import Path
import datetime,hashlib,importlib.util,json
A=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('checkpoint190',A/'prepare_intake_checkpoint.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.m.m.TREE_CACHE_PATH=A/'RESUMPTION02_IMMUTABLE_TREE_CACHE.json'
tip=m.api('git/ref/heads/main')['object']['sha'];pr=m.api('pulls/190');j=json.loads(m.body_at(m.PREFIX+'CURRENT_PROGRESS.json',tip))
if pr['head']['sha']!=m.HEAD or pr['merged'] or pr['state']!='open':raise RuntimeError('Original state drift')
packet=json.loads((A/'publication_package_v1/FINAL_REVIEW_PACKET_MANIFEST.json').read_text())
for n,x in packet['payloads'].items():
 b=(A/'publication_package_v1'/n).read_bytes()
 if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256']:raise RuntimeError('Packet drift '+n)
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'previous_goal_turn_classification':'PROGRESS','new_evidence':'Actual successful primary DOI-version3file retrieval independently authenticates previous website hashes; required current wording repair identified. Gated repair/disposition scripts prepared but not executed.','main_observed':tip,'PR':190,'original_head':pr['head']['sha'],'state':pr['state'],'draft':pr['draft'],'merged':pr['merged'],'completed':j['fully_completed_count'],'published':j['published_count'],'current_PR':j['current_PR'],'current_case_percent':j.get('current_PR_workflow_percent'),'packet_v1_all_five_pins_unchanged':True,'prior_recovery_whole_reviewer':'Authoritatively absent from collaboration.list_agents on15October03:35; final report/seal absent, work preserved, not counted as completed review or approval.','current_new_whole_reviewer':'pr190_whole_package_review_01_final running; fresh source-first initial assessment sealed.','publication_ready':False,'goal_complete':False}
(A/'ROOT_RESUMPTION_REVALIDATION_20261015_02.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
