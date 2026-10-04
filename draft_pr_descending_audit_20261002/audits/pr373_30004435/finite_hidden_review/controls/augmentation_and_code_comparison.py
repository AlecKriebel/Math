#!/usr/bin/env python3
"""Own post-verdict controls: independent augmentation and author-utility comparison.
Reads author modules only after complete inspection and mathematical verdict seal.
No candidate receipt is used as an oracle. Complete per-input JSON is printed.
"""
import importlib.util
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
from independent_controls import classes,stationary,output_quotient,finite_chain,word,new_basis

CANDIDATE=Path(__file__).resolve().parents[2]/'snapshot/unsolved_math_prioritization/attempts/30004435'
def imported(name):
    spec=importlib.util.spec_from_file_location('audited_'+name,CANDIDATE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def augmented(p,e,pi):
    pairs=[(s,a) for s in range(len(p)) for a in range(len(e[0])) if pi[s]*e[s][a]>0]
    q=[[p[s][t]*e[t][b] for t,b in pairs] for s,a in pairs]
    rho=[pi[s]*e[s][a] for s,a in pairs]
    emission=[[F(a==b) for b in range(len(e[0]))] for s,a in pairs]
    return pairs,output_quotient(q,emission,rho)

def normalized_blocks(blocks):return sorted(tuple(sorted(x)) for x in blocks)

def run():
    rows=[[F(0),F(1)],[F(1,2),F(1,2)],[F(1),F(0)]]
    emissions=[[F(0),F(1)],[F(1,2),F(1,2)],[F(1),F(0)]]
    aug=[]
    for p0 in product(rows,repeat=2):
        p=[list(x) for x in p0];pi=stationary(p)
        for e0 in product(emissions,repeat=2):
            e=[list(x) for x in e0];hidden=output_quotient(p,e,pi);pairs,joint=augmented(p,e,pi)
            projected=[[pairs[i][0] for i in ph] for ph in joint['positive_labels']]
            # An augmented phase has repeated hidden states when multiple emissions are possible.
            assert normalized_blocks([list(set(x)) for x in projected])==normalized_blocks(hidden['positive_labels'])
            hm={tuple(sorted(ph)):i for i,ph in enumerate(hidden['positive_labels'])}
            permutation=[hm[tuple(sorted(set(ph)))] for ph in projected]
            projected_quotient=[sorted(permutation[i] for i in group) for group in joint['observable_quotient_by_label_indices']]
            assert normalized_blocks(projected_quotient)==normalized_blocks(hidden['observable_quotient_by_label_indices'])
            aug.append({'hidden_model':hidden,'supported_joint_pairs':[list(x) for x in pairs],'joint_model':joint,'projected_joint_quotient':projected_quotient,'comparison_passed':True})
    # Compare author's supported graph utility and invariant-span basis against independently derived controls.
    fm=imported('finite_markov');obs=imported('observable_space')
    stored=json.loads((Path(__file__).resolve().parents[1]/'streams/independent_controls.stdout.json').read_text())
    utility=[]
    for item in stored['complete_three_state_denominator_two_scan']:
        p=[[F(x) for x in row] for row in item['P']];pi=[F(x) for x in item['stationary']]
        own=finite_chain(p,pi);author=fm.classes_phases(p,pi)
        ownpositive=[c for c in own['closed_classes'] if any(pi[i]>0 for i in c['states'])]
        assert author==ownpositive
        records=[]
        for labels in product(range(2),repeat=3):
            m=obs.matrices(p,labels);basis,dims=obs.observable_basis(m)
            ownbasis=[]
            for k in range(3):
                for w in product(range(2),repeat=k):new_basis(ownbasis,word(p,[[F(x==a) for a in range(2)] for x in labels],w))
            assert len(basis)==len(ownbasis)
            for v in basis:assert not new_basis(ownbasis,list(v))
            for _,v in ownbasis:assert len(obs.basis(basis+[tuple(v)]))==len(basis)
            assert len(dims)<=3
            records.append({'labels':list(labels),'author_basis':basis,'author_dimensions':dims,'independent_dimension':len(ownbasis),'same_span':True})
        utility.append({'P':p,'stationary':pi,'own_supported_class_phase':ownpositive,'author_supported_class_phase':author,'observations':records,'comparison_passed':True})
    return {'augmentation_inputs':aug,'author_utility_comparisons':utility,'all_assertions_passed':True,'scope':'Exact finite comparisons only; mathematical universal verdict was sealed before these tests.'}

if __name__=='__main__':print(json.dumps(run(),indent=2,default=lambda x:str(x) if isinstance(x,F) else x))
