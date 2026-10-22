"""Independent rational first-jet and geometry controls; imports no candidate code."""
from fractions import Fraction as Q
import itertools, json, random, sys
def need(ok,msg):
    if not ok: raise ValueError(msg)
def z(n): return [[Q(0) for j in range(n)] for i in range(n)]
def copy(a): return [r[:] for r in a]
def zero(a): return all(x==0 for r in a for x in r)
def coordinate_torsion(L, derivatives):
    # d[a][k][j] = partial_a L^k_j; direct coordinate-index definition.
    n=len(L); r={}
    for i in range(n):
        for j in range(i+1,n):
            r[i,j]=[sum(L[a][i]*derivatives[a][k][j]-L[a][j]*derivatives[a][k][i]
                       -L[k][a]*(derivatives[i][a][j]-derivatives[j][a][i])
                       for a in range(n)) for k in range(n)]
    return r
def collar(L,D):
    n=len(L);return [[sum((L[k][a]-(L[-1][-1] if k==a else 0))*D[a][j]
                          for a in range(n-1)) for j in range(n-1)] for k in range(n-1)]
def direct(L,D):
    d=[z(len(L)) for _ in L];d[-1]=D
    return coordinate_torsion(L,d)
def compositions(n):
    if n==0: yield ()
    for k in range(1,n+1):
        for p in compositions(n-k): yield (k,)+p
def schedule(parts,chosen,mus):
    # Keep the original block order and move only the chosen terminal vector.
    n=sum(parts); last=sum(parts[:chosen+1])-1
    permutation=[i for i in range(n) if i!=last]+[last]
    old=z(n);start=0
    for size,mu in zip(parts,mus):
        for i in range(start,start+size):
            old[i][i]=mu
            if i+1<start+size:old[i][i+1]=Q(1)
        start+=size
    L=[[old[i][j] for j in permutation] for i in permutation]
    initial=copy(L); stages=0; direct_stages=0
    def stage(changes):
        nonlocal L,stages,direct_stages
        finish=copy(L)
        for i,j,v in changes:finish[i][j]=Q(v)
        D=[[finish[i][j]-L[i][j] for j in range(n)] for i in range(n)]
        # For affine stages torsion is affine: two rational samples test every
        # coefficient exactly, without sharing the candidate polynomial class.
        for t in [Q(-2,3),Q(7,5)]:
            M=[[L[i][j]+t*D[i][j] for j in range(n)] for i in range(n)]
            need(zero(collar(M,D)),'image/kernel stage constraint')
            if n<=4:need(all(not any(v) for v in direct(M,D).values()),'direct coordinate torsion')
        L=finish;stages+=1
        direct_stages+=int(n<=4)
    stage([(i,n-1,0) for i in range(n-1)])
    start=0; angular=[]
    for b,(size,mu) in enumerate(zip(parts,mus)):
        ids=[permutation.index(i) for i in range(start,start+size) if i!=last]
        if ids:angular.append((ids,mu))
        start+=size
    for ids,mu in angular:
        stage([(n-1,n-1,mu)])
        for a,b in zip(ids,ids[1:]):stage([(a,b,0)])
        stage([(i,i,0) for i in ids]+[(n-1,n-1,0)])
    need(zero(L),'final matrix')
    need([[initial[permutation.index(i)][permutation.index(j)] for j in range(n)] for i in range(n)]==old,'original numerical Jordan restored')
    return stages,direct_stages
def det(a):
    a=copy(a);n=len(a);value=Q(1)
    for i in range(n):
        p=next((j for j in range(i,n) if a[j][i]),None)
        if p is None:return Q(0)
        if p!=i:a[i],a[p]=a[p],a[i];value=-value
        v=a[i][i];value*=v
        for j in range(i+1,n):
            f=a[j][i]/v
            for k in range(i+1,n):a[j][k]-=f*a[i][k]
    return value
