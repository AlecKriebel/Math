from itertools import product
from fractions import Fraction as F
from pathlib import Path
import json
checks=0
def ck(b):
 global checks
 assert b;checks+=1
def sensitivity(mask,n):
 return [sum(((mask>>x)^(mask>>(x^(1<<j))))&1 for j in range(n)) for x in range(1<<n)]
# All triples of functions on the two-cube and all eight factor subsets.
S=[sensitivity(t,2) for t in range(16)]
for fs in product(range(16),repeat=3):
 M=[max(S[t][x] for t in fs) for x in range(4)];out=[]
 for subset in range(8):
  mask=15
  for j in range(3):
   if subset>>j&1:mask &= fs[j]
  ss=S[mask];out.append(ss)
  z=sum(ss[x] for x in range(4) if not(mask>>x&1));o=sum(ss[x] for x in range(4) if mask>>x&1)
  ck(z==o);ck(sum(ss)<=2*sum(M))
  for x in range(4):
   ck((mask>>x&1) or ss[x]<=M[x]);ck(ss[x]<=subset.bit_count()*M[x])
 for x in range(4):ck(max(ss[x] for ss in out)<=3*M[x])
# Direct product enumeration of block Hamming weights; independent of full
# truth-table AND implementation and of the event formula derivation.
from math import comb
for k in range(1,7):
 for m in range(1,6):
  total=0
  for weights in product(range(k+1),repeat=m):
   multiplicity=1
   for w in weights:multiplicity*=comb(k,w)
   score=max(k if w==k else 1 if w==k-1 else 0 for w in weights)
   total+=multiplicity*score
  ck(F(total,2**(k*m))==k-(k-1)*(1-F(1,2**k))**m-(1-F(k+1,2**k))**m)
# Full 15-cube syndrome construction, including every coordinate flip.
r=4;n=15;syndromes=[0]*(1<<n)
for x in range(1,1<<n):
 bit=x&-x;syndromes[x]=syndromes[x^bit]^bit.bit_length()
counts=[0]*16;fulltotal=zerototal=0
for x,t in enumerate(syndromes):
 counts[t]+=1
 ss=[];zz=[]
 for a in range(1,16):
  val=t==a;s=sum(val!=(syndromes[x^(1<<j)]==a) for j in range(n))
  ck(s==(n if val else 1));ss.append(s);zz.append(0 if val else s)
 fulltotal+=max(ss);zerototal+=max(zz)
 for b in range(r):
  s=sum(((t>>b)&1)!=((syndromes[x^(1<<j)]>>b)&1) for j in range(n));ck(s==8)
ck(counts==[2048]*16);ck(F(fulltotal,1<<n)==F(113,8));ck(zerototal==(1<<n));ck(F(113,8)<=16)
result={'status':'PASS','exact_assertions':checks,'input_triples_two_cube':4096,'block_weight_cases':30,'full_hamming_cube_vertices':32768,'full_hamming_dimension':15,'scope':'Finite exact controls for restricted bounds and false one-sided shortcut only; no original-conjecture verdict.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
