"""Read-only audit of retained final-source controls; no fixture rerun or service call."""
from pathlib import Path
import json,hashlib,gzip,base64,copy
O=Path(__file__).resolve().parent
SOURCE='5f2a18359d2006783b20650584c2f4560b915f2907c6129b1db4c49488f224c8'
SPECS=[('CONTROL_RESULTS04.json',24),('CONTROL_RESULTS05.json',12),('CONTROL_RESULTS06.json',4),('CONTROL_RESULTS07.json',5)]
MODES='positive2 positive3 transport_applied transport_not_applied binary_reply empty_reply nonzero_reply contradictory_reply false_activation false_acceptance numeric_acceptance boolean_row_count conflated_roles expired missing_semantic_key alternate_case boolean_gid wrong_plan_pin missing_independent partial_existing complete_existing no_capacity formula_drift old43_type row_order raw_unknown metadata_drift owned_boolean_id owned_duplicate_page owned_pass_drift owned_new_alias public_body_drift marker_authority marker_gate marker_history marker_intent_age marker_source marker_input direct_edge_authority direct_edge_expiry candidate_authority candidate_history candidate_source postwrite_authority postwrite_owned_alias'.split()
SUCCESS={'positive2','positive3','transport_applied','binary_reply','empty_reply','nonzero_reply','complete_existing'}
ONE=set(MODES[:8]+['old43_type','row_order','raw_unknown','metadata_drift','candidate_authority','candidate_history','candidate_source','postwrite_authority','postwrite_owned_alias'])
ERRORS={
 'transport_not_applied':'Exact full43 typed prefix plus one ordered batch','contradictory_reply':'Contradictory parsed reply',
 'false_activation':'Activation is not affirmative literal true','false_acceptance':'Exact independent/root action role absent','numeric_acceptance':'Exact independent/root action role absent','boolean_row_count':'Typed review action scope','conflated_roles':'Wrong or conflated review role','expired':'Authority expired','missing_semantic_key':'Every exact semantic/literal decision','alternate_case':'Activation fixed target/SAMECASE drift','boolean_gid':'Activation fixed target/SAMECASE drift','wrong_plan_pin':'Activation exact source/plan/gate binding','missing_independent':'FileNotFoundError','partial_existing':'Partial existing batch','no_capacity':'Allocated grid capacity insufficient','formula_drift':'Complete typed VALUE/FORMULA response mismatch','old43_type':'Exact full43 typed prefix plus one ordered batch','row_order':'Exact full43 typed prefix plus one ordered batch','raw_unknown':'Unknown full raw response/range key changed','metadata_drift':'Full metadata changed','owned_boolean_id':'Full typed owned record','owned_duplicate_page':'Repeated owned ID across pages','owned_pass_drift':'Complete owned passes drift','owned_new_alias':'New/changed complete matching owned carrier forPR1263','public_body_drift':'Full typed publication body changed','marker_authority':'Externally pinned authority/input bytes changed','marker_gate':'Externally pinned authority/input bytes changed','marker_history':'Durable exact history changed: WRITE_ATTEMPTED.json','marker_intent_age':'Durable intent expired','marker_source':'Source/data buffer drift protocol.py','marker_input':'Source/data buffer drift PROPOSAL.json','direct_edge_authority':'Exact full43 typed prefix plus one ordered batch','direct_edge_expiry':'Exact full43 typed prefix plus one ordered batch','candidate_authority':'Externally pinned authority/input bytes changed','candidate_history':'Durable exact history changed: VERIFIED.json','candidate_source':'Source/data buffer drift protocol.py','postwrite_authority':'Externally pinned authority/input bytes changed','postwrite_owned_alias':'New/changed complete matching owned carrier forPR1270'}
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def load_cas():
    p=O/'cas_custody.py';ns={'__file__':str(p),'__name__':'_readonly_controls_cas'};exec(compile(p.read_bytes(),str(p),'exec',optimize=0),ns);return ns

