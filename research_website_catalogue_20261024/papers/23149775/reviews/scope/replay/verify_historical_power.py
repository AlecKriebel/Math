"""Independently reproduce center_power.pdf pp7-8 supplied scalar power proof."""
import sympy as s
h,z,w,S=s.symbols('h z w S',real=True)
rho=(1-h*h)/2
f=2*(1-z)*S/(rho-2*z+2)
g=(rho*z-z*z+rho+1-w)*S/((1+z)*(rho-2*z+2))
k=(rho*z-z*z+rho+1+w)*S/((1+z)*(rho-2*z+2))
w2=(1-z*z)*(h*h-(z-rho)**2)
def check(label,expr):
    num,den=s.together(expr).as_numer_denom()
    residual=s.factor(s.rem(s.Poly(num,w),s.Poly(w*w-w2,w)).as_expr())
    print(label,'residual=',residual,'denominator=',s.factor(den))
    assert residual==0,(label,residual)
Q=f*f+g*g+k*k-2*f*g-2*g*k-2*k*f
product=f*g*k
orig=-(f**3+g**3+k**3-f*f*(g+k)-g*g*(k+f)-k*k*(f+g)+6*product)*product/Q**2
bevan=-12*product**2/Q**2
DD=4*(3+h*h)*S*S/(9-h*h)**2
XX=4*(1+h)*S*S/((3-h)*(3+h)**2)
YY=4*(1-h)*S*S/((3+h)*(3-h)**2)
check('sidelength sum equals 2s',f+g+k-2*S)
check('original P3 equals -D',orig+DD)
check('Bevan P3 equals -48s^2/(9-h^2)^2',bevan+48*S*S/(9-h*h)**2)
check('D^2=X^2-XY+Y^2',DD**2-XX**2+XX*YY-YY**2)
check('Bevan P3 equals -X-Y-2D',-48*S*S/(9-h*h)**2+XX+YY+2*DD)
print('This reproduces the supplied scalar side-parameter algebra; no all-period focal argument or generic vertex-locus CAS is used.')
