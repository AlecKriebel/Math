"""Independent exact rank verification via sink-sandpile recurrentization.
No imports from the original verification programs. Run from any directory.
"""
from collections import deque
from itertools import product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def build(lengths):
    pairs=[(1,2)]*2+[(3,4)]*2+[(5,6)]*2+[(0,i) for i in range(1,7)]+[(2,3),(4,5),(6,1)]
    adj=[[] for _ in range(7)]; paths=[]
    for (u,v),length in zip(pairs,lengths):
        path=[u]
        for _ in range(length-1):
            path.append(len(adj));adj.append([])
        path.append(v)
        for a,b in zip(path,path[1:]):adj[a].append(b);adj[b].append(a)
        paths.append(path)
    return adj,paths[-3:]

def reaches(adj,D,q):
    if D[q]>0:return True
    n=len(adj);deg=list(map(len,adj))
    # Complementary stable sandpile on nonsink vertices.
    a=[deg[v]-1-D[v] for v in range(n)]
    beta=[adj[v].count(q) for v in range(n)]
    for rounds in range(100000):
        b=[a[v]+beta[v] for v in range(n)];todo=deque(v for v in range(n) if v!=q and b[v]>=deg[v])
        while todo:
            v=todo.popleft()
            k=b[v]//deg[v]
            if k==0:continue
            b[v]-=k*deg[v]
            for w in adj[v]:
                if w!=q:
                    b[w]+=k
                    if b[w]>=deg[w]:todo.append(w)
        if all(a[v]==b[v] for v in range(n) if v!=q):
            qchips=sum(D)-sum(deg[v]-1-b[v] for v in range(n) if v!=q)
            return qchips>0
        a=b
    raise RuntimeError('sandpile recurrentization cap exceeded')

def check(lengths,collect_all):
    adj,paths=build(lengths);good=[];count=0
    for indices in product(*(range(len(p)) for p in paths)):
        D=[0]*len(adj);D[0]=2
        for path,i in zip(paths,indices):D[path[i]]+=1
        count+=1
        if all(reaches(adj,D,q) for q in range(len(adj))):
            good.append(list(indices))
            if not collect_all:break
    return good,count

if __name__=='__main__':
    old=json.loads((ROOT/'TRICYCLE_CHECKS.json').read_text());uni=[]
    for row in old:
        m=row['m']; good,count=check([m]*15,True)
        assert good==row['positive_rank_positions'] and count==row['candidates']
        uni.append({'m':m,'candidates':count,'positive_rank_positions':good})
        print('uniform',m,'verified',flush=True)
    oldlens=json.loads((ROOT/'LENGTH_CHECKS.json').read_text());checked=0;visited=0
    for row in oldlens:
        lengths=row['cycle_lengths']+row['spoke_lengths']+row['transition_lengths']
        for ms,expected in row['checks'].items():
            good,count=check([int(ms)*l for l in lengths],False);visited+=count
            actual=5 if good else 6
            assert actual==expected['gonality']
            assert (good[0] if good else None)==expected['witness_positions']
            checked+=1
        print('length vector',checked//3,'verified',flush=True)
    summary={'algorithm':'exact sink-sandpile recurrentization, independently implemented','uniform_checks':uni,'asymmetric_graphs':len(oldlens),'asymmetric_subdivision_checks':checked,'asymmetric_candidates_visited':visited,'all_results_match':True}
    (ROOT/'AUDIT_CHECKS.json').write_text(json.dumps(summary,indent=2)+'\n')
