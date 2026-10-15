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
K = R / 'unsolved_math_prioritization/attempts/2912'
Q = R / 'unsolved_math_prioritization/QUEUE.md'
BASE = B / 'infrastructure/accepted_state_sync'
ID, CODE, PR = '2912', 'KP-4.36', 44
HEAD = 'c772dc5b851ec91da9d46d534577609e5d3ca389'
ORIGINAL_BASE = '01358d66fc67d1c462bddf31c0d4ee5b120e6737'
CURRENT_SHA = '169f2825a8f730735627bdc33a43366c05e317fdf7ec4df4cd96a31e37329eb0'
DEPS_SHA = '2c8d2ef1cd1846a0b82dce49b8c8891f6821ca129bd42ec20cf4fc45ae258c18'
SOURCE_SHA = '44162e54c0f08a328332fc98980ff7e3fa50c96b9dade7583a53c480baf5eb30'
LEDGER_SHA = 'aea558bd24ef7670c20543d79a09fa559afed88ca3871b178b48f6375507233a'
SCIENCE_SHA = '69a3ffb7b6c2ba3bf1a4df8d7d83960d66095db9d175d78cfe49e2324aac1a71'
MIRROR_SHA = 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
ADMIN = {'status.json', 'readiness.json', 'review/verdict.json'}
IMMUTABLE = {'review/submitted_verifier.py', 'review/independent_results.json', 'source_record.json', 'source_manifest.json', 'SOURCES.md', 'OBSTRUCTION.md', 'review/submitted_results.json', 'group_block_verification.json', 'turns.jsonl', 'verify_group_block.py', 'review/independent_checks.py', 'review/reviewed_obstruction.md'}
WHOLE_VERDICT = 'PASS_SCOPED_ACTUAL_WHOLE_CURRENT_STANDARD_PARTIAL_ONLY'
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
NATIVE = {'draft_pr_publication_program_20260930/inventory.json'} | {'unsolved_math_prioritization/' + n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
IGNORED_CACHE3 = {'unsolved_math_prioritization/cache/problems.json', 'unsolved_math_prioritization/cache/research_results.json', 'unsolved_math_prioritization/cache/catalog.sqlite'}
FOREIGN_LOGS = {'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/commands.tsv', 'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/full_transcript.log'}
SCIENCE = {'full_problem_solved': False, 'full_target_resolved_in_prior_published_literature': False, 'full_problem_solved_by_project': False, 'prior_publication_doi': None, 'partial_valid': True, 'novelty_claimed': False, 'priority_claimed': False, 'original_substantive_attempts': 2, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'verification_attempts_added': 0, 'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'paper_or_new_doi_or_tracker': False, 'human_referee_review_claimed': False}


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
        'pr44-acceptance-source-closure/v1':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'},
        'PR44_STRICT_CURRENT_PACKET_v1':{'schema','self_excluded','files_count','files','current_gate','status','full_problem_solved','novelty_claimed','original_substantive_attempts','new_substantive_attempts','audit_turns','full_permission_mode'},
        'pr44-final-root-two-member-closure/v1':{'schema','utc','self_excluded','files_count','files'},
        'pr44-accepted-strict-self-excluding-closure/v1':{'schema','utc','self_excluded','files_count','files','foreign_excluded_prefixes'},
    }
    require(type(obj) is dict and obj.get('schema') in known,'Unknown critical closure schema')
    keyset(obj,known[obj['schema']],'Exact recognized closure schema')
    if obj['schema']=='pr44-acceptance-source-closure/v1':
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
    require(p.resolve().is_relative_to(A.resolve()),'Evidence outside exact PR44 audit')
    return p.read_bytes()


def pin(p):
    raw=Path(p).read_bytes(); return {'path':Path(p).relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)}


def binding(p): return {k:v for k,v in pin(p).items() if k!='bytes'}


