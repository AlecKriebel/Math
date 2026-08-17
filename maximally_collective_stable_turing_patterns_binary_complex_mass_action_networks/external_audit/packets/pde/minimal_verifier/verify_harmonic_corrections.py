#!/usr/bin/env python3
import sympy as sp
from common import Avec,selected,cvec,B,w0,w2
for m in [3,4,5,6,8,10]:
 A=Avec(m);r,d,_=selected(m);D=sp.diag(*d);c=cvec(m);rhs=-sp.Rational(1,4)*B(m,r,r)
 W0=w0(m);W2=w2(m)
 assert sp.simplify(A*W0-rhs)==sp.zeros(m+1,1)
 assert sp.factor((c.T*W0)[0])==0
 assert sp.simplify((A-4*D)*W2-rhs)==sp.zeros(m+1,1)
print('HARMONIC_CORRECTIONS_PASS')
