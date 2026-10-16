"""Independent bounded SOURCE predicate/OS controls; no production imports or execution.
All approval-shaped examples exist only in memory and are fabricated laboratory models.
"""
from pathlib import Path, PurePosixPath
import copy, ctypes, datetime as dt, errno, hashlib, json, math, os, re, stat, sys
F=Path(__file__).absolute().parent;R=Path('/Users/alec/Documents/Math');A=F.parent;S=A/'current_preparation_family';now=dt.datetime.now(dt.timezone.utc);cases=[];modes=[]
def require(x,n):
    if not x:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(b):
    def pairs(ps):
        d={}
        for k,v in ps:require(k not in d,'duplicate key');d[k]=v
        return d
    def number(t):
        x=float(t);require(math.isfinite(x),'nonfinite float');return x
    def const(t):raise ValueError('nonfinite constant')
    return json.loads(b,object_pairs_hook=pairs,parse_float=number,parse_constant=const)
def equal(a,b):return json.dumps(a,sort_keys=True,separators=(',',':'),allow_nan=False)==json.dumps(b,sort_keys=True,separators=(',',':'),allow_nan=False)
def path(n):
    require(type(n) is str and n and '\\' not in n and '\0' not in n,'path text');p=PurePosixPath(n);require(not p.is_absolute() and str(p)==n and not set(p.parts)&{'.','..','.git','__pycache__'},'canonical path');return n
def hex64(x):return type(x) is str and re.fullmatch('[0-9a-f]{64}',x) is not None
def utc(s):
    require(type(s) is str,'UTC string');t=dt.datetime.fromisoformat(s.replace('Z','+00:00'));require(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'aware UTC');return t
def rows(rs,mode=False):
    require(type(rs) is list,'rows list');names=set()
    for r in rs:
        require(type(r) is dict and set(r)==({'path','bytes','sha256','full_mode'} if mode else {'path','bytes','sha256'}),'exact row');n=path(r['path']);require(n not in names,'unique row');names.add(n);require(type(r['bytes']) is int and r['bytes']>=0 and hex64(r['sha256']),'typed bytes/SHA')
        if mode:require(type(r['full_mode']) is int and 0<=r['full_mode']<4096,'typed fullmode')
    return names
def structured(n,b):
    if n.endswith('.json'):strict(b)
    elif n.endswith('.jsonl'):
        try:strict(b)
        except (json.JSONDecodeError,UnicodeDecodeError):
            require(b==b'' or b.strip(),'blank history');
            for line in b.splitlines():require(line.strip(),'blank JSONL row');strict(line)
