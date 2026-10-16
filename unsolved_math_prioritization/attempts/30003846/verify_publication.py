#!/usr/bin/env python3
"""Strict release validator. Execute only through the externally pinned bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'BOOTSTRAP.py', 'CONNECTED_RECONSTRUCTION.md', 'HARDENING.json', 'HARDENING.patch', 'HARDENING_REPLAY.json', 'HISTORICAL_CONNECTED_AUDIT.md', 'INDEPENDENT_REVIEW.md', 'MUTATION_TESTS.py', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_HISTORY.json', 'PREPARATION_STAGE.json', 'PRIOR_OUTPUT_COMPARISON.json', 'PROVENANCE.json', 'PUBLICATION_MANIFEST.json', 'QUEUE_BINDING.json', 'README.md', 'REFERENCE_CAPTURE.json', 'SCOPE_AUDIT.md', 'SCOPE_STATUS_CORRECTION.patch', 'SOURCE_METADATA.json', 'check_combinatorics.py', 'check_combinatorics.reference.stderr', 'check_combinatorics.reference.stdout', 'check_reduction.py', 'check_reduction.reference.stderr', 'check_reduction.reference.stdout', 'independent_controls.py', 'independent_controls.reference.stderr', 'independent_controls.reference.stdout', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'base_support': 'finite', 'connected_classification': 'PASS_WITH_EXPLICIT_IMPORTS', 'credited_author': 'Gili Golan', 'credited_source': 'https://arxiv.org/abs/2607.10961v1', 'credited_submission_date': '2026-07-12', 'decision': 'CONDITIONAL_PRIOR_PROOF_VERIFIED_SCOPE_HOLD', 'decomposition': 'PASS_INDEPENDENTLY_REVIEWED_RESTRICTED_PERMUTATIONAL_NONFAITHFUL_ALLOWED', 'faithful_action_only_exclusion_certified': False, 'indexing_action_faithfulness_required': False, 'journal_acceptance_established': False, 'new_proof_search_attempts': 0, 'novelty_claim': False, 'original_questions_71_72': 'CONDITIONAL_ON_STATED_RESTRICTED_PERMUTATIONAL_INTERPRETATION', 'problem_id': 30003846, 'question109_certified': False, 'queue_status': 'queued', 'queue_turns': '0/5', 'regular_only_exclusion_certified': False, 'schema': 1, 'top_group_replaced_by_permutation_image': False, 'unconditional_original_acceptance': False}
EXPECTED_QUEUE = {'after': {'bytes': 397785, 'sha256': 'fac278d72caa7fcfe95c64ddde331c25c1427bb91559b91e52ff30858629bb4a'}, 'before': {'bytes': 397331, 'git_blob_sha1': '6f68342c8f57a413ba2535d8b20fb49915d5898c', 'sha256': '25fdcea7fdcb23109e4b46ba2b560dcff02c18aeed35899c4d89375e3de6cdfe'}, 'changed_split_column': 11, 'findings': 'Prior proof verified conditionally: Golan, arXiv:2607.10961v1 (July 2026 preprint), connected classification plus independently accepted decomposition under restricted permutational wreath products (finite support; nonfaithful indexing action allowed). Scope hold: original wreath terminology undefined; regular-only/faithful-only exclusions not certified. No new attempt; no novelty or journal-acceptance claim. [Audit](attempts/30003846/ACCEPTANCE.md).', 'status': 'queued', 'status_split_column': 8, 'target': '30003846 / OWR-16167-016', 'turns': '0/5', 'turns_split_column': 9}
EXPECTED_REFERENCE = {'check_combinatorics.py': {'stdout': {'bytes': 1323, 'sha256': '08d0960c6540aa4992fc79b5193a599d3238af6d6d4fc7cfbbd0a5b03dc2899a'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, 'check_reduction.py': {'stdout': {'bytes': 948, 'sha256': '4d578bf0807520afad8d676c30f85ae8d8f58eb2ed2a46ce21351f2eaf78c17d'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, 'independent_controls.py': {'stdout': {'bytes': 2009, 'sha256': '9f741e12f8a51b7c0039c8cb8a5ebb889ad639f9a97b84d32f696f14f8310703'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}
SCRIPTS = ('check_combinatorics.py','check_reduction.py','independent_controls.py')
MAX_BYTES=2000000
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
    if not ok:raise ValueError(message)
def same(a,b):
    if type(a) is not type(b):return False
    if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
    if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def unique(pairs):
    result={}
    for k,v in pairs:
        need(k not in result,'duplicate JSON key');result[k]=v
    return result
def nonfinite(token):raise ValueError('nonfinite JSON')
def number(token):
    x=float(token);need(math.isfinite(x),'overflow JSON');return x
def parse(raw):return json.loads(raw,object_pairs_hook=unique,parse_constant=nonfinite,parse_float=number)
def keys(x,wanted):need(type(x) is dict and set(x)==set(wanted),'object schema')
def integer(x):need(type(x) is int and 0<=x<=MAX_BYTES,'bounded exact integer')
def digest(x):need(type(x) is str and re.fullmatch('[0-9a-f]{64}',x) is not None,'SHA-256')
def ordinary(path):
    for p in path.parents:need(stat.S_ISDIR(p.lstat().st_mode),'linked ancestor')
    st=path.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1 and st.st_size<=MAX_BYTES,'ordinary bounded single-link file')
    with os.fdopen(os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)),'rb') as f:
        fs=os.fstat(f.fileno());need((st.st_dev,st.st_ino,st.st_size)==(fs.st_dev,fs.st_ino,fs.st_size),'replaced file');raw=f.read(MAX_BYTES+1)
    need(len(raw)==st.st_size,'changed size');return raw
def inventory(root):
    for p in (root,*root.parents):need(stat.S_ISDIR(p.lstat().st_mode),'linked root or ancestor')
    entries=list(os.scandir(root));need({e.name for e in entries}==FILES,'exact flat inventory')
    need(all(stat.S_ISREG(e.stat(follow_symlinks=False).st_mode) for e in entries),'linked or special member')
def validate_manifest(m,snapshot):
    keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30003846,'manifest problem')
    need(type(m['files']) is list and len(m['files'])==len(PAYLOAD),'manifest inventory length');seen=set()
    for row in m['files']:
        keys(row,['path','bytes','sha256']);n=row['path'];need(type(n) is str and n in PAYLOAD and n not in seen,'manifest path');seen.add(n)
        integer(row['bytes']);digest(row['sha256']);need(same(row,dict(path=n,bytes=len(snapshot[n]),sha256=sha(snapshot[n]))),'manifest member binding')
    need(seen==PAYLOAD,'complete manifest')
def validate_acceptance(a):need(same(a,EXPECTED_ACCEPTANCE),'exact conditional acceptance')
def validate_queue_binding(q):need(same(q,EXPECTED_QUEUE),'exact queue binding schema')
def validate_queue_pair(before,after):
    for tag,raw in [('before',before),('after',after)]:
        need(type(raw) is bytes,'queue bytes');need(len(raw)==EXPECTED_QUEUE[tag]['bytes'] and sha(raw)==EXPECTED_QUEUE[tag]['sha256'],'actual '+tag+' QUEUE byte binding')
    return validate_queue_delta(before,after)
def validate_queue_delta(before,after):
    a=before.splitlines(keepends=True);b=after.splitlines(keepends=True);need(len(a)==len(b),'queue line count')
    hits=[i for i,line in enumerate(a) if b'| 30003846 / OWR-16167-016 |' in line]
    need(len(hits)==1,'unique target');i=hits[0]
    need(all(x==y for j,(x,y) in enumerate(zip(a,b)) if j!=i),'unrelated queue line')
    x=a[i].split(b'|');y=b[i].split(b'|');need(len(x)==len(y)==14,'queue columns')
    need([j for j,(u,v) in enumerate(zip(x,y)) if u!=v]==[11],'only Findings column')
    need(x[8]==y[8]==b' queued ' and x[9]==y[9]==b' 0/5 ','unchanged queue status and turns')
    need(y[11]==b' '+EXPECTED_QUEUE['findings'].encode()+b' ','exact Findings')
    return dict(target=EXPECTED_QUEUE['target'],before=EXPECTED_QUEUE['before'],after=EXPECTED_QUEUE['after'],changed_split_columns=[11],all_other_bytes_preserved=True)
def normalized(raw):
    obj=parse(raw);need(type(obj) is dict and 'elapsed_seconds' in obj,'elapsed key')
    elapsed=obj['elapsed_seconds'];need(type(elapsed) is float and math.isfinite(elapsed) and elapsed>=0,'finite nonnegative float elapsed')
    pattern=rb'(?m)^  "elapsed_seconds": ([0-9]+\.[0-9]+(?:[eE][+-]?[0-9]+)?),(?=\n)'
    matches=list(re.finditer(pattern,raw));need(len(matches)==1,'one exact top-level elapsed token')
    m=matches[0];need(float(m.group(1))==elapsed,'elapsed token and parsed value')
    obj['elapsed_seconds']='<elapsed_seconds>'
    return raw[:m.start(1)]+b'<elapsed_seconds>'+raw[m.end(1):],obj
def compare_output(script,stdout,stderr,refout,referr):
    need(script in SCRIPTS,'known script');need(type(stdout) is bytes and type(stderr) is bytes,'output bytes')
    for kind,raw in [('stdout',refout),('stderr',referr)]:need(same(dict(bytes=len(raw),sha256=sha(raw)),EXPECTED_REFERENCE[script][kind]),'reference identity')
    actual_bytes,actual_obj=normalized(stdout);reference_bytes,reference_obj=normalized(refout)
    need(actual_bytes==reference_bytes and same(actual_obj,reference_obj),'full output comparison except elapsed token')
    need(stderr==referr,'full stderr equality')
    return dict(script=script,exit_code=0,stdout=stdout.decode(),stderr=stderr.decode(),stdout_bytes=len(stdout),stdout_sha256=sha(stdout),stderr_bytes=len(stderr),stderr_sha256=sha(stderr),complete_output_comparison=True,recursive_exact_type_comparison=True,normalization='Only the single top-level elapsed_seconds numeric token; raw outputs above are unchanged')
def integrity(root,before_path,after_path,mp,bp):
    digest(mp);digest(bp);inventory(root);snap={n:ordinary(root/n) for n in FILES}
    need(sha(snap['PUBLICATION_MANIFEST.json'])==mp,'external manifest pin');need(sha(snap['BOOTSTRAP.py'])==bp,'external bootstrap pin')
    validate_manifest(parse(snap['PUBLICATION_MANIFEST.json']),snap)
    parsed={n:parse(raw) for n,raw in snap.items() if n.endswith('.json')}
    validate_acceptance(parsed['ACCEPTANCE.json']);validate_queue_binding(parsed['QUEUE_BINDING.json'])
    for n in FILES:
        if n.endswith('.py'):need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(snap[n]))),'assertion-free delivery code')
    before=ordinary(before_path);after=ordinary(after_path);q=validate_queue_pair(before,after)
    for n in SCRIPTS:
        tag=n.removesuffix('.py');compare_output(n,snap[tag+'.reference.stdout'],snap[tag+'.reference.stderr'],snap[tag+'.reference.stdout'],snap[tag+'.reference.stderr'])
    return snap,before,after,q
def readonly(root,before,after):
    rows=[]
    for p,label,d in [(root,'.',True)]+[(root/n,n,False) for n in sorted(FILES)]+[(before,'actual QUEUE before',False),(after,'actual QUEUE after',False)]:
        need((p.stat().st_mode&0o777)==(0o555 if d else 0o444) and not os.access(p,os.W_OK),'read-only permissions')
        try:fd=os.open(p/'FORBIDDEN_CREATE' if d else p,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if d else os.O_APPEND),0o600)
        except PermissionError as e:
            need(e.errno==13,'physical denial errno');rows.append(dict(path=label,operation='create' if d else 'append_open',errno=13,denied=True))
        else:os.close(fd);raise ValueError('physical write unexpectedly allowed')
    return rows
def main():
    need(len(sys.argv)==6,'manifest pin, bootstrap pin, packet, before and after QUEUE required')
    mp,bp,rs,bs,afs=sys.argv[1:];root=Path(os.path.abspath(rs));before_path=Path(os.path.abspath(bs));after_path=Path(os.path.abspath(afs))
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'isolated no-site no-bytecode')
    initial=integrity(root,before_path,after_path,mp,bp);snap=initial[0];probes=readonly(root,before_path,after_path)
    mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]
    runner="import sys,runpy;sys.path.insert(0,sys.argv[1]);runpy.run_path(sys.argv[1]+'/'+sys.argv[2],run_name='__main__')"
    records=[]
    for script in SCRIPTS:
        r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',runner,str(root),script],cwd=root,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=900)
        need(r.returncode==0,'fresh suite process failed');tag=script.removesuffix('.py');records.append(compare_output(script,r.stdout,r.stderr,snap[tag+'.reference.stdout'],snap[tag+'.reference.stderr']))
    need(integrity(root,before_path,after_path,mp,bp)==initial,'whole delivery or queue changed')
    print(json.dumps(dict(schema=1,problem_id=30003846,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,queue=initial[3],physical_denials=probes,replays=records,whole_delivery_unchanged=True,source_body_replay='NOT_RUN',dataset_replay='NOT_RUN',original_full_checker_replay='NOT_RUN',mathematics_scope='conditional prior-proof verification; original terminology hold'),sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
