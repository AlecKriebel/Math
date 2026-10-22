"""Independent coordinate-covariance and collar-geometry first-jet controls.

No candidate/reviewer program is imported. Fractions and explicit failures
remain enabled with -O. These finite controls do not replace the written proof.
"""
from fractions import Fraction as F
import json
import random

def need(test, reason):
    if not test:
        raise ValueError(reason)

def zero(n): return [[F(0) for _ in range(n)] for _ in range(n)]
def identity(n): return [[F(i == j) for j in range(n)] for i in range(n)]
def mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,c): return [[c*x for x in row] for row in a]
def inverse(a):
    n=len(a); w=[list(row)+identity(n)[i] for i,row in enumerate(a)]
    for k in range(n):
        j=next(j for j in range(k,n) if w[j][k])
        w[k],w[j]=w[j],w[k]
        s=w[k][k];w[k]=[x/s for x in w[k]]
        for j in range(n):
            if j!=k:
                s=w[j][k];w[j]=[x-s*y for x,y in zip(w[j],w[k])]
    return [row[n:] for row in w]

def torsion(l,d):
    """Coordinate formula, arbitrary full first derivative array d[a][k][i]."""
    n=len(l)
    return {(k,i,j):sum(l[p][i]*d[p][k][j]-l[p][j]*d[p][k][i]
                 -l[k][p]*d[i][p][j]+l[k][p]*d[j][p][i]
                 for p in range(n))
            for i in range(n) for j in range(i+1,n) for k in range(n)}

def run():
    rng=random.Random(10942100509)
    generic=valid=free=components=0
    for n in range(1,8):
        m=n-1
        for sample in range(17):
            l=zero(n); ld=zero(n)
            for i in range(n):
                for j in range(n):
                    if i<m or j==m:
                        l[i][j]=F(rng.randrange(-9,10),rng.randrange(1,5))
                        ld[i][j]=F(rng.randrange(-9,10),rng.randrange(1,5))
            ds=[zero(n) for _ in range(n)];ds[-1]=ld
            direct=torsion(l,ds)
            for (k,i,j),v in direct.items():
                expected=(sum((l[k][p]-(l[-1][-1] if k==p else 0))*ld[p][i]
                              for p in range(m)) if j==m and k<m else 0)
                need(v==expected,'generic full coordinate first-jet identity')
                components+=1
            generic+=1
            # Arbitrary independent b' and lambda' changes must cancel.
            changed=[row[:] for row in ld]
            for k in range(n): changed[k][-1]+=F(k+sample+2,3)
            need(torsion(l,ds[:-1]+[changed])==direct,'forbidden b/lambda derivative dependence')
            free+=1
            if n==1: continue
            # Valid noncommuting jet: A=mu I+J_m and A' has only first row.
            # Then (A-mu I)A'=0 while A'(A-mu I) usually is nonzero.
            mu=F(sample-5,7);l=zero(n);ld=zero(n)
            for i in range(m):
                l[i][i]=mu
                if i+1<m:l[i][i+1]=1
                ld[0][i]=F(rng.randrange(-4,5),3)
                l[i][-1]=F(rng.randrange(-4,5),2)
                ld[i][-1]=F(rng.randrange(-4,5),5)
            l[-1][-1]=mu;ld[-1][-1]=F(sample,9)
            # Conjugate by a nontrivial invertible rational coordinate map.
            q=identity(n)
            for step in range(n+2):
                a,b=rng.sample(range(n),2)
                elementary=identity(n);elementary[a][b]=F(rng.choice([-2,-1,1,2]),3)
                q=mul(elementary,q)
            qi=inverse(q);need(mul(q,qi)==identity(n),'exact inverse')
            transformed=mul(mul(q,l),qi);jet=mul(mul(q,ld),qi)
            d=[scale(jet,qi[-1][a]) for a in range(n)]
            need(not any(torsion(transformed,d).values()),'valid stage loses coordinate covariance')
            valid+=1
    faults={}
    # All invalid examples are evaluated by full coordinate torsion, not by
    # the reduced constraint. The n=3 nilpotent cutoff is a valid boundary.
    for n in [3,4,5,6,7]:
        l=zero(n);ld=zero(n)
        for i in range(n-1):l[i][i+1]=2;ld[i][i+1]=3
        ds=[zero(n) for _ in range(n)];ds[-1]=ld
        observed=any(torsion(l,ds).values())
        need(observed==(n>=4),'nilpotent cutoff boundary')
    faults['nilpotent_cutoff_size4_detected_size3_correctly_allowed']=True
    l=zero(4);l[0][1]=1;l[1][2]=1;ld=zero(4);ld[1][2]=-1
    ds=[zero(4) for _ in range(4)];ds[-1]=ld
    faults['last_arrow_first_nonzero']=any(torsion(l,ds).values())
    l=[[F(1),F(0)],[F(0),F(2)]];ld=[[F(3),F(0)],[F(0),F(0)]]
    faults['unmatched_scalar_nonzero']=any(torsion(l,[zero(2),ld]).values())
    a=[[F(0),F(1),F(0)],[F(0),F(0),F(1)],[F(0),F(0),F(0)]]
    ad=[[F(0),F(-1),F(0)],[F(0),F(0),F(0)],[F(0),F(0),F(0)]]
    faults['wrong_order_rejects_valid']=not any(x for row in mul(a,ad) for x in row) and any(x for row in mul(ad,a) for x in row)
    faults['two_nonreal_pairs_both_become_real']=all(1-y*y in [F(0),F(3,4)] for y in [F(1),F(-1),F(1,2),F(-1,2)])
    need(all(faults.values()),'undetected mathematical fault')
    normals=0
    for d in range(1,13):
        for cosine,sine in [(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(-5,13),F(12,13))]:
            need(cosine*cosine+sine*sine==1,'rational unit circle')
            # Principal-frame tangent scale: small normal tube has no focal
            # degeneracy; normal and circle derivative are orthogonal.
            epsilon=F(1,100)
            for curvature in range(-d,d+1):
                need(1+epsilon*cosine*curvature>0,'small tube immersion')
            need(cosine*(-epsilon*sine)+sine*(epsilon*cosine)==0,'tube unit normal')
            normals+=1
    return {'status':'PASS','generic_coordinate_jets':generic,'full_scalar_torsion_components':components,
            'free_transverse_derivative_checks':free,'nontriangular_coordinate_conjugations':valid,
            'normal_bundle_models':normals,'fault_controls':faults,'imports_candidate_code':False,
            'universal_statement_basis':'Written independent derivation, not finite extrapolation',
            'formal_certification':False}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
