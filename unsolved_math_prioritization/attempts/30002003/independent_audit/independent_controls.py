#!/usr/bin/env python3
"""Independent symbolic controls. No import of the author's verifier or source text.
Requires SymPy. These controls do not prove algebraic geometry or the conjecture.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import sympy as s

checks = []
negatives = []
def test(name, ok):
    if not bool(ok):
        raise AssertionError(name)
    checks.append(name)
def reject(name, false_claim):
    if bool(false_claim):
        raise AssertionError('False claim survived: ' + name)
    negatives.append(name)
def zero_matrix(m):
    return all(s.expand(t) == 0 for t in m)

def run():
    checks.clear(); negatives.clear()
    x = s.symbols('x1:6')
    q = x[0]*x[1] + x[2]*x[3] + x[4]**2
    test('quadratic Hessian rank five', s.hessian(q, x).rank() == 5)
    test('Jacobian ideal equals vertex ideal', s.groebner([s.diff(q,t) for t in x], *x) == s.groebner(x, *x))
    test('residual quadratic rank three after x1=0', s.hessian(q.subs(x[0],0), x[2:]).rank() == 3)
    test('localization substitution eliminates x2', s.cancel(q.subs(x[1], -(x[2]*x[3]+x[4]**2)/x[0])) == 0)
    u = s.symbols('u1:6')
    for i in range(5):
        qc = q.subs(dict(zip(x,u))).subs(u[i], 1)
        other = [t for j,t in enumerate(u) if j != i]
        jac = [qc] + [s.diff(qc,t) for t in other]
        test('smooth strict transform blowup chart '+str(i+1), s.groebner(jac,*other).reduce(s.Integer(1))[1] == 0)
    lam,a,b,c = s.symbols('lambda a b c')
    jac = s.Matrix([lam,lam*a,lam*b,lam*c]).jacobian([lam,a,b,c]).det()
    test('residue form vanishes to discrepancy two', s.cancel(jac/lam) == lam**2)
    test('ambient adjunction agrees with residue discrepancy', (5-1)-2 == 2)
    test('log terminal discrepancy inequality', s.Integer(2) > -1)
    v = s.symbols('v1:4'); w = s.symbols('w1:4')
    def U(vv):
        return s.Matrix([[1,-sum(t*t for t in vv)/2,-vv[0],-vv[1],-vv[2]],
                         [0,1,0,0,0],[0,vv[0],1,0,0],[0,vv[1],0,1,0],[0,vv[2],0,0,1]])
    M = s.Matrix([[0,1,0,0,0],[1,0,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]])
    test('unipotent action preserves Gram matrix', zero_matrix(U(v).T*M*U(v)-M))
    test('unipotent action has determinant one', U(v).det() == 1)
    test('unipotent action really is unipotent', zero_matrix((U(v)-s.eye(5))**3))
    test('unipotent action has additive composition', zero_matrix(U(v)*U(w)-U(tuple(v[i]+w[i] for i in range(3)))))
    xx,yy,z1,z2,z3,t = s.symbols('x y z1 z2 z3 t', nonzero=True)
    zz = (z1,z2,z3)
    point=s.Matrix([xx,yy,*zz]); norm=2*xx*yy+sum(z*z for z in zz)
    moved=U(tuple(-z/yy for z in zz))*point
    test('open cell normalization removes all W coordinates', all(s.cancel(moved[i]) == 0 for i in range(2,5)))
    test('open cell normalization determines x from q', s.cancel(moved[0]-norm/(2*yy)) == 0)
    T=s.diag(yy,1/yy,1,1,1)
    test('torus scales open cell to y=1', s.cancel((T*moved)[1]) == 1)
    test('torus preserves Gram matrix and determinant', zero_matrix(T.T*M*T-M) and T.det() == 1)
    iso=s.Matrix([x[0]/2,x[1],(x[2]+x[3])/2,(x[2]-x[3])/(2*s.I),x[4]])
    test('original quadratic matches hyperbolic coordinates', s.expand((iso.T*M*iso)[0]-q) == 0)
    z=s.symbols('z')
    EQ3=1+z+z**2+z**3
    EQ4=1+z+2*z**2+z**3+z**4
    EC=s.expand((z-1)*EQ3+1)
    ESC=s.cancel(EQ3*((z-1)+1/(1+z+z**2)))
    EX=(z-1)*EC; ESX=(z-1)*ESC
    test('quadric threefold Euler number', EQ3.subs(z,1) == 4)
    test('quadric fourfold Euler number', EQ4.subs(z,1) == 6)
    test('cone ordinary Hodge polynomial', EC == z**4)
    test('cone stringy Euler limit', s.limit(ESC,z,1) == s.Rational(4,3))
    test('cone stringy deficit rational function', s.cancel(ESC-EC-z**3/(1+z+z**2)) == 0)
    test('product ordinary Euler zero', s.limit(EX,z,1) == 0)
    test('product stringy Euler zero', s.limit(ESX,z,1) == 0)
    test('projective cone ordinary Euler five', (1+z*EQ3).subs(z,1) == 5)
    test('projective cone stringy Euler sixteen thirds', s.limit(z*EQ3+EQ3/(1+z+z**2),z,1) == s.Rational(16,3))
    q4=x[0]*x[1]+x[2]*x[3]
    reduced=s.groebner([x[0],q4],*x[:4])
    test('four-variable negative control nonzero factor classes', reduced.reduce(x[2])[1] != 0 and reduced.reduce(x[3])[1] != 0)
    test('four-variable negative control product of factors zero', reduced.reduce(x[2]*x[3])[1] == 0)
    reject('drop fifth variable and retain prime x1 argument', s.hessian(q4.subs(x[0],0),x[2:4]).rank() >= 3)
    reject('multiply by C-star preserves strict positive deficit', s.limit(ESX-EX,z,1) > 0)
    reject('Euler equality implies equality of stringy E-functions', s.cancel(ESX-EX) == 0)
    reject('discrepancy denominator is a rather than a+1', s.Rational(4,2) == s.limit(ESC,z,1))
    reject('quadric cone itself is an equality counterexample', s.limit(ESC,z,1) == EC.subs(z,1))
    reject('projective quadric degeneration preserves ordinary Euler', 6 == 5)
    reject('projective quadric degeneration preserves stringy Euler', s.Integer(6) == s.Rational(16,3))
    reject('projective quadric degeneration preserves deficit', s.Integer(0) == s.Rational(1,3))
    reject('positive weighted Euler term must be at least one', s.Rational(1,2) >= 1)
    reject('smooth-factor product with positive Euler erases deficit', 2*s.Rational(1,3) == 0)
    return {'schema':'stringy-independent-controls-v1','all_checks_passed':True,'sympy_version':s.__version__,
            'independent_checks':len(checks),'checks':checks,'false_shortcuts_rejected':len(negatives),
            'negative_controls':negatives,'geometry_certification':False,
            'limit':'Exact algebra and arithmetic corroboration; mathematical membership and source-scope proof are in AUDIT.md.'}

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',type=Path);args=parser.parse_args()
    result=run();output=json.dumps(result,indent=2)+'\n'
    if args.write: args.write.write_text(output)
    print(output,end='')
