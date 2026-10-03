"""Prepared source only. Root owns all actual execution and Git/remote writes."""
from __future__ import annotations
import copy
import datetime as dt
import hashlib
import importlib.util
import json
import math
import os
import re
import stat
import subprocess
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
A = HERE.parent
R = A.parents[2]
B = R / 'draft_pr_publication_program_20260930'
C = A / 'reviewed_candidate'
K = R / 'unsolved_math_prioritization/attempts/9700035'
Q = R / 'unsolved_math_prioritization/QUEUE.md'
BASE = B / 'infrastructure/accepted_state_sync'
ID, CODE, PR = '9700035', 'AMR-096-0035', 41
HEAD = '292b95ca601f166e6d246e609cf7ed5ca5653e25'
ORIGINAL_BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
CURRENT_SHA = '3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa'
DEPS_SHA = 'ade2f6fe9890f1038810158a284f4a8924e34d6d2f95b3a07654d78fa6501ff6'
SOURCE_SHA = 'd86ee1dc749ef5b9a0446109fb6f0278246cf3584f36aa70205b5bc6c683782f'
LEDGER_SHA = 'bd0a82165c3ac81f7a7d35ace164f20ecb87e6b73a9155815e4eecac655a2549'
SCIENCE_SHA = '464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c'
MIRROR_SHA = 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
ADMIN = {'status.json', 'attempt.json', 'readiness.json', 'review/verdict.json'}
IMMUTABLE = {'PROOF.md','verify.py','verification.json','source_record.json','prior_report.json','source_provenance.json','turns.json','review/independent_checks.py','review/independent_results.json','review/review_summary.json'}
WHOLE_VERDICT = 'PASS_QUALIFIED_UNSOLVED_PARTIAL_NEW_WHOLE_CURRENT'
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
NATIVE = {'draft_pr_publication_program_20260930/inventory.json'} | {'unsolved_math_prioritization/' + n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
IGNORED_CACHE3 = {'unsolved_math_prioritization/cache/problems.json', 'unsolved_math_prioritization/cache/research_results.json', 'unsolved_math_prioritization/cache/catalog.sqlite'}
FOREIGN_LOGS = {'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/commands.tsv', 'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/full_transcript.log'}
SCIENCE = {'full_problem_solved': False, 'partial_valid': True, 'novelty_claimed': False, 'original_substantive_attempts': 2, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'verification_attempts_added': 0, 'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'paper_or_new_doi_or_tracker': False}


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
    def floating(v):
        n=float(v); require(math.isfinite(n),'Nonfinite decoded JSON number'); return n
    return json.loads(data, object_pairs_hook=pairs, parse_float=floating, parse_constant=lambda v: (_ for _ in ()).throw(ValueError('Nonfinite JSON: '+v)))


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
    require(not p.is_absolute() and not {'.','..','.git','__pycache__'}.intersection(p.parts) and p.as_posix() == n, 'Noncanonical relative path')
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


def frozen_files(base,values,self_name=None):
    names={z['path'] for z in rows(values)}
    if self_name is not None:names.add(relative(self_name).as_posix())
    for n in names:
        require(stat.S_IMODE(regular(base,n).stat().st_mode)==0o444,'Literal frozen0444 including special permission bits required: '+n)


def manifest(base,name,pin=None,count=None,frozen=False):
    raw=regular(base,name).read_bytes()
    if pin is not None: require(sha(raw)==digest(pin),'Manifest SHA differs')
    obj=parse(raw); rr=rows(obj['files'])
    declarations=[obj[k] for k in ['excluded','self_excluded'] if k in obj]
    require(declarations and all(equal(value,[name]) for value in declarations),'Only declared literal root manifest self may be excluded')
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
    if frozen:frozen_files(base,rr,name)
    return rr


def bound(pin):
    check(R,[pin]); p=regular(R,pin['path'])
    require(p.resolve().is_relative_to(A.resolve()),'Evidence outside exact PR41 audit')
    return p.read_bytes()


def pin(p):
    raw=Path(p).read_bytes(); return {'path':Path(p).relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)}


def binding(p): return {k:v for k,v in pin(p).items() if k!='bytes'}


def write(p,raw,exclusive=False):
    p=Path(p); require(p.parent.is_dir() and not p.is_symlink() and all(not d.is_symlink() for d in p.parents),'Unsafe output or symlink ancestor')
    if exclusive: require(not p.exists(),'Existing output: inspect before retry')
    tmp=p.with_name(p.name+'.pr41-tmp')
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
    required(o,{'number':41,'url':'https://github.com/AlecKriebel/Math/pull/41','headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual remote')
    return o


def original_native(base):
    snapshot=load(A/'snapshot_manifest.json')
    require(len(snapshot['files'])==16,'Complete original16 required')
    exact(base,{z['path'] for z in rows(snapshot['files'])})
    for z in rows(snapshot['files']):
        raw=regular(base,z['path']).read_bytes()
        require(raw==regular(A/'source_snapshot',z['path']).read_bytes() and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Original16 bytes differ')


def source(base):
    original_native(base/'original_archive')
    for n in IMMUTABLE:
        require(regular(base,n).read_bytes()==regular(A/'source_snapshot',n).read_bytes(),'Immutable current math/code/full saved object/source/prior/ledger changed')
    require(sha(regular(base,'PROOF.md').read_bytes())==SCIENCE_SHA and sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Scientific/source anchors changed')
    raw=regular(base,'turns.json').read_bytes();require(sha(raw)==LEDGER_SHA,'Exact original two-turn list changed')
    turns=parse(raw);require(type(turns) is list and len(turns)==2 and all(type(z) is dict and type(z['turn']) is int for z in turns) and [z['turn'] for z in turns]==[1,2],'Typed complete original2/5 ledger required')
    prior=parse(regular(base,'prior_report.json').read_bytes());require(type(prior) is dict and bool(prior),'Original prior is PRESENT; null/empty fallback prohibited')
    require(sha(regular(base,'SOURCE_PROOF_QUALIFICATIONS.md').read_bytes())=='69196e84de0d627b31b6f2a20a3745ba33048969cb93efba92a886bfedf8bc7e','Exact operative imported proof qualifications required')


def utc_clock(value,context):
    require(type(value) is str and value and value==value.strip(),context+': ISO UTC clock required')
    try:
        clock=dt.datetime.fromisoformat(value[:-1]+'+00:00' if value.endswith('Z') else value)
    except (TypeError,ValueError):
        raise ValueError(context+': invalid ISO UTC clock')
    require(clock.tzinfo is not None and clock.utcoffset()==dt.timedelta(0),context+': timezone-aware UTC required')
    return clock


def exact_reference(obj):
    require(type(obj) is dict and set(obj)=={'path','bytes','sha256'},'Exact literal path/bytes/SHA reference row required; extensions prohibited')
    rows([obj])
    return obj


def root_binding_input(name,pin_value):
    p=regular(R,name)
    require(p.resolve().is_relative_to(A.resolve()) and not p.resolve().is_relative_to(C.resolve()) and not p.resolve().is_relative_to(HERE.resolve()),'Genuine external ROOT bindings outside closed packets required')
    require(sha(p.read_bytes())==digest(pin_value),'Actual ROOT immutable-bindings SHA differs')
    o=parse(p.read_bytes())
    exact_reference(o['whole_manifest']);exact_reference(o['root_whole_inspection'])
    expected=load(HERE/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
    expected.update(status='ROOT_APPROVED_CLOSED_WHOLE_EVIDENCE',created_utc=o['created_utc'],root_full_current_read_completed=True,root_full_whole_read_completed=True,independent_whole_current_pass=True,whole_manifest=o['whole_manifest'],root_whole_inspection=o['root_whole_inspection'])
    require(equal(o,expected),'Complete typed external ROOT bindings schema/value equality required')
    required(o,{'schema':'pr41-root-approved-immutable-acceptance-bindings/v1','status':'ROOT_APPROVED_CLOSED_WHOLE_EVIDENCE','root_full_current_read_completed':True,'root_full_whole_read_completed':True,'independent_whole_current_pass':True,'mandatory_corrections':[],'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0},'Explicit ROOT whole reading, not a draft')
    require(utc_clock(o['created_utc'],'ROOT binding creation')<=dt.datetime.now(dt.timezone.utc),'ROOT binding may not be future dated')
    require(type(o['whole_manifest']) is dict and type(o['root_whole_inspection']) is dict,'Actual explicit whole/root references required')
    return o,p


def basis(root_bindings,root_bindings_sha256):
    reviewed,rp=root_binding_input(root_bindings,root_bindings_sha256)
    inputs=load(HERE/'INPUT_BINDINGS.json');require(inputs['source_only'] is True,'Prepared input contract is source-only')
    refs=[]
    for n in sorted(inputs['pins']):
        v=inputs['pins'][n];bound(v);refs.append(v)
    for c in inputs['closures']:
        root=A/c['directory'];raw=regular(root,c['manifest_name']).read_bytes()
        require(sha(raw)==c['manifest_sha256'],'Closed included manifest changed')
        check(root,c['members']+c['foreign_members'])
        exact(root,{z['path'] for z in rows(c['members']+c['foreign_members'])}|{c['manifest_name']})
        if c.get('requires_all_members_0444') is True:frozen_files(root,c['members']+c['foreign_members'],c['manifest_name'])
    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,547,frozen=True)
    deps=load(C/'CURRENT_PROOF_DEPENDENCIES.json')
    required(deps,{'dependency_anchor_repository_relative':A.relative_to(R).as_posix()},'Exact portable dependency anchor')
    require(sha((C/'CURRENT_PROOF_DEPENDENCIES.json').read_bytes())==DEPS_SHA and len(rows(deps['files']))==469,'Complete469 dependency rows required');check(A,deps['files'])
    source(C)
    for n in ADMIN:
        required(load(C/n),{'id':ID,'problem_number':CODE,'status':'unsolved_scoped_conditional_partial_pending_NEW_whole_gate','full_problem_solved':False,'novelty_claimed':False,'current_gate':'pending_NEW_whole_current_packet_source_first_adversary','current_verdict':None,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'original_substantive_attempts':2,'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,'historical_verdict_transferred':False,'canonical_historical_events_inferred':False},'Dated pending administration retained')
    w=A/'whole_current_source_first_family';wm=reviewed['whole_manifest'];require(wm['path']==(w/'FIRST_PARTY_MANIFEST.json').relative_to(R).as_posix(),'Literal whole-family manifest anchor required')
    required(wm,{k:inputs['whole_observed_only'][k] for k in ['path','bytes','sha256']},'Exact observed actual whole closure required')
    require(equal(reviewed['root_whole_inspection'],inputs['root_whole_observed']),'Exact actually completed ROOT whole review required')
    raw=bound(wm);whole=parse(raw)
    required(whole,{'status':'CLOSED_NEW_WHOLE_CURRENT_SOURCE_FIRST_REVIEW','excluded':['FIRST_PARTY_MANIFEST.json'],'files_count':143,'foreign_count':17,'reviewed_current_manifest_sha256':CURRENT_SHA,'all_members_0444':True},'Closed whole authored/foreign classification')
    authored,foreign=rows(whole['files']),rows(whole['foreign_files'])
    require(len(authored)==143 and len(foreign)==17 and not {z['path'] for z in authored}.intersection(z['path'] for z in foreign),'Exact143/17 distinct whole members')
    check(w,authored+foreign);exact(w,{z['path'] for z in authored+foreign}|{'FIRST_PARTY_MANIFEST.json'})
    frozen_files(w,authored+foreign,'FIRST_PARTY_MANIFEST.json')
    for z in authored+foreign:
        if z['path'].endswith('.json'):parse((w/z['path']).read_bytes())
    verdict=load(w/'RESULT.json')
    required(verdict,{'verdict':WHOLE_VERDICT,'review_completed':True,'partial_valid':True,'full_problem_solved':False,'novelty_claimed':False,'mandatory_repairs':[],'original_substantive_attempts':2,'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,'paper_DOI_tracker_promotion':False,'candidate_helpers_imported_or_executed':False},'Complete new whole scientific disposition')
    required(verdict['reviewed_current'],{'manifest_sha256':CURRENT_SHA,'members':547,'all_modes':'0444'},'Whole exact current')
    require(whole['result_sha256']==sha((w/'RESULT.json').read_bytes()) and whole['report_sha256']==sha((w/'WHOLE_CURRENT_ADVERSARIAL_REVIEW.md').read_bytes()),'Complete whole verdict/report binding differs')
    root= parse(bound(reviewed['root_whole_inspection']))
    required(root,{'status':'PASS','independent_family_manifest_sha256':wm['sha256'],'authored_members':143,'separately_bound_foreign_members':17,'whole_independent_verdict':verdict},'ROOT actual complete whole reading')
    for key in ['root_full_current_read_completed','root_full_whole_read_completed']:
        if key in root:require(root[key] is True,'Typed ROOT read flag required')
    cap=load(A/'root_current_freeze_actual_capture/CAPTURE.json')
    required(cap,{'actual_execution':True,'completed':True,'pid':36236,'exit_code':0,'status':'PASS','stdin_supplied':False,'native13_and_HEAD_unchanged':True},'Actual current freeze')
    require(utc_clock(cap['started_utc'],'Freeze start')<=utc_clock(cap['finished_utc'],'Freeze finish'),'Freeze clock order')
    check(A/'root_current_freeze_actual_capture',[cap['stdout'],cap['stderr']])
    require(equal(cap['fresh_native13_before'],cap['fresh_native13_after']) and cap['head_before']==cap['head_after'],'Dated freeze actual pre/post equality required')
    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json')
    require(ledger['reading_completed'] is True and type(ledger['root_flags']) is dict and len(ledger['root_flags'])==8 and equal(ledger['root_flags'],card['root_flags']) and all(v is True for v in ledger['root_flags'].values()),'Exact eight genuine read-ledger/card flags required')
    refs += [wm,reviewed['root_whole_inspection'],pin(rp),pin(w/'RESULT.json'),pin(w/'WHOLE_CURRENT_ADVERSARIAL_REVIEW.md')]
    require(len({z['path'] for z in refs})==len(refs),'Duplicate immutable evidence reference')
    return frozen,sorted(refs,key=lambda z:z['path'])


def plan_scope(o,prep,root_bindings,root_bindings_sha256):
    _,refs=basis(root_bindings,root_bindings_sha256)
    bindings,_=root_binding_input(root_bindings,root_bindings_sha256)
    draft=load(HERE/'DRAFT_FINAL_PLAN.json')
    draft.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=prep,root_bindings=root_bindings,root_bindings_sha256=root_bindings_sha256,whole_manifest_sha256=bindings['whole_manifest']['sha256'],root_full_current_read_completed=True,root_full_whole_read_completed=True,independent_whole_current_pass=True,immutable_evidence_references=refs)
    require(equal(o,draft),'Only explicit completed ROOT fields and complete actual immutable refs may replace draft placeholders')
    require(equal(o['scientific_scope'],load(HERE/'SCIENTIFIC_SCOPE.json')),'Full scientific qualification differs')
    return refs


def args(parser):
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--preparation-manifest-sha256',required=True)
    for n in ['final-plan','final-receipt','final-manifest','reconciliation-capture','previous-mirror','previous-post','fresh-preimage','root-bindings']:
        parser.add_argument('--'+n,required=True); parser.add_argument('--'+n+'-sha256',required=True)


def explicit(a,n):
    p=regular(R,getattr(a,n)); require(p.resolve().is_relative_to(A.resolve()) or n in {'previous_mirror','previous_post'},'Actual gate outside selected audit')
    require(sha(p.read_bytes())==digest(getattr(a,n+'_sha256')),'Explicit actual gate changed: '+n)
    return p


def gates(a):
    require(a.execute,'Root explicit --execute required'); require(git('branch','--show-current')=='main','Stay on main')
    manifest(HERE,'PREPARATION_MANIFEST.json',a.preparation_manifest_sha256,frozen=True)
    ps={n:explicit(a,n) for n in ['final_plan','final_receipt','final_manifest','reconciliation_capture','previous_mirror','previous_post','fresh_preimage','root_bindings']}
    scope=load(ps['final_plan']); refs=plan_scope(scope,a.preparation_manifest_sha256,a.root_bindings,a.root_bindings_sha256)
    receipt=load(ps['final_receipt'])
    require(type(receipt) is dict and set(receipt)=={'schema','utc','status','actual_root_reconciliation','pr','problem_id','preparation_manifest_sha256','entire_scope','bindings_before','bindings_after','root_reviewed_plan','reconciliation_source','science_helpers_executed','new_substantive_attempts','audit_turns','shared_mutations'},'Complete actual final receipt keyset required')
    required(receipt,{'schema':'pr41-actual-final-reconciliation/v1','status':'PASS','actual_root_reconciliation':True,'pr':41,'problem_id':9700035,'preparation_manifest_sha256':a.preparation_manifest_sha256,'entire_scope':scope,'bindings_before':refs,'bindings_after':refs,'root_reviewed_plan':pin(ps['final_plan']),'reconciliation_source':pin(HERE/'seal_final_evidence.py'),'science_helpers_executed':False,'new_substantive_attempts':0,'audit_turns':0,'shared_mutations':False},'Actual final reconciliation')
    require(ps['final_manifest'].parent==ps['final_receipt'].parent and ps['final_manifest'].name=='FINAL_MANIFEST.json','Literal final closure required')
    fm=manifest(ps['final_manifest'].parent,'FINAL_MANIFEST.json',a.final_manifest_sha256,2,frozen=True)
    require({z['path'] for z in fm}=={'ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json'} and ps['final_receipt'].name=='ROOT_FINAL_RECONCILIATION.json','Exact final output names required')
    require(equal(load(ps['final_manifest'].parent/'ROOT_REVIEWED_SCOPE.json'),scope),'Final complete scope copy differs')
    cap=load(ps['reconciliation_capture']); required(cap,{'actual_execution':True,'completed':True,'exit_code':0,'status':'PASS','stdin_supplied':False,'source_sha256':sha((HERE/'seal_final_evidence.py').read_bytes()),'cwd':str(A)},'Genuine actual final capture')
    require(type(cap['pid']) is int and cap['pid']>0 and type(cap['argv']) is list and str(HERE/'seal_final_evidence.py') in cap['argv'],'Actual PID/argv required')
    started=utc_clock(cap['started_utc'],'Actual capture start')
    finished=utc_clock(cap['finished_utc'],'Actual capture finish')
    require(started<=finished,'Actual capture clocks reversed')
    require(started<=utc_clock(receipt['utc'],'Actual final reconciliation clock')<=finished,'Reconciliation clock outside genuine capture interval')
    for flag,v in [('--root-bindings',a.root_bindings),('--root-bindings-sha256',a.root_bindings_sha256),('--plan',a.final_plan),('--plan-sha256',a.final_plan_sha256),('--preparation-manifest-sha256',a.preparation_manifest_sha256),('--output',ps['final_manifest'].parent.relative_to(A).as_posix())]:
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
    previous_root=B/'audits/pr40_2814'
    require(ps['previous_mirror']==previous_root/'state_mirror_bindings.json' and ps['previous_post']==previous_root/'post_acceptance_verification.json','Literal actual completed PR40 predecessor evidence required')
    previous=load(ps['previous_mirror']); require(len(previous['entries'])==30 and 40 in previous['required_completed_prs'] and 41 not in previous['required_completed_prs'],'Actual completed PR40 prior scope required')
    required(load(ps['previous_post']),{'status':'PASS','pr':40,'targets':31,'consumed_substantive_turns':37,'primary_acceptances':30,'program_completed_count':30,'fresh_native_mirror_noop':True},'Completed actual predecessor post verification')
    fresh=load(ps['fresh_preimage']); required(fresh,{'approved_by_root':True},'Fresh actual native preimage')
    created=utc_clock(fresh['created_utc'],'Actual root fresh preimage creation')
    require(created<=dt.datetime.now(dt.timezone.utc),'Fresh root preimage creation clock is in the future')
    require(type(fresh['reason_date_utc']) is str and fresh['reason_date_utc']==created.date().isoformat(),'Root rebase reason date must match the actual UTC creation date')
    require(type(fresh['reason']) is str and fresh['reason']==fresh['reason'].strip() and len(fresh['reason'])>=40 and len(fresh['reason'].split())>=6,'Substantive root-reviewed rebase reason required; a token such as yes is insufficient')
    require(type(fresh['current_head']) is str and re.fullmatch('[0-9a-f]{40}',fresh['current_head']),'Explicit fresh main HEAD required, independently of archived replay HEAD')
    rr=rows(fresh['files']); require({z['path'] for z in rr}==NATIVE and len(rr)==13,'Exact13 fresh full native/inventory pins required')
    require(all(type(z.get('worktree_mode')) is int and 0<=z['worktree_mode']<=0o7777 for z in rr),'Explicit typed thirteen worktree permission modes required')
    snap=load(A/'snapshot_manifest.json'); required(snap,{'head':HEAD,'base':ORIGINAL_BASE},'Original16/17 snapshot'); require(len(snap['files'])==16 and len(snap['changed_paths'])==17,'Original16/17 counts')
    raw=git_bytes('diff',ORIGINAL_BASE,HEAD); require(len(raw)==201709 and raw==(A/'pr_input/diff.patch').read_bytes(),'Entire original Git diff changed')
    require(git_bytes('diff','--name-only',ORIGINAL_BASE,HEAD).decode().splitlines()==snap['changed_paths'],'Original changed paths differ')
    for z in rows(snap['files']):
        path='unsolved_math_prioritization/attempts/'+ID+'/'+z['path']
        require(git_bytes('show',HEAD+':'+path)==(C/'original_archive'/z['path']).read_bytes(),'Original Git/archive mismatch')
        require(git_bytes('ls-tree','-z',HEAD,'--',path).decode().rstrip('\0')==z['mode']+' blob '+z['git_blob']+'\t'+path,'Exact original Git mode/blob mismatch')
    for rev in [ORIGINAL_BASE,HEAD]:
        state=parse(git_bytes('show',rev+':unsolved_math_prioritization/state.json')); require(ID not in state,'No original primary/duplicate native state allowed')
        hp='unsolved_math_prioritization/history.jsonl'
        hb=git_bytes('show',rev+':'+hp) if git_bytes('ls-tree','-z',rev,'--',hp) else b''
        require(not hb or hb.endswith(b'\n'),'Historical history incomplete')
        require(not any(str(e.get('id',e.get('problem_id',''))) in {ID} for e in map(parse,hb.splitlines())),'No invented original selected history allowed')
    frozen,_=basis(a.root_bindings,a.root_bindings_sha256)
    return frozen,{n:getattr(a,n) for n in ['preparation_manifest_sha256','final_plan','final_plan_sha256','final_receipt','final_receipt_sha256','final_manifest','final_manifest_sha256','reconciliation_capture','reconciliation_capture_sha256','previous_mirror','previous_mirror_sha256','previous_post','previous_post_sha256','fresh_preimage','fresh_preimage_sha256','root_bindings','root_bindings_sha256']}


def selected(data):
    lines=data.decode().splitlines(keepends=True); heads=[s for s in lines if s.startswith('| Rank | ID / code |')]
    require(len(heads)==1 and [s.strip() for s in heads[0].split('|')[1:-1]]==HEADER,'Exact12 named columns required')
    rr=[s for s in lines if len(s.split('|'))==14 and s.split('|')[2].strip()==ID+' / '+CODE]
    require(len(rr)==1,'Unique exact primary queue row required'); return rr[0]


def derive_inventory(before,remote,finalized_utc):
    require(type(before) is dict and type(before.get('items')) is list and len(before['items'])==180,'Complete retained180-item program inventory required')
    require(all(type(z) is dict and type(z.get('number')) is int for z in before['items']),'Typed original inventory identities required')
    identities=[z['number'] for z in before['items']]
    require(len(set(identities))==180 and identities.count(41)==1,'Exact unique selected original inventory identity required')
    require(type(before.get('completed_count')) is int and before['completed_count']==30 and sum(z.get('stage')=='complete' for z in before['items'])==30,'Actual30 prior primaries required')
    required(remote,{'state':'MERGED','isDraft':False,'number':41,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual merged remote inventory derivation')
    require(type(remote['mergeCommit']) is dict and set(remote['mergeCommit'])=={'oid'} and type(remote['mergeCommit']['oid']) is str and re.fullmatch('[0-9a-f]{40}',remote['mergeCommit']['oid']),'Exact actual merge oid required')
    clock=utc_clock(finalized_utc,'Retained actual finalization UTC');merged=utc_clock(remote['mergedAt'],'Actual merged UTC')
    require(merged<=clock<=dt.datetime.now(dt.timezone.utc),'Actual merged/finalization clocks reversed or future')
    inv=copy.deepcopy(before);chosen=next(z for z in inv['items'] if z['number']==41)
    require(chosen.get('stage')!='complete','Original selected inventory is not already complete')
    chosen.update(stage='complete',outcome='unsolved_accepted_partial',queue_status='unsolved',audited_head=HEAD,merge_commit=remote['mergeCommit']['oid'],merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts='2/5',new_substantive_attempts=0,cumulative_attempts='2/5',paper_or_new_doi_or_tracker=False)
    done=sum(z.get('stage')=='complete' for z in inv['items']);require(done==31,'Exactly31 derived primary completions')
    inv.update(updated_at_utc=finalized_utc,last_checkpoint_utc=finalized_utc,completed_count=31,program_completion_estimate_percent=31/180*100,completion_estimate_percent=31/180*100,current_pr=42)
    return inv


def finalization(pins,pre):
    record=load(A/'integration_finalization.json');remote=load(A/'remote_merge_receipt.json')
    require(type(record) is dict and 'utc' in record,'Actual retained finalization record required')
    expected={'schema':'pr41-actual-integration-finalization/v1','utc':record['utc'],**pins,'pr':41,'before_inventory_sha256':pre['inventory_before_sha256'],'remote_merge_receipt':pin(A/'remote_merge_receipt.json'),'merge_commit':remote['mergeCommit']['oid'],'merge_tree':git('show','-s','--format=%T',remote['mergeCommit']['oid']),'source_sha256':sha((HERE/'integrate_reviewed_partial.py').read_bytes())}
    exact_reference(record['remote_merge_receipt']);require(equal(record,expected),'Complete typed actual finalization record required')
    final_clock=utc_clock(record['utc'],'Actual retained finalization UTC')
    phases=[load(A/n) for n in ['integration_preflight.json','integration_check.json','integration_prepush.json']]
    clocks=[utc_clock(z['utc'],'Actual retained phase UTC') for z in phases]+[final_clock]
    require(clocks==sorted(clocks) and final_clock<=dt.datetime.now(dt.timezone.utc),'Retained integration clocks reversed or future')
    require(utc_clock(remote['mergedAt'],'Actual merged UTC')<=final_clock,'Actual merge is after retained finalization')
    before=(A/'integration_inventory_before.json').read_bytes();require(sha(before)==pre['inventory_before_sha256'],'Entire retained before inventory differs')
    derive_inventory(parse(before),remote,record['utc'])
    return record,remote


def expected_acceptance(pins,pre):
    final,remote=finalization(pins,pre)
    return {'schema':'pr41-accepted-qualified-conditional-partial/v1','utc':final['utc'],**SCIENCE,**pins,'pr':41,'id':9700035,'problem_id':9700035,'problem_number':CODE,'queue_status':'unsolved','outcome':'unsolved_accepted_partial_merged','original_head':HEAD,'original_base':ORIGINAL_BASE,'merge_commit':final['merge_commit'],'merge_tree':final['merge_tree'],'merge_parents':[pre['main_before'],HEAD],'merged_at':remote['mergedAt'],'remote_state':'MERGED','remote_isDraft':False,'canonical_scientific_artifact_sha256':SCIENCE_SHA,'source_record_sha256':SOURCE_SHA,'original_ledger_sha256':LEDGER_SHA,'substantive_attempts_used':2,'substantive_attempt_limit':5,'native_historical_events_inferred':False,'historical_metadata_archival_only':True,'workflow_completion_estimate_percent':100,'full_resolution_completion_estimate_percent':0,'scientific_scope':load(HERE/'SCIENTIFIC_SCOPE.json')}


def accepted_invariants(o,pins,pre,audit=False):
    expected=expected_acceptance(pins,pre)
    if audit:
        expected.update(canonical_manifest_sha256=sha(regular(K,'MANIFEST.json').read_bytes()),canonical_manifest_entries=len(rows(load(K/'MANIFEST.json')['files'])))
    require(equal(o,expected),'Complete typed canonical/audit accepted receipt schema and derived values required; meaningful extensions prohibited')
    source(K)
    for n in ADMIN:
        expected_admin=load(C/n)
        expected_admin.update(**SCIENCE,**pins,id=9700035,current_context_path='CURRENT_CONTEXT_PRESENT.md',current_audit_scope_path='CURRENT_AUDIT_SCOPE_PRESENT.md',current_gate='accepted_qualified_partial',current_verdict=WHOLE_VERDICT,status='unsolved_accepted_partial_merged',new_whole_current_gate=WHOLE_VERDICT,historical_verdict_transferred=False,merge_commit=o['merge_commit'],merge_tree=o['merge_tree'],merged_at=o['merged_at'])
        require(equal(load(K/n),expected_admin),'Complete typed present administrative object differs: '+n)


def canonical_names(frozen,accepted=False):
    return {z['path'] for z in frozen}|{'reviewed_pending_administration/'+n for n in ADMIN}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md'}|({'acceptance.json','ACCEPTANCE.md','MANIFEST.json'} if accepted else set())


def canonical(frozen,accepted=False):
    exact(K,canonical_names(frozen,accepted))
    for z in frozen:
        p=K/('reviewed_pending_administration/'+z['path'] if z['path'] in ADMIN else z['path'])
        require(p.read_bytes()==(C/z['path']).read_bytes(),'Frozen science/archival administration changed')
    require((K/'reviewed_pending_administration/MANIFEST.json').read_bytes()==(C/'MANIFEST.json').read_bytes(),'Dated frozen manifest changed');source(K)


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


def native_modes(values):
    for z in rows(values):
        require(type(z.get('worktree_mode')) is int and 0<=z['worktree_mode']<=0o7777,'Explicit typed fresh worktree mode required')
        require(regular(R,z['path']).stat().st_mode&0o7777==z['worktree_mode'],'Exact native worktree permission mode changed: '+z['path'])


def fresh_check(pre,allowed=()):
    f=load(R/pre['fresh_preimage']); remaining=[z for z in rows(f['files']) if z['path'] not in allowed]
    check(R,remaining); native_modes(remaining); foreign_check(pre)


def native_git_snapshot(revision,values,skip=()):
    rr=rows(values)
    require({z['path'] for z in rr}==NATIVE and len(rr)==13,'Exact thirteen native rows required for Git/worktree split')
    require(set(skip)<={'unsolved_math_prioritization/QUEUE.md'},'Only the named accepted queue may be skipped')
    for z in rr:
        n=z['path']
        if n in skip: continue
        entries=git_bytes('ls-tree','-z',revision,'--',n)
        if n in IGNORED_CACHE3:
            require(entries==b'','Exact ignored cache must remain absent from selected Git tree: '+n)
            raw=regular(R,n).read_bytes()
            require(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Entire ignored cache worktree bytes changed: '+n)
        else:
            decoded=entries.decode().split('\0')
            require(len(decoded)==2 and decoded[-1]=='','Exactly one tracked native Git entry required: '+n)
            fields,literal=decoded[0].split('\t'); mode,kind,blob=fields.split()
            require(literal==n and kind=='blob' and mode=='100644','Exact nonexecutable tracked native Git mode required: '+n)
            raw=git_bytes('show',revision+':'+n)
            require(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Entire tracked native Git bytes changed: '+n)


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
    native_git_snapshot(merge,load(R/pre['fresh_preimage'])['files'],{'unsolved_math_prioritization/QUEUE.md'})
    changed=set(git_bytes('diff-tree','-r','--no-commit-id','--name-only','-z',pre['main_before'],merge).decode().split('\0'))-{''}
    require(changed<={prefix+z['path'] for z in rr}|{'unsolved_math_prioritization/QUEUE.md'},'Unrelated real merge paths')
    foreign_check(pre)
    for z in pre['foreign_logs']: require(git_bytes('ls-tree','-z',merge,'--',z['path']).decode().rstrip('\0')==z['head_entry'],'Real merge included foreign log')
    return git('show','-s','--format=%T',merge)


def mirror_module(proposal):
    p=BASE/'revision2/accepted_state_sync_v2.py'; require(sha(p.read_bytes())==MIRROR_SHA,'Reviewed native mirror source changed')
    spec=importlib.util.spec_from_file_location('pr41_bound_native_mirror',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    # Each previously accepted complete ledger and typed budget is exact-bound by the genuine prior proposal.
    budgets=[]
    for e in proposal['entries']:
        b=e['budget']; require(type(b['used']) is int and type(b['limit']) is int and 0<=b['used']<=b['limit'],'Typed preserved prior budget')
        raw=regular(R,b['ledger']['path']).read_bytes(); require(sha(raw)==b['ledger']['sha256'],'Full original prior ledger changed'); budgets.append((b['kind'],b['used'],b['limit'],raw))
    def ledger(raw,kind,used,limit):
        m.require(type(used) is int and type(limit) is int and any(kind==k and used==u and limit==l and raw==d for k,u,l,d in budgets),'Exact complete accepted ledger/budget required; no inference')
    m.ledger_budget=ledger
    def strict_bound(repo,reference):
        require(Path(repo).resolve()==R.resolve(),'Exact native mirror repository required')
        raw=regular(R,reference['path']).read_bytes();require(sha(raw)==digest(reference['sha256']),'Strict native mirror binding changed');return raw
    m.bound=strict_bound
    return m
