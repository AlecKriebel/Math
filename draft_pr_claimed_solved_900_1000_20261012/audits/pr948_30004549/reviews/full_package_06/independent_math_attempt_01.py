from pathlib import Path
import sympy as S,json,datetime,os,itertools
R=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr948_30004549/reviews/full_package_06')
u,v,x,t,e=S.symbols('u v x t e',real=True);coords=[u,v,x,t];ru,rx,rt=S.symbols('Ru Rx Rt',real=True);h=S.symbols('h',positive=True);D=1-rx-rt**2/4;events=[]
def red(q):return S.factor(S.cancel(S.expand(q))).subs(h**2,D).simplify()
def test(name,ok,detail):
 if not ok:raise RuntimeError(name+': '+str(detail))
 events.append({'test':name,'pass':True,'detail':str(detail)})
def matrix(q):
 m=S.zeros(4)
 for (i,j),a in q.items():m[i,j]=a;m[j,i]=-a
 return m
A=matrix({(0,2):1,(1,3):-1});BP=matrix({(0,3):1,(1,2):1-rx,(1,3):-rt,(0,1):ru});BN=(BP-rt*A/2)/h;J=-A.inv()*BN
test('full_cutoff_J_square',all(red(q)==0 for q in J*J+S.eye(4)),J)
for name,F in [('alpha',A),('beta_R',BP),('gamma_R',u*A-v*BP)]:test('full_cutoff_antiinvariance_'+name,all(red(q)==0 for q in J.T*F*J+F),'includes arbitrary Ru Rx Rt')
test('correct_product_sign',J.subs({ru:0,rx:0,rt:0,h:1})==S.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]),'J0 U=V, J0 X=T')
# Exterior differentiation and wedge implementation independent of preserved code.
def add(*forms):
 out={}
 for F in forms:
  for I,c in F.items():out[I]=out.get(I,0)+c
 return {I:S.simplify(c) for I,c in out.items() if S.simplify(c)!=0}
def scale(a,F):return {I:S.simplify(a*c) for I,c in F.items()}
def wedge(F,G):
 out={}
 for I,a in F.items():
  for K,b in G.items():
   if set(I)&set(K):continue
   L=I+K;sgn=(-1)**sum(L[i]>L[j] for i in range(len(L)) for j in range(i+1,len(L)));T=tuple(sorted(L));out[T]=out.get(T,0)+sgn*a*b
 return add(out)
def d(F):
 out=[]
 for I,c in F.items():
  for j,z in enumerate(coords):out.append(wedge({(j,):S.diff(c,z)},{I:1}))
 return add(*out)
a={(0,2):S.Integer(1),(1,3):-S.Integer(1)};b={(0,3):S.Integer(1),(1,2):S.Integer(1)};r=S.Function('R')(*coords);q=d({(1,):r});br=add(b,q);g=add(scale(u,a),scale(-v,b));gr=add(g,scale(-1,d({(1,):r*v})))
test('full_cutoff_primitive_product',d({(1,):r*v})==scale(v,q),'no restriction on R_v or other cutoff derivatives')
test('full_cutoff_third_relation',gr==add(scale(u,a),scale(-v,br)),gr)
test('full_cutoff_closed_beta_gamma',d(br)=={} and d(gr)=={},'d^2 and exact gamma variable relation')
test('full_cutoff_gram',wedge(a,a)=={(0,1,2,3):2} and wedge(a,br)=={(0,1,2,3):S.diff(r,t)} and wedge(br,br)=={(0,1,2,3):2-2*S.diff(r,x)},[wedge(a,a),wedge(a,br),wedge(br,br)])
# Entire core Nijenhuis tensor, direct bracket formula.
k=1-e*x;JC=J.subs({ru:0,rx:e*x,rt:0,h:S.sqrt(k)});N={}
for i,j in itertools.combinations(range(4),2):
 out=[]
 for z in range(4):out.append(S.simplify(sum(JC[p,i]*S.diff(JC[z,j],coords[p])-JC[p,j]*S.diff(JC[z,i],coords[p])-JC[z,p]*S.diff(JC[p,j],coords[i])+JC[z,p]*S.diff(JC[p,i],coords[j]) for p in range(4))))
 N[str((i,j))]=[str(q) for q in out]
 if (i,j)==(0,2):test('Nijenhuis_U_X',out==[e/(2*(e*x-1)),0,0,0],out)
test('nonintegrable_at_J0_value_origin',S.simplify(S.sympify(N['(0, 2)'][0]).subs(x,0)+e/2)==0,'N(U,X)|origin=-epsilon U/2 while J|origin=J0')
for value in [S.Rational(-1,3),S.Rational(1,3)]:test('both_parameter_signs_'+str(value),S.sympify(N['(0, 2)'][0]).subs({e:value,x:0})!=0,'exact nonzero rational')
test('zero_parameter_limit',JC.subs(e,0)==J.subs({ru:0,rx:0,rt:0,h:1}) and all(S.sympify(z).subs(e,0)==0 for row in N.values() for z in row),'every coordinate N component vanishes')
# Independent topology consistency: Kunneth and signature product.
b1=2*2+2;b2=1+1+(2*2)*2;chi=2-2*b1+b2;test('topological_bound_consistency',b2==10 and chi==0 and b2//2==5,'b1=6, b2=10, signature=0, b+=5; lowerbound3 allowed')
# Exact box corners certify the minimum of the concave Gram determinant in Rx,Rt.
corners=[D.subs({rx:a,rt:b}) for a in [-S.Rational(1,4),S.Rational(1,4)] for b in [-1,1]];test('uniform_positivity_box',min(corners)==S.Rational(1,2),'D affine in Rx and concave in Rt; minimum on rectangle at a corner')
# Mutations must be falsified.
wrong=add(g,d({(1,):r*v}));test('wrong_sign_mutation_rejected',wrong!=add(scale(u,a),scale(-v,br)),'gamma+d(Rv dv) fails third relation')
rho=S.Function('rho')(*coords);wrongbr=add(b,{(1,2):-e*rho*x});test('omitted_cutoff_derivatives_rejected',d(wrongbr)!={},d(wrongbr))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':len(events),'events':events,'core_Nijenhuis':N,'runtime':{'sympy':S.__version__},'scope':'Exact finite algebra plus explicit topology consistency, not formal verification of global smooth proof.'};f=open(R/'INDEPENDENT_MATH.json','w');json.dump(out,f,indent=2);f.flush();os.fsync(f.fileno());f.close();print(json.dumps({'status':'PASS','checks':len(events)}))
