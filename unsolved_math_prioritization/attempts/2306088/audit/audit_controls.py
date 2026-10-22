#!/usr/bin/env python3
"""Independent exact/integrity checks. Does not edit the frozen submission."""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json, subprocess, sys

BASE = Path(__file__).resolve().parents[1]
SUB = BASE / 'submission'
EXPECTED = '6c8b21e1fedfbde37339716d8bfd8a57ec5aed6c703c6cb0732b8155adf0331c'
checks=[]
def ck(name, ok):
    if not ok: raise AssertionError(name)
    checks.append({'name':name,'passed':True})
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def add(a,b):
    c=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]+=x
    return c
def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def integrity(prefix):
    ck(prefix+' manifest fingerprint',sha(SUB/'FROZEN_MANIFEST.json')==EXPECTED)
    m=json.loads((SUB/'FROZEN_MANIFEST.json').read_text())
    for e in m['files']:
        p=SUB/e['path']
        ck(prefix+' size '+e['path'],p.stat().st_size==e['bytes'])
        ck(prefix+' hash '+e['path'],sha(p)==e['sha256'])
    ck(prefix+' SHA256SUMS fingerprint',sha(SUB/'SHA256SUMS')==m['sha256sums_sha256'])
    for line in (SUB/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split(maxsplit=1)
        ck(prefix+' SHA256SUMS entry '+name,sha(SUB/name)==digest)

integrity('before')
# Independent coefficient-array algebra, including a monotonicity check.
h=mul([F(4),F(-4),F(1)],[F(1),F(0),F(2)])
gap=add(h,[-F(27,8)])
rhs=[x/F(8) for x in mul([F(1),F(-6),F(12),F(-8)],[F(5),F(-2)])]
ck('small interval exact factorization',gap==rhs)
der=[i*h[i] for i in range(1,len(h))]
ck('small interval derivative factorization',der==mul([F(-4),F(2)],[F(1),F(-4),F(4)]))
ck('q area coefficient identity',F(1)+2*F(1,2)**2==F(3,2))
ck('q functional square',F(3,2)**2*F(3,2)==F(27,8))
# Compute inverse-Koebe series independently through its defining quadratic.
N=9
for tau in [F(1),F(8,9),F(2,3),F(1,3),F(1,150)]:
    p=[F(0)]*(N+1)
    for n in range(1,N+1):
        p[n]=(2-2*tau)*p[n-1]-(p[n-2] if n>=2 else 0)
        p[n]+=tau*sum(p[i]*p[n-1-i] for i in range(1,n-1))
        if n==1: p[n]+=tau
    one_minus_p=[F(1)]+[-x for x in p[1:]]
    lhs=mul(p,[F(1),F(-2),F(1)])[:N+1]
    rhs=([F(0)]+[tau*x for x in mul(one_minus_p,one_minus_p)])[:N+1]
    ck('Pick quadratic through degree 9, tau='+str(tau),lhs==rhs)
    pp=mul(p,p)
    f=[(p[n]+pp[n]/2)/tau for n in range(N+1)]
    a=2-F(3,2)*tau
    ck('composition normalization and coefficient, tau='+str(tau),f[0]==0 and f[1]==1 and f[2]==a)
    ck('exact area normalization, tau='+str(tau),F(3,2)/tau**2==F(27,8)/(2-a)**2)
    ck('finite coefficient area sum below full image area, tau='+str(tau),sum(n*f[n]**2 for n in range(1,N+1))<=F(3,2)/tau**2)
# A rational parametrization of the slit endpoint avoids sampled radicals.
for r in [F(1,4),F(1,2),F(3,4)]:
    tau=4*r/(1+r)**2
    ck('slit endpoint Koebe image r='+str(r),-r/(1+r)**2==-tau/4)
    ck('slit endpoint and tau interior r='+str(r),0<r<1 and 0<tau<1)
ck('perimeter conversion square',4*F(27,8)==F(27,2))
# Mathematically relevant wrong-formula/sign controls.
ck('reject denominator 7 at explicit a=1 witness',F(27,8)<F(27,7))
ck('reject larger area constant with q',F(3,2)**2*F(3,2)<F(27,8)+F(1,100))
ck('reject wrong scaling tau^-1 at tau=2/3',F(3,2)/F(2,3)!=F(27,8))
ck('reject wrong sign in isoperimetry using A/pi=1 and ell/(2pi)=2',F(1)>F(1,2))
# Author script must reproduce its complete recorded JSON, not just exit zero.
r=subprocess.run([sys.executable,str(SUB/'verify_exact.py')],check=True,capture_output=True,text=True)
author=json.loads(r.stdout)
ck('author exact output matches recording',author==json.loads((SUB/'verification.json').read_text()))
ck('author reports all 21 controls',author['status']=='PASS' and author['count']==21 and all(x['passed'] for x in author['checks']))
integrity('after')
result={'verdict':'PASS','frozen_manifest_sha256':EXPECTED,'checks':checks,'check_count':len(checks),'author_controls':21,'scope':'Integrity and exact rational algebra only. Analytic theorem applicability, topology, univalence and isoperimetry are reviewed in AUDIT.md; these controls do not prove them.','frozen_inputs_modified':False,'remote_writes':False}
print(json.dumps(result,indent=2))
