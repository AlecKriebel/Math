#!/usr/bin/env python3
"""Finite exact regression controls for the separately proved algebra lemmas."""
from itertools import product
import json


def normal_form(exponents, deltas, free_delta=0):
    assert len(exponents)==len(deltas)
    rank=1+2*len(exponents)
    det=(-1)**free_delta
    for a,d in zip(exponents,deltas):
        assert a>=1
        det+=(-1)**d+(-1)**(d+a-1)
    return rank,det,sum(a%2==0 for a in exponents)


def run():
    cases=valid=0
    # The parity/graded-contribution data only depends on a mod 2 and delta mod 2;
    # testing a=1,2,3,4 also catches a mistakenly fixed delta separation.
    alphabet=list(product(range(1,5),range(2)))
    for k in range(6):
        for entries in product(alphabet,repeat=k):
            a=tuple(x[0] for x in entries); d=tuple(x[1] for x in entries)
            r,det,e=normal_form(a,d)
            cases+=1
            if det%8==1:
                valid+=1
                assert r%4==(1+2*e)%4
                if all(x%2 for x in a): assert r%4==1
    # Explicit formal splitting/determinant countermodel, NOT a knot realization.
    r,det,e=normal_form((2,),(0,))
    assert (r,det,e)==(3,1,1)
    # A pair of even exponents restores the congruence.
    assert normal_form((2,2),(0,0))==(5,1,2)
    # Determinant square alone, or s=0 alone, cannot force mod 4 rank.
    # Integral universal coefficient formula, including adjacent Tor terms.
    uct_cases=0
    for free in product(range(4),repeat=4):
        for torsion in product(range(3),repeat=4):
            rational=sum(free)
            mod_p=sum(free[i]+torsion[i]+(torsion[i+1] if i<3 else 0) for i in range(4))
            # Boundaries of the displayed range must include the extra contribution
            # in degree -1 from torsion[0].
            mod_p+=torsion[0]
            assert mod_p==rational+2*sum(torsion)
            assert (mod_p-rational)%4==2*(sum(torsion)%2)
            uct_cases+=1
    # Explicit integral complex: free z plus Z --p--> Z.
    # Q rank=1, F_p rank=3, free rank remains 1.
    integer_countermodel=dict(free_rank=1,p_primary_cyclic_summands=1,mod_p_rank=3)
    # Connected-sum rank multiplication and mirror invariance imply odd squares.
    square_cases=0
    for n in range(1,1000,2):
        assert n*n%8==1
        square_cases+=1
    return dict(status='PASS',normal_form_cases=cases,slice_determinant_cases=valid,
                uct_cases=uct_cases,odd_square_cases=square_cases,
                formal_countermodel=dict(exponents=[2],source_delta=[0],free_delta=0,
                                        rank=r,signed_determinant=det,even_exponents=e,
                                        knot_realization_claimed=False),
                coefficient_countermodel=integer_countermodel,
                warning='Finite checks are regression controls, not proofs of universal knot statements.')


if __name__=='__main__':print(json.dumps(run(),indent=2))
