#!/usr/bin/env python3
from __future__ import annotations
import sys,json,itertools,hashlib
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'software/atlas'))
import k3p_atlas_core as k
LOCK=json.load(open(ROOT/'K3P_14_ORBIT_LOCK.json')); R={r['orbit_id']:r for r in LOCK['records']}
S=k.source_supports(); T=k.target_completions(4,True)+k.target_completions(4,False); CH4=k.k3p_assignments(4); CH3=k.k3p_assignments(3)

def add(*terms):
 out=defaultdict(F)
 for c,p in terms:
  for e,v in p.items():out[e]+=F(c)*v
 return {e:v for e,v in out.items() if v}
def mul(*ps):
 if not ps:return {():F(1)}
 z=ps[0]
 for p in ps[1:]:z=k.sparse_mul(z,p)
 return z
def var(n,i):return {tuple(1 if j==i else 0 for j in range(n)):F(1)}
def one(n):return {(0,)*n:F(1)}
def eval_qpoly(q,terms):
 z=F(0)
 for t in terms:
  m=F(t['coefficient'])
  for i in t['coordinate_indices']:m*=q[i]
  z+=m
 return z
def point(r,side):
 d=r[side+'_exact_rank_point'];return tuple(tuple(F(x) for x in a) for a in d['edges']),tuple(F(x) for x in d['inheritance'])
def margin(pt):
 E,L=pt;z=[]
 for c,g,t in E:z += [c,g,t,1-c,1-g,1-t,1+c-g-t,1-c+g-t,1-c-g+t]
 for x in L:z += [x,1-x]
 return min(z)
def pull(desc,terms):
 ops=k.output_sparse_polynomials_cached(desc);out={}
 for t in terms:
  z=k.sparse_mul_many([ops[i] for i in t['coordinate_indices']])
  for e,c in z.items():out[e]=out.get(e,F(0))+F(t['coefficient'])*c
 return {e:c for e,c in out.items() if c}
def hash_poly(p):return hashlib.sha256(json.dumps([(list(e),str(c)) for e,c in sorted(p.items())],separators=(',',':')).encode()).hexdigest()

def verify_rank_minor(desc,pt,cert):
 J=k.descriptor_jacobian(desc,*pt);M=[[J[i][j] for j in cert['parameter_columns']] for i in cert['output_rows']]
 d=k.determinant_square(M);assert str(d)==cert['determinant'] and d

def verify_h21_factorization():
 r=R['H21-02'];td=k.model_descriptor_fast2(k.relabel_record(T[r['target_index']],tuple(r['representative_permutation'])).graph);ops=k.output_sparse_polynomials_cached(td)
 n=3*td.edge_class_count+td.retic_count;O=one(n);E=[[var(n,3*i+s) for s in range(3)] for i in range(8)];l0=var(n,24);l1=var(n,25);m0=add((1,O),(-1,l0));m1=add((1,O),(-1,l1))
 # T-sector letters a,b,c,d,f,h,i,j
 a,b,c,d,f,h,i,j=[E[x][2] for x in range(8)]
 U=mul(a,l0);V=mul(j,m0);Z=mul(c,d,i);D=mul(d,i);I=i;A0=mul(h,b,l1);B0=mul(h,f,m1)
 A=mul(E[2][0],E[3][0],E[6][0]);B=mul(E[2][1],E[3][1],E[6][1]);e2C=E[2][0];e2G=E[2][1]
 rhs3=mul(V,add((1,mul(D,A0)),(1,mul(I,I,B0))))
 rhs12=mul(U,add((1,mul(D,A0)),(1,B0)))
 rhs51=mul(Z,add((1,A0),(1,mul(D,B0))))
 rhs63=mul(V,Z,add((1,mul(I,I,A0)),(1,mul(D,B0))))
 identities=[
  add((1,mul(I,ops[3])),(-1,mul(I,U)),(-1,rhs3)),
  add((1,ops[12]),(-1,rhs12),(-1,mul(V,I))),
  add((1,ops[15]),(-1,mul(D,A0)),(-1,B0)),
  add((1,ops[20]),(-1,A)),
  add((1,mul(e2G,ops[27])),(-1,mul(e2G,B0,A)),(-1,mul(A0,e2C,B))),
  add((1,mul(e2C,ops[39])),(-1,mul(e2C,B0,B)),(-1,mul(A0,e2G,A))),
  add((1,ops[40]),(-1,B)),
  add((1,mul(I,ops[48])),(-1,mul(I,U,ops[51])),(-1,mul(V,Z))),
  add((1,mul(D,ops[51])),(-1,rhs51)),
  add((1,ops[60]),(-1,Z)),
  add((1,mul(D,I,ops[63])),(-1,mul(D,I,U,Z)),(-1,rhs63))]
 assert all(not z for z in identities)
 print('PASS H21-02 ten-generator rational factorization')

