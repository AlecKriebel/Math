"""Check authored wraparound witnesses; coordinates in report are 1-indexed."""
import json
rows=[]
for m in range(1,101):
 core='ABCC'*m+'DDAB'*m
 for r,c in [(1,core+'D'),(3,core+'DBA'),(5,'CC'+core+'DBA'),(7,'ABCC'+core+'DBA')]:
  n=8*m+r
  if r==1:points=[n,1,2,3];d=1;expected='DABC'
  elif r==5:points=[n-2,n-1,n,1];d=1;expected='DBAC'
  else:points=[n-2,n,2,4];d=2;expected='DABC'
  assert len(c)==n
  assert all(n//4<=c.count(b)<=(n+3)//4 for b in 'ABCD')
  assert all((points[i+1]-points[i])%n==d for i in range(3))
  colors=''.join(c[x-1] for x in points)
  assert colors==expected and len(set(colors))==4
  if m==1:rows.append(dict(n=n,r=r,points=points,step=d,colors=colors))
print(json.dumps({'checks':400,'m_range':[1,100],'smallest_examples':rows},indent=2))
