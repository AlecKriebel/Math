#!/usr/bin/env python3
"""Independent exact audit checks. No network or candidate-file writes.
Run from this directory: python audit_verify.py ../public --output audit_results.json
These checks supplement the written proof audit, not its analytic input.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as sp

EXPECTED_MANIFEST = '14e522b5bea40b8dc1c9a222d58048e4f667a4bc805df55dfb630d79b83a162c'
EXPECTED_PROOF = '4deb64c3b249dcf26a87ccdd222bad837e61f107b5304ed0e3ad2c6f1e444b36'
parser = argparse.ArgumentParser()
parser.add_argument('candidate', type=Path)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(args.candidate/'FROZEN_MANIFEST.json') == EXPECTED_MANIFEST
assert sha(args.candidate/'PROOF.md') == EXPECTED_PROOF
manifest = json.loads((args.candidate/'FROZEN_MANIFEST.json').read_text())
for name, meta in manifest['files'].items():
    f = args.candidate/name
    assert sha(f) == meta['sha256'] and f.stat().st_size == meta['bytes']
checks=[]
def exact(name, a, b=0):
    assert sp.simplify(a-b) == 0, (name,sp.simplify(a-b))
    checks.append(name)

u,v,p,x,t=sp.symbols('u v p x t', real=True)
e=sp.Rational(1,96); d=sp.Rational(1,4)
phi=2*sp.log(1+u)+(2-e)/(1+u)+2*sp.log(1+v)+d*u*v**2/((1+u)*(1+v)**2)
radial=lambda f,y:sp.diff(y*sp.diff(f,y),y)
A=4*p+(e+d*x**2)*(1-2*p)
B=2+2*d*p*x*(2-3*x)
Q=4*d*d*p*(1-p)*x**3*(1-x)
sub={p:u/(1+u),x:v/(1+v)}
exact('base radial Hessian',(1+u)**2*radial(phi,u),A.subs(sub))
exact('fiber radial Hessian',(1+v)**2*radial(phi,v),B.subs(sub))
exact('mixed Hessian modulus',(1+u)**2*(1+v)**2*u*v*sp.diff(phi,u,v)**2,Q.subs(sub))

# These decompositions prove inequalities on the entire closed unit square.
Alow=e+sp.Rational(167,48)*p; Blow=sp.Rational(3,2); Qhigh=p/4
RA=d*x*x+2*d*p*(1-x*x)
RB=2*d*((1-p)+p*(1-x)*(1+3*x))
RQ=4*d*d*p*(1-(1-p)*x**3*(1-x))
exact('A universal nonnegative remainder',A-Alow,RA)
exact('B universal nonnegative remainder',B-Blow,RB)
exact('Q universal nonnegative remainder',Qhigh-Q,RQ)
exact('determinant baseline',Alow*Blow-Qhigh,sp.Rational(1,64)+sp.Rational(159,32)*p)
exact('full determinant remainder decomposition',A*B-Q-(Alow*Blow-Qhigh),RA*B+Alow*RB+RQ)

# All four charts, computed from their local weights, with no finite grid.
for si in [False,True]:
    for zi in [False,True]:
        pp=1/(1+u) if si else u/(1+u)
        xx=1/(1+v) if zi else v/(1+v)
        local=2*sp.log(1+u)+(2-e)*(1-pp)+2*sp.log(1+v)+d*pp*xx**2
        label=f'chart s_inverted={si}, z_inverted={zi}'
        exact(label+' base',(1+u)**2*radial(local,u),A.subs({p:pp,x:xx}))
        exact(label+' fiber',(1+v)**2*radial(local,v),B.subs({p:pp,x:xx}))
        exact(label+' mixed',(1+u)**2*(1+v)**2*u*v*sp.diff(local,u,v)**2,Q.subs({p:pp,x:xx}))

F=sp.Function('F')
ff=F(x).subs(x,v/(1+v))
# General chain-rule coefficients, established for F=x and F=x^2.
L=lambda f:(x*(1-x)*sp.diff(f,x,2)+(1-2*x)*sp.diff(f,x))/2
for k in range(7):
    f=x**k
    exact('radial Laplacian degree '+str(k),(1+v)**2*radial(f.subs(x,v/(1+v)),v)/2,L(f).subs(x,v/(1+v)))
P1=2*x-1; P2=6*x*x-6*x+1
exact('first mode eigenvalue',L(P1),-P1)
exact('second mode eigenvalue',L(P2),-3*P2)
exact('first mode mean',sp.integrate(P1,(x,0,1)))
exact('second mode mean',sp.integrate(P2,(x,0,1)))
w=e+d/3+d*P1/2+d*sp.exp(-2*t)*P2/6
mean=sp.integrate(w,(x,0,1))
exact('solution initial value',w.subs(t,0),e+d*x*x)
exact('solution differential equation',sp.diff(w,t),L(w)+w-mean)
exact('exact negative value',w.subs({x:0,t:sp.log(2)/2}),-sp.Rational(1,96))
exact('exact positivity-loss threshold',w.subs({x:0,t:sp.log(sp.Rational(4,3))/2}))
exact('central initial second derivative',radial(phi,u).subs(u,0),e+d*(v/(1+v))**2)
exact('central stationary Hessian',radial(phi,v).subs(u,0),2/(1+v)**2)
exact('probability x density',sp.diff(v/(1+v),v),1/(1+v)**2)

# Defining equation (13) versus literal printed equation (14):
# phi_product=2log(1+u)+2log(1+v), I=pi/(1+u)^2.
# Both probability measures are dA/[pi(1+v)^2]. Thus c_t=0.
# At s=0, c=2, A=0, Laplacian c=0, (log I)_{s bar s}=-2.
cprod=radial(2*sp.log(1+u),u)
logI=sp.log(sp.pi)-2*sp.log(1+u)
exact('product horizontal coefficient',cprod.subs(u,0),2)
exact('product normalization Hessian',radial(logI,u).subs(u,0),-2)
exact('coefficient-one product RHS',cprod+radial(logI,u))
printed_residual=(2*cprod+radial(logI,u)).subs(u,0)
exact('literal printed equation 14 nonzero residual',printed_residual,2)
assert printed_residual != 0

# Algebraic version of the rth-root/time conversion on the symmetric fiber:
# c=w/r, g_root=g/r, tau=t/r. The coefficient-r root operator is r times
# the coefficient-one operator at the original t. This is not a second flow.
r=sp.symbols('r',positive=True)
c=w/r
root_operator=r*L(c)+r*c-r*sp.integrate(c,(x,0,1))
exact('root and time rescaling',root_operator,r*sp.diff(c,t))

report={
    'problem_id':30003571,
    'code':'OWR-15582-005',
    'status':'PASS',
    'frozen_manifest_sha256':EXPECTED_MANIFEST,
    'frozen_proof_sha256':EXPECTED_PROOF,
    'frozen_files_verified':len(manifest['files']),
    'independent_exact_checks':len(checks),
    'check_names':checks,
    'finite_grid_used':False,
    'negative_value':'-1/96',
    'time':'log(2)/2',
    'literal_equation_14_product_residual':'2, while the defining equation gives 0',
    'scope':'Exact algebra and hash integrity; smooth finite-time flow existence remains the cited analytic input.',
    'sympy_version':sp.__version__,
}
out=json.dumps(report,indent=2,sort_keys=True)+'\n'
if args.output: args.output.write_text(out)
print(out,end='')
