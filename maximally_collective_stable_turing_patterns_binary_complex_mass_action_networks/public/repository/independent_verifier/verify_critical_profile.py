#!/usr/bin/env python3
import sympy as sp
from common import Avec,selected,Hsum,ellr_formula,ellDr_formula
for m in [3,4,5,6,8,10]:
 A=Avec(m);r,d,ell=selected(m);D=sp.diag(*d)
 assert sp.simplify((A-D)*r)==sp.zeros(m+1,1)
 assert sp.simplify((A-D).T*ell)==sp.zeros(m+1,1)
 H=Hsum(m)
 assert sp.factor((ell.T*r)[0]-ellr_formula(m,H))==0
 assert sp.factor((ell.T*D*r)[0]-ellDr_formula(m,H))==0
 assert (ell.T*r)[0]<0 and (ell.T*D*r)[0]<0
print('CRITICAL_PROFILE_PASS')
