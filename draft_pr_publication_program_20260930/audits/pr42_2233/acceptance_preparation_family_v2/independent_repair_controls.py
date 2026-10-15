"""Own independent literal-path/historical-source models; proposed helpers never execute."""
from pathlib import Path
import ast,copy,datetime as dt,hashlib,json,os,stat,subprocess
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2];OLD=A/'acceptance_preparation_family'
checks=[];rejections=[]
def demand(ok,label):
    if not ok:raise ValueError(label)
    checks.append(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def expect_reject(label,call):
    try:call()
    except (ValueError,FileNotFoundError,NotADirectoryError):rejections.append(label)
    else:raise ValueError('Accepted forbidden control: '+label)
def resolve_actual(literal):
    if type(literal) is not str or not literal.startswith(str(R)+'/') or '\\' in literal or '\0' in literal:raise ValueError('Scope/type')
    if R.resolve()!=R:raise ValueError('Root alias')
    for node in [R,*R.parents]:
        mode=os.lstat(node).st_mode
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):raise ValueError('Root ancestor')
    stack=[];tail=literal[len(str(R))+1:].split('/')
    if any(not p or p in {'.git','__pycache__'} for p in tail):raise ValueError('Component')
    for word in tail:
        current=R.joinpath(*stack)
        mode=os.lstat(current).st_mode
        if not stat.S_ISDIR(mode) or stat.S_ISLNK(mode):raise ValueError('Traversed parent')
        if word=='.':continue
        if word=='..':
            if not stack:raise ValueError('Escape')
            stack.pop()
        else:stack.append(word)
        mode=os.lstat(R.joinpath(*stack)).st_mode
        if stat.S_ISLNK(mode):raise ValueError('Symlink hop')
    current=R.joinpath(*stack);mode=os.lstat(current).st_mode
    if not stack or not stat.S_ISREG(mode):raise ValueError('Regular interior file')
    return current
def row_model(z,nodes):
    if type(z) is not dict or set(z)!={'path','bytes','sha256','classification'}:raise ValueError('Complete row schema')
    if type(z['bytes']) is not int or z['bytes']<0:raise ValueError('Typed bytes')
    if type(z['sha256']) is not str or len(z['sha256'])!=64 or any(c not in '0123456789abcdef' for c in z['sha256']):raise ValueError('Digest')
    if type(z['classification']) is not str:raise ValueError('Classification')
    name=z['path']
    if type(name) is not str or not name.startswith('/repo/') or '\\' in name or '\0' in name:raise ValueError('Literal scope')
    stack=[]
    parts=name[len('/repo/'):].split('/')
    if any(not p or p in {'.git','__pycache__'} for p in parts):raise ValueError('Component')
    for p in parts:
        current='/repo'+(' /' if False else '')+('/'+'/'.join(stack) if stack else '')
        if nodes.get(current)!='dir':raise ValueError('Real traversed directory')
        if p=='.':continue
        if p=='..':
            if not stack:raise ValueError('Escape')
            stack.pop()
        else:stack.append(p)
        current='/repo'+('/'+'/'.join(stack) if stack else '')
        if current not in nodes or nodes[current]=='symlink':raise ValueError('Missing/symlink hop')
    current='/repo'+('/'+'/'.join(stack) if stack else '')
    if not stack or nodes.get(current)!='regular':raise ValueError('Interior regular file')
    return current
def row_list_model(rr,nodes):
    seen=set();out=[]
    for z in rr:
        if z['path'] in seen:raise ValueError('Duplicate literal identity')
        seen.add(z['path']);out.append(row_model(z,nodes))
    return out
def bound_rows(base,rr,frozen=False):
    for z in rr:
        p=base/z['path'];raw=p.read_bytes();size=z.get('bytes',z.get('size'))
        demand(p.is_file() and not p.is_symlink() and type(size) is int and len(raw)==size and sha(raw)==z['sha256'],'Exact complete bound row '+str(p))
        if frozen:demand(stat.S_IMODE(p.stat().st_mode)==0o444,'Complete preserved0444 '+str(p))
