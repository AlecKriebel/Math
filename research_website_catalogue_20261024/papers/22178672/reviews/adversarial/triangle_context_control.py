"""Independent examination of an ordinary triangle inside a theta blob."""
from fresh_controls import rootings
from itertools import product
from pathlib import Path
import json,random
P=1000003
leaf={f'L{i}' for i in range(4)}
base=[('S','U',False),('S','V',True),('U','V',True),('U','A',False),('A','X',True),('V','B',False),('B','X',True),('S','L0',False),('A','L1',False),('B','L2',False),('X','L3',False)]
other=[('U','S',True),('V','S',True),('U','V',False),('U','A',False),('A','X',True),('V','B',False),('B','X',True),('S','L0',False),('A','L1',False),('B','L2',False),('X','L3',False)]
def rank(A):
 A=[r[:] for r in A];r=0
 for c in range(len(A[0])):
  p=next((j for j in range(r,len(A)) if A[j][c]),None)
  if p is None:continue
  A[r],A[p]=A[p],A[r];v=pow(A[r][c],-1,P)
  for j in range(r+1,len(A)):
   z=A[j][c]*v%P
   for k in range(c,len(A[0])):A[j][k]=(A[j][k]-z*A[r][k])%P
  r+=1
  if r==len(A):break
 return r

def terms(edges,retics,rooting):
 arcs=rooting['arcs'];index={frozenset((a,b)):i for i,(a,b,_) in enumerate(edges)}
 root_a,root_b=rooting['root_edge'];edgeids=[]
 for a,b in arcs:
  edgeids.append(None if a=='ROOT' and b==root_a else index[frozenset((root_a,root_b))] if a=='ROOT' else index[frozenset((a,b))])
 parents={v:sorted(a for a,b in arcs if b==v) for v in retics};outs=[]
 for h0,h1,h2 in product(range(4),repeat=3):
  h=(h0,h1,h2,h0^h1^h2);rs=[]
  for bits in product((0,1),repeat=2):
   active=[(a,b,e) for (a,b),e in zip(arcs,edgeids) if b not in retics or a==parents[b][bits[retics.index(b)]]]
   children={v:[] for a,b in arcs for v in (a,b)}
   for a,b,e in active:children[a].append((b,e))
   powers=[0]*(3*len(edges)+2)
   def rec(v):
    x=h[int(v[1:])] if v in leaf else 0
    for w,e in children[v]:
     y=rec(w);x^=y
     if e is not None and y:powers[3*e+y-1]+=1
    return x
   assert rec('ROOT')==0;rs.append((powers,bits))
  outs.append(rs)
 return outs

def values_and_jac(outs,x):
 vals=[];J=[]
 for row in outs:
  val=0;grad=[0]*len(x)
  for powers,bits in row:
   fac=[pow(x[i],e,P) for i,e in enumerate(powers[:-2])]
   fac += [x[-2+i] if bit==0 else (1-x[-2+i])%P for i,bit in enumerate(bits)]
   t=1
   for z in fac:t=t*z%P
   val=(val+t)%P
   for i,e in enumerate(powers[:-2]):
    if e:grad[i]=(grad[i]+t*e*pow(x[i],-1,P))%P
   for i,bit in enumerate(bits):grad[-2+i]=(grad[-2+i]+t*(1 if bit==0 else -1)*pow(fac[-2+i],-1,P))%P
  vals.append(val);J.append(grad)
 return vals,J

def main():
 out={};maps=[]
 for name,edges,retics in [('N',base,('V','X')),('Nprime',other,('S','X'))]:
  roots=rootings(edges,set(retics),leaf);tc=sum(r['tree_child'] for r in roots)
  out[name]={'mixed_edges':edges,'reticulations':retics,'rooting_census':[len(roots),tc,len(roots)-tc],'rootings':roots}
  root=next(r for r in roots if set(r['root_edge'])==({'S','L0'} if name=='N' else {'A','L1'}))
  maps.append(terms(edges,retics,root))
 rng=random.Random(22178672)
 for entry,mp in zip(out.values(),maps):
  ranks=[]
  for trial in range(3):
   x=[rng.randrange(2,P-1) for _ in range(35)];ranks.append(rank(values_and_jac(mp,x)[1][1:]))
  entry['generic_mod_p_rank_lower_bounds']=ranks;entry['modulus']=P
 inv2=pow(2,-1,P);inv3=pow(3,-1,P);q=2*pow(5,-1,P)%P
 x1=[q]*35;x2=[q]*35
 for e in [0,1,2,3,5,7]:
  for s in range(3):x1[3*e+s]=x2[3*e+s]=inv2
 for s in range(3):x1[s]=inv3;x2[6+s]=inv3
 x1[-2]=x2[-2]=inv2;x1[-1]=x2[-1]=3*pow(7,-1,P)%P
 v1,j1=values_and_jac(maps[0],x1);v2,j2=values_and_jac(maps[1],x2)
 out['common_triangle_point']={'outputs_equal_mod_p':v1==v2,'ranks':[rank(j1[1:]),rank(j2[1:])]}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:{x:y for x,y in v.items() if x!='rootings'} if isinstance(v,dict) else v for k,v in out.items()},indent=2))
if __name__=='__main__':main()
