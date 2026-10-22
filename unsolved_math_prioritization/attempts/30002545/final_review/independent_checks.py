import itertools,json
count=0;objects=0
for m in range(1,6):
 totals=[0,0,0];seen=set()
 def words(rem,prefix=()):
  if not any(rem):yield prefix;return
  for i,a in enumerate(rem):
   if a:
    q=list(rem);q[i]-=1;yield from words(q,prefix+(i+1,))
 for w in words([2]*m):
  pos={i:[j for j,a in enumerate(w) if a==i] for i in range(1,m+1)}
  if any(any(a<i for a in w[l+1:r]) for i,(l,r) in pos.items()):continue
  objects+=1;interval={}
  for i,(l,r) in pos.items():
   while l>0 and w[l-1]>=i:l-=1
   while r+1<len(w) and w[r+1]>=i:r+=1
   interval[i]=(l,r)
  slots={i:[None]*3 for i in pos}
  for i,(l,r) in interval.items():
   if i==1:continue
   outer=[j for j,(a,b) in interval.items() if j!=i and a<=l and r<=b]
   parent=min(outer,key=lambda j:interval[j][1]-interval[j][0]);pl,pr=pos[parent]
   slot=0 if r<pl else 2 if l>pr else 1
   assert slots[parent][slot] is None;count+=1;slots[parent][slot]=i
  def encode(i,rotation=0):
   if i is None:return ()
   s=slots[i];s=s[rotation:]+s[:rotation]
   return encode(s[0],rotation)+(i,)+encode(s[1],rotation)+(i,)+encode(s[2],rotation)
  assert encode(1)==w;count+=1
  empty=[sum(s[j] is None for s in slots.values()) for j in range(3)]
  assert sum(empty)==2*m+1;count+=1
  plateau=sum(w[j]==w[j+1] for j in range(len(w)-1));assert plateau==empty[1];count+=1
  pairparent={i:min([j for j,(a,b) in pos.items() if a<pos[i][0]<pos[i][1]<b],key=lambda j:pos[j][1]-pos[j][0],default=0) for i in pos}
  leaves=sum(i not in pairparent.values() for i in pos)
  assert leaves==plateau;count+=1
  rot=encode(1,1);assert all(all(a>i for a in rot[rot.index(i)+1:len(rot)-1-rot[::-1].index(i)]) for i in pos);count+=1
  seen.add(rot)
  totals=[a+b for a,b in zip(totals,empty)]
 assert totals[0]==totals[1]==totals[2];count+=1
 assert len(seen)*(2*m+1)==sum(totals);count+=1
print(json.dumps({'status':'PASS','assertions':count,'objects':objects,'maximum_stirling_order':5},sort_keys=True))
