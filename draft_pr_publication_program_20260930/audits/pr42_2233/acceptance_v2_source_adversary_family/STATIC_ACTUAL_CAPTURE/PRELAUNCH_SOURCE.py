"""Independent byte/AST/real-filesystem audit. Never execute inspected sources."""
from pathlib import Path
import ast
import copy
import datetime as dt
import difflib
import hashlib
import json
import math
import os
import re
import stat
import subprocess
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2]
V=A/'acceptance_preparation_family_v2';O=A/'acceptance_preparation_family';C=A/'reviewed_candidate';W=A/'whole_current_source_first_family'
checks=[];reads=[];queries=[];mutants=[]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def demand(ok,message):
    if not ok:raise ValueError(message)
    checks.append(message)
def parse(raw):
    def pairs(items):
        out={}
        for key,value in items:
            if key in out:raise ValueError('Duplicate JSON key')
            out[key]=value
        return out
    def floating(s):
        v=float(s)
        if not math.isfinite(v):raise ValueError('Nonfinite JSON')
        return v
    return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('Nonfinite JSON')))
def typed_equal(left,right):
    if type(left) is not type(right):return False
    if type(left) is dict:return left.keys()==right.keys() and all(typed_equal(left[k],right[k]) for k in left)
    if type(left) is list:return len(left)==len(right) and all(typed_equal(x,y) for x,y in zip(left,right))
    return left==right
def observe(path,reason):
    p=Path(path);mode=os.lstat(p).st_mode
    demand(stat.S_ISREG(mode),'Actual regular file '+str(p))
    for ancestor in p.parents:demand(not ancestor.is_symlink(),'Real ancestor '+str(ancestor))
    raw=p.read_bytes();reads.append({'path':str(p),'bytes':len(raw),'sha256':sha(raw),'worktree_mode':stat.S_IMODE(mode),'reason':reason})
    if p.suffix=='.json':parse(raw)
    if p.suffix=='.jsonl':
        demand(not raw or raw.endswith(b'\n'),'Complete JSONL '+str(p))
        for line in raw.splitlines():parse(line)
    return raw
def bound(base,row,reason,frozen=False):
    demand(type(row['path']) is str and not Path(row['path']).is_absolute() and '..' not in Path(row['path']).parts,'Canonical relative bound row')
    raw=observe(base/row['path'],reason)
    n=row.get('bytes',row.get('size'))
    demand(type(n) is int and n>=0 and n==len(raw) and sha(raw)==row['sha256'],'Full independent row bytes/hash '+row['path'])
    if frozen:demand(stat.S_IMODE((base/row['path']).stat().st_mode)==0o444,'Literal complete0444 '+row['path'])
    return raw
def closure(root,name,pin,count):
    raw=observe(root/name,'closed manifest self');demand(sha(raw)==pin,'Exact closure pin '+str(root))
    o=parse(raw);demand(o['files_count']==count and type(o['files_count']) is int and o['self_excluded']==[name] and len(o['files'])==count,'Literal self-only count')
    names={z['path'] for z in o['files']};demand(len(names)==count and name not in names,'Unique self-excluding rows')
    wanted=names|{name};files=set();dirs=set()
    for p in root.rglob('*'):
        demand(not p.is_symlink(),'No closure symlink')
        n=p.relative_to(root).as_posix()
        if p.is_file():files.add(n)
        else:demand(p.is_dir(),'No closure special member');dirs.add(n)
    expected={p.as_posix() for n in wanted for p in Path(n).parents if p.as_posix()!='.'}
    demand(files==wanted and dirs==expected,'Exact files and directories '+str(root))
    demand(stat.S_IMODE((root/name).stat().st_mode)==0o444,'Self literal0444')
    for z in o['files']:bound(root,z,'closed member',True)
    return o
