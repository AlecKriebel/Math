#!/usr/bin/env python3
"""Independent package02 exact checks. Run with effort .venv/bin/python.

This checks identities and custody, not the cited analytic existence theorem.
No candidate files are modified. Outputs live beside this script.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import platform
import subprocess
import zipfile
import sympy as S

HERE = Path(__file__).absolute().parent
AUDIT = HERE.parent.parent
PUB = AUDIT / 'publication'
PKG = HERE / 'extraction/positivity-loss-30003571'
REPO = AUDIT.parents[2]
checks = []


def equal(label, lhs, rhs=0):
    residual = S.factor(S.simplify(lhs-rhs))
    if residual != 0:
        raise RuntimeError((label, residual))
    checks.append(label)


def require(label, condition):
    if not condition:
        raise RuntimeError(label)
    checks.append(label)


sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
PDF_SHA = 'd5c31033f40afaa8dbd1f8642d7c729dfd7a858553e1c1c0856520a10f23bedd'
ZIP_SHA = '9f9ab38e36d4b631f5d14fc2a63325f3a8e4e9cc331f200a06f6bb8ee1bf6210'
HEAD = '91385a9ba0d445a2fae4629cd60b70026584e24b'
require('reviewed PDF exact hash', sha(PUB/'positivity_loss.pdf') == PDF_SHA)
require('reviewed ZIP exact hash', sha(PUB/'verification_package.zip') == ZIP_SHA)
manifest = json.loads((PKG/'MANIFEST.json').read_text())
require('outer manifest equals extracted manifest', (PKG/'MANIFEST.json').read_bytes() == (PUB/'PACKAGE_MANIFEST.json').read_bytes())
with zipfile.ZipFile(PUB/'verification_package.zip') as z:
    names = z.namelist()
    require('ZIP has 40 distinct safe file entries', len(names) == len(set(names)) == 40 and all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names))
    require('ZIP CRC test', z.testzip() is None)
    require('ZIP no downloaded source PDFs or source/record cache', all(not n.endswith('.pdf') and '/sources/' not in n and '/records/' not in n for n in names))
for name, info in manifest['files'].items():
    p = PKG/name
    require('package bytes and hash: '+name, p.stat().st_size == info['bytes'] and sha(p) == info['sha256'])
require('strict extracted inventory', {str(p.relative_to(PKG)) for p in PKG.rglob('*') if p.is_file() and '.venv' not in p.parts and '__pycache__' not in p.parts} == set(manifest['files']) | {'MANIFEST.json'})
original = PKG/'original'
for path, base in [('public/FROZEN_MANIFEST.json', original/'public'), ('audit/AUDIT_MANIFEST.json',original/'audit'), ('PUBLICATION_MANIFEST.json',original)]:
    for name, info in json.loads((original/path).read_text())['files'].items():
        p = base/name
        require('historical '+path+' file '+name, p.stat().st_size == info['bytes'] and sha(p) == info['sha256'])
snapshot = json.loads((AUDIT/'ORIGINAL_SNAPSHOT.json').read_text())
for info in snapshot['files']:
    name = info['path'].split('attempts/30003571/', 1)[1]
    frozen = (original/name).read_bytes()
    p = subprocess.run(['git', 'show', HEAD+':'+info['path']], cwd=REPO, capture_output=True, check=True)
    require('original exact Git HEAD blob: '+name, frozen == p.stdout)
require('provenance original head', snapshot['head'] == manifest['original_head'] == HEAD)

u, v, p, x, t = S.symbols('u v p x t', real=True)
e, d = S.Rational(1,96), S.Rational(1,4)
weight = 2*S.log(1+u)+(2-e)/(1+u)+2*S.log(1+v)+d*u*v**2/((1+u)*(1+v)**2)
A = 4*p+(e+d*x*x)*(1-2*p)
B = 2+2*d*p*x*(2-3*x)
Q = 4*d*d*p*(1-p)*x**3*(1-x)
rad = lambda f, q: S.diff(f,q)+q*S.diff(f,q,2)
# Independent real-coordinate Hessian calculation for each of four charts.
a,b,c,h = S.symbols('a b c h', real=True)
corners = []
for si in (False,True):
    for zi in (False,True):
        pp = 1/(1+u) if si else u/(1+u)
        xx = 1/(1+v) if zi else v/(1+v)
        local = 2*S.log(1+u)+(2-e)*(1-pp)+2*S.log(1+v)+d*pp*xx**2
        real = local.subs({u:a*a+b*b,v:c*c+h*h})
        axis = {b:0,h:0}
        aa = ((S.diff(real,a,2)+S.diff(real,b,2))/4).subs(axis)
        bb = ((S.diff(real,c,2)+S.diff(real,h,2))/4).subs(axis)
        qr = (S.diff(real,a,c)+S.diff(real,b,h))/4
        qi = (S.diff(real,a,h)-S.diff(real,b,c))/4
        qq = (qr*qr+qi*qi).subs(axis)
        sub = {p:pp.subs(u,a*a),x:xx.subs(v,c*c)}
        label = f'four-chart real Hessian ({si},{zi})'
        equal(label+' A', aa*(1+a*a)**2, A.subs(sub))
        equal(label+' B', bb*(1+c*c)**2, B.subs(sub))
        equal(label+' Q', qq*(1+a*a)**2*(1+c*c)**2,Q.subs(sub))
        # Chart origins represent all four finite/infinite corner points.
        vals = [S.simplify(k.subs({a:0,c:0})) for k in (aa,bb,qq)]
        require(label+' origin strictly positive', vals[0]>0 and vals[1]>0 and vals[0]*vals[1]-vals[2]>0)
        corners.append({'base_inverted':si,'fiber_inverted':zi,'A':str(vals[0]),'B':str(vals[1]),'Q':str(vals[2]),'determinant':str(vals[0]*vals[1]-vals[2])})
A0=e+S.Rational(167,48)*p; B0=S.Rational(3,2); Q0=p/4
RA=d*x*x+2*d*p*(1-x*x)
RB=2*d*((1-p)+p*(1-x)*(1+3*x))
RQ=4*d*d*p*(1-(1-p)*x**3*(1-x))
equal('base nonnegative factor remainder',A-A0,RA)
equal('fiber nonnegative factor remainder',B-B0,RB)
equal('mixed upper nonnegative factor remainder',Q0-Q,RQ)
equal('full determinant nonnegative remainder',A*B-Q-(A0*B0-Q0),RA*B+A0*RB+RQ)
equal('strict universal determinant baseline',A0*B0-Q0,S.Rational(1,64)+S.Rational(159,32)*p)
equal('A upper bound factors',4-A,(4-e-d*x*x)*(1-p)+(e+d*x*x)*p)
# For A <= 4: its affine p slope is 4-2(e+d*x²)>0; max p=1 is 4-e-d*x².
equal('fiber upper bound square',S.Rational(13,6)-B,(1-p)/6+S.Rational(3,2)*p*(x-S.Rational(1,3))**2)
equal('fiber density probability',S.integrate(1/(1+v)**2,(v,0,S.oo)),1)
equal('probability coordinate pushforward',S.diff(v/(1+v),v),1/(1+v)**2)
equal('central metric Hessian',rad(weight,v).subs(u,0),2/(1+v)**2)
equal('central initial base jet',rad(weight,u).subs(u,0),e+d*(v/(1+v))**2)

# Taylor coefficient derivation: a smooth rotational solution has phi=H(v)+u*w(v)+O(u²).
g0, gw, I0, J = S.symbols('g0 gw I0 J', positive=True)
equal('exact log curvature second jet', S.diff(S.log(g0+u*gw),u).subs(u,0),gw/g0)
equal('exact log fiber integral second jet',S.diff(S.log(I0-u*J),u).subs(u,0),-J/I0)
F = S.Function('F')
compose = F(v/(1+v))
lap = lambda f:(x*(1-x)*S.diff(f,x,2)+(1-2*x)*S.diff(f,x))/2
equal('general smooth radial Laplacian chain rule',(1+v)**2*rad(compose,v)/2,lap(F(x)).subs(x,v/(1+v)))
P1=2*x-1; P2=6*x*x-6*x+1
equal('degree one eigenmode',lap(P1),-P1)
equal('degree two eigenmode',lap(P2),-3*P2)
equal('degree one mean',S.integrate(P1,(x,0,1)))
equal('degree two mean',S.integrate(P2,(x,0,1)))
equal('quadratic mode decomposition',x*x,S.Rational(1,3)+P1/2+P2/6)
w=e+d/3+d*P1/2+d*S.exp(-2*t)*P2/6
equal('actual jet candidate initial data',w.subs(t,0),e+d*x*x)
equal('actual jet candidate PDE',S.diff(w,t),lap(w)+w-S.integrate(w,(x,0,1)))
equal('actual jet constant mean',S.integrate(w,(x,0,1)),e+d/3)
equal('exact pole curvature',w.subs(x,0),e-d*(1-S.exp(-2*t))/6)
equal('strict negative target',w.subs({x:0,t:S.log(2)/2}),-S.Rational(1,96))
equal('first pole zero time',w.subs({x:0,t:S.log(S.Rational(4,3))/2}))
equal('negative open cap at target',w.subs(t,S.log(2)/2),(x*x+x)/8-S.Rational(1,96))
equal('probability normalization negative control at initial pole',(lap(e+d*x*x)+(e+d*x*x)).subs(x,0),e)
equal('normalized initial pole derivative',(lap(e+d*x*x)+e+d*x*x-S.integrate(e+d*x*x,(x,0,1))).subs(x,0),-d/3)
prod=2*S.log(1+u)+2*S.log(1+v)
logI=S.log(S.pi)-2*S.log(1+u)
equal('product stationary calibrated positive scalar ratio',S.exp(S.log(rad(prod,v))+prod+logI-S.log(2*S.pi)),1)
equal('product horizontal Hessian',rad(prod,u).subs(u,0),2)
equal('product integral Hessian',rad(logI,u).subs(u,0),-2)
equal('same weight equation14 residual',(2*rad(prod,u)+rad(logI,u)).subs(u,0),2)
R = S.symbols('R',positive=True)
psi = S.Function('psi')(u,v,t)
K = S.symbols('K',positive=True)
# Substituting phi=R*psi and t=R*tau gives phi_t=psi_tau, log g=log R+log psi_zbarz.
equal('root-time reaction and mass constant',S.log(R*K)+R*psi+S.log(I0),S.log(K)+R*psi+S.log(I0)+S.log(R))
qledger=json.loads((AUDIT/'reviews/source01/records/query_ledger.json').read_text())
require('source audit records 76 numbered queries',len(qledger['queries'])==76 and [q['number'] for q in qledger['queries']]==list(range(1,77)))
pdfs=json.loads((AUDIT/'reviews/source01/records/source_inventory.json').read_text())['primary_pdfs']
require('source audit records 19 primary PDF files',len(pdfs)==19)
for info in pdfs:
    z=AUDIT/'reviews/source01/sources'/info['name']
    require('retrieved primary PDF hash '+info['name'],z.stat().st_size==info['bytes'] and sha(z)==info['sha256'])
report={'status':'PASS_INDEPENDENT_EXACT_AND_CUSTODY','utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'sympy':S.__version__,'pdf_sha256':PDF_SHA,'zip_sha256':ZIP_SHA,'number_of_checks':len(checks),'checks':checks,'corners':corners,'uniform_smallest_eigenvalue_lower_bound':'3/1184 in product Fubini-Study unit frames (det>=1/64 and trace<=37/6)','limitations':'Analytic finite-time existence and smooth parameter dependence are imported from Naumann Theorem 5; no historical-first priority certification.'}
(HERE/'independent_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
