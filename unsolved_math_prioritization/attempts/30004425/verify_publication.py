#!/usr/bin/env python3
"""Read-only fail-closed delivery and exact replay verification."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
FROZEN={'TROPICAL_WALL_30004425_DELTA_ACCEPTANCE.zip': {'bytes': 8902, 'sha256': '94535a5b74397cc2dd1534adc4dde73a86e4172c389df759bd23b9cdb7eb3da6'}, 'TROPICAL_WALL_30004425_INDEPENDENT_AUDIT.zip': {'bytes': 17343, 'sha256': '8dc1a38f8d761c976162321ad7b707780cc552b61aabb6fe681580d398611ccd'}, 'author/TROPICAL_WALL_30004425_AUTHOR_SAFE_FREEZE.zip': {'bytes': 17849, 'sha256': '8297f9480c92cf9a736468cfeefc008b62a04b7e4674c8851b9e72fb6c99a446'}, 'author/TROPICAL_WALL_30004425_CORRECTED_SAFE_FREEZE.zip': {'bytes': 25136, 'sha256': 'a53534d916ae974461131d47fab6589d80bfc1799ecffad4c6b3f56691d303c8'}, 'author/corrected_safe_freeze/CORRECTIONS.diff': {'bytes': 9236, 'sha256': 'ae6cd7dd45c4192d050fb123d7de6c81f881504557bfaf854fe5c88f9cdd2407'}, 'author/corrected_safe_freeze/CORRECTION_RESULTS.json': {'bytes': 1247, 'sha256': 'd1210cbf315c7115eb2ebf8620fa096c3a11417e3b4487a10485f59b91dbeab1'}, 'author/corrected_safe_freeze/EXACT_CONTROLS.md': {'bytes': 9043, 'sha256': 'a540bafaa17dc137a5d8d0ab430ae7a787fa4f99e6483d8f616d1836b98b91a2'}, 'author/corrected_safe_freeze/MANIFEST.json': {'bytes': 1500, 'sha256': 'bd3994c0ff3a51c3695135291206af0e50455c461a482f1738b0939fe3eb5a82'}, 'author/corrected_safe_freeze/PUBLICATION_SCOPE.md': {'bytes': 3288, 'sha256': '43e8e239cda32ecd0a01bd97419ddae3226b2dc31774db5303f02e206efd2f0d'}, 'author/corrected_safe_freeze/README.md': {'bytes': 675, 'sha256': '83b2d4147191aae4b0d7f9d9f0a21d8762cccc4c0f8caa1e8001e973f3a39e14'}, 'author/corrected_safe_freeze/REPORT.md': {'bytes': 11160, 'sha256': '999042ad21b35edc34db9339a1f4c2345d81631e5f2358223322c4691d548f24'}, 'author/corrected_safe_freeze/SOURCE_VERIFICATION.json': {'bytes': 10216, 'sha256': 'cbc0a113dc81fabaaa36b110a81a51ea64c994c4a2c6595a69abde5d4d6ecb81'}, 'author/corrected_safe_freeze/VERIFICATION_RESULTS.json': {'bytes': 2685, 'sha256': 'ef54c8f482283efaf38cd265c95173f841b5be92d4082025a73d256752a9c082'}, 'author/corrected_safe_freeze/verify.py': {'bytes': 4060, 'sha256': 'c54670cee3952604158f727db607d333247ebaa0a3e6aa95ac2f2b2e1d5b7167'}, 'author/corrected_safe_freeze/verify_manifest.py': {'bytes': 630, 'sha256': 'beff29213501182a42e5f9bc9248a705e1a14caf2cb4ce878bbe270fad571652'}, 'author/safe_freeze/EXACT_CONTROLS.md': {'bytes': 9043, 'sha256': 'a540bafaa17dc137a5d8d0ab430ae7a787fa4f99e6483d8f616d1836b98b91a2'}, 'author/safe_freeze/MANIFEST.json': {'bytes': 1037, 'sha256': '6e7525badc24111de1237f851ebe236d4f057adedce16e8d12d1808011f1aca3'}, 'author/safe_freeze/README.md': {'bytes': 675, 'sha256': '83b2d4147191aae4b0d7f9d9f0a21d8762cccc4c0f8caa1e8001e973f3a39e14'}, 'author/safe_freeze/REPORT.md': {'bytes': 11148, 'sha256': 'c1135354fd55749026c708506f2cc47d52a4ccb7bfe12641ac7c437d3a8f191f'}, 'author/safe_freeze/SOURCE_VERIFICATION.json': {'bytes': 8921, 'sha256': 'b0f2132794ed152293353a84bcbc4d2b3e6a12294880267e18395e1ed2702619'}, 'author/safe_freeze/VERIFICATION_RESULTS.json': {'bytes': 2685, 'sha256': 'ef54c8f482283efaf38cd265c95173f841b5be92d4082025a73d256752a9c082'}, 'author/safe_freeze/verify.py': {'bytes': 4060, 'sha256': 'c54670cee3952604158f727db607d333247ebaa0a3e6aa95ac2f2b2e1d5b7167'}, 'author/safe_freeze/verify_manifest.py': {'bytes': 630, 'sha256': 'beff29213501182a42e5f9bc9248a705e1a14caf2cb4ce878bbe270fad571652'}, 'delta_audit/DELTA_ACCEPTANCE.md': {'bytes': 6124, 'sha256': '316442a7e55ee92f7f5bd143603017993f6bedd73b4508e73bf4c6c832cbab3c'}, 'delta_audit/DELTA_RESULTS.json': {'bytes': 3702, 'sha256': '1a0d7e173dd90092471449d52830c951a6843f7faae3539c22cb3ba96e121c92'}, 'delta_audit/MANIFEST.json': {'bytes': 660, 'sha256': '7cbb232a5f069146ac49163839d8ae2713ca2c9e46c6033af3e6da9c1b41d5d0'}, 'delta_audit/verify_delta.py': {'bytes': 7227, 'sha256': '9ba81ad20620ae16453720436ef255b81dd6542c52e8610b2164e0aaa3676213'}, 'delta_audit/verify_manifest.py': {'bytes': 717, 'sha256': '93ad1118f5c3ef4dddff203a7b66ad51ef7f022d003178e91bf34f8c339b8bce'}, 'independent_audit/AUDIT.md': {'bytes': 15361, 'sha256': 'ebc2b4ab999c7e4dbffee312c27e862861cedae994a28f32b86e104ea5f36b86'}, 'independent_audit/INDEPENDENT_RESULTS.json': {'bytes': 2044, 'sha256': '5399baa7bbdc3ce78405dab67a15fab9f1a3781f79a2c186a91064bb7b16554f'}, 'independent_audit/MANIFEST.json': {'bytes': 1135, 'sha256': 'a52431e654bd7354f89867de09c823a3b0010768cb9ad1c3a4a35f253097e413'}, 'independent_audit/MUTATION_RESULTS.json': {'bytes': 715, 'sha256': 'b49fc3bb911c25e48aac77dffc29ba43f810d2b03c34eb485c2428e0358645ba'}, 'independent_audit/SOURCE_RECHECK.json': {'bytes': 5547, 'sha256': '3816162c8b85d6b91752a2b457db821692a96b3d410b381dc8a01d254fc13628'}, 'independent_audit/independent_verify.py': {'bytes': 8840, 'sha256': '129f948e958c17a2705d900d070364b66244e942c5dd912e906b3d23de55e946'}, 'independent_audit/mutation_verify.py': {'bytes': 1641, 'sha256': 'f7b47e140b4a3c28c249307028f94f1e445fd80321751a26e22ca1fabd6b5d9b'}, 'independent_audit/verify_audit_manifest.py': {'bytes': 1056, 'sha256': '0835a8d137419cc6236c1f9c9f2cc1726b652232b097a8f7c1528870dc05b49a'}}
SCOPE={'problem_id': 30004425, 'problem_number': 'OWR-17473-001', 'rank': 750, 'status': 'unsolved', 'turns': '1/5', 'disposition': 'qualified prior-results/source-curation correction', 'controlling_edition': 'author/corrected_safe_freeze', 'controlling_acceptance': 'delta_audit/DELTA_ACCEPTANCE.md', 'corrected_package_verdict': 'PASS', 'original_audit_verdict': 'REVISE_REQUIRED (historical; two corrections closed by delta acceptance)', 'new_theorem_claim': False, 'novelty_claim': False, 'universal_resolution_claim': False, 'general_piecewise_linear_result': 'Already published by Escobar and Harada', 'semigroup_bijection_condition': 'Both prime cones are faces of a common maximal Groebner cone', 'universal_additivity': False, 'universal_geometric_restriction': False, 'source_conventions': 'Independent integral common rows including the degree row; complementary rows satisfying the relative-interior condition; reverse degree then lexicographic order; vertical value-lattice normalization', 'publication_boundary': 'Authored proof/code/audit/results and public verification metadata only; no source PDFs, source text extracts, raw datasets, private sources, or private coordination files', 'turn_accounting': 'One queue attempt out of five; historical author mathematical passes are separate from this research-turn count'}
def require(ok,message):
    if not ok: raise AssertionError(message)
def pin(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(path,*args):
    return subprocess.check_output([sys.executable,str(path),*map(str,args)])
def verify():
    require(not (ROOT/'PUBLICATION_MANIFEST.json').is_symlink(),'symlink manifest')
    manifest=json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_bytes())
    expected=set(manifest['files'])|{'PUBLICATION_MANIFEST.json'}
    require(all(not p.startswith('/') and '..' not in Path(p).parts for p in expected),'unsafe path')
    expected_dirs={str(p) for name in expected for p in Path(name).parents if str(p)!='.'}
    actual_files=set(); actual_dirs=set()
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(),'symlink: '+str(path))
        rel=path.relative_to(ROOT).as_posix()
        if path.is_file(): actual_files.add(rel)
        elif path.is_dir(): actual_dirs.add(rel)
        else: require(False,'special file')
    require(actual_files==expected,'file allowlist')
    require(actual_dirs==expected_dirs,'directory allowlist')
    for name,meta in manifest['files'].items():
        require(pin((ROOT/name).read_bytes())==meta,'manifest hash '+name)
    for name,meta in FROZEN.items():
        require(pin((ROOT/name).read_bytes())==meta,'frozen pin '+name)
    require(json.loads((ROOT/'PUBLICATION.json').read_bytes())==SCOPE,'scope boundary')
    archives=[
      ('author/TROPICAL_WALL_30004425_AUTHOR_SAFE_FREEZE.zip','author/safe_freeze','safe_freeze'),
      ('author/TROPICAL_WALL_30004425_CORRECTED_SAFE_FREEZE.zip','author/corrected_safe_freeze','corrected_safe_freeze'),
      ('TROPICAL_WALL_30004425_INDEPENDENT_AUDIT.zip','independent_audit','tropical_wall_30004425_independent_audit'),
      ('TROPICAL_WALL_30004425_DELTA_ACCEPTANCE.zip','delta_audit','tropical_wall_30004425_delta_audit')]
    for archive,folder,prefix in archives:
        with zipfile.ZipFile(ROOT/archive) as z:
            names=z.namelist()
            expect={prefix+'/'+p.name for p in (ROOT/folder).iterdir() if p.is_file()}
            require(len(names)==len(set(names)) and set(names)==expect,'zip members '+archive)
            for name in names:
                require(z.read(name)==(ROOT/folder/Path(name).name).read_bytes(),'zip bytes '+name)
    old=ROOT/'author/safe_freeze';new=ROOT/'author/corrected_safe_freeze';audit=ROOT/'independent_audit';delta=ROOT/'delta_audit'
    for author in [old,new]:
        run(author/'verify_manifest.py')
        require(run(author/'verify.py')==(author/'VERIFICATION_RESULTS.json').read_bytes(),'author replay')
    run(audit/'verify_audit_manifest.py')
    for author in [old,new]:
        require(run(audit/'mutation_verify.py',author)==(audit/'MUTATION_RESULTS.json').read_bytes(),'four code mutations')
    run(delta/'verify_manifest.py')
    require(run(delta/'verify_delta.py',old,new,audit)==(delta/'DELTA_RESULTS.json').read_bytes(),'delta replay')
    return {'result':'PASS','problem_id':30004425,'status':'unsolved','turns':'1/5','packet_files':len(expected),'frozen_files_and_archives':len(FROZEN),'archives':4,'original_corrected_independent_delta_replays':'PASS','code_mutations_rejected':4,'false_strengthenings_rejected':8,'new_universal_resolution':False}
if __name__=='__main__': print(json.dumps(verify(),indent=2))
