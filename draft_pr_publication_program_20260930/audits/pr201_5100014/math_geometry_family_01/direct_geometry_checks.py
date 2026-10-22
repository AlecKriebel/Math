#!/usr/bin/env python3
"""Independent direct conic geometry checks; numerical evidence, never proof."""
import math, json

def need(c, message):
    if not c:
        raise RuntimeError(message)

def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def area(ps): return sum(cross(p,ps[(i+1)%len(ps)]) for i,p in enumerate(ps))/2

def orbit(a,b,lam,t,n):
    p=(a*math.cos(t),b*math.sin(t)); points=[]
    # Tangency directions from p to confocal caustic. Find next boundary via
    # oriented chord direction in the positive half-plane, then reflect.
    normal=(p[0]/(a*a),p[1]/(b*b))
    nn=math.hypot(*normal); inward=(-normal[0]/nn,-normal[1]/nn)
    tangent=(-inward[1],inward[0])
    # Joachimsthal normal component sqrt(lam)/(a*b*|normal|).
    s=math.sqrt(lam)/(a*b*nn)
    need(0<s<1, 'invalid incidence')
    velocity=(s*inward[0]-math.sqrt(1-s*s)*tangent[0],s*inward[1]-math.sqrt(1-s*s)*tangent[1])
    # Set positive angular orientation.
    if cross(p,velocity)<0:
        velocity=(s*inward[0]+math.sqrt(1-s*s)*tangent[0],s*inward[1]+math.sqrt(1-s*s)*tangent[1])
    for i in range(n):
        points.append(p)
        vx,vy=velocity
        dist=-2*(p[0]*vx/(a*a)+p[1]*vy/(b*b))/(vx*vx/(a*a)+vy*vy/(b*b))
        need(dist>0,'nonforward collision')
        p=(p[0]+dist*vx,p[1]+dist*vy)
        normal=(p[0]/(a*a),p[1]/(b*b)); nn2=dot(normal,normal)
        vdot=dot(velocity,normal)
        velocity=(vx-2*vdot*normal[0]/nn2,vy-2*vdot*normal[1]/nn2)
    closure=math.hypot(p[0]-points[0][0],p[1]-points[0][1])
    return points,closure

def quantities(a,b,ps,m):
    ns=[(p[0]/(a*a),p[1]/(b*b)) for p in ps]
    outer=[]; feet=[]; normal_sum=0
    for i,u in enumerate(ns):
        v=ns[(i+1)%len(ns)]; d=cross(u,v)
        need(abs(d)>1e-13,'parallel consecutive tangent lines')
        outer.append(((v[1]-u[1])/d,(u[0]-v[0])/d))
        h=(1-dot(u,m))/dot(u,u)
        feet.append((m[0]+h*u[0],m[1]+h*u[1]))
        normal_sum += 2*cross(u,v)*dot(u,v)/(dot(u,u)*dot(v,v))
    return area(outer),area(feet),normal_sum

def run():
    rows=[]
    a,b=2.,1.; lam=a*a*b*b/(a+b)**2
    for t in [0.,.113,.4,.79,1.123,1.5]:
        ps,closure=orbit(a,b,lam,t,6)
        need(closure<1e-12,'N6 closure failed')
        aa,base,s=quantities(a,b,ps,(0.,0.))
        for m in [(0.,0.),(.7,-1.3),(10.,-8.),(math.sqrt(3),0.)]:
            aa2,pedal,_=quantities(a,b,ps,m)
            residual=pedal-base-dot(m,m)*s/8
            need(abs(residual)<2e-11,'isotropic quadratic identity failed')
            rows.append(dict(a=a,b=b,lam=lam,N=6,t=t,M=m,closure=closure,A_outer=aa,A_pedal=pedal,product=aa*pedal,isotropic_residual=residual))
    for m in [(0.,0.),(.7,-1.3),(10.,-8.),(math.sqrt(3),0.)]:
        vals=[r['product'] for r in rows if tuple(r['M'])==m]
        need(max(vals)-min(vals)<2e-9,'N6 product phase variation')
    # Tune several primitive periods directly by collision iteration; float diagnostics.
    def advance(lam,n):
        ps,_=orbit(2.,1.,lam,.173,n+1)
        return sum(math.atan2(cross((u[0]/2,u[1]),(v[0]/2,v[1])),dot((u[0]/2,u[1]),(v[0]/2,v[1]))) for u,v in zip(ps,ps[1:]))
    for n,w in [(10,1),(10,3),(14,3),(14,5)]:
        lo,hi=1e-8,1-1e-9
        for iteration in range(60):
            mid=(lo+hi)/2
            if advance(mid,n)<2*math.pi*w:lo=mid
            else:hi=mid
        lam=(lo+hi)/2; products=[]; coefficients=[]
        for t in [.173,.4,.8,1.2]:
            ps,closure=orbit(2.,1.,lam,t,n)
            need(closure<2e-10,'tuned orbit closure')
            aa,base,ss=quantities(2.,1.,ps,(0.,0.))
            aa2,ped,_=quantities(2.,1.,ps,(.7,-1.3))
            need(abs(ped-base-(.7**2+1.3**2)*ss/8)<2e-11,'star isotropic formula')
            products.append(aa*ped);coefficients.append(aa*ss)
        spread=max(products)-min(products)
        need(spread<2e-8,'primitive higher-period product variation')
        rows.append(dict(numerical_period=True,N=n,w=w,lam=lam,product_spread=spread,coefficient_spread=max(coefficients)-min(coefficients)))
    # Circle, stars, and repeated traversals remain signed sums.
    for n,w in [(6,1),(10,3),(14,3),(18,5),(6,2)]:
        r=3.; t=.271; delta=2*math.pi*w/n
        ps=[(r*math.cos(t+i*delta),r*math.sin(t+i*delta)) for i in range(n)]
        m=(.6,-1.1)
        aa,ped,s=quantities(r,r,ps,m)
        expected_outer=n*r*r*math.tan(delta/2)
        expected_ped=n*r*r*math.sin(delta)/2+n*dot(m,m)*math.sin(2*delta)/8
        need(abs(aa-expected_outer)<2e-11,'circle outer formula failed')
        need(abs(ped-expected_ped)<2e-11,'circle pedal formula failed')
        rows.append(dict(circle=True,N=n,w=w,A_outer=aa,A_pedal=ped,product=aa*ped,least_period=n//math.gcd(n,w)))
    return rows

if __name__=='__main__':
    print(json.dumps({'label':'floating point regression evidence, not proof','checks':run()},indent=2))
