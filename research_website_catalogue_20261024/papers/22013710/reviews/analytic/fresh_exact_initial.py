#!/usr/bin/env python3
"""Independent literal dense-entry reconstruction; imports no submitted module.
Arithmetic: SymPy DomainMatrix over an algebraic number field and polynomial ring.
"""
import sympy as s
from sympy.polys.matrices import DomainMatrix as DM
import json,datetime,sys,time
from pathlib import Path
from itertools import product
start=time.time();checks=[];data={}
F=s.QQ.algebraic_field(s.sqrt(2),s.sqrt(3),s.I)
def dm(m,domain=F): return DM.from_Matrix(s.Matrix(m)).convert_to(domain)
def ident(n,domain=F): return DM.eye(n,domain)
def scale(m,c): return m.scalarmul(m.domain.from_sympy(s.sympify(c)))
def kron(a,b):
 d={(i*b.shape[0]+k,j*b.shape[1]+l):v*w for (i,j),v in a.to_dok().items() for (k,l),w in b.to_dok().items()}
 return DM.from_dok(d,(a.shape[0]*b.shape[0],a.shape[1]*b.shape[1]),a.domain)
def adj(m):
 return DM.from_dok({(j,i):F.from_sympy(s.conjugate(F.to_sympy(v))) for (i,j),v in m.to_dok().items()},m.shape[::-1],F)
def tr(m): return s.simplify(m.domain.to_sympy(sum((m.to_dok().get((i,i),m.domain.zero) for i in range(m.shape[0])),m.domain.zero)))
def eq(label,a,b):
 if not (a-b).is_zero_matrix: raise RuntimeError(label)
 checks.append(label)
def val(label,a,b):
 if s.simplify(a-b)!=0: raise RuntimeError((label,a,b))
 checks.append(label)
def reject(label,a):
 if a.is_zero_matrix: raise RuntimeError('negative control accepted: '+label)
 checks.append('negative: '+label)
I2=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Z=s.diag(1,-1); J=X*Z
Pa={'I':I2,'X':X,'Z':Z,'J':J,'Y':s.I*J}
def word(w,domain=F):
 m=s.ones(1,1)
 for c in w:m=s.kronecker_product(m,Pa[c])
 return dm(m,domain)
def perm(dims,order):
 n=s.prod(dims); out=s.zeros(n)
 def encode(t,ds):
  k=0
  for x,d in zip(t,ds):k=k*d+x
  return k
 for v in product(*[range(d) for d in dims]):out[encode([v[k] for k in order],[dims[k] for k in order]),encode(v,dims)]=1
 return dm(out)
def partial(m,left=True,d=4):
 out={}; src=m.to_dok()
 for i,j in product(range(d),repeat=2):
  v=sum((src.get((k*d+i,k*d+j) if left else (i*d+k,j*d+k),F.zero) for k in range(d)),F.zero)
  if v:out[i,j]=v
 return DM.from_dok(out,(d,d),F)
A,B,C,D,E=[word(w) for w in ('ZIZZ','ZIJJ','JIZJ','JIJZ','XIXX')];I16=ident(16);I4=ident(4)
for label,m in zip('ABCDE',(A,B,C,D,E)):
 eq(label+' involution',m*m,I16);eq(label+' Hermitian',adj(m),m)
eq('D=ABC',D,A*B*C)
M=scale(-A-B-C+D,s.Rational(1,2))
eq('M reflection',M*M,I16);eq('ME anticommutation',M*E,-E*M)
H=scale(M,s.sqrt(6)/3)-scale(E,s.sqrt(3)/3)
eq('H Hermitian',adj(H),H);eq('H reflection',H*H,I16);val('trace H',tr(H),0)
q=(1+s.I*s.sqrt(3))/2;kappa=q-1
R=scale(I16,(q-1)/2)+scale(H,(q+1)/2);Ri=adj(R);P=scale(I16-H,s.Rational(1,2))
eq('unitarity',Ri*R,I16);eq('Hecke',(R+I16)*(R-scale(I16,q)),scale(I16,0));eq('P projection',P*P,P);val('rank P from projector trace',tr(P),8)
for left in (True,False):
 eq('partial P '+str(left),partial(P,left),scale(I4,2));eq('partial R '+str(left),partial(R,left),scale(I4,2*kappa));eq('partial inverse '+str(left),partial(Ri,left),scale(I4,2/s.simplify(kappa)))
R1,R2=kron(R,I4),kron(I4,R);H1,H2=kron(H,I4),kron(I4,H)
eq('64 dimensional YBE',R1*R2*R1,R2*R1*R2)
eq('64 dimensional cubic reflection',H1*H2*H1-H2*H1*H2,scale(H1-H2,s.Rational(1,3)))
for proj,label in ((P,'P'),(I16-P,'complement')):
 e,f=kron(proj,I4),kron(I4,proj);T=e*f*e-scale(e,s.Rational(1,3));val(label+' obstruction trace square',tr(T*T)/64,s.Rational(1,18))
