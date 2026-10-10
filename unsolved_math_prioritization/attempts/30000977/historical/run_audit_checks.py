#!/usr/bin/env python3
"""Run both finite checkers and explicit read-only probes as real UID/EUID 1000.

The candidate is never modified. Copied input fixtures are chmod 0444, their
directory 0555, and all run logs are captured outside that directory.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

def demand(ok, detail):
    if not ok:
        raise RuntimeError(detail)

def record(p):
    b = p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
            'mode':oct(p.stat().st_mode & 0o777)}

def run(candidate, fixture, output):
    demand(os.getuid() == os.geteuid() == 1000, 'Read-only tests require actual UID and EUID 1000.')
    inputs = {p.name:record(p) for p in sorted(candidate.iterdir()) if p.is_file()}
    demand(not fixture.exists(), 'Do not overwrite prior fixtures or uncertain test runs.')
    fixture.mkdir(parents=True)
    for p in sorted(candidate.iterdir()):
        if p.is_file():
            shutil.copyfile(p, fixture / p.name)
    shutil.copyfile(HERE / 'independent_exact_checks.py', fixture / 'independent_exact_checks.py')
    (fixture / 'sentinel').write_text('read-only fixture\n')
    for p in fixture.iterdir():
        p.chmod(0o444)
    fixture.chmod(0o555)
    fixture_before = {p.name:record(p) for p in sorted(fixture.iterdir())}
    probe_code = r'''
import errno, json, os
from pathlib import Path
if os.getuid() != 1000 or os.geteuid() != 1000:
    raise RuntimeError('Not actual UID/EUID 1000')
rows=[]
for name,mode in [('sentinel','ab'),('forbidden_new_file','xb')]:
    try:
        with open(name,mode) as f:
            f.write(b'x')
    except PermissionError as e:
        rows.append({'target':name,'mode':mode,'blocked':True,'errno':e.errno})
    else:
        raise RuntimeError('Read-only protection failed: '+name)
print(json.dumps({'uid':os.getuid(),'euid':os.geteuid(),'cwd_mode':oct(Path('.').stat().st_mode & 0o777),'file_mode':oct(Path('sentinel').stat().st_mode & 0o777),'probes':rows},sort_keys=True))
'''
    runs = []
    independent_mutants = [
        'rank_two_group','dependent_kummer_classes','diagonal_quotient',
        'opposite_F_generators','duality_sign_error','missing_canonical_section',
        'extra_canonical_section','wrong_divisor_coefficients',
        'omitted_singular_stratum','printed_quadric_relation',
        'smooth_quadric_claim','construction_degree_confusion',
    ]
    original_mutants = ['bad_group','bad_relation','missing_section','bad_branch','bad_characteristic']
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for label, flags in [('normal',[]),('-O',['-O']),('-OO',['-OO'])]:
        p = subprocess.run([sys.executable,'-B']+flags+['-c',probe_code],cwd=fixture,env=env,capture_output=True,text=True)
        probe = {'mode':label,'program':'read_only_probe','mutation':None,'expected_exit':0,
                 'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
        runs.append(probe)
        demand(p.returncode == 0, 'Read-only probe failed: '+p.stderr+p.stdout)
        for filename, mutants in [('verify_counterexample.py',original_mutants),('independent_exact_checks.py',independent_mutants)]:
            for mutant in [None]+mutants:
                args = [sys.executable,'-B']+flags+[filename]+(['--mutate',mutant] if mutant else [])
                p = subprocess.run(args,cwd=fixture,env=env,capture_output=True,text=True)
                expected = 2 if mutant else 0
                runs.append({'mode':label,'program':filename,'mutation':mutant,'expected_exit':expected,
                             'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
                demand(p.returncode == expected, 'Unexpected result for '+str(args)+': '+p.stdout+p.stderr)
    fixture_after = {p.name:record(p) for p in sorted(fixture.iterdir())}
    after = {p.name:record(p) for p in sorted(candidate.iterdir()) if p.is_file()}
    demand(inputs == after, 'Original candidate files changed.')
    demand(fixture_before == fixture_after, 'Read-only fixture changed.')
    summary = {'status':'PASS_EXECUTED_CHECKS_ONLY','uid':os.getuid(),'euid':os.geteuid(),
               'positive_checker_runs':6,'expected_mutant_rejections':51,
               'read_only_probe_runs':3,'write_attempts_denied':6,
               'modes':['normal','-O','-OO'],'candidate_files_unchanged':True,
               'readonly_fixtures_unchanged':True,'candidate_snapshot':inputs,
               'auditor_checker':record(HERE/'independent_exact_checks.py'),
               'runner':record(Path(__file__)),
               'run_count':len(runs),'runs':runs}
    output.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('runs','candidate_snapshot')},sort_keys=True))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', type=Path, required=True,
                        help='Read-only input directory containing the original four candidate artifacts.')
    parser.add_argument('--fixture', type=Path, required=True,
                        help='New fixture directory; never reuse an existing path.')
    parser.add_argument('--output', type=Path, required=True,
                        help='JSON log destination outside the read-only fixture.')
    args = parser.parse_args()
    run(args.candidate.resolve(), args.fixture.resolve(), args.output.resolve())
