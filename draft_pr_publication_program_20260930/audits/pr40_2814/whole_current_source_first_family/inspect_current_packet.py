"""Own strict current input inspection, without executing any packet program."""
from pathlib import Path, PurePosixPath
import collections, datetime, hashlib, json, subprocess

A = Path(__file__).resolve().parent.parent
C = A/'reviewed_candidate'
OUT = Path(__file__).resolve().parent
R = A.parents[2]
sha = lambda b: hashlib.sha256(b).hexdigest()

def need(v, message):
    if not v: raise ValueError(message)

def unique(items):
    d = {}
    for k,v in items: need(k not in d, 'Duplicate JSON key'); d[k] = v
    return d

def parse(b):
    return json.loads(b,object_pairs_hook=unique,
        parse_constant=lambda v: (_ for _ in ()).throw(ValueError('Nonfinite '+v)))

def read(p):
    need(p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents), 'Nonregular input')
    return p.read_bytes()

def row(p,root=A):
    b=read(p);return {'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':sha(b)}

def typed(v):
    if type(v) is dict: return ['dict', [[k,typed(w)] for k,w in sorted(v.items())]]
    if type(v) is list: return ['list',[typed(w) for w in v]]
    return [type(v).__name__,v]

def counts(v):
    result=collections.Counter({type(v).__name__:1})
    if type(v) is dict:
        for w in v.values(): result.update(counts(w))
    if type(v) is list:
        for w in v: result.update(counts(w))
    return dict(result)

