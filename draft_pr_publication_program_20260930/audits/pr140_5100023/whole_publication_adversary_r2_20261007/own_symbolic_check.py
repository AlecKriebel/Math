import datetime,json,pathlib
import sympy as s

a,b,C,S,U,V,lam,h,L,N=s.symbols('a b C S U V lam h L N',nonzero=True)
checks=[]
def ck(label,expr):
    value=s.factor(s.cancel(expr))
    if value!=0:raise RuntimeError((label,value))
    checks.append(dict(label=label,residual=str(value)))
A=s.Matrix([a*(C*U+S*V),b*(S*U-C*V)])
B=s.Matrix([a*(C*U-S*V),b*(S*U+C*V)])
Adot=s.Matrix([-a*(S*U-C*V),b*(C*U+S*V)])
Bdot=s.Matrix([-a*(S*U+C*V),b*(C*U-S*V)])
edge=B-A
ck('unconstrained squared-length derivative',2*edge.dot(Bdot-Adot)-8*(a*a-b*b)*S*C*V*V)
ck('positive squared chord metric',(edge.dot(edge))-4*V*V*(a*a*S*S+b*b*C*C))
D2=C*C/a**2+S*S/b**2
Hn=1/D2
nux=C/a/s.sqrt(D2);nuy=S/b/s.sqrt(D2)
K=a*a*b*b-lam*(a*a-b*b)
kappa=K/(b*b-lam)
ck('Ferudun normal pair x',(-2*h+2*kappa*h*nux*nux/Hn)-(-2*h+2*h*K*C*C/(a*a*(b*b-lam))))
ck('Ferudun normal pair y',(2*kappa*h*nux*nuy/Hn)-(2*h*K*S*C/(a*b*(b*b-lam))))
H=a*a/(a*a-b*b)*(1-b*L/(2*a*s.sqrt(lam)*N))
gamma=-1+K/((b*b-lam)*(a*a-b*b))*(1-b*b*L/(2*N*a*b*s.sqrt(lam)))
ck('exact later coefficient equivalence',gamma-(-1+K*H/(a*a*(b*b-lam))))
r=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',SymPy=s.__version__,checks=checks,
       limitations=['These five rational/symbolic identities establish their stated algebra, not general dynamics or priority.'])
pathlib.Path(__file__).with_name('own_symbolic_result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
