#!/usr/bin/env python3
"""Replay the independent family from a separate declarative input file.
The original pre-candidate code/output/seal remain immutable.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import argparse,json
from independent_controls import output_quotient,finite_chain,word

def replay(inputs):
    tests=[]
    for model in inputs['targeted_models']:
        p=[[F(x) for x in r] for r in model['P']];e=[[F(x) for x in r] for r in model['emissions']];pi=[F(x) for x in model['stationary']]
        d=output_quotient(p,e,pi);assert d['observable_quotient_by_label_indices']==model['expected_quotient']
        if model['name']=='first_marginal_equal_word2_separates':
            w=d['pairwise_witnesses'][0];assert len(w['first_distinguishing_word'])==2 and w['probabilities']==[F(1,2),F(1,4)]
        tests.append({'name':model['name'],'data':d,'assertions_passed':True})
    sharp=[]
    for n in inputs['word_bound_sharpness_N_values']:
        p=[[F(j==min(i+1,n-1)) for j in range(n)] for i in range(n)];e=[[F(i!=n-1),F(i==n-1)] for i in range(n)]
        delta=[F(1),F(-1)]+[F(0)]*(n-2);found=None
        for k in range(n):
            for w in product(range(2),repeat=k):
                v=word(p,e,w);val=sum((x*y for x,y in zip(delta,v)),F(0))
                if val:found={'P':p,'emissions':e,'initial_difference':delta,'N':n,'first_distinguishing_word':list(w),'length':k,'probability_difference':val};break
            if found:break
        assert found is not None and found['length']==n-1;sharp.append(found)
    spec=inputs['complete_scan'];rows=[[F(x) for x in row] for row in spec['rows']]
    assert all(len(row)==spec['state_count'] and sum(row)==1 for row in rows)
    scan=[finite_chain([list(row) for row in p]) for p in product(rows,repeat=spec['state_count'])]
    return {'scope':'Finite structural/linear ingredients only; universal probability proof is a separate artifact.','targeted_models':tests,'word_bound_sharpness_general_initial_distributions':sharp,'complete_three_state_denominator_two_scan':scan,'all_assertions_passed':True}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path,default=Path(__file__).with_name('independent_inputs.json'));args=ap.parse_args()
    print(json.dumps(replay(json.loads(args.inputs.read_text())),indent=2,default=lambda x:str(x) if isinstance(x,F) else x))
