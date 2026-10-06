#!/usr/bin/env python3
"""Source-derived floating-point diagnostics, not proof of category existence or exact equalities."""
from pathlib import Path
from itertools import product
import cmath,math,json,sys
labels=[a for a in product(range(6),repeat=4) if sum(a)<=5]
x=[]
for a in labels:
 ell=[sum(a[i:])+4-i for i in range(5)];average=sum(ell)/5
 x.append(tuple(t-average for t in ell))
def determinant(m):
 m=[row[:] for row in m];out=1+0j
 for i in range(5):
  j=max(range(i,5),key=lambda j:abs(m[j][i]))
  if abs(m[j][i])<1e-14:return 0j
  if i!=j:m[i],m[j]=m[j],m[i];out=-out
  piv=m[i][i];out*=piv
  for j in range(i+1,5):
   q=m[j][i]/piv
   for k in range(i+1,5):m[j][k]-=q*m[i][k]
 return out
S=[[-determinant([[cmath.exp(-2j*math.pi*u*v/10) for v in y] for u in xx])/(100*math.sqrt(5)) for y in x] for xx in x]
tw=[cmath.exp(1j*math.pi*(sum(v*v for v in xx)-10)/10) for xx in x]
Tlin=[-v for v in tw]
n=len(labels)
def matrix_product(a,b):
 bt=list(zip(*b));return [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in a]
adj=[[S[j][i].conjugate() for j in range(n)] for i in range(n)]
unit=matrix_product(S,adj);S2=matrix_product(S,S)
ST=[[S[i][j]*Tlin[j] for j in range(n)] for i in range(n)]
ST3=matrix_product(matrix_product(ST,ST),ST)
conj_index=[labels.index(tuple(reversed(a))) for a in labels]
s00_expected=math.prod((2*math.sin(math.pi*j/10))**(5-j) for j in range(1,5))/(100*math.sqrt(5))
A=sum(S[0][i]*tw[i]**5*S[i][0] for i in range(n))
B=sum(S[0][i]*tw[i]**3*S[i][j]*tw[j]**2*S[j][0] for i in range(n) for j in range(n))
S3=sum(S[0][i]*tw[i]*S[i][0] for i in range(n))
S1S2=sum(S[0][i]*S[i][0] for i in range(n))
count=[sum(sum((j+1)*a[j] for j in range(4))%5==c for a in labels) for c in range(5)]
result={'method':'all 126 full-weight labels; direct determinant S from HT Eq12; floating-point diagnostic only','python':sys.version,'label_count':n,'center_charge_label_counts':count,'S00':{'real':S[0][0].real,'imag':S[0][0].imag,'sine_product':s00_expected},'min_dimension_real':min((v/S[0][0]).real for v in S[0]),'max_dimension_imag':max(abs((v/S[0][0]).imag) for v in S[0]),'symmetry_max_residual':max(abs(S[i][j]-S[j][i]) for i in range(n) for j in range(n)),'unitarity_max_residual':max(abs(unit[i][j]-(i==j)) for i in range(n) for j in range(n)),'S_squared_charge_conjugation_max_residual':max(abs(S2[i][j]-(j==conj_index[i])) for i in range(n) for j in range(n)),'linear_ST_cubed_charge_conjugation_max_residual':max(abs(ST3[i][j]-(j==conj_index[i])) for i in range(n) for j in range(n)),'twist_modulus_max_residual':max(abs(abs(v)-1) for v in tw),'surgery_words_normalized_abs_squared':[abs(A/S[0][0])**2,abs(B/S[0][0])**2],'S3_normalized_abs':abs(S3/S[0][0]),'S1xS2_normalized_abs':abs(S1S2/S[0][0]),'D':1/s00_expected,'signature_phases':['(-1)^1','(-1)^2'],'interpretation':'Diagnostics agree with cited construction; they do not substitute for the modular-category theorem or exact cyclotomic proof.'}
assert result['unitarity_max_residual']<1e-11
assert result['S_squared_charge_conjugation_max_residual']<1e-11
assert result['linear_ST_cubed_charge_conjugation_max_residual']<1e-11
assert max(abs(result['surgery_words_normalized_abs_squared'][i]-v) for i,v in enumerate([3475+1550*math.sqrt(5),4025+1800*math.sqrt(5)]))<1e-7
Path('computation/independent_modular_diagnostic.result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
