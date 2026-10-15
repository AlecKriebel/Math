#!/usr/bin/env python3
"""Independent compatibility check, not a proof of the BD theorem or novelty."""
import json
import sympy as s

checks = []
for d in range(2, 7):
    pairs = [(i, j) for i in range(d) for j in range(i, d)]
    variables = s.symbols('h:'+str(len(pairs)))
    H = s.zeros(d)
    for (i,j), h in zip(pairs,variables):
        H[i,j] = H[j,i] = h
    for kind in ('independent', 'parallel'):
        P = s.zeros(d)
        if kind == 'independent':
            P[0,1] = P[1,0] = s.Rational(1,2)
            free_pairs = {(0,0), (1,1)}
        else:
            P[0,0] = 1
            free_pairs = {(0,j) for j in range(d)}
        # Saint-Venant tensor for strain E=P*lambda, with H=D^2 lambda.
        eqs = [P[j,l]*H[i,k] + P[i,k]*H[j,l] - P[j,k]*H[i,l] - P[i,l]*H[j,k]
               for i in range(d) for j in range(d) for k in range(d) for l in range(d)]
        A, _ = s.linear_eq_to_matrix(eqs, variables)
        allowed = [variables[pairs.index(p)] for p in sorted(free_pairs)]
        forbidden = {h:0 for p,h in zip(pairs,variables) if p not in free_pairs}
        assert all(s.expand(q.subs(forbidden)) == 0 for q in eqs)
        rank = A.rank()
        assert len(variables)-rank == len(free_pairs)
        checks.append({'dimension':d,'case':kind,'compatibility_rank':rank,
                       'hessian_nullity':len(free_pairs),'allowed_hessian_entries':sorted(free_pairs)})

# Independent nonorthogonal, nonunit specialization of the displayed smooth form.
x = s.Matrix(s.symbols('x:3'))
a,b,v = s.Matrix([2,1,0]),s.Matrix([1,3,0]),s.Matrix([0,0,7])
A,B,V = x.dot(a),x.dot(b),x.dot(v)
u = a*(B**4+B*V)+b*(A**3+A*V)-v*A*B
D = u.jacobian(x)
assert all(s.expand(z)==0 for z in (D+D.T)/2-(4*B**3+3*A**2+2*V)*(a*b.T+b*a.T)/2)
checks.append({'case':'nonorthogonal_nonunit_independent_specialization','pass':True})
print(json.dumps({'pass':True,'checks':checks,'claim':'Finite exact algebra checks only; classification necessity is read from the cited literature.'},indent=2))
