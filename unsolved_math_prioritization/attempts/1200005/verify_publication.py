#!/usr/bin/env python3
"""Fail-closed, offline verification of the unchanged research and audit freezes."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
FROZEN={'QUESTIONS_1200005_AUTHOR_SAFE_FREEZE.zip': {'bytes': 21562, 'sha256': '6a4403908dcf263fe30c005e94078c116cbb4a6e14db6009b3ac865576a68fb0'}, 'author/CLAIMS.json': {'bytes': 590, 'sha256': '15c4634e0079eb25245c947a4109036eafac9b2a1a4423f5ec3c90a41538e166'}, 'author/CONTROL_RESULTS.json': {'bytes': 2077, 'sha256': '0608327467da27a64bccbecce51d6446616cffeda2d4c0e2c6f413e669243ee4'}, 'author/LITERATURE.md': {'bytes': 5266, 'sha256': '1ec8d8dc5eb6f45caef2b8ac5ae503e430d2f89a2e140cc4025b0493eed65ddf'}, 'author/MANIFEST.json': {'bytes': 1377, 'sha256': '7945b043809987bd5e6af09ee2bd279aaca7855698d9d556cd17a0c081b85aa5'}, 'author/PROOFS.md': {'bytes': 11802, 'sha256': '4b5e0e97f6d655473aa31c6cd56e86d6437df0287cc9e99798367ee688e5418d'}, 'author/README.md': {'bytes': 2653, 'sha256': 'a4828a87dbfd5c3b0984a190359a5708ad001517846276561c801f8800eb4006'}, 'author/RESEARCH_LOG.md': {'bytes': 4436, 'sha256': '47d8fdc1999d2f751d18ecbac6912df09b9aedb311e79ad7faaa81541f0e7fd5'}, 'author/SOURCE_VERIFICATION.json': {'bytes': 7836, 'sha256': '35a42b6a98116f34dbe9798bfc1d6c9fc0885b4f124c484a53bd31d7a6c78a98'}, 'author/controls.py': {'bytes': 12746, 'sha256': '6785e91a61486ced604709ce78c4ebba09e7501df8a7256a4356fc8cc1190533'}, 'author/verify.py': {'bytes': 1601, 'sha256': '9cc8ccaabe255068b59813b8b6fe9e3ce6839ff3d67cb84f16f84403488f7e94'}, 'independent_audit/AUDIT.md': {'bytes': 12227, 'sha256': '26243857c627ae4700f976b03e3d14adf239f090b703af3786aa05ba8382a3e0'}, 'independent_audit/AUDIT_MANIFEST.json': {'bytes': 1514, 'sha256': '57b2d08b11d7662502c9390fb9abc9acd6c0f620b8d2f5090ce84eefb625e384'}, 'independent_audit/CORRECTIONS.md': {'bytes': 1701, 'sha256': 'e69d869cb75cade6c5e898b7e2b4d7b67386194d8a1f113253b71c1e4dd0420a'}, 'independent_audit/INDEPENDENT_RESULTS.json': {'bytes': 2165, 'sha256': '587ee03941ec078915a377a7987aee21ed88eb717bb20fec52885e24012a12b9'}, 'independent_audit/README.md': {'bytes': 1635, 'sha256': 'c3d6e28c2209baa6115ce0c3787eacf54548b9e06c9da6a7bbb3fef35855c9ee'}, 'independent_audit/SOURCE_AUDIT.json': {'bytes': 6286, 'sha256': '6086bed8f9c24ae38859520aab7b2cd8b74dc00a64b581562120b1700f746e85'}, 'independent_audit/independent_verifier.py': {'bytes': 14667, 'sha256': 'faf6ddcfa0e9fc0974220ebfc4989ee390673c14791bf2f1a6867a1344e78160'}, 'independent_audit/replay_audit.py': {'bytes': 1662, 'sha256': '370892255415c3d9f9c1f7a4cf3adfba5d563b8f48cc17c266224b17a9cc9c1d'}}
SCOPE={'problem_id': 1200005, 'problem_code': 'AMR-011-0005', 'rank': 755, 'status': 'unsolved', 'turns': '5/5', 'mathematical_status': 'SCOPED PARTIAL RESULTS ONLY', 'audit_verdict': 'PASS for the stated partial results; no mandatory correction', 'target': 'Minimum nonempty reduced coefficient-free law length in the depth-n full binary-tree automorphism group, with expanded letter length and arbitrary finite variable rank', 'all_rank_general_bound': 'n < L_n <= 2^n', 'all_rank_exact_depths': {'1': 2, '2': 4, '3': 8}, 'fixed_two_variable_exact_depths': {'4': 16}, 'depth_four_all_rank_claim': False, 'source_indexing': 'Our W_n has n factors, W_0 trivial; Bradford uses W_0=C2, so its W_n has n+1 factors. Replace its index by n-1.', 'full_candidate': False, 'target_resolved': False, 'novelty_claim': False, 'formal_verification': False, 'external_human_peer_review': False, 'publication_boundary': 'Authored proof, code, audit, exact results and public verification metadata only; no source PDFs, extracts, raw dataset contents or private coordination'}
def require(ok,message):
    if not ok: raise RuntimeError(message)
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify():
    require(not ROOT.is_symlink(),'symlink root')
    require(not (ROOT/'PUBLICATION_MANIFEST.json').is_symlink(),'symlink manifest')
    manifest=json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_bytes())
    expected=set(manifest['files'])|{'PUBLICATION_MANIFEST.json'}
    require(all(not p.startswith('/') and '..' not in Path(p).parts for p in expected),'unsafe path')
    expect_dirs={p.as_posix() for name in expected for p in Path(name).parents if p.as_posix()!='.'}
    files=set();dirs=set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'symlink: '+str(p))
        rel=p.relative_to(ROOT).as_posix()
        if p.is_file(): files.add(rel)
        elif p.is_dir(): dirs.add(rel)
        else: require(False,'special file')
    require(files==expected,'file allowlist')
    require(dirs==expect_dirs,'directory allowlist')
    for name,meta in manifest['files'].items(): require(pin((ROOT/name).read_bytes())==meta,'manifest '+name)
    for name,meta in FROZEN.items(): require(pin((ROOT/name).read_bytes())==meta,'frozen '+name)
    require(json.loads((ROOT/'PUBLICATION.json').read_bytes())==SCOPE,'scope boundary')
    with zipfile.ZipFile(ROOT/'QUESTIONS_1200005_AUTHOR_SAFE_FREEZE.zip') as z:
        names=z.namelist();allowed={p.name for p in (ROOT/'author').iterdir()}
        require(len(names)==len(set(names)) and set(names)==allowed,'archive allowlist')
        for name in names: require(z.read(name)==(ROOT/'author'/name).read_bytes(),'archive member '+name)
    for folder,name in [('author','MANIFEST.json'),('independent_audit','AUDIT_MANIFEST.json')]:
        m=json.loads((ROOT/folder/name).read_bytes())
        require(set(m['files'])|{name}=={p.name for p in (ROOT/folder).iterdir()},'original allowlist '+folder)
        for p,meta in m['files'].items(): require(pin((ROOT/folder/p).read_bytes())==meta,'original manifest '+p)
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    with tempfile.TemporaryDirectory(prefix='binary-wreath-replay-') as d:
        # A normal child is essential: the frozen author controls use assertions.
        # Parent -O and PYTHONOPTIMIZE must not disable them.
        probe=subprocess.run([sys.executable,'-B','-c','import sys; print(sys.flags.optimize)'],env=env,capture_output=True,text=True,check=True)
        require(probe.stdout.strip()=='0','child assertions disabled')
        run=subprocess.run([sys.executable,'-B',str(ROOT/'independent_audit/replay_audit.py'),'--author',str(ROOT/'author')],cwd=d,env=env,capture_output=True,text=True)
        require(run.returncode==0,'independent replay failed: '+run.stderr)
        audit=json.loads(run.stdout)
        require(audit=={'status':'PASS','audit_bound_files':7,'mathematical_scope':'partial claims only; unsolved target','independent_results_sha256':'587ee03941ec078915a377a7987aee21ed88eb717bb20fec52885e24012a12b9'},'audit result mismatch')
    for name,meta in FROZEN.items(): require(pin((ROOT/name).read_bytes())==meta,'changed after replay '+name)
    return {'result':'PASS','problem_id':1200005,'status':'unsolved','turns':'5/5','packet_files':len(expected),'frozen_files_and_archives':len(FROZEN),'author_and_independent_replay':'PASS','child_assertions_enabled':True,'independent_counterevaluations':13590,'depth_four_scope':'two variables only','target_resolved':False,'novelty_claim':False}
if __name__=='__main__': print(json.dumps(verify(),indent=2))
