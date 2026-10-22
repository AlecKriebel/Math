#!/usr/bin/env python3
"""Strict scope-delivery validator. Execute only through the externally pinned bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'BOOTSTRAP.py', 'COMPARISON_SCOPE_AUDIT.md', 'COMPARISON_SCOPE_CORRECTION.patch', 'MUTATION_TESTS.py', 'PATCH_HISTORY.json', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PUBLICATION_MANIFEST.json', 'QUEUE_BINDING.json', 'README.md', 'SOURCE_METADATA.json', 'check_scope.mode0.reference.stderr', 'check_scope.mode0.reference.stdout', 'check_scope.mode1.reference.stderr', 'check_scope.mode1.reference.stdout', 'check_scope.mode2.reference.stderr', 'check_scope.mode2.reference.stdout', 'check_scope.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'affine_filtered_mechanism': 'Existing HRW multiplicative filtered comparison; conditional on the recorded completed-cobar interpretation', 'canonical_problem_id': 30004167, 'coefficient_twist': 'BK generator epsilon^(-1); tensor-power i generator epsilon^(-i)', 'companion_queue_row_changed': False, 'completed_comodule_ext_category': 'VERIFICATION_REQUIRED', 'dataset_replay': 'NOT_RUN', 'decision': 'PRIMARY_OVERLAP_CONDITIONAL_AFFINE_APPLICATION_GLOBAL_SCOPE_HOLD', 'full_affine_source_formulation_certified': False, 'full_global_target_certified': False, 'global_local_hypotheses': 'SPECIAL_FIBER_LCI_ALONE_NOT_CERTIFIED', 'guo_relative_tp_coefficients_explicitly_included': True, 'imported_theorem_proof_replay': 'NOT_RUN', 'new_proof_claim': False, 'new_proof_search_attempts': 0, 'novelty_claim': False, 'p_flatness_necessary': False, 'p_flatness_sufficient_route': True, 'queue_status': 'queued', 'queue_turns': '0/5', 'schema': 1, 'shared_targets': [30004167, 30004168], 'source_body_replay': 'NOT_RUN', 'spectral_sequence_page_conventions': 'VERIFICATION_REQUIRED', 'validation_scope': 'Delivered metadata, stated scope, authored correction history, inventory, actual queue bytes, and exact output comparisons only'}
EXPECTED_QUEUE = {'after': {'bytes': 397788, 'sha256': '5867133a8eb446d3a6c1d743a2e8267743b96d1604bc6ba9406684119d98f668'}, 'before': {'bytes': 397331, 'git_blob_sha1': '6f68342c8f57a413ba2535d8b20fb49915d5898c', 'sha256': '25fdcea7fdcb23109e4b46ba2b560dcff02c18aeed35899c4d89375e3de6cdfe'}, 'changed_split_column': 11, 'findings': 'Shared primary-literature overlap / scope hold (30004167–30004168): HRW supplies the existing conditional affine multiplicative filtered comparison; exact completed-comodule Ext, twist and page conventions remain to verify. Global lci-special-fiber wording does not certify modern local hypotheses; p-flatness is sufficient, not necessary. Guo TP coefficients included. No new result or attempt; queued 0/5. [Scope audit](attempts/30004167/ACCEPTANCE.md).', 'preserved_companion': '30004168 / OWR-16941-009', 'status': 'queued', 'status_split_column': 8, 'target': '30004167 / OWR-16941-008', 'turns': '0/5', 'turns_split_column': 9}
EXPECTED_REFERENCE = {'0': {'stdout': {'bytes': 6325, 'sha256': '08b30bb30296e55cd6dad9f56de1b2960753c6655295315bdc112147d79d5514'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 6325, 'sha256': '41dfcc58e7f3a8b5f4f3b4d33dc1c27a43a3251c4890fffc0a19542d34518c6a'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 6325, 'sha256': 'f66fe814e44510fd8531bf8303a9de24695a1e05c69ffa2b89e98888af02a428'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}
SCRIPTS = ('check_scope.py',)
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
    keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30004167,'manifest problem')
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
    hits=[i for i,line in enumerate(a) if b'| 30004167 / OWR-16941-008 |' in line]
    need(len(hits)==1,'unique target');i=hits[0]
    need(all(x==y for j,(x,y) in enumerate(zip(a,b)) if j!=i),'unrelated queue line')
    companion=[j for j,line in enumerate(a) if b'| 30004168 / OWR-16941-009 |' in line];need(len(companion)==1 and a[companion[0]]==b[companion[0]],'untouched companion row')
    x=a[i].split(b'|');y=b[i].split(b'|');need(len(x)==len(y)==14,'queue columns')
    need([j for j,(u,v) in enumerate(zip(x,y)) if u!=v]==[11],'only Findings column')
    need(x[8]==y[8]==b' queued ' and x[9]==y[9]==b' 0/5 ','unchanged queue status and turns')
    need(y[11]==b' '+EXPECTED_QUEUE['findings'].encode()+b' ','exact Findings')
    return dict(target=EXPECTED_QUEUE['target'],before=EXPECTED_QUEUE['before'],after=EXPECTED_QUEUE['after'],changed_split_columns=[11],all_other_bytes_preserved=True)
def compare_output(script,stdout,stderr,refout,referr):
    need(script in SCRIPTS,'known script');need(type(stdout) is bytes and type(stderr) is bytes,'output bytes')
    mode=str(sys.flags.optimize)
    for kind,raw in [('stdout',refout),('stderr',referr)]:need(same(dict(bytes=len(raw),sha256=sha(raw)),EXPECTED_REFERENCE[mode][kind]),'mode-specific reference identity')
    need(stdout==refout and stderr==referr,'complete stdout/stderr byte equality')
    need(same(parse(stdout),parse(refout)),'recursive exact output types')
    return dict(script=script,exit_code=0,stdout=stdout.decode(),stderr=stderr.decode(),stdout_bytes=len(stdout),stdout_sha256=sha(stdout),stderr_bytes=len(stderr),stderr_sha256=sha(stderr),complete_output_comparison=True,recursive_exact_type_comparison=True,normalization='NONE')
def refname(kind):return 'check_scope.mode'+str(sys.flags.optimize)+'.reference.'+kind
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
        compare_output(n,snap[refname('stdout')],snap[refname('stderr')],snap[refname('stdout')],snap[refname('stderr')])
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
        need(r.returncode==0,'fresh suite process failed');records.append(compare_output(script,r.stdout,r.stderr,snap[refname('stdout')],snap[refname('stderr')]))
    need(integrity(root,before_path,after_path,mp,bp)==initial,'whole delivery or queue changed')
    print(json.dumps(dict(schema=1,problem_id=30004167,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,queue=initial[3],physical_denials=probes,replays=records,whole_delivery_unchanged=True,source_body_replay='NOT_RUN',dataset_replay='NOT_RUN',imported_theorem_proof_replay='NOT_RUN',mathematics_scope='conditional affine prior-theorem application; global/category/page scope hold; metadata validation only'),sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
