#!/usr/bin/env python3
"""Independent exact controls; no network, no input mutations. Python 3 + SymPy.
Usage: python audit_verify.py [path-to-frozen-submission]
Outputs reproducible JSON. Source texts and data corpora are not required.
"""
import contextlib, hashlib, io, json, random, runpy, sys
from pathlib import Path
import sympy as s
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'submission'
MANIFEST_HASH='43493ad880a6f0a210fe75246301ab81d7575884050b182e63f4e4b71389cf2d'
PARTIAL_HASH='134d3fc65f864d0407fe9135ebd814c0d2c82706f40028c6a8795bd8159587ce'
checks={}
def check(group,condition):
    if not bool(condition):raise AssertionError((group,checks.get(group,0)+1))
    checks[group]=checks.get(group,0)+1
check('frozen_integrity',hashlib.sha256((ROOT/'SHA256SUMS.json').read_bytes()).hexdigest()==MANIFEST_HASH)
check('frozen_integrity',hashlib.sha256((ROOT/'PARTIAL.md').read_bytes()).hexdigest()==PARTIAL_HASH)
manifest=json.loads((ROOT/'SHA256SUMS.json').read_text())
check('frozen_integrity',{r['path'] for r in manifest['files']}=={p.name for p in ROOT.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'})
for r in manifest['files']:
    data=(ROOT/r['path']).read_bytes()
    check('frozen_integrity',len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'])
out=io.StringIO()
with contextlib.redirect_stdout(out):author=runpy.run_path(str(ROOT/'verify.py'))
check('author_replay',out.getvalue().encode()==(ROOT/'CONTROL_RESULTS.json').read_bytes())
check('author_replay',author['checks']==240)
z=author['z']; a,b=s.symbols('a b');rng=random.Random(20000190)
def W(F,a,b):
    E=F*s.diag(a,a,1)*F.T*s.diag(b,b,1)
    return (2*E*F-s.trace(E)*F).applyfunc(s.factor)
def chart(F):
    # Independently transcribed supplement Eq. (1), confirmed from rendered page.
    def f(M):
        f11,f12,f13,f21,f22,f23,f31,f32,f33=list(M)
        n=-f33*(f12*f13*f33-f13**2*f32+f22*f23*f33-f23**2*f32)
        d=f11*f12*f31*f33-f11*f13*f31*f32+f12**2*f32*f33-f12*f13*f32**2+f21*f22*f31*f33-f21*f23*f31*f32+f22**2*f32*f33-f22*f23*f32**2
        return s.expand(n),s.expand(d)
    return f(F),f(F.T)
def label(M):
    if M.rank()!=2:return (0,0,0)
    qs=[n*d for n,d in chart(M)]
    return (1,int(all(q>0 for q in qs)),int(any(q==0 for q in qs)))
def count_projective(B,G):
    c=author['chart_count'](B+z*G)
    c=tuple(c[k] for k in ['real_rank_two','positive_in_chart','at_least_one_zero_q'])
    if G.det()==0:c=tuple(x+y for x,y in zip(c,label(G)))
    return c
B=s.Matrix([[-7,2,16],[5,-4,4],[-20,25,-70]]);G=s.diag(1,2,3);H=s.diag(2,s.Rational(1,2),1)
Bh=H.inv().T*B;T=s.Matrix([[0,0,0],[0,0,-1],[0,1,0]])
# Independent polynomial ideal computations settle *all* calibration pairs for fixtures.
ideal_results={}
for name,F,expected in [('base',B,[a-4,b-25]),('transformed',Bh,[a+s.Rational(112,377),b+s.Rational(1925,67)]),('critical',T,[a-b]),('infeasible_diagonal',s.diag(1,2,0),[a*b])]:
    gb=s.groebner(list(W(F,a,b)),a,b)
    check('calibration_ideal',list(gb)==expected)
    ideal_results[name]=[str(p) for p in gb]
# New independent exact rank certificates, rather than trusting rank() alone.
uv=[(-1,0),(-1,1),(-2,0),(-2,1),(-3,-1),(-3,2),(-4,1)]
rank_certificates={}
for name,base in [('base',B),('transformed',Bh),('critical',T)]:
    direction=H.inv().T*G if name=='transformed' else G
    pairs=[]
    for u,v in uv:
        x=s.Matrix([u,v,1]);y=(base*x).cross(direction*x)
        check('pencil_rank',y[2]!=0 and (y.T*base*x)[0]==0 and (y.T*direction*x)[0]==0)
        pairs.append((x,y))
    D=s.Matrix([[y[j]*x[i] for j in range(3) for i in range(3)] for x,y in pairs])
    cols=D.rref()[1];minor=D[:,list(cols)].det()
    check('pencil_rank',len(cols)==7 and minor!=0)
    check('pencil_rank',s.Matrix.hstack(s.Matrix(list(base)),s.Matrix(list(direction))).rank()==2)
    rank_certificates[name]={'columns_zero_based':list(cols),'minor_determinant':str(minor)}
# Prove the critical matches remain cheiral for *every* positive common focal.
f=s.symbols('f',positive=True)
for u,v in uv:
    u=s.Integer(u);v=s.Integer(v);up=-(2*v*v+3)/u;Z=f/(up-u)
    X=s.Matrix([u*Z/f,v*Z/f,Z]);Xp=X+s.Matrix([1,0,0]);K=s.diag(f,f,1)
    check('critical_continuum',Z.is_positive)
    check('critical_continuum',(K*X)/Z==s.Matrix([u,v,1]))
    check('critical_continuum',(K*Xp)/Z==s.Matrix([up,v,1]))
# New generic real-camera fixtures from exact rational quaternion rotations.
noncritical_cameras=0;critical_cameras=0
for case in range(80):
    w,x,y,t=[s.Integer(rng.randint(-4,4)) for _ in range(4)]
    norm=w*w+x*x+y*y+t*t
    if norm==0:continue
    U=s.Matrix([[w*w+x*x-y*y-t*t,2*(x*y-w*t),2*(x*t+w*y)],
                [2*(x*y+w*t),w*w-x*x+y*y-t*t,2*(y*t-w*x)],
                [2*(x*t-w*y),2*(y*t+w*x),w*w-x*x-y*y+t*t]])/norm
    tx,ty,tz=[s.Integer(rng.randint(-5,5)) for _ in range(3)]
    if (tx,ty,tz)==(0,0,0):continue
    skew=s.Matrix([[0,-tz,ty],[tz,0,-tx],[-ty,tx,0]])
    f1=s.Rational(rng.randint(1,7),rng.randint(1,4));f2=s.Rational(rng.randint(1,7),rng.randint(1,4))
    F=s.diag(1/f2,1/f2,1)*skew*U*s.diag(1/f1,1/f1,1)
    check('physical_cameras',U.T*U==s.eye(3) and U.det()==1 and F.rank()==2)
    check('physical_cameras',W(F,f1*f1,f2*f2)==s.zeros(3))
    nd=chart(F)
    check('physical_cameras',all(n-focal*focal*d==0 for (n,d),focal in zip(nd,[f1,f2])))
    if all(n*d!=0 for n,d in nd):noncritical_cameras+=1
    else:critical_cameras+=1
# Arbitrary rank-two matrices need not be physically feasible. Nonzero chart values
# still must solve the algebraic essential equations; positivity is checked separately.
generic_rank_two=0;chart_zeros=0
for case in range(100):
    L=s.Matrix(3,2,[rng.randint(-6,6) for _ in range(6)])
    R=s.Matrix(2,3,[rng.randint(-6,6) for _ in range(6)])
    F=L*R
    if F.rank()!=2:continue
    nd=chart(F)
    check('arbitrary_rank_two',all(nd[i]==author['nd'](F if i==0 else F.T) for i in range(2)))
    if all(d!=0 for n,d in nd):
        generic_rank_two+=1
        check('arbitrary_rank_two',W(F,s.cancel(nd[0][0]/nd[0][1]),s.cancel(nd[1][0]/nd[1][1]))==s.zeros(3))
    else:chart_zeros+=1
# A universal polynomial certificate, not a randomized inference: after clearing
# chart denominators, all nine essential residuals are divisible by det(F).
v=s.symbols('x0:9'); FF=s.Matrix(3,3,v)
(nn1,dd1),(nn2,dd2)=chart(FF)
PP=FF*s.diag(nn1,nn1,dd1)*FF.T*s.diag(nn2,nn2,dd2)
cleared=2*PP*FF-s.trace(PP)*FF;detpoly=s.Poly(FF.det(),*v)
for residual in cleared:
    _,remainder=s.Poly(residual,*v).div(detpoly)
    check('universal_chart_sufficiency',remainder.is_zero)
# Independent Tarski oracle uses exact rational real-root isolation, no matrix
# signature and no numerical approximation. A shared root gives a zero sign.
def isolation_tarski(p,h):
    p=s.Poly(p,z).sqf_part();h=s.Poly(h,z)
    if p.degree()==0 or h.is_zero:return 0
    common=s.gcd(p,h);answer=0
    for interval,_ in p.intervals():
        lo,hi=interval
        if lo==hi:answer+=s.sign(h.eval(lo));continue
        if common.degree()>0 and common.count_roots(lo,hi)>0:continue
        while h.count_roots(lo,hi)>0 or h.eval(lo)==0 or h.eval(hi)==0:
            lo,hi=p.refine_root(lo,hi,steps=1)
        answer+=s.sign(h.eval(lo))
    return answer
for case in range(100):
    degree=rng.randint(1,5)
    p=s.Poly(sum(rng.randint(-7,7)*z**j for j in range(degree))+rng.choice([-3,-2,-1,1,2,3])*z**degree,z)
    if case%7==0:p=p*s.Poly((z-rng.randint(-3,3))**2,z)
    h=s.Poly(sum(rng.randint(-5,5)*z**j for j in range(rng.randint(1,8))),z)
    if case%5==0:h=h*p.diff()
    if case%11==0:h=h*p
    check('tarski_isolation',author['tq'](p.as_expr(),h.as_expr())==isolation_tarski(p,h))
# Known-root pencils cover repeated roots, nonreal pairs, rank-one roots, degree loss.
known=[(s.diag(z-1,z+2,z-3),[-2,1,3]),(s.diag(z,z,1),[0]),
       (s.Matrix([[z,1,0],[0,z,1],[0,0,1]]),[0]),
       (s.Matrix([[z,-1,0],[1,z,0],[0,0,z-2]]),[2]),
       (s.Matrix([[1,z,0],[0,1,z],[0,0,1]]),[])]
for pencil,roots in known:
    for _ in range(5):
        L=s.eye(3);R=s.eye(3)
        for M in (L,R):
            for k in range(5):
                i,j=rng.sample(range(3),2);M[i,:]=M[i,:]+rng.randint(-3,3)*M[j,:]
        P=L*pencil*R
        expected=tuple(sum(label(P.subs(z,r))[j] for r in roots) for j in range(3))
        c=author['chart_count'](P)
        check('known_root_pencils',tuple(c[k] for k in ['real_rank_two','positive_in_chart','at_least_one_zero_q'])==expected)
# The affine function's documented omission of infinity is repaired by an explicit
# wrapper in this test. GL(2,Q) changes of pencil basis must preserve total counts.
for base,direction,expected in [(B,G,(1,1,0)),(Bh,H.inv().T*G,(1,0,0)),(T,G,(1,0,1))]:
    for A in [s.Matrix([[0,1],[1,0]]),s.Matrix([[1,1],[0,1]]),s.Matrix([[1,-2],[3,1]]),s.Matrix([[-3,0],[0,2]]),s.Matrix([[2,3],[1,2]])]:
        check('projective_reparameterization',A.det()!=0)
        check('projective_reparameterization',count_projective(A[0,0]*base+A[0,1]*direction,A[1,0]*base+A[1,1]*direction)==expected)
# Lower affine degrees and repeated infinity: infinity is counted once only.
N=s.Matrix([[0,1,0],[0,0,1],[0,0,0]])
for BB,GG in [(s.eye(3),N),(s.eye(3),s.diag(0,0,1)),(s.diag(1,1,0),s.diag(0,0,1)),(s.eye(3),s.diag(0,1,1))]:
    check('degree_loss_infinity',count_projective(BB,GG)==(1,0,1))
# Explicit zero and rank guard controls; no infinity multiplicity double counting.
for P in [s.zeros(3),s.diag(z,0,1),T+z*T]:
    try:author['chart_count'](P)
    except ValueError:check('invalid_finite_locus',True)
    else:check('invalid_finite_locus',False)
# All-epsilon proof has exact symbolic factors, with pole and boundary endpoints.
t,e=s.symbols('t e');M=s.Matrix([[1,2,1],[2,1,2],[t+2,2*t+1,t+2]])
focal1=-(t+2)*(2*t-1)/(4*(t-1)*(t+1));focal2=-(t+2)*(2*t+1)/4
check('pole_symbolic',W(M,focal1,focal2)==s.zeros(3))
check('pole_symbolic',list(s.groebner(list(W(M.subs(t,-1),a,b)),a,b))==[1])
# At the exact pole, no finite positive calibration exists despite positive side limits.
for value in [-2,-s.Rational(1,2),s.Rational(1,2),1]:
    nd=chart(M.subs(t,value));check('pole_symbolic',any(n*d==0 for n,d in nd))
result={'problem_id':20000190,'author_manifest_sha256':MANIFEST_HASH,'author_partial_sha256':PARTIAL_HASH,
        'sympy_version':s.__version__,'author_exact_assertions_replayed':240,'new_exact_checks':sum(checks.values()),
        'check_groups':checks,'calibration_ideals':ideal_results,'rank_certificates':rank_certificates,
        'random_physical_camera_fixtures':{'noncritical':noncritical_cameras,'chart_degenerate':critical_cameras},
        'random_rank_two_fixtures':{'denominators_nonzero':generic_rank_two,'chart_denominator_zero':chart_zeros},
        'verdict':'PASS_WITH_SCOPE_NOTES','full_resolution':False,'author_packet_modified':False}
print(json.dumps(result,indent=2,sort_keys=True))
