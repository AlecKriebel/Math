"""Exact finite controls for the credited bijections; the written proof is all-size."""
import itertools,json,math
N=0
def ck(b):
 global N
 N+=1
 assert b

def plane_from_word(w):
 m=len(w)//2;pos={i:[k for k,x in enumerate(w) if x==i] for i in range(1,m+1)}
 children=[[] for _ in range(m+1)]
 for i,(a,b) in pos.items():
  outer=[j for j,(c,d) in pos.items() if c<a<b<d]
  parent=min(outer,key=lambda j:pos[j][1]-pos[j][0]) if outer else 0
  children[parent].append(i)
 for cs in children:cs.sort(key=lambda i:pos[i][0])
 return tuple(tuple(c) for c in children)
def plane_word(t,v=0):
 out=[]
 for u in t[v]:out += [u]+list(plane_word(t,u))+[u]
 return tuple(out)
def ternary_from_word(w):
 m=len(w)//2;I={};pos={i:[k for k,x in enumerate(w) if x==i] for i in range(1,m+1)}
 for i,(a,b) in pos.items():
  l=a;r=b
  while l and w[l-1]>=i:l-=1
  while r+1<len(w) and w[r+1]>=i:r+=1
  I[i]=(l,r)
 slots=[[0,0,0] for _ in range(m+1)]
 for i,(a,b) in I.items():
  if i==1:continue
  outer=[j for j,(c,d) in I.items() if c<=a<=b<=d and j!=i]
  p=min(outer,key=lambda j:I[j][1]-I[j][0]);x,y=pos[p]
  slot=0 if b<x else 1 if x<a and b<y else 2
  ck(slots[p][slot]==0);slots[p][slot]=i
 return tuple(tuple(x) for x in slots)
def ternary_word(t,v=1):
 if not v:return ()
 a,b,c=t[v]
 return ternary_word(t,a)+(v,)+ternary_word(t,b)+(v,)+ternary_word(t,c)
def rotate(t):return tuple((r,l,m) for l,m,r in t)
def is_stirling(w):
 return all(all(j>i for j in w[w.index(i)+1:len(w)-1-w[::-1].index(i)]) for i in set(w))
def main():
 words=[()];rows=[];total=0
 for m in range(1,8):
  words=[w[:k]+(m,m)+w[k:] for w in words for k in range(len(w)+1)]
  ck(len(words)==math.prod(range(1,2*m,2)));ck(len(set(words))==len(words))
  ps=set();ts=set();leaves=0;totals=[0,0,0]
  for w in words:
   ck(is_stirling(w));p=plane_from_word(w);t=ternary_from_word(w)
   ck(plane_word(p)==w);ck(ternary_word(t)==w)
   ck(all(v<u for v,cs in enumerate(p) for u in cs));ck(all(v<u for v,cs in enumerate(t) if v for u in cs if u))
   l=sum(not c for c in p);z=sum(a==b for a,b in zip(w,w[1:]));e=[sum(t[v][j]==0 for v in range(1,m+1)) for j in range(3)]
   ck(l==z==e[1]);ck(sum(e)==2*m+1)
   r=rotate(t);rr=rotate(r);ck(rotate(rr)==t)
   ck(is_stirling(ternary_word(r)));ck(ternary_from_word(ternary_word(r))==r)
   ck([sum(r[v][j]==0 for v in range(1,m+1)) for j in range(3)]==[e[2],e[0],e[1]])
   ps.add(p);ts.add(t);leaves+=l
   for j in range(3):totals[j]+=e[j]
  ck(len(ps)==len(words)==len(ts));ck(totals[0]==totals[1]==totals[2]);ck(3*leaves==(2*m+1)*len(words))
  rows.append({'n_vertices':m+1,'trees':len(words),'total_leaves':leaves,'empty_slot_totals':totals});total+=len(words)
 ck(1==sum(not cs for cs in ((),)))
 print(json.dumps({'problem_id':30002545,'turn':1,'status':'PASS','exact_assertions':N,'objects_checked':total,'rows':rows,'singleton_leaf_probability':1,'scope':'Exhaustive finite controls through n=8. The all-n bijective proof, not this enumeration, proves the candidate.'},indent=2))
if __name__=='__main__':main()
