#!/usr/bin/env python3
"""Regenerate every bounded nonroot cycle JC signature atlas from primitive graphs.

The program builds the two directed paths from an incoming tree vertex to one
reticulation, attaches selected or dummy sink children, enumerates all ordered
side words and outgoing-label permutations, constructs every ordered four-port
descendant-mask tensor, and evaluates the same seven exact JC invariants used
for the theta atlas.  No distributed cycle count or signature is read.
"""
from __future__ import annotations
import argparse, importlib.util, json
from collections import defaultdict
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path

HERE=Path(__file__).resolve().parent; PUB=HERE.parent; OUT=PUB/'certificates'; OUT.mkdir(parents=True,exist_ok=True)

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
 m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ALG=load('theta_algebra',HERE/'regenerate_nonroot_algebra.py')
P=ALG.P; JC_REPS=ALG.JC_REPS; INVARIANTS=ALG.INVARIANTS

def build_cycle(k:int,sink_selected:bool,left_count:int):
 ordinary=k-(1 if sink_selected else 0); right_count=ordinary-left_count
 vv={'IN':'T','X':'R','ROOT':'S','LIN':'L'}; ee=[('ROOT','IN'),('ROOT','LIN')]; leaf_labels={'LIN':k+1}; selected=[]
 label=1
 for side,count in enumerate((left_count,right_count)):
  chain=['IN']
  for j in range(count):
   v=f'P{side}_{j}'; vv[v]='T'; chain.append(v); selected.append((v,label)); label+=1
  chain.append('X'); ee.extend(zip(chain,chain[1:]))
 if sink_selected: selected.append(('X',label)); label+=1
 else:
  vv['Z']='L'; ee.append(('X','Z'))
 assert label==k+1
 for parent,lab in selected:
  leaf=f'L{lab}'; vv[leaf]='L'; ee.append((parent,leaf)); leaf_labels[leaf]=lab
 return {'vertices':vv,'edges':tuple(ee),'leaf_labels':leaf_labels}

def full_signatures(net):
 edges=net['edges']; labels=net['leaf_labels']; incoming=tuple(i for i,(_u,v) in enumerate(edges) if v=='X'); assert len(incoming)==2
 result=[[] for _ in edges]
 for choice in (0,1):
  excluded={incoming[1-choice]}; selected=[i for i in range(len(edges)) if i not in excluded]
  children=defaultdict(list)
  for i in selected: children[edges[i][0]].append(edges[i][1])
  cache={}
  def descend(v):
   if v in cache:return cache[v]
   if v in labels: ans=1<<(labels[v]-1)
   else:
    ans=0
    for w in children.get(v,()): ans|=descend(w)
   cache[v]=ans; return ans
  ss=set(selected)
  for i,(_u,v) in enumerate(edges): result[i].append(descend(v) if i in ss else 0)
 return tuple(tuple(x) for x in result)

def reduced_type(fs,transport):
 sigs=[]
 for sig in fs:
  item=tuple(transport[m] for m in sig)
  if any(item):sigs.append(item)
 sigs=tuple(sorted(set(sigs)))
 flipped=tuple(sorted((b,a) for a,b in sigs))
 return min(sigs,flipped)

def coord_eval(tt,seed):
 vals=[(seed+37*i+11)%P or 2 for i in range(len(tt)+1)]; lam=vals[-1]; out=[]
 for assignment in JC_REPS[1:]:
  total=0
  for ci in (0,1):
   term=lam if ci==0 else 1-lam
   for ei,sig in enumerate(tt):
    mask=sig[ci]; ch=0
    for pos in range(4):
     if mask>>pos&1:ch^=assignment[pos]
    if ch:term=term*vals[ei]%P
   total=(total+term)%P
  out.append(total)
 return out

def coord_sparse(tt):
 n=len(tt)+1; zero=(0,)*n; coords=[]
 for assignment in JC_REPS[1:]:
  total={}
  for ci in (0,1):
   edge=[0]*len(tt)
   for ei,sig in enumerate(tt):
    mask=sig[ci];ch=0
    for pos in range(4):
     if mask>>pos&1:ch^=assignment[pos]
    if ch:edge[ei]=1
   if ci==0:
    m=tuple(edge+[1]); total[m]=(total.get(m,0)+1)%P
   else:
    m0=tuple(edge+[0]);m1=tuple(edge+[1]);total[m0]=(total.get(m0,0)+1)%P;total[m1]=(total.get(m1,0)-1)%P
  coords.append({m:c for m,c in total.items() if c})
 return tuple(coords)
