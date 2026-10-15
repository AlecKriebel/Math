#!/usr/bin/env python3
"""Fresh isolated execution of every actual original/current/family program.

Never edits input packets, source receipts, Git/GitHub or shared ledgers.
Expected failure is retained as failure. Dynamic provenance fields are qualified.
"""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = HERE.parents[3]
OUT = HERE / 'replay_outputs'
OUT.mkdir(exist_ok=True)
SHA = lambda b: hashlib.sha256(b).hexdigest()

def protected():
    inventory = json.loads((HERE/'INPUT_INVENTORY.json').read_text())['files']
    paths = {Path(i['path']) for i in inventory}
    paths |= {REPO/'unsolved_math_prioritization'/n for n in
              ['QUEUE.md','state.json','history.jsonl','assessment_history.jsonl','update_history.jsonl']}
    return {str(p):SHA(p.read_bytes()) for p in sorted(paths)}

def run():
    before = protected()
    base = HERE/'tmp/isolated/Math'
    dst = base/AUDIT.relative_to(REPO)
    if base.exists(): shutil.rmtree(base)
    dst.mkdir(parents=True)
    for n in ['source_snapshot','reviewed_candidate','pr_input']:
        shutil.copytree(AUDIT/n,dst/n)
    shutil.copy2(AUDIT/'snapshot_manifest.json',dst/'snapshot_manifest.json')
    deps=json.loads((AUDIT/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json').read_text())['files']
    for entry in deps:
        p=dst/entry['path'];p.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(AUDIT/entry['path'],p)
    shared=base/'unsolved_math_prioritization';shared.mkdir()
    for n in ['QUEUE.md','state.json','history.jsonl','assessment_history.jsonl','update_history.jsonl']:
        shutil.copy2(REPO/'unsolved_math_prioritization'/n,shared/n)
    tasks=[
        ('original31','source_snapshot/check_monodromy.py','source_snapshot/check_results.json',0),
        ('old53830','source_snapshot/review/independent_checks.py','source_snapshot/review/independent_results.json',0),
        ('current31','reviewed_candidate/check_monodromy.py','reviewed_candidate/check_results.json',0),
        ('geometric_controls','geometric_family/geometric_controls.py','geometric_family/geometric_control_results.json',0),
        ('intentional_failure','geometric_family/failure_harness.py',None,1),
        ('geometric_driver','geometric_family/reproduce.py',None,0),
        ('primary_driver','primary_scope_family/validate_evidence.py','primary_scope_family/validation_results.json',0),
        ('action_controls','monodromy_family/independent_action_controls.py','monodromy_family/independent_action_results.json',0),
        ('monodromy_driver','monodromy_family/reproduce_original.py','monodromy_family/original_replay_and_integrity.json',0),
    ]
    receipts=[]
    for label,script,result,expected in tasks:
        code=dst/script;code_before=SHA(code.read_bytes())
        retained=(AUDIT/result).read_bytes() if result else None
        proc=subprocess.run(['/usr/bin/python3',str(code)],cwd=base,capture_output=True,timeout=120)
        (OUT/(label+'_stdout.txt')).write_bytes(proc.stdout)
        (OUT/(label+'_stderr.txt')).write_bytes(proc.stderr)
        row={'program':script,'source_sha256':code_before,'runtime':'/usr/bin/python3',
             'returncode':proc.returncode,'expected_returncode':expected,
             'code_unchanged':SHA(code.read_bytes())==code_before,
             'stdout_sha256':SHA(proc.stdout),'stderr_sha256':SHA(proc.stderr)}
        if result:
            raw=(dst/result).read_bytes();data=json.loads(raw)
            (OUT/(label+'_results.json')).write_bytes(raw)
            row.update(result_sha256=SHA(raw),frozen_sha256=SHA(retained),byte_identical=raw==retained,
                       assertions=data.get('assertions'))
            if label=='monodromy_driver':
                old=json.loads(retained)
                differences={k for k in old if old[k]!=data[k]}
                assert differences <= {'utc','before_shared_and_snapshot_hashes','original_and_live_pr_bodies_match','live_metadata_base_tip'}
                row['dynamic_fields_differ']=sorted(differences)
                row['dynamic_qualification']='UTC, live PR body/base and dated unrelated accepted-state bytes; exact math and original blobs must match.'
                for k in differences:old.pop(k);data.pop(k)
                assert old==data
                row['all_frozen_and_math_fields_equal']=True
            else: assert raw==retained, label
        elif label=='geometric_driver':
            assert proc.stdout==(AUDIT/'geometric_family/reproduction_results.json').read_bytes()
            row['stdout_byte_identical']=True
        elif label=='intentional_failure':
            assert b'INTENTIONAL_MUTANT' in proc.stderr
            row['classification']='EXPECTED_FAILURE_RECORDED_NOT_PASS'
        assert proc.returncode==expected and row['code_unchanged'], row
        receipts.append(row)
        print(label,proc.returncode,row.get('byte_identical',row.get('classification','driver reproduced')))
    after=protected();assert before==after
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'all_actual_programs_reproduced':True,'program_runs':receipts,
            'before_input_hashes':before,'after_input_hashes':after,
            'protected_inputs_unchanged':True,'new_substantive_attempts':0,
            'no_git_github_shared_mutation':True}
    (HERE/'REPRODUCTION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__': run()
