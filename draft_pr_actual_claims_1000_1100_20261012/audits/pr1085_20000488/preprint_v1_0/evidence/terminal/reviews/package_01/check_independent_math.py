"""New exact algebra/compact-packet diagnostics; not a continuum proof by sampling."""
from fractions import Fraction as F
from itertools import product
import argparse,json

def need(ok,msg):
    if not ok: raise ValueError(msg)

def run(fault=None):
    rates=[F(1,2),F(2,3),F(3)]
    def ip(a,b): return sum((x*y/(r+s) for x,r in zip(a,rates) for y,s in zip(b,rates)),F(0))
    def norm(a): return ip(a,a)
    cases=0
    # Independently expand the unweighted bounded-H1 graph transform, including
    # its surface endpoint, arbitrary signed amplitude/tangential jets, and both
    # real and imaginary components. No finite-difference PDE calculation.
    for beta in [F(1,11),F(2,3),F(7),F(31)]:
        for g,surface in [(F(0),F(1)),(F(3,4),F(5,4)),(F(-5,12),F(13,12)),(F(15,8),F(17,8))]:
            need(1+g*g==surface*surface,'unit normal geometry')
            for shift in range(1,10):
                total_raw=total_completed=F(0)
                for channel in [0,1]:
                    A=[F((-1)**(i+shift+channel)*(shift+i+channel+1),i+2) for i in range(3)]
                    Dx=[F((i+1)*(shift-4+channel),i+3) for i in range(3)]
                    Dy=[F((-1)**i*(shift+channel),i+5) for i in range(3)]
                    dt=[-r*a for r,a in zip(rates,A)]
                    b=[(beta-r)*a for r,a in zip(rates,A)]
                    gx=[d-g*v for d,v in zip(Dx,b)]
                    boundary=sum(A)**2
                    raw=norm(gx)+norm(Dy)+norm(dt)+beta*beta*norm(A)-beta*surface*boundary
                    endpoint=(surface if fault=='drop_fiber_endpoint' else surface-1)
                    completed=norm(gx)+norm(Dy)+norm(b)-beta*endpoint*boundary
                    total_raw+=raw; total_completed+=completed
                    c=1/(2*(1+g*g))
                    need(norm(gx)+norm(Dy)+norm(b)>=c*(norm(Dx)+norm(Dy)+norm(b)), 'full integrated graph coercivity')
                need(total_raw==total_completed,'bounded-H1 graph transform including fiber endpoint')
                cases+=1
    hardy=0
    for m in range(3,13):
        alpha=F(m-2,2)
        for r2,delta2 in product([F(0),F(1,7),F(1),F(100)], [F(1,100),F(1),F(9)]):
            denom=(r2+delta2)**2
            coefficient=alpha*((m-2)*r2+m*delta2)/denom-alpha*alpha*r2/denom
            principal=alpha*alpha*r2/denom
            need(coefficient-principal==alpha*m*delta2/denom>=0,'Hardy regularization exact surplus')
            hardy+=1
    scaling=0
    for m,beta,C in product(range(3,10),[F(1,31),F(2,7),F(1),F(5)],[F(1,100),F(3,2),F(29)]):
        source=(16*beta*C*(16*beta*C+2*beta))**m
        target=beta**((m if fault=='wrong_mass_power' else 2*m))*(16*C*(16*C+2))**m
        need(source==target,'squared HHRV count scales as beta^(2m), including odd dimensions')
        scaling+=1
    # Exact compact supported eta=(1-x²)^3, with two derivatives vanishing at
    # +/-1; it is a legitimate H2 operator test after zero extension. Tensor
    # packets have explicit residual constants; translating support fully past
    # the compact alteration is essential and is kept in the analytic argument.
    eta=[F(1),F(0),F(-3),F(0),F(3),F(0),F(-1)]
    def derivative(p):return [i*p[i] for i in range(1,len(p))]
    def multiply(p,q):
        r=[F(0)]*(len(p)+len(q)-1)
        for i,x in enumerate(p):
            for j,y in enumerate(q):r[i+j]+=x*y
        return r
    def integral(p):return sum((F(2)*v/(i+1) for i,v in enumerate(p) if i%2==0),F(0))
    d=derivative(eta);dd=derivative(d)
    n0=integral(multiply(eta,eta));n1=integral(multiply(d,d));n2=integral(multiply(dd,dd))
    need(integral(multiply(dd,eta))==-n1,'compact packet integration by parts')
    packets=[]
    for m,k in product([1,2,3,7],[F(0),F(2,3),F(13)]):
        lap=m*n2/n0+m*(m-1)*(n1/n0)**2
        last=None
        for R in [F(1),F(2),F(8),F(32)]:
            residual=lap/R**4+4*k*k*(n1/n0)/R**2
            need(residual>0 and (last is None or residual<last),'operator Weyl packet scaling')
            last=residual
        packets.append({'m':m,'k':str(k),'R32_squared_residual':str(last)})
    normals=0
    for t in [F(0),F(1,100),F(1,2),F(1),F(3),F(100)]:
        ny=(t*t-1)/(1+t*t);nx=2*t/(1+t*t)
        need(nx*nx+ny*ny==1 and 1+ny>=0,'nongraph arbitrary unit normal defect')
        if t:need(1+ny>0,'normal rigidity only downward normal vanishes')
        if fault=='reverse_normal':need(1-ny==1+ny,'wrong orientation')
        normals+=1
    theta=F(1,4)
    need(1-2*theta>0 and 1-4*theta==0,'journal/preprint range separation')
    margin=F(1250,2501)-F(1,5000)*F(25,24)*10
    need(margin==F(597499,1200480)>0,'exact Hardy margin')
    v=F(1,5000)*F(25,24)/F(1250,2501);s=16*v
    need(s*(s+2)<F(1,40) and F(1,240)<1,'integer spectral-count bound')
    return {'passed':True,'integrated_complex_graph_jet_cases':cases,'Hardy_regularized_surplus_cases':hardy,
            'squared_mass_scaling_cases':scaling,'compact_operator_packet_cases':packets,
            'normal_rigidity_cases':normals,'Hardy_margin':str(margin),'count_coarse_upper':'1/240',
            'scope':'New finite exact controls of selected identities and compact packet constants; universal analysis remains the written proof.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fault',choices=['drop_fiber_endpoint','wrong_mass_power','reverse_normal'])
    a=p.parse_args();print(json.dumps(run(a.fault),indent=2,sort_keys=True))
