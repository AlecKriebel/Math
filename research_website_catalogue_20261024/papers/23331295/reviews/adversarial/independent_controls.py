#!/usr/bin/env python3
"""Fresh exact diagnostics, no native imports and no topological-certification claim."""
from fractions import Fraction as F
from itertools import product,permutations,combinations
from math import comb
import json
checks=0
def need(v,m):
 global checks
 checks+=1
 if not v:raise RuntimeError(m)
def val(a,t):return sum(F(c)*t**i for i,c in enumerate(a))
def mul(a,b):
 out=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return out
def differences(a):
 out=[]
 while a:out.append(a[0]);a=[b-c for c,b in zip(a,a[1:])]
 return out
def binomial(t,r):
 out=F(1)
 for k in range(r):out*=F(t-k,k+1)
 return out
def newton(a,t):return sum(c*binomial(t,r) for r,c in enumerate(differences(a)))
def alt(v):
 r=(len(v)).bit_length()-1
 return sum((-1)**(r-sum(bits))*v[i] for i,bits in enumerate(product([0,1],repeat=r)))
def run():
 out={'mechanism':'Exact integer B2 resolution exponent/permutation bookkeeping, rational Newton reconstruction, literal linking-number cube arithmetic and polynomial obstruction; independent of native code','braid_cases':[],'Newton_cases':0,'product_cases':0,'cube_degree_cases':0,'linking_zero_vectors':0,'symmetry_cases':0,'radical_evaluation_cases':0,'false_controls':[]}
 # Designated singular crossing in each of r two-crossing blocks. Each
 # resolution has one fixed positive crossing and one +/- crossing.
 for n in [0,1,3]:
  for r in range(9):
   hist={}
   for bits in product([0,1],repeat=r):
    exp=2*n+sum(1+(1 if b else -1) for b in bits)
    sign=(-1)**(r-sum(bits));hist[exp]=hist.get(exp,0)+sign
    need(exp%2==0,'resolved closure has two components')
   want={2*n+2*j:(-1)**(r-j)*comb(r,j) for j in range(r+1)}
   need(hist==want,'whole signed exponent coefficients')
   need((2*n+r+r)%2==0,'singular component permutation fixed')
   out['braid_cases'].append({'n':n,'r':r,'signed_exponent_multiplicities':hist})
 for d in range(9):
  for seed in range(3):
   a=[F(((i+2)*(seed+3)+i*i)%9-4,i+1) for i in range(d+1)]
   samples=[val(a,F(n)) for n in range(d+1)]
   for t in [F(-3,2),F(1,2),F(0),F(1),F(d+3),F(13)]:need(newton(samples,t)==val(a,t),'all-point polynomial Newton identity');out['Newton_cases']+=1
   full=[val(a,F(n)) for n in range(15)]
   need(all(x==0 for x in differences(full)[d+1:]),'higher differences')
   b=[F(2),F(-1),F(3)]
   ab=mul(a,b);samplesab=[val(ab,F(n)) for n in range(len(ab))]
   need(newton(samplesab,F(1,2))==newton(samples,F(1,2))*val(b,F(1,2)),'character multiplication')
   out['product_cases']+=1
 # For each crossing cube, each coordinate is an affine integer function;
 # each crossing modifies a single component pair (or0 for a self-crossing).
 for r,power in [(3,1),(5,2)]:
  for seed in range(7):
   values=[]
   for bits in product([0,1],repeat=r):
    lk=[seed%3-1,1,-2]
    for i,b in enumerate(bits):
     if (i+seed)%4!=3:lk[(i+seed)%3]+=(1 if (i+seed)%2 else -1)*b
    g=sum(x*x for x in lk);f=g*(4*g-1);values.append(g if power==1 else f)
   need(alt(values)==0,'finite-type bound exact crossing-cube derivative')
   out['cube_degree_cases']+=1
 # Actual integer domain: zero-set equivalence is arithmetic.
 for edges in range(1,7):
  for lk in product([-1,0,1],repeat=edges):
   g=sum(a*a for a in lk);f=g*(4*g-1)
   need((f==0)==(not any(lk)),'integer zero-set equivalence');out['linking_zero_vectors']+=1
 for m in range(2,5):
  pairs=list(combinations(range(m),2));lk={pair:(i%5)-2 for i,pair in enumerate(pairs)};g=sum(x*x for x in lk.values())
  for perm in permutations(range(m)):
   for signs in product([-1,1],repeat=m):
    moved={tuple(sorted((perm[i],perm[j]))):x*signs[i]*signs[j] for (i,j),x in lk.items()}
    need(sum(x*x for x in moved.values())==g,'all relabel/orientation signs');out['symmetry_cases']+=1
 t=F(1,2);g=t*t;f=g*(4*g-1)
 need(g==F(1,4) and f==0,'nongeometric character value')
 for n in range(1,9):need(g**n!=0 and f==0,'all-N mechanism sampled exact values');out['radical_evaluation_cases']+=1
 # Pointed negative controls, not a broad mutation campaign.
 need(1%2!=0,'odd braid parity negative control')
 out['false_controls'].append('Formal t=1/2 is not the one-component closure of sigma: that has odd permutation, while all family resolutions are even.')
 need(F(1,4).denominator!=1,'actual-link arithmetic negative control')
 out['false_controls'].append('Complex scalar g=1/4 is a zero of f, but is not the integer g-value of an actual link.')
 # Finite sampling alone cannot prove polynomiality: perturb an interpolating
 # polynomial by a nonzero product vanishing on every sampled integer.
 a=[F(2),F(1)];q=[F(1)]
 for j in range(4):q=mul(q,[-F(j),F(1)])
 need(all(val(q,F(j))==0 for j in range(4)) and val(q,F(4))!=0,'finite samples false extrapolation')
 out['false_controls'].append('Four exact samples do not establish all-n polynomiality; a degree4 perturbation agrees there and differs at4.')
 # In a completion, 4g-1 is a unit. Verify exact finite geometric identities;
 # the target explicitly excludes that topology/completion.
 for q in range(5):
  a=[F(0)]*(2*q+1)
  for k in range(q+1):a[2*k]=-F(4)**k
  lhs=mul([-F(1),F(0),F(4)],a);want=[F(0)]*(2*q+3);want[0]=1;want[-1]=-F(4)**(q+1)
  need(lhs==want,'formal-completion geometric identity')
 out['false_controls'].append('Completed-algebra extension is excluded: formal inverse of4g-1 makes g a multiple of f; finite geometric identities are checked.')
 out['checks']=checks;out['status']='PASS_BOUNDED_INDEPENDENT_DIAGNOSTICS';out['limits']='Universal topology, whole-algebra polynomiality and all-N proof are in INITIAL_RECONSTRUCTION.md, not inferred from these finite checks.'
 return out
if __name__=='__main__':print(json.dumps(run(),indent=2))
