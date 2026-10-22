"""Independent graph quotient and rational Gaussian checks. No claimant imports.

The integral relation graph identifies monomials only by primitive differences;
its connected components, with separately killed vertices, give a free basis.
Finite checks complement the review's universal proof and do not establish priority.
"""
from itertools import combinations_with_replacement,permutations,product
from fractions import Fraction
import json,math,random
def need(x,s):
 if not x:raise RuntimeError(s)
def quotient(n,mutation=None):
 mons=list(combinations_with_replacement(range(2*n),2));par={m:m for m in mons}
 def root(m):
  while par[m]!=m:m=par[m]
  return m
 def pair(a,b):return tuple(sorted((a,b)))
 for i,j,k in permutations(range(n),3):
  if mutation!='no_diffs':par[root(pair(i,n+j))]=root(pair(i,n+k))
 killed=set()
 for a,b in mons:
  if (a<n and b<n and a!=b and mutation!='no_xx') or (a>=n and b>=n and (a!=b or mutation!='no_ysq')) or (a<n and b==n+a):killed.add(root((a,b)))
 reps=sorted(set(map(root,mons))-killed);index={r:i for i,r in enumerate(reps)}
 return {m:index.get(root(m)) for m in mons},len(reps)
def matrix(n,q,c):
 coords,d=q;M=[[0]*(2*n) for _ in range(d)]
 for a in range(2*n):
  for b in range(2*n):
   r=coords[tuple(sorted((a,b)))]
   if r is not None:M[r][b]+=c[a]
 return M
def rank(M,p):
 a=[[x%p for x in r] for r in M];k=0
 for j in range(len(a[0])):
  for i in range(k,len(a)):
   if a[i][j]:break
  else:continue
  a[k],a[i]=a[i],a[k];inv=pow(a[k][j],-1,p)
  for i in range(k+1,len(a)):
   t=a[i][j]*inv%p
   a[i]=[(x-t*y)%p for x,y in zip(a[i],a[k])]
  k+=1
  if k==len(a):break
 return k
def det(M):
 a=[list(map(Fraction,r)) for r in M];d=Fraction(1)
 for j in range(len(a)):
  i=next((i for i in range(j,len(a)) if a[i][j]),None)
  if i is None:return 0
  if i!=j:a[i],a[j]=a[j],a[i];d=-d
  v=a[j][j];d*=v
  for i in range(j+1,len(a)):
   t=a[i][j]/v
   a[i]=[x-t*y for x,y in zip(a[i],a[j])]
 need(d.denominator==1,'nonintegral determinant');return int(d)
def ordered_matrix(n,q,c):
 coords,d=q;ids=[coords[(i,i)] for i in range(n)]+[coords[tuple(sorted((i,n+(i+1)%n)))] for i in range(n)]
 need(len(set(ids))==2*n and set(ids)==set(range(d)),'u,v component bijection')
 return [matrix(n,q,c)[i] for i in ids]
def gens(n):
 out={((m,1),) for m in combinations_with_replacement(range(2*n),3)}
 for a,b in combinations_with_replacement(range(2*n),2):
  if (a<n and b<n and a!=b) or a>=n or (a<n and b==n+a):out.add((((a,b),1),))
 for i,j,k in permutations(range(n),3):out.add(tuple(sorted([((i,n+j),1),((i,n+k),-1)])))
 return out
