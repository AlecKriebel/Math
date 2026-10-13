"""Independent check of candidate geometry, written without accessing any author code/results."""
import sympy as S,json
from pathlib import Path
k,a,b,beta,s,t=S.symbols('k a b beta s t', real=True)
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def sub(p,q):return [x-y for x,y in zip(p,q)]
def add(p,q):return [x+y for x,y in zip(p,q)]
def scale(z,p):return [z*x for x in p]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(P):return S.simplify(sum(det(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2)
def projection(f,p,q):
 d=sub(q,p);return [S.simplify(x) for x in add(p,scale(dot(sub(f,p),d)/dot(d,d),d))]
def linefoot(f,n):return add(f,scale((1-dot(n,f))/dot(n,n),n))
def simpl(x,caustic):
 numerator=S.fraction(S.cancel(x))[0]
 G=S.groebner([t**2+s**2-1,beta**2+k**2-1],t,beta,s,k,a,b) if caustic else S.groebner([t**2+s**2-1,b**2-a**2+k**2],t,b,s,k,a,beta)
 return S.factor(G.reduce(S.expand(numerator))[1])
q=linefoot([k,0],[-s,t/beta]); Q=linefoot([k,0],[-s/a,t/b]);
qp=[(k-s)/(1-k*s),beta*t/(1-k*s)];Qp=[a*(k-a*s)/(a-k*s),a*b*t/(a-k*s)]
map_res=[simpl(q[i]-qp[i],True) for i in range(2)]+[simpl(Q[i]-Qp[i],False) for i in range(2)]
assert map_res==[0,0,0,0]
A,B=S.Integer(21),S.Integer(16);lam=S.Rational(336,25);alpha2=A-lam;beta2=B-lam
P=[[S.sqrt(21),0],[-3*S.sqrt(21)/5,S.Rational(16,5)],[-3*S.sqrt(21)/5,-S.Rational(16,5)]]
ns=[[p[0]/A,p[1]/B] for p in P]
T=[]
for i in range(3):
 n=ns[i];m=ns[(i+1)%3];den=det(n,m);assert den!=0
 T.append([S.simplify((m[1]-n[1])/den),S.simplify((n[0]-m[0])/den)])
for i in range(3):
 p,q=P[i],P[(i+1)%3];assert S.simplify(p[0]**2/A+p[1]**2/B-1)==0
 d=sub(q,p);n=[-d[1],d[0]];h=dot(n,p);assert S.simplify(h**2-alpha2*n[0]**2-beta2*n[1]**2)==0
 j=(i+1)%3;vin=scale(1/S.sqrt(dot(d,d)),d);dd=sub(P[(j+1)%3],P[j]);vout=scale(1/S.sqrt(dot(dd,dd)),dd)
 re=sub(vin,scale(2*dot(vin,ns[j])/dot(ns[j],ns[j]),ns[j]));assert all(S.simplify(x-y)==0 for x,y in zip(re,vout))
areas={}
for sig in [1,-1]:
 f=[sig*S.sqrt(5),0];q=[projection(f,P[i],P[(i+1)%3]) for i in range(3)];qt=[[S.simplify(x) for x in linefoot(f,n)] for n in ns]
 for i in range(3):
  assert [S.simplify(x-y) for x,y in zip(projection(f,T[(i-1)%3],T[i]),qt[i])]==[0,0]
 areas['A'+str(sig)]=area(q);areas['B'+str(sig)]=area(qt)
 assert S.simplify(areas['A'+str(sig)]-84*(7*S.sqrt(21)+sig*S.sqrt(5))/625)==0
 assert S.simplify(areas['B'+str(sig)]-7*(7*S.sqrt(21)+sig*S.sqrt(5))/10)==0
 assert S.simplify(areas['B'+str(sig)]/areas['A'+str(sig)]-S.Rational(125,24))==0
result={'symbolic_projection_residuals':[int(x) for x in map_res],'exact_candidate_triangle_areas':{k:str(v) for k,v in areas.items()},'outer_vertices':[[str(x) for x in p] for p in T],'all_assertions_passed':True,'caustic_squared_axes':[str(alpha2),str(beta2)],'ratio_strictly_above_one_proof':'numerator and denominator are positive and differ by 2sqrt(5); inverted orbit exchanges them'}
print(json.dumps(result,indent=2));Path(__file__).with_name('candidate_exact_and_symbolic_results.json').write_text(json.dumps(result,indent=2)+'\n')
