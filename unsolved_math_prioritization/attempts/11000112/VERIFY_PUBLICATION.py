#!/usr/bin/env python3
"""Authenticated source-free replay; external BOOTSTRAP.py pin is the trust anchor."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,io,json,os,re,stat,subprocess,sys,tempfile,zipfile
EXPECTED_MANIFEST='fc003433b6074ea37e08b717fc2453b9a6f57c8d237206c2dcbf62d031451763'
AUTHOR_BOOTSTRAP='3c892dc01523d9c75f28b41efe0de500407ae02bc21ea13208771dcc91dec817'
AUTHOR_MANIFEST='45f641b37f6e58df37729e194076c2512cdc77ce12faa7c7c937dd6fc09195fa'
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
    need(type(m) is dict and set(m)=={'schema','problem_id','rank','disposition','approaches','files'},'manifest schema')
    for k,v in [('schema','positive-twist-publication-manifest-v1'),('problem_id',11000112),('rank',1012),('disposition','already_solved'),('approaches',0)]:need(type(m[k]) is type(v) and m[k]==v,'manifest scope: '+k)
    need(type(m['files']) is list and 1<=len(m['files'])<=100,'manifest files');expected={'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'}
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');n=e['path'];need(safe(n) and n not in expected,'unsafe or duplicate path');expected.add(n)
        need(n in f,'missing member: '+n);need(type(e['bytes']) is int and e['bytes']>=0 and len(f[n])==e['bytes'],'byte count: '+n)
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(f[n])==e['sha256'],'digest: '+n)
    need(set(f)==expected,'file inventory mismatch');need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory mismatch')
    need(f['VERIFY_PUBLICATION.py']==read(Path(__file__)),'different verifier copy');return f
def archive_members(b,expected):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names=z.namelist();need(len(names)==len(set(names)) and set(names)==set(expected),'archive inventory')
        for e in z.infolist():
            need(safe(e.filename) and not e.is_dir(),'unsafe archive path');mode=e.external_attr>>16;need(not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0,stat.S_IFREG),'archive member type')
            need(e.file_size==len(expected[e.filename]),'archive member size');need(z.read(e)==expected[e.filename],'archive member bytes')
    return len(expected)
def semantics(f):
    pins={'author_original/AUTHOR_MANIFEST.json':(1770,AUTHOR_MANIFEST),'author_original/bootstrap.py':(4332,AUTHOR_BOOTSTRAP),'audit/AUDIT_MANIFEST.json':(1786,'c2872513541ade923f047c7662c656111878e9cb9a639078402c73323f663003'),'archives/AUTHOR_FREEZE.zip':(18503,'383ccc35f8a5230570b411ac5809c6b477d0b341ce09bed3b6d6a34a0133d25d'),'archives/INDEPENDENT_AUDIT.zip':(18581,'0308559d4da47787d75a48971f17d10d5a8b63775b16595b7fbe874fe21ff9af')}
    for n,pin in pins.items():need((len(f[n]),sha(f[n]))==pin,'external frozen pin: '+n)
    author={n.removeprefix('author_original/'):b for n,b in f.items() if n.startswith('author_original/')};audit={n.removeprefix('audit/'):b for n,b in f.items() if n.startswith('audit/')}
    ac=archive_members(f['archives/AUTHOR_FREEZE.zip'],author);rc=archive_members(f['archives/INDEPENDENT_AUDIT.zip'],audit);need(ac==13 and rc==9,'frozen member counts')
    for members,name,prefix,extra in [(author,'AUTHOR_MANIFEST.json','packet/',{'AUTHOR_MANIFEST.json','bootstrap.py'}),(audit,'AUDIT_MANIFEST.json','',{'AUDIT_MANIFEST.json'})]:
        m=load(members[name]);expected=set(extra)
        for e in m['files']:
            n=prefix+e['path'];need(safe(n) and n not in expected,'inner duplicate or unsafe path');expected.add(n);need(type(e['bytes']) is int and e['bytes']==len(members[n]) and e['sha256']==sha(members[n]),'inner byte binding')
        need(set(members)==expected,'inner inventory')
    a=load(audit['ACCEPTANCE.json']);c=load(author['packet/CLAIMS.json'])
    for k,v in [('decision','ACCEPT_PRIOR_NEGATIVE'),('queue_status','already_solved'),('problem_id',11000112),('rank',1012),('substantive_proof_search_turns',0),('turn_limit',5)]:need(type(a[k]) is type(v) and a[k]==v,'acceptance scope: '+k)
    for k in ['author_freeze_changed','corrected_manifest_required','correction_patch_required','finite_checks_certify_mapping_class_identity','formal_verification','human_peer_review_claimed','novelty_claimed','priority_claimed','private_coordination_included','source_material_included']:need(a[k] is False,'acceptance exclusion: '+k)
    for k in ['independent_mathematical_audit','original_freeze_accepted']:need(a[k] is True,'acceptance qualification: '+k)
    need(a['result']=={'all_curves_nonseparating':True,'answer':'no','genus':3,'positive_factors':12,'quotient':'Z^4','quotient_betti_number':4,'torsion_free':True},'exact result')
    need(c['status']=='prior-negative' and type(c['approaches']) is int and c['approaches']==0 and c['independent_review_performed'] is False,'historical author claims')
    for k in ['finite_checks_certify_mapping_class_identity','formal_verification','novelty_claimed','sharp_all_genera_bound_claimed']:need(c[k] is False,'author scope limit')
    for n in ['AUTHOR_RECEIPT.json','AUDIT_RECEIPT.json']:need(load(f[n])['remote_writes']=='none','historical receipt changed')
    need(load(f['AUTHOR_RECEIPT.json'])['independent_mathematical_audit']=='not performed','historical review flag changed')
    need(f['AUTHOR_REPLAY_CONTROLS.json']==audit['AUTHOR_SUITE_RERUN.json'],'historical author controls mismatch')
    need(load(audit['SOURCE_REHASH.json'])['fresh_download_by_auditor'] is False,'historical download flag')
    return {'author_archive_members':ac,'audit_archive_members':rc,'originals_unchanged':True,'correction_required':False,'acceptance':'ACCEPT_PRIOR_NEGATIVE','credited_result':'Baykur 2022; genus 3, twelve positive factors, integral quotient Z^4','geometric_dependency':a['geometric_dependency']}
def invoke(root,script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO'];r=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=600)
    need(r.returncode==0 and not r.stderr,'replay failed '+script+': '+r.stderr.decode('utf8','replace'));return load(r.stdout)
def permissions(root,readonly):
    if not readonly:root.chmod(0o755)
    for p in root.rglob('*'):p.chmod((0o555 if p.is_dir() else 0o444) if readonly else (0o755 if p.is_dir() else 0o644))
    root.chmod(0o555 if readonly else 0o755)
def primary_rehash(f,a):
    ids=load(f['author_original/packet/SOURCE_IDENTITIES.json']);out={'sources':'NOT_RUN','corpora':'NOT_RUN','record_join':'NOT_RUN','fresh_retrieval':'NOT_RUN','fresh_source_inspection':'NOT_RUN'}
    if a.source_dir is not None:
        names=['mcgbook.pdf','baykur2022.pdf','baykur2015v2.pdf','hughes2022_wrong_article.pdf'];matches=[]
        for name,e in zip(names,ids['sources']):
            b=read(a.source_dir/name,10000000);need((len(b),sha(b))==(e['pdf_bytes'],e['pdf_sha256']),'source bytes mismatch: '+name);matches.append({'role':e['role'],'bytes':len(b),'sha256':sha(b)})
        out.update(sources='PASS_CURRENT_LOCAL_REHASH',source_matches=matches)
    if a.problems is not None:
        matches=[]
        for p,e in zip([a.problems,a.research_results],ids['corpora']):
            b=read(p,150000000);need((len(b),sha(b))==(e['bytes'],e['sha256']),'corpus bytes mismatch: '+e['name']);matches.append({'name':e['name'],'bytes':len(b),'sha256':sha(b)})
        out.update(corpora='PASS_CURRENT_LOCAL_REHASH',corpus_matches=matches)
    return out
def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'require -I -S -B')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research-results',type=Path);a=p.parse_args()
    need((a.problems is None)==(a.research_results is None),'both complete corpus inputs required');need(not a.integrity_only or (a.source_dir is None and a.problems is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':11000112,**report}
    need(os.geteuid()!=0,'full replay requires non-root for enforced read-only tests')
    with tempfile.TemporaryDirectory(prefix='positive-twist-publication-') as tmp:
        work=Path(tmp)
        for n,b in before.items():q=work/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        original=work/'author_original';permissions(original,True)
        try:
            control=invoke(work,'author_original/packet/test_bootstrap.py',AUTHOR_BOOTSTRAP,AUTHOR_MANIFEST)
            for k,v in [('status','PASS'),('positive_count',9),('integrity_case_count',49),('integrity_rejection_count',147),('semantic_case_count',39),('semantic_rejection_count',117),('original_write_denied',True),('original_bytes_unchanged',True),('hostile_code_executed',False)]:need(type(control[k]) is type(v) and control[k]==v,'author replay: '+k)
            independent=invoke(work,'audit/independent_checks.py',original,work/'archives/AUTHOR_FREEZE.zip')
            for k,v in [('status','PASS'),('positive_count',6),('integrity_case_count',34),('integrity_rejection_count',102),('semantic_case_count',97),('semantic_rejection_count',291),('minor_count',990),('gcd_rank_two_minors',1),('integral_quotient','Z^4'),('original_bytes_unchanged',True),('original_write_denied',True),('symplectic_check_is_not_mapping_class_proof',True)]:need(type(independent[k]) is type(v) and independent[k]==v,'independent replay: '+k)
            report['author_controls']={k:control[k] for k in ['positive_count','integrity_case_count','integrity_rejection_count','semantic_case_count','semantic_rejection_count','original_write_denied','original_bytes_unchanged','hostile_code_executed']}
            report['independent_controls']={k:independent[k] for k in ['positive_count','integrity_case_count','integrity_rejection_count','semantic_case_count','semantic_rejection_count','minor_count','gcd_rank_two_minors','integral_quotient','original_write_denied','original_bytes_unchanged','symplectic_check_is_not_mapping_class_proof']}
        finally:permissions(original,False)
        report['primary_rehash']=primary_rehash(before,a)
    need(authenticate(root)==before,'publication bytes changed')
    return {'schema':'positive-twist-publication-replay-v1','status':'PASS_CREDITED_PRIOR_NEGATIVE','problem_id':11000112,'rank':1012,'queue_status':'already_solved','approaches':0,'novelty_claimed':False,'formal_verification':False,'human_peer_review':False,'finite_checks_certify_mapping_class_identity':False,'github_ci':False,'source_free_default':a.source_dir is None and a.problems is None,'publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,RecursionError,subprocess.SubprocessError,zipfile.BadZipFile) as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
