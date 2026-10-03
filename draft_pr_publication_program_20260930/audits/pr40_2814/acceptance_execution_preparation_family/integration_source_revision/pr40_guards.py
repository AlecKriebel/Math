"""Prepared source only. Root owns all actual execution and Git/remote writes."""
from __future__ import annotations
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
A = HERE.parents[1]
R = A.parents[2]
B = R / 'draft_pr_publication_program_20260930'
C = A / 'reviewed_candidate'
K = R / 'unsolved_math_prioritization/attempts/2814'
Q = R / 'unsolved_math_prioritization/QUEUE.md'
BASE = B / 'infrastructure/accepted_state_sync'
ID, CODE, PR = '2814', 'KP-3.16', 40
HEAD = '163e34d566d6cbaee3a2a8fdc6394fbb9e49a539'
ORIGINAL_BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
CURRENT_SHA = '8de92d903edaec7471f4ecc3df443b7e779732b0ee83cdec507c22025bfae25f'
DEPS_SHA = 'b2c6d31f3e7230e132761322bef9d3b99e1b0f53521fbefc5a281e6682199a37'
WHOLE_SHA = '90fbc21a211e29a3ba7a385c68479ff5effd864af6247f224d0b7843a447dabc'
SOURCE_SHA = '63363142a7a478b9e57692b0136a601934d1a9fb5b5aae63e6ffb8dd87add60c'
LEDGER_SHA = '3d74f9a6f0185e200349b2f303468d1c97fd7379dd470ea12dfca22585745a62'
SCIENCE_SHA = 'c232697fb80c20a88efe7db12390d9bda2d7f5c2fdc96e5cfad3a98a8cfdf16c'
MIRROR_SHA = 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
ADMIN = {'acceptance.json', 'status.json', 'attempt.json', 'current_readiness.json'}
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
NATIVE = {'draft_pr_publication_program_20260930/inventory.json'} | {'unsolved_math_prioritization/' + n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
FOREIGN_LOGS = {'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/commands.tsv', 'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/full_transcript.log'}
SCIENCE = {'full_problem_solved': False, 'partial_valid': True, 'novelty_claimed': False, 'source_hold': True, 'original_substantive_attempts': 0, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'verification_attempts_added': 0, 'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'paper_or_new_doi_or_tracker': False}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def equal(a, b):
    return type(a) is type(b) and (a.keys() == b.keys() and all(equal(a[k], b[k]) for k in a) if type(a) is dict else len(a) == len(b) and all(equal(x,y) for x,y in zip(a,b)) if type(a) is list else a == b)


def required(obj, values, context):
    require(type(obj) is dict, context + ': object required')
    for k,v in values.items():
        require(k in obj and equal(obj[k], v), context + ': missing/wrong type/value ' + k)


def parse(data):
    def pairs(items):
        obj = {}
        for k,v in items:
            require(k not in obj, 'Duplicate JSON key: ' + k)
            obj[k] = v
        return obj
    return json.loads(data, object_pairs_hook=pairs, parse_constant=lambda v: (_ for _ in ()).throw(ValueError('Nonfinite JSON: '+v)))


def load(p): return parse(Path(p).read_bytes())
def sha(data): return hashlib.sha256(data).hexdigest()
def stamp(): return dt.datetime.now(dt.timezone.utc).isoformat()
def encode(obj): return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode()
def digest(v):
    require(type(v) is str and re.fullmatch('[0-9a-f]{64}',v), 'Explicit SHA256 required')
    return v


def relative(n):
    require(type(n) is str and n and '\\' not in n and '\0' not in n, 'Invalid relative path')
    p = PurePosixPath(n)
    require(not p.is_absolute() and '..' not in p.parts and p.as_posix() == n, 'Noncanonical relative path')
    return p


def regular(base, n):
    relative(n)
    base, p = Path(base), Path(base)/n
    require(base.is_dir() and not base.is_symlink() and p.is_file() and not p.is_symlink(), 'Regular bound file required: '+str(p))
    require(p.resolve().is_relative_to(base.resolve()), 'Escaping member')
    for d in p.parents:
        if d == base: break
        require(not d.is_symlink(), 'Symlink ancestor')
    return p


def rows(value):
    if type(value) is dict: value = [{'path':k, **v} for k,v in value.items()]
    require(type(value) is list, 'Complete ordered rows required')
    out = []
    for z in value:
        require(type(z) is dict, 'Object row required')
        relative(z['path']); digest(z['sha256'])
        n = z['bytes'] if 'bytes' in z else z['size']
        require(type(n) is int and n >= 0 and ('size' not in z or 'bytes' not in z or equal(z['size'],z['bytes'])), 'Typed byte size required')
        out.append({**z, 'bytes':n})
    require(len({z['path'] for z in out}) == len(out), 'Duplicate member path')
    return out


def check(base, value):
    for z in rows(value):
        raw = regular(base,z['path']).read_bytes()
        require(len(raw) == z['bytes'] and sha(raw) == z['sha256'], 'Changed full bound member: '+z['path'])


def topology(base, exclusions=()):
    require(Path(base).is_dir() and not Path(base).is_symlink(), 'Unsafe closure root')
    files, dirs = set(),set()
    for p in Path(base).rglob('*'):
        n = p.relative_to(base).as_posix(); relative(n)
        if PurePosixPath(n).parts[0] in exclusions: continue
        require(not p.is_symlink() and (p.is_file() or p.is_dir()), 'Symlink/special closure member: '+n)
        (files if p.is_file() else dirs).add(n)
    return files,dirs


def exact(base,names,exclusions=()):
    names=set(names); f,d=topology(base,exclusions)
    expected={p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix()!='.'}
    require(f == names and d == expected, 'Exact recursive files/directories differ: '+str(base))


def manifest(base,name,pin=None,count=None):
    raw=regular(base,name).read_bytes()
    if pin is not None: require(sha(raw)==digest(pin),'Manifest SHA differs')
    obj=parse(raw); rr=rows(obj['files'])
    require(name not in {z['path'] for z in rr},'Only literal root manifest self excluded')
    if count is not None: require(len(rr)==count,'Manifest count differs')
    for k in ['files_count','member_count']:
        if k in obj: require(type(obj[k]) is int and obj[k]==len(rr),'Declared count/type differs')
    check(base,rr); exact(base,{z['path'] for z in rr}|{name})
    for z in rr:
        if z['path'].endswith('.json'): parse(regular(base,z['path']).read_bytes())
        if z['path'].endswith('.jsonl'):
            raw=regular(base,z['path']).read_bytes(); require(not raw or raw.endswith(b'\n'),'Incomplete JSONL')
            for line in raw.splitlines(): parse(line)
    return rr


def bound(pin):
    check(R,[pin]); p=regular(R,pin['path'])
    require(p.resolve().is_relative_to(A.resolve()),'Evidence outside exact PR40 audit')
    return p.read_bytes()


def pin(p):
    raw=Path(p).read_bytes(); return {'path':Path(p).relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)}


def binding(p): return {k:v for k,v in pin(p).items() if k!='bytes'}


def write(p,raw,exclusive=False):
    p=Path(p); require(p.parent.is_dir() and not p.is_symlink(),'Unsafe output')
    if exclusive: require(not p.exists(),'Existing output: inspect before retry')
    tmp=p.with_name(p.name+'.pr40-tmp')
    with tmp.open('xb') as s: s.write(raw); s.flush(); os.fsync(s.fileno())
    if exclusive:
        # Atomic absent-only publication of complete fsynced bytes. On failure
        # retain the completed temp and any intervening target for inspection.
        os.link(tmp,p,follow_symlinks=False)
        tmp.unlink()
    else:
        os.replace(tmp,p)
    fd=os.open(p.parent,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


def dump(p,v,exclusive=False): write(p,encode(v),exclusive)
def git_bytes(*a): return subprocess.check_output(['git',*a],cwd=R,timeout=30)
def git(*a): return git_bytes(*a).decode().strip()


def remote():
    o=parse(subprocess.check_output(['gh','pr','view',str(PR),'--repo','AlecKriebel/Math','--json','number,url,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,body'],cwd=R,timeout=30))
    required(o,{'number':40,'url':'https://github.com/AlecKriebel/Math/pull/40','headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual remote')
    return o


def source(base):
    for z in rows(load(A/'snapshot_manifest.json')['files']):
        require(regular(base,z['path']).read_bytes()==regular(C/'original_archive',z['path']).read_bytes(),'Original13 root/archive changed')
    require(sha(regular(base,'SOURCE_STATUS.md').read_bytes())==SCIENCE_SHA,'Original scientific source-status changed')
    require(sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Source record changed')
    ledger=regular(base,'turns.json').read_bytes(); require(sha(ledger)==LEDGER_SHA,'Exact zero attempt ledger changed')
    required(parse(ledger),{'id':2814,'count':0,'substantive_attempts':[]},'Original zero ledger')
    require(parse(regular(base,'prior_report.json').read_bytes()) is None,'Original absent prior must remain literal null')
    require(type(load(base/'duplicate_prior_report.json')) is dict and bool(load(base/'duplicate_prior_report.json')),'Complete imported duplicate prior required')


def utc_clock(value,context):
    require(type(value) is str and value and value==value.strip(),context+': ISO UTC clock required')
    try:
        clock=dt.datetime.fromisoformat(value[:-1]+'+00:00' if value.endswith('Z') else value)
    except (TypeError,ValueError):
        raise ValueError(context+': invalid ISO UTC clock')
    require(clock.tzinfo is not None and clock.utcoffset()==dt.timedelta(0),context+': timezone-aware UTC required')
    return clock


def revision_basis():
    revision=load(HERE/'REVISION_BINDINGS.json')
    required(revision,{'schema':'pr40-acceptance-source-revision-bindings/v1','original_preparation_manifest_sha256':'a7bbde5e024a6e432d7456586651208b3f365170cfc80112e0b98de1cae4c39b','closed_static_audit_manifest_sha256':'84b0e1c5364fac20617c1242e36c0d5b9130ea2784de81d3557ae8cbe94ab526','original_preparation_members':12,'closed_static_audit_members':22,'prepared_helpers_imported_or_executed':False,'actual_execution_pending':True},'Closed source revision inputs')
    check(R,revision['immutable_revision_inputs'])
    manifest(A/'acceptance_preparation_family','PREPARATION_MANIFEST.json',revision['original_preparation_manifest_sha256'],12)
    manifest(A/'acceptance_static_adversary_family','FIRST_PARTY_MANIFEST.json',revision['closed_static_audit_manifest_sha256'],22)


def basis():
    revision_basis()
    inputs=load(HERE/'INPUT_BINDINGS.json')
    for v in inputs['pins'].values(): bound(v)
    for c in inputs['closures']:
        base=R/c['root']
        if c['manifest'] is not None:
            obj=parse(bound(c['manifest'])); rr=rows(obj[c['member_field']])
            require(len(rr)==c['authored_count_excluding_self'],'Closed authored count changed')
            check(base,rr); exact(base,{z['path'] for z in rr}|{Path(c['manifest']['path']).name},c['excluded_root_directories'])
        else:
            check(base,c['files']); exact(base,{z['path'] for z in c['files']})
    original_foreign=load(A/'current_preparation_family/INPUT_PINS.json')['foreign_inventory']
    require(set(original_foreign)=={'primary_scope_family/foreign_cache','geodesic_geometry_family/primary'},'Only literal original foreign roots allowed')
    for n,v in original_foreign.items():
        check(A/n,v['members']); exact(A/n,{z['path'] for z in rows(v['members'])})
    # Entire foreign whole review root is separately exact; no general prefix exclusion.
    w=A/'whole_current_source_first_family'
    required(load(w/'FIRST_PARTY_MANIFEST.json'),{'foreign_excluded_prefixes':['ROOTforeign_primary/'],'no_other_exclusions':True,'disposition':'PASS_BOUNDED_PARTIAL_SOURCE_HOLD'},'Closed whole scope')
    foreign=rows(load(w/'FOREIGN_PRIMARY_INVENTORY.json')['exact_recursive_inventory'])
    require(len(foreign)==21 and all(PurePosixPath(z['path']).parts[0]=='ROOTforeign_primary' for z in foreign),'Exact21 qualified foreign rows required')
    check(w,foreign); exact(w,{z['path'] for z in rows(load(w/'FIRST_PARTY_MANIFEST.json')['files'])+foreign}|{'FIRST_PARTY_MANIFEST.json'})
    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,239)
    require(all((C/z['path']).stat().st_mode & 0o777 == 0o444 for z in frozen) and (C/'MANIFEST.json').stat().st_mode & 0o777 == 0o444,'Current files must remain read-only0444')
    dep=load(C/'CURRENT_PROOF_DEPENDENCIES.json'); required(dep,{'dependency_anchor_repository_relative':A.relative_to(R).as_posix()},'Dependency anchor')
    require(sha((C/'CURRENT_PROOF_DEPENDENCIES.json').read_bytes())==DEPS_SHA and len(rows(dep['files']))==216,'Entire216 dependency rows required'); check(A,dep['files'])
    source(C)
    for n in ADMIN:
        required(load(C/n),{'status':'UNSOLVED','full_problem_solved':False,'partial_valid':True,'novelty_claimed':False,'source_hold':True,'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_attempts_added':0,'verification_attempts_added':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'historical_verdict_transferred':False,'new_whole_current_gate':'PENDING'},'Unchanged dated pending administration')
    verdict=load(w/'ASSESSMENT.json')
    required(verdict,{'review_disposition':'PASS_BOUNDED_PARTIAL_SOURCE_HOLD','whole_current_review_completed':True,'problem_id':2814,'duplicate_target_id':20001896,'pr':40,'original_head':HEAD,'original_base':ORIGINAL_BASE,'genuine_actionable_mathematical_issues':[],'mandatory_frozen_SOURCE_STATUS_corrections':[],'full_problem_solved_by_project':False,'novelty_claimed':False,'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'source_first_reading_status':'QUALIFIED_BY_DISCLOSED_INITIAL_RAW_BACKGROUND_EXPOSURE','fully_unexposed_source_first_claimed':False,'full_recursive_standard_input_certification_claimed':False},'Complete whole assessment')
    root=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json')
    required(root,{'status':'PASS','independent_family_manifest_sha256':WHOLE_SHA,'authored_members':25,'separately_bound_foreign_members':21,'whole_independent_verdict':verdict},'Root actual whole reading')
    cap=load(A/'root_current_freeze_actual_capture/CAPTURE.json')
    required(cap,{'actual_execution':True,'completed':True,'pid':80794,'exit_code':0,'status':'PASS'},'Actual current freeze')
    check(A/'root_current_freeze_actual_capture',[cap['stdout'],cap['stderr']])
    return frozen,[inputs['pins'][n] for n in sorted(inputs['pins'])]


def plan_scope(o,prep):
    required(o,{'schema':'pr40-root-reviewed-final-plan/v1','plan_status':'ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION','pr':40,'problem_id':2814,'original_head':HEAD,'original_base':ORIGINAL_BASE,'reviewed_candidate_manifest_sha256':CURRENT_SHA,'current_proof_dependencies_sha256':DEPS_SHA,'whole_manifest_sha256':WHOLE_SHA,'preparation_manifest_sha256':prep,'root_full_current_read_completed':True,'root_full_whole_read_completed':True,'independent_whole_current_pass':True,'mandatory_corrections':[],'science_reexecution_of_current':False,'historical_PASS_transferred':False,**SCIENCE},'Root final scope')
    _,refs=basis(); require(equal(o['immutable_evidence_references'],refs),'All complete immutable references required')
    require(equal(o['scientific_scope'],load(HERE/'SCIENTIFIC_SCOPE.json')),'Full scientific qualifications differ')
    draft=load(HERE/'DRAFT_FINAL_PLAN.json'); draft.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',preparation_manifest_sha256=prep,root_full_current_read_completed=True,root_full_whole_read_completed=True,independent_whole_current_pass=True)
    require(equal(o,draft),'Only explicit root review flags/status and preparation hash may differ from the complete draft')
    return refs


def args(parser):
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--preparation-manifest-sha256',required=True)
    for n in ['final-plan','final-receipt','final-manifest','reconciliation-capture','previous-mirror','fresh-preimage']:
        parser.add_argument('--'+n,required=True); parser.add_argument('--'+n+'-sha256',required=True)


def explicit(a,n):
    p=regular(R,getattr(a,n)); require(p.resolve().is_relative_to(A.resolve()) or n=='previous_mirror','Actual gate outside selected audit')
    require(sha(p.read_bytes())==digest(getattr(a,n+'_sha256')),'Explicit actual gate changed: '+n)
    return p


def gates(a):
    require(a.execute,'Root explicit --execute required'); require(git('branch','--show-current')=='main','Stay on main')
    manifest(HERE,'PREPARATION_MANIFEST.json',a.preparation_manifest_sha256)
    ps={n:explicit(a,n) for n in ['final_plan','final_receipt','final_manifest','reconciliation_capture','previous_mirror','fresh_preimage']}
    scope=load(ps['final_plan']); refs=plan_scope(scope,a.preparation_manifest_sha256)
    receipt=load(ps['final_receipt'])
    required(receipt,{'schema':'pr40-actual-final-reconciliation/v1','status':'PASS','actual_root_reconciliation':True,'pr':40,'problem_id':2814,'preparation_manifest_sha256':a.preparation_manifest_sha256,'entire_scope':scope,'bindings_before':refs,'bindings_after':refs,'root_reviewed_plan':pin(ps['final_plan']),'reconciliation_source':pin(HERE/'seal_final_evidence.py')},'Actual final reconciliation')
    require(ps['final_manifest'].parent==ps['final_receipt'].parent and ps['final_manifest'].name=='FINAL_MANIFEST.json','Literal final closure required')
    fm=manifest(ps['final_manifest'].parent,'FINAL_MANIFEST.json',a.final_manifest_sha256,2)
    require({z['path'] for z in fm}=={'ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json'} and ps['final_receipt'].name=='ROOT_FINAL_RECONCILIATION.json','Exact final output names required')
    require(equal(load(ps['final_manifest'].parent/'ROOT_REVIEWED_SCOPE.json'),scope),'Final complete scope copy differs')
    cap=load(ps['reconciliation_capture']); required(cap,{'actual_execution':True,'completed':True,'exit_code':0,'status':'PASS','source_sha256':sha((HERE/'seal_final_evidence.py').read_bytes()),'cwd':str(A)},'Genuine actual final capture')
    require(type(cap['pid']) is int and cap['pid']>0 and type(cap['argv']) is list and str(HERE/'seal_final_evidence.py') in cap['argv'],'Actual PID/argv required')
    started=utc_clock(cap['started_utc'],'Actual capture start')
    finished=utc_clock(cap['finished_utc'],'Actual capture finish')
    require(started<=finished,'Actual capture clocks reversed')
    require(started<=utc_clock(receipt['utc'],'Actual final reconciliation clock')<=finished,'Reconciliation clock outside genuine capture interval')
    for flag,v in [('--plan',a.final_plan),('--plan-sha256',a.final_plan_sha256),('--preparation-manifest-sha256',a.preparation_manifest_sha256),('--output',ps['final_manifest'].parent.relative_to(A).as_posix())]:
        require(cap['argv'].count(flag)==1 and cap['argv'][cap['argv'].index(flag)+1]==v,'Actual final argv pin differs')
    require(cap['argv'].count('--execute')==1,'Actual execution flag required')
    cb=ps['reconciliation_capture'].parent
    require(ps['reconciliation_capture'].name=='CAPTURE.json' and cb.parent==A,'Literal CAPTURE.json in a new adjacent root capture required')
    streams=rows([cap['stdout'],cap['stderr']])
    stream_names={z['path'] for z in streams}
    require(len(stream_names)==2 and all(len(relative(n).parts)==1 and n not in {'CAPTURE.json','prelaunch_source.py'} for n in stream_names),'Two distinct declared root stream basenames disjoint from capture/source required')
    require(len({'CAPTURE.json','prelaunch_source.py'}|stream_names)==4,'Exactly four distinct capture members required')
    check(cb,streams); require(sha(regular(cb,'prelaunch_source.py').read_bytes())==cap['source_sha256'],'Actual prelaunch source changed')
    required(parse(regular(cb,cap['stdout']['path']).read_bytes()),{'status':'PASS','final_receipt_sha256':a.final_receipt_sha256,'final_manifest_sha256':a.final_manifest_sha256},'Entire actual child stdout')
    exact(cb,{'CAPTURE.json','prelaunch_source.py'}|stream_names)
    require(not ps['fresh_preimage'].resolve().is_relative_to(C.resolve()) and not ps['fresh_preimage'].resolve().is_relative_to(HERE.resolve()),'Fresh root preimage must be adjacent new evidence')
    require(ps['previous_mirror']==B/'audits/pr39_9500008/state_mirror_bindings.json','Actual completed PR39 proposal required')
    previous=load(ps['previous_mirror']); require(len(previous['entries'])==29 and 39 in previous['required_completed_prs'] and 40 not in previous['required_completed_prs'],'Require completed PR39 prior scope')
    fresh=load(ps['fresh_preimage']); required(fresh,{'approved_by_root':True},'Fresh actual native preimage')
    created=utc_clock(fresh['created_utc'],'Actual root fresh preimage creation')
    require(created<=dt.datetime.now(dt.timezone.utc),'Fresh root preimage creation clock is in the future')
    require(type(fresh['reason_date_utc']) is str and fresh['reason_date_utc']==created.date().isoformat(),'Root rebase reason date must match the actual UTC creation date')
    require(type(fresh['reason']) is str and fresh['reason']==fresh['reason'].strip() and len(fresh['reason'])>=40 and len(fresh['reason'].split())>=6,'Substantive root-reviewed rebase reason required; a token such as yes is insufficient')
    require(type(fresh['current_head']) is str and re.fullmatch('[0-9a-f]{40}',fresh['current_head']),'Explicit fresh main HEAD required, independently of archived replay HEAD')
    rr=rows(fresh['files']); require({z['path'] for z in rr}==NATIVE and len(rr)==13,'Exact13 fresh full native/inventory pins required')
    snap=load(A/'snapshot_manifest.json'); required(snap,{'head':HEAD,'base':ORIGINAL_BASE},'Original13/14 snapshot'); require(len(snap['files'])==13 and len(snap['changed_paths'])==14,'Original13/14 counts')
    raw=git_bytes('diff',ORIGINAL_BASE,HEAD); require(len(raw)==snap['diff_bytes'] and sha(raw)==snap['diff_sha256'] and raw==(A/'pr_input/diff.patch').read_bytes(),'Entire original Git diff changed')
    require(git_bytes('diff','--name-only',ORIGINAL_BASE,HEAD).decode().splitlines()==snap['changed_paths'],'Original changed paths differ')
    for z in rows(snap['files']):
        path='unsolved_math_prioritization/attempts/'+ID+'/'+z['path']
        require(git_bytes('show',HEAD+':'+path)==(C/'original_archive'/z['path']).read_bytes(),'Original Git/archive mismatch')
        require(git_bytes('ls-tree','-z',HEAD,'--',path).decode().rstrip('\0')==z['mode']+' blob '+z['git_blob']+'\t'+path,'Exact original Git mode/blob mismatch')
    for rev in [ORIGINAL_BASE,HEAD]:
        state=parse(git_bytes('show',rev+':unsolved_math_prioritization/state.json')); require(ID not in state and '20001896' not in state,'No original primary/duplicate native state allowed')
        hp='unsolved_math_prioritization/history.jsonl'
        hb=git_bytes('show',rev+':'+hp) if git_bytes('ls-tree','-z',rev,'--',hp) else b''
        require(not hb or hb.endswith(b'\n'),'Historical history incomplete')
        require(not any(str(e.get('id',e.get('problem_id',''))) in {ID,'20001896'} for e in map(parse,hb.splitlines())),'No invented original selected history allowed')
    frozen,_=basis()
    return frozen,{n:getattr(a,n) for n in ['preparation_manifest_sha256','final_plan','final_plan_sha256','final_receipt','final_receipt_sha256','final_manifest','final_manifest_sha256','reconciliation_capture','reconciliation_capture_sha256','previous_mirror','previous_mirror_sha256','fresh_preimage','fresh_preimage_sha256']}


def selected(data):
    lines=data.decode().splitlines(keepends=True); heads=[s for s in lines if s.startswith('| Rank | ID / code |')]
    require(len(heads)==1 and [s.strip() for s in heads[0].split('|')[1:-1]]==HEADER,'Exact12 named columns required')
    rr=[s for s in lines if len(s.split('|'))==14 and s.split('|')[2].strip()==ID+' / '+CODE]
    require(len(rr)==1,'Unique exact primary queue row required'); return rr[0]


def accepted_invariants(o,pins,pre):
    required(o,{'schema':'pr40-accepted-bounded-source-hold/v1','pr':40,'id':2814,'problem_id':2814,'problem_number':CODE,'queue_status':'unsolved','outcome':'unsolved_accepted_partial_merged','original_head':HEAD,'original_base':ORIGINAL_BASE,'merge_parents':[pre['main_before'],HEAD],'remote_state':'MERGED','remote_isDraft':False,'canonical_scientific_artifact_sha256':SCIENCE_SHA,'source_record_sha256':SOURCE_SHA,'original_ledger_sha256':LEDGER_SHA,'substantive_attempts_used':0,'substantive_attempt_limit':5,'duplicate_native_acceptance_added':False,'native_historical_events_inferred':False,'historical_metadata_archival_only':True,'workflow_completion_estimate_percent':100,'full_resolution_completion_estimate_percent':0,'scientific_scope':load(HERE/'SCIENTIFIC_SCOPE.json'),**SCIENCE,**pins},'Strict final acceptance')
    for k in ['merge_commit','merge_tree']: require(type(o[k]) is str and re.fullmatch('[0-9a-f]{40}',o[k]),'Actual merge object required')
    require(type(o['merged_at']) is str and o['merged_at'],'Actual merge date required')
    source(K)
    for n in ADMIN-{'acceptance.json'}:
        required(load(K/n),{**SCIENCE,**pins,'id':2814,'status':'unsolved_accepted_partial_merged','merge_commit':o['merge_commit'],'merge_tree':o['merge_tree'],'merged_at':o['merged_at'],'new_whole_current_gate':'PASS_BOUNDED_PARTIAL_SOURCE_HOLD','historical_verdict_transferred':False},'Current final administrative scope '+n)


def canonical_names(frozen,accepted=False):
    return {z['path'] for z in frozen}|{'reviewed_pending_administration/'+n for n in ADMIN}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md'}|({'ACCEPTANCE.md','MANIFEST.json'} if accepted else set())


def canonical(frozen,accepted=False):
    exact(K,canonical_names(frozen,accepted))
    for z in frozen:
        p=K/('reviewed_pending_administration/'+z['path'] if z['path'] in ADMIN else z['path'])
        require(p.read_bytes()==(C/z['path']).read_bytes(),'Frozen science/archival administration changed')
    require((K/'reviewed_pending_administration/MANIFEST.json').read_bytes()==(C/'MANIFEST.json').read_bytes(),'Old frozen manifest changed'); source(K)


def foreign_capture():
    require(not git('diff','--cached','--name-only'),'Preflight index must be clean')
    dirty=set(git_bytes('diff','--name-only','-z').decode().split('\0'))-{''}; require(dirty<=FOREIGN_LOGS,'Only exact two tracked foreign logs may be dirty')
    out=[]
    for n in sorted(FOREIGN_LOGS):
        e=git_bytes('ls-tree','-z','HEAD','--',n).decode().rstrip('\0'); fields,literal=e.split('\t'); mode,kind,blob=fields.split(); require(literal==n and kind=='blob' and mode in {'100644','100755'},'Exact regular tracked foreign log required')
        raw=regular(R,n).read_bytes(); out.append({'path':n,'bytes':len(raw),'sha256':sha(raw),'head_sha256':sha(git_bytes('show','HEAD:'+n)),'head_entry':e,'index_entry':mode+' '+blob+' 0\t'+n})
    foreign_check({'foreign_logs':out}); return out


def foreign_check(pre):
    rr=pre['foreign_logs']; require(len(rr)==2 and {z['path'] for z in rr}==FOREIGN_LOGS,'No broad tracked exception')
    check(R,rr)
    for z in rr:
        n=z['path']; require(git_bytes('ls-tree','-z','HEAD','--',n).decode().rstrip('\0')==z['head_entry'] and git_bytes('ls-files','--stage','-z','--',n).decode().rstrip('\0')==z['index_entry'] and sha(git_bytes('show','HEAD:'+n))==z['head_sha256'] and sha(git_bytes('show',':'+n))==z['head_sha256'],'Foreign exact HEAD/index bytes/mode/blob changed')


def fresh_check(pre,allowed=()):
    f=load(R/pre['fresh_preimage']); check(R,[z for z in rows(f['files']) if z['path'] not in allowed]); foreign_check(pre)


def tree(merge,pre,overlay,queue):
    require(git('show','-s','--format=%P',merge).split()==[pre['main_before'],HEAD],'Exact original-head no-ff parents required'); git_bytes('merge-base','--is-ancestor',merge,'HEAD')
    prefix='unsolved_math_prioritization/attempts/'+ID+'/'
    rr=rows(overlay['canonical_overlay_files']); entries=git_bytes('ls-tree','-r','-z',merge,'--',prefix).decode().split('\0'); names=set()
    for e in filter(None,entries):
        fields,n=e.split('\t'); mode,kind,blob=fields.split(); require(mode=='100644' and kind=='blob','Nonexecutable regular complete canonical Git tree required'); names.add(n)
    require(names=={prefix+z['path'] for z in rr},'Whole canonical Git tree closure differs')
    for z in rr:
        raw=git_bytes('show',merge+':'+prefix+z['path']); require(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Real tree canonical bytes differ')
    require(git_bytes('show',merge+':unsolved_math_prioritization/QUEUE.md')==queue,'Real whole queue differs')
    for z in rows(load(R/pre['fresh_preimage'])['files']):
        if z['path']=='unsolved_math_prioritization/QUEUE.md': continue
        require(sha(git_bytes('show',merge+':'+z['path']))==z['sha256'],'Real merge changed native/inventory path')
    changed=set(git_bytes('diff-tree','-r','--no-commit-id','--name-only','-z',pre['main_before'],merge).decode().split('\0'))-{''}
    require(changed<={prefix+z['path'] for z in rr}|{'unsolved_math_prioritization/QUEUE.md'},'Unrelated real merge paths')
    foreign_check(pre)
    for z in pre['foreign_logs']: require(git_bytes('ls-tree','-z',merge,'--',z['path']).decode().rstrip('\0')==z['head_entry'],'Real merge included foreign log')
    return git('show','-s','--format=%T',merge)


def mirror_module(proposal):
    p=BASE/'revision2/accepted_state_sync_v2.py'; require(sha(p.read_bytes())==MIRROR_SHA,'Reviewed native mirror source changed')
    spec=importlib.util.spec_from_file_location('pr40_bound_native_mirror',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    # Each previously accepted complete ledger and typed budget is exact-bound by the genuine prior proposal.
    budgets=[]
    for e in proposal['entries']:
        b=e['budget']; require(type(b['used']) is int and type(b['limit']) is int and 0<=b['used']<=b['limit'],'Typed preserved prior budget')
        raw=regular(R,b['ledger']['path']).read_bytes(); require(sha(raw)==b['ledger']['sha256'],'Full original prior ledger changed'); budgets.append((b['kind'],b['used'],b['limit'],raw))
    def ledger(raw,kind,used,limit):
        m.require(type(used) is int and type(limit) is int and any(kind==k and used==u and limit==l and raw==d for k,u,l,d in budgets),'Exact complete accepted ledger/budget required; no inference')
    m.ledger_budget=ledger
    return m
