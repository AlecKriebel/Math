#!/usr/bin/env python3
"""Exact finite witnesses and algebraic controls; Python 3 standard library only.
Mathematical witness data: Lena--Sundqvist, arXiv:2609.08774v1, Appendix A.
This checker proves the finite rational inequalities, not the all-domain conjecture
or the external spectral lower bound Theta_0 > 5901/10000.
"""
from fractions import Fraction as F
from math import factorial, comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
COUNT = 0

def check(value, label):
    global COUNT
    if not value:
        raise AssertionError(label)
    COUNT += 1

def beta(a, b):
    return F(factorial(a-1)*factorial(b-1), factorial(a+b-1))

def matrix_integrals(m, c):
    N = K = V = F(0)
    for j, cj in enumerate(c):
        for k, ck in enumerate(c):
            s = j+k
            N += cj*ck*beta(m+1,s+1)/2
            V += cj*ck*beta(m+2,s+1)/8
            K += cj*ck*(m*m*beta(m,s+1)
                -(m*s*beta(m+1,s) if s else 0)
                +(2*j*k*beta(m+2,s-1) if s>1 else 0))
    return N,K,V

def monomial_integrals(m, c):
    # Independent path: expand f(r)=sum d_l r^(m+2l), integrate monomials.
    d = [sum((c[j]*(-1)**l*comb(j,l) for j in range(l,len(c))),F(0))
         for l in range(len(c))]
    N = K = V = F(0)
    for l, dl in enumerate(d):
        for k, dk in enumerate(d):
            p,q = m+2*l,m+2*k
            N += dl*dk/F(p+q+2)
            K += dl*dk*F(p*q+m*m,p+q)
            V += dl*dk/F(4*(p+q+4))
    return N,K,V

def main():
    data=json.loads((ROOT/'witnesses.json').read_text())
    theta=F(data['threshold'])
    t=F(101,100)
    kappa=(t+1/t)/2
    check(kappa==F(20201,20200),'ellipse factor')
    check(kappa/2<theta,'constant trial covers 0<s<=4')
    check(theta<F('0.590106124'),'external certified lower endpoint exceeds threshold')
    rows=sorted(data['witnesses'],key=lambda w:w['interval'][0])
    check(len(rows)==30,'30 source witnesses')
    right=F(3)
    records=[]
    ratios=[]
    for w in rows:
        m=w['m'];c=list(map(F,w['coefficients']));a,b=map(F,w['interval'])
        check(m>=1 and len(c)==9 and c[0]==1,'nonzero admissible polynomial')
        check(a<=right and a<b,'interval coverage')
        right=max(right,b)
        N,K,V=matrix_integrals(m,c)
        check((N,K,V)==monomial_integrals(m,c),'independent integrals')
        check(N>0 and V>0 and K>0,'positive mass and energies')
        rec={'m':m,'interval':[str(a),str(b)],'mass':str(N),'kinetic':str(K),'potential':str(V),'endpoints':[]}
        for ei,s in enumerate((a,b)):
            q=K-m*s*N+s*s*V
            disk=q-theta*s*N
            ellipse=kappa*q-theta*s*N
            check(q>0,'positive magnetic energy')
            check(disk<0,'source disk endpoint witness')
            check(disk==F(w['source_disk_defects'][ei]),'source Table 3 equality')
            check(ellipse<0,'near-circular ellipse endpoint witness')
            ratios.append((q/(s*N),m,s))
            rec['endpoints'].append({'field':str(s),'disk_defect':str(disk),'ellipse_defect':str(ellipse)})
        records.append(rec)
    check(right==131,'coverage reaches 131')
    # Exact first row values independently read from source Table 3.
    check(records[0]['endpoints'][0]['disk_defect']==str(-F(880729,302400000)),'source table first endpoint')
    check(records[0]['endpoints'][1]['disk_defect']==str(-F(6980243,43200000)),'source table second endpoint')
    # Affine-gauge completion of squares at many rational parameters.
    affine_cases=0
    for v1 in (F(1,4),F(2,3),F(7,2)):
        for v2 in (F(1,7),F(5,4),F(8)):
            for field in (F(1,3),F(2),F(9,2)):
                for x in (F(-2),F(0),F(3,5),F(7)):
                    a=field*v1/(v1+v2)+x
                    check(a*a*v2+(field-a)**2*v1==field*field*v1*v2/(v1+v2)+(v1+v2)*x*x,'affine gauge square identity')
                    affine_cases+=1
    # Exact flux-distance inequality d(x,Z)^2/(2x)<=1/4, sampling only controls.
    # The continuum proof is in PROOF.md; these samples are not that proof.
    for den in range(1,16):
        for num in range(1,8*den+1):
            x=F(num,den);m=x.numerator//x.denominator
            dist=min(x-m,m+1-x)
            check(dist*dist/(2*x)<=F(1,4),'thin-annulus flux ratio control')
    maxratio,m,s=max(ratios)
    out={'status':'PASS','assertions':COUNT,'source_witnesses':len(rows),'disk_endpoint_checks':60,'ellipse_endpoint_checks':60,'independent_integral_comparisons':30,'affine_identity_controls':affine_cases,'theta_threshold':str(theta),'ellipse_aspect_max':str(t),'ellipse_kappa_max':str(kappa),'certified_scaled_field':'0 < beta*a*b <= 131','largest_disk_endpoint_ratio':str(maxratio),'largest_ratio_location':{'m':m,'field':str(s)},'smallest_admissible_kappa_at_endpoints':str(theta/maxratio),'external_input':'Theta_0 > 5901/10000 is a cited certified half-line theorem, not recomputed here.','scope':'Finite certificate and stated partial theorems only; original universal problem unresolved.','records':records}
    return out

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
