#!/usr/bin/env python3
"""Offline read-only verification of the complete scoped publication packet."""
from pathlib import Path, PurePosixPath
import hashlib, json, os, subprocess, sys, zipfile
ROOT = Path(__file__).resolve().parent
FROZEN = {'author/AUTHOR_MANIFEST.json': {'bytes': 1593, 'sha256': 'b14e3900ec0feee118e05a3884c5f2380735950e4e0e252804dd0e26f193c5c9'}, 'author/CHECK_RESULTS.json': {'bytes': 45971, 'sha256': '58325446054a2a3e30d384f3fdf3fa83a71ed5fc7cb79de71a7bbf5dc774e018'}, 'author/LIMITATIONS.md': {'bytes': 1764, 'sha256': '606b05f3c460b3d7c858534352f4841a28b8387b6f403530673d44bf4bcf6782'}, 'author/LITERATURE.md': {'bytes': 5857, 'sha256': '2a61c7ade53e5e061380d0a0ef7c462ad070be2a0d70a3c8eb42b6ce04e35a16'}, 'author/PROOFS.md': {'bytes': 11087, 'sha256': 'f4e42315aa758a084f04e7d1e062024e00a9232223a5620511bec9b682760622'}, 'author/README.md': {'bytes': 2873, 'sha256': '321b91f6b9fe3e04e53218cdd60f3d6f395c1f86a49b582ad5a0fb2d1f8b3de4'}, 'author/RESEARCH_LOG.md': {'bytes': 4100, 'sha256': '2b2929e5bb61f1e976a51e53f74f8f526927999876472c37d6e6b3481d023896'}, 'author/SOURCE_VERIFICATION.json': {'bytes': 9005, 'sha256': '52d6d16c8ffbd169ec12d53abfa4cbf5a0ce7f752ef7249811690bf08a251fed'}, 'author/verify_manifest.py': {'bytes': 880, 'sha256': '49ddb54b45b62ae1b40a385cdb7dc9bfcc37450fa66eb40cdcb0d851733a81b8'}, 'author/verify_math.py': {'bytes': 8579, 'sha256': '797c43e67f0c7c35a69fc6b2cdce7eaf6d7942e7b8d16a67018a3aa652f66511'}, 'independent_audit/AUDIT_CHECK_RESULTS.json': {'bytes': 93521, 'sha256': '3f628cce8679ec394c85ed12d41c48de43db1d3b521d51966195826c45e6be9c'}, 'independent_audit/AUDIT_MANIFEST.json': {'bytes': 1475, 'sha256': '0a47cb6a9c94c73a6d5bc04aabcbc51581dda7001aad96f9b611387811db4ce6'}, 'independent_audit/AUDIT_REPORT.md': {'bytes': 14929, 'sha256': '134378a94c6748ba87b62d300d9c933f692d10f121cf3d36ab5a9f88fc6a5abb'}, 'independent_audit/CORRECTIONS.json': {'bytes': 1185, 'sha256': 'ff34896096d3f05640bce694a2b62dc5953f29c9d26f93638779b760b14a6141'}, 'independent_audit/README.md': {'bytes': 1866, 'sha256': '7df240fcafc1d323dfd84f89da5a573b66f68bbaf22a22696268de0728c417ed'}, 'independent_audit/REPLAY_SUMMARY.json': {'bytes': 564, 'sha256': '7a83800957dae3c5a4ffaa68ad95c0582b49922526a35075f5098fdef2c133c5'}, 'independent_audit/SOURCE_AUDIT.json': {'bytes': 5999, 'sha256': 'ff9a52e2f969fbefbb9608939cc3a61fe95c7333a2daed47f478c78560434aa4'}, 'independent_audit/independent_checks.py': {'bytes': 15184, 'sha256': '4fc244016d073935e0df658b77cbbb0f046491d4ef5b819b851e1cd18b3e43fa'}, 'independent_audit/verify_audit_manifest.py': {'bytes': 876, 'sha256': 'f244166d3d979f0206ad52d38a988e3672da53880b71a9e41dea6fff0d73371a'}, 'KOUROVKA_2604_AUTHOR_SAFE_FREEZE.zip': {'bytes': 25435, 'sha256': '6d51c5e2467b119245a6b8ef2e1444f6ffb07decc0822522ea240106a6a02f91'}, 'KOUROVKA_2604_INDEPENDENT_AUDIT_SAFE.zip': {'bytes': 25077, 'sha256': '79f627888754790aa0e12f94f6ef707533362c765a232b6acd91c46b51751f01'}, 'KOUROVKA_2604_PROVENANCE_SUPPLEMENT.json': {'bytes': 10279, 'sha256': 'a0f4d7d9834485f385cee8839ad26e4fa18e58f7e82ce089de0f51a3299f888f'}}
ARCHIVES = [('KOUROVKA_2604_AUTHOR_SAFE_FREEZE.zip', 'author', '6d51c5e2467b119245a6b8ef2e1444f6ffb07decc0822522ea240106a6a02f91'), ('KOUROVKA_2604_INDEPENDENT_AUDIT_SAFE.zip', 'independent_audit', '79f627888754790aa0e12f94f6ef707533362c765a232b6acd91c46b51751f01')]
SCOPE = {'problem_id': 2604, 'problem_number': 'KOU-21.95', 'rank': 771, 'status': 'unsolved', 'turns': '5/5', 'original_problem_solved': False, 'novelty_claim': False, 'mathematical_audit': 'PASS_SCOPED_PARTIAL_RESULTS', 'required_mathematical_corrections': [], 'provenance_gate': 'PASS_PROVENANCE_GATE_WITH_EXPLICIT_SEARCH_LIMITS', 'comparison_class': 'All finite groups', 'graph_convention': 'Abstract unlabelled Gruenberg-Kegel graph', 'infinite_family_exclusions': ['Every symmetric group S_n with n >= 5 has infinitely many affine labelled-prime-graph competitors.', 'Every concrete intermediate characteristic-two symplectic natural-module field-semilinear group has infinitely many affine labelled-prime-graph competitors; exceptional graph automorphisms are not included.'], 'finite_census': {'targets': 183, 'target_class': 'Odd prime powers q, 5 <= q <= 1000', 'witness_search_cap': 10000, 'maximum_author_witness': 461, 'all_q_theorem': False, 'infinitely_many_partners_for_each_target_proved': False}, 'sporadic_exclusions': 'Five literature-dependent exclusions: Aut(M12), Aut(He), Aut(Fi22), Aut(HN), and Aut(McL). Imported full classification proofs are not independently certified.', 'optional_audit_observations': ['The q=4 fixed-vector transvection test has zero qualifying pairs; q=8 supplies 504 nonvacuous pairs.', 'The independent audit computes 5526 fixed-space dimensions by binary elimination.'], 'historical_certification_boundary': 'The author audit-pending labels and the audit exclusions of corpus/repository provenance remain historical statements in unchanged originals. The separate later provenance supplement adds exactly its documented byte-identity, descriptor and bounded prior-attempt checks. It does not broaden the mathematical verdict or certify full imported proofs, novelty, or universal absence of prior work.', 'publication_boundary': 'Authored proofs, analysis, code, exact results, independent audit, unchanged safe archives, and public verification metadata only. Source PDFs, source extracts/images, raw corpora, selected records, private sources, private personal data, and private coordination files are excluded.'}
def require(condition, message):
    if not condition: raise RuntimeError(message)
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(name): return json.loads((ROOT/name).read_bytes())
def checked_files():
    files=set(); dirs=set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'Unexpected symlink: '+str(p))
        name=p.relative_to(ROOT).as_posix()
        if p.is_dir(): dirs.add(name)
        else:
            require(p.is_file(), 'Unexpected nonregular entry: '+name); files.add(name)
    return files, dirs
