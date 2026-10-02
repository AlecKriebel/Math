#!/usr/bin/env python3
"""Exact integer closure of the directed-interval-certified CCSS graph reconstruction."""
import itertools,json,hashlib,argparse
from pathlib import Path
U=[tuple(map(int,line.split(','))) for line in (Path(__file__).parent/'U_CERTIFIED.csv').read_text().splitlines()]
assert len(U)==497
assert hashlib.sha256((Path(__file__).parent/'U_CERTIFIED.csv').read_bytes()).hexdigest()=='7f7a756b9b7184122190273ba754f9ff617f151a0ddb258b31b47cef50e203d3'
parser=argparse.ArgumentParser();parser.add_argument('--omit-sum-filter',action='store_true');args=parser.parse_args()
idx={x:i for i,x in enumerate(U)};N=len(U)
add=lambda a,b:tuple(x+y for x,y in zip(a,b))
sub=lambda a,b:tuple(x-y for x,y in zip(a,b))
mul=lambda a:(a[0]+a[3],a[2]+a[3],a[0]+a[1],a[1])
zero=(0,0,0,0);e0=(1,0,0,0);e4=(0,0,0,1)
# Alphabet indices correspond to 0,1,3,4.
images=[(0,2),(3,2),(1,),(0,1)]
edges=[[(d,zero if j==0 else (e0 if word[0]==0 else e4)) for j,d in enumerate(word)] for word in images]
trans={};deltas=set()
for chars in itertools.product(range(4),repeat=4):
 c=sum(chars[i]*4**i for i in range(4));rows=[]
 for choice in itertools.product(*(edges[a] for a in chars)):
  cs,ls=zip(*choice);cu=sum(cs[i]*4**i for i in range(4))
  du=add(sub(ls[2],tuple(2*a for a in ls[1])),ls[0]);dv=add(sub(ls[3],tuple(2*a for a in ls[2])),ls[1])
  rows.append((cu,du,dv));deltas.update([du,dv])
 trans[c]=rows
nextu={d:[idx.get(add(mul(x),d),-1) for x in U] for d in deltas}
sums=[[add(a,b) in idx for b in U] for a in U]
isL=[sum(x)==0 and x[1]+3*x[2]+4*x[3]==0 for x in U]
word=[0]
for _ in range(5):word=[b for a in word for b in images[a]]
sig=[zero]
for a in word:
 e=tuple(int(i==a) for i in range(4));sig.append(add(sig[-1],e))
starts=[]
for a,b in [(0,1),(3,4),(5,6)]:
 for split in [(a,a,a,b),(a,a,b,b),(a,b,b,b)]:
  p,q,r,s=split;u=add(sub(sig[r],tuple(2*x for x in sig[q])),sig[p]);v=add(sub(sig[s],tuple(2*x for x in sig[r])),sig[q]);c=sum(word[t]*4**i for i,t in enumerate(split))
  assert u in idx and v in idx and sums[idx[u]][idx[v]];starts.append((c,idx[u],idx[v]))
seen=set(starts);queue=list(starts);edges_checked=0
for c,i,j in queue:
 assert not(isL[i] and isL[j])
 for cc,du,dv in trans[c]:
  ii=nextu[du][i];jj=nextu[dv][j];edges_checked+=1
  if ii<0 or jj<0 or (not args.omit_sum_filter and not sums[ii][jj]):continue
  state=(cc,ii,jj)
  if state not in seen:seen.add(state);queue.append(state)
assert len(seen)==(135572 if args.omit_sum_filter else 78340)
stream='\n'.join(','.join(map(str,(c,)+U[i]+U[j])) for c,i,j in sorted(seen))+'\n'
print(json.dumps({'status':'PASS','U_vectors':len(U),'reachable_states':len(seen),'outgoing_edges_checked':edges_checked,'accepting_states':0,'initial_states':starts,'sum_filter_used':not args.omit_sum_filter,'U_sha256':hashlib.sha256((Path(__file__).parent/'U_CERTIFIED.csv').read_bytes()).hexdigest(),'reachable_stream_sha256':hashlib.sha256(stream.encode()).hexdigest(),'scope':'Exact integer closure relative to the directed-interval-certified outward-rounded U. Printed503-vector count is not reproduced (497 here). The larger graph without the u+v filter has exactly the published135572 reachable states; with the filter there are78340. Full reachable stream is regenerable but not retained. Published theorem and analytic reduction remain credited to CCSS.'},indent=2,sort_keys=True))
