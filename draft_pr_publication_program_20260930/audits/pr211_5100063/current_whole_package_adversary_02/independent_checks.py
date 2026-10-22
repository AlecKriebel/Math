"""Independent review02 controls. No imports from reviewed programs.
Reads only itself/interpreter dependencies; writes one result next to itself.
No network, subprocess, local Git, native, provider or production mutation.
Finite numerical observations are noninterval diagnostics, not a proof.
"""
import json, math, hashlib, platform
from pathlib import Path
import sympy as S
import mpmath as M

HERE=Path(__file__).resolve().parent

def exact():
    k,t,s,h,C,d,r,n,alpha,kp=S.symbols('k t s h C d r n alpha kp')
    D=1-k*k*t*s*s; q=1-t
    rel=[(h,t),(C,q),(d,1-k*k*t),(r,1-s*s),(n,1-k*k*s*s),(kp,1-k*k)]
    checks={}
    def need(name,expr):
        a=S.cancel(expr).as_numer_denom()[0]
        for x,y in rel:a=S.rem(a,x*x-y,x)
        a=S.factor(a); checks[name]=str(a)
        if a!=0:raise AssertionError((name,a))
    sm=(s*C*d-h*r*n)/D; sp=(s*C*d+h*r*n)/D
    cm=(r*C+s*h*n*d)/D; cp=(r*C-s*h*n*d)/D
    # Chord, not outer-tangent equations: this reconstructs the actual caustic.
    need('caustic chord at minus',d*s*sm+r*cm-C)
    need('caustic chord at plus',d*s*sp+r*cp-C)
    need('chord caustic dual equation',s*s+r*r-1)
    a,b=alpha*d/C,alpha*kp/C
    need('confocal input',a*a-b*b-alpha*alpha*k*k)
    X,Y=-a*d*s/C,b*r/C
    need('outer original tangent minus',-X*sm/a+Y*cm/b-1)
    need('outer original tangent plus',-X*sp/a+Y*cp/b-1)
    need('tangent determinant',sp*cm-sm*cp-2*h*C*n/D)
    U=1-2*k*k*t+k*k*t*t;V=1-2*t+k*k*t*t;W=1-k*k*t*t
    need('raw focal distance',(X-alpha*k)**2+Y*Y-alpha*alpha*(1+k*s)*(U+k*V*s)/q**2)
    L0=(U*U-k*k*V*V*t)/d;L1=(V*V-U*U*t)/C
    Z=W*W-4*k*k*t*t*q*(1-k*k*t)
    need('real positive first gap',d*d-k*k*C*C-(1-k*k))
    need('real positive second gap',L0*L0-k*k*L1*L1-(1-k*k)*Z*Z)
    need('root fiber separation expression',L0-d*L1/C-4*(1-k*k)*t*d*W)
    # sn''=-(1+k^2)sn+2k^2 sn^3: branch value +1/k has nonzero second derivative.
    branch_second=S.factor((-(1+k*k)*s+2*k*k*s**3).subs(s,1/k))
    if S.simplify(branch_second-(1-k*k)/k)!=0:raise AssertionError(branch_second)
    return {'polynomial_remainders':checks,'count':len(checks),'critical_sn_second_derivative':str(branch_second),'critical_dn_derivative_squared':'-(1-k^2), hence nonzero for 0<k<1','meaning':'Exact identities only; analytic fiber completeness is proved in DERIVATION.md'}

