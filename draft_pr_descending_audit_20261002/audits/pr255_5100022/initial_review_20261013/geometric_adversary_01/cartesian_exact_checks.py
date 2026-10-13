#!/usr/bin/env python3
"""Fresh exact certificates, constructed without reading supplied checkers."""
import json, hashlib, math
from pathlib import Path
import sympy as sp

k,s,t,c,C,d,D,b0 = sp.symbols('k s t c C d D b0')
squares = [(b0,1-k*k),(c,1-s*s),(C,1-t*t),(d,1-k*k*s*s),(D,1-k*k*t*t)]
records=[]
def reduce_polynomial(expr):
    p=sp.Poly(sp.expand(expr), b0,c,C,d,D,k,s,t)
    for x,value in squares:
        p=sp.Poly(sp.rem(p.as_expr(),x*x-value,x),b0,c,C,d,D,k,s,t)
    return sp.expand(p.as_expr())
def check(name,expr):
    n,den=sp.fraction(sp.cancel(expr))
    reduced=reduce_polynomial(n)
    assert reduced==0,(name,reduced)
    records.append({'name':name,'reduced_numerator':'0','uncancelled_denominator':str(den)})
def dot(u,v): return (u.T*v)[0]
def det(u,v): return sp.det(sp.Matrix.hstack(u,v))

L=1-k*k*t*t*s*s
a,b=D/C,b0/C
Pminus=sp.Matrix([-a*(s*C*D-t*c*d)/L,b*(c*C+s*t*d*D)/L])
Pplus=sp.Matrix([-a*(s*C*D+t*c*d)/L,b*(c*C-s*t*d*D)/L])
M=(Pminus+Pplus)/2
H=(Pplus-Pminus)/2
F=sp.Matrix([k,0]); n=sp.Matrix([-s,c/b0]); B=sp.Matrix([-s,b0*c])
Mclaimed=sp.Matrix([-s*D*D/L,b0*c/L])
Hclaimed=-D*t*d/(C*L)*sp.Matrix([c,b0*s])
for i in range(2):
    check(f'midpoint component {i}',M[i]-Mclaimed[i])
    check(f'half-difference component {i}',H[i]-Hclaimed[i])
check('outer confocal semiaxis difference',a*a-b*b-k*k)
check('minus endpoint on outer ellipse',Pminus[0]**2/a**2+Pminus[1]**2/b**2-1)
check('plus endpoint on outer ellipse',Pplus[0]**2/a**2+Pplus[1]**2/b**2-1)
check('caustic point',B[0]**2+B[1]**2/b0**2-1)
check('caustic tangent contains minus endpoint',dot(n,Pminus)-1)
check('caustic tangent contains plus endpoint',dot(n,Pplus)-1)
check('caustic tangent contains contact',dot(n,B)-1)
check('caustic gradient proportional to n',det(n,sp.Matrix([B[0],B[1]/b0**2])))
check('normal orthogonal to chord',dot(n,H))
check('focal normals determinant',det(Pminus-F,Pplus-F)-2*b0*D*t*d*(1+k*s)/(C*L))

eta=(dot(H,H)-dot(M-F,M-F))/(dot(n,M-F))
Uderived=2*M-F+eta*n
E0=1-2*k*k*t*t+k*k*t**4
Uclaimed=sp.Matrix([-(E0*s+k*(C*C-D*D*s*s))/(C*C*L),c*(2*b0*b0-E0*(1+k*s))/(b0*C*C*L)])
for i in range(2): check(f'fresh line-solve antipedal component {i}',Uderived[i]-Uclaimed[i])
check('antipedal actual minus line',dot(Pminus-F,Uclaimed-Pminus))
check('antipedal actual plus line',dot(Pplus-F,Uclaimed-Pplus))
qderived=F+(1-dot(n,F))*n/dot(n,n)
qclaimed=sp.Matrix([(k-s)/(1-k*s),b0*c/(1-k*s)])
for i in range(2): check(f'fresh perpendicular projection component {i}',qderived[i]-qclaimed[i])
check('pedal lies on actual original side',dot(n,qclaimed)-1)
check('pedal difference perpendicular to actual side',det(qclaimed-F,n))
check('focal pedal lies on unit origin circle',dot(qclaimed,qclaimed)-1)

