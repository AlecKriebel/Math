#!/usr/bin/env python3
"""Exact direct-geometry controls; no floating tolerances or assert statements.
Run using the prescribed Python with -B, also with -O. No universal theorem
is inferred from these finite controls. Writes only CHECK_RESULTS.json here.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

BASE=Path(__file__).resolve().parent
import sympy as S
if S.__version__ != '1.14.0':
    raise RuntimeError('Expected the authorized read-only SymPy 1.14.0 runtime')

X,Y=S.symbols('X Y',real=True)
R=S.Rational
checks=[]

def require(cond,label):
    if cond is not True and cond is not S.true:
        raise RuntimeError('FAILED: '+label+'; condition='+str(cond))
    checks.append(label)

def eq(a,b,label):
    require(S.simplify(a-b)==0,label)

def cross(a,b):
    return a[0]*b[1]-a[1]*b[0]

def vectors(rows):
    return [S.Matrix(z) for z in rows]

def pairs(P):
    return zip(P,P[1:]+P[:1])

def area(P):
    return S.simplify(sum(cross(a,b) for a,b in pairs(P))/2)

def raw_line(a,b):
    e=b-a
    n=S.Matrix([-e[1],e[0]])
    return n,n.dot(a)

def feet(P,M):
    out=[]
    for a,b in pairs(P):
        n,h=raw_line(a,b)
        out.append(M+(h-n.dot(M))/n.dot(n)*n)
    return out

def coefficients(P,label):
    Q=feet(P,S.Matrix([X,Y]))
    expr=S.expand(sum(cross(a,b) for a,b in pairs(Q))/2)
    poly=S.Poly(expr,X,Y)
    allowed={(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)}
    require(set(poly.monoms())<=allowed,label+': degree at most 2')
    c={k:S.simplify(poly.coeff_monomial(X**k[0]*Y**k[1])) for k in allowed}
    eq(c[(1,1)],0,label+': mixed quadratic term zero')
    eq(c[(2,0)],c[(0,2)],label+': quadratic radiality')
    ns=[raw_line(a,b)[0] for a,b in pairs(P)]
    expected=S.simplify(sum(cross(n,m)*n.dot(m)/(n.dot(n)*m.dot(m)) for n,m in pairs(ns))/4)
    eq(c[(2,0)],expected,label+': exact universal C formula')
    return c

def billiard(P,a2,b2,lam,label):
    require(len({tuple(v) for v in P})==len(P),label+': all vertices distinct')
    require(S.simplify(a2-b2).is_positive is True,label+': noncircular outer ellipse')
    require(S.simplify(lam).is_positive is True,label+': positive lambda')
    require(S.simplify(b2-lam).is_positive is True,label+': proper elliptical caustic')
    Dc=S.diag(a2-lam,b2-lam)
    for i,p in enumerate(P):
        eq(p[0]**2/a2+p[1]**2/b2,1,label+': vertex '+str(i)+' on ellipse')
        q=P[(i+1)%len(P)]
        n,h=raw_line(p,q)
        require(S.simplify(n.dot(n)).is_positive is True,label+': side '+str(i)+' nondegenerate')
        eq(h**2-(n.T*Dc*n)[0],0,label+': side '+str(i)+' tangent confocal')
        v_in=p-P[i-1]
        v_out=q-p
        v_in=v_in/S.sqrt(v_in.dot(v_in))
        v_out=v_out/S.sqrt(v_out.dot(v_out))
        N=S.Matrix([p[0]/a2,p[1]/b2])
        eq(cross(v_in-v_out,N),0,label+': reflection '+str(i))
        require(S.simplify((v_in-v_out).dot(N)).is_positive is True,label+': physical reflection sign '+str(i))
    return coefficients(P,label)

# A nonsymmetric rational star checks the universal theorem without symmetry.
G=vectors([(0,0),(4,1),(-1,3),(3,-2),(-2,-1)])
g=coefficients(G,'arbitrary nonsymmetric star')
require(g[(1,0)]!=0 or g[(0,1)]!=0,'arbitrary star genuinely has a linear term')

# Two distinct primitive physical 4-orbit phases for E=(2,1), lambda=4/5.
D=vectors([(2,0),(0,1),(-2,0),(0,-1)])
T=vectors([(4/S.sqrt(5),1/S.sqrt(5)),(-4/S.sqrt(5),1/S.sqrt(5)),(-4/S.sqrt(5),-1/S.sqrt(5)),(4/S.sqrt(5),-1/S.sqrt(5))])
for tag,P in [('4 diamond',D),('4 rectangle',T)]:
    c=billiard(P,S.Integer(4),S.Integer(1),R(4,5),tag)
    eq(c[(1,0)],0,tag+': centered linear x')
    eq(c[(0,1)],0,tag+': centered linear y')
    eq(c[(2,0)],0,tag+': C zero')
    eq(area(P)*c[(0,0)],R(128,25),tag+': exact product')

# A genuine Poncelet pair that is nonconfocal; target extension fails.
N0=D
N1=vectors([(S.sqrt(2),1/S.sqrt(2)),(-S.sqrt(2),1/S.sqrt(2)),(-S.sqrt(2),-1/S.sqrt(2)),(S.sqrt(2),-1/S.sqrt(2))])
for tag,P in [('nonconfocal phase 0',N0),('nonconfocal phase 1',N1)]:
    for i,(a,b) in enumerate(pairs(P)):
        n,h=raw_line(a,b)
        eq(h*h-(n.T*S.diag(2,R(1,2))*n)[0],0,tag+': homothetic tangency '+str(i))
c0=coefficients(N0,'nonconfocal phase 0')
c1=coefficients(N1,'nonconfocal phase 1')
eq(area(N0)*c0[(0,0)],R(128,25),'nonconfocal product phase 0')
eq(area(N1)*c1[(0,0)],8,'nonconfocal product phase 1')
require(R(128,25)!=8,'nonconfocal products differ exactly')

# Same physical primitive 3-family, repeated four times to make list length 12.
r=S.sqrt(13);w=S.sqrt(2*r-5)/3
U=vectors([(2,0),(2*(1-r)/3,w),(2*(1-r)/3,-w)])
V=vectors([(0,1),(-4*w,(r-4)/3),(4*w,(r-4)/3)])
lam3=4*(2*r-5)/9
cu=billiard(U,S.Integer(4),S.Integer(1),lam3,'3 phase x')
cv=billiard(V,S.Integer(4),S.Integer(1),lam3,'3 phase y')
Au=area(U);Av=area(V)
Pu=S.simplify(Au*(cu[(0,0)]+cu[(1,0)]+cu[(2,0)]))
Pv=S.simplify(Av*(cv[(0,0)]+cv[(1,0)]+cv[(2,0)]))
eq(Pu,(11936-3176*r)/729,'3 phase x product at M=(1,0)')
eq(Pv,(67312-18544*r)/729,'3 phase y product at M=(1,0)')
diff3=S.simplify(Pu-Pv)
eq(diff3,(-55376+15368*r)/729,'3 product difference exact')
require(diff3!=0,'3 products differ exactly')
for tag,P,c in [('repeat x',U,cu),('repeat y',V,cv)]:
    Q=P*4
    eq(area(Q),4*area(P),tag+': original area scales by 4')
    eq(area(feet(Q,S.Matrix([1,0]))),4*(c[(0,0)]+c[(1,0)]+c[(2,0)]),tag+': pedal area scales by 4')
    require(len(Q)==12,tag+': nominal length divisible by 4')

# Same physical primitive 6-family; shows false all-even product extension.
H=vectors([(2,0),(R(4,3),S.sqrt(5)/3),(-R(4,3),S.sqrt(5)/3),(-2,0),(-R(4,3),-S.sqrt(5)/3),(R(4,3),-S.sqrt(5)/3)])
J=vectors([(0,1),(-4*S.sqrt(2)/3,R(1,3)),(-4*S.sqrt(2)/3,-R(1,3)),(0,-1),(4*S.sqrt(2)/3,-R(1,3)),(4*S.sqrt(2)/3,R(1,3))])
ch=billiard(H,S.Integer(4),S.Integer(1),R(4,9),'6 phase x')
cj=billiard(J,S.Integer(4),S.Integer(1),R(4,9),'6 phase y')
eq(area(H)*ch[(0,0)],R(14000,729),'6 phase x central product')
eq(area(J)*cj[(0,0)],R(14336,729),'6 phase y central product')
eq(area(J)*cj[(0,0)]-area(H)*ch[(0,0)],R(112,243),'6 central products differ')

# A physical primitive star winding 3/8: exact signed zero/negative pedals.
a=4*S.sqrt(2);b=3*S.sqrt(3);x=4*a/5;y=3*b/5
W=vectors([(a,0),(x,y),(0,b),(-x,y),(-a,0),(-x,-y),(0,-b),(x,-y)])
Z=[W[(3*i)%8] for i in range(8)]
cz=billiard(Z,S.Integer(32),S.Integer(27),R(864,35),'8 star winding 3')
eq(area(Z),168*S.sqrt(6)/5,'8 star original area')
eq(cz[(0,0)],1248*S.sqrt(6)/245,'8 star B0')
eq(cz[(2,0)],-96*S.sqrt(6)/245,'8 star C')
eq(cz[(1,0)],0,'8 star linear x zero')
eq(cz[(0,1)],0,'8 star linear y zero')
eq(cz[(0,0)]+13*cz[(2,0)],0,'8 star zero at |M|^2=13')
require(S.simplify(cz[(0,0)]+16*cz[(2,0)]).is_negative is True,'8 star negative at M=(4,0)')
eq(area(feet(Z,S.Matrix([S.sqrt(13),0]))),0,'8 star direct zero-area foot construction')
rev=list(reversed(Z))
eq(area(rev),-area(Z),'8 star reversal original area')
eq(area(feet(rev,S.Matrix([4,0]))),-area(feet(Z,S.Matrix([4,0]))),'8 star reversal pedal area')
eq(area(rev)*area(feet(rev,S.Matrix([4,0]))),area(Z)*area(feet(Z,S.Matrix([4,0]))),'8 star reversal product')

output={
    'actual_utc':datetime.now(timezone.utc).isoformat(),
    'status':'PASS',
    'checks':len(checks),
    'optimization_level':sys.flags.optimize,
    'python':sys.version,
    'sympy':S.__version__,
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'exact_results':{
        'N4_product':'128/25 for a=2,b=1, all M',
        'nonconfocal_products':['128/25','8'],
        'repeated_triangle_M10_product_difference':'16*(-55376+15368*sqrt(13))/729',
        'primitive_N6_central_products':['14000/729','14336/729'],
        'primitive_star_3_8_B_M':'96*sqrt(6)/245*(13-|M|^2)',
        'primitive_star_3_8_A':'168*sqrt(6)/5'
    },
    'limitations':'Finite exact controls do not prove the all-period invariant.',
    'passed_labels':checks
}
name='CHECK_RESULTS_OPT.json' if sys.flags.optimize else 'CHECK_RESULTS.json'
(BASE/name).write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:output[k] for k in ['actual_utc','status','checks','optimization_level','script_sha256']}))
