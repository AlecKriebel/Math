#!/usr/bin/env python3
"""Offline, fail-closed verification of preserved EP-100 partial-result freezes."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,stat,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
FROZEN={'ERDOS_1929_AUTHOR_SAFE_FREEZE.zip': {'bytes': 20826, 'sha256': 'eab5d5ccc69c6fd8ef9771d14ca78c9da36fc31ddfc32052b718bce97684ce62'}, 'ERDOS_1929_INDEPENDENT_AUDIT.zip': {'bytes': 16238, 'sha256': 'e4eb14f0b28b285f7073bdce7e68c2473ea596c1ee8e65d87d44fc48d53f89e3'}, 'author/AUTHOR_CHECKS.json': {'bytes': 640, 'sha256': '2ee179bdff0de94338321ee0f01857b67e37835c6ce881b9cf32d511a805d377'}, 'author/CONTROL_RESULTS.json': {'bytes': 955, 'sha256': '61735a1c55f8a01b6d5ffb361842a1223420edffdb233d6702000c7e56d970d2'}, 'author/MANIFEST.json': {'bytes': 1303, 'sha256': '6156bec0ed953bc03854b4f6926b10eb9d8a4c3a1e676247716374e712a3bedc'}, 'author/PROOFS.md': {'bytes': 13902, 'sha256': 'f387b836a7b5c80cf3dfc9ce76a29d601311db2a9365a327aa242342c41d28ae'}, 'author/README.md': {'bytes': 2868, 'sha256': '3966ece7c3805891b13113e86fa987938dcc965deb40f3061be1362d017cc6f7'}, 'author/RESEARCH_LOG.md': {'bytes': 5405, 'sha256': '073e7de26bb5ba5ef8393b13344784cbd8849512b127f1fd914c6505217f309c'}, 'author/SOURCE_VERIFICATION.json': {'bytes': 9254, 'sha256': '18a11e22c26cb9711a2ba194ffa6ad0b10d7ad7fb63c464c7caeca1ec8c46575'}, 'author/verify_manifest.py': {'bytes': 4227, 'sha256': '86b322afa7c20d5d7a7a26eaddf6cd28c031f8ef16c981252f5b5e55709a71df'}, 'author/verify_math.py': {'bytes': 8552, 'sha256': '8e56ad2921372d4708301204730f672b99eafbcc4ef591bb6b82da511ec8d9b9'}, 'independent_audit/AUDIT_MANIFEST.json': {'bytes': 1168, 'sha256': '2231a5d62276eb43695f53e1f75a0e67cab69330748fe8771029ac0f511948da'}, 'independent_audit/AUDIT_REPORT.md': {'bytes': 12121, 'sha256': 'b88b5ab80179dd6e6103164dcdcd271c78911d4a9553f62a4a7345a35adf0ffe'}, 'independent_audit/INDEPENDENT_RESULTS.json': {'bytes': 2877, 'sha256': '14981b186540665e0bd80780f4cfcbf137a1ae6646a5b6367c574291f1890b9c'}, 'independent_audit/REPLAY_AND_MUTATION_RESULTS.json': {'bytes': 911, 'sha256': 'c2c4f42b2d8d091d7216cd86469990f324542c7525577b4aa568d8a87fb45f27'}, 'independent_audit/SOURCE_AUDIT.json': {'bytes': 5259, 'sha256': 'b476091a3445c320d6fdab05c2a6fc9632521ddca37b0e6d3f06785b9a5bb73c'}, 'independent_audit/VERDICT.json': {'bytes': 799, 'sha256': 'e6f6b09e6a57d9b052f440f58b407af383167f7edfd1d09e184180995ae8d859'}, 'independent_audit/independent_verify.py': {'bytes': 11237, 'sha256': 'a1df4d27ffd2c9782fb3f36d1f70fec61798732a781db45aeede230ac63b9578'}, 'independent_audit/verify_audit_manifest.py': {'bytes': 1601, 'sha256': '7058f89e98e96228b876df25286a127086e15b15962b71d077c0333d0e88c7c5'}}
SCOPE={'schema': 1, 'problem_id': 1929, 'problem_code': 'EP-100', 'rank': 756, 'status': 'unsolved', 'turns': '5/5', 'mathematical_status': 'Audited partial results only; general linear-diameter target unresolved', 'audit_verdict': 'PASS within the retained-claims scope; no mandatory correction', 'exact_target': 'An absolute positive linear lower bound, eventually uniformly in n, for the diameter of n distinct planar points with minimum distance and gaps between unequal positive distance values at least one; repeated equal distances allowed, integrality not required', 'retained_elementary_bound': 'D >= sqrt((n-2)*(sqrt(n)-1)/12), a reconstruction of the historically known n^(3/4) order', 'stronger_imported_bound': 'Guth-Katz yields an absolute-constant n/log n lower bound; full theorem proof imported, not re-proved', 'special_case_boundary': 'Attained minimum distance exactly one is an additional hypothesis and cannot be obtained by rescaling general admissible instances', 'finite_counterexample_boundary': 'Piepmeyer credited nine-point example refutes only the unqualified all-n D >= n-1 inequality, not either eventual conjecture', 'live_tracker_status_certified': False, 'formal_proof': False, 'full_resolution': False, 'novelty_or_priority_claim': False, 'external_human_peer_review': False, 'publication_boundary': 'Authored mathematics, code, audit, exact results, and public verification metadata only; excludes source PDFs, extracted source text, raw datasets, and private coordination'}

def require(ok,message):
    if not ok: raise RuntimeError(message)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def distinct(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'duplicate JSON key: '+key);result[key]=value
    return result
def read_json(path):return json.loads(Path(path).read_bytes(),object_pairs_hook=distinct)
def safe(name):
    return isinstance(name,str) and bool(name) and '\\' not in name and not name.startswith('/') and all(x not in ('','.','..') for x in name.split('/'))
def check_integrity():
    require(not ROOT.is_symlink(),'symlink root')
    manifest_path=ROOT/'PUBLICATION_MANIFEST.json'
    require(stat.S_ISREG(manifest_path.lstat().st_mode),'regular publication manifest required')
    manifest=read_json(manifest_path)
    require(set(manifest)=={'schema','problem_id','status','files'},'manifest schema')
    require(manifest['schema']==1 and manifest['problem_id']==1929 and manifest['status']=='unsolved','manifest identity')
    entries=manifest['files'];require(isinstance(entries,dict) and bool(entries),'manifest entries')
    require(all(safe(n) for n in entries),'unsafe path')
    expected=set(entries)|{'PUBLICATION_MANIFEST.json'}
    dirs={str(p) for name in expected for p in PurePosixPath(name).parents if str(p)!='.'}
    found_files=set();found_dirs=set()
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT).as_posix();mode=p.lstat().st_mode
        if stat.S_ISDIR(mode):found_dirs.add(rel)
        elif stat.S_ISREG(mode):found_files.add(rel)
        else:raise RuntimeError('nonregular member: '+rel)
    require(found_files==expected,'exact file allowlist');require(found_dirs==dirs,'exact directory allowlist')
    for name,meta in entries.items():
        require(set(meta)=={'bytes','sha256'} and type(meta['bytes']) is int and meta['bytes']>=0,'entry schema')
        require(pin((ROOT/name).read_bytes())==meta,'publication size/hash: '+name)
    for name,meta in FROZEN.items():require(pin((ROOT/name).read_bytes())==meta,'frozen size/hash: '+name)
    require(read_json(ROOT/'PUBLICATION.json')==SCOPE,'publication scope')
    for folder,archive,manifest_name in [('author','ERDOS_1929_AUTHOR_SAFE_FREEZE.zip','MANIFEST.json'),('independent_audit','ERDOS_1929_INDEPENDENT_AUDIT.zip','AUDIT_MANIFEST.json')]:
        allowed={p.name for p in (ROOT/folder).iterdir()}
        with zipfile.ZipFile(ROOT/archive) as z:
            names=z.namelist();require(len(names)==len(set(names)) and set(names)==allowed,'archive allowlist: '+archive)
            for info in z.infolist():
                require(not info.is_dir() and not stat.S_ISLNK(info.external_attr>>16),'archive member type')
                require(z.read(info)==(ROOT/folder/info.filename).read_bytes(),'archive bytes: '+info.filename)
        m=read_json(ROOT/folder/manifest_name);items=m['files'];names=[e['path'] for e in items]
        require(len(names)==len(set(names)) and set(names)|{manifest_name}==allowed,'frozen manifest allowlist')
        for e in items:require(pin((ROOT/folder/e['path']).read_bytes())=={'bytes':e['bytes'],'sha256':e['sha256']},'frozen manifest entry')
    return len(expected)

def verify():
    count=check_integrity()
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    with tempfile.TemporaryDirectory(prefix='ep100-replay-') as cwd:
        def run(args,ok=True):
            result=subprocess.run([sys.executable,'-B',*args],cwd=cwd,env=env,capture_output=True,text=True)
            if ok:require(result.returncode==0,'child failed: '+result.stderr)
            return result
        probe=run(['-c','import sys; print(sys.flags.optimize)'])
        require(probe.stdout.strip()=='0','author child assertions disabled')
        author=run([str(ROOT/'author/verify_math.py')])
        require(json.loads(author.stdout)==read_json(ROOT/'author/CONTROL_RESULTS.json'),'author control-output mismatch')
        negative=run(['-O',str(ROOT/'author/verify_math.py')],False)
        require(negative.returncode!=0 and 'requires active assertions' in negative.stderr,'author optimized-mode rejection')
        author_manifest=json.loads(run([str(ROOT/'author/verify_manifest.py'),'--self-test']).stdout)
        expected_replay=read_json(ROOT/'independent_audit/REPLAY_AND_MUTATION_RESULTS.json')
        require(author_manifest==expected_replay['author_manifest_replay'],'author manifest replay mismatch')
        require(json.loads(run([str(ROOT/'independent_audit/verify_audit_manifest.py')]).stdout)=={'passed':True,'files':7,'verdict':'PASS','problem_id':1929},'audit manifest replay mismatch')
        independent=run([str(ROOT/'independent_audit/independent_verify.py'),str(ROOT/'author')])
        optimized=run(['-O',str(ROOT/'independent_audit/independent_verify.py'),str(ROOT/'author')])
        expected=read_json(ROOT/'independent_audit/INDEPENDENT_RESULTS.json')
        require(json.loads(independent.stdout)==expected,'independent result mismatch')
        require(json.loads(optimized.stdout)==expected,'optimized independent result mismatch')
        require(independent.stdout==optimized.stdout,'independent normal/optimized bytes differ')
    require(check_integrity()==count,'post-replay integrity')
    return {'result':'PASS','problem_id':1929,'status':'unsolved','turns':'5/5','publication_files':count,'frozen_files_and_archives':len(FROZEN),'author_assertions_enabled':True,'author_optimized_mode_rejected':True,'independent_normal_and_optimized_outputs_equal':True,'author_manifest_mutation_controls':10,'piepmeyer_pair_checks':36,'general_target_resolved':False,'novelty_or_priority_claim':False}
if __name__=='__main__':print(json.dumps(verify(),sort_keys=True,indent=2))
