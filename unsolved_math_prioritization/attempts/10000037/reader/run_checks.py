#!/usr/bin/env python3
"""Replay the two authored finite checkers in temporary copies under three modes."""
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHECKS=[('pass1_validation/validate_construction.py','pass1_validation/validation_report.json',True),('pass1_audit/recheck_exact_constants.py','pass1_audit/INDEPENDENT_ARITHMETIC.json',False)]
MODES=[('normal',[]),('optimized',['-O']),('double_optimized',['-OO'])]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def identity(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():return {p.relative_to(ROOT).as_posix():identity(p) for p in ROOT.rglob('*') if p.is_file()}
def main():
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
    cp=subprocess.run([sys.executable,'-I','-B',str(ROOT/'verify_package.py')],capture_output=True,text=True,env=env,timeout=30)
    require(cp.returncode==0,'Package integrity failed before replay: '+cp.stderr)
    before=snapshot();records=[]
    with tempfile.TemporaryDirectory(prefix='percolation-public-replay-') as temp:
        for rel,baseline,writes in CHECKS:
            require(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse((ROOT/rel).read_text()))),'Checker contains optimization-sensitive assert: '+rel)
            expected=(ROOT/baseline).read_bytes()
            outputs=[]
            for label,flags in MODES:
                work=Path(temp)/(Path(rel).parent.name+'-'+label)
                shutil.copytree(ROOT,work)
                for p in work.rglob('*'):
                    if p.is_file():p.chmod(0o644)
                cp=subprocess.run([sys.executable,'-I','-B',*flags,str(work/rel)],cwd=work,env=env,capture_output=True,timeout=180)
                require(cp.returncode==0,'Checker failed: '+rel+' '+label+' '+cp.stderr.decode())
                require(cp.stderr==b'','Unexpected checker stderr: '+rel+' '+label)
                require(cp.stdout==expected,'Checker output differs from exact retained baseline: '+rel+' '+label)
                if writes:require((work/baseline).read_bytes()==expected,'Regenerated artifact differs: '+rel+' '+label)
                outputs.append(cp.stdout)
                records.append({'script':rel,'script_sha256':identity(ROOT/rel),'mode':label,'baseline':baseline,'output_sha256':hashlib.sha256(cp.stdout).hexdigest(),'output_bytes':len(cp.stdout),'exact_baseline_match':True,'regenerated_baseline_match':True if writes else None,'returncode':0})
            require(len(set(outputs))==1,'Optimization modes disagree: '+rel)
    require(before==snapshot(),'Public source tree modified by replay')
    print(json.dumps({'status':'PASS','script_count':len(CHECKS),'execution_count':len(records),'modes':[x[0] for x in MODES],'optimization_sensitive_asserts':False,'source_tree_modified':False,'python_version':sys.version.split()[0],'scope':'Exact finite checks corroborate arithmetic and implementation; infinite-event claims depend on the authored mathematical proofs.','checks':records},indent=2,sort_keys=True))
if __name__=='__main__':main()
