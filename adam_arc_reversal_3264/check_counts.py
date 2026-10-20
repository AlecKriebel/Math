"""Independent finite base-graph audit of Thomassen (2023), Theorem 1.
Standard library only; no third-party source text or data included.
"""
from collections import Counter
import json

def base(m):
    adj=[set() for _ in range(2*m)]
    for i in range(m):
        j=(i+1)%m
        for a,b in [(i,j),(j,m+i),(m+i,m+j),(m+j,i)]: adj[a].add(b)
    return [sorted(x) for x in adj]

def cycles(adj):
    counts=Counter()
    for start in range(len(adj)):
        def dfs(v,seen):
            for w in adj[v]:
                if w==start: counts[len(seen)]+=1
                elif w>start and w not in seen: dfs(w,seen|{w})
        dfs(start,{start})
    return counts

def paths(adj,start,end):
    counts=Counter()
    def dfs(v,seen):
        for w in adj[v]:
            if w==end: counts[len(seen)]+=1
            elif w not in seen: dfs(w,seen|{w})
    dfs(start,{start})
    return counts

def good_trails(adj,m,required_arc=None):
    # Even zero-based indices correspond to odd indices in the paper.
    odd={i for i in range(2*m) if i%m%2==0}
    counts=Counter()
    for start in sorted(odd):
        visits=[0]*(2*m);visits[start]=1
        def dfs(v,used):
            for w in adj[v]:
                e=(v,w)
                if e in used: continue
                if w==start:
                    ev=[visits[i] for i in range(2*m) if i not in odd]
                    if required_arc is None or required_arc in used|{e}:
                        key=(ev.count(1),ev.count(2))
                        if required_arc is not None: key=key+(visits[required_arc[1]],)
                        counts[key]+=1
                elif not (w in odd and w<start) and visits[w]<(1 if w in odd else 2):
                    visits[w]+=1;dfs(w,used|{e});visits[w]-=1
        dfs(start,set())
    return counts

def run():
    results={}
    for m in (6,10):
        adj=base(m);u,v=0,1
        old=paths(adj,v,u)
        without=[a.copy() for a in adj];without[u].remove(v)
        new=paths(without,u,v)
        results[f'D{2*m}']={'cycles_by_length':dict(sorted(cycles(adj).items())),
            'deleted_cycles_by_length':dict(sorted((l+1,n) for l,n in old.items())),
            'created_cycles_by_length':dict(sorted((l+1,n) for l,n in new.items()))}
        if m==10:
            counts=good_trails(adj,m)
            results['D20']['good_closed_trails_by_a_b']={f'{a},{b}':n for (a,b),n in sorted(counts.items())}
            results['D20']['maximum_weight']=max(2**a*3**b for a,b in counts)
    print(json.dumps(results,indent=2))
if __name__=='__main__':run()

# Exact finite certificate, separately usable by import.
def certificate(d=64,k=24):
    adj=base(10)
    all_counts=good_trails(adj,10)
    A=(d+1)**2*2**k-1
    B=(d*d+d+1)**2*3**k-2*(d+1)**2*2**k+1
    A0=(d+1)*2**k
    B0=d*(d*d+d+1)*3**k-(d+1)*2**k
    # Every possible position of the fixed vertex in its gadget.
    local=[(A0,B0)] + [((d+1)*2**(k-i),
      (d+1)*(d*d+d+1)*2**(i-1)*3**(k-i)-(d+1)*2**(k-i))
      for i in range(1,k+1)] + [(1,d*(d+1)*2**k-1)]
    assert all(a<=A0 and b<=B0 for a,b in local)
    f_values=[]
    for u in range(20):
        if u%10%2: continue
        for v in adj[u]:
            c=good_trails(adj,10,(u,v))
            f=sum(n*(A0*A**(a-1)*B**b if r==1 else
                     B0*A**a*B**(b-1)) for (a,b,r),n in c.items())
            f_values.append(f)
            minus=[x.copy() for x in adj];minus[u].remove(v)
            assert paths(minus,u,v)[19]>=1
    assert len(set(f_values))==1
    f=max(f_values)
    g=d**18*512**k
    total=sum(n*A**a*B**b for (a,b),n in all_counts.items())
    assert f<g
    assert len(adj)==20 and sum(map(len,adj))==40
    assert all(u not in adj[v] for u in range(20) for v in adj[u])
    def connected_without(removed):
        remaining=set(range(20))-{removed}
        for start in remaining:
            reached={start}; stack=[start]
            while stack:
                for v in adj[stack.pop()]:
                    if v in remaining and v not in reached: reached.add(v);stack.append(v)
            if reached!=remaining:return False
        return True
    assert all(connected_without(v) for v in range(20))
    return {'d':d,'k':k,'vertices':10+10*(k+2*d),
      'arcs':40*(k+2*d)+10*(k*(k-1)//2+2*d*k+d*d),
      'cycles':total,'max_destroyed_external_arc':f,
      'created_external_arc_lower_bound':g,'strict_margin':g-f,
      'ratio_approximation':f/g,'checked_odd_outgoing_base_arcs':len(f_values),
      'all_assertions_passed':True}

def expanded(m,d,k):
    old=base(m);groups=[];n=0
    for i in range(2*m):
        size=k+2*d if i%m%2 else 1
        groups.append(list(range(n,n+size)));n+=size
    adj=[set() for _ in range(n)]
    for u in range(2*m):
        for v in old[u]:
            for a in groups[u]:adj[a].update(groups[v])
    for i,group in enumerate(groups):
        if not i%m%2:continue
        ranks=[0]*d+list(range(1,k+1))+[k+1]*d
        for a,ra in zip(group,ranks):
            for b,rb in zip(group,ranks):
                if ra<rb:adj[a].add(b)
    return [sorted(a) for a in adj]

def small_expansion_crosscheck():
    checks=[]
    for m,d,k in [(6,1,0),(6,2,0),(6,1,1)]:
        A=(d+1)**2*2**k-1
        B=(d*d+d+1)**2*3**k-2*(d+1)**2*2**k+1
        predicted=sum(n*A**a*B**b for (a,b),n in good_trails(base(m),m).items())
        actual=sum(cycles(expanded(m,d,k)).values())
        assert predicted==actual
        checks.append({'m':m,'d':d,'k':k,'predicted':predicted,'direct_enumeration':actual})
    return checks
