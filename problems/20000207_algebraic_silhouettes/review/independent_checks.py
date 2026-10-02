import sympy as S,json
count=0
s,t=S.symbols('s t')
for d in range(7,35):
 f=s**d+t**d;g=s**(d-3)*t**2;h=s**(d-5)*t**4
 pol=[f,s*g,t*g,s*h,t*h,s*S.diff(f,t),t*S.diff(f,s),s*S.diff(f,s)-t*S.diff(f,t)]
 M=S.Matrix([[S.expand(p).coeff(s,d-j).coeff(t,j) for p in pol] for j in range(d+1)])
 assert M.rank()==8;count+=1
for d in range(1,9):
 for H in [S.eye(2),S.Matrix([[1,1],[0,1]]),S.Matrix([[0,1],[1,0]]),S.Matrix([[2,0],[0,1]])]:
  x,y=H*S.Matrix([s,t]);M=S.Matrix([[S.expand(x**(d-k)*y**k).coeff(s,d-j).coeff(t,j) for k in range(d+1)] for j in range(d+1)])
  # Coordinates consist of common A0=B0, A1..Ad, B1..Bd.
  for lam in [S.Integer(1),S.Integer(2),S.Integer(-1)]:
   X=S.zeros(d+1,2*d+1)
   for j in range(d+1):
    X[j,0]=(1 if j==0 else 0)-lam*M[j,0]
    if j>0:X[j,j]=1
    for k in range(1,d+1):X[j,d+k]=-lam*M[j,k]
   exceptional=H[1,0]==0 and lam*H[0,0]**d==1
   assert X.rank()==(d if exceptional else d+1);count+=1
# Symbolic sphere camera motion, including calibration and visible ray discriminant.
a=S.symbols('a',positive=True);R=S.Rational(5,3);f=S.Rational(4,3);c=(1-a*a)/(1+a*a);sine=2*a/(1+a*a)
A1=S.diag(1,-1,-1);A2=S.Matrix([[c,0,-sine],[0,-1,0],[-sine,0,-c]])
simp=lambda X:X.applyfunc(S.factor)
assert simp(A2*A2.T)==S.eye(3);assert S.factor(A2.det())==1;count+=2
C2=S.Matrix([R*sine,0,R*c]);tr=S.Matrix([0,0,R]);assert simp(A2*C2+tr)==S.zeros(3,1);count+=1
A=A2*A1.T;T=simp(tr-A*tr);tx=S.Matrix([[0,-T[2],T[1]],[T[2],0,-T[0]],[-T[1],T[0],0]]);K=S.diag(f,f,1);F=simp(K.inv()*tx*A*K.inv())
expect=R*S.Matrix([[0,(c-1)/f**2,0],[(c-1)/f**2,0,sine/f],[0,-sine/f,0]])
assert simp(F-expect)==S.zeros(3);assert S.factor(F[1,2]/F[0,1])==-f/a;count+=2
u,v=S.symbols('u v');assert S.factor(R**2-(R**2-1)*(1+(u*u+v*v)/f**2))==1-u*u-v*v;count+=1
print(json.dumps({'status':'PASS','assertions':count,'jacobian_degrees':28,'line_incidence_cases':96,'symbolic_camera_model':True},sort_keys=True))