def write(p,raw,exclusive=False):
    p=Path(p); require(p.parent.is_dir() and not p.is_symlink() and all(not d.is_symlink() for d in p.parents),'Unsafe output or symlink ancestor')
    if exclusive: require(not p.exists(),'Existing output: inspect before retry')
    tmp=p.with_name(p.name+'.pr44-tmp')
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
    required(o,{'number':44,'url':'https://github.com/AlecKriebel/Math/pull/44','headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual remote')
    return o


def original_native(base):
    snapshot=load(A/'snapshot_manifest_v2.json')
    require(snapshot['schema']=='pr44-root-readonly-original-snapshot/v1' and len(snapshot['files'])==18,'Complete original18 required')
    exact(base,{z['path'] for z in rows(snapshot['files'])})
    for z in rows(snapshot['files']):
        raw=regular(base,z['path']).read_bytes()
        require(raw==regular(A/'source_snapshot',z['path']).read_bytes() and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Original18 bytes differ')


def source(base):
    original_native(base/'original_archive')
    for n in IMMUTABLE:require(regular(base,n).read_bytes()==regular(A/'source_snapshot',n).read_bytes(),'Immutable science/helper/result/source/ledger changed')
    require(sha(regular(base,'OBSTRUCTION.md').read_bytes())==SCIENCE_SHA and sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Science/source anchors changed')
    raw=regular(base,'turns.jsonl').read_bytes();require(raw==regular(A/'source_snapshot','turns.jsonl').read_bytes() and sha(raw)==LEDGER_SHA,'Exact original two-turn ledger required')
    entries=ledger_list(raw);require(len(entries)==2 and all(type(z.get('turn')) is int for z in entries) and [z['turn'] for z in entries]==[1,2] and all(z['outcome']=='stalled' for z in entries),'Original2/5 stalled routes only')
    require(sha(regular(base,'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes())==load(HERE/'SCIENTIFIC_SCOPE.json')['global_qualification_sha256'],'Global category/source/realization qualification exact')


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
    require(p.parent==A and p.name!='DRAFT_ROOT_IMMUTABLE_BINDINGS.json','Genuine adjacent ROOT completed bindings required')
    require(sha(p.read_bytes())==digest(pin_value),'Actual ROOT immutable-bindings SHA differs')
    o=parse(p.read_bytes());draft=load(HERE/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
    reference_keys=['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection']
    for key in reference_keys:exact_reference(o[key]);check(R,[o[key]])
    draft.update(status='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR43_EVIDENCE',created_utc=o['created_utc'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR43_predecessor_read_completed=True)
    for key in reference_keys:draft[key]=o[key]
    require(equal(o,draft),'Complete exact typed ROOT binding keys and values required')
    require(utc_clock(o['created_utc'],'ROOT binding creation')<=dt.datetime.now(dt.timezone.utc),'No future ROOT approval')
    inputs=load(HERE/'INPUT_BINDINGS.json')
    for key in ['previous_mirror','previous_post','previous_root_post']:
        require(equal(o[key],inputs[key]),'Actual43 predecessor entire immutable binding differs')
    previous=load(R/o['previous_mirror']['path']);post=load(R/o['previous_post']['path']);rootpost=load(R/o['previous_root_post']['path'])
    require(type(previous['entries']) is list and len(previous['entries'])==33 and all(type(z['pr']) is int for z in previous['entries']),'Exact33 original primary entries')
    numbers=[z['pr'] for z in previous['entries']]
    require(len(set(numbers))==33 and 43 in numbers and 44 not in numbers and equal(sorted(numbers),previous['required_completed_prs']),'Actual43 prior identities')
    required(post,{'status':'PASS','pr':43,'targets':34,'consumed_substantive_turns':41,'primary_acceptances':33,'program_completed_count':33,'merge_commit':'c60255489a342fae02c0acf3d1026255b47be3d1','merge_tree':'fdc2bb213905051a430d24e13afb20e54fa9106a','fresh_native_mirror_noop':True,'one_present_primary_event':True,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,'full_problem_solved':False,'paper_or_new_doi_or_tracker':False},'Actual43 completed predecessor')
    required(rootpost,{'schema':'pr43-root-complete-actual-post-inspection/v1','status':'PASS','completed_primary_prs':33,'all33_prior_states_and_full_history_prefix_preserved':True,'current13_match_exact_allowed_acceptance_changes':True,'canonical357_plus_manifest_fullbytes_modes':True,'merge355_overlay_plus_queue_Git_bodies_and_parents':True,'entire_current_inventory_reconstructed':True,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False},'Actual43 ROOT entire-post reading')
    require(equal(rootpost['entire_post'],post),'Entire actual43 predecessor post equals completed ROOT read')
    require(utc_clock(rootpost['utc'],'Actual43 ROOT post')<=utc_clock(o['created_utc'],'ROOT44 approval'),'ROOT44 approval cannot precede predecessor actual post')
    expected_operator=regular(HERE,'capture_root_final_operation.py').read_bytes()
    require(o['root_capture_operator']['path']==(A/'capture_root_final_operation.py').relative_to(R).as_posix() and bound(o['root_capture_operator'])==expected_operator,'Literal personally reviewed ROOT operator must equal prepared complete source')
    sm=regular(R,o['acceptance_source_manifest']['path']);sv=regular(R,o['acceptance_source_verdict']['path']);sr=regular(R,o['root_source_inspection']['path'])
    require(sm.parent==sv.parent and sm.parent.parent==A and sm.parent not in {C,HERE} and sm.name=='SELF_MANIFEST.json' and sv.name=='VERDICT.json','New distinct source-adversary literal closure and verdict required')
    require(sr.parent==A and sr.name=='ROOT_SOURCE_ACCEPTANCE_REVIEW.json','Literal genuine ROOT source inspection required')
    own=load(sm);rr=rows(own['files']);require(own['self_excluded']==['SELF_MANIFEST.json'] and type(own['files_count']) is int and own['files_count']==len(rr),'Exact source-adversary self-only closure')
    check(sm.parent,rr);exact(sm.parent,{z['path'] for z in rr}|{'SELF_MANIFEST.json'});frozen_files(sm.parent,rr,'SELF_MANIFEST.json')
    verdict=load(sv)
    required(verdict,{'schema':'pr44-acceptance-source-adversary-verdict/v1','verdict':'PASS_SOURCE_ONLY_SCOPED','preparation_manifest_sha256':sha((HERE/'PREPARATION_MANIFEST.json').read_bytes()),'mandatory_corrections':[],'production_imported_compiled_executed':False,'future_acceptance_approved':False},'New actual independent source gate')
    root=load(sr)
    required(root,{'schema':'pr44-root-complete-acceptance-source-inspection/v1','status':'PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION','all_prepared_source_and_controls_fully_read':True,'exact_preparation_closure_and_full_modes_checked':True,'all_individual_source_adversary_inputs_checked':True,'all_complete_actual_captures_checked':True,'complete_VERDICT_object':verdict,'preparation_manifest_sha256':sha((HERE/'PREPARATION_MANIFEST.json').read_bytes()),'acceptance_source_manifest':o['acceptance_source_manifest'],'acceptance_source_verdict':o['acceptance_source_verdict'],'mandatory_corrections':[],'future_execution_approved':False},'Genuine ROOT complete source/adversary reading')
    require(utc_clock(root['utc'],'ROOT source read')<=utc_clock(o['created_utc'],'Completed approval'),'Source read after approval prohibited')
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
    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,430,frozen=True)
    deps=load(C/'CURRENT_DEPENDENCIES.json')
    keyset(deps,{'anchor_repository_relative','resolution','files','foreign_primary_and_derivative_members_individually_hash_bound_not_copied','current_native13','current_main_head'},'Exact portable dependency schema')
    required(deps,{'anchor_repository_relative':A.relative_to(R).as_posix(),'resolution':'repository_root / anchor_repository_relative / files.path; never scratch','foreign_primary_and_derivative_members_individually_hash_bound_not_copied':True,'current_main_head':'2b9d0234b1396fa84c4b34055b5e8e14c873588b'},'Exact dated dependencies')
    require(sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())==DEPS_SHA and len(rows(deps['files']))==369,'Complete369 dependencies');check(A,deps['files']);source(C)
    for n in ADMIN:require(equal(load(C/n),load(HERE/'EXPECTED_CURRENT_ADMIN.json')),'Entire dated pending admin differs')
    w=A/'whole_current_source_first_family';wm=exact_reference(approved['whole_manifest'])
    require(equal(wm,inputs['closed_whole_manifest']),'Exact actual whole manifest')
    whole=parse(bound(wm));keyset(whole,{'schema','utc','operator_pid','files_count','files','directories','self_excluded','full_permission_mode','foreign_inputs_manifest','foreign_primary_or_raw_cache_bodies_copied','whole_native4_Git_stdout_is_procedural_actual_evidence','candidate_manifest_sha256','original_substantive_attempts','new_substantive_attempts','audit_turns','full_problem_solved','future_ROOT_acceptance_or_reconciliation_approved'},'Exact actual whole closure schema')
    required(whole,{'schema':'pr44-whole-current-source-first-self-only-closure/v1','files_count':96,'self_excluded':['SELF_MANIFEST.json'],'full_permission_mode':'0444','candidate_manifest_sha256':CURRENT_SHA,'foreign_primary_or_raw_cache_bodies_copied':False,'future_ROOT_acceptance_or_reconciliation_approved':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False},'Actually closed whole family')
    authored=rows(whole['files']);require(len(authored)==96,'Exact96 whole members');check(w,authored);exact(w,{z['path'] for z in authored}|{'SELF_MANIFEST.json'});frozen_files(w,authored,'SELF_MANIFEST.json')
    require(equal(sorted(topology(w)[1]),whole['directories']),'Entire required whole directory topology')
    foreign_inventory=load(w/whole['foreign_inputs_manifest']);foreign=rows(foreign_inventory['files'])
    required(foreign_inventory,{'schema':'pr44-source-first-individual-foreign-inputs/v1','resolution':'repository_root / files.path','foreign_bodies_copied':False,'git_stdout_firstparty_native4_and_query_metadata_are_procedural_evidence':True},'Individual foreign scope')
    require(len(foreign)==964,'Exact964 individual foreign identities')
    dated_head='2b9d0234b1396fa84c4b34055b5e8e14c873588b';historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    dated=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');require(dated['current_head']==dated_head,'Dated freeze authority stays fixed');dated_native={z['path']:z for z in rows(dated['files'])};require(set(dated_native)==NATIVE,'Exact frozen native13')
    historical_checked=set();names=set()
    for z in foreign:
        keyset(z,{'path','bytes','sha256','excluded_from_family_authorship'},'Exact individual foreign reference');require(z['excluded_from_family_authorship'] is True,'Foreign exclusion true required');relative(z['path']);names.add(z['path'])
        if z['path'] in historical:
            require(z['bytes']==dated_native[z['path']]['bytes'] and z['sha256']==dated_native[z['path']]['sha256'],'Dated foreign row differs')
            entries=git_bytes('ls-tree','-z',dated_head,'--',z['path']).decode().split('\0');require(len(entries)==2 and entries[-1]=='','One historical Git blob');fields,literal=entries[0].split('\t');mode,kind,blob=fields.split();require(mode=='100644' and kind=='blob' and literal==z['path'],'Historical exact Git path/mode')
            raw=git_bytes('show',dated_head+':'+z['path']);historical_checked.add(z['path'])
        else:raw=regular(R,z['path']).read_bytes()
        require(len(raw)==z['bytes'] and sha(raw)==digest(z['sha256']),'Entire individual input changed')
    require(len(names)==964 and (NATIVE-historical)<=names and not historical.intersection(names),'Exact964 foreign identities and nine stable native inputs')
    for n in sorted(historical):
        z=dated_native[n]
        entries=git_bytes('ls-tree','-z',dated_head,'--',n).decode().split('\0')
        require(len(entries)==2 and entries[-1]=='','Exactly one independent frozen Git blob')
        fields,literal=entries[0].split('\t');mode,kind,blob=fields.split()
        require(mode=='100644' and kind=='blob' and literal==n,'Frozen native4 exact immutable Git modes')
        raw=git_bytes('show',dated_head+':'+n)
        require(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Entire independent frozen native4 body differs')
        historical_checked.add(n)
    require(historical_checked==historical,'All four independently rechecked frozen native bodies')
    verdict=parse(bound(inputs['closed_whole_result']));require(equal(verdict,load(HERE/'EXPECTED_WHOLE_VERDICT.json')),'Entire actual typed whole verdict')
    required(verdict,{'verdict':WHOLE_VERDICT,'candidate_manifest_sha256':CURRENT_SHA,'mandatory_mathematical_corrections':[],'mandatory_source_scope_corrections':[],'mandatory_current_contract_corrections':[],'full_problem_solved':False,'novelty_claimed':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'exact_remaining_gaps':load(HERE/'SCIENTIFIC_SCOPE.json')['exact_remaining_gaps']},'Scoped UNSOLVED mathematical gate')
    bound(inputs['closed_whole_report'])
    rootref=exact_reference(approved['root_whole_inspection']);require(equal(rootref,inputs['closed_root_whole_inspection']),'Genuine ROOT whole read pin')
    root=parse(bound(rootref));require(equal(root,load(HERE/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and equal(root['complete_VERDICT_object'],verdict),'Entire exact ROOT44 whole read')
    required(root,{'schema':'pr44-root-complete-closed-whole-inspection/v1','status':'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION','candidate_manifest_sha256':CURRENT_SHA,'closed_whole_manifest_sha256':wm['sha256'],'first_party_members':96,'individually_bound_foreign_inputs':964,'personal_report_and_verdict_fully_read':True,'all_first_party_whole_bytes_and_modes_checked':True,'all_foreign_individual_whole_bytes_checked':True,'exact_self_only_recursive_closure_checked':True,'future_execution_approved':False,'mandatory_defects':[],'mandatory_corrections':[],'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved_by_project':False,'full_target_resolved_in_prior_published_literature':False,'dated_four_native_source_head':dated_head},'ROOT44 complete whole read flags and explicit source limits')
    require(root.get('direct_four_independent_ROOT_Git_checks_completed') is True and type(root.get('actual_direct_four_operator_pid')) is int and root['actual_direct_four_operator_pid']>0,'Genuine direct ROOT native4 operation')
    commands=root['complete_dated_git_captures'];require(type(commands) is list and len(commands)==8,'Exact eight genuine direct ROOT Git captures')
    expected=[]
    for n in sorted(historical):expected.extend([['git','ls-tree',dated_head,'--',n],['git','show',dated_head+':'+n]])
    require(equal([z['argv'] for z in commands],expected),'Exact entire direct ROOT native4 argv sequence')
    for i,z in enumerate(commands):
        required(z,{'cwd':str(R),'operator_pid':root['actual_direct_four_operator_pid'],'stdin_supplied':False,'exit_code':0,'actual_execution':True,'completed':True},'Genuine complete direct Git query')
        require(type(z['pid']) is int and z['pid']>0 and utc_clock(z['started_utc'],'Git start')<=utc_clock(z['finished_utc'],'Git finish')<=utc_clock(root['created_utc'],'Root read completion'),'Actual Git PID/time')
        for channel in ['stdout','stderr']:exact_reference(z[channel]);check(R,[z[channel]])
        require(regular(R,z['stderr']['path']).read_bytes()==b'','Complete direct Git stderr')
        n=sorted(historical)[i//2];raw=regular(R,z['stdout']['path']).read_bytes()
        if i%2:
            require(len(raw)==dated_native[n]['bytes'] and sha(raw)==dated_native[n]['sha256'],'Entire direct show stdout equals frozen native body')
        else:
            require(raw.endswith(b'\n') and raw.count(b'\n')==1,'One literal direct ls-tree line')
            fields,literal=raw.decode().rstrip('\n').split('\t');mode,kind,blob=fields.split()
            require(mode=='100644' and kind=='blob' and literal==n,'Exact direct100644 path/mode')
    require(utc_clock(root['created_utc'],'ROOT whole inspection')<=utc_clock(approved['created_utc'],'ROOT acceptance approval'),'Completed whole inspection must precede ROOT approval')
    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json');require(ledger['reading_completed'] is True and card['reading_completed'] is True and len(ledger['root_flags'])==9 and equal(ledger['root_flags'],card['root_flags']) and all(v is True for v in ledger['root_flags'].values()),'Nine distinct actual ROOT source/math flags')
    refs += [pin(C/'MANIFEST.json'),pin(C/'CURRENT_DEPENDENCIES.json'),wm,inputs['closed_whole_result'],inputs['closed_whole_report'],rootref,pin(rp)]
    refs += [approved[n] for n in ['previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection','root_capture_operator']]
    out={}
    for z in refs:
        require(z['path'] not in out or equal(out[z['path']],z),'Conflicting immutable identity');out[z['path']]=z
    return frozen,sorted(out.values(),key=lambda z:z['path'])


def plan_scope(o,prep,root_bindings,root_bindings_sha256):
    _,refs=basis(root_bindings,root_bindings_sha256)
    bindings,_=root_binding_input(root_bindings,root_bindings_sha256)
    draft=load(HERE/'DRAFT_FINAL_PLAN.json')
    draft.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=prep,root_bindings=root_bindings,root_bindings_sha256=root_bindings_sha256,whole_manifest_sha256=bindings['whole_manifest']['sha256'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR43_predecessor_read_completed=True,immutable_evidence_references=refs)
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
    required(receipt,{'schema':'pr44-actual-final-reconciliation/v1','status':'PASS','actual_root_reconciliation':True,'pr':44,'problem_id':2912,'preparation_manifest_sha256':a.preparation_manifest_sha256,'entire_scope':scope,'bindings_before':refs,'bindings_after':refs,'root_reviewed_plan':pin(ps['final_plan']),'reconciliation_source':pin(HERE/'seal_final_evidence.py'),'science_helpers_executed':False,'new_substantive_attempts':0,'audit_turns':0,'shared_mutations':False},'Actual final reconciliation')
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
    authority,_=root_binding_input(a.root_bindings,a.root_bindings_sha256)
    require(equal(pin(ps['previous_mirror']),authority['previous_mirror']) and equal(pin(ps['previous_post']),authority['previous_post']),'Entire actual43 predecessor references')
    fresh=load(ps['fresh_preimage']); required(fresh,{'approved_by_root':True},'Fresh actual native preimage')
    keyset(fresh,{'schema','approved_by_root','created_utc','reason_date_utc','reason','current_head','files'},'Exact current ROOT fresh input schema')
    require(fresh['schema']=='pr44-root-fresh-acceptance-input-preimages/v1','Unknown fresh authority schema')
    created=utc_clock(fresh['created_utc'],'Actual root fresh preimage creation')
    require(created<=dt.datetime.now(dt.timezone.utc),'Fresh root preimage creation clock is in the future')
    require(type(fresh['reason_date_utc']) is str and fresh['reason_date_utc']==created.date().isoformat(),'Root rebase reason date must match the actual UTC creation date')
    require(type(fresh['reason']) is str and fresh['reason']==fresh['reason'].strip() and len(fresh['reason'])>=40 and len(fresh['reason'].split())>=6,'Substantive root-reviewed rebase reason required; a token such as yes is insufficient')
    require(type(fresh['current_head']) is str and re.fullmatch('[0-9a-f]{40}',fresh['current_head']),'Explicit fresh main HEAD required, independently of archived replay HEAD')
    rr=rows(fresh['files']); require({z['path'] for z in rr}==NATIVE and len(rr)==13,'Exact13 fresh full native/inventory pins required')
    require(all(type(z.get('worktree_mode')) is int and 0<=z['worktree_mode']<=0o7777 for z in rr),'Explicit typed thirteen worktree permission modes required')
    for z in fresh['files']:keyset(z,{'path','bytes','sha256','worktree_mode'},'Exact fresh native reference')
    snap=load(A/'snapshot_manifest_v2.json'); required(snap,{'head':HEAD,'base':ORIGINAL_BASE},'Original18/19 snapshot'); require(len(snap['files'])==18 and len(snap['changed_paths'])==19,'Original18/19 counts')
    raw=git_bytes('diff',ORIGINAL_BASE,HEAD); require(len(raw)==75046 and sha(raw)==snap['diff_sha256'] and raw==(C/'original_diff.patch').read_bytes(),'Entire original Git diff changed')
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
    identities=[z['number'] for z in before['items']];require(len(set(identities))==180 and identities.count(44)==1,'Unique original selected PR44')
    require(type(before.get('completed_count')) is int and before['completed_count']==33 and sum(z.get('stage')=='complete' for z in before['items'])==33,'Actual33 prior primaries')
    required(remote,{'state':'MERGED','isDraft':False,'number':44,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual merged standard-partial remote')
    require(type(remote['mergeCommit']) is dict and set(remote['mergeCommit'])=={'oid'} and type(remote['mergeCommit']['oid']) is str and re.fullmatch('[0-9a-f]{40}',remote['mergeCommit']['oid']),'Exact actual merge oid')
    clock=utc_clock(finalized_utc,'Actual finalization');merged=utc_clock(remote['mergedAt'],'Actual mergedUTC');require(merged<=clock<=dt.datetime.now(dt.timezone.utc),'No reversed/future merge finalization')
    inv=copy.deepcopy(before);chosen=next(z for z in inv['items'] if z['number']==44);require(chosen.get('stage')!='complete','Selected not already complete')
    chosen.update(stage='complete',outcome='unsolved_accepted_partial',queue_status='unsolved',audited_head=HEAD,merge_commit=remote['mergeCommit']['oid'],merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts='2/5',new_substantive_attempts=0,cumulative_attempts='2/5',paper_or_new_doi_or_tracker=False)
    require(sum(z.get('stage')=='complete' for z in inv['items'])==34,'Exactly34 derived primary completions')
    inv.update(updated_at_utc=finalized_utc,last_checkpoint_utc=finalized_utc,completed_count=34,program_completion_estimate_percent=34/180*100,completion_estimate_percent=34/180*100,current_pr=45)
    return inv


def finalization(pins,pre):
    record=load(A/'integration_finalization.json');remote=load(A/'remote_merge_receipt.json')
    keyset(remote,{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Complete actual retained remote schema')
    require(type(record) is dict and 'utc' in record,'Actual retained finalization record required')
    expected={'schema':'pr44-actual-integration-finalization/v1','utc':record['utc'],**pins,'pr':44,'before_inventory_sha256':pre['inventory_before_sha256'],'remote_merge_receipt':pin(A/'remote_merge_receipt.json'),'merge_commit':remote['mergeCommit']['oid'],'merge_tree':git('show','-s','--format=%T',remote['mergeCommit']['oid']),'source_sha256':sha((HERE/'integrate_reviewed_partial.py').read_bytes())}
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
    return {'schema':'pr44-accepted-qualified-standard-partial/v1','utc':final['utc'],**SCIENCE,**pins,'pr':44,'id':2912,'problem_id':2912,'problem_number':CODE,'queue_status':'unsolved','outcome':'unsolved_accepted_partial_merged','original_head':HEAD,'original_base':ORIGINAL_BASE,'merge_commit':final['merge_commit'],'merge_tree':final['merge_tree'],'merge_parents':[pre['main_before'],HEAD],'merged_at':remote['mergedAt'],'remote_state':'MERGED','remote_isDraft':False,'canonical_scientific_artifact_sha256':SCIENCE_SHA,'source_record_sha256':SOURCE_SHA,'original_ledger_sha256':LEDGER_SHA,'substantive_attempts_used':2,'substantive_attempt_limit':5,'native_historical_events_inferred':False,'historical_metadata_archival_only':True,'workflow_completion_estimate_percent':100,'full_resolution_by_project_completion_estimate_percent':0,'scientific_scope':load(HERE/'SCIENTIFIC_SCOPE.json')}


def accepted_invariants(o,pins,pre,audit=False):
    expected=expected_acceptance(pins,pre)
    if audit:
        expected.update(canonical_manifest_sha256=sha(regular(K,'MANIFEST.json').read_bytes()),canonical_manifest_entries=len(rows(load(K/'MANIFEST.json')['files'])))
    require(equal(o,expected),'Complete typed canonical/audit accepted receipt schema and derived values required; meaningful extensions prohibited')
    source(K)
    for n in ADMIN:
        expected_admin=load(C/n)
        expected_admin.update(**SCIENCE,**pins,id=2912,current_context_path='CURRENT_CONTEXT_PRESENT.md',current_audit_scope_path='CURRENT_AUDIT_SCOPE_PRESENT.md',current_gate='accepted_qualified_partial',current_verdict=WHOLE_VERDICT,status='unsolved_accepted_standard_partial_merged',new_whole_current_gate=WHOLE_VERDICT,historical_verdict_transferred=False,merge_commit=o['merge_commit'],merge_tree=o['merge_tree'],merged_at=o['merged_at'])
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
    spec=importlib.util.spec_from_file_location('pr44_bound_native_mirror',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
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
    required(o,{'schema':'pr44-original-head-integration-preflight/v1',**pins,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'dated_frozen_preimage_not_rewritten':True},'Original-head preflight source and scope')
    fresh=load(R/o['fresh_preimage']);require(o['main_before']==fresh['current_head'],'Original preflight main differs from fresh inputs')
    rr={z['path']:z for z in fresh['files']}
    for field,path in [('whole_queue_before_sha256',Q.relative_to(R).as_posix()),('state_before_sha256','unsolved_math_prioritization/state.json'),('history_before_sha256','unsolved_math_prioritization/history.jsonl'),('inventory_before_sha256','draft_pr_publication_program_20260930/inventory.json')]:
        require(o[field]==rr[path]['sha256'],'Complete fresh preflight source binding differs')
    keyset(o['pr'],{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Complete preflight remote schema')
    required(o['pr'],{'number':44,'url':'https://github.com/AlecKriebel/Math/pull/44','state':'OPEN','isDraft':True,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main','mergeCommit':None,'mergedAt':None},'Literal original draft head')
    before=regular(A,'integration_queue_before.md').read_bytes()
    require(sha(before)==o['whole_queue_before_sha256'] and selected(before)==o['selected_row_before'],'Complete retained queue preimage differs')
    require(sha(regular(A,'integration_inventory_before.json').read_bytes())==o['inventory_before_sha256'],'Complete retained inventory preimage differs')
    require(utc_clock(o['utc'],'Preflight UTC')<=dt.datetime.now(dt.timezone.utc),'Future preflight timestamp')
    foreign_check(o)
    return o


def overlay_record(pins,frozen):
    o=load(A/'integration_check.json')
    keyset(o,set(pins)|{'schema','utc','canonical_overlay_files','whole_queue_after_sha256','automatic_merge_queue_preimage_sha256','original_substantive_attempts','new_substantive_attempts','audit_turns','remote_pending'},'Complete overlay schema')
    required(o,{'schema':'pr44-original-head-overlay/v1',**pins,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'remote_pending':True},'Complete overlay scope and pins')
    for z in o['canonical_overlay_files']:exact_reference(z)
    require({z['path'] for z in rows(o['canonical_overlay_files'])}==canonical_names(frozen),'Entire owned overlay closure differs')
    require(sha(regular(A,'integration_merge_queue_before.md').read_bytes())==o['automatic_merge_queue_preimage_sha256'],'Entire automatic/conflicted queue preimage differs')
    digest(o['whole_queue_after_sha256']);utc_clock(o['utc'],'Overlay UTC')
    return o


def prepush_record(pins):
    o=load(A/'integration_prepush.json')
    keyset(o,set(pins)|{'schema','utc','merge_commit','merge_tree','merge_parents','canonical_overlay_files','whole_queue_after_sha256','remote_before_push','actual_push_performed_by_helper'},'Complete prepush schema')
    required(o,{'schema':'pr44-original-head-prepush/v1',**pins,'actual_push_performed_by_helper':False},'Whole original-head prepush pins')
    utc_clock(o['utc'],'PrepushUTC');pre=preflight_record(pins)
    require(equal(o['merge_parents'],[pre['main_before'],HEAD]) and git('show','-s','--format=%P',o['merge_commit']).split()==o['merge_parents'],'Complete archived prepush parents must equal actual original-head merge')
    require(o['merge_tree']==git('show','-s','--format=%T',o['merge_commit']),'Complete actual archived prepush tree')
    overlay=overlay_record(pins,rows(load(C/'MANIFEST.json')['files']))
    require(equal(o['canonical_overlay_files'],overlay['canonical_overlay_files']) and o['whole_queue_after_sha256']==overlay['whole_queue_after_sha256'],'Entire prepush overlay and queue derivation')
    observed=o['remote_before_push'];keyset(observed,{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Entire actual archived prepush remote')
    expected={'number':44,'url':'https://github.com/AlecKriebel/Math/pull/44','state':'OPEN','isDraft':False,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main','mergeCommit':None,'mergedAt':None,'body':regular(A,'accepted_pr_body.md').read_text()}
    require(equal(observed,expected),'Complete typed actual original-head prepush remote/body')
    return o


def mirror_proposal(proposal,pins):
    previous=load(R/pins['previous_mirror']);expected=copy.deepcopy(previous)
    expected.update(created_at_utc=proposal.get('created_at_utc'),scope='Incremental present accepted primary PR44 standard partial; original2/5, no new proof turn or historical reconstruction.')
    for n in ['inventory','queue']:expected[n]=binding(R/previous[n]['path'])
    expected['required_completed_prs']=sorted(previous['required_completed_prs']+[44])
    expected['entries'].append({'pr':44,'id':ID,'status':'unsolved','acceptance':binding(K/'acceptance.json'),'audit_acceptance':binding(A/'acceptance.json'),'remote':binding(A/'remote_merge_receipt.json'),'accepted_source':binding(K/'source_record.json'),'canonical_acceptance_text':binding(K/'ACCEPTANCE.md'),'canonical_manifest':binding(K/'MANIFEST.json'),'artifact':{**binding(K/'OBSTRUCTION.md'),'acceptance_hash_field':'canonical_scientific_artifact_sha256'},'budget':{'used':2,'limit':5,'kind':'pr44_exact_original_two_turn_JSONL','ledger':binding(K/'turns.jsonl')},'duplicates':[]})
    require(equal(proposal,expected),'Entire typed exact old proposal plus one standard-partial primary')
    require(utc_clock(proposal['created_at_utc'],'Actual proposalUTC')<=dt.datetime.now(dt.timezone.utc),'No future proposal clock')


def mirror_records(pins,pre,plan,intent,receipt,proposal):
    keyset(plan,{'bindings','created_at_utc','decisions','dry_run','duplicate_count','duplicate_decisions','history_after_sha256','history_append','history_append_bytes','limitations','preconditions','primary_count','proposal_spec','protected','schema','state_after','state_after_bytes','state_after_sha256','writes_authorized_to_live_repo'},'Known complete native plan schema')
    require(plan['schema']=='acceptance-mirror-plan/v2','Unknown critical native mirror plan schema')
    mirror_proposal(proposal,pins);require(equal(plan['proposal_spec'],proposal),'Entire native plan proposal differs')
    before_state=regular(A,'integration_state_before.json').read_bytes();before_history=regular(A,'integration_history_before.jsonl').read_bytes()
    require(equal(plan,rebuild_saved_mirror_plan(proposal,plan['created_at_utc'],before_state,before_history)),'Entire native plan must derive exactly from actual old bodies and same timestamp')
    expected={'schema':'pr44-present-acceptance-mirror/v1','status':'COMPLETED','utc':intent.get('utc'),**pins,'plan_sha256':sha(encode(plan)),'before':plan['preconditions'],'before_state_bytes':before_state.decode(),'before_history_bytes':before_history.decode(),'state_after_sha256':plan['state_after_sha256'],'history_after_sha256':plan['history_after_sha256'],'write_order':['history.jsonl','state.json'],'new_event':ID,'new_proof_turns':0,'lock_limitation':'Cooperative advisory lock; noncooperating writers remain outside protocol.','completed_utc':intent.get('completed_utc')}
    require(equal(intent,expected),'Entire typed completed native intent, source pins and exact old bytes required')
    clocks=[utc_clock(intent[n],'Actual native intent clock') for n in ['utc','completed_utc']]
    require(clocks==sorted(clocks) and clocks[-1]<=dt.datetime.now(dt.timezone.utc),'Native intent clock order/future')
    keyset(receipt,set(pins)|{'utc','status','validation','negative_ledger_controls','history_events_added','prior_state_entries_preserved','current_targets','consumed_substantive_turns','primary_acceptances','duplicate_count','new_duplicate_native_acceptance_added','new_proof_turns','state_sha256','history_sha256'},'Complete native mirror receipt')
    required(receipt,{'status':'COMPLETED',**pins,'negative_ledger_controls':['empty','whitespace_only','invented_JSONL','bool_used','wrong_used','wrong_limit'],'history_events_added':1,'prior_state_entries_preserved':34,'current_targets':35,'consumed_substantive_turns':43,'primary_acceptances':34,'duplicate_count':1,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,'state_sha256':plan['state_after_sha256'],'history_sha256':plan['history_after_sha256']},'Entire native receipt disposition')
    keyset(receipt['validation'],{'bindings_verified','preflight','remote_check','shared_files_changed','targets'},'Known complete native validation schema')
    required(receipt['validation'],{'preflight':'PASS','remote_check':'Pinned saved receipt verification; fresh network acceptance check remains root-owned.','shared_files_changed':0,'targets':35},'Native validation meaning')
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
