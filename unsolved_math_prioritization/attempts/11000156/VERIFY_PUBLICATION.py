#!/usr/bin/env python3
"""Authenticated source-free replay; external BOOTSTRAP.py pin is the trust anchor."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,io,json,os,re,stat,subprocess,sys,tempfile,tarfile
EXPECTED_MANIFEST='a7282d50e4887cf9f24339965299c30b836d925b44acaaaa056caa9ebc899951'
class Reject(Exception):pass
def need(c,m):
    if not c:raise Reject(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(ps):
    d={}
    for k,v in ps:need(k not in d,'duplicate JSON key');d[k]=v
    return d
def constant(x):raise Reject('nonfinite JSON')
def load(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=constant)
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
    need(type(m) is dict and set(m)=={'schema','problem_id','rank','disposition','turns','files'},'manifest schema')
    for k,v in [('schema','boundary-twist-publication-manifest-v1'),('problem_id',11000156),('rank',1013),('disposition','unsolved'),('turns',5)]:need(type(m[k]) is type(v) and m[k]==v,'manifest scope: '+k)
    need(type(m['files']) is list and 1<=len(m['files'])<=100,'manifest files');expected={'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'}
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');n=e['path'];need(safe(n) and n not in expected,'unsafe or duplicate path');expected.add(n)
        need(n in f,'missing member: '+n);need(type(e['bytes']) is int and e['bytes']>=0 and len(f[n])==e['bytes'],'byte count: '+n)
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(f[n])==e['sha256'],'digest: '+n)
    need(set(f)==expected,'file inventory mismatch');need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory mismatch')
    need(f['VERIFY_PUBLICATION.py']==read(Path(__file__)),'different verifier copy');return f
def archive_members(b,expected,prefix):
    with tarfile.open(fileobj=io.BytesIO(b),mode='r:gz') as z:
        members=z.getmembers();names=[e.name for e in members];need(len(names)==len(set(names)),'duplicate archive names')
        got={};dirs=set();allowed_dirs={prefix}|{prefix+'/'+str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
        for e in members:
            need(safe(e.name) and (e.isfile() or e.isdir()),'unsafe archive path/type')
            if e.isdir():need(e.name in allowed_dirs,'extra archive directory');dirs.add(e.name);continue
            need(e.name.startswith(prefix+'/'),'archive prefix');n=e.name[len(prefix)+1:];need(n in expected and e.size==len(expected[n]),'archive inventory/size')
            got[n]=z.extractfile(e).read();need(got[n]==expected[n],'archive member bytes')
        need(set(got)==set(expected),'archive file inventory')
    return len(got)
def semantics(f):
    pins={
        'original/FREEZE_MANIFEST.json':(852,'913c3e9341eb863e7906d234707bf92188bd78f7af8a4833d1ee47b859c8a077'),
        'original/bootstrap.py':(1265,'dcc50e895d0373014bc9098742b4c20bb090753958b1bc338c244f32003c03b1'),
        'archives/source_free_packet.tar.gz':(13801,'3f8104fcf841db20f90769427c0a218971bf5a542c5d24a9747a5c931f28da06'),
        'audit/corrected_source_free_packet.tar.gz':(14381,'05517ab277dcafd77200b9477a9cdfeea630dd4bdba5f7eb149a8fdaec4cbf68'),
        'audit/corrected_distribution/FREEZE_MANIFEST.json':(852,'c4c7a8b35ff946adbd92aed28d62a9272b9e256b322267b9f84e37d12454eb06'),
        'audit/corrected_distribution/bootstrap.py':(1265,'58e9c58468260041de720c687eef34c43ee52c18d080c4194fd7e110f208e155')}
    for n,p in pins.items():need((len(f[n]),sha(f[n]))==p,'external frozen pin: '+n)
    original={n.removeprefix('original/'):b for n,b in f.items() if n.startswith('original/')}
    audit={n.removeprefix('audit/'):b for n,b in f.items() if n.startswith('audit/')}
    corrected={n.removeprefix('corrected_distribution/'):b for n,b in audit.items() if n.startswith('corrected_distribution/')}
    need(archive_members(f['archives/source_free_packet.tar.gz'],original,'boundary_twist_11000156')==10,'original member count')
    need(archive_members(audit['corrected_source_free_packet.tar.gz'],corrected,'boundary_twist_11000156_corrected')==10,'corrected member count')
    am=load(audit['AUDIT_MANIFEST.json']);need(am['schema']=='boundary-twist-independent-audit-manifest-v1' and type(am['files']) is dict,'audit manifest schema')
    need(set(audit)==set(am['files'])|{'AUDIT_MANIFEST.json'},'audit exact inventory')
    for n,r in am['files'].items():need(safe(n) and type(r['bytes']) is int and (len(audit[n]),sha(audit[n]))==(r['bytes'],r['sha256']),'audit binding')
    for data in [original,corrected]:
        m=load(data['FREEZE_MANIFEST.json']);need(m['schema']=='boundary-twist-packet-v1','inner schema')
        need(set(data)=={'packet/'+n for n in m['files']}|{'FREEZE_MANIFEST.json','bootstrap.py','BOOTSTRAP_PINS.json','ACCEPTANCE.json'},'distribution exact inventory')
        for n,r in m['files'].items():need(safe(n) and type(r['bytes']) is int and (len(data['packet/'+n]),sha(data['packet/'+n]))==(r['bytes'],r['sha256']),'inner binding')
        st=load(data['packet/STATUS.json'])
        for k,v in [('problem_id',11000156),('rank',1013),('turns',5),('budget',5),('main_problem_resolved',False),('formal_certification',False),('status','unsolved_scoped_prior_resolution')]:need(type(st[k]) is type(v) and st[k]==v,'scope '+k)
        need(len(st['ledger'])==5 and [x['turn'] for x in st['ledger']]==[1,2,3,4,5],'five-turn ledger')
    for n in ['README.md','STATUS.json','proof_checks.py','verify.py']:need(original['packet/'+n]==corrected['packet/'+n],'noncitation packet drift')
    delivery=load(audit['CORRECTED_DELIVERY.json']);need(delivery['status']=='unsolved' and delivery['turns']=='5/5' and delivery['correction']=='Wajnryb source attribution only','correction scope')
    need(load(audit['AUDIT_RECEIPT.json'])['malformed_rejections']==186,'historical audit count')
    return {'original_archive_members':10,'corrected_archive_members':10,'original_bytes_preserved':True,'correction':'Wajnryb source attribution only','main_problem_resolved':False,'formal_certification':False}
def invoke(script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')};env.update(PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1')
    p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*map(str,args)],cwd=script.parent,env=env,capture_output=True,timeout=600)
    need(p.returncode==0 and not p.stderr,'replay failed '+script.name+': '+p.stderr.decode('utf8','replace'));return load(p.stdout)
def materialize(d,f):
    d.mkdir(parents=True,exist_ok=True)
    for n,b in f.items():p=d/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def permissions(root,readonly):
    root.chmod(0o755)
    for p in root.rglob('*'):p.chmod((0o555 if p.is_dir() else 0o444) if readonly else (0o755 if p.is_dir() else 0o644))
    root.chmod(0o555 if readonly else 0o755)
def primary_rehash(f,a):
    ids=load(f['original/packet/SOURCES.json']);out={k:'NOT_RUN' for k in ['sources','corpora','record_join','fresh_retrieval','fresh_source_inspection']}
    if a.source_dir is not None:
        need(not a.source_dir.is_symlink() and a.source_dir.is_dir(),'invalid source directory');rows=[]
        for n,e in zip(['farb-book.pdf','baykur-v3.pdf','auroux-stable.pdf'],ids['pdf_metadata']):
            b=read(a.source_dir/n,10000000);need((len(b),sha(b))==(e['bytes'],e['sha256']),'source mismatch '+n);rows.append({'bytes':len(b),'sha256':sha(b)})
        out.update(sources='PASS_CURRENT_LOCAL_REHASH',source_matches=rows)
    if a.problems is not None:
        rows=[]
        for p,e in zip([a.problems,a.research_results],ids['corpus_metadata']):
            b=read(p,150000000);need((len(b),sha(b))==(e['bytes'],e['sha256']),'corpus mismatch');rows.append({'name':e['public_corpus'],'bytes':len(b),'sha256':sha(b)})
        out.update(corpora='PASS_CURRENT_LOCAL_REHASH',corpus_matches=rows)
    return out
def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'require -I -S -B')
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research-results',type=Path);a=p.parse_args()
    need((a.problems is None)==(a.research_results is None),'both complete corpus inputs required');need(not a.integrity_only or (a.source_dir is None and a.problems is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':11000156,**report}
    need(os.geteuid()!=0,'full replay requires non-root for enforced read-only tests')
    with tempfile.TemporaryDirectory(prefix='boundary-twist-publication-') as tmp:
        top=Path(tmp);original=top/'boundary_twist_11000156';audit=top/'boundary_twist_11000156_audit'
        materialize(original,{n.removeprefix('original/'):b for n,b in before.items() if n.startswith('original/')})
        (original/'source_free_packet.tar.gz').write_bytes(before['archives/source_free_packet.tar.gz'])
        materialize(audit,{n.removeprefix('audit/'):b for n,b in before.items() if n.startswith('audit/')})
        corrected=audit/'corrected_distribution';permissions(original,True);permissions(corrected,True)
        try:
            result=invoke(audit/'test_distribution.py')
            for k,v in [('uid',os.geteuid()),('exact_modes_per_distribution',3),('malformed_rejections',186),('original_unchanged',True),('independent_modes',3)]:need(type(result[k]) is type(v) and result[k]==v,'audit rerun '+k)
            full=load(read(audit/'AUDIT_RECEIPT.json'))
            for key in ['original_exact','corrected_exact']:
                need(full[key]['uid']==os.geteuid() and full[key]['unchanged'] is True and len(full[key]['read_only_denials'])==4,'read-only replay scope')
            for r in full['independent_checks']:
                need(r['main_problem_resolved'] is False and r['formal_certification'] is False,'finite scope')
                need(r['integer_hurwitz']['integer_matrices']==692 and r['integer_hurwitz']['hurwitz_steps']==10,'integer checks')
                need(r['doubling']['admissible_sequences']==1105 and r['quadratic']['formula_cases']==4096,'finite check counts')
                need(r['finite_orbits']['identity_words']==243 and r['finite_orbits']['components']==[[1,1,1,240],[243]],'finite orbits')
            report['fresh_audit_replay']=result
            # Apply the actual accepted patch to a writable original packet copy.
            replay=top/'patch_replay';materialize(replay,{n.removeprefix('original/'):b for n,b in before.items() if n.startswith('original/packet/')})
            command=['patch','--batch','--forward','--fuzz=0','-p1','-i',str(audit/'citation_correction.patch')]
            pr=subprocess.run(command,cwd=replay,capture_output=True,timeout=30);need(pr.returncode==0 and not pr.stderr,'actual citation patch failed')
            actual,dirs=inventory(replay);expected={n.removeprefix('audit/corrected_distribution/'):b for n,b in before.items() if n.startswith('audit/corrected_distribution/packet/')}
            need(actual==expected and dirs=={'packet'},'actual patch did not reconstruct six corrected packet files')
            report['actual_patch_replay']={'packet_files':6,'all_match':True,'external_manifest_bootstrap_rebound_separately':True}
        finally:permissions(original,False);permissions(corrected,False)
        report['primary_rehash']=primary_rehash(before,a)
    need(authenticate(root)==before,'publication bytes changed')
    return {'schema':'boundary-twist-publication-replay-v1','status':'PASS_UNSOLVED_PARTIALS','problem_id':11000156,'rank':1013,'queue_status':'unsolved','turns':'5/5','novelty_claimed':False,'human_peer_review':False,'github_ci':False,'source_free_default':a.source_dir is None and a.problems is None,'publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,RecursionError,subprocess.SubprocessError,tarfile.TarError) as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
