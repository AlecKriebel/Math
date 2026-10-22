def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

import sympy as s
from itertools import combinations
B=s.Matrix([[1,s.Rational(1,2)],[1,-s.Rational(1,2)],[1,s.Rational(3,4)],[1,-s.Rational(3,4)]])
Q=B*B.T
Bp=(B.T*B).inv()*B.T
P=s.eye(4)-B*Bp
H=s.diag(-1,s.Rational(3,4))
for t in [1,2,4,8,16,32,64,100]:
 Y=t*P+Bp.T*H*Bp
 minors=[Y.extract(S,S).det() for j in range(1,4) for S in combinations(range(4),j)]
 if min(minors)>=0: break
print('Q=',Q,'\nt=',t,'\nY=',Y,'\nminors=',minors,'\ntraceYQ=',s.trace(Y*Q),'\ntraceY=',s.trace(Y))
require(min(minors)>0 and s.trace(Y*Q)==-s.Rational(1,4), 'Certificate validation failed at original line 13')
# Positive-definite rational perturbation stays outside FW3.
eps=s.Rational(1,1000)
Qpd=Q+eps*s.eye(4)
require(s.trace(Y*Qpd)<0, 'Certificate validation failed at original line 17')
print('PD example epsilon=',eps,'negative pairing=',s.trace(Y*Qpd))
