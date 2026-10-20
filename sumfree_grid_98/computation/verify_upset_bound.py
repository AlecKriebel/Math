"""Fail-closed independent integer checker of all Boolean upsets in dimension 6.
No external libraries, numerical optimization, or assert statements.
The comparison bound uses only actual disjoint-union witnesses.
"""
import json,time

def require(c,msg):
 if not c:raise ValueError(msg)
def upsets(d):
 if d==0:return [0,1]
 old=upsets(d-1);q=1<<(d-1)
 new=[a+(b<<q) for a in old for b in old if a&b==a]
 require(len(new)==len(set(new)), 'Duplicate enumeration')
 return new

def prove(d,bound):
 old=upsets(d-1);q=1<<(d-1);pop=[x.bit_count() for x in old]
 members=[[i for i in range(q) if f>>i&1] for f in old]
 cache=[];selfsizes=[]
 for i,f in enumerate(old):
  row=[]
  for a in range(q):
   row.append(sum(1<<c for c in {a|b for b in members[i] if not a&b}))
  cache.append(row)
  D=0
  for a in members[i]:D|=row[a]
  selfsizes.append(D.bit_count())
 count=0;admissible=0
 for i,a in enumerate(old):
  for j,b in enumerate(old):
   if a&b!=a:continue
   count+=1
   if a&1 or not (b>>(q-1)&1):continue
   admissible+=1
   # D with last coordinate absent is exactly D(a).
   need=pop[i]+pop[j]-selfsizes[i]-bound
   if need<=0:continue
   cross=0
   for x in members[i]:
    cross|=cache[j][x]
    if cross.bit_count()>=need:break
   require(cross.bit_count()>=need,'Found counterexample to claimed bound')
 return {'d':d,'all_upsets':count,'admissible_upsets':admissible,'deficiency_upper_bound':bound,'integer_only':True}
if __name__=='__main__':
 start=time.time();r=prove(6,41);r['seconds']=time.time()-start
 print(json.dumps(r,indent=2))
