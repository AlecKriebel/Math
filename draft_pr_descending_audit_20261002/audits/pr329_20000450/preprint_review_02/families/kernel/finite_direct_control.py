"""Fresh direct Tate-law enumeration; curve points and [5] oracle independent of R."""
import json

def residual(x,b,p):
    # Formula copied only from manuscript table, used as prediction, never oracle.
    co=[5,5*(b*b-5*b+1),b**4-7*b**3+44*b*b-38*b+1,
        b*(b**4+3*b**3-26*b*b+127*b-9),b*b*(b**4+3*b**3+19*b*b-248*b+36),
        b**3*(b**4+3*b**3-71*b*b+322*b-84),b**4*(b**4-12*b**3+94*b*b-293*b+126),
        5*b**5*(b**3-10*b*b+36*b-25),5*b**6*(2*b*b-13*b+16),10*b**7*(b-3),5*b**8]
    ans=0
    for a in co:ans=(ans*x+a)%p
    return ans

summary=[];full=[];plane_collisions=[];mutants={'alter_R_x8':0,'drop_ordinate_branch':0}
tot=0
for p in [19,29,59,71,79,89,101,109]:
    roots5=[r for r in range(p) if r*r%p==5]
    r=roots5[0] if roots5 else None
    delta_roots=[d for d in range(p) if d*d%p==(5+2*r)%p] if r is not None else []
    inv=lambda z:pow(z%p,-1,p)
    count={'p':p,'smooth_Tate_fibers':0,'enumerated_affine_points':0,'full_kernel_fibers':0,'inverse_checked_residual_points':0,'cuspidal_plane_fibers':0}
    for b in range(p):
        if b**5*(b*b-11*b-1)%p==0:continue
        a1=(1-b)%p;a2=(-b)%p;a3=(-b)%p
        def on(P):
            return P is None or (P[1]**2+a1*P[0]*P[1]+a3*P[1]-P[0]**3-a2*P[0]**2)%p==0
        def neg(P):
            return None if P is None else (P[0],(-P[1]-a1*P[0]-a3)%p)
        def plus(P,Q):
            if P is None:return Q
            if Q is None:return P
            if P[0]==Q[0] and P[1]!=Q[1]:
                assert Q==neg(P);return None
            u,w=P;v,z=Q
            if P==Q:
                den=2*w+a1*u+a3
                if den%p==0:return None
                slope=(3*u*u+2*a2*u-a1*w)*inv(den)%p
            else:slope=(z-w)*inv(v-u)%p
            intercept=(w-slope*u)%p
            xx=(slope*slope+a1*slope-a2-u-v)%p
            yy=(-(slope+a1)*xx-intercept-a3)%p
            result=(xx,yy);assert on(result)
            return result
        points=[(u,w) for u in range(p) for w in range(p) if on((u,w))]
        ker=[]
        for P in points:
            assert plus(P,neg(P)) is None
            double=plus(P,P)
            five=plus(plus(double,double),P)
            if five is None:ker.append(P)
        ker=set(ker)
        expected={P for P in points if P[0]*(P[0]-b)*residual(P[0],b,p)%p==0}
        assert expected==ker
        assert plus((0,0),(0,0))==(b,b*b%p)
        assert plus((b,b*b%p),(0,0))==(b,0)
        assert len(ker) in (4,24)
        byx={}
        for u,w in ker:
            assert (2*w+(1-b)*u-b)%p!=0
            byx.setdefault(u,[]).append(w)
        assert all(len(ws)==2 for ws in byx.values())
        mutants['drop_ordinate_branch']+=int(len(byx)!=len(ker))
        alter={P for P in points if P[0]*(P[0]-b)*(residual(P[0],b,p)+b*P[0]**8)%p==0}
        mutants['alter_R_x8']+=int(alter!=ker)
        if len(ker)==24:full.append({'p':p,'beta':b})
        count['full_kernel_fibers']+=int(len(ker)==24)
        count['smooth_Tate_fibers']+=1;count['enumerated_affine_points']+=len(points);tot+=len(points)
        if r is None or not delta_roots:continue
        delta=delta_roots[0];phi=(1+r)*inv(2)%p;c=(11+5*r)*inv(2)%p
        lam=10*b*r*inv(11-5*r-2*b)%p
        if lam in (0,(-5*r)%p,(-c)%p):raise AssertionError('Tate smooth fiber mapped to excluded lambda')
        alpha=(1-r*inv(5))%p;gamma=2*r*inv(5)%p
        k=4*(lam+5*r)*inv(r)%p;q=(5+2*r)*k*k%p
        cubic_a1=((-26+10*r)*lam-20*r)%p
        cubic_a2=((42-86*r*inv(5))*lam*lam+(-100+100*r)*lam+500+200*r)%p
        cubic_a3=(-112+48*r)*lam*lam*(lam+5*r)*inv(5)%p
        cusp=-(25+10*r)*inv(4)%p
        count['cuspidal_plane_fibers']+=int(lam==cusp)
        images={}
        for u,w in ker:
            if u in (0,b):continue
            xi=q*(u-b)%p
            vv=(w+((1-b)*u-b)*inv(2))%p
            eta=k**3*(5+2*r)*delta*vv%p
            assert (eta*eta-xi**3-cubic_a2*xi*xi-cubic_a1*cubic_a3*xi-(5-2*r)*cubic_a3*cubic_a3)%p==0
            zz=(cubic_a3*inv(xi)-alpha*lam)%p;tt=(zz-(5+2*r))%p
            aa=(40+20*r+8*lam)%p;bb=(aa+5)%p
            denX=(aa+4*r*tt)%p;denY=20*xi*(zz+gamma*lam)%p
            assert denX!=0 and denY!=0
            X=(bb-tt*tt)*inv(denX)%p;Y=eta*zz*inv(denY)%p
            Pval=2*(X**5-10*X**3*Y*Y+5*X*Y**4)+5*phi*(X*X+Y*Y)**2-5*pow(phi,3,p)*(X*X+Y*Y)+c
            assert (Pval+lam*(X*X+Y*Y-1)**2)%p==0
            images.setdefault((X,Y),[]).append((u,w))
            count['inverse_checked_residual_points']+=1
        for image,lifts in images.items():
            if len(lifts)>1:plane_collisions.append({'p':p,'lambda':lam,'beta':b,'image':image,'lifts':lifts})
    summary.append(count)
assert all(mutants.values()) and full
print(json.dumps({'status':'FINITE_PASS','mechanism':'Enumerate uncompleted Tate equation and compute 5P=(2P+2P)+P by independent line intersection',
 'per_prime':summary,'enumerated_points_total':tot,'full25_examples':full[:12],
 'collision_examples':plane_collisions[:12],'collision_instances':len(plane_collisions),
 'mutant_detection_counts':mutants,
 'scope':'Finite implementation controls only. Universal algebra, iff proof and map-domain exclusions are separate artifacts; rational kernel counts are not geometric counts.'},indent=2))
