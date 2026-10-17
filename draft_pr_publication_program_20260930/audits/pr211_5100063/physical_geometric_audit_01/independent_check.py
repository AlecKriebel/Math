#!/opt/homebrew/bin/python3.11
"""Fresh physical-geometric audit. Does not import, execute or modify source checkers.

Outputs only next to this file. Sympy checks are exact rational identities modulo
explicit Jacobi quadratic equations. Mpmath diagnostics use actual caustic
tangents, physical reflection, line intersections, Euclidean inversions and
shoelace sums. No interval-certification claim is made for numerical results.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import math
import sys
import sympy as sp
import mpmath as mp

OUT = Path(__file__).resolve().parent


def utc():
    return datetime.now(timezone.utc).isoformat()


def exact_checks():
    k, t, s, r, e, h, C, d, l, alpha = sp.symbols(
        'k t s r e h C d l alpha', real=True)
    q = 1-t
    H = 1-k*k*t*s*s
    U = 1-2*k*k*t+k*k*t*t
    V = 1-2*t+k*k*t*t
    W = 1-k*k*t*t
    Z = W*W-4*k*k*t*t*q*(1-k*k*t)
    constraints = [(h, t), (C, q), (d, 1-k*k*t),
                   (r, 1-s*s), (e, 1-k*k*s*s), (l, 1-k*k)]
    records = []

    def check(name, expr):
        n = sp.fraction(sp.cancel(expr))[0]
        for var, square in constraints:
            n = sp.rem(n, var*var-square, var)
        residual = sp.factor(n)
        if residual != 0:
            raise AssertionError((name, residual))
        records.append({'name': name, 'residual': '0', 'kind': 'exact polynomial remainder'})

    sm = (s*C*d-h*r*e)/H
    ss = (s*C*d+h*r*e)/H
    cm = (r*C+s*h*e*d)/H
    cp = (r*C-s*h*e*d)/H
    check('raw tangent matrix determinant', ss*cm-sm*cp-2*h*C*e/H)
    X, Y = -d*s/C, r/C
    check('first raw tangent equation', -X*sm+Y*cm-1)
    check('second raw tangent equation', -X*ss+Y*cp-1)
    check('confocal outer and caustic axes', (alpha*d/C)**2-(alpha*l/C)**2-alpha**2*k**2)
    check('strict x-axis expansion squared', d*d-C*C-(1-k*k)*t)
    Ao, Bo = alpha*d*d/q, alpha*l/q
    check('outer locus axes difference', Ao*Ao-Bo*Bo-alpha**2*k*k*V/q**2)
    check('distance constant coefficient', Bo*Bo+(alpha*k)**2-alpha**2*U/q**2)
    check('distance linear coefficient', U+V-2*q*d*d)
    distance = (Ao*s+alpha*k)**2+(Bo*r)**2
    check('raw focal squared-distance factorization',
          distance-alpha**2/q**2*(1+k*s)*(U+k*V*s))
    L0 = (U*U-k*k*V*V*t)/d
    L1 = (V*V-U*U*t)/C
    check('first shifted distance-factor product',
          (1+k*sm)*(1+k*ss)-(d+k*C*s)**2/H)
    check('second shifted distance-factor product',
          (U+k*V*sm)*(U+k*V*ss)-(d+k*C*s)*(L0+k*L1*s)/H)
    qm, qp = sp.Matrix([-Ao*sm-alpha*k, Bo*cm]), sp.Matrix([-Ao*ss-alpha*k, Bo*cp])
    rawdet = sp.det(sp.Matrix.hstack(qm, qp))/2
    detform = alpha*Bo*h*d*e*(d+k*C*s)/(C*H)
    check('raw translated outer edge determinant', rawdet-detform)
    distance_product = alpha**4/q**4*(d+k*C*s)**3*(L0+k*L1*s)/H**2
    kernel = Bo*h*d*q**4/(alpha**3*C)*e*H/((d+k*C*s)**2*(L0+k*L1*s))
    check('division gives exact q^4 edge normalization', detform/distance_product-kernel)
    D3 = U*W-2*k*k*t*q*V
    C3 = V*W-2*t*d*d*U
    check('triple-angle dn numerator', U*U-k*k*V*V*t-d*d*D3)
    check('triple-angle cn numerator', V*V-U*U*t-q*C3)
    sn2, cn2, dn2 = 2*h*C*d/W, V/W, U/W
    den3 = 1-k*k*t*sn2*sn2
    check('triple-angle addition denominator', den3-Z/W**2)
    cn3 = (cn2*C-sn2*h*dn2*d)/den3
    dn3 = (dn2*d-k*k*sn2*h*cn2*C)/den3
    check('L0 equals Z dn(3v)', L0-Z*dn3)
    check('L1 equals Z cn(3v)', L1-Z*cn3)
    check('positive gap for first real denominator', d*d-k*k*C*C-(1-k*k))
    check('positive gap for triple denominator', L0*L0-k*k*L1*L1-(1-k*k)*Z*Z)
    return {'generated_utc': utc(), 'sympy': sp.__version__,
            'assumptions': '0<k<1; 0<t<1; h,C,d,l positive; s=sn(u), r=cn(u), e=dn(u); real e>0',
            'quadratic_constraints': [str(v*v)+'='+str(z) for v,z in constraints],
            'denominators': 'C,d,alpha,q,H,W,Z are nonzero on strict real domain, proved in DERIVATION.md',
            'checks': records, 'count': len(records)}


def det(p, q):
    return p[0]*q[1]-p[1]*q[0]


def exact_geometry():
    simp = sp.simplify
    def line_intersections(P, a2, b2):
        Q = []
        for p, q in zip(P, P[1:]+P[:1]):
            M = sp.Matrix([[p[0]/a2, p[1]/b2], [q[0]/a2, q[1]/b2]])
            sol = M.inv()*sp.Matrix([1,1])
            Q.append(tuple(map(simp,sol)))
        return Q
    def area(P):
        return simp(sum(det(p,q) for p,q in zip(P,P[1:]+P[:1]))/2)
    def invert(P, f):
        Q=[]
        for p in P:
            v=(p[0]-f[0],p[1]-f[1]); dd=simp(v[0]**2+v[1]**2)
            assert dd != 0
            Q.append((simp(f[0]+v[0]/dd),simp(f[1]+v[1]/dd)))
        return Q
    def geometric_validations(P, a2,b2, al2,be2):
        vals=[]
        for i,p in enumerate(P):
            pre=P[i-1]; nxt=P[(i+1)%len(P)]
            vals.append(simp(p[0]**2/a2+p[1]**2/b2-1))
            # A line n.x=1 is tangent iff alpha^2 nx^2+beta^2 ny^2=1.
            L=sp.Matrix([[p[0],p[1]],[nxt[0],nxt[1]]]).inv()*sp.Matrix([1,1])
            vals.append(simp(al2*L[0]**2+be2*L[1]**2-1))
            vin=sp.Matrix([p[0]-pre[0],p[1]-pre[1]])
            vout=sp.Matrix([nxt[0]-p[0],nxt[1]-p[1]])
            vin=vin/sp.sqrt(vin.dot(vin));vout=vout/sp.sqrt(vout.dot(vout))
            n=sp.Matrix([p[0]/a2,p[1]/b2])
            refl=vin-2*(vin.dot(n))/(n.dot(n))*n
            vals.extend(simp(z) for z in refl-vout)
        assert all(v==0 for v in vals), vals
        return {'ellipse_caustic_reflection_residuals': [str(v) for v in vals], 'all_exact_zero':True}
    families=[]
    for name,a2,b2,x in [('triangle_A',sp.Integer(21),sp.Integer(16),sp.Rational(3,5)),
                        ('triangle_B',sp.Integer(8),sp.Integer(3),sp.Rational(4,5))]:
        a,b=sp.sqrt(a2),sp.sqrt(b2);y=1-x
        al2,be2=a2*x*x,b2*y*y
        P0=[(a,0),(-a*x,b*sp.sqrt(1-x*x)),(-a*x,-b*sp.sqrt(1-x*x))]
        P1=[(0,b),(-a*sp.sqrt(1-y*y),-b*y),(a*sp.sqrt(1-y*y),-b*y)]
        phases=[]
        for P in [P0,P1]:
            valid=geometric_validations(P,a2,b2,al2,be2)
            Q=line_intersections(P,a2,b2); c=sp.sqrt(a2-b2)
            Iplus=invert(Q,(c,0));Iminus=invert(Q,(-c,0))
            bp,bm=area(Iplus),area(Iminus)
            phases.append({'P':str(P),'Q':str(Q),'Iplus':str(Iplus),'Iminus':str(Iminus),
                           'Bplus':str(bp),'Bminus':str(bm),'product':str(simp(bp*bm)),**valid})
        assert simp(sp.sympify(phases[0]['product'])-sp.sympify(phases[1]['product']))==0
        phases_product=phases[0]['product']
        q=be2/b2;t=1-q;m=(a2-b2)/al2;d2=a2*q/al2
        U=1-2*m*t+m*t*t;V=1-2*t+m*t*t;W=1-m*t*t
        Z=W*W-4*m*t*t*q*d2
        L0=(U*U-m*V*V*t)/sp.sqrt(d2);L1=(V*V-U*U*t)/sp.sqrt(q)
        assert simp(L0/Z-1)==0 and simp(L1/Z+1)==0
        families.append({'name':name,'a2':str(a2),'b2':str(b2),'alpha2':str(al2),'beta2':str(be2),
                         'modulus_squared':str(m),'t':str(t),'q':str(q),'d2':str(d2),
                         'critical_L0_over_Z':str(simp(L0/Z)),'critical_L1_over_Z':str(simp(L1/Z)),
                         'common_product':phases_product,'phases':phases})
    # Exact even primitive boundary witness: same ellipse and same caustic.
    a2,b2,al2,be2=sp.Integer(2),sp.Integer(1),sp.Rational(4,3),sp.Rational(1,3)
    P0=[(0,1),(-sp.sqrt(2),0),(0,-1),(sp.sqrt(2),0)]
    z=sp.sqrt(3)
    P1=[(2/z,1/z),(-2/z,1/z),(-2/z,-1/z),(2/z,-1/z)]
    even=[]
    for P in [P0,P1]:
        valid=geometric_validations(P,a2,b2,al2,be2)
        Q=line_intersections(P,a2,b2)
        bp,bm=area(invert(Q,(1,0))),area(invert(Q,(-1,0)))
        even.append({'P':str(P),'Q':str(Q),'Bplus':str(bp),'Bminus':str(bm),
                     'product':str(simp(bp*bm)),**valid})
    assert simp(sp.sympify(even[0]['product'])-sp.sympify(even[1]['product'])) != 0
    return {'generated_utc':utc(),'exact_triangles':families,
            'exact_even_N4_counterexample':{'a2':str(a2),'b2':str(b2),'alpha2':str(al2),'beta2':str(be2),
                                            'phases':even,'distinct_products':True}}


def numeric_checks(precision=85, specifications_override=None):
    mp.mp.dps=precision
    def fstr(x): return mp.nstr(x,24)
    def norm(p): return mp.sqrt(p[0]*p[0]+p[1]*p[1])
    def sub(p,q): return (p[0]-q[0],p[1]-q[1])
    def dot(p,q): return p[0]*q[0]+p[1]*q[1]
    def area(P): return mp.fsum(det(p,q) for p,q in zip(P,P[1:]+P[:1]))/2
    def inverse(P,f):
        inv=[];minD=mp.inf
        for p in P:
            z=sub(p,f);D=dot(z,z);minD=min(minD,D)
            inv.append((f[0]+z[0]/D,f[1]+z[1]/D))
        return inv,minD
    def shoelaces(P,c):
        Ip,Dp=inverse(P,(c,mp.mpf(0)));Im,Dm=inverse(P,(-c,mp.mpf(0)))
        return area(Ip),area(Im),min(Dp,Dm)
    def raw_outer(P,a,b):
        Q=[];dets=[]
        for p,q in zip(P,P[1:]+P[:1]):
            A,B,C,D=p[0]/a**2,p[1]/b**2,q[0]/a**2,q[1]/b**2
            den=A*D-B*C;dets.append(den)
            Q.append(((D-B)/den,(A-C)/den))
        return Q,min(dets)

    records=[]
    # All coprime stars at every listed small odd period, not just convex p=1.
    specifications=[(str(k),N,tau,'standard') for k in ['0.2','0.65','0.94']
                    for N in [3,5,7,9,11,13,15,17]
                    for tau in range(1,(N+1)//2) if math.gcd(tau,N)==1]
    specifications += [(k,N,tau,'boundary') for k,N,tau in
                       [('0.00000001',3,1),('0.00000001',11,5),('0.999999',3,1),
                        ('0.999999',13,1),('0.999999',13,6),('0.999999',31,15),
                        ('0.75',101,1),('0.75',101,50)]]
    specifications += [('0.65',N,tau,'even_control') for N,tau in [(4,1),(6,1),(8,1),(8,3),(10,3)]]
    if specifications_override is not None:
        specifications=specifications_override
    phasefractions=[mp.mpf(x) for x in ['0.021','0.233','0.611','0.977','1.317','2.141','3.503']]
    global_max={name:mp.mpf(0) for name in ['closure','canonical_vertex','ellipse','caustic_tangency',
                                         'reflection','outer_formula','distance_factor','edge_kernel',
                                         'focus_shift','reversal','repeat_scaling','spatial_scale']}
    genuine_orbits=0;points=0
    for ktext,N,tau,kind in specifications:
        k=mp.mpf(ktext); m=k*k; kp=mp.sqrt(1-m); alpha=mp.mpf('1.3'); beta=alpha*kp
        K=mp.ellipk(m);v=2*K*tau/N;delta=2*v
        sn=lambda u:mp.ellipfun('sn',u,m)
        cn=lambda u:mp.ellipfun('cn',u,m)
        dn=lambda u:mp.ellipfun('dn',u,m)
        h,C,d=sn(v),cn(v),dn(v);q=C*C;t=h*h
        a,b=alpha*d/C,beta/C;c=alpha*k
        Ao,Bo=a*d/C,b/C
        U,V,W=1-2*m*t+m*t*t,1-2*t+m*t*t,1-m*t*t
        L0,L1=(U*U-m*V*V*t)/d,(V*V-U*U*t)/C
        def canon(w):return (-a*sn(w),b*cn(w))
        def kernel(u):
            s=sn(u);H=1-m*t*s*s
            return Bo*h*d*q**4/(alpha**3*C)*dn(u)*H/((d+k*C*s)**2*(L0+k*L1*s))
        def qformula(w):return (-Ao*sn(w),Bo*cn(w))
        local={name:mp.mpf(0) for name in global_max}; products=[];bps=[];bms=[];phase_rows=[]
        mindet=mp.inf;minfocus=mp.inf;minout=mp.inf;minedge=mp.inf
        for frac in phasefractions:
            w=frac*K;P=[canon(w)]
            # Construct a genuine tangent from P0 to the caustic, without using
            # the claimed outer formula or candidate edge kernel.
            R=(P[0][0]/alpha,P[0][1]/beta);R2=dot(R,R)
            z=mp.sqrt(R2-1)
            T=(alpha*(R[0]-z*R[1])/R2,beta*(R[1]+z*R[0])/R2)
            vel=sub(T,P[0]);vel=(vel[0]/norm(vel),vel[1]/norm(vel))
            incoming=None; turn=mp.mpf(0)
            for j in range(N):
                p=P[-1]
                if incoming is not None:
                    n=(p[0]/a**2,p[1]/b**2)
                    vel=(incoming[0]-2*dot(incoming,n)/dot(n,n)*n[0],
                         incoming[1]-2*dot(incoming,n)/dot(n,n)*n[1])
                hit=-2*(p[0]*vel[0]/a**2+p[1]*vel[1]/b**2)/(vel[0]**2/a**2+vel[1]**2/b**2)
                assert hit>0
                nxt=(p[0]+hit*vel[0],p[1]+hit*vel[1]);P.append(nxt)
                incoming=vel
                turn+=mp.atan2(det((p[0]/a,p[1]/b),(nxt[0]/a,nxt[1]/b)),
                               dot((p[0]/a,p[1]/b),(nxt[0]/a,nxt[1]/b)))
                # Raw line cross product has scale arbitrary; normalize n.x=1.
                cross=det(p,nxt)
                nx,ny=(nxt[1]-p[1])/cross,(p[0]-nxt[0])/cross
                local['caustic_tangency']=max(local['caustic_tangency'],abs(alpha**2*nx**2+beta**2*ny**2-1))
            local['closure']=max(local['closure'],norm(sub(P[-1],P[0]))/max(a,b))
            assert abs(turn/(2*mp.pi)-tau)<mp.mpf('1e-45')
            P=P[:-1];genuine_orbits+=1;points+=len(P)
            for j,p in enumerate(P):
                local['canonical_vertex']=max(local['canonical_vertex'],norm(sub(p,canon(w+j*delta)))/max(a,b))
                local['ellipse']=max(local['ellipse'],abs(p[0]**2/a**2+p[1]**2/b**2-1))
                pre=P[j-1];nxt=P[(j+1)%N];vi=sub(p,pre);vo=sub(nxt,p)
                vi=(vi[0]/norm(vi),vi[1]/norm(vi));vo=(vo[0]/norm(vo),vo[1]/norm(vo))
                n=(p[0]/a**2,p[1]/b**2)
                expected=(vi[0]-2*dot(vi,n)/dot(n,n)*n[0],vi[1]-2*dot(vi,n)/dot(n,n)*n[1])
                local['reflection']=max(local['reflection'],norm(sub(vo,expected)))
            Q,dd=raw_outer(P,a,b);mindet=min(mindet,dd)
            bp,bm,focusD=shoelaces(Q,c);minfocus=min(minfocus,focusD);minout=min(minout,min(p[0]**2/a**2+p[1]**2/b**2-1 for p in Q))
            bps.append(bp);bms.append(bm);products.append(bp*bm)
            for j,Qj in enumerate(Q):
                u=w+(j+mp.mpf('0.5'))*delta
                local['outer_formula']=max(local['outer_formula'],norm(sub(Qj,qformula(u)))/max(Ao,Bo))
                Dactual=(Qj[0]-c)**2+Qj[1]**2
                Dfactor=alpha**2/q**2*(1+k*sn(u))*(U+k*V*sn(u))
                local['distance_factor']=max(local['distance_factor'],abs(Dactual-Dfactor)/max(1,abs(Dactual)))
                Qnext=Q[(j+1)%N]
                Ip=(Qj[0]-c,Qj[1]);In=(Qnext[0]-c,Qnext[1])
                edge=det(Ip,In)/(2*dot(Ip,Ip)*dot(In,In));minedge=min(minedge,edge)
                E=kernel(w+(j+1)*delta)
                local['edge_kernel']=max(local['edge_kernel'],abs(edge-E)/max(mp.mpf('1e-100'),abs(edge)))
            # Opposite-focus shift is tested through raw tangent intersections.
            shifted=[canon(w+2*K+j*delta) for j in range(N)]
            shiftQ,_=raw_outer(shifted,a,b);shiftbp,_,_=shoelaces(shiftQ,c)
            local['focus_shift']=max(local['focus_shift'],abs(bm-shiftbp)/abs(bm))
            reversebp,reversebm,_=shoelaces(list(reversed(Q)),c)
            local['reversal']=max(local['reversal'],abs(reversebp+bp)/abs(bp),abs(reversebm+bm)/abs(bm))
            repeatbp,repeatbm,_=shoelaces(Q*3,c)
            local['repeat_scaling']=max(local['repeat_scaling'],abs(repeatbp*repeatbm/(bp*bm)-9))
            lam=mp.mpf('2.7');scaledQ=[(lam*p[0],lam*p[1]) for p in Q]
            sbp,sbm,_=shoelaces(scaledQ,lam*c)
            local['spatial_scale']=max(local['spatial_scale'],abs(sbp*sbm*lam**4/(bp*bm)-1))
            phase_rows.append({'w_over_K':fstr(frac),'Bplus':fstr(bp),'Bminus':fstr(bm),'product':fstr(bp*bm)})
        variation=(max(products)-min(products))/abs(products[0])
        if N%2: assert variation<mp.mpf('1e-40'), (N,tau,ktext,variation)
        assert mindet>0 and minfocus>0 and minout>0 and minedge>0
        assert max(local.values())<mp.mpf('1e-40'), (N,tau,ktext,local)
        for name in global_max:global_max[name]=max(global_max[name],local[name])
        records.append({'k':ktext,'N':N,'tau':tau,'kind':kind,'phase_count':len(phase_rows),
                        'a':fstr(a),'b':fstr(b),'outer_axis_order':'x_longer' if Ao>Bo else 'y_longer',
                        'min_tangent_det':fstr(mindet),'min_focus_squared_distance':fstr(minfocus),
                        'min_E_level_minus_one':fstr(minout),'min_translated_inverse_edge':fstr(minedge),
                        'relative_product_variation':fstr(variation),
                        'relative_Bplus_variation':fstr((max(bps)-min(bps))/abs(bps[0])),
                        'max_residuals':{x:fstr(y) for x,y in local.items()},'phases':phase_rows})
        print('family',len(records),'/',len(specifications),ktext,N,tau,'variation',fstr(variation),flush=True)
    # Wrong object controls at a representative star with reversed outer axes.
    # Constancy can also occur for a different invariant, so compare values.
    k=mp.mpf('0.65');m=k*k;kp=mp.sqrt(1-m);alpha=mp.mpf('1.3');beta=alpha*kp
    N,tau=5,2;K=mp.ellipk(m);v=2*K*tau/N;delta=2*v
    sn=lambda u:mp.ellipfun('sn',u,m);cn=lambda u:mp.ellipfun('cn',u,m);dn=lambda u:mp.ellipfun('dn',u,m)
    a,b=alpha*dn(v)/cn(v),beta/cn(v);c=alpha*k;Ao,Bo=a*dn(v)/cn(v),b/cn(v)
    controls=[]
    for w in [mp.mpf('0.233')*K,mp.mpf('0.977')*K]:
        P=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)];Q,_=raw_outer(P,a,b)
        bp,bm,_=shoelaces(Q,c);op,om,_=shoelaces(P,c)
        fo=(0,mp.sqrt(Bo**2-Ao**2)) if Bo>Ao else (mp.sqrt(Ao**2-Bo**2),0)
        Fp,_=inverse(Q,fo);Fm,_=inverse(Q,(-fo[0],-fo[1]))
        # Deliberate library bug: use k instead of m=k^2 at fixed intended axes.
        badP=[(-a*mp.ellipfun('sn',w+j*delta,k),b*mp.ellipfun('cn',w+j*delta,k)) for j in range(N)]
        cross=det(badP[-1],badP[0]);nx=(badP[0][1]-badP[-1][1])/cross;ny=(badP[-1][0]-badP[0][0])/cross
        controls.append({'w_over_K':fstr(w/K),'correct_outer_product':fstr(bp*bm),
                         'wrong_original_vertices_product':fstr(op*om),
                         'wrong_outer_locus_foci_product':fstr(area(Fp)*area(Fm)),
                         'wrong_library_parameter_closing_edge_caustic_residual':fstr(abs(alpha**2*nx**2+beta**2*ny**2-1))})
    return {'generated_utc':utc(),'mpmath':mp.__version__,'decimal_precision':mp.mp.dps,
            'method':'physical tangent-to-caustic start, Euclidean reflection and second ellipse ray hit; raw tangent intersections, actual center-inclusive Euclidean inversion, signed shoelace',
            'not_interval_certified':True,'families':len(records),'genuine_closed_orbits':genuine_orbits,
            'vertices_checked':points,'max_residuals':{x:fstr(y) for x,y in global_max.items()},
            'records':records,'wrong_object_controls':controls}


if __name__=='__main__':
    modes=sys.argv[1:] or ['exact','numeric']
    if 'exact' in modes:
        (OUT/'EXACT_ALGEBRA_RESULTS.json').write_text(json.dumps(exact_checks(),indent=2)+'\n')
        (OUT/'EXACT_GEOMETRY_RESULTS.json').write_text(json.dumps(exact_geometry(),indent=2)+'\n')
        print('Exact algebra and geometric constructions completed.',flush=True)
    if 'numeric' in modes:
        (OUT/'NUMERICAL_GEOMETRY_RESULTS.json').write_text(json.dumps(numeric_checks(),indent=2)+'\n')
        print('Numerical physical geometry completed.',flush=True)
