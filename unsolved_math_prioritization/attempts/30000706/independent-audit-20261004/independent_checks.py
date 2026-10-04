#!/usr/bin/env python3
"""Independent diagnostics for the frozen rank606 partial report; no classification certificate.
Writes only this audit's independent-results.json. Source PDFs are neither copied nor emitted.
"""
from collections import Counter, defaultdict
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
checks = []

def check(label, condition):
    assert bool(condition), label
    checks.append(label)

def same(label, lhs, rhs=0):
    check(label, s.cancel(lhs-rhs) == 0)

manifest_expected = 'cb3fd99d35566ff256249f4eb19f0aa8036bab8892d7575899cb5218400d0bc1'
manifest = (BASE/'public/SHA256SUMS').read_bytes()
check('audited author manifest SHA256', hashlib.sha256(manifest).hexdigest() == manifest_expected)
for line in manifest.decode().splitlines():
    digest, name = line.split('  ', 1)
    check('author payload integrity: '+name, hashlib.sha256((BASE/'public'/name).read_bytes()).hexdigest() == digest)
check('isolated author replay receipt byte equality',
      (BASE/'public/CONTROL_RESULTS.json').read_bytes() == (HERE/'replay/CONTROL_RESULTS.json').read_bytes())
provenance = json.loads((BASE/'public/SOURCE_PROVENANCE.json').read_text())
source_files = ['owr-2007.pdf','steinmetz-2011.pdf','steinmetz-2025-published.pdf',
                'steinmetz-2024.pdf','li-zhai-yi-2026.pdf','huang-du-crossref.json']
source_results=[]
for source, name in zip(provenance['sources'], source_files):
    content = (BASE/'private'/name).read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    check('source digest and byte count: '+source['key'], digest == source['sha256'] and len(content)==source['bytes'])
    source_results.append({'key':source['key'],'sha256':digest,'bytes':len(content),'matched':True})
record=(BASE/'private/selected-record.json').read_bytes()
check('pinned target record hash',hashlib.sha256(record).hexdigest()==provenance['catalogue']['record_sha256'])

# Independent endpoint valuation models. This tests every category in the proof table,
# not all analytic germs; arbitrary-order proof is in AUDIT.md.
t=s.symbols('t')
P=lambda w:w*(w*w-1)

def valuation(expr):
    num,den=s.fraction(s.cancel(expr))
    if num==0:return s.oo
    return min(m[0] for m in s.Poly(num,t).monoms())-min(m[0] for m in s.Poly(den,t).monoms())

endpoint_counts=Counter()
for p,q in product(range(1,5),repeat=2):
    cases=[
        ('distinct finite roots', 2*t**p, 1+3*t**q, -2),
        ('root versus finite nonroot',2*t**p,2+3*t**q,q-2),
        ('distinct finite nonroots',2+2*t**p,3+3*t**q,p+q-2),
        ('pole versus root',2/t**p,1+3*t**q,-2),
        ('pole versus finite nonroot',2/t**p,2+3*t**q,q-2),
        ('equal finite root',2*t**p,3*t**q,2*min(p,q)-2),
        ('equal pole',2/t**p,3/t**q,2*min(p,q)-2),
        ('equal finite nonroot',2+2*t**p,2+3*t**q,p+q-2+2*min(p,q))]
    for label,F,G,expected in cases:
        E=s.diff(F,t)*s.diff(G,t)*(F-G)**2/(P(F)*P(G))
        check(f'endpoint order {label}, p={p}, q={q}',valuation(E)==expected)
        endpoint_counts[label]+=1
# Equal leading terms, rather than only the generic-coefficient case.
for p in range(1,5):
    for extra in range(1,4):
        F=t**p;G=t**p+t**(p+extra)
        E=s.diff(F,t)*s.diff(G,t)*(F-G)**2/(P(F)*P(G))
        check(f'finite leading cancellation p={p}, extra={extra}',valuation(E)==2*(p+extra)-2)
        F=t**(-p);G=t**(-p)+t**(-p+extra)
        E=s.diff(F,t)*s.diff(G,t)*(F-G)**2/(P(F)*P(G))
        check(f'pole leading cancellation p={p}, extra={extra}',valuation(E)==2*p+2*extra-2)

# Exhaustive degree-two FIBER DATA enumeration, not rational-map existence.
# n=4 follows from the proved Riemann-Hurwitz argument. Sorted labels quotient out
# permutation of domain shared points. The two punctures remain ordered.
endpoint_options=defaultdict(list)
for a,b in product(range(4),repeat=2):
    for e0,ei in product([1,2],repeat=2):
        vector=[0]*4;vector[a]+=e0;vector[b]+=ei
        endpoint_options[tuple(vector)].append((a,b,e0,ei))
signature_counts=Counter()
representatives={}
for labels in combinations_with_replacement(range(4),4):
    for mult in product([(1,1),(1,2),(2,1)],repeat=4):
        residual_R=[2]*4;residual_S=[2]*4
        for a,(p,q) in zip(labels,mult):
            residual_R[a]-=p;residual_S[a]-=q
        for R in endpoint_options[tuple(residual_R)]:
            for S in endpoint_options[tuple(residual_S)]:
                if R[0]==S[0] or R[1]==S[1]:continue
                omitted=set(range(4))-set(labels)
                attained_CM={a for a in set(labels)
                             if all(p==q for b,(p,q) in zip(labels,mult) if b==a)}
                key=f'omitted={len(omitted)},attained_CM={len(attained_CM)}'
                signature_counts[key]+=1
                representatives.setdefault(key,{'labels':labels,'multiplicities':mult,'R_punctures':R,'S_punctures':S})
                if omitted:
                    check(f'omitted fiber signature {sum(signature_counts.values())} has attained CM',bool(attained_CM))
                else:
                    check(f'full fiber signature {sum(signature_counts.values())} has complementary degrees',
                          all(p!=q for p,q in mult) and R[2:]==(1,1) and S[2:]==(1,1))
