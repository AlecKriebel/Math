"""Independent finite diagnostics for C4. No author code imported."""
from collections import deque
from itertools import combinations
import json, math, random
from pathlib import Path

OUT=Path(__file__).resolve().parent
rng=random.Random(9700042)

def require(condition):
    if not condition:
        raise AssertionError('Independent C4 diagnostic failed')

def paths(n):
    end=(n,n); p=[(0,0)]; seen=set(p)
    def rec():
        if p[-1]==end:
            yield tuple(p); return
        x,y=p[-1]
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            z=(x+dx,y+dy)
            if 0<=z[0]<=n and 0<=z[1]<=n and z not in seen:
                seen.add(z);p.append(z);yield from rec();p.pop();seen.remove(z)
    yield from rec()

def forward(e):
    a,b=e; return b[0]+b[1]>a[0]+a[1]

def dual_reward(w,h,marks):
    # 0-1 shortest paths, freshly written with costly forward and free reverse edges.
    ds={(0,0):0}; Q=deque([(0,0)])
    while Q:
        a=Q.popleft(); d=ds[a]
        for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
            b=(a[0]+dx,a[1]+dy)
            if not (0<=b[0]<=w and 0<=b[1]<=h):continue
            c=int((dx+dy)>0 and (a,b) not in marks)
            if d+c<ds.get(b,10**9):
                ds[b]=d+c
                (Q.append if c else Q.appendleft)(b)
    return w+h-ds[(w,h)]

def slices(p,n,L):
    levels=list(range(L,2*n,L))+[2*n]
    ends=[0]; idx=0
    for level in levels:
        while p[idx][0]+p[idx][1]!=level:idx+=1
        ends.append(idx)
    return [p[a:b+1] for a,b in zip(ends,ends[1:])]

counts=dict(simple_paths=0,skeletons=0,rectangles=0,bad_rectangles=0,witness_tests=0,sparse_cases=0,tail_samples=0)
for n in [1,2,3]:
 for p in paths(n):
    counts['simple_paths']+=1
    all_edges=list(zip(p,p[1:])); all_forward=[e for e in all_edges if forward(e)]
    marks={e for e in all_forward if rng.random()<.58}
    for h,m in [(1,1),(1,2),(1,3),(1,5),(2,1),(2,2),(2,3),(3,1),(3,2)]:
        L=m*h; parts=slices(p,n,L);J=math.ceil(2*n/L)
        require(len(parts)==J)
        total_b=sum(not forward(e) for e in all_edges)
        total_s=0;bad_per=0;witnesses=[];rs=[]
        counts['skeletons']+=1
        for j,part in enumerate(parts):
            counts['rectangles']+=1
            edges=list(zip(part,part[1:])); b=sum(not forward(e) for e in edges)
            s=b//h;a=(s+1)*h;total_s+=s
            x,y=part[0];xx,yy=part[-1];t=x+y;tt=xx+yy;tau=tt-t
            i=x//h;ii=xx//h;z=ii-i
            lo=(i*h-a,t-(i+1)*h-a);hi=((ii+1)*h+a,tt-ii*h+a)
            W,H=hi[0]-lo[0],hi[1]-lo[1]
            require(W>=h and H>=h)
            require(all(lo[0]<=v[0]<=hi[0] and lo[1]<=v[1]<=hi[1] for v in part))
            require(W+H==tau+2*h+4*a)
            require(-s-2<=z<=m+s+2)
            require((s+1)*h<=b+h<=2*b if s>=1 else True)
            good=(s==0 and j<J-1)
            if good:
                require(W==(z+3)*h and H==(m-z+3)*h and -2<=z<=m+2)
            else:
                bad_per+=W+H;counts['bad_rectangles']+=1
            witness=set(edges)&marks
            require(all(not(witness&old) for old in witnesses))
            witnesses.append(witness)
            r=max(0,len(witness)-b);rs.append(r)
            shifted={((u[0]-lo[0],u[1]-lo[1]),(v[0]-lo[0],v[1]-lo[1])) for u,v in witness}
            require(dual_reward(W,H,shifted)>=r)
            counts['witness_tests']+=1
        require(total_s<=total_b//h)
        require(bad_per<=(m+10)*total_b+L+6*h)
        require(sum(rs)>=len(marks)-total_b)

# Deterministic sparse stability: exact maximum against strict coordinate chains.
def lis(points):
    points=sorted(points);d=[]
    for i,(x,y) in enumerate(points):
        d.append(1+max([0]+[d[j] for j,(xx,yy) in enumerate(points[:i]) if xx<x and yy<y]))
    return max(d,default=0)
for case in range(900):
    M=rng.randrange(1,7);w=rng.randrange(8,42);h=rng.randrange(8,42)
    points=[]
    for attempt in range(70):
        if len(points)>=M:break
        z=(rng.randrange(w),rng.randrange(h))
        if all(abs(z[0]-x)>M and abs(z[1]-y)>M for x,y in points):points.append(z)
    marks=set()
    for x,y in points:
        dx,dy=rng.choice([(1,0),(0,1)]);marks.add(((x,y),(x+dx,y+dy)))
    require(len(marks)<=M)
    require(dual_reward(w,h,marks)==lis(points))
    counts['sparse_cases']+=1

# Log-form samples only; the uniform proof is in the written audit.
for N in [1,2,7,30,100,10_000,1_000_000]:
 for q in [1e-6,1e-8,1e-12]:
    threshold=math.ceil(32*math.sqrt(q)*N)
    for k in sorted(set([max(1,threshold),max(1,threshold+1),max(1,N//4),N,N*10])):
        if k<threshold:continue
        logA=k*math.log(2*q)+2*(math.lgamma(N+2*k+1)-math.lgamma(k+1)-math.lgamma(N+k+1))+(4*k+2)*math.log1p(math.sqrt(k/(N+2*k)))
        require(logA<=math.log(4)-k*math.log(4)+1e-6)
        counts['tail_samples']+=1
result={'all_checks_passed':True,'counts':counts,'constants':{'small_range_base':2*math.e**2*(1.5)**6/32**2,'large_range_base_at_q_1e_6':32*math.e**2*1e-6*36},'scope':'Finite diagnostics only. No author code imported. These checks do not prove asymptotics or external theorems.'}
(OUT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