def closed(root,name,pin):
    raw=(root/name).read_bytes();demand(sha(raw)==pin,'Preserved actual closure '+str(root));o=json.loads(raw);bound_rows(root,o['files'],True)
    demand({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}=={z['path'] for z in o['files']}|{name},'Exact preserved files '+str(root))
    demand(stat.S_IMODE((root/name).stat().st_mode)==0o444,'Preserved literal self mode '+str(root));return o
inputs=load(H/'INPUT_BINDINGS.json');repair=load(H/'REPAIR_INPUTS.json')
old=closed(OLD,'PREPARATION_MANIFEST.json',repair['old_preparation_manifest']['sha256'])
oldadv=closed(A/'acceptance_source_adversary_family','OWN_CLOSED_MANIFEST.json',repair['old_adversary_manifest']['sha256'])
bound_rows(R,list(inputs['pins'].values()))
C=A/'reviewed_candidate';W=A/'whole_current_source_first_family'
current=closed(C,'MANIFEST.json',inputs['current_manifest_sha256']);demand(len(current['files'])==385,'Unchanged actual current385')
deps=load(C/'CURRENT_DEPENDENCIES.json');demand(len(deps['files'])==517 and sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())==inputs['current_dependencies_sha256'],'Unchanged complete dependency517');bound_rows(A,deps['files'])
whole=closed(W,'OWN_CLOSED_MANIFEST.json',inputs['closed_whole_manifest']['sha256']);foreign=whole['foreign_files_individually_pinned_and_excluded'];demand(len(whole['files'])==25 and len(foreign)==925,'Unchanged whole25+925')
for n in ['closed_whole_result','closed_whole_report','closed_root_whole_inspection','root_capture_operator']:bound_rows(R,[inputs[n]])
demand(inputs['root_capture_operator']['path'].endswith('/capture_root_final_operation_v2.py') and inputs['root_capture_operator']['sha256']=='48e5e5ccbd68ddbc4dc6c661a306003902dfb856a3bcdb0061278cb51749e5c2','Actual separately authored V2 ROOT operator')
failed=load(A/'root_final_reconciliation_actual_capture/CAPTURE.json');demand(failed['pid']==97064 and failed['status']=='FAIL' and failed['exit_code']==1,'Actual meaningful V1 failed sealer retained')
demand('Noncanonical relative path' in (A/'root_final_reconciliation_actual_capture/stderr.bin').read_text(),'Exact V1 literal-alias failure retained')
dated=load(A/'root_current_freeze_actual_capture/CAPTURE.json');dated_head=dated['main_head_before'];demand(dated_head==dated['main_head_after']=='c61dc0cb572de281b871264819c8b80d647d0373','Actual dated Git anchor')
dated_rows={z['path']:z for z in dated['native13_before']};demand(len(dated_rows)==13 and dated['native13_before']==dated['native13_after'],'Actual complete dated13')
historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
G=H/'DATED_GIT_NATIVE4_ACTUAL_QUERY_CAPTURE';G.mkdir(exist_ok=False);records=[];git_raw={}
def git_query(tail):
    number=len(records);argv=['git',*tail];start=dt.datetime.now(dt.timezone.utc).isoformat()
    proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'});out,err=proc.communicate();finish=dt.datetime.now(dt.timezone.utc).isoformat()
    streams=[]
    for channel,raw in [('stdout',out),('stderr',err)]:
        name=str(number)+'_'+channel+'.bin';(G/name).write_bytes(raw);streams.append({'path':name,'bytes':len(raw),'sha256':sha(raw)})
    records.append({'argv':argv,'cwd':str(R),'actual_execution':True,'completed':True,'pid':proc.pid,'started_utc':start,'finished_utc':finish,'exit_code':proc.returncode,'stdout':streams[0],'stderr':streams[1],'stdin_supplied':False})
    if proc.returncode:raise ValueError('Read-only actual Git query failed')
    return out
