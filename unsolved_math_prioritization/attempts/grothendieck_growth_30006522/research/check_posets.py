import pickle,json
from explore import length,left
A=pickle.load(open('groth_supports7.pickle','rb'))
def inv(w):return sum(1<<k for k,(i,j) in enumerate(( (i,j) for i in range(len(w)) for j in range(i+1,len(w)))) if w[i]>w[j])
I={w:inv(w) for w in A}
conv=[];bottom=[];gaps=0
for w,a in A.items():
 for u in a:
  if I[w]&I[u]!=I[w] and len(bottom)<5:bottom.append([w,u])
  for k in range(1,7):
   if u.index(k)>u.index(k+1):continue
   v=left(u,k)
   if v in a:continue
   if any(I[v]&I[t]==I[v] for t in a):
    gaps+=1
    if len(conv)<5:conv.append([w,u,v,next(t for t in a if I[v]&I[t]==I[v])])
r={'n':7,'convexity_missing_neighbor_witnesses':conv,'total_witnesses':gaps,'not_above_bottom_examples':bottom}
json.dump(r,open('poset_n7.json','w'),indent=2);print(r)
