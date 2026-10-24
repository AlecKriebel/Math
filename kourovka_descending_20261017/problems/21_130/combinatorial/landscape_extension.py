import itertools,json,random,time
from pathlib import Path
from monotone_landscape import analyze
random.seed(217130)
instances=[]
for p,n,count in [(11,9,8),(13,9,8),(17,9,8),(11,10,2),(13,10,2)]:
 cs=list(itertools.combinations(range(1,p),n-1))
 for B in random.sample(cs,min(count,len(cs))):instances.append(([(x,) for x in (0,)+B],(p,)))
for mods,n,count in [((3,3,3),9,5),((3,5),9,5),((3,3),8,1)]:
 E=list(itertools.product(*(range(x) for x in mods)))
 for _ in range(count):
  A=sorted(random.sample(E,n));instances.append((A,mods))
results=[];t=time.time()
for i,(A,M) in enumerate(instances):
 r=analyze(A,M); results.append(r)
 print(i, len(instances), M,len(A),r['blocked_count'],time.time()-t,flush=True)
 Path('landscape_extension_result.json').write_text(json.dumps({'results':results,'elapsed_seconds':time.time()-t},indent=2)+'\n')
 if r['blocked_count']:break
