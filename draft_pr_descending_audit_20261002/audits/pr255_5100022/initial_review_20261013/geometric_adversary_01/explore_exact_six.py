import sympy as s
import json
from pathlib import Path
r,a,k=s.symbols('r a k',positive=True)
b=a*r/(1-r);y=b*r
P=[s.Matrix(x) for x in [(0,b),(-1,y),(-1,-y),(0,-b),(1,-y),(1,y)]]
F=s.Matrix([k,0]);U=[];Q=[]
dot=lambda x,z:(x.T*z)[0]
det=lambda x,z:s.det(s.Matrix.hstack(x,z))
for j,p in enumerate(P):
    pp=P[(j+1)%6];ray=p-F;ray2=pp-F
    mat=s.Matrix.vstack(ray.T,ray2.T)
    U.append(mat.inv()*s.Matrix([dot(ray,p),dot(ray2,pp)]))
    e=pp-p;Q.append(p+dot(F-p,e)/dot(e,e)*e)
area=lambda Z:s.factor(sum(det(Z[j],Z[(j+1)%6]) for j in range(6))/2)
def constrained(expr):
    expr=s.cancel(expr)
    n,d=s.fraction(expr)
    n=s.rem(n,k*k-(a*a-b*b),k);d=s.rem(d,k*k-(a*a-b*b),k)
    expr=s.cancel(n/d)
    n,d=s.fraction(expr)
    n=s.rem(n,a*a-1/(1-r*r),a);d=s.rem(d,a*a-1/(1-r*r),a)
    return s.factor(n/d)
AP=constrained(area(P));AQ=constrained(area(Q));AU=constrained(area(U));gamma=constrained(AU/AQ)
result={'original_area':str(AP),'pedal_area':str(AQ),'antipedal_area':str(AU),'ratio':str(gamma),'ratio_numerator_factorization':str(s.factor(s.fraction(gamma)[0]))}
Path(__file__).with_name('EXACT_SIX_EXPLORATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
