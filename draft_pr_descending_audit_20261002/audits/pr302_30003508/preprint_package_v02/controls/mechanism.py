import datetime, hashlib, json, os, pathlib, sys
import sympy as s
F=pathlib.Path(__file__).resolve().parent
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
checks=[]
def check(name,value):
    assert value, name
    checks.append(name)
x,y,a,t,sig=s.symbols('x y a t sig',real=True)
mean=(s.exp(-a*t)-1)*x/t
check('OU mean infinitesimal limit',s.simplify(s.limit(mean,t,0)+a*x)==0)
check('OU fixed lag mean bias',s.simplify(mean.subs({a:1,t:1})-(-x))==x/s.E)
var=sig**2*(1-s.exp(-2*a*t))/(2*a*t)
check('OU variance infinitesimal limit',s.simplify(s.limit(var,t,0)-sig**2)==0)
check('OU fixed lag centered covariance bias',s.simplify(var.subs({a:1,t:1,sig:1})-(1-s.exp(-2))/2)==0)
check('OU fixed lag covariance differs',s.simplify(var.subs({a:1,t:1,sig:1})-1)!=0)
sigma=s.diag(1+y,1);inv=sigma.inv()
check('Lamperti row-integrability fails',s.simplify(s.diff(inv[0,0],y)-s.diff(inv[0,1],x))==-1/(1+y)**2)
S=s.Matrix([[2,s.Rational(1,2)],[s.Rational(1,2),1]])
check('SPD anisotropic witness',S.det()>0 and S[0,0]>0)
check('cannot equal any scalar times identity',S[0,1]!=0)
for n in range(1,21):
    orig=s.exp(-n*n);mod=s.exp(-2*n*n)
    check('positive eigenvalue witness '+str(n),orig>0 and mod>0)
    check('log difference exact '+str(n),s.simplify(s.log(orig)-s.log(mod))==n*n)
check('transition-norm perturbation tends zero',s.limit(s.exp(-x*x)-s.exp(-2*x*x),x,s.oo)==0)
modules=[]
for name,m in sorted(sys.modules.items()):
    p=getattr(m,'__file__',None)
    if p and pathlib.Path(p).is_file():
        q=pathlib.Path(p);b=q.read_bytes();modules.append({'module':name,'path':str(q),'resolved_path':str(q.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':oct(q.stat().st_mode&0o777)})
record={'started_utc':started,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_self_pid':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'optimized':sys.flags.optimize,'python':sys.version,'executable':sys.executable,'sympy':s.__version__,'checks':checks,'assertions':len(checks),'status':'PASS_EXACT_MECHANISM_NEGATIVE_CONTROLS_NOT_PRIORITY_CERTIFICATE','loaded_modules':modules}
(F/'CONTROL_RESULTS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ('loaded_modules','checks')}))
