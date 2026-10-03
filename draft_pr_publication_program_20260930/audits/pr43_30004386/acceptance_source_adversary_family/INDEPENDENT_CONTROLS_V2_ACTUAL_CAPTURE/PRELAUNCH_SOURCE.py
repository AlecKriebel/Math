"""Handwritten source/OS/schema/native-plan controls. No proposed code imported."""
from pathlib import Path, PurePosixPath
import ast
import copy
import ctypes
import datetime as dt
import hashlib
import json
import math
import os
import stat
import sys
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2];S=A/'acceptance_preparation_family'
count=0;negative=[];witnesses=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def check(v,label):
    global count
    count+=1
    if not v:raise AssertionError(label)
def typed(a,b):
    if type(a) is not type(b):return False
    if type(a)is dict:return set(a)==set(b) and all(typed(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b) and all(typed(x,y)for x,y in zip(a,b))
    return a==b
def reject(label,call):
    try:call()
    except (ValueError,AssertionError,FileNotFoundError,FileExistsError,NotADirectoryError,OSError):negative.append(label);check(True,'rejected '+label)
    else:raise AssertionError('accepted '+label)
def strict(raw):
    def pairs(rows):
        o={}
        for k,v in rows:
            if k in o:raise ValueError('duplicate key')
            o[k]=v
        return o
    def fl(v):
        x=float(v)
        if not math.isfinite(x):raise ValueError('nonfinite')
        return x
    return json.loads(raw,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda v:(_ for _ in()).throw(ValueError(v)))
texts={n:(S/n).read_text()for n in ['pr43_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']}
trees={n:ast.parse(text,filename=n)for n,text in texts.items()}
guard={n.name:n for n in trees['pr43_guards.py'].body if isinstance(n,ast.FunctionDef)}
constants={}
for n in trees['pr43_guards.py'].body:
    if isinstance(n,ast.Assign):
        for t in n.targets:
            if isinstance(t,ast.Name):
                try:constants[t.id]=ast.literal_eval(n.value)
                except (ValueError,TypeError):pass
check(constants['HEAD']=='86be0f85c7a37a5cad8d24abd16a32d8d1f27e62','original literal head')
check(constants['LEDGER_SHA']==sha(b''),'empty ledger literal anchor')
check(constants['SCIENCE']['prior_publication_doi']=='10.4064/sm210413-16-9','prior DOI literal')
for key in ['current_model','current_reasoning_effort','current_deadline_utc']:check(constants['SCIENCE'][key]is None,'current null '+key)
for key in ['full_problem_solved','full_problem_solved_by_project','novelty_claimed','priority_claimed','human_referee_review_claimed','paper_or_new_doi_or_tracker']:check(constants['SCIENCE'][key]is False,'scope false '+key)
check(constants['SCIENCE']['full_target_resolved_in_prior_published_literature']is True,'prior solution true')
check(all(type(constants['SCIENCE'][k])is int and constants['SCIENCE'][k]==0 for k in ['original_substantive_attempts','new_substantive_attempts','audit_turns']),'typed all zero counts')
# Concrete real-file witness: overlay names a missing original snapshot.
it=trees['integrate_reviewed_partial.py']
wrong=[n for n in ast.walk(it)if isinstance(n,ast.Constant)and n.value=='snapshot_manifest_v2.json']
check(len(wrong)==1,'exact copied snapshot path witness')
check(not (A/'snapshot_manifest_v2.json').exists() and (A/'snapshot_manifest.json').is_file(),'actual missing path, correct original exists')
reject('actual_missing_overlay_snapshot_filename',lambda:(A/'snapshot_manifest_v2.json').read_bytes())
witnesses.append({'id':'M1','file':'integrate_reviewed_partial.py','line':wrong[0].lineno,'actual_literal':wrong[0].value,'actual_named_path_absent':True,'correct_actual_path':'snapshot_manifest.json','production_execution_required':False})
# Concrete literal witness: compare AST literal argument values without executing either function.
def scopes(tree):
    out=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            for kw in node.keywords:
                if kw.arg=='scope' and isinstance(kw.value,ast.Constant) and type(kw.value.value)is str:out.append((kw.value.value,kw.value.lineno))
    return out
gs=scopes(guard['mirror_proposal']);ms=scopes(trees['state_mirror_reconciliation.py'])
check(len(gs)==len(ms)==1 and gs[0][0]!=ms[0][0],'exact source-level mirror scope disagreement')
check(gs[0][0].replace('PR43 source-status','PR43; source-status')==ms[0][0],'narrow semicolon difference witness')
witnesses.append({'id':'M2','file':'state_mirror_reconciliation.py','line':ms[0][1],'emitted_scope':ms[0][0],'guard_file':'pr43_guards.py','guard_line':gs[0][1],'required_scope':gs[0][0],'whole_typed_equality_rejects':not typed({'scope':ms[0][0]},{'scope':gs[0][0]}),'production_execution_required':False})
# All g.* calls have actual declared definitions/constants; scientific helpers are not imported.
exported=set(guard)|{n.id for z in trees['pr43_guards.py'].body if isinstance(z,ast.Assign)for target in z.targets for n in ast.walk(target) if isinstance(n,ast.Name)}
for name,t in trees.items():
    for n in ast.walk(t):
        if isinstance(n,ast.Attribute)and isinstance(n.value,ast.Name)and n.value.id=='g':check(n.attr in exported,'declared guard export '+n.attr)
        if isinstance(n,(ast.Import,ast.ImportFrom)):
            modules=[a.name for a in n.names]if isinstance(n,ast.Import)else[n.module]
            check(not any(q and any(x in q for x in ['check_normalization','independent_checks','current_preparation','source_snapshot'])for q in modules),'no scientific helper import')
fn=lambda name:ast.get_source_segment(texts['pr43_guards.py'],guard[name])
for phrase in ["raw==b''",'sha(raw)==LEDGER_SHA',"equal(parse(prior),{})"]:check(phrase in fn('source'),'literal scientific/source prior boundary '+phrase)
for phrase in ['root_actual_PR42_predecessor_read_completed=True',"previous_root=B/'audits/pr42_2233'",'equal(rootpost[\'entire_post\'],post)',"rootpost['utc']",'created_utc']:
    check(phrase in fn('root_binding_input'),'actual predecessor source guard '+phrase)
for phrase in ["len(foreign)==756","len(authored)==30","raw=git_bytes('show',dated_head+':'+n)",'else:raw=canonical.read_bytes()','historical_checked==historical']:
    check(phrase in fn('basis'),'full whole binding rule '+phrase)
for phrase in ['equal(plan,rebuild_saved_mirror_plan','before_state,before_history','keyset(plan,']:
    check(phrase in fn('mirror_records'),'complete native reconstruction '+phrase)
rebuild=fn('rebuild_saved_mirror_plan')
check(rebuild.count("R/'unsolved_math_prioritization/")==2 and 'finally:m.Path=actual_path'in rebuild,'only exact state/history overridden and restored')
for phrase in ['merge_parents','--format=%P','canonical_overlay_files','whole_queue_after_sha256','equal(observed,expected)']:
    check(phrase in fn('prepush_record'),'saved prepush derivation '+phrase)
# Strict JSON, exact keys, typed object equality and literal empty original0/5.
for label,raw in [('duplicate-key',b'{"x":0,"x":1}'),('nested-duplicate',b'{"x":{"a":0,"a":1}}'),('NaN',b'{"x":NaN}'),('Infinity',b'{"x":Infinity}'),('overflow',b'{"x":1e999}')]:reject(label,lambda raw=raw:strict(raw))
check(typed(strict(b'{"zero":0,"unknown":null,"truth":false}'),{'zero':0,'unknown':None,'truth':False}),'strict honest object')
def empty(raw,used,limit):
    check(type(raw)is bytes and raw==b'' and type(used)is int and used==0 and type(limit)is int and limit==5,'empty original0/5 contract')
empty(b'',0,5)
for label,raw,used,limit in [('nonempty',b'x',0,5),('white',b'\n',0,5),('invented-turn',b'{"turn":1}\n',0,5),('bool-used',b'',False,5),('bool-limit',b'',0,True),('float-used',b'',0.0,5),('str-used',b'','0',5),('used-one',b'',1,5),('limit-four',b'',0,4)]:reject(label,lambda raw=raw,used=used,limit=limit:empty(raw,used,limit))
mode_predicate=fn('frozen_files');check('stat.S_IMODE(regular(base,n).stat().st_mode)==0o444'in mode_predicate,'production full permission predicate')
for mode in range(0o10000):
    accepted=stat.S_IMODE(stat.S_IFREG|mode)==0o444
    check(accepted==(mode==0o444),'all permission patterns including special bits '+oct(mode))
F=H/'PRIVATE';F.mkdir();observations=[]
for mode in [0o444,0o1444,0o2444,0o4444,0o644]:
    p=F/('mode_'+oct(mode));p.write_bytes(b'Independent permission probe.\n');p.chmod(mode)
    observed=stat.S_IMODE(p.stat().st_mode);check(observed==mode,'actual full permission observation')
    observations.append({'path':p.relative_to(H).as_posix(),'actual_full_permission_bits':observed,'accepts_frozen0444':observed==0o444})
# Own filesystem resolver checks all path prefixes, including escape then return.
def resolve(literal,base):
    if type(literal)is not str or not literal.startswith(str(base)+'/')or'\\'in literal or'\0'in literal:raise ValueError('literal')
    q=base;parts=literal[len(str(base))+1:].split('/')
    for i,p in enumerate(parts):
        if not p or p in {'.git','__pycache__'}:raise ValueError('private/empty component')
        if not q.is_dir()or q.is_symlink():raise ValueError('prefix')
        if p=='.':continue
        if p=='..':
            if q==base:raise ValueError('escape prefix')
            q=q.parent
        else:q=q/p
        if not q.exists()or q.is_symlink()or not(q==base or q.is_relative_to(base)):raise ValueError('missing/symlink/escape')
        if i<len(parts)-1 and not q.is_dir():raise ValueError('non directory')
    if not q.is_file()or q.is_symlink()or q==base or q.resolve()!=q:raise ValueError('final ordinary regular')
    return q
root=F/'resolver_root';root.mkdir();d=root/'d';d.mkdir();regular=d/'regular';regular.write_bytes(b'Private resolver source.\n')
check(resolve(str(root)+'/d/../d/./regular',root)==regular,'honest safe literal alias')
link=d/'link';link.symlink_to(regular);ancestor=root/'ancestor';ancestor.symlink_to(d,target_is_directory=True)
private=root/'.git';private.mkdir();(private/'hidden').write_bytes(b'not public')
for label,literal in [('escape-return',str(root)+'/../resolver_root/d/regular'),('final-symlink',str(link)),('ancestor-symlink',str(ancestor)+'/regular'),('missing',str(d)+'/missing'),('through-file',str(regular)+'/../regular'),('final-dir',str(d)),('private-git',str(private)+'/hidden'),('double-slash',str(root)+'/d//regular'),('backslash',str(root)+'/d\\regular'),('nul',str(root)+'/d/regular\0'),('outside',str(F)+'/mode_0o444')]:reject(label,lambda literal=literal:resolve(literal,root))
link.unlink();ancestor.unlink()
# Absent-only regular-file and macOS directory publication controls.
target=F/'target';temporary=F/'completed_stage';target.write_bytes(b'KEEP');temporary.write_bytes(b'NEW COMPLETE')
reject('existing_regular_target',lambda:os.link(temporary,target,follow_symlinks=False));check(target.read_bytes()==b'KEEP'and temporary.read_bytes()==b'NEW COMPLETE','target and failed stage preserved')
if sys.platform=='darwin':
    old=F/'directory_target';old.mkdir();(old/'prior').write_bytes(b'KEEP DIR');new=F/'directory_stage';new.mkdir();(new/'new').write_bytes(b'NEW DIR')
    libc=ctypes.CDLL(None,use_errno=True);rename=libc.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
    code=rename(os.fsencode(new),os.fsencode(old),4);check(code!=0 and (old/'prior').read_bytes()==b'KEEP DIR'and(new/'new').read_bytes()==b'NEW DIR','real RENAME_EXCL existing-directory refusal')
    negative.append('existing_directory_target')
    destination=F/'new_published_directory';check(rename(os.fsencode(new),os.fsencode(destination),4)==0 and not new.exists()and(destination/'new').read_bytes()==b'NEW DIR','real RENAME_EXCL absent-directory success')
# Independent complete typed inventory transform fixture; explicitly NOT actual predecessor.
inv=strict((R/'draft_pr_publication_program_20260930/inventory.json').read_bytes());check(len(inv['items'])==180,'actual180 inventory')
fixture=copy.deepcopy(inv);prior_complete=sum(z.get('stage')=='complete'for z in fixture['items']);check(prior_complete in (31,32),'contemporaneous31or32 complete only')
if prior_complete==31:next(z for z in fixture['items']if z['number']==42).update(stage='complete')
fixture['completed_count']=32;expected=copy.deepcopy(fixture);chosen=next(z for z in expected['items']if z['number']==43)
chosen.update(stage='complete',outcome='already_solved_accepted_partial',queue_status='already_solved',audited_head=constants['HEAD'],merge_commit='a'*40,merged_at='2026-10-03T01:00:00+00:00',workflow_completion_estimate_percent=100,original_attempts='0/5',new_substantive_attempts=0,cumulative_attempts='0/5',paper_or_new_doi_or_tracker=False)
expected.update(updated_at_utc='2026-10-03T01:01:00+00:00',last_checkpoint_utc='2026-10-03T01:01:00+00:00',completed_count=33,program_completion_estimate_percent=33/180*100,completion_estimate_percent=33/180*100,current_pr=44)
check(all(typed(a,b)for a,b in zip(fixture['items'],expected['items'])if a['number']!=43),'all179 complete typed unrelated records preserved')
for label,mutation in [('inventory-bool',lambda x:x.update(completed_count=True)),('other-inventory-row',lambda x:x['items'][0].update(invented=True)),('future-count',lambda x:x.update(completed_count=34)),('new-attempt',lambda x:next(z for z in x['items']if z['number']==43).update(new_substantive_attempts=1)),('null-runtime-to-string',lambda x:x.update(current_model='unknown')),('missing-clock',lambda x:x.pop('last_checkpoint_utc'))]:
    mutant=copy.deepcopy(expected);mutation(mutant);check(not typed(mutant,expected),'whole typed schema rejects '+label);negative.append(label)
# Whole native plan fixture: original prefix/all33 prior states plus one new zero-turn event.
prior={'old_'+str(i):{'turns_used':(2 if i<8 else 1 if i<33 else 0),'typed':None,'id':str(i)}for i in range(33)}
turns=sum(z['turns_used']for z in prior.values());check(turns==41,'synthetic prior33/41 contract')
event={'id':'30004386','event':'acceptance_mirror_import','status':'already_solved','turns_used':0,'turn_limit':5,'evidence':{'historical_transitions_asserted':False,'import_is_present_day_mirror':True,'duplicate_ids':[]}}
after=copy.deepcopy(prior);after[event['id']]=event;history=b'FULL ORIGINAL PREFIX\n';append=(json.dumps(event,sort_keys=True)+'\n').encode()
plan={'state_after':after,'history_append':[event],'history_after_bytes':(history+append).decode(),'primary_count':33,'duplicate_count':1,'created_at_utc':'2026-10-03T01:01:00+00:00'}
check(len(after)==34 and sum(z['turns_used']for z in after.values())==41 and all(typed(after[k],v)for k,v in prior.items()),'preserve33 typed states/41 turns after zero-turn event')
for label,mutation in [('native-extra-event',lambda x:x['history_append'].append(event)),('native-prefix-loss',lambda x:x.update(history_after_bytes=append.decode())),('native-old-state',lambda x:x['state_after']['old_0'].update(turns_used=False)),('native-bool-count',lambda x:x.update(primary_count=True)),('native-unknown-key',lambda x:x.update(invented=True)),('native-new-turn',lambda x:x['state_after'][event['id']].update(turns_used=1))]:
    mutant=copy.deepcopy(plan);mutation(mutant);check(not typed(mutant,plan),'complete reconstructed plan rejects '+label);negative.append(label)
queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();matches=[l for l in queue.decode().splitlines(keepends=True)if len(l.split('|'))==14 and l.split('|')[2].strip()=='30004386 / OWR-17469-011'];check(len(matches)==1,'unique current43 queue')
row=matches[0];cells=row.split('|');check(cells[8].strip()=='queued'and cells[9].strip()=='0/5','original queued0/5');new=list(cells);new[8]=' already_solved ';new[11]=' [Accepted qualified scoped partial](attempts/30004386/ACCEPTANCE.md) ';replacement='|'.join(new);qafter=queue.replace(row.encode(),replacement.encode(),1)
check({i for i in range(14)if cells[i]!=new[i]}=={8,11}and qafter.replace(replacement.encode(),row.encode(),1)==queue,'all other complete queue bytes and ChatDOI preserved')
result={'schema':'PR43_NEW_ACCEPTANCE_SOURCE_ADVERSARY_INDEPENDENT_CONTROLS_v1','utc':now(),'actual_pid':os.getpid(),'status':'PASS_INDEPENDENT_CONTROLS_WITH_TWO_MANDATORY_SOURCE_DEFECTS','predicate_count':count,'negative_controls':negative,'mandatory_source_witnesses':witnesses,'all4096_permission_patterns_checked':True,'actual_mode_observations':observations,'only_private_fixtures_written':True,'future_PR42_inventory_and_native_plans_are_synthetic_not_actual':True,'proposed_sources_imported_compiled_executed':False,'no_native_Git_remote_people_mutations':True,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'future_acceptance_APPROVED':False}
(H/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
