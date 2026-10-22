"""Independent real controls; Python -B; existing mpmath only; no writes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'pr200_5100007' / 'math_algebra_family_01' / 'runtime_packages'))
import mpmath as mp
mp.mp.dps = 80
A, B = mp.mpf(4), mp.mpf(1)
a, b = mp.sqrt(A), mp.sqrt(B)
pi = mp.pi

def step(theta, lam):
    alpha, beta = mp.sqrt(A-lam), mp.sqrt(B-lam)
    x,y = a*mp.cos(theta),b*mp.sin(theta)
    X,Y = x/alpha,y/beta
    radius = mp.sqrt(X*X+Y*Y)
    phi = mp.atan2(Y,X)+mp.acos(min(mp.mpf(1),1/radius))
    dx,dy = -mp.sin(phi)/beta,mp.cos(phi)/alpha
    h = -2*(x*dx/A+y*dy/B)/(dx*dx/A+dy*dy/B)
    xn,yn = x+h*dx,y+h*dy
    tn = mp.atan2(yn/b,xn/a)
    delta = mp.atan2(mp.sin(tn-theta),mp.cos(tn-theta))
    assert delta > 0, 'Chosen forward branch failed'
    return theta+delta

def advance(theta,lam,N):
    for j in range(N): theta=step(theta,lam)
    return theta

def closing_lambda(N,r):
    theta=mp.mpf('0.271828182845904523536')
    lo,hi=mp.mpf('1e-40'),B-mp.mpf('1e-65')
    for j in range(250):
        mid=(lo+hi)/2
        if advance(theta,mid,N)-theta < 2*pi*r: lo=mid
        else: hi=mid
    return (lo+hi)/2

def det(U,V): return U[0]*V[1]-U[1]*V[0]
def area(P): return sum(det(U,V) for U,V in zip(P,P[1:]+P[:1]))/2

def polygon(theta,lam,N):
    points=[]
    for j in range(N):
        points.append((a*mp.cos(theta),b*mp.sin(theta)))
        theta=step(theta,lam)
    return points,theta

def foot(U,V,M):
    u,v,w=U[1]-V[1],V[0]-U[0],det(U,V)
    q=(u*M[0]+v*M[1]+w)/(u*u+v*v)
    return M[0]-q*u,M[1]-q*v

print('mpmath_dps =',mp.mp.dps)
for N,r in [(4,1),(8,1),(8,3),(12,1),(12,5)]:
    lam=closing_lambda(N,r)
    max_closure=mp.mpf(0);max_tangency=mp.mpf(0);max_relative_spread=mp.mpf(0)
    first_areas=[]
    for M in [(mp.mpf(0),mp.mpf(0)),(mp.mpf('2.3'),mp.mpf('-1.7')),(mp.mpf(20),mp.mpf(13)),(mp.sqrt(A-B),mp.mpf(0))]:
        products=[]
        for theta in map(mp.mpf,['0.013','0.37','1.271','2.41']):
            P,thetaN=polygon(theta,lam,N)
            max_closure=max(max_closure,abs(thetaN-theta-2*pi*r))
            for U,V in zip(P,P[1:]+P[:1]):
                u,v,w=U[1]-V[1],V[0]-U[0],det(U,V)
                max_tangency=max(max_tangency,abs(((A-lam)*u*u+(B-lam)*v*v-w*w)/(u*u+v*v+w*w)))
            Q=[foot(U,V,M) for U,V in zip(P,P[1:]+P[:1])]
            products.append(area(P)*area(Q))
            # Reversal is required to reverse both signed areas and preserve product.
            assert abs(area(P)*area(Q)-area(list(reversed(P)))*area(list(reversed(Q)))) < mp.mpf('1e-65')
        spread=(max(products)-min(products))/max(mp.mpf(1),max(map(abs,products)))
        max_relative_spread=max(max_relative_spread,spread)
        first_areas.append(products[0])
    assert max_closure < mp.mpf('1e-55')
    assert max_tangency < mp.mpf('1e-55')
    assert max_relative_spread < mp.mpf('1e-55')
    print('N,r =',N,r,'lambda =',mp.nstr(lam,28))
    print('  closure max',mp.nstr(max_closure,5),'tangency max',mp.nstr(max_tangency,5),'relative product spread',mp.nstr(max_relative_spread,5))
    print('  products for M=(0,0),(2.3,-1.7),(20,13),(sqrt(3),0):',','.join(mp.nstr(x,20) for x in first_areas))
print('All real controls passed. These computations support but do not replace the proof.')

# Zero signed pedal area is permitted. Area is an even quadratic in M because
# opposite side lines are centrally related. Infer an exact-zero candidate on
# the x-axis from two values and verify it at independent phases.
lam=closing_lambda(8,3)
def product_at(theta, M, N=8):
    P,_=polygon(theta,lam,N)
    Q=[foot(U,V,M) for U,V in zip(P,P[1:]+P[:1])]
    return area(P)*area(Q)
c0=product_at(mp.mpf('0.37'),(mp.mpf(0),mp.mpf(0)))
c2=product_at(mp.mpf('0.37'),(mp.mpf(1),mp.mpf(0)))-c0
root=mp.sqrt(-c0/c2)
zero_residue=max(abs(product_at(theta,(root,mp.mpf(0)))) for theta in map(mp.mpf,['0.013','0.37','1.271','2.41']))
assert zero_residue < mp.mpf('1e-65')
print('N8/3 zero-pedal control: M=(',mp.nstr(root,30),',0), max |A B| =',mp.nstr(zero_residue,5))

# Scope control: a doubled primitive six-periodic trajectory has 12 listed
# vertices but does not satisfy the theorem's least-period hypothesis.
lam=closing_lambda(6,1)
values=[]
for theta in map(mp.mpf,['0.013','0.37','1.271','2.41']):
    P,_=polygon(theta,lam,6)
    P=P+P
    Q=[foot(U,V,(mp.mpf(0),mp.mpf(0))) for U,V in zip(P,P[1:]+P[:1])]
    values.append(area(P)*area(Q))
assert max(values)-min(values) > mp.mpf('0.1')
print('Excluded nonprimitive N=12-list control, least period6: products =',','.join(mp.nstr(x,16) for x in values))
