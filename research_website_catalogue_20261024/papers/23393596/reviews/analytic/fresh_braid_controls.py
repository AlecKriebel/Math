"""Fresh Fraction-only two-dimensional Meyer calculation; no submitted imports."""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import hashlib,json,datetime,random
C=Counter()
def check(test,label):
 if not test:raise RuntimeError(label)
 C[label]+=1
def red(w):
 out=[]
 for t in w:
  if out and out[-1]==-t:out.pop()
  else:out.append(t)
 return tuple(out)
def inv(w):return tuple(-x for x in w[::-1])
def prod(*words):return red(sum((tuple(w) for w in words),()))
def comm(a,b):return prod(a,b,inv(a),inv(b))
I=(1,0,0,1);X=(1,0,-1,1);Y=(1,1,0,1)
def mul(a,b):return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
def mi(a):
 check(a[0]*a[3]-a[1]*a[2]==1,'SL2_determinant')
 return (a[3],-a[1],-a[2],a[0])
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def solve(a,e):
 det=a[0]*a[3]-a[1]*a[2]
 if det:return (F(a[3]*e[0]-a[1]*e[1],det),F(a[0]*e[1]-a[2]*e[0],det))
 for j in range(2):
  col=(a[j],a[2+j])
  if col==(0,0):continue
  l=next(i for i in range(2) if col[i]);v=F(e[l],col[l])
  if tuple(v*t for t in col)==e:return (v,F(0)) if j==0 else (F(0),v)
 return (F(0),F(0)) if e==(0,0) else None
def meyer(prefix,g):
 # E=im(prefix^-1-I) intersect im(I-g). For a generator the latter has rank1.
 a=minus(mi(prefix),I);b=minus(I,g)
 j=next(j for j in range(2) if (b[j],b[2+j])!=(0,0));e=(b[j],b[2+j])
 v1=solve(a,e)
 if v1 is None:return 0
 v2=(1,0) if j==0 else (0,1)
 q=(v1[0]+v2[0])*e[1]-(v1[1]+v2[1])*e[0]
 return int(q>0)-int(q<0)
def signature(w):
 M=I;s=0;terms=[]
 for t in w:
  G=X if abs(t)==1 else Y
  if t<0:G=mi(G)
  q=meyer(M,G);s-=q;terms.append(q);M=mul(M,G)
 return s,M,terms
def strands(w):
 labels=[0,1,2];cross=Counter()
 for t in w:
  j=abs(t)-1;a,b=labels[j:j+2];cross[tuple(sorted((a,b)))]+=1 if t>0 else -1
  labels[j:j+2]=[b,a]
 return labels,dict(cross)
def rank(mat,p=None):
 a=[[F(x) if p is None else x%p for x in row] for row in mat];r=0
 for c in range(len(a[0])):
  hit=next((i for i in range(r,len(a)) if a[i][c]),None)
  if hit is None:continue
  a[r],a[hit]=a[hit],a[r];v=a[r][c]
  a[r]=[x/v for x in a[r]] if p is None else [x*pow(v,-1,p)%p for x in a[r]]
  for i in range(len(a)):
   if i==r:continue
   v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])] if p is None else [(x-v*y)%p for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r

def run():
 x=(1,);y=(2,);a=x*2;b=y*2;h=prod(y,a,inv(y));z=prod(x,y)*3
 c=comm(a,b);d=prod(inv(a),c,a);e=prod(inv(b),c,b);u=comm(c,d);v=comm(d,e);beta=comm(u,v)
 check(len(beta)==104,'explicit_free_length')
 check(mul(mul(X,Y),X)==mul(mul(Y,X),Y),'Artin_matrix_relation')
 check(signature(prod(a,h,b))[1]==signature(z)[1],'ahb_central_matrix_identity')
 checks={}
 for name,w in [('a',a),('b',b),('h',h),('z',z),('c',c),('d',d),('e',e),('u',u),('v',v),('beta',beta)]:
  permutation,cr=strands(w);check(permutation==[0,1,2],'pure_permutation')
  if name in ['c','d','e','u','v','beta']:check(all(t==0 for t in cr.values()),'derived_linking_zero')
  sig,M,terms=signature(w);checks[name]={'word':list(w),'length':len(w),'signature':sig,'matrix':list(M),'crossing_sums':{str(k):v for k,v in cr.items()},'meyer_terms':terms}
 check(checks['beta']['signature']==-2,'explicit_signature')
 check(signature(inv(beta))[0]==2,'inverse_signature')
 check(signature(tuple(-t for t in beta))[0]==2,'mirror_signature')
 for r in range(1,13):
  for w in [a,b,h]:check(signature(w*r)[0]==1-2*r,'two_strand_family')
  check(signature(z*(2*r))[0]==-8*r,'even_central_powers')
 for word in [(),x,y,x*3,beta,(1,-2,1,2,1,-2)]:
  check(signature(prod(word,(1,2,1)))[0]==signature(prod(word,(2,1,2)))[0],'Artin_signature_relation')
  check(signature(prod(word,(1,-1)))[0]==signature(word)[0],'inverse_cancellation_signature')
  check(signature(prod(word,z*2))[0]==signature(word)[0]-8,'full_twist_shift')
 for n in range(1,9):
  g=(3,);u0=(4,);tail=()
  for j in range(n-1,-1,-1):tail=prod(tail,inv(g*j),u0,g*j)
  check(prod(g*n,tail)==prod(*(g+u0 for _ in range(n))),'normal_coset_power_identity')
 rng=random.Random(23393596)
 for _ in range(120):
  n=rng.randrange(1,6);m=rng.randrange(1,6);A=[[rng.randrange(-8,9) for j in range(m)] for i in range(n)]
  check(rank(A)>=rank(A,2),'mod2_rank_bound')
 check(checks['beta']['signature']!=0,'negative_zero_signature_control')
 check(signature(x*3)[0]==-2,'trefoil_sign_anchor')
 check(signature(tuple(-t for t in x*3))[0]==2,'negative_reversed_sign_anchor')
 result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Fresh Fraction-only rank-one Meyer forms from primary definition and exact strand tracking, before submitted helper inspection.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'assertion_counts':dict(C),'total_assertions':sum(C.values()),'explicit_example':checks['beta'],'braid_checks':checks,'limits':'Finite controls do not prove derived-series persistence or 4-dimensional solvability obstruction; these require the written argument and primary interfaces.'}
 Path(__file__).with_name('fresh_braid_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','assertions':sum(C.values()),'beta_length':len(beta),'beta_signature':checks['beta']['signature'],'beta_matrix':checks['beta']['matrix']},indent=2))
if __name__=='__main__':run()
