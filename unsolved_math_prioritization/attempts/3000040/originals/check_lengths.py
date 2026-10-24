import itertools,json
from check_tricycles import reaches

def test(lengths,m):
    base=[(1,2),(1,2),(3,4),(3,4),(5,6),(5,6)]+[(0,i) for i in range(1,7)]+[(2,3),(4,5),(6,1)]
    edges=[];paths=[];n=7
    for j,((a,b),ell) in enumerate(zip(base,lengths)):
        path=[a]+list(range(n,n+m*ell-1))+[b];n+=m*ell-1;edges.extend(zip(path,path[1:]))
        if j>=12:paths.append(path)
    adj=[{} for _ in range(n)]
    for a,b in edges:adj[a][b]=adj[a].get(b,0)+1;adj[b][a]=adj[b].get(a,0)+1
    for pos in itertools.product(*paths):
        D=[0]*n;D[0]=2
        for p in pos:D[p]+=1
        if all(reaches(adj,D,q)[0] for q in range(n)):
            return {'gonality':5,'witness_positions':[paths[i].index(pos[i]) for i in range(3)]}
    return {'gonality':6,'witness_positions':None}
results=[]
for spokes in (1,2):
 for tr in itertools.product(range(1,4),repeat=3):
    lens=[1]*6+[spokes]*6+list(tr)
    r={'cycle_lengths':[1]*6,'spoke_lengths':[spokes]*6,'transition_lengths':list(tr),'checks':{str(m):test(lens,m) for m in (1,2,3)}}
    results.append(r)
print(json.dumps({'graphs':len(results),'odd_drops':sum(r['checks']['3']['gonality']<r['checks']['1']['gonality'] for r in results),'first_beyond_two':sum(r['checks']['3']['gonality']<r['checks']['2']['gonality']==r['checks']['1']['gonality'] for r in results)}))
open('gonality_subdivisions_3000040/residual_attempt/LENGTH_CHECKS.json','w').write(json.dumps(results,indent=2)+'\n')
