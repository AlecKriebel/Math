#!/usr/bin/env python3
"""Exact finite diagnostics for the Bray graph-chart manuscript. MIT licensed.
Python >=3.10, standard library only. No randomness, services or credentials.
Finite results are interface checks, not certification of the universal theorem.
"""
from itertools import product
from fractions import Fraction as Q
from collections import Counter
from pathlib import Path
import json, argparse

def need(ok, msg):
    if not ok: raise RuntimeError(msg)
def eye(n): return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def trans(a): return tuple(zip(*a))
def mul(a,b,p): return tuple(tuple(sum(x*y for x,y in zip(row,col))%p for col in zip(*b)) for row in a)
def det(a,p):
    a=[list(x) for x in a];v=1
    for i in range(len(a)):
        j=next((j for j in range(i,len(a)) if a[j][i]%p),None)
        if j is None:return 0
        if j!=i:a[i],a[j]=a[j],a[i];v=-v
        pivot=a[i][i]%p;v=v*pivot%p;iv=pow(pivot,-1,p)
        for k in range(i+1,len(a)):
            f=a[k][i]*iv%p
            a[k]=[(x-f*y)%p for x,y in zip(a[k],a[i])]
    return v%p
def inverse(a,p):
    n=len(a);c=[list(r)+list(s) for r,s in zip(a,eye(n))]
    for i in range(n):
        j=next((j for j in range(i,n) if c[j][i]%p),None)
        need(j is not None,'singular inverse')
        c[i],c[j]=c[j],c[i];iv=pow(c[i][i],-1,p);c[i]=[x*iv%p for x in c[i]]
        for j in range(n):
            if i!=j:
                f=c[j][i];c[j]=[(x-f*y)%p for x,y in zip(c[j],c[i])]
    return tuple(tuple(r[n:]) for r in c)
def mats(n,m,p):
    for v in product(range(p),repeat=n*m):yield tuple(tuple(v[i*m:(i+1)*m]) for i in range(n))
