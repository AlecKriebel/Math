#!/usr/bin/env python3
"""Read-only reproduction of final verification. Standard library, Python 3.9+.
Temporary certificates are generated outside the bundle and then deleted.
"""
import json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(*args):
    print('\n$ '+sys.executable+' '+' '.join(map(str,args)),flush=True)
    subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,check=True)

def main():
    run(ROOT/'src/test_check.py')
    run(ROOT/'src/test_verification.py')
    run(ROOT/'src/verify_unsat.py',ROOT/'certificates/local_relaxation.cnf',ROOT/'certificates/local_unsat_tree.json')
    with tempfile.TemporaryDirectory(prefix='knights_rooks_verify_') as tmp:
        out=Path(tmp)/'regenerated.json'
        run(ROOT/'src/dpll_prove.py',ROOT/'certificates/local_relaxation.cnf',out,'--prefer',19)
        run(ROOT/'src/verify_unsat.py',ROOT/'certificates/local_relaxation.cnf',out)
        original=json.loads((ROOT/'certificates/local_unsat_tree.json').read_text())
        if json.loads(out.read_text())!=original:raise RuntimeError('Regenerated certificate differs')
    print('\nALL CHECKS PASSED: 20 test methods; bundled certificate accepted; identical certificate regenerated.',flush=True)
    print('The universal conclusion additionally uses the explicit reduction in FINITE_REDUCTION.md and the proof in PROOF.md.',flush=True)
if __name__=='__main__':main()
