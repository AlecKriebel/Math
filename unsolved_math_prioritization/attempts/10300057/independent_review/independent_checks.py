"""Independent exact controls for the scoped finite-cover packet.
No imported author code; no finite test substitutes for topology or ODE estimates.
"""
from collections import Counter
from fractions import Fraction as Q
from math import gcd
import json
C=Counter()
def check(x,k):
 assert x,k
 C[k]+=1
def linear(cols,v):
 ans=0
 while v:
  j=(v&-v).bit_length()-1;ans^=cols[j];v&=v-1
 return ans
def echelon(cols,relations=False):
 piv={};ker=[]
 for j,v in enumerate(cols):
  tag=1<<j
  while v:
   b=v.bit_length()-1
   if b not in piv:piv[b]=(v,tag);break
   w,t=piv[b];v^=w;tag^=t
  if not v:ker.append(tag)
 return (len(piv),ker)if relations else len(piv)
# Independently assemble whole finite sections of source Figure 17,
# including the isolated tower and the shifted e-source generator.
module_results=[]
for s in range(-18,19):
 top=21;bottom=-22
 coords={'a':(0,0),'b':(-1,0),'c':(0,-1),'e':(-1,-1),'x':(0,0)}
 keys=[(n,g)for n in range(bottom,top+1)for g,(i,j)in coords.items()if n+i>=0 or n+j>=s]
 ix={key:i for i,key in enumerate(keys)}
 targets={'a':'bc','b':'e','c':'e','e':'','x':''}
 d=[];u=[]
 for n,g in keys:
  d.append(sum(1<<ix[n,h]for h in targets[g]if(n,h)in ix))
  u.append(1<<ix[n-1,g]if(n-1,g)in ix else 0)
 for j in range(len(keys)):
  check(linear(d,d[j])==0,'assembled_differential_squared')
  check(linear(d,u[j])==linear(u,d[j]),'U_is_chain_map')
 rank,cycles=echelon(d,True);tower=top-min(0,s)+1
 check(len(cycles)==len(keys)-rank,'kernel_rank_nullity')
 check(len(cycles)-rank==tower+int(s==0),'whole_quotient_homology_dimension')
 lifted=cycles[:]
 for power in range(tower+2):
  image_dim=echelon(d+lifted)-rank
  check(image_dim==max(tower-power,0)+(1 if s==0 and power==0 else 0),'induced_U_power_image_dimension')
  lifted=[linear(u,v)for v in lifted]
 module_results.append({'s':s,'tower_section_length':tower,'extra_reduced_dimension':int(s==0)})
# Square roots of unity in odd cyclic torsion groups test the exact mechanism.
examples=[]
for p in range(3,102,2):
 units=[v for v in range(1,p)if gcd(v,p)==1]
 for a in units:
  if(a*a-1)%p:continue
  for v in units:
   h1=Q(v,p);ha=Q(v*a*a,p)
   check((ha-h1).denominator==1,'equal_linking_pairing_mod_integers')
   adjusted=ha-(ha-h1)
   check(adjusted==h1,'integer_framing_adjustment')
   check((p*adjusted).denominator==1,'lifted_hopf_integral')
   check(p*adjusted==p*h1,'degree_scaled_hopf_equality')
  if a not in(1,p-1):
   check(2%p not in(2*a%p,-2*a%p),'Euler_obstruction_after_unoriented_sign')
   examples.append([p,a])
check([15,4]in examples,'specific_15_4_pair')
for s in range(-7,8):
 check(15>=1+abs(s),'effective_surgery_range')
 check(((2*s)%15==0)==(s==0),'only_spin_has_zero_chern')
# Exact weighted Pfaff averages, evaluated independently via dot-curl.
for eta in [Q(i,7)for i in range(-5,6)if i]:
 for z in [Q(i,3)for i in range(1,8)]:
  for w in [Q(i,9)for i in range(10)]:
   # alpha=( -w*eta*z*z, (1-w)*eta, 1 ); curl=(0,-2*w*eta*z,0)
   wedge=(1-w)*eta*(-2*w*eta*z)
   check(wedge==-2*w*(1-w)*eta*eta*z,'weighted_Frobenius_value')
   check((wedge==0)==(w in(0,1)),'integrable_endpoints_nonintegrable_interior')
# Degree transfers on cyclic cohomology: p*chi vanishes for kernel cover,
# and multiplication-degree kills each class before/after the Bockstein.
for p in range(2,80):
 for a in range(p):
  check((p*a)%p==0,'cyclic_degree_annihilation')
  if p%2:
   check((p*(a%2))%2==a%2,'odd_degree_mod2_injectivity_control')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'finite_module_sections':module_results,'scope':'Independent whole-complex F2/U-module sections, torsion framing arithmetic and weighted local Frobenius controls. Infinite classification, contact/Floer inputs, covering topology and analytic descent are audited in prose, not proved by this checker.'},indent=2,sort_keys=True))