for n in sorted(historical):
    entry=git_query(['ls-tree','-z',dated_head,'--',n]).decode().split('\0');demand(len(entry)==2 and entry[-1]=='','Exactly one historical Git tree row '+n)
    fields,literal=entry[0].split('\t');mode,kind,blob=fields.split();demand(mode=='100644' and kind=='blob' and literal==n,'Exact dated regular tracked100644 '+n)
    git_raw[n]=git_query(['show',dated_head+':'+n]);z=dated_rows[n];demand(len(git_raw[n])==z['bytes'] and sha(git_raw[n])==z['sha256'],'Entire actual immutable Git body equals actual freeze row '+n)
(G/'QUERY_RECEIPTS.json').write_text(json.dumps({'schema':'pr42-own-readonly-dated-git-query-capture/v1','actual_parent_pid':os.getpid(),'queries':records,'native_Git_remote_mutations':False},indent=2)+'\n')
literal_seen=set();canonical_seen=set();aliases=[];checked_old=set()
for z in foreign:
    demand(set(z)=={'path','bytes','sha256','classification'} and type(z['path']) is str and z['path'] not in literal_seen,'Complete distinct original literal identity');literal_seen.add(z['path'])
    p=resolve_actual(z['path']);n=p.relative_to(R).as_posix();canonical_seen.add(n)
    if '/../' in z['path']:aliases.append({'literal':z['path'],'canonical':str(p),'bytes':z['bytes'],'sha256':z['sha256']})
    if n in historical:
        demand(z['bytes']==dated_rows[n]['bytes'] and z['sha256']==dated_rows[n]['sha256'],'Exact archived row equals dated capture');raw=git_raw[n];checked_old.add(n)
    else:raw=p.read_bytes()
    demand(type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'All925 exact individual old/live bytes '+z['path'])
demand(len(literal_seen)==925 and checked_old==historical and len(aliases)==3,'Exact925/literal aliases3/historical4 verified')
demand({Path(z['canonical']).name for z in aliases}=={'snapshot_manifest_v2.json','pinned_problem.json','pinned_prior_report.json'},'All three actual archived aliases, no guessed identity')
live_queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();demand(live_queue!=git_raw['unsolved_math_prioritization/QUEUE.md'],'Legitimate fresh queue differs from old dated whole row')
for n in ['seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','SCIENTIFIC_SCOPE.json','CLOSED_WHOLE_RESULT_KEYS.json']:
    demand((H/n).read_bytes()==(OLD/n).read_bytes(),'Unrelated source/schema/science byte unchanged '+n)
old_ast=ast.parse((OLD/'pr42_guards.py').read_text());new_ast=ast.parse((H/'pr42_guards.py').read_text())
functions=lambda tree:{x.name:ast.dump(x,include_attributes=False) for x in tree.body if isinstance(x,ast.FunctionDef)}
old_functions=functions(old_ast);new_functions=functions(new_ast)
demand(set(new_functions)==set(old_functions)|{'resolve_foreign_literal'},'Only new foreign resolver function')
for n in old_functions:
    if n!='basis':demand(old_functions[n]==new_functions[n],'Other complete guard unchanged '+n)
