"""Independent high-precision focal inversion checker.
No submitted code imports. Vertices after the first are constructed by Euclidean
line/ellipse intersection and specular reflection. Jacobi functions set a closed
family's axes; optional Jacobi comparisons never generate Euclidean successors.
These are floating-point diagnostics, not interval or universal certificates.
"""
import argparse, json, math, time
from pathlib import Path
from datetime import datetime, timezone
import mpmath as mp


def dot(x,y): return x[0]*y[0]+x[1]*y[1]
def det(x,y): return x[0]*y[1]-x[1]*y[0]
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def scale(x,t): return (x[0]*t,x[1]*t)
def unit(x): return scale(x,1/mp.sqrt(dot(x,x)))
def area(pts): return mp.fsum(det(p,pts[(j+1)%len(pts)]) for j,p in enumerate(pts))/2

def focal_area(pts,c):
    inv=[]
    for p in pts:
        v=(p[0]-c,p[1]); inv.append(scale(v,1/dot(v,v)))
    return area(inv)

def geometry(k,N,tau):
    K=mp.ellipk(k*k); v=2*K*mp.mpf(tau)/N
    sn=mp.ellipfun('sn',v,k*k); cn=mp.ellipfun('cn',v,k*k); dn=mp.ellipfun('dn',v,k*k)
    beta=mp.sqrt((1-k)*(1+k))
    return {'k':k,'K':K,'v':v,'N':N,'tau':tau,'alpha':mp.mpf(1),'beta':beta,'a':dn/cn,'b':beta/cn,'snv':sn,'cnv':cn,'dnv':dn}

def orbit(g,theta):
    a,b,beta=g['a'],g['b'],g['beta']; N=g['N']
    p=(a*mp.cos(theta),b*mp.sin(theta)); start=p
    # Map the caustic to a unit circle. Tangency points are explicit and both
    # branches are checked for the prescribed positive orientation.
    z=(p[0],p[1]/beta); zz=dot(z,z)
    foot=scale(z,1/zz); ortho=scale((-z[1],z[0]),mp.sqrt(zz-1)/zz)
    directions=[]
    for sign in [-1,1]:
        t=add(foot,scale(ortho,sign)); tangent=(t[0],beta*t[1])
        d=unit(sub(tangent,p))
        if det(p,d)>0: directions.append(d)
    assert len(directions)==1
    d=directions[0]; pts=[]
    outer=mp.mpf(0); tangent=mp.mpf(0); winding=mp.mpf(0); minimum_return=mp.inf
    initial_d=d
    for j in range(N):
        pts.append(p)
        outer=max(outer,abs((p[0]/a)**2+(p[1]/b)**2-1))
        normal=(d[1],-d[0]); support=dot(normal,p)
        support2=normal[0]**2+beta**2*normal[1]**2
        tangent=max(tangent,abs(support**2-support2)/max(support2,mp.mpf('1e-1000')))
        step=-2*(p[0]*d[0]/a**2+p[1]*d[1]/b**2)/(d[0]**2/a**2+d[1]**2/b**2)
        assert step>0
        pnext=add(p,scale(d,step))
        pscaled=(p[0]/a,p[1]/b); qscaled=(pnext[0]/a,pnext[1]/b)
        turn=mp.atan2(det(pscaled,qscaled),dot(pscaled,qscaled))
        assert turn>0
        winding+=turn
        if j+1<N:
            minimum_return=min(minimum_return,mp.sqrt(((pnext[0]-start[0])/a)**2+((pnext[1]-start[1])/b)**2))
        n=(pnext[0]/a**2,pnext[1]/b**2)
        d=sub(d,scale(n,2*dot(d,n)/dot(n,n)))
        p=pnext
    closure=mp.sqrt(((p[0]-start[0])/a)**2+((p[1]-start[1])/b)**2)
    direction_closure=mp.sqrt(dot(sub(d,initial_d),sub(d,initial_d)))
    return pts,{'closure':closure,'direction_closure':direction_closure,'outer_residual':outer,'caustic_tangency_residual':tangent,'winding_error':abs(winding/(2*mp.pi)-g['tau']),'minimum_earlier_return':minimum_return}

