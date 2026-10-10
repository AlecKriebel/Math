#!/usr/bin/env python3
"""Exact algebra sanity checks and packet integrity, not formal proof verification."""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json, sys
if not __debug__:
    raise SystemExit('Optimized execution is refused: checks require assertions.')


def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a): return (a[0],-a[1])
def inv(a):
    n=a[0]*a[0]+a[1]*a[1]
    return (a[0]/n,-a[1]/n)
def scale(a,t): return (a[0]*t,a[1]*t)
def power(a,n):
    r=(F(1),F(0))
    for _ in range(n): r=mul(r,a)
    return r

def checks():
    counts={'unit_circle_checks':0,'kernel_identity_checks':0,'denominator_bound_checks':0,'geometric_remainder_checks':0,'gram_identity_checks':0,'convention_controls':0}
    one=(F(1),F(0))
    xs=[F(i,10) for i in range(-9,10)]
    for t in [F(i,7) for i in range(-10,11) if i]:
        z=((1-t*t)/(1+t*t),2*t/(1+t*t))
        assert mul(z,conj(z))==one
        counts['unit_circle_checks']+=1
        for x in xs:
            d=1-2*x*z[0]+x*x
            k=sub(inv(sub(one,scale(conj(z),x))),inv(sub(one,scale(z,x))))
            assert k==(F(0),-2*x*z[1]/d)
            counts['kernel_identity_checks']+=1
            u=1-abs(x); s=abs(z[1])
            assert 5*d>=u*u+s*s
            counts['denominator_bound_checks']+=1
            for n in (1,3,7):
                w=scale(conj(z),x)
                finite=(F(0),F(0))
                for j in range(n+1):finite=add(finite,power(w,j))
                remainder=mul(power(w,n+1),inv(sub(one,w)))
                assert add(finite,remainder)==inv(sub(one,w))
                counts['geometric_remainder_checks']+=1
    measures=[[(F(0),F(1))],[(F(-2,3),F(2)),(F(1,4),F(3,5))],[(F(-9,10),F(1,3)),(F(0),F(1,7)),(F(9,10),F(2,3))]]
    for measure in measures:
        for n in range(1,9):
            cs=[(F(2*j-3,5),F(j+1,7)) for j in range(n)]
            moments=[sum(w*x**j for x,w in measure) for j in range(2*n-1)]
            q=(F(0),F(0))
            for i in range(n):
                for j in range(n):q=add(q,scale(mul(conj(cs[i]),cs[j]),moments[i+j]))
            direct=F(0)
            for x,w in measure:
                v=(F(0),F(0))
                for j,c in enumerate(cs):v=add(v,scale(c,x**j))
                direct+=w*(v[0]*v[0]+v[1]*v[1])
            assert q==(direct,F(0)) and direct>=0
            counts['gram_identity_checks']+=1
    # n=0 versus n=1 convention, null-symbol, and pointwise positivity controls.
    a=lambda coeff,n:coeff.get(-n,F(0))
    const={0:F(1)}
    assert [a(const,n) for n in range(4)]==[1,0,0,0]
    counts['convention_controls']+=1
    analytic={1:F(2),3:F(-4)}
    assert all(a(analytic,n)==0 for n in range(8))
    counts['convention_controls']+=1
    f={-2:F(3),-1:F(2),0:F(7),1:F(5)}
    zf={k+1:v for k,v in f.items()}
    assert all(a(zf,n)==f.get(-n-1,F(0)) for n in range(8))
    counts['convention_controls']+=1
    positive_pointwise={0:F(1),-1:F(1,2),1:F(1,2)}
    assert a(positive_pointwise,0)*a(positive_pointwise,2)-a(positive_pointwise,1)**2==F(-1,4)
    counts['convention_controls']+=1
    counts['total_exact_checks']=sum(counts.values())
    return {'result':'PASS_EXACT_SANITY_CHECKS','counts':counts,'scope':'Finite algebraic checks support the formulas; no numerical experiment or automated proof of the full theorem is claimed.'}


def main():
    result=checks()
    if sys.argv[1:]==['--math-only']:
        print(json.dumps(result,indent=2));return
    if sys.argv[1:]:raise SystemExit('Usage: verify.py [--math-only]')
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'MANIFEST.json').read_text())
    expected={item['path'] for item in manifest['files']}
    if len(expected)!=len(manifest['files']):raise SystemExit('Duplicate paths in manifest')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual==expected|{'MANIFEST.json'},'Unexpected/missing packet members'
    for item in manifest['files']:
        rel=Path(item['path'])
        assert not rel.is_absolute() and '..' not in rel.parts
        b=(root/rel).read_bytes()
        assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],item['path']
    assert json.loads((root/'verification_results.json').read_text())==result
    result['integrity']='PASS_EXACT_INVENTORY_AND_ALL_SHA256'
    result['payload_members_verified']=len(expected)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
