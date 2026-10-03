import sympy as s
p,q,u,v,w=s.symbols('p q u v w')
vars=(p,q,u,v,w)
def char(kind,p,q,u,v,w,corrected=True):
 A=u*v*w-v*v-w*w if corrected or kind=='vir' else u*v*w-u*u-v*v
 B=u/v/w+v/u/w+w/u/v-u**-2
 return ((p*p*q if kind=='sl' else p*p*q*q)*A+B)/(1-p)/(1-q)
def R(l,n,m,corrected=True,reverse=False):
 return s.cancel(char('sl',p,q/p,u*p**l,v*p**n,w*p**m,corrected)+char('vir',p/q,q,u*q**(m if reverse else l),v*q**n,w*q**(l if reverse else m))-char('sl',p,q/p,u,v,w,corrected)-char('vir',p/q,q,u,v,w))
def E(f,weights):
 out=s.Integer(1)
 for term in s.Add.make_args(s.expand(f)):
  powers=term.as_powers_dict()
  coef=term
  wt=0
  for x,y in zip(vars,weights):
   power=powers.get(x,0); coef/=x**power; wt+=power*y
  if not coef.is_Integer or any(x in coef.free_symbols for x in vars):raise ValueError('not Laurent: '+str(coef))
  out*=wt**(-int(coef))
 return s.factor(out)
def t(n,a,e1,e2):
 out=s.Integer(1)
 if n>0:
  for i in range(n):
   for j in range(n-i):out*=a-i*e1-j*e2
 elif n<0:
  for i in range(1,-n):
   for j in range(1,-n-i+1):out*=a+i*e1+j*e2
 return out
def C(m,n,l,mu,nu,la,K):
 T=lambda n,a:t(n,a,1,-1/K)
 sign=(-1)**(s.Rational(1,2)*(l-m+n)*(l-m+n+1)+4*n*(m-n)*(m-n-s.Rational(1,2)))
 return sign*T(-l-m-n,-(2+la+mu+nu)/(2*K))*T(-l+m-n,-(la-mu+nu)/(2*K))*T(-l-m+n,-(la+mu-nu)/(2*K))*T(l-m-n,-(-la+mu+nu)/(2*K))/(T(-2*l,-(la+1)/K)*T(-2*m,-(mu+1)/K)*T(-2*n,-(nu+1)/K))
def norm(l,la,K):return t(-2*l,-la/K,1,-1/K)/t(-2*l,-(la+1)/K,1,-1/K)
