import itertools,json
checks=0;words=0
def check(c):
 global checks
 assert c;checks+=1
def partitions(n):
 def rec(a):
  if len(a)==n:yield tuple(a);return
  for x in range(max(a,default=-1)+2):yield from rec(a+[x])
 yield from rec([])
for n in range(1,5):
 X=set(range(n));outside=n
 for f in itertools.product(range(n+1),repeat=n):
  for labels in partitions(n):
   cells=[{i for i in X if labels[i]==j} for j in range(max(labels)+1)]
   for T in range(5):
    byword={}
    for x in X:
     path=[x]
     for t in range(T):
      y=f[path[-1]]
      if y==outside:break
      path.append(y)
     if len(path)!=T+1:continue
     word=tuple(labels[y] for y in path);byword.setdefault(word,[]).append(path)
    for word,paths in byword.items():
     words+=1;P=[cells[i] for i in word];A=[P[0]]
     for t in range(1,T+1):A.append({f[x] for x in A[-1]}&P[t])
     B=[None]*(T+1);B[T]=P[T]
     for t in range(T-1,-1,-1):B[t]={x for x in P[t] if f[x] in B[t+1]}
     Q=[A[t]&B[t] for t in range(T+1)]
     for t in range(T+1):check(Q[t]=={p[t] for p in paths})
     check(all(Q[t]==P[t] for t in range(T+1))==all({f[x] for x in P[t]}==P[t+1] for t in range(T)))
print(json.dumps({'assertions':checks,'realizable_words':words,'scope':'exhaustive maps on at most4states with optional escape, all partitions and horizons0through4; proofs cover arbitrary sets'},indent=2))
