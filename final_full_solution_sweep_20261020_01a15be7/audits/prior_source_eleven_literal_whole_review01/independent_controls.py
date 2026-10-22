"""Small exact falsification controls; no imported research code or services.
These finite controls supplement, and do not prove, the universal theorems.
"""
import json,math
from fractions import Fraction as F
def primes(n):return [p for p in range(2,n+1)if all(p%d for d in range(2,math.isqrt(p)+1))]
def bad_sums(a,targets):
 bad=set();n=len(a)
 for i in range(n):
  z=a[i]
  for j in range(i+1,n):
   z+=a[j]
   if z>a[-1]:break
   if z in targets:bad.add(z)
 return bad
def main():
 freud=[]
 for y in range(1,25):
  x=17*y-2
  a=list(range(2*x-2*y,2*x+2*y+1));a+=[v for v in range(3*x-3*y+1,3*x+3*y)if v%3];a+=list(range(4*x-4*y+2,4*x+4*y,2));d=set(range(4*x+4*y+2,8*x+8*y+5));a+=sorted(d)
  assert a==sorted(set(a));removed=bad_sums(a,d);f=[v for v in a if v not in removed]
  assert len(f)==76*y-7 and f[-1]==144*y-12 and len(f)-F(f[-1],2)==4*y-1
  assert not bad_sums(f,set(f));freud.append([y,len(f),f[-1],len(removed)])
 pp=primes(256);odd=pp[1:];q=math.prod(odd);phi=math.prod(p-1 for p in odd)
 assert len(odd)==53 and q>128 and 3*q<16*phi and 2**4096*32769**53<3**4096
 def U(d):return 2*(F(1,d)+F(1,3*d**3))+F(2,5*d**5*(1-F(1,d*d)))
 ss=sum((U(2*r+3)/4**r for r in range(1,7)),F(1,98304));bound=4*ss+F(2,3)*F(1123,1620)
 assert bound==F(21498408212212214497,22462131847034880000)<F(2393,2500)
 for x in range(1,101):
  t=5289;p=42*t*x+11;qv=72*t*x+13;r=28*t*x+5;s=72*t*x+19
  assert 2*p*qv-1==3*r*s
  assert all(math.gcd(a,b)==1 for i,a in enumerate([p,qv,r,s])for b in [p,qv,r,s][i+1:])
 tail=[];budget=F(0)
 for p in reversed(primes(100)):
  if budget+F(1,p)<=F(1,2):tail.append(p);budget+=F(1,p)
  else:break
 count=lambda a:sum(all(n%v for v in a)for n in range(1,101))
 assert count(tail)==62
 # Direct event mismatch already falsifies the gcd-one interpretation independently.
 assert sum(all(n%a for a in [4])for n in range(1,3))==2
 assert sum(all(math.gcd(n,a)==1 for a in [4])for n in range(1,3))==1
 return {'status':'PASS','Freud_controls_y_1_to_24':freud,'Gessel_constants_exact':True,'Blair_rational_bad_budget':str(bound),'good_parameter_margin_over_107_2500':str(F(2393,2500)-bound),'Blair_100_family_identity_and_coprimality_checks':True,'Tao_N100_exact_feasible_tail':tail,'Tao_tail_survivors':count(tail),'avoidance_is_not_gcd_one':True,'limits':'Finite controls only; no Lean/kernel/build replay, no infinite-density inference, no exact optimizer or growing-C theorem.'}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True))
