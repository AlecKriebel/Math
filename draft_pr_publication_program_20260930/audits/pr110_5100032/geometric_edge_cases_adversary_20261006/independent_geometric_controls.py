#!/usr/bin/env python3
"""Independent geometry; no submitted verifier/reviewer imports or execution.

Exact rational endpoint / antipedal linear solves, plus a small numerical
reconstruction by caustic tangent normals and outer-ellipse intersections.
All requirements remain effective under Python -O.
"""
import fractions, hashlib, json, math, pathlib, sys
F = fractions.Fraction
checks = 0

def require(value, why):
    global checks
    checks += 1
    if not value:
        raise RuntimeError(why)

def near(x, y, why, tolerance=2e-9):
    require(abs(x-y) <= tolerance * max(1.0, abs(x), abs(y)), why)

def dot(p, q):
    return p[0]*q[0]+p[1]*q[1]

def cross(p, q):
    return p[0]*q[1]-p[1]*q[0]

def sub(p, q):
    return p[0]-q[0], p[1]-q[1]

def rational_vertex(a, b, t):
    return a*(1-t*t)/(1+t*t), 2*b*t/(1+t*t)

def direct_antipedal_squared(A, B, focus):
    u, v = sub(A, focus), sub(B, focus)
    du, dv, determinant = dot(u,u), dot(v,v), cross(u,v)
    require(determinant != 0, "singular direct antipedal solve")
    Q = ((du*v[1]-u[1]*dv)/determinant,
         (u[0]*dv-du*v[0])/determinant)
    require(dot(Q,u) == du and dot(Q,v) == dv, "antipedal defining equations")
    return dot(Q,Q)

exact = []
for ai, bi, ci in ((5,3,4), (13,5,12), (17,8,15)):
    a, b, c = F(ai), F(bi), F(ci)
    require(c*c == a*a-b*b, "focal identity")
    cases = [(F(0),F(1,10)), (F(0),F(1,2)), (F(0),F(1)),
             (F(0),F(2)), (F(0),F(10)), (F(1,2),F(2)),
             (F(-2),F(-1,2))]
    for ta, tb in cases:
        A, B = rational_vertex(a,b,ta), rational_vertex(a,b,tb)
        dx, dy = sub(B,A)
        m, k = (dy,-dx), cross(A,B)
        M = dot(m,m)
        H0 = a*a*m[0]*m[0] + b*b*m[1]*m[1]
        lam = (H0-k*k)/M
        require(k > 0 and M > 0, "left-oriented nonzero chord")
        require(0 < lam < b*b, "strict nested elliptical caustic")
        require(H0*H0 == 4*a*a*b*b*lam*M, "rational chord discriminant")
        require((k-c*m[0])*(k+c*m[0]) == (b*b-lam)*M,
                "positive focal-height product")
        coefficients = {}
        for sigma in (1,-1):
            hnum = k-sigma*c*m[0]
            require(hnum > 0, "focus lies on inner side of chord")
            rA, rB = a-sigma*c*A[0]/a, a-sigma*c*B[0]/a
            require(rA > 0 and rB > 0, "positive focal endpoint distances")
            require(rA*rA == dot(sub(A,(sigma*c,F(0))),sub(A,(sigma*c,F(0)))),
                    "first focal distance")
            require(rB*rB == dot(sub(B,(sigma*c,F(0))),sub(B,(sigma*c,F(0)))),
                    "second focal distance")
            qsq = direct_antipedal_squared(A,B,(sigma*c,F(0)))
            coeff = rA*rB/hnum
            require(qsq == coeff*coeff*M, "ordinary norm equals positive focal product / height")
            require(rA*rB == (a*a*hnum*hnum+b*b*lam*M)/H0,
                    "normal-coordinate focal product")
            coefficients[sigma] = coeff
        predicted = 2*c*dy/H0*(-a*a+b*b*lam/(b*b-lam))
        require(coefficients[1]-coefficients[-1] == predicted,
                "ordinary-distance difference per-edge coefficient")
        exact.append({"axes": [ai,bi,ci], "half_angles": [str(ta),str(tb)],
                      "lambda": str(lam), "q_plus_over_sqrt_M": str(coefficients[1]),
                      "q_minus_over_sqrt_M": str(coefficients[-1]),
                      "signed_difference_coefficient": str(predicted)})

