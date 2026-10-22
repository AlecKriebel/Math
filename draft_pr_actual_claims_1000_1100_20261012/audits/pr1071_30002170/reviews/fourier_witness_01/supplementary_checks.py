#!/usr/bin/env python3
"""Fresh checks for PR1071. Numerical results supplement, never replace, proof.

Run with the bundled Python (numpy available). The exact polynomial part uses
fractions only. All outputs are local to this review directory.
"""
from pathlib import Path
from fractions import Fraction as Q
import datetime
import hashlib
import json
import math
import platform
import sys
import numpy as np

OUT = Path(__file__).resolve().parent
phi = [Q(0)]*4 + [Q(1),Q(-4),Q(6),Q(-4),Q(1)]

def derivative(p):
    return [Q(k+1)*p[k+1] for k in range(len(p)-1)]

def multiply(p,q):
    r=[Q(0)]*(len(p)+len(q)-1)
    for i,c in enumerate(p):
        for j,d in enumerate(q):
            r[i+j]+=c*d
    return r

def integrate(p):
    return sum((c/Q(i+1) for i,c in enumerate(p)),Q(0))

def value(p,x):
    return sum((c*x**i for i,c in enumerate(p)),Q(0))

f=derivative(phi)
g=phi
a=integrate(multiply(f,f))
b=integrate(multiply(derivative(f),derivative(f)))
assert a==Q(4,45045) and b==Q(24,5005)
exact={"area":str(a),"brownian_f_gram":str(b),
       "brownian_g_gram":str(a),"brownian_sharper_c_squared":str(a/b),
       "endpoint_derivatives":{}}
for name,p in [("f",f),("g",g)]:
    exact["endpoint_derivatives"][name]=[]
    for k in range(4):
        ends=[value(p,Q(0)),value(p,Q(1))]
        if k<3:
            assert ends==[Q(0),Q(0)]
        exact["endpoint_derivatives"][name].append([str(x) for x in ends])
        p=derivative(p)

# Exact centered moments avoid cancellation in the low-frequency transform.
center=[Q(-1,2),Q(1)]
pow_center=[Q(1)]
moments=[]
for k in range(81):
    moments.append(float(integrate(multiply(g,pow_center))))
    pow_center=multiply(pow_center,center)

def endpoints(p):
    vals=[]
    while p:
        vals.append((float(value(p,Q(0))),float(value(p,Q(1)))))
        p=derivative(p)
    return vals

epg=endpoints(g)
epf=endpoints(f)

def transform_endpoint(eta,ep):
    eta=np.asarray(eta,dtype=float)
    z=1j*eta
    e=np.exp(-1j*eta)
    r=np.zeros_like(eta,dtype=complex)
    for k,(p0,p1) in enumerate(ep):
        if p0 or p1:
            r+=(p0-p1*e)/z**(k+1)
    return r

def transform_g(eta):
    eta=np.asarray(eta,dtype=float)
    r=np.zeros_like(eta,dtype=complex)
    lo=np.abs(eta)<=16
    x=eta[lo]
    base=np.zeros_like(x)
    for k in range(40):
        base+=(-1)**k*moments[2*k]*x**(2*k)/math.factorial(2*k)
    r[lo]=np.exp(-.5j*x)*base
    r[~lo]=transform_endpoint(eta[~lo],epg)
    return r

def transform_f(eta):
    return 1j*np.asarray(eta)*transform_g(eta)

def quadrature_grid(limit=256,order=24,width=.5):
    z,w=np.polynomial.legendre.leggauss(order)
    left=np.arange(0,limit,width)
    x=left[:,None]+width*(z[None,:]+1)/2
    ww=np.broadcast_to(width*w[None,:]/2,x.shape)
    return x.ravel(),ww.ravel()

def numeric_L1(p):
    coeff=np.array([float(v) for v in p])
    roots=np.polynomial.polynomial.polyroots(coeff)
    cuts=sorted([0.,1.]+[float(z.real) for z in roots
                        if abs(z.imag)<1e-8 and 0<z.real<1])
    primitive=np.array([0.]+[float(c)/float(k+1) for k,c in enumerate(p)])
    return sum(abs(np.polynomial.polynomial.polyval(y,primitive)-
                   np.polynomial.polynomial.polyval(x,primitive))
               for x,y in zip(cuts,cuts[1:]))

