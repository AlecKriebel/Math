#!/usr/bin/env python3
"""Independent full-sn-torus classification checks, separate from ROOT code."""
from collections import Counter
from fractions import Fraction
import json
import math
from pathlib import Path

from check_divisor import Jacobi


def divisor(n,tau,focus_sign):
    # Full sn torus: real coordinates divided by 4K, with p subtracted.
    delta=Fraction(tau,n)
    v=delta/2
    poles=Counter()
    zeros=Counter()
    # g_+ zeros are -K +/-v; g_- zeros are +K +/-v relative to p.
    quarter=-Fraction(focus_sign,4)
    for j in range(n):
        poles.update([(-j*delta)%1,(Fraction(1,2)-j*delta)%1])
        zeros.update([(quarter+v-j*delta)%1,(quarter-v-j*delta)%1])
    return poles,zeros


def main():
    exact_counts={"odd_nonconstant":0,"n_2_mod_4_constant":0,"n_0_mod_4_nonconstant":0}
    for n in range(3,102):
        for tau in range(1,(n+1)//2):
            if math.gcd(tau,n)!=1:
                continue
            for sign in [-1,1]:
                poles,zeros=divisor(n,tau,sign)
                assert sum(poles.values())==2*n==sum(zeros.values())
                assert len(zeros)==n and set(zeros.values())=={2}
                if n%2:
                    assert len(poles)==2*n and set(poles.values())=={1}
                    assert not (poles.keys() & zeros.keys())
                    key="odd_nonconstant"
                elif n%4==2:
                    assert len(poles)==n and set(poles.values())=={2}
                    assert zeros==poles
                    key="n_2_mod_4_constant"
                else:
                    assert len(poles)==n and set(poles.values())=={2}
                    assert not (poles.keys() & zeros.keys())
                    key="n_0_mod_4_nonconstant"
            exact_counts[key]+=1

    # Supplementary real diagnostics across each residue class, including stars.
    numerical=[]
    for k in [0.1,0.7,0.99]:
        J=Jacobi(k)
        for n,tau in [(3,1),(5,2),(7,3),(9,4),(4,1),(8,3),(12,5),
                      (6,1),(10,3),(14,5),(18,7)]:
            delta=4*J.K*tau/n
            _,cv,dv=J.scd(delta/2)
            a=(dv/cv).real
            phases=[0,0.173*J.K,0.317*J.K,0.533*J.K,0.887*J.K]
            values={}
            for sign in [-1,1]:
                vals=[math.prod(1+sign*(k/a)*J.scd(u+j*delta)[0].real
                                for j in range(n)) for u in phases]
                assert min(vals)>0
                spread=max(vals)-min(vals)
                if n%4==2:
                    assert spread<2e-11
                # Check exact repetition behavior directly, not only symbolic.
                for r in [2,3,4]:
                    for u,primitive in zip(phases,vals):
                        repeated=math.prod(1+sign*(k/a)*J.scd(u+j*delta)[0].real
                                           for j in range(r*n))
                        assert abs(repeated-primitive**r)<3e-11
                values["plus" if sign==1 else "minus"]={
                    "normalized_products":vals,"spread":spread,
                    "diagnostic_status":("constant compatible" if n%4==2
                                          else "variation observed" if spread>1e-12
                                          else "variation below float resolution")}
            numerical.append({"k":k,"least_period_n":n,"tau":tau,
                              "expected_constant":n%4==2,"foci":values})
    for residue_class in ["odd","divisible_by_four"]:
        for focus in ["plus","minus"]:
            candidates=[x for x in numerical
                        if (x["least_period_n"]%2==1 if residue_class=="odd"
                            else x["least_period_n"]%4==0)]
            assert any(x["foci"][focus]["spread"]>1e-5 for x in candidates)
    result={"status":"PASS","exact_counts_by_primitive_pair":exact_counts,
            "both_foci_checked":True,"full_sn_lattice_used_for_every_parity":True,
            "numerical_cases":numerical,
            "evidence_status":"Finite Fraction cosets are exact. Theta products are supplementary floating-point diagnostics; the all-period proof is in EXTENSION_REVIEW.md."}
    Path(__file__).with_name("classification_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"PASS","exact_counts_by_primitive_pair":exact_counts,
                      "numerical_cases":len(numerical),"both_foci_checked":True},indent=2))


if __name__=="__main__":
    main()
