import itertools,random,json
count=0;eligible=0
mats=[tuple(x) for x in itertools.product((-1,0,1),repeat=4)]
def mv(A,x):return(A[0]*x[0]+A[1]*x[1],A[2]*x[0]+A[3]*x[1])
def mul(A,B):
 a=mv(A,(B[0],B[2]));b=mv(A,(B[1],B[3]));return(a[0],b[0],a[1],b[1])
def cols(A):return[(A[0],A[2]),(A[1],A[3])]
def span_has(v,basis):
 B=[x for x in basis if x!=(0,0)]
 if not B:return v==(0,0)
 det=lambda a,b:a[0]*b[1]-a[1]*b[0]
 if any(det(B[0],x)!=0 for x in B):return True
 return det(B[0],v)==0
for C in [(1,0),(0,1),(1,1),(1,-1)]:
 ker=(-C[1],C[0])
 for V in [[],[ker],[(1,0),(0,1)]]:
  for K in mats:
   if any(C[0]*v[0]+C[1]*v[1] for v in cols(K)):continue
   if any(not span_has(mv(K,v),V) for v in V):continue
   for A in mats:
    KA=mul(K,A);AK=mul(A,K);comm=tuple(a-b for a,b in zip(KA,AK))
    if not span_has(mv(comm,ker),V):continue
    eligible+=1;M=cols(mul(K,K))
    assert all(span_has(mv(A,v),M+V) for v in M);count+=1
    null_zero=not span_has(mv(A,ker),[ker]+V)
    if null_zero:assert mul(K,K)==(0,0,0,0);count+=1
# Exact Neumann disturbance inversion with E=I, H strictly upper triangular.
rng=random.Random(1199)
for _ in range(1000):
 a,b,c=[rng.randrange(-9,10) for j in range(3)];H=((0,a,b),(0,0,c),(0,0,0))
 def h(x):return(a*x[1]+b*x[2],c*x[2],0)
 r1=tuple(rng.randrange(-10,11) for j in range(3));r2=tuple(rng.randrange(-10,11) for j in range(3));r=tuple(x+y for x,y in zip(r1,r2));hr=h(r);hhr=h(hr)
 v1=tuple(r[i]+hr[i]+hhr[i] for i in range(3));hv=h(v1);v2=tuple(r2[i]+hv[i] for i in range(3))
 assert tuple(v1[i]-v2[i] for i in range(3))==r1;count+=1
 assert tuple(v2[i]-hv[i] for i in range(3))==r2;count+=1
print(json.dumps({'status':'PASS','assertions':count,'stable_image_fixtures':eligible,'nilpotent_disturbance_fixtures':1000},sort_keys=True))