def regular(p):
    require(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular nonsymlink');return p.read_bytes()
def inventory(p):
    require(p.is_dir() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'regular directory');names=set();dirs=set()
    for q in p.rglob('*'):
        require(not q.is_symlink(),'symlink');n=path(q.relative_to(p).as_posix());m=q.stat().st_mode
        if stat.S_ISREG(m):names.add(n)
        else:require(stat.S_ISDIR(m),'special');dirs.add(n)
    require(dirs=={str(a) for n in names for a in PurePosixPath(n).parents if str(a)!='.'},'empty/extra directory');return names
def capture(c):
    require(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and type(c['operator_pid']) is int and c['operator_pid']==60012 and c['cwd']==str(R) and c['stdin_supplied'] is False and c['operator_unchanged'] is True and utc(c['started_utc'])<=utc(c['finished_utc'])<=now,'actual capture')
    if c['schema']=='pr49-root-actual-unchanged-helper/v1':rows([c['source']],True);require(c['source_unchanged'] is True and c['argv']==['/usr/bin/python3','-B',str(R/c['source']['path'])],'typed helper')
    else:require(c['schema']=='pr49-root-actual-readonly-git/v1' and c['source'] is None and c['source_unchanged'] is None and type(c['argv']) is list and len(c['argv'])>=2 and c['argv'][0]=='git' and c['argv'][1] in ('show','ls-tree','diff','merge-base'),'Git explicit null-null')
    rows([c['stdout'],c['stderr']],True);require(c['stderr']['bytes']==0,'successful stderr')
FLAGS=list(strict((S/'DRAFT_ROOT_PRIMARY_READ_LEDGER.json').read_bytes())['root_flags'])
NATIVE={'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}|{'draft_pr_publication_program_20260930/inventory.json'}
prep=strict((S/'PREPARATION_MANIFEST.json').read_bytes());preptime=utc(prep['created_utc']);prepSHA=sha((S/'PREPARATION_MANIFEST.json').read_bytes());qualSHA=sha((S/'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes());builderSHA=sha((S/'prepare_current_packet.py').read_bytes());operatorSHA=sha((S/'capture_root_builder_operation.py').read_bytes())
def root_records(v):
    # This is an independent normative conjunction model, never a ROOT certificate.
    require(type(v) is dict and set(v)=={'scope','reading','science','evidence','current','source_adversary','source_manifest','close','readback'},'whole model')
    scope=v['scope'];require(scope.splitlines()[0]=='# ROOT PR49 exact known-result acceptance' and scope.splitlines().count('ROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY')==1 and 'DRAFT' not in scope,'scope sentinel')
    for text in ['036a5ed59bee5ed79f08349290481584610f1456','c6975ca76f9f667f1250ba403d0e6da2aafe14d0','PR49 / 30000703 / OWR-1460-009','Status: already_solved','Original turns: 0/5; new: 0; audit: 0','Full exact target verified: true','Novelty: false','Kraus, Roth and Ruscheweyh (2007)','Imported journal proof independently certified: false','NEW whole-current review: PENDING','Paper/new DOI/tracker: false']:require(text in scope,'exact scope text')
    for key,schema in [('reading','primary-read-ledger'),('science','science-card'),('evidence','evidence-bindings')]:
        obj=v[key];require(obj['schema']=='pr49-root-'+schema+'/v1' and obj['approved_by_root'] is True and obj['operative_preparation_directory']=='current_preparation_family' and preptime<=utc(obj['created_utc'])<=now and obj['preparation_manifest_sha256']==prepSHA and obj['source_qualification_sha256']==qualSHA,'dated SOURCE pins')
    reading=v['reading'];science=v['science'];require(reading['reading_completed'] is True and equal(reading['root_flags'],{f:True for f in FLAGS}) and type(reading['reading_notes']) is str and len(reading['reading_notes'].strip())>=40,'personal reading')
    for k in ['exact_known_target_verified','full_problem_solved','full_target_prior_result_verified']:require(science[k] is True,'known full target')
    for k in ['project_solved','novelty_claimed','full_2007_journal_proof_independently_certified','paper_created','new_DOI_created','tracker_row_created']:require(science[k] is False,'qualification false')
    for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']:require(science[k] is None,'current null')
    require(science['status']=='already_solved' and science['credit']=='Kraus, Roth and Ruscheweyh (2007)' and science['new_whole_current_gate']=='PENDING','credited pending')
    for k,x in [('original_substantive_attempts',0),('turn_limit',5),('new_substantive_attempts',0),('audit_turns',0)]:require(type(science[k]) is int and science[k]==x,'typed turns')
    evidence=v['evidence'];require(science['scope_certificate_sha256']==reading['scope_certificate_sha256']==sha(scope.encode()) and science['evidence_bindings_sha256']==reading['evidence_bindings_sha256']==sha(json.dumps(evidence,sort_keys=True).encode()),'crosspins')
    for k,n in [('manifest','root_original_actual_reproduction/MANIFEST.json'),('summary','root_original_actual_reproduction/ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),('proof_notes','ROOT_MATHEMATICAL_REVIEW.md'),('raw_audit','ROOT_COMPLETE_RAW_SQL_AUDIT.json')]:require(evidence[k]['path']==A.relative_to(R).as_posix()+'/'+n,'evidence anchors');rows([evidence[k]],True)
    rows([evidence['source_adversary']],True)
    adv=v['source_adversary'];require(adv['schema']=='pr49-root-new-source-adversary-record/v1' and adv['approved_by_root'] is True and adv['complete_report_personally_read'] is True and adv['new_different_source_adversary'] is True and adv['closed_clean'] is True and adv['mandatory_corrections']==[] and adv['preparation_manifest_sha256']==prepSHA and adv['builder_sha256']==builderSHA and adv['operator_sha256']==operatorSHA and preptime<=utc(adv['created_utc'])<=now,'fresh SOURCE gate')
    m=v['source_manifest'];rows(m['files'],True);require(m['schema']=='pr49-current-source-adversary-self-only-closure/v1' and m['self_excluded']==['MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==len(m['files']) and all(r['full_mode']==292 for r in m['files']),'exact new adversary closure')
    normalized=[{k:r[k] for k in ('path','bytes','sha256')} for r in m['files']];root=PurePosixPath(adv['manifest']['path']).parent;require(equal(adv['members'],[dict(r,path=str(root/r['path'])) for r in normalized]) and adv['report']['path'] in {r['path'] for r in adv['members']},'all normalized members/report')
    rows([adv[k] for k in ['manifest','report','completed_closing_capture','completed_postexit_readback_capture']],True)
    for c in [v['close'],v['readback']]:
        require(c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['operator_unchanged'] is True and utc(c['started_utc'])<utc(c['finished_utc'])<=utc(adv['created_utc']),'CAP4 real metadata');rows([c['stdout'],c['stderr']])
    require(utc(v['close']['finished_utc'])<utc(v['readback']['started_utc']),'separate readback')
    current=v['current'];require(set(current)=={'schema','approved_by_root','created_utc','reason','current_head','files','operative_preparation_directory'} and current['schema']=='pr49-root-fresh13-input-preimages/v1' and current['approved_by_root'] is True and current['operative_preparation_directory']=='current_preparation_family' and preptime<=utc(current['created_utc'])<=now and type(current['reason']) is str and len(current['reason'].strip())>=40 and type(current['current_head']) is str and re.fullmatch('[0-9a-f]{40}',current['current_head']) and len(current['files'])==13 and rows(current['files'],True)==NATIVE,'all fresh13')
def check(name,fn,good):
    try:fn();passed=True
    except (ValueError,TypeError,KeyError,AttributeError,UnicodeDecodeError,OverflowError,json.JSONDecodeError,OSError):passed=False
    require(passed is good,'unexpected private predicate result '+name);cases.append({'name':name,'expected_acceptance':good,'actual_acceptance':passed})
def main():
    for n,b in [('valid_json',b'{"a":0,"b":true,"c":null}'),('pretty_whole_history',b'{\n "count":0\n}\n'),('empty_history',b''),('two_json_lines',b'{}\n{"a":0}\n')]:check(n,lambda n=n,b=b:structured('fixture.jsonl' if n!='valid_json' else 'fixture.json',b),True)
    for n,b in [('duplicate',b'{"a":1,"a":2}'),('nested_duplicate',b'{"a":{"x":0,"x":1}}'),('NaN',b'{"a":NaN}'),('Infinity',b'Infinity'),('overflow',b'1e9999'),('truncated',b'{'),('blank_row',b'{}\n\n{}'),('whitespace_history',b' \n'),('duplicate_jsonl',b'{}\n{"a":0,"a":1}')]:check(n,lambda b=b:structured('fixture.jsonl',b),False)
    for a,b in [(False,0),(True,1),(1,1.0),({'a':False},{'a':0}),(None,{})]:check('recursive_type_difference_'+repr(a),lambda a=a,b=b:require(equal(a,b),'type distinct'),False)
    for n in ['safe/body','file.json','Case','case'] :check('safe_path_'+n,lambda n=n:path(n),True)
    for n in ['', '.', '..','./a','a//b','a/./b','a/../b','/abs','a/','a\\b','a\0b','.git/x','x/__pycache__/y']:check('unsafe_path_'+repr(n),lambda n=n:path(n),False)
    base={'path':'body','bytes':1,'sha256':'0'*64,'full_mode':292};check('exact_full_row',lambda:rows([base],True),True)
    for key in base:
        for value in [None,True,False,{},[],1.0,'bad']:
            if value==base[key] and type(value)==type(base[key]):continue
            x=dict(base,**{key:value});check('bad_row_'+key+'_'+repr(value),lambda x=x:rows([x],True),False)
    for x in [dict(base,bytes=-1),dict(base,full_mode=-1),dict(base,full_mode=4096),dict(base,sha256='A'*64),dict(base,extra=0)]:check('bad_bound_'+repr(x),lambda x=x:rows([x],True),False)
    check('duplicate_rows',lambda:rows([base,base],True),False)
    repro=strict((A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json').read_bytes())
    for c in repro['complete_actual_Git_captures']+repro['complete_actual_helper_captures']:check('actual_cap_'+str(c['pid']),lambda c=c:capture(c),True)
    for sample in [repro['complete_actual_Git_captures'][0],repro['complete_actual_helper_captures'][0]]:
        for k in ['actual_execution','completed','operator_unchanged','stdin_supplied','pid','exit_code','operator_pid','source_unchanged']:
            for val in [None,False,True,0,1,0.0,'0',{},[]]:
                if equal(val,sample[k]):continue
                x=copy.deepcopy(sample);x[k]=val;check('capture_mutant_'+sample['schema']+'_'+k+'_'+repr(val),lambda x=x:capture(x),False)
        for k,val in [('schema','unknown'),('cwd','/tmp'),('finished_utc','2999-01-01T00:00:00+00:00'),('started_utc','2999-01-01T00:00:00+00:00'),('finished_utc','2026-01-01T00:00:00'),('source',{})]:
            x=copy.deepcopy(sample);x[k]=val;check('capture_semantics_'+k+'_'+sample['schema'],lambda x=x:capture(x),False)
    # A complete fabricated control model, expressly never saved as approval evidence.
    stamp=(preptime+dt.timedelta(seconds=1)).isoformat();scope='# ROOT PR49 exact known-result acceptance\nROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY\n'+'\n'.join(['036a5ed59bee5ed79f08349290481584610f1456','c6975ca76f9f667f1250ba403d0e6da2aafe14d0','PR49 / 30000703 / OWR-1460-009','Status: already_solved','Original turns: 0/5; new: 0; audit: 0','Full exact target verified: true','Novelty: false','Kraus, Roth and Ruscheweyh (2007)','Imported journal proof independently certified: false','NEW whole-current review: PENDING','Paper/new DOI/tracker: false'])
    record={k:strict((S/n).read_bytes()) for k,n in [('science','DRAFT_ROOT_SCIENCE_CARD.json'),('reading','DRAFT_ROOT_PRIMARY_READ_LEDGER.json'),('evidence','DRAFT_ROOT_EVIDENCE_BINDINGS.json'),('current','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json'),('source_adversary','DRAFT_ROOT_NEW_SOURCE_ADVERSARY_RECORD.json')]};record['scope']=scope
    for k in ('science','reading','evidence'):record[k].update(approved_by_root=True,created_utc=stamp,preparation_manifest_sha256=prepSHA,source_qualification_sha256=qualSHA)
    reading=record['reading'];reading.update(reading_completed=True,root_flags={f:True for f in FLAGS},reading_notes='Fabricated laboratory notes only, never an actual ROOT approval record.')
    science=record['science'];science.update(exact_known_target_verified=True,full_problem_solved=True,full_target_prior_result_verified=True)
    def fake(n):return dict(path=n,bytes=1,sha256='0'*64,full_mode=292)
    prefix=A.relative_to(R).as_posix()+'/'
    for k,n in [('manifest','root_original_actual_reproduction/MANIFEST.json'),('summary','root_original_actual_reproduction/ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),('proof_notes','ROOT_MATHEMATICAL_REVIEW.md'),('raw_audit','ROOT_COMPLETE_RAW_SQL_AUDIT.json')]:record['evidence'][k]=fake(prefix+n)
    record['evidence']['source_adversary']=fake(prefix+'LABORATORY_ONLY.json')
    for x in (science,reading):x.update(scope_certificate_sha256=sha(scope.encode()),evidence_bindings_sha256=sha(json.dumps(record['evidence'],sort_keys=True).encode()))
    adv=record['source_adversary'];adv.update(approved_by_root=True,created_utc=(preptime+dt.timedelta(seconds=5)).isoformat(),complete_report_personally_read=True,new_different_source_adversary=True,closed_clean=True,mandatory_corrections=[],preparation_manifest_sha256=prepSHA,builder_sha256=builderSHA,operator_sha256=operatorSHA,manifest=fake(prefix+'laboratory/MANIFEST.json'),report=fake(prefix+'laboratory/REPORT.md'),members=[{k:v for k,v in fake(prefix+'laboratory/REPORT.md').items() if k!='full_mode'}],completed_closing_capture=fake(prefix+'laboratory_closing/CAPTURE.json'),completed_postexit_readback_capture=fake(prefix+'laboratory_readback/CAPTURE.json'))
    record['source_manifest']=dict(schema='pr49-current-source-adversary-self-only-closure/v1',self_excluded=['MANIFEST.json'],files_count=1,files=[fake('REPORT.md')])
    for key,offset in [('close',1),('readback',3)]:record[key]=dict(schema='root-explicit-command-capture/v1',actual_execution=True,completed=True,pid=offset,exit_code=0,operator_unchanged=True,started_utc=(preptime+dt.timedelta(seconds=offset)).isoformat(),finished_utc=(preptime+dt.timedelta(seconds=offset+0.5)).isoformat(),stdout=dict(path='stdout.bin',bytes=1,sha256='0'*64),stderr=dict(path='stderr.bin',bytes=0,sha256=sha(b'')))
    record['current'].update(approved_by_root=True,created_utc=stamp,reason='Fabricated laboratory current native preimage, not an actual approval.',current_head='0'*40,files=[fake(n) for n in sorted(NATIVE)])
    check('full_normative_five_SOURCE_gate_model',lambda:root_records(record),True)
    for group in ['reading','science','evidence','source_adversary','current','source_manifest','close','readback']:
        for key,value in record[group].items():
            for val in [None,True,False,0,1,{},[],'INVALID']:
                if equal(val,value):continue
                x=copy.deepcopy(record);x[group][key]=val;check('whole_gate_mutant_'+group+'_'+key+'_'+repr(val),lambda x=x:root_records(x),False)
    for f in FLAGS:
        for val in [False,1,None]:x=copy.deepcopy(record);x['reading']['root_flags'][f]=val;check('read_flag_'+f+'_'+repr(val),lambda x=x:root_records(x),False)
    for target in ['scope','reading','science','evidence','source_adversary','current','source_manifest','close','readback']:
        x=copy.deepcopy(record);del x[target];check('missing_whole_prerequisite_'+target,lambda x=x:root_records(x),False)
    for group in ['reading','science','evidence','source_adversary','current']:
        for time in ['2999-01-01T00:00:00+00:00','2025-01-01T00:00:00+00:00','2026-10-03T07:25:00','2026-10-03T07:25:00-01:00']:
            x=copy.deepcopy(record);x[group]['created_utc']=time;check('nonfresh_time_'+group+'_'+time,lambda x=x:root_records(x),False)
    for key in ['files']:
        for val in [record['current']['files'][:-1],record['current']['files']+[record['current']['files'][0]],record['current']['files']+[fake('foreign')]]:
            x=copy.deepcopy(record);x['current'][key]=val;check('fresh13_wrong_set_'+str(len(val)),lambda x=x:root_records(x),False)
    d=F/'private_fixtures';d.mkdir(mode=0o700);fixture=d/'mode_fixture';fixture.write_bytes(b'full4096')
    for mode in range(4096):
        fixture.chmod(mode);actual=stat.S_IMODE(fixture.stat().st_mode);require(actual==mode,'actual chmod mode');modes.append({'requested_full_mode':mode,'actual_full_mode':actual});check('actual_mode_'+str(mode),lambda mode=mode:rows([dict(base,full_mode=mode)],True),True);check('mismatched_actual_mode_'+str(mode),lambda mode=mode,actual=actual:require(actual==(mode^0o4000),'changed full mode'),False)
    fixture.chmod(0o600)
    t=d/'topology';t.mkdir();(t/'body').write_bytes(b'body');check('real_topology',lambda:inventory(t),True);(t/'empty').mkdir();check('empty_directory',lambda:inventory(t),False);(t/'empty').rmdir();(t/'link').symlink_to(t/'body');check('symlink_file',lambda:inventory(t),False);check('symlink_body',lambda:regular(t/'link'),False);(t/'link').unlink();(d/'ancestor_link').symlink_to(t,target_is_directory=True);check('symlink_parent',lambda:regular(d/'ancestor_link/body'),False);(d/'ancestor_link').unlink()
    require(sys.platform=='darwin','macOS real OS controls');lib=ctypes.CDLL(None,use_errno=True);fn=lib.renamex_np;fn.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];fn.restype=ctypes.c_int
    src=d/'rename_source';src.write_bytes(b'source');dst=d/'rename_existing';dst.write_bytes(b'existing');rc=fn(os.fsencode(src),os.fsencode(dst),4);err=ctypes.get_errno();require(rc==-1 and err==errno.EEXIST and src.read_bytes()==b'source' and dst.read_bytes()==b'existing','real EXCL refusal');cases.append(dict(name='actual_macOS_RENAME_EXCL_existing_refusal',return_code=rc,errno=err))
    absent=d/'rename_absent';require(fn(os.fsencode(src),os.fsencode(absent),4)==0 and not src.exists() and absent.read_bytes()==b'source','real absent publication');cases.append(dict(name='actual_macOS_RENAME_EXCL_absent_success',return_code=0))
    upper=d/'CaseProbe';upper.write_bytes(b'upper');lower=d/'caseprobe';case_insensitive=lower.exists();require(not case_insensitive or lower.read_bytes()==b'upper','observed case collision')
    if case_insensitive:
        other=d/'case_source';other.write_bytes(b'other');require(fn(os.fsencode(other),os.fsencode(lower),4)==-1 and ctypes.get_errno()==errno.EEXIST and other.read_bytes()==b'other' and upper.read_bytes()==b'upper','exclusive case collision preserved')
    cases.append(dict(name='actual_filesystem_case_collision',case_insensitive=case_insensitive,canonical_case_names_distinct_in_predicate=path('Case')!=path('case')))
    result=dict(schema='pr49-current-source-adversary-private-controls/v1',status='PASS_BOUNDED_INDEPENDENT_PREDICATE_AND_MACOS_CONTROLS',actual_pid=os.getpid(),created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),cases_count=len(cases),negative_predicates_rejected=sum(v.get('expected_acceptance') is False for v in cases),cases=cases,actual_permission_mode_observations=modes,fabricated_approval_models_only_in_memory=True,production_imported_compiled_executed=False,helpers_executed=False,future_acceptance_approved=False,mandatory_corrections_found=[],limitations='These independent predicate/OS controls supplement source inspection. They do not execute production, prove full runtime correctness, authenticate ROOT authorship, or certify the future current packet.')
    with (F/'PRIVATE_CONTROL_RESULT.json').open('xb') as f:f.write((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','actual_permission_mode_observations')},sort_keys=True))
if __name__=='__main__':main()
