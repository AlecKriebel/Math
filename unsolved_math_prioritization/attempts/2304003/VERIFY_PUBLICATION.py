#!/usr/bin/env python3
"""Externally authenticated, source-free replay of the five accepted bounded-polynomial partial approaches."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,io,json,math,os,re,stat,subprocess,sys,tempfile,tarfile
EXPECTED_MANIFEST='7f08b49713df5990826f2bce0e9acae816fcb3c3e6c025b0ccdec601c3ce6d17'
EXPECTED_CLAIMS={'schema': 'bounded-polynomial-partials-v1', 'problem_id': 2304003, 'problem_number': 'AMR-022-4003', 'rank': 1032, 'proof_turns': 5, 'queue_status': 'unsolved', 'arbitrary_term_count_growth': 'logarithmic lower bound; square-root upper bound; sharp growth unresolved', 'dense_growth': 'A(d,k)=log(min(k,d-k))/pi+O(1), uniformly for 1<=k<d; A(d,d)=1', 'quadratic_exact': 'A(3,2)=2/sqrt(3); fixed arithmetic-progression triples only', 'arbitrary_subset_growth': 'U_N has square-root order; favorable subset is not generally an increasing-exponent prefix', 'general_exact_dense_formula_resolved': False, 'full_problem_resolved': False, 'novelty_claimed': False, 'formal_certification': False, 'human_peer_review_claimed': False, 'technau_2026': 'Published degree-bounded result credited; not an arbitrary-support term-count theorem', 'newman_1978_and_1979_erratum': 'Bibliographic attribution only; original full texts not inspected', 'source_documents_included': False, 'dataset_contents_included': False, 'private_coordination_included': False}
EXPECTED_ALLOWLIST={'schema': 'bounded-polynomial-publication-allowlist-v1', 'accepted_files': {'original/public/README.md': {'bytes': 1140, 'sha256': 'c694929116246d5494e75a14180b902bbf3e96bf7c4c2fd2ad49fb36e445e144'}, 'original/public/REPORT.md': {'bytes': 14281, 'sha256': '7851e655463054aa6313de3cb19b220abfa110e4e30720a1aa2bef3c6535997a'}, 'original/public/fixtures.json': {'bytes': 427, 'sha256': 'dee04b8b72af0ad3ff9022f079e0b93481fcf6f59fa81eded4eb17681ade2966'}, 'original/public/provenance.json': {'bytes': 798, 'sha256': '01470c43aa69c1bf7ede63755c0d6f0e3bae466f05bccb6cf2bc730672180fa4'}, 'original/public/sources.json': {'bytes': 2966, 'sha256': '96a06dbdaaa37c544d73e8e9c479a3b62de3312728bed3152893936f8430339b'}, 'original/public/verify.py': {'bytes': 6902, 'sha256': 'd30c41ef27e19b483ca4787ba1f8e942a3cf9d6f3772b64c508a57939fd55001'}, 'original/external/AUDIT_INSTRUCTIONS.md': {'bytes': 1845, 'sha256': '62bd4b00f45bebb0a38b71ddfa40a9764f5d998b33e7591e4fc1df4dd9225750'}, 'original/external/MANIFEST.json': {'bytes': 919, 'sha256': '6ea1b356144ded0d39f7c7469f94ea7e8546de8e4bb440e36cce5e48d4661dd9'}, 'original/external/PINS.json': {'bytes': 900, 'sha256': '4d164a991c90fa93d23a4349b6d90698ca29ff6ca0631d949fd546bdbb4d5781'}, 'original/external/TEST_RESULTS.json': {'bytes': 3607, 'sha256': 'c5e3ba9752096972eade1095af80398970cff6148670547d92190a1bca5474a0'}, 'original/external/bootstrap.py': {'bytes': 3369, 'sha256': 'caf367205cefac84461fbd5e270c3cad7548f4bb18bbb169857c42ca3f914196'}, 'original/external/test_harness.py': {'bytes': 7983, 'sha256': 'bd055782f2851e7644a02115de763649638c3253e2c0a03d31d77f9754fb5845'}, 'original/bounded_partial_sums_2304003_frozen.tar.gz': {'bytes': 15909, 'sha256': '0e66432923a00ba78a2926096779430a0bbfb630edfcf299fcc20e77c6417989'}, 'audit/public/AUDIT_MANIFEST.json': {'bytes': 1397, 'sha256': '0e7ba492e8f7fa7a836ca2fd5c0226626df7a4e07db61573229abe13bb78d9e1'}, 'audit/public/INDEPENDENT_PROVENANCE.json': {'bytes': 535, 'sha256': '9824c71227ce7cddd5eb70d926cbd15645a4bafb6ff6aab6d0b0cd9e20a3f4c8'}, 'audit/public/INDEPENDENT_TEST_RESULTS.json': {'bytes': 28355, 'sha256': 'dcd01544dea852521650d28047bb611300879e7a6350bb4c6bdce9ef4389ca74'}, 'audit/public/MATHEMATICAL_AUDIT.md': {'bytes': 19113, 'sha256': '71bf1644db3ed1a688819c5a9c26803eb04d3a36184f6c3d224169d2023c38d9'}, 'audit/public/REPRODUCED_TEST_RESULTS.json': {'bytes': 3607, 'sha256': 'c5e3ba9752096972eade1095af80398970cff6148670547d92190a1bca5474a0'}, 'audit/public/REVIEW_DISPOSITION.json': {'bytes': 1062, 'sha256': '2f2bece141389611381d2e0b3fcdd0ca94f16a99f10aeca4cc6489e2f0f3cf5a'}, 'audit/public/SNAPSHOT_HASHES.json': {'bytes': 2142, 'sha256': 'fa7625662f74a032b332ef51375ba030471f62a846762169363534d5def8f0c2'}, 'audit/public/SOURCE_INSPECTION.json': {'bytes': 3321, 'sha256': '9e31842aadc3353986d2ed50087bfdc802a412e3e6dfca0c1d748ad0fd18e4a5'}, 'audit/public/independent_checks.py': {'bytes': 10747, 'sha256': 'cbe9d7dcb3653d0274cbc6a52b035ab3db68124bf598fce3e9aba92ef387b2a9'}, 'audit/bounded_partial_sums_2304003_independent_audit_frozen.tar.gz': {'bytes': 16530, 'sha256': 'd545febe7c0b2deb080f7934aba126879ab43826d4d2382f48cc0b90820b18cd'}}, 'original_archive_members': ['public/README.md', 'public/REPORT.md', 'public/fixtures.json', 'public/provenance.json', 'public/sources.json', 'public/verify.py', 'external/AUDIT_INSTRUCTIONS.md', 'external/MANIFEST.json', 'external/PINS.json', 'external/TEST_RESULTS.json', 'external/bootstrap.py', 'external/test_harness.py'], 'audit_archive_members': ['public/AUDIT_MANIFEST.json', 'public/INDEPENDENT_PROVENANCE.json', 'public/INDEPENDENT_TEST_RESULTS.json', 'public/MATHEMATICAL_AUDIT.md', 'public/REPRODUCED_TEST_RESULTS.json', 'public/REVIEW_DISPOSITION.json', 'public/SNAPSHOT_HASHES.json', 'public/SOURCE_INSPECTION.json', 'public/independent_checks.py'], 'source_documents': False, 'source_extracts': False, 'dataset_contents': False, 'private_coordination': False, 'source_retrieval_in_publication_replay': 'NOT_RUN', 'source_inspection_in_publication_replay': 'NOT_RUN', 'corpus_rehash_in_publication_replay': 'NOT_RUN', 'record_join_in_publication_replay': 'NOT_RUN', 'instruction_document_review': 'external/AUDIT_INSTRUCTIONS.md was read in full: generic external-pin and replay instructions, with no private coordination payload. Preserved unchanged.'}
ACCEPTED_PINS={'original/public/README.md': {'bytes': 1140, 'sha256': 'c694929116246d5494e75a14180b902bbf3e96bf7c4c2fd2ad49fb36e445e144'}, 'original/public/REPORT.md': {'bytes': 14281, 'sha256': '7851e655463054aa6313de3cb19b220abfa110e4e30720a1aa2bef3c6535997a'}, 'original/public/fixtures.json': {'bytes': 427, 'sha256': 'dee04b8b72af0ad3ff9022f079e0b93481fcf6f59fa81eded4eb17681ade2966'}, 'original/public/provenance.json': {'bytes': 798, 'sha256': '01470c43aa69c1bf7ede63755c0d6f0e3bae466f05bccb6cf2bc730672180fa4'}, 'original/public/sources.json': {'bytes': 2966, 'sha256': '96a06dbdaaa37c544d73e8e9c479a3b62de3312728bed3152893936f8430339b'}, 'original/public/verify.py': {'bytes': 6902, 'sha256': 'd30c41ef27e19b483ca4787ba1f8e942a3cf9d6f3772b64c508a57939fd55001'}, 'original/external/AUDIT_INSTRUCTIONS.md': {'bytes': 1845, 'sha256': '62bd4b00f45bebb0a38b71ddfa40a9764f5d998b33e7591e4fc1df4dd9225750'}, 'original/external/MANIFEST.json': {'bytes': 919, 'sha256': '6ea1b356144ded0d39f7c7469f94ea7e8546de8e4bb440e36cce5e48d4661dd9'}, 'original/external/PINS.json': {'bytes': 900, 'sha256': '4d164a991c90fa93d23a4349b6d90698ca29ff6ca0631d949fd546bdbb4d5781'}, 'original/external/TEST_RESULTS.json': {'bytes': 3607, 'sha256': 'c5e3ba9752096972eade1095af80398970cff6148670547d92190a1bca5474a0'}, 'original/external/bootstrap.py': {'bytes': 3369, 'sha256': 'caf367205cefac84461fbd5e270c3cad7548f4bb18bbb169857c42ca3f914196'}, 'original/external/test_harness.py': {'bytes': 7983, 'sha256': 'bd055782f2851e7644a02115de763649638c3253e2c0a03d31d77f9754fb5845'}, 'original/bounded_partial_sums_2304003_frozen.tar.gz': {'bytes': 15909, 'sha256': '0e66432923a00ba78a2926096779430a0bbfb630edfcf299fcc20e77c6417989'}, 'audit/public/AUDIT_MANIFEST.json': {'bytes': 1397, 'sha256': '0e7ba492e8f7fa7a836ca2fd5c0226626df7a4e07db61573229abe13bb78d9e1'}, 'audit/public/INDEPENDENT_PROVENANCE.json': {'bytes': 535, 'sha256': '9824c71227ce7cddd5eb70d926cbd15645a4bafb6ff6aab6d0b0cd9e20a3f4c8'}, 'audit/public/INDEPENDENT_TEST_RESULTS.json': {'bytes': 28355, 'sha256': 'dcd01544dea852521650d28047bb611300879e7a6350bb4c6bdce9ef4389ca74'}, 'audit/public/MATHEMATICAL_AUDIT.md': {'bytes': 19113, 'sha256': '71bf1644db3ed1a688819c5a9c26803eb04d3a36184f6c3d224169d2023c38d9'}, 'audit/public/REPRODUCED_TEST_RESULTS.json': {'bytes': 3607, 'sha256': 'c5e3ba9752096972eade1095af80398970cff6148670547d92190a1bca5474a0'}, 'audit/public/REVIEW_DISPOSITION.json': {'bytes': 1062, 'sha256': '2f2bece141389611381d2e0b3fcdd0ca94f16a99f10aeca4cc6489e2f0f3cf5a'}, 'audit/public/SNAPSHOT_HASHES.json': {'bytes': 2142, 'sha256': 'fa7625662f74a032b332ef51375ba030471f62a846762169363534d5def8f0c2'}, 'audit/public/SOURCE_INSPECTION.json': {'bytes': 3321, 'sha256': '9e31842aadc3353986d2ed50087bfdc802a412e3e6dfca0c1d748ad0fd18e4a5'}, 'audit/public/independent_checks.py': {'bytes': 10747, 'sha256': 'cbe9d7dcb3653d0274cbc6a52b035ab3db68124bf598fce3e9aba92ef387b2a9'}, 'audit/bounded_partial_sums_2304003_independent_audit_frozen.tar.gz': {'bytes': 16530, 'sha256': 'd545febe7c0b2deb080f7934aba126879ab43826d4d2382f48cc0b90820b18cd'}}
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
    for k,v in [('schema','bounded-polynomial-publication-manifest-v1'),('problem_id',2304003),('rank',1032),('disposition','unsolved'),('proof_turns',5),('scope','five unchanged partial approaches; term-count question unresolved')]:exact(m[k],v,'manifest '+k)
    need(type(m['files']) is list and 1<=len(m['files'])<=100,'manifest files');expected={'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'}
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');n=e['path'];need(safe(n) and n not in expected,'unsafe or duplicate path');expected.add(n)
        need(n in f,'missing member: '+n);identity(f[n],{k:e[k] for k in ['bytes','sha256']})
    need(set(f)==expected,'file inventory mismatch');need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory mismatch')
def authenticate(root):
    f,dirs=inventory(root);need('PUBLICATION_MANIFEST.json' in f,'missing manifest');raw=f['PUBLICATION_MANIFEST.json'];need(sha(raw)==EXPECTED_MANIFEST,'manifest external pin');validate_manifest(load(raw),f,dirs)
    need(f['VERIFY_PUBLICATION.py']==read(Path(__file__)),'different verifier copy');return f
def archive_members(b,expected):
    with tarfile.open(fileobj=io.BytesIO(b),mode='r:gz') as t:
        entries=t.getmembers();names=[e.name for e in entries]
        need(len(names)==len(set(names)) and set(names)==set(expected),'archive inventory')
        for e in entries:
            need(safe(e.name) and e.isfile() and not e.pax_headers and e.mode==0o444,'unsafe archive member')
            need(e.size==len(expected[e.name]),'archive size');need(t.extractfile(e).read()==expected[e.name],'archive bytes')
    return len(expected)
def semantics(f):
    exact(load(f['CLAIMS.json']),EXPECTED_CLAIMS,'claims')
    exact(load(f['PUBLICATION_ALLOWLIST.json']),EXPECTED_ALLOWLIST,'publication allowlist')
    for n,pin in ACCEPTED_PINS.items():identity(f['accepted/'+n],pin)
    for n,b in f.items():
        if n.endswith('.json'):load(b)
    archive_counts={}
    for group,key,archive in [('original','original_archive_members','bounded_partial_sums_2304003_frozen.tar.gz'),('audit','audit_archive_members','bounded_partial_sums_2304003_independent_audit_frozen.tar.gz')]:
        members={n:f['accepted/'+group+'/'+n] for n in EXPECTED_ALLOWLIST[key]}
        archive_counts[group]=archive_members(f['accepted/'+group+'/'+archive],members)
    original=load(f['accepted/original/external/MANIFEST.json'])
    exact(original['schema_version'],1);need(set(e['name'] for e in original['files'])=={'README.md','REPORT.md','fixtures.json','provenance.json','sources.json','verify.py'},'original file inventory')
    for e in original['files']:identity(f['accepted/original/public/'+e['name']],{k:e[k] for k in ['bytes','sha256']})
    audit=load(f['accepted/audit/public/AUDIT_MANIFEST.json']);exact(audit['schema_version'],1)
    exact(audit['source_free'],True);exact(audit['contains_source_documents_or_dataset_contents'],False)
    need(set(e['name'] for e in audit['files'])=={n.removeprefix('public/') for n in EXPECTED_ALLOWLIST['audit_archive_members'] if n!='public/AUDIT_MANIFEST.json'},'audit file inventory')
    for e in audit['files']:identity(f['accepted/audit/public/'+e['name']],{k:e[k] for k in ['bytes','sha256']})
    disposition=load(f['accepted/audit/public/REVIEW_DISPOSITION.json'])
    for k,v in [('schema_version',1),('problem_id',2304003),('rank',1032),('mathematical_approaches',5),('mathematical_disposition','ACCEPTED_PARTIAL_PROGRESS_UNRESOLVED'),('general_term_count_question_resolved',False),('general_exact_degree_bounded_question_resolved',False),('novelty_claim',False),('mathematical_corrections_required',False),('original_snapshot_preserved',True),('source_documents_included',False)]:exact(disposition[k],v,'disposition '+k)
    fixture=load(f['accepted/original/public/fixtures.json'])
    for k,v in [('problem_id',2304003),('approaches_counted',5),('searches_counted',0),('status','PARTIAL_PROGRESS_UNRESOLVED')]:exact(fixture[k],v,'fixture '+k)
    provenance=load(f['accepted/original/public/provenance.json'])
    for k,v in [('problem_id',2304003),('rank',1032),('problem_number','AMR-022-4003'),('mathematical_approaches',5),('source_contents_included',False)]:exact(provenance[k],v,'provenance '+k)
    source=load(f['accepted/original/public/sources.json'])
    exact(source['publication_status']['status'],'published')
    exact(source['publication_status']['doi'],'https://doi.org/10.1017/fms.2026.10213')
    exact([s['full_text_inspected'] for s in source['bibliographic_only']],[False,False])
    return {'accepted_files':len(ACCEPTED_PINS),'archive_members':archive_counts,'accepted_bytes_preserved':True}
def flags():return ['-I','-S','-B']+(['-'+'O'*sys.flags.optimize] if sys.flags.optimize else [])
def invoke(root,script,*args,cwd=None,env=None):
    r=subprocess.run([sys.executable,*flags(),str(root/script),*map(str,args)],cwd=cwd or root,env=env,capture_output=True,timeout=600)
    need(r.returncode==0 and not r.stderr,'replay failed '+script+': '+r.stderr.decode('utf8','replace'));return load(r.stdout)
def modes(root):return {str(p.relative_to(root)):stat.S_IMODE(p.stat().st_mode) for p in (root,*root.rglob('*'))}
def permissions(root,readonly):
    if not readonly:root.chmod(0o755)
    for p in root.rglob('*'):p.chmod((0o555 if p.is_dir() else 0o444) if readonly else (0o755 if p.is_dir() else 0o644))
    root.chmod(0o555 if readonly else 0o755)
def denied_writes(root):
    need(os.geteuid()!=0,'nonroot required');count=0
    for p in (root,*root.rglob('*')):
        need(not p.stat().st_mode&0o222,'writable frozen input')
        try:
            with (p/'FORBIDDEN_WRITE' if p.is_dir() else p).open('xb' if p.is_dir() else 'ab'):pass
        except PermissionError:count+=1
        else:raise Reject('actual write succeeded')
    return count
def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'require -I -S -B')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');a=p.parse_args()
    root=a.root.absolute();before=authenticate(root);before_modes=modes(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':2304003,**report}
    need(os.getuid()!=0 and os.geteuid()!=0,'full replay requires nonroot for enforced read-only tests')
    with tempfile.TemporaryDirectory(prefix='bounded-polynomial-publication-') as tmp:
        work=Path(tmp);packet=work/'packet';packet.mkdir()
        for n,b in before.items():q=packet/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        hostile=work/'hostile imports';hostile.mkdir();marker=hostile/'UNTRUSTED_EXECUTED'
        for n in ['json.py','hashlib.py','sitecustomize.py','subprocess.py','fractions.py']:(hostile/n).write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\nraise RuntimeError("hijack")\n')
        env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONHOME=str(hostile/'nonexistent'),PYTHONOPTIMIZE='2',PYTHONDONTWRITEBYTECODE='0')
        permissions(packet,True)
        try:
            frozen_modes=modes(packet);denials=denied_writes(packet)
            author=invoke(packet,'accepted/original/external/test_harness.py',packet/'accepted/original/public',packet/'accepted/original/external','6ea1b356144ded0d39f7c7469f94ea7e8546de8e4bb440e36cce5e48d4661dd9',cwd=hostile,env=env)
            historical_author=load(before['accepted/original/external/TEST_RESULTS.json'])
            exact(author['uid'],os.getuid());exact(author['euid'],os.geteuid());need(type(author['python_version']) is str,'Python version')
            exact({k:v for k,v in author.items() if k not in ['uid','euid','python_version']},{k:v for k,v in historical_author.items() if k not in ['uid','euid','python_version']},'fresh author replay')
            exact([r['mode'] for r in author['reports']],['normal','O','OO']);exact([len(r['hostile_fixtures_rejected']) for r in author['reports']],[20,20,20]);exact(len(author['tamper_controls_rejected_in_all_modes']),10)
            independent=invoke(packet,'accepted/audit/public/independent_checks.py',packet/'accepted/original',cwd=hostile,env=env)
            exact(independent,load(before['accepted/audit/public/INDEPENDENT_TEST_RESULTS.json']),'fresh independent replay')
            exact(independent['independent_identity_counts']['dense_shifted_cuts'],8385)
            exact([r['mode'] for r in independent['modes']],['normal','O','OO'])
            exact([len(r['malformed_rejections']) for r in independent['modes']],[64,64,64])
            for mode in independent['modes']:
                for r in mode['malformed_rejections']:
                    need(type(r['exit_code']) is int and r['exit_code']!=0,'malformed exit code')
                    exact(r['structured_json_error'],r['label']!='deep_nesting','known diagnostic boundary')
            need(not marker.exists() and not any(p.name=='__pycache__' for p in work.rglob('*')),'hostile import or bytecode write')
            need(authenticate(packet)==before and modes(packet)==frozen_modes,'frozen packet changed')
            report.update(read_only={'uid':os.geteuid(),'actual_write_denials':denials,'packet_bytes_and_modes_unchanged':True,'hostile_environment_ignored':True},fresh_author={'modes':['normal','O','OO'],'identity_counts_per_mode':author['reports'][0]['positive_exact_identities'],'malformed_rejections_per_mode':20,'tamper_rejections_per_mode':10},fresh_independent={'identity_counts_per_invocation':independent['independent_identity_counts'],'malformed_rejections_per_mode':64,'malformed_rejections_all_three_modes':192,'valid_boundary_cases_per_mode':2,'deep_nesting':'nonzero exit; no success stdout; unstructured RecursionError diagnostic; no acceptance bypass'})
        finally:permissions(packet,False)
    need(authenticate(root)==before and modes(root)==before_modes,'input publication changed')
    return {'schema':'bounded-polynomial-publication-replay-v1','status':'PASS_SCOPED_PARTIAL_RESULTS','problem_id':2304003,'rank':1032,'queue_status':'unsolved','proof_turns':5,'full_problem_resolved':False,'novelty_claimed':False,'formal_certification':False,'human_peer_review':False,'historical_receipts_preserved':True,'current_source_rehash':'NOT_RUN','current_corpus_rehash':'NOT_RUN','current_record_join':'NOT_RUN','fresh_source_retrieval':'NOT_RUN','fresh_source_inspection':'NOT_RUN','github_ci':'NOT_RUN','publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,allow_nan=False))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,RecursionError,subprocess.SubprocessError,tarfile.TarError) as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
