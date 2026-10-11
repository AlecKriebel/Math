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
K = R / 'unsolved_math_prioritization/attempts/30000703'
Q = R / 'unsolved_math_prioritization/QUEUE.md'
BASE = B / 'infrastructure/accepted_state_sync'
ID, CODE, PR = '30000703', 'OWR-1460-009', 49
HEAD = '036a5ed59bee5ed79f08349290481584610f1456'
ORIGINAL_BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
GITHUB_BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
CURRENT_SHA = '8ca8820e1e1493391224ea8f93dde859bd9b3f6316c41763e86433dc85a1fa47'
DEPS_SHA = 'b354740dece80bb27991bcf6972f846715bae4f862592666b0153ba03cd47dc3'
SOURCE_SHA = 'ffcf36d030968377d092098f279f575397b8b15b7bb812bf7fd2f525e55a1d22'
LEDGER_SHA = '23426c68094e4cb553fcd260468b5a106efc4df6092b10eca730e0f440e9eeaf'
SCIENCE_SHA = '7690840787fd9be528beb649dc6db4b77bc637867720765812ec4cb31d5a73ba'
MIRROR_SHA = 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
ADMIN = {'status.json','readiness.json','review/verdict.json','review/review_summary.json'}
IMMUTABLE = {'review/independent_checks.py', 'source_checksums.json', 'SOURCE_STATUS.md', 'source_record.json', 'prior_report.json', 'verification.json', 'verify.py', 'turns.json', 'review/verification.json', 'review/independent_results.json', 'review/submitted_verify.py'}
WHOLE_VERDICT = 'PASS_CREDITED_KNOWN_UNRESTRICTED_REFLECTION_CURRENT_PACKET_CUSTODY_REPAIRED'
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
NATIVE = {'draft_pr_publication_program_20260930/inventory.json'} | {'unsolved_math_prioritization/' + n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
IGNORED_CACHE3 = {'unsolved_math_prioritization/cache/problems.json', 'unsolved_math_prioritization/cache/research_results.json', 'unsolved_math_prioritization/cache/catalog.sqlite'}
SCIENCE = {'full_problem_solved': True, 'full_target_prior_result_verified': True, 'full_target_resolved_in_prior_published_literature': True, 'full_problem_solved_by_project': False, 'project_solved': False, 'prior_publication_doi': '10.1007/s11854-007-0009-x', 'partial_valid': True, 'novelty_claimed': False, 'priority_claimed': False, 'original_substantive_attempts': 0, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'verification_attempts_added': 0, 'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'paper_or_new_doi_or_tracker': False, 'human_referee_review_claimed': False, 'human_peer_review_claimed': False, 'full_2007_journal_proof_independently_certified': False, 'existing_result_credit': ['Daniela Kraus', 'Oliver Roth', 'Stephan Ruscheweyh']}


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
        'pr48-acceptance-source-closure/v1':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'},
        'pr48-acceptance-source-closure/v2':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'},
        'pr48-acceptance-source-closure/v3':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'},
        'pr46-acceptance-source-closure/v1':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'},
        'pr49-acceptance-source-closure/v1':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'},
        'pr49-acceptance-source-closure/v2':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'},
        'pr49-strict-current-packet/v1':{'schema','self_excluded','files_count','files','current_gate','status','full_problem_solved','project_solved','novelty_claimed','original_substantive_attempts','new_substantive_attempts','audit_turns','full_permission_mode','turn_limit'},
        'pr49-final-root-two-member-closure/v1':{'schema','utc','self_excluded','files_count','files'},
        'pr49-accepted-strict-self-excluding-closure/v1':{'schema','utc','self_excluded','files_count','files','foreign_excluded_prefixes'},
    }
    require(type(obj) is dict and obj.get('schema') in known,'Unknown critical closure schema')
    keyset(obj,known[obj['schema']],'Exact recognized closure schema')
    if obj['schema'] in {'pr49-acceptance-source-closure/v2','pr48-acceptance-source-closure/v3','pr49-acceptance-source-closure/v1','pr48-acceptance-source-closure/v2','pr48-acceptance-source-closure/v1','pr46-acceptance-source-closure/v1'}:
        required(obj,{'status':'CLOSED_SOURCE_ONLY','source_only':True,'proposed_helpers_imported_compiled_executed':False,'future_acceptance_or_ROOT_approval_claimed':False},'Closed preparation, not future execution')
    rr=rows(obj['files'])
    declarations=[obj[k] for k in ['excluded','self_excluded'] if k in obj]
    require(declarations and all(equal(value,[name]) for value in declarations),'Only declared literal root manifest self may be excluded')
    require(name not in {z['path'] for z in rr},'Only literal root manifest self excluded')
    if count is not None: require(len(rr)==count,'Manifest count differs')
    for k in ['files_count','member_count']:
        if k in obj: require(type(obj[k]) is int and obj[k]==len(rr),'Declared count/type differs')
    check(base,rr); exact(base,{z['path'] for z in rr}|{name})
    if frozen:frozen_files(base,rr,name)
    return rr


def bound(pin):
    check(R,[pin]); p=regular(R,pin['path'])
    require(p.resolve().is_relative_to(A.resolve()),'Evidence outside exact PR49 audit')
    return p.read_bytes()


def pin(p):
    raw=Path(p).read_bytes(); return {'path':Path(p).relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)}


def binding(p): return {k:v for k,v in pin(p).items() if k!='bytes'}


def write(p,raw,exclusive=False):
    p=Path(p);require(type(raw) is bytes,'Complete output bytes required')
    require(p.parent.is_dir() and not p.is_symlink() and all(not d.is_symlink() for d in p.parents),'Unsafe output or symlink ancestor')
    existed=p.exists();old_mode=None;old_body=None;old_identity=None
    if exclusive:require(not existed,'Existing output: inspect before retry')
    elif existed:
        old_stat=p.lstat();require(stat.S_ISREG(old_stat.st_mode),'Existing replacement must be a regular file')
        old_mode=stat.S_IMODE(old_stat.st_mode);old_identity=(old_stat.st_dev,old_stat.st_ino);old_body=p.read_bytes()
    tmp=p.with_name(p.name+'.pr49-tmp')
    with tmp.open('xb') as s:
        s.write(raw);s.flush()
        if old_mode is not None:os.fchmod(s.fileno(),old_mode)
        os.fsync(s.fileno())
    if exclusive:
        os.link(tmp,p,follow_symlinks=False);tmp.unlink()
    elif existed:
        now=p.lstat();require(stat.S_ISREG(now.st_mode) and not p.is_symlink() and (now.st_dev,now.st_ino)==old_identity and stat.S_IMODE(now.st_mode)==old_mode and p.read_bytes()==old_body,'Replacement preimage changed before atomic replace')
        os.replace(tmp,p)
    else:
        os.link(tmp,p,follow_symlinks=False);tmp.unlink()
    require(p.is_file() and not p.is_symlink() and p.read_bytes()==raw,'Atomic output full bytes differ')
    if old_mode is not None:require(stat.S_IMODE(p.lstat().st_mode)==old_mode,'Atomic replacement changed full permission mode')
    fd=os.open(p.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)


