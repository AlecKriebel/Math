#!/usr/bin/env python3
import sys
if sys.flags.optimize:
    raise SystemExit("Verification refuses Python optimization (-O/-OO).")
"""Portable exact content/primitivity check. Requires SymPy 1.14.0; no network."""

def main():
    from datetime import datetime,timezone
    import sys
    print("native_utc_start",datetime.now(timezone.utc).isoformat(),flush=True)
    import sympy as S
    print("sympy",S.__version__,flush=True)
    X,Y,T,L=S.symbols("X Y T L")
    r=S.sqrt(5);phi=(1+r)/2
    K=S.QQ.algebraic_field(r)
    R=K.frac_field(X,Y,T,L)
    checks=0
    def canon(expr):return R.to_sympy(R.from_sympy(expr))
    def equal(label,a,b=0):
     nonlocal checks
     assert R.from_sympy(a-b)==R.zero,(label,canon(a-b))
     checks+=1
     print("PASS",label,flush=True)
    def gcd_coeffs(coeffs):
     polys=[S.Poly(c,X,domain=K) for c in coeffs]
     value=polys[0]
     for p in polys[1:]:value=S.gcd(value,p)
     return value.monic()
    # Reconstructed product of the five regular-pentagon side equations.
    P=2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*phi*(X*X+Y*Y)**2*T-5*phi**3*(X*X+Y*Y)*T**3+phi**5*T**5
    Ph=P+L*T*(X*X+Y*Y-T*T)**2
    G=S.Poly(S.expand(Ph.subs(T,1)),Y)
    A=G.coeff_monomial(Y**4);B=G.coeff_monomial(Y**2);C=G.coeff_monomial(1)
    H=5*phi+L;X0=-H/10
    print("A",canon(A),"B",canon(B),"C",canon(C),flush=True)
    equal("A_from_side_product",A,10*X+H)
    equal("B_from_side_product",B,-20*X**3+2*H*X*X-5*phi**3-2*L)
    equal("C_from_side_product",C,2*X**5+H*X**4-(5*phi**3+2*L)*X*X+phi**5+L)
    equal("A_unique_root",A.subs(X,X0))
    B0=canon(B.subs(X,X0));C0=canon(C.subs(X,X0))
    Bfactor=L*(L+5*r)*(L+5*(phi+1))/25
    equal("B_at_Aroot_factorization",B0,Bfactor)
    print("B_at_Aroot_factored",Bfactor,flush=True)
    print("C_at_Aroot",C0,flush=True)
    third=-5*(phi+1)
    equal("sole_allowed_Bzero_Xroot",X0.subs(L,third),S.Rational(1,2))
    equal("sole_allowed_Bzero_B",B0.subs(L,third))
    equal("sole_allowed_Bzero_C_is_minus_one",C0.subs(L,third),-1)
    # Independent resultant-elimination check: no hidden shared-root parameter.
    resB=canon(S.resultant(A,B,X));resC=canon(S.resultant(A,C,X))
    gcdRes=S.gcd(S.Poly(resB,L,domain=K),S.Poly(resC,L,domain=K)).monic()
    equal("gcd_of_content_resultants",gcdRes.as_expr(),L*(L+5*r))
    print("RESULTANT_A_B",S.factor(resB,extension=r),flush=True)
    print("RESULTANT_A_C",S.factor(resC,extension=r),flush=True)
    print("MONIC_RESULTANT_GCD",gcdRes.as_expr(),flush=True)
    # Real bad vertical components at the two excluded finite values.
    for lam,expected_root in [(0,-phi/2),(-5*r,(phi-1)/2)]:
     specialized=[canon(v.subs(L,lam)) for v in (A,B,C)]
     content=gcd_coeffs(specialized)
     equal("excluded_parameter_actual_vertical_content",content.as_expr(),X-expected_root)
     print("BAD_VERTICAL_CONTENT",lam,content.as_expr(),flush=True)
    # Uniform statement includes these concrete boundary specializations.
    for label,lam in [("center_genus_zero",-phi**5),("allowed_cusp",-(25+10*r)/4),("allowed_Bzero",third)]:
     content=gcd_coeffs([canon(v.subs(L,lam)) for v in (A,B,C)])
     equal(label+"_primitive",content.as_expr(),1)
     print("BOUNDARY_CONTENT",label,content.as_expr(),flush=True)
    # False-content control: A=B=0 does not imply all coefficients vanish.
    ABgcd=S.gcd(S.Poly(canon(A.subs(L,third)),X,domain=K),S.Poly(canon(B.subs(L,third)),X,domain=K)).monic()
    equal("false_content_control_AB_have_factor",ABgcd.as_expr(),X-S.Rational(1,2))
    assert gcd_coeffs([canon(v.subs(L,third)) for v in (A,B,C)]).degree()==0
    print("NEGATIVE_CONTROL_REJECTED false_common_content_from_A_and_B_only",flush=True)
    # Inject a real vertical factor into a permitted fibre and demand detection.
    injected=[canon((X-S.Rational(1,2))*v.subs(L,third)) for v in (A,B,C)]
    content_injected=gcd_coeffs(injected)
    equal("injected_content_detected",content_injected.as_expr(),X-S.Rational(1,2))
    assert content_injected.degree()==1
    print("NEGATIVE_CONTROL_REJECTED primitivity_of_injected_vertical_component",flush=True)
    # Projective completion: degree-five homogenization has no T factor.
    equal("exact_degree_five_homogenization",Ph,S.expand(T**5*G.as_expr().subs({X:X/T,Y:Y/T})))
    infinity=S.Poly(S.expand(Ph.subs(T,0)),X,Y,domain=K)
    assert not infinity.is_zero
    assert S.Poly(Ph,T).coeff_monomial(1)!=0
    equal("nonzero_infinity_restriction",infinity.as_expr(),2*X*(X**4-10*X*X*Y*Y+5*Y**4))
    print("INFINITY_RESTRICTION",infinity.as_expr(),flush=True)
    print("PASS no_projective_T_factor",flush=True)
    # Check a pure-T mutation is actually caught by the same necessary test.
    assert S.expand((T*Ph).subs(T,0))==0
    print("NEGATIVE_CONTROL_REJECTED no_T_factor_for_Tmultiplied_polynomial",flush=True)
    print("exact_identity_checks",checks,"status","PASS",flush=True)
    print("native_utc_end",datetime.now(timezone.utc).isoformat(),flush=True)

if __name__ == "__main__":
    main()
