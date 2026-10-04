#!/usr/bin/env python3
"""Standard-library exact polynomial coefficient and endpoint controls."""
from fractions import Fraction as F
import itertools,json

def add(a,b):
    out=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a):out[i]+=x
    for i,x in enumerate(b):out[i]+=x
    return out

def mul(a,b,degree=None):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out if degree is None else out[:degree+1]

def scale(a,k):return [k*x for x in a]

def verify():
    # x=1/M. The z^2,z^3 coefficients in F/(1-xF)^2=k(z).
    A2=[F(2),F(-2)];A3=[F(3),F(-8),F(5)];x=[F(0),F(1)]
    assert add(A2,scale(x,2))==[F(2),F(0)]
    assert add(add(A3,scale(mul(x,A2),4)),[F(0),F(0),F(3)])==[F(3),F(0),F(0)]
    # Difference of the Pick and square-root competitor coefficients.
    assert add(A3,[F(-1),F(0),F(1)])==[F(2),F(-8),F(6)]
    assert mul([F(2),F(-2)],[F(1),F(-3)])==[F(2),F(-8),F(6)]
    assert add(A2,scale(A3,-1))==[F(-1),F(6),F(-5)]
    assert mul([F(-1),F(1)],[F(1),F(-5)])==[F(-1),F(6),F(-5)]
    # p^2*(1-2az+z²)*(1-2cz+z²)=(1-2bz+z²)^2 through z².
    # These residual coefficients have degree <=4 in EACH of a,b,c.
    # Vanishing on the full five-by-five-by-five tensor grid proves the
    # polynomial identities, by successive univariate root counting.
    count=0
    for a,b,c in itertools.product(map(F,range(-2,3)),repeat=3):
        S=a+c;q1=S-2*b;q2=F(3,2)*S*S-2*b*S-2*a*c
        den=mul([F(1),-2*a,F(1)],[F(1),-2*c,F(1)],2)
        lhs=mul(mul([F(1),q1,q2],[F(1),q1,q2],2),den,2)
        rhs=mul([F(1),-2*b,F(1)],[F(1),-2*b,F(1)],2)
        assert lhs==rhs;count+=1
    for M in [F(3),F(5),F(10)]:
        r=1/M;pick=3-8*r+5*r*r;odd=1-r*r
        assert (M!=3 or pick==odd==F(8,9))
        assert (M!=5 or pick==F(8,5))
    return {'arithmetic':'exact Python Fraction','Pick_coefficients':True,'endpoint_differences':True,'slit_identity_tensor_grid':count,'tensor_grid_proves_polynomial_identity':True,'M3_and_M5_controls':True,'limits':'Algebraic identities only. No global analytic optimization is encoded.'}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
