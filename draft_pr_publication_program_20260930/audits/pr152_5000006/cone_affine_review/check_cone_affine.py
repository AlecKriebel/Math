#!/usr/bin/env python3
"""Independent finite falsification checks; analytical proof is in REVIEW.md.
Uses a literal transcription of Fuchs Definition 2.1 with its p.502 sign.
No imports from the submission verifier and no trajectory simulation.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import sin, cos, atan2, floor, pi
import hashlib, json

counts={}
def check(name, value):
    if not value:
        raise AssertionError(name)
    counts[name]=counts.get(name,0)+1

def clauses(n,a,b,parity=None):
    h=n//2; labels=set()
    for k in range(n-1): # Fuchs includes duplicate An-2=A0 for the other side
        if n%2==0:
            cases=[
                ('even',k<=h-1 and a<=Q(h-k-1,h) and b-a==Q(k+1,h)),
                ('odd',k<=h-1 and a>=Q(h-k-1,h) and b+a==Q(n-k-1,h)),
                ('even',k>=h-1 and a>=Q(n-k-2,h) and b-a==Q(k+3-n,h)),
                ('odd',k>=h-1 and a<=Q(n-k-2,h) and b+a==Q(n-k-1,h))]
        else:
            cases=[
                ('even',k<=h+1 and a<=Q(n-2*k-2,n) and b-a==Q(2*k+2,n)),
                ('odd',k<=h-1 and a>=Q(n-2*k-2,n) and b+a==Q(2*n-2*k-2,n)),
                ('even',k>=h and a>=Q(2*n-2*k-4,n) and b-a==Q(2*k+6-2*n,n)),
                ('odd',k>=h and a<=Q(2*n-2*k-4,n) and b+a==Q(2*n-2*k-2,n))]
        if any(v and (parity is None or p==parity) for p,v in cases): labels.add(k%(n-2))
    return labels

topology=[]
angle_cases=0
for n in range(3,81):
    modulus=n-2; r=modulus if n%2 else modulus//2
    corners={(sheet,j) for sheet in (0,1) for j in range(n)}
    cycles=[]
    while corners:
        begin=min(corners); seq=[]; c=begin
        while c not in seq:
            seq.append(c); corners.remove(c); c=(1-c[0],(c[1]+1)%n)
        check('cycle_closes', c==begin)
        cycles.append(seq)
    check('cone_classes',len(cycles)==(1 if n%2 else 2))
    check('cone_angle',all(Q(len(c)*(n-2),n)==2*r for c in cycles))
    genus=Q(n-len(cycles),2)
    check('genus_integral',genus.denominator==1)
    check('genus_formula',genus==Q(n-1,2) if n%2 else genus==Q(n-2,2))
    where={c:i for i,cyc in enumerate(cycles) for c in cyc}
    ivfixed=sum(all(where[(1-s,j)]==i for s,j in cyc) for i,cyc in enumerate(cycles))
    check('involution_vertex_action',ivfixed==(1 if n%2 else 0))
    fixed=n+ivfixed
    check('fixed_point_count',fixed==2*genus+2)
    topology.append({'n':n,'corner_cycle_sizes':[len(c) for c in cycles],
                     'cone_angle_over_pi':2*r,'cone_zero_order':r-1,
                     'genus':int(genus),'involution_fixed_points':fixed})
    # An exact partition of all allowed alpha values: source conditions are
    # linear, so endpoints plus midpoints exhaust their possible truth patterns.
    breaks={Q(0),Q(n-2,n)}
    if n%2==0:
        for k in range(n-1): breaks|={Q(h-k-1,h) for h in [n//2]}|{Q(n-k-2,n//2)}
    else:
        for k in range(n-1): breaks|={Q(n-2*k-2,n),Q(2*n-2*k-4,n)}
    for parity in ('odd','even'):
        for s in range(-n,2*n+1):
            if parity=='odd':
                lo=max(Q(0),Q(2*s,n)-1)
                hi=min(Q(n-2,n),Q(2*s-2,n))
                beta=lambda a:Q(2*s,n)-a
                expected=(n-1-s)%modulus
            else:
                lo=max(Q(0),Q(2-2*s,n))
                hi=min(Q(n-2,n),1-Q(2*s,n))
                beta=lambda a:a+Q(2*s,n)
                expected=(s-1)%modulus
            if lo>hi: continue
            bs=sorted({lo,hi}|{x for x in breaks if lo<=x<=hi})
            samples=set(bs)|{(a+b)/2 for a,b in zip(bs,bs[1:])}
            for a in samples:
                b=beta(a)
                check('source_angles_valid',Q(0)<=a<=Q(n-2,n) and Q(2,n)<=b<=1)
                check('source_residue_exact',clauses(n,a,b,parity)=={expected})
                ar=1-b; br=1-a
                source_reverse=(-expected if parity=='odd' else expected)%modulus
                check('physical_reverse_type',clauses(n,ar,br,parity)=={source_reverse})
                angle_cases+=1
    # This is the corner equation, not a billiard unfolding check. Exhaust all
    # corners/lifts whose developed germs have compatible antipodal directions.
    for e in ([0] if n%2 else [0,1]):
        for t in range(2*n if n%2 else n):
            parity='odd' if (t+e)%2==0 else 'even'
            for m in range(r):
                for sheet in (-2,-1,0,1,2):
                    cone_delta=Q(1-e)+2*m+2*r*sheet
                    if parity=='odd':
                        two_s=n*(Q(t*(n-2),n)+1-cone_delta)
                        s=two_s/2; kval=n-1-s
                    else:
                        two_s=n*(cone_delta-Q(t*(n-2),n)+Q(2,n))
                        s=two_s/2; kval=s-1
                    check('corner_integrality',s.denominator==1)
                    check('cone_label_residue',(int(kval)%modulus)==(2*m+1-e)%modulus)
                    if parity=='odd':
                        sn=n*(cone_delta-Q(t*(n-2),n)+1)/2
                        kn=n-1-sn
                    else:
                        sn=n*(Q((t-1)*(n-2),n)+1-cone_delta)/2
                        kn=sn-1
                    check('negative_chart_integrality',sn.denominator==1)
                    check('negative_chart_type',int(kn)%modulus==(-(2*m+1-e))%modulus)
        for m in range(r):
            km=(2*m+1-e)%modulus
            mr=(-m-1 if e==0 else -m)%r
            check('reversal_residue',(2*mr+1-e)%modulus==(-km)%modulus)
            check('canonical_weight_reversal',abs(sin(((km+1)*pi)/n)-sin((((-km)%modulus+1)*pi)/n))<2e-14)
    for j in range(1,n):
        a=Q(n-1-j,n); b=Q(n+1-j,n)
        check('direct_chord_label',clauses(n,a,b,'odd')=={(j-1)%modulus})

# Concrete omitted-parity ambiguity, retained as an adversarial warning rather
# than falsely counted as a candidate failure (candidate explicitly uses parity).
ambiguous={'n':5,'j':2,'alpha_over_pi':'2/5','beta_over_pi':'4/5',
           'without_parity':sorted(clauses(5,Q(2,5),Q(4,5))),
           'odd_parity':sorted(clauses(5,Q(2,5),Q(4,5),'odd'))}
check('omitting_parity_is_ambiguous',ambiguous['without_parity']==[0,1])

# Numerical adversarial probes of angle lifts: determinant signs, arbitrary
# 2pi sheet offsets, negative angles and many turns. These are not actual global
# surface automorphisms; the universal linear-lift identity is proved separately.
def angular_lift(A,theta,offset):
    a,b,c,d=A; eps=1 if a*d-b*c>0 else -1
    turns=floor(theta/(2*pi)); t=theta-2*pi*turns
    base=atan2(c,a); val=atan2(c*cos(t)+d*sin(t),a*cos(t)+b*sin(t))
    turn=(val-base)%(2*pi)
    if t<1e-13: turn=0
    elif eps<0: turn-=2*pi
    return base+turn+eps*2*pi*turns+2*pi*offset
matrices=[(2,1,1,1),(1,2,0,1),(1,0,0,3),(0,-1,1,0),
          (1,2,0,-1),(0,1,1,0),(-2,1,1,1)]
for A in matrices:
    eps=1 if A[0]*A[3]-A[1]*A[2]>0 else -1
    for theta in [-41.27,-2.2,0.123,1.74,19.91]:
        for offset in range(-3,4):
            for halfturns in range(-7,8):
                diff=angular_lift(A,theta+halfturns*pi,offset)-angular_lift(A,theta,offset)
                check('linear_halfturn_lift',abs(diff-eps*halfturns*pi)<1e-12)
            for e in [0,1]:
                for m in range(-5,6):
                    gap=(1-e)*pi+2*pi*m
                    diff=angular_lift(A,theta+gap,offset)-angular_lift(A,theta,offset)
                    check('cone_gap_after_lift',abs(diff-eps*gap)<1e-12)

root=Path(__file__).resolve().parent
receipt={'status':'PASS','independent_from_submission_verifier':True,
 'n_range':[3,80],'continuous_source_angle_partitions_checked':angle_cases,
 'counts':counts,'assertions':sum(counts.values()),'topology':topology,
 'omitted_parity_counterexample':ambiguous,
 'limitations':['No physical reflected-label unfolding simulation.',
 'Numerical GL probes test the local lift law, not existence of global maps.',
 'Classical cusp reduction and publication claims outside this review scope.'],
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'fuchs_pdf_sha256':hashlib.sha256((root/'fuchs2021.pdf').read_bytes()).hexdigest()}
(root/'checks.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='topology'},indent=2))
