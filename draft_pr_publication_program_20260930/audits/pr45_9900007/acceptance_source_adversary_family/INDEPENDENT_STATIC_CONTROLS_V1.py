"""Independent inert source/text and evidence audit. No imported or compiled production code."""
from pathlib import Path,PurePosixPath
import argparse,copy,datetime as dt,hashlib,io,json,math,os,re,sqlite3,stat,subprocess,sys,tokenize
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2];P=A/'acceptance_preparation_family';C=A/'reviewed_candidate';W=A/'whole_current_source_first_family';PREP='867faf71a96ada5acf2a92539bfdacd3b69bd3a1a1e0cb7e37ea6a106be1958e204'
checks=[];reads={};captures=[]
def need(x,m):
    if not x:raise ValueError(m)
    checks.append(m)
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(xs):
        o={}
        for k,v in xs:
            if k in o:raise ValueError('duplicate JSON key')
            o[k]=v
        return o
    def floating(s):
        x=float(s)
        if not math.isfinite(x):raise ValueError('nonfinite number')
        return x
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
def typed(x,y):
    if type(x)!=type(y):return False
    if type(x) is dict:return x.keys()==y.keys() and all(typed(x[k],y[k]) for k in x)
    if type(x) is list:return len(x)==len(y) and all(typed(a,b) for a,b in zip(x,y))
    return x==y
def rel(s):
    if type(s) is not str or not s or '\\' in s or '\0' in s:raise ValueError('invalid relative path')
    p=PurePosixPath(s)
    if p.is_absolute() or p.as_posix()!=s or any(x in {'.','..','.git','__pycache__'} for x in p.parts):raise ValueError('noncanonical relative path')
    return p
def safe(p):
    need(p.is_file() and not p.is_symlink(),'regular file '+str(p))
    need(all(d.is_dir() and not d.is_symlink() for d in p.parents),'real ancestors '+str(p))
    need(p.resolve(strict=True).is_relative_to(R),'inside actual repository '+str(p))
    return p
def read(p):
    p=safe(p);b=p.read_bytes();reads[str(p)]={'path':str(p),'bytes':len(b),'sha256':sha(b),'worktree_mode':stat.S_IMODE(p.stat().st_mode)};return b
def load(p):return parse(read(p))
def ref(p):
    b=read(p);return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def verify(z,base=R):
    need(type(z) is dict and type(z.get('bytes')) is int and z['bytes']>=0 and type(z.get('sha256')) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']),'strict reference')
    s=z['path'];p=Path(s) if s.startswith('/') else base/rel(s);b=read(p);need(len(b)==z['bytes'] and sha(b)==z['sha256'],'complete reference '+str(p));return b
def closure(base,name,pin,count):
    raw=read(base/name);need(sha(raw)==pin,'exact closure SHA '+str(base));m=parse(raw);need(m['self_excluded']==[name] and type(m['files_count']) is int and m['files_count']==count==len(m['files']),'literal sole self/count '+str(base))
    names={name};dirs=set()
    for z in m['files']:
        rel(z['path']);need(z['path'] not in names,'unique member');names.add(z['path']);verify(z,base)
    actual=set();actualdirs=set()
    for q in base.rglob('*'):
        n=q.relative_to(base).as_posix();rel(n);need(not q.is_symlink() and (q.is_file() or q.is_dir()),'no closure symlink/special')
        (actual if q.is_file() else actualdirs).add(n)
        if q.is_file():need(stat.S_IMODE(q.stat().st_mode)==0o444,'literal full0444 '+str(q))
    for n in names:dirs.update(d.as_posix() for d in PurePosixPath(n).parents if str(d)!='.')
    need(names==actual and dirs==actualdirs,'complete exact file/directory topology '+str(base));return m
def clock(s):
    if type(s) is not str or s!=s.strip():raise ValueError('bad clock type')
    t=dt.datetime.fromisoformat(s.replace('Z','+00:00'))
    if t.tzinfo is None or t.utcoffset()!=dt.timedelta(0):raise ValueError('aware UTC required')
    return t
def abs_literal(s):
    need(type(s) is str and s.startswith(str(R)+'/') and '\\' not in s and '\0' not in s,'literal repository absolute identity');p=R
    for x in s[len(str(R))+1:].split('/'):
        need(x and x not in {'.git','__pycache__'} and p.is_dir() and not p.is_symlink(),'safe lexical foreign traversal')
        if x=='..':need(p!=R,'foreign traversal no escape');p=p.parent
        elif x!='.':p=p/x
        need(p.exists() and not p.is_symlink() and p.is_relative_to(R),'every foreign prefix safe')
    return safe(p)
def stream(z,base):
    s=z['path'];return verify(z,R if s.startswith('draft_pr_publication_program_20260930/') else base)
def own_git(label,args):
    d=H/'actual_git'/label;d.mkdir(parents=True);src=Path(__file__).read_bytes();op=(H/'capture_own.py').read_bytes();argv=['git',*args]
    pre={'schema':'pr45-source-adversary-local-git-prelaunch/v1','argv':argv,'cwd':str(R),'operator_pid':os.getpid(),'prepared_utc':utc(),'source_sha256':sha(src),'operator_sha256':sha(op),'stdin_supplied':False}
    for n,b in [('PRELAUNCH_SOURCE.py',src),('PRELAUNCH_OPERATOR.py',op),('PRELAUNCH.json',json.dumps(pre,sort_keys=True,indent=2).encode()+b'\n')]: (d/n).write_bytes(b)
    started=utc();p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));out,err=p.communicate();finished=utc()
    rec={**pre,'child_pid':p.pid,'started_utc':started,'finished_utc':finished,'exit_code':p.returncode,'actual_execution':True,'completed':True,'source_unchanged':Path(__file__).read_bytes()==src,'operator_unchanged':(H/'capture_own.py').read_bytes()==op}
    for ch,b in [('stdout',out),('stderr',err)]: (d/(ch+'.bin')).write_bytes(b);rec[ch]={'path':str(d/(ch+'.bin')),'bytes':len(b),'sha256':sha(b)}
    (d/'CAPTURE.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n');captures.append(rec);need(p.returncode==0 and not err,'local read-only Git '+label);return out
