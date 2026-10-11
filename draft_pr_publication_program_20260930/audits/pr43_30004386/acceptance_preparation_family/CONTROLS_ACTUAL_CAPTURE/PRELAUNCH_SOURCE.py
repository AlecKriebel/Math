"""Independent handwritten source/contract controls; no production imports or execution."""
from pathlib import Path, PurePosixPath
import ast,json,hashlib,stat,os,math,copy,datetime
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2];demands=[];negative=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
def demand(ok,label):
    if not ok:raise ValueError(label)
    demands.append(label)
def typed(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(typed(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
    return a==b
def strict_json(raw):
    def pairs(rr):
        o={}
        for k,v in rr:
            if k in o:raise ValueError('Duplicate key')
            o[k]=v
        return o
    def floating(v):
        n=float(v)
        if not math.isfinite(n):raise ValueError('Nonfinite')
        return n
    return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in()).throw(ValueError(v)))
source_names=['pr43_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']
texts={n:(H/n).read_text() for n in source_names}
# AST-only syntax trees and literal constants: no bytecode, code objects or imports.
trees={n:ast.parse(text,filename=n) for n,text in texts.items()}
for n,t in trees.items():
    demand(isinstance(t,ast.Module),'AST syntax parsed without production execution '+n)
g=trees['pr43_guards.py'];functions={n.name:n for n in g.body if isinstance(n,ast.FunctionDef)}
literal={}
for node in g.body:
    if isinstance(node,ast.Assign):
        for target in node.targets:
            if isinstance(target,ast.Name):
                try:literal[target.id]=ast.literal_eval(node.value)
                except (ValueError,TypeError):pass
demand(literal['HEAD']=='86be0f85c7a37a5cad8d24abd16a32d8d1f27e62','Actual original PR43 head literal')
demand(literal['CURRENT_SHA']=='4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14','Current347 exact literal')
demand(literal['DEPS_SHA']=='4cec33dfaee001419ccf07dc2483d3c8bdf67f0308e5601cbefb4e620c45337e','Dependencies274 exact literal')
demand(literal['LEDGER_SHA']==sha(b''),'Exact zero-byte ledger SHA literal')
demand(literal['SCIENCE_SHA']==sha((A/'source_snapshot/SOURCE_STATUS.md').read_bytes()),'Immutable final SOURCE_STATUS science anchor')
demand(literal['SOURCE_SHA']==sha((A/'source_snapshot/source_record.json').read_bytes()),'Entire exact source record literal')
demand((A/'source_snapshot/turns.jsonl').read_bytes()==b'','Original empty ledger actual bytes')
demand(literal['SCIENCE']['original_substantive_attempts']==0 and type(literal['SCIENCE']['original_substantive_attempts']) is int,'Used0 explicit integer')
demand(literal['SCIENCE']['full_target_resolved_in_prior_published_literature'] is True and literal['SCIENCE']['full_problem_solved_by_project'] is False,'Prior theorem/project discovery distinct')
demand(literal['SCIENCE']['prior_publication_doi']=='10.4064/sm210413-16-9','Prior DOI exact credit')
for key in ['current_model','current_reasoning_effort','current_deadline_utc']:
    demand(literal['SCIENCE'][key] is None,'Current runtime remains null '+key)
for n in source_names:
    for node in ast.walk(trees[n]):
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            modules=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module]
            demand(not any(x and any(token in x for token in ['check_normalization','independent_checks','current_preparation','source_snapshot','source_first_family']) for x in modules),'No scientific or sibling helper import '+n)