# Direct polynomial matrices, no word multiplication implementation.
a,b=s.symbols('alpha beta');G=s.QQ.poly_ring(a,b);M0=M.convert_to(G);E0=E.convert_to(G)
Hp=scale(M0,a)+scale(E0,b);h1,h2=kron(Hp,ident(4,G)),kron(ident(4,G),Hp)
res=h1*h2*h1-h2*h1*h2-scale(h1-h2,s.Rational(1,3))
groups=[(-a*(3*b*b-1)/6,['IIJIJZ','JIZJII','ZIJJII','ZIZZII']),(a*(3*b*b-1)/6,['IIJIZJ','IIZIJJ','IIZIZZ','JIJZII']),(-b*(3*a*a-3*b*b-1)/3,['IIXIXX']),(b*(3*a*a-3*b*b-1)/3,['XIXXII']),(a*(a*a-2*b*b)/2,['JIJZXX','JIZJXX','XIJXZJ','ZIZZXX']),(-a*(a*a-2*b*b)/2,['XIJXJZ','XIZXJJ','XIZXZZ','ZIJJXX'])]
certificate=DM.zeros((64,64),G)
for coefficient,ws in groups:
 for w in ws:
  wmat=word(w,G);certificate+=scale(wmat,coefficient)
  val('polynomial coefficient '+w,tr(wmat.transpose()*res)/64,coefficient)
eq('full 18 word certificate as polynomial matrix',res,certificate)
# Ideal on unit circle and exact boundary controls.
gb=s.groebner([a*a+b*b-1]+[c for c,_ in groups],a,b)
val('circle ideal alpha squared',gb.reduce(a*a-s.Rational(2,3))[1],0);val('circle ideal beta squared',gb.reduce(b*b-s.Rational(1,3))[1],0)
for av,bv in ((0,1),(0,-1),(1,0),(-1,0),(s.Rational(3,5),s.Rational(4,5))):
 Hp0=scale(M,av)+scale(E,bv);u,v=kron(Hp0,I4),kron(I4,Hp0)
 eq('negative point still a reflection '+str((av,bv)),Hp0*Hp0,I16)
 reject('non-YBE reflection '+str((av,bv)),u*v*u-v*u*v-scale(u-v,s.Rational(1,3)))
# Literal 4x4 S from displayed equation; no submitted data copied at runtime.
t=s.sqrt(2); ii=s.I
S=dm(s.Matrix([[2+t,-ii*t,ii*t,2-t],[t,ii*(2+t),ii*(2-t),-t],[-(2-t),-ii*t,ii*t,-(2+t)],[-t,ii*(2-t),ii*(2+t),t]])/4)
eq('S unitary',adj(S)*S,I4)
U=scale(word('IZZI'),ii);V=scale(word('XIXX'),ii);GR=scale(I16+U+V+U*V,kappa/2);swap=perm([4,4],[1,0]);SS=kron(S,S)
eq('GR opposite local conjugacy',adj(SS)*swap*GR*swap*SS,R)
reject('omitting opposite in displayed conjugacy',adj(SS)*GR*SS-R)
eq('GR ordered quarter turns',GR,scale((I16+U)*(I16+V),kappa/2))
# Actual dense 3-site same-generator intertwiner, not word/Clifford bookkeeping.
g1,g2=kron(GR,I4),kron(I4,GR);Sn=kron(kron(S,S),S);Rev=perm([4,4,4],[2,1,0]);Delta=g1*g2*g1;Un=adj(Delta)*Rev*Sn
for i,(r,g) in enumerate(((R1,g1),(R2,g2))):eq('same-generator all-strand intertwiner n3 i'+str(i),Un*r*adj(Un),g)
# Spectator removal and wrong shift control.
KH=scale(-word('ZZZ')-word('ZJJ')-word('JJZ')+word('JZJ'),1/s.sqrt(6))-scale(word('XXX'),1/s.sqrt(3));I8=ident(8)
K=scale(I8,(q-1)/2)+scale(KH,(q+1)/2);W=perm([2]*4,[1,0,3,2]);eq('spectator removal',W*R*adj(W),kron(ident(2),K))
k1,k2=kron(K,I4),kron(I4,K);eq('gYBE shift2',k1*k2*k1,k2*k1*k2)
l1,l2=kron(K,ident(2)),kron(ident(2),K);bad=l1*l2*l1-l2*l1*l2;val('wrong shift1 exact squared residual',tr(adj(bad)*bad),24)
# Braid closure computations from direct matrix products, including Markov controls.
def link(n,w):
 size=4**n;z=ident(size)
 for gen in w:
  h=R if gen>0 else Ri;j=abs(gen)-1
  z=z*kron(kron(ident(4**j),h),ident(4**(n-j-2)))
 return s.simplify(tr(z)*kappa**(-sum(1 if x>0 else -1 for x in w))/2**n)
for name,n,w,target in [('unknot',1,[],2),('unlink2',2,[],4),('hopf',2,[1,1],-2),('trefoil',2,[1]*3,-4),('figure8',3,[1,-2]*2,-4),('borromean',3,[1,-2]*3,2)]:val('link '+name,link(n,w),target)
for w in ([],[1],[1,1],[1,-1],[1]*3,[-1]*3):
 for sign in (1,-1):val('Markov stabilization '+str((w,sign)),link(3,w+[sign*2]),link(2,w))
eq('R order6',R**6,I16);eq('R cube',R**3,-I16)
data.update(check_count=len(checks),checks=checks,negative_controls=6,elapsed_seconds=time.time()-start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sympy=s.__version__,optimization=sys.flags.optimize,method='native SymPy DomainMatrix primitive algebraic field and polynomial matrices; no submitted module imported',circle_groebner=[str(g) for g in gb.polys])
Path(__file__).with_suffix('.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({k:v for k,v in data.items() if k!='checks'},indent=2))
