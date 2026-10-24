#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import json
from check_covers import path,rels,cover

def add(u,v):return tuple(a+b for a,b in zip(u,v))
def neg(u):return tuple(-a for a in u)
def sub(u,v):return add(u,neg(v))
def scale(k,u):return tuple(k*a for a in u)
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def perm(p,v):
 w=[0]*len(v)
 for i,j in enumerate(p):w[j]=v[i]
 return tuple(w)
def pmul(p,q):return tuple(p[q[i]] for i in range(len(p)))
def mul(x,y):
 v,p=x;w,q=y
 return add(v,perm(p,w)),pmul(p,q)
def inverse(x):
 v,p=x;q=inv(p)
 return neg(perm(q,v)),q
def power(x,k):
 one=(tuple(0 for _ in x[0]),tuple(range(len(x[0]))));out=one
 for _ in range(k):out=mul(out,x)
 return out

def check(k):
 n=3*k;ix=lambda j,i:(j%3)*k+(i%k);one=tuple(range(n));zero=(0,)*n
 P=tuple(ix(j,i+1) for j in range(3) for i in range(k));B=tuple(ix(j+1,i) for j in range(3) for i in range(k));C=list(one)
 for x,y in [(ix(0,0),ix(1,0)),(ix(1,1),ix(2,0)),(ix(2,1),ix(0,1))]:C[x],C[y]=C[y],C[x]
 C=tuple(C);T=tuple(k if i<k else 0 for i in range(n));diff=sub(perm(inv(B),T),T);assert all(x%k==0 for x in diff);A=tuple(x//k for x in diff)
 D=sub(perm(C,T),T);R=sub(D,sub(A,perm(B,A)));u=[0]*n
 for j in range(3):
  assert sum(R[j*k:(j+1)*k])==0
  for i in range(1,k):u[ix(j,i)]=u[ix(j,i-1)]-R[ix(j,i)]
 u=tuple(u);assert sub(perm(P,u),u)==R
 a=(A,P);b=(u,B);c=(zero,C);t=(T,one)
 assert mul(mul(t,a),inverse(t))==a
 assert mul(mul(t,b),inverse(t))==mul(b,power(a,k))
 w=mul(mul(mul(a,b),inverse(a)),inverse(b));assert w==(D,one)
 assert mul(mul(t,c),inverse(t))==mul(c,w)
 assert power(a,k)==(scale(k,A),one)
 assert -sum(A[:k])==k
 assert any(A)
 return {'k':k,'dimension':n,'a_power_translation_nonzero':True,'integer_relations':'pass','max_abs_b_translation':max(map(abs,u)),'integral_translation_sum_on_block0_of_a':sum(A[:k]),'P':P,'B':B,'C':C,'A':A,'T':T,'u':u}

def main():
 vals=[check(k) for k in range(2,41)]
 lifted=[]
 for cert in vals:
  k=cert['k']
  if k not in [3,5,7]:continue
  n=3*k;ps={'a':inv(cert['P']),'b':inv(cert['B']),'c':inv(cert['C']),'t':tuple(range(n))}
  wt=[x for i in range(n) for x in [cert['A'][i],cert['u'][i],0,cert['T'][i]]]
  evaluations=[]
  for i in range(n):
   for rel in rels(k):
    end,vec=path(rel,i,ps);val=sum(x*y for x,y in zip(vec,wt));assert end==i and val==0
    evaluations.append(val)
  end,vec=path('a'*k,0,ps);assert end==0
  val=sum(x*y for x,y in zip(vec,wt));assert val==-k
  lifted.append({'k':k,'degree':n,'all_lifted_relator_evaluations_zero':all(x==0 for x in evaluations),'lifted_relators_checked':len(evaluations),'a_power_at_vertex0':k,'a_power_evaluation':val,'exact_homology':cover(k,ps)})
 out={'utc':datetime.now(timezone.utc).isoformat(),'arithmetic':'integer','uniform_family_tests':[ {key:v for key,v in x.items() if key not in ['P','B','C','A','T','u']} for x in vals],'sample_full_certificates':[x for x in vals if x['k'] in [3,5,7]],'lifted_cocycle_certificates':lifted,'scope':'exact affine relations and nonzero a-power translation; theoretical proof and functional produce virtual retraction for all k>=2; no RAAG embedding claim'}
 Path(__file__).with_name('uniform_retraction_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({key:v for key,v in out.items() if key!='sample_full_certificates'},indent=2))
if __name__=='__main__':main()
