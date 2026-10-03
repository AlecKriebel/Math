#!/usr/bin/env python3
"""Independent exact controls. Does not import either frozen-packet script."""
import hashlib, itertools, json, math
from pathlib import Path

ROOT=Path(__file__).parent
PUB=ROOT.parent/'public'
IMAGE={1:(2,),2:(3,),3:(1,2),4:(5,1),5:(5,4)}

def inverse(w): return tuple(-a for a in reversed(w))
def reduce(w):
    s=[]
    for a in w:
        if s and s[-1]==-a: s.pop()
        else:s.append(a)
    return tuple(s)
def substitute(w,images=IMAGE):
    return reduce(a for b in w for a in (images[b] if b>0 else inverse(images[-b])))
def cyclic(w):
    w=reduce(w);l=0;r=len(w)
    while r-l>=2 and w[l]==-w[r-1]:l+=1;r-=1
    return w[l:r]
def necklace(w):
    return min(z[k:]+z[:k] for z in (w,inverse(w)) for k in range(len(w)))

def identity(rank):return ((0,)*rank,(0,)*(rank*(rank-1)//2))
def product(x,y):
    p,c=x;q,d=y
    return tuple(a+b for a,b in zip(p,q)),tuple(c[k]+d[k]-p[j]*q[i] for k,(i,j) in enumerate(itertools.combinations(range(len(p)),2)))
def power(x,n):
    p,c=x
    if n<0:
        x=tuple(-a for a in p),tuple(-c[k]-p[i]*p[j] for k,(i,j) in enumerate(itertools.combinations(range(len(p)),2)))
        n=-n
    out=identity(len(p))
    while n:
        if n&1:out=product(out,x)
        x=product(x,x);n//=2
    return out
def normal(w,rank):
    out=identity(rank)
    for a in w:
        p=[0]*rank;p[abs(a)-1]=1 if a>0 else -1
        out=product(out,(tuple(p),(0,)*(rank*(rank-1)//2)))
    return out
def comm(x,y):return product(product(product(x,y),power(x,-1)),power(y,-1))
def act(x,images):
    p,c=x;rank=len(p);out=identity(rank)
    ims=[normal(images[i+1],rank) for i in range(rank)]
    for a,n in zip(ims,p):out=product(out,power(a,n))
    for n,(i,j) in zip(c,itertools.combinations(range(rank),2)):
        out=product(out,power(comm(ims[i],ims[j]),n))
    return out

def no_retraction():
    alpha={i:IMAGE[i] for i in (1,2,3)}
    def residual(z):
        x=((-1,-1,1),tuple(z[:3]));y=((0,0,-1),tuple(z[3:]));a=normal((1,),3)
        p=product(act(x,alpha),power(product(y,a),-1))
        q=product(act(y,alpha),power(product(y,x),-1))
        assert p[0]==q[0]==(0,0,0)
        return p[1]+q[1]
    b=residual([0]*6);cols=[]
    for i in range(6):
        e=[0]*6;e[i]=1;cols.append(tuple(a-bb for a,bb in zip(residual(e),b)))
    E=tuple(zip(*cols))
    witness=next(v for v in itertools.product(range(5),repeat=6)
        if any(v) and all(sum(v[i]*E[i][j] for i in range(6))%5==0 for j in range(6))
        and sum(v[i]*b[i] for i in range(6))%5)
    return {'method':'collected integral Malcev normal form, not Magnus expansions',
        'matrix':E,'constant':b,'left_mod5_certificate':witness,
        'certificate_constant_mod5':sum(v*bb for v,bb in zip(witness,b))%5}

def exterior_controls():
    from fractions import Fraction
    def rank(a):
        a=[list(map(Fraction,row)) for row in a];r=0
        for j in range(len(a[0])):
            k=next((k for k in range(r,len(a)) if a[k][j]),None)
            if k is None:continue
            a[k],a[r]=a[r],a[k];z=a[r][j];a[r]=[v/z for v in a[r]]
            for k in range(len(a)):
                if k!=r:
                    z=a[k][j];a[k]=[v-z*w for v,w in zip(a[k],a[r])]
            r+=1
        return r
    pairs=list(itertools.combinations(range(5),2));cols=[]
    for i,j in pairs:
        cols.append(act(normal((i+1,j+1,-i-1,-j-1),5),IMAGE)[1])
    W=tuple(zip(*cols));v=(0,1,0,1,1,0,1,-1,-1,1)
    assert tuple(sum(a*b for a,b in zip(row,v)) for row in W)==tuple(-x for x in v)
    plus=rank([[W[i][j]+int(i==j) for j in range(10)] for i in range(10)])
    minus=rank([[W[i][j]-int(i==j) for j in range(10)] for i in range(10)])
    assert (plus,minus)==(9,10)
    return {'method':'automorphism action on collected commutator normal forms','W':W,
        'rank_W_plus_I':plus,'rank_W_minus_I':minus,'minus_one_vector':v}

def balanced_multiset_words(n):
    def counts(m,r):
        if r==1:yield (m,);return
        for a in range(m+1):
            for rest in counts(m-a,r-1):yield (a,)+rest
    for c in counts(n//2,5):
        left={s*(i+1):c[i] for i in range(5) for s in (1,-1)}
        def perm(w):
            if len(w)==n:
                if w[-1]!=-w[0]:yield w
                return
            for a in left:
                if left[a] and (not w or w[-1]!=-a):
                    left[a]-=1;yield from perm(w+(a,));left[a]+=1
        yield from perm(())

def periodic_controls():
    v=(0,1,0,1,1,0,1,-1,-1,1);rows=[];hits=[];survivors=[]
    for n in (2,4,6,8):
        words=list(balanced_multiset_words(n));classes={necklace(w) for w in words}
        keep=[]
        for w in classes:
            p,c=normal(w,5);assert not any(p)
            if c==tuple(c[-1]*a for a in v):keep.append(w)
        assert all(not any(normal(w,5)[1]) for w in keep)
        rows.append({'length':n,'words':len(words),'classes':len(classes),'kept':len(keep),'all_kept_in_gamma3':True})
        for w in keep:
            z=w
            for k in range(1,13):
                z=cyclic(substitute(z))
                if len(z)==len(w) and necklace(z)==w:hits.append((w,k))
            survivors.append({'word':''.join('abcde'[a-1] if a>0 else 'ABCDE'[-a-1] for a in w),'cyclic_length_after_12':len(z)})
    return {'independent_generator':'balanced multiset permutations; no packet imports','rows':rows,'max_period':12,'hits':hits,'length8_survivors':sorted(survivors,key=lambda x:x['word'])}

def matrix_product(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def determinant(a):
    a=[r[:] for r in a];n=len(a);sgn=1;old=1
    for k in range(n-1):
        if not a[k][k]:
            j=next((j for j in range(k+1,n) if a[j][k]),None)
            if j is None:return 0
            a[k],a[j]=a[j],a[k];sgn=-sgn
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):a[i][j]=(a[i][j]*pivot-a[i][k]*a[k][j])//old
            a[i][k]=0
        old=pivot
    return sgn*a[-1][-1]
def homology_controls():
    A=[[0,0,1],[1,0,1],[0,1,0]];M=[[0,0,1,1,0],[1,0,1,0,0],[0,1,0,0,0],[0,0,0,0,1],[0,0,0,1,1]]
    p=[3,0,2];q=[3,-1,1];luc=[2,1]
    for n in range(2,31):luc.append(luc[-1]+luc[-2])
    for n in range(3,31):p.append(p[n-2]+p[n-3]);q.append(-q[n-1]+q[n-3])
    X=[[int(i==j) for j in range(3)] for i in range(3)];Y=[[int(i==j) for j in range(5)] for i in range(5)];rows=[]
    for n in range(1,31):
        X=matrix_product(X,A);Y=matrix_product(Y,M)
        a=abs(determinant([[X[i][j]-int(i==j) for j in range(3)] for i in range(3)]))
        g=abs(determinant([[Y[i][j]-int(i==j) for j in range(5)] for i in range(5)]))
        ratio=luc[n]-1-(-1)**n
        assert a==abs(p[n]-q[n]) and g==a*ratio and a>0
        if n<=8:rows.append([n,a,g,ratio])
    return {'through_n':30,'method':'Bareiss determinants versus trace recurrences and Lucas formula','first8':rows}

def core_and_gaps():
    theta={i:substitute(substitute(substitute((i,)))) for i in IMAGE}
    center=0;word=(5,);cores=[]
    for n in range(1,5):
        center=len(substitute(word[:center],theta))+2;word=substitute(word,theta)
        cores.append([n,len(word),center,len(word)-center-1])
    assert cores[2]==[3,162,73,88]
    assert cores[3]==[4,717,340,376]
    # Check the finite core after the worst-case trimming allowed by BCC.
    core=(5,)
    for _ in range(3):core=substitute(core,theta)
    one=substitute(core,theta);kept=one[35:-35]
    assert core in [kept[i:i+len(core)] for i in range(len(kept)-len(core)+1)]
    alpha5={i:(i,) for i in IMAGE}
    for _ in range(5):alpha5={i:substitute(w) for i,w in alpha5.items()}
    assert alpha5[1]==(3,1,2) and all(1 in alpha5[i] for i in (1,2,3))
    lower=(1,);lowercenter=0
    for _ in range(5):
        lowercenter=len(substitute(lower[:lowercenter],alpha5))+1
        lower=substitute(lower,alpha5)
    assert (len(lower),lowercenter,len(lower)-lowercenter-1)==(816,464,351)
    low,high=1.,1.4
    for _ in range(60):
        mid=(low+high)/2
        if mid**3-mid-1>0:high=mid
        else:low=mid
    rho=(low+high)/2;tau=(1+math.sqrt(5))/2
    words={i:(i,) for i in IMAGE};checks=[]
    for n in range(1,19):
        words={i:substitute(w) for i,w in words.items()};w=words[5];best=run=0
        for a in w:
            run=run+1 if a<=3 else 0;best=max(best,run)
        if n>=2:assert rho**(n-4)<=best+1e-9 and best<=(rho**n-1)/(rho-1)+1e-9
        if n in (2,5,10,15,18):checks.append([n,len(w),best])
    return {'cores':cores,'trim35_retains_full_core':True,'explicit_lower_language_seed':alpha5[1],
        'lower_phi5_BCC_bound':105,'lower_core_N5':[len(lower),lowercenter,len(lower)-lowercenter-1],
        'explicit_word_gap_controls':checks,'exponent':math.log(rho)/math.log(tau),
        'certified_surviving_margin_formulas':['left >= 35 + 38*2^k','right >= 35 + 53*2^k']}

def integrity():
    raw=(PUB/'MANIFEST.json').read_bytes();m=json.loads(raw)
    for fn,v in m['files'].items():
        b=(PUB/fn).read_bytes();assert len(b)==v['bytes'];assert hashlib.sha256(b).hexdigest()==v['sha256']
    return {'manifest_sha256':hashlib.sha256(raw).hexdigest(),'bound_file_count':len(m['files']),'all_match':True}

if __name__=='__main__':
    print(json.dumps({'integrity':integrity(),'homology':homology_controls(),'nonretraction':no_retraction(),
        'exterior_square':exterior_controls(),'attraction_gaps':core_and_gaps(),'periodic':periodic_controls()},indent=2))