# Explicit excluded-boundary and false-generalization controls.
a,b,c = F(5),F(3),F(4)
A, B = rational_vertex(a,b,F(0)), rational_vertex(a,b,F(1,2))
qplus2 = direct_antipedal_squared(A,B,(c,F(0)))
qminus2 = direct_antipedal_squared(A,B,(-c,F(0)))
require(qplus2/qminus2 == F(169,1369), "backtracking ratio is exactly 13/37")
require(qplus2 != qminus2, "tangent closed backtrack is a negative control")
hyper_A, hyper_B = rational_vertex(a,b,F(-1,2)), rational_vertex(a,b,F(1,2))
hdx,hdy = sub(hyper_B,hyper_A)
hm,hk = (hdy,-hdx),cross(hyper_A,hyper_B)
hyper_lambda = (a*a*hm[0]**2+b*b*hm[1]**2-hk*hk)/dot(hm,hm)
require(hyper_lambda == 16 and hyper_lambda > b*b, "excluded hyperbolic-caustic line")
require(hk-c*hm[0] < 0, "one focus outside this excluded chord half-plane")
for boundary_lambda in (F(0),F(9)):
    require(not (0 < boundary_lambda < b*b), "degenerate endpoints excluded")

def step(P, lam, a=5.0, b=3.0):
    """Select the forward tangent from P; never use the submitted chord formula."""
    ca, cb = math.sqrt(a*a-lam),math.sqrt(b*b-lam)
    X, Y = P[0]/ca, P[1]/cb
    phi, theta = math.atan2(Y,X),math.acos(1/math.hypot(X,Y))
    options = []
    for u in (phi-theta,phi+theta):
        n = math.cos(u)/ca,math.sin(u)/cb
        v = -n[1],n[0]
        t = -2*(P[0]*v[0]/(a*a)+P[1]*v[1]/(b*b)) / (v[0]**2/(a*a)+v[1]**2/(b*b))
        if t > 1e-12:
            Q = P[0]+t*v[0],P[1]+t*v[1]
            options.append((Q,n))
    require(len(options)==1, "unique forward tangent branch")
    return options[0]

def path(lam, N, start):
    points = [(5*math.cos(start),3*math.sin(start))]
    normals,advance = [],0.0
    for i in range(N):
        P = points[-1]
        Q,n = step(P,lam)
        t0,t1 = math.atan2(P[1]/3,P[0]/5),math.atan2(Q[1]/3,Q[0]/5)
        delta = (t1-t0)%(2*math.pi)
        require(0 < delta < math.pi, "strict positive half-turn advance")
        advance += delta
        points.append(Q)
        normals.append(n)
    return points,normals,advance

def closed_lambda(N,winding):
    lo,hi = 1e-7,9.0-1e-8
    require(path(lo,N,0)[2] < 2*math.pi*winding < path(hi,N,0)[2], "winding bracket")
    for _ in range(52):
        mid = (lo+hi)/2
        if path(mid,N,0)[2] < 2*math.pi*winding:
            lo=mid
        else:
            hi=mid
    return (lo+hi)/2

def q_numeric(A,B,f):
    u,v = sub(A,f),sub(B,f)
    d,du,dv = cross(u,v),dot(u,u),dot(v,v)
    require(abs(d)>1e-8, "finite numerical antipedal determinant")
    Q = ((du*v[1]-u[1]*dv)/d,(u[0]*dv-du*v[0])/d)
    near(dot(Q,u),du,"numerical antipedal equation A")
    near(dot(Q,v),dv,"numerical antipedal equation B")
    return math.hypot(*Q)

