#!/usr/bin/env python3
"""Fresh controls: determinant subset DP, SymPy quotient reductions, full modular diagnostics.
No submitted-code imports. Exact identities use explicit non-removable checks.
"""
import itertools,json,math,cmath,random
from pathlib import Path
from collections import Counter
from fractions import Fraction
import sympy as sp
import numpy as np
checks=Counter()
def require(p,name):
 if not p:raise RuntimeError(name)
 checks[name]+=1
x=sp.Symbol('x');phi=sp.Poly(sp.cyclotomic_poly(100,x),x,domain=sp.ZZ)
require(phi.as_expr()==x**40-x**30+x**20-x**10+1,'Phi100_independent_SymPy')
require(sp.totient(100)==40 and phi.is_irreducible,'field_degree_irreducibility')
rem=[]
for j in range(100):
 p=sp.rem(sp.Poly(x**j,x),phi);rem.append(tuple(int(p.nth(k)) for k in range(40)))
zero=(0,)*40;one=rem[0]
def add(a,b):return tuple(u+v for u,v in zip(a,b))
def sc(c,a):return tuple(c*u for u in a)
def shift(a,j):
 # Reduce high exponents by independently generated SymPy monomial remainders.
 z=[0]*40
 for k,c in enumerate(a):
  if c:
   for l,d in enumerate(rem[(k+j)%100]):
    if d:z[l]+=c*d
 return tuple(z)
def mul(a,b):
 z=zero
 for j,c in enumerate(b):
  if c:z=add(z,sc(c,shift(a,j)))
 return z
def conj(a):
 z=zero
 for j,c in enumerate(a):
  if c:z=add(z,sc(c,rem[-j%100]))
 return z
def from_poly(p):return tuple(int(p.nth(j)) for j in range(40))
def to_poly(a):return sp.Poly(sum(c*x**i for i,c in enumerate(a)),x,domain=sp.ZZ)
require(rem[50]==sc(-1,one),'X50_is_minus_one')
require(from_poly(sp.rem(sp.Poly(x**100,x),phi))==one,'X100_is_one')
rng=random.Random(10400120)
for _ in range(30):
 a=tuple(rng.randrange(-3,4) if rng.randrange(6)==0 else 0 for i in range(40));b=tuple(rng.randrange(-3,4) if rng.randrange(6)==0 else 0 for i in range(40))
 require(mul(a,b)==from_poly(sp.rem(to_poly(a)*to_poly(b),phi)),'multiplication_SymPy_oracle')
 require(conj(conj(a))==a and conj(mul(a,b))==mul(conj(a),conj(b)),'conjugation_involution_homomorphism')
# Labels from strictly decreasing residues, independent of product filtering.
labels=[];Y=[]
for c in itertools.combinations(range(1,10),4):
 r=tuple(sorted(c,reverse=True))+(0,);lab=tuple(r[i]-r[i+1]-1 for i in range(4))
 labels.append(lab);Y.append(tuple(5*v-sum(r) for v in r))
order=sorted(range(126),key=lambda i:labels[i]);labels=[labels[i] for i in order];Y=[Y[i] for i in order]
product_labels={q for q in itertools.product(range(6),repeat=4) if sum(q)<=5}
require(set(labels)==product_labels and len(labels)==len(set(labels))==math.comb(9,4)==126,'weight_completeness_exact')
require(labels[0]==(0,0,0,0) and Y[0]==(10,5,0,-5,-10),'vacuum_coordinate_scale')
T=[]
for y in Y:
 require(sum(y)==0 and len({v%5 for v in y})==1,'centered_coordinate_residue')
 t=Fraction(sum(v*v for v in y)-250,5);require(t.denominator==1,'T_exponent_exact_division');T.append(int(t)%100)
perms=list(itertools.permutations(range(5)));signs=[]
for p in perms:
 inv=sum(p[i]>p[j] for i in range(5) for j in range(i+1,5));seen=set();cycles=0
 for i in range(5):
  if i not in seen:
   cycles+=1;j=i
   while j not in seen:seen.add(j);j=p[j]
 sign=(-1)**inv;require(sign==(-1)**(5-cycles),'permutation_sign_cycle_control');signs.append(sign)
require(len(set(perms))==math.factorial(5)==120 and Counter(signs)=={1:60,-1:60},'Weyl_completeness_even_odd')
def exponents(a,b):
 out=[]
 for ai in a:
  row=[]
  for bj in b:
   # Individual phases can have denominator5. Work in zeta500 for matrix
   # entries, but every determinant permutation total is divisible by5.
   row.append(-2*ai*bj)
  out.append(row)
 return out
