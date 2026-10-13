"""Independent symbolic checks of displayed external-paper algebra.

Does not import the external checkers or our candidate proof.
Run with SymPy 1.14.0. All assertions concern rational identities after
explicit substitution of the stated algebraic constraints.
"""
from pathlib import Path
import json
import sympy as s

checks = {}
def check(name, expr):
    residual = s.factor(s.cancel(expr))
    checks[name] = str(residual)
    assert residual == 0, (name, residual)

a, b, c, X, Y, lam = s.symbols('a b c X Y lam', real=True)
alpha, beta, W, U, z, C2 = s.symbols('alpha beta W U z C2')
d = alpha-beta; D=alpha*beta; S=alpha+beta; L=D-S*lam
J=(alpha-lam)*(beta-lam)

# Reflection product difference, divided by 2*h*j.
check('velocity_product_coefficient',
      (beta*X**2-alpha*(1-X**2))/(beta*X**2+alpha*(1-X**2))
      - (2*D-S*(beta*X**2+alpha*(1-X**2)))/
      (d*(beta*X**2+alpha*(1-X**2))))

# Projection identity in the orthonormal (n,t) frame: Q=P-v*(u dot v).
pn, pt, un, ut, h, j = s.symbols('pn pt un ut h j')
P=s.Matrix([pn,pt]); up=s.Matrix([un,ut])
vm=s.Matrix([j,h]); vp=s.Matrix([-j,h])
qm=P-vm*(up.dot(vm)); qp=P-vp*(up.dot(vp))
check('pedal_ordered_half_determinant',
      s.det(s.Matrix.hstack(qm,qp))/2-
      h*j*(pn*un-pt*ut+ut**2*h**2-un**2*j**2))

# Eliminate b^2 and Y^2 in the focal frame; no square root remains.
B=a**2-c**2; WW=a**2-c**2*X**2
pnun=a*B*(a-c*X)/WW
ptut=-c**3*X*(1-X**2)*(a-c*X)/WW
ut2=c**2*(1-X**2)*(a-c*X)**2/WW
un2=B*(a-c*X)**2/WW
bracket=pnun-ptut+ut2*(WW-lam)/WW-un2*lam/WW
check('focal_pedal_bracket',bracket-(a-c*X)*(a*(WW-lam)+c*X*lam)/WW)
f=(a*a-lam+a*c*X)/(a+c*X)**2
check('focal_pedal_single_term',bracket/WW-f)
check('focal_pedal_opposite_pair', f+f.subs(X,-X)-2*((a*a+lam)/WW-2*a*a*lam/WW**2))
check('pedal_after_velocity_telescope',alpha+lam-2*alpha*lam*S/(2*D)-alpha*(beta-lam)/beta)

# Half-gap discriminant and rational Jacobi quarter shift.
check('half_gap_discriminant',
      ((lam*d*X*Y)**2+lam*W*(L+lam*W)-lam*D*(W-lam))
      .subs(W,beta+d*Y**2).subs(X**2,1-Y**2))
S0=s.symbols('sn_squared')
k2=d/(alpha-lam); W0=alpha-d*S0
Wshift=alpha-d*(1-S0)/(1-k2*S0)
check('quarter_shift_W',Wshift-(lam*W0+L)/(W0-lam))
Wp=(lam*W+L)/(W-lam)
check('quarter_shift_W_minus_lambda',Wp-lam-J/(W-lam))
check('quarter_shift_outer_denominator',L+lam*Wp-J*W/(W-lam))
check('quarter_shift_outer_trace', (W-lam)/(J*W)-1/(J*W/(W-lam)))
check('pedal_to_outer_factor',
      (alpha*(beta-lam)/beta)/(D/s.sqrt(J))-s.sqrt(J)*(beta-lam)/beta**2)

# Derive the antipedal numerator from distances and a chord length.
M, ss, V=s.symbols('M ss V')
rprod=(M**2-V*ss)**2
rsum=2*(M**2+V*ss)
udot=M**2+V*ss-2*U*ss
check('antipedal_numerator',
      (rprod-rsum*udot/2).subs(V,U-beta)-2*ss*((2*beta-U)*M**2+U*(U-beta)*ss))
C=s.symbols('C')
H=(2*beta-U)*(a-z*C)**2+U*(U-beta)*(1-C**2)
pair=(H/(a*C-z)+H.subs(z,-z)/(a*C+z))/(2*a*beta*C)
paired_closed=((2*beta-U)*(a*a+z*z*C*C-2*z*z)+U*(U-beta)*(1-C*C))/(beta*(a*a*C*C-z*z))
check('antipedal_opposite_fraction',pair-paired_closed)
pairU=paired_closed.subs(a*a,alpha).subs(z*z,alpha-U).subs(C*C,1-lam*U/D)
check('antipedal_paired_ratio',pairU-(2-L*U/(D*(beta-lam))))
check('antipedal_transversality_product',
      (alpha*(1-lam*U/D)-(alpha-U))-U*(beta-lam)/beta)
R=(D*(3*beta-alpha)+lam*d*d)/(2*D*(beta-lam))
check('antipedal_total_factor',2-S*L/(2*D*(beta-lam))-R)
check('four_period_R',R.subs(lam,D/S)-2)
check('four_period_K_squared',
      (J*(beta-lam)**2/beta**4).subs(lam,D/S)-(D/S**2)**2)

# Gradient determinant and conic intersection values.
xx=alpha*(alpha-lam)/d; yy=-beta*(beta-lam)/d
check('boundary_at_complex_intersections',xx/alpha+yy/beta-1)
check('caustic_at_complex_intersections',xx/(alpha-lam)+yy/(beta-lam)-1)
check('gradient_determinant_coefficient',
      1/(alpha*(beta-lam))-1/(beta*(alpha-lam))-lam*d/(D*J))

out={'sympy_version':s.__version__,'identity_count':len(checks),'all_exact_residuals_zero':True,'checks':checks}
Path(__file__).with_name('INDEPENDENT_ALGEBRA.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
