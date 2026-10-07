#!/usr/bin/env python3
"""Regression tests: false claims and bad computations must fail in every Python mode."""
import ast
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
MODES=[[],['-O'],['-OO']]

def need(ok,label):
    if not ok:
        raise ValueError(label)

def run(script,claims,mode):
    return subprocess.run([sys.executable,*mode,str(script),'--claims',str(claims)],capture_output=True,text=True)

def main():
    base=json.loads((ROOT/'CLAIMS.json').read_text())
    script=ROOT/'verify_math.py'
    expected=(ROOT/'CHECK_RESULTS.json').read_text()
    source=script.read_text()
    for name in ['verify_math.py','test_fail_closed.py','verify_packet.py','test_integrity.py']:
        p=ROOT/name
        if p.exists():
            need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))),'Optimizable assertion present in '+name)
    claim_mutations=[
        ('turn_1','convection_cross','1/59'),
        ('turn_1','amplification_coefficient','0'),
        ('turn_2','isometry_factor','2'),
        ('turn_2','blind_error_squared','0'),
        ('turn_3','catalan_10',16795),
        ('turn_3','rate_dilation_base',1),
        ('turn_4','theta_limit_at_a_1','1'),
        ('turn_4','marking_contradiction_upper','1'),
        ('turn_5','backward_euler_endpoint_error_squared','0'),
        ('turn_5','allocation_p_2_q_1_2_3_N_12','1')]
    code_mutations=[
        ('coefficient=Y/(eps*P)','coefficient=-Y/(eps*P)','wrong Galerkin solve sign'),
        ('residual=[eps*x-y,x+eps*y]','residual=[eps*x+y,x+eps*y]','wrong residual matrix'),
        ('endpoint=F(3,2)','endpoint=F(1)','wrong backward Euler computation')]
    rejected_claims=rejected_code=rejected_malformed=positive=0
    with tempfile.TemporaryDirectory(prefix='transport_fail_closed_') as td:
        td=Path(td)
        for mode in MODES:
            p=run(script,ROOT/'CLAIMS.json',mode)
            need(p.returncode==0 and p.stdout==expected,'Positive replay mismatch in '+repr(mode))
            positive+=1
            for i,(section,key,bad) in enumerate(claim_mutations):
                obj=copy.deepcopy(base);obj[section][key]=bad
                path=td/('bad_claim_'+str(i)+'.json');path.write_text(json.dumps(obj))
                p=run(script,path,mode)
                need(p.returncode!=0 and 'FAILED:' in p.stderr,'False mathematical claim accepted: '+section+'.'+key+' '+repr(mode))
                rejected_claims+=1
            malformed=[
                json.dumps(base)[:-1]+',"problem_id": 30002760}',
                json.dumps({**base,'status':'claimed_solved'}),
                json.dumps({**base,'unexpected':True})]
            for i,body in enumerate(malformed):
                path=td/('malformed_'+str(i)+'.json');path.write_text(body)
                p=run(script,path,mode)
                need(p.returncode!=0,'Malformed or unsupported status accepted: '+str(i)+' '+repr(mode))
                rejected_malformed+=1
            for i,(old,new,label) in enumerate(code_mutations):
                need(source.count(old)==1,'Computation mutation anchor is not unique: '+label)
                path=td/('bad_computation_'+str(i)+'.py');path.write_text(source.replace(old,new))
                p=run(path,ROOT/'CLAIMS.json',mode)
                need(p.returncode!=0 and 'FAILED:' in p.stderr,'Bad computation accepted: '+label+' '+repr(mode))
                rejected_code+=1
    result={'status':'PASS_FAIL_CLOSED','positive_replays':positive,'rejected_false_claims':rejected_claims,'rejected_bad_computations':rejected_code,'rejected_malformed_or_unsupported_claims':rejected_malformed,'modes':['normal','-O','-OO'],'optimizable_assert_statements':0,'scope':'Finite regression evidence, not proof of correctness for arbitrary future code edits.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(str(exc),file=sys.stderr)
        sys.exit(1)
