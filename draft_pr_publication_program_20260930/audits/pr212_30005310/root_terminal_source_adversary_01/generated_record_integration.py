"""Exact generated repaired record -> actual unchanged consumer, owned mirror.

Producer controls are inherited fixture generation, not independent tests. This
wrapper captures actual emitted bytes without changing the publisher/core, then
independently challenges the unchanged consumer and checks terminal dataflow AST.
"""
from pathlib import Path
import ast,copy,datetime,hashlib,json,tempfile,types
HERE=Path(__file__).resolve().parent;CASE=HERE.parent
PARSER={'bytes':24760,'sha256':'0292388c3722d04cb2c11108d409c14759b61a370b0478fbbef41c92e19349eb'}
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def module(name,path,raw):
    m=types.ModuleType(name);m.__file__=str(path);exec(compile(raw,str(path),'exec'),m.__dict__);return m
def write(path,raw):path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw);path.chmod(0o444)

def main():
    src=(CASE/'root_terminal_source_preparation_02/ROOT_TERMINAL_INSPECTION.py').read_bytes()
    controls=(CASE/'root_terminal_source_preparation_02/offline_controls.py').read_bytes()
    parser_path=CASE.parents[1]/'ordered_intakes_after_PR212_20261017/preparation_01/status_only_intake_after_pr212.py'
    parser_source=parser_path.read_bytes();assert pin(parser_source)==PARSER
    tree=ast.parse(src);checks=[]
    binds=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='bind_runtime']
    assert len(binds)==1 and isinstance(binds[0].args[-1],ast.Constant) and binds[0].args[-1].value=='terminal'
    checks.append('sole extension bind explicitly uses terminal operation')
    functions={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    context=functions['context'];ret=[n for n in context.body if isinstance(n,ast.Return)][-1]
    assert isinstance(ret.value,ast.Tuple) and isinstance(ret.value.elts[1],ast.Name) and ret.value.elts[1].id=='rt'
    checks.append('context returns extension-rebound Runtime')
    delegated=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='driver':
            if node.func.attr in ('actual_cas','verify_immutable','main_closure','checked_pointer','local_states'):
                assert isinstance(node.args[0],ast.Name) and node.args[0].id=='rt';delegated.append(node.func.attr)
            assert node.func.attr not in ('candidate','sync','hold_CAS','lease_guard')
    assert set(delegated)=={'actual_cas','verify_immutable','main_closure','checked_pointer','local_states'}
    checks.append('all five delegated check families receive rebound rt; no operational driver calls')
    inspect=functions['inspect'];identity=next(n for n in inspect.body[-1].body if isinstance(n,ast.FunctionDef) and n.name=='identity_guard')
    assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('api','pointer_and_posts','native_semantics') for n in ast.walk(identity))
    checks.append('postpublication identity guard has no direct native or mutable-five check')
    captured=[]
    with tempfile.TemporaryDirectory(prefix='_owned_generated_consumer_',dir=HERE) as tmp:
        program=Path(tmp)/'checkout/program';a=program/'audits/pr212_30005310'
        s=a/'root_terminal_source_preparation_02';b=a/'native_administrative_preparation_01'
        write(s/'ROOT_TERMINAL_INSPECTION.py',src)
        for name in ('native212_primitives.py','native212_model.py','BASELINE_MEMBERSHIP.json'):
            write(b/name,(CASE/'native_administrative_preparation_01'/name).read_bytes())
        write(program/'ordered_intakes_after_PR212_20261017/preparation_01/status_only_intake_after_pr212.py',parser_source)
        original_queue=(CASE/'root_packet_preparation_01/_private_parent_capture_01/PARENT_QUEUE_BODY.txt').read_bytes()
        rows=[x for x in original_queue.splitlines(keepends=True) if b'30005310 / OWR-11695865-009' in x]
        assert len(rows)==1
        write(a/'root_packet_preparation_01/_private_parent_capture_01/PARENT_QUEUE_BODY.txt',rows[0])
        fixture=module('owned_inherited_controls',s/'offline_controls.py',controls);original_loader=fixture.load
        def capture_loader(name,path):
            loaded=original_loader(name,path)
            if name=='synthetic_terminal212':
                publisher=loaded.exclusive_root_receipt
                def capture(e,path,raw,*args,**kwargs):
                    captured.append(raw);return publisher(e,path,raw,*args,**kwargs)
                loaded.exclusive_root_receipt=capture
            return loaded
        fixture.load=capture_loader
        inherited=fixture.run()
        raw=next(v for v in captured if json.loads(v).get('schema')=='pr212-root-actual-administrative-skip-verification-v1')
        consumer_dir=a/'owned_consumer';write(consumer_dir/'BASELINE_MEMBERSHIP.json',(b/'BASELINE_MEMBERSHIP.json').read_bytes())
        consumer=module('owned_actual_after212_consumer',consumer_dir/'status_only_intake_after_pr212.py',parser_source)
        positive=consumer.completion_proof(raw,pin(raw))
        assert consumer.REQUESTS==[] and consumer.ACTIVE_PR is None
        checks.append('actual generated repaired record accepted by unchanged completion_proof without intake/network')
        negatives=[]
        cases=[('accepted',False),('accepted',1),('administrative_checkpoint_percent',100.0),
            ('fully_completed_count',54),('published_count',38),('last_completed_PR',212),('next_numeric_intake_cursor',212),
            ('advance_to_next_PR_authorized_now',False),('goal_complete',True),('completed_eligible_workflow',True),
            ('publication_workflow_completed',True),('publication_ready',True),('no_PR_or_publication_actions',False),
            ('numeric_advance_conditional_on_actual_Root_terminal',True),('original_eligibility_rewritten_or_erased',True),
            ('original_eligible_status','already_solved'),('current_corrected_status','claimed_solved'),
            ('current_PR_open_draft_unmerged',False),('actual_original_PR_merged',True),
            ('selected_postimage_paths_verified',0),('selected_postimage_paths_verified',True),
            ('protected_body_paths_verified',False),('protected_body_paths_verified',-1),('protected_body_paths_verified',10001),
            ('CAS_or_completion_inferred_from_ancestry',True),('perpetual_or_write_time_Main_equality_claimed',True),
            ('CAS_target','7'*40),('CAS_target_tree','7'*40),('actual_MAIN_observed','x'*40),
            ('native_final_ref_UTC',''),('terminal_observation_boundary',False)]
        def refuses(label,body,wanted=None):
            try:consumer.completion_proof(body,pin(body) if wanted is None else wanted)
            except (RuntimeError,KeyError,ValueError,TypeError):negatives.append(label)
            else:raise AssertionError('Consumer accepted '+label)
        for field,value in cases:
            bad=copy.deepcopy(positive);bad[field]=value;refuses(field+'='+repr(value),json.dumps(bad).encode())
        for field in ('numeric_advance_conditional_on_actual_Root_terminal','no_PR_or_publication_actions','protected_body_paths_verified'):
            bad=copy.deepcopy(positive);bad.pop(field);refuses('missing '+field,json.dumps(bad).encode())
        for field in ('fully_completed_eligible_PRs','published_PRs'):
            bad=copy.deepcopy(positive);bad[field][0]=212;refuses('membership replacement '+field,json.dumps(bad).encode())
            bad=copy.deepcopy(positive);bad[field][0]=True;refuses('membership Boolean '+field,json.dumps(bad).encode())
        refuses('external body pin changed',raw,{'bytes':len(raw),'sha256':'0'*64})
        refuses('duplicate accepted JSON key',raw.rstrip()[:-1]+b',"accepted":true}\n')
        assert positive['protected_body_paths_verified']==0
        assert positive['numeric_advance_conditional_on_actual_Root_terminal'] is False and positive['no_PR_or_publication_actions'] is True
    out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','source_pin':pin(src),
        'producer_control_source_pin':pin(controls),'parser_pin':PARSER,'generated_record_pin':pin(raw),
        'producer_fixture_checks':inherited['check_count'],'independent_AST_and_positive_checks':checks,
        'delegated_check_calls':delegated,'independent_consumer_negative_controls':negatives,'negative_count':len(negatives),
        'hooks':'Inherited producer controls only generate owned fixture facts. Module loader wraps publisher to capture exact inspect-generated bytes, then calls unchanged publisher. No terminal core/parser logic patched. Whole recorded QUEUE replaced only in owned disposable fixture by its exact166-byte own row; no foreign rows copied. After212 source and853-byte baseline copied unchanged. Independent mutation and AST controls are separately authored.',
        'all_fixtures_removed':True,'production_context_API_original_lock_gate_CAS_receipt_five_ref_PR_intake_actions':0,
        'limitation':'Synthetic generated-record interface test, not actual Root terminal or native truth. Optional future extension implementation still needs its own separate source/admission acceptance.'}
    (HERE/'GENERATED_RECORD_INTEGRATION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','producer_fixture_checks':inherited['check_count'],'independent_consumer_negatives':len(negatives),'AST_and_positive':len(checks),'source_pin':pin(src)}))
if __name__=='__main__':main()
