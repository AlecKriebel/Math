from fractions import Fraction as F
import json
n=0
def check(c):
 global n
 assert c;n+=1
for rho in (F(1,4),F(1,2),F(3,4),F(9,10)):
 for theta in ((rho+1)/2,(2*rho+1)/3):
  K=(1+rho*theta)/(theta-rho)+(theta+rho)/(1-rho*theta)
  C1=1/(theta-rho)+rho/(1-rho*theta)
  C2=theta/(1-rho*theta)+rho*theta/(theta-rho)
  check(K==C1+C2)
  for T in range(31):
   w=[theta**t+theta**(T-t) for t in range(T+1)]
   for t in range(T+1):
    S=sum((rho**(t-1-k)*w[k] for k in range(t)),F(0))+sum((rho**(k-t+1)*w[k] for k in range(t,T)),F(0))
    check(S<=C1*theta**t+C2*theta**(T-t));check(S<=K*w[t])
  eps=1/(2*K);check(eps*K<1);check(1/(1-eps*K)==2)
print(json.dumps({'assertions':n,'scope':'exact finite dichotomy geometric sums and contraction margins; nonlinear trajectory proof is analytical'},indent=2))
