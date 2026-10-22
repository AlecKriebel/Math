from pathlib import Path
import sys,json,math,collections
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'math_algebra_family_01/runtime_packages'))
import mpmath as mp
import sympy as sp
root=Path(__file__).resolve().parent
checks=[]
def ck(label,ok):
    if not ok:raise RuntimeError(label)
    checks.append(label)
# An independent symbolic witness using physical squared semiaxes.
a2,b2,lam,X=sp.symbols('a2 b2 lam X')
u=a2*a2/(a2-lam);w=b2*b2/(b2-lam);f=a2-b2
physical=(w+f+(u-w)*X)**2-4*f*u*X
candidate=(1-f*X/(a2-lam))*((w+f)**2-(a2-lam)*(u-w)**2*X/f)
ck('physical rational factorization',sp.cancel(physical-candidate)==0)
ck('N4 degree drop only zero outer axes difference',sp.factor(u-w-f*(a2*b2-lam*(a2+b2))/((a2-lam)*(b2-lam)))==0)
# Independently encode the torus on integer residues mod 2N; no package functions.
count=0
for N in range(3,258):
    M=2*N
    for tau in range(1,(N+1)//2):
        if math.gcd(N,tau)!=1:continue
        L=N//math.gcd(N,2);step=4*tau
        G={(j*step)%M for j in range(L)}
        ck('order '+str((N,tau)),len(G)==L)
        exceptional=N==4
        D=collections.Counter()
        for g in G:
            D[(-g)%M]-=2 if exceptional else 4
            D[(N-g)%M]+=2
            if not exceptional:
                D[(N+step-g)%M]+=1
                D[(N-step-g)%M]+=1
        D={p:m for p,m in D.items() if m}
        ck('norm criterion '+str((N,tau)),bool(D)==(N%4!=0))
        ck('coset criterion '+str((N,tau)),(N in G)==(N%4==0))
        if D:ck('exact nonzero multiplicity '+str((N,tau)),len(D)==2*L and set(D.values())=={-4,4})
        count+=1
mp.mp.dps=120
numeric=[];divisors=[]
for kt in ['0.0001','0.81','0.9999']:
    k=mp.mpf(kt);m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m);Kp=mp.ellipk(1-m)
    sn=lambda z:mp.ellipfun('sn',z,m)
    cn=lambda z:mp.ellipfun('cn',z,m)
    dn=lambda z:mp.ellipfun('dn',z,m)
    for N in [3,4,7,8,11,12,31,32,33,34,36]:
        candidates=[1,max(t for t in range(1,(N+1)//2) if math.gcd(t,N)==1)]
        for tau in sorted(set(candidates)):
            delta=4*K*tau/N;v=delta/2;C=cn(v);D=dn(v)
            a=D/C;b=kp/C;Ao=a*D/C;Bo=b/C
            phases=[K*mp.mpf(j)/7 for j in [0,1,2,4,6]]
            logs=[];max_tangent=mp.mpf(0);max_reflection=mp.mpf(0)
            for phase in phases:
                lp=mp.mpf(0);lm=mp.mpf(0)
                for j in range(N):
                    u=phase+j*delta
                    p=(-a*sn(u-v),b*cn(u-v));q=(-a*sn(u+v),b*cn(u+v))
                    det=p[0]*q[1]-p[1]*q[0]
                    # Directly solve x*px/a²+y*py/b²=1 etc.
                    xx=a*a*(q[1]-p[1])/det;yy=b*b*(p[0]-q[0])/det
                    max_tangent=max(max_tangent,abs(xx+Ao*sn(u))/max(1,abs(xx)),abs(yy-Bo*cn(u))/max(1,abs(yy)))
                    lp+=mp.log((xx-k)**2+yy*yy)/2;lm+=mp.log((xx+k)**2+yy*yy)/2
                    if j==0:
                        prev=(-a*sn(u-v-delta),b*cn(u-v-delta))
                        inc=(p[0]-prev[0],p[1]-prev[1]);out=(q[0]-p[0],q[1]-p[1]);n=(p[0]/(a*a),p[1]/(b*b))
                        il=mp.hypot(*inc);ol=mp.hypot(*out);inc=tuple(z/il for z in inc);out=tuple(z/ol for z in out)
                        scale=2*(inc[0]*n[0]+inc[1]*n[1])/(n[0]*n[0]+n[1]*n[1])
                        ref=(inc[0]-scale*n[0],inc[1]-scale*n[1])
                        max_reflection=max(max_reflection,abs(ref[0]-out[0]),abs(ref[1]-out[1]))
                logs.append((lp,lm))
            spreads=[max(z[i] for z in logs)-min(z[i] for z in logs) for i in [0,1]]
            ck('direct tangent/physical reflection '+str((kt,N,tau)),max_tangent<mp.mpf('1e-100') and max_reflection<mp.mpf('1e-100'))
            if N%4==0:ck('ordinary positive constancy '+str((kt,N,tau)),max(spreads)<mp.mpf('1e-100'))
            else:
                # Only require a resolved finite counterexample when not nearly circular.
                if kt!='0.0001':ck('ordinary nonconstancy '+str((kt,N,tau)),min(spreads)>mp.mpf('1e-100'))
            numeric.append({'k':kt,'N':N,'tau':tau,'log_product_spreads':[mp.nstr(s,12) for s in spreads],'tangent_residual':mp.nstr(max_tangent,8),'reflection_residual':mp.nstr(max_reflection,8),'diagnostic_only':True,'nearly_circular_undetected_variation_possible':kt=='0.0001' and N%4!=0})
    # Probe actual local orders from Jacobi evaluation, distinct from integer bookkeeping.
    for N,tau in [(3,1),(4,1),(7,3),(8,3),(11,5),(12,5)]:
        delta=4*K*tau/N;v=delta/2;Cv=(1-k*k*sn(v)**4)**2/cn(v)**8
        H=lambda z:Cv*dn(z)**2*(dn(delta)**2-k*k*cn(delta)**2*sn(z)**2)
        p=mp.j*Kp;eps=mp.mpc('0.0000000007','0.0000000002')
        centers=[(p,-2 if N==4 else -4),(p+K,2)]
        if N!=4:centers += [(p+K+delta,1),(p+K-delta,1)]
        orders=[]
        for z,order in centers:
            observed=mp.log10(abs(H(z+eps)/H(z+eps/10)))
            ck('actual complex local order '+str((kt,N,tau,order)),abs(observed-order)<mp.mpf('1e-4'))
            orders.append({'expected':order,'observed':mp.nstr(observed,15)})
        divisors.append({'k':kt,'N':N,'tau':tau,'orders':orders})
result={'status':'PASS','runtime':{'sympy':sp.__version__,'mpmath':mp.__version__,'dps':mp.mp.dps},'subgroup_cases':count,'check_count':len(checks),'numeric_families':numeric,'local_order_probes':divisors,'limitation':'Finite diagnostics are not interval certificates or substitutes for DERIVATION.md.'}
(root/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','subgroup_cases':count,'checks':len(checks),'numeric_families':len(numeric),'complex_divisors':len(divisors)},indent=2))
