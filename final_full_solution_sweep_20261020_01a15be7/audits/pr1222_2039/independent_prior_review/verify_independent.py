#!/usr/bin/env python3
"""Read-only exact audit controls. No author code, network, asserts, or service writes."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import factorial, gcd, prod, isqrt
from pathlib import Path
import hashlib
import json
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / 'private'
CHECKS = []

def require(name, condition):
    if not condition:
        raise RuntimeError('FAILED: ' + name)
    CHECKS.append(name)

def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a

def division(a, b):
    a = a[:]
    q = [0] * max(1, len(a)-len(b)+1)
    while len(a) >= len(b) and any(a):
        k = len(a)-len(b)
        if a[-1] % b[-1]:
            raise RuntimeError('nonintegral polynomial division')
        c = a[-1] // b[-1]
        q[k] += c
        for i, v in enumerate(b):
            a[i+k] -= c*v
        trim(a)
    return trim(q), trim(a)

@lru_cache(None)
def cyclotomic(n):
    a = [-1] + [0]*(n-1) + [1]
    for d in range(1,n):
        if n % d == 0:
            a, rem = division(a, cyclotomic(d))
            if rem != [0]:
                raise RuntimeError('cyclotomic remainder')
    return a

def prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n)+1))

def squarefree(n):
    return all(n % (d*d) for d in range(2,isqrt(n)+1))

def crt(a,p,b,q):
    return (a+p*((b-a)*pow(p,-1,q) % q)) % (p*q)

def balanced(a,n):
    a %= n
    return a-n if 2*a > n else a

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    # These are independent finite controls, not a computation of the eventual construction.
    require('exp(3/4) rational lower series', sum(F(3,4)**j/factorial(j) for j in range(5)) > F(21,10))
    require('log2 upper comparison', F(21,10) > 2)
    for n in [1,3,5,7,9]:
        require('odd factorial seed '+str(n), F(factorial(n),factorial(n//2)**2) < F(21,10)**n)
    require('odd factorial induction ratio', F(22,5) < F(21,10)**2)
    require('log2 lower series', F(56,81) > F(69,100))
    require('log301 upper comparison', F(21,10)**8 > 301)
    require('factorial lower base n300', 300*F(69,100)-6 > F(2,3)*301)
    require('factorial lower monotone increment', F(69,100)-F(2,3)-F(1,301) > 0)
    require('prime count threshold sqrtx126', F(1,6)-F(3,126) == F(1,7))
    require('dyadic reciprocal mass strict margin', 72**50 > 2**7 * 65**50)
    require('epsilon rounded constant safe direction', 10240000 < 20000000)
    require('divisor count half rows at onset', F(800,20)+10 <= F(800,16))
    require('incoherent exponential gap', F(63,64)*F(127,128) > F(1,2))
    require('coherent mismatch final constant', F(3,127) < F(1,4))
    for n in range(1,101):
        require('finite primorial '+str(n), prod(p for p in range(2,n+1) if prime(p)) <= 4**n)
    # Exact rational target reduction, including integer and tiny targets.
    for tau in [F(1),F(17,30),F(2,3),F(43),F(1,1000003)]:
        q = max(2, (400*tau.numerator)//tau.denominator+1)
        while not prime(q) or (tau.numerator*tau.denominator) % q == 0:
            q += 1
        x = tau/q
        require('rational reduction '+str(tau), 0 < x <= F(1,400) and squarefree(x.denominator) and q*x == tau)
    require('non-squarefree boundary rejected', not squarefree(4) and squarefree(F(2,4).denominator))
    # Tuning is tested on a finite interval with the exact same last-endpoint mechanism.
    V=(2,3,5)
    U=[p for p in range(10001,20001) if prime(p)]
    H=sum((F(1,v) for v in V),F(0)); tau=F(1,400)
    means=[]; mu=F(0)
    for u in U:
        mu += H/(2*u); means.append(mu)
    k=max(i for i,m in enumerate(means) if m <= tau)
    mu=means[k]
    require('tuning first endpoint and full interval', means[0] < tau and means[-1] >= 2*tau)
    require('tuning last endpoint and next', mu <= tau < means[k+1])
    require('tuning gap and column count', 0 <= tau-mu < H/20000 and mu >= tau/2 and k+1 >= tau*10000/H)
    sums=[F(0),mu,2*mu]
    require('tuning mass congruence range', all(-1 < s-tau < 1 for s in sums))
    # Pairwise CRT identities are checked for every label pair, not sampled floats.
    wrong_factor_detected=False; total=0
    for p in (2,3,5):
        for u in (7,11):
            for a,b,c in product(range(p),range(u),range(u)):
                j=crt(a,p,b,u); jp=crt(a,p,c,u)
                lhs=F(j-jp,p*u) % 1
                rhs=F(((b-c)*pow(p,-1,u)) % u,u)
                if lhs != rhs:
                    raise RuntimeError('CRT phase difference failed')
                total += 1
                wrong_factor_detected |= (lhs != (30*rhs) % 1)
    require('all '+str(total)+' CRT phase differences exact', True)
    require('negative control hidden L multiplier detected', wrong_factor_detected)
    # No-wrap mechanism over every row pattern and column label in a toy instance.
    hits=0
    for rows in product(range(2),range(3),range(5)):
        for z in range(101):
            js=[balanced(crt(a,v,z,101),v*101) for a,v in zip(rows,(2,3,5))]
            if all(F(abs(j),v*101) <= F(1,20) for j,v in zip(js,(2,3,5))):
                if len(set(js)) != 1 or abs(js[0]) > F(101,10):
                    raise RuntimeError('no wrap control failed')
                hits += 1
    require('no wrap exhaustive nonempty control', hits > 0)
    # Exact finite Fourier identity: cyclotomic remainder, without floating trigonometry.
    V=(2,3); U=(5,7); L=210; edges=[v*u for v in V for u in U]
    weights=[L//n for n in edges]
    direct=[sum(weights[i] for i in range(len(edges)) if mask>>i & 1) % L for mask in range(1<<len(edges))]
    histogram=[direct.count(j) for j in range(L)]
    dyn=[0]*L;dyn[0]=1
    for w in weights:
        dyn=[dyn[j]+dyn[(j-w)%L] for j in range(L)]
    require('subset product polynomial exact', dyn == histogram)
    for target in [0,F(1,6),F(1,10),F(1,14),F(1,210),F(1,2)]:
        t=F(target)*L
        require('target denominator divides L '+str(target), t.denominator == 1)
        coeff=[0]*L
        for h in range(-L//2+1,L//2+1):
            for s in direct:
                coeff[(h*(s-t.numerator))%L] += 1
        _,rem=division(coeff,cyclotomic(L))
        require('exact Fourier normalization '+str(target), rem == [L*histogram[t.numerator%L]])
    require('negative missing target phase detectable', any(n != histogram[0] for n in histogram))
    # Classification uses a toy cutoff with uniqueness; every frequency is classified.
    coherent={tuple(M%v for v in V):M for M in (-1,0,1)}
    require('coherent toy labels unique', len(coherent) == 3)
    cases=[0,0,0]
    for h in range(-L//2+1,L//2+1):
        rows=tuple(h%v for v in V); M=coherent.get(rows)
        if M is None:
            cases[2] += 1
        elif all(h%u == M%u for u in U):
            cases[0] += 1
            if h != M:
                raise RuntimeError('coherent matching h not M')
        else:
            cases[1] += 1
    require('all toy frequencies disjoint exhaustive', sum(cases)==L and cases==[3,102,105])
    require('squarefree hypothesis needed for Fourier', (F(1,4)*L).denominator != 1)
    # All eight payload bindings and actual exact-base/head changed paths.
    names=['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json']
    manifest=json.loads((PRIVATE/'MANIFEST.json').read_text())
    require('exact eight manifest members', manifest['members'] == names)
    for n in names:
        b=(PRIVATE/n).read_bytes()
        obj=json.loads((PRIVATE/('blob_'+n+'.json')).read_text())['value']['structuredContent']
        require('git blob sha '+n, hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==obj['sha'])
    for e in manifest['entries']:
        b=(PRIVATE/e['file']).read_bytes()
        require('manifest digest '+e['file'], len(b)==e['bytes'] and sha(b)==e['sha256'])
    require('manifest body identity', sha((PRIVATE/'MANIFEST.json').read_bytes()) == '8b7bdeac18a20ebbb3c43ee56cf3ee035e022c2e9adb0f30635f7c3511e58961')
    cmp=json.loads((PRIVATE/'github_compare.json').read_text())['structuredContent']
    require('exact base-head comparison', cmp['base']=='4b27092a448d53b61408355ce44ec38d103a1ce4' and cmp['head']=='4cf2bd2b9d934dc0fc47771c4da20d3cf704b1dd')
    require('exact eight additions no queue', [e['filename'] for e in cmp['files']] == ['unsolved_math_prioritization/attempts/2039/'+n for n in names] and all(e['status']=='added' for e in cmp['files']))
    require('primary PDF pinned', sha((PRIVATE/'li_september.pdf').read_bytes()) == '9983c8340b91610e082bbe3161cea13385745add23e6cb41f3b12be52d91c4d8')
    zbytes=(PRIVATE/'tang_v0.0.3.zip').read_bytes()
    require('Tang entire ZIP official checksum', len(zbytes)==356148 and hashlib.md5(zbytes).hexdigest()=='aa73ac6778c2e4fc0d8ea3beeec4339f')
    with zipfile.ZipFile(PRIVATE/'tang_v0.0.3.zip') as z:
        require('Tang all 111 ZIP CRCs and Lean source presence', len(z.infolist())==111 and z.testzip() is None and sum(n.endswith('.lean') for n in z.namelist())==98)
    if '--negative-control' in sys.argv:
        require('intentional corruption must fail', F(1,6)==F(1,7))
    print(json.dumps({'passed':True,'checks':len(CHECKS),'cases':cases,'crt_pairs':total,'no_wrap_hits':hits,'author_code_executed':False,'scope':'Exact supporting controls; not an eventual-construction computation, formal build or proof of the infinite theorem.','check_names':CHECKS},sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
