"""Replay mechanism mutations against independent acceptance checks.

No author modules or verifier read. The frozen first-seal controls are imported
only to reuse independently authored endpoint/cube primitives. Assertions are
not used; python -O must have the same rejection behavior.
"""
from itertools import product
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import sys

spec=importlib.util.spec_from_file_location('sealed_independent',
    Path(__file__).with_name('independent_controls.py'))
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def real_compile(n, choices):
    return (1,)*(2*n) + tuple(unit for choice in choices for unit in (1,choice))


def validate_resolution(n, choices, compiler):
    word=compiler(n, choices)
    info=base.diagram(word)
    base.require(info['components']==2, 'wrong closure-component count')
    normal,_=base.cancellation_normal_form(word)
    expected_n=n+choices.count(1)
    base.require(normal==(1,)*(2*expected_n), 'wrong RII reduction/family member')
    base.require(sum(info['linking'].values())==expected_n, 'wrong mixed-crossing number')
    base.require(not info['self_writhe'], 'unexpected self crossing/framing change')


def test_compiler(name, compiler, expect_pass):
    checked=0
    for n in range(3):
        for r in range(1,5):
            for choices in product((-1,1),repeat=r):
                checked+=1
                try:
                    validate_resolution(n, choices, compiler)
                except base.Failure as error:
                    base.require(not expect_pass, 'baseline rejected')
                    return {'name':name, 'outcome':'rejected', 'cases_before_rejection':checked,
                            'witness':{'n':n,'choices':list(choices),'word':list(compiler(n,choices)),
                                       'reason':str(error)}}
    base.require(expect_pass, 'mutant escaped: '+name)
    return {'name':name,'outcome':'PASS','cases':checked}


def cube_product_tests():
    count=0
    for a in range(32):
        for b in range(32):
            av=[Q(int(mask&a==a)) for mask in range(32)]
            bv=[Q(int(mask&b==b)) for mask in range(32)]
            values=[x*y for x,y in zip(av,bv)]
            coefficients=base.cube_coefficients(values,5)
            union=a|b
            base.require(all(c==Q(int(i==union)) for i,c in enumerate(coefficients)),
                         'Boolean product did not have union support')
            base.require(union.bit_count()<=a.bit_count()+b.bit_count(), 'product order bound')
            count+=1
    # Non-monomial rational coefficients ensure overlap and cancellation cases.
    coefficients_a=[Q((-1)**m*(m+1),m+2) if m.bit_count()<=2 else Q(0) for m in range(32)]
    coefficients_b=[Q(m-7,m+3) if m.bit_count()<=1 else Q(0) for m in range(32)]
    av=[base.evaluate_cube(coefficients_a,m) for m in range(32)]
    bv=[base.evaluate_cube(coefficients_b,m) for m in range(32)]
    pv=[x*y for x,y in zip(av,bv)]
    pc=base.cube_coefficients(pv,5)
    base.require(all(c==0 for m,c in enumerate(pc) if m.bit_count()>3), 'generic product order')
    base.require(base.finite_difference([Q(4*n**4-n*n) for n in range(5)],4)==96,
                 'quartic sharp order control')
    return {'monomial_pairs':count,'generic_rational_product':'PASS','quartic_fourth_difference':'96'}


def main():
    compiler_cases=[('baseline',real_compile,True),
        ('deleted_companion',lambda n,c:(1,)*(2*n)+tuple(c),False),
        ('smoothed_negative_branch',lambda n,c:(1,)*(2*n)+tuple(u for s in c for u in ((1,1) if s==1 else (1,))),False),
        ('odd_prefix',lambda n,c:(1,)+real_compile(n,c),False),
        ('positive_negative_sign_mistranscription',lambda n,c:real_compile(n,tuple(1 for s in c)),False),
        ('shared_physical_site',lambda n,c:real_compile(n,(c[0],)),False)]
    return {'status':'PASS','optimization_level':sys.flags.optimize,
            'compiler_replays':[test_compiler(*case) for case in compiler_cases],
            'product_controls':cube_product_tests(),
            'limitations':'exact finite mechanism replays; universal proof is in FIRST_ASSESSMENT.md'}


if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
