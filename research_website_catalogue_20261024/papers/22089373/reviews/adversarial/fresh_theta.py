from fresh_graph_library import *
from sympy.polys.matrices import DomainMatrix
# Independent graph tensor; inherits no submitted model code.
E=[('r','A'),('r','C'),('A','B'),('B','C'),('C','D'),('D','E'),('A','F'),('E','F'),('B','LB'),('D','LD'),('F','LF'),('E','LE')]
Ls={'LB':0,'LD':1,'LF':2,'LE':3};Lt={'LE':0,'LD':1,'LF':2,'LB':3}
_,Ts=tensor_terms(E,Ls);_,Tt=tensor_terms(E,Lt)
rows=[(0,0,1,1),(0,1,0,1),(0,1,1,0),(0,1,2,3),(1,0,0,1),(1,0,1,0),(1,0,2,3),(1,1,0,0),(1,1,1,1),(1,1,2,2),(1,2,0,3),(1,2,1,2),(1,2,2,1),(1,2,3,0)]
def sym(T,g,p,inherit):
 total=0
 for bits,elist in T:
  term=sp.Integer(1)
  for k,b in enumerate(bits):term*=inherit[k] if b==0 else 1-inherit[k]
  for i,mask in elist:
   h=0
   for j,c in enumerate(g):
    if mask>>j&1:h^=c
   if h:term*=p[i]
  total+=term
 return sp.expand(total)
p=list(sp.symbols('e0:12'));inh=list(sp.symbols('lc lf'))
for tag,T in [('source',Ts),('target',Tt)]:
 A,B,C,D,E0,F0,G,H,J,K,L,M,N,O=[sym(T,g,p,inh) for g in rows]
 eq=[J-K-M+N,J-A*H-B*F0+C*E0,G*L-E0*N,L**2-B*E0*H,B*M-D*L-B**2*F0+B*C*E0,B*E0*O-B*G*H-C*E0*L+D*E0*H]
 for i,e in enumerate(eq):ck('Theta universal localized equation '+tag+str(i),sp.expand(e)==0)
beta=sp.symbols('beta');Pbeta=43337075*beta**2-36083110*beta+7336259
lo=sp.Rational(441,1250);hi=sp.Rational(3529,10000)
ck('quadratic strict isolating interval smaller root',Pbeta.subs(beta,lo)>0 and Pbeta.subs(beta,hi)<0 and hi<sp.Rational(36083110,2*43337075))
ck('target strictness interval inequalities',hi<sp.Rational(20678,2*24835) and lo>sp.Rational(10339,53010) and lo>sp.Rational(3,20))
src=list(map(sp.Rational,['2/3','3/4','3/5','1/2','9/20','2/5','1/2','1/3','1/5','1/2','1/2','3/8']))
tgt=[sp.Rational(2,3),sp.Rational(3,4),24835*beta/(20678-24835*beta),sp.Rational(1,2),sp.Rational(9934,12215),sp.Rational(171,775),10339/(53010*beta),sp.Rational(1,2),3/(20*beta),sp.Rational(1,2),sp.Rational(1767,4832),sp.Rational(31,190)]
half=sp.Rational(1,2)
for a,b,c in product(range(4),repeat=3):
 g=(a,b,c,a^b^c);difference=sp.cancel(sym(Ts,g,src,[half]*2)-sym(Tt,g,tgt,[half]*2));num,den=sp.fraction(difference);ck('Theta quadratic exact Fourier '+str(g),sp.rem(num,Pbeta,beta)==0 and sp.gcd(den,Pbeta)==1)
P,s,Q,t,R,u,v,S=sp.symbols('P s Q t R u v S');params=[1,half,v,half,u,s,half,t,S,P,R,Q];coords=[sym(Ts,g,params,[half]*2) for g in rows[:8]];J=sp.Matrix(coords).jacobian([P,s,Q,t,R,u,v,S]);det=DomainMatrix.from_Matrix(J).to_field().det().as_expr();expected=-P**3*s**3*Q**4*t*R**4*u**3*v*S**3*(s-1)**2*(v-1)*(v+1)**2/16384;ck('Theta printed source determinant exact polynomial',sp.cancel(det-expected)==0)
P,x,y,z,R,w,S,Q=sp.symbols('P x y z R w S Q');params=[1,half,z,half,w,x,y,half,Q,P,R,S];coords=[sym(Tt,g,params,[half]*2) for g in rows[:8]];J=sp.Matrix(coords).jacobian([P,x,y,z,R,w,S,Q]);det=DomainMatrix.from_Matrix(J).to_field().det().as_expr();expected=-P**3*x**2*y**2*z*R**4*w**4*S**3*Q**4*(x-1)**2*(z-1)*(z+1)**3/32768;ck('Theta printed target determinant exact polynomial',sp.cancel(det-expected)==0)
print(json.dumps({'status':'PASS','checks':checks,'check_count':len(checks),'scope':'Fresh literal graph-derived universal six equations for both graphs, all64 quadratic-field point identities, exact isolating interval strictness, and both gauge determinant factorizations. These support dimension8 and common regular germ after the written localization argument.'},indent=2))
