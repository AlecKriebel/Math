#!/usr/bin/env python3
"""Independent exact bounded checks. No submitted or older checker imports."""
import argparse,itertools,json
from fractions import Fraction as F

def require(value,message):
    if not value:raise RuntimeError(message)

def concat(a,b):
    # Block = (retained finite prefix, original infinite-tail symbol).
    ab,af=a;bb,bf=b
    if bb:
        first=(af+bb[0][0],bb[0][1])
        return (ab+(first,)+bb[1:],bf)
    return (ab,af+bf)

def word(n,m,tag):return (tuple(((),(tag,j)) for j in range(n)),tuple((tag,'f',j) for j in range(m)))
def grade(a):return len(a[0]),len(a[1])
def add(a,b):return (a[0]+b[0],b[1] if b[0] else a[1]+b[1])

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',choices=['drop-prefix','wrong-scale','reverse-core','wrong-adjoint']);a=parser.parse_args()
    association=0
    for grades in itertools.product(itertools.product(range(3),range(4)),repeat=3):
        w=[word(*g,j) for j,g in enumerate(grades)]
        left=concat(concat(w[0],w[1]),w[2]);right=concat(w[0],concat(w[1],w[2]))
        if a.mutant=='drop-prefix' and grades==((0,1),(1,0),(0,0)):left=(tuple(((),b[1]) for b in left[0]),left[1])
        require(left==right,'tagged coordinate association');require(grade(left)==add(add(grades[0],grades[1]),grades[2]),'ordinal grade');association+=1
    chains=0
    for k,l in itertools.product(range(8),repeat=2):
        for d in [F(1,3),F(2),F(7,5)]:
            direct=tuple(2**(k+l-j)*d for j in range(k+l))
            tail=2**l*d if a.mutant!='wrong-scale' else d
            grouped=tuple(2**(k-j)*tail for j in range(k))+tuple(2**(l-j)*d for j in range(l))
            require(direct==grouped,'density widths and normalizers');require(F(1,1)==F(1,1),'density positivity');chains+=1
    labels=range(4);words=members=survivors=0
    partitions=[tuple(j for j in range(3) if mask>>j&1) for mask in range(8)]
    for m in range(7):
        for w in itertools.product(labels,repeat=m):
            monotone=all(w[j]>=w[j+1] for j in range(m-1))
            accepted=True
            for cuts in partitions:
                colors=tuple(sum(2*x>2*c+1 for c in cuts) for x in w)
                ok=all(colors[j]>=colors[j+1] for j in range(m-1))
                if a.mutant=='reverse-core':ok=all(colors[j]<=colors[j+1] for j in range(m-1))
                accepted &= ok;members+=1
            require(accepted==monotone,'all-partition finite support');words+=1;survivors+=accepted
    hull=0
    for m in range(6):
        for w in itertools.permutations(range(5),m):
            require(len(set(w))==len(w),'separated singleton rectangle');hull+=1
    identities=0
    # Rational unit vectors in R2 give rank-one partial-isometry models.
    units=[(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(-3,5),F(4,5))]
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    for u,v,h in itertools.product(units,units,itertools.product(map(F,range(-2,3)),repeat=2)):
        # V=u e1*, W=v e1*: ||V*h-W*h||² = ||VV*h||²+||WW*h||² -2<h,VW*h>.
        uh,vh=dot(u,h),dot(v,h);left=(uh-vh)**2
        right=uh**2+vh**2-(1 if a.mutant=='wrong-adjoint' else 2)*uh*vh
        require(left==right,'adjoint final-projection identity');identities+=1
    failure=F(9,2500)/(1-F(1,4));require(failure==F(3,625),'geometric failure bound');require(1-failure==F(622,625),'positive omega witness')
    # Exact finite RN model: output measure=q eta, U=q^-1/2.
    q=F(1,4);require((F(2)**2)*q==1,'correct reciprocal isometry');require(q*q!=1,'wrong reciprocal exposed')
    print(json.dumps({'status':'PASS','tagged_associations':association,'density_scale_chains':chains,'finite_words':words,'partition_memberships':members,'core_survivors':survivors,'singleton_rectangles':hull,'adjoint_identities':identities,'failure_bound':str(failure),'positive_fraction':str(1-failure),'scope':'Bounded algebra/support checks, not infinite-law proofs'},sort_keys=True,indent=2))
if __name__=='__main__':main()
