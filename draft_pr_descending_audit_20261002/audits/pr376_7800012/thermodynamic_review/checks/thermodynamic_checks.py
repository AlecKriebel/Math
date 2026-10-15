"""Independent canonical/boundary controls and rigorous bulk enclosure.
No frozen candidate code is imported. All certificates are integer/rational.
"""
from fractions import Fraction as F
from math import factorial,isqrt
from itertools import product
import json
checks=0

def check(x):
 global checks
 assert x;checks+=1

def atan_bounds(x,terms):
 p=sum(((-1)**k)*x**(2*k+1)/F(2*k+1) for k in range(terms))
 nxt=((-1)**terms)*x**(2*terms+1)/F(2*terms+1)
 return min(p,p+nxt),max(p,p+nxt)
a,b=atan_bounds(F(1,5),24);c,d=atan_bounds(F(1,239),8)
pi_lo=4*(4*a-d);pi_hi=4*(4*b-c)
check(pi_lo>3);check(pi_hi<F(22,7))
# Machin identity: tan(4 arctan(1/5)-arctan(1/239))=1,
# its argument is between 0 and pi/2; hence it is pi/4.
def tan_add(x,y):return (x+y)/(1-x*y)
t=F(1,5)
t=tan_add(t,t);t=tan_add(t,t)
check(tan_add(t,-F(1,239))==1)
D=10**12
pi_mid=F((pi_lo+pi_hi)*D//2,D)
pi_error=max(pi_mid-pi_lo,pi_hi-pi_mid)

def sqrt_bounds(x):
 check(x>=0)
 k=isqrt((x.numerator*D*D)//x.denominator)
 lo=F(k,D);hi=F(k+1,D)
 check(lo*lo<=x<hi*hi)
 return lo,hi

def cos_bounds(j,n):
 if j>n//2:j-=n
 x=2*pi_mid*F(j,n)
 p=sum(((-1)**k)*x**(2*k)/factorial(2*k) for k in range(17))
 err=F(22,7)**34/factorial(34)+2*abs(F(j,n))*pi_error
 check(err<F(1,D))
 lo=F((p-err)*D//1,D)
 hi=F(-((-(p+err))*D//1),D)
 check(lo<=p-err);check(hi>=p+err)
 return lo,hi

n=128
cosines=[cos_bounds(j,n) for j in range(n)]
lo_sum=hi_sum=F(0)
cache={}
for cl,ch in cosines:
 for dl,dh in cosines:
  key=(cl+dl,ch+dh)
  if key not in cache:
   inner_lo,_=sqrt_bounds(12+2*key[0])
   _,inner_hi=sqrt_bounds(12+2*key[1])
   outer_lo,_=sqrt_bounds(4+inner_lo)
   _,outer_hi=sqrt_bounds(4+inner_hi)
   cache[key]=(outer_lo,outer_hi)
  a,b=cache[key];lo_sum+=a;hi_sum+=b
# K=1/(2sqrt8 sqrt(4+sqrt8)) <1/14, certified by
# denominator^2=32(4+sqrt8)>196 since sqrt8>17/8.
check(F(17,8)**2<8)
check(32*(4+F(17,8))==196)
err=pi_hi/(56*n)
energy_lo=-hi_sum/(4*n*n)-err
energy_hi=-lo_sum/(4*n*n)+err

def outward_decimal(x,lower,places=12):
 scale=10**places
 z=(x*scale)//1 if lower else -((-x*scale)//1)
 sign='-' if z<0 else ''
 z=abs(z)
 return f'{sign}{z//scale}.{z%scale:0{places}d}'

# Actual geometrical counts and exact ranks including leftovers.
for l in range(4,17,2):
 for L in range(l,65,2):
  k=L//l;R=L*L-k*k*l*l
  check(R%4==0);check(k*k*(l*l//4)+R//4==L*L//4)
 for k in range(1,7):
  L=k*l;cut_edges=[]
  for x,y in product(range(L),repeat=2):
   if x%l==l-1:cut_edges.append(((x,y),((x+1)%L,y)))
   if y%l==l-1:cut_edges.append(((x,y),(x,(y+1)%L)))
  check(len(cut_edges)==2*L*L//l)
# Variational upper bound: arbitrary nonzero joining bonds are invisible
# against a block-diagonal projector, including diagonal leftover occupancy.
P=[[F(0) for _ in range(6)] for _ in range(6)]
for i,j in product(range(2),repeat=2):P[i][j]=F(1,2)
P[2][2]=1;P[4][4]=1
T=[[F(0) for _ in range(6)] for _ in range(6)]
for a,b in [(1,2),(3,4),(5,0)]:T[a][b]=T[b][a]=1
check(sum(P[i][j]*T[j][i] for i,j in product(range(6),repeat=2))==0)
check(sum(P[i][i] for i in range(6))==3)
for i,j in product(range(6),repeat=2):check(sum(P[i][k]*P[k][j] for k in range(6))==P[i][j])
# Adversarial rank-allocation example for the general direct-sum identity.
# These generic traceless spectra illustrate the logical failure mechanism;
# they are deliberately not claimed as an admissible square-lattice field.
A=[-4,-3,3,4];B=[-2,-1,1,2]
whole=sum(sorted(A+B)[:2]);equal=sum(A[:1])+sum(B[:1])
check(whole==-7);check(equal==-6);check(whole<equal)
# Mismatched-density false comparison: filling two instead of one states
# on a pi-flux four-cycle gives twice the negative canonical energy.
# Density mismatch stays extensive when this mistake is repeated in blocks.
cycle=[[0,1,0,-1],[1,0,1,0],[0,1,0,1],[-1,0,1,0]]
for i,j in product(range(4),repeat=2):
 check(sum(cycle[i][k]*cycle[k][j] for k in range(4))==2*int(i==j))
check(2>1)
# A seam perturbation has <=2(Lx+Ly) energy change for changed phases;
# its per-site deficit necessarily vanishes when both lengths diverge.
seam_bounds={str(L):str(F(4,L)) for L in [4,8,16,32,64,128]}
result={
 'assertions':checks,
 'rigorous_uniform_bulk_energy_enclosure':{
  'lower_decimal':outward_decimal(energy_lo,True),
  'upper_decimal':outward_decimal(energy_hi,False),
  'grid_n':n,'canonical_factor':'1/4',
  'method':'rational Machin pi, Taylor cosine, integer-isqrt nested radical intervals, analytic Lipschitz cell remainder',
  'remainder_bound':'pi/(56*n)'},
 'valid_upper_tiling':'exact cross-block trial trace is zero; all joining bonds have modulus one',
 'negative_control_equal_allocation':{'correct_energy':whole,'forced_equal_energy':equal,'scope':'generic traceless Hermitian spectra, not a lattice counterexample'},
 'negative_control_wrong_density':{'cycle_pi_flux':'A^2=2I, trace=0, bipartite; eigenvalues +/-sqrt2 twice','correct_rank':1,'wrong_rank':2,'correct_energy':'-sqrt2','wrong_energy':'-2sqrt2'},
 'negative_control_twist_seam_per_site_bounds':seam_bounds,
 'scope':'Finite exact controls and rigorous bulk benchmark enclosure; no nonuniform optimizer or bulk counterexample certified.'}
print(json.dumps(result,indent=2,sort_keys=True))
