#!/usr/bin/env python3
"""Independent noninterval physical diagnostic. No Jacobi orbit construction.
Tangent point on scaled caustic circle, then second intersection with outer ellipse.
All checks use explicit exceptions, hence survive Python -O.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
from datetime import datetime, timezone
HERE=Path(__file__).resolve().parent
RUNTIME=HERE.parent.parent.parent/'audits/pr200_5100007/math_algebra_family_01/runtime_packages'
sys.path.insert(0,str(RUNTIME))
import mpmath as mp
mp.mp.dps=200
COUNTS={}
MAX={}
def require(kind, cond, detail=''):
    COUNTS[kind]=COUNTS.get(kind,0)+1
    if not cond: raise RuntimeError(kind+': '+str(detail))
def near(kind,x,scale=1,tol=mp.mpf('1e-48')):
    err=abs(x)/max(mp.mpf(1),abs(scale))
    MAX[kind]=max(MAX.get(kind,mp.mpf(0)),err)
    require(kind,err<tol,mp.nstr(err,12))
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def add(p,q): return (p[0]+q[0],p[1]+q[1])
def mul(c,p): return (c*p[0],c*p[1])
def norm(p): return mp.sqrt(dot(p,p))
def step(p,a,b,lam,validate=False):
    ca,cb=mp.sqrt(a*a-lam),mp.sqrt(b*b-lam)
    wx,wy=p[0]/ca,p[1]/cb
    r2=wx*wx+wy*wy
    z=mp.sqrt(r2-1)
    contact=(ca*(wx-z*wy)/r2,cb*(wy+z*wx)/r2)
    v=sub(contact,p)
    tau=-2*(p[0]*v[0]/a**2+p[1]*v[1]/b**2)/(v[0]**2/a**2+v[1]**2/b**2)
    q=add(p,mul(tau,v))
    if validate:
        near('boundary',q[0]**2/a**2+q[1]**2/b**2-1)
        near('caustic_boundary',contact[0]**2/ca**2+contact[1]**2/cb**2-1)
        near('tangency',contact[0]*v[0]/ca**2+contact[1]*v[1]/cb**2, norm(v)/cb)
        require('strict_contact',tau>1)
        require('forward_step',cross(p,q)>0)
    return q

def orbit(a,b,lam,phase,N,validate=False):
    p=(a*mp.cos(phase),b*mp.sin(phase)); pts=[p]; advance=mp.mpf(0)
    for _ in range(N):
        q=step(p,a,b,lam,validate)
        old=mp.atan2(p[1]/b,p[0]/a); new=mp.atan2(q[1]/b,q[0]/a)
        advance+=(new-old)%(2*mp.pi)
        pts.append(q);p=q
    return pts,advance

def find_lambda(a,b,N,w):
    lo=mp.mpf('1e-170')*b*b;hi=(1-mp.mpf('1e-170'))*b*b
    phase=mp.mpf('0.371')
    for _ in range(600):
        mid=(lo+hi)/2
        _,advance=orbit(a,b,mid,phase,N)
        if advance<2*mp.pi*w:lo=mid
        else:hi=mid
    return (lo+hi)/2

def area(pts):return sum(cross(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))/2

def pedal(pts,M):
    feet=[]
    for p,q in zip(pts,pts[1:]+pts[:1]):
        v=sub(q,p);vv=dot(v,v)
        foot=add(p,mul(dot(sub(M,p),v)/vv,v))
        near('projection_parallel',cross(sub(foot,p),v),vv)
        near('projection_perpendicular',dot(sub(M,foot),v),max(vv,norm(M)*norm(v)))
        feet.append(foot)
    return area(feet)

def reflection(pts,a,b):
    for prev,p,q in zip(pts[-1:]+pts[:-1],pts,pts[1:]+pts[:1]):
        vi=mul(1/norm(sub(p,prev)),sub(p,prev));vo=mul(1/norm(sub(q,p)),sub(q,p))
        normal=(p[0]/a**2,p[1]/b**2)
        predicted=sub(vi,mul(2*dot(vi,normal)/dot(normal,normal),normal))
        near('reflection',norm(sub(predicted,vo)))

def exact_n4(mutate=False):
    import sympy as s
    a,b,x,y,D,X,Y=s.symbols('a b x y D X Y',nonzero=True,real=True)
    p=s.Matrix([a*x,b*y]);q=s.Matrix([-a**3*y/D,b**3*x/D])
    determinant=s.det(s.Matrix.hstack(p,q));minus=(q-p).dot(q-p);plus=(q+p).dot(q+p)
    # Algebraic constraints x²+y²=1, D²=b⁴x²+a⁴y². Clear denominators.
    basis=s.groebner([x*x+y*y-1,D*D-b**4*x*x-a**4*y*y],D,x,y,a,b,order='grevlex')
    def zero(name,expr):
        num=s.fraction(s.cancel(expr))[0]
        require(name,basis.reduce(num)[1]==0,str(num))
    zero('exact_boundary_q',q[0]**2/a**2+q[1]**2/b**2-1)
    tangent=s.Matrix([-a*y,b*x])
    zero("exact_reflection_squared",tangent.dot(q-p)**2*plus-tangent.dot(p+q)**2*minus)
    G=b*b*x*x+a*a*y*y
    zero("exact_reflection_sign_margin",D*D-(a*a-b*b)**2*x*x*y*y-G*G)
    # Both tangent dot products D +/- (a²-b²)xy are strictly positive,
    # since D>0 and G>0; squared identity therefore is unsquared reflection.
    # A*B = 8 det(p,q)^4 / (|p-q|² |p+q|²); all M cancel for any parallelogram.
    coeff=9 if mutate else 8
    zero('exact_product',coeff*determinant**4*(a*a+b*b)**2-8*a**4*b**4*minus*plus)
    # Tangency of both distinct sides to lambda=a²b²/(a²+b²).
    lam=a*a*b*b/(a*a+b*b)
    for k,v in enumerate([q-p,-p-q]):
        n=s.Matrix([v[1],-v[0]]);h=n.dot(p if k==0 else q)
        zero('exact_tangency',h*h-(a*a-lam)*n[0]**2-(b*b-lam)*n[1]**2)
    # Arbitrary-M pedal area cancellation, proven for arbitrary nonparallel side directions.
    n0=s.Matrix([a,b]);n1=s.Matrix([x,y]);h0,h1=s.symbols('h0 h1',real=True)
    M=s.Matrix([X,Y]);feet=[]
    for n,h in [(n0,h0),(n1,h1),(-n0,h0),(-n1,h1)]:
        feet.append(M+(h-n.dot(M))*n/n.dot(n))
    B=sum(s.det(s.Matrix.hstack(feet[i],feet[(i+1)%4])) for i in range(4))/2
    expected=2*h0*h1*s.det(s.Matrix.hstack(n0,n1))/(n0.dot(n0)*n1.dot(n1))
    require('exact_arbitrary_M',s.cancel(B-expected)==0)
    return 'AB=8*a^4*b^4/(a^2+b^2)^2; B independent of M for four-sided parallelograms'

def diagnostic(quick=False):
    ratios=['1.0001','2','10'] if not quick else ['2']
    pairs=[(4,1),(8,1),(8,3),(12,1),(12,5),(16,1),(16,3),(16,5),(16,7),(20,1),(20,3),(20,7),(20,9)]
    phases=[mp.mpf(s) for s in ['0','0.173','0.731','1.417']]
    rows=[]
    for ratio in ratios:
        a=mp.mpf(ratio);b=mp.mpf(1)
        Ms=[(mp.mpf(0),mp.mpf(0)),(mp.sqrt(a*a-b*b),mp.mpf(0)),(a/3,-b*mp.mpf('0.7')),(a*100,-b*53)]
        for N,w in pairs:
            require('coprime',math.gcd(N,w)==1)
            lam=find_lambda(a,b,N,w);products=[[] for _ in Ms];bvalues=[]
            for phase in phases:
                allpts,advance=orbit(a,b,lam,phase,N,True);pts=allpts[:-1]
                near('closure',norm(sub(allpts[-1],pts[0])),a)
                near('winding',advance-2*mp.pi*w,N)
                # Every proper initial subsequence stays separated; numerical diagnostic only.
                require('least_period_diagnostic',all(norm(sub(p,pts[0]))>mp.mpf('1e-35') for p in pts[1:]))
                reflection(pts,a,b)
                A=area(pts)
                for j,M in enumerate(Ms):
                    B=pedal(pts,M);products[j].append(A*B);bvalues.append(B)
                    reverse=pts[::-1]
                    near('reversal_area',area(reverse)+A,a*a*N)
                    near('reversal_pedal',pedal(reverse,M)+B,max(1,abs(B)))
                    near('odd_repeat_area',area(pts*3)-3*A,max(1,abs(A)))
                    near('odd_repeat_pedal',pedal(pts*3,M)-3*B,max(1,abs(B)))
            for j,values in enumerate(products):
                for product in values[1:]:near('phase_product',product-values[0],values[0],mp.mpf('1e-43'))
            row={'a':ratio,'b':'1','N':N,'w':w,'lambda':mp.nstr(lam,45),'AB_at_Ms':[mp.nstr(v[0],30) for v in products],'min_B':mp.nstr(min(bvalues),15),'max_B':mp.nstr(max(bvalues),15)}
            rows.append(row);print('CASE',ratio,N,w,'OK',flush=True)
    # Padded odd and N=6 periods: check finite examples to distinguish from an extension.
    excluded=[]
    a=mp.mpf(2);b=mp.mpf(1)
    for N,w,reps in [(3,1,4),(6,1,2),(5,1,4)]:
        lam=find_lambda(a,b,N,w);vals=[]
        for phase in phases:
            pts=orbit(a,b,lam,phase,N)[0][:-1]*reps
            vals.append(area(pts)*pedal(pts,(mp.mpf('0.2'),mp.mpf('0.3'))))
        spread=max(vals)-min(vals)
        require('excluded_padding_variation',abs(spread)>mp.mpf('1e-8'))
        excluded.append({'least_N':N,'list_length':N*reps,'AB_range':[mp.nstr(min(vals),25),mp.nstr(max(vals),25)]})
    # For eligible cases, seek zero/negative pedal areas from direct quadratic in M.
    # B along t*direction is quadratic. Origin slope and coefficients are checked directly.
    signs=[]
    for N,w in [(4,1),(8,1),(8,3),(12,1),(12,5)]:
        lam=find_lambda(a,b,N,w)
        pts=orbit(a,b,lam,mp.mpf('0.217'),N)[0][:-1]
        B0=pedal(pts,(0,0));B1=pedal(pts,(a,b));Bm=pedal(pts,(-a,-b));quad=(B1+Bm)/2-B0;lin=(B1-Bm)/2
        near('central_linear_cancellation',lin,max(1,abs(B0)))
        if abs(quad)>mp.mpf('1e-40'):
            if B0*quad<0:
                t=mp.sqrt(-B0/quad);Bzero=pedal(pts,(t*a,t*b));Bnegative=pedal(pts,(2*t*a,2*t*b))
                near('zero_pedal',Bzero,max(1,abs(B0)),mp.mpf('1e-40'))
                require('negative_pedal',Bnegative<0)
                signs.append({'N':N,'w':w,'root_t':mp.nstr(t,30),'negative_B':mp.nstr(Bnegative,30)})
            else:signs.append({'N':N,'w':w,'quadratic_same_sign':mp.nstr(quad,20)})
        else:signs.append({'N':N,'w':w,'M_dependence_below':'1e-40','B0':mp.nstr(B0,30)})
    return rows,excluded,signs

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mutate-coefficient',action='store_true');parser.add_argument('--exact-only',action='store_true');parser.add_argument('--quick',action='store_true');parser.add_argument('--out',default='independent_results.json');args=parser.parse_args()
    exact=exact_n4(args.mutate_coefficient)
    rows,excluded,signs=([],[],[]) if args.exact_only else diagnostic(args.quick)
    result={'actual_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'optimized':sys.flags.optimize,'mpmath':mp.__version__,'exact_result':exact,'noninterval':True,'cases':rows,'excluded_padding':excluded,'signed_pedal_probes':signs,'counts':COUNTS,'maximum_relative_residuals':{k:mp.nstr(v,12) for k,v in MAX.items()},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','checks':COUNTS,'total_checks':sum(COUNTS.values()),'optimized':sys.flags.optimize,'cases':len(rows),'out':args.out},sort_keys=True))
if __name__=='__main__':main()
