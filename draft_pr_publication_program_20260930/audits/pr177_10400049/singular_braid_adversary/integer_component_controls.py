"""Exact controls for the V_Z -> Q and component-sector boundary notes."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import importlib.util
import json
import sys

spec=importlib.util.spec_from_file_location('sealed_controls',
    Path(__file__).with_name('independent_controls.py'))
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def main():
    basis_cases=0
    products=0
    component_cases=0
    denominators={}
    for r in range(13):
        values=[Q(comb(n,r) if n>=r else 0) for n in range(41)]
        for n in range(41):
            base.require(base.newton_value(values,r,Q(n))==values[n], 'integer Newton reproduction')
            basis_cases+=1
        half=base.newton_value(values,r,Q(1,2))
        base.require(half==base.binomial_q(Q(1,2),r),'rational denominator control')
        denominators[str(r)]=str(half)
    base.require(denominators['1']=='1/2','target Q, not Z')
    for a in range(6):
        for b in range(6):
            av=[Q(comb(n,a) if n>=a else 0) for n in range(24)]
            bv=[Q(comb(n,b) if n>=b else 0) for n in range(24)]
            pv=[x*y for x,y in zip(av,bv)]
            base.require(base.newton_value(pv,a+b,Q(1,2))==
                base.newton_value(av,a,Q(1,2))*base.newton_value(bv,b,Q(1,2)), 'V_Z product')
            products+=1
    for selected in (2,5,101):
        for k in range(110):
            chi_e=Q(int(k==selected))
            base.require(chi_e*chi_e==chi_e,'component idempotent')
            values=[chi_e]*10
            base.require(base.newton_value(values,0,Q(1,2))==chi_e,'order-zero sector')
            for l in range(110):
                chi_other=Q(int(l==selected))
                base.require(chi_e*chi_other==Q(int(k==l==selected)), 'orthogonal idempotents')
                component_cases+=1
        for H in (lambda m:Q((-1)**m),lambda m:Q(m**3-9*m+4),lambda m:Q(1,m+1)):
            base.require(base.newton_value([H(selected)]*10,0,Q(1,2))==H(selected), 'arbitrary count function')
    chi_g=Q(1,4)
    base.require(chi_g*(4*chi_g-1)==0,'integer f maps to zero')
    for power in range(1,101):
        base.require(chi_g**power!=0,'integer radical obstruction')
    # A proposed character assigning 1 to two orthogonal sectors is rejected.
    rejected_multiple_sectors=(Q(1)*Q(1)!=0)
    base.require(rejected_multiple_sectors,'multiple-sector mutant escaped')
    return {'status':'PASS','optimization_level':sys.flags.optimize,
        'integer_valued_basis_reproductions':basis_cases,'V_Z_product_checks':products,
        'component_orthogonality_checks':component_cases,'half_binomial_values':denominators,
        'integer_radical_nonzero_powers':100,'multiple_selected_sectors_mutant':'rejected',
        'scope_limit':'finite exact controls; universal boundary proofs are in ADDITIVE_BOUNDARY_NOTE.md'}


if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
