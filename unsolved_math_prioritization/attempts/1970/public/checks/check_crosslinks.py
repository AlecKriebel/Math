#!/usr/bin/env python3
"""Cross-link independently regenerated outputs and check every witness directly.
This script does not compute a new optimum. The wrapper independently reruns
both optimizers before comparing their published exact output fixtures.
"""
import argparse,copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def require(ok,why):
    if not ok:raise ValueError(why)
def read(rel):return json.loads((ROOT/rel).read_text())
def smooth(n):
    values=[];a=1
    while a<=n:
        b=a
        while b<=n:values.append(b);b*=3
        a*=2
    return sorted(values)
def verify(packet,independent,base):
    rows=packet['rows'];require(len(rows)==200,'prefix length mismatch')
    alt=independent['smooth'];require(len(alt)==77,'independent comparison length')
    qrows=base['finite_cutoffs'];require(len(qrows)==280,'single-defect base length')
    qbyx={r['cutoff']:r for r in qrows};require(len(qbyx)==280,'duplicate base cutoff')
    for index,row in enumerate(rows,1):
        X=row['X'];vertices=smooth(X)
        require(row['index']==index and len(vertices)==index and vertices[-1]==X,'smooth domain/index mismatch')
        edges=[(n,2*n,3*n) for n in vertices if 3*n<=X]
        for key,size,cap in [('selected','tau',None),('q0_selected','q0',0),('q1_selected','q1',1)]:
            witness=row[key];H=set(witness)
            require(len(witness)==len(H)==row[size] and H<=set(vertices),'witness cardinality/domain mismatch')
            hits=[len(H.intersection(edge)) for edge in edges]
            require(all(h>=1 for h in hits),'uncovered complete triple')
            excess=sum(h-1 for h in hits)
            if cap is None:require(excess==row['defect'],'reported unrestricted defect mismatch')
            else:require(excess<=cap,'excess cap mismatch')
        require(row['q1']==qbyx[X]['q1'],'overlapping q1 minimum mismatch')
        if index<=77:
            other=alt[index-1]
            for key in ['index','X','tau','optimal_count']:
                require(row[key]==other[key],'independent '+key+' comparison mismatch')
            require(row['q0_candidate']==other['q0_color_candidate'],'independent color comparison mismatch')
            require(row['q1_candidate']==other['q1_terminal_candidate'],'independent patch comparison mismatch')
    numeric=read('fixtures/exact/tau_through_X192.json')
    require(numeric==[{'index':r['index'],'X':r['X'],'tau':r['tau']} for r in rows if r['X']<=192],'numeric table cross-link mismatch')
    arithmetic=read('fixtures/check_arithmetic.json')
    require(arithmetic['tau_input_sha256']==hashlib.sha256((ROOT/'fixtures/exact/tau_through_X192.json').read_bytes()).hexdigest(),'arithmetic input identity mismatch')
    for script,fixture in [('checks/check_structure.py','fixtures/check_structure.json'),('checks/check_single_defect.py','fixtures/check_single_defect.json')]:
        require(read(fixture)['script_sha256']==hashlib.sha256((ROOT/script).read_bytes()).hexdigest(),'checker-to-fixture identity mismatch')
    return {'status':'PASS','directly_checked_prefix_witnesses':200,'independent_minimum_and_count_comparisons':77,'overlapping_q1_comparisons':200,'numeric_cutoff_values':len(numeric),'finite_only':True,'global_tau_equals_q1_inferred':False}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inject',choices=['independent_count','base_q1','missing_witness','missing_row']);args=p.parse_args()
    packet=read('fixtures/exact/prefix_200.json');other=read('fixtures/check_independently.json');base=read('fixtures/check_single_defect.json')
    if args.inject=='independent_count':other['smooth'][44]['optimal_count']+=1
    elif args.inject=='base_q1':base['finite_cutoffs'][0]['q1']+=1
    elif args.inject=='missing_witness':packet['rows'][44]['selected'].remove(3)
    elif args.inject=='missing_row':packet['rows'].pop()
    result=verify(packet,other,base)
    if args.inject:raise RuntimeError('cross-link mutation was not rejected')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
