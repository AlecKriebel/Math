import sympy as S
from itertools import combinations
import json
n=3;N=6;Q=S.ones(n)*S.Rational(2,3)-S.eye(n);U=S.eye(n).col_join(-Q)
G=U.T*U;b=U.T*S.ones(N,1)
W=Y=FW=FY=S.Integer(0);rows=[]
for ids in combinations(range(N),n):
 A=U[list(ids),:];det=A.det();assert det!=0
 x=A.inv()*S.ones(n,1);w=det**2;r2=(x.T*x)[0];feasible=all(t<=1 for t in U*x)
 W+=w;Y+=w*r2
 if feasible:FW+=w;FY+=w*r2
 rows.append({'rows':ids,'weight':str(w),'squared_norm':str(r2),'feasible':feasible})
theory=(G.inv()*b).dot(G.inv()*b)+(N-(b.T*G.inv()*b)[0])*S.trace(G.inv())
assert W==G.det() and Y/W==theory==9
assert max(S.Rational(r['squared_norm']) for r in rows if r['feasible'])==6
print(json.dumps({'all_bases_nonsingular':True,'number_of_bases':len(rows),'total_determinant_weight':str(W),'all_basis_average_squared_norm':str(Y/W),'theoretical_identity_value':str(theory),'feasible_basis_count':sum(r['feasible'] for r in rows),'feasible_basis_weight':str(FW),'feasible_basis_weighted_average_squared_norm':str(FY/FW),'maximum_feasible_squared_norm':'6','all_intersections':rows,'all_exact_checks_passed':True},indent=2))
