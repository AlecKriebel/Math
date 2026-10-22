#!/usr/bin/env python3
"""Externally authenticated, source-free replay of the planar convex prior-result audit."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,io,json,math,os,re,stat,subprocess,sys,tempfile,zipfile
EXPECTED_MANIFEST='1f612293103d83de224d9773cd58fe585e212f179a07fd7a89186cf6c0995d9b'
EXPECTED_CLAIMS={'schema': 'integer-ikea-publication-claims-v1', 'problem_id': 1900002, 'problem_code': 'AMR-018-0002', 'rank': 1016, 'queue_status': 'already_solved', 'proof_turns': 0, 'proof_turn_limit': 5, 'scope': 'planar convex lattice polygons only', 'original_2017_question_explicitly_requires_convexity': False, 'credited_result': 'Dolan–Karpenkov, Lattice angles of lattice polygons, JTNB 37(3) (2025), Theorem 3.3', 'publication_url': 'https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.1345/', 'original_frozen_v1_published': False, 'accepted_corrected_release': 'corrected_v3', 'accepted_bytes_preserved': True, 'prior_result': True, 'novelty_claimed': False, 'formal_verification': False, 'human_peer_review_claimed': False, 'nonconvex_classification_claimed': False, 'higher_dimensional_solution_claimed': False, 'cosine_rule_solution_claimed': False, 'total_bounded_search_decision_procedure_claimed': False, 'source_text_or_datasets_included': False, 'sail_lemmas_are_credited_imports': True, 'source_correction_changes_main_theorem': False, 'source_correction_supporting_slips': 3}
ACCEPTED_PINS={'corrected_v3/PINS.json': {'bytes': 735, 'sha256': '98c944665abffac215a6e72d556b0117be2847f4906996c5652651cd86563332'}, 'corrected_v3/USAGE.md': {'bytes': 1793, 'sha256': '39625d22faeeaf5a04bb3989c92a64306a0fb8bc458397ed450d32f3949741c2'}, 'corrected_v3/bootstrap.py': {'bytes': 5070, 'sha256': '3cc10cb75fbaf266f990e3dc99dc46fd36095439fd6a345d9ec672a023df4ea0'}, 'corrected_v3/bundle/AUTHOR.zip': {'bytes': 14265, 'sha256': '5e68021c3bb1d16eff575beeae468412e17f5a08ab20eca52fac7940a52a5239'}, 'corrected_v3/bundle/EXTERNAL_MANIFEST.json': {'bytes': 1284, 'sha256': '896aa18f3f5d56d440e2150221f08f478de0f7f99613097a211723947a71c0cb'}, 'corrected_v3/bundle/author/AUDIT.md': {'bytes': 6808, 'sha256': '13f4069e3fcf781e31abceb712575190428fb92f27f341405a116ab339de4aa6'}, 'corrected_v3/bundle/author/CONTROL_OUTPUT.json': {'bytes': 538, 'sha256': '834927c3181f3fcc4b1c3283527943deacb4593496c4f96be82e4693f4c92143'}, 'corrected_v3/bundle/author/CORPUS_BINDINGS.json': {'bytes': 1046, 'sha256': '241e4fb84c33c6ff438808834e1b94e98bca6dfe4a626bcff548e5b9d9bf326b'}, 'corrected_v3/bundle/author/GATE_SUMMARY.md': {'bytes': 1357, 'sha256': '9e46e3c04792f5c995f778190cbfe77ef1e895bbbb4f26401fe21eb11dab1bb7'}, 'corrected_v3/bundle/author/RESULT.md': {'bytes': 3306, 'sha256': '0486836216a2a7dbf45cc982fffc7c3833b3f6229fe3d078a69a6f39e20c3618'}, 'corrected_v3/bundle/author/SOURCE_METADATA.json': {'bytes': 6096, 'sha256': 'dc970bf927c5ad191c10d3c6a42c8fbab66bf510fafe3a3f6569b189b235121f'}, 'corrected_v3/bundle/author/TURN_LEDGER.json': {'bytes': 1337, 'sha256': '5696ce2517379aba1bebecc94a7126021a5f2933269a51253c61a1ff95fb93e0'}, 'corrected_v3/bundle/author/verify_math.py': {'bytes': 10319, 'sha256': 'e571e6d24aa8087e6a62c694a1c6969428f523de834fe8d8ea6c278193d0aca4'}, 'corrected_v3/controls.py': {'bytes': 5611, 'sha256': '235b6bdaeaf9e8d3527e881946b1141326f7920a93a9d106e3587b26a0e1b193'}, 'public/ACCEPTANCE.md': {'bytes': 5884, 'sha256': 'f0f8ad537f95b6de4e9c20e701461e791b944b48c17cf59b8f569e80e1026f16'}, 'public/CORRECTIONS.md': {'bytes': 1826, 'sha256': 'c6106872e6b8d4b6ed8a7ddd392a9bd1a76d7a3a09bd4cb275ebe8a1242934fd'}, 'public/MATHEMATICAL_AUDIT.md': {'bytes': 15704, 'sha256': '34599fd5ebe78b37cbe7c57debc56b77d9cdd1204bb73a6b0c4df705cf65e4a3'}, 'public/REPRODUCE.md': {'bytes': 1672, 'sha256': '057177d00d4a20cb3e826f5b5db824bab7e8aa199007684b2b37eb109789bf2c'}, 'public/SOURCE_STATUS.json': {'bytes': 3526, 'sha256': 'bad3663b6f0cc0d2ae166bf032a48358f908d7ba964ada06f91320eb004fd5c8'}, 'public/independent_controls.py': {'bytes': 12156, 'sha256': 'ef46db5e9c227ddc50067dd59950c6431ebec46cc1bed961de36b1df764405d5'}, 'public/replay_readonly.py': {'bytes': 5555, 'sha256': 'ecb987fbff0c0adc2fda9154cffc82a81f2515c45ecf1584ea75aa509b6c4b22'}, 'receipts/CORRECTED_V3_CONTROLS.json': {'bytes': 1387, 'sha256': '19a442a1895e0f9f330263beadef4452cf1b573b2ac4ac7a931cbe84ea084925'}, 'receipts/CORRECTED_V3_READONLY_PRIVATE_REPLAY.json': {'bytes': 13755, 'sha256': 'c48990ebd1e5f5e9545422b1cc1d1f13d962a7e44adc2c619dc77aab36bfec28'}, 'receipts/CORRECTION_V3_PINS.json': {'bytes': 735, 'sha256': '98c944665abffac215a6e72d556b0117be2847f4906996c5652651cd86563332'}, 'receipts/FINAL_FREEZE_CHECK.json': {'bytes': 343, 'sha256': '40c79dabb3f8a099b4cf8bcc968fd4248bfc0860b168d6b57fd32b5216dcd8f9'}, 'receipts/INDEPENDENT_NORMAL.json': {'bytes': 840, 'sha256': '8291f060d2203be637ab847af305dd14db77cefe1a52146ef489a92da4c414ca'}, 'receipts/INDEPENDENT_O.json': {'bytes': 840, 'sha256': '419401228be7fba651d029c2d976296c40dacc7b69da5d9baa69092c8e865ae2'}, 'receipts/INDEPENDENT_OO.json': {'bytes': 840, 'sha256': '23956ece3ac157a49c120087bf501e2c347743b1d737149f4c37651410526ed9'}, 'receipts/ORIGINAL_CONTROLS_REPLAY.json': {'bytes': 1387, 'sha256': '19a442a1895e0f9f330263beadef4452cf1b573b2ac4ac7a931cbe84ea084925'}, 'receipts/ORIGINAL_FINAL_PRIVATE_REPLAY.json': {'bytes': 6316, 'sha256': '58fb14d2c752dbebc14b1cde4d4150733b94582d46e455ceb3b86e888adebb02'}, 'receipts/SOURCE_BYTE_RECHECK.json': {'bytes': 652, 'sha256': '7dcd0741bee27568e011ed8b7d4c3f8207a93d9a4b10dd724d525fcff87bcb48'}, 'PUBLIC_MANIFEST.json': {'bytes': 5356, 'sha256': 'f383d57c5d7c07e39be2d9c5431a41f794418b03032ffcfc52fa7a964b4f737f'}, 'FINAL_ARCHIVE_RECEIPT.json': {'bytes': 6842, 'sha256': '532d12e2e121fc2c62c94b3d0b884e3372bd21cef821b9f749633051c0a78ce0'}, 'DELIVERY_PINS.json': {'bytes': 853, 'sha256': '3072ff0edcb4d47014aa6a299557451bac9f4fd1b855abc88c3619c2e6b026d8'}, 'PUBLIC_AUDIT.zip': {'bytes': 66715, 'sha256': '35c43e72132049210b6c0f1152b32c9df50600e6d971cba96ca4f0454166bdff'}}
class Reject(Exception):pass
def need(c,m):
    if not c:raise Reject(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def exact(a,b,label='exact value'):
    need(type(a) is type(b),label+' type')
    if type(b) is dict:
        need(set(a)==set(b),label+' keys')
        for k in b:exact(a[k],b[k],label+'.'+k)
    elif type(b) is list:
        need(len(a)==len(b),label+' length')
        for i,(x,y) in enumerate(zip(a,b)):exact(x,y,label+'.'+str(i))
    else:need(a==b,label)
def pairs(ps):
    d={}
    for k,v in ps:need(k not in d,'duplicate JSON key');d[k]=v
    return d
def constant(x):raise Reject('nonfinite JSON')
def finite_float(s):
    value=float(s);need(math.isfinite(value),'nonfinite JSON number');return value
def load(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=finite_float)
def safe(n):return type(n) is str and n!='' and '\\' not in n and not n.startswith('/') and all(x not in ('','.','..') for x in n.split('/'))
def pathcheck(p):
    for q in (p,*p.parents):need(not q.is_symlink(),'symlink path component')
def read(p,limit=2000000):
    pathcheck(p);st=p.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'nonregular or hard-linked input: '+p.name);need(st.st_size<=limit,'oversized input')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        a=os.fstat(fd);need((a.st_dev,a.st_ino)==(st.st_dev,st.st_ino),'input changed before read')
        with os.fdopen(fd,'rb',closefd=False) as f:b=f.read(limit+1)
        z=os.fstat(fd);need((a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_size,z.st_mtime_ns,z.st_ctime_ns) and len(b)==st.st_size,'unstable input')
    finally:os.close(fd)
    return b
def inventory(root):
    pathcheck(root);need(root.is_dir(),'invalid root');out={};dirs=set()
    def visit(d,prefix):
        for e in os.scandir(d):
            n=prefix+e.name;mode=e.stat(follow_symlinks=False).st_mode;need(not stat.S_ISLNK(mode),'symlink: '+n)
            if stat.S_ISDIR(mode):dirs.add(n);visit(Path(e.path),n+'/')
            else:need(stat.S_ISREG(mode),'nonregular member: '+n);out[n]=read(Path(e.path))
    visit(root,'');return out,dirs
def identity(b,e):
    need(type(e) is dict and set(e)=={'bytes','sha256'},'identity schema')
    need(type(e['bytes']) is int and 0<=e['bytes']<=2000000 and len(b)==e['bytes'],'byte identity')
    need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(b)==e['sha256'],'hash identity')
def validate_manifest(m,f,dirs):
    need(type(m) is dict and set(m)=={'schema','problem_id','rank','disposition','proof_turns','scope','files'},'manifest schema')
    for k,v in [('schema','integer-ikea-publication-manifest-v1'),('problem_id',1900002),('rank',1016),('disposition','already_solved'),('proof_turns',0),('scope','planar convex lattice polygons only')]:exact(m[k],v,'manifest '+k)
    need(type(m['files']) is list and 1<=len(m['files'])<=100,'manifest files');expected={'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'}
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');n=e['path'];need(safe(n) and n not in expected,'unsafe or duplicate path');expected.add(n)
        need(n in f,'missing member: '+n);identity(f[n],{k:e[k] for k in ['bytes','sha256']})
    need(set(f)==expected,'file inventory mismatch');need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory mismatch')
def authenticate(root):
    f,dirs=inventory(root);need('PUBLICATION_MANIFEST.json' in f,'missing manifest');raw=f['PUBLICATION_MANIFEST.json'];need(sha(raw)==EXPECTED_MANIFEST,'manifest external pin');validate_manifest(load(raw),f,dirs)
    need(f['VERIFY_PUBLICATION.py']==read(Path(__file__)),'different verifier copy');return f
def archive_members(b,expected):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names=z.namelist();need(len(names)==len(set(names)) and set(names)==set(expected),'archive inventory')
        for e in z.infolist():
            need(safe(e.filename) and not e.is_dir() and not e.flag_bits&1,'unsafe/encrypted archive path');mode=e.external_attr>>16;need(stat.S_IFMT(mode) in (0,stat.S_IFREG),'archive member type')
            need(e.file_size==len(expected[e.filename]),'archive member size');need(z.read(e)==expected[e.filename],'archive member bytes')
    return len(expected)
def semantics(f):
    exact(load(f['CLAIMS.json']),EXPECTED_CLAIMS,'claims')
    for n,pin in ACCEPTED_PINS.items():identity(f['accepted/'+n],pin)
    m=load(f['accepted/PUBLIC_MANIFEST.json']);exact(m['format'],'integer-ikea-independent-audit-v1');exact(m['problem_id'],1900002);exact(m['proof_turns'],0);exact(m['decision'],'ACCEPT-SOLVED-IN-LITERATURE-PLANAR-CONVEX')
    entries=m['publish_only_these_files'];need(type(entries) is dict and len(entries)==31,'accepted manifest members')
    need(set(ACCEPTED_PINS)==set(entries)|{'PUBLIC_MANIFEST.json','PUBLIC_AUDIT.zip','FINAL_ARCHIVE_RECEIPT.json','DELIVERY_PINS.json'},'accepted manifest exact inventory')
    members={}
    for n,e in entries.items():need(safe(n),'unsafe accepted member');identity(f['accepted/'+n],e);members[n]=f['accepted/'+n]
    members['PUBLIC_MANIFEST.json']=f['accepted/PUBLIC_MANIFEST.json'];ac=archive_members(f['accepted/PUBLIC_AUDIT.zip'],members)
    pref='accepted/corrected_v3/bundle/';a=load(f[pref+'EXTERNAL_MANIFEST.json']);exact(a['format'],'ikea-prior-v1');exact(a['problem_id'],1900002);identity(f[pref+'AUTHOR.zip'],a['archive'])
    authors={n.removeprefix(pref+'author/'):b for n,b in f.items() if n.startswith(pref+'author/')};need(set(a['files'])==set(authors),'inner author inventory')
    for n,e in a['files'].items():need(safe(n) and '/' not in n,'inner author path');identity(authors[n],e)
    count=archive_members(f[pref+'AUTHOR.zip'],authors);need(ac==32 and count==8,'archive member counts')
    ledger=load(authors['TURN_LEDGER.json'])
    for k,v in [('problem_id',1900002),('rank',1016),('proof_turns',0),('status','SOLVED-IN-LITERATURE-PLANAR-CONVEX')]:exact(ledger[k],v,'ledger '+k)
    exact(load(f['accepted/FINAL_ARCHIVE_RECEIPT.json'])['accepted'],True,'final archive accepted')
    return {'accepted_public_files':len(ACCEPTED_PINS),'audit_archive_members':ac,'author_archive_members':count,'accepted_bytes_preserved':True}
def flags():return ['-I','-S','-B']+(['-'+'O'*sys.flags.optimize] if sys.flags.optimize else [])
def invoke(root,script,*args):
    r=subprocess.run([sys.executable,*flags(),str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=600)
    need(r.returncode==0 and not r.stderr,'replay failed '+script+': '+r.stderr.decode('utf8','replace'));return load(r.stdout)
def modes(root):return {str(p.relative_to(root)):stat.S_IMODE(p.stat().st_mode) for p in (root,*root.rglob('*'))}
def permissions(root,readonly):
    if not readonly:root.chmod(0o755)
    for p in root.rglob('*'):p.chmod((0o555 if p.is_dir() else 0o444) if readonly else (0o755 if p.is_dir() else 0o644))
    root.chmod(0o555 if readonly else 0o755)
def denied_writes(root):
    need(os.geteuid()!=0,'non-root required');count=0
    for p in (root,*root.rglob('*')):
        need(not p.stat().st_mode&0o222,'writable frozen input')
        try:
            with (p/'FORBIDDEN_WRITE' if p.is_dir() else p).open('xb' if p.is_dir() else 'ab'):pass
        except PermissionError:count+=1
        else:raise Reject('actual write succeeded')
    return count
def optional(f,a,work):
    report={'sources':'NOT_RUN','corpora':'NOT_RUN','record_join':'NOT_RUN','fresh_retrieval':'NOT_RUN','fresh_source_inspection':'NOT_RUN'};arguments=[]
    # Read and bind before invoking inner code; child consumes only these stable copies.
    if a.sources is not None:
        ids=load(f['accepted/corrected_v3/bundle/author/SOURCE_METADATA.json']);dest=work/'private_sources';dest.mkdir()
        for e in ids['pdfs']:
            n=e['filename'];need(safe(n) and '/' not in n,'source filename');b=read(a.sources/n,15000000);need(len(b)==e['bytes'] and sha(b)==e['sha256'],'source identity');(dest/n).write_bytes(b)
        arguments+=['--sources',dest];report['sources']='PASS_CURRENT_LOCAL_REHASH'
    if a.problems is not None:
        ids=load(f['accepted/corrected_v3/bundle/author/CORPUS_BINDINGS.json'])['corpora']
        for key,path,name in [('problems',a.problems,'problems.json'),('reports',a.reports,'research_results.json')]:
            b=read(path,150000000);e=ids[name];need(len(b)==e['bytes'] and sha(b)==e['sha256'],'corpus identity');p=work/name;p.write_bytes(b);arguments+=['--'+key,p]
        report.update(corpora='PASS_CURRENT_LOCAL_REHASH',record_join='PASS_EXACT_ACCEPTED_RECORD_BINDING')
    return report,arguments
def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'require -I -S -B')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--sources',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--reports',type=Path);a=p.parse_args()
    need((a.problems is None)==(a.reports is None),'both complete corpus inputs required');need(not a.integrity_only or (a.sources is None and a.problems is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);before_modes=modes(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':1900002,**report}
    need(os.geteuid()!=0,'full replay requires non-root for enforced read-only tests')
    with tempfile.TemporaryDirectory(prefix='integer-ikea-publication-') as tmp:
        work=Path(tmp);packet=work/'packet';packet.mkdir()
        for n,b in before.items():q=packet/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        opt,args=optional(before,a,work);permissions(packet,True)
        try:
            frozen_modes=modes(packet);denials=denied_writes(packet)
            baseline=invoke(packet,'accepted/corrected_v3/bootstrap.py',*args);expected=load(before['accepted/corrected_v3/bundle/author/CONTROL_OUTPUT.json'])
            if a.sources is not None:expected['source_binding']='both_private_pdf_identities_match'
            if a.problems is not None:expected['corpus_binding']='full_files_and_exact_target_records_match'
            exact(baseline,{'accepted':True,'problem_id':1900002,'archive_sha256':'5e68021c3bb1d16eff575beeae468412e17f5a08ab20eca52fac7940a52a5239','result':expected},'author replay')
            controls=invoke(packet,'accepted/corrected_v3/controls.py')
            expected_controls=load(before['accepted/receipts/CORRECTED_V3_CONTROLS.json']);expected_controls['uid']=os.geteuid();exact(controls,expected_controls,'producer controls')
            independent=invoke(packet,'accepted/public/independent_controls.py','--checker',packet/'accepted/corrected_v3/bundle/author/verify_math.py')
            wanted=load(before['accepted/receipts/INDEPENDENT_NORMAL.json']);wanted['optimize']=sys.flags.optimize;exact(independent,wanted,'independent controls')
            readonly=invoke(packet,'accepted/public/replay_readonly.py','--release',packet/'accepted/corrected_v3','--independent',packet/'accepted/public/independent_controls.py')
            for k,v in [('accepted',True),('release','corrected_v3'),('uid',os.geteuid()),('unchanged',True)]:exact(readonly[k],v,'read-only '+k)
            need(len(readonly['runs'])==3 and len(readonly['negative_controls'])==15,'read-only counts')
            for run in readonly['runs']:
                expected_readonly={'accepted':True,'problem_id':1900002,'archive_sha256':'5e68021c3bb1d16eff575beeae468412e17f5a08ab20eca52fac7940a52a5239','result':load(before['accepted/corrected_v3/bundle/author/CONTROL_OUTPUT.json'])};exact(run['original'],expected_readonly,'read-only baseline');exact(run['original'],run['relocated'],'relocated result');expected_independent=load(before['accepted/receipts/INDEPENDENT_NORMAL.json']);expected_independent['optimize']=run['optimize'];exact(run['independent'],expected_independent,'read-only independent')
            need(authenticate(packet)==before and modes(packet)==frozen_modes,'frozen packet changed')
            report.update(read_only={'uid':os.geteuid(),'actual_write_denials':denials,'packet_bytes_and_modes_unchanged':True,'relocated_replay_modes':3,'accepted_readonly_negative_controls':15},producer_controls={'positive':controls['positive_count'],'negative':controls['negative_count']},independent_counts=independent['counts'],primary_rehash=opt)
        finally:permissions(packet,False)
    need(authenticate(root)==before and modes(root)==before_modes,'input publication changed')
    return {'schema':'integer-ikea-publication-replay-v1','status':'PASS_CREDITED_PRIOR_RESULT_PLANAR_CONVEX_ONLY','problem_id':1900002,'rank':1016,'queue_status':'already_solved','proof_turns':0,'scope':'planar convex lattice polygons only','original_2017_question_explicitly_requires_convexity':False,'novelty_claimed':False,'formal_verification':False,'human_peer_review':False,'total_bounded_search_decision_procedure':False,'github_ci':'NOT_RUN','publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,RecursionError,subprocess.SubprocessError,zipfile.BadZipFile) as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
