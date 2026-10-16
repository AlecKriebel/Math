"""Independent geometric/divisor diagnostics; finite numerics are not a proof.

Run with the existing scientific runtime and Python -B. No inherited code imported.
"""
import json
import math
from pathlib import Path
from datetime import datetime, timezone
import mpmath as mp
import sympy as sp

mp.mp.dps = 85
HERE = Path(__file__).resolve().parent

def vec_cross(p, q):
    return p[0]*q[1] - p[1]*q[0]

def area(points):
    return sum(vec_cross(points[j], points[(j+1) % len(points)])
               for j in range(len(points))) / 2

def intersect(n1, n2):
    det = vec_cross(n1, n2)
    return ((n2[1]-n1[1])/det, (n1[0]-n2[0])/det)

def make(k, n, wind):
    k = mp.mpf(k)
    K = mp.ellipk(k*k)
    Kp = mp.ellipk(1-k*k)
    sn = lambda z: mp.ellipfun('sn', z, k*k)
    cn = lambda z: mp.ellipfun('cn', z, k*k)
    dn = lambda z: mp.ellipfun('dn', z, k*k)
    v = 2*wind*K/n
    alpha = mp.mpf(3)
    beta = alpha*mp.sqrt(1-k*k)
    a = alpha*dn(v)/cn(v)
    b = beta/cn(v)
    p = lambda z: (a*sn(z), b*cn(z))
    norm = lambda z: (sn(z)/a, cn(z)/b)
    q = lambda z: (a*sn(z)*dn(v)/cn(v), b*cn(z)/cn(v))
    def foot(z, M=(mp.mpf(0), mp.mpf(0))):
        nx, ny = norm(z)
        d = (1-nx*M[0]-ny*M[1])/(nx*nx+ny*ny)
        return M[0]+d*nx, M[1]+d*ny
    def geometric(z, M=(mp.mpf(0), mp.mpf(0)), chord=False):
        normals = [norm(z+2*j*v) for j in range(n)]
        outer = [intersect(normals[j], normals[(j+1) % n]) for j in range(n)]
        feet = [foot(z+2*j*v, M) for j in range(n)]
        if chord:
            pts = [p(z+2*j*v) for j in range(n)]
            feet = []
            for j in range(n):
                p1, p2 = pts[j], pts[(j+1) % n]
                d = p2[0]-p1[0], p2[1]-p1[1]
                normal = d[1], -d[0]
                rhs = normal[0]*p1[0]+normal[1]*p1[1]
                d2 = normal[0]**2+normal[1]**2
                feet.append((rhs*normal[0]/d2, rhs*normal[1]/d2))
        return area(outer), area(feet)
    return locals()

def spread(vals):
    return max(abs(v-vals[0]) for v in vals)/(1+max(abs(v) for v in vals))

def sf(x):
    return mp.nstr(x, 24)

checks = {}

# Independent formal algebra: all assertions are identities modulo the defining
# sn/cn/dn algebraic relations, not empirical special values.
s,c,d,S,C,D,h,A,B = sp.symbols('s c d S C D h A B', nonzero=True)
den = 1-h*s*s*S*S
sm = (s*C*D-S*c*d)/den
sp_ = (s*C*D+S*c*d)/den
cm = (c*C+s*d*S*D)/den
cp = (c*C-s*d*S*D)/den
dm = (d*D+h*s*c*S*C)/den
dp = (d*D-h*s*c*S*C)/den
relations = [c*c+s*s-1,d*d+h*s*s-1,C*C+S*S-1,D*D+h*S*S-1]
G = sp.groebner(relations,c,d,C,D,s,S,h,order='lex')
def zero_relation(expr):
    numerator = sp.cancel(expr).as_numer_denom()[0]
    return G.reduce(sp.Poly(numerator,c,d,C,D,s,S,h).as_expr())[1] == 0
checks['formal_chord_on_line_minus'] = zero_relation(s*D*sm+c*cm-C)
checks['formal_chord_on_line_plus'] = zero_relation(s*D*sp_+c*cp-C)
checks['formal_tangent_intersection_minus'] = zero_relation(sm*s*D/C+cm*c/C-1)
checks['formal_tangent_intersection_plus'] = zero_relation(sp_*s*D/C+cp*c/C-1)
checks['formal_area_dn_identity'] = zero_relation(sm*cp-sp_*cm + S*C/D*(dm+dp))

# The independent pole-collision argument uses sn² and cn ratios at
# K+iK'±v. The two normal directions are equal, hence isotropic parallel.
kp = sp.symbols('kp', positive=True)
nvplus = sp.Matrix([D/(sp.sqrt(h)*C), -sp.I*kp/(sp.sqrt(h)*C)])
nvminus = nvplus.copy()
checks['formal_adjacent_pole_direction_equal'] = nvplus == nvminus
checks['formal_adjacent_pole_wedge_zero'] = sp.det(sp.Matrix.hstack(nvplus,nvminus)) == 0
checks['formal_symbolic_mutant_rejected'] = not zero_relation(sm*cp-sp_*cm - S*C/D*(dm+dp))
a,b,cc,ss,cw = sp.symbols('a b cc ss cw',nonzero=True)
normal=sp.Matrix([ss/a,cc/b])
direct_foot=normal/(normal.dot(normal))
pair_den=1-(1-b*b/(a*a))*ss*ss
pair=sp.Matrix([2*b*ss*cw/pair_den,2*b*cc*cw/pair_den])
mapped=sp.diag(b/a,1)*pair/(2*cw)
checks['formal_center_foot_edge_map']=all(
    sp.rem(sp.cancel(direct_foot[i]-mapped[i]).as_numer_denom()[0],cc*cc+ss*ss-1,cc)==0
    for i in range(2))
assert all(checks.values())

