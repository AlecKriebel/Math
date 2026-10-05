#!/usr/bin/env python3
"""Read-only fail-closed publication integrity and exact replay controls."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
FROZEN={'CI_LIMITS_20000814_INDEPENDENT_AUDIT.zip': {'bytes': 19685, 'sha256': '2f49b6e54713d761ce198b18cd42b2fc3746c80d6e34cec01b159a34a7ff7074'}, 'CI_LIMITS_20000814_SAFE_FREEZE.zip': {'bytes': 22081, 'sha256': 'bd7848a35c7c0e676f8b161f98184b36a39ec251db534c9530646e55966bb420'}, 'author/AUTHOR_REPLAY.json': {'bytes': 332, 'sha256': 'acc3202d9aa780f1e812ff52efc262b7b54cc0575dd4294248c67aee160434a5'}, 'author/MANIFEST.json': {'bytes': 1386, 'sha256': '23aa3cc77bd3e78439a2fd09867382acbfe2a3e5517057b7111870270a48641c'}, 'author/PROOFS.md': {'bytes': 17121, 'sha256': '45225482ea9c82da9ea21cc6ed075c18ec62513337b1940bb07d15d5ef459028'}, 'author/README.md': {'bytes': 1193, 'sha256': 'd098aba1e3dc205a05fbcb8c85b1f9157aeddb46bca211cacc27cb29a795d8a3'}, 'author/REPORT.md': {'bytes': 14050, 'sha256': '6a6146a1daa421b22d5f76bdcf32b3460d7eb279a76c47412e5ce8d595c8a52e'}, 'author/SOURCE_METADATA.json': {'bytes': 8803, 'sha256': '55ea36e42d7f6ed8b4e4cbbbb8888d0e92b7b1965f8c1de72253b92ff87fc674'}, 'author/verification_results.json': {'bytes': 677, 'sha256': '009003c1c60ed490cadb9aadc19b36c2c45b938bc01cfc44460a0d712a4a2ff2'}, 'author/verify_controls.py': {'bytes': 5172, 'sha256': '3ea9acb8b78bfa81aa6060c217a7710c5161cac151296b8a873961c62b2413c3'}, 'independent_audit/AUDIT.md': {'bytes': 16297, 'sha256': 'd1f852c7e912c807df2912e7c96dffcf10c94c194ff1d3a3baf0efca5cbad6f5'}, 'independent_audit/MANIFEST.json': {'bytes': 1343, 'sha256': '361c9c5f798fae7e3c365747a6d45142a2f0367d902c85d59f070e22b37907e5'}, 'independent_audit/README.md': {'bytes': 1931, 'sha256': 'f43e420a23b4a616276041fd2d155134465ba50dc0a7fc7193b5b8cf4064c5af'}, 'independent_audit/REPLAY_AND_NEGATIVE_CONTROLS.json': {'bytes': 761, 'sha256': 'd0bcb228f32e11c408d68e31fd9f4032e127e14b2cb4ef603a2d66e4b946e481'}, 'independent_audit/SOURCE_AUDIT.json': {'bytes': 6888, 'sha256': 'b24269a26926842a6d998945ea1d5822625517b2d29a98d4df33a10e38f300da'}, 'independent_audit/VERDICT.json': {'bytes': 1116, 'sha256': 'b17a2a7e36e15cde05b5c625b1ded8748dfda75a3f114f1879e0ecb9af97f527'}, 'independent_audit/verification_results.json': {'bytes': 2117, 'sha256': 'cd2effc63ed09df6fc2ed65a66320bcd893cc1604bb8b737eafbf1bd7115a8bf'}, 'independent_audit/verify_independent.py': {'bytes': 13336, 'sha256': 'c79283bbab763f84693761c7182c34b3e37fcc6242d0c9f861211eac676ee495'}}
SCOPE={'problem_id': 20000814, 'problem_number': 'AIM-ARITHMETIC_GEOMETRY-0060', 'rank': 759, 'status': 'unsolved', 'turns': '5/5', 'disposition': 'partial_progress', 'general_AIM_Problem_13_solved': False, 'novelty_claim': False, 'audit_verdict': 'PASS at the stated partial-progress scope', 'mandatory_corrections': [], 'affirmative_cases': ['1 <= a <= 3, b >= a', '(a,b)=(4,4)'], 'remaining_obstruction': '3 <= c < a; nonreduced lci auxiliary curve of degree (a-c)(b-c)>1; fixed-factor equations through degree b; an actual embedded smoothing to CI(a,b) still required', 'precision': ['The Serre bundle is an absolute construction on the special P3, not a relative bundle family or a specialization-of-splitting claim.', 'The degree-one exclusion uses purity supplied by the lci zero-section construction.'], 'EH_1999_full_chapter_inspected': False, 'source_limits': 'No exhaustive current-literature or priority certification. Scholarly-source inspection scopes remain those in the frozen packets.', 'publication_boundary': 'Authored proof, code, audit and public verification metadata only; no source PDFs, source-text extracts, raw dataset, selected dataset record, private sources, or private coordination files.'}
def require(test,label):
    if not test:raise RuntimeError('FAIL: '+label)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(path,*args):
    p=subprocess.run([sys.executable,str(path),*map(str,args)],cwd=ROOT,capture_output=True,timeout=180)
    require(p.returncode==0 and not p.stderr,'replay execution '+path.name)
    return p.stdout
def main():
    require(not (ROOT/'PUBLICATION_MANIFEST.json').is_symlink(),'manifest symlink')
    manifest=json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_bytes())
    expected=set(manifest['files'])|{'PUBLICATION_MANIFEST.json'}
    require(all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in expected),'safe paths')
    dirs={str(p) for n in expected for p in Path(n).parents if str(p)!='.'}
    actual_files=set();actual_dirs=set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'symlink')
        rel=p.relative_to(ROOT).as_posix()
        if p.is_file():actual_files.add(rel)
        elif p.is_dir():actual_dirs.add(rel)
        else:require(False,'special file')
    require(actual_files==expected,'file allowlist')
    require(actual_dirs==dirs,'directory allowlist')
    for n,h in manifest['files'].items():require(pin((ROOT/n).read_bytes())==h,'manifest hash '+n)
    for n,h in FROZEN.items():require(pin((ROOT/n).read_bytes())==h,'frozen pin '+n)
    require(json.loads((ROOT/'PUBLICATION.json').read_bytes())==SCOPE,'scope boundary')
    for folder,archive,prefix in [('author','CI_LIMITS_20000814_SAFE_FREEZE.zip','ci_limits_20000814'),('independent_audit','CI_LIMITS_20000814_INDEPENDENT_AUDIT.zip','ci_limits_20000814_independent_audit')]:
        source=ROOT/folder
        m=json.loads((source/'MANIFEST.json').read_bytes())
        require({x['path'] for x in m['files']}|{'MANIFEST.json'}=={p.name for p in source.iterdir()},'frozen manifest inventory')
        for x in m['files']:require(pin((source/x['path']).read_bytes())=={k:x[k] for k in ['bytes','sha256']},'frozen manifest entry')
        with zipfile.ZipFile(ROOT/archive) as z:
            wanted={prefix+'/'+p.name for p in source.iterdir()}
            require(len(z.namelist())==len(wanted) and set(z.namelist())==wanted,'archive membership')
            require(z.testzip() is None,'archive CRC')
            for p in source.iterdir():require(z.read(prefix+'/'+p.name)==p.read_bytes(),'archive file equality')
    author=ROOT/'author';audit=ROOT/'independent_audit'
    a=run(author/'verify_controls.py');require(a==(author/'verification_results.json').read_bytes(),'author exact replay')
    b=run(audit/'verify_independent.py','--author-dir',author,'--archive',ROOT/'CI_LIMITS_20000814_SAFE_FREEZE.zip')
    require(b==(ROOT/'PORTABLE_AUDIT_RESULTS.json').read_bytes(),'portable audit exact replay')
    ar=json.loads(a);br=json.loads(b)
    require(br['optional_source_checks']=={},'portable source scope')
    print(json.dumps({'result':'PASS','problem_id':20000814,'status':'unsolved','turns':'5/5','packet_files':len(expected),'frozen_files_and_archives':len(FROZEN),'author_checks':ar['checks'],'independent_portable_checks':br['checks'],'general_problem_solved':False,'novelty_claim':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