def determinant(a,b):
 # Polynomial determinant DP in group algebra of cyclic group500.
 # Unlike author, no Weyl permutations and no asserted per-dot floor division.
 phase=exponents(a,b);states={0:{0:1}}
 for mask in range(1,32):
  row=mask.bit_count()-1 if hasattr(mask,'bit_count') else bin(mask).count('1')-1
  out={};pos=0
  for col in range(5):
   if mask&(1<<col):
    sign=(-1)**(row+pos);pos+=1
    for e,v in states[mask^(1<<col)].items():
     f=(e+phase[row][col])%500;out[f]=out.get(f,0)+sign*v
  states[mask]={e:v for e,v in out.items() if v}
 result=zero
 for e,v in states[31].items():
  require(e%5==0,'determinant_total_exponent_divisibility')
  result=add(result,sc(v,rem[e//5]))
 return result
def weyl(a,b):
 result=zero
 for p,sgn in zip(perms,signs):
  dot=sum(a[i]*b[p[i]] for i in range(5));require(dot%5==0,'Weyl_dot_exact_division')
  result=add(result,sc(sgn,rem[(-2*(dot//5))%100]))
 return result
D=[[determinant(a,b) for b in Y] for a in Y]
require(all(D[i][j]==D[j][i] for i in range(126) for j in range(126)),'full_exact_determinant_symmetry')
for i,j in [(0,0),(0,125),(1,2),(2,3),(37,80),(79,49),(125,125),(58,14)]:
 require(D[i][j]==weyl(Y[i],Y[j]),'determinant_DP_vs_120_Weyl_terms')
 require(determinant(tuple(reversed(Y[i])),Y[j])==D[i][j],'five_row_reversal_even_sign')
 swapped=list(Y[i]);swapped[0],swapped[1]=swapped[1],swapped[0]
 require(determinant(tuple(swapped),Y[j])==sc(-1,D[i][j]),'row_swap_determinant_sign')
 require(determinant(tuple(-v for v in Y[i]),Y[j])==conj(D[i][j]),'determinant_conjugation')
A=zero;B=zero
for i in range(126):
 A=add(A,shift(mul(D[0][i],D[i][0]),5*T[i]))
 inner=zero
 for j in range(126):inner=add(inner,shift(mul(D[i][j],D[j][0]),2*T[j]))
 B=add(B,shift(mul(D[0][i],inner),3*T[i]))
DD=mul(D[0][0],conj(D[0][0]));AA=mul(A,conj(A));BB=mul(B,conj(B));u=add(rem[20],sc(-1,rem[30]));sqrt5=add(one,sc(2,u))
require(add(mul(u,u),u)==one and mul(sqrt5,sqrt5)==sc(5,one),'radical_algebraic_relation')
values=[add(sc(3475,one),sc(1550,sqrt5)),add(sc(4025,one),sc(1800,sqrt5))]
require(mul(sc(50000,DD),values[0])==AA,'first_squared_magnitude_cross_product')
require(mul(sc(50000**2,DD),values[1])==BB,'second_squared_magnitude_cross_product')
require(sc(50000,AA)!=BB and AA!=zero and BB!=zero,'nonzero_unequal_numerators')
inverse=sp.invert(to_poly(D[0][0]),phi);require(sp.rem(to_poly(D[0][0])*inverse,phi)==sp.Poly(1,x),'vacuum_exact_inverse')
fresh={'S00':D[0][0],'A':A,'B':B,'DD':DD,'AA':AA,'BB':BB,'difference':add(sc(50000,AA),sc(-1,BB))}
historical=json.loads((Path(__file__).parent/'private_original/verification.json').read_text())
require(all(list(v)==historical[k] for k,v in fresh.items()),'fresh_DP_complete_certificate_equal_original')
# Positive root embedding: u=2cos(2pi/5) lies (0,1) by 0<2pi/5<pi/2.
# Its equation u²+u=1 then selects (-1+sqrt5)/2. Rational isolating
# bounds sqrt5 in (2236/1000,2237/1000) prove 0<u<5/8 and positivity.
lo=Fraction(2236,1000);hi=Fraction(2237,1000)
require(lo*lo<5<hi*hi and 0<(lo-1)/2<(hi-1)/2<Fraction(5,8),'positive_embedding_rational_interval')
require(125-200*(hi-1)/2>0 and 550+250*lo>0,'positive_denominator_and_difference')
# Exact SL2 surgery matrices and linking forms of chains.
S2=sp.Matrix([[0,-1],[1,0]]);T2=sp.Matrix([[1,1],[0,1]])
m1=S2*T2**5*S2;m2=S2*T2**3*S2*T2**2*S2;rev=S2*T2**2*S2*T2**3*S2
require(m1==sp.Matrix([[-1,0],[5,-1]]) and m2==sp.Matrix([[-2,1],[5,-3]]),'SL2_actual_surgery_words')
require(rev==sp.Matrix([[-3,1],[5,-2]]),'SL2_reversed_chain_q_inverse')
link=sp.Matrix([[3,1],[1,2]]);require(link.det()==5 and link.inv()[0,0]==sp.Rational(2,5),'chain_pq_and_linking_form')
require(S2**2==-sp.eye(2) and (S2*T2)**3==-sp.eye(2),'SL2_generator_relations')
# Independent floating diagnostics: direct 5x5 complex determinants, not
# field vectors, then unitary/modular identities on all126 states.
Ynp=np.array(Y,dtype=float);Sn=np.empty((126,126),dtype=complex)
for i in range(126):
 for j in range(126):Sn[i,j]=-np.linalg.det(np.exp(-2j*np.pi*np.outer(Ynp[i]/5,Ynp[j]/5)/10))/(100*math.sqrt(5))
C=np.zeros((126,126))
for i,lab in enumerate(labels):C[i,labels.index(tuple(reversed(lab)))]=1
h=np.array(T)*2*np.pi/100;Trel=np.exp(1j*h)
# c=k dim(g)/(k+hdual)=12, hence vacuum T phase exp(-2pi*i*c/24)=-1.
Tphys=-Trel;ST=Sn*Tphys[None,:]
res={'unitarity_max':float(np.max(np.abs(Sn@Sn.conj().T-np.eye(126)))),'S_squared_C_max':float(np.max(np.abs(Sn@Sn-C))),'ST_cubed_C_max':float(np.max(np.abs(ST@ST@ST-C))),'S_symmetry_max':float(np.max(np.abs(Sn-Sn.T)))}
tau1=(Sn@np.diag(Trel**5)@Sn)[0,0]/Sn[0,0];tau2=(Sn@np.diag(Trel**3)@Sn@np.diag(Trel**2)@Sn)[0,0]/Sn[0,0]
res['normalized_squared_magnitudes']=[abs(tau1)**2,abs(tau2)**2]
require(all(v<2e-12 for k,v in res.items() if k!='normalized_squared_magnitudes'),'floating_modular_diagnostics_tolerance')
require(all(abs(res['normalized_squared_magnitudes'][i]-(a+b*math.sqrt(5)))<1e-7 for i,(a,b) in enumerate([(3475,1550),(4025,1800)])),'floating_surgery_diagnostics_tolerance')
# Exact small SU(2) level1 known semion control. S=Hadamard/sqrt2,
# relative T=diag(1,i); normalized p surgery is (1+i^p)/sqrt2.
H=sp.Matrix([[1,1],[1,-1]])/sp.sqrt(2);Ts=sp.diag(1,sp.I);Cp=sp.eye(2)
require(sp.simplify(H*H)==Cp,'SU2_level1_S_squared')
phys=Ts*sp.exp(-sp.I*sp.pi/12)
require(sp.simplify((H*phys)**3)==Cp,'SU2_level1_physical_modular_relation')
for p in range(1,9):
 z=sp.simplify((H*Ts**p*H)[0,0]/H[0,0]);require(sp.simplify(z-(1+sp.I**p)/sp.sqrt(2))==0,'SU2_level1_exact_Gauss_control')
result={'status':'PASS','method':'Independent subset determinant DP in Z[C500], independently generated SymPy Phi100 reductions, exact integer certificate; full modular floating diagnostics and exact SU2 level1 controls.','explicit_checks':dict(checks),'exact_certificate':{k:list(v) for k,v in fresh.items()},'S00_inverse':str(inverse.as_expr()),'SL2_words':{'L5_1':str(m1),'L5_2':str(m2),'reversed':str(rev)},'positive_embedding_sqrt5_interval':[str(lo),str(hi)],'floating_diagnostics':res,'exact_vs_diagnostic':'All certificate, sign/divisibility, reduction, cross-product, inverse, embedding, SL2 and SU2 identities are exact. Full126-state unitarity and modular relations are floating diagnostic controls only.'}
print(json.dumps(result,indent=2,sort_keys=True))
