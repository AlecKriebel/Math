"""Independently authored finite falsification controls; no inherited code imported."""
import sys
sys.path.insert(0, '/Users/alec/Library/Python/3.11/lib/python/site-packages')
from pathlib import Path
from datetime import datetime, timezone
import json, math, hashlib
import mpmath as m
import sympy as s

if sys.flags.optimize or not sys.dont_write_bytecode:
    raise RuntimeError('Require assertions and -B')
m.mp.dps = 70
checks = 0
worst = {}
def close(name,x,y,tol=m.mpf('1e-50')):
    global checks
    e=abs(x-y)/max(m.mpf(1),abs(x),abs(y))
    worst[name]=max(worst.get(name,m.mpf(0)),e)
    checks+=1
    assert e < tol, (name, str(x), str(y), str(e))
def det(x,y): return x[0]*y[1]-x[1]*y[0]
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def dot(x,y): return x[0]*y[0]+x[1]*y[1]
def area(p): return sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2
def exact(z):
    global checks
    checks+=1
    assert s.simplify(z)==0,z

# Direct exact geometry for the excluded common-caustic 4-period family.
four=[]
for P in [[(s.Integer(2),0),(0,s.Integer(1)),(-s.Integer(2),0),(0,-s.Integer(1))],
          [(4/s.sqrt(5),1/s.sqrt(5)),(-4/s.sqrt(5),1/s.sqrt(5)),
           (-4/s.sqrt(5),-1/s.sqrt(5)),(4/s.sqrt(5),-1/s.sqrt(5))]]:
    P=[tuple(map(s.sympify,p)) for p in P]
    R=[];Q=[]
    for j,p in enumerate(P):
        prev=P[j-1];q=P[(j+1)%4]
        exact(p[0]**2/4+p[1]**2-1)
        n=s.Matrix([p[0]/4,p[1]])
        nn=s.Matrix([q[0]/4,q[1]])
        rr=s.Matrix([list(n),list(nn)]).inv()*s.Matrix([1,1])
        R.append(tuple(rr));Q.append(tuple(n/n.dot(n)))
        d=s.Matrix(sub(q,p));v=s.Matrix(p)
        G=s.diag(s.Rational(5,16),s.Integer(5)) # inverse squared caustic semiaxes
        exact((d.dot(G*v))**2-d.dot(G*d)*(v.dot(G*v)-1))
        incoming=s.Matrix(sub(p,prev));outgoing=s.Matrix(sub(q,p))
        incoming=incoming/s.sqrt(incoming.dot(incoming))
        outgoing=outgoing/s.sqrt(outgoing.dot(outgoing))
        reflected=incoming-2*incoming.dot(n)/n.dot(n)*n
        for a,b in zip(reflected,outgoing):exact(a-b)
    four.append({'outer':str(s.simplify(area(R))),'pedal':str(s.simplify(area(Q))),
                 'product':str(s.simplify(area(R)*area(Q)))})
assert {x['product'] for x in four}=={'32','50'}

