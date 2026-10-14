#!/usr/bin/env python3
"""Finite local identities in family029; numerical checks, not zero-free proof.
Uses exact integer residue indexing and standard Python complex arithmetic.
Reproduce: python3 agent_notes/analytic_audit_local_checks.py
"""
import cmath
import json
import math


def primitive_root(p):
    for g in range(2, p):
        vals = {pow(g, j, p) for j in range(p-1)}
        if len(vals) == p-1:
            return g
    raise ValueError(p)


def character(p):
    g = primitive_root(p)
    log = {pow(g, j, p): j for j in range(p-1)}
    def chi(x, exponent=1):
        x %= p
        return 0j if x == 0 else cmath.exp(2j*math.pi*(log[x]*exponent % 6)/6)
    return chi


def check_phases(p):
    chi = character(p)
    psi = lambda x: cmath.exp(2j*math.pi*(x % p)/p)
    gamma = {j: sum(chi(x,j)*psi(x) for x in range(p))/math.sqrt(p)
             for j in [1,2,3,4,5]}
    jacobi = sum(chi(x,2)*chi(1-x,2) for x in range(p))
    equations = {
        "cubic_gauss_jacobi": (gamma[2]**3, jacobi/math.sqrt(p)),
        "sextic_duplication": (gamma[1]*gamma[2],
                              chi(4,-1)*gamma[3]*gamma[2]**3),
        "gauss_inversion": (gamma[2]*gamma[4], 1),
        "quadratic_sign": (gamma[3]**2, 1),
    }
    errors = {name: abs(a-b) for name,(a,b) in equations.items()}
    assert max(errors.values()) < 1e-10, (p, errors)
    return {"p":p, "max_error":max(errors.values()), "identities":len(errors)}


def check_quadratic_residue_extension(p, nonsquare):
    # F_(p^2)=F_p[z]/(z^2-nonsquare). Order-six character is norm lift.
    assert pow(nonsquare, (p-1)//2, p) == p-1
    chi = character(p)
    elements=[(a,b) for a in range(p) for b in range(p)]
    norm=lambda x:(x[0]*x[0]-nonsquare*x[1]*x[1])%p
    char=lambda x,j:chi(norm(x),j)
    addchar=lambda x:cmath.exp(2j*math.pi*((2*x[0])%p)/p)
    gam={j:sum(char(x,j)*addchar(x) for x in elements)/p for j in [1,2,3,4]}
    jac=sum(char(x,2)*char(((1-x[0])%p,(-x[1])%p),2) for x in elements)
    basejac=sum(chi(x,2)*chi(1-x,2) for x in range(p))
    equations={
      "cubic_gauss_jacobi":(gam[2]**3,jac/p),
      "sextic_duplication":(gam[1]*gam[2],chi(16,-1)*gam[3]*gam[2]**3),
      "jacobi_lifting":(jac,-basejac**2),
      "gauss_inversion":(gam[2]*gam[4],1),
    }
    errors={k:abs(a-b) for k,(a,b) in equations.items()}
    assert max(errors.values()) < 1e-10, errors
    return {"field_size":p*p,"modulus":f"z^2-{nonsquare}","identities":len(errors),"max_error":max(errors.values())}


def check_C_values(p):
    # For t,k>0, the two residue sums in family029 (C-local-definition).
    # A unit mask is retained even when a character exponent is 0 mod 6.
    chi = character(p)
    T = lambda v,y: sum(chi(x,v)*cmath.exp(2j*math.pi*(y*x % p)/p) for x in range(p))
    tau1 = T(1,1)
    count, max_error = 0, 0.0
    for t in range(1,3):
        for k in range(4):
            for J in range(7):
                modulus = p**(k+t)
                total = 0j
                for d in range(p**k):
                    if (p**J-p**t*d) % (p**k):
                        continue
                    cd = 1 if k == 0 else chi(d,k)
                    if cd == 0:
                        continue
                    for v in range(p**t):
                        cv = chi(v,t)
                        if cv:
                            phase = ((p**J-p**t*d)*v) % modulus
                            total += cd*cv*cmath.exp(2j*math.pi*phase/modulus)
                if k == 0:
                    expected = p**(t-1)*T(t,p**(J-t+1)) if J >= t-1 else 0
                elif k == 1:
                    expected = tau1*p**(t-1)*T(t-1,p**(J-t)) if J >= t else 0
                else:
                    expected = 0
                err=abs(total-expected)
                max_error=max(max_error,err)
                assert err < 1e-8, (p,t,k,J,total,expected,err)
                count+=1
    return {"p":p,"cases":count,"max_error":max_error}


def check_margins():
    from fractions import Fraction as Q
    C=Q(7,15)
    margins={
      "reflection":Q(933,2000)-C,
      "principal_Rw":Q(11,10)*Q(1,10000000)-Q(5,100)*Q(133,1000),
      "principal_Rz":Q(1,10000000)+Q(1,10)*(Q(16,100)-Q(1,6)),
      "low_rows":Q(1,10000000)+Q(7,300)-Q(132601,1000000)+Q(9,100)*Q(11,10),
      "good_rows":-Q(2,1000)+Q(7,300)-Q(132601,1000000)+Q(10001,100000)*Q(11,10),
      "far_rows":Q(44901,100000)-C,
    }
    assert all(x < 0 for x in margins.values())
    assert margins["reflection"] == -Q(1,6000)
    assert margins["good_rows"] == -Q(377,300000)
    return {k:str(v) for k,v in margins.items()}

if __name__ == "__main__":
    print(json.dumps({
      "scope":"finite numerical local checks; no analytic theorem certified",
      "phase_checks":[check_phases(p) for p in [13,37,61,73]],
      "residue_extension_checks":[check_quadratic_residue_extension(13,2)],
      "C_value_checks":[check_C_values(13)],
      "exact_margin_checks":check_margins(),
    }, indent=2))
