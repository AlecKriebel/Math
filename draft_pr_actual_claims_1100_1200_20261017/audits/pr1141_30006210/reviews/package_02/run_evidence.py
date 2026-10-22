#!/usr/bin/env python3
"""Reproduce fresh baselines/counterfactuals and disposable corruption guards."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys,ast
from review_io import BASE,REVIEW,pin

def require(c,m):
    if not c:raise RuntimeError(m)
def call(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True,cwd=REVIEW)
    return {'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def negative(cmd,diag,kind,**extra):
    r=call(cmd);require(r['exit_code']!=0 and diag in r['stdout']+r['stderr'],'missing rejection '+kind)
    return dict(r,required_diagnostic=diag,kind=kind,**extra)

def main():
    script=REVIEW/'fresh_controls.py'
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(script.read_text()))),'removable assertions')
    baselines=[];counter=[]
    mutants={'zero-maximizer':'global maximizing magnitude','post-query-law':'post-query pair law','square-density-variance':'full norm mean-square','drop-square-half':'probability-half','demand-cover':'common zeros','covariance-overstrength':'binary covariance'}
    for opt in (False,True):
        cmd=[sys.executable,'-B']+(['-O'] if opt else [])
        b=call(cmd+[str(script)]);require(b['exit_code']==0 and not b['stderr'],'fresh baseline')
        value=json.loads(b['stdout']);require(value['optimized'] is opt and value['python']==sys.version,'fresh runtime')
        (REVIEW/('FRESH.optimized.json' if opt else 'FRESH.normal.json')).write_text(b['stdout'])
        baselines.append(value)
        for name,diag in mutants.items():counter.append(negative(cmd+[str(script),'--counterfactual',name],diag,'computed counterfactual sanity check',optimized=opt,name=name))
    for v in baselines:del v['python'];del v['optimized']
    require(baselines[0]==baselines[1],'fresh mathematical outputs differ')
    (REVIEW/'FRESH_NEGATIVES.json').write_text(json.dumps({'scope':'12 computed explicit counterexamples to false formulas/laws in both modes. Limited sanity checks; not mutations of the implemented separator/covariance algorithms and not an implementation error-coverage claim.','runs':counter},indent=2)+'\n')
    extract=REVIEW/'tmp/extracted';vpath=extract/'verification/verify_all.py'
    spec=importlib.util.spec_from_file_location('verifier',vpath);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    plan=json.loads((extract/'verification/CONTROL_PLAN.json').read_text())
    actual=json.loads((REVIEW/'tmp/runner.normal.json').read_text())
    original=json.loads(pin(BASE/'publication/verification/REPLAY_RECEIPT.json','original frozen complete replay receipt semantic mathematical comparison'))
    require(actual['status']=='PASS' and len(actual['runs'])==8 and len(actual['actual_failure_guards'])==40,'complete frozen replay')
    for run in actual['runs']:
        row=next(x for x in plan['controls'] if x['program']==run['program'])
        expected=json.loads((extract/plan['source_prefix']/row['expected']).read_text())
        v.compare(v.normalize(run['result'],row,run['optimized']),v.expected_semantics(expected,row))
    import copy
    aa,oo=copy.deepcopy(actual),copy.deepcopy(original)
    for container in (aa,oo):
        for run in container['runs']:
            row=next(x for x in plan['controls'] if x['program']==run['program'])
            run['result']=v.expected_semantics(run['result'],row)
    v.compare(aa,oo)
    fixtures=[("v.compare(True,1)",'Type mismatch'),("v.compare(2,1)",'Value mismatch'),("v.compare({},{\"a\":1})",'Keys mismatch'),("v.compare({\"a\":1,\"b\":2},{\"a\":1})",'Keys mismatch'),("v.compare([1],[1,2])",'Length mismatch'),("v.compare((1,),[1])",'Type mismatch'),("v.compare({\"proof_sha256\":\"bad\"},{\"proof_sha256\":\"good\"})",'Value mismatch'),("v.compare({\"runtime\":{\"code_sha256\":\"bad\"}},{\"runtime\":{\"code_sha256\":\"good\"}})",'Value mismatch'),("v.normalize({\"runtime\":{\"python\":\"wrong\",\"optimization\":0}},{\"runtime_kind\":\"separator\",\"drop_paths\":[]},False)",'Unexpected separator interpreter'),("v.normalize({\"python_version\":\"wrong\",\"optimized\":False},{\"runtime_kind\":\"target\",\"drop_paths\":[]},False)",'Unexpected target interpreter'),("v.normalize({\"runtime\":{\"python\":sys.version,\"optimization\":1}},{\"runtime_kind\":\"separator\",\"drop_paths\":[]},False)",'Unexpected separator mode'),("v.normalize({\"python_version\":platform.python_version(),\"optimized\":True},{\"runtime_kind\":\"target\",\"drop_paths\":[]},False)",'Unexpected target mode')]
    guards=[]
    for opt in (False,True):
        cmd=[sys.executable,'-B']+(['-O'] if opt else [])
        for expression,diag in fixtures:
            code='import importlib.util,sys,platform; s=importlib.util.spec_from_file_location("v",'+repr(str(vpath))+'); v=importlib.util.module_from_spec(s); s.loader.exec_module(v); '+expression
            guards.append(negative(cmd+['-c',code],diag,'comparison/runtime fixture',optimized=opt,expression=expression))
    (REVIEW/'COMPARISON_GUARDS.json').write_text(json.dumps(guards,indent=2)+'\n')
    # Corrupt only disposable extracted paths, restoring exact bytes immediately.
    files=[plan['source_prefix']+'/inputs/PROOF.md','zenodo-metadata.json','output/pdf/polynomial-compatibility.pdf','verification/verify_all.py']
    corrupt=[]
    for name in files:
        p=extract/name;original=p.read_bytes()
        try:
            p.write_bytes(original+b'\n')
            for opt in (False,True):
                cmd=[sys.executable,'-B']+(['-O'] if opt else [])+[str(vpath)]
                corrupt.append(negative(cmd,'Fingerprint mismatch','disposable file corruption',optimized=opt,member=name))
        finally:p.write_bytes(original)
    name='README.md';p=extract/name;original=p.read_bytes();target=REVIEW/'tmp/symlink-readme-target';target.write_bytes(original)
    try:
        p.unlink();p.symlink_to(target)
        for opt in (False,True):
            cmd=[sys.executable,'-B']+(['-O'] if opt else [])+[str(vpath)]
            corrupt.append(negative(cmd,'Fingerprint mismatch README.md','disposable final-file symlink',optimized=opt,member=name))
    finally:p.unlink();p.write_bytes(original)
    (REVIEW/'CORRUPTION_GUARDS.json').write_text(json.dumps(corrupt,indent=2)+'\n')
    summary={'fresh_baselines':2,'all_fresh_mathematical_fields_equal':True,'fresh_code_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'fresh_counts':baselines[0]['counts'],'fresh_counterfactual_sanity_failures':len(counter),'counterfactual_implementation_mutation_claim':False,'frozen_runner_baselines':8,'frozen_runner_actual_bad_math_failures':40,'entire_frozen_replay_receipt_semantics_equal':True,'comparison_runtime_rejections':len(guards),'actual_disposable_corruption_or_symlink_rejections':len(corrupt),'all_extracted_corruptions_restored':True,'normalization':'Only the plan-declared runtime fields are removed; actual interpreter and optimization are validated first. All mathematical hashes, values, keys and types retained; comparison fixtures reject their corruption.'}
    (REVIEW/'EXECUTION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
