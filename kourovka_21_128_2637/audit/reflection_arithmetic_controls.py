"""Independent exact Coxeter representation, torsion weights and Euler controls."""
import sympy as S
from fractions import Fraction as F
from math import lcm, gcd, prod
from pathlib import Path
import json
out={}
for name,labels,h,exponents,weights,n,periodic in [
 ('F4',[3,4,3],12,[1,5,7,11],[1,1,0,0],12,[[0,1,2,3],[0,1,2,3,1,2]]),
 ('H4',[5,3,3],30,[1,11,19,29],[1,1,1,1],60,[[0,1,2,3],[0,1,0,1,2,3],[0,1,0,1,2,1,0,1,2,3]])]:
    G=S.eye(4)
    for i,m in enumerate(labels): G[i,i+1]=G[i+1,i]=-S.cos(S.pi/m)
    reflections=[]
    for i in range(4):
        R=S.eye(4)
        for j in range(4): R[i,j]-=2*G[i,j]
        reflections.append(R)
    C=prod(reflections,start=S.eye(4))
    C=C.applyfunc(S.simplify)
    power=S.eye(4); minus_i_powers=[]
    for k in range(1,h+1):
        power=(power*C).applyfunc(S.simplify)
        if power==-S.eye(4): minus_i_powers.append(k)
        if k<h: assert power!=S.eye(4)
    assert power==S.eye(4) and minus_i_powers==[h//2]
    t=S.Symbol('t')
    poly=S.Poly(prod(1+e*t for e in exponents[1:]),t)
    chi=int(poly.eval(-1)); order=prod(e+1 for e in exponents)
    values=[sum(weights[i] for i in word) for word in periodic]
    out[name]={'Coxeter_order':h,'minus_identity_powers':minus_i_powers,'decone_poincare_ascending':list(reversed([int(z) for z in poly.all_coeffs()])),'pure_central_quotient_chi':chi,'Coxeter_order_from_degrees':order,'pure_central_quotient_index':order//2,'rational_chi':str(F(chi,order//2)),'periodic_word_weights':values,'periodic_image_orders':[n//gcd(n,w) for w in values],'kernel_chi':str(n*F(chi,order//2))}
valid=[(i,j) for i in range(1,1009) for j in range(1,601) if F(-5,12)*i==F(-7,10)*j and i%12==0 and j%30==0]
assert valid==[(252*k,150*k) for k in range(1,5)]
out['first_four_necessary_torsionfree_pairs']=valid
out['cohomology_transfer_identity']='cor_U^K composed with res_U^K = [K:U] id on H^1(K; Q)'
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
