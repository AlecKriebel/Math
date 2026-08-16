#!/usr/bin/env python3
from core import A_matrix,D_seed,r_seed,ell_seed
import sympy as sp
for m in (3,4,5,6,8,10):
 A=A_matrix(m);D=D_seed(m);r=r_seed(m);ell=ell_seed(m)
 assert (A-D)*r==sp.zeros(m+1,1); assert (A-D).T*ell==sp.zeros(m+1,1)
 assert (ell.T*r)[0]!=0 and (ell.T*D*r)[0]!=0
print('PRIMARY_CROSSING_PASS')