def inspect_cycle(points,lam,winding):
    N=len(points)-1
    near(math.hypot(*(sub(points[-1],points[0]))),0,"orbit closes",tolerance=3e-9)
    qs={1:[],-1:[]}
    tangency_residual=0.0
    reflection_residual=0.0
    for i in range(N):
        P,Q=points[i],points[i+1]
        chord=sub(Q,P)
        length=math.hypot(*chord)
        n=(chord[1]/length,-chord[0]/length)
        rho=dot(n,P)
        near(P[0]**2/25+P[1]**2/9,1,"vertex on outer ellipse")
        require(rho>0,"inner caustic lies left")
        residual=rho*rho-((25-lam)*n[0]**2+(9-lam)*n[1]**2)
        tangency_residual=max(tangency_residual,abs(residual))
        near(residual,0,"every edge has the same caustic")
        require(rho-4*n[0]>0 and rho+4*n[0]>0,"both foci lie strictly inside support")
        for sigma in (1,-1):
            qs[sigma].append(q_numeric(P,Q,(sigma*4.0,0.0)))
        incoming=sub(P,points[(i-1)%N]); outgoing=chord
        incoming=tuple(x/math.hypot(*incoming) for x in incoming)
        outgoing=tuple(x/length for x in outgoing)
        normal=(P[0]/25,P[1]/9)
        normal=tuple(x/math.hypot(*normal) for x in normal)
        reflected=tuple(incoming[j]-2*dot(incoming,normal)*normal[j] for j in (0,1))
        err=math.hypot(*(sub(reflected,outgoing)))
        reflection_residual=max(reflection_residual,err)
        near(err,0,"actual billiard reflection law",tolerance=2e-8)
    near(sum(qs[1]),sum(qs[-1]),"ordinary focal distance sums agree")
    reverse=list(reversed(points))
    rplus=sum(q_numeric(reverse[i],reverse[i+1],(4.0,0.0)) for i in range(N))
    rminus=sum(q_numeric(reverse[i],reverse[i+1],(-4.0,0.0)) for i in range(N))
    near(rplus,sum(qs[1]),"reversal preserves ordinary plus sum")
    near(rminus,sum(qs[-1]),"reversal preserves ordinary minus sum")
    repeated=points[:-1]+points
    tplus=sum(q_numeric(repeated[i],repeated[i+1],(4.0,0.0)) for i in range(2*N))
    tminus=sum(q_numeric(repeated[i],repeated[i+1],(-4.0,0.0)) for i in range(2*N))
    near(tplus,2*sum(qs[1]),"double traversal plus")
    near(tminus,2*sum(qs[-1]),"double traversal minus")
    return {"N":N,"winding":winding,"lambda":lam,
            "sum_plus":sum(qs[1]),"sum_minus":sum(qs[-1]),
            "maximum_tangency_residual":tangency_residual,
            "maximum_reflection_residual":reflection_residual}

cycles=[]
diamond=[(5.0,0.0),(0.0,3.0),(-5.0,0.0),(0.0,-3.0),(5.0,0.0)]
cycles.append(inspect_cycle(diamond,225/34,1))
for N,w in ((3,1),(5,1),(5,2),(7,2)):
    lam=closed_lambda(N,w)
    for start in (0.0,0.417):
        points,normals,advance=path(lam,N,start)
        near(advance,2*math.pi*w,"closed winding")
        result=inspect_cycle(points,lam,w)
        result["start_parameter"]=start
        result["total_parameter_advance"]=advance
        cycles.append(result)

require(len(exact)==21 and len(cycles)==9,"purposeful control set size")
root=pathlib.Path(__file__).resolve().parent
pins=[]
for path in [root/"independent_geometric_controls.py",
             root.parent/"original_head_authentication_20261006/original_attempt/PROOF.md",
             root.parent/"original_head_authentication_20261006/original_attempt/source_record.json",
             root.parent/"primary_sources_private/reznik_garcia_koiller_arxiv_v11.pdf",
             root.parent/"primary_sources_private/reznik_garcia_koiller_published2021.pdf"]:
    body=path.read_bytes()
    pins.append({"path":str(path),"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest()})
print(json.dumps({"schema":"pr110-independent-geometric-controls/v1","mode":"optimized" if sys.flags.optimize else "normal",
                  "checks":checks,"exact_chords":exact,"closed_cycle_controls":cycles,
                  "negative_controls":{"excluded_backtrack_sum_ratio":"13/37",
                                       "excluded_hyperbolic_lambda":"16",
                                       "excluded_degenerate_lambda_endpoints":["0","9"]},
                  "input_pins":pins,
                  "limits":"Numerical cycles are falsification controls, not proof or novelty evidence."},indent=2))