def dump(p,v,exclusive=False): write(p,encode(v),exclusive)
def git_bytes(*a): return subprocess.check_output(['git',*a],cwd=R,timeout=30)
def git(*a): return git_bytes(*a).decode().strip()


def remote():
    o=parse(subprocess.check_output(['gh','pr','view',str(PR),'--repo','AlecKriebel/Math','--json','number,url,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,body'],cwd=R,timeout=30))
    keyset(o,{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Complete known GitHub receipt')
    required(o,{'number':49,'url':'https://github.com/AlecKriebel/Math/pull/49','headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual remote')
    return o


def original_native(base):
    snapshot=load(A/'snapshot_manifest.json')
    require(snapshot['schema']=='pr49-original-source-snapshot/v1' and snapshot['head']==HEAD and snapshot['merge_base']==ORIGINAL_BASE==GITHUB_BASE and len(snapshot['files'])==16,'Literal original16 and equal head/base identities')
    exact(base,{z['relative_path'] for z in snapshot['files']})
    for z in snapshot['files']:
        n=z['relative_path'];relative(n);require(z['path']=='unsolved_math_prioritization/attempts/'+ID+'/'+n and z['git_mode']=='100644','Exact original literal paths/Git mode')
        raw=regular(base,n).read_bytes();require(raw==regular(A/'source_snapshot',n).read_bytes() and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Original16 full bytes differ')


def source(base):
    original_native(base/'original_archive')
    for n in IMMUTABLE:require(regular(base,n).read_bytes()==regular(A/'source_snapshot',n).read_bytes(),'Literal operative immutable11 changed')
    for n,h in load(HERE/'SCIENTIFIC_SCOPE.json')['operative_artifact_sha256'].items():require(sha(regular(base,n).read_bytes())==h,'Entire globally qualified science changed')
    require(sha(regular(base,'SOURCE_STATUS.md').read_bytes())==SCIENCE_SHA and sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Exact original science/source anchors')
    record=load(base/'source_record.json');require(type(record['id']) is int and record['id']==30000703 and record['problem_number']==CODE,'Plain integer original source ID')
    body=regular(base,'turns.json').read_bytes();require(body==regular(A/'source_snapshot','turns.json').read_bytes() and sha(body)==LEDGER_SHA,'Entire original zero-turn object')
    ledger=parse(body);require(equal(ledger,load(HERE/'EXPECTED_ORIGINAL_LEDGER.json')),'Literal typed ledger object unchanged');required(ledger,{'id':30000703,'count':0,'substantive_attempts':[]},'Exact original0/5 ledger')
    require('source_verification_responses' not in ledger and 'source_verification_response' not in ledger,'No invented original response count')
    require(regular(base,'prior_report.json').read_bytes()==b'null\n' and load(base/'prior_report.json') is None,'Exact original null marker, distinct absence/SQL fallback')


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
    p=regular(R,name);require(p.parent==A and p.name=='ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json','Genuine adjacent final ROOT approval required');require(sha(p.read_bytes())==digest(pin_value),'Actual ROOT approval pin')
    o=parse(p.read_bytes());draft=load(HERE/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json');keys=['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post','previous_post_contract','previous_preparation_manifest','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection']
    for k in keys:exact_reference(o[k]);check(R,[o[k]])
    require(equal(o['root_whole_inspection'],{k:v for k,v in load(HERE/'INPUT_BINDINGS.json')['root_whole_record'].items() if k!='full_mode'}),'Exact actual completed ROOT whole record')
    draft.update(status='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR48_EVIDENCE',created_utc=o['created_utc'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR48_predecessor_read_completed=True)
    for k in keys:draft[k]=o[k]
    require(equal(o,draft),'Complete typed ROOT approval, no extension or pending predecessor');clock=utc_clock(o['created_utc'],'Actual ROOT approval');require(clock<=dt.datetime.now(dt.timezone.utc),'No future approval')
    predecessor48(o,clock)
    require(o['root_capture_operator']['path']==(A/'capture_root_final_operation.py').relative_to(R).as_posix() and bound(o['root_capture_operator'])==regular(HERE,'capture_root_final_operation.py').read_bytes(),'Exact prepared final operator separately read by ROOT')
    sm=regular(R,o['acceptance_source_manifest']['path']);sv=regular(R,o['acceptance_source_verdict']['path']);sr=regular(R,o['root_source_inspection']['path'])
    require(sm.parent==sv.parent and sm.parent.parent==A and sm.parent.name.startswith('acceptance_source_adversary_family') and sm.name=='SELF_MANIFEST.json' and sv.name=='VERDICT.json','New distinct acceptance SOURCE adversary closure required')
    own=load(sm);rr=rows(own['files']);require(own['self_excluded']==['SELF_MANIFEST.json'] and type(own['files_count']) is int and own['files_count']==len(rr),'Literal SOURCE self-only count');check(sm.parent,rr);exact(sm.parent,{z['path'] for z in rr}|{'SELF_MANIFEST.json'});frozen_files(sm.parent,rr,'SELF_MANIFEST.json')
    verdict=load(sv);required(verdict,{'schema':'pr49-acceptance-source-adversary-verdict/v1','verdict':'PASS_SOURCE_ONLY_SCOPED','preparation_manifest_sha256':sha((HERE/'PREPARATION_MANIFEST.json').read_bytes()),'mandatory_corrections':[],'production_imported_compiled_executed':False,'future_acceptance_approved':False},'New SOURCE gate')
    require(sr.parent==A and sr.name=='ROOT_SOURCE_ACCEPTANCE_REVIEW.json','Genuine ROOT acceptance SOURCE read')
    root=load(sr);required(root,{'schema':'pr49-root-complete-acceptance-source-inspection/v1','status':'PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION','all_prepared_source_and_controls_fully_read':True,'exact_preparation_closure_and_full_modes_checked':True,'all_individual_source_adversary_inputs_checked':True,'all_complete_actual_captures_checked':True,'complete_VERDICT_object':verdict,'preparation_manifest_sha256':sha((HERE/'PREPARATION_MANIFEST.json').read_bytes()),'acceptance_source_manifest':o['acceptance_source_manifest'],'acceptance_source_verdict':o['acceptance_source_verdict'],'mandatory_corrections':[],'future_execution_approved':False},'Complete genuine ROOT SOURCE reading')
    full_source_adversary_bindings(root,sm.parent)
    require(utc_clock(root['utc'],'Actual SOURCE read')<=clock,'SOURCE reading precedes approval')
    return o,p

def predecessor48(o,clock):
    p48=B/'audits/pr48_2961';cp=R/o['previous_post_contract']['path'];sm=R/o['previous_preparation_manifest']['path']
    require(cp==p48/'acceptance_preparation_family_v3/ROOT_POST_CONTRACT.json' and sm==cp.parent/'PREPARATION_MANIFEST.json','Actual repaired48 V3 closure/contract required')
    require(stat.S_IMODE(cp.stat().st_mode)==0o444 and sha(cp.read_bytes())=='26f89f5ebf8444f96394ca5050c503920de1b9adb7417489241fcbe04885b410','Exact known source contract; unfinished V3 never pins or readiness')
    manifest(cp.parent,'PREPARATION_MANIFEST.json',o['previous_preparation_manifest']['sha256'],frozen=True)
    require(load(sm)['schema']=='pr48-acceptance-source-closure/v3','Exact repaired48 V3 predecessor schema; V1/V2 never transfer')
    contract=load(cp);require(contract['schema']=='pr48-future-ROOT-whole-post-contract/v1' and contract['source_only'] is True and contract['future_ROOT_post_completed'] is False,'Source contract alone asserts no completion')
    previous=load(R/o['previous_mirror']['path']);post=load(R/o['previous_post']['path']);rootpost=load(R/o['previous_root_post']['path'])
    for k,n in [('previous_mirror','state_mirror_bindings.json'),('previous_post','post_acceptance_verification.json'),('previous_root_post','ROOT_ACTUAL_POST_INSPECTION.json')]:require(R/o[k]['path']==p48/n,'Genuine actual48 adjacent evidence')
    require(len(contract['future48_required_ROOT_complete_keyset'])==22,'Exact22-key predecessor ROOT contract');keyset(rootpost,contract['future48_required_ROOT_complete_keyset'],'Entire actual48 ROOT post');required(rootpost,{'schema':contract['future48_required_ROOT_schema'],**contract['future48_required_completed_values'],'entire_post':post},'Completed48 full evidence')
    required(post,contract['future48_required_entire_post_values'],'Actual48 typed post');required(post,{'status':'PASS','pr':48,'targets':39,'consumed_substantive_turns':47,'primary_acceptances':38,'program_completed_count':38,'new_proof_turns':0,'paper_or_new_doi_or_tracker':False},'Actual48 completes39/47/38 before49')
    require(utc_clock(post['utc'],'Actual48 post')<=utc_clock(rootpost['utc'],'Actual48 ROOT')<=clock,'Actual predecessor chronology')
    require(type(previous['entries']) is list and len(previous['entries'])==38,'Every38 primary predecessor entries');nums=[z['pr'] for z in previous['entries']];require(all(type(n) is int for n in nums) and len(set(nums))==38 and all(n in nums for n in [46,47,48]) and 49 not in nums and equal(sorted(nums),previous['required_completed_prs']),'Actual ascending membership, never manufactured');require(type(previous['duplicate_mirrors']) is list and len(previous['duplicate_mirrors'])==1,'Existing one duplicate preserved')
    caps=rootpost['all_six_real_phase_captures'];require(type(caps) is list and len(caps)>=6,'Complete actual predecessor phase captures')
    for item in caps:
        require(type(item) is dict,'Actual capture row');ref=item.get('capture',item.get('CAPTURE',item));exact_reference(ref);check(R,[ref]);p=R/ref['path'];cap=load(p);required(cap,{'actual_execution':True,'completed':True,'exit_code':0,'stdin_supplied':False,'source_unchanged':True,'operator_unchanged':True},'Completed actual predecessor child');require(type(cap['pid']) is int and cap['pid']>0,'Actual PID')
        for channel in ['stdout','stderr']:exact_reference(cap[channel]);check(p.parent,[cap[channel]])
        require(regular(p.parent,'stderr.bin').read_bytes()==b'' and sha(regular(p.parent,'PRELAUNCH_SOURCE.py').read_bytes())==digest(cap['source_sha256']) and sha(regular(p.parent,'PRELAUNCH_OPERATOR.py').read_bytes())==digest(cap['operator_sha256']),'Full predecessor streams/source/operator')
        require(type(cap['argv']) is list and cap['argv'][:2]==['/usr/bin/python3','-B'] and cap['argv'][2] in [str(cp.parent/n) for n in ['integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']],'Actual repaired48 source argv whitelist');require(utc_clock(cap['started_utc'],'Start')<=utc_clock(cap['finished_utc'],'Exit')<=utc_clock(rootpost['utc'],'ROOT'),'Actual phase chronology')


def full_source_adversary_bindings(root,folder):
    refs=root['normalized_complete_external_input_bindings'];require(type(refs) is list and refs and all(type(z) is dict for z in refs),'Complete SOURCE individual external body bindings')
    seen=set()
    for z in refs:
        keyset(z,{'path','bytes','sha256','full_mode'},'Full SOURCE binding');check(R,[z]);require(type(z['full_mode']) is int and stat.S_IMODE(regular(R,z['path']).stat().st_mode)==z['full_mode'],'SOURCE input fullmode');require(z['path'] not in seen,'Duplicate SOURCE binding');seen.add(z['path'])
    captures=root['complete_actual_closing_and_postclosing_readback_captures'];require(type(captures) is list and len(captures)==2,'Actual SOURCE closer and separate readback')
    clocks=[]
    for row in captures:
        ref=row['capture'];exact_reference(ref);check(R,[ref]);p=R/ref['path'];cap=load(p);require(equal(cap,row['complete_capture']),'Entire actual SOURCE capture');required(cap,{'actual_execution':True,'completed':True,'exit_code':0,'stdin_supplied':False},'Actual SOURCE completed capture');require(type(cap['pid']) is int and cap['pid']>0,'Actual SOURCE PID');clocks.extend([utc_clock(cap['started_utc'],'SOURCE start'),utc_clock(cap['finished_utc'],'SOURCE finish')]);check(R,row['complete_members'])
        for channel in ['stdout','stderr']:exact_reference(cap[channel]);check(p.parent,[cap[channel]])
        require(regular(p.parent,'stderr.bin').read_bytes()==b'','Whole SOURCE stderr')
    require(clocks==sorted(clocks) and clocks[-1]<=utc_clock(root['utc'],'ROOT SOURCE read'),'SOURCE close/readback before ROOT read')


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
    approved,rp=root_binding_input(root_bindings,root_bindings_sha256);inputs=load(HERE/'INPUT_BINDINGS.json')
    require(inputs['whole_binding_completed'] is True and inputs['actual_predecessor_PR48_completed'] is False,'Only actual ROOT whole is bound; actual48 acceptance supplied later')
    refs=[]
    for z in inputs['pins'].values():check(R,[z]);require(stat.S_IMODE(regular(R,z['path']).stat().st_mode)==z['full_mode'],'Exact fixed input full mode');refs.append({k:v for k,v in z.items() if k!='full_mode'})
    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,1544,frozen=True)
    deps=load(C/'CURRENT_DEPENDENCIES.json');require(sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())==DEPS_SHA and len(rows(deps['files']))==1407,'Complete1407 dependencies')
    root=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json');verdict=load(A/'current_whole_adversary_family/VERDICT.json')
    required(root,{'schema':'pr49-root-complete-closed-whole-inspection/v1','status':'PASS_ROOT_COMPLETE_CLOSED_CURRENT_WHOLE_RECONCILIATION','approved_by_root':True,'complete_report_personally_read':True,'complete_verdict_personally_read':True,'complete_sources_and_actual_captures_personally_read':True,'entire_VERDICT_object':verdict,'current_payload_count':1544,'current_dependency_count':1407,'current_fixed_dependency_count':1403,'closed_whole_payload_count':127,'whole_fixed_input_count':3083,'original_final_inner_commands':50,'frozen_inner_prefix':48,'original_full_inner_streams':100,'actual_ROOT_clean_closure':267,'actual_ROOT_clean_readback':755,'ROOT_initial_failed_closure':82903,'ROOT_wrong_hash_failed_readback':444,'status_classification':'already_solved','exact_full_known_target_verified':True,'project_solved':False,'novelty_claimed':False,'full_2007_journal_proof_independently_certified':False,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'separate_original_source_response_count':None,'future_acceptance_approved':False,'current_native_acceptance_approved':False,'future_PR48_acceptance_approved':False},'Entire actual ROOT whole meaning')
    required(verdict,{'verdict':WHOLE_VERDICT,'mandatory_corrections':[],'status':'already_solved','full_problem_solved':True,'full_target_prior_result_verified':True,'project_solved':False,'novelty_claimed':False,'full_2007_journal_proof_independently_certified':False,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'future_acceptance_approved':False},'Credited exact known target only')
    historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    fixed=root['normalized_complete_fixed_bindings'];require(len(fixed)==3229 and not ({z['path'] for z in fixed}&historical),'All fixed normalized bindings; exactly4 dated native excluded')
    for z in fixed:keyset(z,{'path','bytes','sha256','full_mode'},'Complete normalized binding');check(R,[z]);require(type(z['full_mode']) is int and stat.S_IMODE(regular(R,z['path']).stat().st_mode)==z['full_mode'],'Complete fixed fullmode');refs.append({k:v for k,v in z.items() if k!='full_mode'})
    require(len(root['dated_native4'])==4 and {z['original_observed_row']['path'] for z in root['dated_native4']}==historical,'Exact4 dated native witnesses')
    for row in root['dated_native4']:
        old=row['original_observed_row'];snap=row['whole_historical_snapshot'];check(R,[snap]);require(old['bytes']==snap['bytes'] and old['sha256']==snap['sha256'] and old['full_mode']==0o644 and snap['full_mode']==0o444 and row['future_fresh13_ROOT_required'] is True and row['live_unchanged_required_by_review_closure'] is False,'Full-body dated witness, never freshness')
    for z in deps['files']:
        if z['path'] in historical:require(any(equal(z,q['original_observed_row']) for q in root['dated_native4']),'Exact dependency dated observation')
        else:check(R,[z])
    w=A/'current_whole_adversary_family';wm=load(w/'SELF_MANIFEST.json');require(sha((w/'SELF_MANIFEST.json').read_bytes())==inputs['whole_manifest']['sha256'] and wm['files_count']==127,'Actual closed WHOLE127');rr=rows(wm['files']);check(w,rr);exact(w,{z['path'] for z in rr}|{'SELF_MANIFEST.json'});frozen_files(w,rr,'SELF_MANIFEST.json');require(sorted(topology(w)[1])==wm['directories'],'Complete16 WHOLE dirs')
    for z in wm['directory_full_modes']:require(stat.S_IMODE((w/z['path']).stat().st_mode)==z['full_mode'],'Whole full directory modes')
    source(C)
    for n in ADMIN:require(equal(load(C/n),load(HERE/'EXPECTED_CURRENT_ADMIN.json')),'Entire four frozen admin bodies')
    refs+=[pin(C/'MANIFEST.json'),pin(C/'CURRENT_DEPENDENCIES.json'),pin(w/'SELF_MANIFEST.json'),pin(w/'REPORT.md'),pin(w/'VERDICT.json'),pin(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),pin(rp)]+[approved[k] for k in ['previous_mirror','previous_post','previous_root_post','previous_post_contract','previous_preparation_manifest','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection','root_capture_operator']]
    out={}
    for z in refs:require(z['path'] not in out or equal(out[z['path']],z),'Conflicting immutable identity');out[z['path']]=z
    return frozen,sorted(out.values(),key=lambda z:z['path'])


def plan_scope(o,prep,root_bindings,root_bindings_sha256):
    _,refs=basis(root_bindings,root_bindings_sha256)
    bindings,_=root_binding_input(root_bindings,root_bindings_sha256)
    draft=load(HERE/'DRAFT_FINAL_PLAN.json')
    draft.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=prep,root_bindings=root_bindings,root_bindings_sha256=root_bindings_sha256,whole_manifest_sha256=bindings['whole_manifest']['sha256'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR48_predecessor_read_completed=True,immutable_evidence_references=refs)
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
    required(receipt,{'schema':'pr49-actual-final-reconciliation/v1','status':'PASS','actual_root_reconciliation':True,'pr':49,'problem_id':30000703,'preparation_manifest_sha256':a.preparation_manifest_sha256,'entire_scope':scope,'bindings_before':refs,'bindings_after':refs,'root_reviewed_plan':pin(ps['final_plan']),'reconciliation_source':pin(HERE/'seal_final_evidence.py'),'science_helpers_executed':False,'new_substantive_attempts':0,'audit_turns':0,'shared_mutations':False},'Actual final reconciliation')
    require(ps['final_manifest'].parent==ps['final_receipt'].parent and ps['final_manifest'].name=='FINAL_MANIFEST.json','Literal final closure required')
    fm=manifest(ps['final_manifest'].parent,'FINAL_MANIFEST.json',a.final_manifest_sha256,2,frozen=True)
    require({z['path'] for z in fm}=={'ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json'} and ps['final_receipt'].name=='ROOT_FINAL_RECONCILIATION.json','Exact final output names required')
    require(equal(load(ps['final_manifest'].parent/'ROOT_REVIEWED_SCOPE.json'),scope),'Final complete scope copy differs')
    cap=load(ps['reconciliation_capture'])
    keyset(cap,{'schema','argv','cwd','actual_execution','completed','pid','source_sha256','stdin_supplied','native13_before','main_head_before','started_utc','exit_code','finished_utc','source_unchanged','main_head_after','native13_after','stdout','stderr','readonly_git_queries','status'},'Complete final actual ROOT capture schema')
    required(cap,{'schema':'ROOT_actual_audit_administrative_capture_v1','actual_execution':True,'completed':True,'exit_code':0,'status':'PASS','stdin_supplied':False,'source_unchanged':True,'source_sha256':sha((HERE/'seal_final_evidence.py').read_bytes()),'cwd':str(A)},'Genuine actual final capture')
    require(equal(cap['native13_before'],cap['native13_after']) and cap['main_head_before']==cap['main_head_after'],'Final sealer capture must preserve native13 and HEAD')
    require(len(rows(cap['native13_before']))==13 and {z['path'] for z in rows(cap['native13_before'])}==NATIVE,'Exact thirteen actual final capture native references')
    for z in cap['native13_before']:
        keyset(z,{'path','bytes','sha256','worktree_mode'},'Exact sealer captured native row/mode');require(type(z['worktree_mode']) is int and 0<=z['worktree_mode']<=0o7777,'Complete full native mode')
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
    require(equal(pin(ps['previous_mirror']),authority['previous_mirror']) and equal(pin(ps['previous_post']),authority['previous_post']),'Entire actual48 predecessor references')
    fresh=load(ps['fresh_preimage']); required(fresh,{'approved_by_root':True},'Fresh actual native preimage')
    keyset(fresh,{'schema','approved_by_root','created_utc','reason_date_utc','reason','current_head','files','protected_foreign_tracked_paths'},'Exact current ROOT fresh input schema')
    require(fresh['schema']=='pr49-root-fresh-acceptance-input-preimages/v1','Unknown fresh authority schema')
    created=utc_clock(fresh['created_utc'],'Actual root fresh preimage creation')
    require(created<=dt.datetime.now(dt.timezone.utc),'Fresh root preimage creation clock is in the future')
    require(type(fresh['reason_date_utc']) is str and fresh['reason_date_utc']==created.date().isoformat(),'Root rebase reason date must match the actual UTC creation date')
    require(type(fresh['reason']) is str and fresh['reason']==fresh['reason'].strip() and len(fresh['reason'])>=40 and len(fresh['reason'].split())>=6,'Substantive root-reviewed rebase reason required; a token such as yes is insufficient')
    require(type(fresh['current_head']) is str and re.fullmatch('[0-9a-f]{40}',fresh['current_head']),'Explicit fresh main HEAD required, independently of archived replay HEAD')
    rr=rows(fresh['files']); require({z['path'] for z in rr}==NATIVE and len(rr)==13,'Exact13 fresh full native/inventory pins required')
    require(all(type(z.get('worktree_mode')) is int and 0<=z['worktree_mode']<=0o7777 for z in rr),'Explicit typed thirteen worktree permission modes required')
    for z in fresh['files']:keyset(z,{'path','bytes','sha256','worktree_mode'},'Exact fresh native reference')
    foreign_paths=fresh['protected_foreign_tracked_paths'];require(type(foreign_paths) is list and all(type(n) is str for n in foreign_paths) and foreign_paths==sorted(set(foreign_paths)),'Exact sorted ROOT protected foreign path list')
    protected_foreign_paths(fresh)
    snap=load(A/'snapshot_manifest.json');original_native(C/'original_archive')
    raw=git_bytes('diff','--no-ext-diff','--no-textconv','--binary',ORIGINAL_BASE,HEAD,'--');require(raw==(C/'original_diff.patch').read_bytes() and raw==(A/'original_diff.patch').read_bytes() and len(raw)==52829,'Entire original17-path diff')
    require(len(git_bytes('diff','--name-only',ORIGINAL_BASE,HEAD).decode().splitlines())==17,'Original17 changed paths')
    for z in snap['files']:
        require(git_bytes('show',HEAD+':'+z['path'])==(C/'original_archive'/z['relative_path']).read_bytes(),'Original Git/archive full bytes')
        require(git_bytes('ls-tree','-z',HEAD,'--',z['path']).decode().rstrip('\0')==z['git_mode']+' blob '+z['git_object']+'\t'+z['path'],'Exact original Git mode/object')
    for rev in [ORIGINAL_BASE,HEAD]:
        state=parse(git_bytes('show',rev+':unsolved_math_prioritization/state.json')); require(ID not in state,'No original primary/duplicate native state allowed')
        hp='unsolved_math_prioritization/history.jsonl'
        hb=git_bytes('show',rev+':'+hp) if git_bytes('ls-tree','-z',rev,'--',hp) else b''
        require(not hb or hb.endswith(b'\n'),'Historical history incomplete')
        require(not any(str(e.get('id',e.get('problem_id',''))) in {ID} for e in map(parse,hb.splitlines())),'No invented original selected history allowed')
    frozen,_=basis(a.root_bindings,a.root_bindings_sha256)
    return frozen,{n:getattr(a,n) for n in ['preparation_manifest_sha256','final_plan','final_plan_sha256','final_receipt','final_receipt_sha256','final_manifest','final_manifest_sha256','reconciliation_capture','reconciliation_capture_sha256','previous_mirror','previous_mirror_sha256','previous_post','previous_post_sha256','fresh_preimage','fresh_preimage_sha256','root_bindings','root_bindings_sha256']}


def selected(data):
    alias_QUEUE_absent(data); lines=data.decode().splitlines(keepends=True); heads=[s for s in lines if s.startswith('| Rank | ID / code |')]
    require(len(heads)==1 and [s.strip() for s in heads[0].split('|')[1:-1]]==HEADER,'Exact12 named columns required')
    rr=[s for s in lines if len(s.split('|'))==14 and s.split('|')[2].strip()==ID+' / '+CODE]
    require(len(rr)==1,'Unique exact primary queue row required'); return rr[0]


def derive_inventory(before,remote,finalized_utc):
    require(type(before) is dict and type(before.get('items')) is list and len(before['items'])==180,'Complete retained180 inventory')
    require(all(type(z) is dict and type(z.get('number')) is int for z in before['items']),'Typed inventory identities')
    identities=[z['number'] for z in before['items']];require(len(set(identities))==180 and identities.count(49)==1,'Unique original selected PR49')
    require(type(before.get('completed_count')) is int and before['completed_count']==38 and sum(z.get('stage')=='complete' for z in before['items'])==38,'Actual38 prior primaries')
    required(remote,{'state':'MERGED','isDraft':False,'number':49,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual merged standard-partial remote')
    require(type(remote['mergeCommit']) is dict and set(remote['mergeCommit'])=={'oid'} and type(remote['mergeCommit']['oid']) is str and re.fullmatch('[0-9a-f]{40}',remote['mergeCommit']['oid']),'Exact actual merge oid')
    clock=utc_clock(finalized_utc,'Actual finalization');merged=utc_clock(remote['mergedAt'],'Actual mergedUTC');require(merged<=clock<=dt.datetime.now(dt.timezone.utc),'No reversed/future merge finalization')
    inv=copy.deepcopy(before);chosen=next(z for z in inv['items'] if z['number']==49);require(chosen.get('stage')!='complete','Selected not already complete')
    chosen.update(stage='complete',outcome='already_solved_accepted_partial',queue_status='already_solved',audited_head=HEAD,merge_commit=remote['mergeCommit']['oid'],merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts='0/5',new_substantive_attempts=0,cumulative_attempts='0/5',paper_or_new_doi_or_tracker=False)
    require(sum(z.get('stage')=='complete' for z in inv['items'])==39,'Exactly39 derived primary completions')
    inv.update(updated_at_utc=finalized_utc,last_checkpoint_utc=finalized_utc,completed_count=39,program_completion_estimate_percent=39*100/180,completion_estimate_percent=39*100/180,current_pr=50)
    return inv


def finalization(pins,pre):
    record=load(A/'integration_finalization.json');remote=load(A/'remote_merge_receipt.json')
    keyset(remote,{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Complete actual retained remote schema')
    require(type(record) is dict and 'utc' in record,'Actual retained finalization record required')
    expected={'schema':'pr49-actual-integration-finalization/v1','utc':record['utc'],**pins,'pr':49,'before_inventory_sha256':pre['inventory_before_sha256'],'remote_merge_receipt':pin(A/'remote_merge_receipt.json'),'merge_commit':remote['mergeCommit']['oid'],'merge_tree':git('show','-s','--format=%T',remote['mergeCommit']['oid']),'source_sha256':sha((HERE/'integrate_reviewed_partial.py').read_bytes())}
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
    return {'schema':'pr49-accepted-qualified-known-result/v1','utc':final['utc'],**SCIENCE,**pins,'pr':49,'id':30000703,'problem_id':30000703,'problem_number':CODE,'queue_status':'already_solved','outcome':'already_solved_accepted_known_result_merged','original_head':HEAD,'original_base':ORIGINAL_BASE,'merge_commit':final['merge_commit'],'merge_tree':final['merge_tree'],'merge_parents':[pre['main_before'],HEAD],'merged_at':remote['mergedAt'],'remote_state':'MERGED','remote_isDraft':False,'canonical_scientific_artifact_sha256':SCIENCE_SHA,'source_record_sha256':SOURCE_SHA,'original_ledger_sha256':LEDGER_SHA,'substantive_attempts_used':0,'substantive_attempt_limit':5,'native_historical_events_inferred':False,'historical_metadata_archival_only':True,'workflow_completion_estimate_percent':100,'full_resolution_by_project_completion_estimate_percent':0,'scientific_scope':load(HERE/'SCIENTIFIC_SCOPE.json'),'separate_original_source_response_count':None}


def accepted_invariants(o,pins,pre,audit=False):
    expected=expected_acceptance(pins,pre)
    if audit:
        expected.update(canonical_manifest_sha256=sha(regular(K,'MANIFEST.json').read_bytes()),canonical_manifest_entries=len(rows(load(K/'MANIFEST.json')['files'])))
    require(equal(o,expected),'Complete typed canonical/audit accepted receipt schema and derived values required; meaningful extensions prohibited')
    source(K)
    for n in ADMIN:
        expected_admin=load(C/n)
        expected_admin.update(**SCIENCE,**pins,id=30000703,current_context_path='CURRENT_CONTEXT_PRESENT.md',current_audit_scope_path='CURRENT_AUDIT_SCOPE_PRESENT.md',current_gate='accepted_qualified_known_result',current_verdict=WHOLE_VERDICT,status='already_solved_accepted_known_result_merged',new_whole_current_gate=WHOLE_VERDICT,historical_verdict_transferred=False,merge_commit=o['merge_commit'],merge_tree=o['merge_tree'],merged_at=o['merged_at'])
        require(equal(load(K/n),expected_admin),'Complete typed present administrative object differs: '+n)


def canonical_names(frozen,accepted=False):
    return {z['path'] for z in frozen}|{'reviewed_pending_administration/'+n for n in ADMIN}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md'}|({'acceptance.json','ACCEPTANCE.md','MANIFEST.json'} if accepted else set())


def canonical(frozen,accepted=False):
    exact(K,canonical_names(frozen,accepted))
    for z in frozen:
        p=K/('reviewed_pending_administration/'+z['path'] if z['path'] in ADMIN else z['path'])
        require(p.read_bytes()==(C/z['path']).read_bytes(),'Frozen science/archival administration changed')
    require((K/'reviewed_pending_administration/MANIFEST.json').read_bytes()==(C/'MANIFEST.json').read_bytes(),'Dated frozen manifest changed');source(K)


def foreign_capture(fresh):
    require(not git('diff','--cached','--name-only'),'Preflight index clean required')
    paths=fresh['protected_foreign_tracked_paths'];require(type(paths) is list and paths==sorted(set(paths)),'Exact ROOT-declared sorted protected foreign paths')
    protected_foreign_paths(fresh)
    dirty=set(git_bytes('diff','--name-only','-z').decode().split('\0'))-{''};require(dirty<=set(paths),'No undeclared tracked dirty exception')
    out=[]
    for n in paths:
        e=git_bytes('ls-tree','-z','HEAD','--',n).decode().rstrip('\0');fields,literal=e.split('\t');mode,kind,blob=fields.split();require(literal==n and kind=='blob' and mode in {'100644','100755'},'Regular tracked foreign path');raw=regular(R,n).read_bytes();out.append({'path':n,'bytes':len(raw),'sha256':sha(raw),'worktree_mode':stat.S_IMODE(regular(R,n).stat().st_mode),'head_sha256':sha(git_bytes('show','HEAD:'+n)),'head_entry':e,'index_entry':mode+' '+blob+' 0\t'+n})
    foreign_check({'foreign_logs':out,'fresh_preimage':fresh['_actual_path']});return out


def foreign_check(pre):
    fresh=load(R/pre['fresh_preimage']);paths=protected_foreign_paths(fresh);rr=pre['foreign_logs'];require([z['path'] for z in rr]==paths,'Exact protected ROOT declared foreign identities');check(R,rr)
    for z in rr:
        keyset(z,{'path','bytes','sha256','worktree_mode','head_sha256','head_entry','index_entry'},'Complete exact protected foreign reference');require(type(z['worktree_mode']) is int and stat.S_IMODE(regular(R,z['path']).stat().st_mode)==z['worktree_mode'],'Protected foreign full modes changed');n=z['path'];require(git_bytes('ls-tree','-z','HEAD','--',n).decode().rstrip('\0')==z['head_entry'] and git_bytes('ls-files','--stage','-z','--',n).decode().rstrip('\0')==z['index_entry'] and sha(git_bytes('show','HEAD:'+n))==z['head_sha256'] and sha(git_bytes('show',':'+n))==z['head_sha256'],'Protected foreign exact HEAD/index body/mode changed')


def native_modes(values):
    for z in rows(values):
        require(type(z.get('worktree_mode')) is int and 0<=z['worktree_mode']<=0o7777,'Explicit typed fresh worktree mode required')
        require(regular(R,z['path']).stat().st_mode&0o7777==z['worktree_mode'],'Exact native worktree permission mode changed: '+z['path'])


def fresh_check(pre,allowed=()):
    f=load(R/pre['fresh_preimage']);all_rows=rows(f['files']);remaining=[z for z in all_rows if z['path'] not in allowed]
    require(len(all_rows)==13 and {z['path'] for z in all_rows}==NATIVE,'Exact thirteen complete fresh native identities at every phase')
    require(set(allowed)<=NATIVE,'Only owned native body changes allowed');check(R,remaining);native_modes(all_rows);foreign_check(pre)


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
    spec=importlib.util.spec_from_file_location('pr49_bound_native_mirror',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
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
    required(o,{'schema':'pr49-original-head-integration-preflight/v1',**pins,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'dated_frozen_preimage_not_rewritten':True},'Original-head preflight source and scope')
    fresh=load(R/o['fresh_preimage']);require(o['main_before']==fresh['current_head'],'Original preflight main differs from fresh inputs')
    rr={z['path']:z for z in fresh['files']}
    for field,path in [('whole_queue_before_sha256',Q.relative_to(R).as_posix()),('state_before_sha256','unsolved_math_prioritization/state.json'),('history_before_sha256','unsolved_math_prioritization/history.jsonl'),('inventory_before_sha256','draft_pr_publication_program_20260930/inventory.json')]:
        require(o[field]==rr[path]['sha256'],'Complete fresh preflight source binding differs')
    keyset(o['pr'],{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Complete preflight remote schema')
    required(o['pr'],{'number':49,'url':'https://github.com/AlecKriebel/Math/pull/49','state':'OPEN','isDraft':True,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main','mergeCommit':None,'mergedAt':None},'Literal original draft head')
    before=regular(A,'integration_queue_before.md').read_bytes()
    require(sha(before)==o['whole_queue_before_sha256'] and selected(before)==o['selected_row_before'],'Complete retained queue preimage differs')
    require(sha(regular(A,'integration_inventory_before.json').read_bytes())==o['inventory_before_sha256'],'Complete retained inventory preimage differs')
    require(utc_clock(o['utc'],'Preflight UTC')<=dt.datetime.now(dt.timezone.utc),'Future preflight timestamp')
    foreign_check(o)
    return o


def overlay_record(pins,frozen):
    o=load(A/'integration_check.json')
    keyset(o,set(pins)|{'schema','utc','canonical_overlay_files','whole_queue_after_sha256','automatic_merge_queue_preimage_sha256','original_substantive_attempts','new_substantive_attempts','audit_turns','remote_pending'},'Complete overlay schema')
    required(o,{'schema':'pr49-original-head-overlay/v1',**pins,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'remote_pending':True},'Complete overlay scope and pins')
    for z in o['canonical_overlay_files']:exact_reference(z)
    require({z['path'] for z in rows(o['canonical_overlay_files'])}==canonical_names(frozen),'Entire owned overlay closure differs')
    require(sha(regular(A,'integration_merge_queue_before.md').read_bytes())==o['automatic_merge_queue_preimage_sha256'],'Entire automatic/conflicted queue preimage differs')
    digest(o['whole_queue_after_sha256']);utc_clock(o['utc'],'Overlay UTC')
    return o


def prepush_record(pins):
    o=load(A/'integration_prepush.json')
    keyset(o,set(pins)|{'schema','utc','merge_commit','merge_tree','merge_parents','canonical_overlay_files','whole_queue_after_sha256','remote_before_push','actual_push_performed_by_helper'},'Complete prepush schema')
    required(o,{'schema':'pr49-original-head-prepush/v1',**pins,'actual_push_performed_by_helper':False},'Whole original-head prepush pins')
    utc_clock(o['utc'],'PrepushUTC');pre=preflight_record(pins)
    require(equal(o['merge_parents'],[pre['main_before'],HEAD]) and git('show','-s','--format=%P',o['merge_commit']).split()==o['merge_parents'],'Complete archived prepush parents must equal actual original-head merge')
    require(o['merge_tree']==git('show','-s','--format=%T',o['merge_commit']),'Complete actual archived prepush tree')
    overlay=overlay_record(pins,rows(load(C/'MANIFEST.json')['files']))
    require(equal(o['canonical_overlay_files'],overlay['canonical_overlay_files']) and o['whole_queue_after_sha256']==overlay['whole_queue_after_sha256'],'Entire prepush overlay and queue derivation')
    observed=o['remote_before_push'];keyset(observed,{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Entire actual archived prepush remote')
    expected={'number':49,'url':'https://github.com/AlecKriebel/Math/pull/49','state':'OPEN','isDraft':False,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main','mergeCommit':None,'mergedAt':None,'body':regular(A,'accepted_pr_body.md').read_text()}
    require(equal(observed,expected),'Complete typed actual original-head prepush remote/body')
    return o


def mirror_proposal(proposal,pins):
    previous=load(R/pins['previous_mirror']);expected=copy.deepcopy(previous)
    expected.update(created_at_utc=proposal.get('created_at_utc'),scope='Incremental present accepted primary PR49 credited known Schwarz–Pick local reflection; original0/5,new0,audit0, no historical reconstruction.')
    for n in ['inventory','queue']:expected[n]=binding(R/previous[n]['path'])
    expected['required_completed_prs']=sorted(previous['required_completed_prs']+[49])
    expected['entries'].append({'pr':49,'id':ID,'status':'already_solved','acceptance':binding(K/'acceptance.json'),'audit_acceptance':binding(A/'acceptance.json'),'remote':binding(A/'remote_merge_receipt.json'),'accepted_source':binding(K/'source_record.json'),'canonical_acceptance_text':binding(K/'ACCEPTANCE.md'),'canonical_manifest':binding(K/'MANIFEST.json'),'artifact':{**binding(K/'SOURCE_STATUS.md'),'acceptance_hash_field':'canonical_scientific_artifact_sha256'},'budget':{'used':0,'limit':5,'kind':'pr49_exact_original_zero_turn_object','ledger':binding(K/'turns.json')},'duplicates':[]})
    require(equal(proposal,expected),'Entire typed exact old proposal plus one standard-partial primary')
    require(utc_clock(proposal['created_at_utc'],'Actual proposalUTC')<=dt.datetime.now(dt.timezone.utc),'No future proposal clock')


def mirror_records(pins,pre,plan,intent,receipt,proposal):
    keyset(plan,{'bindings','created_at_utc','decisions','dry_run','duplicate_count','duplicate_decisions','history_after_sha256','history_append','history_append_bytes','limitations','preconditions','primary_count','proposal_spec','protected','schema','state_after','state_after_bytes','state_after_sha256','writes_authorized_to_live_repo'},'Known complete native plan schema')
    require(plan['schema']=='acceptance-mirror-plan/v2','Unknown critical native mirror plan schema')
    mirror_proposal(proposal,pins);require(equal(plan['proposal_spec'],proposal),'Entire native plan proposal differs')
    before_state=regular(A,'integration_state_before.json').read_bytes();before_history=regular(A,'integration_history_before.jsonl').read_bytes()
    require(equal(plan,rebuild_saved_mirror_plan(proposal,plan['created_at_utc'],before_state,before_history)),'Entire native plan must derive exactly from actual old bodies and same timestamp')
    expected={'schema':'pr49-present-acceptance-mirror/v1','status':'COMPLETED','utc':intent.get('utc'),**pins,'plan_sha256':sha(encode(plan)),'before':plan['preconditions'],'before_state_bytes':before_state.decode(),'before_history_bytes':before_history.decode(),'state_after_sha256':plan['state_after_sha256'],'history_after_sha256':plan['history_after_sha256'],'write_order':['history.jsonl','state.json'],'new_event':ID,'new_proof_turns':0,'lock_limitation':'Cooperative advisory lock; noncooperating writers remain outside protocol.','completed_utc':intent.get('completed_utc')}
    require(equal(intent,expected),'Entire typed completed native intent, source pins and exact old bytes required')
    clocks=[utc_clock(intent[n],'Actual native intent clock') for n in ['utc','completed_utc']]
    require(clocks==sorted(clocks) and clocks[-1]<=dt.datetime.now(dt.timezone.utc),'Native intent clock order/future')
    keyset(receipt,set(pins)|{'utc','status','validation','negative_ledger_controls','history_events_added','prior_state_entries_preserved','current_targets','consumed_substantive_turns','primary_acceptances','duplicate_count','new_duplicate_native_acceptance_added','new_proof_turns','state_sha256','history_sha256'},'Complete native mirror receipt')
    required(receipt,{'status':'COMPLETED',**pins,'negative_ledger_controls':['empty','whitespace_only','invented_JSONL','bool_used','wrong_used','wrong_limit'],'history_events_added':1,'prior_state_entries_preserved':39,'current_targets':40,'consumed_substantive_turns':47,'primary_acceptances':39,'duplicate_count':1,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,'state_sha256':plan['state_after_sha256'],'history_sha256':plan['history_after_sha256']},'Entire native receipt disposition')
    keyset(receipt['validation'],{'bindings_verified','preflight','remote_check','shared_files_changed','targets'},'Known complete native validation schema')
    required(receipt['validation'],{'preflight':'PASS','remote_check':'Pinned saved receipt verification; fresh network acceptance check remains root-owned.','shared_files_changed':0,'targets':40},'Native validation meaning')
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


PROGRAM_LOG=B/'RESEARCH_LOG.md'
ADDITIONAL_OWNED_MUTATION_PATHS={PROGRAM_LOG.relative_to(R).as_posix()}
OWNED_OPERATIONAL_LOGS=[('root_problem',A/'ROOT_RESEARCH_LOG.md'),('program',PROGRAM_LOG)]

def owned_mutation_path(name):
    relative(name)
    return name in NATIVE or name in ADDITIONAL_OWNED_MUTATION_PATHS or name.startswith(K.relative_to(R).as_posix()+'/') or name.startswith(A.relative_to(R).as_posix()+'/')

def protected_foreign_paths(fresh):
    paths=fresh['protected_foreign_tracked_paths'];require(type(paths) is list and all(type(n) is str for n in paths) and paths==sorted(set(paths)),'Exact sorted foreign identities')
    for name in paths:require(not owned_mutation_path(name),'Owned mutation path may never be declared protected foreign: '+name)
    return paths

def operational_log_note(clock):
    utc_clock(clock,'Actual finalization UTC')
    return '\n## '+clock+' — PR49 accepted credited known result\n\nWorkflow100%; discovery0%; original0/5,new0,audit0. Exact unrestricted Schwarz–Pick local circle-reflection criterion credited to Kraus/Roth/Ruscheweyh2007, prior DOI10.1007/s11854-007-0009-x; imported full journal proof not independently certified. Program39/180='+str(39*100/180)+'%; one present native mirror remains. Extensive AI use; unrefereed; no project solution, novelty, paper/newDOI/tracker/release.\n'


def owned_log_append_check(pre):
    foreign_check(pre);record=load(A/'integration_log_append_receipt.json');keyset(record,{'schema','utc','logs','note','source_preparation_did_not_append'},'Exact owned append receipt');required(record,{'schema':'pr49-owned-operational-log-appends/v1','source_preparation_did_not_append':True},'Actual append, not preparation mutation');final=load(A/'integration_finalization.json');note=operational_log_note(final['utc']);require(record['note']==note and type(record['logs']) is list and len(record['logs'])==2,'Only two authorized exact prefix appends')
    require(utc_clock(final['utc'],'Finalization')<=utc_clock(record['utc'],'Append')<=dt.datetime.now(dt.timezone.utc),'Append actual clock')
    for row,(label,path) in zip(record['logs'],OWNED_OPERATIONAL_LOGS):
        keyset(row,{'log','before','retained_preimage','after','before_worktree_mode','after_worktree_mode'},'Complete owned log identity and full modes')
        name=path.relative_to(R).as_posix();require(row['log']==name and row['before']['path']==name and row['after']['path']==name,'Exact authorized program/A48 log only')
        for k in ['before','retained_preimage','after']:exact_reference(row[k])
        retained=A/'integration_log_preimages'/(label+'.bin');require(row['retained_preimage']['path']==retained.relative_to(R).as_posix(),'Exact retained full prefix path');check(R,[row['retained_preimage'],row['after']]);prefix=regular(R,row['retained_preimage']['path']).read_bytes();require(len(prefix)==row['before']['bytes'] and sha(prefix)==row['before']['sha256'] and regular(R,name).read_bytes()==prefix+note.encode(),'Exact retained prefix plus fixed append, no rewrite')
        before=row['before_worktree_mode'];after=row['after_worktree_mode'];require(type(before) is int and type(after) is int and 0<=before<=0o7777 and before==after==stat.S_IMODE(regular(R,name).stat().st_mode),'Authorized full mode preserved')
    return record


def alias_QUEUE_absent(data):
    require(type(data) is bytes,'Whole QUEUE bytes required;49 has no related alias')