L_f=float(Q(1,128))
L_g=float(Q(1,630))
N_f=numeric_L1(derivative(derivative(derivative(f))))
N_g=numeric_L1(derivative(derivative(derivative(g))))
x,w=quadrature_grid()
gf=transform_g(x)
ff=transform_f(x)

# Fourier derivative identity checked against separately evaluated endpoint
# formula (rather than the transform_f definition itself) at stable eta>=16.
probe=np.array([16.,17.,25.,47.,80.,143.])
derivative_residual=float(np.max(np.abs(
    transform_endpoint(probe,epf)-1j*probe*transform_endpoint(probe,epg))))
assert derivative_residual<1e-12

# Inversion: E[B_t W(u_h)] cancels D_H and is (h(t)-h(0)). Compare
# the correct and incorrect conjugation/sign conventions at t in the support.
inversion=[]
for t in [.2,.37,.5,.8,1.2]:
    for name,hhat,p in [("f",ff,f),("g",gf,g)]:
        correct=float(np.sum(w*2*np.real((np.exp(1j*t*x)-1)*hhat))/(2*math.pi))
        wrong=float(np.sum(w*2*np.real((np.exp(1j*t*x)-1)*np.conj(hhat)))/(2*math.pi))
        expected=float(value(p,Q(str(t)))) if 0<=t<=1 else 0.
        inversion.append({"r":name,"t":t,"correct":correct,
                          "expected":expected,"wrong_sign_control":wrong,
                          "abs_error":abs(correct-expected)})
assert max(v["abs_error"] for v in inversion)<1e-6

H_cases=[.251,.3,.49,.5,.51,.749,.75,.751,.9,.999]
theta=np.linspace(-math.pi,math.pi,101)
ell=np.arange(-40,41)
eta=(theta[:,None]+2*math.pi*ell[None,:]).ravel()
period_g=transform_g(eta).reshape(len(theta),len(ell))
period_f=(1j*eta*transform_g(eta)).reshape(len(theta),len(ell))
weights=w
records=[]
for H in H_cases:
    alpha=2*H+1
    D=2*math.pi/(math.gamma(1+2*H)*math.sin(math.pi*H))
    Pbar_f=math.pi**alpha*L_f**2+2*N_f**2*math.pi**(alpha-6)*(1+1/(2*(5-alpha)))
    Pbar_g=math.pi**alpha*L_g**2+2*N_g**2*math.pi**(alpha-6)*(1+1/(2*(5-alpha)))
    Mf=D/(2*math.pi)*Pbar_f
    Mg=D/(2*math.pi)*Pbar_g
    pf=(np.abs(eta).reshape(period_f.shape)**alpha*np.abs(period_f)**2).sum(axis=1)
    pg=(np.abs(eta).reshape(period_g.shape)**alpha*np.abs(period_g)**2).sum(axis=1)
    rows=[]
    for n in [1,2,8]:
        lag=np.arange(n)
        wf=2*weights*x**alpha*np.abs(ff)**2*D/(4*math.pi**2)
        wg=2*weights*x**alpha*np.abs(gf)**2*D/(4*math.pi**2)
        Af=np.array([float(np.sum(wf*np.cos(k*x))) for k in lag])
        Cg=np.array([float(np.sum(wg*np.cos(k*x))) for k in lag])
        A=Af[np.abs(np.arange(n)[:,None]-np.arange(n)[None,:])]
        C=Cg[np.abs(np.arange(n)[:,None]-np.arange(n)[None,:])]
        eigA=np.linalg.eigvalsh(A);eigC=np.linalg.eigvalsh(C)
        var=float(np.trace(A@C))
        assert eigA[0]>-1e-8 and eigC[0]>-1e-8
        assert eigA[-1]<Mf and eigC[-1]<Mg
        assert var<n*Mf*Mg
        rows.append({"n":n,"min_eig_A":float(eigA[0]),"max_eig_A":float(eigA[-1]),
                     "min_eig_C":float(eigC[0]),"max_eig_C":float(eigC[-1]),
                     "variance_trace":var,"variance_bound":n*Mf*Mg,
                     "negative_offdiagonal_A":bool(np.any(A-np.diag(np.diag(A))<0)),
                     "negative_offdiagonal_C":bool(np.any(C-np.diag(np.diag(C))<0))})
    assert pf.max()<Pbar_f and pg.max()<Pbar_g
    # Brownian exact diagonal Gram comparison, with truncation/numerical error.
    if H==.5:
        assert abs(rows[-1]["max_eig_A"]-float(b))<1e-7
        assert abs(rows[-1]["max_eig_C"]-float(a))<1e-9
    records.append({"H":H,"alpha":alpha,"D":D,"Pbar_f":Pbar_f,
                    "Pbar_g":Pbar_g,"sampled_period_f_max":float(pf.max()),
                    "sampled_period_g_max":float(pg.max()),
                    "c_submission_formula":float(a)/math.sqrt(Mf*Mg),"grams":rows})

