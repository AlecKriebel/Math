"""Exact coefficient identities for the N=3 implication of old results.

This checks universal rational algebra modulo D^2=X^2-XY+Y^2. It does not
numerically certify or presume the old geometric statements listed in the note.
"""
import sympy as s
X,Y,D=s.symbols('X Y D',positive=True)
c2=X-Y;n=X-D;m=D-Y
rho=2*m*n/c2**2
AI2=m**2/X;BI2=n**2/Y;AO2=n**2/(4*X);BO2=m**2/(4*Y)
relation=D**2-X**2+X*Y-Y**2
def check(name,expr):
    numerator,denominator=s.together(expr).as_numer_denom()
    residual=s.factor(s.rem(s.Poly(numerator,D),s.Poly(relation,D)).as_expr())
    assert residual==0,(name,residual)
    print(name+': exact polynomial residual 0; denominator '+str(s.factor(denominator)))
alpha=1-BI2/AI2
beta=1-BO2/AO2
check('constant term of |I|^2+4rho|O|^2',BI2+4*rho*BO2-(X+Y-4*rho*D))
check('coefficient gives I_x^2=4m^2/n^2 O_x^2',4*rho*beta+4*alpha*m**2/n**2)
check('major-axis dot product fixes negative sign',X+Y-2*D+AI2+2*n*m/X)
check('Bevan longitudinal ratio equals focal power ratio',2+2*m/n-2*(Y+D)/(D-X+Y))
check('alpha numerator factorization',m**2*Y-n**2*X-2*(X-Y)*(D*(X+Y)-X**2-Y**2))
check('strict-positive alpha squared comparison',D**2*(X+Y)**2-(X**2+Y**2)**2-X*Y*(X-Y)**2)
xx,yy,dd=s.Integer(21),s.Integer(16),s.Integer(19)
U=D-c2;V=X+Y+2*D-c2
C0=s.factor(V/(2*rho*U))
assert C0.subs({X:xx,Y:yy,D:dd})==s.Rational(125,24)
print('rho =',rho)
print('I_x/O_x = -2(D-Y)/(X-D) after the analytic sign argument')
print('N3 common multiplier =',C0)
print('exact axes-squared (21,16) multiplier = 125/24')
print('SCOPE: coefficient algebra only; geometric inputs and sign/domain arguments are separately proved/read in ROOT_TRIANGULAR_OLD_IMPLICATION.md.')
