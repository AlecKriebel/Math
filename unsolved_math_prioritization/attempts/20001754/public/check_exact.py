#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; not a substitute for its analytic proofs."""
import json
from pathlib import Path
import sympy as s

I=s.eye(2)
S=s.Matrix([[0,1],[1,0]])
R=s.Matrix([[-1,0],[-1,1]])
T=s.Matrix([[1,0],[1,-1]])
J=s.diag(-1,1)
M=s.Matrix([[1,s.Rational(-1,2)],[s.Rational(-1,2),1]])
def tup(a):return tuple(a)
def closure(gens):
    seen={tup(I):I}; pending=[I]
    while pending:
        a=pending.pop()
        for g in gens:
            b=g*a
            if tup(b) not in seen:
                seen[tup(b)]=b;pending.append(b)
                assert len(seen)<=24
    return list(seen.values())
G=closure([S,R]);old=closure([S,T])
assert len(G)==6 and len(old)==12
assert S*S==R*R==I and (S*R)**3==I and (S*T)**3==-I
assert J*R==s.Matrix([[1,0],[-1,1]])
x,y=s.symbols('x y',real=True)
v=s.Matrix([x,y]); edges=[x*x,y*y,(x-y)**2]
for a in G:
    assert abs(a.det())==1 and a.T*M*a==M
    av=a*v
    transformed=[s.expand(av[0]**2),s.expand(av[1]**2),s.expand((av[0]-av[1])**2)]
    assert all(any(s.expand(z-e)==0 for e in edges) for z in transformed)
for k in range(-10,11):
    assert (J*R)**k==s.Matrix([[1,0],[-k,1]])
assert M.det()==s.Rational(3,4) and M.eigenvals()=={s.Rational(1,2):1,s.Rational(3,2):1}

def allowed(t):return t==0 or abs(t)>=1
def tri(a,b):return (a,b)!=(0,0) and all(allowed(t) for t in [a,b,a-b])
w=(s.Rational(2),s.Rational(-3,2))
assert tri(*w) and not tri(w[0],-w[1])

n,beta,u=s.symbols('n beta u',positive=True)
H=(2*s.pi/beta)**n/3**(n/2)*s.exp(-s.pi**2*u/beta)
P=1-n/beta+s.pi**2*u/beta**2
assert s.simplify(H+s.diff(H,beta)-H*P)==0
C=3**(n/2)*(beta/(2*s.pi))**n/(1-n/beta)
assert s.simplify(C*H.subs(u,0)*(1-n/beta))==1
assert s.simplify(s.diff(s.log(C),beta)-n*(beta-n-1)/(beta*(beta-n)))==0
Copt=3**(n/2)*(n+1)**(n+1)/(2*s.pi)**n
assert s.simplify(C.subs(beta,n+1)/Copt)==1
C2=2*3**(n/2)*(n/s.pi)**n
assert s.simplify(C.subs(beta,2*n)/C2)==1
A=s.Rational(3,4)*C2*(s.pi/(2*n))**(n/2)
ratio=s.Rational(9,8)*(s.sqrt(3)/2)**n
assert s.simplify(A*A/C2/ratio)==1
assert s.simplify(ratio.subs(n,1)**2)==s.Rational(243,256)<1
# Symbolic recurrence plus its factor <1 proves the same bound for all integer n>=1.
assert s.simplify(ratio.subs(n,n+1)/ratio)==s.sqrt(3)/2
assert s.Rational(3,4)<1

# Gaussian one-point primal tensor failure: (1-|u|^2)^2 is positive at |u|=2.
assert (1-s.Integer(4))**2==9 and tri(s.Integer(2),s.Integer(-2))
# Concrete non-independent Gaussian values differ by their q and polynomial factors.
assert (s.Matrix([s.Rational(1,2),s.Rational(1,2)]).T*M*s.Matrix([s.Rational(1,2),s.Rational(1,2)]))[0]==s.Rational(1,4)
assert (s.Matrix([s.Rational(1,2),s.Rational(-1,2)]).T*M*s.Matrix([s.Rational(1,2),s.Rational(-1,2)]))[0]==s.Rational(3,4)

out={
 'status':'PASS',
 'scope':'Finite exact algebra; all-dimensional analytic arguments are in PROOF.md.',
 'rebasing_group_order':len(G),
 'alternative_generator_group_order':len(old),
 'JR_shear':[[int(v) for v in row] for row in (J*R).tolist()],
 'quadratic_matrix_determinant':str(M.det()),
 'quadratic_matrix_inverse':[[str(v) for v in row] for row in M.inv().tolist()],
 'edge_mass_squared_ratio':'(9/8)*(sqrt(3)/2)^n',
 'n1_edge_mass_squared_ratio_squared':str(s.Rational(243,256)),
 'ratio_successive_dimension_factor':'sqrt(3)/2',
 'gaussian_optimal_parameter':'beta=n+1',
 'gaussian_optimal_objective':'3^(n/2)*(n+1)^(n+1)/(2*pi)^n',
 'sample_exact_ratios':{str(k):str(s.simplify(ratio.subs(n,k))) for k in range(1,9)},
 'triangle_set_rotation_witness':['2','-3/2'],
 'all_assertions_passed':True
}
print(json.dumps(out,indent=2))
if __name__=='__main__':
    Path(__file__).with_name('exact_results.json').write_text(json.dumps(out,indent=2)+'\n')
