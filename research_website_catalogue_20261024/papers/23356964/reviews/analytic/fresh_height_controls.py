"""Fresh controls before submitted helpers: prefix-code Cantor lifts and infinite-height actions.
Finite checks corroborate local mechanisms; they do not prove Baire category or hyperfiniteness.
"""
from pathlib import Path
from collections import Counter,deque
from itertools import product
from math import factorial
import hashlib,json,datetime
C=Counter()
def check(ok,label):
 if not ok:raise RuntimeError(label)
 C[label]+=1

def norm(bits):return bits.rstrip('0')
def prefix(bits,n):return (bits+'0'*n)[:n]
def codes(d):return [''] if d==1 else ['1'*j+'0' for j in range(d-1)]+['1'*(d-1)]
def split(bits,d):
 for i,w in enumerate(codes(d)):
  if prefix(bits,len(w))==w:return i,norm(bits[len(w):])
 raise RuntimeError('prefix code incomplete')
def lift(x,m,d,Q):
 c,bits=x;head=prefix(bits,Q);i,tail=split(bits[Q:],d)
 return (c,norm(head+tail),c+m*i)
def unlift(y,m,d,Q):
 c,u,j=y
 check(c==j%m,'fiber_compatibility')
 return c,norm(prefix(u,Q)+codes(d)[j//m]+u[Q:])
def beta(x,k,m,d,Q):
 c,u,j=lift(x,m,d,Q);j=(j+k)%(m*d)
 return unlift((j%m,u,j),m,d,Q)

def rot(b,k):
 k%=len(b)
 return b[-k:]+b[:-k] if k else b

def T(x,k=1):b,h=x;return rot(b,k),h+k
def A(x,i=0,step=1,q=2):
 b,h=x;b=list(b);b[i%len(b)]=(b[i%len(b)]+step)%q
 return tuple(b),h

def coord(x,m,offset=0):
 b,h=x;r=(offset+h)%m
 return T(x,-r),r

def neighbors(x,m,q,offset=0):
 out={A(x,step=1,q=q),A(x,step=-1,q=q)}
 r=(offset+x[1])%m
 if r<m-1:out.add(T(x))
 if r>0:out.add(T(x,-1))
 out.discard(x)
 return out

def distances(x,m,q,offset=0):
 d={x:0};todo=deque([x])
 while todo:
  u=todo.popleft()
  for v in neighbors(u,m,q,offset):
   if v not in d:d[v]=d[u]+1;todo.append(v)
 return d

def run():
 lift_cases=[]
 words=[''.join(w) for n in range(7) for w in product('01',repeat=n)]
 for m,d,Q in product([1,2,3],[1,2,3,5],[0,2,4]):
  for c in range(m):
   for bits in words:
    x=c,norm(bits);y=lift(x,m,d,Q)
    check(unlift(y,m,d,Q)==x,'prefix_lift_inverse')
    for k in [-m*d-1,-1,0,1,m,m*d+1]:
     z=beta(x,k,m,d,Q)
     check(prefix(z[1],Q)==prefix(bits,Q) and z[0]==(c+k)%m,'finite_partition_perturbation')
     check(lift(z,m,d,Q)[2]==(y[2]+k)%(m*d),'new_residue_equivariance')
     check(beta(z,-k,m,d,Q)==x,'lift_inverse_action')
    check(beta(beta(x,1,m,d,Q),m,m,d,Q)==beta(x,m+1,m,d,Q),'lift_action_composition')
  lift_cases.append({'old_modulus':m,'extension_degree':d,'preserved_tail_bits':Q})
 # Infinite-height nonfree action: cyclic finite lamp quotient, but h remains an integer.
 slab_cases=[]
 for L,q,m in product([1,2,3,4],[2,3],[1,2,3,4,5]):
  lamps=list(product(range(q),repeat=L))
  for offset in [0,1]:
   H=-offset
   points=[(b,H+r) for b in lamps for r in range(m)]
   all_components=[];unused=set(points)
   while unused:
    x=next(iter(unused));D=distances(x,m,q,offset);unused-=set(D)
    check(len(D)==m*q**min(m,L),'nonfree_slab_component_size')
    all_components.append(len(D))
   for x in points:
    z,r=coord(x,m,offset)
    check(T(z,r)==x and (offset+z[1])%m==0,'slab_coordinate_bijection')
    z2,r2=coord(A(x,q=q),m,offset)
    check(z2==A(z,i=-r,q=q) and r2==r,'negative_lamp_index')
    for y in neighbors(x,m,q,offset):
     zy,ry=coord(y,m,offset)
     if y in [T(x),T(x,-1)]:check(zy==z and abs(ry-r)==1,'vertical_base_unchanged')
    if L<=3 and q==2:
     for y,dist in distances(x,m,q,offset).items():
      zy,ry=coord(y,m,offset);enabled={(-i)%L for i in range(m)}
      check(all(z[0][i]==zy[0][i] for i in range(L) if i not in enabled),'slab_inactive_lamps')
      wordlen=sum(min((z[0][i]-zy[0][i])%q,(zy[0][i]-z[0][i])%q) for i in enabled)
      check(wordlen<=dist,'threshold_endpoint_projection')
   slab_cases.append({'L':L,'q':q,'width':m,'offset':offset,'component_sizes':all_components})
 # Proper divisibility matters; cutting at -1 never disappears in integer-height models.
 for m in range(1,10):
  for mult in range(1,7):
   M=m*mult
   for h in range(-3*M,3*M):
    check(not(h%m<m-1) or h%M<M-1,'divisor_cut_monotonicity')
 check(2%2<1 and not(2%3<2),'nondivisor_negative_control')
 for n in range(1,11):check((-1)%factorial(n)==factorial(n)-1,'persistent_integer_cut')
 # lambda has factorial digits all one: r_n=sum_{j<n}j! mod n!.
 # r_n and n!-r_n both tend to infinity, so this is not an embedded integer.
 residues={n:sum(factorial(j) for j in range(1,n))%factorial(n) for n in range(1,11)}
 for n in range(1,10):check(residues[n+1]%factorial(n)==residues[n],'profinite_compatibility')
 admissions={}
 for h in range(-100,101):
  admissible=[n for n in range(1,11) if (residues[n]+h)%factorial(n)<factorial(n)-1]
  check(bool(admissible),'regular_translate_eventual_admission')
  first=min(admissible);admissions[str(h)]=first
  check(all(n in admissible for n in range(first,11)),'regular_edge_stays_admitted')
 # Exact exceptional-band equivalence in the infinite-height model.
 L=3;q=2;pts=[(b,h) for b in product(range(q),repeat=L) for h in range(-8,9)]
 def normal(x):return rot(x[0],-x[1])
 def related(x,y,j):
  return x==y or (abs(x[1])<=j and abs(y[1])<=j and normal(x)[min(j,L):]==normal(y)[min(j,L):])
 previous=set();band_sizes=[]
 for j in range(0,7):
  pairs={(i,k) for i,x in enumerate(pts) for k,y in enumerate(pts) if related(x,y,j)}
  check(previous<=pairs,'band_relation_nested');previous=pairs
  for i,x in enumerate(pts):
   cls={k for a,k in pairs if a==i}
   check(i in cls,'band_reflexive')
   check(all((k,i) in pairs for k in cls),'band_symmetric')
   check(all({b for a,b in pairs if a==k}==cls for k in cls),'band_transitive')
   expected=(2*j+1)*q**min(j,L) if abs(x[1])<=j else 1
   check(len(cls)==expected,'band_exact_fiber_bound')
  band_sizes.append({'stage':j,'inside_class_size':(2*j+1)*q**min(j,L)})
 check(len({T(((0,0,0),0),h) for h in range(-20,21)})==41,'uncut_pullback_growth_control')
 # A wrong sign is detected; L=3 and r=1 prevent coincident +r/-r coordinates.
 x=((0,0,0),1);z,r=coord(x,3)
 check(coord(A(x),3)[0]!=A(z,i=r),'wrong_conjugation_rejected')
 check(coord(T(((0,0,0),2)),3)[0]!=coord(((0,0,0),2),3)[0],'uncut_wrap_rejected')
 out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'assertion_counts':dict(C),'total_assertions':sum(C.values()),'cantor_lift_cases':lift_cases,'slab_cases':slab_cases,'regular_residues':residues,'regular_admission_levels':admissions,'exceptional_band_sizes':band_sizes,'method':'New exact prefix-code Cantor lifts; infinite integer-height nonfree action with finite lamp quotient; genuine noninteger profinite height sampled through its compatible factorial residues. No supplied executable/data imported.','limits':'Finite controls corroborate formulas and detect specified mutations. They do not prove the Baire-category genericity, finite Borel asymptotic dimension theorem, or universal Borel hyperfiniteness conclusion.'}
 Path(__file__).with_name('fresh_height_results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':'PASS','assertions':sum(C.values()),'families':len(C),'slab_cases':len(slab_cases),'lift_cases':len(lift_cases)}))
if __name__=='__main__':run()