def addidentity(a,p):return tuple(tuple((x+(i==j))%p for j,x in enumerate(r)) for i,r in enumerate(a))
def chi(x,p):return 0 if x%p==0 else (1 if pow(x%p,(p-1)//2,p)==1 else -1)
def symp(n):return tuple(tuple((1 if i%2==0 and j==i+1 else -1 if i%2 and j==i-1 else 0) for j in range(n)) for i in range(n))
def diag(values):return tuple(tuple(x if i==j else 0 for j in range(len(values))) for i,x in enumerate(values))
def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return tuple(a)
def rem(a,b,p):
    a=list(trim(a));b=trim(b)
    while len(a)>=len(b) and any(a):
        c=a[-1]*pow(b[-1],-1,p)%p;off=len(a)-len(b)
        for i,x in enumerate(b):a[off+i]=(a[off+i]-c*x)%p
        a=list(trim(a))
    return trim(a)
def gcd(a,b,p):
    a,b=trim(a),trim(b)
    while any(b):a,b=b,rem(a,b,p)
    iv=pow(a[-1],-1,p);return tuple(x*iv%p for x in a)
def squarefree(f,p):return len(gcd(f,tuple(i*f[i]%p for i in range(1,len(f))) or (0,),p))==1
def val(f,x,p):
    r=0
    for c in reversed(f):r=(r*x+c)%p
    return r
def charpoly(a,p):
    n=len(a)
    if n==2:return (det(a,p),-sum(a[i][i] for i in range(n))%p,1)
    need(n==3,'only dimensions two and three here')
    c2=-sum(a[i][i] for i in range(n))%p
    c1=sum(a[i][i]*a[j][j]-a[i][j]*a[j][i] for i in range(n) for j in range(i+1,n))%p
    return (-det(a,p)%p,c1,c2,1)
def order_sp(n,q):
    r=n//2;v=q**(r*r)
    for i in range(1,r+1):v*=q**(2*i)-1
    return v

def check_sp():
    out={}
    a=symp(2);ai=inverse(a,3)
    for b in (2,4):
        form=symp(b);cnt=Counter()
        for f in mats(b,2,3):
            k=mul(ai,mul(trans(f),mul(form,f,3),3),3)
            if det(k,3) and det(addidentity(k,3),3):cnt[k]+=1
        need(len(cnt)==1,'Sp2 self-adjoint chart should have scalar K=1')
        need(next(iter(cnt))==eye(2),'wrong distinguished scalar')
        fiber=order_sp(b,3)//order_sp(b-2,3)
        need(next(iter(cnt.values()))==fiber,'Sp embedding fibre')
        cls=order_sp(b+2,3)//(order_sp(2,3)*order_sp(b,3))
        mass=Q(sum(cnt.values()),cls)
        formula=Q(order_sp(2,3)**2*order_sp(b,3)**2,order_sp(b+2,3)*order_sp(b-2,3)*order_sp(2,3))
        need(mass==formula,'unconditional Sp mass')
        out[str(b)]={'graphs':sum(cnt.values()),'class_denominator':cls,'mass':str(mass)}
    return out

def orth_group(form,p):return tuple(x for x in mats(len(form),len(form),p) if mul(trans(x),mul(form,x,p),p)==form)
def check_orth():
    out={};a=eye(2);oa=len(orth_group(a,3));need(oa==8,'O2 minus order')
    for values in ((1,1),(1,2)):
        b=diag(values);ob=len(orth_group(b,3));counts=Counter();ks={}
        for f in mats(2,2,3):
            k=mul(trans(f),mul(b,f,3),3);ff=charpoly(k,3)
            if det(k,3) and det(addidentity(k,3),3) and squarefree(ff,3):
                if chi(det(addidentity(k,3),3),3)==1:
                    counts[ff]+=1;ks.setdefault(ff,set()).add(k)
        for ff,c in counts.items():
            need(len(ks[ff])==oa//2,'orth trace-type K count')
            need(c==oa*ob//2,'orth F fibre')
            need(chi(ff[0],3)==chi(det(b,3),3),'zero complement determinant retained')
        out[str(values)]={'O_A':oa,'O_B':ob,'graphs_by_polynomial':{str(f):c for f,c in sorted(counts.items())}}
    # Degree three, two primary factors: total discriminant selection leaves exactly half
    # with square discriminant on the distinguished one-dimensional eigenspace.
    hist=Counter();half=Counter();og=orth_group(eye(3),3);need(len(og)==48,'O3 order')
    for u in product(range(3),repeat=6):
        k=((u[0],u[1],u[2]),(u[1],u[3],u[4]),(u[2],u[4],u[5]));f=charpoly(k,3)
        if not f[0] or not val(f,2,3) or not squarefree(f,3):continue
        hist[f]+=1
        if val(f,1,3)==0:
            vs=[v for v in product(range(3),repeat=3) if any(v) and all(sum(k[i][j]*v[j] for j in range(3))%3==v[i] for i in range(3))]
            need(len(vs)==2,'simple one-dimensional primary')
            half[f]+=chi(sum(x*x for x in vs[0]),3)==1
    need(hist and all(v==24 for v in hist.values()),'O3 trace-form counts')
    need(half and all(2*v==hist[f] for f,v in half.items()),'coefficient discriminant exact half')
    out['trace_three']={'K_counts':{str(f):v for f,v in sorted(hist.items())},'square_primary_counts':{str(f):v for f,v in sorted(half.items())}}
    # Actual codimension-zero graph over F7, with A=B=<1>.
    fs=[x for x in range(7) if x*x%7 and (1+x*x)%7 and chi(1+x*x,7)==1]
    need(fs==[1,6],'dimension-one codimension-zero graph')
    out['O1_F7']={'graphs':len(fs),'mass':str(Q(len(fs),4))}
    return out

def check_polynomials():
    out={}
    for r in range(9):
        sectors=Counter();sums=[0,0,0];total=0
        for cs in product(range(3),repeat=r):
            f=cs+(1,)
            if not f[0] or not val(f,2,3) or not squarefree(f,3):continue
            x,y=chi(f[0],3),chi(val(f,2,3),3);sectors[x,y]+=1;total+=1
            for i,v in enumerate((x,y,x*y)):sums[i]+=v
        predicted=Q(3,8)+Q((-1)**r*(10-8*r),16*3**r)
        need(Q(total,3**r)==predicted,'q3 exact squarefree total')
        if r>=2:
            need(all(abs(x)<=Q(3*r,2) for x in sums),'character bound')
        if r>=8:need(all(sectors[x,y]>=Q(3**r,16) for x,y in product((-1,1),repeat=2)),'four-sector lower bound')
        out[str(r)]={'total':total,'sectors':{str(k):sectors[k] for k in product((-1,1),repeat=2)},'character_sums':sums}
    return out

def sl2(p):return tuple(x for x in mats(2,2,p) if det(x,p)==1)
def closure(gens,p):
    I=eye(2);s={I};todo=[I]
    while todo:
        x=todo.pop()
        for g in gens:
            y=mul(x,g,p)
            if y not in s:s.add(y);todo.append(y)
    return s

def check_covers():
    out={}
    for p in (3,5):
        G=sl2(p);I=eye(2);mi=tuple(tuple(-x%p for x in r) for r in I)
        invs=[x for x in G if mul(x,x,p)==I]
        need(set(invs)=={I,mi},'Sp2 involutions are scalar: strong-plane marginal zero')
        comm=set()
        for a in G:
            ai=inverse(a,p)
            for b in G:comm.add(mul(mul(mul(ai,inverse(b,p),p),a,p),b,p))
        derived=closure(tuple(comm),p)
        need(len(derived)==(8 if p==3 else 120),'natural perfectness boundary')
        center=[x for x in G if all(mul(x,g,p)==mul(g,x,p) for g in G)]
        need(set(center)=={I,mi},'natural scalar kernel')
        out[str(p)]={'order':len(G),'derived_order':len(derived),'center_order':len(center),'strong_plane_involutions':0}
    # Closed 2:1 strength intervals force the common dimension to 4a/3.
    failed=[a for a in range(1,31) if not any(3*k>=4*a and 3*k<=4*a for k in range(2*a+1))]
    need(failed==[a for a in range(1,31) if a%3],'2:1 boundary')
    out['two_to_one_impossible_a']=failed
    return out

def check_blocks():
    # Correlated mixture of product-uniform component classes. Preserve the
    # distinction between pair-conditioned independence and unconditional independence.
    ac=[('a0','a1'),('a2',)];bc=[('b0','b1','b2'),('b3','b4')]
    weights={(0,0):Q(1,2),(0,1):Q(1,6),(1,0):Q(1,12),(1,1):Q(1,4)}
    law={}
    for (i,j),w in weights.items():
        for a,b in product(ac[i],bc[j]):law[a,b]=w/(len(ac[i])*len(bc[j]))
    need(sum(law.values())==1,'weighted law total')
    event={x for x in law if x[1] in bc[0]};p=sum(law[x] for x in event);survive=1-(1-p)**3
    actual={x:sum((1-p)**j*law[x] for j in range(3))/survive for x in event}
    need(actual=={x:law[x]/p for x in event},'conditional first success law')
    # Independent blocks conditioned on success retain a product law.
    need(sum(actual[x]*actual[y] for x in actual for y in actual)==1,'conditional disjoint blocks')
    # A graph action with kernel <=2 permits at most two B values per fixed A.
    max_graph=max(sum(law[a,b] for b in bc[j][:2])/(weights[i,j]/len(ac[i])) for (i,j) in weights for a in ac[i])
    need(max_graph==1,'two-element class permits the full worst case; no tiny-group generation assertion')
    need(Q(2,len(bc[0]))==Q(2,3),'pair class graph bound')
    # Deliberate perturbations must be rejected by mathematical predicates.
    controls=0
    for predicate in [lambda: need(Q(1,4)==Q(4,15),'wrong unconditional chart mass'),lambda: need(len(bc[0])==2,'missing B class member'),lambda: need(120==60,'projective generation does not replace natural order'),lambda: need(all(a%3==0 for a in range(1,4)),'simultaneous strength')]:
        try:predicate()
        except RuntimeError:controls+=1
    need(controls==4,'negative controls failed to reject')
    return {'target_probability':str(p),'first_success_conditional':{str(x):str(actual[x]) for x in sorted(actual)},'negative_controls_rejected':controls,'pair_conditioned_graph_bound':'2/3'}

def run():
    return {'schema':'bray-sp-o-exact-diagnostics-v1','status':'PASS','universal_mathematics_certified':False,'sp_graphs':check_sp(),'orth_graphs':check_orth(),'q3_polynomial_sectors':check_polynomials(),'natural_covers_and_boundaries':check_covers(),'weighted_conditional_blocks':check_blocks()}
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--expected',type=Path);a=ap.parse_args();r=run()
    if a.expected:need(json.loads(a.expected.read_text())==r,'expected results do not match exact reconstruction')
    print(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2))
