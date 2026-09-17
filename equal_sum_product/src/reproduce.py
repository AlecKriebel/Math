#!/usr/bin/env python3
"""Run all certificate checks and regression tests. No third-party packages."""
import json
import platform
from pathlib import Path
import re
import subprocess
import sys

VERSION = '1.0.0'
ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT/'logs'


def run(name, args, expected_returncode=0):
    command = [sys.executable] + args
    process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    (LOGS/(name+'.stdout')).write_text(process.stdout,encoding='utf-8')
    (LOGS/(name+'.stderr')).write_text(process.stderr,encoding='utf-8')
    result = {'name':name,'command':command,'expected_returncode':expected_returncode,
              'returncode':process.returncode,'passed':process.returncode==expected_returncode}
    match = re.search(r'Ran (\d+) tests',process.stderr)
    if match:
        result['unittest_cases'] = int(match.group(1))
    print(name+': '+('PASS' if result['passed'] else 'FAIL'),flush=True)
    if not result['passed']:
        print(process.stdout)
        print(process.stderr,file=sys.stderr)
    return result


def main():
    LOGS.mkdir(exist_ok=True)
    stages = [
        run('checker_tests',['-m','unittest','discover','-s','tests','-v']),
        run('exact_audit',['src/audit_inequalities.py']),
        run('source_control',['src/verify_matrix.py','certificates/source_two_rows.json','--min-rows','2']),
        run('source_dimension_guard',['src/verify_matrix.py','certificates/source_two_rows.json'],1),
        run('ordinary_three_rows',['src/verify_matrix.py','certificates/ordinary_three_rows.json'],1),
        run('repeated_entries',['src/verify_matrix.py','certificates/repeated_three_rows.json'],1),
        run('scaled_source',['src/verify_matrix.py','certificates/scaled_source.json','--min-rows','2'],1)
    ]
    summary = {'reproducer_version':VERSION,'all_passed':all(s['passed'] for s in stages),
               'environment':{'python':platform.python_version(),'system':platform.system(),
                              'machine':platform.machine()},'stages':stages,
               'proof_status':'Universal nonexistence is established by the mathematical note, not by these finite tests.',
               'matrix_search_performed':False}
    (LOGS/'reproduction_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
    return 0 if summary['all_passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
