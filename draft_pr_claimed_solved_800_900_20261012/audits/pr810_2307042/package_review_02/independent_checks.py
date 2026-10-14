"""Fresh diagnostic, using Machin pi and independently separated cylinder modes.
The analytic proof is independent_derivation.md; arithmetic is not interval-certified.
"""
from decimal import Decimal as D, localcontext
from pathlib import Path
import json

def compute(prec):
 with localcontext() as ctx:
  ctx.prec=prec
  one=D(1);two=D(2)
  def atan(q):
   n=0;t=q;total=q
   while True:
    n+=1;t*=-q*q;new=total+t/(2*n+1)
    if new==total:return total
    total=new
  pi=16*atan(one/5)-4*atan(one/239)
  def trig(t):
   t=t%(2*pi)
   if t>pi:t-=2*pi
   a=t;b=one;s=t;c=one;n=0
   while True:
    n+=1;a*=-t*t/((2*n)*(2*n+1));b*=-t*t/((2*n-1)*(2*n))
    ns=s+a;nc=c+b
    if ns==s and nc==c:return s,c
    s,c=ns,nc
  def cosh(t):
   e=t.exp();return (e+1/e)/2
  def sinh(t):
   e=t.exp();return (e-1/e)/2
  def lp(t):
   # Independent stable atanh expansion for log(1+t).
   q=t/(2+t);term=q;total=q;n=0
   while True:
    n+=1;term*=q*q;new=total+term/(2*n+1)
    if new==total:return 2*total
    total=new
  def image(x,y,eta):
   sx,cx=trig(pi*x)
   return sum((sx/(2*(cosh(pi*(y-eta+2*pi*k))-cx)) for k in range(-16,17)),D(0))
  def green(x,y,s,eta):
   sx,_=trig(pi*x);ss,_=trig(pi*s);_,cm=trig(pi*(x-s))
   return sum((lp(2*sx*ss/(cosh(pi*(y-eta+2*pi*k))-cm))/2 for k in range(-16,17)),D(0))
  def modes(x,y,derivative=False):
   ans=-1/(2*pi) if derivative else (1-x)/(2*pi)
   st,ct=trig(y-pi);sn=D(0);cn=one
   for n in range(1,1201):
    sn,cn=sn*ct+cn*st,cn*ct-sn*st
    coeff=-n*cosh(n*(1-x))/sinh(D(n)) if derivative else sinh(n*(1-x))/sinh(D(n))
    ans+=coeff*cn/pi
   return ans
  half=D('.5');zero=D(0);P=image(half,zero,pi)
  c=-modes(half,zero,True)/P
  b=1/(2*cosh(half));minimum=(1-c)*b/(1+b*b).sqrt()
  discrepancies=[]
  for xs,ys in [('.2','-2'),('.35','.27'),('.5','0'),('.73','-.4'),('.95','2.8')]:
   x,y=D(xs),D(ys);im=image(x,y,pi);fm=modes(x,y)
   # Analytic tail from independently separated coefficients.
   tail=(-x*1201).exp()/(pi*(1-D(-2).exp())*(1-(-x).exp()))
   image_tail=4*(pi*abs(y-pi)-2*pi*pi*17).exp()/(1-(-2*pi*pi).exp())
   tail+=image_tail
   delta=abs(im-fm)
   assert delta<tail+D(10)**(-prec+10)
   discrepancies.append({'x':xs,'y':ys,'discrepancy':str(delta),'fourier_tail_bound':str(tail)})
  approach=[]
  for eps in [D('1e-5'),D('1e-10'),D('1e-20'),D('1e-40')]:
   s=D('1e-300');eta=pi+eps;x=D('.35');y=D('.27')
   ratio=green(x,y,s,eta)/green(half,zero,s,eta)
   expected=image(x,y,pi)/P
   approach.append({'eta_offset':str(eps),'s':'1e-300','error':str(abs(ratio-expected))})
  assert D(approach[-1]['error'])<D('1e-35')
  return {'precision':prec,'pi_machin':str(pi),'P_base':str(P),'c_fourier':str(c),'b':str(b),'minimum_slope_formula':str(minimum),'mode_checks':discrepancies,'severe_tangential_approaches':approach}
rows=[compute(140),compute(180)]
assert abs(D(rows[0]['c_fourier'])-D(rows[1]['c_fourier']))<D('1e-120')
result={'status':'PASS','rounding_limit':'Decimal arithmetic and precision stability are diagnostics, not certified interval enclosures. Finite samples do not prove unrestricted convergence or a neighborhood radius.','runs':rows}
Path(__file__).with_name('independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','c':rows[-1]['c_fourier'],'minimum_slope':rows[-1]['minimum_slope_formula'],'final_tangential_error':rows[-1]['severe_tangential_approaches'][-1]['error']},indent=2))
