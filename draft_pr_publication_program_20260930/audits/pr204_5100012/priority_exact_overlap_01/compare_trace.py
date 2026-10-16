"""Diagnostic comparison of the two published/proposed trace normalizations.

The algebraic derivation is in TRACE_COMPARISON.md; finite checks do not prove
its universal identity. No network, installation, shared bytecode or Git calls.
"""
import datetime, json, pathlib
import mpmath as mp
import sympy as sp

mp.mp.dps=75
a2,b2,lam,x=sp.symbols('a2 b2 lam x', positive=True)
k2=(a2-b2)/(a2-lam)
cv2=(b2-lam)/b2
dv2=a2*(b2-lam)/(b2*(a2-lam))
kp2=(b2-lam)/(a2-lam)
den=1-k2*x-k2*(1-x)*lam/b2
den_check=sp.factor(den-cv2*(a2-(a2-b2)*x)/(a2-lam))
coeff_check=sp.factor(kp2*dv2*(a2-lam)**2/cv2**2-a2*b2)
if den_check!=0 or coeff_check!=0:
    raise RuntimeError('symbolic trace normalization mismatch')

def jac(u,m): return [mp.ellipfun(f,u,m) for f in ['sn','cn','dn']]
pointwise=[]
for a,b,L in [(5,3,mp.mpf(1)),(5,3,mp.mpf(8)),(2,1,mp.mpf('.2')),(mp.mpf('1.01'),1,mp.mpf('.7'))]:
    m=(a*a-b*b)/(a*a-L); K=mp.ellipk(m)
    v=mp.ellipf(mp.asin(mp.sqrt(L)/(b)),m)
    errors=[]
    for fraction in ['0','.2','.77','1.8']:
        u=mp.mpf(fraction)*K; sn,cn,dn=jac(u,m)
        lhs=jac(u+K-v,m)[2]+jac(u+K+v,m)[2]
        rhs=2*a*b*dn/(a*a-(a*a-b*b)*sn*sn)
        errors.append(abs(lhs-rhs))
    pointwise.append({'a':str(a),'b':str(b),'lambda':str(L),'max_abs_error':str(max(errors))})

closed=[]
for N,tau in [(3,1),(4,1),(5,1),(5,2),(6,1),(8,1),(8,3),(10,3),(12,5)]:
    a,b=mp.mpf(5),mp.mpf(3)
    lo,hi=mp.mpf(0),b*b
    for _ in range(260):
        L=(lo+hi)/2; m=(a*a-b*b)/(a*a-L)
        v=mp.ellipf(mp.asin(mp.sqrt(L)/b),m); K=mp.ellipk(m)
        if v/K<mp.mpf(2)*tau/N: lo=L
        else: hi=L
    L=(lo+hi)/2; ac=mp.sqrt(a*a-L); bc=mp.sqrt(b*b-L)
    m=(a*a-b*b)/(a*a-L); K=mp.ellipk(m)
    v=mp.ellipf(mp.asin(mp.sqrt(L)/b),m); delta=2*v
    w=mp.mpf('.213')*K
    def Q(u):
        sn,cn,dn=jac(u,m)
        return (-ac*(bc/ac)**2*sn/dn**2,bc*cn/dn**2)
    q=[Q(w+v+j*delta) for j in range(N)]
    pedal=sum(q[j][0]*q[(j+1)%N][1]-q[j][1]*q[(j+1)%N][0] for j in range(N))/2
    trace=sum(jac(w+K+v+j*delta,m)[2] for j in range(N))
    ct=mp.sqrt(L)*ac*((a*a+b*b)*a*a*b*b-L*(a**4+b**4))/(2*a**3*b**3)
    err=abs(pedal/trace-ct)
    if not err<mp.mpf('1e-65'):
        raise RuntimeError(('coefficient mismatch',N,tau,str(err)))
    closed.append({'least_N':N,'tau':tau,'lambda':str(L),'direct_Q_area_over_shifted_dn_trace':str(pedal/trace),'Ferudun_prefactor_converted_to_CT':str(ct),'abs_error':str(err)})
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'symbolic_denominator_difference':str(den_check),'symbolic_squared_positive_coefficient_difference':str(coeff_check),'pointwise_checks':pointwise,'closed_trace_checks':closed,'status':'all finite diagnostics passed; universal derivation in TRACE_COMPARISON.md'}
pathlib.Path(__file__).with_name('TRACE_COMPARISON_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