cases = []
for k,n,w in [('0.2',3,1),('0.7',5,1),('0.7',5,2),('0.97',7,3),
              ('0.7',6,1),('0.7',10,1),('0.7',10,3),('0.97',14,5),
              ('0.7',9,2),('0.7',18,7),('0.97',31,15)]:
    x = make(k,n,w)
    K,v,p,q,foot = [x[name] for name in ['K','v','p','q','foot']]
    zs = [K/17,2*K/7,13*K/19]
    values = [x['geometric'](z) for z in zs]
    products = [v1*v2 for v1,v2 in values]
    tangent_residual = max(abs(x['norm'](z-v)[0]*q(z)[0]+x['norm'](z-v)[1]*q(z)[1]-1)
                           for z in zs)
    even_residual = max(abs(a-b)/(1+abs(a)) for z in zs
                        for a,b in zip(x['geometric'](z),x['geometric'](-z)))
    imaginary_sign = max(abs(a+b)/(1+abs(a)) for a,b in
                         zip(x['geometric'](zs[0]),x['geometric'](zs[0]+2j*x['Kp'])))
    assert spread(products) < mp.mpf('1e-65')
    assert tangent_residual < mp.mpf('1e-65')
    assert even_residual < mp.mpf('1e-65')
    assert imaginary_sign < mp.mpf('1e-65')
    cases.append(dict(k=k,n=n,winding=w,product=sf(products[0]),
                      relative_phase_spread=sf(spread(products)),
                      tangent_formula_residual=sf(tangent_residual),
                      evenness_residual=sf(even_residual),
                      imaginary_antiperiod_residual=sf(imaginary_sign)))

mutants = []
for n,w,mode in [(4,1,'excluded_parity'),(8,3,'excluded_parity'),(12,5,'excluded_parity'),
                 (5,2,'off_center'),(5,1,'wrong_chord_feet')]:
    x=make('0.7',n,w)
    zs=[x['K']/17,2*x['K']/7,13*x['K']/19]
    vals=[x['geometric'](z,M=(mp.mpf('0.3'),mp.mpf('0.2')) if mode=='off_center' else (0,0),
                         chord=(mode=='wrong_chord_feet')) for z in zs]
    ss=spread([a*b for a,b in vals])
    print('negative control',n,w,mode,sf(ss),flush=True)
    if mode != 'wrong_chord_feet':
        assert ss > mp.mpf('1e-20'), (n,w,mode,sf(ss))
    mutants.append(dict(n=n,winding=w,mode=mode,relative_phase_spread=sf(ss),
                        discriminating=(ss > mp.mpf('1e-20'))))

trace_checks=[]
k=mp.mpf('0.7'); K=mp.ellipk(k*k); Kp=mp.ellipk(1-k*k)
dn=lambda z:mp.ellipfun('dn',z,k*k)
for q in [1,3,5,7,9,15,31]:
    U=lambda z:sum(dn(z+2*K*j/q) for j in range(q))
    zs=[K/17,mp.mpc(K/5,Kp/7),mp.mpc(2*K/3,Kp/4)]
    vals=[U(z)*U(z+K) for z in zs]
    zero=abs(U(K+1j*Kp))
    assert spread(vals) < mp.mpf('1e-65')
    assert zero < mp.mpf('1e-65')
    trace_checks.append(dict(q=q,relative_product_spread=sf(spread(vals)),reflected_zero=sf(zero)))
for q in [2,4,6]:
    U=lambda z:sum(dn(z+2*K*j/q) for j in range(q))
    vals=[U(z)*U(z+K) for z in [K/17,2*K/7,13*K/19]]
    ss=spread(vals)
    assert ss>mp.mpf('1e-12')
    mutants.append(dict(mode='even_trace_order',q=q,relative_phase_spread=sf(ss)))

pole_checks=[]
for n,w in [(5,1),(6,1),(10,3)]:
    x=make('0.7',n,w)
    eps=mp.mpc('1e-9','2e-10')
    poleA=1j*x['Kp']-x['v']
    poleB=x['K']+1j*x['Kp']+x['v']
    a1,b1=x['geometric'](poleA+eps)
    a2,b2=x['geometric'](poleA+eps/2)
    c1,d1=x['geometric'](poleB+eps)
    c2,d2=x['geometric'](poleB+eps/2)
    res=[abs(a2/a1-2),abs(b2/b1-mp.mpf('0.5')),
         abs(c2/c1-mp.mpf('0.5')),abs(d2/d1-2)]
    assert max(res) < mp.mpf('1e-12')
    pole_checks.append(dict(n=n,winding=w,epsilon=sf(eps),
                            simple_pole_zero_ratio_residuals=list(map(sf,res))))

# Exact finite subgroup enumeration checks the arithmetic implementation and
# deliberately includes composite odd order/star winding and repetitions.
arithmetic=[]
for n in range(3,121):
    if n%4 == 0: continue
    for w in range(1,(n+1)//2):
        if math.gcd(n,w)!=1: continue
        q=n//math.gcd(n,2)
        residues=[(2*w*j)%n for j in range(n)]
        expected=list(range(0,n,n//q))
        assert sorted(set(residues)) == expected
        assert all(residues.count(r)==n//q for r in expected)
        assert q%2==1
        arithmetic.append((n,w,q))

output=dict(utc=datetime.now(timezone.utc).isoformat(),mpmath_dps=mp.mp.dps,
            status='all_assertions_passed',numerical_evidence_is_uncertified=True,
            symbolic=checks,geometric_cases=cases,negative_controls=mutants,
            trace_cases=trace_checks,pole_checks=pole_checks,
            finite_arithmetic_case_count=len(arithmetic),
            universal_scope='Written meromorphic argument is the universal proof; these are diagnostics only.')
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
