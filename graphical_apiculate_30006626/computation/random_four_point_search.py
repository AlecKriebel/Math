import sys,random,itertools,time,json
sys.path.insert(0,'/workspace/scratch/c7d6ade09fc0/recovery_algebra_1815_20261019/computation')
from atlas_apex import *
rng=random.Random(1815);start=time.time();counts=collections.Counter()
for k in range(4000):
 n=rng.choice([8,9,10]);p=rng.choice([.15,.25,.4,.55,.7,.85]);G=nx.gnp_random_graph(n,p,seed=rng.randrange(2**32))
 if not nx.is_connected(G):continue
 counts['connected']+=1;a,err=apex_table(G)
 if err:continue
 counts['apiculate']+=1
 if any(all(a[t] in S for t in itertools.product(S,repeat=3)) and test_subset(S,a)[1] for S in map(set,itertools.combinations(range(n),4))):continue
 counts['no_bad_four']+=1
 for size in range(5,n):
  for ss in itertools.combinations(range(n),size):
   S=set(ss)
   if any(a[t] not in S for t in itertools.product(S,repeat=3)):continue
   H,err=test_subset(S,a)
   if err:
    print('COUNTEREXAMPLE',json.dumps({'edges':list(G.edges()),'subset':ss,'error':err}),flush=True);sys.exit()
 if k%100==0:print(k,dict(counts),round(time.time()-start,1),flush=True)
print('DONE',dict(counts),time.time()-start)
