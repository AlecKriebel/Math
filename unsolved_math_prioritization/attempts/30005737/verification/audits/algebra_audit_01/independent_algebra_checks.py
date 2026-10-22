"""Exact finite boundary diagnostics; no external packages."""
from fractions import Fraction as F
import json
def zero(n):return (0,)*n
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(c,a):return tuple(c*x for x in a)
def basis(n):return [tuple(int(i==j) for i in range(n)) for j in range(n)]
def law(n,entries):
 t={}
 for i,j,v in entries:t[i,j]=tuple(v);t[j,i]=neg(v)
 def b(x,y):
  v=zero(n)
  for i in range(n):
   for j in range(n):
    if x[i] and y[j]:v=add(v,scale(x[i]*y[j],t.get((i,j),zero(n))))
  return v
 return b
def rank(rows):
 if not rows:return 0
 a=[[F(x) for x in row] for row in rows];r=0
 for c in range(len(a[0])):
  k=next((i for i in range(r,len(a)) if a[i][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];t=a[r][c];a[r]=[v/t for v in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][c]:
    t=a[i][c];a[i]=[v-t*w for v,w in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
def lin(cols,x):
 y=zero(len(cols[0]))
 for c,v in zip(cols,x):y=add(y,scale(v,c))
 return y
def postcheck(n,g,b,p):
 E=basis(n);counts=[0]*5
 for x in E:
  for y in E:
   counts[0]+=sub(sub(p(x,y),p(y,x)),sub(g(x,y),b(x,y)))!=zero(n)
   for z in E:
    counts[1]+=sub(p(g(x,y),z),sub(p(x,p(y,z)),p(y,p(x,z))))!=zero(n)
    counts[2]+=sub(p(x,b(y,z)),add(b(p(x,y),z),b(y,p(x,z))))!=zero(n)
    counts[3]+=add(add(g(x,g(y,z)),g(y,g(z,x))),g(z,g(x,y)))!=zero(n)
    counts[4]+=add(add(b(x,b(y,z)),b(y,b(z,x))),b(z,b(x,y)))!=zero(n)
 assert counts==[0]*5,counts
 traces=[sum(g(x,E[j])[j] for j in range(n)) for x in E]
 return {'basis_pair_checks':n*n,'basis_triples_per_identity':n**3,'failures':counts,'derived_rank':rank([g(x,y) for x in E for y in E]),'ad_traces':traces}
def homfail(n,g,b,cols):
 return sum(lin(cols,g(x,y))!=b(lin(cols,x),lin(cols,y)) for x in basis(n) for y in basis(n))
sl=law(3,[(0,1,(0,2,0)),(0,2,(0,0,-2)),(1,2,(1,0,0))])
E=basis(3);z=lambda x,y:zero(3)
results={}
results['semisimple_zero_product']=postcheck(3,sl,sl,z)
opp=lambda x,y:neg(sl(x,y))
results['opposite_bracket_minus_product']=postcheck(3,opp,sl,opp)
gsol=law(3,[(0,1,(0,2,0))])
Rcols=[(0,0,0),(0,0,0),(0,0,-1)]
prod=lambda x,y:sl(lin(Rcols,x),y)
results['nonunimodular_source_sl2_split']=postcheck(3,gsol,sl,prod)
plus=[add(c,e) for c,e in zip(Rcols,E)]
minus=[sub(c,e) for c,e in zip(Rcols,E)]
results['split_homomorphisms']={'R_failures':homfail(3,gsol,sl,Rcols),'R_plus_I_failures':homfail(3,gsol,sl,plus),'R_minus_I_failures_intentional_negative':homfail(3,gsol,sl,minus),'difference_rank':rank([sub(x,y) for x,y in zip(plus,Rcols)])}
assert results['split_homomorphisms']['R_failures']==0 and results['split_homomorphisms']['R_plus_I_failures']==0 and results['split_homomorphisms']['R_minus_I_failures_intentional_negative']>0 and results['split_homomorphisms']['difference_rank']==3
# Semisimple centerless/inner diagnostic, solve full derivation equations.
Dcols=basis(9)
def derivres(flat):
 cols=[tuple(flat[i*3:(i+1)*3]) for i in range(3)]
 out=[]
 for x in E:
  for y in E:out.extend(sub(lin(cols,sl(x,y)),add(sl(lin(cols,x),y),sl(x,lin(cols,y)))))
 return out
constraint_cols=[derivres(d) for d in Dcols]
constraint_rows=list(zip(*constraint_cols))
ad_cols=[tuple(v for y in E for v in sl(x,y)) for x in E]
results['sl2_inner_derivations']={'endomorphism_dimension':9,'derivation_constraint_rank':rank(constraint_rows),'derivation_dimension':9-rank(constraint_rows),'inner_dimension':rank(ad_cols),'center_dimension':3-rank(ad_cols)}
assert results['sl2_inner_derivations']['derivation_dimension']==3
assert results['sl2_inner_derivations']['inner_dimension']==3
# Perfect nonsemisimple source with reductive target center C^2.
entries=[(0,1,(0,2,0,0,0)),(0,2,(0,0,-2,0,0)),(1,2,(1,0,0,0,0))]
rep=[(0,3,(0,0,0,1,0)),(0,4,(0,0,0,0,-1)),(1,4,(0,0,0,1,0)),(2,3,(0,0,0,0,1))]
gn=law(5,entries+rep);red=law(5,entries);p=law(5,[]) # product is nonskew action, defined separately
def pr(x,y):
 return (0,0,0,x[0]*y[3]+x[1]*y[4],-x[0]*y[4]+x[2]*y[3])
results['perfect_source_reductive_target']=postcheck(5,gn,red,pr)
assert results['perfect_source_reductive_target']['derived_rank']==5
assert results['perfect_source_reductive_target']['ad_traces']==[0]*5
# Embedding sl2 semidirect natural module into sl3 by 2x2 affine block.
H=((1,0,0),(0,-1,0),(0,0,0));A=((0,1,0),(0,0,0),(0,0,0));B=((0,0,0),(1,0,0),(0,0,0));U=((0,0,1),(0,0,0),(0,0,0));V=((0,0,0),(0,0,1),(0,0,0))
M=[H,A,B,U,V]
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def ms(a,b):return tuple(tuple(a[i][j]-b[i][j] for j in range(3)) for i in range(3))
def ml(x):return tuple(tuple(sum(x[k]*M[k][i][j] for k in range(5)) for j in range(3)) for i in range(3))
embedding_fail=sum(ml(gn(x,y))!=ms(mm(ml(x),ml(y)),mm(ml(y),ml(x))) for x in basis(5) for y in basis(5))
results['injective_difference_not_surjective']={'source_dimension':5,'target_sl3_dimension':8,'image_rank':rank([tuple(v for row in m for v in row) for m in M]),'homomorphism_failures':embedding_fail,'source_perfect':results['perfect_source_reductive_target']['derived_rank']==5,'nonzero_abelian_ideal_basis':['u','v']}
assert embedding_fail==0 and results['injective_difference_not_surjective']['image_rank']==5
# Equal dimensions without invertible difference: Takiff sl2 -> sl2+sl2 by Levi projection.
def tak(x,y):return sl(x[:3],y[:3])+add(sl(x[:3],y[3:]),sl(x[3:],y[:3]))
def dbl(x,y):return sl(x[:3],y[:3])+sl(x[3:],y[3:])
def tp(x):return x[:3]+zero(3)
tf=sum(tp(tak(x,y))!=dbl(tp(x),tp(y)) for x in basis(6) for y in basis(6))
results['singular_difference_equal_dimension']={'source_dimension':6,'target_dimension':6,'source_derived_rank':rank([tak(x,y) for x in basis(6) for y in basis(6)]),'source_ad_traces':[sum(tak(x,basis(6)[j])[j] for j in range(6)) for x in basis(6)],'difference_rank':rank([tp(x) for x in basis(6)]),'homomorphism_failures':tf,'nonzero_abelian_ideal_dimension':3}
assert tf==0 and results['singular_difference_equal_dimension']['source_derived_rank']==6
# Compute B columns by exact 3x3 conjugation for selected SL2 points.
I=((1,0,0),(0,1,0),(0,0,1))
P=((2,0,0),(0,F(1,2),0),(0,0,1));Pi=((F(1,2),0,0),(0,2,0),(0,0,1))
W=((0,-1,0),(1,0,0),(0,0,1));Wi=((0,1,0),(-1,0,0),(0,0,1))
def coords(m):return (m[0][0],m[0][1],m[1][0])
def bc(p,pi):return [coords(mm(mm(pi,M[k]),p)) for k in [0,1]]+[(0,0,1)]
def det3(c):
 a,b,c=c
 return a[0]*(b[1]*c[2]-b[2]*c[1])-b[0]*(a[1]*c[2]-a[2]*c[1])+c[0]*(a[1]*b[2]-a[2]*b[1])
boundary={name:{'B_columns':bc(p,pi),'det':det3(bc(p,pi))} for name,p,pi in [('identity',I,I),('diagonal_2_half',P,Pi),('weyl',W,Wi)]}
assert [boundary[n]['det'] for n in boundary]==[1,F(1,4),0]
results['nonunimodular_determinant_boundary']=boundary
print(json.dumps(results,indent=2,default=str))
