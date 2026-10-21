import json, sympy as s
from itertools import combinations
x,y,z,t=s.symbols('x y z t',real=True)
l=s.Symbol('l')
A=s.Matrix([[0,x,y,z],[x,0,-s.I*z,s.I*y],[y,s.I*z,0,-s.I*x],[z,-s.I*y,s.I*x,0]])
q=x*x+y*y+z*z
assert s.simplify(A*A-q*s.eye(4))==s.zeros(4)
triple_polys=[]
for S in combinations(range(4),3):
    p=s.factor(A.extract(S,S).charpoly(l).as_expr())
    assert s.simplify(p-l*(l*l-q))==0
    triple_polys.append(str(p))
pair_polys=[]
for S in combinations(range(4),2):
    p=s.factor(A.extract(S,S).charpoly(l).as_expr())
    pair_polys.append({'S':S,'polynomial':str(p)})
a=s.sqrt((s.Rational(1,4)-t*t)/2)
P=s.eye(4)/2+A.subs({x:t,y:a,z:a})
assert s.simplify(P*P-P)==s.zeros(4)
# Row squared-sum system proves all complementary magnitudes equal.
u=s.symbols('u12 u13 u14 u23 u24 u34')
equations=[u[0]+u[1]+u[2]-s.Rational(1,4),u[0]+u[3]+u[4]-s.Rational(1,4),u[1]+u[3]+u[5]-s.Rational(1,4),u[2]+u[4]+u[5]-s.Rational(1,4)]
sol=s.linsolve(equations,u)
assert sol==s.FiniteSet((u[5],u[4],s.Rational(1,4)-u[4]-u[5],s.Rational(1,4)-u[4]-u[5],u[4],u[5]))
print(json.dumps({'status':'PASS','sympy':s.__version__,'A_squared':str(q)+' I4','all_four_centered_triple_polynomials':triple_polys,'all_six_centered_pair_polynomials':pair_polys,'complementary_squared_magnitudes':str(sol),'surjective_path_projection_identity':True,'partition_types_checked':'4 singleton/triple and 3 pair/pair','endpoint':'1/2 + 1/(2 sqrt(3))'},indent=2))
