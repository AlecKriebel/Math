"""Handwritten private predicates. No proposed or historical helper is imported, parsed as code, compiled or executed."""
from pathlib import Path, PurePosixPath
import copy, ctypes, datetime as dt, hashlib, json, math, os, re, stat, sys
F=Path(__file__).absolute().parent;A=F.parent;R=F.parents[3];B=R/'draft_pr_publication_program_20260930';C=A/'reviewed_candidate';T=B/'audits/pr47_2849/acceptance_preparation_family'
NAMES=['pr48_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py'];observations=[];assertions=0
def insist(v,m):
    global assertions
    assertions+=1
    if not v:raise ValueError(m)
def equal(a,b):return type(a) is type(b) and (a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(items):
        o={}
        for k,v in items:insist(k not in o,'Duplicate key');o[k]=v
        return o
    def floating(x):v=float(x);insist(math.isfinite(v),'Nonfinite');return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('Nonfinite constant')))
def load(p):return parse(p.read_bytes())
def emit(n,o):
    with (F/n).open('xb') as h:h.write((json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());h.flush();os.fsync(h.fileno())
def negative(n,fn):
    try:fn()
    except (ValueError,TypeError,KeyError,IndexError,FileExistsError,OSError,json.JSONDecodeError) as e:observations.append({'label':n,'expected_rejected':True,'exception':type(e).__name__,'message':str(e)})
    else:raise ValueError('Accepted mutant '+n)
def keyset(o,k):insist(type(o) is dict and set(o)==set(k),'Exact keys')
def rel(n):
    insist(type(n) is str and n and '\\' not in n and '\0' not in n,'Literal path')
    p=PurePosixPath(n);insist(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical path');return n
def regular(base,n):
    rel(n);p=base/n;insist(base.is_dir() and not base.is_symlink() and p.is_file() and not p.is_symlink(),'Regular path')
    for x in p.parents:
        insist(not x.is_symlink(),'No symlink ancestor')
        if x==base:break
    insist(p.resolve().is_relative_to(base.resolve()),'Contained');return p
def ref(o):
    keyset(o,{'path','bytes','sha256'});rel(o['path']);insist(type(o['bytes']) is int and o['bytes']>=0 and type(o['sha256']) is str and re.fullmatch('[a-f0-9]{64}',o['sha256']),'Typed bytes/hash')
def check(base,o,mode=False):
    r={k:v for k,v in o.items() if k!='full_mode'};ref(r);p=regular(base,r['path']);b=p.read_bytes();insist(len(b)==r['bytes'] and sha(b)==r['sha256'],'Complete body')
    if mode:insist(type(o['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==o['full_mode'],'Full mode')
    return b
def utc(s):
    insist(type(s) is str and s==s.strip(),'UTC string');v=dt.datetime.fromisoformat(s.replace('Z','+00:00'));insist(v.tzinfo is not None and v.utcoffset()==dt.timedelta(0),'UTC');return v
def original_capture(z,argv,helper):
    keyset(z,{'schema','argv','cwd','started_utc','actual_operator_pid','stdin_supplied','source','actual_execution','pid','completed','exit_code','finished_utc','stdout','stderr','source_unchanged','operator_sha256','operator_unchanged'})
    insist(equal(z['argv'],argv) and z['cwd']==str(R) and type(z['pid']) is int and z['pid']>0 and type(z['actual_operator_pid']) is int and z['actual_operator_pid']==11716,'Typed original PID/argv/cwd')
    for k,v in {'actual_execution':True,'completed':True,'exit_code':0,'stdin_supplied':False,'operator_unchanged':True}.items():insist(equal(z[k],v),'Typed execution scalar '+k)
    insist(z['operator_sha256']=='a1a9682541d585dab8fa4278bfd66848d646b506877df93310339d565968bc7d' and utc(z['started_utc'])<=utc(z['finished_utc']),'Operator/UTC')
    for ch in ['stdout','stderr']:ref(z[ch]);check(R,z[ch])
    insist(check(R,z['stderr'])==b'','Whole stderr')
    if helper:
        insist(z['schema']=='pr48-root-unchanged-helper-actual-capture/v1' and z['source_unchanged'] is True,'Typed helper class');ref(z['source']);check(R,z['source']);insist(argv[:2]==['/usr/bin/python3','-B'] and R/z['source']['path']==Path(argv[2]),'Literal helper path')
    else:insist(z['schema']=='pr48-root-readonly-git-actual-capture/v1' and z['source'] is None and z['source_unchanged'] is None,'Real Git null/null class')
def exact_topology(base,names):
    files=set();dirs=set()
    for p in base.rglob('*'):
        insist(not p.is_symlink() and (p.is_file() or p.is_dir()),'No special/symlink');n=p.relative_to(base).as_posix();rel(n);(files if p.is_file() else dirs).add(n)
    expected={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'};insist(files==set(names) and dirs==expected,'Full topology')
def owned(n):
    rel(n);return n in NATIVE or n==PROGRAM or n.startswith(A.relative_to(R).as_posix()+'/') or n.startswith('unsolved_math_prioritization/attempts/2961/')
def foreign(paths):
    insist(type(paths) is list and all(type(n) is str for n in paths) and paths==sorted(set(paths)),'Sorted exact foreign');insist(all(not owned(n) for n in paths),'No owned foreign exclusion')
NATIVE={z['path'] for z in load(F/'INPUT_BINDINGS.json')['dated_native13']};PROGRAM=B.relative_to(R).as_posix()+'/RESEARCH_LOG.md'
def two_logs(record,prefixes,note,modes):
    keyset(record,{'schema','utc','logs','note','source_preparation_did_not_append'});insist(record['schema']=='private-two-log-fixture/v1' and record['source_preparation_did_not_append'] is True and record['note']==note and type(record['logs']) is list and len(record['logs'])==2,'Only exact two logs')
    for row,(name,prefix,mode) in zip(record['logs'],zip([A.relative_to(R).as_posix()+'/ROOT_RESEARCH_LOG.md',PROGRAM],prefixes,modes)):
        keyset(row,{'path','before','after','full_mode'});insist(row['path']==name and row['before']==prefix.hex() and row['after']==(prefix+note.encode()).hex() and type(row['full_mode']) is int and row['full_mode']==mode,'Whole prefix+append+mode')
def ledger(raw,used,limit):
    insist(type(used) is int and type(limit) is int and used==2 and limit==5 and type(raw) is bytes and raw==(C/'turns.jsonl').read_bytes() and raw.endswith(b'\n'),'Shared literal budget');v=[parse(s) for s in raw.splitlines()];insist(equal(v,load(F/'EXPECTED_ORIGINAL_LEDGER.json')) and len(v)==2 and all(type(z['turn']) is int for z in v) and [z['turn'] for z in v]==[1,2],'Original exact two turns')
def contract_post(root,post,contract):
    keyset(root,contract['future48_required_ROOT_complete_keyset']);expected=contract['future48_required_completed_values']
    for k,v in expected.items():insist(k in root and equal(root[k],v),'Typed full ROOT contract '+k)
    insist(root['schema']==contract['future48_required_ROOT_schema'] and equal(root['entire_post'],post),'Full entire post')
    for k,v in contract['future48_required_entire_post_values'].items():insist(k in post and equal(post[k],v),'Actual post value '+k)
def inventory(before):
    insist(type(before) is dict and type(before['items']) is list and len(before['items'])==180 and all(type(z['number']) is int for z in before['items']),'Inventory shape');ids=[z['number'] for z in before['items']];insist(len(set(ids))==180 and ids.count(48)==1 and type(before['completed_count']) is int and before['completed_count']==37 and sum(z['stage']=='complete' for z in before['items'])==37,'Actual prerequisite inventory')
    result=copy.deepcopy(before);next(z for z in result['items'] if z['number']==48).update(stage='complete',original_attempts='2/5');result.update(completed_count=38,current_pr=49,program_completion_estimate_percent=38*100/180);insist(sum(z['stage']=='complete' for z in result['items'])==38,'Exactly38');return result
def main():
    if (F/'PRIVATE_CONTROLS_RESULT.json').exists():
        history=F/'control_history/v1';history.mkdir(parents=True,exist_ok=False)
        for n in ['PRIVATE_CONTROLS_RESULT.json','PRIVATE_CONTROL_OBSERVATIONS.json','ALL_4096_ACTUAL_FULL_MODES.json','SPECIAL_PATH_FIXTURE_OBSERVATIONS.json']:(F/n).rename(history/n)
        (F/'private_fixtures').rename(history/'private_fixtures')
    inputs=load(F/'INPUT_BINDINGS.json');insist(inputs['actual_predecessor_PR47_completed'] is False and inputs['previous_root_post'] is None and inputs['whole_binding_completed'] is True,'No invented future authority')
    checked=0;bytes_read=0
    for z in list(inputs['pins'].values())+inputs['external_input_rows']+list(inputs['source_pattern_dated_references'].values())+[inputs['known_predecessor_source_contract'],inputs['known_predecessor_source_manifest']]:bytes_read+=len(check(R,z,True));checked+=1
    cm=load(C/'MANIFEST.json');wm=load(A/'current_whole_adversary_family/MANIFEST.json');pm=load(T/'PREPARATION_MANIFEST.json')
    for base,m,count in [(C,cm,1946),(A/'current_whole_adversary_family',wm,162),(T,pm,126)]:
        insist(type(m['files_count']) is int and m['files_count']==len(m['files'])==count and m['self_excluded']==['PREPARATION_MANIFEST.json' if base==T else 'MANIFEST.json'],'Self-only counts');names=set()
        for z in m['files']:
            r={'path':z['path'],'bytes':z.get('bytes',z.get('size')),'sha256':z['sha256']};bytes_read+=len(check(base,r));insist(stat.S_IMODE(regular(base,z['path']).stat().st_mode)==0o444,'Actual frozen full444');names.add(z['path']);checked+=1
        selfname='PREPARATION_MANIFEST.json' if base==T else 'MANIFEST.json';names.add(selfname);exact_topology(base,names);insist(stat.S_IMODE((base/selfname).stat().st_mode)==0o444,'Self444')
    frozen={z['path'] for z in cm['files']};extras={'reviewed_pending_administration/'+n for n in ['status.json','readiness.json','review/verdict.json','review/review_summary.json']}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md'};insist(len(frozen|extras)==1955 and len(frozen|extras|{'acceptance.json','ACCEPTANCE.md','MANIFEST.json'})==1958,'Independent canonical1955/1957+self')
    roots=load(F/'EXPECTED_ROOT_WHOLE_REVIEW.json');insist(roots['actual_readback_pid']==30858 and len(roots['normalized_complete_external_input_bindings'])==3916 and len(inputs['external_input_rows'])==3912 and len(roots['legitimate_dated_native_changes'])==2,'Complete actual ROOT with qualified dated4')
    for z in roots['legitimate_dated_native_changes']:insist(z['fresh_native_authority'] is False,'No historical live authorization')
    ledger((C/'turns.jsonl').read_bytes(),2,5)
    for label,b,u,l in [('empty',b'',2,5),('space',b'\n',2,5),('invented',b'{"turn":1}\n',2,5),('bool_used',(C/'turns.jsonl').read_bytes(),True,5),('float_used',(C/'turns.jsonl').read_bytes(),2.0,5),('extra_budget',(C/'turns.jsonl').read_bytes(),3,5),('limit',(C/'turns.jsonl').read_bytes(),2,4)]:negative('ledger_'+label,lambda b=b,u=u,l=l:ledger(b,u,l))
    rr=load(F/'EXPECTED_ORIGINAL_CAPTURE_RESULT.json');git=rr['complete_actual_Git_captures'];helpers=rr['complete_actual_helper_captures'];insist(len(git)==38 and len(helpers)==4,'Distinct actual capture classes')
    expected=[];head='e2e5c8c3e5ad218f867fa753c465bb96b3687bda';base='60292bed09f59236aa192cb17aa138f7b4750e1a';gh='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
    for z in load(A/'snapshot_manifest.json')['files']:expected.extend([['git','show',head+':'+z['path']],['git','ls-tree',head,'--',z['path']]])
    expected.extend([['git','merge-base',head,gh],['git','diff','--no-ext-diff','--no-textconv','--binary',base,head,'--'],['git','ls-tree','-r','-z',head,'--','unsolved_math_prioritization/attempts/2961/'],['git','show','2c32c34e6ddfa52ce067805afd3e2157dc32a130:unsolved_math_prioritization/attempts/2961/PARTIAL.md']]);insist(equal([z['argv'] for z in git],expected),'Independent exact full38argv')
    for z,e in zip(git,expected):original_capture(z,e,False)
    helperpaths=['author_historical/check_algebra.py','identical_submitted_historical/check_algebra.py','author_final/check_algebra.py','historical_independent/independent_checks.py']
    for z,n in zip(helpers,helperpaths):original_capture(z,['/usr/bin/python3','-B',str(A/'root_original_actual_reproduction_v2'/n)],True)
    for index,z in enumerate(git+helpers):
        expectedargv=expected[index] if index<38 else ['/usr/bin/python3','-B',str(A/'root_original_actual_reproduction_v2'/helperpaths[index-38])];ish=index>=38
        for field,value in [('pid',True),('exit_code',False),('actual_execution',1),('completed',1),('argv',['git','status']),('source_unchanged',False),('operator_unchanged',None),('cwd',str(F)),('unexpected',True)]:
            mutant=copy.deepcopy(z);mutant[field]=value;negative('capture_'+str(index)+'_'+field,lambda mutant=mutant,e=expectedargv,ish=ish:original_capture(mutant,e,ish))
        if not ish:
            mutant=copy.deepcopy(z);mutant['source']=helpers[0]['source'];negative('Git_helper_substitution_'+str(index),lambda mutant=mutant,e=expectedargv:original_capture(mutant,e,False))
    for n in ['../x','a/../x','a//b','./x','/tmp/x','a\\b','a\0b','.git/a','__pycache__/x']:negative('path_'+repr(n),lambda n=n:rel(n))
    for b in [b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}',b'{"a":1e999}']:negative('JSON_'+repr(b),lambda b=b:parse(b))
    insist(not equal({'a':True},{'a':1}) and not equal([2],[2.0]) and not equal({'a':None},{'a':False}),'Scalar recursive typing')
    foreign(['README.md','draft_pr_publication_program_20260930/audits/other/RESEARCH_LOG.md'])
    for n in [PROGRAM,A.relative_to(R).as_posix()+'/ROOT_RESEARCH_LOG.md','unsolved_math_prioritization/attempts/2961/PARTIAL.md',*sorted(NATIVE)]:negative('owned_foreign_'+n,lambda n=n:foreign([n]))
    for v in [['README.md','README.md'],['z','a'],[True]]:negative('foreign_identity_'+repr(v),lambda v=v:foreign(v))
    prefixes=[b'FULL A48 PREFIX\n',b'FULL PROGRAM PREFIX\n'];note='\nFIXED ACTUAL FINALIZATION NOTE\n';modes=[0o644,0o4755];logs={'schema':'private-two-log-fixture/v1','utc':'2026-10-03T08:00:00+00:00','source_preparation_did_not_append':True,'note':note,'logs':[{'path':n,'before':b.hex(),'after':(b+note.encode()).hex(),'full_mode':m} for n,b,m in zip([A.relative_to(R).as_posix()+'/ROOT_RESEARCH_LOG.md',PROGRAM],prefixes,modes)]};two_logs(logs,prefixes,note,modes)
    for i in range(2):
        for field,v in [('path','README.md'),('before',b'prefix truncated'.hex()),('after',b'wrong append'.hex()),('full_mode',True),('full_mode',0o755)]:
            mutant=copy.deepcopy(logs);mutant['logs'][i][field]=v;negative('owned_log_'+str(i)+'_'+field+repr(v),lambda mutant=mutant:two_logs(mutant,prefixes,note,modes))
    mutant=copy.deepcopy(logs);mutant['logs'].append(copy.deepcopy(logs['logs'][0]));negative('third_log',lambda:two_logs(mutant,prefixes,note,modes))
    # All4096 full permission modes are actually set/read, including special bits.
    fixtures=F/'private_fixtures';fixtures.mkdir(exist_ok=False);mf=fixtures/'mode_file.bin';mf.write_bytes(b'private fullmode specimen\n');mode_rows=[]
    for mode in range(0o10000):
        mf.chmod(mode);actual=stat.S_IMODE(mf.stat().st_mode);insist(actual==mode,'Actual complete chmod');mode_rows.append({'requested':mode,'actual':actual,'frozen_literal0444':actual==0o444})
    mf.chmod(0o644);emit('ALL_4096_ACTUAL_FULL_MODES.json',{'schema':'pr48-private-full-mode-controls/v1','actual_pid':os.getpid(),'rows':mode_rows,'only_literal0444_accepts':sum(z['frozen_literal0444'] for z in mode_rows)==1,'final_mode':stat.S_IMODE(mf.stat().st_mode)})
    target=fixtures/'target.bin';tmp=fixtures/'temp.bin';target.write_bytes(b'original target');tmp.write_bytes(b'fully written staged bytes');negative('exclusive_file_existing_target',lambda:os.link(tmp,target,follow_symlinks=False));insist(target.read_bytes()==b'original target' and tmp.read_bytes()==b'fully written staged bytes','Exclusive race bodies retained')
    new=fixtures/'published.bin';os.link(tmp,new,follow_symlinks=False);insist(new.read_bytes()==tmp.read_bytes(),'Absent-only complete file publication')
    stage=fixtures/'stage';dest=fixtures/'published_directory';stage.mkdir();(stage/'member').write_bytes(b'complete directory specimen');insist(sys.platform=='darwin','Private actual macOS test');libc=ctypes.CDLL(None,use_errno=True);ren=libc.renamex_np;ren.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];ren.restype=ctypes.c_int;insist(ren(os.fsencode(stage),os.fsencode(dest),4)==0,'Actual exclusive directory publication');stage.mkdir();(stage/'member').write_bytes(b'second full stage');code=ren(os.fsencode(stage),os.fsencode(dest),4);insist(code!=0 and (dest/'member').read_bytes()==b'complete directory specimen' and (stage/'member').read_bytes()==b'second full stage','Existing directory race cannot replace');observations.append({'label':'exclusive_directory_existing_target','expected_rejected':True,'actual_errno':ctypes.get_errno(),'return_code':code})
    topology=fixtures/'topology';topology.mkdir();(topology/'d').mkdir();(topology/'d/member').write_bytes(b'x');exact_topology(topology,{'d/member'});(topology/'empty').mkdir();negative('extra_empty_directory',lambda:exact_topology(topology,{'d/member'}));(topology/'empty').rmdir()
    link=fixtures/'link';link.symlink_to(target.name);negative('symlink_file',lambda:regular(fixtures,'link'));link.unlink();emit('SPECIAL_PATH_FIXTURE_OBSERVATIONS.json',{'symlink_actually_exercised_then_removed_for_regular_closure':True,'race_stage_and_original_bodies_retained':True,'extra_empty_directory_actually_tested_then_removed':True})
    contract=load(F/'ROOT_POST_CONTRACT.json');insist(len(contract['future48_required_ROOT_complete_keyset'])==22,'Exact22post keys');post={**contract['future48_required_entire_post_values'],'utc':'2026-10-03T08:00:00+00:00'};root={k:None for k in contract['future48_required_ROOT_complete_keyset']};root.update(contract['future48_required_completed_values'],schema=contract['future48_required_ROOT_schema'],entire_post=post);contract_post(root,post,contract)
    for field in contract['future48_required_ROOT_complete_keyset']:
        mutant=copy.deepcopy(root);mutant.pop(field);negative('ROOT_missing_'+field,lambda mutant=mutant:contract_post(mutant,post,contract))
    mutant=copy.deepcopy(root);mutant['future']=True;negative('ROOT_extension',lambda:contract_post(mutant,post,contract));mutant=copy.deepcopy(root);mutant['entire_post']['full_problem_solved']=True;negative('ROOT_entire_post_mutant',lambda:contract_post(mutant,post,contract))
    for field in contract['future48_required_completed_values']:
        mutant=copy.deepcopy(root);mutant[field]='mutant';negative('ROOT_wrong_'+field,lambda mutant=mutant:contract_post(mutant,post,contract))
    before={'items':[{'number':i,'stage':'complete' if i<=37 else 'pending','opaque':{'nested':[i,None,False]}} for i in range(1,181)],'completed_count':37,'opaque':'retain'};after=inventory(before);insist(all(equal(a,b) for a,b in zip(before['items'],after['items']) if a['number']!=48) and after['opaque']==before['opaque'] and after['program_completion_estimate_percent']==21.11111111111111,'Every179 inventory row + float exact')
    for field,v in [('completed_count',True),('completed_count',36)]:mutant=copy.deepcopy(before);mutant[field]=v;negative('inventory_'+field+repr(v),lambda mutant=mutant:inventory(mutant))
    mutant=copy.deepcopy(before);mutant['items'][47]['number']=True;negative('inventory_bool_identity',lambda:inventory(mutant));mutant=copy.deepcopy(before);mutant['items'][47]['number']=47;negative('inventory_duplicate_identity',lambda:inventory(mutant))
    source={n:(F/n).read_text() for n in NAMES};g=source['pr48_guards.py'];i=source['integrate_reviewed_partial.py'];m=source['state_mirror_reconciliation.py'];p=source['verify_post_acceptance.py'];se=source['seal_final_evidence.py']
    required_text={
      'pr48_guards.py':['ID, CODE, PR = \'2961\', \'KP-4.85\', 48','predecessor47(o,clock)','known_predecessor_source_contract','len(helpers)==4 and len(queries)==38',"z['source'] is None and z['source_unchanged'] is None",'len(rr)==162',"inputs['external_input_count']==3912",'len(rows(deps[\'files\']))==1798','CURRENT_SHA = \'3f8d6b38',"ADDITIONAL_OWNED_MUTATION_PATHS={PROGRAM_LOG.relative_to(R).as_posix()}",'protected_foreign_paths(fresh)',"before==after==stat.S_IMODE",'os.link(tmp,p,follow_symlinks=False)',"'full_permission_mode','duplicate_shared_budget','turn_limit'",'exact original',"'substantive_attempts_used':2"],
      'integrate_reviewed_partial.py':["cells[9]=' 2/5 '",'g.alias_QUEUE_absent(before)',"'30004403' not in state",'g.foreign_capture(',"for name,f in g.OWNED_OPERATIONAL_LOGS",'previous+note.encode()',"f.chmod(before_mode)",'g.owned_log_append_check(pre)'],
      'state_mirror_reconciliation.py':["'used':2,'limit':5",'pr48_exact_original_two_turn_JSONL',"'duplicates':[]", "'30004403' not in prior",'g.owned_log_append_check(pre)',"'wrong_used',g.regular(g.K,'turns.jsonl').read_bytes(),3,5",'len(plan[\'state_after\'])==39'],
      'verify_post_acceptance.py':["'targets':39","'consumed_substantive_turns':47", "'primary_acceptances':38",'exact_original17_and_corrected_PARTIAL_unchanged',"'30004403' not in current",'related_shared_original2of5_disclosed','g.owned_log_append_check(pre)'],
      'seal_final_evidence.py':['rename(os.fsencode(stage),os.fsencode(target),4)','g.basis(','--execute'],
      'capture_root_final_operation.py':["script.parent == A / 'acceptance_preparation_family' and script.name == 'seal_final_evidence.py'",'stdin=subprocess.DEVNULL','native13_before','PRELAUNCH_OPERATOR.py']}
    required_text['pr48_guards.py'].remove('exact original')
    for n,tokens in required_text.items():
        for token in tokens:insist(token in source[n],'Critical source text absent '+n+':'+token)
    for token in ['Seifert','instanton','REALIZED_DEGENERACY_PROOF','SOURCE_PROVENANCE_CORRECTION','OBSTRUCTION','one_turn_object','original1/5','Original1/5','exact_original16','whole_current1328']:
        insist(all(token not in s for s in source.values()),'Foreign inherited scope '+token)
    # Root5 and plan remain false/null; private specimens never claim real ROOT acceptance.
    for n in ['DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json']:
        z=load(F/n);insist(z['root_completed'] is False and z['actual_pid'] is None and z['created_utc'] is None and z['actual_PR47_predecessor_completed'] is False and z['future_acceptance_approved'] is False,'False/null pending ROOT')
    z=load(F/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json');insist(z['root_actual_PR47_predecessor_read_completed'] is False and z['previous_post'] is None and z['previous_root_post'] is None and type(z['original_substantive_attempts']) is int and z['original_substantive_attempts']==2,'Actual predecessor not manufactured; shared budget2');plan=load(F/'DRAFT_FINAL_PLAN.json');insist(plan['root_actual_PR47_predecessor_read_completed'] is False and type(plan['pr']) is int and plan['pr']==48 and type(plan['original_substantive_attempts']) is int and plan['original_substantive_attempts']==2,'Plan pending predecessor, literal48/shared2')
    emit('PRIVATE_CONTROL_OBSERVATIONS.json',observations)
    result={'schema':'pr48-acceptance-private-handwritten-controls/v1','status':'PASS_PRIVATE_PREDICATES_ONLY','actual_pid':os.getpid(),'assertions':assertions,'expected_negative_controls':len(observations),'actual_full_permission_modes':4096,'all_original_actual_Git_captures':38,'genuine_first33_null_Git_positive_subset':33,'literal_historical_and_final_typed_helpers':4,'full_bound_inputs_checked':checked,'full_bound_bytes_read':bytes_read,'current_payload':1946,'WHOLE_payload':162,'known_predecessor_source_payload':126,'canonical_overlay':1955,'canonical_accepted_payload':1957,'ROOT_post_keys':22,'alias_native_gap_disclosed':True,'source_sha256':{n:sha((F/n).read_bytes()) for n in NAMES},'proposed_source_imported_compiled_executed':False,'native_index_remote_mutated':False,'independent_adversarial_review_claimed':False,'actual47_predecessor_completed':False,'future_acceptance_approved':False};emit('PRIVATE_CONTROLS_RESULT.json',result);print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