def audit():
    C=load_cas();allrows=[];pins=[];rows=json.loads((O/'PROPOSAL.json').read_bytes())['items'];literal=[i['row']for i in rows]
    for name,count in SPECS:
        raw=(O/name).read_bytes();v=json.loads(raw);assert v['source_manifest_sha256']==SOURCE and v['real_service_effects']==0 and v['fake_service_only']is True
        chosen=v['controls'][:count];assert len(chosen)==count;pins.append({'path':name,'sha256':sha(raw),'selected_prefix_count':count});allrows+=chosen
    assert [r['mode']for r in allrows]==MODES
    for r in allrows:
        mode=r['mode'];assert r['passed']is True and type(r['process_delegate_calls'])is int and r['process_delegate_calls']==int(mode in ONE)
        assert r['expected_success']is(mode in SUCCESS)
        if mode in SUCCESS:
            assert r['error']is None;v=r['receipt']
            if mode=='complete_existing':assert v['status']=='EXACT_EXISTING_BATCH_NOOP' and v['writes']==0 and len(v['positions'])==34
            else:assert v['status']=='VERIFIED_EXACT_ONE_ATOMIC_EXISTING_PUBLICATION_BATCH' and v['new_rows']==34 and v['new_publications']==0 and v['attempts']==1 and v['old43_rows_preserved']==3 and v['after_rows']==37 and v['action_authority']is False
        else:assert ERRORS[mode]in r['error']and'RESOURCE_'not in r['error']and'LIVE_CAPABILITY_BLOCKED'not in r['error']and r['receipt']is None
        ref=r['custody'];raw=C['exact_compressed'](ref['path']);assert sha(raw)==ref['sha256'];inv=json.loads(gzip.decompress(raw));entries=inv['entries']
        def read(leaf):
            e=entries[leaf];b=C['raw'](e['capture']);assert len(b)==e['bytes']and sha(b)==e['sha256'];return json.loads(b)
        if 'original_case/INTENT.json'in entries:
            request=read('original_case/INTENT.json')['request'];assert list(request)==['requests']and len(request['requests'])==1
            ac=request['requests'][0]['appendCells'];assert ac['sheetId']==1254632077 and ac['fields']=='userEnteredValue'
            expected=[{'values':[{'userEnteredValue':{'stringValue':c}}for c in row]}for row in literal];assert canonical(ac['rows'])==canonical(expected)
        if mode in ['direct_edge_authority','direct_edge_expiry']:
            error=read('original_case/TRANSPORT.json')['error'];assert ('Externally pinned authority/input bytes changed'if mode.endswith('authority')else'Native/source guard expired')in error
            assert 'original_case/ORIGINAL_APPEND_TRANSPORT.json'not in entries
        if mode in ONE:
            transport=read('original_case/ORIGINAL_APPEND_TRANSPORT.json');stdout=base64.b64decode(transport['stdout_base64']);stderr=base64.b64decode(transport['stderr_base64']);assert isinstance(stdout,bytes)and isinstance(stderr,bytes)
        if mode in ['marker_source','marker_input','candidate_source']:
            fault=read('FILE_READ_FAULT.json');assert 'no source/data file mutation'in fault['mechanism']
        if r['same_CASE_retry']is not None:assert r['same_CASE_retry']!='UNEXPECTED_SUCCESS'
        rec=r['GET_only_reconciliation'];assert rec is None or rec['writes']==0
    summary={'source_manifest_sha256':SOURCE,'unique_controls':45,'ordered_modes':MODES,'all_intended_results':True,'one_atomic_request_rows':34,'new_publications':0,'maximum_process_delegate_calls':1,'real_service_effects':0,'selection':pins,'resource_interrupted_trials_excluded':True,'same_source_across_selected_runs':True,'source_fault_last_three_use_read_seam':True,'readiness':False}
    return summary

def verify_expected(actual,envelope):
    assert set(envelope)=={'summary','summary_sha256'}and sha(canonical(envelope['summary']))==envelope['summary_sha256'],'Expected summary hash mismatch'
    assert canonical(envelope['summary'])==canonical(actual),'Self-consistent false expected summary rejected'

if __name__=='__main__':
    result=audit();envelope=json.loads((O/'FINAL_CONTROL_ACCOUNTING.json').read_bytes());verify_expected(result,envelope);print(json.dumps({'controls':45,'all_intended_results':True,'source_manifest_sha256':SOURCE,'readiness':False}))
