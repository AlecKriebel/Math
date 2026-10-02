import itertools,json
checks=0
def ck(x):
 global checks
 checks+=1
 assert x
c=[1,0,3,2,4]; pairs=list(itertools.combinations(range(4),2));accepted=[]
for choices in itertools.product(range(3),repeat=6):
 R={(i,i) for i in range(5)}|{(i,4) for i in range(4)}
 for (i,j),v in zip(pairs,choices):
  if v:R.add((i,j) if v==1 else (j,i))
 if any((i,j) in R and (j,k) in R and (i,k) not in R for i,j,k in itertools.product(range(5),repeat=3)):continue
 if any(((i,j) in R)!=((c[i],c[j]) in R) for i,j in itertools.product(range(5),repeat=2)):continue
 js={};good=True
 for i,j in itertools.product(range(5),repeat=2):
  up=[k for k in range(5) if (i,k) in R and (j,k) in R]
  low=[k for k in up if all((k,l) in R for l in up)]
  if len(low)!=1:good=False;break
  js[i,j]=low[0]
 if not good or any(js[i,c[i]]!=4 for i in range(5)):continue
 edges=sorted((i,j) for i,j in R if i!=j and j!=4);ck(len(edges) in (0,2));accepted.append(edges)
ck(len(accepted)==5);ck(sum(not e for e in accepted)==1)
for k in range(1,21):
 t=2*k; cs=lambda x:x^1 if x<t else t
 join=lambda x,y:x if x==y else t
 for x in range(t+1):
  ck(cs(cs(x))==x);ck((cs(x)==x)==(x==t));ck(join(x,cs(x))==t)
  for y in range(t+1):
   ck(join(x,y)==join(y,x));ck(cs(join(x,y))==join(cs(x),cs(y)))
   for z in range(t+1):ck(join(join(x,y),z)==join(x,join(y,z)))
mon=[]
for n in range(1,4):
 N=1<<n;count=0
 for table in itertools.product(range(2),repeat=N):
  if not all(table[x]<=table[y] for x in range(N) for y in range(N) if x&y==x):continue
  dual=[1-table[N-1-x] for x in range(N)];count+=1
  ck(all(dual[x]<=dual[y] for x in range(N) for y in range(N) if x&y==x))
  ck(all(1-dual[N-1-x]==table[x] for x in range(N)))
 mon.append(count)
ck(mon==[3,6,20])
print(json.dumps({'assertions':checks,'five_element_labelled_models':len(accepted),'types':['four atoms below top','two paired two-element chains below top'],'non_top_edges':accepted,'star_sizes':list(range(3,42,2)),'monotone_boolean_counts':mon},indent=2))