def reject(fn,label):
    try:fn()
    except (ValueError,TypeError,KeyError,OverflowError):return label
    raise ValueError('hostile control escaped: '+label)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mutant',default='none');v=ap.parse_args()
    if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise ValueError('unoptimized auditor required')
    # These deliberately failing children exercise the independent oracle, never production.
    if v.mutant=='boolean':need(typed({'n':True},{'n':1}),'deliberate boolean impostor rejected')
    elif v.mutant=='permission':need(0o2444==0o444,'deliberate special-mode impostor rejected')
    elif v.mutant=='duplicate_json':parse(b'{"approval":false,"approval":true}')
    elif v.mutant=='path':rel('a/../b')
    elif v.mutant!='none':raise ValueError('unknown mutant')
    if v.mutant!='none':raise ValueError('negative child unexpectedly survived')
    native=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')['files'];before=[ref(R/z['path'])|{'worktree_mode':stat.S_IMODE((R/z['path']).stat().st_mode)} for z in native]
    head=own_git('main_before',['rev-parse','HEAD']);need(own_git('branch',['branch','--show-current'])==b'main\n','stay on main')
    prep=closure(P,'PREPARATION_MANIFEST.json',PREP,204);packet=closure(C,'MANIFEST.json','d136815406dc35265a828deece080813c716c69c2bb915192e606acafdcdd4c5',497);whole=closure(W,'MANIFEST.json','b372d0fdad3ae40c6a1b82530504dd2584022f15e703b468a8631faa455f9646',1068)
    need(prep['schema']=='pr45-acceptance-source-closure/v1' and prep['source_only'] is True and prep['proposed_helpers_imported_compiled_executed'] is False and prep['future_acceptance_or_ROOT_approval_claimed'] is False,'exact source-only closure meaning')
    depraw=read(C/'CURRENT_DEPENDENCIES.json');deps=parse(depraw);need(sha(depraw)=='e215d1b33f3cdc562aeb53cee76519386d7d203acbe8c1c251370b3fd3bd2410' and len(deps['files'])==416,'exact416 dependency manifest')
    for z in deps['files']:verify(z,A)
    outside=load(W/'EXTERNAL_INPUT_INVENTORY.json');need(typed(outside,load(P/'EXPECTED_EXTERNAL_INPUT_INVENTORY.json')) and len(outside['foreign_inputs'])==1109,'full typed1109 inventory')
    outside_names=set()
    for z in outside['foreign_inputs']:
        need(set(z)=={'path','bytes','sha256'},'exact absolute input row schema');q=abs_literal(z['path']);b=read(q);need(type(z['bytes']) is int and len(b)==z['bytes'] and sha(b)==z['sha256'],'full individual external identity');outside_names.add(str(q.relative_to(R)))
    need(len(outside_names)==1109,'unique canonical outside identities')
    four={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'};native_map={z['path']:z for z in native};need(len(native_map)==13 and not four&outside_names and (set(native_map)-four)<=outside_names,'frozen4 historical and stable9 split')
    for i,n in enumerate(sorted(four)):
        body=own_git('frozen_body_'+str(i),['show','264c26d539d616b0da6f8df76478a213d20939e4:'+n]);tree=own_git('frozen_tree_'+str(i),['ls-tree','264c26d539d616b0da6f8df76478a213d20939e4','--',n]);z=native_map[n];need(len(body)==z['bytes'] and sha(body)==z['sha256'],'fresh own full frozen native body');blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest();need(tree==('100644 blob '+blob+'\t'+n+'\n').encode(),'exact native Git100644 full tree')
    inputs=load(P/'INPUT_BINDINGS.json')
    for z in list(inputs['pins'].values())+[inputs[k] for k in ['previous_mirror','previous_post','previous_root_post','closed_whole_manifest','closed_whole_report','closed_whole_result','closed_root_whole_inspection']]:verify(z)
    root=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json');need(typed(root,load(P/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and typed(root['complete_VERDICT_object'],load(W/'VERDICT.json')),'whole actual ROOT typed128346 record and entire verdict')
    need(len(read(A/'ROOT_WHOLE_CURRENT_REVIEW.json'))==128346 and sha(read(A/'ROOT_WHOLE_CURRENT_REVIEW.json'))=='122fd1e3df7918cc32cbcccd75a94956e01cf1acbfc914c71f1547217beacc71','actual ROOT raw identity')
    need(len(root['complete_actual_captures_checked'])==58 and len(root['complete_dated_git_captures'])==8 and root['actual_direct_four_operator_pid']==59667 and root['future_execution_approved'] is False,'past ROOT reading cannot approve future acceptance')
    for z in root['complete_actual_captures_checked']:
        cp=R/z['capture']['path'];actual=parse(verify(z['capture']));need(typed(actual,z['entire_capture']),'full stored capture type equality');start=actual.get('started_utc',actual.get('start_utc'));end=actual.get('finished_utc',actual.get('end_utc'));need(clock(start)<=clock(end)<=clock(root['created_utc']),'stored genuine completed capture clocks')
        for ch in ['stdout','stderr']:stream(actual[ch],cp.parent)
        for key,filenames in [('source_sha256',['prelaunch_source.py','PRELAUNCH_SOURCE.py']),('operator_sha256',['prelaunch_operator.py','PRELAUNCH_OPERATOR.py'])]:
            candidates=[cp.parent/n for n in filenames if (cp.parent/n).exists()];need(len(candidates)==1 and sha(read(candidates[0]))==actual[key],'full stored prelaunch chain')
    expected=[]
    for n in sorted(four):expected.extend([['git','show','264c26d539d616b0da6f8df76478a213d20939e4:'+n],['git','ls-tree','264c26d539d616b0da6f8df76478a213d20939e4','--',n]])
    need(typed([x['argv'] for x in root['complete_dated_git_captures']],expected),'all8 actual body-then-tree query order')
    for z in root['complete_dated_git_captures']:
        need(z['operator_pid']==59667 and type(z['pid']) is int and z['pid']>0 and z['exit_code']==0 and z['source_unchanged'] is True and z['operator_unchanged'] is True,'actual ROOT direct query PIDs/status');verify(z['stdout']);need(verify(z['stderr'])==b'','all8 full direct stderr');need(clock(z['started_utc'])<=clock(z['finished_utc'])<=clock(root['created_utc']),'actual ROOT direct awareUTC')
    # Independently retained source operation failures and successful revision must agree exactly.
    prep_caps=[]
    for cp in sorted(P.glob('*ACTUAL_CAPTURE/CAPTURE.json')):
        z=load(cp);pre=z['prelaunch'];need(z['actual_execution'] is True and z['completed'] is True and type(z['pid']) is int and z['pid']>0 and type(z['operator_pid']) is int and z['operator_pid']>0,'all completed preparation captures');need(typed(pre,load(cp.parent/'PRELAUNCH.json')),'entire prelaunch metadata');need(sha(read(cp.parent/'PRELAUNCH_SOURCE.py'))==pre['source_sha256'] and sha(read(cp.parent/'PRELAUNCH_OPERATOR.py'))==pre['operator_sha256'],'entire preparation source/operator');need(clock(z['started_utc'])<=clock(z['finished_utc'])<=clock(prep['utc']),'capture completion precedes sealing')
        for ch in ['stdout','stderr']:verify(z[ch],cp.parent)
        prep_caps.append(z)
    bypid={z['pid']:z for z in prep_caps};need(bypid[63648]['exit_code']==bypid[63650]['exit_code']==1 and bypid[64423]['exit_code']==bypid[64425]['exit_code']==bypid[66648]['exit_code']==0,'failed runs retained and new successes distinct');need(bypid[66648]['operator_pid']==66645,'actual SOURCE sequential child-then-outer closure')
    previous=load(R/inputs['previous_post']['path']);previous_root=load(R/inputs['previous_root_post']['path']);need(typed(previous,load(P/'EXPECTED_PREVIOUS_POST.json')) and typed(previous_root,load(P/'EXPECTED_PREVIOUS_ROOT_POST.json')) and typed(previous_root['entire_post'],previous),'actual44 full typed post and entire_post');need(previous_root['schema']=='pr44-root-complete-actual-post-inspection/v1' and previous['targets']==35 and previous['primary_acceptances']==34 and previous['consumed_substantive_turns']==43,'actual predecessor counts')
    oldproposal=load(R/inputs['previous_mirror']['path']);need(len(oldproposal['entries'])==34 and len(oldproposal['duplicate_mirrors'])==1 and 45 not in oldproposal['required_completed_prs'],'actual44 full proposal34 and one duplicate')
    snapshot=load(A/'snapshot_manifest.json');need(len(snapshot['files'])==18 and snapshot['head']=='d9b4acf5d070d1f04ffac86a4f08916a5629ff16' and snapshot['merge_base']=='01358d66fc67d1c462bddf31c0d4ee5b120e6737' and snapshot['github_base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0','distinct original18 heads')
    for i,z in enumerate(snapshot['files']):
        n=z['relative_path'];need(read(A/'source_snapshot'/n)==read(C/'original_archive'/n),'original archive exact');b=own_git('original_body_'+str(i),['show',snapshot['head']+':'+z['path']]);t=own_git('original_tree_'+str(i),['ls-tree',snapshot['head'],'--',z['path']]);need(len(b)==z['bytes'] and sha(b)==z['sha256'] and b==read(A/'source_snapshot'/n),'own original full Git bytes');need(t==(z['git_mode']+' blob '+z['git_object']+'\t'+z['path']+'\n').encode(),'own original literal Git row')
    immutable=['PARTIAL.md','SOURCES.md','source_record.json','source_manifest.json','turns.jsonl','binary_verification.json','verify_binary_process.py','review/PARTIAL.md','review/independent_checks.py','review/independent_results.json','review/submitted_results.json','review/verify_binary_process.py']
    for n in immutable:need(read(C/n)==read(A/'source_snapshot'/n),'all12 immutable original bodies')
    ledger=read(C/'turns.jsonl');events=[parse(b) for b in ledger.splitlines()];need(ledger.endswith(b'\n') and len(events)==1 and type(events[0]['turn']) is int and events[0]['turn']==1,'whole exact original one-turn JSONL')
    def budget(raw,u,l):
        if type(u) is not int or type(l) is not int or (u,l)!=(1,5) or raw!=ledger:raise ValueError('exact1/5 ledger')
    rejects=[reject(lambda r=r,u=u,l=l:budget(r,u,l),n) for n,r,u,l in [('empty',b'',1,5),('whitespace',b'\n',1,5),('invented',b'{"turn":1}\n',1,5),('bool',ledger,True,5),('wrong_used',ledger,2,5),('wrong_limit',ledger,1,4)]]
    for b in [b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1e999}']:rejects.append(reject(lambda b=b:parse(b),'JSON '+str(b)))
    for s in ['', '/a','a//b','a/./b','a/../b','a\\b','a\0b','.git/a','__pycache__/a']:rejects.append(reject(lambda s=s:rel(s),'path '+repr(s)))
    need(not typed(True,1) and not typed(1,1.0) and not typed(None,False),'recursive scalar type hostility');need([x for x in range(4096) if stat.S_IMODE(stat.S_IFREG|x)==0o444]==[0o444],'all4096 full-mode oracle')
    probe=H/'private_mode_probe.bin';probe.write_bytes(b'private fullmode probe\n');mode_results=[]
    for mode in [0o444,0o644,0o1444,0o2444,0o4444]:probe.chmod(mode);observed=stat.S_IMODE(probe.stat().st_mode);need(observed==mode,'own actual special-bit probe');mode_results.append({'requested':mode,'observed':observed,'accepted':observed==0o444})
    probe.chmod(0o444)
    lex=[]
    for n in ['pr45_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','capture_root_final_operation.py']:
        b=read(P/n);ts=list(tokenize.tokenize(io.BytesIO(b).readline));need(all(t.type!=tokenize.ERRORTOKEN for t in ts),'inert lexical tokens '+n);stack=[];matching={')':'(',']':'[','}':'{'}
        for t in ts:
            if t.type==tokenize.OP:
                if t.string in matching:need(bool(stack) and stack.pop()==matching[t.string],'source delimiter matching')
                elif t.string in matching.values():stack.append(t.string)
        need(not stack,'all source delimiters complete');lex.append({'path':n,'sha256':sha(b),'tokens':len(ts),'code_objects_created':False})
    guard=read(P/'pr45_guards.py').decode();integration=read(P/'integrate_reviewed_partial.py').decode();mirror=read(P/'state_mirror_reconciliation.py').decode();post=read(P/'verify_post_acceptance.py').decode();sealer=read(P/'seal_final_evidence.py').decode();operator=read(P/'capture_root_final_operation.py').decode()
    tokens=[('preparation complete exact typed schema',"keyset(obj,known[obj['schema']]"),('fresh protected foreign declaration',"'protected_foreign_tracked_paths'},'Exact current ROOT fresh input schema'"),('all dirty paths explicitly scoped','dirty<=set(paths)'),('foreign entire HEAD/index preservation',"git_bytes('show',':'+n)"),('fresh complete typed native13',"'path','bytes','sha256','worktree_mode'"),('full-mode specialbit rejection','stat.S_IMODE(regular(base,n).stat().st_mode)==0o444'),('whole typed expected current','equal(whole,load(HERE/\'EXPECTED_WHOLE_MANIFEST.json\'))'),('typed original previous ROOT','equal(rootpost,load(HERE/\'EXPECTED_PREVIOUS_ROOT_POST.json\'))'),('genuine future ROOT source read','ROOT_SOURCE_ACCEPTANCE_REVIEW.json'),('saved mirror full plan reconstruction','equal(plan,rebuild_saved_mirror_plan('),('exact prior proposal plus new','equal(proposal,expected)'),('full actual final capture known keys','Complete final actual ROOT capture schema')]
    for label,literal in tokens:need(literal in guard,'source mechanism '+label)
    need('set(changed)=={8,9,11}' in integration and "cells[10]==row.split('|')[10]" in integration and "cells[12]==row.split('|')[12]" in integration,'whole queue exact named-column protection')
    need("prior.items()" in mirror and "history==old_history+plan['history_append_bytes'].encode()" in post and "replay['history_append']==[]" in post,'whole typed state, complete history prefix and no-op source mechanisms');need('fcntl.LOCK_EX|fcntl.LOCK_NB' in mirror and 'g.write(history,old_history+' in mirror and mirror.index('g.write(history,old_history+')<mirror.index('g.write(state,plan['),'cooperative history-first write ordering')
    need('renamex_np' in sealer and 'os.fsencode(target),4' in sealer and 'not output.exists()' in sealer,'sealer absent-only two-record stage publication');need("'worktree_mode':stat.S_IMODE(path.stat().st_mode)" in operator and "rec['native13_after'] == before_files" in operator,'new actual sealer operator13 fullmode/current-head boundary')
    for n in ['DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json']:
        d=load(P/n);need(all(d[k] is False for k in ['root_full_current_read_completed','root_full_whole_read_completed','root_acceptance_source_review_completed','independent_whole_current_pass','root_actual_PR44_predecessor_read_completed']),'all draft flags false');need((d.get('created_utc') is None and d['whole_manifest'] is None) if n.startswith('DRAFT_ROOT') else d['partial_valid'] is None and d['preparation_manifest_sha256'] is None and d['immutable_evidence_references']==[],'draft cannot self approve')
    scope=load(P/'SCIENTIFIC_SCOPE.json');need(scope['full_problem_solved'] is False and scope['partial_valid'] is True and scope['original_substantive_attempts']==1 and scope['new_substantive_attempts']==scope['audit_turns']==0 and scope['current_model'] is scope['current_reasoning_effort'] is scope['current_deadline_utc'] is None,'scoped unsolved1/5 zero runtime authority');need(scope['offsets_nonnegative_finite_or_uniformly_tight_and_may_be_dependent'] is True and scope['finite_controls_do_not_prove_arbitrary_coupling_quantifier'] is True and scope['paper_or_new_doi_or_tracker'] is False,'mathematical quantifier and publication boundaries')
    source_record=load(C/'source_record.json');need(set(source_record)=={'dataset_revision','problem','upstream_report'} and type(source_record['upstream_report']) is dict and bool(source_record['upstream_report']),'plain wrapper and PRESENT nonempty prior')
    with sqlite3.connect((R/'unsolved_math_prioritization/cache/catalog.sqlite').as_uri()+'?mode=ro',uri=True) as db:row=db.execute('SELECT payload,report FROM records WHERE key=?',('9900007',)).fetchone()
    need(row is not None and typed(source_record['problem'],parse(row[0])) and typed(source_record['upstream_report'],parse(row[1])),'independent read-only cache selected source/prior type equality')
    need(len(packet['files'])+8==505 and len(packet['files'])+10==507 and 35/180*100==scope.get('program_completion_estimate_percent',35/180*100),'independent overlay/canonical arithmetic')
    need(len(load(R/'unsolved_math_prioritization/state.json'))==35 and sum(z['turns_used'] for z in load(R/'unsolved_math_prioritization/state.json').values())==43,'current predecessor native35targets43turns')
    after=[ref(R/z['path'])|{'worktree_mode':stat.S_IMODE((R/z['path']).stat().st_mode)} for z in native];need(typed(before,after) and own_git('main_after',['rev-parse','HEAD'])==head,'current native13 entire bytes/fullmodes and main preserved during own audit')
    result={'schema':'pr45-independent-acceptance-source-static-controls/v1','status':'PASS_STATIC_OWN_CONTROLS_ONLY','utc':utc(),'actual_child_pid':os.getpid(),'preparation_manifest_sha256':PREP,'checks':len(checks),'preparation_members':204,'candidate_members':497,'dependencies':416,'whole_members':1068,'external_inputs':1109,'own_git_captures':len(captures),'stored_whole_captures':58,'ROOT_direct_queries':8,'preparation_captures':len(prep_caps),'negative_controls':rejects,'all4096_full_modes_checked':True,'private_mode_probes':mode_results,'lexical_only':lex,'native13_before':before,'native13_after':after,'production_imported_compiled_executed':False,'future_acceptance_approved':False,'full_target_discovery_percent':0}
    for name,value in [('CONTROL_RESULTS.json',result),('COMPLETE_READ_INVENTORY.json',{'schema':'pr45-adversary-read-inventory/v1','utc':utc(),'files':sorted(reads.values(),key=lambda z:z['path']),'foreign_bodies_copied':False}),('OWN_GIT_CAPTURES.json',captures)]:
        with (H/name).open('x') as f:json.dump(value,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({k:result[k] for k in ['status','utc','actual_child_pid','checks','preparation_manifest_sha256','own_git_captures','stored_whole_captures','preparation_captures','production_imported_compiled_executed','future_acceptance_approved']}))
if __name__=='__main__':main()
