"""Exact finite falsification controls for the self-contained proof.
These controls do not prove the universal theorem.
"""
from fractions import Fraction as Q
import json
def fibonacci(n):
    a,b=0,1
    for _ in range(n):a,b=b,a+b
    return a
offsets=0; terminal=0; lattice_coordinates=0
for n in range(3,23):
    q,p=fibonacci(n),fibonacci(n-1)
    for m in range(1,q):
        j=2
        while fibonacci(j+1)<=m:j+=1
        a,b,c=fibonacci(j),fibonacci(j-1),fibonacci(j+1)
        determinant=a*a-b*c
        assert determinant==(-1)**(j-1)
        h=n-j;A,B=fibonacci(h),fibonacci(h-1)
        assert p*a-q*b==(-1)**(j-1)*A
        assert p*c-q*a==(-1)**j*B
        assert q==a*fibonacci(h+1)+b*A and q<=3*a*A
        nearest=(m*p)//q
        for ell in (nearest,nearest+1,nearest-2,nearest+3):
            S=(a*m-c*ell)//determinant
            T=(a*ell-b*m)//determinant
            assert (m,ell)==(S*a+T*c,S*b+T*a)
            assert S!=0 and (T==0 and S>0 or S*T<0)
            r=m*p-ell*q
            assert abs(r)==abs(S*A-T*B) and abs(r)>=A
            assert 3*m*abs(r)>=q
            lattice_coordinates+=1
        terminal+=h==1;offsets+=1
geometry_cases=0
for a,b in [(Q(0),Q(1,2)),(Q(1,10),Q(4,5)),(Q(2,7),Q(6,7)),(Q(1,3),Q(2,3))]:
    d=b-a;U=2*(a+b-2*a*b);V2=16*a*(1-a)*b*(1-b)
    assert U-2*d==4*a*(1-b) and V2==U*U-4*d*d and U>=2*d
    for c in (Q(-1),Q(0),Q(1,5),Q(3,5),Q(4,5)):
        # Polynomial identity underlying the irrational-square-root bound:
        # (U-cV)^2-4d^2(1-c^2)=(V-cU)^2, using V^2=V2.
        assert U*U+c*c*V2-4*d*d*(1-c*c)==V2+c*c*U*U
        geometry_cases+=1
print(json.dumps({'status':'PASS','arithmetic_n':'3..22','offsets':offsets,'integer_lattice_coordinates':lattice_coordinates,'terminal_h1_offsets':terminal,'rational_geometry_cases':geometry_cases,'scope':'Finite exact recurrence, basis, sign, residue and metric-identity controls; not an infinite proof'},sort_keys=True))
