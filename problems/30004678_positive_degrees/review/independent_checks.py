import itertools,json,math
n=0
def ck(v):
 global n
 assert v;n+=1
le=lambda a,b:(a&b)==a
cube=range(8)
mon=[f for f in itertools.product([0,1],repeat=8) if all(not le(a,b) or f[a]<=f[b] for a in cube for b in cube)]
ck(len(mon)==20)
for fs in itertools.product(mon,repeat=3):
 good=[z for z in cube if all(fs[i][z]==1-((z>>i)&1) for i in range(3))]
 ck(len(good)<=3)
 ck(all(not le(a,b) and not le(b,a) for a,b in itertools.combinations(good,2)))
compatible=0
for labels in itertools.product([-1,0,1],repeat=8):
 support=[i for i in cube if labels[i]>=0]
 ok=all(not le(i,j) or labels[i]<=labels[j] for i in support for j in support)
 if ok:
  compatible+=1;f=[int(any(labels[i]==1 and le(i,j) for i in support)) for j in cube]
  ck(all(f[i]==labels[i] for i in support));ck(all(not le(i,j) or f[i]<=f[j] for i in cube for j in cube))
orders=0;types={}
for choices in itertools.product([-1,0,1],repeat=6):
 R={(i,i) for i in range(5)}|{(i,4) for i in range(4)}
 for (i,j),v in zip(itertools.combinations(range(4),2),choices):
  if v:R.add((i,j) if v==1 else (j,i))
 if any((a,c) not in R for a,b in R for bb,c in R if b==bb):continue
 star=lambda i:4 if i==4 else i^1
 if any((star(a),star(b)) not in R for a,b in R):continue
 joins={}
 for a,b in itertools.product(range(5),repeat=2):
  U=[u for u in range(5) if (a,u) in R and (b,u) in R];L=[u for u in U if all((u,v) in R for v in U)]
  if len(L)!=1:break
  joins[a,b]=L[0]
 else:
  if all(joins[a,star(a)]==4 for a in range(5)):
   orders+=1;c=sum(a!=b and a<4 and b<4 for a,b in R);types[c]=types.get(c,0)+1
ck(orders==5);ck(types=={0:1,2:4})
for m in range(1,300):ck(math.comb(2*m,m)**2*(m+1)<=2**(4*m))
print(json.dumps({'status':'PASS','independent_assertions':n,'monotone_vector_maps':len(mon)**3,'compatible_partial_labellings':compatible,'five_element_labelled_structures':orders,'comparison_counts':types},indent=2))