def main():
    manifest_bytes=read(C/'MANIFEST.json')
    need(sha(manifest_bytes)=='8de92d903edaec7471f4ecc3df443b7e779732b0ee83cdec507c22025bfae25f','Exact actual current manifest')
    m=parse(manifest_bytes);need(m['self_excluded']==['MANIFEST.json'],'Only exact root self may exclude')
    names=[];jsons=[]
    for e in m['files']:
        n=e['path'];p=PurePosixPath(n)
        need(type(n) is str and str(p)==n and not p.is_absolute() and all(x not in ('','.','..') for x in n.split('/')),'Unsafe name')
        need(type(e['bytes']) is int and e['bytes']>=0 and e['mode']=='0444','Exact row type/mode')
        b=read(C/n);need(len(b)==e['bytes'] and sha(b)==e['sha256'],'Whole current member byte drift')
        need((C/n).stat().st_mode&0o777==0o444,'Physical current mode');names.append(n)
        if n.endswith('.json'):
            v=parse(b);jsons.append(dict(row(C/n,C),root_type=type(v).__name__,node_types=counts(v),typed_tree_sha256=sha(json.dumps(typed(v),separators=(',',':'),ensure_ascii=False).encode())))
    actual_files=[];actual_dirs=[]
    for p in C.rglob('*'):
        need(not p.is_symlink(),'Symlink in current')
        if p.is_file(): actual_files.append(p.relative_to(C).as_posix())
        else: need(p.is_dir(),'Special member');actual_dirs.append(p.relative_to(C).as_posix())
    need(len(names)==len(set(names))==m['files_count']==239,'Exact239')
    need(set(actual_files)==set(names)|{'MANIFEST.json'} and sorted(actual_dirs)==m['directories'],'Exact recursive current topology')
    need((C/'MANIFEST.json').stat().st_mode&0o777==0o444,'Root manifest444')
    snapshot=parse(read(A/'snapshot_manifest.json'))
    for e in snapshot['files']:
        source=read(A/'source_snapshot'/e['path'])
        need(read(C/e['path'])==source and read(C/'original_archive'/e['path'])==source,'Whole original root/archive')
    deps=parse(read(C/'CURRENT_PROOF_DEPENDENCIES.json'))
    need(deps['dependency_anchor_repository_relative']==A.relative_to(R).as_posix(),'Resolvable exact dependency anchor')
    copied=[]
    for e in deps['files']:
        b=read(A/e['path']);need(type(e['bytes']) is int and len(b)==e['bytes'] and sha(b)==e['sha256'],'Complete dependency bytes')
        n=e['path']
        if n.startswith(('primary_scope_family/','geodesic_geometry_family/','root_audit_SQL_qualification_family/')):dest='family_evidence/'+n
        elif n in ('snapshot_manifest.json','pr_input/metadata.json','pr_input/diff.patch'):dest='original_archive/'+n
        elif n.startswith('source_snapshot/'):continue
        else:dest='root_verification/'+n
        need(read(C/dest)==b,'Whole retained dependency copy');copied.append({'dependency':n,'current_copy':dest})
    need(read(C/'CURRENT_OVERVIEW.md')==read(A/'current_preparation_family/CURRENT_OVERVIEW_TEMPLATE.md'),'Whole current overview source')
    need(read(C/'CURRENT_PARTIAL_SCOPE_CERTIFICATE.md')==read(A/'ROOT_PARTIAL_SCOPE_CERTIFICATE.md'),'Whole scientific scope')
    common=parse(read(C/'status.json'))
    for n in ('acceptance.json','attempt.json','current_readiness.json','review/current_verdict.json'):
        need(typed(parse(read(C/n)))==typed(common),'Complete current status typed equality')
    for k,v in {'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_attempts_added':0,'verification_attempts_added':0}.items():
        need(type(common[k]) is int and common[k]==v,'Budget type/value')
    need(common['status']=='UNSOLVED' and common['source_hold'] is True and common['partial_valid'] is True,'Bounded current status')
    need(common['full_problem_solved'] is False and common['novelty_claimed'] is False and common['historical_verdict_transferred'] is False,'Scientific overpromotion')
    need(common['new_whole_current_gate']=='PENDING' and common['current_verdict'] is None,'Frozen current gate remains historically pending')
    need(all(common[k] is None for k in ('current_model','current_reasoning_effort','current_deadline_utc')),'Unavailable exposure nulls')
    cap_path=A/'root_current_freeze_actual_capture/CAPTURE.json';cap_bytes=read(cap_path)
    need(sha(cap_bytes)=='0b0fd559bd5d339d8686f3f2ff42f9074b3dba173c787aa09f46d839ae75e70d','Actual capture pin')
    cap=parse(cap_bytes);need(cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code']==0 and type(cap['pid']) is int and cap['pid']==80794,'Actual current launch')
    need(read(A/'root_current_freeze_actual_capture/prelaunch_source.py')==read(A/'current_preparation_family/prepare_current_packet.py'),'Full actual prelaunch code')
    streams=[]
    for channel in ('stdout','stderr'):
        e=cap[channel];p=cap_path.parent/e['path'];b=read(p)
        need(type(e['size']) is int and len(b)==e['size'] and sha(b)==e['sha256'],'Whole actual current stream');streams.append(row(p))
    stdout=parse(read(cap_path.parent/'stdout.bin'))
    need(stdout['manifest_sha256']==sha(manifest_bytes) and stdout['members']==239,'Actual stdout manifest/239')
    preimage=parse(read(A/'ROOT_CURRENT_INPUT_PREIMAGES.json'))
    need(typed(preimage['files'])==typed(cap['native_preimages'])==typed(deps['repository_preimages']),'Whole dated native row equality')
    need(preimage['current_head']==cap['current_head_before']==common['root_current_head']=='c7da3726e31648bf854f92d7fe1ea83b34a420d5','Dated HEAD binding')
    # Live differences are separately recorded; historical freeze rows stay fixed.
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=R,check=True,capture_output=True).stdout.decode().strip()
    live=[]
    for e in preimage['files']:
        b=read(R/e['path']);live.append({'path':e['path'],'observed_bytes':len(b),'observed_sha256':sha(b),'matches_dated_freeze':len(b)==e['size'] and sha(b)==e['sha256']})
    receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'WHOLE_CURRENT_BYTE_TYPE_TOPOLOGY_CHECKS_PASS',
        'inspector':row(Path(__file__)),'current_manifest':row(C/'MANIFEST.json'),'whole239_members_checked':True,'root_self_only_recursive_closure':True,
        'whole_original13_root_and_archive_exact':True,'complete_dependency_copies':copied,'whole_typed_current_JSON':jsons,
        'actual_current_capture':row(cap_path),'complete_actual_current_streams':streams,'genuine_actual_build':True,
        'whole_current_scientific_verdict':None,'current_frozen_gate':'PENDING','dated_native_rows_retained':preimage['files'],
        'dated_HEAD':preimage['current_head'],'live_HEAD_at_own_read':head,'live_native_observation':live,
        'integration_qualification':'Any later native/HEAD differences require an explicit dated root rebase at integration; do not rewrite the closed freeze receipts or broadly ignore differences.',
        'packet_program_or_old_verifier_executed_or_imported':False,'only_readonly_Git_HEAD_query':True,
        'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0}
    target=OUT/'CURRENT_PACKET_TYPED_BYTE_TOPOLOGY.json';need(not target.exists(),'Preserve earlier own result')
    target.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':receipt['status'],'whole_JSON':len(jsons),'current_members':239,'receipt_sha256':sha(read(target)),
        'live_native_differences':[r['path'] for r in live if not r['matches_dated_freeze']],'live_HEAD':head}))

if __name__=='__main__':main()
