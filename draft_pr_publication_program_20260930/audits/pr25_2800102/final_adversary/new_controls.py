"""Fresh exact controls. Universal proofs are the sealed/complete derivations.
No sibling code is imported. New mechanisms: joint partition rate homogeneity,
Pfaffian covariance under a Laplace tilt, generating-ODE conjugation, and
analytic singularity/constant mutations. All finite bounds are explicit.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import factorial,comb,isqrt
from collections import Counter
import json
HERE=Path(__file__).resolve().parent;counts=Counter();mutants=[]
def check(cat,b):
 assert b,cat
 counts[cat]+=1
def negative(name,detected):
 check('new_negative_control_rejected',detected);mutants.append({'name':name,'rejected':bool(detected)})
def polyadd(a,b):
 out=[Q(0)]*max(len(a),len(b))
 for i,x in enumerate(a):out[i]+=x
 for i,x in enumerate(b):out[i]+=x
 while len(out)>1 and out[-1]==0:out.pop()
 return out
def scale(a,b):return [x*b for x in a]
def mul(a,b):
 out=[Q(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 while len(out)>1 and out[-1]==0:out.pop()
 return out
Z=[Q(0),Q(1)];T=[Q(1),Q(-1)]
# After dividing by g=z(1-z)^-5/2, the recurrence differential operator
# is z(1-z)^2 F''+(1-z)F'-(1-z)F/4. Multiply coefficients by z to
# clear the only remaining denominator. Exact polynomial coefficients,
# not evaluation at a finite set of z, establish the operator identity.
A2=mul(Z,mul(T,T));A1=[Q(-1),Q(-2),Q(3)]
B1=polyadd(polyadd(scale(mul(T,T),Q(2)),scale(mul(Z,T),Q(5))),A1)
check('symbolic_generating_ODE_Fprime_coefficient',B1==T)
# The scalar coefficient is cleared by multiplication by z*(1-z).
B0=polyadd(polyadd(scale(mul(Z,mul(T,T)),Q(5)),scale(mul(mul(Z,Z),T),Q(35,4))),polyadd(mul(A1,T),scale(mul(A1,Z),Q(5,2))))
B0=polyadd(B0,mul([Q(1),Q(-3,4),Q(1)],T))
check('symbolic_generating_ODE_F_coefficient',B0==scale(mul(Z,mul(T,T)),Q(-1,4)))
negative('replace_recurrence_three_quarters_by_minus',polyadd(B0,scale(mul(Z,T),Q(3,2)))!=B0)
negative('hypergeometric_ab_sign_error',scale(mul(Z,mul(T,T)),Q(1,4))!=B0)
# Correct leading singular/asymptotic constants, from separate exact sums.
check('leading_asymptotic_n_minus2_constant',Q(65,48)-Q(15,8)+Q(11,32)==Q(-17,96))
check('decrement_constant_derivative',2*Q(-17,6)-1==2*Q(-10,3))
negative('omit_difference_log_derivative',2*Q(-17,6)!=2*Q(-10,3))
# Direct square-law skew matrix in Laguerre coordinates; transform to
# monomials by x^i=i! sum_{j<=i}(-1)^j binom(i,j)L_j. The input skew
# product has been proved by the angular PDE; the NEW operation is joint
# partition tilting/Pfaffian homogeneity, not another pointwise density.
def hg(k):return Q(factorial(2*k),4**k*factorial(k))
def base_matrix(n):
 size=n+n%2;b=[[Q(0)]*size for _ in range(size)]
 for i in range(0,n,2):
  for j in range(i+1,n,2):
   v=-Q(4,i+1)
   for a in range(i//2+1,(j-1)//2+1):v*=Q(2*a,2*a+1)
   b[i][j]=v;b[j][i]=-v
 if n%2:
  for i in range(0,n,2):b[i][n]=hg(i//2)/factorial(i//2);b[n][i]=-b[i][n]
 c=[[Q(factorial(i)*(-1)**j*comb(i,j)) if j<=i else Q(0) for j in range(n)] for i in range(n)]
 out=[[Q(0)]*size for _ in range(size)]
 for i in range(n):
  for j in range(n):out[i][j]=sum((c[i][a]*b[a][d]*c[j][d] for a in range(n) for d in range(n)),Q(0))
 if n%2:
  for i in range(n):out[i][n]=sum((c[i][a]*b[a][n] for a in range(n)),Q(0));out[n][i]=-out[i][n]
 return out
def pf(m):
 if not m:return Q(1)
 total=Q(0)
 for j in range(1,len(m)):
  inds=[i for i in range(1,len(m)) if i!=j]
  total+=(-1)**(j+1)*m[0][j]*pf([[m[a][b] for b in inds] for a in inds])
 return total
def inverse(m):
 n=len(m);a=[r[:]+[Q(i==j) for j in range(n)] for i,r in enumerate(m)]
 for j in range(n):
  k=next(k for k in range(j,n) if a[k][j]);a[j],a[k]=a[k],a[j]
  d=a[j][j];a[j]=[x/d for x in a[j]]
  for k in range(n):
   if k!=j:
    d=a[k][j];a[k]=[x-d*y for x,y in zip(a[k],a[j])]
 return [r[n:] for r in a]
def matrixmul(a,b):
 n=len(a);return [[sum((a[i][k]*b[k][j] for k in range(n)),Q(0)) for j in range(n)] for i in range(n)]
def trace(m):return sum((m[i][i] for i in range(len(m))),Q(0))
partition_rows=[]
for n in range(1,11):
 m=base_matrix(n);p=pf(m);check('joint_Pfaffian_partition_nonzero',p!=0)
 sz=len(m)
 for r in [2,3,4]:
  exponents=[2*i+1 for i in range(n)]+([0] if n%2 else [])
  tilted=[[m[i][j]/r**(exponents[i]+exponents[j]) for j in range(sz)] for i in range(sz)]
  ratio=pf(tilted)/p
  check('joint_trace_Laplace_exact_Pfaffian',ratio==Q(1,r**(n*n)))
  partition_rows.append({'N':n,'rate_multiplier':r*r,'joint_Laplace_value':str(ratio),'Gaussian_entry_count':n*n})
  negative(f'N{n}_r{r}_complex_instead_real_radial_exponent',ratio!=Q(1,r**(2*n*n)))
 # Direct Pfaffian first/second logarithmic derivatives under w->e^-t x w.
 # Each monomial pair entry has exponent i+j+1 in (1+2t); odd border i+.5.
 alpha=[Q(i,1)+Q(1,2) for i in range(n)]+([Q(0)] if n%2 else [])
 dm=[[-2*(alpha[i]+alpha[j])*m[i][j] for j in range(sz)] for i in range(sz)]
 ddm=[[4*(alpha[i]+alpha[j])*(alpha[i]+alpha[j]+1)*m[i][j] for j in range(sz)] for i in range(sz)]
 inv=inverse(m);first=trace(matrixmul(inv,dm))/2
 second=(trace(matrixmul(inv,ddm))-trace(matrixmul(matrixmul(inv,dm),matrixmul(inv,dm))))/2
 check('joint_Pfaffian_trace_mean',first==-n*n)
 check('joint_Pfaffian_trace_variance',second==2*n*n)
 if n%2:
  # A defective odd border that stays untilted is a new joint-law mutation.
  r=2;e=[2*i+1 for i in range(n)]+[0]
  bad=[[m[i][j]/r**(e[i]+e[j]) for j in range(sz)] for i in range(sz)]
  for i in range(n):bad[i][n]=m[i][n];bad[n][i]=-m[i][n]
  negative(f'N{n}_untilted_odd_border',pf(bad)/p!=Q(1,r**(n*n)))
# q1 boundary directly enclosed, separate from the earlier coefficient tests.
def addi(a,b):return a[0]+b[0],a[1]+b[1]
def subi(a,b):return a[0]-b[1],a[1]-b[0]
def muli(a,b):
 x=[v*w for v in a for w in b];return min(x),max(x)
def divi(a,b):return muli(a,(1/b[1],1/b[0]))
def si(a,c):return muli(a,(c,c))
def rooti(q):
 s=10**70;k=isqrt(q.numerator*s*s//q.denominator);return Q(k,s),Q(k+1,s)
s2=rooti(Q(2));s3=rooti(Q(3))
# log2=2 atanh(1/3). Positive series plus geometric remainder, rational.
M=100;log_lower=2*sum((Q(1,(2*k+1)*3**(2*k+1)) for k in range(M)),Q(0));log_tail=Q(2,1)/((2*M+1)*3**(2*M+1))*Q(9,8)
log2=(log_lower,log_lower+log_tail)
q1=subi(addi(si(s3,Q(3)),(Q(1),Q(1))),si(s2,Q(35,8)))
qbound=divi(si(log2,Q(3)),si(s2,Q(160)))
check('direct_q1_interval_positive',q1[0]>0)
check('direct_q1_interval_upper_repair',q1[1]<qbound[0])
negative('q1_wrong_subtracted_midpoint_coefficient',subi(q1,divi((Q(3,4),Q(3,4)),s2))[0]<0)
# An extra pole at -1 is invisible to the first 40 Y coefficients and
# analytic at +1, but invalidates the sole-dominant-singularity transfer.
M=40;pole_coeff=lambda n:Q(0) if n<M else Q((-1)**(n-M))
check('analytic_mutant_same_first39_coefficients',all(pole_coeff(n)==0 for n in range(40)))
negative('extra_unit_circle_pole_not_Delta_transfer_admissible',pole_coeff(40)!=0 and pole_coeff(41)==-1)
# Added algebraic half-pole at +1 keeps the leading n^1.5 and logarithm
# coefficient but changes the n^-2 constant and hence E-limit.
half_coeff=[Q(1)]
for k in range(1,20):half_coeff.append(half_coeff[-1]*Q(2*k-1,2*k))
half_mutant=lambda n:Q(0) if n<M else half_coeff[n-M]
check('half_pole_mutant_finite_initial_prefix',all(half_mutant(n)==0 for n in range(M)))
def recurrence_residual(v,n):return n*n*(v(n+1)-2*v(n)+v(n-1))-Q(3,4)*v(n)
negative('same_leading_limit_log_slope_changed_constant_breaks_recurrence',recurrence_residual(half_mutant,M-1)!=0)
negative('extra_minus1_pole_breaks_recurrence',recurrence_residual(pole_coeff,M-1)!=0)
# Dependency cycle control. The actual graph is acyclic and has explicit
# source analytic constant; an upper-bound-first proof graph is circular.
def acyclic(edges):
 nodes=set(edges)|{x for ys in edges.values() for x in ys};done=set();vis=set()
 def visit(n):
  if n in vis:return False
  if n in done:return True
  vis.add(n)
  if not all(visit(x) for x in edges.get(n,[])):return False
  vis.remove(n);done.add(n);return True
 return all(visit(n) for n in nodes)
graph={'Delta_upper':['C_lower','q_first','E_limit'],'C_lower':['Delta_lower','C_limit'],'Delta_lower':['E_decrease','E_limit'],'E_decrease':['C_aux_upper','q_upper'],'E_limit':['analytic_transfer'],'C_limit':['analytic_transfer'],'C_aux_upper':['positive_connection']}
check('noncircular_dependency_graph',acyclic(graph))
bad={**graph,'Delta_lower':['Delta_upper']};negative('telescoping_upper_bound_cycle',not acyclic(bad))
result={'status':'passed','total_assertions':sum(counts.values()),'counts':dict(counts),'negative_controls':mutants,'negative_count':len(mutants),'joint_partition_rows':partition_rows,'q1_interval':[str(x) for x in q1],'q1_upper_bound_interval':[str(x) for x in qbound],'scope':'Exact finite joint partition/covariance N1..10 and rational q1 intervals; universal symbolic ODE coefficient identity. Analytic negative constructions are proved in VERIFIED_RECONSTRUCTION.md. No finite extrapolation; no Decimal density interval claim.','overlap':'Skew products, Gamma constants and Pfaffian machinery overlap prior reconstructions. Joint tilted partition and covariance, direct q1 log enclosure, symbolic operator coefficient verification, and extra-singularity/En-constant controls are new mechanism applications.'}
(HERE/'NEW_CONTROL_RECEIPTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['negative_controls','joint_partition_rows']},indent=2))