def geometry():
    rows=[];c=Q(3,5);s=Q(4,5)
    f=[c,s];nu=f[:];df=[[-s,c]];dn=[[-s,c]]
    for dim in range(1,9):
        dot=lambda a,b:sum(x*y for x,y in zip(a,b))
        need(dot(nu,nu)==1 and all(dot(nu,v)==0 for v in df),'recursive normal')
        determinant=det([*df,nu]);need(determinant!=0,'recursive immersion')
        rows.append({'torus_dimension':dim,'ambient_dimension':dim+1,'exact_frame_determinant':str(determinant)})
        e=Q(1,100**dim)
        f=[x+e*c*y for x,y in zip(f,nu)]+[e*s]
        df=[[x+e*c*y for x,y in zip(a,b)]+[Q(0)] for a,b in zip(df,dn)]+[[-e*s*y for y in nu]+[e*c]]
        dn=[[c*x for x in a]+[Q(0)] for a in dn]+[[-s*y for y in nu]+[c]]
        nu=[c*y for y in nu]+[s]
    return rows
def run():
    rng=random.Random(6021094); jet_cases=jet_components=0
    for n in range(1,10):
        for _ in range(31):
            L=z(n);D=z(n)
            for i in range(n):
                for j in range(n):
                    if i!=n-1 or j==n-1:
                        L[i][j]=Q(rng.randrange(-19,20),rng.randrange(1,8))
                        D[i][j]=Q(rng.randrange(-19,20),rng.randrange(1,8))
            found=direct(L,D);c=collar(L,D)
            for (i,j),v in found.items():
                want=[c[k][i] for k in range(n-1)]+[Q(0)] if j==n-1 else [Q(0)]*n
                need(v==want,'generic coordinate identity');jet_components+=len(v)
            jet_cases+=1
    families=stages=direct_stages=0
    for n in range(2,7):
        for p in compositions(n):
            for chosen in range(len(p)):
                for mus in [[Q(0)]*len(p),[Q((-1)**i*(i+2),i+3) for i in range(len(p))]]:
                    a,b=schedule(p,chosen,mus);families+=1;stages+=a;direct_stages+=b
    for p,c in [((13,),0),((2,3,1,2),1),((1,2,1,3),0),((3,3,3),2)]:
        a,b=schedule(p,c,[Q(5,7)]*len(p));families+=1;stages+=a;direct_stages+=b
    faults={}
    L=z(4);D=z(4);L[0][1]=1;L[1][2]=1;D[1][2]=-1
    faults['reverse_arrow']=any(any(v) for v in direct(L,D).values())
    L=z(4);D=z(4);L[0][1]=L[1][2]=Q(2,3);D[0][1]=D[1][2]=1
    faults['simultaneous_nilpotent_cutoff']=any(any(v) for v in direct(L,D).values())
    L=z(2);D=z(2);L[0][0]=Q(3,7);L[1][1]=Q(4,7);D[0][0]=1
    faults['unmatched_scalar']=any(any(v) for v in direct(L,D).values())
    L=z(2);D=z(2);L[0][0]=Q(3,7);L[1][1]=Q(6,7);D[0][0]=1;D[1][1]=2
    faults['distinct_spectral_cutoff']=any(any(v) for v in direct(L,D).values())
    # Dependence on angular coordinates would invalidate the one-variable reduction.
    L=z(2);L[0][0]=1;L[1][1]=2;dd=[z(2),z(2)];dd[0][1][1]=1
    faults['angular_coefficient_added']=any(any(v) for v in coordinate_torsion(L,dd).values())
    # Same pointwise spectrum does not force a fixed type on an open coefficient chart.
    faults['companion_repeated_root_not_open']=all(Q(0)**2+4*Q(1,10**k)!=0 for k in range(1,12))
    need(all(faults.values()),'fault did not trigger')
    rows=geometry()
    return {'status':'PASS','imports_candidate_code':False,'exact_arithmetic':'fractions; direct coordinate torsion and two-point affine coefficient identity',
            'generic_first_jet_cases':jet_cases,'generic_scalar_components':jet_components,
            'Jordan_families':families,'affine_stages':stages,'direct_coordinate_stages':direct_stages,
            'recursive_geometry_controls':rows,'unconditional_detected_faults':faults,
            'n1':'empty alternating pair list; general smooth scalar proof in frozen derivation',
            'limits':'Finite checks do not prove all dimensions, global embedding or novelty; those are analytic argument and UNKNOWN priority.'}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
