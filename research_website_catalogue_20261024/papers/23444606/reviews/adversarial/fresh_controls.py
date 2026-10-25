"""Independent exact finite controls, written before inspecting supplied programs.
These computations do not prove any ordinal-length or proper-class theorem.
"""
from fractions import Fraction as Q
from itertools import product
from functools import cmp_to_key
from pathlib import Path
import datetime, hashlib, json, random
O=Path(__file__).resolve().parent
def comp(s,t):
 for i in range(max(len(s),len(t))):
  a=s[i] if i<len(s) else 0; b=t[i] if i<len(t) else 0
  if a!=b:return (a>b)-(a<b)
 return 0
def pref(s,t):return len(s)<len(t) and t[:len(s)]==s
def prefixes(s):return {s[:i] for i in range(len(s))}
def f(s,alpha):
 a=(-1,)*alpha
 if s==a:return ()
 if s[:alpha]==a:return (1,)+a+s[alpha+1:]
 return (1,)+s
def h(s,alpha):
 a=(-1,)*alpha
 if not s:return a
 v=s[1:]
 return a+(1,)+v[alpha:] if v[:alpha]==a else v
def words(n):return [s for k in range(n+1) for s in product((-1,1),repeat=k)]
def value(s):
 if not s:return Q(0)
 i=1
 while i<len(s) and s[i]==s[0]:i+=1
 return Q(i*s[0])+sum((Q(s[j],2**(j-i+1)) for j in range(i,len(s))),Q(0))
counts={};fail_controls={}
pool=words(8)
assert all(comp(a,b)==((value(a)>value(b))-(value(a)<value(b))) for a in pool for b in pool)
counts['independent_dyadic_order_pairs']=len(pool)**2
pair_count=0;point_count=0
for alpha in range(7):
 a=(-1,)*alpha;ray=sorted((s for s in pool if comp(s,a)>=0),key=cmp_to_key(comp))
 for s in ray:
  point_count+=1
  z=f(s,alpha);assert h(z,alpha)==s
  assert (not z) if s==a else z[0]==1
  if s!=a:assert prefixes(z)=={()}|{f(v,alpha) for v in prefixes(s) if v!=a}
 for s,t in zip(ray,ray[1:]):assert comp(f(s,alpha),f(t,alpha))<0
 for s in ray:
  for t in ray:
   pair_count+=1;fs,ft=f(s,alpha),f(t,alpha)
   if s!=a and t!=a:assert pref(s,t)==pref(fs,ft)
   if pref(fs,ft) and comp(fs,ft)>0:assert pref(s,t) and comp(s,t)>0
 for z in (s for s in pool if not s or s[0]==1):assert f(h(z,alpha),alpha)==z
counts['rotation_points']=point_count;counts['rotation_pairs']=pair_count

def initial_sets(depth):
 if depth<0:return [frozenset()]
 old=initial_sets(depth-1)
 return [frozenset()]+[frozenset({()}|{(-1,)+s for s in l}|{(1,)+s for s in r}) for l in old for r in old]
sets=initial_sets(3)
for E in sets:
 if not E:continue
 a=min(E,key=cmp_to_key(comp));assert all(x==-1 for x in a)
 image={f(s,len(a)) for s in E}
 assert all(prefixes(s)<=image for s in image)
 assert min(image,key=cmp_to_key(comp))==()
counts['all_initial_exponent_sets_depth3']=len(sets)
# Independent finite surreal addition checks the auxiliary initial-sum lemma.
table={value(s):s for s in words(10)}
sm=initial_sets(2)
for S in sm:
 for U in sm:
  vals={value(s)+value(u) for s in S for u in U}
  assert all({value(z) for z in prefixes(table[x])}<=vals for x in vals)
counts['initial_sum_pairs']=len(sm)**2

def add(A,B):
 C=dict(A)
 for k,v in B.items():C[k]=C.get(k,Q(0))+v
 return {k:v for k,v in C.items() if v}
def neg(A):return {k:-v for k,v in A.items()}
def sign(A):
 if not A:return 0
 v=A[max(A,key=cmp_to_key(comp))];return (v>0)-(v<0)
def transport(A,alpha,n):
 bottom=(-1,)*alpha
 return {f(y,alpha):r*(2**n if y==bottom else 1) for y,r in A.items()}
rng=random.Random(23444606)
for j in range(1500):
 alpha=j%5;n=(j//5)%4;bottom=(-1,)*alpha
 exps=[s for s in words(5) if comp(s,bottom)>=0]
 def sample():
  keys=rng.sample(exps,rng.randrange(1,min(9,len(exps))))
  return {y:Q(rng.choice([-3,-2,-1,1,2,3]),2**(n if y==bottom else rng.randrange(5))) for y in keys}
 A,C=sample(),sample();TA,TC=transport(A,alpha,n),transport(C,alpha,n)
 assert transport(add(A,C),alpha,n)==add(TA,TC)
 assert sign(add(A,neg(C)))==sign(add(TA,neg(TC)))
 assert all(comp(y,())>=0 for y in TA)
 assert TA.get((),Q(0)).denominator==1
 assert transport({bottom:Q(1,2**n)},alpha,n)=={():Q(1)}
 for k in range(len(A)+1):
  prefix=dict(sorted(A.items(),key=lambda p:cmp_to_key(comp)(p[0]),reverse=True)[:k])
  mapped=dict(sorted(TA.items(),key=lambda p:cmp_to_key(comp)(p[0]),reverse=True)[:k])
  assert transport(prefix,alpha,n)==mapped
counts['finite_hahn_pairs']=1500

# Formal unit options: later lower exponent dominates any possible cancellation
# at that exponent, whereas the first discrepant coefficient is at earlier mu.
unit_checks=0
for rs in product([-3,-1,1,2],repeat=5):
 for mu in range(4):
  for nu in range(mu+1,5):
   for k in range(1,6):
    center=[Q(rs[i]) if i<=mu else Q(0) for i in range(5)]
    left=center.copy();right=center.copy();left[mu]-=Q(1,2**k);right[mu]+=Q(1,2**k)
    lower=[Q(rs[i]) if i<=nu else Q(0) for i in range(5)];upper=lower.copy()
    lower[nu]-=1;upper[nu]+=1
    assert left<lower<list(map(Q,rs))<upper<right
    unit_checks+=1
counts['unit_cut_cofinality_finite_prefix_controls']=unit_checks
# Deliberately wrong alternatives must be caught; they are not manuscript defects.
fail_controls['omit_bottom_normalization']=Q(1,4).denominator!=1
fail_controls['negative_bottom_scale_reverses_order']=Q(1,4)*(-4)<0
fail_controls['simplicity_not_preserved_at_bottom']=not pref((-1,),()) and pref(f((-1,),1),f((),1))
fail_controls['dyadic_option_illegal_for_integer_coefficient']=Q(1)-Q(1,2) not in set(map(Q,range(-5,6)))
assert all(fail_controls.values())
out={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'counts':counts,'negative_controls':fail_controls,'status':'FINITE_CONTROLS_PASS','ordinal_or_class_theorem_proved_by_computation':False,'supplied_programs_read_or_run_before_this':False}
(O/'fresh-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
