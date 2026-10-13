#!/usr/bin/env python3
"""Fresh diagnostic checks, independent of supplied diagnostic. Not a proof."""
from pathlib import Path
import sys,json,datetime,math
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
import mpmath as m
m.mp.dps=100
pi=m.pi
N=20
F=1200

def p(x,t):return m.sin(pi*x)/(2*(m.cosh(pi*t)-m.cos(pi*x)))
def P(x,y,eta=pi):return m.fsum(p(x,y-eta+2*pi*k) for k in range(-N,N+1))
def G(x,y,s,eta):
 return m.fsum(m.log1p(2*m.sin(pi*x)*m.sin(pi*s)/(m.cosh(pi*(y-eta+2*pi*k))-m.cos(pi*(x-s))))/2 for k in range(-N,N+1))
def fourier(x,y):
 return (1-x)/(2*pi)+m.fsum((m.exp(-n*x)-m.exp(-n*(2-x)))/(1-m.exp(-2*n))*m.cos(n*(y-pi))/pi for n in range(1,F+1))
def ftail(x):return m.exp(-(F+1)*x)/(pi*(1-m.exp(-2))*(1-m.exp(-x)))
def itail(y):return 4*m.exp(pi*abs(y-pi)-2*pi*pi*(N+1))/(1-m.exp(-2*pi*pi))
def fgrad(x,y):return -1/(2*pi)-m.fsum(n*(m.exp(-n*x)+m.exp(-n*(2-x)))/(1-m.exp(-2*n))*m.cos(n*(y-pi))/pi for n in range(1,F+1))
p0=P(m.mpf('.5'),0)
q=[m.sech((2*k-1)*pi*pi) for k in range(-N,N+1)]
c=pi*m.fsum(i*i for i in q)/m.fsum(q);b=1/(2*m.cosh(m.mpf('.5')))
rows=[]
for x,y in [('.2','-2'),('.4','.3'),('.5','0'),('.7','-.4'),('.9','2')]:
 x,y=m.mpf(x),m.mpf(y);err=abs(P(x,y)-fourier(x,y));tail=ftail(x)+itail(y)
 assert err<tail+m.mpf('1e-95')
 rows.append({'x':str(x),'y':str(y),'error':str(err),'analytic_tail_bound':str(tail)})
graderr=abs(fgrad(m.mpf('.5'),0)/p0+c);assert graderr<m.mpf('1e-90')
ratios=[]
for e in [2,4,6,10]:
 eps=m.mpf(10)**(-e);s=eps**20;eta=pi+eps
 err=abs(G(m.mpf('.3'),m.mpf('.2'),s,eta)/G(m.mpf('.5'),0,s,eta)-P(m.mpf('.3'),m.mpf('.2'))/p0)
 ratios.append({'epsilon':str(eps),'s':str(s),'error':str(err)})
assert m.mpf(ratios[-1]['error'])<m.mpf(ratios[0]['error'])*m.mpf('1e-7')
# Symmetry and independently pulled-back conformal expression.
conformal=[]
for x,y,s,eta in [('.3','.2','.1','2.8'),('.7','-.4','.2','3')]:
 x,y,s,eta=map(m.mpf,(x,y,s,eta));w=y+1j*x;wp=eta+1j*s
 single=m.log(abs((m.exp(pi*w)-m.exp(pi*m.conj(wp)))/(m.exp(pi*w)-m.exp(pi*wp))))
 stable=m.log1p(2*m.sin(pi*x)*m.sin(pi*s)/(m.cosh(pi*(y-eta))-m.cos(pi*(x-s))))/2
 assert abs(single-stable)<m.mpf('1e-90')
 assert abs(G(x,y,s,eta)-G(s,eta,x,y))<m.mpf('1e-90')
 conformal.append({'single_formula_error':str(abs(single-stable))})
# Boundary asymptotic in extreme tangential coordinates.
sing=[]
for e in [1,2,4,8]:
 t=m.mpf(10)**(-e);x=t**10;r2=x*x+t*t
 norm=(P(x,pi+t)-x/(pi*r2))/x
 assert abs(norm)<1
 sing.append({'x':str(x),'t':str(t),'remainder_divided_by_x':str(norm)})
# Exact directional minimum: on the adverse half-plane, switch -u=b|v|.
minslope=(1-c)*b/m.sqrt(1+b*b)
assert c>0 and c<m.mpf(8)/83<m.mpf('.1') and b>m.mpf('.25') and minslope>m.mpf('.1')
# High-precision counterexample hunt at the switching directions and coordinate axes.
angles=[0,pi/2,pi,3*pi/2,m.atan(1/b),pi-m.atan(1/b),pi+m.atan(1/b),2*pi-m.atan(1/b)]
mesh=[]
for r in map(m.mpf,['.05','.01','.0001','1e-8','1e-16']):
 gaps=[]
 for a in angles:
  u,v=r*m.cos(a),r*m.sin(a)
  hs=[1+u,1-u,1+b*m.sin(v)*m.cosh(u),1-b*m.sin(v)*m.cosh(u)]
  gaps.append(max(hs)-P(m.mpf('.5')+u,v)/p0)
 assert min(gaps)>0
 mesh.append({'radius':str(r),'minimum_sampled_gap_over_radius':str(min(gaps)/r)})
out={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'all diagnostics passed','scope':'100-digit floating diagnostics and analytic truncation tails; arithmetic rounding unvalidated; no numerical radius or theorem is certified','mpmath_version':m.__version__,'P_A':str(p0),'c':str(c),'b':str(b),'exact_directional_minimum_formula_value':str(minslope),'poisson_image_vs_separation':rows,'gradient_discrepancy':str(graderr),'ultratangential_green_ratios':ratios,'green_conformal_formula_and_symmetry':conformal,'singularity_stress':sing,'switching_directions_actual_gap':mesh}
Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','c','b','gradient_discrepancy']},indent=2))