def resolve_inside(root,literal):
    root=Path(root)
    if type(literal) is not str or not literal.startswith(str(root)+'/') or '\\' in literal or '\0' in literal:raise ValueError('Literal scope/type')
    for parent in [root,*root.parents]:
        mode=os.lstat(parent).st_mode
        if not stat.S_ISDIR(mode) or stat.S_ISLNK(mode):raise ValueError('Real root ancestor')
    if root.resolve()!=root:raise ValueError('Root is alias')
    parts=literal[len(str(root))+1:].split('/')
    if any(not p or p in {'.git','__pycache__'} for p in parts):raise ValueError('Invalid component')
    stack=[]
    for p in parts:
        mode=os.lstat(root.joinpath(*stack)).st_mode
        if not stat.S_ISDIR(mode):raise ValueError('Not traversing real directory')
        if p=='.':continue
        if p=='..':
            if not stack:raise ValueError('Escape')
            stack.pop()
        else:stack.append(p)
        mode=os.lstat(root.joinpath(*stack)).st_mode
        if stat.S_ISLNK(mode):raise ValueError('Symlink hop')
    out=root.joinpath(*stack)
    if not stack or not stat.S_ISREG(os.lstat(out).st_mode):raise ValueError('Interior regular file')
    return out
def reject(label,call):
    try:call()
    except (ValueError,OSError,TypeError,KeyError):mutants.append(label)
    else:raise ValueError('Own control accepted forbidden mutant '+label)
def git_query(tail):
    argv=['git',*tail];start=dt.datetime.now(dt.timezone.utc).isoformat()
    proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    out,err=proc.communicate();finish=dt.datetime.now(dt.timezone.utc).isoformat();number=len(queries)
    G=H/'READONLY_GIT_CAPTURE';G.mkdir(exist_ok=True)
    streams={}
    for channel,raw in [('stdout',out),('stderr',err)]:
        name=str(number)+'_'+channel+'.bin';(G/name).write_bytes(raw);streams[channel]={'path':name,'bytes':len(raw),'sha256':sha(raw)}
    queries.append({'argv':argv,'cwd':str(R),'pid':proc.pid,'started_utc':start,'finished_utc':finish,'actual_execution':True,'completed':True,'exit_code':proc.returncode,'stdin_supplied':False,**streams})
    demand(proc.returncode==0,'Own actual read-only Git query')
    return out
assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
prep=closure(V,'PREPARATION_MANIFEST.json','f5cd2d41d448c97fcf160afeca63dc4c57c283deb03ffa4fe2292125db06b1a8',51)
old=closure(O,'PREPARATION_MANIFEST.json','48358afc32922caefd8cb0fad5a59c52352d86261c5da3429e33c627c8afbe31',27)
oldadv=closure(A/'acceptance_source_adversary_family','OWN_CLOSED_MANIFEST.json','a8dac6d97ef72071a03763b4ee1ed3ce873f8e241b1a14dd35af10e0445c7bef',18)
current=closure(C,'MANIFEST.json','09ac3a27edc2113da9574e57a13e7a0c99baa194fa50efb07548ec47fa7493de',385)
deps=parse(observe(C/'CURRENT_DEPENDENCIES.json','portable dependencies'));demand(len(deps['files'])==517,'Exact517 dependency rows')
for z in deps['files']:bound(A,z,'portable complete dependency')
whole=closure(W,'OWN_CLOSED_MANIFEST.json','8cf1878a94133feb6a68d757481978630114262c0490451b54176395fc4ec0fe',25)
inputs=parse(observe(V/'INPUT_BINDINGS.json','V2 inputs'))
for z in inputs['pins'].values():bound(R,z,'V2 complete input pin')
for n in ['closed_whole_manifest','closed_whole_result','closed_whole_report','closed_root_whole_inspection','root_capture_operator']:bound(R,inputs[n],'V2 exact whole/root/operator reference')
whole_result=parse(observe(R/inputs['closed_whole_result']['path'],'whole exact RESULT'));root_result=parse(observe(R/inputs['closed_root_whole_inspection']['path'],'ROOT whole exact read'))
demand(typed_equal(root_result['complete_RESULT_object'],whole_result) and root_result['future_execution_approved'] is False,'Actual entire whole RESULT equals genuine ROOT inspection')
demand(whole_result['mandatory_defects']==whole_result['mandatory_corrections']==[] and whole_result['full_problem_solved'] is False,'Scoped clean whole result only')
freeze=parse(observe(A/'root_current_freeze_actual_capture/CAPTURE.json','actual historical freeze'))
dated='c61dc0cb572de281b871264819c8b80d647d0373'
demand(freeze['main_head_before']==freeze['main_head_after']==dated and typed_equal(freeze['native13_before'],freeze['native13_after']),'Actual unchanged dated13 freeze')
rows13={z['path']:z for z in freeze['native13_before']};demand(len(rows13)==13,'Exact dated13')
historic={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
dated_bodies={}
for n in sorted(historic):
    entries=git_query(['ls-tree','-z',dated,'--',n]).decode().split('\0');demand(len(entries)==2 and entries[-1]=='','Exact historical tree entry')
    fields,name=entries[0].split('\t');mode,kind,blob=fields.split();demand(name==n and mode=='100644' and kind=='blob','Regular historical native100644')
    raw=git_query(['show',dated+':'+n]);z=rows13[n];demand(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Entire dated Git body equals actual freeze13')
    dated_bodies[n]=raw
foreign=whole['foreign_files_individually_pinned_and_excluded'];demand(len(foreign)==925,'Full925 individually inspected')
literal=set();canon=set();aliases=[];old_seen=set();live_count=0
for z in foreign:
    demand(set(z)=={'path','bytes','sha256','classification'} and z['path'] not in literal,'Exact distinct whole foreign row');literal.add(z['path'])
    p=resolve_inside(R,z['path']);n=p.relative_to(R).as_posix();canon.add(n)
    if '/../' in z['path']:aliases.append({'literal':z['path'],'canonical':str(p),'bytes':z['bytes'],'sha256':z['sha256']})
    if n in historic:
        demand(z['bytes']==rows13[n]['bytes'] and z['sha256']==rows13[n]['sha256'],'Historical whole row equals genuine freeze row')
        raw=dated_bodies[n];old_seen.add(n)
        reads.append({'path':z['path'],'canonical':str(p),'bytes':len(raw),'sha256':sha(raw),'authority':'immutable_Git_'+dated,'reason':'whole historical row'})
    else:raw=observe(p,'whole individual live foreign row');live_count+=1
    demand(type(z['bytes']) is int and z['bytes']==len(raw) and z['sha256']==sha(raw),'Entire exact whole foreign body')
demand(len(literal)==925 and len(aliases)==3 and old_seen==historic and live_count==921,'Exact925 identities/3 aliases/4 historical/921 live')
demand({Path(z['canonical']).name for z in aliases}=={'snapshot_manifest_v2.json','pinned_problem.json','pinned_prior_report.json'},'Three actual aliases independently resolved')
latest=git_query(['rev-parse','HEAD']).decode().strip();branch=git_query(['branch','--show-current']).decode().strip();demand(branch=='main','Remain main')
demand((R/'unsolved_math_prioritization/QUEUE.md').read_bytes()!=dated_bodies['unsolved_math_prioritization/QUEUE.md'],'Historical queue is distinct from legitimate fresh current queue')
for n in ['seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','SCIENTIFIC_SCOPE.json','CLOSED_WHOLE_RESULT_KEYS.json']:
    demand((V/n).read_bytes()==(O/n).read_bytes(),'Unrelated helper/authority/science unchanged '+n)
oldtree=ast.parse((O/'pr42_guards.py').read_text());newtree=ast.parse((V/'pr42_guards.py').read_text())
functions=lambda t:{n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,ast.FunctionDef)}
of,nf=functions(oldtree),functions(newtree);demand(set(nf)==set(of)|{'resolve_foreign_literal'},'Exact one new resolver')
for n in of:
    if n!='basis':demand(of[n]==nf[n],'Unchanged whole original guard function '+n)
delta=''.join(difflib.unified_diff((O/'pr42_guards.py').read_text().splitlines(True),(V/'pr42_guards.py').read_text().splitlines(True),fromfile='preserved_V1/pr42_guards.py',tofile='adjacent_V2/pr42_guards.py'))
demand(delta.encode()==(V/'SOURCE_REPAIR_DELTA.patch').read_bytes(),'Exact full source delta')
for p in V.rglob('*.py'):
    ast.parse(p.read_text());demand(True,'Syntax parse without compile/import '+str(p))
for label in ['AUTHORING_ACTUAL_CAPTURE','DATED_NATIVE_REVISION_ACTUAL_CAPTURE','CONTROLS_ACTUAL_CAPTURE']:
    rec=parse((V/label/'CAPTURE.json').read_bytes());demand(type(rec['pid']) is int and rec['pid']>0 and rec['exit_code']==0 and rec['completed'] is True,'Actual own prep child')
    demand(sha((V/label/'PRELAUNCH_SOURCE.py').read_bytes())==rec['source_sha256'],'Actual prep prelaunch source')
    for n in ['stdout','stderr']:bound(V/label,rec[n],'actual complete prep stream')
    demand(dt.datetime.fromisoformat(rec['started_utc'])<=dt.datetime.fromisoformat(rec['finished_utc']),'Actual prep clock order')
for z in parse((V/'DATED_GIT_NATIVE4_ACTUAL_QUERY_CAPTURE/QUERY_RECEIPTS.json').read_bytes())['queries']:
    demand(z['completed'] is True and z['exit_code']==0 and type(z['pid']) is int,'Actual dated read-only Git child')
    for n in ['stdout','stderr']:bound(V/'DATED_GIT_NATIVE4_ACTUAL_QUERY_CAPTURE',z[n],'actual prep complete dated Git stream')
failed=parse(observe(A/'root_final_reconciliation_actual_capture/CAPTURE.json','retained actual failure'))
demand(failed['pid']==97064 and failed['exit_code']==1 and failed['status']=='FAIL','Meaningful original sealer failure retained')
for n in ['stdout','stderr']:bound(A/'root_final_reconciliation_actual_capture',failed[n],'retained failed stream')
demand(b'Noncanonical relative path' in (A/'root_final_reconciliation_actual_capture/stderr.bin').read_bytes(),'Actual original literal path failure')
original=parse(observe(A/'snapshot_manifest_v2.json','original snapshot'))
for z in original['files']:
    demand(bound(A/'source_snapshot_v2',z,'original17')==bound(C/'original_archive',z,'actual original archive17'),'Exact original archive member')
ledger=(C/'turns.jsonl').read_bytes();demand(sha(ledger)=='60d0413980ac5f251913a26298692c5efc797d8f5084ca03e8d134472ab820e4','Exact unchanged original2 ledger')
objects=[parse(line) for line in ledger.splitlines()];demand([z['turn'] for z in objects]==[1,2] and all(type(z['turn']) is int for z in objects),'Two typed ordered original turns')
previous=parse(observe(R/inputs['pins']['previous/state_mirror_bindings.json']['path'],'actual prior proposal'))
demand(len(previous['entries'])==31 and len(previous['duplicate_mirrors'])==1,'Actual31 primary/one existing duplicate')
for e in previous['entries']:
    budget=e['budget'];demand(type(budget['used']) is int and type(budget['limit']) is int and 0<=budget['used']<=budget['limit'],'Typed prior budget')
    raw=observe(R/budget['ledger']['path'],'complete original prior ledger');demand(sha(raw)==budget['ledger']['sha256'],'Exact prior ledger bytes')
native=observe(R/'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py','bound native source read only')
demand(sha(native)=='ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f','Exact reviewed native module')
operator=observe(A/'capture_root_final_operation_v2.py','actual ROOT operator read only');demand(sha(operator)=='48e5e5ccbd68ddbc4dc6c661a306003902dfb856a3bcdb0061278cb51749e5c2','Exact new ROOT operator')
draft=parse((V/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json').read_bytes());plan=parse((V/'DRAFT_FINAL_PLAN.json').read_bytes())
demand(all(draft[n] is False for n in ['root_full_current_read_completed','root_full_whole_read_completed','root_acceptance_source_review_completed','independent_whole_current_pass']) and draft['root_capture_operator'] is None and plan['partial_valid'] is None,'No V2 future ROOT approval inherited')
# Private filesystem is wholly inside our own new family; no source fixture is altered.
F=H/'PRIVATE_PATH_CONTROLS';F.mkdir();(F/'sub').mkdir();(F/'file').write_bytes(b'private bound body');(F/'sub'/'nested').mkdir();(F/'link').symlink_to(F/'file');(F/'sub'/'dirlink').symlink_to(F/'sub',target_is_directory=True)
positive=[str(F)+'/file',str(F)+'/sub/../file',str(F)+'/sub/nested/../../file',str(F)+'/./file']
for literal_path in positive:demand(resolve_inside(F,literal_path)==F/'file','Own actual safe alias resolution')
bad={'escape-return':str(F)+'/../'+F.name+'/file','symlink-final':str(F)+'/link','symlink-hop-cancel':str(F)+'/sub/dirlink/../../file','file-hop':str(F)+'/file/../file','missing-hop':str(F)+'/missing/../file','double-slash':str(F)+'//file','private-git':str(F)+'/.git/file','root-end':str(F)+'/sub/..','backslash':str(F)+'/sub\\file','NUL':str(F)+'/file\0','outside-prefix':str(F.parent)+'/file'}
for label,value in bad.items():reject(label,lambda value=value:resolve_inside(F,value))
for value in [True,None,12]:reject('nonstring-path-'+repr(value),lambda value=value:resolve_inside(F,value))
# Retain only authored real regular files; symlinks are finite probes, recorded, then removed.
(F/'link').unlink();(F/'sub'/'dirlink').unlink();(F/'sub'/'nested').rmdir();(F/'sub').rmdir()
mode_file=F/'file';mode_observations=[]
for mode in [0o444,0o1444,0o2444,0o4444]:
    mode_file.chmod(mode);actual=stat.S_IMODE(mode_file.stat().st_mode);demand(actual==mode,'Actual full mode including special bits');mode_observations.append({'requested':mode,'actual':actual,'literal0444':actual==0o444})
mode_file.chmod(0o444)
for mode in range(0o10000):demand((mode==0o444)==((mode&0o7777)==0o444),'Exhaustive full mode predicate')
def strict_record(got,expected):
    if not typed_equal(got,expected):raise ValueError('Complete typed expected record mismatch')
for label,field,value in [('boolean-turn-count','original_substantive_attempts',True),('full-solution','full_problem_solved',True),('invented-model','current_model','invented'),('wrong-percentage-type','turn_limit',5.0)]:reject(label,lambda field=field,value=value:strict_record({**plan,field:value},plan))
reject('unknown-authority-field',lambda:strict_record({**draft,'future_runtime_PASS':True},draft))
reject('missing-authority-field',lambda:strict_record({k:v for k,v in draft.items() if k!='root_full_whole_read_completed'},draft))
reject('duplicate-JSON-key',lambda:parse(b'{"a":1,"a":2}'))
reject('nonfinite-JSON',lambda:parse(b'{"a":1e999}'))
reject('NaN-JSON',lambda:parse(b'{"a":NaN}'))
ledger_expected=copy.deepcopy(objects)
for name in ['bool','phantom','missing','reverse','extra']:
    mutant=copy.deepcopy(objects)
    if name=='bool':mutant[0]['turn']=True
    if name=='phantom':mutant.append({'turn':3})
    if name=='missing':mutant.pop()
    if name=='reverse':mutant.reverse()
    if name=='extra':mutant[0]['extra']=None
    reject('exact-ledger-'+name,lambda mutant=mutant:strict_record(mutant,ledger_expected))
inventory=parse(dated_bodies['draft_pr_publication_program_20260930/inventory.json']);chosen=next(z for z in inventory['items'] if z['number']==42)
demand(type(inventory['completed_count']) is int and inventory['completed_count']==31 and sum(z.get('stage')=='complete' for z in inventory['items'])==31,'Actual31 original inventory completions')
prospective=copy.deepcopy(inventory);selected=next(z for z in prospective['items'] if z['number']==42);selected.update(stage='complete',workflow_completion_estimate_percent=100)
prospective.update(completed_count=32,program_completion_estimate_percent=32/180*100,completion_estimate_percent=32/180*100,current_pr=43)
demand(type(selected['workflow_completion_estimate_percent']) is int and type(prospective['program_completion_estimate_percent']) is float,'Integer workflow/float fractional program model')
demand(all(typed_equal(x,y) for x,y in zip(inventory['items'],prospective['items']) if x['number']!=42),'Other179 inventory objects exact')
for value in [True,32.0]:reject('bool-or-float-integer-count-'+repr(value),lambda value=value:strict_record({**prospective,'completed_count':value},prospective))
def utc(value):
    if type(value) is not str:raise ValueError('UTC string required')
    clock=dt.datetime.fromisoformat(value[:-1]+'+00:00' if value.endswith('Z') else value)
    if clock.tzinfo is None or clock.utcoffset()!=dt.timedelta(0):raise ValueError('Aware UTC required')
    return clock
for value in [None,True,'2026-10-03T01:00:00','2026-10-03T01:00:00-07:00']:reject('clock-'+repr(value),lambda value=value:utc(value))
demand(utc('2026-10-03T01:00:00Z')==utc('2026-10-03T01:00:00+00:00'),'UTC equivalent finite clocks')
(H/'READONLY_GIT_CAPTURE/QUERIES.json').write_text(json.dumps({'schema':'PR42_V2_NEW_ADVERSARY_ACTUAL_READONLY_GIT_v1','actual_parent_pid':os.getpid(),'queries':queries},indent=2)+'\n')
(H/'INDIVIDUAL_INPUT_READS.json').write_text(json.dumps({'schema':'PR42_V2_NEW_ADVERSARY_FULL_INDIVIDUAL_READS_v1','files':reads},indent=2)+'\n')
result={'schema':'PR42_V2_NEW_DIFFERENT_SOURCE_ADVERSARY_OWN_CONTROL_v1','status':'PASS_OWN_SOURCE_ONLY_INDEPENDENT_CONTROLS','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'demands':len(checks),'individual_read_rows':len(reads),'total_bound_input_bytes':sum(z['bytes'] for z in reads),'preparation_members':51,'current_members':385,'dependency_rows':517,'whole_owned_members':25,'whole_foreign_rows':925,'actual_aliases':aliases,'historical_native_rows':4,'other_live_whole_rows':921,'canonical_foreign_identities':len(canon),'rejected_mutants':mutants,'actual_mode_observations':mode_observations,'observed_main':latest,'read_only_git_pids':[z['pid'] for z in queries],'proposed_native_candidate_helpers_imported_compiled_executed':False,'root_approval_authored':False,'future_runtime_or_acceptance_certified':False,'native_Git_remote_people_mutations':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'novelty_claimed':False,'limitations':'Only independently handwritten byte, AST and finite real-filesystem/type/mode checks ran; source parsing is not compilation or runtime validation of production.'}
(H/'CONTROL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