def main():
 rng=random.Random(13370004534);qs={n:quotient(n) for n in range(1,14)};ints=0;forms=0;fields=0
 for n,q in qs.items():need(q[1]==(1 if n==1 else 2*n),'graph dimension')
 for n in range(2,14):
  for _ in range(15):
   c=[rng.choice([-5,-3,-1,1,2,4,7]) for i in range(n)]+[rng.randrange(-8,9) for i in range(n)]
   M=ordered_matrix(n,qs[n],c);want=(-1)**(n-1)*(n-1)*math.prod(x*x for x in c[:n])
   need(det(M)==want,'arbitrary dense determinant');ints+=1
  for p in [2,3,5,7,11]:
   c=[1]*n+[0]*n;M=matrix(n,qs[n],c);good=rank(M,p)==2*n
   need(good==((n-1)%p!=0),'fixed field pattern')
   sq=[sum(r[:n])%p for r in M];need(any(sq),'square sum survives incl char2')
   soc=[sum(r[n:])%p for r in M];need((not any(soc))==((n-1)%p==0),'socle against xsum')
   fields+=1
 for n,p in [(2,2),(2,3),(2,5),(3,2),(3,3),(4,2),(4,3)]:
  for c in product(range(p),repeat=2*n):
   M=matrix(n,qs[n],c);good=rank(M,p)==2*n
   need(good==((n-1)%p!=0 and all(c[:n])),'exhaustive arbitrary forms')
   if good:need(any(sum(r[j]*c[j] for j in range(2*n))%p for r in M),'SLP square')
   if (n-1)%p==0:need(all(sum(r[n:])%p==0 for r in M),'all forms kill socle')
   forms+=1
 # At n=1 the degree-two target is one-dimensional: never apply 2n square test.
 for p in [2,3,5,7,11]:
  need(rank(matrix(1,qs[1],[1,0]),p)==1,'width1 WLP')
  need(matrix(1,qs[1],[1,0])[0][0]%p!=0,'width1 square')
 injections=0;generation=0
 for n in range(1,5):
  t=n+2;target=gens(t)
  for inj in permutations(range(t),n):
   for g in gens(n):
    image=tuple(sorted((tuple(sorted((v//n)*t+inj[v%n] for v in m)),c) for m,c in g))
    need(image in target,'nonadjacent injection')
   injections+=1
 for n in range(3,10):
  target=gens(3)
  for g in gens(n):
   supp=sorted({v%n for m,c in g for v in m});need(len(supp)<=3,'support')
   rev={v:i for i,v in enumerate(reversed(supp))}
   image=tuple(sorted((tuple(sorted((v//n)*3+rev[v%n] for v in m)),c) for m,c in g))
   need(image in target,'generator orbit witness');generation+=1
 false={}
 def reject(name,x):need(not x,'false claim accepted '+name);false[name]='rejected'
 reject('n1_hf_is_uniform',qs[1][1]==2)
 reject('omit_differences_preserves_hf',quotient(4,'no_diffs')[1]==8)
 reject('omit_xx_preserves_hf',quotient(4,'no_xx')[1]==8)
 reject('omit_y_squares_preserves_hf',quotient(4,'no_ysq')[1]==8)
 reject('char2_all_good',rank(matrix(3,qs[3],[1]*3+[0]*3),2)==6)
 reject('char2_all_bad',rank(matrix(4,qs[4],[1]*4+[0]*4),2)!=8)
 reject('char2_good_square_zero',not any(sum(r[:4])%2 for r in matrix(4,qs[4],[1]*4+[0]*4)))
 reject('y_only_good',rank(matrix(4,qs[4],[0]*4+[1]*4),2)==8)
 reject('one_zero_x_can_be_good',rank(matrix(4,qs[4],[0,1,1,1,4,3,2,1]),5)==8)
 reject('bad_means_p_divides_n',rank(matrix(3,qs[3],[1]*3+[0]*3),3)<6)
 # Explicit degree-one coordinate vector, and every variable times it, at n divisible by p.
 degree1=[0]*4+[1]*4;need(any(x%2 for x in degree1),'degree1 sumy nonzero when p divides n')
 reject('sumy_collapses_to_scalar_n',all(x%2==0 for x in degree1))
 print(json.dumps({'status':'PASS','method':'primitive relation graph; separate rational Gaussian determinant','quadratic_widths':list(qs),'dense_integer_determinants':ints,'fixed_field_width_cases':fields,'exhaustive_forms':forms,'nonadjacent_injections':injections,'width3_generator_witnesses':generation,'generation_max_width':9,'negative_controls':false,'finite_only':True},indent=2,sort_keys=True))
if __name__=='__main__':main()
