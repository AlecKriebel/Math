#!/usr/bin/env python3
"""Check the optional two quintic factors against our chord-derived R, not a candidate import."""
import json
from pathlib import Path
import sympy as s
x,beta=s.symbols('x beta');r=s.sqrt(5)
record=json.loads((Path(__file__).parent/'native/independent_generic_chord_final.stdout').read_text())
co=[s.sympify(a,locals={'beta':beta}) for a in record['Tate_remainder_coefficients']]
R=sum(a*x**(10-j) for j,a in enumerate(co))
Rp=x**5+((beta**2-5*beta+1)/2+r*(-beta**2+11*beta+1)/10)*x**4+(4*beta**2-2*beta+r*(beta**3-11*beta**2-beta)/5)*x**3+((beta**4-7*beta**3+7*beta**2)/2+r*(-beta**4+11*beta**3+beta**2)/10)*x**2+(beta**4-3*beta**3)*x+beta**4
Rm=Rp.xreplace({r:-r})
if s.expand(5*Rp*Rm-R)!=0: raise ValueError('Optional quintic factor coefficients fail')
if s.expand(5*(Rp+1)*Rm-R)==0: raise ValueError('Quintic factor mutant missed')
print(json.dumps({'status':'PASS','sympy_version':s.__version__,'input':'own direct chord/tangent native coefficient record','factor_identity':'5 Rplus Rminus=Rbeta','coefficient_mutant_rejected':True},indent=2))
