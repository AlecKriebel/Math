#!/usr/bin/env python3
"""Independent full-byte/typed traversal. Never import or execute reviewed sources."""
import collections
import datetime as dt
import difflib
import gzip
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat
import tokenize

P=Path(__file__).resolve().parent
A=P.parent
R=A.parents[2]
V=A/'acceptance_preparation_family_v2'
PIN='5f73ee3594751d176ed206ac521558045b0783cfa8b932af1bdde633deacd9aa'
READ={}
CLOSURES=[]
sha=lambda b:hashlib.sha256(b).hexdigest()

def parse(b):
    def pairs(values):
        result={}
        for key,value in values:
            assert key not in result,('duplicate key',key)
            result[key]=value
        return result
    def floating(v):
        f=float(v)
        assert math.isfinite(f)
        return f
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,
                      parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))

def typed_counts(value):
    counts=collections.Counter()
    stack=[value]
    while stack:
        x=stack.pop()
        counts[type(x).__name__]+=1
        if type(x) is dict:stack.extend(x.values())
        elif type(x) is list:stack.extend(x)
    return dict(sorted(counts.items()))

def relative(n):
    p=PurePosixPath(n)
    assert type(n) is str and n and '\\' not in n and '\0' not in n
    assert not p.is_absolute() and p.as_posix()==n
    assert not {'.','..','.git','__pycache__'}.intersection(p.parts)
    return p

def read(path):
    path=Path(path)
    assert path.is_file() and not path.is_symlink()
    assert all(not q.is_symlink() for q in path.parents)
    raw=path.read_bytes()
    name=path.relative_to(R).as_posix()
    row={'path':name,'bytes':len(raw),'sha256':sha(raw),'worktree_mode':stat.S_IMODE(path.stat().st_mode)}
    if name in READ:
        assert all(READ[name][k]==row[k] for k in row),('input changed during inspection',name)
        return raw
    if path.suffix=='.json':
        value=parse(raw)
        row['typed_counts']=typed_counts(value)
        row['root_keyset']=sorted(value) if type(value) is dict else None
    elif path.suffix in {'.jsonl','.ndjson'}:
        assert not raw or raw.endswith(b'\n')
        total=collections.Counter()
        for line in raw.splitlines():total.update(typed_counts(parse(line)))
        row['typed_counts']=dict(sorted(total.items()))
        row['jsonl_records']=len(raw.splitlines())
    elif path.suffix=='.py':
        # Tokenization reads the complete source without compiling even an AST.
        tokens=list(tokenize.tokenize(io.BytesIO(raw).readline))
        row['source_tokens']=len(tokens)
        row['source_lines']=len(raw.splitlines())
        row['declared_functions']=[tokens[i+1].string for i,t in enumerate(tokens[:-1]) if t.type==tokenize.NAME and t.string=='def']
    READ[name]=row
    return raw

def row_check(root,rows,frozen=False):
    assert type(rows) is list and len({z['path'] for z in rows})==len(rows)
    for z in rows:
        relative(z['path'])
        size=z.get('bytes',z.get('size'))
        assert type(size) is int and size>=0
        if 'bytes' in z and 'size' in z:assert type(z['bytes']) is type(z['size']) and z['bytes']==z['size']
        assert type(z['sha256']) is str and len(z['sha256'])==64 and all(c in '0123456789abcdef' for c in z['sha256'])
        q=root/z['path'];raw=read(q)
        assert len(raw)==size and sha(raw)==z['sha256'],('binding differs',str(q))
        if frozen:assert stat.S_IMODE(q.stat().st_mode)==0o444,('frozen mode differs',str(q))

def exact(root,names):
    assert root.is_dir() and not root.is_symlink()
    files=set();dirs=set()
    for q in root.rglob('*'):
        relative(q.relative_to(root).as_posix())
        assert not q.is_symlink()
        if q.is_file():files.add(q.relative_to(root).as_posix())
        else:
            assert q.is_dir()
            dirs.add(q.relative_to(root).as_posix())
    expected={q.as_posix() for n in names for q in PurePosixPath(n).parents if q.as_posix()!='.'}
    assert files==set(names),('closure files differ',str(root),files^set(names))
    assert dirs==expected,('closure directories differ',str(root),dirs^expected)
    return sorted(dirs)

