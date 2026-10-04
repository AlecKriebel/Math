#!/usr/bin/env python3
"""Independent finite falsification controls. No proof of an infinite hierarchy."""
from itertools import product
from pathlib import Path
from hashlib import sha256
import json, random

OUT=Path(__file__).resolve().parent
rng=random.Random(334137448)

# Implement the relational diagonal clauses independently of the release script.
geom=[]
for h in range(1,5):
 for w in range(1,5):
  cells=[(i,j) for i in range(h) for j in range(w)]
  found=[[],[]]
  for m in range(1<<(h*w)):
   S={cells[t] for t in range(h*w) if (m>>t)&1}
   for idx,delta in enumerate([1,-1]):
    first=0 if delta==1 else w-1
    last=w-1 if delta==1 else 0
    ok=(S & {(0,j) for j in range(w)})=={(0,first)}
    ok=ok and all(i==h-1 or (i+1,j+delta) in S for i,j in S)
    ok=ok and all(i==0 or (i-1,j-delta) in S for i,j in S)
    ok=ok and all(i!=h-1 or j==last for i,j in S)
    if ok: found[idx].append(sorted(S))
  expected=[sorted((i,i) for i in range(h)),sorted((i,w-1-i) for i in range(h))]
  assert found==([[expected[0]],[expected[1]]] if h==w else [[],[]])
  geom.append({'h':h,'w':w,'assignments':1<<(h*w),'positive_models':len(found[0]),'negative_models':len(found[1])})

# Paired comparisons on squares, including middle-column and side-one cases.
mirror=[]
for n in range(1,5):
 symmetric=0
 for seq in product(range(2),repeat=n*n):
  rows=[seq[i*n:(i+1)*n] for i in range(n)]
  direct=all(r==r[::-1] for r in rows)
  mismatch=any(rows[i][j]!=rows[i][n-j-1] for i in range(n) for j in range(n))
  assert direct == (not mismatch)
  symmetric+=direct
 assert symmetric==2**(n*((n+1)//2))
 mirror.append({'side':n,'tested':2**(n*n),'symmetric':symmetric})

# Splices with independent nonbinary alphabets, arbitrary cuts, and exterior borders.
def tiles(a):
 h,w=len(a),len(a[0])
 def get(i,j): return a[i][j] if 0<=i<h and 0<=j<w else -1
 return {tuple(get(i+di,j+dj) for di,dj in [(0,0),(0,1),(1,0),(1,1)]) for i in range(-1,h) for j in range(-1,w)}
splices=0
for h in range(1,9):
 for w in range(2,10):
  for cut in range(1,w):
   for g in [2,3,7]:
    a=[[rng.randrange(g) for _ in range(w)] for _ in range(h)]
    b=[[rng.randrange(g) for _ in range(w)] for _ in range(h)]
    for i in range(h):
     b[i][cut-1:cut+1]=a[i][cut-1:cut+1]
    s=[a[i][:cut]+b[i][cut:] for i in range(h)]
    assert tiles(s)<=tiles(a)|tiles(b)
    splices+=1

# Exhaustive pointwise alternating truth tables through four blocks.
def evaluate(k,table,certificate):
 def go(i,assignment):
  if i==k:
   accept=bool((table>>assignment)&1)
   if not certificate: return accept
   valid=(assignment^(assignment>>1))&1
   def term(c): return (c==valid and accept) if k%2 else (c!=valid or accept)
   return any(map(term,[0,1])) if k%2 else all(map(term,[0,1]))
  vals=[go(i+1,assignment|(b<<i)) for b in [0,1]]
  return any(vals) if i%2==0 else all(vals)
 return go(0,0)
parity=[]
for k in range(1,5):
 total=1<<(1<<k)
 for table in range(total): assert evaluate(k,table,False)==evaluate(k,table,True)
 parity.append({'blocks':k,'truth_tables':total})

# Independently draw the binary code at broader code widths and cross-block boundaries.
ring=((1,1,1),(1,0,1),(1,1,1))
coding=0
for ell in range(1,13):
 c=2*ell+8
 for n in range(1,5):
  for mode in ['zeros','ones','alternating','random']:
   size=c*n
   a=[[0]*size for _ in range(size)]
   expected=[]
   for i in range(n):
    for j in range(n):
     for di in range(3):
      for dj in range(3): a[i*c+di][j*c+dj]=ring[di][dj]
     bits=([0]*ell if mode=='zeros' else [1]*ell if mode=='ones' else [(q+i+j)%2 for q in range(ell)] if mode=='alternating' else [rng.randrange(2) for _ in range(ell)])
     for q,b in enumerate(bits): a[i*c+5][j*c+1+2*q]=b
     expected.append(((i*c+1,j*c+1),bits))
   markers=[]
   for i in range(1,size-1):
    for j in range(1,size-1):
     if all(a[i+di-1][j+dj-1]==ring[di][dj] for di in range(3) for dj in range(3)):
      markers.append((i,j))
   assert markers==[m for m,b in expected]
   for (i,j),bits in expected: assert [a[i+4][j+2*q] for q in range(ell)]==bits
   # Counterexample to literal assertion that all four block margins are zero.
   assert a[0][0]==1 and a[0][1]==1 and a[1][0]==1
   coding+=1

# Hash verification before and after the audit is recorded separately by the auditor.
result={'status':'PASS','finite_only':True,'geometry':geom,'mirror':mirror,'nonbinary_arbitrary_cut_splices':splices,'last_block_truth_tables':parity,'expanded_binary_code_cases':coding,'code_widths_tested':[1,12],'zero_top_left_margin_claim':False}
(OUT/'independent-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'mirror_pictures':sum(r['tested'] for r in mirror),'splices':splices,'parity_tables':sum(r['truth_tables'] for r in parity),'coding_cases':coding,'zero_top_left_margin_claim':False},indent=2))
