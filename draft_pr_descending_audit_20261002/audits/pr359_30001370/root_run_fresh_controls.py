#!/usr/bin/env python3
"""Parent native replays of independent exact and parsed numerical controls."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys
A=Path(__file__).resolve().parent
RUN=A/'root_replay_private/fresh_controls_002'
def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
def run(label,argv,cwd):
    start=utc(); p=subprocess.run(argv,cwd=cwd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    end=utc()
    (RUN/(label+'.stdout')).write_bytes(p.stdout)
    (RUN/(label+'.stderr')).write_bytes(p.stderr)
    rec=dict(argv=argv,cwd=str(cwd),started_utc=start,completed_utc=end,exit_code=p.returncode,
             stdout=dict(path=label+'.stdout',bytes=len(p.stdout),sha256=sha(p.stdout)),
             stderr=dict(path=label+'.stderr',bytes=len(p.stderr),sha256=sha(p.stderr)))
    (RUN/(label+'.execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
    return p,rec
def main():
    assert not RUN.exists()
    RUN.mkdir(parents=True)
    tasks=[('algebra_continuous','algebra_certificate_review/public/check_uniform_algebra.py',
            'algebra_certificate_review/public/UNIFORM_CERTIFICATE.json',
            ['--candidate-csv',str(A/'snapshot/problems/30001370_basin_boundaries/TURN_3_CONTRACTION.csv')]),
           ('algebra_symbolic','algebra_certificate_review/public/check_symbolic_equations.py',
            'algebra_certificate_review/public/SYMBOLIC_IDENTITIES.json',[]),
           ('topology','topology_density_review/public/check_topology.py',
            'topology_density_review/public/topology_checks.json',[]),
           ('backward_portable','backward_feedback_review/public/verify_controls.py',
            'backward_feedback_review/private/replays/portable_controls_python311.stdout',[])]
    receipts=[]
    for label,code,expected,args in tasks:
        p,rec=run(label,[sys.executable,'-B',str(A/code)]+args,A)
        rec['expected_path']=expected
        rec['whole_stdout_byte_exact']=p.stdout==(A/expected).read_bytes()
        assert p.returncode==0 and not p.stderr and rec['whole_stdout_byte_exact'], rec
        receipts.append(rec)
    out={'utc':utc(),'status':'PASS_FOUR_INDEPENDENT_CONTROLS_REPRODUCED',
         'native_runs':receipts,'all_four_whole_stdout_byte_exact':True,
         'backward_numerical_summary_policy':'Every exact field equals its saved value; only two labeled floating summaries use1e-12 absolute tolerance and independent experimental bounds. Prior raw crossruntime mismatch retained at fresh_controls_001.',
         'scope':'New exact continuous certificates and finite falsification controls reproduced; infinite-dimensional proof checked analytically.'}
    (A/'ROOT_FRESH_CONTROLS_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='native_runs'},indent=2))
if __name__=='__main__': main()
