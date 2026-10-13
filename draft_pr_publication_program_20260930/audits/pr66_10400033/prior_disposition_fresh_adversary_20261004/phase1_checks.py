from fractions import Fraction as F
from math import comb
import json
# Fiedler-Stoimenow eq. (3) printed endpoint order; over = +, under = -.
source_P=[(1,3),(4,0),(5,2)]
source_T=[(0,3),(4,1),(2,5)]
candidate_P=[(3,0),(5,1),(2,4)]
candidate_T=[(3,0),(1,4),(5,2)]
def canon(a):return min(tuple(sorted(((x+k)%6,(y+k)%6) for x,y in a)) for k in range(6))
def inside(x,t,h):return 0<(x-t)%6<(h-t)%6
def edges(a):
 out=[]
 for i,(t,h) in enumerate(a):
  for j,(u,v) in enumerate(a):
   if i<j and inside(u,t,h)!=inside(v,t,h):
    if inside(u,t,h):out.append([i,j])
    else:out.append([j,i])
 return out
assert canon(source_P)==canon(candidate_P)
assert canon(source_T)==canon(candidate_T)
assert sorted(edges(candidate_P))==[[0,1],[2,0]]
assert sorted(edges(candidate_T))==[[0,2],[1,0],[2,1]]
rows=[]
for n in range(13):
 binomial=F((comb(n,2) if n>=2 else 0)+(comb(n,3) if n>=3 else 0),4)
 exact=F(n*(n*n-1),24)
 assert binomial==exact
 row={'n':n,'binomial_div4':str(binomial),'target_floor':exact.numerator//exact.denominator}
 if n%2==0 and n>=2:
  m=n-1
  stronger=F(m*(m*m-1),24)
  candidate_even=F(n*(n*n-4),24)
  assert stronger<=exact
  assert stronger<=candidate_even
  assert candidate_even.denominator==1
  row.update({'page8_prior_max':str(stronger),'candidate_even':str(candidate_even),'gap':str(candidate_even-stronger)})
 rows.append(row)
print(json.dumps({'scope':'finite transcription and arithmetic checks only; universal proof is the algebra in FIRST_CONCLUSION.md','pattern_canonical_matches':True,'candidate_P_edges':edges(candidate_P),'candidate_T_edges':edges(candidate_T),'small_n_rows':rows},indent=2))
