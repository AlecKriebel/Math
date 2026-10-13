#!/usr/bin/env python3
"""SOURCE ONLY: ROOT may execute after fresh SOURCE review and five genuine records.
Administrative copying/read-only Git only. Never execute any mathematical helper,
change native state, stage, commit, merge, publish a paper, create a DOI or contact people.
"""
import argparse, ctypes, datetime as dt, hashlib, json, math, os, re, stat, subprocess, sys, traceback
from pathlib import Path, PurePosixPath
HEAD='e2e5c8c3e5ad218f867fa753c465bb96b3687bda'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
MERGE_BASE='60292bed09f59236aa192cb17aa138f7b4750e1a'
SCIENCE='196568d2029fd378dfa43919efbf49dcbd11244a2de8c525483f84484f00e5fa'
HISTORICAL='0036b78ba3164a52c15a7a24ea73fe4438a3db3c9a206f2882070c23e91cd3b2'
GATE='PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'
FLAGS=['original17_complete18_path_diff_helpers_results_metadata_fully_read','complete_partial_compression_support_stabilization_scope_checked','raw_all15458_SQL_both_report_keys_ABSENT_literal_empty_fallback_fully_read','actual_ROOT38_Git_and_four_literal_historical_final_replays_fully_read','both_closed_independent_mathematical_family_reports_fully_read','duplicate_exact_target_shared2of5_budget_accepted','operative_provenance_review_and_historical_receipt_qualifications_fully_read','new_source_adversary_closed_clean_complete_report_personally_read']
HEADER=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
NATIVE={'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
NATIVE.add('draft_pr_publication_program_20260930/inventory.json')
IMMUTABLE=['PARTIAL.md','check_algebra.py','check_results.json','related_source_record.json','source_record.json','turns.jsonl','source_checksums.json','review/author_replay/check_algebra.py','review/author_replay/check_results.json','review/independent_checks.py','review/independent_results.json']
def require(value,message):
    if not value:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def encode(obj):return (json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
def equal(a,b):return json.dumps(a,sort_keys=True,separators=(',',':'),allow_nan=False)==json.dumps(b,sort_keys=True,separators=(',',':'),allow_nan=False)
def hex64(v):return type(v) is str and re.fullmatch('[0-9a-f]{64}',v) is not None
def clock(v):
    require(type(v) is str,'UTC text required');p=dt.datetime.fromisoformat(v[:-1]+'+00:00' if v.endswith('Z') else v)
    require(p.tzinfo is not None and p.utcoffset()==dt.timedelta(0),'Aware UTC required');return p
def load(raw):
    def pairs(items):
        out={}
        for k,v in items:require(k not in out,'Duplicate JSON key');out[k]=v
        return out
    def constant(v):raise ValueError('Nonfinite JSON constant')
    def floating(v):
        f=float(v);require(math.isfinite(f),'Nonfinite JSON number');return f
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)
def relative(v):
    require(type(v) is str and v and '\\' not in v and '\0' not in v,'POSIX path text required');p=PurePosixPath(v)
    require(not p.is_absolute() and p.as_posix()==v and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Unsafe relative path');return v
def regular(p):
    require(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink file required');return p.read_bytes()
def inventory(root):
    require(root.is_dir() and not root.is_symlink() and all(not q.is_symlink() for q in root.parents),'Regular nonsymlink directory required');files=set();dirs=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'Symlink member');n=relative(p.relative_to(root).as_posix())
        if stat.S_ISREG(p.stat().st_mode):files.add(n)
        else:require(stat.S_ISDIR(p.stat().st_mode),'Special member');dirs.add(n)
    expected={p.as_posix() for n in files for p in PurePosixPath(n).parents if p.as_posix()!='.'}
    require(dirs==expected,'Extra/empty directory');return files

def rows(items,with_mode=False):
    require(type(items) is list,'List of exact rows required');names=set()
    for r in items:
        require(type(r) is dict and set(r)==({'path','bytes','sha256','full_mode'} if with_mode else {'path','bytes','sha256'}),'Exact typed row schema')
        n=relative(r['path']);require(n not in names,'Duplicate row');names.add(n)
        require(type(r['bytes']) is int and r['bytes']>=0 and hex64(r['sha256']),'Typed bytes/SHA required')
        if with_mode:require(type(r['full_mode']) is int and 0<=r['full_mode']<0o10000,'Typed full mode')
    return names

def structured(name,raw):
    if name.endswith('.json'):load(raw)
    elif name.endswith('.jsonl'):
        # Historical selected wrappers may be pretty whole JSON. True turn/history ledgers are JSONL.
        try:load(raw)
        except (json.JSONDecodeError,UnicodeDecodeError):
            require(bool(raw.strip()),'Empty JSONL rejected')
            for line in raw.splitlines():require(bool(line.strip()),'Blank JSONL row');load(line)
def publish_absent(src,dst):
    require(sys.platform=='darwin','Reviewed macOS exclusive rename required');lib=ctypes.CDLL(None,use_errno=True);fn=lib.renamex_np
    fn.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];fn.restype=ctypes.c_int
    if fn(os.fsencode(src),os.fsencode(dst),4)!=0:n=ctypes.get_errno();raise OSError(n,os.strerror(n),str(dst))
def build(args,script,A,R,attempt):
    dest=A/'reviewed_candidate';require(not dest.exists() and not dest.is_symlink(),'Never overwrite a candidate');outputs={};dependencies={};commands=[]
    def bind(name,role,expected=None,mode=None):
        name=relative(name);p=R/name;raw=regular(p);r={'path':name,'bytes':len(raw),'sha256':sha(raw),'full_mode':stat.S_IMODE(p.stat().st_mode),'roles':[role]}
        require(expected is None or r['sha256']==expected,'Pinned body changed');require(mode is None or r['full_mode']==mode,'Pinned full mode changed')
        if name in dependencies:
            old=dependencies[name];require(all(old[k]==r[k] for k in ['path','bytes','sha256','full_mode']),'Repeated input changed');r['roles']=sorted(set(old['roles']+r['roles']))
        dependencies[name]=r;return raw
    def checked(r,role):
        require(type(r) is dict and set(r) in ({'path','bytes','sha256'},{'path','bytes','sha256','full_mode'}),'Typed referenced row required')
        rows([{k:r[k] for k in ['path','bytes','sha256']}]);raw=bind(r['path'],role,r['sha256'],r.get('full_mode'));require(len(raw)==r['bytes'],'Pinned size changed');return raw
    def local(name,role,expected=None):return bind(A.relative_to(R).as_posix()+'/'+relative(name),role,expected)
    def git(*argv):
        require(argv and argv[0] in {'branch','rev-parse','show','ls-tree','diff','merge-base'},'Read-only Git only');require(argv[0]!='branch' or argv[1:]==('--show-current',),'Read-only branch only')
        d=attempt/'git';d.mkdir(exist_ok=True);i=len(commands);c={'argv':['git',*argv],'cwd':str(R),'started_utc':utc(),'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False};commands.append(c)
        try:
            with (d/(str(i)+'.stdout')).open('xb') as out,(d/(str(i)+'.stderr')).open('xb') as err:
                child=subprocess.Popen(c['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));c.update(actual_execution=True,pid=child.pid)
                try:c['exit_code']=child.wait(timeout=60);c['completed']=True
                except BaseException:child.kill();c['exit_code']=child.wait();raise
        except BaseException:c['failure']=traceback.format_exc();raise
        finally:
            c['finished_utc']=utc()
            for channel in ['stdout','stderr']:
                p=d/(str(i)+'.'+channel)
                if p.exists():b=regular(p);c[channel]={'path':p.relative_to(attempt).as_posix(),'bytes':len(b),'sha256':sha(b)}
            (attempt/'GIT_COMMANDS.json').write_bytes(encode(commands))
        require(c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0,'Actual Git failed, preserved');require(not regular(d/(str(i)+'.stderr')),'Unexpected Git stderr');return regular(d/(str(i)+'.stdout'))
    prepraw=local('current_preparation_family/PREPARATION_MANIFEST.json','closed_SOURCE');prep=load(prepraw)
    require(prep['schema']=='pr48-current-source-only-closure/v1' and prep['self_excluded']==['PREPARATION_MANIFEST.json'] and type(prep['files_count']) is int and prep['files_count']==len(prep['files']),'Closed SOURCE required')
    preparer_names=rows(prep['files']);require(inventory(script.parent)==preparer_names|{'PREPARATION_MANIFEST.json'},'Exact SOURCE topology required')
    for r in prep['files']:outputs['build/source_preparation/'+r['path']]=local('current_preparation_family/'+r['path'],'closed_SOURCE_member',r['sha256']);require(len(outputs['build/source_preparation/'+r['path']])==r['bytes'] and stat.S_IMODE((script.parent/r['path']).stat().st_mode)==0o444,'SOURCE mode/size changed')
    require(stat.S_IMODE((script.parent/'PREPARATION_MANIFEST.json').stat().st_mode)==0o444,'SOURCE manifest full0444');outputs['build/source_preparation/PREPARATION_MANIFEST.json']=prepraw
    pins=load(local('current_preparation_family/STATIC_INPUT_BINDINGS.json','fixed_SOURCE_inputs'));require(pins['schema']=='pr48-fixed-current-source-inputs/v1' and pins['status']=='SOURCE_ONLY_ROOT_PREREQUISITES_PENDING' and pins['production_builder_executed'] is False and pins['future_acceptance_approved'] is False,'SOURCE-only status required')
    fixed_names=rows(pins['fixed_rows'],True)
    for r in pins['fixed_rows']:outputs['fixed_evidence/'+r['path']]=checked(r,'completed_first_party_fixed_evidence')
    for key,info in pins['closed_inputs'].items():
        m=load(checked(info['manifest'],'closed_'+key));require(m['schema']==info['schema'] and equal(m['self_excluded'],True if key=='smooth' else [info['self_name']]) and type(m['files_count']) is int and m['files_count']==len(m['files']),'Distinct true self-only schema required');root=R/info['root']
        names={r['path'] for r in m['files']};require(names=={PurePosixPath(r['path']).relative_to(info['root']).as_posix() for r in info['members']},'Closed rows changed')
        if key=='original':
            owned=set(info['authorship_root_files'])
            for sub in info['authorship_directory_roots']:owned|={sub+'/'+n for n in inventory(root/sub)}
        else:owned=inventory(root)-{info['self_name']}
        require(owned==names,'Scoped original/family topology changed')
        actualdirs={'.'}|{p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix()!='.'}
        require(actualdirs=={r['path'] for r in info['directories']},'Complete directory set changed')
        for r in info['directories']:require(type(r['full_mode']) is int and stat.S_IMODE((root/r['path']).stat().st_mode)==r['full_mode'],'Directory full mode changed')
        for r in info['members']:require(r['full_mode']==0o444,'Closed member full0444 required');checked(r,'closed_member')
    exceptions={r['path']:r for r in pins['exact_literal_structured_exceptions']}
    require(set(exceptions)<=fixed_names,'Only pinned archived exceptions')
    for name in fixed_names:
        b=regular(R/name)
        if name in exceptions:require(len(b)==exceptions[name]['bytes'] and sha(b)==exceptions[name]['sha256'] and exceptions[name]['interpretation']=='IMMUTABLE_LITERAL_ARCHIVED_FAILED_OR_NONJSON_STREAM','Exact archived stream exception only')
        else:structured(name,b)
    require(git('branch','--show-current').strip()==b'main','Stay on main');snapraw=local('snapshot_manifest.json','original17');snap=load(snapraw)
    require(snap['schema']=='pr48-original-source-snapshot/v1' and snap['head']==HEAD and snap['github_base']==BASE and snap['merge_base']==MERGE_BASE and snap['original_files']==len(snap['files'])==17,'Exact original17 snapshot')
    original={}
    for r in snap['files']:
        n=relative(r['relative_path']);native='unsolved_math_prioritization/attempts/2961/'+n;require(r['path']==native and r['git_mode']=='100644' and r['snapshot_full_mode']==0o444 and type(r['git_object']) is str and re.fullmatch('[0-9a-f]{40}',r['git_object']),'Original blob schema/mode')
        b=local('source_snapshot/'+n,'immutable_original17',r['sha256']);require(len(b)==r['bytes'] and git('show',HEAD+':'+native)==b and git('ls-tree',HEAD,'--',native).decode().strip()=='100644 blob '+r['git_object']+'\t'+native,'Original Git bytes/blob/mode');original[n]=b
    require(inventory(A/'source_snapshot')==set(original) and sha(original['PARTIAL.md'])==SCIENCE,'Exact science body required');require(git('merge-base',HEAD,BASE).decode().strip()==MERGE_BASE,'Actual merge base differs')
    meta=load(local('original_pr_metadata.json','original_metadata'));diff=checked(meta['full_diff'] | {'path':A.relative_to(R).as_posix()+'/'+meta['full_diff']['path']},'original_whole_diff')
    require(meta['head']==HEAD and meta['github_base']==BASE and meta['merge_base']==MERGE_BASE and meta['changed_files']==18 and len(diff)==80679 and sha(diff)=='994b4bbd4993227d1100cbd9d7493de776c6619c9daa379dca7f4ef3b3a26698' and git('diff','--no-ext-diff','--no-textconv','--binary',MERGE_BASE,HEAD,'--')==diff,'Whole18path original diff differs')
    require(git('diff','--name-only',MERGE_BASE,HEAD).decode().splitlines()==[r['path'] for r in meta['all_changed_paths']],'Complete changed paths differ')
    ledger=[load(line) for line in original['turns.jsonl'].splitlines()];require(len(ledger)==2 and [r['turn'] for r in ledger]==[1,2] and all(type(r['turn']) is int for r in ledger),'Exact two-entry original ledger')
    author=load(original['check_results.json']);independent=load(original['review/independent_results.json']);require(author['all_passed'] is True and type(author['assertions']) is int and author['assertions']==6570 and author['partial_sha256']==HISTORICAL,'Historical6570 receipt input');require(independent['status']=='PASS' and type(independent['assertions']) is int and independent['assertions']==228 and sum(independent['checks'].values())==228 and independent['sympy_version']=='1.14.0','Independent228 receipt')
    for n,ident,code in [('source_record.json',2961,'KP-4.85'),('related_source_record.json',30004403,'OWR-17471-009')]:s=load(original[n]);require(type(s['id']) is int and s['id']==ident and s['problem_number']==code and 'problem' not in s,'Plain raw integer ID records')
    result=load(local('root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json','ROOT_actual_result'));summary=load(local('root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json','ROOT_closed_summary'))
    require(result['schema']=='pr48-root-original-complete-reproduction/v1' and result['status']=='PASS_ROOT_ORIGINAL_AND_HISTORICAL_FINAL_REPRODUCTION' and result['actual_operator_pid']==11716 and result['original_head']==HEAD and result['actual_merge_base']==MERGE_BASE and result['github_base']==BASE and equal(result['entire_original_author_result'],author) and equal(result['entire_historical_independent_result'],independent) and equal(result['complete_original_turns'],ledger),'Complete genuine ROOT reproduction')
    require(summary['schema']=='pr48-root-current-complete-reproduction-summary/v1' and summary['status']=='PASS_ROOT_COMPLETED_FIRST_PARTY_REPRODUCTION' and equal(summary['entire_reproduction_result'],result) and summary['full_problem_solved'] is False and summary['future_acceptance_approved'] is False and summary['duplicate_shared_budget'] is True,'ROOT dated summary exact')
    caps=result['complete_actual_helper_captures'];gitcaps=result['complete_actual_Git_captures'];require(type(caps) is list and len(caps)==4 and type(gitcaps) is list and len(gitcaps)==38,'Exactly four literal helpers and38 Git')
    for c in caps+gitcaps:
        require(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and type(c['actual_operator_pid']) is int and c['actual_operator_pid']==11716 and c['cwd']==str(R) and c['operator_unchanged'] is True and clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Genuine completed actual ROOT capture')
        if c['schema']=='pr48-root-unchanged-helper-actual-capture/v1':
            require(type(c['source']) is dict and c['source_unchanged'] is True and c['argv']==['/usr/bin/python3','-B',str(R/c['source']['path'])],'Typed unchanged literal helper');checked(c['source'],'actual_helper_source')
        else:
            require(c['schema']=='pr48-root-readonly-git-actual-capture/v1' and c['source'] is None and c['source_unchanged'] is None and type(c['argv']) is list and len(c['argv'])>=2 and c['argv'][0]=='git' and c['argv'][1] in {'show','ls-tree','diff','merge-base'},'Read-only Git explicit null source convention')
        for stream in ['stdout','stderr']:checked(c[stream],'actual_ROOT_'+stream)
        require(c['stderr']['bytes']==0,'Original successful ROOT child stderr must be empty')
    replay=result['entire_historical_and_final_replayed_results'];require(equal(replay['author_historical'],author) and equal(replay['identical_submitted_historical'],author) and result['identical_submitted_counted_independent'] is False and equal(replay['author_final'],dict(author,partial_sha256=SCIENCE)) and result['final_author_receipt_only_partial_sha256_changes'] is True,'Old and final hash coverage exact; duplicate not independent')
    raw=load(local('ROOT_COMPLETE_RAW_SQL_AUDIT.json','ROOT_full_raw_SQL'));require(raw['schema']=='pr48-root-in-place-complete-raw-sql-audit/v1' and raw['status']=='PASS_FULL_RAW_PRIOR_SQL_AND_TWO_ORIGINAL_PLAIN_SOURCES' and type(raw['actual_pid']) is int and raw['actual_pid']==16308 and type(raw['full_raw_and_prior_bytes']) is int and raw['full_raw_and_prior_bytes']==149266659 and type(raw['all_SQL_rows']) is int and raw['all_SQL_rows']==len(raw['complete_row_bindings'])==15458 and raw['raw_or_SQL_or_foreign_source_bodies_copied'] is False and raw['future_acceptance_approved'] is False,'Complete raw audit exact')
    selected=raw['complete_selected_source_bindings'];require(type(selected) is list and {r['key'] for r in selected}=={'2961','30004403'},'Both selected raw sources')
    for r in selected:require(r['complete_saved_source_equals_raw_selected'] is True and r['raw_key_presence']=='ABSENT' and r['raw_present_null'] is False and r['sqlite_literal_fallback']=='{}' and equal(r['SQLite_typed_fallback'],{}) and r['original_prior_report_file_exists'] is False,'Absence is not null; no original prior file')
    algebra=load(local('algebra_cocycle_family/VERDICT.json','algebra_verdict'));smooth=load(local('smooth_geometry_family/VERDICT.json','smooth_verdict'));require(algebra['mathematical_verdict']=='PASS_STATED_PARTIAL_RESULTS' and algebra['mandatory_mathematical_corrections']==[] and algebra['full_target_resolved'] is False and smooth['mathematical_partial']=='PASS' and smooth['mathematical_repairs_required']==[] and smooth['open_problem_outcome']=='unsolved','Both independent mathematical partials pass; repairs remain source only')
    future={}
    for n,k in [('ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','root_scope_certificate_sha256'),('ROOT_PRIMARY_READ_LEDGER.json','root_read_ledger_sha256'),('ROOT_SCIENCE_CARD.json','root_science_card_sha256'),('ROOT_CURRENT_INPUT_PREIMAGES.json','root_current_input_manifest_sha256'),('ROOT_EVIDENCE_BINDINGS.json','root_evidence_bindings_sha256')]:future[n]=local(n,'genuine_ROOT_separate_prerequisite',getattr(args,k))
    qualification=local('current_preparation_family/SOURCE_PRECISION_QUALIFICATIONS.md','global_operative_qualification')
    scope=future['ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md'].decode();require(scope.splitlines()[0]=='# ROOT PR48 exact unresolved partial acceptance' and scope.splitlines().count('ROOT_SCOPE_ACCEPTED_EXACT_UNSOLVED_PARTIAL_ONLY')==1 and 'DRAFT' not in scope,'Actual ROOT scope, never a draft')
    for literal in [HEAD,BASE,MERGE_BASE,'Status: unsolved','Original shared turns: 2/5; new: 0; audit: 0','Full target resolved: false','Novelty: false','Duplicate: 30004403 / OWR-17471-009','NEW whole-current review: PENDING','Paper/new DOI/tracker: false']:require(literal in scope,'Missing exact ROOT scope literal')
    evidence=load(future['ROOT_EVIDENCE_BINDINGS.json']);reading=load(future['ROOT_PRIMARY_READ_LEDGER.json']);science=load(future['ROOT_SCIENCE_CARD.json'])
    for obj,schema in [(evidence,'pr48-root-evidence-bindings/v1'),(reading,'pr48-root-primary-read-ledger/v1'),(science,'pr48-root-science-card/v1')]:
        require(obj['schema']==schema and obj['approved_by_root'] is True and obj['operative_preparation_directory']=='current_preparation_family' and clock(prep['created_utc'])<=clock(obj['created_utc'])<=dt.datetime.now(dt.timezone.utc) and obj['preparation_manifest_sha256']==sha(prepraw) and obj['source_qualification_sha256']==sha(qualification),'Genuine dated ROOT prerequisites pin actual closed SOURCE')
    require(reading['reading_completed'] is True and equal(reading['root_flags'],{f:True for f in FLAGS}) and type(reading['reading_notes']) is str and len(reading['reading_notes'].strip())>=40,'ROOT complete personal reading')
    require(science['status']=='unsolved' and science['full_problem_solved'] is False and science['project_solved'] is False and science['novelty_claimed'] is False and science['duplicate_id']==30004403 and science['duplicate_shared_budget'] is True and type(science['original_substantive_attempts']) is int and science['original_substantive_attempts']==2 and type(science['turn_limit']) is int and science['turn_limit']==5 and type(science['new_substantive_attempts']) is int and science['new_substantive_attempts']==0 and type(science['audit_turns']) is int and science['audit_turns']==0 and all(science[k] is False for k in ['paper_created','new_DOI_created','tracker_row_created']) and all(science[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']) and science['new_whole_current_gate']=='PENDING','Scoped partial; no future/current runtime invented')
    for obj in [reading,science]:require(obj['scope_certificate_sha256']==args.root_scope_certificate_sha256 and obj['evidence_bindings_sha256']==args.root_evidence_bindings_sha256,'ROOT cross-pins')
    for key,name in [('manifest','root_original_actual_reproduction_v2/MANIFEST.json'),('summary','root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),('proof_notes','ROOT_MATHEMATICAL_REVIEW.md'),('raw_audit','ROOT_COMPLETE_RAW_SQL_AUDIT.json')]:require(evidence[key]['path']==A.relative_to(R).as_posix()+'/'+name,'Exact ROOT evidence anchors');checked(evidence[key],'ROOT_evidence')
    advraw=checked(evidence['source_adversary'],'new_SOURCE_adversary_record');adv=load(advraw)
    require(adv['schema']=='pr48-root-new-source-adversary-record/v1' and adv['approved_by_root'] is True and adv['complete_report_personally_read'] is True and adv['new_different_source_adversary'] is True and adv['closed_clean'] is True and adv['mandatory_corrections']==[] and adv['preparation_manifest_sha256']==sha(prepraw) and adv['builder_sha256']==sha(regular(script)) and adv['operator_sha256']==sha(regular(script.parent/'capture_root_builder_operation.py')) and clock(prep['created_utc'])<=clock(adv['created_utc'])<=dt.datetime.now(dt.timezone.utc),'New independent SOURCE review, not inherited PASS')
    advmraw=checked(adv['manifest'],'new_SOURCE_manifest');advm=load(advmraw);advroot=(R/adv['manifest']['path']).parent;selfname=Path(adv['manifest']['path']).name
    require(advm['self_excluded']==[selfname] and type(advm['files_count']) is int and advm['files_count']==len(advm['files']),'New SOURCE self-only closure')
    normalized=[{k:r[k] for k in ['path','bytes','sha256']} for r in advm['files']];require(inventory(advroot)==rows(normalized)|{selfname},'Exact fresh SOURCE closure topology')
    normalizedrepo=[dict(r,path=advroot.relative_to(R).as_posix()+'/'+r['path']) for r in normalized];require(equal(adv['members'],normalizedrepo),'ROOT normalized member rows exact')
    require(adv['report']['path'] in {r['path'] for r in normalizedrepo},'Complete fresh report belongs to closure');checked(adv['report'],'new_SOURCE_complete_report')
    outputs['new_source_adversary_evidence/'+adv['manifest']['path']]=advmraw
    for r in normalizedrepo:require(stat.S_IMODE((R/r['path']).stat().st_mode)==0o444,'Fresh reviewer full0444');outputs['new_source_adversary_evidence/'+r['path']]=checked(r,'new_SOURCE_member')
    require(stat.S_IMODE((R/adv['manifest']['path']).stat().st_mode)==0o444,'Fresh reviewer manifest full0444');outputs['root_approval/ROOT_NEW_SOURCE_ADVERSARY_RECORD.json']=advraw
    current=load(future['ROOT_CURRENT_INPUT_PREIMAGES.json']);require(set(current)=={'schema','approved_by_root','created_utc','reason','current_head','files','operative_preparation_directory'} and current['schema']=='pr48-root-fresh13-input-preimages/v1' and current['approved_by_root'] is True and current['operative_preparation_directory']=='current_preparation_family' and clock(prep['created_utc'])<=clock(current['created_utc'])<=dt.datetime.now(dt.timezone.utc) and type(current['reason']) is str and len(current['reason'].strip())>=40 and type(current['current_head']) is str and re.fullmatch('[0-9a-f]{40}',current['current_head']) and rows(current['files'],True)==NATIVE and len(current['files'])==13,'ROOT actual fresh13/head authority')
    def validate_native():
        require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==current['current_head'],'Approved current main changed')
        for r in current['files']:checked(r,'actual_live_native13')
    validate_native();native4=['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json']
    for n in native4:require(git('show',current['current_head']+':'+n)==regular(R/n),'Native4 committed/live differ');git('ls-tree',current['current_head'],'--',n)
    outername=relative(os.environ.get('PR48_ROOT_OUTER_CAPTURE',''));require(re.fullmatch(r'tmp/root_pr48_current_outer_[0-9]{8}T[0-9]{6}\.[0-9]{6}Z',outername),'Actual outer prelaunch required')
    outerraw=local(outername+'/OPERATION_PRELAUNCH.json','actual_outer_prelaunch');outer=load(outerraw)
    require(outer['schema']=='pr48-root-builder-prelaunch/v1' and type(outer['operator_pid']) is int and outer['operator_pid']==os.getppid() and outer['builder_sha256']==sha(regular(script)) and outer['operator_sha256']==sha(regular(script.parent/'capture_root_builder_operation.py')) and outer['argv']==['/usr/bin/python3','-B',str(script),*sys.argv[1:]] and outer['cwd']==str(R) and clock(outer['started_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual parent/source/argv/cwd')
    for n,k in [('PRELAUNCH_BUILDER_SOURCE.py','builder_sha256'),('PRELAUNCH_OPERATOR.py','operator_sha256')]:outputs['build/root_outer_prelaunch/'+n]=local(outername+'/'+n,'actual_outer_source',outer[k])
    outputs['build/root_outer_prelaunch/OPERATION_PRELAUNCH.json']=outerraw
    outputs['CURRENT_EXECUTION_REFERENCE.json']=encode({'audit_relative_outer_capture':outername,'outer_parent_pid':os.getppid(),'audit_relative_inner_attempt':attempt.relative_to(A).as_posix(),'actual_builder_pid':os.getpid(),'outer_prelaunch_sha256':sha(outerraw),'complete_outer_capture_written_only_after_child_exit':True,'final_inner_GIT_COMMANDS_written_incrementally_by_builder_before_exit':True,'frozen_inner_command_copy_is_prepublication_prefix':True,'outer_operator_does_not_write_inner_GIT_COMMANDS':True,'ROOT_final_original_inner_commands_inspection_required_AFTER_child_exit':True,'ROOT_must_read_final_actual_outer_and_inner_at_original_paths':True,'already_complete_outer_receipt_or_whole_PASS_certified':False})
    queue=regular(R/'unsolved_math_prioritization/QUEUE.md');lines=queue.splitlines(keepends=True);require(sum(line.startswith(b'|') and [v.strip() for v in line.decode().split('|')[1:-1]]==HEADER for line in lines)==1,'Unique named queue header')
    replacements={};changes=[];absent_queue_labels=[];indexes={n:HEADER.index(n)+1 for n in HEADER}
    finding='Accepted UNSOLVED partial: ambient cl(f x id_S2)<=4 on the stabilized subgroup, and exact signed pushforward defect/invariant-probability obstruction. Full closed orientable smooth4D Diff0 ordinary-length target unresolved. Exact duplicate2961/30004403 shares original2/5; new0; audit0. No novelty/paper/DOI/tracker. NEW whole-current review PENDING.'
    for label in ['2961 / KP-4.85','30004403 / OWR-17471-009']:
        hits=[(line,line.decode().split('|')) for line in lines if line.startswith(b'|') and len(line.decode().split('|'))==len(HEADER)+2 and line.decode().split('|')[indexes['ID / code']].strip()==label]
        if label=='30004403 / OWR-17471-009' and not hits:absent_queue_labels.append(label);continue
        require(len(hits)==1,'Unique existing target row');before,fields=hits[0]
        require(fields[indexes['Status']].strip()=='queued' and fields[indexes['Turns']].strip()=='0/5','Expected queued0/5 target preimage')
        afterfields=list(fields)
        for name,value in [('Status','unsolved'),('Turns','2/5'),('Findings',finding)]:afterfields[indexes[name]]=' '+value+' '
        require(all(a==b for i,(a,b) in enumerate(zip(fields,afterfields)) if i not in {indexes[n] for n in ['Status','Turns','Findings']}),'All other columns including Chat/DOI unchanged');after='|'.join(afterfields).encode();replacements[before]=after;changes.append({'id_code':label,'row_before':before.decode(),'row_prospective':after.decode()})
    prospective=b''.join(replacements.get(line,line) for line in lines);overview=local('current_preparation_family/CURRENT_OVERVIEW.md','operative_overview');sourceaudit=local('current_preparation_family/OPERATIVE_SOURCE_AUDIT.md','operative_source_repair');notice=local('current_preparation_family/HISTORICAL_ORIGINAL_NOTICE.md','historical_qualification')
    outputs.update({'original_archive/'+n:b for n,b in original.items()});outputs.update({n:original[n] for n in IMMUTABLE})
    for n in ['README.md','CURRENT_CONTEXT.md','PR_DRAFT.md','pr_body.md']:outputs[n]=overview+b'\n'+qualification
    outputs.update({'SOURCE_AUDIT.md':sourceaudit,'SOURCE_PRECISION_QUALIFICATIONS.md':qualification,'HISTORICAL_ORIGINAL_NOTICE.md':notice,'review/REVIEW.md':qualification+b'\n'+notice+original['review/REVIEW.md'],'CURRENT_ORIGINAL_RESEARCH_LOG.md':qualification+b'\n'+notice+original['RESEARCH_LOG.md'],'original_snapshot_manifest.json':snapraw,'original_diff.patch':diff})
    common={'id':2961,'problem_number':'KP-4.85','duplicate_id':30004403,'duplicate_code':'OWR-17471-009','duplicate_shared_budget':True,'status':'unsolved','full_problem_solved':False,'project_solved':False,'novelty_claimed':False,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'current_verdict':None,'new_whole_current_gate':GATE,'human_peer_review_claimed':False,'paper_created':False,'new_DOI_created':False,'tracker_row_created':False,'historical_PASS_transferred':False,'historical_runtime_certified':False,'strongest_verified_partial':'Ambient commutator length at most four for f x id_S2 on M x S2; exact averaging signed-pushforward term and invariant-probability obstruction.','exact_remaining_gap':'No unbounded ordinary ambient commutator-length sequence in one required full smooth closed orientable4D group and no theorem excluding every example.','global_qualification':'SOURCE_PRECISION_QUALIFICATIONS.md','current_publication_gap':'NEW whole-current review and ROOT actual reconciliation/integration'}
    for n in ['status.json','readiness.json','review/verdict.json','review/review_summary.json']:outputs[n]=encode(common)
    outputs['CURRENT_PRECISION_RECEIPT.json']=encode({'original17_archive_byte_exact':True,'immutable_literal_helpers_results_plain_sources_and_two_entry_ledger':True,'both_report_keys_ABSENT_SQLite_literal_empty_fallback_no_priorfile':True,'historical_author6570_receipt_bound_to_genuine_pre_review_Git_note':HISTORICAL,'actual_final6570_replay_only_partial_sha256_changed_to':SCIENCE,'duplicated_author_copy_not_independent':True,'independent228_byte_type_exact':True,'ambient_four_bound_only_included_subgroup_not_full_group':True,'Borel_cocycle_diagnostic_not_smooth_geometric_full_target_solution':True,'original_model_and_review_state_are_dated_attribution':True,'native4_proposals_not_future_merge_authority':True,'foreign_raw_SQL_PDF_OCR_pixels_headers_cookies_never_copied':True,'new_whole_current_gate':'PENDING'})
    outputs['CURRENT_QUEUE_PATCH.json']=encode({'phase':'LOCAL_PROPOSAL_ONLY_NO_NATIVE_WRITE','target_ids':[2961,30004403],'existing_rows_only':True,'absent_queue_labels':absent_queue_labels,'single_shared_turn_allocation':'2/5','allowed_named_changes':['Status','Turns','Findings'],'whole_preimage_sha256':sha(queue),'whole_prospective_sha256':sha(prospective),'changes':changes,'all_other_rows_columns_Chat_DOI_byte_preserved':True})
    for n in native4:
        label=n.replace('/','__');b=regular(R/n);outputs['native4_proposal/preimage/'+label]=b;outputs['native4_proposal/prospective/'+label]=prospective if n.endswith('/QUEUE.md') else b
    outputs['native4_proposal/PROPOSAL_SCOPE.json']=encode({'phase':'PENDING_NATIVE_ACCEPTANCE_LOCAL_PROPOSAL_ONLY','QUEUE_named_changes':['Status','Turns','Findings'],'selected_ids':[2961,30004403],'absent_queue_labels':absent_queue_labels,'no_missing_queue_row_created':True,'duplicate_shared_budget':'2/5','state_history_inventory_prospective':'UNCHANGED_BYTE_EXACT','native_acceptance_requires_later_ROOT_saved_full_plan_and_fresh13_currentHEAD':True})
    outputs.update({'root_approval/'+n:b for n,b in future.items()});outputs['RESEARCH_LOG.md']=(utc()+' — Actual administrative freeze; source audit75%; full-target discovery0%. UNSOLVED, one shared original2/5; new0; audit0. NEW whole-current review PENDING. No paper/DOI/tracker.\n').encode()
    def validate_dependencies():
        for r in dependencies.values():b=regular(R/r['path']);require(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE((R/r['path']).stat().st_mode)==r['full_mode'],'Dependency body/full mode changed')
    validate_dependencies();validate_native();outputs['CURRENT_DEPENDENCIES.json']=encode({'resolution':'repository_root / files.path; never scratch','files':sorted(dependencies.values(),key=lambda r:r['path']),'current_native13':current['files'],'current_main_head':current['current_head'],'stable9_live_required_by_later_whole_review':True,'fresh13_new_authority_required_again_before_final_acceptance':True})
    retained=[]
    for d in sorted((A/'tmp').glob('root_pr48_current_build_*')):
        require(d.is_dir() and not d.is_symlink(),'Actual retained attempt directory');members=[]
        for n in sorted(inventory(d)):
            b=regular(d/n);members.append({'path':n,'bytes':len(b),'sha256':sha(b)})
            if d==attempt:outputs['build/actual_attempt_prepublication_prefix/'+n]=b
        retained.append({'audit_relative_directory':d.relative_to(A).as_posix(),'files':members,'current_attempt_listing_is_prepublication_prefix':d==attempt,'positive_packet_claimed':False})
    outputs['build/RETAINED_ACTUAL_ATTEMPT_TREES.json']=encode(retained);stage=attempt/'stage';stage.mkdir(exist_ok=False)
    for n,b in sorted(outputs.items()):p=stage/relative(n);p.parent.mkdir(parents=True,exist_ok=True);h=p.open('xb');h.write(b);h.flush();os.fsync(h.fileno());h.close();p.chmod(0o444)
    require(inventory(stage/'original_archive')==set(original),'Exact original17 archive')
    for n,b in original.items():require(regular(stage/'original_archive'/n)==b,'Original archive changed')
    for n in IMMUTABLE:require(regular(stage/n)==original[n],'Immutable science/source/helper/result/ledger changed')
    members=[{'path':n,'bytes':len(regular(stage/n)),'sha256':sha(regular(stage/n))} for n in sorted(inventory(stage))];manifest={'schema':'pr48-strict-current-packet/v1','self_excluded':['MANIFEST.json'],'files_count':len(members),'files':members,'current_gate':GATE,'status':'unsolved','full_problem_solved':False,'novelty_claimed':False,'duplicate_shared_budget':True,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'full_permission_mode':'0444'}
    with (stage/'MANIFEST.json').open('xb') as h:h.write(encode(manifest));h.flush();os.fsync(h.fileno())
    (stage/'MANIFEST.json').chmod(0o444);require(inventory(stage)=={r['path'] for r in members}|{'MANIFEST.json'},'Self-only exact packet closure')
    for r in members:p=stage/r['path'];b=regular(p);require(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Staged body/full0444')
    require(stat.S_IMODE((stage/'MANIFEST.json').stat().st_mode)==0o444,'Manifest full0444');validate_dependencies();validate_native();require(regular(R/'unsolved_math_prioritization/QUEUE.md')==queue,'Queue preimage changed');require(not dest.exists() and not dest.is_symlink(),'Candidate appeared; keep actualstage');publish_absent(stage,dest)
    print(json.dumps({'status':'ACTUAL_CURRENT_FREEZE_WHOLE_REVIEW_PENDING','destination':str(dest),'manifest_sha256':sha(regular(dest/'MANIFEST.json')),'full_problem_solved':False,'duplicate_shared_original_attempts':'2/5','new_attempts':0,'audit_turns':0,'native_writes':0,'current_whole_verdict':None},indent=2))
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--execute',action='store_true')
    for n in ['root-scope-certificate','root-read-ledger','root-science-card','root-current-input-manifest','root-evidence-bindings']:parser.add_argument('--'+n+'-sha256',required=True)
    args=parser.parse_args();require(args.execute and all(hex64(v) for k,v in vars(args).items() if k.endswith('sha256')),'ROOT explicit execution and five SHA pins');require(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimized guards')
    script=Path(__file__).absolute();regular(script);A=script.parent.parent;R=A.parents[2];require(script.parent.name=='current_preparation_family' and A.name=='pr48_2961' and R==Path('/Users/alec/Documents/Math'),'Exact PR48 anchor')
    (A/'tmp').mkdir(exist_ok=True);require(not (A/'tmp').is_symlink(),'Regular tmp');attempt=A/'tmp'/('root_pr48_current_build_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'));attempt.mkdir(exist_ok=False);(attempt/'PRELAUNCH_BUILDER_SOURCE.py').write_bytes(regular(script));(attempt/'INVOCATION.json').write_bytes(encode({'argv':sys.argv,'cwd':str(Path.cwd()),'pid':os.getpid(),'parent_pid':os.getppid(),'utc':utc(),'source_sha256':sha(regular(script)),'administrative_only':True}))
    try:build(args,script,A,R,attempt)
    except BaseException:
        err=traceback.format_exc();(attempt/'BUILD_FAILURE.json').write_bytes(encode({'utc':utc(),'status':'FAILED_ACTUAL_BUILD_PRESERVED','traceback':err,'current_positive_verdict':False}));print(err,file=sys.stderr);raise
if __name__=='__main__':main()
