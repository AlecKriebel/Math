#!/usr/bin/env python3
"""Independent exact cancellation controls; stdout only, no source-file edits.
The analytic proof of the general inequality is in REVIEWER_CORRECTION.md.
"""
import json
import sympy as s

# For g=a*z^ell, h=b*z^k, calculate all means and pole terms exactly
# at the rational radius r, using log(max(1, |monomial|)).
# This deliberately includes complete, incomplete and absent cancellation.
checks = 0
counterexample = None
for r in (s.Rational(1,2),s.Rational(3,4),s.Rational(7,8)):
    for ell in range(6):
        for k in range(6):
            for a,b in ((1,2),(2,1),(s.Rational(1,3),2)):
                a,b=s.sympify(a),s.sympify(b)
                p=max(k-ell,0)
                mg=s.log(max(s.S.One,a*r**ell))
                mh=s.log(max(s.S.One,b*r**k))
                mf=s.log(max(s.S.One,(a/b)*r**(ell-k)))
                T=mf+p*s.log(r)
                rhs=mg+mh-s.log(b)+(k-p)*s.log(1/r)
                difference=s.expand_log(rhs-T,force=True)
                # Exact positivity is checked on the rational inside the log.
                quotient=s.simplify(s.exp(difference))
                assert quotient.is_Rational and quotient>=1
                checks+=1
                if r==s.Rational(3,4) and ell==k==1 and a==1 and b==2:
                    uncorrected=s.expand_log(mg+mh-s.log(b),force=True)
                    assert s.simplify(uncorrected-s.log(r))==0
                    assert s.simplify(T)==0 and s.simplify(rhs)==0
                    counterexample={"g":"z","h":"2*z","r":"3/4",
                        "T":"0","uncorrected_rhs":"log(3/4)",
                        "corrected_rhs":"0"}
assert counterexample is not None
print(json.dumps({"status":"pass","exact_monomial_controls":checks,
    "counterexample":counterexample,
    "scope":"finite exact controls only; not formal verification of the analytic proof"},indent=2,sort_keys=True))
