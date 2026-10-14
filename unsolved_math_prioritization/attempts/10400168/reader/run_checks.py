#!/usr/bin/env python3
"""Replay authored finite checks in disposable copies, with isolated interpreters."""
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
SCRIPT='pass1_validation/verify_examples.py'
BASELINE='pass1_validation/RESULTS.normal.json'
MODES=[('normal',[]),('optimized',['-O']),('double_optimized',['-OO'])]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():return {p.relative_to(ROOT).as_posix():digest(p) for p in ROOT.rglob('*') if p.is_file()}
def invoke(args,cwd,env):
    return subprocess.run([sys.executable,'-I','-B',*args],cwd=cwd,env=env,capture_output=True,timeout=240)
def main():
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
    cp=invoke([str(ROOT/'verify_package.py')],ROOT,env)
    require(cp.returncode==0 and not cp.stderr,'Package integrity failed before replay')
    before=snapshot();expected=(ROOT/BASELINE).read_bytes();records=[]
    for rel in [SCRIPT,'pass1_validation/run_checks.py']:
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((ROOT/rel).read_text()))),'Optimization-sensitive assert in '+rel)
    with tempfile.TemporaryDirectory(prefix='subcategory-tqft-replay-') as temp:
        for mode,flags in MODES:
            work=Path(temp)/mode;shutil.copytree(ROOT,work)
            for p in work.rglob('*'):
                if p.is_file():p.chmod(0o644)
            cp=invoke([*flags,str(work/SCRIPT)],work,env)
            require(cp.returncode==0 and not cp.stderr,'Finite check failed: '+mode)
            require(cp.stdout==expected,'Finite baseline differs: '+mode)
            result=json.loads(cp.stdout)
            require(result['status']=='PASS' and result['explicit_checks_completed']==17857,'Wrong finite check status or count')
            probe='import runpy; ns=runpy.run_path('+repr(str(work/SCRIPT))+'); ns["check"](False,"intentional public guard probe")'
            negative=invoke([*flags,'-c',probe],work,env)
            require(negative.returncode!=0 and b'RuntimeError: intentional public guard probe' in negative.stderr,'False guard accepted: '+mode)
            records.append({'script':SCRIPT,'mode':mode,'script_sha256':digest(ROOT/SCRIPT),'output_sha256':hashlib.sha256(cp.stdout).hexdigest(),'output_bytes':len(cp.stdout),'exact_baseline_match':True,'explicit_checks_completed':17857,'intentional_guard_rejected':True,'returncode':0})
        # Also replay the original authored orchestration script in an isolated copy.
        work=Path(temp)/'original-runner';shutil.copytree(ROOT,work)
        for p in work.rglob('*'):
            if p.is_file():p.chmod(0o644)
        cp=invoke([str(work/'pass1_validation/run_checks.py')],work,env)
        require(cp.returncode==0 and not cp.stderr,'Original runner failed')
        receipt=json.loads(cp.stdout)
        require(receipt['status']=='PASS' and receipt['all_outputs_byte_identical'],'Original runner reported failure')
        require(all(r['explicit_checks_completed']==17857 and r['explicit_guard_failure_confirmed'] for r in receipt['runs']),'Original runner check/guard mismatch')
        for name in ['RESULTS.normal.json','RESULTS.O.json','RESULTS.OO.json']:
            require((work/'pass1_validation'/name).read_bytes()==expected,'Regenerated output differs: '+name)
        original_receipt=json.loads((ROOT/'pass1_validation/RUN_RECEIPT.json').read_text())
        # Python patch-version metadata is informative; the mathematical output bytes are exact.
        receipt.pop('python',None);original_receipt.pop('python',None)
        require(receipt==original_receipt,'Original runner receipt differs beyond Python version')
    require(snapshot()==before,'Replay modified the public source tree')
    print(json.dumps({'status':'PASS','finite_script_count':1,'direct_finite_executions':3,'original_runner_finite_executions':3,'total_finite_executions':6,'total_intentional_guard_rejections':6,'modes':[x[0] for x in MODES],'optimization_sensitive_asserts':False,'source_tree_modified':False,'original_runner_replayed_in_isolated_copy':True,'all_finite_outputs_byte_identical':True,'scope':'Exact finite examples and trace consistency checks; general theorems depend on the mathematical proofs and cited constructions.','checks':records},indent=2,sort_keys=True))
if __name__=='__main__':main()