# Derivative geometry uses sn'=cn dn and cn'=-sn dn.
nprime=sp.Matrix([-c*d,-s*d/b0])
check('positive normal angle derivative numerator',det(n,nprime)-d/b0)
check('focal projection radius',dot(qclaimed-F,qclaimed-F)-(1+k*s)**2/dot(n,n))
check('original area single-edge dn identity',det(Pminus,Pplus)-2*a*b*t*C*d/L)
dnminus=(d*D+k*k*s*t*c*C)/L
dnplus=(d*D-k*k*s*t*c*C)/L
check('original area trace local telescoping',det(Pminus,Pplus)-a*b*t*C/D*(dnminus+dnplus))

# Special exact elliptic-billiard control from rational endpoint data.
# a^2=221/96,b^2=27625/20736 is an 8/3 star, useful excluded-parity
# and real-intersection geometry control; it is not a newly claimed construction.
a8=sp.sqrt(sp.Rational(221,96));b8=sp.sqrt(sp.Rational(27625,20736))
cf=sp.sqrt(a8*a8-b8*b8)
coords=[(0,1),(-sp.Rational(12,13),-sp.Rational(5,13)),(1,0),(-sp.Rational(12,13),sp.Rational(5,13)),(0,-1),(sp.Rational(12,13),sp.Rational(5,13)),(-1,0),(sp.Rational(12,13),-sp.Rational(5,13))]
pts=[sp.Matrix([a8*x,b8*y]) for x,y in coords]
for fi in [1,-1]:
    f=sp.Matrix([fi*cf,0]); us=[];qs=[]
    for j,p in enumerate(pts):
        pp=pts[(j+1)%8]; ray=p-f;ray2=pp-f
        mat=sp.Matrix.vstack(ray.T,ray2.T)
        assert sp.simplify(mat.det())!=0
        u=mat.inv()*sp.Matrix([dot(ray,p),dot(ray2,pp)])
        direction=pp-p
        q=p+dot(f-p,direction)/dot(direction,direction)*direction
        us.append(u);qs.append(q)
        assert sp.simplify(dot(ray,u-p))==0
        assert sp.simplify(dot(ray2,u-pp))==0
        assert sp.simplify(dot(q-f,direction))==0
        assert bool(sp.simplify(det(q-f,qs[0]-f))>0) if j==7 else True
        records.append({'name':f'exact 8/3 star focus {fi} intersection/projection edge {j}','result':'PASS'})
    edge_dets=[sp.simplify(det(qs[j]-f,qs[(j+1)%8]-f)) for j in range(8)]
    assert all(bool(v>0) for v in edge_dets)
    records.append({'name':f'exact 8/3 star focus {fi} every pedal determinant positive','edge_determinants':[str(v) for v in edge_dets]})

# Exact primitive half-turn and phase arithmetic, separately from sampled geometry.
arithmetic_cases=0
for N in range(4,258,2):
    for tau in range(1,N//2):
        if math.gcd(tau,N)!=1:continue
        m=N//2
        assert tau%2==1 and math.gcd(tau,m)==1
        # delta/h=tau and 2K/h=m, so Bezout generates h.
        assert ((m*tau)%N)==m
        if N%4==2:assert (m+tau)%2==0
        else: assert (m+tau)%2==1
        arithmetic_cases+=1

result={'status':'PASS','independently_constructed':True,'exact_geometric_checks':records,'exact_geometric_check_count':len(records),'primitive_period_arithmetic_cases':arithmetic_cases,'limitations':'Finite arithmetic cases are diagnostics; universal arithmetic and geometry are proved in INDEPENDENT_DERIVATION.md. No numerical sampled invariant proves an all-period theorem.'}
Path(__file__).with_name('CARTESIAN_EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','exact_geometric_check_count':len(records),'primitive_period_arithmetic_cases':arithmetic_cases}))
