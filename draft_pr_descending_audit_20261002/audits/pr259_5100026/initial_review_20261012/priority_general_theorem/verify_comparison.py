"""Post-freeze comparison with the exact Ferudun candidate.

No candidate/submitted program is imported. This re-expresses its geometric
identities and compares them with the frozen independent Jacobi reduction.
Finite mpmath checks supplement the exact identities; they are not interval
proofs and do not establish historical priority.
"""
from pathlib import Path
import datetime, hashlib, json, math
import sympy as sp
import mpmath as mp

HERE = Path(__file__).resolve().parent
checks=[]
def exact(name, expression):
    answer=sp.factor(expression)
    assert answer == 0, (name,answer)
    checks.append(name)

a,b,lam=sp.symbols('a b lam',positive=True)
cf2=a*a-b*b
alpha=(b*b-lam)/b**4
beta=(lam*(a*a+b*b)-a*a*b*b)/(a**4*b**4)
gamma=(a*a-lam)/a**4
kappa=alpha+lam/(a*a*b*b)
Lx2=1/gamma; Ly2=1/alpha
exact('candidate conic inverse eigenvalues',alpha+beta*cf2-gamma)
bridge=(Lx2*Ly2+Lx2*b*b-Ly2*a*a)/b**2
exact('candidate kappa equals frozen G2 coefficient divided by Lx2Ly2',
      bridge-kappa*Lx2*Ly2)
x2=sp.symbols('x2'); y2=1-x2
exact('same weighted chord-normal denominator',
      alpha+beta*cf2*y2-(Lx2*x2+Ly2*y2)/(Lx2*Ly2))

k2,s2=sp.symbols('k2 s2',positive=True)
c2=1-s2; d2=1-k2*s2; q2=1-k2
ae2=d2/c2; be2=q2/c2; lambdae=q2*s2/c2
H0=1-2*k2*s2+k2*s2*s2
sub={a*a:ae2,b*b:be2,lam:lambdae}
exact('original focus normalization',ae2-be2-k2)
exact('candidate outer x equals independent a squared',Lx2.subs(sub)-ae2**2)
exact('candidate outer y equals independent b over cn',Ly2.subs(sub)-be2/c2)
exact('candidate mean coefficient equals G3',
      (kappa*Ly2).subs(sub)*d2-H0/c2)

S,C,Dn,s,c,d,k=sp.symbols('S C Dn s c d k')
D0=1-k*k*s*s*S*S
snminus=(S*c*d-s*C*Dn)/D0
snplus=(S*c*d+s*C*Dn)/D0
cnminus=(C*c+S*s*Dn*d)/D0
cnplus=(C*c-S*s*Dn*d)/D0
rules={C*C:1-S*S,Dn*Dn:1-k*k*S*S,c*c:1-s*s,d*d:1-k*k*s*s}
exact('circle adjacent product real part',
      sp.factor(snminus*snplus-cnminus*cnplus-(2*d*d*S*S/D0-1)).subs(rules))
exact('circle adjacent product imaginary part',
      sp.factor(snminus*cnplus+snplus*cnminus-2*d*S*C/D0).subs(rules))

z,w,eta,diff=sp.symbols('z w eta diff')
curve=diff*z*z*w*w-z*z-w*w+2*eta*z*w+diff
Q=diff*z**4+(eta*eta-diff*diff-1)*z*z+diff
exact('compact curve completed-square identity',
      ((diff*z*z-1)*w+eta*z)**2-Q-(diff*z*z-1)*curve)
exact('exact grouped pole cancellation',
      z*(-2*eta*z/(diff*z*z-1))-(-2*eta/(diff-z**-2)))
exact('N4 eta zero gives candidate C zero',
      (kappa*Ly2).subs(lam,a*a*b*b/(a*a+b*b))/2-1)

mp.mp.dps=80
maxerr=mp.mpf(0); cases=[]
for kval in ['0.1','0.6','0.95','0.999']:
    km=mp.mpf(kval); mm=km*km; qp=mp.sqrt(1-mm); K=mp.ellipk(mm)
    sn=lambda u:mp.ellipfun('sn',u,mm)
    cn=lambda u:mp.ellipfun('cn',u,mm)
    dn=lambda u:mp.ellipfun('dn',u,mm)
    for N in [4,6,8,10,12,14,18,22,30]:
        for tau in range(1,N//2):
            if math.gcd(N,tau)!=1: continue
            v=2*K*tau/N; delta=2*v; sv=sn(v); cv=cn(v); dv=dn(v)
            aa=dv/cv; bb=qp/cv; lamn=aa*aa-1
            alph=(bb*bb-lamn)/bb**4
            kap=alph+lamn/(aa*aa*bb*bb)
            Lx=aa*aa; Ly=bb/cv
            H=1-2*mm*sv**2+mm*sv**4
            Z=mp.ellipe(mp.atan2(sn(delta),cn(delta)),mm)-mp.ellipe(mm)*delta/K
            av=(sv**2+Z/(mm*sn(delta)))/(1-mm*sv**4)
            trace_formula=2*dv**2*av-1
            centroid_formula=km*(-1+H/cv**2*av)
            for phase in ['0','0.137','0.731']:
                u=mp.mpf(phase)*K
                # Actual affine outer-vertex coordinates are (-sn,cn).
                coords=[-sn(u+j*delta)+1j*cn(u+j*delta) for j in range(N)]
                trace=mp.fsum(coords[j]*coords[(j+1)%N] for j in range(N))/N
                centroid_candidate=(km*(-1+kap*Ly**2/2*(1+trace.real)),
                    kap*km*Lx*Ly*trace.imag/2)
                error=max(abs(trace-trace_formula),
                    abs(centroid_candidate[0]-centroid_formula),abs(centroid_candidate[1]))
                assert error < mp.mpf('1e-60'),(kval,N,tau,phase,error)
                maxerr=max(maxerr,error)
                cases.append(dict(k=kval,N=N,tau=tau,phase=phase,
                    error=mp.nstr(error,8),trace_mean=mp.nstr(trace.real,20),
                    centroid=mp.nstr(centroid_formula,20)))

result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    independent_freeze_utc='2026-10-12T12:31:07.550095+00:00',
    symbolic_checks=len(checks),checks=checks,numeric_cases=len(cases),cases=cases,
    maximum_numeric_error=mp.nstr(maxerr,10),numeric_precision_dps=mp.mp.dps,
    sympy=sp.__version__,mpmath=mp.__version__,numeric_is_not_interval_proof=True,
    no_candidate_program_imported=True,
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(HERE/'COMPARISON_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['symbolic_checks','numeric_cases','maximum_numeric_error']},indent=2))
