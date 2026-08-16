#!/usr/bin/env python3
"""Generate the machine-readable all-m proof certificate."""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
from closed_form import (
    qpoly,cubic_lower_polynomial,ell_r_upper_polynomial,
)

m=sp.symbols('m');u=sp.symbols('u')
A5=(
sp.Integer(86392373709756938206702324880)*m**5
-sp.Integer(878316832027584429913234554493)*m**4
+sp.Integer(3570576759617470240582317330966)*m**3
-sp.Integer(7255203323904441261456947317999)*m**2
+sp.Integer(7368642295819384535817788489606)*m
-sp.Integer(2992572008943165191299483794816))
B4=(
sp.Integer(892292533383541579520)*m**4
-sp.Integer(7159841249775619992477)*m**3
+sp.Integer(21539344009097108736900)*m**2
-sp.Integer(28792766432259158176231)*m
+sp.Integer(14430205416389750108352))

def coeffs(p):
    q=sp.Poly(sp.expand(p.subs(m,u+3)),u)
    return [str(q.coeff_monomial(u**k)) for k in range(q.degree(),-1,-1)]

obj={
 "family":"Nhat_m",
 "dimension":"m>=3",
 "seed":{"a":"1","b":"1","H":"I","u":"7/3","v":"1/32","p":"11/16","q":"1/40"},
 "shifted_positive_polynomials":{
   "Q_m":coeffs(qpoly(m)),
   "A5_m":coeffs(A5),
   "B4_m":coeffs(B4),
   "ell_r_bound_m":coeffs(ell_r_upper_polynomial(m)),
   "cubic_lower_m":coeffs(cubic_lower_polynomial(m)),
 },
 "harmonic_sum":{"definition":"sum_{j=2}^{m-2} 1/(227m-451-3j)","upper_bound":"(m-3)/(224m-445)"},
 "finite_regressions":[3,4,5,6,8,10],
 "m3":{"eta":"110895887/1051840297","c":"-140491463269357313/2273342938789442560"}
}
out=Path(__file__).resolve().parents[1]/'nonlinear'/'all_m_normal_form_certificate.json'
out.write_text(json.dumps(obj,indent=2)+'\n')
print(out)