def closure(root,name,rows,pin=None,frozen=False):
    raw=read(root/name)
    if pin:assert sha(raw)==pin
    row_check(root,rows,frozen)
    dirs=exact(root,{z['path'] for z in rows}|{name})
    if frozen:assert stat.S_IMODE((root/name).stat().st_mode)==0o444
    CLOSURES.append({'root':root.relative_to(R).as_posix(),'manifest':name,'manifest_sha256':sha(raw),'members':len(rows),'exact_directories':dirs,'literal_0444_required':frozen})

def same(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

m=parse(read(V/'PREPARATION_MANIFEST.json'))
assert sha((V/'PREPARATION_MANIFEST.json').read_bytes())==PIN
assert m['self_excluded']==['PREPARATION_MANIFEST.json'] and m['files_count']==32
closure(V,'PREPARATION_MANIFEST.json',m['files'],PIN,True)
assert CLOSURES[-1]['exact_directories']==m['exact_directories']
inputs=parse(read(V/'INPUT_BINDINGS.json'))
for z in inputs['pins'].values():row_check(R,[z])
for c in inputs['closures']:
    closure(A/c['directory'],c['manifest_name'],c['members']+c['foreign_members'],c['manifest_sha256'],c.get('requires_all_members_0444') is True)
current=A/'reviewed_candidate';cm=parse(read(current/'MANIFEST.json'))
assert cm['files_count']==547 and cm['excluded']==['MANIFEST.json']
closure(current,'MANIFEST.json',cm['files'],'3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa',True)
deps=parse(read(current/'CURRENT_PROOF_DEPENDENCIES.json'))
assert len(deps['files'])==469 and deps['dependency_anchor_repository_relative']==A.relative_to(R).as_posix()
row_check(A,deps['files'])
whole=A/'whole_current_source_first_family';wm=parse(read(whole/'FIRST_PARTY_MANIFEST.json'))
assert len(wm['files'])==143 and len(wm['foreign_files'])==17
assert not {z['path'] for z in wm['files']}.intersection(z['path'] for z in wm['foreign_files'])
closure(whole,'FIRST_PARTY_MANIFEST.json',wm['files']+wm['foreign_files'],inputs['whole_observed_only']['sha256'],True)
row_check(R,[inputs['root_whole_observed']])
root_whole=parse(read(R/inputs['root_whole_observed']['path']))
assert same(root_whole['whole_independent_verdict'],parse(read(whole/'RESULT.json')))
adv=A/'acceptance_static_adversary_family'
am=parse(read(adv/'FIRST_PARTY_MANIFEST.json'))
foreign=am['individual_external_foreign_dependencies_excluded_from_authored_copy']
assert len(foreign)==46
row_check(R,foreign)
for z in foreign:assert stat.S_IMODE((R/z['path']).stat().st_mode)==z['worktree_mode']

helpers=['pr41_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']
deltas=[]
for name in helpers:
    old=read(A/'acceptance_preparation_family'/name).decode()
    new=read(V/name).decode()
    deltas.extend(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='closed_v1/'+name,tofile='proposed_v2/'+name))
assert ''.join(deltas).encode()==read(V/'SOURCE_DELTAS.patch')
row_check(V,parse(read(V/'REVISION_SOURCE_BINDINGS.json'))['repaired_sources'])
for name in ['SCIENTIFIC_SCOPE.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FUTURE_GATE_PINS.json']:
    assert read(V/name)==read(A/'acceptance_preparation_family'/name)
