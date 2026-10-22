#!/usr/bin/env python3
"""Small exact diagnostics. Baire category and density are proved in the text."""
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

count=0; sections={}
def check(ok,section):
    global count
    assert bool(ok),section
    count+=1;sections[section]=sections.get(section,0)+1

# The nerve cycle has no triangle: the closure-overlap argument cannot have
# a third cover element meeting both endpoints at an intersection point.
cycle_count=0
for n in range(4,17):
    adjacent=lambda i,j: i==j or (i-j)%n in (1,n-1)
    for i in range(n):
        check(all(not(adjacent(k,i) and adjacent(k,(i+1)%n)) for k in range(n) if k not in (i,(i+1)%n)), 'cycle intersection pattern')
    check(all(not all(adjacent(i,j) for i,j in itertools.combinations(T,2)) for T in itertools.combinations(range(n),3)), 'no triple overlaps')
    # Explicit lifted paths through each vertex. The image of an intersection
    # point is an arbitrary interior point of the corresponding edge.
    for seed in range(1,8):
        u=[F(1+(seed*i+2*seed)%9,10) for i in range(n)]
        total=F(0)
        for i in range(n):
            start=F(i-1)+u[(i-1)%n]
            end=F(i)+u[i]
            check(i-1<start<i<end<i+1,'star-contained path endpoints')
            total+=F(i)-start+end-F(i)
        check(total==n,'winding number one')
        check(total/n==1,'winding number one')
    # Integral cellular boundary of a cycle: one-dimensional cycle space.
    boundary=s.zeros(n,n)
    for i in range(n):boundary[i,i]=-1;boundary[(i+1)%n,i]=1
    check(boundary.rank()==n-1,'nerve homology')
    check(boundary*s.ones(n,1)==s.zeros(n,1),'nerve homology')
    # Deleting one edge kills the cycle, illustrating why a local loop is not
    # automatically a cycle cover of the whole space.
    check(boundary[:,0:n-1].rank()==n-1,'nerve homology')
    cycle_count+=1

# Standard one-cell-per-dimension cellular complexes. H1(S2)=0,
# H1(RP2)=Z/2, H1(S1)=Z, while H1(torus)=Z^2.
complexes={'sphere':(s.zeros(1,0),s.zeros(0,1),0),
 'projective_plane':(s.zeros(1,1),s.Matrix([[2]]),0),
 'circle':(s.zeros(1,1),s.zeros(1,0),1),
 'torus':(s.zeros(1,2),s.zeros(2,1),2)}
for name,(d1,d2,rank_expected) in complexes.items():
    check(d1*d2==s.zeros(d1.rows,d2.cols),'cellular chain complexes')
    check(d1.cols-d1.rank()-d2.rank()==rank_expected,'free first homology rank')
check(smith_normal_form(s.Matrix([[2]]),domain=ZZ)==s.Matrix([[2]]),'projective torsion')
u=s.symbols('u')
check(s.solve(2*u,u)==[0],'torsion cannot map nontrivially to Z')

# Finite incidence-witness encodings, not a finite model of Baire category.
# A prefix chain has a proper member containing B iff it has such a member
# that additionally omits a singleton U. This diagnoses exactly the witness
# enumeration used in equation(4), with a fixed nonempty B.
incidence_cases=0
for n in range(2,6):
    X=set(range(n))
    for order in itertools.permutations(range(n)):
        chain=[set(order[:k]) for k in range(1,n+1)]
        for size in (1,2):
            if size>n:continue
            for B in itertools.combinations(range(n),size):
                B=set(B)
                left=any(B<=K and K!=X for K in chain)
                right=any(B<=K and j not in K for K in chain for j in X)
                check(left==right,'incidence witness enumeration')
                incidence_cases+=1
# A transitive action may have local orbit interior: rational additive
# translations model the local one-step inclusion, without replacing S1.
for j in range(1,10):
    eps=F(j,100)
    for k in range(-4,5):
        t=F(k,5)*eps
        check(abs(t)<eps,'local translation neighborhood controls')

receipt={'problem_id':30006161,'result':'PASS','assertions':count,'sections':sections,
 'cycle_lengths_checked':list(range(4,17)),'incidence_cases':incidence_cases,
 'arithmetic':'exact rational and integer matrices',
 'artifact_sha256':sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),
 'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Finite supporting diagnostics only. No numerical or finite certificate of comeagreness, ray density, or a solution of the exceptional-surface problem is asserted.'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
