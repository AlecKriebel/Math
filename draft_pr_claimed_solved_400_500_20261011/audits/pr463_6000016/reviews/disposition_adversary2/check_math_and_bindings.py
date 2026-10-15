#!/usr/bin/env python3
"""Independent exact identities and frozen source replay; no source writes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import sympy as s

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parents[1]
SOURCE=AUDIT/'source_snapshot/unsolved_math_prioritization/attempts/6000016'

def require(value,message):
    if not value:raise RuntimeError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    source=json.loads((AUDIT/'SOURCE_RECEIPT.json').read_text());records=[]
    require(len(source['files'])==14,'Wrong frozen inventory')
    for entry in source['files']:
        path=AUDIT/'source_snapshot'/entry['path']
        require(path.stat().st_size==entry['bytes'] and sha(path)==entry['sha256'],'Frozen source drift')
        records.append(entry)
    references=0
    for filename in ['FROZEN_AUTHOR_MANIFEST.json','audit/AUDIT_MANIFEST.json','PUBLICATION_MANIFEST.json']:
        manifest=json.loads((SOURCE/filename).read_text())
        for entry in manifest['files']:
            root=SOURCE/'audit' if filename=='audit/AUDIT_MANIFEST.json' else SOURCE
            path=root/entry['path'];require(path.stat().st_size==entry['bytes'] and sha(path)==entry['sha256'],'Historical binding drift');references+=1
    auditmanifest=json.loads((SOURCE/'audit/AUDIT_MANIFEST.json').read_text())
    # Actual standalone key spelling is inspected, rather than guessed.
    require(auditmanifest['frozen_author_manifest_sha256']==sha(SOURCE/'FROZEN_AUTHOR_MANIFEST.json'),'Author manifest standalone binding')
    require(auditmanifest['frozen_proof_sha256']==sha(SOURCE/'PROOF.md'),'Proof standalone binding')
    references+=2
    replay=[]
    for optimized in [False,True]:
        env=dict(os.environ)
        if optimized:env['PYTHONOPTIMIZE']='1'
        else:env.pop('PYTHONOPTIMIZE',None)
        for filename,resultname,extra in [('check_exact.py','exact_results.json',[]),('audit/check_audit.py','audit/audit_results.json',['--author-dir',str(SOURCE)])]:
            command=[sys.executable]+(['-O'] if optimized else [])+[str(SOURCE/filename)]+extra
            result=subprocess.run(command,cwd=HERE/'private_cases',env=env,capture_output=True)
            require(result.returncode==0 and not result.stderr and result.stdout==(SOURCE/resultname).read_bytes(),'Frozen replay mismatch')
            replay.append({'script':filename,'optimized':optimized,'bytes':len(result.stdout),'sha256':hashlib.sha256(result.stdout).hexdigest()})
    names=[]
    def eq(name,actual,expected=0):
        residual=actual-expected
        if isinstance(residual,s.MatrixBase):valid=all(s.simplify(x)==0 for x in residual)
        else:valid=s.simplify(residual)==0
        require(valid,name);names.append(name)
    x,y,t,m,n,p,q,a,b,c,C=s.symbols('x y t m n p q a b c C',real=True)
    X=s.Matrix([x,y]);F=s.Matrix([x,y+t*x*x/2]);J=F.jacobian(X)
    eq('developing determinant',J.det(),1)
    eq('developing inverse',s.Matrix([F[0],F[1]-t*F[0]**2/2]),X)
    eq('pullback coefficient',J.inv()*F.diff(x,2),s.Matrix([0,t]))
    def rho(u,v,m,n):return s.Matrix([u+m,v+n+t*m*u+t*m*m/2])
    eq('full deck equivariance',F.subs({x:x+m,y:y+n}),rho(F[0],F[1],m,n))
    uv=s.Matrix([x,y]);first=rho(x,y,p,q)
    eq('full deck group law',rho(first[0],first[1],m,n),rho(x,y,m+p,n+q))
    K=s.Matrix([[0,0],[t,0]]);eq('connection nilpotent curvature',K*K,s.zeros(2));eq('parallel volume trace',s.trace(K),0)
    A=s.Function('A')(x,y);B=s.Function('B')(x,y);D=s.Function('C')(x,y);g=s.Matrix([[A,B],[B,D]])
    covx=g.diff(x)-K.T*g-g*K;covy=g.diff(y)
    eq('all metric Codazzi residual',covx[1,0]-covy[0,0],B.diff(x)-A.diff(y)-t*D)
    eq('second Codazzi residual',covx[1,1]-covy[0,1],D.diff(x)-B.diff(y))
    eq('given metric countercontrol',s.diff(1+s.Symbol('e')*s.cos(2*s.pi*x),x),-2*s.pi*s.Symbol('e')*s.sin(2*s.pi*x))
    S=s.Matrix([[1,0],[t,1]]);H=s.Matrix([[a,b],[b,c]])
    eq('constant positive metric shear difference',S.T*H*S-H,s.Matrix([[2*t*b+t*t*c,t*c],[t*c,0]]))
    positiveC=s.symbols('positiveC',positive=True);eq('determinant rescaling in dimension two',(H/s.sqrt(positiveC)).det(),H.det()/positiveC)
    R,r0,t0=s.symbols('R r0 t0',positive=True)
    eq('Jorgens first bound large radius limit',s.limit(24*(r0+t0)**2*r0**2/R**2,R,s.oo),0)
    eq('Jorgens second bound large radius limit',s.limit(24*(r0+t0)**2*t0**2/R**2,R,s.oo),0)
    for entry in records:require(sha(AUDIT/'source_snapshot'/entry['path'])==entry['sha256'],'Frozen source changed during replay')
    print(json.dumps({'status':'PASS','frozen_objects':records,'historical_reference_count':references,'historical_replays':replay,
                      'independent_exact_identity_count':len(names),'identities':names,
                      'analytical_not_encoded':['positive integral Stokes for arbitrary metrics','Delanoe published theorem application','global cover Poincare integration','Jorgens published disk estimate'],
                      'original_proof_search_attempts':0,'genuine_api_dispatches':0},indent=2))

if __name__=='__main__':main()
