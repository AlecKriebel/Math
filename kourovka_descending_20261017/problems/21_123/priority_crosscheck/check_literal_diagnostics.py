#!/usr/bin/env python3
"""Independently reproduce diagnostics already present in Fraga's prior preprint.

These are not new solutions, and do not disprove the corrected group law.
"""
from pathlib import Path
from datetime import datetime, timezone
import json


class Undefined(Exception):
    pass


def vp_factorial(n, p):
    out = 0
    while n:
        n //= p
        out += n
    return out


def zero_ring_example(p):
    modulus = p * p
    def d(x):
        x %= modulus
        if x % p:
            raise Undefined
        return p if x == 0 else x // p
    assert all(p * d(x) % modulus == x for x in range(0, modulus, p))
    assert d(0) == p and d(d(0)) == 1
    try:
        d(d(d(0)))
    except Undefined:
        pass
    else:
        raise AssertionError('third section iterate must be undefined')
    m = (p - 1) // 4
    degree = 3*p
    s = vp_factorial(degree, p)
    eta = m*s
    assert s == 3 and eta >= 2
    # Zero pre-Lie product: every product of two or more entries is zero.
    # Thus the innermost unit iterate of length eta is zero, yet d^3(0) fails.
    return {'p': p, 'additive_modulus': modulus, 'product': 'zero',
            'Property3': 'holds because m>=2 and all products vanish',
            'degree': degree, 'vp_factorial': s, 'eta': eta,
            'section_iterates_on_zero': [0, p, 1, 'undefined'],
            'corrected_protected_value': 0}


def movement_example():
    p = 11
    modulus = 121
    def d(x):
        x %= modulus
        if x % p:
            raise Undefined
        return 22 if x == 0 else x//p
    L = lambda x: 11*x % modulus
    assert all(p*d(x) % modulus == x for x in range(0,modulus,p))
    lhs, rhs = L(d(11)), d(L(11))
    assert lhs == 11 and rhs == 22 and lhs != rhs
    assert vp_factorial(1,p) == 0
    # The accepted manuscript has a changed, longer shielding condition; do not
    # claim this counterexample refutes that changed Remark22.
    return {'p': p, 'product': 'x*y=11xy mod121', 'source': 'arXivv2 Remark63 only',
            'source_eta_1': 0, 'source_i': 1, 'source_r': 1, 'source_b': 11,
            'left': lhs, 'right': rhs,
            'accepted_Remark22_refuted': False}


def index_table():
    p = 11
    m = (p - 1)//4
    out=[]
    for j in [1,10,11,12,22,33,121]:
        s=vp_factorial(j,p)
        out.append({'j':j,'s_j':s,'eta_j':m*s,'eta_subscript_s_j':m*vp_factorial(s,p),
                    'requires_p_division_for_factorial':bool(s),
                    'j_divisible_by_p':j%p==0,
                    'printed_no_p_branch_says_s_j_zero':j%p!=0,
                    'printed_branch_consistent':j%p==0 or s==0})
    assert not out[3]['printed_branch_consistent']
    return out


def accepted_literal_control():
    # Supplied by root and independently verified here; same previously known
    # section-domain mechanism, not a novel theorem or corrected-law failure.
    p=11
    def d(x):
        if x % p != 0:
            raise Undefined
        return 1
    assert p*d(0) % p == 0
    assert d(0) == 1
    try:
        d(d(0))
    except Undefined:
        pass
    else:
        raise AssertionError('accepted literal second section is undefined')
    j=22
    s=vp_factorial(j,p)
    m=(p-1)//4
    eta=m*s
    assert j%p==0 and s==2 and eta==4
    return {'source':'accepted Definition19 operator on A',
            'ring':'F11 with zero product', 'Property3':'holds, m=2',
            'section':'domain pA={0}, d(0)=1', 'j':j,'s_j':s,'eta_j':eta,
            'literal_term':'L^18 d^2 L^4(b)',
            'inner_operator_value':0,'first_section_value':1,'second_section':'undefined',
            'provenance':'root supplied control independently checked here',
            'new_solution_claim':False,'corrected_group_failure':False}


def main():
    out={'utc':datetime.now(timezone.utc).isoformat(),
         'scope':'Reproduction of prior literal diagnostics and version distinctions only; no new mathematical result.',
         'zero_ring_prior_examples':[zero_ring_example(p) for p in [11,13,17,19,23]],
         'prior_movement_counterexample':movement_example(),
         'factorial_index_controls':index_table(),
         'accepted_literal_control':accepted_literal_control(),
         'p5_p7_boundary':'m=1 makes first Property3 clause A subset pA; finite p-group then A=0',
         'corrected_group_law_disproved':False}
    Path(__file__).with_name('literal_diagnostic_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'result':'PASS','prior_zero_ring_cases':5,'prior_movement_counterexample':'reproduced','new_solution_claim':False}))


if __name__=='__main__':
    main()
