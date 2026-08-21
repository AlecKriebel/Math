#!/usr/bin/env python3
"""Verify package hashes, imports, source census, and a resumable smoke run."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, pathlib, shutil, subprocess, sys, tempfile


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--skip-smoke',action='store_true');parser.add_argument('--skip-mutations',action='store_true');parser.add_argument('--skip-prepared-audit',action='store_true');args=parser.parse_args()
    root=pathlib.Path(__file__).resolve().parent
    lock=json.loads((root/'INPUT_LOCK.json').read_text())
    for rel,want in lock['files'].items():
        path=root/rel
        if not path.exists() or sha(path)!=want:raise SystemExit(f'INPUT_LOCK_FAIL {rel}')
    subprocess.run([sys.executable,str(root/'test_exact_kernels.py')],check=True)
    lock_command=[sys.executable,str(root/'resumable_four_port_driver.py'),'--package-root',str(root)]
    if args.skip_prepared_audit:
        result=subprocess.run(lock_command+['--list-sources'],text=True,capture_output=True,check=True)
        census=json.loads(result.stdout)
        counts=[row['canonical_class_count'] for row in census];ranks=[row['source_rank'] for row in census];prepared_checked=None
    else:
        result=subprocess.run(lock_command+['--audit-prepared-relations'],text=True,capture_output=True,check=True)
        audit=json.loads(result.stdout);counts=audit['source_class_counts'];ranks=audit['source_ranks'];prepared_checked=audit['prepared_relation_presentations_checked']
        if prepared_checked<=0:raise SystemExit('PREPARED_RELATION_AUDIT_EMPTY')
    expected=lock['expected_source_class_counts'];expected_ranks=lock['expected_source_ranks']
    if counts!=expected:raise SystemExit(('SOURCE_CENSUS_FAIL',counts))
    if ranks!=expected_ranks:raise SystemExit(('SOURCE_RANK_FAIL',ranks))
    if not args.skip_smoke:
        with tempfile.TemporaryDirectory(prefix='k2p_sweep_smoke_') as tmp:
            cmd=[sys.executable,str(root/'resumable_four_port_driver.py'),'--package-root',str(root),
                 '--source-index','0','--start','206','--end','210','--output-root',tmp]
            first=subprocess.run(cmd,text=True,capture_output=True,check=True)
            second=subprocess.run(cmd,text=True,capture_output=True,check=True)
            if '"processed": 4' not in first.stdout or '"reused": 4' not in second.stdout:
                raise SystemExit(('RESUME_SMOKE_FAIL',first.stdout,second.stdout))
            records=list((pathlib.Path(tmp)/'source_0'/'records').glob('*.json'))
            if len(records)!=4:raise SystemExit('RECORD_COUNT_FAIL')
            if any(json.loads(p.read_text())['status']!='separated' for p in records):raise SystemExit('HARD_CASE_SMOKE_FAIL')
    if not args.skip_mutations:
        subprocess.run([sys.executable,str(root/'test_mutations.py'),'--package-root',str(root)],check=True)
    print('K2P_OFFLINE_SWEEP_PACKAGE_PASS')
    print(json.dumps({'source_class_counts':expected,'source_ranks':expected_ranks,'prepared_relation_presentations_checked':prepared_checked,'python':sys.version.split()[0]},sort_keys=True))

if __name__=='__main__':main()
