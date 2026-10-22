#!/usr/bin/env python3
"""Portable, read-only, fail-closed publication checks. No external inputs."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
FROZEN={'author/MANIFEST.json': {'bytes': 1726, 'sha256': '9f7f9d00e8a41afa503bbb6fbd275e402d19d69da6ed44d4303af36c75b904ef'}, 'author/PROOFS.md': {'bytes': 12483, 'sha256': '3ab85452dc65f7a49cb43eb747b9ecae56c79db1c461733c4e80012c492192ca'}, 'author/README.md': {'bytes': 1642, 'sha256': '7285a5525f24685ea9016d7cb648202d35e1c533d921f1311d1c28bee3f428fc'}, 'author/REPORT.md': {'bytes': 12128, 'sha256': 'de903f00f50189f85bd44b3fb06a41be6081ad405da665c9663ee0b852941a90'}, 'author/SEARCH_LOG.md': {'bytes': 3693, 'sha256': '785774fee4568a4f1adc1408d626f42d0fb3a8fa9ec13398c758a02ce5bb4148'}, 'author/claims.json': {'bytes': 1670, 'sha256': '1fdecc2c0153a43fd2d84cfc17f73cfb744261348d3642b8993f482ecd7a78d0'}, 'author/dataset_verification.json': {'bytes': 1769, 'sha256': '84155060e8894eca21c8f0b148999555bf4e22d097e06b9a92c2b94893d74207'}, 'author/source_metadata.json': {'bytes': 7150, 'sha256': '71ce2b6d5f24db0465dd33f88001f16f35f1a870e70ba0fcd9a93ad1c2ecc364'}, 'author/verification_results.json': {'bytes': 8763, 'sha256': '7aca1833799d6fe51d2fa2e4ea571007e566745bd9e316044398ca7c97fefc1a'}, 'author/verify.py': {'bytes': 10768, 'sha256': '2941448092f69b24a1e0c151a85a0275f4e8b1dedc0c484411fa60593205e72a'}, 'independent_audit/AUDIT_REPORT.md': {'bytes': 14834, 'sha256': '160b6aa769083978c76f14973e153b44e4ff69837b96dffe966a0725d0a267f1'}, 'independent_audit/MANIFEST.json': {'bytes': 2254, 'sha256': '92c9f9ef82c1a95db66336a4829f9d4f868f854364552871b8ab87479fb9a4f5'}, 'independent_audit/README.md': {'bytes': 1533, 'sha256': '3c1801aa502242b9e7d1a596dec8ea859337e106a168848f120cef66e8d68d8e'}, 'independent_audit/audit_summary.json': {'bytes': 1492, 'sha256': '47643193ede0496e81cb3b1847f8608800ac91b4019f8647470025ff995b7650'}, 'independent_audit/author_replay_results.json': {'bytes': 8763, 'sha256': '7aca1833799d6fe51d2fa2e4ea571007e566745bd9e316044398ca7c97fefc1a'}, 'independent_audit/dataset_integrity.json': {'bytes': 1223, 'sha256': 'eb947900e8b84194c7650e149f49106338000045122bbf8636f914c582e63f44'}, 'independent_audit/independent_results.json': {'bytes': 5066, 'sha256': 'bff3eb879237ab4008047c9d67c08568d04495b7b00357490a4f00f2d38bbaa6'}, 'independent_audit/independent_verify.py': {'bytes': 14401, 'sha256': 'b34f275ad738425617156e12f4acb0add567a22bfd0b5f024454ba13df923af3'}, 'independent_audit/input_integrity.json': {'bytes': 1811, 'sha256': 'b30a0b75b2ee1aac1cb4545c55c4536e3ea5f6e9b0bfad08cc112480839505ba'}, 'independent_audit/negative_control_results.json': {'bytes': 807, 'sha256': '8554ca095834d2c56d5b3243241b1112d7f074afd4d6cab0dbfc6a5d14ea5563'}, 'independent_audit/negative_controls.py': {'bytes': 2251, 'sha256': '5fd2d62a6bb6e7e86271f47796c492bdadeaf807f58e0a3a9130d065677c2e88'}, 'independent_audit/source_checks.json': {'bytes': 4419, 'sha256': '29c3281bb11106395baa5df6f2828b0124ff11b9ca1a6631309469bcbaacafa4'}, 'independent_audit/source_integrity.json': {'bytes': 1805, 'sha256': 'c5519d000f7ba26ac3d756be13b0724cf3bb48e9c4c1c008160083b238996cf0'}, 'CONNECTED_20000826_AUTHOR_SAFE_FREEZE.zip': {'bytes': 24231, 'sha256': '3ac3fb42d81b47b6982d529d43882ee6721af7dadfd52b5137e19dd3f2a3ff25'}, 'CONNECTED_20000826_INDEPENDENT_AUDIT_PASS.zip': {'bytes': 22734, 'sha256': '5e1be0cec8aa80149894b366c8cc95a6735642a7ab2ad55e228b1486d3add516'}}
SCOPE={'problem_id': 20000826, 'problem_number': 'AIM-ARITHMETIC_GEOMETRY-0072', 'rank': 761, 'status': 'unsolved', 'turns': '5/5', 'disposition': 'scoped partial results and literature update', 'general_three_variable_question_resolved': False, 'novelty_claim': False, 'audit_verdict': 'PASS strictly scoped to the stated partial results and literature update', 'mandatory_mathematical_corrections': [], 'weighted_classification': 'Positive integer coarsening, h(0)=1, all other supported degrees of weight 1 or 2, explicit vanishing in unattained degrees and admissible quotient ranks; smooth and geometrically irreducible if nonempty.', 'theorem_1_clarification': 'Vanishing in degrees not attained by monomials is an explicit additional nonemptiness condition. It is not a consequence of support in weights zero through two. The frozen In particular wording is read subject to this condition.', 'cubic_classification': 'Standard grading, h=(1,r,s,1), zero in degrees at least four, 1<=r<=n, 1<=s<=r(r+1)/2; geometric connectedness in every characteristic, without smoothness or irreducibility claims.', 'five_variable_update': 'Cid-Ruiz arXiv:2608.07704v1 is treated as a preprint; five-variable disconnectedness is not a three-variable answer, a toric-function result, or a minimum-variable theorem.', 'polynomial_to_function_transfer': 'Uses a uniform sufficiently positive upper orthant and extension of truncated ideals by zero outside it, not equality of the original saturated ideals full Hilbert functions.', 'scope_limits': ['The classical standard-graded result cannot be transferred to arbitrary finer gradings.', 'The contraction proof uses the dual of multiplication, not ordinary polynomial differentiation.', 'The known two-component comparison retains its characteristic exclusions.', 'Functorial arguments retain nonreduced-base conditions; finite counts do not replace them.', 'Nonpositive gradings and arbitrary admissible three-variable Hilbert functions remain unresolved.', 'The positive finite-support reduction supplies no universal weight-two or weight-three cutoff.', 'No exhaustive current-literature or novelty certification is claimed.'], 'historical_freeze_labels': 'Author pending-audit labels and audit no-remote-writes labels describe their preserved checkpoints. This wrapper records the subsequently accepted scoped audit and publication.', 'publication_boundary': 'Authored proof, analysis, code, audit and public verification metadata only. No source PDFs or extracts, raw dataset or selected records, private sources, private personal data, or private coordination files.'}
def require(ok,label):
    if not ok: raise RuntimeError('FAIL: '+label)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(path,*args,optimized=False):
    cmd=[sys.executable]+(['-O'] if optimized else [])+[str(path)]+list(map(str,args))
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    with tempfile.TemporaryDirectory(prefix='connected-publication-replay-') as tmp:
        result=subprocess.run(cmd,cwd=tmp,env=env,capture_output=True,timeout=240)
    require(result.returncode==0 and not result.stderr,'successful replay '+path.name)
    return result.stdout
def main():
    require(not (ROOT/'PUBLICATION_MANIFEST.json').is_symlink(),'manifest symlink')
    manifest=json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_bytes())
    expected=set(manifest['files'])|{'PUBLICATION_MANIFEST.json'}
    require(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in expected),'safe paths')
    dirs={str(p) for n in expected for p in Path(n).parents if str(p)!='.'}
    actual_files=set();actual_dirs=set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'symlink')
        rel=p.relative_to(ROOT).as_posix()
        if p.is_file():actual_files.add(rel)
        elif p.is_dir():actual_dirs.add(rel)
        else:require(False,'special file')
    require(actual_files==expected,'closed file allowlist')
    require(actual_dirs==dirs,'closed directory allowlist')
    for n,h in manifest['files'].items():require(pin((ROOT/n).read_bytes())==h,'manifest hash '+n)
    for n,h in FROZEN.items():require(pin((ROOT/n).read_bytes())==h,'frozen pin '+n)
    require(json.loads((ROOT/'PUBLICATION.json').read_bytes())==SCOPE,'scope boundary')
    for folder,archive,prefix in [('author','CONNECTED_20000826_AUTHOR_SAFE_FREEZE.zip','connected_20000826'),('independent_audit','CONNECTED_20000826_INDEPENDENT_AUDIT_PASS.zip','connected_20000826_independent_audit')]:
        source=ROOT/folder;m=json.loads((source/'MANIFEST.json').read_bytes())
        require({x['path'] for x in m['files']}|{'MANIFEST.json'}=={p.name for p in source.iterdir()},'frozen manifest inventory')
        for x in m['files']:require(pin((source/x['path']).read_bytes())=={k:x[k] for k in ['bytes','sha256']},'frozen manifest entry')
        with zipfile.ZipFile(ROOT/archive) as z:
            wanted={prefix+'/'+p.name for p in source.iterdir()}
            require(len(z.namelist())==len(wanted) and set(z.namelist())==wanted,'ZIP membership')
            require(z.testzip() is None,'ZIP CRC')
            for p in source.iterdir():require(z.read(prefix+'/'+p.name)==p.read_bytes(),'ZIP directory equality')
    author=ROOT/'author';audit=ROOT/'independent_audit'
    a=run(author/'verify.py')
    require(a==(author/'verification_results.json').read_bytes()==(audit/'author_replay_results.json').read_bytes(),'author exact replay')
    b=run(audit/'independent_verify.py');c=run(audit/'independent_verify.py',optimized=True)
    require(b==c==(audit/'independent_results.json').read_bytes(),'independent ordinary and optimized exact replay')
    d=run(audit/'negative_controls.py','--author-dir',author)
    require(d==(audit/'negative_control_results.json').read_bytes(),'five mathematical negative controls exact replay')
    out={'result':'PASS','problem_id':20000826,'status':'unsolved','turns':'5/5','packet_files':len(expected),'frozen_files_and_archives':len(FROZEN),'author_replay':'byte-identical','independent_replay':'ordinary and optimized byte-identical','mathematical_negative_mutations_rejected':5,'general_three_variable_question_resolved':False,'novelty_claim':False}
    encoded=json.dumps(out,indent=2,sort_keys=True)+'\n'
    require(encoded.encode()==(ROOT/'VERIFICATION_RESULTS.json').read_bytes(),'publication expected result')
    print(encoded,end='')
if __name__=='__main__':main()
