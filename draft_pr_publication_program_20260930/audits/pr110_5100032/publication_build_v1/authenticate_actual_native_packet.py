#!/usr/bin/env python3
"""Root pure/full-body authentication of genuine packet; no native assessment."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sys,types
A=Path(__file__).resolve().parents[1];D=A/'native_execution_programs_v1';F=A/'native_actual_input_preparation_20261006/root_fresh_native_preflight_20261006/EXECUTION_INPUTS.json'
def mod(name,path):
 m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m;exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
p=mod('protocol',D/'protocol.py');w=mod('native_worker',D/'native_worker.py');r=mod('native_runner',D/'native_runner.py');raw=F.read_bytes();packet=p.loads(raw)
p.need(raw==p.canonical(packet),'Actual canonical packet');bodies={e['path']:w.read_file(A/e['path'],8*1024*1024,e) for e in packet['input_files']};inputs=p.Inputs(packet['input_files'],bodies)
original,source,prior=p.validate_original(packet['original'],inputs);doi,_,ze=p.publication(inputs.obj(packet['publication_receipt']),packet['package'],inputs);selected,se=p.sheet(inputs.obj(packet['sheet_receipt']),doi,source,ze,inputs)
pre=inputs.obj(packet['preflight_receipt']);p.need(pre['root_independently_authenticated_actual_preflight_processes'] is True and pre['main_parent']==packet['main_parent'],'Authentic root preflight')
inputs.read(packet['package']['effective_proof']);inputs.obj(packet['package']['transport_inventory_receipt'])
for contract in packet['service_process_contracts'].values():
 for spec in contract['program_inputs']:inputs.read(spec)
for spec in packet['checked_artifacts']:inputs.read(spec)
for name,spec in packet['attempt_offer_sources'].items():
 p.need(name.startswith('unsolved_math_prioritization/attempts/5100032/'),'Only exact target offers');inputs.read(spec)
inputs.finish();r.validate_runtime(packet['runtime'],w,p);w.limits_policy(packet['resources']);r.process_policy(packet['parent_policy'])
p.need(packet['identity']=={'PR':110,'id':p.K,'code':p.CODE,'original_head':p.HEAD,'review_hash':p.REVIEW,'statement_hash':p.STATEMENT,'dataset_revision':p.REV,'literal_status':'claimed_solved','turns_used':2,'new_central_proof_search_turns':0,'exact_claim':p.CLAIM},'Exact scientific identity')
p.need(set(packet['assessment_overlay'])<=p.ASSESSMENT_METADATA and packet['assessment_overlay']['original_budget']=='2/5' and packet['assessment_overlay']['new_central_proof_search_turns']==0,'No substantive score/effort mutation')
caps=w.derive_caps(packet['native_baseline'],packet['resources']);capacity=sum(caps.values())+sum(caps[n] for n in p.DERIVED)+sum(s['bytes'] for s in packet['attempt_offer_sources'].values())+max(caps.values())+2*1024*1024
p.need(capacity<=packet['parent_policy']['allocation_cap'],'Concrete sufficient allocation')
for label in ('root_fresh_native_preflight_20261006','root_actual_native_packet_20261006'):
 op=A/'actual_operations'/label;e=p.loads((op/'execution.json').read_bytes());p.need(e['exit_code']==0 and e['reaped'] is True,'Actual successful builder/preflight')
 for stream in ('stdout','stderr'):p.need(p.pin((op/e[stream]['path']).read_bytes())=={k:e[stream][k] for k in ('bytes','sha256')},'Actual full parent streams')
builder=p.loads((A/'actual_operations/root_actual_native_packet_20261006/stdout.bin').read_bytes());p.need(builder['sha256']==p.sha(raw) and builder['bytes']==len(raw) and builder['input_count']==len(bodies),'Genuine output custody')
root={'schema':'pr110-root-actual-native-packet-authentication/v1','UTC':datetime.now(timezone.utc).isoformat(),'actual_root_PID':os.getpid(),'packet':{'path':str(F.relative_to(A)),**p.pin(raw)},'main_parent':packet['main_parent'],'full_registered_inputs_authenticated_and_consumed':len(bodies),'original_files_byte_preserved':17,'nonempty_original_prior_preserved':True,'exact_scientific_identity_checked':True,'actual_publication_fullbody_protocol_pass':True,'actual_GWS_protocol_pass':True,'DOI':doi,'Sheet_range':selected,'current_runtime_graph_authenticated_without_retrospective_claim':True,'private_capacity_bytes':capacity,'original_effort':'2/5','new_central_proof_search_turns':0,'native_assess_executed':False,'fresh_adversary_and_root_commission_remaining':True,'workflow_percent':80}
(A/'ROOT_ACTUAL_NATIVE_PACKET_AUTHENTICATION_20261006.json').write_bytes(p.canonical(root));print(json.dumps(root))
