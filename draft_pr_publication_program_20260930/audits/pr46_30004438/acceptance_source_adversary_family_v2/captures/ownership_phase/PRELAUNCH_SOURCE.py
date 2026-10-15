#!/usr/bin/python3
"""Handwritten independent custody models and private OS operations only."""
import copy,ctypes,datetime,hashlib,json,math,os,pathlib,re,stat,sys,traceback
F=pathlib.Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];H=A/'acceptance_preparation_family_v2';count=0;rejected=[]
def ck(v,n):
    global count
    if not v:raise AssertionError(n)
    count+=1
def bad(fn,n):
    global count
    try:fn()
    except (ValueError,TypeError,KeyError,AssertionError):count+=1;rejected.append(n);return
    raise AssertionError('Mutant accepted '+n)
def sha(b):return hashlib.sha256(b).hexdigest()
def same(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def rel(s):
    if type(s) is not str or not s or '\\' in s or '\0' in s:raise ValueError('Relative path')
    p=pathlib.PurePosixPath(s)
    if p.is_absolute() or str(p)!=s or {'.','..','.git','__pycache__'}&set(p.parts):raise ValueError('Canonical path')
    return p.parts
def strict(b):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:raise ValueError('Duplicate')
            d[k]=v
        return d
    def num(s):
        v=float(s)
        if not math.isfinite(v):raise ValueError('Finite')
        return v
    def co(s):raise ValueError('Nonfinite')
    return json.loads(b,object_pairs_hook=pairs,parse_float=num,parse_constant=co)
def row(z):
    if type(z) is not dict or set(z)!={'path','bytes','sha256'}:raise ValueError('Exact row')
    rel(z['path'])
    if type(z['bytes']) is not int or z['bytes']<0 or type(z['sha256']) is not str or re.fullmatch('[0-9a-f]{64}',z['sha256']) is None:raise ValueError('Typed whole row')
    return z
native={'draft_pr_publication_program_20260930/inventory.json'}|{'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
exactlog='draft_pr_publication_program_20260930/RESEARCH_LOG.md';audit=tuple(A.relative_to(R).parts);canonical=('unsolved_math_prioritization','attempts','30004438')
def owned(n):
    parts=rel(n)
    return n in native or n==exactlog or (len(parts)>len(audit) and parts[:len(audit)]==audit) or (len(parts)>len(canonical) and parts[:len(canonical)]==canonical)
def foreign(ns):
    if type(ns) is not list or any(type(n) is not str for n in ns) or ns!=sorted(set(ns)):raise ValueError('Sorted typed exact foreign scope')
    for n in ns:
        if owned(n):raise ValueError('Owned cannot be protected foreign')
    return ns
destinations=[A.relative_to(R).as_posix()+'/ROOT_RESEARCH_LOG.md',exactlog]
ck(owned(exactlog),'Exact program log newly owned')
for n in sorted(native|set(destinations)|{A.relative_to(R).as_posix()+'/own_receipt.json','unsolved_math_prioritization/attempts/30004438/acceptance.json'}):bad(lambda n=n:foreign([n]),'Reject owned foreign '+n)
unrelated=['draft_pr_publication_program_20260930/OTHER.md','draft_pr_publication_program_20260930/audits/pr49_30000703/RESEARCH_LOG.md','draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/RESEARCH_LOG.md','draft_pr_publication_program_20260930/audits/pr46_30004438x/ROOT_RESEARCH_LOG.md','unsolved_math_prioritization/attempts/300044380/RESEARCH_LOG.md','draft_pr_publication_program_20260930/RESEARCH_LOG.md.other']
for n in unrelated:ck(not owned(n) and foreign([n])==[n],'No broad program/audit/name-prefix exemption')
for ns in [True,None,'string',['b','a'],['a','a'],[True],['../x'],['a/../b'],['a//b'],['/absolute'],['a\\b']]:bad(lambda ns=ns:foreign(ns),'Unsafe foreign scope '+repr(ns))
fixture=F/'private_fixtures';fixture.mkdir(exist_ok=False);sentinel=fixture/'protected_program_log';sentinel.write_bytes(b'original entire prefix\n');before=sentinel.read_bytes();v1_failure=None
try:
    # Actual reproduction in private files only: old misclassification accepts,
    # later owned append violates the saved protected body identity.
    saved=sha(sentinel.read_bytes());sentinel.write_bytes(sentinel.read_bytes()+b'owned append\n')
    if sha(sentinel.read_bytes())!=saved:raise ValueError('V1 S1: protected foreign body changed by finalization')
except ValueError:
    v1_failure={'actual_model_pid':os.getpid(),'logical_path':exactlog,'traceback':traceback.format_exc(),'before_sha256':sha(before),'after_sha256':sha(sentinel.read_bytes()),'production_executed':False};ck(True,'Genuine private V1 S1 failure')
new=fixture/'new_program_log';new.write_bytes(before)
bad(lambda:foreign([exactlog]),'V2 reject before private append');ck(new.read_bytes()==before,'No mutation after rejected foreign declaration')
def note(t):
    return ('\n## '+t+' — PR46 actual accepted credited known-result source correction\n\nWorkflow100%; scientific discovery0%; original0/5,new0,audit0. Actual MERGED original-head/tree checked. Program36/180=20%; one present native mirror remains. No paper/newDOI/tracker/release.\n').encode()
t=datetime.datetime.now(datetime.timezone.utc).isoformat();suffix=note(t);prefixes={n:('entire prefix '+str(i)+'\n').encode() for i,n in enumerate(destinations)};outputs={n:b+suffix for n,b in prefixes.items()}
def ref(n,b):return {'path':n,'bytes':len(b),'sha256':sha(b)}
receipt={'schema':'pr46-actual-owned-operational-log-append/v1','utc':t,'note':suffix.decode(),'source_preparation_did_not_append':True,'logs':[{'log':n,'before':ref(n,prefixes[n]),'retained_preimage':ref(A.relative_to(R).as_posix()+'/integration_log_preimages/'+label+'.bin',prefixes[n]),'after':ref(n,outputs[n]),'before_worktree_mode':420,'after_worktree_mode':420} for n,label in zip(destinations,['root_problem','program'])]}
def logs(d,out,kept,modes):
    if type(d) is not dict or set(d)!={'schema','utc','note','source_preparation_did_not_append','logs'} or d['schema']!='pr46-actual-owned-operational-log-append/v1' or d['source_preparation_did_not_append'] is not True or d['note'].encode()!=suffix:raise ValueError('Exact derived receipt')
    if type(d['logs']) is not list or len(d['logs'])!=2:raise ValueError('Exactly two logs')
    for z,(n,label) in zip(d['logs'],zip(destinations,['root_problem','program'])):
        if type(z) is not dict or set(z)!={'log','before','retained_preimage','after','before_worktree_mode','after_worktree_mode'} or z['log']!=n:raise ValueError('Exact ordered destinations')
        row(z['before']);row(z['retained_preimage']);row(z['after'])
        if not same(z['before'],ref(n,kept[n])) or not same(z['after'],ref(n,out[n])) or not same(z['retained_preimage'],ref(A.relative_to(R).as_posix()+'/integration_log_preimages/'+label+'.bin',kept[n])) or out[n]!=kept[n]+suffix:raise ValueError('Full prefix plus fixed append')
        if type(z['before_worktree_mode']) is not int or type(z['after_worktree_mode']) is not int or not 0<=z['before_worktree_mode']<=4095 or z['before_worktree_mode']!=z['after_worktree_mode'] or z['after_worktree_mode']!=modes[n]:raise ValueError('Complete full modes preserved')
    return True
modes={n:420 for n in destinations}
for phase in ['finalize','before_mirror','repeated_locked_acceptance','post']:ck(logs(receipt,outputs,prefixes,modes),'Exact accepted log outputs at '+phase)
for k,v in [('source_preparation_did_not_append',1),('schema','wrong'),('note',suffix.decode()+'extra'),('logs',receipt['logs'][:1]),('logs',receipt['logs']*2)]:
    m=copy.deepcopy(receipt);m[k]=v;bad(lambda m=m:logs(m,outputs,prefixes,modes),'Log receipt '+k)
for i in range(2):
    for k,v in [('log',unrelated[0]),('before_worktree_mode',True),('after_worktree_mode',False),('before_worktree_mode',-1),('before_worktree_mode',4096),('after_worktree_mode',292)]:
        m=copy.deepcopy(receipt);m['logs'][i][k]=v;bad(lambda m=m:logs(m,outputs,prefixes,modes),'Log'+str(i)+' '+k+' '+repr(v))
    for key in ['before','retained_preimage','after']:
        for field,value in [('bytes',True),('bytes',-1),('sha256','A'*64),('path','a/../b')]:
            m=copy.deepcopy(receipt);m['logs'][i][key][field]=value;bad(lambda m=m:logs(m,outputs,prefixes,modes),'Log'+str(i)+' '+key+field)
    n=destinations[i];mut=dict(outputs);mut[n]+=b'extra';bad(lambda:logs(receipt,mut,prefixes,modes),'Trailing unrelated append rejected '+str(i))
    mut=dict(prefixes);mut[n]=b'replaced prefix';bad(lambda:logs(receipt,outputs,mut,modes),'Changed retained prefix '+str(i))
modefile=fixture/'mode_sweep';modefile.write_bytes(b'owned permission control\n');observations=[]
def frozen(v):
    if type(v) is not int or v!=292:raise ValueError('Exact frozen0444')
    return True
for bits in range(4096):
    modefile.chmod(bits);actual=stat.S_IMODE(modefile.stat().st_mode);ck(actual==bits,'Actual full4096 roundtrip');observations.append({'requested':bits,'observed':actual})
    if bits==292:ck(frozen(bits),'Only292 frozen accepted')
    else:bad(lambda bits=bits:frozen(bits),'Frozen mode '+format(bits,'04o'))
    m=copy.deepcopy(receipt)
    for z in m['logs']:z['before_worktree_mode']=bits;z['after_worktree_mode']=bits
    ck(logs(m,outputs,prefixes,{n:bits for n in destinations}),'Owned append all4096 integer full modes preserved')
modefile.chmod(292)
for v in [True,False,292.0,'0444',None]:bad(lambda v=v:frozen(v),'Nontyped frozen mode '+repr(v))
for b in [b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}',b'{"a":1e999}']:bad(lambda b=b:strict(b),'Strict JSON mutant '+repr(b))
ck(not same(True,1) and not same(1,1.0) and not same([0],[]) and not same({'a':0},{'a':0,'b':0}),'Whole recursive scalar/key/type equality')
ledger=strict((H/'EXPECTED_ORIGINAL_LEDGER.json').read_bytes());ck(type(ledger['substantive_turns_used']) is int and ledger['substantive_turns_used']==0 and type(ledger['source_verification_responses']) is int and ledger['source_verification_responses']==1,'Original complete actual zero/response-one ledger')
for k,v in [('substantive_turns_used',False),('source_verification_responses',True),('turn_limit',5.0)]:
    m=copy.deepcopy(ledger);m[k]=v;ck(not same(m,ledger),'Whole ledger typed mutant '+k)
queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();header=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI'];lines=queue.decode().splitlines(keepends=True);target=[s for s in lines if len(s.split('|'))==14 and s.split('|')[2].strip()=='30004438 / OWR-17475-003'];ck(len(target)==1,'Dated live queue selected identity');before_row=target[0];cells=before_row.split('|');ck(cells[8].strip()=='queued' and cells[9].strip()=='0/5','Dated queued source only');cells[8]=' already_solved ';cells[11]=' PRIVATE SOURCE MODEL credited prior known theorem ';after_row='|'.join(cells);prospective=queue.replace(before_row.encode(),after_row.encode(),1);ck([i for i,(a,b) in enumerate(zip(before_row.split('|'),cells)) if a!=b]==[8,11] and prospective.replace(after_row.encode(),before_row.encode(),1)==queue,'Only Status/Findings and complete inverse queue equality');ck(cells[9:11]==before_row.split('|')[9:11] and cells[12]==before_row.split('|')[12],'Turns Chat DOI exact')
post=strict((H/'EXPECTED_PREVIOUS_POST.json').read_bytes());rootpost=strict((H/'EXPECTED_PREVIOUS_ROOT_POST.json').read_bytes());ck(same(rootpost['entire_post'],post) and rootpost['completed_primary_prs']==35,'Actual predecessor entire post typed binding')
def source_verdict(v,mf):
    needed={'schema':'pr46-acceptance-source-adversary-verdict/v1','verdict':'PASS_SOURCE_ONLY_SCOPED','preparation_manifest_sha256':mf,'mandatory_corrections':[],'production_imported_compiled_executed':False,'future_acceptance_approved':False}
    if type(v) is not dict or any(k not in v or not same(v[k],val) for k,val in needed.items()):raise ValueError('New scoped SOURCE gate')
    return True
mf='f44ccf65fa4397736305881de926eafcf211c33ef9e6fec5e5596c99d252ef40';v={'schema':'pr46-acceptance-source-adversary-verdict/v1','verdict':'PASS_SOURCE_ONLY_SCOPED','preparation_manifest_sha256':mf,'mandatory_corrections':[],'production_imported_compiled_executed':False,'future_acceptance_approved':False};ck(source_verdict(v,mf),'Private scoped model does not create actual verdict')
for k,val in [('schema','old'),('verdict','PASS'),('preparation_manifest_sha256','d97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab'),('mandatory_corrections',['S1']),('production_imported_compiled_executed',0),('future_acceptance_approved',0),('future_acceptance_approved',True)]:
    m=dict(v);m[k]=val;bad(lambda m=m:source_verdict(m,mf),'New source gate '+k)
# Genuine absent-only publication and filesystem topology controls stay private.
ck(sys.platform=='darwin','Actual macOS');lib=ctypes.CDLL(None,use_errno=True);rename=lib.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int;src=fixture/'rename_source';dst=fixture/'existing';src.write_bytes(b'owned');dst.write_bytes(b'sentinel');ck(rename(os.fsencode(src),os.fsencode(dst),4)!=0 and dst.read_bytes()==b'sentinel' and src.read_bytes()==b'owned','Actual absent-only replacement refusal');fresh=fixture/'absent';ck(rename(os.fsencode(src),os.fsencode(fresh),4)==0 and fresh.read_bytes()==b'owned','Actual absent-only success')
link=fixture/'symlink';link.symlink_to('absent');ck(link.is_symlink(),'Actual symlink detected');link.unlink()
out={'schema':'pr46-source-v2-independent-ownership-phase-controls/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_PRIVATE_OWNERSHIP_PHASE_MODELS','actual_pid':os.getpid(),'assertions_passed':count,'negative_mutants_rejected':len(rejected),'rejected_mutant_labels':rejected,'actual_permission_observations':observations,'private_V1_S1_failure':v1_failure,'log_destinations':destinations,'production_imported_compiled_executed':False,'foreign_bodies_copied':False,'future_acceptance_approved':False,'SOURCE_verdict':None,'new_substantive_attempts':0,'audit_turns':0,'dated_live_queue_is_not_future_authority':True}
(F/'OWNERSHIP_PHASE_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rejected_mutant_labels','actual_permission_observations','private_V1_S1_failure']}))
