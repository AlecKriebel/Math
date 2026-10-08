#!/usr/bin/env python3
"""Externally authenticated, source-free replay of the five accepted restricted cycle-set approaches."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,io,json,math,os,re,stat,subprocess,sys,tempfile,tarfile
EXPECTED_MANIFEST='e18a365514b4c6f22e55387c76be4287488c47013fe618d83b886bfdf38307f9'
EXPECTED_CLAIMS={'schema': 'cycle-sets-publication-claims-v1', 'problem_id': 1919, 'code': 'EP-84', 'rank': 1017, 'status': 'unsolved', 'proof_turns': 5, 'proof_turn_limit': 5, 'f_definition': 'number of complete sets of simple-cycle lengths realized by n-vertex simple graphs', 'upper_assertion': 'credited_prior_Verstraete_Nenadov', 'lower_ratio_divergence': 'unresolved_here', 'exponential_growth_limit': 'unresolved_here', 'scope': 'five restricted partial approaches and explicit limitations', 'm_at_least_two_baseline_correction': True, 'exact_integer_ledger_correction': True, 'accepted_bytes_preserved': True, 'full_problem_resolved': False, 'novelty_claimed': False, 'formal_certification': False, 'human_peer_review_claimed': False, 'source_documents_included': False, 'dataset_contents_included': False, 'private_coordination_included': False}
ACCEPTED_PINS={'ARCHIVE_REPLAY.json': {'bytes': 1334, 'sha256': '7187dac6d4c43ccd67792f91346d2ac1840e00aff5a4de3a992d762e5f993103'}, 'AUDIT_FROZEN_REPLAY.json': {'bytes': 1010, 'sha256': '5c0740a0a316248965c9b4b842beb7935bd320f8f85e2ca1e3d6daad692ee522'}, 'EXTERNAL_RECEIPT.json': {'bytes': 3725, 'sha256': '30384f0568f25eaaeea11899c3d6c4e47d738ba253fd419fd750dcb81a415e62'}, 'PUBLICATION_ALLOWLIST.json': {'bytes': 7393, 'sha256': '403be4dc40904fbcfbd09a4592c9a3384152f3b99f3c66b23e925b5412e43826'}, 'audit/freeze/BOOTSTRAP_PINS.json': {'bytes': 458, 'sha256': 'a5cfe25ff246ad5322150b1ffdb7854e84601ea893f24e7f7a67277efeff8eb6'}, 'audit/freeze/FREEZE_MANIFEST.json': {'bytes': 1611, 'sha256': 'd7d4da929fa81626df3a30ecab6420144b7e78e669aa01df31435c2669b9f44c'}, 'audit/freeze/bootstrap.py': {'bytes': 1213, 'sha256': 'ccb097fdfc8a283df23d46671cf1c43bb5d54bb2850d183461eb048114220d23'}, 'audit/packet/ACCEPTANCE.json': {'bytes': 1486, 'sha256': '0eb5e87585d2e5450f91e281b2881f00343e3d07f199b7e2f9de331e064dff19'}, 'audit/packet/AUDIT.md': {'bytes': 16405, 'sha256': '36b4e3a774521e27a2533d3fecd71de32f7140ccfb38698d19f4c53e7be09860'}, 'audit/packet/INDEPENDENT_RESULTS.json': {'bytes': 3792, 'sha256': '3ce2f47f0a67c33b69c30a3d1e5fd3d247bf00406ba4db60d5ff118a421c2946'}, 'audit/packet/INTEGRITY_RESULTS.json': {'bytes': 61441, 'sha256': '9deed13a2af55da55d7cc7f1ce6d66d83e8af59511c7ad61acaeb266e6f19574'}, 'audit/packet/LEDGER_VALIDATION.patch': {'bytes': 994, 'sha256': '41d430b9cc38dc8aa42402cb2fc87b08cf6268649e1cc8b8da228267ff250b20'}, 'audit/packet/README.md': {'bytes': 2880, 'sha256': 'fa6104ca0b5be7b4568b0073d3a5ff3f42826f26e14059c3da8a5cb29bd92cf3'}, 'audit/packet/SOURCE_REVIEW.json': {'bytes': 3045, 'sha256': 'a5daead9f9ea1f9a6da06bba9d40c8b6c12e6c0a3657e766943394112658cdaa'}, 'audit/packet/check_ledger_correction.py': {'bytes': 4403, 'sha256': 'e9bd0cb75de57676b8a54ee24749c58da9bbb37b07149ce694ac2f7b296c03ba'}, 'audit/packet/extra_integrity_checks.py': {'bytes': 5596, 'sha256': 'ec777e52870b547ae11003d02cae03fac59d658692e247a43f7b2679640000e1'}, 'audit/packet/independent_checks.py': {'bytes': 9038, 'sha256': 'be18040f8321ca8c137a703dc5bc96303734ed20643d7b8e3639837c9158effe'}, 'audit/packet/verify_audit.py': {'bytes': 3651, 'sha256': '3c59c13ea69872363abf54aa422a06e1d72a58d755a3d1d6cbafac3d7b9f3aa9'}, 'corrected/freeze/BOOTSTRAP_PINS.json': {'bytes': 447, 'sha256': '5f2ac734035fe0cbcc1ec326f5c3d8bd989c29f54d6a4db704c80494e9962dc2'}, 'corrected/freeze/FREEZE_MANIFEST.json': {'bytes': 1257, 'sha256': 'af6631e1537a26720df4234f41974a8de54185e5bd625bc24d6997f3174c1958'}, 'corrected/freeze/bootstrap.py': {'bytes': 1455, 'sha256': '714afb752a56c50c447f778a2ffbf301b5c5f28b4fd99b54a1768151e5863304'}, 'corrected/packet/CORRECTION.patch': {'bytes': 4277, 'sha256': '8e191b40e683c145974a13815fdb1f6f05b622c6847007d157bd130a1a1a19a2'}, 'corrected/packet/CORRECTIONS.md': {'bytes': 940, 'sha256': 'b23276330577e6e2b7fd7e3faa7672791f58638bc157471030fa61e078609113'}, 'corrected/packet/LEDGER.json': {'bytes': 2259, 'sha256': 'aa06156c5c257c13a8b02783284c27fd7b9b0e5bacce51545f581bca70dac2fc'}, 'corrected/packet/README.md': {'bytes': 1637, 'sha256': 'd94d069649fd9870357f8b5541e2f0ddbcc1e7a5880c296473ba073440b26f7b'}, 'corrected/packet/REPORT.md': {'bytes': 16653, 'sha256': '86428f2fd218f8d6ebb54a9e6d6a0a9e8643ef8d2d99fb532fc524319bcd7083'}, 'corrected/packet/SOURCES.json': {'bytes': 3873, 'sha256': '2508ca4265ce262e5c3ded5adcc8775599e8abe65f0e93cd9231e6cac640fb8c'}, 'corrected/packet/STATUS.json': {'bytes': 581, 'sha256': '114b2c9d5b008c2322dbeedb5cd838128e64349c32fd9d404fd3de7311944a04'}, 'corrected/packet/proof_checks.py': {'bytes': 10196, 'sha256': 'bb7b8c1cbdd993360cc662b15816c33b5cfaafdcafa16cf65b5ca8b78529c4ce'}, 'corrected/packet/verify.py': {'bytes': 5427, 'sha256': '5603afacfc7d8754eb5a94b61097863b01776dcca023210e46e6e96090695945'}, 'historical_revision2/freeze/BOOTSTRAP_PINS.json': {'bytes': 447, 'sha256': '609fc2022b4214b4ed087d76524a99b62af0e7e74ae68c3aade711ae4bdb0b8b'}, 'historical_revision2/freeze/FREEZE_MANIFEST.json': {'bytes': 1257, 'sha256': '4a68c2510b717b1e6e4afcf267fdc0b40bf97a8156eab1c4c44c51f65e7410da'}, 'historical_revision2/freeze/bootstrap.py': {'bytes': 1455, 'sha256': 'b79a21252ad5d12e5cf44bed4543578d15226f15ed12c2d2594fa79697e9a950'}, 'historical_revision2/packet/CORRECTION.patch': {'bytes': 4277, 'sha256': '8e191b40e683c145974a13815fdb1f6f05b622c6847007d157bd130a1a1a19a2'}, 'historical_revision2/packet/CORRECTIONS.md': {'bytes': 940, 'sha256': 'b23276330577e6e2b7fd7e3faa7672791f58638bc157471030fa61e078609113'}, 'historical_revision2/packet/LEDGER.json': {'bytes': 2259, 'sha256': 'aa06156c5c257c13a8b02783284c27fd7b9b0e5bacce51545f581bca70dac2fc'}, 'historical_revision2/packet/README.md': {'bytes': 1637, 'sha256': 'd94d069649fd9870357f8b5541e2f0ddbcc1e7a5880c296473ba073440b26f7b'}, 'historical_revision2/packet/REPORT.md': {'bytes': 16653, 'sha256': '86428f2fd218f8d6ebb54a9e6d6a0a9e8643ef8d2d99fb532fc524319bcd7083'}, 'historical_revision2/packet/SOURCES.json': {'bytes': 3873, 'sha256': '2508ca4265ce262e5c3ded5adcc8775599e8abe65f0e93cd9231e6cac640fb8c'}, 'historical_revision2/packet/STATUS.json': {'bytes': 581, 'sha256': '114b2c9d5b008c2322dbeedb5cd838128e64349c32fd9d404fd3de7311944a04'}, 'historical_revision2/packet/proof_checks.py': {'bytes': 10196, 'sha256': 'bb7b8c1cbdd993360cc662b15816c33b5cfaafdcafa16cf65b5ca8b78529c4ce'}, 'historical_revision2/packet/verify.py': {'bytes': 5077, 'sha256': '7fb843326a441b6898836dc50b59fea41a6c9bf071352ad3470008a76f84e469'}, 'source_free_audit.tar.gz': {'bytes': 55104, 'sha256': '8ce03e7074c042754e2328a17e730d197b87fa056273c3eaa2cdf9e11f9c9ee2'}}
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
    for k,v in [('schema','cycle-sets-publication-manifest-v1'),('problem_id',1919),('rank',1017),('disposition','unsolved'),('proof_turns',5),('scope','five restricted partial approaches and explicit limitations')]:exact(m[k],v,'manifest '+k)
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
    for n,pin in ACCEPTED_PINS.items():identity(f['accepted/'+n],pin)
    for n,b in f.items():
        if n.endswith('.json'):load(b)
    a=load(f['accepted/PUBLICATION_ALLOWLIST.json'])
    exact(a['schema'],'erdos-cycle-sets-publication-allowlist-v1');exact(a['file_count'],38)
    for k in ['source_documents','source_extracts','dataset_contents','private_coordination','absolute_private_paths']:exact(a[k],False,'allowlist '+k)
    metadata=['PUBLICATION_ALLOWLIST.json','ARCHIVE_REPLAY.json','AUDIT_FROZEN_REPLAY.json','EXTERNAL_RECEIPT.json']
    exact(a['separate_metadata_deliverables'],metadata);exact(a['archive_deliverable'],'source_free_audit.tar.gz')
    need(set(ACCEPTED_PINS)==set(a['files'])|set(metadata)|{'source_free_audit.tar.gz'},'accepted exact inventory')
    members={}
    for n,e in a['files'].items():
        need(safe(n) and type(e) is dict and set(e)=={'bytes','sha256','mode'},'allowlist member schema')
        exact(e['mode'],'0o444');identity(f['accepted/'+n],{k:e[k] for k in ['bytes','sha256']});members[n]=f['accepted/'+n]
    count=archive_members(f['accepted/source_free_audit.tar.gz'],members)
    for slice in ['historical_revision2','corrected','audit']:
        prefix='accepted/'+slice+'/';manifest=load(f[prefix+'freeze/FREEZE_MANIFEST.json'])
        need(type(manifest) is dict and set(manifest)=={'schema','files'},'inner manifest shape')
        expected={n.removeprefix(prefix+'packet/'):b for n,b in f.items() if n.startswith(prefix+'packet/')}
        need(set(manifest['files'])==set(expected),'inner manifest exact files')
        for n,e in manifest['files'].items():need(safe(n) and '/' not in n,'inner path');identity(expected[n],e)
        pins=load(f[prefix+'freeze/BOOTSTRAP_PINS.json']);exact(pins['manifest_sha256'],sha(f[prefix+'freeze/FREEZE_MANIFEST.json']))
        exact(pins['bootstrap_sha256'],sha(f[prefix+'freeze/bootstrap.py']))
        exact(pins['verifier_sha256'],sha(f[prefix+'packet/'+('verify_audit.py' if slice=='audit' else 'verify.py')]))
    acceptance=load(f['accepted/audit/packet/ACCEPTANCE.json'])
    for k,v in [('problem_id',1919),('rank',1017),('proof_turns',5),('status','unsolved'),('full_problem_resolved',False),('formal_certification',False),('novelty_claim',False),('upper_assertion','credited_prior_literature'),('lower_assertion','unresolved_here'),('growth_rate_limit','unresolved_here')]:exact(acceptance[k],v,'acceptance '+k)
    ledger=load(f['accepted/corrected/packet/LEDGER.json'])
    for key in ['source_lookup_proof_turns','duplicate_gate_proof_turns','audit_packaging_proof_turns']:exact(ledger[key],0,'ledger '+key)
    exact([r['turn'] for r in ledger['approaches']],list(range(1,6)),'ledger turn order')
    for n in [n for n in members if n.startswith('corrected/packet/') and n!='corrected/packet/verify.py']:
        need(members[n]==members[n.replace('corrected/','historical_revision2/',1)],'changed mathematical bytes')
    receipt=load(f['accepted/EXTERNAL_RECEIPT.json'])
    for n,e in receipt['deliverables'].items():identity(f['accepted/'+n],e)
    exact(receipt['status'],'unsolved');exact(receipt['approaches_used'],5);exact(receipt['full_problem_resolved'],False)
    return {'accepted_public_files':len(ACCEPTED_PINS),'archive_members':count,'accepted_bytes_preserved':True}
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
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':1919,**report}
    need(os.geteuid()!=0,'full replay requires nonroot for enforced read-only tests')
    with tempfile.TemporaryDirectory(prefix='cycle-publication-') as tmp:
        work=Path(tmp);packet=work/'packet';packet.mkdir()
        for n,b in before.items():q=packet/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        hostile=work/'hostile imports';hostile.mkdir();marker=hostile/'UNTRUSTED_EXECUTED'
        for n in ['json.py','hashlib.py','sitecustomize.py','subprocess.py']:(hostile/n).write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\nraise RuntimeError("hijack")\n')
        env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONHOME=str(hostile/'nonexistent'),PYTHONOPTIMIZE='2',PYTHONDONTWRITEBYTECODE='0')
        permissions(packet,True)
        try:
            frozen_modes=modes(packet);denials=denied_writes(packet)
            corrected=invoke(packet,'accepted/corrected/freeze/bootstrap.py',packet/'accepted/corrected/packet',cwd=hostile,env=env)
            exact(corrected['integrity'],'pass');exact(corrected['optimize'],sys.flags.optimize);exact(corrected['uid'],os.geteuid());exact(corrected['no_formal_certification'],True)
            need(corrected['finite_checks']['main_problem_resolved'] is False,'author scope')
            audit=invoke(packet,'accepted/audit/freeze/bootstrap.py',packet/'accepted/audit/packet',cwd=hostile,env=env)
            exact(audit,{'audit_integrity':'pass','independent_mathematics':'finite_controls_pass','optimize':sys.flags.optimize,'uid':os.geteuid(),'finite_check_count':732874,'formal_certification':False,'full_problem_resolved':False},'independent audit')
            ledger=invoke(packet,'accepted/audit/packet/check_ledger_correction.py',packet/'accepted/historical_revision2',packet/'accepted/corrected')
            for k,v in [('case_count',14),('old_new_pairs',42),('old_direct_acceptances',42),('corrected_direct_rejections',42),('fixed_bootstrap_rejections',84),('frozen_bytes_and_modes_unchanged',True)]:exact(ledger[k],v,'ledger replay '+k)
            extra=invoke(packet,'accepted/audit/packet/extra_integrity_checks.py',packet/'accepted/historical_revision2')
            for k,v in [('strict_parser_cases',8),('strict_parser_runs',24),('all_fixed_bootstrap_mutations_rejected',True),('author_frozen_bytes_and_modes_unchanged',True)]:exact(extra[k],v,'historical parser '+k)
            controls=invoke(packet,'REPLAY_CORRECTED_CONTROLS.py',packet/'accepted/corrected')
            for k,v in [('hostile_case_count',34),('hostile_run_count',102),('frozen_files_unchanged',True)]:exact(controls[k],v,'corrected controls '+k)
            exact(len(controls['read_only_denials']),4);exact(len(controls['relocated_hostile_successes']),3)
            need(not marker.exists() and not any(p.name=='__pycache__' for p in work.rglob('*')),'hostile import or bytecode write')
            need(authenticate(packet)==before and modes(packet)==frozen_modes,'frozen packet changed')
            report.update(read_only={'uid':os.geteuid(),'actual_write_denials':denials,'packet_bytes_and_modes_unchanged':True,'hostile_environment_ignored':True},independent_all_graph_cases=33868,independent_finite_checks=732874,corrected_hostile_rejections=102,old_ledger_acceptances=42,corrected_ledger_rejections=42,fixed_bootstrap_ledger_rejections=84,historical_parser_rejections=24)
        finally:permissions(packet,False)
    need(authenticate(root)==before and modes(root)==before_modes,'input publication changed')
    return {'schema':'cycle-sets-publication-replay-v1','status':'PASS_SCOPED_PARTIAL_RESULTS','problem_id':1919,'rank':1017,'queue_status':'unsolved','proof_turns':5,'full_problem_resolved':False,'novelty_claimed':False,'formal_certification':False,'human_peer_review':False,'current_source_rehash':'NOT_RUN','current_corpus_rehash':'NOT_RUN','current_record_join':'NOT_RUN','fresh_source_retrieval':'NOT_RUN','fresh_source_inspection':'NOT_RUN','github_ci':'NOT_RUN','publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,RecursionError,subprocess.SubprocessError,tarfile.TarError) as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
