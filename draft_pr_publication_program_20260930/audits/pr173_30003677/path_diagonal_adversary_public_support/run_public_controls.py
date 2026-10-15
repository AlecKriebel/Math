#!/usr/bin/env python3
"""Portable standard-library reproduction of own positive/negative controls."""
from pathlib import Path
import argparse, datetime, hashlib, json, platform, subprocess, sys

VARIANTS=('endpoint_only','open_ball','voronoi','parallel_collapse','parity_plus_one','budget_without_rate','seed_divergence_without_floor','uniform_identity_without_uniform_root','log_bound_replaced_by_size')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def need(condition,reason):
    if not condition:
        raise RuntimeError(reason)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='Write aggregate receipt here; default prints JSON to standard output.')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent;control=root/'explicit_controls.py'
    need(control.is_file(),'Place this driver beside explicit_controls.py.')
    runs=[];baseline=[]
    for optimized in (False,True):
        for variant in ('true',*VARIANTS):
            command=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(control)]
            portable=['python3','-B']+(['-O'] if optimized else [])+['explicit_controls.py']
            if variant!='true':command+=['--variant',variant];portable+=['--variant',variant]
            began=datetime.datetime.now(datetime.timezone.utc).isoformat()
            p=subprocess.run(command,cwd=root,text=True,capture_output=True)
            record={'variant':variant,'optimized':optimized,'began_utc':began,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command_sanitized':portable,'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()}
            if variant=='true':
                need(p.returncode==0,'Positive controls failed: '+p.stderr)
                data=json.loads(p.stdout)
                need(data.get('status')=='PASS','Positive receipt is not PASS.')
                need(data['checks']==159474 and data['finite_competition_instances']==20016 and data['protected_path_witnesses']==25176,'Exact control totals changed.')
                need(len(data['semantic_false_variants'])==len(VARIANTS),'Wrong false-variant count.')
                record['stdout_json']=data;baseline.append(data)
            else:
                need(p.returncode!=0,'False variant was accepted: '+variant)
                lines=p.stderr.splitlines()
                marker='VerificationFailure: '
                need(bool(lines) and lines[-1].startswith(marker),'Negative run did not raise expected explicit exception: '+variant)
                record['semantic_rejection']={'exception':'VerificationFailure','payload':json.loads(lines[-1][len(marker):])}
            runs.append(record)
    need(baseline[0]==baseline[1],'Ordinary and optimized baseline outputs differ.')
    result={'status':'PASS','scope':'Twenty actual runs of own finite and arithmetic controls. No stochastic local-limit, source-scope, novelty, or external-checker certification.','control_source_sha256':digest(control),'driver_source_sha256':digest(Path(__file__)),'runtime':{'python_version':sys.version,'implementation':platform.python_implementation(),'platform':platform.platform(),'machine':platform.machine(),'python_binary_sha256':digest(Path(sys.executable).resolve())},'runs':runs,'summary':{'run_count':len(runs),'positive_runs':2,'negative_runs':18,'all_negative_runs_rejected':True,'ordinary_optimized_positive_output_equal':True}}
    rendered=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(rendered)
        print(json.dumps({'status':'PASS','receipt':args.output.name,'run_count':len(runs),'positive_checks_each':159474,'negative_runs_rejected':18},sort_keys=True))
    else:
        print(rendered,end='')

if __name__=='__main__':main()
