"""Original independent checks of visually inspected primary-source matrices.

No source packet, audit script, or printed F formula is imported.
Run with repository .venv/bin/python (SymPy 1.14.0).
"""
import json
import sympy as s

t = s.symbols('t', positive=True)
k = s.sqrt(1+t*t)
J = s.Matrix([[0,-1],[1,0]])
N = s.Matrix([[0,t],[0,0]])
D = s.diag(J,N)
E = s.diag(s.Matrix([[t,-k],[k,-t]]),N)

def curvature(A):
    S = (A+A.T)/2
    comm = A*A.T-A.T*A
    sym2=s.simplify(s.trace(S*S))
    comm2=s.simplify(s.trace(comm*comm.T))
    assert s.trace(A)==0
    F=s.factor(sym2**2/(sym2**2+comm2/4))
    return sym2,comm2,F

d=curvature(D); e=curvature(E)
assert d==(t*t/2,2*t**4,s.Rational(1,3))
assert all(s.simplify(got-want)==0 for got,want in zip(e,(5*t*t/2,34*t**4+32*t*t,25*t*t/(59*t*t+32))))
printed=4*t**4/(3*t**4+2*t*t)
assert s.factor(e[2]-printed)!=0
assert s.limit(e[2],t,0)==0
assert s.limit(d[2],t,0)==s.Rational(1,3)
assert s.simplify((E**2+ s.eye(4))*(E**2))==s.zeros(4)
assert D.charpoly().as_expr()==E.charpoly().as_expr()
# Independent same-group check: upper block of E has eigenvalues +-i and is
# conjugate to J; its cyclic basis [v,Lv] with v=e1 gives the conjugator.
T=s.diag(s.Matrix([[1,t],[0,k]]),s.eye(2))
assert s.simplify(T*D*T.inv()-E)==s.zeros(4)
H=s.diag(1,1,t,1)
assert H*D.subs(t,1)*H.inv()==D

# Fixed-group algebraic obstruction, independent of geometric Ricci soliton.
Ric=s.diag(-t*t/2,0,0,t*t/2,-t*t/2)
c=s.symbols('c')
diag=list((Ric-c*s.eye(5)).diagonal())
rotation_residual=s.factor(diag[2]-diag[0]-diag[1])
c_for_rotation=s.solve(rotation_residual,c)[0]
nil_residual=s.factor((diag[3]-diag[0]-diag[4]).subs(c,c_for_rotation))
assert c_for_rotation==-t*t/2
assert nil_residual==t*t

print(json.dumps({'D':dict(zip(['sym_norm2','comm_norm2','F'],map(str,d))),
 'E':dict(zip(['sym_norm2','comm_norm2','F'],map(str,e))),
 'E_printed_formula':str(printed),'printed_minus_computed':str(s.factor(printed-e[2])),
 'E_limit':str(s.limit(e[2],t,0)),'D_limit':str(s.limit(d[2],t,0)),
 'E_conjugator':str(T),'fixed_algebra_nil_bracket_derivation_residual':str(nil_residual),
 'status':'PASS'},indent=2))
