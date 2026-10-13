"""Coefficient-Frobenius and polynomial quotient invariants in extension fields.

Dense oracle factorization is only a test oracle for these small cases. This file
checks the Cartier recurrence identity separately from sparse-Pade discovery.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
from finite_fields import (FiniteField,factor,exhaustive_prime_split_oracle,mul,
                          exact_div,polynomial_pth_root,trim)


def power(K,f,e):
    a=(K.one,)
    while e:
        if e&1:a=mul(K,a,f)
        e//=2
        if e:f=mul(K,f,f)
    return a


def inverse_coefficient_frobenius(K,f):
    return trim(K,[K.pow(a,K.p**(K.m-1)) for a in f])


def step(K,U,V):
    uf=factor(K,U,exhaustive_prime_split_oracle)
    vf=factor(K,V,exhaustive_prime_split_oracle)
    AU=(K.one,);AV=(K.one,)
    for g,e in uf.factors:AU=mul(K,AU,power(K,g,e%K.p))
    for g,e in vf.factors:AV=mul(K,AV,power(K,g,e%K.p))
    HU=polynomial_pth_root(K,exact_div(K,U,AU))
    HV=polynomial_pth_root(K,exact_div(K,V,AV))
    W=inverse_coefficient_frobenius(K,AU[::K.p])
    Un=inverse_coefficient_frobenius(K,U[::K.p])
    Vn=mul(K,W,HV)
    assert Un==mul(K,W,HU)
    H=exact_div(K,HU,HV)
    assert exact_div(K,Un,Vn)==H
    F=exact_div(K,U,V)
    # Exact identity F * A_V = A_U * H^p.
    assert mul(K,F,AV)==mul(K,AU,power(K,H,K.p))
    return len(Vn)-1


def run():
    out={'scope':'small extension-field Cartier identity checks; not a proof or novelty certification',
         'fields':{}}
    for p,h,length in [(2,(1,1,1),4),(3,(1,0,1),3)]:
        K=FiniteField(p,h);elements=list(K.elements_for_testing());count=0;maxv=0
        for coefficients in itertools.product(elements,repeat=length):
            if coefficients[0]==K.zero:continue
            U=trim(K,coefficients)
            if not U:continue
            choices=[(K.one,)]
            uf=factor(K,U,exhaustive_prime_split_oracle)
            if uf.factors:choices.append(uf.factors[0][0])
            for V in choices:
                maxv=max(maxv,step(K,U,V));count+=1
        out['fields'][f'F{K.q}_length{length}']={'cases':count,'maximum_next_V_degree':maxv}
    K=FiniteField(2,(1,1,1));alpha=K.element((0,1))
    U=(alpha,K.zero,K.one)
    wrong=(alpha,K.one)
    correct=(K.pow(alpha,2),K.one)
    assert power(K,correct,2)==U
    assert power(K,wrong,2)!=U
    out['inverse_frobenius_omission_counterexample']={
        'field':'F4=F2[a]/(a^2+a+1)','input':'X^2+a',
        'correct_root':'X+a^2','wrong_root_if_coefficients_unchanged':'X+a',
        'wrong_root_square':'X^2+a^2'}
    out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return out

if __name__=='__main__':
    out=run()
    (ROOT/'agent_notes'/'sparse_adversarial_frobenius_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