TYPE_BITS={}
def bits(tt):
 if tt in TYPE_BITS:return TYPE_BITS[tt]
 evals=[coord_eval(tt,s) for s in (101,1009,10007)]; sparse=None; ans=0
 for j,inv in enumerate(INVARIANTS):
  nz=any(ALG.invariant_eval(c,inv) for c in evals)
  if not nz:
   if sparse is None:sparse=coord_sparse(tt)
   nz=bool(ALG.invariant_sparse(sparse,inv))
  if nz:ans|=1<<j
 TYPE_BITS[tt]=ans;return ans

def deck(net,total):
 quartets=ALG.ordered_quartets(total); lookup={q:i for i,q in enumerate(quartets)}; subsets,tables=ALG.subset_transports(total); fs=full_signatures(net); out=bytearray(len(quartets))
 for subset,transport in zip(subsets,tables):
  base=reduced_type(fs,transport)
  for ordered in permutations(subset):
   pos=tuple(ordered.index(x) for x in subset)
   transformed=[]
   for sig in base:
    item=[]
    for mask in sig:
     v=0
     for old,new in enumerate(pos):
      if mask>>old&1:v|=1<<new
     item.append(v)
    transformed.append(tuple(item))
   tt=tuple(sorted(set(transformed))); tt=min(tt,tuple(sorted((b,a) for a,b in tt)))
   out[lookup[ordered]]=bits(tt)
 return bytes(out)

def transports(k):return ALG.permutation_transports(k,ALG.ordered_quartets(k+1))

def generate(k:int):
 perms=tuple(permutations(range(1,k+1))); trans=transports(k)
 strong_base=[build_cycle(k,True,left) for left in range(k)]
 weak_base=[build_cycle(k,True,left) for left in range(k)]+[build_cycle(k,False,left) for left in range(k+1)]
 strong_decks=[deck(x,k+1) for x in strong_base]; weak_decks=[deck(x,k+1) for x in weak_base]
 strong=set(); weak_status={}
 for d in strong_decks:
  for t in trans: strong.add(bytes(d[i] for i in t))
 for base_index,d in enumerate(weak_decks):
  status=base_index<k
  for t in trans:
   sig=bytes(d[i] for i in t)
   if sig in weak_status: assert weak_status[sig]==status
   weak_status[sig]=status
 equal=strong & set(weak_status); assert all(weak_status[x] for x in equal)
 strong=sorted(strong);weak=sorted(weak_status)
 (OUT/f'cycle_k{k}_strong_signatures.bin').write_bytes(b''.join(strong));(OUT/f'cycle_k{k}_weak_signatures.bin').write_bytes(b''.join(weak))
 want={3:(9,12,9),4:(48,63,48),5:(300,390,300),6:(2160,2790,2160)}[k]
 assert (len(strong),len(weak),len(equal))==want
 result={'status':'EXACTLY COMPUTED FROM PRIMITIVE CYCLE GRAPHS','outgoing_count':k,'ordered_quartets':len(ALG.ordered_quartets(k+1)),'bytes_per_signature':len(ALG.ordered_quartets(k+1)),'strong_role_presentations':k,'weak_role_presentations':2*k+1,'strong_signatures':len(strong),'weak_signatures':len(weak),'equal_signatures':len(equal),'mixed_strength_signatures':0,'reduced_tensor_types':len(TYPE_BITS),'strong_sha256':sha256((OUT/f'cycle_k{k}_strong_signatures.bin').read_bytes()).hexdigest(),'weak_sha256':sha256((OUT/f'cycle_k{k}_weak_signatures.bin').read_bytes()).hexdigest()}
 (OUT/f'cycle_k{k}_regenerated.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps(result,indent=2,sort_keys=True)); return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,choices=(3,4,5,6));args=ap.parse_args();generate(args.k);print('ALL PRIMITIVE CYCLE ATLAS CHECKS PASSED')
if __name__=='__main__':main()
