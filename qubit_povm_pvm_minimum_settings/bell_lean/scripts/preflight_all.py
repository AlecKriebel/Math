#!/usr/bin/env python3
"""Run the compiler-free preflight and exact checks; never invoke Lean or Lake.

The final status is preflight_passed, NOT proof_verified. Tests of the future
Lean runner use mocked process outputs in temporary folders, explicitly labelled.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
from pathlib import Path
import py_compile
import subprocess
import sys
from run_lean import write_json

ROOT=Path(__file__).resolve().parents[1]
COMMANDS=[
 ('source_audit',['scripts/source_audit.py']),
 ('import_inventory',['scripts/source_completion_inventory.py']),
 ('static_checks',['scripts/preflight_checks.py']),
 ('parser_tests',['scripts/test_axiom_audit.py']),
 ('source_root_tests',['scripts/test_source_roots.py']),
 ('runner_tests',['scripts/test_preflight.py']),
 ('package_tests',['scripts/test_packaging.py']),
 ('environment_tests',['environment/test_handoff.py']),
 ('exact_checks',['scripts/exact_checks.py']),
 ('sos_checks',['scripts/sos_checks.py']),
 ('sos_bareiss',['scripts/sos_bareiss_check.py']),
 ('deterministic_gap',['scripts/deterministic_gap_checks.py']),
 ('expanded_source_algebra',['scripts/source_completion_checks.py','--suite','all']),
 ('physical_interface_audit',['scripts/semantic_audit.py','--suite','all']),
]


def main():
    out=ROOT/'reports/preflight';out.mkdir(parents=True,exist_ok=True)
    report={'status':'in_progress','started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'lean_invoked':False,'kernel_checked':False,'commands':[],
            'scope':'Compiler-free byte/structure/harness checks and independent finite exact algebra only.'}
    path=out/'validation_summary.json';write_json(path,report)
    try:
        syntax=[]
        for folder in ('scripts','environment'):
            for p in sorted((ROOT/folder).glob('*.py')):
                py_compile.compile(str(p),doraise=True);syntax.append(p.relative_to(ROOT).as_posix())
        for p in sorted((ROOT/'scripts').glob('*.sh')):
            subprocess.run(['bash','-n',str(p)],check=True,cwd=ROOT)
            syntax.append(p.relative_to(ROOT).as_posix())
        report['syntax_checked_files']=syntax
        for name,argv in COMMANDS:
            log=out/(name+'.log')
            with log.open('w') as f:
                result=subprocess.run([sys.executable,*argv],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
            entry={'name':name,'argv':[sys.executable,*argv],'exit_code':result.returncode,
                   'log':log.relative_to(ROOT).as_posix(),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
            report['commands'].append(entry);write_json(path,report)
            print(f'{name}: '+('passed' if result.returncode==0 else 'FAILED'),flush=True)
            if result.returncode:
                raise RuntimeError(f'{name} failed; inspect {log}')
        reports={
            'static':'reports/preflight/static_checks.json',
            'runner_harness':'reports/preflight/harness_tests.json',
            'packaging':'reports/preflight/package_tests.json',
            'parser':'reports/source_completion/axiom_parser_tests.json',
            'expanded_finite_algebra':'reports/source_completion/exact_all.json',
            'baseline_finite_algebra':'reports/exact_checks.json',
            'physical_interface_audit':'reports/semantic_audit/all.json',
        }
        report['evidence']={key:{'path':rel,'sha256':hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()}
                            for key,rel in reports.items()}
        report['status']='preflight_passed'
    except BaseException as exc:
        report['status']='preflight_failed';report['error']=str(exc)
        raise
    finally:
        report['ended_utc']=dt.datetime.now(dt.timezone.utc).isoformat();write_json(path,report)
    print('COMPILER-FREE PREFLIGHT PASSED. This compiler-free run does not certify Lean proofs.')

if __name__=='__main__':main()
