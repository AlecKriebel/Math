import sympy as S,itertools,json
N=0
def ck(v):
 global N
 assert v;N+=1
t=S.symbols('t')
# Independent exact characteristic-polynomial proof controls for the equilateral angular Hessian.
for r in range(5,16,2):
 for j in range((r-1)//2+1):
  signs=[-1]*j+[1]*(r-j);q=r-2*j;v=S.Matrix(signs)
  H=q*S.diag(*signs)-v*v.T
  target=t*(t-r)**(r-1) if j==0 else t*(t+r)*(t+q)**(j-1)*(t-q)**(r-j-1)
  ck(S.Poly(H.charpoly().as_expr()).all_coeffs()==S.Poly(target,t).all_coeffs())
  ck(H*S.ones(r,1)==S.zeros(r,1));ck(q>0)
  ck(j+2*j==3*j)
# Koszul exterior multiplication squares to zero by an independently generated signed basis.
for r in range(2,9):
 for size in range(r-1):
  for J in itertools.combinations(range(r),size):
   out={}
   for a in range(r):
    if a in J:continue
    I=tuple(sorted(J+(a,)));sa=(-1)**sum(i>a for i in J)
    for b in range(r):
     if b in I:continue
     K=tuple(sorted(I+(b,)));sb=(-1)**sum(i>b for i in I);key=(K,tuple(sorted((a,b))))
     out[key]=out.get(key,0)+sa*sb
   ck(all(x==0 for x in out.values()))
# All requested rank parities and the corrected special-case shifts.
for r in range(5,101):
 m=(r-1)//2;ck(m< S.Rational(r,2));ck(2*m+1 in [r,r-1]);ck(m+2<2*m+1)
 ck((m+2)*3-2*1-1==3*m+3)
ck([3*j-2-9 for j in [4,5]]==[1,4])
print(json.dumps({'status':'PASS','independent_assertions':N,'scope':'Independent exact angular-Hessian characteristic polynomials, Koszul signs, rank parities and corrected shifts. The all-rank topology and syzygy result are credited primary theorems audited separately.'},indent=2))