def diagnostic():
    M.mp.dps=135
    det=lambda p,q:p[0]*q[1]-p[1]*q[0]
    dot=lambda p,q:p[0]*q[0]+p[1]*q[1]
    sub=lambda p,q:(p[0]-q[0],p[1]-q[1])
    norm=lambda p:M.sqrt(dot(p,p))
    def area(P):return M.fsum(det(p,q) for p,q in zip(P,P[1:]+P[:1]))/2
    def invert(P,c):
        out=[];mind=M.inf
        for x,y in P:
            den=(x-c)**2+y*y;mind=min(mind,den)
            out.append((c+(x-c)/den,y/den))
        return out,mind
    def raw_outer(P,a,b):
        ans=[]
        for p,q in zip(P,P[1:]+P[:1]):
            m11,m12,m21,m22=p[0]/a**2,p[1]/b**2,q[0]/a**2,q[1]/b**2
            den=m11*m22-m12*m21
            assert den>0
            ans.append(((m22-m12)/den,(m11-m21)/den))
        return ans
    configs=[('0.73',N,tau) for N in (3,5,7,9,11) for tau in range(1,(N+1)//2) if math.gcd(N,tau)==1]
    configs += [('0.000000000000001',7,3),('0.999999999999999999',3,1),('0.999999999999999999',41,20),('0.91',41,1),('0.91',41,20),('0.6',41,10),('0.6',41,11),('0.73',4,1)]
    rows=[];glob={x:M.mpf(0) for x in ('closure','ellipse','caustic','canonical','kernel','antiperiod','reflection','common_pole_limit','focus_shift','reversal','repetition','scale')}
    for kt,N,tau in configs:
        k=M.mpf(kt);m=k*k;kp=M.sqrt(1-m);al=M.mpf('1.7');be=al*kp
        K=M.ellipk(m);p=1j*M.ellipk(1-m);v=2*K*tau/N;step=2*v
        sn=lambda z:M.ellipfun('sn',z,m)
        cn=lambda z:M.ellipfun('cn',z,m)
        dn=lambda z:M.ellipfun('dn',z,m)
        h,C,d=sn(v),cn(v),dn(v);q=C*C;t=h*h
        a,b,c=al*d/C,be/C,al*k;Ao,Bo=a*d/C,b/C
        U,V,W=1-2*m*t+m*t*t,1-2*t+m*t*t,1-m*t*t
        L0,L1=(U*U-m*V*V*t)/d,(V*V-U*U*t)/C
        C0=Bo*h*d*q**4/(al**3*C)
        edge=lambda z:C0*dn(z)*(1-m*t*sn(z)**2)/((d+k*C*sn(z))**2*(L0+k*L1*sn(z)))
        loc={x:M.mpf(0) for x in glob};products=[];bvalues=[];minD=M.inf
        canon=lambda z:(-a*sn(z),b*cn(z))
        for ph in ('0.039','0.481','1.223','2.971'):
            w=K*M.mpf(ph);P=[canon(w)]
            R=(P[0][0]/al,P[0][1]/be);R2=dot(R,R);rr=M.sqrt(R2-1)
            T=(al*(R[0]-rr*R[1])/R2,be*(R[1]+rr*R[0])/R2)
            vel=sub(T,P[0]);vel=(vel[0]/norm(vel),vel[1]/norm(vel))
            for j in range(N):
                z=P[-1]
                if j:
                    normal=(z[0]/a**2,z[1]/b**2);fac=2*dot(vel,normal)/dot(normal,normal)
                    vel=(vel[0]-fac*normal[0],vel[1]-fac*normal[1])
                lam=-2*(z[0]*vel[0]/a**2+z[1]*vel[1]/b**2)/(vel[0]**2/a**2+vel[1]**2/b**2)
                assert lam>0
                zz=(z[0]+lam*vel[0],z[1]+lam*vel[1]);P.append(zz)
                cr=det(z,zz);nx,ny=(zz[1]-z[1])/cr,(z[0]-zz[0])/cr
                loc['caustic']=max(loc['caustic'],abs(al*al*nx*nx+be*be*ny*ny-1))
            loc['closure']=max(loc['closure'],norm(sub(P[-1],P[0]))/a);P=P[:-1]
            for j,z in enumerate(P):
                loc['canonical']=max(loc['canonical'],norm(sub(z,canon(w+j*step)))/a)
                loc['ellipse']=max(loc['ellipse'],abs(z[0]**2/a**2+z[1]**2/b**2-1))
            Q=raw_outer(P,a,b);Ip,Dp=invert(Q,c);Im,Dm=invert(Q,-c);minD=min(minD,Dp,Dm)
            bp,bm=area(Ip),area(Im);assert bp>0 and bm>0
            products.append(bp*bm);bvalues.append(bp)
            raw=M.fsum(edge(w+(j+1)*step) for j in range(N))
            loc['kernel']=max(loc['kernel'],abs(bp-raw)/abs(bp))
            shifted=raw_outer([canon(w+2*K+j*step) for j in range(N)],a,b)
            loc['focus_shift']=max(loc['focus_shift'],abs(area(invert(shifted,c)[0])-bm)/abs(bm))
            loc['reversal']=max(loc['reversal'],abs(area(list(reversed(Ip)))+bp)/abs(bp))
            loc['repetition']=max(loc['repetition'],abs(area(Ip*2)/bp-2))
            scale=M.mpf('0.41');qs=[(scale*x,scale*y) for x,y in Q]
            scaled=area(invert(qs,c*scale)[0])*area(invert(qs,-c*scale)[0])
            loc['scale']=max(loc['scale'],abs(scaled*scale**4/(bp*bm)-1))
        z=K*(M.mpf('.317')+M.mpf('.221')*1j);r0=3*K+p
        loc['antiperiod']=abs(edge(z+2*p)+edge(z))/max(1,abs(edge(z)))
        loc['reflection']=abs(edge(2*r0-z)+edge(z))/max(1,abs(edge(z)))
        eps=M.mpf('1e-35')
        observed=(edge(p+eps)+edge(p-eps))/2;expected=1j*C0*t/(q*L1)
        loc['common_pole_limit']=abs(observed-expected)/max(1,abs(expected))
        variation=max(abs(x/products[0]-1) for x in products)
        if N%2:assert variation<M.mpf('1e-75'),(kt,N,tau,variation)
        else:assert variation>M.mpf('1e-5')
        assert minD>0
        assert max(vv for key,vv in loc.items() if key!='common_pole_limit')<M.mpf('1e-75'),(kt,N,tau,loc)
        assert loc['common_pole_limit']<M.mpf('1e-45')
        for key in glob:glob[key]=max(glob[key],loc[key])
        rows.append({'k':kt,'N':N,'tau':tau,'outer_axis_order':'y_longer' if Bo>Ao else 'x_longer','product':M.nstr(products[0],35),'phase_variation':M.nstr(variation,12),'Bplus_variation':M.nstr(max(abs(x/bvalues[0]-1) for x in bvalues),12),'min_focal_distance_squared':M.nstr(minD,15),'max_errors':{x:M.nstr(y,12) for x,y in loc.items()}})
    return {'precision':M.mp.dps,'noninterval':True,'families':len(rows),'phases_per_family':4,'rows':rows,'max_errors':{x:M.nstr(y,12) for x,y in glob.items()}}

if __name__=='__main__':
    out={'schema':'review02-independent-controls-v1','python':platform.python_version(),'sympy':S.__version__,'mpmath':M.__version__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'exact':exact(),'finite':diagnostic()}
    (HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','exact_checks':out['exact']['count'],'families':out['finite']['families'],'max_errors':out['finite']['max_errors']},indent=2))