def run():
    manifest=read('PUBLICATION_MANIFEST.json')
    require(manifest['problem_id']==2604 and manifest['status']=='unsolved' and manifest['turns']=='5/5', 'Manifest scope mismatch')
    entries=manifest['files']; names=[e['path'] for e in entries]
    require(len(names)==len(set(names)), 'Duplicate manifest path')
    for name in names:
        p=PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in name, 'Unsafe manifest path')
    files,dirs=checked_files()
    require(files==set(names)|{'PUBLICATION_MANIFEST.json'}, 'Recursive file inventory mismatch')
    require(dirs=={'author','independent_audit'}, 'Recursive directory inventory mismatch')
    for entry in entries:
        require(pin((ROOT/entry['path']).read_bytes())=={k:entry[k] for k in ('bytes','sha256')}, 'Manifest byte mismatch: '+entry['path'])
    for name,expected in FROZEN.items(): require(pin((ROOT/name).read_bytes())==expected, 'Frozen byte mismatch: '+name)
    require(read('PUBLICATION.json')==SCOPE, 'Publication scope mismatch')
    require(read('author/AUTHOR_MANIFEST.json')['original_problem_solved'] is False, 'Author status mismatch')
    corrections=read('independent_audit/CORRECTIONS.json')
    require(corrections['original_problem_solved'] is False and corrections['research_approaches_used']==5 and corrections['required_mathematical_corrections']==[], 'Audit scope mismatch')
    supplement=read('KOUROVKA_2604_PROVENANCE_SUPPLEMENT.json')
    require(supplement['verdict']==SCOPE['provenance_gate'] and supplement['original_problem_solved'] is False, 'Provenance scope mismatch')
    members=0
    for archive,sub,_ in ARCHIVES:
        with zipfile.ZipFile(ROOT/archive) as z:
            expected=sorted(p.name for p in (ROOT/sub).iterdir())
            require(z.testzip() is None and sorted(z.namelist())==expected and len(z.namelist())==len(set(z.namelist())), 'ZIP inventory mismatch: '+archive)
            for name in z.namelist():
                require(z.read(name)==(ROOT/sub/name).read_bytes(), 'ZIP member mismatch: '+name); members+=1
    env=dict(os.environ); env.pop('PYTHONOPTIMIZE',None); env['PYTHONDONTWRITEBYTECODE']='1'
    commands=[('author_manifest','author',['verify_manifest.py']),('author_math','author',['verify_math.py']),('audit_manifest','independent_audit',['verify_audit_manifest.py']),('independent_math','independent_audit',['independent_checks.py','--author-dir',str(ROOT/'author')])]
    results={}
    for label,sub,args in commands:
        result=subprocess.run([sys.executable,*args],cwd=ROOT/sub,env=env,capture_output=True,text=True,check=True)
        results[label]=json.loads(result.stdout)
    result={'status':'PASS','problem_id':2604,'original_problem_solved':False,'turns':'5/5','recursive_files':len(files),'frozen_files':len(FROZEN),'zip_members':members,'replays':results}
    require(result==read('VERIFICATION_RESULTS.json'), 'Recorded verification results mismatch')
    require(checked_files()==(files,dirs), 'Replay changed inventory')
    for entry in entries:
        require(pin((ROOT/entry['path']).read_bytes())=={k:entry[k] for k in ('bytes','sha256')}, 'Replay modified bytes: '+entry['path'])
    return result
if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
