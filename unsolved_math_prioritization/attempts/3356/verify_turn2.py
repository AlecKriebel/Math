from math import gcd
import json
q=5;m=42;r=16*q**m+1;N=r-1;D=N//5
assert r==3637978807091712951660156250001
assert pow(6,N,r)==1
assert pow(6,N//2,r)==r-1
assert pow(6,N//5,r)==505004010963654974860773778891
assert gcd(pow(6,N//2,r)-1,r)==gcd(pow(6,N//5,r)-1,r)==1
assert pow(3,D,r)==1
assert pow(3,D//2,r)==r-1
assert pow(3,D//5,r)==505004010963654974860773778891!=1
controls=0
for q in [5,7,11,13,17,19,23,29,31]:
 M=96*q**5;a=16*q**4+1
 assert gcd(a,M)==1
 # All residue-class representatives have exactly the target valuations.
 for k in range(101):
  n=a+M*k
  assert n%12==5 and (n-1)//16%2==1
  assert (n-1)//q**4%q==16%q
  controls+=1
 c=pow(q,-1,16)
 while c%q==0:c+=16
 assert q*c%16==1 and gcd(q*c,16*q**4)==q
 for chi in range(16):
  assert (chi*q*c)%16==chi
  controls+=1
print(json.dumps({'status':'PASS_EXACT_NEIGHBOR_AND_ALGEBRA_CONTROLS','neighbor_prime':r,'primitive_certificate_base':6,'order_of_3':D,'index_of_3':5,'residue_and_character_controls':controls,'qualification':'Not a counterexample to exponent4. Finite controls do not prove Chebotarev.'},indent=2))
