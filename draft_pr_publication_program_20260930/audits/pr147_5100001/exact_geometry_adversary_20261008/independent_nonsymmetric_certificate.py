"""Exact nonsymmetric phase certificate using Q(sqrt(193)).

The four nonsymmetric vertices are reconstructed directly from the family
formula at (cos t,sin t)=(3/5,4/5). This is an extra falsification check, not
the general proof. It does not import any submitted verifier or result.
"""
from pathlib import Path
import json
import sympy as s
R=s.Rational
rho=s.sqrt(193)
P=(R(12,5),R(12,5)); Q=(-R(256,5)/rho,R(81,5)/rho)
V=[P,Q,tuple(-v for v in P),tuple(-v for v in Q)]
A=R(16); B=R(9); Ac=R(256,25); Bc=R(81,25)
checks=[]

def sub(u,v): return tuple(x-y for x,y in zip(u,v))
def scale(k,u): return tuple(k*x for x in u)
def dot(u,v): return sum(x*y for x,y in zip(u,v))
def det(u,v): return u[0]*v[1]-u[1]*v[0]
def zero(label,x):
    residue=s.simplify(x)
    if residue != 0: raise ValueError(label+": "+str(residue))
    checks.append({"identity":label,"exact_residue":"0"})

lengths=[5+R(84,5)/rho,5-R(84,5)/rho]*2
for i,p in enumerate(V):
    q=V[(i+1)%4]; prev=V[(i-1)%4]
    zero("ellipse boundary "+str(i),p[0]**2/A+p[1]**2/B-1)
    edge=sub(q,p)
    zero("exact edge length squared "+str(i),dot(edge,edge)-lengths[i]**2)
    # Both chosen branches are positive since 84^2 < 25^2*193.
    vin=scale(1/lengths[(i-1)%4],sub(p,prev))
    vout=scale(1/lengths[i],edge)
    n=(p[0]/A,p[1]/B)
    reflected=sub(vin,scale(2*dot(vin,n)/dot(n,n),n))
    for j in range(2): zero("physical reflection "+str(i)+","+str(j),reflected[j]-vout[j])
    zero("incoming Joachimsthal "+str(i),dot(vin,n)-R(1,5))
    zero("outgoing negative Joachimsthal "+str(i),dot(vout,n)+R(1,5))
    en=(-edge[1],edge[0]); h=dot(en,p)
    zero("fixed confocal tangency "+str(i),Ac*en[0]**2+Bc*en[1]**2-h**2)
zero("period-four perimeter",sum(lengths)-20)
zero("determinant of P,Q",det(P,Q)-R(4044,25)/rho)
result={"status":"PASS_EXACT_NONSYMMETRIC_PHASE","field":"Q(sqrt(193))",
        "cos_t":"3/5","sin_t":"4/5","vertices":[list(map(str,v)) for v in V],
        "edge_lengths":list(map(str,lengths)),"checks":checks,
        "positive_length_branch_certificate":"84^2=7056 < 25^2*193=120625",
        "limitation":"Pointwise exact diagnostic; the general family and strict contact interiors are proved in the report."}
Path(__file__).with_name("NONSYMMETRIC_CERTIFICATE.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"status":result["status"],"checks":len(checks)}))
