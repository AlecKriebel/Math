#!/usr/bin/env python3
"""Read-only source/package checks and isolated copied-script replays."""
from pathlib import Path
import hashlib, json, shutil, subprocess, datetime

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
ROOT=AUDIT.parents[2]
TMP=HERE/'ignoredtmp'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)

def check_entries(folder, entries):
    result=[]
    for path,expected in entries.items():
        actual=sha((folder/path).read_bytes())
        assert actual==expected,(folder,path,expected,actual)
        result.append({'path':str(folder.relative_to(AUDIT)/path),'sha256':actual})
    return result

def integrity(output_name='integrity_checks.json'):
    snap=json.loads((AUDIT/'snapshot_manifest.json').read_text())
    original={f['path']:f['sha256'] for f in snap['files']}
    assert len(original)==17
    original_checks=check_entries(AUDIT/'source_snapshot',original)
    for f in snap['files']:
        source=git('show',snap['head']+':unsolved_math_prioritization/attempts/30000819/'+f['path'])
        assert sha(source)==f['sha256']
    candidate=json.loads((AUDIT/'reviewed_candidate/MANIFEST.json').read_text())['sha256']
    assert len(candidate)==19
    actualpaths={str(p.relative_to(AUDIT/'reviewed_candidate')) for p in (AUDIT/'reviewed_candidate').rglob('*') if p.is_file()}
    assert actualpaths==set(candidate)|{'MANIFEST.json'}
    current_checks=check_entries(AUDIT/'reviewed_candidate',candidate)
    for path in original:
        if path.startswith('review/') or path in ('source_record.json','source_provenance.json','verify.py','verification.json','.gitignore'):
            assert candidate[path]==original[path]
    families=json.loads((AUDIT/'FAMILY_MANIFEST.json').read_text())['sha256']
    family_checks=[]
    for folder,entries in families.items():
        family_checks+=check_entries(AUDIT/folder,entries)
    assert len(family_checks)==21
    primary=json.loads((AUDIT/'primary_scope_family/family_manifest.json').read_text())
    for entry in primary['files']:
        assert sha((AUDIT/'primary_scope_family'/entry['path']).read_bytes())==entry['sha256']
    first=json.loads((AUDIT/'final_adversary/MANIFEST.json').read_text())
    # The earlier adversarial verdict remains bound to its earlier candidate.
    if 'sha256' in first:
        first_checks=check_entries(AUDIT/'final_adversary',first['sha256'])
    elif isinstance(first['files'],dict):
        first_checks=check_entries(AUDIT/'final_adversary',{p:v['sha256'] for p,v in first['files'].items()})
    else:
        first_checks=[]
        for entry in first['files']:
            assert sha((AUDIT/'final_adversary'/entry['path']).read_bytes())==entry['sha256']
            first_checks.append(entry)
    round1_bytes=(AUDIT/'round1_input_manifest.json').read_bytes()
    commit='1252d9d7855ab2ca7c856d644698d2863a19558e'
    old_path='draft_pr_publication_program_20260930/audits/pr15_30000819/reviewed_candidate/MANIFEST.json'
    assert git('show',commit+':'+old_path)==round1_bytes
    assert sha(round1_bytes)=='e91e7e60e9ce379c0f942a854f86d555fb2e2bc4d955acbeae9955826df88358'
    for path,expected in json.loads(round1_bytes)['sha256'].items():
        assert sha(git('show',commit+':'+str(Path(old_path).parent/path)))==expected
    attempt=json.loads((AUDIT/'reviewed_candidate/attempt.json').read_text())
    assert attempt['proof_sha256']==candidate['PROOF.md']==attempt['current_proof_sha256']
    assert attempt['original_proof_sha256']==original['PROOF.md']
    assert attempt['substantive_attempts_used']==1 and attempt['substantive_attempt_limit']==5
    assert attempt['queue_status_proposed']=='already_solved'
    assert attempt['dataset_existential_status']=='already_solved'
    assert attempt['formulated_target_status']=='already_solved'
    assert not any(attempt[k] for k in ('paper_created','zenodo_deposit_created','tracker_row_created'))
    six=['PROOF.md','README.md','SOURCE_AUDIT.md','PRIORITY_SCOPE_UPDATE.md','attempt.json','pr_body.md']
    for name in six:
        text=(AUDIT/'reviewed_candidate'/name).read_text()
        assert 'already_solved' in text
    inventory=json.loads((ROOT/'draft_pr_publication_program_20260930/inventory.json').read_text())
    item=next(x for x in inventory['items'] if x['number']==15)
    assert item['proof_sha256']==candidate['PROOF.md']
    assert item['proposed_queue_status']=='already_solved'
    queue=ROOT/'unsolved_math_prioritization/QUEUE.md'
    row=next(s for s in queue.read_text().splitlines() if '| 30000819 /' in s)
    ignored=subprocess.run(['git','check-ignore',str(TMP/'owr.pdf')],cwd=ROOT,capture_output=True,text=True)
    assert ignored.returncode==0
    result=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                frozen_head=snap['head'],original_17_checks=original_checks,
                current_19_checks=current_checks,current_total_files=len(actualpaths),
                family_21_checks=family_checks,first_fresh_checks=first_checks,
                round1_commit=commit,round1_manifest_sha256=sha(round1_bytes),
                current_proof_sha256=candidate['PROOF.md'],
                current_manifest_sha256=sha((AUDIT/'reviewed_candidate/MANIFEST.json').read_bytes()),
                historical_frozen_proof_sha256=original['PROOF.md'],
                historical_reviewed_proof_sha256=original['review/reviewed_PROOF.md'],
                six_classification_locations=six,all_six_already_solved=True,
                current_inventory_item=item,canonical_queue_preintegration_row=row,
                canonical_queue_sha256=sha(queue.read_bytes()),
                integration_followthrough='Parent confirms canonical queued0/5 is pre-integration state. Accepted merge must change only numeric target to already_solved1/5, DOI blank, preserving all previous accepted rows.',
                cache_ignore_verified=True,read_only_git_operations=True,passed=True)
    (HERE/output_name).write_text(json.dumps(result,indent=2)+'\n')
    return result

