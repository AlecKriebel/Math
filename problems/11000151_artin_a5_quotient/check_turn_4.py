#!/usr/bin/env python3
"""Complete finite B6 certificate, using only exact integers and free words.
No cap. The generated state stream is hashed incrementally, not retained.
"""
from itertools import combinations
from collections import deque
import hashlib,json
N=6
pairs=list(combinations(range(N),2));index={p:i for i,p in enumerate(pairs)}
power=[3**i for i in range(len(pairs))];full=3**len(pairs)-1
identity_perm=tuple(range(N));records={0:(identity_perm,-1,0)};queue=[0];edges=0
for code in queue:
 perm,_,_=records[code]
 for i in range(N-1):
  j=index[tuple(sorted((perm[i],perm[i+1])))];step=power[j]
  if code//step%3==2:continue
  edges+=1;nc=code+step;np=list(perm);np[i],np[i+1]=np[i+1],np[i];np=tuple(np)
  if nc not in records:records[nc]=(np,code,i+1);queue.append(nc)
  else:assert records[nc][0]==np
co={code for code in records if full-code in records}
identity=tuple((i,)for i in range(1,N+1))
def actgen(images,g):
 out=[]
 for word in images:
  w=[]
  for x in word:
   if abs(x)==g:part=(g,g+1,-g)if x>0 else(g,-g-1,-g)
   elif abs(x)==g+1:part=(g,)if x>0 else(-g,)
   else:part=(x,)
   for y in part:
    if w and w[-1]==-y:w.pop()
    else:w.append(y)
  out.append(tuple(w))
 return tuple(out)
images={0:identity}
for code in queue:
 if code and code in co:
  perm,parent,g=records[code];assert parent in images;images[code]=actgen(images[parent],g)
comparisons=0
for code in queue:
 if code not in co:continue
 perm,_,_=records[code]
 for i in range(N-1):
  j=index[tuple(sorted((perm[i],perm[i+1])))];step=power[j]
  if code//step%3==2:continue
  nc=code+step
  if nc not in co:continue
  assert actgen(images[code],i+1)==images[nc];comparisons+=1
standard=identity
for _ in range(N):
 for i in range(1,N):standard=actgen(standard,i)
assert images[full]==standard
assert len(records)==234368 and edges==711342 and len(co)==90921 and comparisons==261810
sha=hashlib.sha256()
for code in sorted(co):
 perm=records[code][0];packed=sum(a<<(3*i)for i,a in enumerate(perm))
 line='S|'+str(code)+'|'+str(packed)+'|'+('|'.join(','.join(map(str,w))for w in images[code]))+'\n'
 sha.update(line.encode())
print(json.dumps({'status':'PASS','strands':N,'reachable_states':len(records),'outgoing_edges':edges,'coaccessible_states':len(co),'coaccessible_edges':comparisons,'exact_Artin_action_edge_equalities':comparisons,'terminal_full_twist_action_equal':True,'canonical_action_stream_sha256':sha.hexdigest(),'scope':'Exhaustive all positive six-strand words with every labelled pair crossing exactly twice. Faithful Artin action gives equality to the full twist; no quotient faithfulness or finite-prefix extrapolation.'},indent=2,sort_keys=True))