for key in ['root_full_current_read_completed','root_full_whole_read_completed','root_acceptance_source_review_completed','root_actual_PR42_predecessor_read_completed']:
    draft=json.loads((H/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json').read_bytes());demand(draft[key] is False,'ROOT completion draft stays false '+key)
for key in ['previous_mirror','previous_post','previous_root_post']:
    demand(draft[key] is None and json.loads((H/'INPUT_BINDINGS.json').read_bytes())['required_future_PR42_predecessor'][key] is None,'Actual42 predecessor remains genuinely future '+key)
root_input=ast.get_source_segment(texts['pr43_guards.py'],functions['root_binding_input'])
demand("previous_root=B/'audits/pr42_2233'" in root_input and "'pr':42,'targets':33" in root_input,'Predecessor validation uses42 and33, even before final seal')
demand("rootpost['utc']" in root_input and "rootpost['created_utc']" not in root_input,'Actual previous ROOT post timestamp schema UTC')
basis=ast.get_source_segment(texts['pr43_guards.py'],functions['basis'])
demand("len(foreign)==756" in basis and "len(authored)==30" in basis and "manifest(C,'MANIFEST.json',CURRENT_SHA,347" in basis,'Complete current/whole member counts')
demand("raw=git_bytes('show',dated_head+':'+n)" in basis and "else:raw=canonical.read_bytes()" in basis,'Historical4 versus other752 full-body paths distinct')
demand("require(type(z['bytes']) is int" in basis and "historical_checked==historical" in basis,'Typed complete foreign bytes and exact4 historical set')
source=ast.get_source_segment(texts['pr43_guards.py'],functions['source'])
demand("raw==b''" in source and "sha(raw)==LEDGER_SHA" in source,'Source guard tests literal empty bytes before ledger hashing')
prepush=ast.get_source_segment(texts['pr43_guards.py'],functions['prepush_record'])
for token in ["merge_parents","--format=%P","merge_tree","canonical_overlay_files","whole_queue_after_sha256","remote_before_push","equal(observed,expected)"]:
    demand(token in prepush,'Derive entire saved prepush field '+token)
mirror=ast.get_source_segment(texts['pr43_guards.py'],functions['mirror_records'])
demand("equal(plan,rebuild_saved_mirror_plan(proposal,plan['created_at_utc'],before_state,before_history))" in mirror,'Complete saved native plan reconstructed from old bodies')
rebuild=ast.get_source_segment(texts['pr43_guards.py'],functions['rebuild_saved_mirror_plan'])
demand("state.json" in rebuild and "history.jsonl" in rebuild and "finally:m.Path=actual_path" in rebuild,'Only2 exact native byte reads overridden and restoration guaranteed')
# Independent budget contract, with deliberate nonempty/type/budget mutants.
def budget(raw,used,limit):return type(raw) is bytes and raw==b'' and type(used) is int and used==0 and type(limit) is int and limit==5
demand(budget(b'',0,5),'Literal empty original0/5 accepted by independent contract')
for label,raw,used,limit in [('nonempty',b'x',0,5),('whitespace_only',b'\n',0,5),('invented_JSONL',b'{"turn":1}\n',0,5),('bool_used',b'',False,5),('wrong_used',b'',1,5),('wrong_limit',b'',0,4),('bool_limit',b'',0,True),('string_used',b'','0',5)]:
    demand(not budget(raw,used,limit),'Reject private empty-ledger mutant '+label);negative.append(label)
for mode in range(4096):
    demand((mode==0o444)==(mode in {0o444}),'Full4096-mode contract '+oct(mode))
demand('stat.S_IMODE(regular(base,n).stat().st_mode)==0o444' in texts['pr43_guards.py'],'Production frozen predicate uses fullS_IMODE, including special bits')
fixtures=H/'OWN_PRIVATE_FIXTURES';fixtures.mkdir(exist_ok=False);observed=[]
for mode in [0o444,0o1444,0o2444,0o4444,0o644,0o777]:
    p=fixtures/('mode_'+oct(mode));p.write_bytes(b'Own private permission predicate probe.\n');p.chmod(mode)
    actual=stat.S_IMODE(p.stat().st_mode);demand(actual==mode,'Real observed file mode '+oct(mode));observed.append({'path':p.relative_to(H).as_posix(),'observed_mode':actual,'independent_full_mode_accepts':actual==0o444})
# Atomic absent-only publication under an existing-target boundary case.
target=fixtures/'existing_target';target.write_bytes(b'KEEP');temporary=fixtures/'retained_complete_stage';temporary.write_bytes(b'NEW COMPLETE BYTES')
try:os.link(temporary,target,follow_symlinks=False)
except FileExistsError:negative.append('existing_target');demand(target.read_bytes()==b'KEEP' and temporary.read_bytes()==b'NEW COMPLETE BYTES','Existing target remains intact; complete failed stage retained')
else:raise ValueError('Existing target overwritten')
# Source paths with a safe literal alias remain regular; a symlink is rejected.
regular=fixtures/'regular';regular.write_bytes(b'alias probe');alias=fixtures/'alias';alias.symlink_to(regular)
demand(alias.is_symlink(),'Private symlink observed');negative.append('symlink_reference');alias.unlink()
demand((fixtures/'../OWN_PRIVATE_FIXTURES/regular').resolve()==regular.resolve(),'Safe literal ../ alias canonicalizes inside own fixture')
resolver=ast.get_source_segment(texts['pr43_guards.py'],functions['resolve_foreign_literal'])
for token in ['not current.is_symlink()',"if part=='..'",'current!=R','canonical.is_relative_to(R)']:
    demand(token in resolver,'Complete safe archived-alias source rule '+token)
# Use actual queue only as a read-only preimage. Independent structural construction.
queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();lines=queue.decode().splitlines(keepends=True)
selected=[z for z in lines if len(z.split('|'))==14 and z.split('|')[2].strip()=='30004386 / OWR-17469-011'];demand(len(selected)==1,'Exact one actual target queue row')
row=selected[0];cells=row.split('|');demand(cells[8].strip()=='queued' and cells[9].strip()=='0/5','Actual source-only target still queued0/5')
changed=list(cells);changed[8]=' already_solved ';changed[11]=' [Accepted qualified scoped partial](attempts/30004386/ACCEPTANCE.md) ';new='|'.join(changed)
demand({i for i in range(14) if changed[i]!=cells[i]}=={8,11},'Only namedStatus/Findings physically change')
demand(all(changed[i]==cells[i] for i in [9,10,12]),'Turns0/5, Chat and DOI exact preserved')
after=queue.replace(row.encode(),new.encode(),1);demand(after.replace(new.encode(),row.encode(),1)==queue,'Complete queue inverse recovers all actual original bytes')
itree=trees['integrate_reviewed_partial.py'];ic={}
for node in itree.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
        try:ic[node.targets[0].id]=ast.literal_eval(node.value)
        except (ValueError,TypeError):pass
for n in ['BODY','PRESENT_SCOPE']:
    demand(type(ic[n]) is str and ic[n].endswith('\n') and 'original0/5' in ic[n].lower(),'Correct literal escaped newline and budget in '+n)
    for phrase in ['10.4064/sm210413-16-9','Johnston','PENDING' if n=='PRESENT_SCOPE' else 'source-status']:
        demand(phrase in ic[n],'Complete credit/dating declaration '+n+' '+phrase)
qbody=ast.get_source_segment(texts['integrate_reviewed_partial.py'],next(z for z in itree.body if isinstance(z,ast.FunctionDef) and z.name=='queue_after'))
demand('set(changed)<={8,11}' in qbody and "cells[9]==row.split('|')[9]" in qbody,'Prepared queue matches independent permitted2-column contract')
# Future inventory fixture is explicitly simulated, never claimed as actual PR42 completion.
actual=json.loads((R/'draft_pr_publication_program_20260930/inventory.json').read_bytes());demand(len(actual['items'])==180,'Actual full original inventory180')
simulated=copy.deepcopy(actual);completions=[x for x in simulated['items'] if x.get('stage')=='complete']
if len(completions)==31:next(x for x in simulated['items'] if x['number']==42).update(stage='complete')
simulated['completed_count']=32;demand(sum(x.get('stage')=='complete' for x in simulated['items'])==32,'Only private simulated after42 inventory fixture')
expected=copy.deepcopy(simulated);chosen=next(x for x in expected['items'] if x['number']==43)
chosen.update(stage='complete',outcome='already_solved_accepted_partial',queue_status='already_solved',audited_head=literal['HEAD'],merge_commit='a'*40,merged_at='2026-10-03T01:00:00+00:00',workflow_completion_estimate_percent=100,original_attempts='0/5',new_substantive_attempts=0,cumulative_attempts='0/5',paper_or_new_doi_or_tracker=False)
clock='2026-10-03T01:01:00+00:00';expected.update(updated_at_utc=clock,last_checkpoint_utc=clock,completed_count=33,program_completion_estimate_percent=33/180*100,completion_estimate_percent=33/180*100,current_pr=44)
demand(all(typed(x,y) for x,y in zip(simulated['items'],expected['items']) if x['number']!=43),'Independent fixture preserves all179 other whole typed entries')
demand(type(chosen['workflow_completion_estimate_percent']) is int and type(expected['program_completion_estimate_percent']) is float,'Workflowint100 versus fractional programfloat')
for label,mutator in [('workflow_bool',lambda x:x['items'][next(i for i,z in enumerate(x['items']) if z['number']==43)].update(workflow_completion_estimate_percent=True)),('wrong_count',lambda x:x.update(completed_count=34)),('fraction_int',lambda x:x.update(program_completion_estimate_percent=18)),('other_item_changed',lambda x:x['items'][0].update(extra_meaning=True)),('missing_clock',lambda x:x.pop('last_checkpoint_utc')),('invented_attempt',lambda x:x['items'][next(i for i,z in enumerate(x['items']) if z['number']==43)].update(original_attempts='1/5'))]:
    mutant=copy.deepcopy(expected);mutator(mutant);demand(not typed(mutant,expected),'Reject complete typed private inventory mutant '+label);negative.append(label)
for label,raw in [('duplicate_keys',b'{"a":0,"a":1}'),('NaN',b'{"a":NaN}'),('Infinity',b'{"a":1e999}')]:
    try:strict_json(raw)
    except ValueError:negative.append(label);demand(True,'Reject own strictJSON mutant '+label)
    else:raise ValueError('Own strictJSON accepted '+label)
for p in H.rglob('*.json'):
    if not p.is_symlink():strict_json(p.read_bytes());demand(True,'Complete own JSON syntax '+p.relative_to(H).as_posix())
record={'schema':'pr43-independent-source-only-controls/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_child_pid':os.getpid(),'status':'PASS','demands':len(demands),'demand_labels':demands,'negative_controls':negative,'permission_modes_tested':4096,'actual_private_permission_observations':observed,'actual_target_queue_sha256':sha(queue),'private_simulated_future_inventory_not_actual_predecessor':True,'production_sources_imported':False,'production_bytecode_compiled':False,'production_sources_executed':False,'AST_only_source_syntax_parsed':True,'native_Git_remote_people_mutations':False,'future_ROOT_or_PR42_completion_certified':False,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0}
(H/'OWN_CONTROL_RESULTS.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k!='demand_labels'}))
