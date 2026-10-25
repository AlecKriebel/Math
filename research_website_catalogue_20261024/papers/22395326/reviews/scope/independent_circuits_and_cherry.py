"""Own exact universal controls for target Lemma8.5 and Theorem5.3.

Only SymPy is imported; no archive source executes. Output goes to stdout.
The universal positivity deduction is stated separately from symbolic equalities.
"""
import json
import sympy as s

lam=s.symbols('lam')
E={k:[s.Integer(1)]+list(s.symbols(k+'1:4')) for k in 'abcdef'}
def q(t):
    x,y,z=t
    a,b,c,d,e,f=[E[k] for k in 'abcdef']
    if x^y^z: return s.Integer(0)
    return a[x]*b[y]*c[z]*(lam*f[y]*d[z]+(1-lam)*f[x]*e[z])
circuits=[(((0,0,0),(1,2,3),(2,3,1)),((0,3,3),(1,0,1),(2,2,0))),
          (((0,0,0),(1,3,2),(3,2,1)),((0,2,2),(1,0,1),(3,3,0))),
          (((0,0,0),(2,1,3),(3,2,1)),((0,1,1),(2,2,0),(3,0,3))),
          (((0,0,0),(2,3,1),(3,1,2)),((0,1,1),(2,0,2),(3,3,0))),
          (((0,0,0),(1,3,2),(2,1,3)),((0,3,3),(1,1,0),(2,0,2))),
          (((0,0,0),(1,2,3),(3,1,2)),((0,2,2),(1,1,0),(3,0,3)))]
f1,f2,f3=E['f'][1:];d1,d2,d3=E['d'][1:];e1,e2,e3=E['e'][1:]
expected=[(f1*f3-f2)*(d1*e3-d3*e1*f2),
          (f1*f2-f3)*(d1*e2-d2*e1*f3),
          -(f1*f3-f2)*(d1*e3*f2-d3*e1),
          -(f1*f2-f3)*(d1*e2*f3-d2*e1),
          -(f1-f2*f3)*(d2*e3-d3*e2*f1),
          (f1-f2*f3)*(d2*e3*f1-d3*e2)]
rows=[]
for i,((L,R),expected_i) in enumerate(zip(circuits,expected),1):
    pendant=s.prod(E[k][t[j]] for t in L for j,k in enumerate('abc'))
    raw=s.prod(q(t) for t in L)-s.prod(q(t) for t in R)
    residual=s.expand(raw-lam*(1-lam)*pendant*expected_i)
    if residual!=0: raise RuntimeError(('universal_factorization',i))
    tree=lambda t:s.prod(E[k][t[j]] for j,k in enumerate('abc'))
    if s.expand(s.prod(tree(t) for t in L)-s.prod(tree(t) for t in R))!=0:
        raise RuntimeError(('tree_identity',i))
    if s.expand(raw.subs(lam,0))!=0 or s.expand(raw.subs(lam,1))!=0:
        raise RuntimeError(('inheritance_boundary',i))
    rows.append({'circuit':i,'universal_factorization_zero_residual':True,
                 'tree_identity':True,'lambda_zero_or_one_boundary_vanishes':True,
                 'normalized_factorization':str(expected_i)})
# Cherry coordinate map (u,v)->(uv,u/v), one independent block per character tie.
u,v=s.symbols('u v',positive=True);J=s.Matrix([u*v,u/v]).jacobian([u,v]);det=s.factor(J.det())
if det!=-2*u/v:raise RuntimeError('cherry_determinant')
# Ordering (u/v,uv) reverses the sign; nonzero is the invariant content.
print(json.dumps({'six_circuits':rows,
 'strict_domain_universal_deduction':'All pendant factors and lambda(1-lambda) are positive. A nonzero first factor in paired circuits forces f_h^2=1 if both circuits vanish. If all three first factors vanish then p=p^2 with 0<p=f1*f2*f3<1. Both alternatives are impossible. Hence sum of six squares is strictly positive at every strict sunlet point, including tied JC/K2P restrictions.',
 'boundary_control':'At lambda=0 or 1 every circuit vanishes identically; strict inheritance is necessary for the pointwise separator. Identity internal f=(1,1,1) also kills these factors and lies outside the strict domain.',
 'cherry_coordinate_order':['u*v','u/v'],'cherry_Jacobian_determinant':str(det),
 'r_tie_blocks':'Independent blocks give absolute determinant 2^r times product(u_h/v_h), never zero for positive spectra. Positive inverse u=sqrt(P*R), v=sqrt(P/R) and full old tensor division prove an analytic local inverse; this is not a finite sample argument.',
 'scope_limit':'No supplied finite atlas, interval/Krawczyk certificate, global restoration deck or all-network rank census was executed by this diagnostic.'},indent=2))
