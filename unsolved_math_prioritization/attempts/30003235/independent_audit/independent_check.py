#!/usr/bin/env python3
"""Independent exact finite audit controls. This is not an infinite-proof verifier."""
import argparse
from fractions import Fraction as Q
from pathlib import Path
from math import lcm, isqrt
import hashlib
import itertools
import json
import random
import sys

ANCHOR='b499c40203ef2203d86d3dd6fd6e612944d7cbad92edb801170626965bc07b90'
COUNTS={}
class Rejected(Exception): pass

def require(ok,category,detail):
    if not ok: raise Rejected(category+': '+detail)
    COUNTS[category]=COUNTS.get(category,0)+1

def duplicate_guard(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise Rejected('duplicate JSON key')
        d[k]=v
    return d

def load(path):
    return json.loads(path.read_text(), object_pairs_hook=duplicate_guard,
                      parse_constant=lambda x: (_ for _ in ()).throw(Rejected('nonfinite JSON')))

def norm(x):
    x=Q(x); r=x-x.numerator//x.denominator
    return min(r,1-r)

def det(v):
    return sum((-1)**sum(p[a]>p[b] for a in range(3) for b in range(a+1,3))*
               v[0][p[0]]*v[1][p[1]]*v[2][p[2]] for p in itertools.permutations(range(3)))

def rank(rows):
    basis=[]
    for row in rows:
        row=list(map(Q,row))
        for pivot,v in basis:
            z=row[pivot]
            row=[a-z*b for a,b in zip(row,v)]
        if any(row):
            pivot=next(k for k,x in enumerate(row) if x)
            z=row[pivot]; basis.append((pivot,[a/z for a in row]))
    return len(basis)

def hp(A,B,i,j):
    k=lcm(i.numerator,j.numerator)
    return max(abs(Q(A))**int(k/i),abs(Q(B))**int(k/j)),k

def validate_probe(p):
    require(type(p) is dict and set(p)=={'schema','weights','point','image','rank_rows','rank_bound','global_endpoint_proved'},'input','exact fields')
    require(type(p['schema']) is int and p['schema']==1,'input','integer schema')
    require(p['global_endpoint_proved'] is False,'input','global endpoint must remain unproved')
    for key,n in [('weights',2),('point',2),('image',2)]:
        require(type(p[key]) is list and len(p[key])==n and all(type(v) is str for v in p[key]),'input','rational strings required')
    i,j=map(Q,p['weights']); x,y=map(Q,p['point']); u,v=map(Q,p['image'])
    require(i>0 and j>0 and i+j==1 and i>=j,'input','positive normalized weights in heavier order')
    require(x!=0 and x*u==1 and x*v==y,'input','projective identity')
    rows=p['rank_rows']
    require(type(rows) is list and len(rows)>0 and all(type(r) is list and len(r)==3 and all(type(v) is int for v in r) for r in rows),'input','integer rows')
    require(type(p['rank_bound']) is int and 0<=p['rank_bound']<=2,'input','rank bound')
    require(rank(rows)<=p['rank_bound'],'input','false rank claim')

def integrity(root):
    manifest=root/'MANIFEST.json'
    require(hashlib.sha256(manifest.read_bytes()).hexdigest()==ANCHOR,'frozen_integrity','anchor mismatch')
    m=load(manifest); require(type(m['schema']) is int and m['schema']==1,'frozen_integrity','schema')
    require(len(m['files'])==16,'frozen_integrity','sixteen payloads')
    names=[]
    for rec in m['files']:
        n=rec['path']; names.append(n); p=root/n
        require(p.is_file() and not p.is_symlink(),'frozen_integrity','regular file')
        b=p.read_bytes()
        require(len(b)==rec['bytes'] and hashlib.sha256(b).hexdigest()==rec['sha256'],'frozen_integrity','payload drift')
    actual=sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
    require(sorted(names+['MANIFEST.json'])==actual and len(actual)==17,'frozen_integrity','exact file inventory')
    final=(root/'PROOF.md').read_bytes()
    for n in range(1,6):
        require(final.startswith((root/'checkpoints'/f'{n:02d}_PROOF.md').read_bytes()),'chronology','checkpoint is not a cumulative prefix')
    require(final==(root/'checkpoints/05_PROOF.md').read_bytes(),'chronology','final checkpoint differs')
    c=load(root/'claims.json')
    require(c['status']=='unsolved' and c['author_approaches']==5 and c['global_endpoint_proved'] is False,'scope','disposition')

def mathematics():
    rng=random.Random(8675309)
    weights=sorted(set((Q(a,d),Q(d-a,d)) for d in range(2,10) for a in range(1,d) if 2*a>=d))
    for n in range(1400):
        i,j=rng.choice(weights); x=Q(rng.choice([-7,-3,-1,1,2,5]),rng.randrange(1,6)); y=Q(rng.randrange(-9,10),rng.randrange(1,6))
        u,v=1/x,y/x
        A,B=rng.randrange(-9,10),rng.randrange(-9,10)
        if not (A or B): A=1
        # Choose C nearest to -Au-Bv so the delicate small-form case is exercised.
        raw=-(A*u+B*v); C=(raw+Q(1,2)).numerator//(raw+Q(1,2)).denominator
        f=A*u+B*v+C; K=1+abs(u)+abs(v)
        require(x*f==C*x+B*y+A and 1/u==x and v/u==y,'inversion','form and involution')
        require(abs(f)<=Q(1,2) and abs(C)<=K*max(abs(A),abs(B)),'inversion','constant coefficient bound')
        new,k=hp(A,B,i,j); old,_=hp(C,B,i,j)
        require(old<=K**int(k/i)*new,'weighted_height','heavier-coordinate bound')
        # Rational translation includes the extra factor d in the form value.
        r,s=Q(rng.randrange(-4,5),3),Q(rng.randrange(-4,5),5); d=15
        trans=d*(A*(x-r)+B*(y-s)+C)
        require(trans==(d*A)*x+(d*B)*y+d*C-d*A*r-d*B*s,'translation','integer transformed form')
        dil,_=hp(d*A,d*B,i,j)
        require(dil<=d**int(k/min(i,j))*new,'translation','height bound')
    # The weight order cannot simply be removed from this estimate.
    i,j=Q(1,3),Q(2,3); lhs,k=hp(100,100,i,j); rhs,_=hp(0,100,i,j)
    require(lhs>3**int(k/i)*rhs,'negative_boundary','wrong weight order fails height estimate')
    # Degenerate old coefficient pair is handled separately, including negative x.
    for x in [Q(-5,3),Q(1,7),Q(8)]:
        for A in range(1,8):
            require(Q(A*A*A,1)/abs(x)>=1/abs(x),'zero_old_pair','equal-weight exact constant')
    for n in range(400):
        a=Q(rng.randrange(-15,16),rng.randrange(1,12)); r=Q(rng.randrange(-8,9),rng.randrange(1,8)); s=Q(rng.randrange(-8,9),rng.randrange(1,8)); q=rng.randrange(1,80)
        d=lcm(r.denominator,s.denominator); b=s-a*r; K=max(Q(d),abs(d*r))
        require(max(norm(d*q*a),norm(d*q*b))<=K*norm(q*a),'coefficient_reduction','rational-point dilation')
    # Exact inversion Lipschitz bounds on both sides of the excluded pole.
    for sign in [-1,1]:
        delta=Q(1,7); R=Q(11,3)
        for n in range(1,50):
            x=sign*(delta+(R-delta)*Q(n,51)); y=sign*(delta+(R-delta)*Q(n+1,51))
            diff=abs(1/x-1/y); dx=abs(x-y)
            require(dx/(R*R)<=diff<=dx/(delta*delta),'local_dimension','bi-Lipschitz constants')
    for t in [Q(2),Q(5,2),Q(3),Q(4)]:
        prev,q=1,2
        for n in range(4):
            if t.denominator==1: digit=q**(int(t)-1)
            else:
                digit=isqrt(q**3)
                if digit*digit<q**3: digit+=1
            nxt=digit*q+prev
            require(nxt**t.denominator>=q**t.numerator and nxt**t.denominator<=(3**t.denominator)*q**t.numerator,'continued_fraction','real-exponent recurrence bound')
            prev,q=q,nxt
    for sigma in [Q(1,2),Q(2,5),Q(1,3)]:
        for n in range(1,20):
            s=sigma*Q(n,n+1); eps=(1/s-1/sigma)/2
            require(eps>0 and 1/s-eps-1/sigma==eps,'weight_perturbation','individual positive excess')
    for i,j in [(Q(1,2),Q(1,2)),(Q(1,3),Q(2,3)),(Q(2,3),Q(1,3)),(Q(1,4),Q(3,4))]:
        tau=int(1/min(i,j))
        for a in [Q(-7,3),Q(9,4),Q(17,5)]:
            for B in range(2,35):
                raw=-a*B; A=(raw+Q(1,2)).numerator//(raw+Q(1,2)).denominator; alpha=A+a*B
                if not alpha: continue
                b=Q(5,11); C=-1; beta=C+b*B; center=-beta/alpha; X=abs(center)+1
                height,k=hp(A,B,i,j); kap=B**tau*max(norm(B*a),norm(B*b)); eta=kap/4
                require(abs(alpha)<=abs(a)*B/2,'resonance','near-parallel domain')
                require(height>=B**(tau*k),'resonance','h-minus equals one for |a|>=2')
                require(abs(alpha)>=kap/(2*(X+1)*B**tau),'resonance','endpoint slope lower bound')
                require(height*abs(alpha)**k >= (kap/(2*(X+1)))**k,'resonance','equivalent powered length bound')
    for n in range(400):
        rows=[[rng.randrange(-8,9) for _ in range(3)] for _ in range(3)]
        x0,a,b=Q(-3,5),Q(7,4),Q(2,9)
        cols=[[A,B,A*x0+B*(a*x0+b)+C] for A,B,C in rows]
        HA=max(abs(v[0]) for v in cols); HB=max(abs(v[1]) for v in cols); E=max(abs(v[2]) for v in cols)
        require(det(rows)==det(cols),'determinant','column identity')
        require(abs(det(cols))<=6*HA*HB*E,'determinant','six-term bound')
    # Enumerate genuine height-window dangerous families, including unequal weights.
    for i,j in [(Q(1,2),Q(1,2)),(Q(1,3),Q(2,3)),(Q(2,3),Q(1,3))]:
        d=lcm(i.denominator,j.denominator); N=3; H=N**d; R=3; a=Q(7,4); b=Q(-13,24); x0=Q(1,2); Ca=1+abs(a)
        r=1/(24*Ca*N**int(d*(1+max(i,j)))); eta=Q(1,24*R); rows=[]
        for A in range(-N**int(d*i),N**int(d*i)+1):
            for B in range(-N**int(d*j),N**int(d*j)+1):
                if not(A or B): continue
                height,k=hp(A,B,i,j)
                if not ((Q(H,R))**k<=height<=H**k): continue
                raw=-(A*x0+B*(a*x0+b)); C=(raw+Q(1,2)).numerator//(raw+Q(1,2)).denominator
                F=A*x0+B*(a*x0+b)+C; excess=abs(F)-abs(A+a*B)*r
                if excess<=0 or excess**k*height<eta**k: rows.append([A,B,C])
        require(6*Ca*N**int(d*(1+max(i,j)))*r+6*eta*R==Q(1,2),'determinant_family','scale is strictly below one')
        require(rows and rank(rows)<=2,'determinant_family','actual dangerous family rank')
    require(det([[1,0,0],[0,1,0],[0,0,1]])==1,'negative_boundary','rank-three integer boundary')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,required=True); ap.add_argument('--probe',type=Path,required=True); args=ap.parse_args()
    try:
        validate_probe(load(args.probe)); integrity(args.root); mathematics()
    except (Rejected,ValueError,TypeError,KeyError,OSError,ZeroDivisionError) as e:
        print(json.dumps({'status':'FAIL','reason':str(e)},sort_keys=True)); return 1
    print(json.dumps({'status':'PASS','scope':'independent_exact_finite_controls_only','counts':COUNTS,'total':sum(COUNTS.values()),'frozen_manifest_sha256':ANCHOR},sort_keys=True)); return 0
if __name__=='__main__': sys.exit(main())