def replay(name, source, generated, expected):
    folder=TMP/'replays'/name
    folder.mkdir(parents=True,exist_ok=True)
    copied=folder/source.name
    shutil.copyfile(source,copied)
    r=subprocess.run(['python3',str(copied)],cwd=folder,capture_output=True)
    assert r.returncode==0,(name,r.stderr.decode())
    (folder/'stdout.txt').write_bytes(r.stdout)
    (folder/'stderr.txt').write_bytes(r.stderr)
    data=(folder/generated).read_bytes() if generated else r.stdout
    assert data==expected.read_bytes(),name
    return dict(name=name,source=str(source.relative_to(AUDIT)),script_sha256=sha(source.read_bytes()),
                reproduced_sha256=sha(data),expected_sha256=sha(expected.read_bytes()),
                stdout_sha256=sha(r.stdout),byte_identical=True,exit_code=r.returncode)

def replays():
    runs=[
        ('historical_author',AUDIT/'source_snapshot/verify.py',None,AUDIT/'source_snapshot/verification.json'),
        ('historical_independent',AUDIT/'source_snapshot/review/independent_checks.py','independent_checks.json',AUDIT/'source_snapshot/review/independent_checks.json'),
        ('candidate_author',AUDIT/'reviewed_candidate/verify.py',None,AUDIT/'reviewed_candidate/verification.json'),
        ('candidate_historical_checker',AUDIT/'reviewed_candidate/review/independent_checks.py','independent_checks.json',AUDIT/'reviewed_candidate/review/independent_checks.json'),
        ('algebra_family',AUDIT/'algebra_family/exact_checks.py','exact_checks.json',AUDIT/'algebra_family/exact_checks.json'),
        ('combinatorial_family',AUDIT/'combinatorial_family/exact_checks.py','exact_checks.json',AUDIT/'combinatorial_family/exact_checks.json'),
        ('first_fresh_adversary',AUDIT/'final_adversary/exact_checks.py','exact_checks.json',AUDIT/'final_adversary/exact_checks.json')]
    results=[replay(*run) for run in runs]
    (HERE/'replay_receipts.json').write_text(json.dumps(dict(passed=True,isolated=True,replays=results),indent=2)+'\n')
    return results

if __name__=='__main__':
    result=integrity()
    print('Integrity passed:',len(result['original_17_checks']),'original,',len(result['current_19_checks']),'candidate entries,',len(result['family_21_checks']),'family entries.')
    results=replays()
    print('All',len(results),'isolated replays byte-identical.')
