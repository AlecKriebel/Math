"""Fresh exhaustive supplemental checks; no infinite-volume proof by testing."""
import heapq, itertools, json, math, random
from pathlib import Path

DIR=Path(__file__).resolve().parent

def vertices(n): return [(x,y) for x in range(n) for y in range(n)]
def edges(n):
    return [(u,(u[0]+dx,u[1]+dy)) for u in vertices(n) for dx,dy in [(1,0),(0,1)] if u[0]+dx<n and u[1]+dy<n]

def dual_cost(n,c):
    N=n-2
    if N==0: return 0
    dist={(0,0):0}; heap=[(0,(0,0))]
    while heap:
        d,u=heapq.heappop(heap)
        if d!=dist[u]: continue
        if u==(N,N): return d
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            v=(u[0]+dx,u[1]+dy)
            if not(0<=v[0]<=N and 0<=v[1]<=N): continue
            if dx==1:
                j=n-2-u[1]; pe=((u[0]+1,j),(u[0]+1,j+1)); w=c[pe]
            elif dy==1:
                j=n-2-u[1]; pe=((u[0],j),(u[0]+1,j)); w=c[pe]
            else: w=0
            nd=d+w
            if nd<dist.get(v,10**10): dist[v]=nd;heapq.heappush(heap,(nd,v))

def cut_cost(n,c):
    src={u for u in vertices(n) if (u[0]==0 or u[1]==0) and max(u)<n-1}
    snk={u for u in vertices(n) if u[0]==n-1 or u[1]==n-1}
    free=[u for u in vertices(n) if u not in src|snk]
    ans=10**10
    for z in range(1<<len(free)):
        S=src|{v for i,v in enumerate(free) if z>>i&1}
        ans=min(ans,sum(w for (u,v),w in c.items() if u in S and v not in S))
    return ans

def all_simple_paths(N):
    end=(N,N); seen={(0,0)}; path=[(0,0)]
    def rec(u):
        if u==end:
            yield tuple(path);return
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            v=(u[0]+dx,u[1]+dy)
            if 0<=v[0]<=N and 0<=v[1]<=N and v not in seen:
                path.append(v);seen.add(v);yield from rec(v);seen.remove(v);path.pop()
    yield from rec((0,0))

def slice_check(path,m,h):
    N=path[-1][0]; L=m*h; levels=list(range(L,2*N,L))+[2*N]
    cuts=[0]; pos=0
    for level in levels:
        pos=next(k for k in range(pos+1,len(path)) if sum(path[k])==level)
        cuts.append(pos)
    tot_b=0; bad_per=0; sums=0; segments=0
    for j,(a,b) in enumerate(zip(cuts,cuts[1:])):
        p=path[a:b+1];x,y=p[0]; xx,yy=p[-1]; t=x+y;tt=xx+yy
        bwd=sum(sum(v)<sum(u) for u,v in zip(p,p[1:]));tot_b+=bwd
        s=bwd//h;sums+=s;i=x//h;ii=xx//h;pad=(s+1)*h
        lo=(i*h-pad,t-(i+1)*h-pad);hi=((ii+1)*h+pad,tt-ii*h+pad)
        W,H=hi[0]-lo[0],hi[1]-lo[1]
        assert W>=h and H>=h
        assert all(lo[0]<=v[0]<=hi[0] and lo[1]<=v[1]<=hi[1] for v in p)
        assert W+H==tt-t+2*h+4*pad
        assert -s-2<=ii-i<=m+s+2
        if s==0 and j<len(cuts)-2:
            z=ii-i;assert (W,H)==((z+3)*h,(m-z+3)*h)
        else: bad_per+=W+H
        segments+=1
    assert sums<=tot_b//h
    assert bad_per<=(m+10)*tot_b+L+6*h
    return segments

def main():
    rng=random.Random(773019)
    cut_cases=0
    for n in [2,3,4,5]:
        es=edges(n)
        states=range(1<<len(es)) if n<=3 else [rng.getrandbits(len(es)) for _ in range(120)]
        for mask in states:
            c={e:(mask>>i)&1 for i,e in enumerate(es)}
            boundary=c[((0,n-2),(0,n-1))]+c[((n-2,0),(n-1,0))]
            assert cut_cost(n,c)==boundary+dual_cost(n,c)
            cut_cases+=1
    path_cases=segment_cases=0
    for N in range(1,5):
        for p in all_simple_paths(N):
            for m in [1,2,3,5]:
                for h in [1,2,3]:
                    segment_cases+=slice_check(p,m,h);path_cases+=1
    # Exhaust every orientation subset on a 2x2 dual square against all simple paths.
    N=2;es=edges(N+1); ps=list(all_simple_paths(N)); sep_cases=0;budget_cases=0
    for mask in range(1<<len(es)):
        marked={e for i,e in enumerate(es) if mask>>i&1}; M=len(marked)
        rewards=[]
        for p in ps:
            k=sum((u,v) in marked for u,v in zip(p,p[1:]))
            b=sum(sum(v)<sum(u) for u,v in zip(p,p[1:]))
            rewards.append(k-b)
            if b<=k:
                seq=[(0,0)]+[u for u,v in zip(p,p[1:]) if (u,v) in marked]+[(N,N)]
                assert all(sum(max(u[c]-v[c],0) for u,v in zip(seq,seq[1:]))<=k for c in [0,1])
                budget_cases+=1
        starts=[u for u,v in marked]
        if all(abs(a[0]-b[0])>M and abs(a[1]-b[1])>M for a,b in itertools.combinations(starts,2)):
            best=[]
            for u in sorted(starts):
                best.append((u,1+max([k for v,k in best if v[0]<u[0] and v[1]<u[1]]or[0])))
            assert max(rewards)==max([k for _,k in best]or[0]);sep_cases+=1
    out={'all_passed':True,'seed':773019,'primal_dual_cases':cut_cases,'exhaustive_skeleton_path_parameter_cases':path_cases,'exhaustive_segments':segment_cases,'marked_list_variation_cases':budget_cases,'sparse_separated_cases':sep_cases,'constants':{'small_k':2*math.e**2*1.5**6/32**2,'large_k':32*math.e**2*1e-6*36},'scope':'Supplemental finite checks only; not proof of asymptotics.'}
    (DIR/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
