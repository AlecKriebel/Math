"""Independent actual-fixture controls for the PR209 terminal-LF repair.

No transport, production CLI, Root gate, monkeypatch or source adapter exists.
The reviewed pure predicate and deterministic commit constructor run directly.
AST equality checks bind unchanged surrounding validation mechanisms.
"""
import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path
import types

OWN=Path(__file__).absolute().parent
B=OWN.parents[1]/'native_integration_preparation_01'
OLD=OWN.parent/'candidate_addendum_01'
RECORDS=[]
def need(ok,message):
    if not ok:raise AssertionError(message)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def check(name,function):function();RECORDS.append({'control':name,'result':'PASS'})
def refuse(name,function):
    try:function()
    except (RuntimeError,ValueError,KeyError,TypeError):RECORDS.append({'control':name,'result':'PASS_REFUSED'});return
    raise AssertionError('Unexpected acceptance: '+name)
parser=argparse.ArgumentParser()
parser.add_argument('--manifest',required=True);parser.add_argument('--bytes',type=int,required=True);parser.add_argument('--sha256',required=True)
args=parser.parse_args()
manifest_pin={'bytes':args.bytes,'sha256':args.sha256}
raw=(B/args.manifest).read_bytes();need(pin(raw)==manifest_pin,'exact current manifest');m=json.loads(raw)
source=(B/'native209_model.py').read_bytes();need(pin(source)==m['helper_pin'],'model exact packet pin')
H=types.ModuleType('independent_message_repair_model');H.__file__=str(B/'native209_model.py');exec(compile(source,H.__file__,'exec'),H.__dict__)
old_m=json.loads((B/'ROOT_EXACT_MERGE95_MANIFEST_02.json').read_bytes())
fixture_raw=(OLD/'metadata/git_commits_45d77dd0d8780135182dcab3fc6ac518e9ac7564.json').read_bytes()
fixture=json.loads(fixture_raw);canonical=old_m['commit_message'];display=fixture['message']
need(len(canonical.encode())==267 and len(display.encode())==266 and canonical==display+'\n','actual one-LF fixture')

def correct_exact():
    r=H.commit_message_readback(canonical,canonical)
    need(r=={'representation':'exact','terminal_LFs_omitted':0,'canonical_message_pin':pin(canonical.encode()),'metadata_message_pin':pin(canonical.encode())},'exact record')
check('exact_canonical_message_accepted_and_pinned',correct_exact)
def correct_actual():
    r=H.commit_message_readback(canonical,display)
    need(r=={'representation':'omits_exactly_one_terminal_LF','terminal_LFs_omitted':1,'canonical_message_pin':pin(canonical.encode()),'metadata_message_pin':pin(display.encode())},'actual omitted-LF record')
check('actual_native_metadata_single_terminal_LF_omission_accepted_and_pinned',correct_actual)
for label,value in [('leading_space',' '+display),('leading_LF','\n'+display),('trailing_space',display+' '),
 ('terminal_CR',display+'\r'),('terminal_CRLF',display+'\r\n'),('extra_terminal_LF',canonical+'\n'),
 ('two_extra_terminal_LFs',canonical+'\n\n'),('internal_blank_line',display.replace('\n\n','\n',1)),
 ('changed_text',display.replace('Audited','Reviewed') if 'Audited' in display else display.replace('Audit','Review',1)),
 ('empty_message',''),('trailing_tab',display+'\t')]:
    refuse('metadata_'+label,lambda value=value:H.commit_message_readback(canonical,value))
refuse('multiple_terminal_LFs_removed',lambda:H.commit_message_readback(canonical+'\n',display))
for index,value in enumerate((None,True,123,b'x',{},[])):
    refuse('metadata_type_'+str(index),lambda value=value:H.commit_message_readback(canonical,value))
for index,value in enumerate((None,True,123,b'x',{},[],display)):
    refuse('canonical_type_or_missing_LF_'+str(index),lambda value=value:H.commit_message_readback(value,display))

# Actual canonical commit identity remains deterministically fixed. These are
# constructor equations, not an adapter to a service response or production run.
req,oid=H.commit_request(old_m,fixture['tree']['sha'],[r['sha'] for r in fixture['parents']])
check('actual_canonical_fixture_OID_still_exact45d',lambda:need(oid==fixture['sha']=='45d77dd0d8780135182dcab3fc6ac518e9ac7564','canonical fixture OID'))
for label,changed,tree,parents in [
 ('wrong_tree',old_m,'0'*40,[r['sha'] for r in fixture['parents']]),
 ('reversed_parents',old_m,fixture['tree']['sha'],[r['sha'] for r in reversed(fixture['parents'])]),
 ('wrong_parent',old_m,fixture['tree']['sha'],['f'*40,fixture['parents'][1]['sha']]),
 ('canonical_message_changed',dict(old_m,commit_message=canonical+'\n'),fixture['tree']['sha'],[r['sha'] for r in fixture['parents']]),
 ('author_changed',dict(old_m,commit_author=dict(old_m['commit_author'],name='Other researcher')),fixture['tree']['sha'],[r['sha'] for r in fixture['parents']]),
 ('committer_changed',dict(old_m,commit_committer=dict(old_m['commit_committer'],email='other@example.invalid')),fixture['tree']['sha'],[r['sha'] for r in fixture['parents']]),
]:
    check('canonical_OID_changes_with_'+label,lambda changed=changed,tree=tree,parents=parents:need(H.commit_request(changed,tree,parents)[1]!=oid,'alteration changes canonical OID'))