def relabel_keep(G,omit):
 keep=[x for x in range(4) if x!=omit];H=k.restrict_rooted(G,set(keep));mp={old:i for i,old in enumerate(keep)}
 for n,d in H.nodes(data=True):
  if d.get('role')=='leaf' and isinstance(d.get('label'),int):d['label']=mp[d['label']]
 return H,keep

def compress_selected(desc,omit):
 rows=[i for i,c in enumerate(CH4) if c[omit]==0];ops=k.output_sparse_polynomials_cached(desc)
 # variable occurrence signatures across selected sparse monomials
 sig={}
 for ci in range(desc.edge_class_count):
  arr=[]
  for oi in rows:
   for ex in sorted(ops[oi]):arr.extend(ex[3*ci:3*ci+3])
  sig[ci]=tuple(arr)
 groups=defaultdict(list)
 for ci,s in sig.items():groups[s].append(ci)
 active=[g for s,g in groups.items() if any(s)];invis=[g for s,g in groups.items() if not any(s)]
 active=sorted(active,key=lambda g:min(g));assert len(active)==4
 nnew=13;retvars=[]
 for j in range(desc.retic_count):
  idx=3*desc.edge_class_count+j
  if any(any(e[idx] for e in ops[oi]) for oi in rows):retvars.append(j)
 assert len(retvars)==1
 out=[]
 for oi in rows:
  P=defaultdict(F)
  for ex,co in ops[oi].items():
   for g in invis:
    for ci in g:assert ex[3*ci:3*ci+3]==(0,0,0)
   ne=[0]*nnew
   for aidx,g in enumerate(active):
    vals=[ex[3*ci:3*ci+3] for ci in g];assert all(v==vals[0] for v in vals)
    ne[3*aidx:3*aidx+3]=vals[0]
   for j in range(desc.retic_count):
    if j==retvars[0]:ne[12]=ex[3*desc.edge_class_count+j]
    else:assert ex[3*desc.edge_class_count+j]==0
   P[tuple(ne)]+=co
  out.append({e:c for e,c in P.items() if c})
 # reorder full rows into standard 3-port assignments
 rowmap={tuple(c[x] for x in range(4) if x!=omit):p for p,c in enumerate(CH4) if c[omit]==0}
 return tuple(out),rows,active,invis,retvars[0]

def canonical_sunlet_raw(emap,flip,pp):
 n=13;O=one(n);E=[[var(n,3*i+s) for s in range(3)] for i in range(4)];L=var(n,12);Lm=add((1,O),(-1,L));ea,eb,eu,ev=[E[i] for i in emap]
 if not flip:A=[mul(L,ea[s]) for s in range(3)];B=[mul(Lm,eb[s]) for s in range(3)]
 else:A=[mul(Lm,ea[s]) for s in range(3)];B=[mul(L,eb[s]) for s in range(3)]
 U=eu;V=ev;can=[];deps=[]
 for x,y,z in CH3:
  if x==y==z==0:P=O;D=set()
  elif x==0:P=add((1,A[y-1]),(1,mul(V[y-1],B[y-1])));D={('A',y),('V',y),('B',y)}
  elif y==0:P=mul(U[x-1],add((1,mul(V[x-1],A[x-1])),(1,B[x-1])));D={('U',x),('V',x),('A',x),('B',x)}
  elif z==0:P=mul(U[x-1],V[x-1]);D={('U',x),('V',x)}
  else:P=mul(U[x-1],add((1,mul(V[x-1],A[z-1])),(1,mul(V[y-1],B[z-1]))));D={('U',x),('V',x),('A',z),('V',y),('B',z)}
  can.append(P);deps.append(D)
 idx={a:i for i,a in enumerate(CH3)};op=[idx[tuple(a[pp[i]] for i in range(3))] for a in CH3]
 return tuple(can[op[i]] for i in range(16)),tuple(deps[op[i]] for i in range(16))

def verify_sunlet_compression(name,omit,selected_rows=None,expected_dep_count=12):
 r=R[name];td=k.model_descriptor_fast2(k.relabel_record(T[r['target_index']],tuple(r['representative_permutation'])).graph);compressed,rows,active,invis,ret=compress_selected(td,omit)
 # compressed list rows follows CH4 filtered order, which equals CH3 order after dropping omitted coordinate
 found=None
 for em in itertools.permutations(range(4)):
  for fl in (False,True):
   for pp in itertools.permutations(range(3)):
    can,deps=canonical_sunlet_raw(em,fl,pp)
    if compressed==can:found=(em,fl,pp,deps);break
   if found:break
  if found:break
 assert found
 deps=found[3]
 if selected_rows is None:sel3=range(1,16)
 else:
  maprow={r:i for i,r in enumerate(rows)};sel3=[maprow[i] for i in selected_rows]
 union=set().union(*(deps[i] for i in sel3));assert len(union)==expected_dep_count,(name,union)
 print('PASS',name,'sunlet compression groups',active,'invisible',invis,'retic',ret,'canonical',found[:3],'generators',len(union))

