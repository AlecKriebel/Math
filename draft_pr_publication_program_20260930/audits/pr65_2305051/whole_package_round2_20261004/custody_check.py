#!/usr/bin/env python3
"""Independent byte/hash custody check; no Git writes, network, or source mutations."""
import hashlib, json, pathlib, datetime
from audit_operations import HERE, PACKAGE, inventory, sha, write

AUTH = HERE.parent/'original_source_authentication_20261004'

def git_hash(kind, body):
    return hashlib.sha1(kind.encode()+b' '+str(len(body)).encode()+b'\0'+body).hexdigest()

def main():
    commit = json.loads((AUTH/'ORIGINAL_GIT_COMMIT.json').read_text())
    body=(AUTH/'ORIGINAL_GIT_COMMIT_BODY.bin').read_bytes()
    assert git_hash('commit',body)==commit['sha']=='5cc1602c05d79502defb07cec7027963149494d2'
    tree=json.loads((AUTH/'ORIGINAL_RECURSIVE_TREE.json').read_text())
    assert not tree['truncated']
    assert tree['sha']==commit['tree']['sha']
    assert b'tree '+tree['sha'].encode()+b'\n' in body
    groups={'':[]}
    expected={'':tree['sha']}
    for row in tree['tree']:
        parent=pathlib.PurePosixPath(row['path']).parent
        parent='' if str(parent)=='.' else str(parent)
        groups.setdefault(parent,[]).append(row)
        if row['type']=='tree':
            groups.setdefault(row['path'],[])
            expected[row['path']]=row['sha']
    for path,rows in groups.items():
        def order(row):
            return pathlib.PurePosixPath(row['path']).name.encode()+(b'/' if row['type']=='tree' else b'')
        serial=b''
        for row in sorted(rows,key=order):
            name=pathlib.PurePosixPath(row['path']).name.encode()
            mode=row['mode'].lstrip('0').encode()
            serial+=mode+b' '+name+b'\0'+bytes.fromhex(row['sha'])
        assert git_hash('tree',serial)==expected[path], path
    tree_paths={r['path']:r for r in tree['tree']}
    comparisons=[]
    for relative,original in [
        ('verification/author/CANDIDATE.md','unsolved_math_prioritization/attempts/2305051/CANDIDATE.md'),
        ('verification/author/verify_recursion.py','unsolved_math_prioritization/attempts/2305051/verify_recursion.py'),
        ('verification/legacy_independent/independent_checks.py','unsolved_math_prioritization/attempts/2305051/review/independent_checks.py')]:
        package_body=(PACKAGE/relative).read_bytes()
        assert package_body==(AUTH/'original'/original).read_bytes()
        assert git_hash('blob',package_body)==tree_paths[original]['sha']
        comparisons.append({'package_path':relative,'original_path':original,
                            'git_blob':tree_paths[original]['sha'],'sha256':sha(package_body),'bytes':len(package_body)})
    prov=json.loads((PACKAGE/'PROVENANCE.json').read_text())
    assert prov['immutable_head']==commit['sha']
    assert prov['candidate_git_blob']==comparisons[0]['git_blob']
    assert prov['candidate_sha256']==comparisons[0]['sha256']
    receipt=json.loads((PACKAGE/'execution/EXECUTIONS.json').read_text())
    assert sha((PACKAGE/'execution/historical_run_verification.py').read_bytes())==receipt['harness_sha256']
    assert receipt['harness_sha256']!=sha((PACKAGE/'run_verification.py').read_bytes())
    for entry in receipt['executions']:
        label=entry['label']
        for stream in ('stdout','stderr'):
            b=(PACKAGE/entry[stream+'_path']).read_bytes()
            assert sha(b)==entry[stream+'_sha256']
            assert len(b)==entry[stream+'_bytes']
        matching=[r for r in prov['copied_files'] if r['package_path'].startswith('verification/'+label+'/') and r['package_path'].endswith('.py')]
        assert len(matching)==1
        assert matching[0]['sha256']==entry['script_sha256_before_execution']
        assert entry['exit_code']==0
    assert json.loads((PACKAGE/'verification/author/verification.json').read_text())==json.loads((PACKAGE/'execution/author.stdout.txt').read_text())
    assert json.loads((PACKAGE/'verification/legacy_independent/independent_results.json').read_text())==json.loads((PACKAGE/'execution/legacy_independent.stdout.txt').read_text())
    assert json.loads((PACKAGE/'verification/factorization/EXACT_CONTROL_RESULTS.json').read_text())==json.loads((PACKAGE/'execution/factorization.stdout.txt').read_text())
    assert json.loads((PACKAGE/'verification/analytic/DIAGNOSTIC_RESULTS.json').read_text())==json.loads((PACKAGE/'execution/analytic.stdout.txt').read_text())
    metadata=json.loads((PACKAGE/'zenodo-deposit.json').read_text())['metadata']
    assert metadata['title']=='An effective Blaschke construction with Bloch Cayley transform'
    assert metadata['creators']==[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}]
    assert metadata['license']=='cc-by-4.0'
    note=(PACKAGE/'note.tex').read_text()
    assert '\\title{'+metadata['title']+'}' in note
    assert metadata['creators'][0]['orcid'] in note
    assert 'MIT License' in (PACKAGE/'LICENSE-CODE.txt').read_text()
    assert 'Creative Commons Attribution 4.0 International' in (PACKAGE/'LICENSE-TEXT.md').read_text()
    initial=json.loads((HERE/'PACKAGE_BEFORE.json').read_text())
    assert inventory(PACKAGE)==initial['files']
    result={'status':'PASS: independent custody/metadata controls',
            'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'commit_git_sha1':commit['sha'],'root_tree_git_sha1':tree['sha'],
            'independently_recomputed_trees':len(groups),'frozen_original_comparisons':comparisons,
            'historical_operator_matches_receipt':True,
            'current_operator_is_different_and_disclosed':True,
            'package_unchanged_since_snapshot':True,
            'scope':'Internal byte/hash custody and metadata consistency. Historical receipt PIDs are preserved, not retroactively observed or independently authenticated.'}
    write(HERE/'CUSTODY_RESULTS.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