for n in ['pr42_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']:demand(isinstance(ast.parse((H/n).read_text()),ast.Module),'Syntax inspection only '+n)
source=(H/'pr42_guards.py').read_text();demand('literal_names.add(z[\'path\'])' in source and "canonical=resolve_foreign_literal(z['path'])" in source and "raw=git_bytes('show',dated_head+':'+n)" in source,'Explicit preserved literal identity/canonical mapping/dated Git source')
demand('p=regular(A,historical[n])' not in source and "if n in historical:" in source,'Historic four do not use future current preflight bytes')
nodes={'/repo':'dir','/repo/A':'dir','/repo/file':'regular','/repo/A/link':'symlink','/repo/link':'symlink','/repo/native':'dir','/repo/native/sub':'dir','/repo/native/state':'regular'}
row={'path':'/repo/A/../file','bytes':3,'sha256':'a'*64,'classification':'private model only'}
demand(row_model(row,nodes)=='/repo/file','Private safe parent alias')
direct={**row,'path':'/repo/file'};demand(row_list_model([row,direct],nodes)==['/repo/file','/repo/file'],'Distinct literal canonical alias duplication allowed')
expect_reject('duplicate-literal',lambda:row_list_model([row,row],nodes))
for name,path in [('outside-prefix','/outside/file'),('outside-escape','/repo/../outside/file'),('escape-return','/repo/../repo/file'),('symlink-cancel','/repo/A/link/../file'),('symlink-final','/repo/link'),('missing-cancel','/repo/missing/../file'),('empty-component','/repo//file'),('private-git','/repo/.git/file'),('backslash','/repo/A\\file'),('NUL','/repo/file\0')]:expect_reject(name,lambda path=path:row_model({**row,'path':path},nodes))
for name,field,value in [('bool-path','path',True),('bool-bytes','bytes',True),('negative-bytes','bytes',-1),('null-digest','sha256',None),('uppercase-digest','sha256','A'*64),('bool-classification','classification',True)]:expect_reject(name,lambda field=field,value=value:row_model({**row,field:value},nodes))
expect_reject('unknown-row-scope',lambda:row_model({**row,'human_peer_review':True},nodes))
expect_reject('missing-row-field',lambda:row_model({k:v for k,v in row.items() if k!='bytes'},nodes))
native_alias={**row,'path':'/repo/native/sub/../state'};demand(row_model(native_alias,nodes)=='/repo/native/state','Canonical identity selects historical native mapping')
old_bytes=b'old historical bytes';new_bytes=b'fresh current bytes';reference=sha(old_bytes)
demand(sha(old_bytes)==reference and sha(new_bytes)!=reference,'Historical/fresh distinct byte authority')
def select_bytes(name):return old_bytes if name in {'native4'} else new_bytes
demand(sha(select_bytes('native4'))==reference,'Exact four dated model admitted')
expect_reject('unrelated-live-drift-not-exempt',lambda:(_ for _ in ()).throw(ValueError('Live mismatch')) if sha(select_bytes('unrelated'))!=reference else None)
draft=load(H/'DRAFT_FINAL_PLAN.json');bind=load(H/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
demand(draft['partial_valid'] is None and draft['root_acceptance_source_review_completed'] is False and draft['root_full_whole_read_completed'] is False and bind['root_capture_operator'] is None,'Fresh V2 ROOT flags/references false/null')
for field,value in [('original_substantive_attempts',True),('full_problem_solved',True),('current_model','invented')]:
    mutant={**draft,field:value};demand(not equal(mutant,draft),'Typed full scope mutant '+field)
result={'schema':'pr42-v2-own-independent-repair-controls/v1','status':'PASS_OWN_SOURCE_ONLY_REPAIR_CONTROLS','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'demands':len(checks),'rejected_mutants':rejections,'literal_foreign_rows':len(literal_seen),'canonical_foreign_identities':len(canonical_seen),'actual_literal_aliases':aliases,'historical_native_git_rows':len(checked_old),'other_foreign_rows_checked_live':len(foreign)-len(checked_old),'actual_readonly_Git_query_PIDs':[z['pid'] for z in records],'proposed_helpers_imported_compiled_executed':False,'old_source_PASS_transferred':False,'native_Git_remote_people_mutation':False,'limitations':'Own handwritten resolver/virtual filesystem/typed scope models and syntax inspection do not execute proposed helpers; new independent source adversary and ROOT personal read required.'}
(H/'OWN_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
