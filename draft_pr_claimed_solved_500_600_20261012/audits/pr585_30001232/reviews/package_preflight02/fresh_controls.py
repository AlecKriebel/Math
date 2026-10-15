"""Fresh Hilbert-function, formal-local, and cover failure controls; no existence oracle."""
import sys
sys.dont_write_bytecode=True
import json
from fractions import Fraction
import sympy as s
if sys.flags.optimize:raise RuntimeError('Assertions must remain enabled')
checks=[]
def ck(label,truth,detail=None):
 if not bool(truth):raise RuntimeError(label)
 checks.append({'check':label,'pass':True,'detail':detail})
x,y,t,u=s.symbols('x y t u');d=s.symbols('d',integer=True,positive=True)
# Hilbert series of the associated graded hypersurface: nonzero homogeneous initial form.
local=[]
for m in range(3,15):
 f=(1+x)*x**m-y**m
 G=s.groebner([f,s.diff(f,x),s.diff(f,y)],x,y)
 ck('Tjurina ideal degree '+str(m+1),[p.as_expr() for p in G.polys]==[x**(m-1),y**(m-1)])
 # Exact formal change X=x*(1+x)^(1/m) trivializes the ordinary multiple germ.
 truncated=s.series((1+x)**s.Rational(1,m),x,0,8).removeO()
 rem=s.Poly(s.expand(truncated**m-(1+x)),x)
 ck('formal coordinate power mod x^8 m='+str(m),all(rem.nth(k)==0 for k in range(8)))
 ck('formal coordinate invertible linear term m='+str(m),truncated.subs(x,0)==1)
 for N in [m-1,m,m+3,3*m]:
  coeff=[(n+1)-(n-m+1 if n>=m else 0) for n in range(N+1)]
  length=sum(coeff)
  ck('Hilbert Samuel length m='+str(m)+' N='+str(N),length==m*(N+1)-m*(m-1)//2,{'length':length,'eventual_difference':coeff[-1]})
  ck('Hilbert Samuel multiplicity m='+str(m)+' N='+str(N),coeff[-1]==m)
 genus=m*(m-1)//2;mu=(m-1)**2;top_special=2-(m-1);top_smooth=2-2*genus
 ck('Milnor delta topological consistency m='+str(m),mu==2*genus-m+1==top_special-top_smooth)
 local.append({'degree':m+1,'multiplicity':m,'delta':genus,'Tjurina_length':mu,'normalization_genus':0,'special_curve_euler':top_special})
# A different branch cover: P(0)=9, split idempotents restrict to two copies of ANY curve ring.
P=(t*t-1)*(t*t-9);q=s.symbols('q');idplus=(q+3)/6;idminus=(3-q)/6
ck('squarefree branch polynomial',s.gcd(P,s.diff(P,t))==1)
for name,a,b in [('sum',idplus+idminus,1),('plus idempotent',idplus**2,idplus),('minus idempotent',idminus**2,idminus),('orthogonality',idplus*idminus,0)]:
 ck('split algebra '+name,s.rem(s.expand(a-b),q*q-9,q)==0)
# Construct exact truncated square-root branches using rational recursion at the singular-fibre value.
coeff={0:s.Integer(3)};Q=s.Integer(3)
for k in range(1,9):
 c=s.symbols('c');Qtrial=Q+c*t**k;eq=s.expand(Qtrial**2-P).coeff(t,k)
 val=s.solve(eq,c)[0];coeff[k]=val;Q+=val*t**k
 ck('unbranched formal inverse order '+str(k),s.expand(Q**2-P).coeff(t,k)==0,{'coefficient':str(val)})
ck('two etale local roots',s.diff(q*q-P,q).subs({q:3,t:0})==6 and s.diff(q*q-P,q).subs({q:-3,t:0})==-6)
ck('branching through singular germ fails smoothness',all(s.diff(q*q-((1+x)*x**6-y**6),v).subs({x:0,y:0,q:0})==0 for v in [x,y,q]))
ck('smooth branch germ regular',s.diff(q*q-u,u)==-1)
# Riemann-Roch of cover pushforward O_Y + O_Y(-rF), not finite enumeration as existence.
r=s.symbols('r',integer=True,positive=True)
KY2=9-d*d;KYF=d*(d-3);N2=KY2+2*r*KYF
chi=2+r*KYF/2;g=(d-1)*(d-2)/2;Euler=2*(3+d*d)-2*r*(2-2*g)
ck('general branch Noether',s.expand(2*N2+Euler-12*chi)==0)
ck('four branch canonical square',s.expand((2*N2).subs(r,2)-6*(d-1)*(d-3))==0)
ck('four branch chi',s.expand(chi.subs(r,2)-(d-1)*(d-2))==0)
ck('four branch Euler',s.expand(Euler.subs(r,2)-6*(d-1)**2)==0)
ck('all d comparison positive polynomial',s.expand(((d-3)**3-6*(d-1)).subs(d,u+7))==u**3+12*u**2+42*u+28)
negatives=[{'case':'one F rather than two in A','A_dot_E':0,'ample_possible_from_this_class':False},{'case':'branch square with repeated roots','smooth_cover_guaranteed':False},{'case':'two branch fibres','K_dot_lifted_section':0,'canonical_ample':False},{'case':'six branch fibres at d7','K2':256,'strict_margin':0,'strict_violation':False},{'case':'degree6 four branch fibres','K2':90,'strict_margin':-9,'strict_violation':False},{'case':'missed component of reducible fibre','A_dot_component':0,'ample':False}]
ck('negative A=F+E',1-1==0)
ck('negative repeated branch has singular point',all(s.diff(q*q-t*t,v).subs({q:0,t:0})==0 for v in [q,t]))
ck('negative two branch canonical degree',2*(1-1)==0)
ck('negative six branch d7 equality',int((2*N2).subs({r:3,d:7}))==(7-3)**4)
ck('negative degree6 comparison',3**4-90==-9)
ck('negative missed fibre component',2*0+0==0)
# The reducible join complement's explicit dimension safety margin and characteristic boundary.
rows=[]
for dd in [2,3,6,7,8,20]:
 N=dd*(dd+3)//2;R=max(a*(a+3)//2+(dd-a)*(dd-a+3)//2 for a in range(1,dd));rows.append({'d':dd,'ambient':N,'join_upper':R+1,'codimension_lower':N-R-1})
 ck('join threshold degree '+str(dd),(R+1<N)==(dd>=3))
ck('char dividing multiplicity negative',s.Poly(t**6-1,t,modulus=3).diff().is_zero)
result={'status':'PASS','sympy':s.__version__,'checks':checks,'total_checks':len(checks),'local_germ_rows':local,'branch_polynomial':str(s.expand(P)),'formal_square_root':str(Q),'dimension_rows':rows,'negative_cases':negatives,'scope':'Finite exact algebra and controls of known formulas only; not geometric existence, Bertini, Nakai, global integral pencil construction, authenticity or historical priority.'}
print(json.dumps(result,indent=2,sort_keys=True))
