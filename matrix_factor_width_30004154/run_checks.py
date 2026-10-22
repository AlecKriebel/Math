"""Exact certificate and complete-output replay, in ordinary and optimized Python."""
import ast
import json
import pathlib
import subprocess
import sys

def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def main():
    root=pathlib.Path(__file__).resolve().parent
    checks=[]
    for p in root.glob('*.py'):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))), 'Assertion-dependent script: '+p.name)
    for optimized in (False,True):
        for script,expected in [('verify_exact.py','exact_verification.txt'),('verify_low_rank.py','low_rank_verification.txt'),('replay.py','replay.txt')]:
            result=subprocess.run([sys.executable,'-I','-B']+(['-O'] if optimized else [])+[script],cwd=root,capture_output=True,timeout=120)
            require(result.returncode==0 and not result.stderr, 'Replay failed: '+script+' '+result.stderr.decode())
            require(result.stdout==(root/expected).read_bytes(),'Complete output mismatch: '+script)
            checks.append({'script':script,'optimized':optimized,'complete_output_match':True})
    print(json.dumps({'status':'PASS','checks':checks,'scope':'Exact finite certificate checks; universal statements require the authored proofs.'},indent=2))
if __name__=='__main__': main()
