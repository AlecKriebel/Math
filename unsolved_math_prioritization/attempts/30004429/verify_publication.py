#!/usr/bin/env python3
"""Fail-closed, read-only delivery checks and deterministic exact replay."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
FROZEN={'SPECIFICATIONS_30004429_AUTHOR_SAFE_FREEZE.zip': {'bytes': 20899, 'sha256': 'a6b1e798dfa5776e174ed2bf01ee273c6923988d1cb1a2e3b846da63ef108d83'}, 'SPECIFICATIONS_30004429_INDEPENDENT_AUDIT_SAFE.zip': {'bytes': 16386, 'sha256': '2c6f66285bb4937b38c66e0f6412020a34a16f6a4a782316bf3e03d533897bae'}, 'author/APPROACHES.md': {'bytes': 4740, 'sha256': '785400ea2f14846a29d417caaf7af2b107488a3af1393bdc4c6dc4b4a1262bd5'}, 'author/CHECK_RESULTS.json': {'bytes': 2190, 'sha256': '366e6ecd8277305cf99c1711c526ad5efdd73c3dfb0b4bcafe182cb551542fac'}, 'author/MANIFEST.json': {'bytes': 1247, 'sha256': 'b840e923b5046dc8c0d4db028f2a6d70a1275b39b9b4caa7b88332e1d7162271'}, 'author/PRIOR_WORK_CHECK.json': {'bytes': 3069, 'sha256': '3179d72e4ad63c16780a089bf7280bc086521e66416e5a4f1147c8721fafc383'}, 'author/PROOFS.md': {'bytes': 17618, 'sha256': '93d89f8ba63f469339f923a311dc7b4f04271d001332a5d5d0ab099260745fe0'}, 'author/README.md': {'bytes': 4773, 'sha256': '5487a4c618c0632f10fa0aead3595569c9936a1eaae16194ffee391d26dcbb9b'}, 'author/SOURCE_VERIFICATION.json': {'bytes': 7533, 'sha256': '7ef7b0a4c0c5ac038a256358d4beea60fbe028c80821cf24e39117f5448cdfd0'}, 'author/verify_controls.py': {'bytes': 5656, 'sha256': 'edf4fb0cda695cf0807654ca66a4c3e96d7ba21a5ad70858cd809d19e948bd55'}, 'independent_audit/AUDIT_MANIFEST.json': {'bytes': 881, 'sha256': 'ff1e48733cc3f02d9197e5a27998d586905f4dabd8a4c782e84fe23468366d9a'}, 'independent_audit/AUDIT_REPORT.md': {'bytes': 15073, 'sha256': '311b242dff3417076aa97a964943e59df70fe3c85756e7e019bac04c161d1c77'}, 'independent_audit/AUDIT_SUMMARY.json': {'bytes': 1859, 'sha256': 'a0b2199b4bd1c41f6ba6d369d2435868b7411f7151136f49265d082b058cf007'}, 'independent_audit/INDEPENDENT_CHECK_RESULTS.json': {'bytes': 6441, 'sha256': 'e58c5545c8fdbc82c5fb586d696cc4ce2db7fe79d869f78c3e54106c2d4943f3'}, 'independent_audit/SOURCE_AUDIT.json': {'bytes': 5547, 'sha256': '343ce8cf219c24fc35a8ac428f35bb70b79a1ff457de529e7dce5e2f75ea0296'}, 'independent_audit/independent_verify.py': {'bytes': 9746, 'sha256': '936bf3e37c3d2f3bf1a701fcc529ae701f0b998f8c1f8d4058facc8aee85477e'}}
SCOPE={'problem_id': 30004429, 'problem_number': 'OWR-17474-001', 'rank': 751, 'status': 'unsolved', 'turns': '5/5', 'mathematical_status': 'NO RESOLUTION', 'audit_verdict': 'PASS within the partial-result scope', 'target': 'Singleton almost-Gibbs question for the horizontal-line marginal of the extremal plus phase of finite-temperature, zero-field 2D nearest-neighbor ferromagnetic Ising above beta_c', 'retained_results': ['Version-invariant essential-oscillation criterion', 'Extremal monochromatic-annulus reduction', 'Summable-log-variation sufficient one-sided transfer with unproved target hypothesis', 'Dense-null bad-version, mixture, and rare-evidence controls', 'Canonical continuity of the original absolutely summable Dyson interaction'], 'strict_mixture_essential_range': ['1/4', '3/4'], 'mixture_essential_bounds_interval': '[1/4,3/4]', 'covariance_convention': 'Displayed author covariances use {0,1} plus indicators; {-1,+1} spin covariances are four times those values', 'target_resolved': False, 'automatic_full_specification_extension': False, 'one_sided_continuity_implies_target': False, 'long_range_catalog_clause_resolved': False, 'novelty_claim': False, 'audit_is_peer_review': False, 'publication_boundary': 'Authored proof, code, audit, exact results and public verification metadata only; no source PDFs, extracts, dataset contents or private coordination'}
def require(ok,message):
    if not ok: raise AssertionError(message)
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify():
    require(not (ROOT/'PUBLICATION_MANIFEST.json').is_symlink(),'symlink manifest')
    manifest=json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_bytes())
    expected=set(manifest['files'])|{'PUBLICATION_MANIFEST.json'}
    require(all(not p.startswith('/') and '..' not in Path(p).parts for p in expected),'unsafe path')
    expect_dirs={str(p) for name in expected for p in Path(name).parents if str(p)!='.'}
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
    for archive,folder in [('SPECIFICATIONS_30004429_AUTHOR_SAFE_FREEZE.zip','author'),('SPECIFICATIONS_30004429_INDEPENDENT_AUDIT_SAFE.zip','independent_audit')]:
        with zipfile.ZipFile(ROOT/archive) as z:
            names=z.namelist();allowed={p.name for p in (ROOT/folder).iterdir()}
            require(len(names)==len(set(names)) and set(names)==allowed,'archive allowlist '+archive)
            for name in names: require(z.read(name)==(ROOT/folder/name).read_bytes(),'archive member '+name)
    for folder,name in [('author','MANIFEST.json'),('independent_audit','AUDIT_MANIFEST.json')]:
        m=json.loads((ROOT/folder/name).read_bytes())
        for p,meta in m['files'].items(): require(pin((ROOT/folder/p).read_bytes())==meta,'original manifest '+p)
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    with tempfile.TemporaryDirectory(prefix='schonmann-replay-') as d:
        output=Path(d)/'audit.json'
        run=subprocess.run([sys.executable,'-B',str(ROOT/'independent_audit/independent_verify.py'),'--author-dir',str(ROOT/'author'),'--archive',str(ROOT/'SPECIFICATIONS_30004429_AUTHOR_SAFE_FREEZE.zip'),'--output',str(output)],cwd=d,env=env,capture_output=True,text=True)
        require(run.returncode==0,'independent replay failed: '+run.stderr)
        require(output.read_bytes()==(ROOT/'independent_audit/INDEPENDENT_CHECK_RESULTS.json').read_bytes(),'exact independent and author replay')
    for name,meta in FROZEN.items(): require(pin((ROOT/name).read_bytes())==meta,'changed after replay '+name)
    return {'result':'PASS','problem_id':30004429,'status':'unsolved','turns':'5/5','packet_files':len(expected),'frozen_files_and_archives':len(FROZEN),'author_and_independent_replay':'PASS','author_ising_states':32768,'independent_mixture_cases':2541,'independent_ising_temperatures':3,'independent_memory_two_cases':336,'target_resolved':False,'novelty_claim':False}
if __name__=='__main__': print(json.dumps(verify(),indent=2))
