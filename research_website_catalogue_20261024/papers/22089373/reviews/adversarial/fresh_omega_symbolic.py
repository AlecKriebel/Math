from fresh_graph_library import *
from sympy.polys.matrices import DomainMatrix
E=[('U','V'),('U','P0'),('P0','P1'),('P1','V'),('S','U'),('S','X'),('V','P4'),('P4','X'),('P0','L0'),('P1','L1'),('P4','L2'),('X','L3')]
Ls={f'L{i}':i for i in range(4)};Lt={f'L{i}':j for i,j in enumerate([1,0,3,2])};ret,Ts=tensor_terms(E,Ls);_,Tt=tensor_terms(E,Lt)
def symbolic(T,g,params,inherit):
 total=0
 for bits,elist in T:
  term=sp.Integer(1)
  for k,bit in enumerate(bits):term*=inherit[k] if bit==0 else 1-inherit[k]
  for i,mask in elist:
   h=0
   for j,c in enumerate(g):
    if mask>>j&1:h^=c
   if h:term*=params[i]
  total+=term
 return sp.expand(total)
u0,u1,u2,u3,u4,u5,p0,p1,p2=sp.symbols('u0 u1 u2 u3 u4 u5 p0 p1 p2');half=sp.Rational(1,2);g=u4+2*u5;h=u0*u5+2*u4
src=[u0,u1,u2,u3,u4,half,half,u5,p0,p1,p2,half]
tgt=[2*u5*(4-u0)/g,u3/(4-u0),u2,2*u1*h/g,4*u4*p2*(4-u0)/h,half,half,2*u0*p2*g/h,p1,p0,g/8,half]
for a,b,c in product(range(4),repeat=3):
 q=(a,b,c,a^b^c);ck('rational map exact Fourier '+str(q),sp.cancel(symbolic(Ts,q,src,[half]*2)-symbolic(Tt,q,tgt,[half]*2))==0)
rows=[(0,0,1,1),(0,1,0,1),(0,1,1,0),(0,1,2,3),(1,0,0,1),(1,0,1,0),(1,0,2,3),(1,1,0,0),(1,1,1,1),(1,1,2,2),(1,2,0,3),(1,2,1,2),(1,2,2,1),(1,2,3,0)]
core=list(sp.symbols('a0:8'));lam=list(sp.symbols('lv lx'));co=[symbolic(Ts,q,core+[1]*4,lam) for q in rows]
J=sp.Matrix(co).jacobian(core+lam);rank=DomainMatrix.from_Matrix(J).to_field().rank();ck('exact rational-function core rank6',rank==6)
for q,c in zip(rows,co):ck('pendant4 Euler identity '+str(q),sp.expand(core[4]*sp.diff(c,core[4])+core[7]*sp.diff(c,core[7])-int(q[3]!=0)*c)==0)
print(json.dumps({'status':'PASS','checks':checks,'check_count':len(checks),'core_rational_function_rank':rank,'scope':'Full64 rational correspondence identities and symbolic core rank/Euler identity, freshly graph-derived; no published helper imported. Paired with exact strict rank9 control and positivity, these support the full Omega common-germ dimension claim.'},indent=2))