def verify_all():
 assert LOCK['canonical_orbits']==14 and LOCK['raw_survivors']==40
 assert sum(len(r['raw_members']) for r in LOCK['records'])==38
 assert len(LOCK['prelock_exact_separations'])==2
 # Exact integrity correction for the two source-5 sink-swap presentations.
 pc=json.load(open(ROOT/'software/certificates/k3p_prelock_source5_quartic.json'))
 assert len(pc['records'])==2
 sd5=k.model_descriptor_fast2(S[5].graph); e5,l5=k.default_exact_point(sd5,2); q5=k.eval_descriptor(sd5,e5,l5)
 for c,lk in zip(pc['records'],LOCK['prelock_exact_separations']):
  assert c['permutation']==lk['permutation'] and lk['category']=='POLYNOMIALLY-SEPARATED'
  td5=k.model_descriptor_fast2(k.selected_graph_from_completion(k.relabel_record(T[822],tuple(c['permutation']))))
  assert k.mixed_relation_exact(S[5].graph,k.selected_graph_from_completion(k.relabel_record(T[822],tuple(c['permutation']))))=='none'
  assert not pull(td5,c['terms']); sp=pull(sd5,c['terms']); assert sp and hash_poly(sp)==c['source_pullback_sha256']
  assert eval_qpoly(q5,c['terms'])==F(c['source_evaluation']) and margin((e5,l5))>0
 print('PASS two pre-lock source-5 sink-swap quartic separations')
 # literal graph/map binding and graph relation
 for r in LOCK['records']:
  sd=k.model_descriptor_fast2(S[r['source_index']].graph);td=k.model_descriptor_fast2(k.relabel_record(T[r['target_index']],tuple(r['representative_permutation'])).graph)
  assert hashlib.sha256(repr(sd).encode()).hexdigest()==r['source_map_hash'];assert hashlib.sha256(repr(td).encode()).hexdigest()==r['target_map_hash']
  assert k.mixed_relation_exact(S[r['source_index']].graph,k.relabel_record(T[r['target_index']],tuple(r['representative_permutation'])).graph)=='none'
 print('PASS fourteen literal graph/map bindings')
 # exact H14 marginal identities
 hcert=json.load(open(ROOT/'software/certificates/k3p_h14_marginal_orbit_certificates.json'))
 for c in hcert['records']:
  r=R[c['orbit_id']];sd=k.model_descriptor_fast2(S[r['source_index']].graph);td=k.model_descriptor_fast2(k.relabel_record(T[r['target_index']],tuple(r['representative_permutation'])).graph)
  assert not pull(td,c['terms']);sp=pull(sd,c['terms']);assert hash_poly(sp)==c['source_pullback_sha256'];pt=point(r,'source');assert eval_qpoly(k.eval_descriptor(sd,*pt),c['terms'])==F(c['source_evaluation']) and margin(pt)>0
  print('PASS',c['orbit_id'],'transported H14 quartic')
 # exact remaining quartics
 qcert=json.load(open(ROOT/'software/certificates/k3p_remaining_quartic_separators.json'))
 for c in qcert['records']:
  r=R[c['orbit_id']];sd=k.model_descriptor_fast2(S[r['source_index']].graph);td=k.model_descriptor_fast2(k.relabel_record(T[r['target_index']],tuple(r['representative_permutation'])).graph)
  assert not pull(td,c['terms']);sp=pull(sd,c['terms']);assert hash_poly(sp)==c['source_pullback_sha256'];pt=point(r,'source');assert eval_qpoly(k.eval_descriptor(sd,*pt),c['terms'])==F(c['source_evaluation']) and margin(pt)>0
  print('PASS',c['orbit_id'],'exact quartic')
 verify_h21_factorization()
 verify_sunlet_compression('L20-02',3)
 subset=[5,15,17,20,27,39,40,45,51,57,60]
 verify_sunlet_compression('L21a-02',3,subset,10);verify_sunlet_compression('L21b-02',3,subset,10)
 verify_sunlet_compression('L23-01',2)
 rcert=json.load(open(ROOT/'software/certificates/k3p_directed_rank_obstructions.json'))
 for c in rcert['records']:
  r=R[c['orbit_id']];sd=k.model_descriptor_fast2(S[r['source_index']].graph);td=k.model_descriptor_fast2(k.relabel_record(T[r['target_index']],tuple(r['representative_permutation'])).graph);sp=point(r,'source');tp=point(r,'target')
  verify_rank_minor(sd,sp,c['source_rank_certificate']);verify_rank_minor(td,tp,c['target_rank_certificate']);assert c['source_rank_certificate']['rank']>c['target_dimension_upper_bound']==c['target_rank_certificate']['rank'];assert margin(sp)>0 and margin(tp)>0
  print('PASS',c['orbit_id'],'directed rank obstruction')
 covered={x['orbit_id'] for x in hcert['records']}|{x['orbit_id'] for x in qcert['records']}|{x['orbit_id'] for x in rcert['records']}
 assert covered==set(R),(covered,set(R)-covered)
 print('K3P_FOURTEEN_ORBITS_ZERO_UNRESOLVED')
if __name__=='__main__':verify_all()