# Explicit scaling cancellation cross-check with the original xi variable.
scaling=[]
H=.3;alpha=2*H+1;D=2*math.pi/(math.gamma(1+2*H)*math.sin(math.pi*H))
base=float(np.sum(2*w*x**alpha*np.abs(ff)**2)*D/(4*math.pi**2))
for Delta in [.07,.5,1.,3.2]:
    xi=x/Delta
    transform_cell=Delta**(H+1)*ff
    cell=float(np.sum(2*w/Delta*xi**alpha*np.abs(transform_cell)**2)*D/(4*math.pi**2))
    scaling.append({"Delta":Delta,"base_norm_sq":base,"cell_norm_sq":cell,"relative_error":abs(cell-base)/base})
assert max(z["relative_error"] for z in scaling)<1e-12

# Deterministic finite Euler pairing for nontrivial n,T, with each complete cell.
pairings=[]
H=.3;T=2.7;n=3;Delta=T/n
for m in [31,127,1021,4093]:
    t=np.arange(m)*T/m;tp=(np.arange(m)+1)*T/m
    total=0.
    for j in range(n):
        xx=t/Delta-j;yy=tp/Delta-j
        def evalpoly(p,z):
            r=np.zeros_like(z)
            inside=(z>=0)&(z<=1)
            r[inside]=np.polynomial.polynomial.polyval(z[inside],[float(c) for c in p])
            return Delta**H*r
        total+=float(np.sum(evalpoly(f,xx)*(evalpoly(g,yy)-evalpoly(g,xx))))
    expected=n*float(a)*Delta**(2*H)
    pairings.append({"m":m,"finite_sum":total,"limit_exact":expected,"abs_error":abs(total-expected)})
assert pairings[-1]["abs_error"]<pairings[0]["abs_error"]*1e-3

# Independent rho covariance computation for polygonal-Euler correction.
q_checks=[]
for H in H_cases:
    for m in [8,64,512,4096]:
        r=np.arange(1,m,dtype=float)
        rho=((r+1)**(2*H)+(r-1)**(2*H)-2*r**(2*H))/2
        variance=(m+2*np.sum((m-r)*rho*rho))/(4*m**(4*H))
        q_checks.append({"H":H,"m":m,"T":1,"variance_Q":float(variance)})

# The external NTU eq(27) cannot be little-o. This positive lower coefficient
# follows analytically from lag2 and product triangle volumes, not quadrature.
source_countercheck=[]
for H in [.3,.49]:
    lag2_lower=H**2*(2*H-1)**2*3**(4*H-4)/4
    source_countercheck.append({"H":H,"positive_lag2_covariance_lower_bound":lag2_lower,
                               "asymptotic_normalized_offdiagonal_lower_bound":2*lag2_lower})

result={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status":"PASS supplementary checks; exact rational identities plus unvalidated numerical quadrature",
        "python":sys.version,"python_executable":sys.executable,
        "numpy":np.__version__,"platform":platform.platform(),
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "exact":exact,"quadrature":{"positive_frequency_limit":256,"composite_width":.5,"order":24},
        "norms":{"L_f":L_f,"L_g":L_g,"N_f_numeric":N_f,"N_g_numeric":N_g},
        "fourier_derivative_independent_residual":derivative_residual,
        "fourier_inversion":inversion,"H_records":records,"scaling":scaling,
        "finite_euler_pairings":pairings,"polygonal_Q":q_checks,
        "source_eq27_countercheck":source_countercheck,
        "limits":"Finite H,n grids, finite frequency and periodization truncations, floating roots and quadrature are supplementary consistency evidence; they are not interval-validated or a universal proof."}
(OUT/'SUPPLEMENTARY_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({"status":result["status"],"max_fourier_inversion_error":max(v['abs_error'] for v in inversion),
                  "area":str(a),"H_cases":H_cases,"gram_n_cases":[1,2,8],
                  "N_f_numeric":N_f,"N_g_numeric":N_g,"script_sha256":result['script_sha256']},indent=2))
