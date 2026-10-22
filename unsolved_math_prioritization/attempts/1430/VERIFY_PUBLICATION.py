#!/usr/bin/env python3
"""Source-free, externally authenticated replay of accepted corrected partials."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,json,math,os,re,stat,subprocess,sys,tempfile
EXPECTED_MANIFEST='bc46b9d008b2635e991702f807f0e100c1e6f6b070e112c191c5b4a336738ff0'
AUDIT_PIN='c003b1e3bdae387ddf7b85da18f31778dc2b47efeda369a6612cde45473e2064'
AUTHOR_PIN='14f71c06b96e52cf76c99fa546e7698266f0e3d7ba05de940a02a053733fee15'
BOOT_PIN='b0d07f67ea355b51085aaaeeb42a00d47a367529514e4c8e426cb4b7463e549a'
class Reject(Exception):pass
def need(c,m):
    if not c:raise Reject(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(ps):
    d={}
    for k,v in ps:need(k not in d,'duplicate JSON key');d[k]=v
    return d
def constant(x):raise Reject('nonfinite JSON constant')
def finite(x):
    v=float(x);need(math.isfinite(v),'nonfinite JSON float');return v
def load(b):
    need(len(b)<=2000000,'JSON size limit')
    return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=finite)
def safe(n):return type(n) is str and bool(n) and '\\' not in n and not n.startswith('/') and all(re.fullmatch('[A-Za-z0-9_.-]+',x) and x not in ('.','..') for x in n.split('/'))
def exact(v,expected,name):need(type(v) is type(expected) and v==expected,'exact scope: '+name)
def read(p,limit=2000000):
    st=p.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'nonregular or hardlinked file')
    need(stat.S_IMODE(st.st_mode) in (0o444,0o644),'unsafe file mode');need(st.st_size<=limit,'oversized file')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        a=os.fstat(fd);need((a.st_dev,a.st_ino)==(st.st_dev,st.st_ino),'changed file identity')
        with os.fdopen(fd,'rb',closefd=False) as f:b=f.read(limit+1)
        z=os.fstat(fd);need((a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_size,z.st_mtime_ns,z.st_ctime_ns) and len(b)==st.st_size,'unstable file')
    finally:os.close(fd)
    return b
def inventory(root):
    for p in [root,*root.parents]:need(not p.is_symlink(),'symlink in root ancestry')
    need(root.is_dir(),'invalid root');out={};dirs=set()
    def visit(d,prefix):
        need(stat.S_IMODE(d.stat().st_mode) in (0o555,0o755),'unsafe directory mode')
        for e in os.scandir(d):
            n=prefix+e.name;need(safe(n),'unsafe filesystem name');mode=e.stat(follow_symlinks=False).st_mode
            need(not stat.S_ISLNK(mode),'symlink member')
            if stat.S_ISDIR(mode):dirs.add(n);visit(Path(e.path),n+'/')
            else:out[n]=read(Path(e.path))
    visit(root,'');return out,dirs
def entries(rows,files,expected):
    need(type(rows) is list and 1<=len(rows)<=100,'manifest inventory type/count')
    for e in rows:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');n=e['path'];need(safe(n) and n not in expected,'unsafe or duplicate path');expected.add(n)
        need(n in files,'missing file');need(type(e['bytes']) is int and 0<=e['bytes']<=2000000 and len(files[n])==e['bytes'],'byte count')
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(files[n])==e['sha256'],'digest')
    need(set(files)==expected,'exact file inventory')
def authenticate(root):
    f,dirs=inventory(root);need('PUBLICATION_MANIFEST.json' in f,'missing manifest');raw=f['PUBLICATION_MANIFEST.json'];need(sha(raw)==EXPECTED_MANIFEST,'manifest external pin');m=load(raw)
    need(type(m) is dict and set(m)=={'schema','problem_id','rank','disposition','turns','files'},'manifest schema')
    for k,v in [('schema','word-representation-publication-manifest-v1'),('problem_id',1430),('rank',1015),('disposition','unsolved'),('turns',5)]:exact(m[k],v,k)
    entries(m['files'],f,{'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'})
    need(dirs=={str(p) for n in f for p in PurePosixPath(n).parents if str(p)!='.'},'exact directory inventory')
    need(f['VERIFY_PUBLICATION.py']==read(Path(__file__)),'different verifier copy')
    for n,b in f.items():
        if n.endswith('.json'):load(b)
    return f
def semantics(f):
    data={n.removeprefix('accepted/'):b for n,b in f.items() if n.startswith('accepted/')}
    need(len(data)==25 and sum(map(len,data.values()))==205180,'accepted candidate count/bytes')
    for n,h in [('AUDIT_MANIFEST.json',AUDIT_PIN),('freeze/AUTHOR_MANIFEST.json',AUTHOR_PIN),('freeze/bootstrap.py',BOOT_PIN)]:need(sha(data[n])==h,'accepted external pin')
    audit=load(data['AUDIT_MANIFEST.json']);exact(audit['problem_id'],1430,'audit problem');exact(audit['approaches_used'],5,'audit turns');exact(audit['verdict'],'accept corrected packet as unresolved','audit verdict')
    entries(audit['files'],data,{'AUDIT_MANIFEST.json'})
    packet={n.removeprefix('packet/'):b for n,b in data.items() if n.startswith('packet/')};m=load(data['freeze/AUTHOR_MANIFEST.json'])
    exact(m['problem_id'],1430,'author problem');exact(m['status'],'unsolved','author status');exact(m['approaches_used'],5,'author turns');entries(m['files'],packet,set())
    need(len(packet)==11 and sum(map(len,packet.values()))==85362,'corrected payload count/bytes')
    pins=load(data['EXTERNAL_PINS.json']);need(pins==audit['corrected_pins'],'accepted pins disagreement')
    for k,v in [('problem_id',1430),('payload_files',11),('payload_bytes',85362),('manifest_sha256',AUTHOR_PIN),('bootstrap_sha256',BOOT_PIN),('diagnostics_sha256',sha(packet['DIAGNOSTICS.json']))]:exact(pins[k],v,k)
    ledger=load(packet['ATTEMPT_LEDGER.json'])
    for k,v in [('problem_id',1430),('rank',1015),('code','GRAPH-043'),('status','unsolved'),('approaches_used',5),('budget',5)]:exact(ledger[k],v,k)
    need(type(ledger['approaches']) is list and len(ledger['approaches'])==5,'ledger five approaches')
    for i,e in enumerate(ledger['approaches'],1):exact(e['number'],i,'approach number');exact(e['status'],'partial, target not closed','approach status')
    for k in ['general_resolution','novelty','formal_certification']:exact(ledger['claims'][k],False,k)
    exact(ledger['claims']['independent_audit_completed'],True,'audit completed')
    # Historical claims.remote_writes remains the accepted pre-publication value.
    exact(ledger['claims']['remote_writes'],False,'historical remote writes')
    for n,k,count in [('packet/DIAGNOSTICS.json','checks',89818),('audit/INDEPENDENT_RESULTS.json','checks',313309)]:
        o=load(data[n]);exact(o['problem_id'],1430,'diagnostic identity');exact(o['status'],'PASS','diagnostic status');exact(o[k],count,'bounded check count')
    for n in ['audit/ORIGINAL_REPLAY.json','audit/CORRECTED_REPLAY.json']:
        r=load(data[n]);exact(r['total_runs'],84,'historical replay runs');exact(r['original_snapshot_unchanged'],True,'historical replay immutability')
    return data
def invoke(script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')};env.update(PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1')
    p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*map(str,args)],cwd=script.parent,env=env,capture_output=True,timeout=300)
    need(p.returncode==0 and not p.stderr,'replay failed: '+script.name);return p.stdout

def permissions(root,readonly):
    root.chmod(0o755)
    for p in root.rglob('*'):p.chmod((0o555 if p.is_dir() else 0o444) if readonly else (0o755 if p.is_dir() else 0o644))
    root.chmod(0o555 if readonly else 0o755)
def primary_rehash(data,a):
    out={k:'NOT_RUN' for k in ['sources','corpora','record_join','fresh_retrieval','fresh_source_inspection','external_Lean_build','external_certificate_reproduction']}
    if a.source_dir is not None:
        for p in [a.source_dir,*a.source_dir.parents]:need(not p.is_symlink(),'source directory symlink')
        need(a.source_dir.is_dir(),'source directory absent');matched=[]
        for e in load(data['packet/SOURCE_METADATA.json'])['sources']:
            if 'sha256' not in e:continue
            b=read(a.source_dir/(e['id']+'.pdf'),10000000);need((len(b),sha(b))==(e['bytes'],e['sha256']),'source rehash mismatch');matched.append(e['id'])
        need(len(matched)==8,'source metadata count');out.update(sources='PASS_CURRENT_LOCAL_REHASH',source_ids=matched)
    if a.problems is not None:
        matched=[]
        for p,e in zip([a.problems,a.research_results],load(data['packet/CORPUS_VERIFICATION.json'])['corpora']):
            b=read(p,150000000);need((len(b),sha(b))==(e['bytes'],e['sha256']),'corpus rehash mismatch');matched.append(e['public_dataset_name'])
        out.update(corpora='PASS_CURRENT_LOCAL_REHASH',corpus_names=matched)
    return out

def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'require -I -S -B')
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research-results',type=Path);a=p.parse_args()
    need((a.problems is None)==(a.research_results is None),'both corpus inputs required');need(not a.integrity_only or (a.source_dir is None and a.problems is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);data=semantics(before)
    basic={'problem_id':1430,'rank':1015,'queue_status':'unsolved','turns':'5/5','accepted_files':25,'accepted_bytes':205180,'corrected_payload_files':11,'corrected_payload_bytes':85362,'general_resolution':False,'formal_certification':False,'novelty_claimed':False}
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY',**basic}
    need(os.geteuid()!=0,'nonroot required for permission-enforced replay')
    with tempfile.TemporaryDirectory(prefix='word-publication-') as temp:
        copy=Path(temp)/'accepted';copy.mkdir()
        for n,b in data.items():q=copy/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        permissions(copy,True)
        try:
            result=load(invoke(copy/'audit/replay_audit.py',copy,copy/'EXTERNAL_PINS.json'))
            for k,v in [('status','PASS'),('problem_id',1430),('effective_uid',os.geteuid()),('original_snapshot_unchanged',True),('bootstrap_positive_runs',6),('integrity_mutant_variants',16),('integrity_mutant_mode_runs',48),('direct_malformed_variants',10),('direct_malformed_mode_runs',30),('total_runs',84)]:exact(result[k],v,'fresh '+k)
            need(type(result['readonly_write_probes_denied']) is list and result['readonly_write_probes_denied']==['packet/audit_write_probe','freeze/audit_write_probe','packet/README.md','freeze/bootstrap.py'],'four actual read-only denials')
            need(type(result['results']) is list and len(result['results'])==84,'replay detailed count')
            raw=invoke(copy/'audit/independent_checks.py',copy/'packet');need(raw==data['audit/INDEPENDENT_RESULTS.json'],'independent output mismatch')
            after,_=inventory(copy);need(after==data,'accepted copied bytes changed')
        finally:permissions(copy,False)
    primary=primary_rehash(data,a);need(authenticate(root)==before,'publication input changed')
    return {'schema':'word-representation-publication-replay-v1','status':'PASS_UNSOLVED_PARTIALS',**basic,'publication_manifest_sha256':EXPECTED_MANIFEST,'audit_manifest_sha256':AUDIT_PIN,'fresh_corrected_replay_runs':84,'readonly_write_probes_denied':4,'actual_nonroot':True,'author_checks':89818,'independent_checks':313309,'source_free_default':a.source_dir is None and a.problems is None,'primary_rehash':primary,'original_and_private_patch_replay':'NOT_RUN_EXCLUDED_FROM_PUBLICATION','github_ci':'NOT_RUN','limitations':['Finite exact diagnostics and AI audit do not certify the general theorem.','The 2026 bipartite theorem is credited preprint mathematics; no external Lean build or certificate reproduction.','Original quotation-bearing freeze and literal private correction patch are excluded.','Historical original replay receipts are preserved; fresh replay applies only to the accepted corrected candidate.','Read-only guarantees are non-root permission checks, not mount isolation or concurrent hostile filesystem protection.']}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,separators=(',',':')))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,RecursionError,subprocess.SubprocessError) as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
