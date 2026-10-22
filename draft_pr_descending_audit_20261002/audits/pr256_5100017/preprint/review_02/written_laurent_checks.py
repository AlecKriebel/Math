"""Focused checks of the manuscript's displayed local complex formulas."""
from pathlib import Path
from datetime import datetime,timezone
import sympy as s
import json
x,y,h,k,t,tb,H,e,D=s.symbols('x y h k t tb H e D',nonzero=True)
checked=[]
def eq(name,value):
 assert s.factor(s.together(value))==0,name
 checked.append(name)
Z,W=x*x,y*y
Vi,Vj=h*x-t*Z,k*y-t*W
ci,cj=h/x-tb/Z,k/y-tb/W
raw=(ci*Vj-Vi*cj)*(Vi+Vj)
paired=s.expand((raw+raw.subs({h:-h,k:-k},simultaneous=True))/2)
p=s.Poly(paired,t,tb)
c=k*k*x*x-h*h*y*y+2*h*k*(x**3/y-y**3/x)
b=h*h*x*x/(y*y)-k*k*y*y/(x*x)+h*k*(x/y-y/x)
eq('paired coefficient t',p.coeff_monomial(t)-c)
eq('paired coefficient conjugate t',p.coeff_monomial(tb)-b)
for degree in [(0,0),(2,0),(1,1),(0,2),(3,0),(1,2),(0,3)]:
 eq('paired absent monomial '+str(degree),p.coeff_monomial(t**degree[0]*tb**degree[1]))
eq('paired cubic coefficient',p.coeff_monomial(t*t*tb)-(Z/W-W/Z)*(Z+W))
h2=H+e*(x*x+x**(-2))/2
k2=H+e*(y*y+y**(-2))/2
hk=D*(y/x+x/y)/2+e*(x*y+1/(x*y))/2
def support_sub(expr):
 p=s.Poly(s.expand(expr),h,k)
 return p.coeff_monomial(h*h)*h2+p.coeff_monomial(k*k)*k2+p.coeff_monomial(h*k)*hk
r=Z/W-W/Z
ss=Z*Z/W-W*W/Z
eq('written c support reduction',support_sub(c)-(D*ss+3*e*r/2+(D+H)*(Z-W)+e*(Z*Z-W*W)))
eq('written b support reduction',support_sub(b)-((D/2+H)*r+e*ss/2+e*(Z-W)/2+e*(1/W-1/Z)))
eq('written s local telescope',ss+(W/Z-Z/W)*(Z+W)-(W-Z))
receipt={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','assertion_count':len(checked),'checks':checked,'sympy_version':s.__version__}
(Path(__file__).resolve().parent/'WRITTEN_LAURENT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(f'PASS: {len(checked)} manuscript-local Laurent assertions')
