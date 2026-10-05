#!/usr/bin/env python3
"""Read-only, fail-closed publication integrity and exact scientific replay."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
FROZEN={'MONOMIAL_SIGNATURES_20000817_AUTHOR_SAFE_FREEZE.zip': {'bytes': 21964, 'sha256': 'ff634df72962777e7fd39797542604251c8c1b4d8c6ccedf52b2dc5696c78592'}, 'MONOMIAL_SIGNATURES_20000817_INDEPENDENT_AUDIT_SAFE_FREEZE.zip': {'bytes': 21604, 'sha256': 'e23b32d29c5f334b0f9c4259d47680e8d5fd4f18ed66ec0699ba32101e9651f2'}, 'author/AUTHOR_REPLAY.json': {'bytes': 122, 'sha256': '4cd35933806001e1f5d0b58ea3f07afbe7cb6c6947d3be5d860f450d856f0710'}, 'author/MANIFEST.json': {'bytes': 1335, 'sha256': '2b8f5c3d571d3c3f6a59849f4b03788115fe12d1be56943c9ad52a89d7d83d1a'}, 'author/PROOFS.md': {'bytes': 15011, 'sha256': 'd7d3bc8fbff546fafec519771a54514779c58f1ae3a7e7f61713730ff3056a84'}, 'author/README.md': {'bytes': 2740, 'sha256': '4264f62f026adc3338e18584b0161057a02ce58adcfc0b44ce33f5c399d64e1b'}, 'author/RESEARCH_REPORT.md': {'bytes': 8578, 'sha256': '9540cee6752e001144d9f86446ac3bad4bb2ab27be2cfe1dcf94ed43f1341e58'}, 'author/code/verify_signatures.py': {'bytes': 6472, 'sha256': '8ecd8fbfcaa586c901301e0c2a06b3edf22525a2197268be369ba9e0aae75387'}, 'author/provenance.json': {'bytes': 2794, 'sha256': '8b255527f9fb9c1c652c5b6b53b70a8f0a96056430e6890771fcc8be89c94eaa'}, 'author/results/verification.json': {'bytes': 3128, 'sha256': 'e46c8987ab0028cf7de65ec0b90e017ad13d3801e76d52edf5d2dae54ac92f0a'}, 'author/sources.json': {'bytes': 8149, 'sha256': '64609398cc270ca74fe91299ef8fc16ad740cc1cf5499c4a8852ba9ec2494346'}, 'author/verify_packet.py': {'bytes': 850, 'sha256': '2cf0f2f26f6f36bbd0dde49ed62ffc86d66e95807c79bc87d693f4f022d7a234'}, 'independent_audit/AUDIT_REPLAY.json': {'bytes': 254, 'sha256': 'f06d7eaefcede1d2ac0a7ae98fe08ba4f86829e235c31db0ecb2f060c3a597f4'}, 'independent_audit/AUDIT_REPORT.md': {'bytes': 14388, 'sha256': '5b2256b51d03a5637b081b67c58a69c8513b38662c5fd24a3e2d7a9d82ac033d'}, 'independent_audit/MANIFEST.json': {'bytes': 1371, 'sha256': '181c36b045ba0917ca28d0ec6a23c60274a503931727fd74b6b51dae436b1e6b'}, 'independent_audit/README.md': {'bytes': 1620, 'sha256': 'ccc8db156724e94ba8a1303ffa1b874e4e59c3cd452364cc13b44f6eac739af6'}, 'independent_audit/code/independent_controls.py': {'bytes': 9017, 'sha256': 'c743686ab7fcb65f934c39ef4b023df8df5a2b34de738179ea36b4d3f164c5b0'}, 'independent_audit/results/independent_controls.json': {'bytes': 3690, 'sha256': 'b2717bff58b36875a7d9b50273f845ad9bfe0743e7c6c03df448a4a8aacfd76d'}, 'independent_audit/results/input_integrity.json': {'bytes': 7455, 'sha256': 'c3e8655bbaf3af40f2a2046caf0e9f294c414edc726493c0508b1d31d47c669f'}, 'independent_audit/source_audit.json': {'bytes': 7025, 'sha256': '65599c4192e0c271004d52e4f6d6b41505f028d80ef2ea39a3a8c0fdeba0d22e'}, 'independent_audit/verdict.json': {'bytes': 2865, 'sha256': 'bfe6dfd1a8170fe6d6dea7f673f38ce78e9252a8a0a52d19d73bcd52bded4a2d'}, 'independent_audit/verify_audit.py': {'bytes': 3100, 'sha256': 'e221b33598f29d73b09bd5580bdaa08bc521103e5cfd431165c30bec8cfee830'}}
SCOPE={'problem_id': 20000817, 'problem_code': 'AIM-ARITHMETIC_GEOMETRY-0063', 'rank': 760, 'status': 'unsolved', 'turns': '5/5', 'general_problem_solved': False, 'novelty_claim': False, 'audit_verdict': 'PASS scoped to rigorous partial progress; no mandatory corrections', 'audit_is_peer_review': False, 'target': 'Injectivity of the full monomial-point signature of irreducible components of ordinary affine and projective Hilbert schemes', 'length_eight_classification_characteristic': 'not 2 or 3', 'projective_boundary': 'Actual at most two Borel-fixed closed points over an algebraically closed field, in every characteristic', 'characteristic_two_case_ii': 'Excluded because it no longer has exactly two Borel-fixed points; not a gap in Staal classification', 'full_signature_equals_double_generic_invariant': False, 'smoothness_required_for_anchor': 'Ambient Hilbert-scheme smoothness; component smoothness alone does not suffice', 'projective_separator_characteristic': 'zero', 'retained_results': ['Universal affine monomial smoothability and nonsmoothable-pair reduction', 'Exact length-eight nonsmoothable-component signature including boundary Hilbert functions', 'At-most-two actual Borel-fixed-point projective result in all characteristics', 'Explicit saturated monomial separator for the published equal-double-generic pair'], 'finite_controls_are_general_proof': False, 'publication_boundary': 'Authored proofs, code, audit and public verification metadata only; excludes source documents, extracts, raw datasets and private coordination'}
WRAPPERS={'README.md','PUBLICATION.json','RESEARCH_LOG.md','verify_publication.py','PUBLICATION_MANIFEST.json'}
def require(ok,message):
    if not ok: raise AssertionError(message)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def replay(script,*args):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    with tempfile.TemporaryDirectory(prefix='monomial-replay-') as d:
        r=subprocess.run([sys.executable,'-B',str(ROOT/script),*map(str,args)],cwd=d,env=env,capture_output=True,text=True)
    require(r.returncode==0,'replay '+script+': '+r.stderr)
    return json.loads(r.stdout)
def verify():
    expected=set(FROZEN)|WRAPPERS
    expect_dirs={str(p) for name in expected for p in Path(name).parents if str(p)!='.'}
    files=set();dirs=set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'symlink: '+str(p))
        rel=p.relative_to(ROOT).as_posix()
        if p.is_file():files.add(rel)
        elif p.is_dir():dirs.add(rel)
        else:require(False,'special file')
    require(files==expected,'file allowlist');require(dirs==expect_dirs,'directory allowlist')
    manifest=json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_bytes())
    require(set(manifest['files'])==expected-{'PUBLICATION_MANIFEST.json'},'manifest allowlist')
    for name,meta in manifest['files'].items():require(pin((ROOT/name).read_bytes())==meta,'manifest '+name)
    for name,meta in FROZEN.items():require(pin((ROOT/name).read_bytes())==meta,'frozen '+name)
    require(json.loads((ROOT/'PUBLICATION.json').read_bytes())==SCOPE,'scope boundary')
    for archive,folder,prefix in [('MONOMIAL_SIGNATURES_20000817_AUTHOR_SAFE_FREEZE.zip','author','monomial_signatures_20000817/'),('MONOMIAL_SIGNATURES_20000817_INDEPENDENT_AUDIT_SAFE_FREEZE.zip','independent_audit','monomial_signatures_20000817_independent_audit/')]:
        with zipfile.ZipFile(ROOT/archive) as z:
            names=z.namelist();allowed={prefix+p.relative_to(ROOT/folder).as_posix() for p in (ROOT/folder).rglob('*') if p.is_file()}
            require(len(names)==len(set(names)) and set(names)==allowed,'archive allowlist '+archive)
            for name in names:require(z.read(name)==(ROOT/folder/name[len(prefix):]).read_bytes(),'archive member '+name)
    for folder in ['author','independent_audit']:
        m=json.loads((ROOT/folder/'MANIFEST.json').read_bytes())
        for row in m['files']:require(pin((ROOT/folder/row['path']).read_bytes())=={'bytes':row['bytes'],'sha256':row['sha256']},'original manifest '+row['path'])
    author=replay('author/verify_packet.py')
    audit=replay('independent_audit/verify_audit.py','--author-dir',ROOT/'author','--author-zip',ROOT/'MONOMIAL_SIGNATURES_20000817_AUTHOR_SAFE_FREEZE.zip')
    require(author['status']=='PASS' and audit['status']=='PASS','scientific replay status')
    require(author['general_problem_solved'] is False and audit['general_problem_solved'] is False,'scientific scope')
    for name,meta in FROZEN.items():require(pin((ROOT/name).read_bytes())==meta,'changed after replay '+name)
    return {'result':'PASS','problem_id':20000817,'status':'unsolved','turns':'5/5','packet_files':len(expected),'frozen_files_and_archives':len(FROZEN),'author_replay':author,'independent_replay':audit,'general_problem_solved':False,'novelty_claim':False,'source_acquisition_repeated':False}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
