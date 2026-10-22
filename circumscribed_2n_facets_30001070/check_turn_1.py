"""Exact rational checks of the local Hessian coefficient; not a global proof."""
from itertools import product
import sympy as S

def check(P,Q):
 n=P.rows; total0=S.Integer(0);total1=S.Integer(0);total2=S.Integer(0)
 for sig in product([-1,1], repeat=n):
  s=S.Matrix(sig);D=S.diag(*sig);M=D*P+Q
  b=S.Matrix([sum((P[i,j]+sig[i]*Q[i,j])**2 for j in range(n)) for i in range(n)])
  v=-M*s;w=M*M*s+D*b/2
  total0+=(s.T*s)[0];total1+=2*(s.T*v)[0];total2+=(v.T*v)[0]+2*(s.T*w)[0]
 total0/=2**n;total1/=2**n;total2/=2**n
 norm=lambda A:sum(x*x for x in A)
 expected=2*norm(P)+4*norm((Q+Q.T)/2)
 assert total0==n and total1==0 and S.simplify(total2-expected)==0
 return {'n':n,'constant':str(total0),'linear':str(total1),'quadratic':str(total2),'expected':str(expected)}

if __name__=='__main__':
 import json
 out=[]
 for n in range(2,6):
  P=S.Matrix(n,n,lambda i,j:0 if i==j else S.Rational((i+2)*(j+3)%7-3,5))
  Q=S.Matrix(n,n,lambda i,j:0 if i==j else S.Rational((i+1)*(j+4)%11-5,7))
  out.append(check(P,Q));out.append(check(S.zeros(n),(Q-Q.T)/2))
 print(json.dumps({'checks':out,'all_passed':True},indent=2))