def ssum(g,w):
    return mp.fsum(mp.ellipfun('dn',w+j*2*g['v'],g['k']**2) for j in range(g['N']//2))

def family(k,N,tau,phases,formula=False):
    g=geometry(k,N,tau); values=[]; am=[]; ap=[]; diagnostics=[]; formula_errors=[]
    cr=[]; ss=[]; orient_error=mp.mpf(0)
    for i,phase in enumerate(phases):
        theta=mp.pi*mp.mpf(phase); pts,diag=orbit(g,theta); diagnostics.append(diag)
        A=area(pts); invp=focal_area(pts,k); invm=focal_area(pts,-k)
        values.append(A*invp); ap.append(invp); am.append(invm)
        if i==0:
            rev=list(reversed(pts))
            orient_error=max(abs(A+area(rev))/max(1,abs(A)),abs(invp+focal_area(rev,k))/max(1,abs(invp)),abs(A*invp-area(rev)*focal_area(rev,k))/max(1,abs(A*invp)))
        if formula:
            w=mp.ellipf(theta-mp.pi/2,k*k)
            S=ssum(g,w)
            ca=g['a']*g['b']*g['snv']*g['cnv']/g['dnv']
            errA=abs(A-2*ca*S)/max(1,abs(A))
            # Compare the independently propagated orbit with the canonical map.
            point_error=mp.mpf(0)
            for j in [0,N//3,N-1]:
                z=w+j*2*g['v']; expect=(-g['a']*mp.ellipfun('sn',z,k*k),g['b']*mp.ellipfun('cn',z,k*k))
                point_error=max(point_error,abs((pts[j][0]-expect[0])/g['a']),abs((pts[j][1]-expect[1])/g['b']))
            shifted=ssum(g,w+g['K']+g['v']); ell=4*g['K']/N
            cr.append(invp/shifted); ss.append(S*ssum(g,w+ell/2))
            formula_errors.append(max(errA,point_error))
    denom=max(abs(x) for x in values)
    spread=(max(values)-min(values))/denom
    focus=max(abs(x-y)/max(1,abs(x),abs(y)) for x,y in zip(ap,am))
    summary={'k':mp.nstr(k,50),'N':N,'tau':tau,'phases':len(phases),'relative_product_spread':spread,'focus_equality_error':focus,'orientation_error':orient_error,'representative_product':values[0],'max_closure':max(x['closure'] for x in diagnostics),'max_direction_closure':max(x['direction_closure'] for x in diagnostics),'max_outer_residual':max(x['outer_residual'] for x in diagnostics),'max_tangency_residual':max(x['caustic_tangency_residual'] for x in diagnostics),'max_winding_error':max(x['winding_error'] for x in diagnostics),'minimum_earlier_return':min(x['minimum_earlier_return'] for x in diagnostics),'outer_eccentricity':k/g['a'],'relative_axis_gap':(g['a']-1)/g['a'],'caustic_beta':g['beta']}
    if formula:
        summary['max_area_and_canonical_point_error']=max(formula_errors)
        summary['relative_CR_spread']=(max(cr)-min(cr))/max(abs(x) for x in cr)
        summary['relative_half_shift_product_spread']=(max(ss)-min(ss))/max(abs(x) for x in ss)
    if N==4: summary['N4_product_error']=max(abs(x-4) for x in values)
    return summary

def serialize(x):
    if isinstance(x,dict): return {k:serialize(v) for k,v in x.items()}
    if isinstance(x,list): return [serialize(v) for v in x]
    if isinstance(x,mp.mpf): return mp.nstr(x,18)
    return x

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--max-N',type=int,default=64); parser.add_argument('--dps',type=int,default=90); args=parser.parse_args()
    mp.mp.dps=args.dps; start=time.time(); families=[]
    phases=['0','0.137','0.333','0.5','0.731']
    kvals=['0.00000001','0.6','0.999','0.9999999999']
    for N in range(4,args.max_N+1,4):
        for tau in range(1,N//2):
            if math.gcd(tau,N)!=1: continue
            for ks in kvals:
                # Every admissible coprime star of each N is included at each k.
                families.append(family(mp.mpf(ks),N,tau,phases,formula=N<=12 or (N==args.max_N and tau in [1,N//2-1])))
        print('completed N',N,'families',len(families),'seconds',round(time.time()-start,1),flush=True)
    # Boundary and resolution stress tests. k near 1 makes the caustic thin;
    # large N and tau=1 puts the caustic close to the outer boundary.
    stresses=[]
    for ks,N,tau in [('0.8',256,1),('0.8',1024,1),('0.999999999999999999999999',8,1),('0.999999999999999999999999',12,5),('0.000000000000000000000001',12,5),('0.8',128,63)]:
        stresses.append(family(mp.mpf(ks),N,tau,phases[:3],formula=True))
        print('stress',ks,N,tau,'seconds',round(time.time()-start,1),flush=True)
    # Wrong parity controls intentionally fall outside the theorem.
    controls=[]
    for N,tau in [(3,1),(5,1),(5,2),(6,1),(7,2),(10,1),(10,3),(14,3)]:
        controls.append(family(mp.mpf('0.8'),N,tau,phases,formula=False))
    numeric_metrics=['relative_product_spread','focus_equality_error','orientation_error','max_closure','max_direction_closure','max_outer_residual','max_tangency_residual','max_winding_error']
    maxima={key:max(x[key] for x in families+stresses) for key in numeric_metrics}
    formula_keys=['max_area_and_canonical_point_error','relative_CR_spread','relative_half_shift_product_spread']
    maxima.update({key:max(x[key] for x in families+stresses if key in x) for key in formula_keys})
    result={'created_utc':datetime.now(timezone.utc).isoformat(),'implementation':'Independent Euclidean reflection, not submitted Jacobi successor code','mpmath_version':mp.__version__,'precision_dps':args.dps,'max_N_all_coprime':args.max_N,'family_count':len(families),'family_orbit_count':len(families)*len(phases),'maxima_target_and_stress':maxima,'stress_cases':stresses,'wrong_parity_controls':controls,'families':families,'elapsed_seconds':time.time()-start,'certificate_status':'Floating-point diagnostic only; no interval enclosure and no universal proof.'}
    Path(__file__).with_name('euclidean_results.json').write_text(json.dumps(serialize(result),indent=2)+'\n')
    print(json.dumps(serialize({'maxima':maxima,'controls':controls,'count':len(families),'seconds':time.time()-start}),indent=2))
    assert max(maxima.values())<mp.mpf('1e-45')
    assert all(x['relative_product_spread']>mp.mpf('1e-8') for x in controls)
if __name__=='__main__': main()
