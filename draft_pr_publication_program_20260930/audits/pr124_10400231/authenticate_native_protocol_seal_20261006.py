"""Full-body authentication of sealed independent protocol evidence, read-only."""
from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent;F=A/'native_published_obstruction_protocol_adversary_20261006';C=A.parents[2]
def req(v,s):
 if not v:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
expected={'REPORT.md':'50dede228eb2fa0f654c6625040608abf0ebbf0d9e0a5e5e1a32c74e4d88ea43','RESULT.json':'7a6c01d9261d28e6cc1172527547c9c3fee0041485b1f0fd86e75eb29b3de7c7','INPUT_HASHES.json':'6100429345682db0a20a025461620093eba065d1dabaeba5b8af4a6b1a7c2367','PUBLIC_MANIFEST.json':'040172226c067c4bae60105ff3459daf36fe97243fca8b4171e878b762ba4577','SEAL.json':'3525b5bd63fbb3297c6bf8e8c0e29af580fba4170b11138b952f85d3b17165f4'}
for n,h in expected.items():req(sha((F/n).read_bytes())==h,'Independent final pin '+n)
manifest=load(F/'PUBLIC_MANIFEST.json');result=load(F/'RESULT.json');seal=load(F/'SEAL.json')
req(result['verdict']=='PASS' and seal['verdict']=='PASS' and not result['global_corrections_required'],'Clean exact V2')
req(result['new_central_proof_search_turns']==0 and not result['operational_mutation_authorization'],'Validation only')
members=[]
for item in manifest['members']:
 p=F/item['path'];b=p.read_bytes();req(len(b)==item['bytes'] and sha(b)==item['sha256'],'Sealed public member')
 members.append({'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha(b)})
for name in ['PUBLIC_MANIFEST.json','SEAL.json']:
 item=pin(F/name);item['path']=str((F/name).relative_to(A));members.append(item)
inputs=load(F/'INPUT_HASHES.json')['inputs'];verified=[]
for item in inputs:
 p=Path(item['path']);b=p.read_bytes();req(len(b)==item['bytes'] and sha(b)==item['sha256'],'Full current input '+str(p));verified.append(item)
operators=load(F/'UNEXECUTED_OPERATOR_PINS.json')['operators']
for item in operators:
 b=Path(item['path']).read_bytes();req(len(b)==item['bytes'] and sha(b)==item['sha256'],'Unexecuted operator changed')
prep_path=A/result['exact_reviewed_preparation'];req(sha(prep_path.read_bytes())==result['exact_reviewed_preparation_sha256'],'V2 preparation pin')
req(len(members)==24 and len(inputs)==237 and len(operators)==5,'Exact reviewed cardinality')
record={'schema':'pr124-root-native-protocol-full-body-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'all24_public_bodies_verified':True,'all237_current_input_bodies_verified':True,'all5_unexecuted_operator_bodies_verified':True,'public_members':members,'current_inputs':verified,'V1_failure_and_locator_finding_preserved':True,'V2_receipt_sha256':result['exact_reviewed_preparation_sha256'],'shared_native_index_Git_service_mutations':False,'new_central_proof_search_turns':0}
out=A/'ROOT_NATIVE_PROTOCOL_AUTHENTICATION_20261006.json';req(not out.exists(),'Authenticate once');dump(out,record)
ready={'schema':'pr124-root-exact-native-protocol-ready/v1','UTC':record['UTC'],'actual_operator_PID':os.getpid(),'fresh_protocol_PASS':True,'protocol_report':str((F/'REPORT.md').relative_to(A)),'protocol_report_sha256':expected['REPORT.md'],'sealed_protocol_members':members,'full_body_authentication':str(out.relative_to(A)),'full_body_authentication_sha256':sha(out.read_bytes()),'exact_prepared_receipt':str(prep_path.relative_to(A)),'exact_prepared_receipt_sha256':result['exact_reviewed_preparation_sha256'],'base_commit':result['base_commit'],'native_status':'already_solved','native_status_scoped_to_old_published_content':True,'express_historical_refutation_established':False,'native_export_performed':False,'fresh_concrete_writer_handoff_still_required':True,'original_budget':'2/5','new_central_proof_search_turns':0,'publication_authorization':False}
dump(A/'ROOT_NATIVE_PUBLISHED_OBSTRUCTION_PROTOCOL_READY_20261006.json',ready)
print(json.dumps({'UTC':record['UTC'],'actual_operator_PID':os.getpid(),'public':len(members),'inputs':len(inputs),'operators':len(operators),'fresh_protocol_PASS':True,'shared_mutations':False},sort_keys=True))
