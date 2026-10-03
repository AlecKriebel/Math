"""Exact small-graph twin-width checks; standard library only.
Partitions are tuples of disjoint nonzero integer bit masks.
Red adjacency is recomputed from the original graph (independent of history).
"""
from functools import lru_cache
from itertools import combinations

def graph(n, code):
    adj=[0]*n
    for k,(i,j) in enumerate(combinations(range(n),2)):
        if code>>k&1: adj[i]|=1<<j;adj[j]|=1<<i
    return tuple(adj)

def vertices(mask):
    while mask:
        bit=mask&-mask;yield bit.bit_length()-1;mask-=bit

def red(adj,a,b):
    seen_edge=seen_nonedge=False
    for u in vertices(a):
        z=adj[u]&b
        seen_edge |= bool(z)
        seen_nonedge |= z!=b
    return seen_edge and seen_nonedge

def red_degrees(adj,part):
    deg=[0]*len(part)
    for i,j in combinations(range(len(part)),2):
        if red(adj,part[i],part[j]):deg[i]+=1;deg[j]+=1
    return deg

def width(adj,part):return max(red_degrees(adj,part),default=0)

def merge(part,i,j):return tuple(sorted([a for k,a in enumerate(part) if k not in (i,j)]+[part[i]|part[j]]))

def exact(adj):
    @lru_cache(None)
    def rec(part):
        w=width(adj,part)
        if len(part)<=1:return w,()
        best=100;seq=None
        for i,j in combinations(range(len(part)),2):
            nxt=merge(part,i,j);v,s=rec(nxt);v=max(w,v)
            if v<best:best=v;seq=((part[i],part[j]),)+s
            if best==w:break
        return best,seq
    return rec(tuple(1<<i for i in range(len(adj))))

def pair_only(adj,bound,return_visited=False):
    n=len(adj)
    visited={}
    def rec(part):
        if part in visited:return None
        visited[part]=True
        if len(part)==(n+1)//2:return ()
        choices=[i for i,p in enumerate(part) if p.bit_count()==1]
        for i,j in combinations(choices,2):
            nxt=merge(part,i,j)
            if width(adj,nxt)<=bound:
                s=rec(nxt)
                if s is not None:return ((part[i],part[j]),)+s
        return None
    s=rec(tuple(1<<i for i in range(n)))
    return (s,list(visited)) if return_visited else s

def pair_profile(adj,pairs,fixed=()):
    d=[];mix=[];base=[]
    for i,(a,b) in enumerate(pairs):
        dis=(adj[a]^adj[b])&~((1<<a)|(1<<b))
        base.append(dis.bit_count())
        d.append([0 if i==j else sum((dis>>v)&1 for v in pair) for j,pair in enumerate(pairs)])
        mix.append([0 if i==j else int(red(adj,(1<<a)|(1<<b),sum(1<<v for v in pair))) for j,pair in enumerate(pairs)])
    return base,d,mix

if __name__=='__main__':
    import json,random,time,pathlib
    out={};start=time.monotonic()
    for n in range(1,7):
        D=(n-1)//2;failed=[];counts=0
        for code in range(1<<(n*(n-1)//2)):
            a=graph(n,code);s=pair_only(a,D);counts+=1
            if s is None:
                ex,seq=exact(a);failed.append({'code':code,'adjacency':a,'twin_width':ex,'sequence':seq})
                if len(failed)>=3:break
        out[str(n)]={'checked':counts,'total_labeled':1<<(n*(n-1)//2),'bound':D,'pair_only_failures':failed}
        print(n,counts,failed,flush=True)
    rng=random.Random(481)
    for n in [7,8,9,10,11,12]:
        failed=[]
        for z in range(250):
            code=rng.getrandbits(n*(n-1)//2);a=graph(n,code)
            if pair_only(a,(n-1)//2) is None:
                failed.append({'code':code,'adjacency':a,'sample_index':z});break
        out['random_'+str(n)]={'samples':z+1,'pair_only_failures':failed}
        print('random',n,z+1,failed,flush=True)
    out['elapsed_seconds']=time.monotonic()-start
    pathlib.Path(__file__).with_name('pair_search_results.json').write_text(json.dumps(out,indent=2)+'\n')
