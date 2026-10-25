"""Independent full crossing-DAG/potential reconstruction. No source records loaded."""
from pathlib import Path
from array import array
from collections import deque
from itertools import combinations
import sys,json,datetime,time
E=Path(__file__).resolve().parent;fault=sys.argv[1] if len(sys.argv)>1 else '';start=time.monotonic()
def need(v,s):
 if not v:raise RuntimeError(s)
def step(A,g):
 i=abs(g);out=[]
 for word in A:
  stack=[]
  for x in word:
   a=abs(x)
   if g>0:base=(i,i+1,-i) if a==i else (i,) if a==i+1 else (a,)
   else:base=(i+1,) if a==i else (-(i+1),i,i+1) if a==i+1 else(a,)
   if x<0:base=tuple(-t for t in base[::-1])
   for y in base:
    if stack and stack[-1]==-y:stack.pop()
    else:stack.append(y)
  out.append(tuple(stack))
 return tuple(out)
I=tuple((i,) for i in range(1,7))
def action(word):
 a=I
 for g in word:a=step(a,g)
 return a
powers=[3**i for i in range(16)];pair_index={p:i for i,p in enumerate(combinations(range(6),2))};initial=sum(i<<(3*i) for i in range(6));full=powers[15]-1
q=array('I',[0]);p=array('I',[initial]);par=array('I',[0]);letter=bytearray([0]);depth=bytearray([0]);edges=array('i');ids={0:0};u=0
while u<len(q):
 code=q[u];perm=p[u]
 for i in range(5):
  a=(perm>>(3*i))&7;b=(perm>>(3*(i+1)))&7;pw=powers[pair_index[min(a,b),max(a,b)]]
  if code//pw%3==2:edges.append(-1);continue
  new=code+pw;np=perm^((a^b)<<(3*i))^((a^b)<<(3*(i+1)));v=ids.get(new)
  if v is None:v=len(q);ids[new]=v;q.append(new);p.append(np);par.append(u);letter.append(i+1);depth.append(depth[u]+1)
  else:need(p[v]==np and depth[v]==depth[u]+1,'parity_permutation_and_depth_merge')
  edges.append(v)
 u+=1
N=len(q);redges=sum(v>=0 for v in edges);fid=ids[full];need(p[fid]==initial and depth[fid]==30,'full_vector_pure_depth30')
# Reverse graph in compressed-row representation, built from every legal forward edge.
indeg=[0]*N
for v in edges:
 if v>=0:indeg[v]+=1
off=array('I',[0])
for x in indeg:off.append(off[-1]+x)
backedges=array('I',[0])*redges;cursor=list(off[:-1])
for u in range(N):
 for v in edges[5*u:5*u+5]:
  if v>=0:backedges[cursor[v]]=u;cursor[v]+=1
del indeg,cursor
good=bytearray(N);good[fid]=1;todo=deque([fid])
while todo:
 v=todo.popleft()
 for u in backedges[off[v]:off[v+1]]:
  if not good[u]:good[u]=1;todo.append(u)
for u in range(N):need(bool(good[u])==((full-q[u]) in ids),'reverse_vs_complement_coaccessibility')
S=sum(good);SE=sum(v>=0 and good[u] and good[v] for u in range(N) for v in edges[5*u:5*u+5]);need(good[0],'start_coaccessible')
A=[None]*N;A[0]=I
for u in range(1,N):
 if good[u]:need(good[par[u]],'parent_path_coaccessible');A[u]=step(A[par[u]],letter[u])
if fault=='potential':
 u=next(u for u in range(1,N) if good[u] and depth[u]==6);w=A[u][0];A[u]=(w+((1,) if not w or w[-1]!=-1 else(2,)),)+A[u][1:]
comparisons=0;skipped=False
for u in range(N):
 if not good[u]:continue
 for i in range(5):
  v=edges[5*u+i]
  if v<0 or not good[v]:continue
  if fault=='skip-edge' and not skipped:skipped=True;continue
  need(step(A[u],i+1)==A[v],f'literal_edge_action:q{q[u]}:generator{i+1}');comparisons+=1
need(comparisons==SE,'every_coaccessible_edge_compared')
c=[1,2,3,4]*5;h=[5,4,3,2,1,1,2,3,4,5];d=[1,2,3,4,5];z=d*6;az=action(z);need(A[fid]==az,'terminal_full_twist_action');need(action(c+h)==az==action(h+c),'B6_full_twist_decomposition')
for i in range(1,6):need(action(z+[i])==action([i]+z),'full_twist_centrality')
for i in range(1,5):need(action(d+[i]+[-g for g in d[::-1]])==action([i+1]),'shift_conjugation')
def node(word):
 u=0
 for i in word:u=edges[5*u+i-1];need(u>=0,'negative_control_path')
 return u
l=node([1,1,2,2]);r=node([2,2,1,1]);need(l==r and not good[l] and action([1,1,2,2])!=action([2,2,1,1]),'same_counts_different_prefix_actions')
need((N,redges,S,SE)==(234368,711342,90921,261810),'exact_independent_counts')
letters=sum(len(w) for u in range(N) if good[u] for w in A[u]);maxword=max(len(w) for u in range(N) if good[u] for w in A[u])
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','forward_states':N,'forward_edges':redges,'independent_backward_and_complement_coaccessible_states':S,'coaccessible_edges':SE,'literal_six_free_word_edge_comparisons':comparisons,'final_displayed_full_twist_action':az,'full_twist_decomposition_both_orders':True,'five_central_and_four_shift_identities':True,'equal_counts_unequal_prefix_actions_outside_coaccessible_negative_control':True,'total_stored_free_word_letters':letters,'maximum_single_free_word_length':maxword,'source_code_or_stream_loaded':False,'elapsed_seconds':time.monotonic()-start}
(E/'CROSSING_DAG_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
