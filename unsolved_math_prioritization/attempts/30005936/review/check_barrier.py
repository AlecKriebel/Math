import sympy as s,json
v,t=s.symbols('v t',positive=True);b=8/(t*s.sqrt(v));F=v*(1-(1+b)*s.exp(-b));n=0
def check(x):
 global n
 assert x;n+=1
check(s.simplify(s.diff(F,t)-s.Rational(1,2)*v**s.Rational(5,2)*s.diff(F,v,2))==0)
check(s.simplify(s.diff(F,v,2)+b**3*s.exp(-b)/(4*v))==0)
check(s.simplify(s.diff(F,v)-(1-(1+b+b*b/2)*s.exp(-b)))==0)
check(s.limit(F,v,0,dir='+')==0)
check(s.limit(s.diff(F,v),v,0,dir='+')==1)
check(s.limit(s.diff(F,v,2),v,0,dir='+')==0)
check(s.limit(F,t,0,dir='+')==v)
check(s.limit(F,v,s.oo)==32/t**2)
print(json.dumps({'status':'PASS','independent_assertions':n,'sympy':s.__version__,'scope':'exact barrier derivatives and endpoint limits; stochastic localization separately audited'},indent=2))