for key in ('author','committer'):
    check('actual_'+key+'_identity_matches',lambda key=key:H.matches(fixture[key],old_m['commit_'+key],'fixed actual identity'))
    for field,value in [('name','Other'),('email','other@example.invalid'),('date','2026-10-17T02:00:59Z')]:
        bad=copy.deepcopy(fixture[key]);bad[field]=value
        refuse('wrong_'+key+'_'+field,lambda bad=bad,key=key:H.matches(bad,old_m['commit_'+key],'fixed identity'))

old_ast=ast.parse((B/'source_history_05/native209_model.py').read_bytes());new_ast=ast.parse(source)
old_defs={n.name:n for n in old_ast.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
new_defs={n.name:n for n in new_ast.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def unchanged_functions():
    need(set(new_defs)==set(old_defs)|{'commit_message_readback'},'only expected new pure helper')
    for name,node in old_defs.items():
        if name!='verify':need(ast.dump(node,include_attributes=False)==ast.dump(new_defs[name],include_attributes=False),'unchanged mechanism '+name)
check('all_other_model_functions_AST_identical_to_reviewed_pre_repair_source',unchanged_functions)
def fixed_verify_guards():
    old_verify=old_defs['verify'];new_verify=new_defs['verify']
    # State readback, deterministic request and candidateOID guard precede the
    # new representation check; those first six statements remain exact.
    need([ast.dump(n,include_attributes=False) for n in old_verify.body[:6]]==[ast.dump(n,include_attributes=False) for n in new_verify.body[:6]],'original deterministic OID/readback prefix intact')
    expected_guard=ast.parse("commit.get('sha') == candidate and commit['tree']['sha'] == s['wanted'] and [r['sha'] for r in commit['parents']] == s['parents']",mode='eval').body
    need(ast.dump(new_verify.body[6].value.args[0],include_attributes=False)==ast.dump(expected_guard,include_attributes=False),'exact native SHA/tree/orderedparents guard')
    source_text=ast.unparse(new_verify)
    positions=[source_text.index(text) for text in [
      'candidate == expected_commit',"commit.get('sha') == candidate",'Fixed canonical author metadata differs',
      'Fixed canonical committer metadata differs','commit_message_readback(m[\'commit_message\'], commit.get(\'message\'))','c.NativeTrees(api)']]
    need(positions==sorted(positions),'hash/tree/parent/identity checks precede representation and scope')
    old_index=next(i for i,n in enumerate(old_verify.body) if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='trees')
    new_index=next(i for i,n in enumerate(new_verify.body) if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='trees')
    need([ast.dump(n,include_attributes=False) for n in old_verify.body[old_index:-1]]==[ast.dump(n,include_attributes=False) for n in new_verify.body[new_index:-1]],'full scope/body/finalMAIN verification unchanged')
check('full_verify_retains_canonical_OID_parent_tree_identity_scope_body_and_finalMAIN_barriers',fixed_verify_guards)
def executor_same():
    old_tree=ast.parse((B/'source_history_05/native209_future_executor.py').read_bytes());new_tree=ast.parse((B/'native209_future_executor.py').read_bytes())
    def without_pin(tree):return [ast.dump(n,include_attributes=False) for n in tree.body if not (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODEL_PIN' for t in n.targets))]
    need(without_pin(old_tree)==without_pin(new_tree),'executor unchanged except model pin')
check('executor_AST_unchanged_except_model_pin',executor_same)

result={'schema':'pr209-independent-message-repair-controls-v1','evidence_scope':'OFFLINE_ACTUAL_FIXTURE_CONTROLS_NOT_ROOT_AUTHORITY',
 'manifest_pin':manifest_pin,'helper_pin':m['helper_pin'],'executor_pin':m['executor_pin'],
 'actual_metadata_fixture_pin':pin(fixture_raw),'controls':RECORDS,'control_count':len(RECORDS),'all_passed':True,
 'actual_provider_calls':0,'production_CLI_invoked':False,'Root_gates_created':False,'production_source_adapters_or_monkeypatches':False,
 'native_objects_or_refs_created':False,'local_five_modified':False,'publication_or_tracker_action':False,
 'limits':'Pure actual-fixture predicate/constructor controls and AST-preservation proofs. Fresh exact packet and later actual candidate still require their own readbacks.'}
(OWN/'TARGETED_CONTROLS_RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='controls'},sort_keys=True))
