"""Small exact sanity checks; not a proof of the general conjecture."""
import hashlib,itertools,json
from pathlib import Path
import sympy as s
x=s.symbols('x')
f=x**5-x-1
n=5
ps=[s.expand((x+1)**i*(x+2)**(n-1-i)) for i in range(n)]
U=s.Matrix([[p.coeff(x,j) for p in ps] for j in range(n)])
residues=[str(s.rem(ps[i]*ps[0]**(i-1)-ps[1]**i,f,x)) for i in range(2,n)]
quartic=x**4-x-1
qs=[s.rem(x**(2*i),quartic,x) for i in range(4)]
V=s.Matrix([[p.coeff(x,j) for p in qs] for j in range(4)])
perms=[p for p in itertools.permutations(range(1,7)) if sum(p[i]>p[j] for i in range(6) for j in range(i+1,6))%2==0]
forbidden=[p for p in perms if p[0]==1 and p[1]==3 and p[2]==2 and p[3]==4 and p[4]==5]
r={"purpose":"Exact sanity checks, not completeness or a conjecture solution","quintic_irreducible":bool(s.Poly(f,x).is_irreducible),"symmetric_power_det":int(U.det()),"quintic_congruence_residues":residues,"quartic_power_basis_matrix_det":int(V.det()),"quartic_inverse_residue":str(s.rem((x**2)**2-1-x,quartic,x)),"quadratic_inverse_quintic_residue":str(s.rem(x**4-x-1,f,x)),"A6_order":len(perms),"A6_ordered_four_image_count":len({p[:4] for p in perms}),"A6_forbidden_transport_count":len(forbidden)}
checks=[r['quintic_irreducible'],r['symmetric_power_det']==1,all(v=='0' for v in residues),abs(r['quartic_power_basis_matrix_det'])==1,r['quartic_inverse_residue']=='0',r['quadratic_inverse_quintic_residue']!='0',r['A6_order']==360,r['A6_ordered_four_image_count']==360,r['A6_forbidden_transport_count']==0]
if not all(checks): raise RuntimeError(r)
r['all_checks_passed']=True
print(json.dumps(r,indent=2))
