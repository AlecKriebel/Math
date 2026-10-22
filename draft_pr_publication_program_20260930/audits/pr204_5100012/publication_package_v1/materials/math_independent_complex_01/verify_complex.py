"""Exact algebra controls and explicitly nonrigorous numerical diagnostics.
Uses preexisting read-only sibling runtime; no installs and no bytecode writes.
"""
import sys, json, math, datetime
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr200_5100007/math_algebra_family_01/runtime_packages')
import sympy as sp
import mpmath as mp

checks = {}
def exact(name, expression):
    reduced = sp.factor(expression)
    if reduced != 0:
        raise RuntimeError((name, str(reduced)))
    checks[name] = 'zero exactly'

s, c, d, h, C, D, k, al, kp = sp.symbols('s c d h C D k al kp', nonzero=True)
den = 1-k*k*s*s*h*h
sm = (s*C*D-h*c*d)/den
spl = (s*C*D+h*c*d)/den
cm = (c*C+s*h*d*D)/den
cpl = (c*C-s*h*d*D)/den
# Contact equation after replacing a/alpha=D/C and b/beta=1/C.
contact_minus = (D*s*sm+c*cm)/C-1
contact_plus = (D*s*spl+c*cpl)/C-1
subs = {c*c:1-s*s, d*d:1-k*k*s*s, D*D:1-k*k*h*h, C*C:1-h*h}
# Groebner reduction keeps every polynomial relation explicit.
g = sp.groebner([c*c+s*s-1,d*d+k*k*s*s-1,C*C+h*h-1,D*D+k*k*h*h-1], c,d,C,D,s,h,k)
for name, ex in [('contact_minus',contact_minus),('contact_plus',contact_plus),('edge_cross',spl*cm-sm*cpl-2*h*C*d/den)]:
    numerator=sp.fraction(sp.together(ex))[0]
    rem=g.reduce(sp.expand(numerator))[1]
    exact(name,rem)
# Shifted-pole derivative, with s'=c*d, c'=-s*d, d'=-k^2*s*c.
# q_z(r+t)=-alpha*k*c/(1+d).
qzprime=al*k*s*(d/(1+d)-k*k*c*c/(1+d)**2)
ct=al*al*s*(d+kp*kp)/(1+d)**2
num=sp.fraction(sp.together(al/k*qzprime-ct))[0]
g2=sp.groebner([c*c+s*s-1,d*d+k*k*s*s-1,kp*kp+k*k-1],c,d,kp,s,k,al)
exact('residue_constant',g2.reduce(sp.expand(num))[1])
# Independent eccentric-anomaly local pedal formula numerator simplification.
a,b,L,x,y=sp.symbols('a b L x y',positive=True)
rho=a*a*y*y+b*b*x*x
rad=a*a*x*x+b*b*y*y
num=a*a*b*b*(rho-L*L)-L*L*(a*a-b*b)**2*x*x*y*y-rho*(a*a*b*b-L*L*rad)
exact('local_pedal_numerator',sp.rem(sp.Poly(sp.expand(num),x),sp.Poly(x*x+y*y-1,x)).as_expr())

mp.mp.dps=60
rows=[]
for mod in ['0.3','0.7','0.95']:
    kval=mp.mpf(mod);par=kval*kval;kcomp=mp.sqrt(1-par);K=mp.ellipk(par)
    f=lambda name,u:mp.ellipfun(name,u,par)
    for N,tau in [(3,1),(4,1),(5,1),(5,2),(6,1),(7,3),(8,3),(10,3),(12,5)]:
        v=2*K*tau/N;delta=2*v
        aa=f('dn',v)/f('cn',v);bb=kcomp/f('cn',v)
        P=lambda u:(-aa*f('sn',u),bb*f('cn',u))
        Q=lambda u:(-kcomp*kcomp*f('sn',u)/f('dn',u)**2,kcomp*f('cn',u)/f('dn',u)**2)
        det=lambda p,q:p[0]*q[1]-p[1]*q[0]
        ca=aa*bb*f('sn',v)*f('cn',v)/f('dn',v)
        ctval=f('sn',delta)*(kcomp*kcomp+f('dn',delta))/(1+f('dn',delta))**2
        errs=[];products=[]
        for phase in [mp.mpf('0.123'),K/3,mp.mpf('1.317')*K]:
            verts=[P(phase+j*delta) for j in range(N)]
            area=mp.fsum(det(verts[j],verts[(j+1)%N]) for j in range(N))/2
            # Direct Euclidean line projection, independent of closed Q formula.
            feet=[]
            for j in range(N):
                px,py=verts[j];rx,ry=verts[(j+1)%N];vx,vy=rx-px,ry-py
                z=-(px*vx+py*vy)/(vx*vx+vy*vy)
                feet.append((px+z*vx,py+z*vy))
            pedal=mp.fsum(det(feet[j],feet[(j+1)%N]) for j in range(N))/2
            S=lambda u:mp.fsum(f('dn',u+j*delta) for j in range(N))
            errs += [abs(area-ca*S(phase)),abs(pedal-ctval*S(phase+v+K))]
            products.append(area*pedal)
        mx=max(errs)
        if mx > mp.mpf('1e-50'):
            raise RuntimeError(('numeric_formula_diagnostic',N,tau,mod,mp.nstr(mx)))
        eligible=N%2==1 or N%4==0
        spread=max(products)-min(products)
        if eligible and spread > mp.mpf('1e-48'):
            raise RuntimeError(('numeric_invariance_diagnostic',N,tau,mod,mp.nstr(spread)))
        rows.append({'k':mod,'N':N,'tau':tau,'eligible':eligible,'maximum_formula_residual':mp.nstr(mx,8),'product_spread':mp.nstr(spread,8),'C_T':mp.nstr(ctval,12)})

# Repeated-list control: primitive 6, duplicated to list length 12.
kval=mp.mpf('0.9');par=kval*kval;kcomp=mp.sqrt(1-par);K=mp.ellipk(par);v=K/3;delta=2*v
f=lambda name,u:mp.ellipfun(name,u,par)
aa=f('dn',v)/f('cn',v);bb=kcomp/f('cn',v)
ca=aa*bb*f('sn',v)*f('cn',v)/f('dn',v)
ctval=f('sn',delta)*(kcomp*kcomp+f('dn',delta))/(1+f('dn',delta))**2
repeated=[]
for phase in [mp.mpf(0),K/3]:
    S=mp.fsum(f('dn',phase+j*delta) for j in range(6))
    repeated.append({'phase_over_K':mp.nstr(phase/K,12),'primitive_6_product':mp.nstr(ca*ctval*S*S,35),'repeated_12_product':mp.nstr(4*ca*ctval*S*S,35)})
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'symbolic_checks':checks,'numeric_diagnostics_only':rows,'repeated_list_diagnostic_only':repeated,'proof_status':'Universal theorem depends on written complex-analytic proof, not these finite diagnostics.'},indent=2))
