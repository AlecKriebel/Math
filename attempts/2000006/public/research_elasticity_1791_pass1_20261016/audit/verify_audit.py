#!/usr/bin/env python3
"""Exact algebra checks supplementing, not replacing, the written audit."""
import json
from pathlib import Path
import sympy as s

t = s.symbols('t', real=True)
a, b, c, d = s.symbols('a b c d', positive=True)
eye = s.eye(3)

def norm2(M):
    return sum(z*z for z in M)

def W(F):
    C, J = F.cofactor_matrix(), F.det()
    return a*norm2(F)**3 + b*norm2(C)**s.Rational(3,2) + c*J**2 + d/J**2

matrices = [s.diag(2, 3, 4), s.Matrix([[1,1,0],[0,2,1],[1,0,3]]),
            s.Matrix([[2,1,-1],[1,3,0],[0,2,2]])]
checks = []
for index, F in enumerate(matrices):
    assert F.det() > 0
    C, J = F.cofactor_matrix(), F.det()
    T = 6*a*norm2(F)**2*F*F.T + 3*b*s.sqrt(norm2(C))*(norm2(C)*eye-C*C.T) + (2*c*J**2-2*d/J**2)*eye
    U = 6*a*norm2(F)**2*F.T*F + 3*b*s.sqrt(norm2(C))*(norm2(C)*eye-C.T*C) + (2*c*J**2-2*d/J**2)*eye
    for i in range(3):
        for j in range(3):
            H = s.zeros(3); H[i,j] = 1
            left = s.diff(W((eye+t*H)*F), t).subs(t, 0)
            right = s.diff(W(F*(eye+t*H)), t).subs(t, 0)
            assert s.simplify(left-T[i,j]) == 0
            assert s.simplify(right-U[i,j]) == 0
    checks.append({'matrix': index, 'determinant': int(J), 'left_and_right_directions': 18, 'passed': True})

u, v, j = s.symbols('u v j', real=True, positive=True)
F = s.Matrix([[1,0,0],[0,1,0],[u,v,j]])
C = F.cofactor_matrix()
assert C == s.Matrix([[j,0,-u],[0,j,-v],[0,0,1]])
p33 = s.diff(W(F), j)
expected = 6*a*norm2(F)**2*j+6*b*s.sqrt(norm2(C))*j+2*c*j-2*d/j**3
assert s.simplify(p33-expected) == 0

alpha = s.symbols('alpha', positive=True)
gain = alpha**(-2)/(9-6*alpha)-s.Rational(1,3)
factor = (alpha-1)**2*(2*alpha+1)/(3*alpha**2*(3-2*alpha))
assert s.factor(gain-factor) == 0

result = {'purpose': 'Exact supplementary checks; these do not prove minimization or resolve E-6322.',
          'stress_checks': checks, 'triangular_cofactor_and_piola_33': 'passed',
          'homogeneous_core_gain_factorization': 'passed'}
out = Path(__file__).with_name('AUDIT_CHECKS.json')
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
