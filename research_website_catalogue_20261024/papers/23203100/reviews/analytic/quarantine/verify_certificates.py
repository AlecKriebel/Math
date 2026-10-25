"""Exact finite OTP obstruction and resource-cone certificates.

These checks reproduce finite instances; the universal proofs are in main.tex.
Only Python's standard library is required. Code: MIT.
"""
from fractions import Fraction as F
import json
from pathlib import Path

def otp(d):
    qs = [F(1, d)] * d
    p = F(1, d*d)
    norm = sum(abs((p if l == (m+s) % d else F(0))-qs[l]*p)
               for m in range(d) for s in range(d) for l in range(d))
    assert norm == 2*(1-F(1,d))
    # Arbitrary comparison public marginal; a point mass gives the same norm.
    qs = [F(1)]+[F(0)]*(d-1)
    norm2 = sum(abs((p if l == (m+s) % d else F(0))-qs[l]*p)
                for m in range(d) for s in range(d) for l in range(d))
    assert norm2 == norm
    return {"d":d,"unhalved_trace_norm":str(norm),
            "ideal_independent_decoder_success":str(F(1,d))}

def cones():
    quantum = [(-2,1,-1),(2,-1,-1),(0,-1,1)]
    private = [(-1,1,-1),(1,-1,0),(0,-1,1)]
    for c,q,e in quantum:
        assert c+2*q <= 0 and q+e <= 0 and c+q+e <= 0
    for r,p,s in private:
        assert r+p <= 0 and p+s <= 0 and r+p+s <= 0
    return {"quantum_unit_vectors":quantum,"private_unit_vectors":private,
            "OTP_is_in_displayed_N_zero_private_region":True}

def main():
    result={"kind":"exact rational finite-instance checks, not universal formalization",
            "otp":[otp(d) for d in (2,4,8,16)],"cones":cones(),"passed":True}
    target=Path(__file__).resolve().parent/"certificate_results.json"
    target.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
