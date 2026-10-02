import sympy as S,json
x,y,t=S.symbols('x y t');q=y**2*(y-1)**2*(y-2);qt=y*(y-t)*(y-1)*(y-1-t)*(y-2)
G=[S.Integer(1),y,y**2,y**3,y**4+q];n=0
def ck(v):
 global n
 assert v;n+=1
M=S.Matrix([[S.Poly(S.rem(g,qt,y),y).coeff_monomial(y**i) for g in G] for i in range(5)])
ck(S.factor(M.det())==1+2*t)
nodes=[0,t,1,1+t,2]
V=S.Matrix([[g.subs(y,r) for g in G] for r in nodes])
ck(S.factor(V.det())==S.factor((1+2*t)*S.prod(nodes[j]-nodes[i] for i in range(5) for j in range(i+1,5))))
for a in range(5):
 for b in range(8):
  f=y**(2*a+b);r=S.rem(f,qt,y);rv=S.Matrix([S.Poly(r,y).coeff_monomial(y**i) for i in range(5)]);cs=M.inv()*rv
  P=S.expand(sum(cs[j]*G[j] for j in range(5)))
  ck(S.rem(S.cancel(P-f),qt,y)==0)
  ck(all(S.denom(S.cancel(c)).subs(t,0)!=0 for c in cs))
  ck(S.expand(P.subs(t,0))==S.expand(sum((M.subs(t,0).inv()*S.Matrix([S.Poly(S.rem(f,q,y),y).coeff_monomial(y**i) for i in range(5)]))[j]*G[j] for j in range(5))))
ck(S.Matrix([[1,0,0],[1,1,1],[1,4,2]]).det()!=0)
ck(len(set(r.subs(t,S.Rational(-1,2)) if hasattr(r,'subs') else r for r in nodes))==5)
ck(V.subs(t,S.Rational(-1,2)).det()==0)
print(json.dumps({'status':'PASS','independent_symbolic_assertions':n,'bivariate_monomials':40},indent=2))
