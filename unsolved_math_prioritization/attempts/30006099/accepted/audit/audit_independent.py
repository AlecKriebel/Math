#!/usr/bin/env python3
"""Independent finite controls; the mathematical audit remains an analytic review.
Usage: python audit_independent.py PATH_TO_PACKET
Does not require or read datasets or scholarly source files.
"""
import hashlib, json, pathlib, shutil, subprocess, sys, tempfile
from fractions import Fraction as Q
import sympy as s

packet=pathlib.Path(sys.argv[1]).resolve()
checks=[]
def require(condition,label):
    if not bool(condition): raise RuntimeError(label)
    checks.append(label)
x,u,t=s.symbols('x u t', real=True)
r=3-2*s.sqrt(2)
L=lambda v:s.cancel(-x*s.diff(v,x)/(1+x*x))
require(s.cancel(L(x*x)+2*x*x/(1+x*x))==0,'generator obtained by differentiating observable')
require(s.cancel(L(L(x*x))-4*x*x/(1+x*x)**3)==0,'second generator independently differentiated')
require(s.cancel(s.Rational(16,27)-4*u/(1+u)**3-4*(u+4)*(2*u-1)**2/(27*(u+1)**3))==0,'exact factorization certifies second-generator upper bound')
require(s.simplify(2*s.sqrt(2)*r*r/(1-r)-(10-7*s.sqrt(2)))==0,'degree-two negative gap normalization')
require(s.simplify((1-r*r)/(s.sqrt(2)*(1+2*r*(2*x*x-1)+r*r))-1/(1+x*x))==0,'independent Poisson-kernel identity')
# Exact antiderivative along the flow gives t = log(x0/x) + (x0^2-x^2)/2.
require(s.cancel(s.diff(s.log(x)+x*x/2,x)*(-x/(1+x*x)))==-1,'implicit positive-trajectory flow law')
for a in range(1,31):
    q0=-2+s.sqrt(2)+2*s.sqrt(2)*sum(r**j for j in range(1,a+1))
    gap=2*s.sqrt(2)*r**(a+1)/(1-r)
    require(s.simplify(q0+gap)==0,f'exact projected maximum tail for half-degree {a}')
# The constants, including both factors of two, are checked independently.
p,k,N,B,D,alpha=s.symbols('p k N B D alpha',positive=True)
tGsq=2*B**4*s.log(4*p*p/alpha)/N
tbsq=2*B*B*D*D*s.log(4*p*k/alpha)/N
require(s.simplify(2*p*p*s.exp(-N*tGsq/(2*B**4))-alpha/2)==0,'Gram Hoeffding union budget is alpha/2')
require(s.simplify(2*p*k*s.exp(-N*tbsq/(2*B*B*D*D))-alpha/2)==0,'response Hoeffding union budget is alpha/2')
# A complete rational primal/dual LP family on {-1,0,1}: g=(1,0,1),
# exact generator=(-1,0,-1), relaxed stationarity error e. Primal mass off zero
# is <=e, attained with w=(e,1-e,0); dual optimum at c=1 is e.
for denom in range(2,22):
    for numer in range(1,denom):
        e=Q(numer,denom); weights=(e,1-e,Q(0))
        require(sum(weights)==1 and all(w>=0 for w in weights),'rational relaxed primal witness')
        require(abs(-weights[0]-weights[2])<=e,'rational relaxed stationarity witness')
        primal=weights[0]+weights[2]
        dual=max(Q(1)-Q(1),Q(0))+e*Q(1)
        require(primal==dual==e,'exact matching rational primal/dual witness')
# Integrity fault injection invokes the frozen verifier out of tree so importing
# cannot add __pycache__ to the manifest-controlled packet.
controls=[]
for optimized in (False,True):
    for variant in ('clean','edited','same_size_edit','missing','extra','symlink_file','symlink_directory','symlink_manifest','duplicate_manifest_path','parent_traversal','absolute_path'):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)/'packet';shutil.copytree(packet,root)
            manifest=root/'MANIFEST.json'
            if variant=='edited':(root/'README.md').write_bytes((root/'README.md').read_bytes()+b'\n')
            if variant=='same_size_edit':
                p=root/'README.md';b=p.read_bytes();p.write_bytes(bytes([b[0]^1])+b[1:])
            if variant=='missing':(root/'README.md').unlink()
            if variant=='extra':(root/'EXTRA').write_text('test')
            if variant=='symlink_file':
                (root/'README.md').unlink();(root/'README.md').symlink_to(packet/'README.md')
            if variant=='symlink_directory':(root/'EXTRA_DIR').symlink_to(packet,target_is_directory=True)
            if variant=='symlink_manifest':manifest.unlink();manifest.symlink_to(packet/'MANIFEST.json')
            if variant=='duplicate_manifest_path':
                j=json.loads(manifest.read_text());j['files'].append(j['files'][0].copy());manifest.write_text(json.dumps(j))
            if variant in ('parent_traversal','absolute_path'):
                j=json.loads(manifest.read_text());j['files'][0]['path']='../outside' if variant=='parent_traversal' else '/outside';manifest.write_text(json.dumps(j))
            cmd=[sys.executable]+(['-O'] if optimized else [])+[str(packet/'verify_packet.py'),str(root)]
            run=subprocess.run(cmd,capture_output=True,text=True)
            accepted=run.returncode==0
            require(accepted==(variant=='clean'),f'integrity {variant}, optimized={optimized}')
            controls.append({'variant':variant,'optimized':optimized,'accepted':accepted,'expected_acceptance':variant=='clean','returncode':run.returncode})
print(json.dumps({'status':'PASS','positive_requirements':len(checks),'projection_half_degrees_checked':[1,30],'exact_rational_lp_cases':210,'integrity_invocations':len(controls),'integrity_fault_rejections':20,'integrity_controls':controls,'limits':'Finite symbolic, rational and mutation controls support the analytic audit. They do not establish infinite-family convergence or protect against replacement of both the verifier and its external trust anchor.'},indent=2,sort_keys=True))
