"""High precision direct original-polygon geometry. Numerical evidence only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,time
import mpmath as mp

HERE=Path(__file__).resolve().parent
mp.mp.dps=180
started=time.monotonic()
tolerance=mp.mpf('1e-90')
maxima={}
checks=0
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def add(p,q): return (p[0]+q[0],p[1]+q[1])
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def mul(x,p): return (x*p[0],x*p[1])
def area(points): return mp.fsum(det(points[j],points[(j+1)%len(points)]) for j in range(len(points)))/2
def residual(name,x,scale=1):
    global checks
    e=abs(x)/max(mp.mpf(1),abs(scale))
    maxima[name]=max(maxima.get(name,mp.mpf(0)),e)
    if e>tolerance: raise AssertionError((name,mp.nstr(e,30)))
    checks+=1
def require(name,condition):
    global checks
    if not condition: raise AssertionError(name)
    checks+=1
def constructions(points):
    feet=[];anti=[]
    for p,q in zip(points,points[1:]+points[:1]):
        side=sub(q,p);normal=(-side[1],side[0]);h=dot(normal,p)
        foot=mul(h/dot(normal,normal),normal)
        cp=det(p,q);hp=dot(p,p);hq=dot(q,q)
        corner=((hp*q[1]-p[1]*hq)/cp,(p[0]*hq-hp*q[0])/cp)
        feet.append(foot);anti.append(corner)
        residual('actual_foot_on_side',det(sub(foot,p),side),mp.sqrt(dot(side,side)*dot(p,p)))
        residual('actual_foot_perpendicular',dot(foot,side),mp.sqrt(dot(foot,foot)*dot(side,side)))
        residual('actual_antipedal_line_first',dot(p,corner)-hp,hp)
        residual('actual_antipedal_line_second',dot(q,corner)-hq,hq)
    return feet,anti

families=[]
for n in (3,5,7,9,11,13,15):
    for tau in range(1,(n+1)//2):
        if math.gcd(n,tau)==1:
            for k in ('0.17','0.61','0.93'):
                families.append((n,tau,k))
for n,tau in ((3,1),(5,2),(21,10),(51,25),(101,50),(201,100)):
    for k in ('1e-30','0.9999999999999999999999999999999999999999'):
        families.append((n,tau,k))
for n,tau in ((51,1),(101,1),(201,1),(101,49),(201,98)):
    for k in ('0.07','0.88'):
        families.append((n,tau,k))

records=[]
for n,tau,kstr in families:
    k=mp.mpf(kstr);m=k*k;K=mp.ellipk(m);v=2*K*tau/n;delta=2*v
    b0=mp.sqrt(1-m);cv=mp.ellipfun('cn',v,m);dv=mp.ellipfun('dn',v,m)
    a=dv/cv;b=b0/cv;aa=a*a;bb=b*b;gap=bb-b0*b0
    residual('confocal_axes',aa-1-bb+b0*b0,aa)
    require('strict_caustic',0<gap<bb and aa>bb>0)
    phases=(mp.mpf(0),K*mp.sqrt(2)/7,K*mp.sqrt(3)/5)
    phase_records=[]
    for phase in phases:
        points=[(-a*mp.ellipfun('sn',phase+j*delta,m),b*mp.ellipfun('cn',phase+j*delta,m)) for j in range(n)]
        closing=(-a*mp.ellipfun('sn',phase+n*delta,m),b*mp.ellipfun('cn',phase+n*delta,m))
        residual('closure_x',closing[0]-points[0][0],a)
        residual('closure_y',closing[1]-points[0][1],b)
        require('least_period_arithmetic',math.gcd(n,tau)==1)
        winding=mp.mpf(0);mins={'vertex_cross':mp.inf,'pedal_cross':mp.inf,'contact_fraction':mp.inf,'caustic_segment_margin':mp.inf}
        for j,p in enumerate(points):
            q=points[(j+1)%n];prev=points[(j-1)%n];side=sub(q,p)
            residual('outer_ellipse',p[0]**2/aa+p[1]**2/bb-1)
            cp=det(p,q);require('finite_antipedal_actual_determinant',cp>0)
            mins['vertex_cross']=min(mins['vertex_cross'],cp)
            winding+=mp.atan2(cp,dot(p,q))
            normal=(-side[1],side[0]);h=dot(normal,p)
            residual('caustic_actual_side_tangency',normal[0]**2+b0*b0*normal[1]**2-h*h,h*h)
            contact=(normal[0]/h,b0*b0*normal[1]/h)
            fraction=dot(sub(contact,p),side)/dot(side,side)
            residual('contact_actual_segment',det(sub(contact,p),side),mp.sqrt(dot(side,side)))
            require('contact_strictly_inside',0<fraction<1)
            mins['contact_fraction']=min(mins['contact_fraction'],fraction)
            mins['caustic_segment_margin']=min(mins['caustic_segment_margin'],1-fraction)
            nu=(p[0]/aa,p[1]/bb);incoming=sub(p,prev)
            reflected=sub(incoming,mul(2*dot(incoming,nu)/dot(nu,nu),nu))
            residual('reflection_actual_cartesian',det(reflected,side),mp.sqrt(dot(reflected,reflected)*dot(side,side)))
            require('reflection_forward',dot(reflected,side)>0)
        residual('actual_winding',winding-2*mp.pi*tau,2*mp.pi*tau)
        feet,anti=constructions(points)
        for j,q in enumerate(feet):
            cross=det(q,feet[(j+1)%n]);require('positive_origin_pedal_edge',cross>0)
            mins['pedal_cross']=min(mins['pedal_cross'],cross)
        ap=area(feet);au=area(anti);product=ap*au
        # F formula is a secondary cross-check; the primary area uses line intersections.
        edge_sum=mp.fsum((dot(points[j],points[j])*dot(points[(j+1)%n],points[(j+1)%n])-(dot(points[j],points[j])+dot(points[(j+1)%n],points[(j+1)%n]))*dot(points[j],points[(j+1)%n])/2)/det(points[j],points[(j+1)%n]) for j in range(n))
        residual('actual_area_vs_support_line_formula',au-edge_sum,au)
        if phase==phases[0]:
            reverse=list(reversed(points));rf,ra=constructions(reverse)
            residual('reversed_pedal_area',area(rf)+ap,ap)
            residual('reversed_antipedal_area',area(ra)+au,au)
            repeat=points*2;pf,pa=constructions(repeat)
            residual('repeated_pedal_area',area(pf)-2*ap,ap)
            residual('repeated_antipedal_area',area(pa)-2*au,au)
            residual('repeated_product',area(pf)*area(pa)-4*product,product)
        phase_records.append({'phase_K':mp.nstr(phase/K,30),'pedal_area':mp.nstr(ap,60),'antipedal_area':mp.nstr(au,60),'product':mp.nstr(product,60),'minima':{key:mp.nstr(value,30) for key,value in mins.items()}})
        if len(phase_records)>1:
            # Baseline is retained at full precision, never reconstructed from receipt strings.
            residual('odd_product_phase_invariance',product-baseline,product)
        else: baseline=product
    records.append({'N':n,'tau':tau,'modulus':kstr,'outer_a':mp.nstr(a,35),'outer_b':mp.nstr(b,35),'phases':phase_records})

# Direct rotating circular odd stars, using explicit Cartesian vertices.
circle_records=[]
for n,tau in ((3,1),(5,1),(5,2),(9,4),(101,50)):
    theta=2*mp.pi*tau/n;R=mp.mpf('1.7');want=n*n*R**4*mp.sin(theta)**2/4
    for phase in (mp.mpf(0),mp.sqrt(2)):
        points=[(R*mp.cos(phase+j*theta),R*mp.sin(phase+j*theta)) for j in range(n)]
        foot,anti=constructions(points);got=area(foot)*area(anti)
        residual('circular_formula',got-want,want)
    circle_records.append({'N':n,'tau':tau,'radius':str(R),'product':mp.nstr(want,60)})

# Excluded even parity: same canonical family, genuine finite reflected trajectories.
k=mp.mpf('0.73');m=k*k;K=mp.ellipk(m);n=4;delta=K;v=K/2
a=mp.ellipfun('dn',v,m)/mp.ellipfun('cn',v,m);b=mp.sqrt(1-m)/mp.ellipfun('cn',v,m)
even_products=[]
for phase in (mp.mpf(0),K/2):
    p=[(-a*mp.ellipfun('sn',phase+j*delta,m),b*mp.ellipfun('cn',phase+j*delta,m)) for j in range(n)]
    foot,anti=constructions(p);even_products.append(area(foot)*area(anti))
require('even_N4_product_noninvariant',abs(even_products[1]-even_products[0])>mp.mpf('0.01'))

data={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'precision_digits':mp.mp.dps,'tolerance':str(tolerance),'geometry_checks':checks,'noncircular_families':len(records),'noncircular_phases':3*len(records),'circular_families':len(circle_records),'max_normalized_residuals':{key:mp.nstr(value,40) for key,value in maxima.items()},'records':records,'circle_records':circle_records,'excluded_N4_products':[mp.nstr(x,60) for x in even_products],'elapsed_seconds':round(time.monotonic()-started,3),'scope':'Diagnostics and falsification search; universal proof is separately audited, and sampling is not a proof.'}
out=HERE/'CARTESIAN_NUMERIC_CHECKS.json';out.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'status':'PASS','families':len(records),'phases':3*len(records),'checks':checks,'max_error':mp.nstr(max(maxima.values()),30),'elapsed_seconds':data['elapsed_seconds'],'receipt_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
