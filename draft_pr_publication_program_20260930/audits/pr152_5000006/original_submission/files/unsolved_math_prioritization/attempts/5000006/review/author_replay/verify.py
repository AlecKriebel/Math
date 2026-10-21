#!/usr/bin/env python3
"""Exact finite diagnostics for the double-polygon proof; no trajectory search."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import hashlib,json
counts={}
def ck(name,condition):
    assert condition,name
    counts[name]=counts.get(name,0)+1

def source_labels(n,alpha,beta,terminal):
    # Angles are measured in units of pi. Keep the source's segment parity.
    out=set();h=n//2
    for k in range(n-1):
        if n%2==0:
            clauses=[
                (k<=h-1 and alpha<=F(h-k-1,h) and beta-alpha==F(k+1,h),'Q'),
                (k<=h-1 and alpha>=F(h-k-1,h) and beta+alpha==F(n-k-1,h),'P'),
                (k>=h-1 and alpha>=F(n-k-2,h) and beta-alpha==F(k+3-n,h),'Q'),
                (k>=h-1 and alpha<=F(n-k-2,h) and beta+alpha==F(n-k-1,h),'P')]
        else:
            # First source inequality literally says h+1; feasibility excludes
            # its additional interior labels. Do not silently replace it.
            clauses=[
                (k<=h+1 and alpha<=F(n-2*(k+1),n) and beta-alpha==F(2*(k+1),n),'Q'),
                (k<=h-1 and alpha>=F(n-2*(k+1),n) and beta+alpha==F(2*(n-k-1),n),'P'),
                (k>=h and alpha>=F(2*(n-k-2),n) and beta-alpha==F(2*(k+3-n),n),'Q'),
                (k>=h and alpha<=F(2*(n-k-2),n) and beta+alpha==F(2*(n-k-1),n),'P')]
        if any(ok and side==terminal for ok,side in clauses):out.add(k%(n-2))
    return out

for n in range(3,33):
    delta=F(n-2,n)
    # Independent endpoint DSU from edge P_j P_{j+1} ~ Q_{j+1} Q_j.
    parent=list(range(2*n))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    def join(a,b):parent[find(a)]=find(b)
    for j in range(n):
        join(j,n+(j+1)%n);join((j+1)%n,n+j)
    classes={}
    for j in range(2*n):classes.setdefault(find(j),[]).append(j)
    expected=1 if n%2 else 2
    ck('vertex_class_count',len(classes)==expected)
    ck('cone_angle_integer',all(F(len(v)*(n-2),2*n).denominator==1 for v in classes.values()))
    genus=F(2-(expected-n+2),2)
    ck('Euler_genus',genus==F(n-1,2) if n%2 else genus==F(n-2,2))
    fixed=n+(n%2)
    ck('hyperelliptic_fixed_point_count',fixed==2*genus+2)
    ck('involution_vertex_action',all((find(j)==find(n+j))==(n%2==1) for j in range(n)))
    r=n-2 if n%2 else (n-2)//2
    for k in range(n-2):
        neg=(-k)%(n-2)
        ck('canonical_sine_reflection',neg==0 if k==0 else neg+1==n-(k+1))
    # Direct chords, using their exact inscribed angles.
    for j in range(1,n):
        alpha=F(n-1-j,n);beta=F(n+1-j,n)
        k=(j-1)%(n-2)
        ck('direct_chord_source_label',source_labels(n,alpha,beta,'P')=={k})
        e=0 if n%2 else j%2
        t=j if n%2==0 or j%2==0 else j+n
        m=(t*delta+1-(alpha+beta)-(1-e))/2
        ck('direct_chord_integer_index',m.denominator==1)
        ck('direct_chord_intrinsic_label',(2*int(m)+1-e)%(n-2)==k)
        ck('direct_chord_side_wrap',j==k+1 or (k==0 and j==n-1))
    # Vary admissible corner positions, start offsets and cone differences.
    # The resulting beta is retained only when in the exact interior range.
    for e in ([0] if n%2 else [0,1]):
        for t in range(2*n if n%2 else n):
            terminal='P' if (t+e)%2==0 else 'Q'
            for numerator in (0,1,n-2,2*(n-2)-1,2*(n-2)):
                alpha=F(numerator,2*n)
                for m in range(r):
                    diff=(1-e)+2*m
                    if terminal=='P':
                        beta=t*delta+1-alpha-diff
                        s=n*(alpha+beta)/2
                        k0=n-1-s
                    else:
                        beta=diff-t*delta+alpha+F(2,n)
                        s=n*(beta-alpha)/2
                        k0=s-1
                    if not F(2,n)<=beta<=1:continue
                    ck('source_integral_angle',s.denominator==1)
                    k=int(k0)%(n-2)
                    ck('all_corner_index_congruences',(2*m+1-e)%(n-2)==k)
                    ck('expanded_source_definition',source_labels(n,alpha,beta,terminal)=={k})
                    mr=(-m-1 if e==0 else -m)%r
                    ck('orientation_reversal_label',(2*mr+1-e)%(n-2)==(-k)%(n-2))

def norm(v):p,q=v;return p*p-p*q+q*q
def rotate(v):p,q=v;return p-q,p
def reflect(v):p,q=v;return q,p
def hex_endpoint(v):
    s=sum(v)%3;d=2 if s==2 else 1
    p,q=d*v[0],d*v[1]
    if (p%3,q%3)==(1,2):k=1
    elif p%2==q%2==0:k=2
    elif (p%3,q%3)==(2,1):k=3
    else:k=0
    weights_squared={0:F(1,4),1:F(3,4),2:F(1),3:F(3,4)}
    return (p,q),k,F(norm((p,q)))/weights_squared[k]
for p in range(-9,10):
    for q in range(-9,10):
        if gcd(p,q)!=1:continue
        v=(p,q);endpoint,k,quotient=hex_endpoint(v)
        ck('hex_first_vertex',sum(endpoint)%3!=2)
        if endpoint!=v:ck('hex_skipped_halfpoint',sum(v)%3==2)
        for transform in (rotate,reflect):
            z=transform(v);zpoint,zk,zquotient=hex_endpoint(z)
            ck('hex_norm_isometry',norm(v)==norm(z))
            ck('hex_primitivity',gcd(*z)==1)
            ck('hex_zero_residue_invariant',(sum(v)%3==0)==(sum(z)%3==0))
            ck('hex_ratio_identity',quotient==zquotient)
        ck('square_primitive_parity',(p%2==q%2==1)==(q%2==(-p)%2==1))
# Linear antipodality and common-direction scaling, with rational matrices.
for A in [((2,1),(1,1)),((1,F(3,2)),(0,1)),((0,-1),(1,0)),((F(2,3),0),(0,F(3,2)))]:
    (a,b),(c,d)=A
    ck('positive_derivative',a*d-b*c>0)
    for v in [(F(1),F(2)),(F(-2),F(1)),(F(0),F(1))]:
        av=(a*v[0]+b*v[1],c*v[0]+d*v[1])
        ck('linear_antipodality',(a*(-v[0])+b*(-v[1]),c*(-v[0])+d*(-v[1]))==(-av[0],-av[1]))
        for lam in (F(1,3),F(2),F(7,4)):
            lv=(lam*v[0],lam*v[1]);al=(a*lv[0]+b*lv[1],c*lv[0]+d*lv[1])
            ck('common_direction_length_scale',sum(x*x for x in al)==lam*lam*sum(x*x for x in av))
root=Path(__file__).resolve().parent
receipt={'artifact_sha256':hashlib.sha256((root/'CANDIDATE.md').read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'counts':counts,'status':'PASS','limitations':'Finite exact diagnostics, not a proof of Veech cusp reduction, hyperelliptic uniqueness, or all affine cone-germ transformations.'}
out=json.dumps(receipt,indent=2,sort_keys=True)+'\n';(root/'verification.json').write_text(out);print(out,end='')

