#!/usr/bin/env python3
"""Optimization-invariant malformed-claim controls for independent_exact.py."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

def need(ok,reason):
    if not ok: raise ValueError(reason)

def variants(c):
    cases=[]
    def edit(name,path,value):
        d=copy.deepcopy(c); q=d
        for k in path[:-1]: q=q[k]
        q[path[-1]]=value
        cases.append((name,json.dumps(d)))
    edit('false_global_solution',['status'],'SOLVED')
    edit('false_approach_count',['approaches_used'],6)
    edit('boolean_for_integer',['borcherds_inputs',0,'m'],True)
    edit('float_for_integer',['curves','713','good_factors',0,'a'],-3.0)
    edit('false_point_count',['curves','893','good_factors',1,'count_p2'],13)
    edit('false_middle_coefficient',['curves','713','good_factors',4,'b'],-5)
    edit('false_good_factor',['curves','893','good_factors',2,'euler_ascending'],[1,4,11,20,26])
    edit('false_ordinarity',['curves','713','good_factors',1,'ordinary'],True)
    edit('false_root_number',['curves','893','local_root_number_product'],1)
    edit('false_node_sign',['curves','713','bad_factors',0,'epsilon'],1)
    edit('false_bad_factor',['curves','893','bad_factors',0,'euler_ascending'],[1,4,14,19])
    edit('false_normalization',['curves','893','bad_factors',1,'node_value'],37)
    edit('false_residual_group',['residual','713','group'],'S6')
    edit('false_irreducibility',['residual','713','representation'],'absolutely irreducible')
    edit('false_frobenius_witness',['residual','893','frobenius_factorizations',0,'factors_ascending'],[[1,0,0,0,0,0,1]])
    edit('false_theta_weight',['borcherds_inputs',0,'weight'],3)
    edit('false_theta_index',['borcherds_inputs',2,'index'],892)
    edit('false_theta_multiplier',['borcherds_inputs',1,'m'],2)
    edit('false_theta_entry',['borcherds_inputs',0,'phi_entries',0],2)
    edit('false_q_order',['borcherds_inputs',2,'q_order'],1)
    edit('false_simplicity_polynomial',['simplicity','713','characteristic_ascending'],[121,-22,-6,-1,1])
    edit('false_fixed_conductor_twist',['finite_match_control','new_conductor_multiplier'],1)
    edit('null_residual',['residual'],None)
    d=copy.deepcopy(c); d['invented_theorem']='modularity follows'; cases.append(('extra_claim',json.dumps(d)))
    d=copy.deepcopy(c); del d['scope']; cases.append(('missing_scope',json.dumps(d)))
    raw=json.dumps(c)
    cases += [('duplicate_status','{"status":"SOLVED",'+raw[1:]),
              ('nonfinite_number',raw.replace('120121','NaN',1)),
              ('truncated_json',raw[:-1]),('nonobject_json','[]')]
    return cases

def main():
    p=argparse.ArgumentParser(); p.add_argument('packet',type=Path); a=p.parse_args()
    script=Path(__file__).with_name('independent_exact.py')
    c=json.loads((a.packet/'certificate.json').read_text())
    cases=variants(c); report={'modes':[],'positive':0,'rejected':0,'cases':[n for n,_ in cases]}
    with tempfile.TemporaryDirectory(prefix='independent-borcherds-') as td:
        for flag in ('','-O','-OO'):
            cmd=[sys.executable,'-B']+([flag] if flag else [])+[str(script),str(a.packet)]
            r=subprocess.run(cmd,capture_output=True,text=True)
            need(r.returncode==0 and 'PASS_INDEPENDENT_BOUNDED_ARITHMETIC' in r.stdout,'positive '+flag+': '+r.stderr)
            report['positive']+=1; report['modes'].append(flag or 'normal')
            for name,raw in cases:
                claim=Path(td)/(name+'.json'); claim.write_text(raw)
                r=subprocess.run(cmd+['--certificate',str(claim)],capture_output=True,text=True)
                need(r.returncode==2 and 'AUDIT_REJECT:' in r.stderr,'accepted malformed claim '+name+'/'+flag)
                report['rejected']+=1
    report['status']='PASS_INDEPENDENT_NEGATIVE_CONTROLS'
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':
    try: main()
    except Exception as e:
        print('CONTROL_FAILURE: '+str(e),file=sys.stderr); sys.exit(2)