mirror=R/'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py'
assert sha(read(mirror))=='ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
snap=parse(read(A/'snapshot_manifest.json'))
assert len(snap['files'])==16 and len(snap['changed_paths'])==17
row_check(A/'source_snapshot',snap['files'])
original_dirs=exact(A/'source_snapshot',{z['path'] for z in snap['files']})
assert len(read(A/'pr_input/diff.patch'))==201709
assert sha(read(current/'PROOF.md'))=='464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c'
assert sha(read(current/'turns.json'))=='bd0a82165c3ac81f7a7d35ace164f20ecb87e6b73a9155815e4eecac655a2549'
turns=parse(read(current/'turns.json'))
assert type(turns) is list and len(turns)==2 and [z['turn'] for z in turns]==[1,2] and all(type(z['turn']) is int for z in turns)
prior=parse(read(current/'prior_report.json'));assert type(prior) is dict and prior
scope=parse(read(V/'SCIENTIFIC_SCOPE.json'));draft=parse(read(V/'DRAFT_FINAL_PLAN.json'))
assert same(scope,draft['scientific_scope']) and draft['partial_valid'] is False and draft['preparation_manifest_sha256'] is None
assert scope['full_problem_solved'] is False and scope['novelty_claimed'] is False and scope['human_peer_review_asserted'] is False

# Publication recovery is adjacent qualification, never substituted authority.
pub=A/'acceptance_static_adversary_publication_qualification'
pm=parse(read(pub/'MANIFEST.json'))
pr=pm['files']
row_check(pub,pr)
exact(pub,{z['path'] for z in pr}|{'MANIFEST.json'})
compressed=read(pub/'COMPLETE_TYPED_NODES.jsonl.gz')
original=read(adv/'COMPLETE_TYPED_NODES.jsonl')
assert gzip.decompress(compressed)==original
qualification=parse(read(pub/'QUALIFICATION.json'))
assert sha(original)==qualification['original_raw_file']['sha256']
recovery={'compressed_bytes':len(compressed),'compressed_sha256':sha(compressed),'original_bytes':len(original),'original_sha256':sha(original),'lossless_recovery_verified':True,'original_local_bytes_not_changed':True,'qualification_is_not_new_acceptance_authority':True}

# Bind actual predecessor records as observations; no future fresh root pins assumed.
previous=R/'draft_pr_publication_program_20260930/audits/pr40_2814'
prev=parse(read(previous/'state_mirror_bindings.json'));post=parse(read(previous/'post_acceptance_verification.json'))
assert len(prev['entries'])==30 and 40 in prev['required_completed_prs'] and 41 not in prev['required_completed_prs']
for k,v in {'status':'PASS','pr':40,'targets':31,'consumed_substantive_turns':37,'primary_acceptances':30,'program_completed_count':30,'fresh_native_mirror_noop':True}.items():assert same(post[k],v)

result={'schema':'pr41-independent-v2-source-full-input-inspection/v1','status':'PASS_FULL_BYTE_TYPED_READ_STATIC_BINDING_INSPECTION','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'reviewed_preparation_manifest_sha256':PIN,'files':sorted(READ.values(),key=lambda z:z['path']),'unique_full_files':len(READ),'full_bytes_read':sum(z['bytes'] for z in READ.values()),'typed_nodes_seen':sum(sum(z.get('typed_counts',{}).values()) for z in READ.values()),'exact_closures':CLOSURES,'current_members':547,'dependency_members':469,'whole_authored_members':143,'whole_foreign_members':17,'prior_adversary_foreign_dependencies':46,'source_delta_exact':True,'mirror_source_sha256':sha(mirror.read_bytes()),'original16_checked':True,'original17_path_diff_bytes':201709,'actual_PR40_records_observed':True,'lossless_publication_qualification':recovery,'candidate_helpers_imported_compiled_or_executed':False,'scientific_helpers_reexecuted':False,'future_external_ROOT_bindings_plan_final_capture_status':'NOT_CERTIFIED','future_fresh13_native_runtime_status':'NOT_CERTIFIED','native_canonical_Git_index_remote_shared_writes':False,'external_human_contact':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'review_completion_estimate_percent':65,'actual_acceptance_execution_estimate_percent':0,'unconditional_discovery_estimate_percent':0}
target=P/'INPUT_INSPECTION_RESULT.json';assert not target.exists();target.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','actual_pid','unique_full_files','full_bytes_read','typed_nodes_seen','source_delta_exact','candidate_helpers_imported_compiled_or_executed']},indent=2))