check('degree-two fiber signature count',dict(signature_counts)=={
    'omitted=2,attained_CM=2':12,'omitted=1,attained_CM=1':48,'omitted=0,attained_CM=0':24})

# Degree-two coefficient reconstruction via polynomial resultants, and symmetry guards.
r,alpha,beta=s.symbols('r alpha beta',nonzero=True)
R=alpha*(t-r)/(t-1)**2;S=beta*(t-r)**2/(t-1)
eqR=s.factor(s.together((R.subs(t,2-r)-R.subs(t,0))/alpha))
eqS=s.factor(s.together((S.subs(t,2*r-1)-S.subs(t,0))/beta))
same('degree-two residual R',(r-1)*eqR,(r-2)*(r+1))
same('degree-two residual S',2*eqS,(2*r-1)*(r+1))
check('degree-two nondegenerate root set',s.solve([s.together(eqR).as_numer_denom()[0],s.together(eqS).as_numer_denom()[0]],[r])==[(-1,)])
same('remaining equality fixes beta',R.subs({r:-1,t:-3})-S.subs({r:-1,t:-3}),beta-alpha/8)
R0=(t+1)/(t-1)**2;S0=(t+1)**2/(8*(t-1))
J=lambda w:(w-1)/(8*w+1)
same('input inversion absorbed: R',J(R0.subs(t,1/t)),-R0.subs(t,-3*t))
same('input inversion absorbed: S',J(S0.subs(t,1/t)),-S0.subs(t,-3*t))
same('function exchange absorbed: R',-1/(8*R0.subs(t,-t)),S0)
same('function exchange absorbed: S',-1/(8*S0.subs(t,-t)),R0)

# All four locations of the target pole in the Mobius classification; use direct
# transformed functions and transformed finite values, not a reused factor identity.
for pole in [None,-1,0,1]:
    T=(lambda w:3*w+2) if pole is None else (lambda w:3/(w-pole)+2)
    F=T(t);G=T(1/t)
    values=[-1,0,1]
    if pole is None:
        finite=[T(s.Integer(a)) for a in values];lam2=s.Integer(9)
    else:
        finite=[T(s.Integer(a)) for a in values if a!=pole]+[s.Integer(2)]
        lam2=s.Rational(9,(3*pole*pole-1)**2)
    den=s.prod(F-a for a in finite)*s.prod(G-a for a in finite)
    same(f'Mobius normalized psi target pole={pole}',lam2*t*t*s.diff(F,t)*s.diff(G,t)*(F-G)**2/den,1)

# Independent Reinders computation: write F=A(u)*v, G=B(u)*v and eliminate v^2
# immediately. D(A*v)=A'*Q+A*Q'/2 is rational, so no quotient-field reducer is used.
u=s.symbols('u');Q=12*u*(u+1)*(u+4)
A=u/(8*s.sqrt(3)*(u+1));B=(u+4)/(8*s.sqrt(3)*(u+1)**2)
Fp=s.diff(A,u)*Q+A*s.diff(Q,u)/2
Gp=s.diff(B,u)*Q+B*s.diff(Q,u)/2
U=s.factor(Fp*(A-B)/(A*(A*A*Q-1)))
V=s.factor(Gp*(A-B)/(B*(B*B*Q-1)))
same('Reinders rational derivative U',U,12*s.sqrt(3)/(u+1))
same('Reinders rational derivative V',V,4*s.sqrt(3)*(u+1))
same('Reinders psi',U*V,144)
same('Reinders normalized psi',U*V/144,1)
same('Reinders F squared fiber identity',A*A*Q-1,(u-2)*(u+2)**3/(16*(u+1)))
same('Reinders G squared fiber identity',B*B*Q-1,(u-2)**3*(u+2)/(16*(u+1)**3))
for u0,ratio in [(0,3),(-4,s.Rational(1,3)),(2,s.Rational(1,3)),(-2,3)]:
    same(f'Reinders normalized finite U squared at u={u0}',(U/12).subs(u,u0)**2,ratio)
check('elliptic cubic nonsingular',s.discriminant(Q,u)!=0)
for u0 in [-2,2]:
    check(f'elliptic u coordinate unramified at {u0}',Q.subs(u,u0)!=0)
    same(f'elliptic signs agree at {u0}',(B/A).subs(u,u0),1)

receipt={'schema':1,'target':30000706,'scope':'independent bounded diagnostics, not a global classification',
         'author_manifest_sha256':manifest_expected,'passed':len(checks),'failed':0,'sympy':s.__version__,
         'source_integrity':source_results,'endpoint_models':dict(endpoint_counts),
         'degree_two_fiber_signature_counts':dict(signature_counts),
         'degree_two_fiber_representatives':representatives,
         'external_theorems_not_formalized':['Picard omission theorem','Riemann-Hurwitz','Gundersen corrected 2CM+2IM theorem','elliptic uniformization'],
         'checks':checks}
(HERE/'independent-results.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:receipt[k] for k in ['target','passed','failed','degree_two_fiber_signature_counts']},sort_keys=True))
