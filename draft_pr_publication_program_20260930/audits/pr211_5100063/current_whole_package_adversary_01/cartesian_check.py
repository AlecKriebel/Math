from pathlib import Path
import json, math, datetime
import mpmath as mp
mp.mp.dps=90
OUT=Path(__file__).resolve().parent

def dot(x,y):return sum(a*b for a,b in zip(x,y))
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def mul(s,x):return tuple(s*a for a in x)
def area(x):return sum(det(x[i],x[(i+1)%len(x)]) for i in range(len(x)))/2

def raw(n,tau,k,phase,scale=1):
    K=mp.ellipk(k*k);v=2*K*tau/n;C=mp.ellipfun("cn",v,k*k);d=mp.ellipfun("dn",v,k*k)
    alpha=mp.mpf(scale);beta=alpha*mp.sqrt(1-k*k);a=alpha*d/C;b=beta/C;c=alpha*k
    p=(a*mp.cos(phase),b*mp.sin(phase));first=p
    z=(p[0]/alpha,p[1]/beta);r2=dot(z,z);fac=mp.sqrt(r2-1)
    tc=((z[0]-z[1]*fac)/r2,(z[1]+z[0]*fac)/r2)
    tangent=(alpha*tc[0],beta*tc[1]);di=add(tangent,mul(-1,p))
    vertices=[];q=[];reflection=[];caustic=[]
    for j in range(n):
        vertices.append(p)
        lam=-2*(p[0]*di[0]/a**2+p[1]*di[1]/b**2)/(di[0]**2/a**2+di[1]**2/b**2)
        nxt=add(p,mul(lam,di))
        x=(p[0]/a**2,p[1]/b**2);y=(nxt[0]/a**2,nxt[1]/b**2);de=det(x,y)
        q.append(((y[1]-x[1])/de,(x[0]-y[0])/de))
        # The discriminant of the caustic intersection quadratic must vanish.
        A=di[0]**2/alpha**2+di[1]**2/beta**2;B=2*(p[0]*di[0]/alpha**2+p[1]*di[1]/beta**2);E=p[0]**2/alpha**2+p[1]**2/beta**2-1
        caustic.append(abs(B*B-4*A*E)/max(1,abs(B*B),abs(4*A*E)))
        normal=(nxt[0]/a**2,nxt[1]/b**2);di=add(di,mul(-2*dot(di,normal)/dot(normal,normal),normal));p=nxt
    inverses=[];minimum=[]
    for f in [(c,mp.mpf(0)),(-c,mp.mpf(0))]:
        invers=[];dist=[]
        for x in q:
            z=add(x,mul(-1,f));D=dot(z,z);dist.append(D);invers.append(add(f,mul(1/D,z)))
        inverses.append(area(invers));minimum.append(min(dist))
    return dict(product=inverses[0]*inverses[1],areas=inverses,close=mp.sqrt(dot(add(p,mul(-1,first)),add(p,mul(-1,first))))/a,caustic=max(caustic),focus_min=min(minimum),q=q,axes_reversed=(a*d/C<b/C))

def main():
    rows=[];maxspread=mp.mpf(0);maxclose=mp.mpf(0);maxcaustic=mp.mpf(0);scale_error=mp.mpf(0);reversal_error=mp.mpf(0)
    phases=list(map(mp.mpf,["0.12","0.73","2.4","4.1"]))
    for n in [3,5,7,9,11,15,21]:
      for tau in range(1,(n+1)//2):
       if math.gcd(n,tau)!=1:continue
       for ks in ["0.08","0.6","0.99"]:
        k=mp.mpf(ks);rs=[raw(n,tau,k,p) for p in phases];base=rs[0]["product"];spread=max(abs(x["product"]-base)/abs(base) for x in rs);maxspread=max(maxspread,spread);maxclose=max(maxclose,max(x["close"] for x in rs));maxcaustic=max(maxcaustic,max(x["caustic"] for x in rs))
        if n in [3,7,21] and tau in [1,(n-1)//2]:
            scaled=raw(n,tau,k,phases[0],mp.mpf("2.5"));scale_error=max(scale_error,abs(scaled["product"]*mp.mpf("2.5")**4/base-1))
        q=rs[0]["q"];c=k
        av=[]
        for f in [(c,mp.mpf(0)),(-c,mp.mpf(0))]:
            inv=[]
            for x in reversed(q):
                z=add(x,mul(-1,f));inv.append(add(f,mul(1/dot(z,z),z)))
            av.append(area(inv))
        reversal_error=max(reversal_error,abs(av[0]*av[1]/base-1))
        assert base>0 and all(x["focus_min"]>0 for x in rs)
        rows.append(dict(N=n,tau=tau,k=ks,relative_phase_spread=mp.nstr(spread,8),closure=mp.nstr(max(x["close"] for x in rs),8),caustic_discriminant=mp.nstr(max(x["caustic"] for x in rs),8),reversed_outer_axes=rs[0]["axes_reversed"],product=mp.nstr(base,18)))
    result=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),method="New direct Cartesian caustic tangent, physical reflection, 2x2 tangent intersections and original-focus inversion; Jacobi used only to select the closed ellipse pair.",precision=mp.mp.dps,interval_certified=False,families=len(rows),phases_per_family=len(phases),max_relative_phase_spread=mp.nstr(maxspread,10),max_relative_closure=mp.nstr(maxclose,10),max_caustic_discriminant_residual=mp.nstr(maxcaustic,10),scale_relative_error=mp.nstr(scale_error,10),reversal_relative_error=mp.nstr(reversal_error,10),reversed_outer_axis_families=sum(x["reversed_outer_axes"] for x in rows),rows=rows)
    assert maxspread<mp.mpf("1e-65") and maxclose<mp.mpf("1e-65") and maxcaustic<mp.mpf("1e-65")
    (OUT/"CARTESIAN_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="rows"},indent=2))
if __name__=="__main__":main()
