#!/usr/bin/env python3
"""Fail-closed, read-only publication binding and portable exact replays."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
FROZEN={'ERDOS_2235_AUTHOR_SAFE_FREEZE.zip': {'bytes': 15683, 'sha256': 'e5d6e7b26638daf7cedcc4e20456bb3bef3af3e5df3686ffa312164c3e072615'}, 'ERDOS_2235_INDEPENDENT_AUDIT.zip': {'bytes': 14636, 'sha256': '81b335030a4e3ea64edff6e9e8c27b364d9a519c556e5f276a57bc6139c1c122'}, 'author/MANIFEST.json': {'bytes': 1654, 'sha256': '8c709f826b2646098379f87aa3b1a56a54f1486fb1839a6283f7159a12c07b56'}, 'author/PROOF.md': {'bytes': 5338, 'sha256': '0ab3bfafb14f93f6ed6ef9237d63b8361f7719ce15a02d47d04ababac594c4fc'}, 'author/REPORT.md': {'bytes': 7562, 'sha256': '8c09d18e13bdbff82e58372d2544459334aeaeceb42b0542342008c4137e409e'}, 'author/RESEARCH_LOG.md': {'bytes': 1962, 'sha256': 'd8d6117e7c8d487f499ff0e28178ccca4644373d5d8583c75d62259d59763ef0'}, 'author/SOURCES.json': {'bytes': 4273, 'sha256': '99a487662255e726a30624bef572aacc65ae69e7936517247a127ca8dce50521'}, 'author/STATUS.json': {'bytes': 699, 'sha256': 'c189b2c96124fbbb03a2a852927cabb6ec72c9fd97bfe89a96119659e75c1372'}, 'author/VERIFICATION.json': {'bytes': 973, 'sha256': '3bd0f7cb828e433996817b94e59979de79e1fae205d5e965031e3333b6414c32'}, 'author/VERIFICATION_METADATA.json': {'bytes': 2556, 'sha256': '9aea6a7a56878c15400a08f8a5ec51a3d70e6bb5a4912268d608142fdddbe572'}, 'author/verify.py': {'bytes': 5423, 'sha256': '76c70f33a64d4ed7daa1f0a7edbcd94ef560a5d5e06f6de9e703934bd4b85d3e'}, 'author/verify_manifest.py': {'bytes': 1935, 'sha256': '3a277587eba8f3fb5345e09dcf06e500e993d0c950bb857d9ebf9d10bdcdf0c3'}, 'independent_audit/AUDIT.md': {'bytes': 10885, 'sha256': '382b471b980dd1336d380093611831bcbb8a40a922cecbd2a16964b582e9f38b'}, 'independent_audit/INDEPENDENT_VERIFICATION.json': {'bytes': 1776, 'sha256': 'c8e72293774a43c30fb63cdf958786ba51719c67923581a8c1f7bbd440f21c68'}, 'independent_audit/MANIFEST.json': {'bytes': 1486, 'sha256': '31b70ef7d85e70a9b8291a954be4f371036fb93234ea6537909311bc8b99373e'}, 'independent_audit/SOURCE_VERIFICATION.json': {'bytes': 4304, 'sha256': '7b2a2db32993c91e2bd54695df5d59dfc7365f675f413408aa62549114b7bc7a'}, 'independent_audit/VERDICT.json': {'bytes': 2105, 'sha256': '5b63fc031c2cf9a63ec4d30f6f16324e32fcc834633eda99b2eb5f08861b581d'}, 'independent_audit/independent_verify.py': {'bytes': 8988, 'sha256': 'dc229414ffa073cde5c78ac64fe353a66c60ac4c59707421bc714b79220896fe'}, 'independent_audit/verify_audit_manifest.py': {'bytes': 1433, 'sha256': '862502bae61665b13473fe2364ce6ae61dc0e9249a6cb4923397657369c89dab'}}
SCOPE={'schema': 'erdos-2235-qualified-publication-v1', 'id': '2235', 'code': 'EP-655', 'rank': 765, 'status': 'unsolved', 'turns_used': 1, 'turn_limit': 5, 'original_solution_credit': 0, 'disposition': 'Known literal-counterexample verification and qualified source correction only', 'literal_statement': {'hypothesis': 'A2: every positive-radius circle centered at a selected point contains at most two selected points on its circumference; n distinct planar points', 'truth_value': False, 'known_result': True, 'minimum_global_positive_distances': 'floor(n/2)', 'minimum_maximum_pinned_positive_distances': 'floor(n/2)', 'minimum_sum_pinned_positive_distances': 'n floor(n/2)', 'attainment': 'Regular n-gons for n>=3, with singleton and two-point boundary cases', 'novel_result': False}, 'historical_target': {'resolved_here': False, 'inspected_1988_formulation': 'A2 and no four concyclic points; maximum pinned distance count and a subsequent sum question', 'modern_general_position_global_variant_resolved_here': False, 'current_literature_status_certified': False}, 'audit_verdict': 'PASS strictly scoped to known literal-counterexample verification and source fidelity', 'freeze_policy': 'The author proposal already_solved applies to the literal statement only. Its pending-audit and no-remote-write fields describe the author freeze. This wrapper and the independent audit govern the conservative overall queue disposition; neither frozen packet was rewritten.', 'source_limits': ['Exact 1997 Er97e passage not retrieved or verified', 'Live tracker dynamic state not certified', 'FormalConjectures registry contains sorry; linked external Lean proof not built or certified', 'Prior-attempt searches bounded; no exhaustive-history claim'], 'publication_boundary': 'Authored proof, code, audit, public source metadata and verification metadata only. No source PDFs, source-text extracts, raw dataset contents, private sources or private coordination files.', 'human_peer_review': False, 'proof_assistant_certificate': False}
def require(ok,label):
    if not ok:raise RuntimeError('FAIL: '+label)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(path,flags=(),args=()):
    p=subprocess.run([sys.executable,'-B',*flags,str(path),*map(str,args)],cwd=ROOT,capture_output=True,timeout=240)
    require(p.returncode==0 and not p.stderr,'replay '+path.name)
    return p.stdout
def main():
    mp=ROOT/'PUBLICATION_MANIFEST.json'
    require(not mp.is_symlink(),'manifest symlink')
    manifest=json.loads(mp.read_bytes())
    require(manifest['schema']=='erdos-2235-publication-manifest-v1','manifest schema')
    expected=set(manifest['files'])|{'PUBLICATION_MANIFEST.json'}
    require(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in expected),'safe paths')
    dirs={str(p) for n in expected for p in Path(n).parents if str(p)!='.'}
    files=set(); actual_dirs=set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'symlink')
        n=p.relative_to(ROOT).as_posix()
        if p.is_file():files.add(n)
        elif p.is_dir():actual_dirs.add(n)
        else:require(False,'special file')
    require(files==expected,'file allowlist')
    require(actual_dirs==dirs,'directory allowlist')
    for n,h in manifest['files'].items():require(pin((ROOT/n).read_bytes())==h,'manifest hash '+n)
    for n,h in FROZEN.items():require(pin((ROOT/n).read_bytes())==h,'frozen pin '+n)
    require(json.loads((ROOT/'PUBLICATION.json').read_bytes())==SCOPE,'qualified scope')
    for folder,archive in [('author','ERDOS_2235_AUTHOR_SAFE_FREEZE.zip'),('independent_audit','ERDOS_2235_INDEPENDENT_AUDIT.zip')]:
        source=ROOT/folder
        with zipfile.ZipFile(ROOT/archive) as z:
            wanted={p.name for p in source.iterdir()}
            require(len(z.namelist())==len(wanted) and set(z.namelist())==wanted,'archive membership')
            require(z.testzip() is None,'archive CRC')
            for p in source.iterdir():require(z.read(p.name)==p.read_bytes(),'archive equality')
    author=ROOT/'author';audit=ROOT/'independent_audit'
    run(author/'verify_manifest.py')
    run(audit/'verify_audit_manifest.py',args=('--expected-manifest-sha256','31b70ef7d85e70a9b8291a954be4f371036fb93234ea6537909311bc8b99373e'))
    for flags in [(),('-O',)]:
        av=run(author/'verify.py',flags)
        require(av==(author/'VERIFICATION.json').read_bytes(),'author replay equality')
        iv=run(audit/'independent_verify.py',flags,('--author-dir',author,'--archive',ROOT/'ERDOS_2235_AUTHOR_SAFE_FREEZE.zip'))
        require(iv==(audit/'INDEPENDENT_VERIFICATION.json').read_bytes(),'independent replay equality')
    require(json.loads(av)['total_checks']==711511,'author total')
    require(json.loads(iv)['total_checks']==711870,'independent total')
    print(json.dumps({'result':'PASS','id':'2235','status':'unsolved','turns':'1/5','original_solution_credit':0,'packet_files':len(files),'frozen_files_and_archives':len(FROZEN),'author_checks_per_replay':711511,'independent_checks_per_replay':711870,'normal_and_optimized_replays':'byte-identical','historical_target_resolved_here':False,'novelty_claim':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
