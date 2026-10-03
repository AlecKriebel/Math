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
K = R / 'unsolved_math_prioritization/attempts/30004386'
Q = R / 'unsolved_math_prioritization/QUEUE.md'
BASE = B / 'infrastructure/accepted_state_sync'
ID, CODE, PR = '30004386', 'OWR-17469-011', 43
HEAD = '86be0f85c7a37a5cad8d24abd16a32d8d1f27e62'
ORIGINAL_BASE = '60292bed09f59236aa192cb17aa138f7b4750e1a'
CURRENT_SHA = '4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14'
DEPS_SHA = '4cec33dfaee001419ccf07dc2483d3c8bdf67f0308e5601cbefb4e620c45337e'
SOURCE_SHA = 'a98970b4196fbc9f53d8b9ba431337b88d5807e73c7bfdda63a091ad166765b6'
LEDGER_SHA = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
SCIENCE_SHA = '90402aea80b79b7713d740863b6058b43c64050c3499701b2bf8490c90b210e3'
MIRROR_SHA = 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
ADMIN = {'status.json', 'readiness.json', 'review/verdict.json'}
IMMUTABLE = {'SOURCE_STATUS.md','check_normalization.py','check_results.json','source_record.json','source_checksums.json','turns.jsonl','review/author_replay/check_normalization.py','review/author_replay/check_results.json','review/independent_checks.py','review/independent_results.json'}
WHOLE_VERDICT = 'PASS_EXACT_FROZEN_CURRENT_PACKET_FOR_CREDITED_SOURCE_STATUS_ACCEPTANCE'
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
NATIVE = {'draft_pr_publication_program_20260930/inventory.json'} | {'unsolved_math_prioritization/' + n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
IGNORED_CACHE3 = {'unsolved_math_prioritization/cache/problems.json', 'unsolved_math_prioritization/cache/research_results.json', 'unsolved_math_prioritization/cache/catalog.sqlite'}
FOREIGN_LOGS = {'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/commands.tsv', 'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/full_transcript.log'}
SCIENCE = {'full_problem_solved': False, 'full_target_resolved_in_prior_published_literature': True, 'full_problem_solved_by_project': False, 'prior_publication_doi': '10.4064/sm210413-16-9', 'partial_valid': True, 'novelty_claimed': False, 'priority_claimed': False, 'original_substantive_attempts': 0, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'verification_attempts_added': 0, 'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'paper_or_new_doi_or_tracker': False, 'human_referee_review_claimed': False}


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
    obj=parse(raw)
    known={
        'pr43-acceptance-source-closure/v1':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'},
        'PR43_STRICT_CURRENT_PACKET_v1':{'schema','self_excluded','files_count','files','current_gate','prior_source_status','full_problem_solved_by_project','novelty_claimed','original_substantive_attempts','new_substantive_attempts','audit_turns'},
        'pr43-final-root-two-member-closure/v1':{'schema','utc','self_excluded','files_count','files'},
        'pr43-accepted-strict-self-excluding-closure/v1':{'schema','utc','self_excluded','files_count','files','foreign_excluded_prefixes'},
    }
    require(type(obj) is dict and obj.get('schema') in known,'Unknown critical closure schema')
    keyset(obj,known[obj['schema']],'Exact recognized closure schema')
    if obj['schema']=='pr43-acceptance-source-closure/v1':
        required(obj,{'status':'CLOSED_SOURCE_ONLY','source_only':True,'proposed_helpers_imported_compiled_executed':False,'future_acceptance_or_ROOT_approval_claimed':False},'Closed preparation, not future execution')
    rr=rows(obj['files'])
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
    require(p.resolve().is_relative_to(A.resolve()),'Evidence outside exact PR43 audit')
    return p.read_bytes()


def pin(p):
    raw=Path(p).read_bytes(); return {'path':Path(p).relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)}


def binding(p): return {k:v for k,v in pin(p).items() if k!='bytes'}


def write(p,raw,exclusive=False):
    p=Path(p); require(p.parent.is_dir() and not p.is_symlink() and all(not d.is_symlink() for d in p.parents),'Unsafe output or symlink ancestor')
    if exclusive: require(not p.exists(),'Existing output: inspect before retry')
    tmp=p.with_name(p.name+'.pr43-tmp')
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
    keyset(o,{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Complete known GitHub receipt')
    required(o,{'number':43,'url':'https://github.com/AlecKriebel/Math/pull/43','headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual remote')
    return o


def original_native(base):
    snapshot=load(A/'snapshot_manifest.json')
    require(snapshot['schema']=='pr43-root-readonly-original-snapshot/v1' and len(snapshot['files'])==16,'Complete original16 required')
    exact(base,{z['path'] for z in rows(snapshot['files'])})
    for z in rows(snapshot['files']):
        raw=regular(base,z['path']).read_bytes()
        require(raw==regular(A/'source_snapshot',z['path']).read_bytes() and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Original16 bytes differ')


def source(base):
    original_native(base/'original_archive')
    for n in IMMUTABLE:
        require(regular(base,n).read_bytes()==regular(A/'source_snapshot',n).read_bytes(),'Immutable math/code/saved result/source/empty ledger changed')
    require(sha(regular(base,'SOURCE_STATUS.md').read_bytes())==SCIENCE_SHA and sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Scientific/source anchors changed')
    raw=regular(base,'turns.jsonl').read_bytes();require(raw==b'' and sha(raw)==LEDGER_SHA,'Literal original zero-byte ledger required, no fictitious attempt')
    prior=regular(base,'root_evidence/pinned_prior_report.json').read_bytes()
    require(prior==regular(A,'pinned_prior_report.json').read_bytes() and equal(parse(prior),{}),'Absent raw OWR-17469-011 key and SQL fallback{} must not become PRESENT/null')
    require(sha(regular(base,'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes())=='868b8e2af799f8371c3900529079af354ef51cf01ee08adeccc666ec0884d3cd','Exact global source qualifications required')


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
    for key in ['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post']:exact_reference(o[key])
    expected=load(HERE/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
    expected.update(status='ROOT_APPROVED_CLOSED_WHOLE_AND_ACTUAL_PR42_EVIDENCE',created_utc=o['created_utc'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR42_predecessor_read_completed=True)
    for key in ['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post']:expected[key]=o[key]
    require(equal(o,expected),'Complete typed external ROOT bindings equality required')
    require(utc_clock(o['created_utc'],'ROOT binding creation')<=dt.datetime.now(dt.timezone.utc),'ROOT binding may not be future dated')
    previous_root=B/'audits/pr42_2233'
    for key,file in [('previous_mirror','state_mirror_bindings.json'),('previous_post','post_acceptance_verification.json'),('previous_root_post','ROOT_ACTUAL_POST_INSPECTION.json')]:
        require(o[key]['path']==(previous_root/file).relative_to(R).as_posix(),'Literal genuine completed PR42 predecessor required')
        check(R,[o[key]])
    previous=load(R/o['previous_mirror']['path']);post=load(R/o['previous_post']['path']);rootpost=load(R/o['previous_root_post']['path'])
    require(type(previous['entries']) is list and len(previous['entries'])==32 and all(type(z['pr']) is int for z in previous['entries']),'Exact32 typed original prior primary entries')
    numbers=[z['pr'] for z in previous['entries']];require(len(set(numbers))==32 and 42 in numbers and 43 not in numbers and equal(sorted(numbers),previous['required_completed_prs']),'Exact completed32-primary predecessor identities')
    required(post,{'status':'PASS','pr':42,'targets':33,'consumed_substantive_turns':41,'primary_acceptances':32,'program_completed_count':32,'fresh_native_mirror_noop':True,'one_present_primary_event':True,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,'full_problem_solved':False,'paper_or_new_doi_or_tracker':False},'Genuine completed actual PR42 predecessor, mandatory even for final seal')
    required(rootpost,{'schema':'pr42-root-complete-actual-post-inspection/v1','status':'PASS','completed_primary_prs':32,'all32_prior_states_and_full_history_prefix_preserved':True,'current13_match_exact_allowed_acceptance_changes':True,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False},'Completed ROOT actual PR42 post reading')
    require(equal(rootpost['entire_post'],post),'Entire actual predecessor post object equals ROOT completed read')
    require(utc_clock(rootpost['created_utc'],'ROOT predecessor postUTC')<=utc_clock(o['created_utc'],'ROOT source/predecessor acceptanceUTC'),'ROOT source binding cannot precede actual predecessor reading')
    return o,p


def resolve_foreign_literal(literal):
    """Preserve a literal archived row; resolve traversal with no symlink hops."""
    require(type(literal) is str and literal.startswith(str(R)+'/') and '\\' not in literal and '\0' not in literal,'Exact absolute foreign reference inside repository required')
    require(R.is_dir() and not R.is_symlink() and R.resolve(strict=True)==R,'Regular canonical repository root required')
    for ancestor in R.parents:require(ancestor.is_dir() and not ancestor.is_symlink(),'Symlink repository ancestor prohibited')
    parts=literal[len(str(R))+1:].split('/')
    require(parts and all(part and part not in {'.git','__pycache__'} for part in parts),'Empty or private foreign reference component prohibited')
    current=R
    for i,part in enumerate(parts):
        require(current.is_dir() and not current.is_symlink(),'Every traversed foreign ancestor must be a real directory')
        if part=='.':continue
        if part=='..':
            require(current!=R,'Foreign traversal outside repository prohibited')
            current=current.parent
        else:current=current/part
        require(current.exists() and not current.is_symlink(),'Missing/symlink foreign traversal component prohibited')
        require(current==R or current.is_relative_to(R),'Every foreign traversal prefix must stay inside repository')
        if i<len(parts)-1:require(current.is_dir(),'Non-directory foreign traversal component')
    canonical=current.resolve(strict=True)
    require(canonical!=R and canonical.is_relative_to(R) and canonical==current,'Foreign canonical path must stay strictly inside repository')
    return regular(R,canonical.relative_to(R).as_posix())


def basis(root_bindings,root_bindings_sha256):
    approved,rp=root_binding_input(root_bindings,root_bindings_sha256)
    inputs=load(HERE/'INPUT_BINDINGS.json');refs=[]
    for n in sorted(inputs['pins']):
        ref=exact_reference(inputs['pins'][n]);check(R,[ref]);refs.append(ref)
    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,347,frozen=True)
    deps=load(C/'CURRENT_DEPENDENCIES.json')
    keyset(deps,{'anchor_repository_relative','resolution','files','foreign_primary_and_derivative_members_individually_hash_bound_not_copied','current_native13','current_main_head'},'Exact portable dependency schema')
    required(deps,{'anchor_repository_relative':A.relative_to(R).as_posix(),'resolution':'repository_root / anchor_repository_relative / files.path; never scratch','foreign_primary_and_derivative_members_individually_hash_bound_not_copied':True,'current_main_head':'c61dc0cb572de281b871264819c8b80d647d0373'},'Exact dated dependencies')
    require(sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())==DEPS_SHA and len(rows(deps['files']))==274,'Complete274 dependencies');check(A,deps['files']);source(C)
    for n in ADMIN:require(equal(load(C/n),load(HERE/'EXPECTED_CURRENT_ADMIN.json')),'Complete dated pending admin differs')
    w=A/'whole_current_source_first_family';wm=exact_reference(approved['whole_manifest'])
    require(equal(wm,inputs['closed_whole_manifest']) and wm['path']==(w/'SELF_MANIFEST.json').relative_to(R).as_posix(),'Exact actual whole closure required')
    whole=parse(bound(wm));keyset(whole,{'schema','created_utc','actual_closure_pid','files_count','files','self_excluded','mode','directories','candidate_manifest_sha256','external_individually_excluded_inputs','external_copied_members','authorship_scope','review_completion_percent','new_discovery_percent','ROOT_future_approval_certified'},'Complete known whole closure')
    required(whole,{'schema':'PR43_NEW_WHOLE_CURRENT_SOURCE_FIRST_SELF_ONLY_CLOSURE_v1','files_count':30,'self_excluded':['SELF_MANIFEST.json'],'mode':'0444','candidate_manifest_sha256':CURRENT_SHA,'external_copied_members':[],'ROOT_future_approval_certified':False},'Actually closed new whole family')
    authored=rows(whole['files']);require(len(authored)==30,'Exact30 owned whole members')
    for z in whole['files']:keyset(z,{'path','bytes','sha256','mode','classification','novelty_claim'},'Complete whole owned reference');require(z['mode']=='0444' and z['novelty_claim'] is False,'Declared whole ownership/mode')
    check(w,authored);exact(w,{z['path'] for z in authored}|{'SELF_MANIFEST.json'});frozen_files(w,authored,'SELF_MANIFEST.json')
    dated_head='c61dc0cb572de281b871264819c8b80d647d0373';historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    dated=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');required(dated,{'schema':'PR43_ROOT_FRESH13_INPUT_PREIMAGES_v1','current_head':dated_head},'Genuine dated freeze13 authority, not current state')
    dated_native={z['path']:z for z in rows(dated['files'])};require(set(dated_native)==NATIVE and len(dated_native)==13,'Exact dated13')
    foreign=whole['external_individually_excluded_inputs'];require(type(foreign) is list and len(foreign)==756,'Exact756 individual excluded references')
    literal_names=set();canonical_names=set();historical_checked=set()
    for z in foreign:
        keyset(z,{'path','bytes','sha256','role','individual_exclusion'},'Exact foreign reference')
        require(z['path'] not in literal_names,'Duplicate literal foreign identity');literal_names.add(z['path'])
        canonical=resolve_foreign_literal(z['path']);n=canonical.relative_to(R).as_posix();canonical_names.add(n)
        if n in historical:
            captured=dated_native[n];require(type(z['bytes']) is int and z['bytes']==captured['bytes'] and z['sha256']==captured['sha256'],'Historical row must equal actual freeze13 pin')
            entries=git_bytes('ls-tree','-z',dated_head,'--',n).decode().split('\0');require(len(entries)==2 and entries[-1]=='','One immutable historical Git blob')
            fields,literal=entries[0].split('\t');mode,kind,blob=fields.split();require(mode=='100644' and kind=='blob' and literal==n,'Exact historical Git path/mode')
            raw=git_bytes('show',dated_head+':'+n);historical_checked.add(n)
        else:raw=canonical.read_bytes()
        require(type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==digest(z['sha256']),'Entire individual foreign input changed')
    require(len(literal_names)==756 and NATIVE<=canonical_names and historical_checked==historical,'Exact756 identities, native13 and historical4')
    verdict=parse(bound(inputs['closed_whole_result']));require(equal(verdict,load(HERE/'EXPECTED_WHOLE_VERDICT.json')),'Entire exact typed new independent VERDICT')
    required(verdict,{'verdict':WHOLE_VERDICT,'candidate_manifest_sha256':CURRENT_SHA,'mandatory_defects':[],'source_or_packet_repair_required':False,'mathematical_gap':None,'justified_status':'already_solved','full_target_resolved_in_prior_published_literature':True,'prior_publication_doi':'10.4064/sm210413-16-9','full_problem_solved_by_project':False,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0},'Scientific/source-status independent gate')
    bound(inputs['closed_whole_report'])
    rootref=exact_reference(approved['root_whole_inspection']);require(equal(rootref,inputs['closed_root_whole_inspection']),'Exact ROOT whole read pin')
    root=parse(bound(rootref));require(equal(root,load(HERE/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and equal(root['complete_VERDICT_object'],verdict),'Entire genuine ROOT whole inspection and complete VERDICT')
    required(root,{'schema':'pr43-root-complete-closed-whole-inspection/v1','status':'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION','personal_report_and_verdict_fully_read':True,'all_first_party_whole_bytes_and_modes_checked':True,'all_foreign_individual_whole_bytes_checked':True,'exact_self_only_recursive_closure_checked':True,'future_execution_approved':False,'mandatory_defects':[],'mandatory_corrections':[]},'Genuine own ROOT full reading')
    require(utc_clock(root['created_utc'],'ROOT whole read')<=dt.datetime.now(dt.timezone.utc),'No future ROOT read')
    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json')
    require(ledger['schema']=='PR43_ROOT_PRIMARY_READ_LEDGER_v1' and card['schema']=='PR43_ROOT_SCIENCE_CARD_v1' and ledger['reading_completed'] is True and card['reading_completed'] is True and len(ledger['root_flags'])==8 and equal(ledger['root_flags'],card['root_flags']) and all(v is True for v in ledger['root_flags'].values()),'Distinct actual scientific ledger/card schemas and eight true flags')
    operator=exact_reference(approved['root_capture_operator']);require(equal(operator,inputs['root_capture_operator']),'ROOT43 reviewed operator differs');bound(operator)
    refs += [pin(C/'MANIFEST.json'),pin(C/'CURRENT_DEPENDENCIES.json'),wm,inputs['closed_whole_result'],inputs['closed_whole_report'],rootref,pin(rp)]
    refs += [approved[n] for n in ['previous_mirror','previous_post','previous_root_post']]
    require(len({z['path'] for z in refs})==len(refs),'No duplicate immutable evidence identity')
    return frozen,sorted(refs,key=lambda z:z['path'])


def plan_scope(o,prep,root_bindings,root_bindings_sha256):
    _,refs=basis(root_bindings,root_bindings_sha256)
    bindings,_=root_binding_input(root_bindings,root_bindings_sha256)
    draft=load(HERE/'DRAFT_FINAL_PLAN.json')
    draft.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=prep,root_bindings=root_bindings,root_bindings_sha256=root_bindings_sha256,whole_manifest_sha256=bindings['whole_manifest']['sha256'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR42_predecessor_read_completed=True,immutable_evidence_references=refs)
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
    required(receipt,{'schema':'pr43-actual-final-reconciliation/v1','status':'PASS','actual_root_reconciliation':True,'pr':43,'problem_id':30004386,'preparation_manifest_sha256':a.preparation_manifest_sha256,'entire_scope':scope,'bindings_before':refs,'bindings_after':refs,'root_reviewed_plan':pin(ps['final_plan']),'reconciliation_source':pin(HERE/'seal_final_evidence.py'),'science_helpers_executed':False,'new_substantive_attempts':0,'audit_turns':0,'shared_mutations':False},'Actual final reconciliation')
    require(ps['final_manifest'].parent==ps['final_receipt'].parent and ps['final_manifest'].name=='FINAL_MANIFEST.json','Literal final closure required')
    fm=manifest(ps['final_manifest'].parent,'FINAL_MANIFEST.json',a.final_manifest_sha256,2,frozen=True)
    require({z['path'] for z in fm}=={'ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json'} and ps['final_receipt'].name=='ROOT_FINAL_RECONCILIATION.json','Exact final output names required')
    require(equal(load(ps['final_manifest'].parent/'ROOT_REVIEWED_SCOPE.json'),scope),'Final complete scope copy differs')
    cap=load(ps['reconciliation_capture'])
    keyset(cap,{'schema','argv','cwd','actual_execution','completed','pid','source_sha256','stdin_supplied','native13_before','main_head_before','started_utc','exit_code','finished_utc','source_unchanged','main_head_after','native13_after','stdout','stderr','readonly_git_queries','status'},'Complete final actual ROOT capture schema')
    required(cap,{'schema':'ROOT_actual_audit_administrative_capture_v1','actual_execution':True,'completed':True,'exit_code':0,'status':'PASS','stdin_supplied':False,'source_unchanged':True,'source_sha256':sha((HERE/'seal_final_evidence.py').read_bytes()),'cwd':str(A)},'Genuine actual final capture')
    require(equal(cap['native13_before'],cap['native13_after']) and cap['main_head_before']==cap['main_head_after'],'Final sealer capture must preserve native13 and HEAD')
    require(len(rows(cap['native13_before']))==13 and {z['path'] for z in rows(cap['native13_before'])}==NATIVE,'Exact thirteen actual final capture native references')
    root_authority,_=root_binding_input(a.root_bindings,a.root_bindings_sha256)
    require(type(cap['pid']) is int and cap['pid']>0 and type(cap['argv']) is list and str(HERE/'seal_final_evidence.py') in cap['argv'],'Actual PID/argv required')
    started=utc_clock(cap['started_utc'],'Actual capture start')
    finished=utc_clock(cap['finished_utc'],'Actual capture finish')
    require(started<=finished<=dt.datetime.now(dt.timezone.utc),'Actual capture clocks reversed or future')
    require(started<=utc_clock(receipt['utc'],'Actual final reconciliation clock')<=finished,'Reconciliation clock outside genuine capture interval')
    for flag,v in [('--root-bindings',a.root_bindings),('--root-bindings-sha256',a.root_bindings_sha256),('--plan',a.final_plan),('--plan-sha256',a.final_plan_sha256),('--preparation-manifest-sha256',a.preparation_manifest_sha256),('--output',ps['final_manifest'].parent.relative_to(A).as_posix())]:
        require(cap['argv'].count(flag)==1 and cap['argv'][cap['argv'].index(flag)+1]==v,'Actual final argv pin differs')
    require(cap['argv'].count('--execute')==1,'Actual execution flag required')
    cb=ps['reconciliation_capture'].parent
    require(ps['reconciliation_capture'].name=='CAPTURE.json' and cb.parent==A,'Literal CAPTURE.json in a new adjacent root capture required')
    streams=rows([cap['stdout'],cap['stderr']])
    exact_reference(cap['stdout']);exact_reference(cap['stderr'])
    stream_names={z['path'] for z in streams}
    require(stream_names=={'stdout.bin','stderr.bin'},'Literal two ROOT operator streams required')
    check(cb,streams); require(sha(regular(cb,'PRELAUNCH_SOURCE.py').read_bytes())==cap['source_sha256'],'Actual prelaunch source changed')
    require(regular(cb,'PRELAUNCH_OPERATOR.py').read_bytes()==bound(root_authority['root_capture_operator']),'Actual personally reviewed ROOT prelaunch operator changed')
    required(parse(regular(cb,cap['stdout']['path']).read_bytes()),{'status':'PASS','final_receipt_sha256':a.final_receipt_sha256,'final_manifest_sha256':a.final_manifest_sha256},'Entire actual child stdout')
    exact(cb,{'CAPTURE.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py'}|stream_names)
    require(not ps['fresh_preimage'].resolve().is_relative_to(C.resolve()) and not ps['fresh_preimage'].resolve().is_relative_to(HERE.resolve()),'Fresh root preimage must be adjacent new evidence')
    previous_root=B/'audits/pr42_2233'
    authority,_=root_binding_input(a.root_bindings,a.root_bindings_sha256)
    require(equal(pin(ps['previous_mirror']),authority['previous_mirror']) and equal(pin(ps['previous_post']),authority['previous_post']),'Exact genuine ROOT-approved PR42 predecessor bytes')
    previous=load(ps['previous_mirror']);require(len(previous['entries'])==32 and 42 in previous['required_completed_prs'] and 43 not in previous['required_completed_prs'],'Actual completed PR42 prior scope')
    required(load(ps['previous_post']),{'status':'PASS','pr':42,'targets':33,'consumed_substantive_turns':41,'primary_acceptances':32,'program_completed_count':32,'fresh_native_mirror_noop':True},'Completed actual PR42 predecessor post')
    rootpost=load(R/authority['previous_root_post']['path'])
    required(rootpost,{'schema':'pr42-root-complete-actual-post-inspection/v1','status':'PASS','completed_primary_prs':32,'all32_prior_states_and_full_history_prefix_preserved':True,'current13_match_exact_allowed_acceptance_changes':True,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False},'Genuine completed ROOT PR42 post read')
    require(equal(rootpost['entire_post'],load(ps['previous_post'])),'Entire genuine predecessor post object')
    fresh=load(ps['fresh_preimage']); required(fresh,{'approved_by_root':True},'Fresh actual native preimage')
    keyset(fresh,{'schema','approved_by_root','created_utc','reason_date_utc','reason','current_head','files'},'Exact current ROOT fresh input schema')
    require(fresh['schema']=='pr43-root-fresh-acceptance-input-preimages/v1','Unknown fresh authority schema')
    created=utc_clock(fresh['created_utc'],'Actual root fresh preimage creation')
    require(created<=dt.datetime.now(dt.timezone.utc),'Fresh root preimage creation clock is in the future')
    require(type(fresh['reason_date_utc']) is str and fresh['reason_date_utc']==created.date().isoformat(),'Root rebase reason date must match the actual UTC creation date')
    require(type(fresh['reason']) is str and fresh['reason']==fresh['reason'].strip() and len(fresh['reason'])>=40 and len(fresh['reason'].split())>=6,'Substantive root-reviewed rebase reason required; a token such as yes is insufficient')
    require(type(fresh['current_head']) is str and re.fullmatch('[0-9a-f]{40}',fresh['current_head']),'Explicit fresh main HEAD required, independently of archived replay HEAD')
    rr=rows(fresh['files']); require({z['path'] for z in rr}==NATIVE and len(rr)==13,'Exact13 fresh full native/inventory pins required')
    require(all(type(z.get('worktree_mode')) is int and 0<=z['worktree_mode']<=0o7777 for z in rr),'Explicit typed thirteen worktree permission modes required')
    for z in fresh['files']:keyset(z,{'path','bytes','sha256','worktree_mode'},'Exact fresh native reference')
    snap=load(A/'snapshot_manifest.json'); required(snap,{'head':HEAD,'base':ORIGINAL_BASE},'Original16/17 snapshot'); require(len(snap['files'])==16 and len(snap['changed_paths'])==17,'Original16/17 counts')
    raw=git_bytes('diff',ORIGINAL_BASE,HEAD); require(len(raw)==54344 and sha(raw)==snap['diff_sha256'] and raw==(C/'original_diff.patch').read_bytes(),'Entire original Git diff changed')
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
    require(type(before) is dict and type(before.get('items')) is list and len(before['items'])==180,'Complete retained180 inventory')
    require(all(type(z) is dict and type(z.get('number')) is int for z in before['items']),'Typed inventory identities')
    identities=[z['number'] for z in before['items']];require(len(set(identities))==180 and identities.count(43)==1,'Unique original selected PR43')
    require(type(before.get('completed_count')) is int and before['completed_count']==32 and sum(z.get('stage')=='complete' for z in before['items'])==32,'Actual32 prior primaries')
    required(remote,{'state':'MERGED','isDraft':False,'number':43,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual merged source-status remote')
    require(type(remote['mergeCommit']) is dict and set(remote['mergeCommit'])=={'oid'} and type(remote['mergeCommit']['oid']) is str and re.fullmatch('[0-9a-f]{40}',remote['mergeCommit']['oid']),'Exact actual merge oid')
    clock=utc_clock(finalized_utc,'Actual finalization');merged=utc_clock(remote['mergedAt'],'Actual mergedUTC');require(merged<=clock<=dt.datetime.now(dt.timezone.utc),'No reversed/future merge finalization')
    inv=copy.deepcopy(before);chosen=next(z for z in inv['items'] if z['number']==43);require(chosen.get('stage')!='complete','Selected not already complete')
    chosen.update(stage='complete',outcome='already_solved_accepted_partial',queue_status='already_solved',audited_head=HEAD,merge_commit=remote['mergeCommit']['oid'],merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts='0/5',new_substantive_attempts=0,cumulative_attempts='0/5',paper_or_new_doi_or_tracker=False)
    require(sum(z.get('stage')=='complete' for z in inv['items'])==33,'Exactly33 derived primary completions')
    inv.update(updated_at_utc=finalized_utc,last_checkpoint_utc=finalized_utc,completed_count=33,program_completion_estimate_percent=33/180*100,completion_estimate_percent=33/180*100,current_pr=44)
    return inv


def finalization(pins,pre):
    record=load(A/'integration_finalization.json');remote=load(A/'remote_merge_receipt.json')
    keyset(remote,{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Complete actual retained remote schema')
    require(type(record) is dict and 'utc' in record,'Actual retained finalization record required')
    expected={'schema':'pr43-actual-integration-finalization/v1','utc':record['utc'],**pins,'pr':43,'before_inventory_sha256':pre['inventory_before_sha256'],'remote_merge_receipt':pin(A/'remote_merge_receipt.json'),'merge_commit':remote['mergeCommit']['oid'],'merge_tree':git('show','-s','--format=%T',remote['mergeCommit']['oid']),'source_sha256':sha((HERE/'integrate_reviewed_partial.py').read_bytes())}
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
    return {'schema':'pr43-accepted-qualified-source-status-partial/v1','utc':final['utc'],**SCIENCE,**pins,'pr':43,'id':30004386,'problem_id':30004386,'problem_number':CODE,'queue_status':'already_solved','outcome':'already_solved_accepted_partial_merged','original_head':HEAD,'original_base':ORIGINAL_BASE,'merge_commit':final['merge_commit'],'merge_tree':final['merge_tree'],'merge_parents':[pre['main_before'],HEAD],'merged_at':remote['mergedAt'],'remote_state':'MERGED','remote_isDraft':False,'canonical_scientific_artifact_sha256':SCIENCE_SHA,'source_record_sha256':SOURCE_SHA,'original_ledger_sha256':LEDGER_SHA,'substantive_attempts_used':0,'substantive_attempt_limit':5,'native_historical_events_inferred':False,'historical_metadata_archival_only':True,'workflow_completion_estimate_percent':100,'full_resolution_by_project_completion_estimate_percent':0,'scientific_scope':load(HERE/'SCIENTIFIC_SCOPE.json')}


def accepted_invariants(o,pins,pre,audit=False):
    expected=expected_acceptance(pins,pre)
    if audit:
        expected.update(canonical_manifest_sha256=sha(regular(K,'MANIFEST.json').read_bytes()),canonical_manifest_entries=len(rows(load(K/'MANIFEST.json')['files'])))
    require(equal(o,expected),'Complete typed canonical/audit accepted receipt schema and derived values required; meaningful extensions prohibited')
    source(K)
    for n in ADMIN:
        expected_admin=load(C/n)
        expected_admin.update(**SCIENCE,**pins,id=30004386,current_context_path='CURRENT_CONTEXT_PRESENT.md',current_audit_scope_path='CURRENT_AUDIT_SCOPE_PRESENT.md',current_gate='accepted_qualified_partial',current_verdict=WHOLE_VERDICT,status='already_solved_accepted_source_status_merged',new_whole_current_gate=WHOLE_VERDICT,historical_verdict_transferred=False,merge_commit=o['merge_commit'],merge_tree=o['merge_tree'],merged_at=o['merged_at'])
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
        raw=regular(R,n).read_bytes(); out.append({'path':n,'bytes':len(raw),'sha256':sha(raw),'worktree_mode':stat.S_IMODE(regular(R,n).stat().st_mode),'head_sha256':sha(git_bytes('show','HEAD:'+n)),'head_entry':e,'index_entry':mode+' '+blob+' 0\t'+n})
    foreign_check({'foreign_logs':out}); return out


def foreign_check(pre):
    rr=pre['foreign_logs']; require(len(rr)==2 and {z['path'] for z in rr}==FOREIGN_LOGS,'No broad tracked exception')
    check(R,rr)
    for z in rr:
        keyset(z,{'path','bytes','sha256','worktree_mode','head_sha256','head_entry','index_entry'},'Complete exact foreign project log reference')
        require(type(z['worktree_mode']) is int and stat.S_IMODE(regular(R,z['path']).stat().st_mode)==z['worktree_mode'],'Foreign project log full permission bits changed')
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
    spec=importlib.util.spec_from_file_location('pr43_bound_native_mirror',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
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

def ledger_list(raw):
    require(type(raw) is bytes and (not raw or raw.endswith(b'\n')),'Exact complete JSONL bytes')
    return [parse(line) for line in raw.splitlines()]


def keyset(obj,keys,context):
    require(type(obj) is dict and set(obj)==set(keys),context+': unknown/missing critical fields prohibited')


def preflight_record(pins):
    o=load(A/'integration_preflight.json')
    keyset(o,set(pins)|{'schema','utc','main_before','pr','foreign_logs','whole_queue_before_sha256','selected_row_before','state_before_sha256','history_before_sha256','inventory_before_sha256','original_substantive_attempts','new_substantive_attempts','audit_turns','dated_frozen_preimage_not_rewritten'},'Complete original-head preflight')
    required(o,{'schema':'pr43-original-head-integration-preflight/v1',**pins,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'dated_frozen_preimage_not_rewritten':True},'Original-head preflight source and scope')
    fresh=load(R/o['fresh_preimage']);require(o['main_before']==fresh['current_head'],'Original preflight main differs from fresh inputs')
    rr={z['path']:z for z in fresh['files']}
    for field,path in [('whole_queue_before_sha256',Q.relative_to(R).as_posix()),('state_before_sha256','unsolved_math_prioritization/state.json'),('history_before_sha256','unsolved_math_prioritization/history.jsonl'),('inventory_before_sha256','draft_pr_publication_program_20260930/inventory.json')]:
        require(o[field]==rr[path]['sha256'],'Complete fresh preflight source binding differs')
    keyset(o['pr'],{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Complete preflight remote schema')
    required(o['pr'],{'number':43,'url':'https://github.com/AlecKriebel/Math/pull/43','state':'OPEN','isDraft':True,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main','mergeCommit':None,'mergedAt':None},'Literal original draft head')
    before=regular(A,'integration_queue_before.md').read_bytes()
    require(sha(before)==o['whole_queue_before_sha256'] and selected(before)==o['selected_row_before'],'Complete retained queue preimage differs')
    require(sha(regular(A,'integration_inventory_before.json').read_bytes())==o['inventory_before_sha256'],'Complete retained inventory preimage differs')
    require(utc_clock(o['utc'],'Preflight UTC')<=dt.datetime.now(dt.timezone.utc),'Future preflight timestamp')
    foreign_check(o)
    return o


def overlay_record(pins,frozen):
    o=load(A/'integration_check.json')
    keyset(o,set(pins)|{'schema','utc','canonical_overlay_files','whole_queue_after_sha256','automatic_merge_queue_preimage_sha256','original_substantive_attempts','new_substantive_attempts','audit_turns','remote_pending'},'Complete overlay schema')
    required(o,{'schema':'pr43-original-head-overlay/v1',**pins,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'remote_pending':True},'Complete overlay scope and pins')
    for z in o['canonical_overlay_files']:exact_reference(z)
    require({z['path'] for z in rows(o['canonical_overlay_files'])}==canonical_names(frozen),'Entire owned overlay closure differs')
    require(sha(regular(A,'integration_merge_queue_before.md').read_bytes())==o['automatic_merge_queue_preimage_sha256'],'Entire automatic/conflicted queue preimage differs')
    digest(o['whole_queue_after_sha256']);utc_clock(o['utc'],'Overlay UTC')
    return o


def prepush_record(pins):
    o=load(A/'integration_prepush.json')
    keyset(o,set(pins)|{'schema','utc','merge_commit','merge_tree','merge_parents','canonical_overlay_files','whole_queue_after_sha256','remote_before_push','actual_push_performed_by_helper'},'Complete prepush schema')
    required(o,{'schema':'pr43-original-head-prepush/v1',**pins,'actual_push_performed_by_helper':False},'Whole original-head prepush pins')
    utc_clock(o['utc'],'PrepushUTC');pre=preflight_record(pins)
    require(equal(o['merge_parents'],[pre['main_before'],HEAD]) and git('show','-s','--format=%P',o['merge_commit']).split()==o['merge_parents'],'Complete archived prepush parents must equal actual original-head merge')
    require(o['merge_tree']==git('show','-s','--format=%T',o['merge_commit']),'Complete actual archived prepush tree')
    overlay=overlay_record(pins,rows(load(C/'MANIFEST.json')['files']))
    require(equal(o['canonical_overlay_files'],overlay['canonical_overlay_files']) and o['whole_queue_after_sha256']==overlay['whole_queue_after_sha256'],'Entire prepush overlay and queue derivation')
    observed=o['remote_before_push'];keyset(observed,{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Entire actual archived prepush remote')
    expected={'number':43,'url':'https://github.com/AlecKriebel/Math/pull/43','state':'OPEN','isDraft':False,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main','mergeCommit':None,'mergedAt':None,'body':regular(A,'accepted_pr_body.md').read_text()}
    require(equal(observed,expected),'Complete typed actual original-head prepush remote/body')
    return o


def mirror_proposal(proposal,pins):
    previous=load(R/pins['previous_mirror']);expected=copy.deepcopy(previous)
    expected.update(created_at_utc=proposal.get('created_at_utc'),scope='Incremental present accepted primary PR43 source-status correction; original0/5, no new proof turn or historical reconstruction.')
    for n in ['inventory','queue']:expected[n]=binding(R/previous[n]['path'])
    expected['required_completed_prs']=sorted(previous['required_completed_prs']+[43])
    expected['entries'].append({'pr':43,'id':ID,'status':'already_solved','acceptance':binding(K/'acceptance.json'),'audit_acceptance':binding(A/'acceptance.json'),'remote':binding(A/'remote_merge_receipt.json'),'accepted_source':binding(K/'source_record.json'),'canonical_acceptance_text':binding(K/'ACCEPTANCE.md'),'canonical_manifest':binding(K/'MANIFEST.json'),'artifact':{**binding(K/'SOURCE_STATUS.md'),'acceptance_hash_field':'canonical_scientific_artifact_sha256'},'budget':{'used':0,'limit':5,'kind':'pr43_exact_original_empty_ledger','ledger':binding(K/'turns.jsonl')},'duplicates':[]})
    require(equal(proposal,expected),'Entire typed exact old proposal plus one source-status primary')
    require(utc_clock(proposal['created_at_utc'],'Actual proposalUTC')<=dt.datetime.now(dt.timezone.utc),'No future proposal clock')


def mirror_records(pins,pre,plan,intent,receipt,proposal):
    keyset(plan,{'bindings','created_at_utc','decisions','dry_run','duplicate_count','duplicate_decisions','history_after_sha256','history_append','history_append_bytes','limitations','preconditions','primary_count','proposal_spec','protected','schema','state_after','state_after_bytes','state_after_sha256','writes_authorized_to_live_repo'},'Known complete native plan schema')
    require(plan['schema']=='acceptance-mirror-plan/v2','Unknown critical native mirror plan schema')
    mirror_proposal(proposal,pins);require(equal(plan['proposal_spec'],proposal),'Entire native plan proposal differs')
    before_state=regular(A,'integration_state_before.json').read_bytes();before_history=regular(A,'integration_history_before.jsonl').read_bytes()
    require(equal(plan,rebuild_saved_mirror_plan(proposal,plan['created_at_utc'],before_state,before_history)),'Entire native plan must derive exactly from actual old bodies and same timestamp')
    expected={'schema':'pr43-present-acceptance-mirror/v1','status':'COMPLETED','utc':intent.get('utc'),**pins,'plan_sha256':sha(encode(plan)),'before':plan['preconditions'],'before_state_bytes':before_state.decode(),'before_history_bytes':before_history.decode(),'state_after_sha256':plan['state_after_sha256'],'history_after_sha256':plan['history_after_sha256'],'write_order':['history.jsonl','state.json'],'new_event':ID,'new_proof_turns':0,'lock_limitation':'Cooperative advisory lock; noncooperating writers remain outside protocol.','completed_utc':intent.get('completed_utc')}
    require(equal(intent,expected),'Entire typed completed native intent, source pins and exact old bytes required')
    clocks=[utc_clock(intent[n],'Actual native intent clock') for n in ['utc','completed_utc']]
    require(clocks==sorted(clocks) and clocks[-1]<=dt.datetime.now(dt.timezone.utc),'Native intent clock order/future')
    keyset(receipt,set(pins)|{'utc','status','validation','negative_ledger_controls','history_events_added','prior_state_entries_preserved','current_targets','consumed_substantive_turns','primary_acceptances','duplicate_count','new_duplicate_native_acceptance_added','new_proof_turns','state_sha256','history_sha256'},'Complete native mirror receipt')
    required(receipt,{'status':'COMPLETED',**pins,'negative_ledger_controls':['nonempty','whitespace_only','invented_JSONL','bool_used','wrong_used','wrong_limit'],'history_events_added':1,'prior_state_entries_preserved':33,'current_targets':34,'consumed_substantive_turns':41,'primary_acceptances':33,'duplicate_count':1,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,'state_sha256':plan['state_after_sha256'],'history_sha256':plan['history_after_sha256']},'Entire native receipt disposition')
    keyset(receipt['validation'],{'bindings_verified','preflight','remote_check','shared_files_changed','targets'},'Known complete native validation schema')
    required(receipt['validation'],{'preflight':'PASS','remote_check':'Pinned saved receipt verification; fresh network acceptance check remains root-owned.','shared_files_changed':0,'targets':34},'Native validation meaning')
    require(type(receipt['validation']['bindings_verified']) is int and receipt['validation']['bindings_verified']==len(plan['bindings']),'All original native plan bindings verified')
    require(clocks[-1]<=utc_clock(receipt['utc'],'Actual native receipt UTC')<=dt.datetime.now(dt.timezone.utc),'Native receipt clock order/future')


def rebuild_saved_mirror_plan(proposal,timestamp,old_state,old_history):
    m=mirror_module(proposal)
    overrides={str((R/'unsolved_math_prioritization/state.json').resolve()):old_state,str((R/'unsolved_math_prioritization/history.jsonl').resolve()):old_history}
    class ArchivedReadPath(type(Path())):
        def read_bytes(self):
            key=str(self.resolve())
            return overrides[key] if key in overrides else Path.read_bytes(self)
    actual_path=m.Path;m.Path=ArchivedReadPath
    try:return m.build_plan(R,proposal,timestamp)
    finally:m.Path=actual_path
