import sympy as S,json
r,l,t,x=S.symbols('r l t x');count=0
mod=S.Poly(r*r-5,r)
def zero(e):
 num=S.cancel(e).as_numer_denom()[0]
 return S.Poly(S.expand(num),r).rem(mod).is_zero
phi=(1+r)/2;c=(11+5*r)/2;d=5+2*r
f=t**4+3*t**3+4*t*t+2*t+1;g=t**4-2*t**3+4*t*t-3*t+1;R=t*f/g
eps=(phi*t+1)/(t-phi);iota=lambda v:(c*v+1)/(v-c)
assert zero(R-iota(eps**5));count+=1
assert S.cancel(S.diff(R,t)-(t*t-t-1)**4/g**2)==0;count+=1
beta=(11-5*r)*l/(2*(l+5*r));assert zero(iota(beta)+1/(l+c));count+=1
assert zero(iota(iota(t))-t);count+=1
assert zero(((phi*eps+1)/(eps-phi))-t);count+=1
# Exact twist polynomial, independently entered from the claimed model.
a0=5-2*r;a1=(-26+10*r)*l-20*r;a2=(42-S.Rational(86,5)*r)*l*l+(-100+100*r)*l+500+200*r;a3=(-112+48*r)*l*l*(l+5*r)/5
k=4*(l+5*r)/r;q=d*k*k;xi=q*(x-beta)
T=4*x**3+(beta*beta-6*beta+1)*x*x+2*(beta*beta-beta)*x+beta*beta
assert zero(xi**3+a2*xi**2+a1*a3*xi+a0*a3*a3-q**3*T/4);count+=1
# Check rational parameter specializations of the cubic discriminant independently.
for v in range(-10,11):
 if v==0:continue
 aa=[S.expand(z.subs(l,v)) for z in [a0,a1,a2,a3]]
 poly=x**3+aa[2]*x*x+aa[1]*aa[3]*x+aa[0]*aa[3]**2
 disc=16*S.discriminant(poly,x)
 expected=2**24*(161-72*r)*v**5*(v+5*r)**5*(v+c)
 assert zero(disc-expected);count+=1
# Degree-ten division remainder: no overlap with known x-coordinates generically.
b=S.symbols('b');b2=b*b-6*b+1;b4=b*b-b;b6=b*b;b8=-b**3
TT=4*x**3+b2*x*x+2*b4*x+b6
p3=3*x**4+b2*x**3+3*b4*x*x+3*b6*x+b8
h6=2*x**6+b2*x**5+5*b4*x**4+10*b6*x**3+10*b8*x*x+(b2*b8-b4*b6)*x+b4*b8-b6*b6
p5=S.expand(TT**2*h6-p3**3);rr,rem=S.div(p5,x*(x-b),x);assert rem==0 and S.degree(rr,x)==10;count+=1
assert S.expand(rr).coeff(x,0)==5*b**8;count+=1
assert S.factor(rr.subs(x,b))==5*b**12;count+=1
print(json.dumps({'status':'PASS','assertions':count,'discriminant_specializations':20,'full_level_cover_derivative':'(t^2-t-1)^4/g(t)^2'},sort_keys=True))
