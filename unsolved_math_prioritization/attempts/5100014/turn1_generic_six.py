import sympy as s
F=s.Rational
P=s.Matrix([F(6,5),F(4,5)]);B=s.diag(F(1,4),1);n=B*P;n2=(n.dot(n));J=F(1,3)
d=s.simplify((-J*n+s.sqrt(n2-J*J)*s.Matrix([-n[1],n[0]]))/n2)
points=[]
for i in range(6):
 points.append(P)
 length=s.simplify(-2*(P.dot(B*d))/(d.dot(B*d)))
 P=(P+length*d).applyfunc(s.simplify);nn=B*P
 d=(d-2*d.dot(nn)/nn.dot(nn)*nn).applyfunc(s.simplify)
assert P==points[0]
def area(p):return s.simplify(sum(s.det(s.Matrix.hstack(x,y)) for x,y in zip(p,p[1:]+p[:1]))/2)
T=[];Q=[]
for p,q in zip(points,points[1:]+points[:1]):
 T.append(s.Matrix.vstack((B*p).T,(B*q).T).inv()*s.Matrix([1,1]))
 n=B*p;Q.append(n/n.dot(n))
ap=area(T);am=area(Q)
print('closure exact; generic start',points[0]);print('A_prime',ap);print('A_prime_0',am);print('product',s.simplify(ap*am));print('A_prime_0 / A',s.simplify(am/area(points)))
