"""Independent cubic-field/continuous-time and exact-family checks.
Reuses only our fresh graph/AD routines; imports no published verification code.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,permutations
import sympy as sp
import json,datetime,hashlib,time
import fresh_main_controls as m
t0=time.time();start=len(m.checks);m.phase('cubic K2P: independent field, interval and graph reconstruction')
x=sp.symbols('x');poly=634127002560*x**3-2160769703472*x**2+1746884136303*x-169873318739
ell=sp.CRootOf(poly,1);F=sp.QQ.algebraic_field(ell);l=F.from_sympy(ell);f=lambda a,b=1:F.convert(sp.Rational(a,b));zero=f(0);one=f(1)
lo,hi=Q(1073231219980,10**12),Q(1073231219981,10**12)
m.ck('unique cubic root in stated interval',sp.Poly(poly,x).count_roots(sp.Rational(lo.numerator,lo.denominator),sp.Rational(hi.numerator,hi.denominator))==1)
def peval(q):return 634127002560*q**3-2160769703472*q**2+1746884136303*q-169873318739
m.ck('cubic endpoints have opposite signs',peval(lo)*peval(hi)<0)
for _ in range(180):
    mid=(lo+hi)/2
    if peval(lo)*peval(mid)<=0:hi=mid
    else:lo=mid
tl,th=Q(37),Q(38)
m.ck('sqrt1423 isolation',tl*tl<1423<th*th)
for _ in range(180):
    mid=(tl+th)/2
    if mid*mid<1423:tl=mid
    else:th=mid
class E:
    def __init__(self,a,b=None):
        self.a=a if hasattr(a,'to_list') else f(a);self.b=zero if b is None else b
    def wrap(self,x):return x if isinstance(x,E) else E(x)
    def __add__(self,x):x=self.wrap(x);return E(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self):return E(-self.a,-self.b)
    def __sub__(self,x):return self+-self.wrap(x)
    def __rsub__(self,x):return self.wrap(x)+-self
    def __mul__(self,x):
        if isinstance(x,m.Dual):return NotImplemented
        x=self.wrap(x);return E(self.a*x.a+1423*self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.wrap(x);den=x.a*x.a-1423*x.b*x.b
        return E((self.a*x.a-1423*self.b*x.b)/den,(self.b*x.a-self.a*x.b)/den)
    def __eq__(self,x):
        try:x=self.wrap(x);return self.a==x.a and self.b==x.b
        except:return False
    def __bool__(self):return bool(self.a) or bool(self.b)
    def __pow__(self,n):
        out=E(one)
        for _ in range(n):out*=self
        return out
    def __str__(self):return str(F.to_sympy(self.a))+' +sqrt1423*('+str(F.to_sympy(self.b))+')'
basebound=m.bound
def ebound(z,ignored=None):
    if isinstance(z,E):return m.iadd(basebound(z.a,(lo,hi)),m.imul(basebound(z.b,(lo,hi)),(tl,th)))
    return basebound(z,(lo,hi))
m.bound=ebound
L=E(l);rt=E(zero,one);o=E(one);z=E(zero);r=lambda a,b=1:E(f(a,b))
v=r(73394329,14503216)*L**2-r(1453474193,248626560)*L+r(4133719,3669120)
xx=-r(366971645,99450624)*L**2+r(4259402513,340973568)*L-r(42362455,5031936)
K=[o,r(1,2),r(1,2),r(1,2)];U=[o,r(3,4),v,r(3,4)];V=[o,r(1,16),xx,r(1,16)];S=[o,r(1,5),r(1,2),r(1,5)];T=[o,r(7,30),r(1,15),r(7,30)]
PG=r(73394329,4762633008)*L**2+r(368713223407,81645137280)*L-r(4985775401,1204882560)
P=[o,r(79)/(4*rt),PG,r(79)/(4*rt)];B=[o,rt/240,L/4,rt/240]
tree=[[K[g]*K[g]*P[g] for g in range(4)],[K[g]*B[g] for g in range(4)],[K[g]*B[g] for g in range(4)]];par=m.parmake(K,U,V,S,T)
m.admissible('cubic',par,tree,None,ct=True)
qq,pp=m.collision('cubic',par,tree,None)
minimum=min(pp,key=lambda q:sum(ebound(q))/2)
for i,p in enumerate(pp):m.ck('cubic minimum comparison'+str(i),p==minimum or ebound(p-minimum)[0]>0)
pb=ebound(minimum);m.ck('published pmin lower/upper',Q(149867914232177,10**16)<pb[0] and pb[1]<Q(149867914232311,10**16))
margin=r(11,900)
all_edges=[par[k] for k in ['E','R','U','V','A2','B2','A3','B3','D2','D3']]+tree+[[K[g]*K[g] for g in range(4)]]
mm=[a[2]-a[1]*a[1] for a in all_edges]
m.ck('minimum K2P continuous-time margin attained',any(q==margin for q in mm))
for i,q in enumerate(mm):m.ck('minimum K2P continuous-time margin'+str(i),q==margin or ebound(q-margin)[0]>0)
jd=m.det(m.jacobian(par,m.r2,m.c2,True));jb=ebound(jd)
m.ck('cubic rank9 stated determinant interval',Q(-4129735,10**28)<jb[0] and jb[1]<Q(-4129729,10**28))
def invariant(qq,perm=(0,1,2)):
    def val(name):
        a=tuple('ACGT'.index(c) for c in name);return qq[tuple(a[i] for i in perm)]
    return val('AGG')*val('GAG')*val('CCA')**2-val('AAA')*val('GGA')*val('TCG')**2
children=[]
for val in [z,o]:
    child=dict(par);child['d3']=val;cq={xyz:m.fq(child,xyz) for xyz in product(range(4),repeat=3)}
    children.append((invariant(cq),invariant(cq,(0,2,1))))
matches=[]
for a,b in children:
    aa,bb=ebound(a),ebound(b)
    if Q(-19200,10**13)<aa[0] and aa[1]<Q(-19199,10**13) and Q(34284,10**13)<bb[0] and bb[1]<Q(34286,10**13):matches.append(True)
m.ck('published negative-child and reordered-positive intervals',bool(matches))
details={'cubic_pmin_interval':list(map(str,pb)),'cubic_rank9_interval':list(map(str,jb)),
         'cubic_rank9':str(jd),'child_invariant_intervals':[[list(map(str,ebound(a))),list(map(str,ebound(b)))] for a,b in children]}

m.phase('rational all-order negative point and exact symmetric-family determinant')
# All rational field calculations are new direct graph evaluations.
par={};pairs={'E':(Q(69,100),Q(4,5)),'R':(Q(1),Q(1)),'U':(Q(53,100),Q(23,100)),
 'V':(Q(23,50),Q(3,20)),'A2':(Q(9,25),Q(89,100)),'B2':(Q(19,50),Q(17,50)),
 'A3':(Q(9,20),Q(21,100)),'B3':(Q(3,25),Q(39,50)),'D2':(Q(17,100),Q(19,100)),'D3':(Q(49,100),Q(27,100))}
for key,(a,b) in pairs.items():par[key]=[Q(1),a,b,a]
par.update(d2=Q(3,5),d3=Q(11,50));qq={xyz:m.fq(par,xyz) for xyz in product(range(4),repeat=3)}
signs=[invariant(qq,p) for p in permutations(range(3))]
wants={-Q(1622035263547207769829908849883,122070312500000000000000000000000000000),
       -Q(167331432602036163517296212056077,19531250000000000000000000000000000000000),
       -Q(51058092403609003822417228842579,381469726562500000000000000000000000000000)}
m.ck('all six order invariants match exact published fractions',set(signs)==wants and all(signs.count(v)==2 for v in wants))
pp=[m.invert(qq,p) for p in product(range(4),repeat=3)];m.ck('rational point published exact pmin',min(pp)==Q(2920987217429243,200000000000000000))
for key,a in par.items():
    if key not in ['d2','d3','R']:m.ck('rational point admissible '+key,all(0<v<1 for v in a[1:]) and min(m.row(a))>0)
u,v,w,xx,a,b,c,d=sp.symbols('u v w x a b c d')
MAC=(a*u+c*w)/2;MAG=(b*v+d*xx)/2;MCC=(a*a+2*a*c*u*w+c*c)/4;MGG=(b*b+2*b*d*v*xx+d*d)/4
MCG=(a*b*u+a*d*u*xx+b*c*v*w+c*d*w)/4;MCT=(a*a*v+2*a*c*u*w+c*c*xx)/4
equations=sp.Matrix([MCG**2-MAC**2*MGG,MCT**2*MGG-MAG**2*MCC**2]);J=equations.jacobian([v,xx])
subs={u:sp.Rational(4,5),v:sp.Rational(19,30),w:sp.Rational(7,240),xx:sp.Rational(239,360),a:sp.Rational(1,4),b:sp.Rational(1,2),c:sp.Rational(1,3),d:sp.Rational(1,27)}
m.ck('symmetric core factorization equations at witness',equations.subs(subs)==sp.zeros(2,1))
fd=J.subs(subs).det();m.ck('published symmetric-family determinant',fd==sp.Rational(675554683609333,194995116803358720000000));details['family_det']=str(fd)

out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':len(m.checks)-start,'labels':m.checks[start:],'details':details,'seconds':time.time()-t0,
 'scope':'Independent cubic K2P collision, all probabilities via graph and ordinary states, exact CT/pmin/rank/sign bounds, rational sign witness and family determinant. No supplied code/certificate imported.'}
out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();Path(__file__).with_name('fresh_ct_family_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','checks','seconds']}),flush=True)
