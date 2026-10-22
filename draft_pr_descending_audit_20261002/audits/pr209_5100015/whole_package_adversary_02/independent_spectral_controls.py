"""Independent nome/Fourier falsification, not imported from the package.

Exact truncated Laurent-series checks and arbitrary precision real diagnostics.
These finite checks are not a universal or interval proof.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
import json, math
import mpmath as mp
import sympy as sp

O=Path(__file__).resolve().parent
ORDER=32
series={(0,0):1}
for ell in range(1,ORDER+1):
    for j in range((ORDER//ell+1)//2):
        power=ell*(2*j+1)
        if power<=ORDER:
            for sign in (-1,1):series[power,sign*ell]=2*(-1)**j
out=defaultdict(int); mutant=defaultdict(int)
for (p,l),a in series.items():
    for (r,h),b in series.items():
        if p+r<=ORDER:
            out[p+r,l+h]+=a*b*(-1 if h%2 else 1)
            mutant[p+r,l+h]+=a*b
assert all(val==0 for (power,harmonic),val in out.items() if harmonic)
assert any(val!=0 for (power,harmonic),val in mutant.items() if harmonic)

# Generic period-four pair in any noncircular ellipse, without Jacobi functions.
a,b=sp.symbols('a b', positive=True)
s=a*a+b*b
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def area(pp):return sum(det(pp[i],pp[(i+1)%len(pp)]) for i in range(len(pp)))/2
def geometry(pp,A,B):
    nn=[(x/A**2,y/B**2) for x,y in pp];rr=[];ff=[]
    for n,m in zip(nn,nn[1:]+nn[:1]):
        D=det(n,m);rr.append(((m[1]-n[1])/D,(n[0]-m[0])/D))
        ff.append((n[0]/dot(n,n),n[1]/dot(n,n)))
    return area(rr),area(ff)
diamond=[(a,0),(0,b),(-a,0),(0,-b)]
rectangle=[(a*a/sp.sqrt(s),b*b/sp.sqrt(s)),(-a*a/sp.sqrt(s),b*b/sp.sqrt(s)),(-a*a/sp.sqrt(s),-b*b/sp.sqrt(s)),(a*a/sp.sqrt(s),-b*b/sp.sqrt(s))]
pd=sp.factor(sp.prod(geometry(diamond,a,b)))
pr=sp.factor(sp.prod(geometry(rectangle,a,b)))
assert sp.simplify(pd-8*a*a*b*b)==0
assert sp.simplify(pr-2*s*s)==0
assert sp.factor(pr-pd)==2*(a-b)**2*(a+b)**2

mp.mp.dps=100
rows=[];maximum=mp.mpf(0)
for ktext in ['0.003','0.77','0.9999999']:
    k=mp.mpf(ktext);m=k*k;K=mp.ellipk(m);Ki=mp.ellipk(1-m);nome=mp.exp(-mp.pi*Ki/K);kp=mp.sqrt(1-m)
    for q in [1,3,9,17,31]:
        t=nome**q
        # Independent Fourier construction, with a real-axis absolute tail bound.
        terms=math.ceil(float((110*mp.log(10))/(-mp.log(t))))+3
        def U(z):
            theta=q*mp.pi*z/K
            return q*mp.pi/(2*K)*(1+4*sum(t**ell/(1+t**(2*ell))*mp.cos(ell*theta) for ell in range(1,terms+1)))
        tail=2*q*mp.pi/K*t**(terms+1)/(1-t)
        assert tail<mp.mpf('1e-105')
        C=mp.fprod((mp.ellipfun('cn',2*K*j/q,m)/mp.ellipfun('sn',2*K*j/q,m))**2 for j in range(1,(q-1)//2+1))
        constant=kp**q/C**2
        errs=[]
        for frac in ['0','0.0000001','0.1732050807568877','0.6180339887498948','1.9999997']:
            z=mp.mpf(frac)*K
            direct=sum(mp.ellipfun('dn',z+2*K*j/q,m) for j in range(q))
            errs.extend([abs(U(z)-direct)/max(1,abs(direct)),abs(U(z)*U(z+K)-constant)/max(1,abs(constant))])
        e=max(errs);maximum=max(maximum,e);assert e<mp.mpf('1e-85')
        rows.append(dict(k=ktext,q=q,real_phases=5,fourier_terms=terms,tail_bound=str(tail),maximum_scaled_error=mp.nstr(e,16)))

circle=[]
for N,tau in [(3,1),(4,1),(9,4),(18,7),(31,15),(62,29)]:
    R=mp.mpf(5);v=mp.pi*tau/N;vals=[]
    for phase in [mp.mpf(0),mp.sqrt(2),mp.sqrt(3)]:
        pp=[(R*mp.cos(phase+2*j*v),R*mp.sin(phase+2*j*v)) for j in range(N)]
        outer,pedal=geometry(pp,R,R);expected=N*N*R**4*mp.sin(v)**2
        assert abs(outer*pedal-expected)/expected<mp.mpf('1e-90')
        vals.append(mp.nstr(outer*pedal,30))
    circle.append(dict(N=N,tau=tau,phases=3,products=vals,includes_excluded_elliptic_parity=N%4==0))
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',mechanism='Exact Laurent nome series and independent dn Fourier spectral projection, plus generic Cartesian period-four and circle controls',exact_nome_order=ORDER,series_terms=len(series),product_coefficients_checked=len(out),nonconstant_coefficients_all_zero=True,wrong_even_q_shift_rejected=True,constant_nome_polynomial={str(p):v for (p,h),v in out.items() if h==0 and v},generic_four_products=[str(pd),str(pr)],generic_four_difference=str(sp.factor(pr-pd)),spectral_families=rows,circle_controls=circle,maximum_scaled_error=mp.nstr(maximum,16),mpmath_version=mp.__version__,sympy_version=sp.__version__,limitations='Exact formal series check is finite to nome degree 32. Floating-point diagnostics are not interval certificates; stated tails bound truncation only, not floating rounding. No scientific candidate program imported or run.')
(O/'INDEPENDENT_SPECTRAL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('spectral_families','circle_controls','constant_nome_polynomial')},indent=2))
