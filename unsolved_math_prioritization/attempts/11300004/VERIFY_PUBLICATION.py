#!/usr/bin/env python3
"""Authenticated source-free replay; external BOOTSTRAP.py pin is the trust anchor."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,io,json,math,os,re,stat,subprocess,sys,tempfile,tarfile
EXPECTED_MANIFEST='1ac74b0eff582d70ccc85984bedd4b2be478fcd1d3eae71749da7ce7ec817807'
class Reject(Exception):pass
def need(c,m):
    if not c:raise Reject(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(ps):
    d={}
    for k,v in ps:need(k not in d,'duplicate JSON key');d[k]=v
    return d
def constant(x):raise Reject('nonfinite JSON')
def finite_float(token):
    value=float(token);need(math.isfinite(value),'nonfinite JSON float');return value
def load(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=finite_float)
def safe(n):return type(n) is str and n!='' and '\\' not in n and not n.startswith('/') and all(x not in ('','.','..') for x in n.split('/'))
def read(p,limit=2000000):
    st=p.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'nonregular or hard-linked input: '+p.name);need(st.st_size<=limit,'oversized input')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        a=os.fstat(fd);need((a.st_dev,a.st_ino)==(st.st_dev,st.st_ino),'input changed before read')
        with os.fdopen(fd,'rb',closefd=False) as f:b=f.read(limit+1)
        z=os.fstat(fd);need((a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_size,z.st_mtime_ns,z.st_ctime_ns) and len(b)==st.st_size,'unstable input')
    finally:os.close(fd)
    return b
def inventory(root):
    need(not root.is_symlink() and root.is_dir(),'invalid root');out={};dirs=set()
    def visit(d,prefix):
        for e in os.scandir(d):
            n=prefix+e.name;mode=e.stat(follow_symlinks=False).st_mode;need(not stat.S_ISLNK(mode),'symlink: '+n)
            if stat.S_ISDIR(mode):dirs.add(n);visit(Path(e.path),n+'/')
            else:need(stat.S_ISREG(mode),'nonregular member: '+n);out[n]=read(Path(e.path))
    visit(root,'');return out,dirs
def authenticate(root):
    f,dirs=inventory(root);need('PUBLICATION_MANIFEST.json' in f,'missing manifest');raw=f['PUBLICATION_MANIFEST.json'];need(sha(raw)==EXPECTED_MANIFEST,'manifest external pin');m=load(raw)
    need(type(m) is dict and set(m)=={'schema','problem_id','rank','disposition','approaches','files'},'manifest schema')
    for k,v in [('schema','wild-quadrisecants-publication-manifest-v1'),('problem_id',11300004),('rank',1014),('disposition','unsolved'),('approaches',5)]:need(type(m[k]) is type(v) and m[k]==v,'manifest scope: '+k)
    need(type(m['files']) is list and 1<=len(m['files'])<=100,'manifest files');expected={'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'}
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');n=e['path'];need(safe(n) and n not in expected,'unsafe or duplicate path');expected.add(n)
        need(n in f,'missing member: '+n);need(type(e['bytes']) is int and e['bytes']>=0 and len(f[n])==e['bytes'],'byte count: '+n)
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(f[n])==e['sha256'],'digest: '+n)
    need(set(f)==expected,'file inventory mismatch');need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory mismatch')
    need(f['VERIFY_PUBLICATION.py']==read(Path(__file__)),'different verifier copy');return f
def archive_members(b,expected):
    expected_dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
    with tarfile.open(fileobj=io.BytesIO(b),mode='r:gz') as z:
        members=z.getmembers();names=[e.name.rstrip('/') for e in members]
        need(len(names)==len(set(names)) and set(names)==set(expected)|expected_dirs,'archive inventory')
        for e,n in zip(members,names):
            need(safe(n) and not e.pax_headers and (e.isfile() or e.isdir()),'unsafe archive member')
            if e.isdir():need(n in expected_dirs and e.size==0,'archive directory')
            else:
                need(n in expected and e.size==len(expected[n]),'archive member size')
                need(z.extractfile(e).read()==expected[n],'archive member bytes')
    return len(expected)
def same_typed(actual,expected,label):
    need(type(actual) is type(expected) and actual==expected,label)
def semantics(f):
    pins={
        'audit/source_free_audit.tar.gz':(63839,'abedd01e348ee17ba369b4eb961599f5e5a8fa3e4d7fc71ca471c332d570ddf0'),
        'audit/FINAL_BUNDLE_REPLAY.json':(3806,'b78fbb9c6d7a74994cf8a1b0cb77368ee43c9a79ca713979ecd2c3abd3245419'),
        'audit/public/PUBLIC_MANIFEST.json':(3747,'5340bc1aea0a77722ad47931c4049f115eed42e55b80949695ea02ab5a5545d8'),
        'audit/public/corrected/source_free_packet.tar.gz':(18347,'29f3c6c8c4c0fad6298263a16ab66d95cf1460854346441a6c53a8173c29a865'),
        'audit/public/corrected/freeze/FREEZE_MANIFEST.json':(988,'9097b3da520bdee1facde8b7fdb92b7b23e974fb7cbb726c2903ccbc1965cd56'),
        'audit/public/corrected/freeze/bootstrap.py':(1455,'4bcfe34c55a37eb7c1323a63de12e86f7060110efaf10b8237b08c974e96fcfa'),
        'audit/public/corrected/packet/verify.py':(5087,'4f55b4aee1cae738e45891f9ad53fe3e1c901aeef3b4b87af6669beffe3cd331')}
    for n,pin in pins.items():need((len(f[n]),sha(f[n]))==pin,'accepted frozen pin: '+n)
    public={n.removeprefix('audit/public/'):b for n,b in f.items() if n.startswith('audit/public/')}
    manifest=load(public['PUBLIC_MANIFEST.json']);need(type(manifest) is dict and set(manifest)=={'schema','files','excluded_from_manifest','contains_copied_source_text','contains_dataset_contents'},'public manifest schema')
    same_typed(manifest['contains_copied_source_text'],False,'source exclusion');same_typed(manifest['contains_dataset_contents'],False,'dataset exclusion')
    need(type(manifest['files']) is dict and set(public)==set(manifest['files'])|{'PUBLIC_MANIFEST.json','DELIVERY.json'},'public exact allowlist')
    for n,e in manifest['files'].items():
        need(safe(n) and type(e) is dict and set(e)=={'bytes','sha256'},'public record')
        need(type(e['bytes']) is int and e['bytes']==len(public[n]) and sha(public[n])==e['sha256'],'public byte binding')
    need(sha(public['DELIVERY.json'])=='6b82f7f7e1c5af0eab11b59c65a1b7d9be023dc5204b1969d195d797d0e490bb','public delivery pin')
    ac=archive_members(f['audit/source_free_audit.tar.gz'],public);need(ac==26,'audit file count')
    corrected={n.removeprefix('corrected/'):b for n,b in public.items() if n.startswith('corrected/') and n!='corrected/source_free_packet.tar.gz'}
    cc=archive_members(public['corrected/source_free_packet.tar.gz'],corrected);need(cc==11,'corrected file count')
    fm=load(corrected['freeze/FREEZE_MANIFEST.json']);need(set(fm)=={'schema','files'} and type(fm['files']) is dict,'corrected manifest schema')
    need(set(fm['files'])=={n.removeprefix('packet/') for n in corrected if n.startswith('packet/')},'corrected packet exact allowlist')
    for n,e in fm['files'].items():
        need(safe(n) and type(e) is dict and set(e)=={'bytes','sha256'},'corrected file record')
        b=corrected['packet/'+n];need(type(e['bytes']) is int and e['bytes']==len(b) and sha(b)==e['sha256'],'corrected file binding')
    acceptance=load(public['ACCEPTANCE.json']);status=load(corrected['packet/STATUS.json']);delivery=load(f['audit/AUDIT_DELIVERY.json'])
    for obj in [acceptance,status]:
        for k,v in [('problem_id',11300004),('rank',1014),('code','AMR-112-0004'),('status','unsolved'),('main_problem_resolved',False),('formal_certification',False),('novelty_claim',False),('remote_writes_performed',False)]:same_typed(obj[k],v,'scope: '+k)
    same_typed(acceptance['turns'],'5/5','audit turns');same_typed(status['turns'],5,'status turns')
    same_typed(delivery['publication_allowlist'],['public/','source_free_audit.tar.gz','AUDIT_DELIVERY.json','FINAL_BUNDLE_REPLAY.json'],'historical allowlist')
    need({n for n in f if n.startswith('audit/')}=={'audit/'+n for n in ['AUDIT_DELIVERY.json','FINAL_BUNDLE_REPLAY.json','source_free_audit.tar.gz']}|{'audit/public/'+n for n in public},'accepted delivery inventory')
    need(acceptance['decision']=='accept corrected packet at unresolved five-route scope','accepted mathematical scope')
    return {'audit_archive_files':ac,'corrected_archive_files':cc,'accepted_bytes_unchanged':True,'status':'unsolved','turns':'5/5','main_problem_resolved':False,'novelty_claim':False,'formal_certification':False,'finite_checks_prove_wild_knot_claim':False}
def invoke(root,script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    r=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=600)
    need(r.returncode==0 and not r.stderr,'replay failed '+script+': '+r.stderr.decode('utf8','replace'));return load(r.stdout)
def permissions(root,readonly):
    if not readonly:root.chmod(0o755)
    for p in root.rglob('*'):p.chmod((0o555 if p.is_dir() else 0o444) if readonly else (0o755 if p.is_dir() else 0o644))
    root.chmod(0o555 if readonly else 0o755)
def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'require -I -S -B')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');a=p.parse_args()
    root=a.root.absolute();before=authenticate(root);report=semantics(before)
    if a.integrity_only:return {'verification':'PASS_PUBLICATION_INTEGRITY','problem_id':11300004,**report}
    need(os.getuid()!=0 and os.geteuid()!=0,'full replay requires actual non-root UID and EUID')
    with tempfile.TemporaryDirectory(prefix='wild-quadrisecants-publication-') as tmp:
        work=Path(tmp);frozen=work/'relocated';frozen.mkdir()
        for n,b in before.items():q=frozen/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        permissions(frozen,True)
        try:
            denied=[]
            for n in ['UNEXPECTED_WRITE','audit/public/corrected/packet/REPORT.md','audit/public/UNEXPECTED_WRITE']:
                try:fd=os.open(frozen/n,os.O_WRONLY|os.O_CREAT,0o600)
                except PermissionError:denied.append(n)
                else:os.close(fd);raise Reject('read-only write unexpectedly permitted')
            independent=invoke(frozen,'audit/public/independent_archive_replay.py','--archive',frozen/'audit/public/corrected/source_free_packet.tar.gz','--archive-sha256','29f3c6c8c4c0fad6298263a16ab66d95cf1460854346441a6c53a8173c29a865','--manifest-sha256','9097b3da520bdee1facde8b7fdb92b7b23e974fb7cbb726c2903ccbc1965cd56','--bootstrap-sha256','4bcfe34c55a37eb7c1323a63de12e86f7060110efaf10b8237b08c974e96fcfa','--verifier-sha256','4f55b4aee1cae738e45891f9ad53fe3e1c901aeef3b4b87af6669beffe3cd331','--ledger-hardened')
            for k,v in [('uid',os.getuid()),('euid',os.geteuid()),('independent_case_count',43),('independent_run_count',129),('ledger_regression_case_count',4),('ledger_hardened',True),('frozen_files_unchanged',True),('formal_certification',False)]:same_typed(independent[k],v,'independent replay: '+k)
            need(len(independent['ledger_regression'])==12 and all(x['accepted'] is False for x in independent['ledger_regression']),'ledger regression controls')
            need(len(independent['read_only_denials'])==5 and [x['optimize'] for x in independent['modes']]==[0,1,2],'inner read-only and optimization coverage')
            h=independent['distributed_harness']
            for k,v in [('hostile_case_count',31),('hostile_run_count',93),('frozen_files_unchanged',True),('uid',os.getuid())]:same_typed(h[k],v,'distributed author harness: '+k)
            need(sum(x['accepted'] is False for x in independent['controls'])==126 and sum(x['accepted'] is True for x in independent['controls'])==3,'ordinary rejection/positive counts')
            exact=invoke(frozen,'audit/public/independent_exact_controls.py')
            for k,v in [('uid',os.getuid()),('euid',os.geteuid()),('optimize',sys.flags.optimize),('isolated',1),('collapse_piece_samples',680),('lifted_circle_triples',286),('degenerate_jacobian_controls',3),('exact_affine_offset_transversal',True),('noncollinear_control_rejected',True),('formal_certification',False),('main_problem_resolved',False)]:same_typed(exact[k],v,'exact control: '+k)
            need(exact['line_counts']==[{'contacts':n,'marked_sets':m,'supporting_lines':1} for n,m in [(4,1),(5,5),(7,35),(11,330)]],'marked configurations vs supporting lines')
            need(exact['determinants']==['1','24','6/49'] and exact['tangent_cosine']=='-3/5','exact finite values')
            need(authenticate(frozen)==before,'read-only replay changed accepted bytes')
            report.update(actual_uid=os.getuid(),actual_euid=os.geteuid(),readonly_denials=len(denied),inner_readonly_denials=5,author_runs=93,independent_runs=129,ledger_rejections=12,exact_controls={k:exact[k] for k in ['collapse_piece_samples','lifted_circle_triples','determinants','tangent_cosine','line_counts']})
        finally:permissions(frozen,False)
    need(authenticate(root)==before,'publication bytes changed')
    return {'schema':'wild-quadrisecants-publication-replay-v1','verification':'PASS_CORRECTED_PARTIALS','problem_id':11300004,'rank':1014,'source_free_default':True,'primary_rehash':{'sources':'NOT_RUN','corpora':'NOT_RUN','record_join':'NOT_RUN','fresh_retrieval':'NOT_RUN','fresh_source_inspection':'NOT_RUN'},'github_ci':'NOT_RUN','publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,RecursionError,subprocess.SubprocessError,tarfile.TarError) as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
