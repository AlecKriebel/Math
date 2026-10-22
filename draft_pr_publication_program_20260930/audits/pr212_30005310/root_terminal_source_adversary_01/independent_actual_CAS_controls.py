"""Independent actual-CAS PARSER challenges in an owned synthetic checkout.

The unchanged approved parser/strict JSON/file reads execute. Runtime facts,
Root envelopes, PID/session evidence and the sole comparison observer are
explicitly synthetic. No production Runtime/context/API/lock or action executes.
"""
from pathlib import Path
import copy,hashlib,json,tempfile,types,datetime

HERE=Path(__file__).resolve().parent
CASE=HERE.parent
DRIVER={'bytes':43897,'sha256':'16e5e3a15cc4cf34554aabf0b094b34996064c1abb05c008e26b47b00bf18ce8'}
MODEL={'bytes':33579,'sha256':'d8d749b9f45f24077668d60c916a431bf807f58df8189843f89c00026baca0f7'}

def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def load(name,path,raw):
    m=types.ModuleType(name);m.__file__=str(path)
    exec(compile(raw,str(path),'exec'),m.__dict__)
    return m

def main():
    raw=(CASE/'native_administrative_preparation_01/administrative_checkpoint.py').read_bytes()
    model=(CASE/'native_administrative_preparation_01/native212_model.py').read_bytes()
    assert pin(raw)==DRIVER and pin(model)==MODEL
    checks=[]
    with tempfile.TemporaryDirectory(prefix='_owned_actual_CAS_parser_',dir=HERE) as tmp:
        checkout=Path(tmp)/'checkout';a=checkout/'program/audits/pr212_30005310'
        b=a/'native_administrative_preparation_01';b.mkdir(parents=True)
        d=load('owned_actual_CAS_driver',b/'administrative_checkpoint.py',raw)
        h=load('owned_actual_CAS_model',b/'native212_model.py',model)
        n=0
        def put(value):
            nonlocal n
            n+=1;p=a/('synthetic_evidence_'+str(n)+'.json');body=d.enc(value)
            p.write_bytes(body);p.chmod(0o444)
            return {'path':str(p),**pin(body)}
        sp=DRIVER;sm={'bytes':22,'sha256':'a'*64};lp={'bytes':23,'sha256':'b'*64}
        lg={'bytes':24,'sha256':'c'*64};ap={'bytes':25,'sha256':'d'*64}
        rt=types.SimpleNamespace(h=h,seed=types.SimpleNamespace(source_pin=sp,source_manifest_pin=sm,
            manifest_pin=lp,logical_gate_pin=lg,s=types.SimpleNamespace(read_regular=d.read_regular)),
            admission_pin=ap,admission={'parent':'1'*40,'parent_tree':'2'*40,'candidate':'3'*40,'tree':'4'*40},
            overlay={'synthetic_'+str(x):b'fixture' for x in range(5)},m={'facts':h.phase_facts()})
        proof={'schema':'pr212-administrative-immutable-candidate-verification-v1','evidence_scope':d.IMMUTABLE_SCOPE,
            'protocol_pin':sp,'source_manifest_pin':sm,'admission_pin':ap,'logical_manifest_pin':lp,
            'logical_gate_pin':lg,'candidate':'3'*40,'tree':'4'*40,'parent':'1'*40,'parent_tree':'2'*40,
            'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,
            'selected_count':5,'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
            'mutable_Main_observed_or_spoofed':False,'actual_CAS_or_completion_inferred':False}
        precas={'schema':'pr212-root-administrative-preCAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'PR':212,'accepted':True,'protocol_pin':sp,'admission_pin':ap,'logical_manifest_pin':lp,
            'logical_gate_pin':lg,'candidate':'3'*40,'tree':'4'*40,'immutable_candidate_verification_accepted':True,
            'independent_GET_candidate_verification_accepted':True,'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY}
        ready={'schema':'pr212-administrative-locked-CAS-ready-v1',
            'evidence_scope':'HELD_LOCK_AND_DATED_FRESH_LEASE_NOT_CAS_SUCCESS','protocol_pin':sp,
            'admission_pin':ap,'parent':'1'*40,'candidate':'3'*40,'original_stable_lock_held':True,'guard_pid':12345}
        request={'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main',
            'expected_sha':'1'*40,'sha':'3'*40,'force':False}
        response={'isError':False,'structuredContent':{'success':True}}
        readback={'ref':'refs/heads/main','object':{'type':'commit','sha':'3'*40}}
        poll={'session_id':54321,'exit_code':None,'output':'synthetic running-session poll'}
        confirmation={'schema':'pr212-root-postCAS-same-live-guard-confirmation-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'accepted':True,'protocol_pin':sp,'admission_pin':ap,
            'same_session_live_poll_after_actual_MCP_and_readback_before_acceptance_and_ack':True,
            'original_lock_continuity_from_linear_held_source_and_same_live_session':True,
            'guard_pid':12345,'session_id':54321}
        acceptance={'schema':'pr212-root-administrative-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'PR':212,'accepted':True,'hostname':'github.com','repository_full_name':'AlecKriebel/Math',
            'protocol_pin':sp,'source_manifest_pin':sm,'admission_pin':ap,'logical_manifest_pin':lp,'logical_gate_pin':lg,
            'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,'facts':h.phase_facts(),
            'parent':'1'*40,'candidate':'3'*40,'tree':'4'*40,'actual_Root_MCP_CAS_performed':True,
            'actual_tool_success_and_readback_accepted':True,'original_lock_held_across_actual_Root_CAS':True,
            'unknown_outcome':False,'actual_MAIN_after_CAS':'3'*40}
        template={'proof1':proof,'proof2':proof,'precas':precas,'ready':ready,'request':request,'response':response,
            'readback':readback,'poll':poll,'confirmation':confirmation,'acceptance':acceptance}
        class Observer:
            def __init__(self,good=True):self.calls=[];self.good=good
            def __call__(self,method,path):
                self.calls.append((method,path))
                assert method=='GET' and path=='compare/'+'3'*40+'...'+'5'*40
                return {'status':'ahead','merge_base_commit':{'sha':('3' if self.good else '6')*40}}
        def execute(change=None,post=None,good_compare=True):
            values=copy.deepcopy(template)
            if change:change(values)
            refs={}
            for key in ('proof1','proof2','ready','request','response','readback','poll'):refs[key]=put(values[key])
            values['precas']['verification_reports']=[refs['proof1'],refs['proof2']]
            refs['precas']=put(values['precas'])
            rec={'method':'GET','path':'git/ref/heads/main','exit':0,'stdout_pin':{k:refs['readback'][k] for k in ('bytes','sha256')}}
            refs['readback_receipt']=put(rec)
            values['confirmation'].update(actual_lock_guard_ready_pin={k:refs['ready'][k] for k in ('bytes','sha256')},
                actual_tool_response_pin={k:refs['response'][k] for k in ('bytes','sha256')},
                actual_readback_response_pin={k:refs['readback'][k] for k in ('bytes','sha256')},
                actual_same_session_poll_response=refs['poll'])
            refs['confirmation']=put(values['confirmation'])
            values['acceptance'].update(preCAS_acceptance=refs['precas'],actual_lock_guard_ready=refs['ready'],
                actual_tool_request=refs['request'],actual_tool_response=refs['response'],actual_readback_response=refs['readback'],
                actual_readback_receipt=refs['readback_receipt'],post_CAS_same_live_guard_confirmation=refs['confirmation'])
            if post:post(values,refs)
            root=put(values['acceptance']);api=Observer(good_compare)
            return d.actual_cas(rt,root,api),api.calls
        got,calls=execute();assert got['candidate']=='3'*40 and not calls
        checks.append({'name':'real parser accepts coherent synthetic candidate readback','expected':'accept'})
        def mutation(key,field,value):return lambda v:v[key].__setitem__(field,value)
        cases=[
            ('CAS not performed','acceptance','actual_Root_MCP_CAS_performed',False),
            ('CAS bool numeric substitution','acceptance','actual_Root_MCP_CAS_performed',1),
            ('unknown outcome','acceptance','unknown_outcome',True),
            ('missing same original lock','acceptance','original_lock_held_across_actual_Root_CAS',False),
            ('false Root acceptance','acceptance','accepted',False),
            ('wrong PR','acceptance','PR',213),
            ('bool PR','acceptance','PR',True),
            ('wrong parent','acceptance','parent','7'*40),
            ('wrong candidate','acceptance','candidate','7'*40),
            ('wrong tree','acceptance','tree','7'*40),
            ('wrong scope','acceptance','evidence_scope','PLANNED'),
            ('tool false force','request','force',True),
            ('force numeric false','request','force',0),
            ('tool wrong expected parent','request','expected_sha','7'*40),
            ('tool wrong target','request','sha','7'*40),
            ('tool wrong ref','request','ref','heads/other'),
            ('tool wrong owner','request','owner','other'),
            ('tool isError','response','isError',True),
            ('tool numeric isError','response','isError',0),
            ('ready wrong scope','ready','evidence_scope','ACTUAL_ROOT_RECEIPT'),
            ('ready no lock','ready','original_stable_lock_held',False),
            ('ready bool PID','ready','guard_pid',True),
            ('confirmation wrong PID','confirmation','guard_pid',54321),
            ('confirmation no live poll','confirmation','same_session_live_poll_after_actual_MCP_and_readback_before_acceptance_and_ack',False),
            ('confirmation no continuity','confirmation','original_lock_continuity_from_linear_held_source_and_same_live_session',False),
            ('poll exited','poll','exit_code',0),
            ('poll bool session','poll','session_id',True),
            ('poll wrong session','poll','session_id',76543),
            ('poll output missing','poll','output',None),
            ('proof wrong selected count','proof1','selected_count',4),
            ('proof bool selected count','proof1','selected_count',True),
            ('proof ancestry inference','proof1','actual_CAS_or_completion_inferred',True),
            ('proof mutable Main spoof','proof2','mutable_Main_observed_or_spoofed',True),
            ('preCAS no independent proof','precas','independent_GET_candidate_verification_accepted',False),
            ('preCAS no immutable proof','precas','immutable_candidate_verification_accepted',False),
        ]
        for label,key,field,value in cases:
            try:execute(mutation(key,field,value))
            except (RuntimeError,KeyError,TypeError,ValueError):checks.append({'name':label,'expected':'refuse'})
            else:raise AssertionError('Accepted '+label)
        def descendant(v):
            v['readback']['object']['sha']='5'*40;v['acceptance']['actual_MAIN_after_CAS']='5'*40
        got,calls=execute(descendant);assert got['candidate']=='3'*40 and len(calls)==1
        checks.append({'name':'actual CAS candidate retained distinct from preserving descendant R','expected':'accept'})
        try:execute(descendant,good_compare=False)
        except RuntimeError:checks.append({'name':'unrelated readback is not actual CAS','expected':'refuse'})
        else:raise AssertionError('Unrelated descendant accepted')
        def corrupt_pin(v,refs):v['acceptance']['actual_tool_response']['sha256']='0'*64
        try:execute(post=corrupt_pin)
        except RuntimeError:checks.append({'name':'actual tool body pin changed','expected':'refuse'})
        else:raise AssertionError('Changed response pin accepted')
    out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':checks,'check_count':len(checks),
        'driver_pin':DRIVER,'model_pin':MODEL,'all_fixture_inputs_removed':True,
        'hooks':'Only explicit SimpleNamespace Runtime/Seed/source pin facts and synthetic local Root envelopes; real approved actual_cas, accepted_verifications, ref, read_regular, strict model matches/decode execute. No driver function is patched. The sole supplied observer is an in-memory GET comparison returning declared synthetic ancestry.',
        'production_context_or_CLI_API_lock_gate_receipt_five_ref_PR_intake_actions':0,
        'limitation':'Checks parser semantics against fabricated evidence, not authenticity/truth of Root authorization or PID/session lifetime; no live operational authority.'}
    (HERE/'ACTUAL_CAS_PARSER_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'checks':len(checks),'production_actions':0}))
if __name__=='__main__':main()
