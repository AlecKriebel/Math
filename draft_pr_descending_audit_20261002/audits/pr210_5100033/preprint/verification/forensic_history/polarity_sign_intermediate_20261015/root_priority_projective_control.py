"""Fresh exact geometric equivalence controls for the PR210 priority audit.
No outside theorem or priority conclusion follows from this algebra.
"""
import json
import sympy as s
A,B,lam,X,Y,x,y=s.symbols('A B lam X Y x y',positive=True)
c=s.sqrt(A-B);U=A-lam;V=B-lam
checks={}
def zero(label,expr):
 val=s.factor(s.cancel(expr));assert val==0,(label,val);checks[label]=str(val)
fx=A*(x+c)/(A+c*x);fy=A*y/(A+c*x)
ix=A*(X-c)/(A-c*X);iy=B*Y/(A-c*X)
zero('inverse_x',fx.subs({x:ix,y:iy},simultaneous=True)-X)
zero('inverse_y',fy.subs({x:ix,y:iy},simultaneous=True)-Y)
image=s.factor((ix**2/U+iy**2/V-1)*(A-c*X)**2)
ux=A*A/U-c*c;vy=B*B/V;ell=c*A*lam/U
conic=ux*X*X+vy*Y*Y-2*ell*X-A*A*V/U
zero('image_caustic_conic',image-conic)
zero('noncircular_coefficient_gap',vy-ux-(A-B)*lam**2/(U*V))
h=ell/ux;R2=ell**2/ux+A*A*V/U
zero('image_ellipse_focus_at_circle_center',R2*(1/ux-1/vy)-h*h)
zero('ux_positive_formula',ux-(A*B+(A-B)*lam)/U)
zero('strict_confocal_nonhomothetic_ratio',A/U-B/V+(A-B)*lam/(U*V))
# Polar dual wrt radius-a auxiliary circle: point (X,Y) represents
# line (X/A,Y/A).X_old=1. Track the PLUS-focus convention literally.
ss=A*A*V/U;matrix=s.Matrix([[ux,0,-ell],[0,vy,0],[-ell,0,-ss]])
Z=s.Matrix([X/A,Y/A,1]);dual=(Z.T*matrix.adjugate()*Z)[0]
dual_lead=-vy*ss/(A*A)
circle_center=c*lam/V;circle_radius_squared=U*B*B/(V*V)
circle_form=X*X+Y*Y-2*circle_center*X+circle_center**2-circle_radius_squared
zero('polar_image_is_bicentric_outer_circle_with_correct_plus_sign',dual/dual_lead-circle_form)
# Exact genuine triangular caustic example, all inequalities literal.
val={A:s.Integer(21),B:s.Integer(16),lam:s.Rational(336,25)}
aX=s.factor((R2/ux).subs(val));aY=s.factor((R2/vy).subs(val));hh=s.factor(h.subs(val))
assert aX>aY>0 and hh>0 and s.simplify(aX-aY-hh**2)==0
# Plus/minus normalized auxiliary-circle maps are Mobius conjugates.
z,t=s.symbols('z t');e=2*t/(1+t*t);M=lambda zz,tt:(zz+tt)/(1+tt*zz)
zero('focus_switch_Mobius_map',M(M(z,t),-e)-M(z,-t))
out=dict(status='PASS finite exact symbolic equivalence controls',sympy=s.__version__,domain='A>B>0 and 0<lambda<B; all denominators positive on real boundary',checks=checks,projective_map='X=A(x+c)/(A+cx), Y=A y/(A+cx)',image_caustic='ux X^2+vy Y^2-2ell X-A^2 V/U=0',image_coefficients=dict(ux=str(s.factor(ux)),vy=str(s.factor(vy)),ell=str(s.factor(ell))),image_ellipse_foci='0 and 2h on the x-axis, h=ell/ux',polar_dual_circle=dict(plus_focus_center_x=str(circle_center),radius_squared=str(circle_radius_squared),auxiliary_inner_circle_center='0',auxiliary_inner_circle_radius='sqrt(A)',mutually_concentric=False,exact_triangle_center_x=str(s.simplify(circle_center.subs(val))),exact_triangle_radius_squared=str(s.simplify(circle_radius_squared.subs(val)))),image_is_not_circle_for_strict_domain=True,exact_triangle_example=dict(center_x=str(hh),squared_major_semiaxis=str(aX),squared_minor_semiaxis=str(aY),focus_square=str(s.factor(hh**2))),limits='Algebraic equivalence used to examine prior general Poncelet theorems. No new invariant proof, claim of novelty, bicentric circle/circle reduction, or prior-coverage conclusion.')
print(json.dumps(out,indent=2))