# Independent direct physical constructions, all coprime windings in these periods.
cases=[]
for kval in ['0.00001','0.1','0.7','0.99','0.99999']:
    k=m.mpf(kval); kp=m.sqrt(1-k*k); K=m.ellipk(k*k)
    sn=lambda t:m.ellipfun('sn',t,k*k)
    cn=lambda t:m.ellipfun('cn',t,k*k)
    dn=lambda t:m.ellipfun('dn',t,k*k)
    f=lambda t:sn(t)*cn(t)/dn(t)
    for N in [3,5,6,7,9,10,14]:
      for tau in range(1,(N+1)//2):
        if math.gcd(tau,N)!=1:continue
        v=2*tau*K/N; alpha=m.mpf('1.37');beta=alpha*kp
        a=alpha*dn(v)/cn(v);b=beta/cn(v);lam=a*a-alpha*alpha
        close('confocal',lam,b*b-beta*beta)
        assert 0<lam<b*b
        P=lambda z:(-a*sn(z),b*cn(z))
        q=N//math.gcd(N,2);r=N//q
        C=m.fprod((cn(2*K*j/q)/sn(2*K*j/q))**2 for j in range(1,(q+1)//2))
        const=(a*a*b**4*f(v)*(2*f(v)-f(2*v))/(4*alpha*beta*cn(K-v)**2)
               *r*r*kp**q/C**2)
        products=[]
        for phase in ['0','0.137','0.973']:
            u=m.mpf(phase)*K;ps=[P(u+2*j*v) for j in range(N)]
            ns=[(x/(a*a),y/(b*b)) for x,y in ps]
            R=[];Q=[]
            for j,(p,n) in enumerate(zip(ps,ns)):
                nn=ns[(j+1)%N];d=det(n,nn)
                assert abs(d)>m.mpf('1e-50')
                R.append(((nn[1]-n[1])/d,(n[0]-nn[0])/d))
                Q.append((n[0]/dot(n,n),n[1]/dot(n,n)))
                tangent=(-sn(u+(2*j+1)*v)/alpha,cn(u+(2*j+1)*v)/beta)
                close('inner_tangency_left',dot(tangent,p),1)
                close('inner_tangency_right',dot(tangent,ps[(j+1)%N]),1)
                inc=sub(p,ps[j-1]);out=sub(ps[(j+1)%N],p)
                inc=tuple(x/m.sqrt(dot(inc,inc)) for x in inc)
                out=tuple(x/m.sqrt(dot(out,out)) for x in out)
                reflected=tuple(inc[h]-2*dot(inc,n)/dot(n,n)*n[h] for h in range(2))
                for h in range(2):close('physical_reflection',reflected[h],out[h])
                z=u+2*j*v
                edge=sub(P(z+K-v),P(z+K+v))
                footedge=(b/a*edge[0]/(2*cn(K-v)),edge[1]/(2*cn(K-v)))
                for h in range(2):close('pointwise_edgefoot',Q[-1][h],footedge[h])
                expectedR=(a*a/alpha*(-sn(u+(2*j+1)*v)),b*b/beta*cn(u+(2*j+1)*v))
                for h in range(2):close('polarity',R[-1][h],expectedR[h])
            T=lambda z:sum(dn(z+2*j*v) for j in range(N))
            close('outer_formula',area(R),a*a*b*b/(alpha*beta)*f(v)*T(u+v))
            close('pedal_formula',area(Q),b*b/(4*cn(K-v)**2)*(2*f(v)-f(2*v))*T(u+K-v))
            prod=area(R)*area(Q);products.append(prod)
            close('explicit_product',prod,const)
            close('reversal',area(list(reversed(R)))*area(list(reversed(Q))),prod)
            close('threefold_repeat',area(R*3)*area(Q*3),9*prod)
        close('phase_constancy',products[0],products[-1])
        cases.append({'k':kval,'N':N,'tau':tau,'phases':3,'product':m.nstr(const,20)})

# Complex trace checks, away from the poles; not proofs of meromorphic continuation.
traces=[]
for kval in ['0.01','0.73','0.9999']:
    k=m.mpf(kval);kp=m.sqrt(1-k*k);K=m.ellipk(k*k);Ki=m.ellipk(kp*kp)
    dn=lambda t:m.ellipfun('dn',t,k*k)
    sn=lambda t:m.ellipfun('sn',t,k*k)
    cn=lambda t:m.ellipfun('cn',t,k*k)
    for q in [1,3,5,7,11,21]:
      C=m.fprod((cn(2*K*j/q)/sn(2*K*j/q))**2 for j in range(1,(q+1)//2))
      for imag in ['0','0.31','0.997']:
        z=K*m.mpf('0.173')+1j*Ki*m.mpf(imag)
        U=lambda z:sum(dn(z+2*K*j/q) for j in range(q))
        V=m.fprod(dn(z+2*K*j/q) for j in range(q))
        close('classical_product_sum',V,C*U(z))
        close('complex_trace',U(z)*U(z+K),kp**q/C**2)
        close('imaginary_antiperiod',U(z+2j*Ki),-U(z))
        traces.append({'k':kval,'q':q,'imag_fraction':imag})

result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','checks':checks,
        'physical_families':len(cases),'phase_cases':3*len(cases),'complex_trace_cases':len(traces),
        'four_period_exact':four,'physical_cases':cases,'traces':traces,
        'worst_relative_errors':{k:m.nstr(v,9) for k,v in worst.items()},
        'mpmath_version':m.__version__,'sympy_version':s.__version__,'python':sys.version,
        'dps':m.mp.dps,'tolerance':'1e-50',
        'limits':'Finite diagnostics, arbitrary precision without intervals; exact four-period SymPy simplifications. These support analytic audit and do not prove the theorem.'}
out=Path(__file__).with_name('OWNED_CONTROL_RESULTS.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','checks','physical_families','phase_cases','complex_trace_cases','four_period_exact','worst_relative_errors']},indent=2))
