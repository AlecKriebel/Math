"""Independent direct physical billiard audit: no Jacobi coordinates used."""
from pathlib import Path
import sys, json, hashlib, datetime, math
sys.path.insert(0, "/Users/alec/Library/Python/3.11/lib/python/site-packages")
import sympy as S
import mpmath as M
D=Path(__file__).resolve().parent
COUNTS={"exact_assertions":0,"numeric_assertions":0}
def exact_zero(z,label):
    z=S.simplify(z)
    COUNTS["exact_assertions"]+=1
    if z != 0: raise AssertionError((label,str(z)))
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def dot(p,q): return sum(x*y for x,y in zip(p,q))
def sub(p,q): return [p[i]-q[i] for i in range(2)]
def add(p,q): return [p[i]+q[i] for i in range(2)]
def mul(t,p): return [t*x for x in p]
def area(P): return sum(det(P[j],P[(j+1)%len(P)]) for j in range(len(P)))/2
def exact_intersection(n,m):
    d=det(n,m)
    if S.simplify(d)==0: raise AssertionError("parallel outer tangents")
    return [S.simplify((m[1]-n[1])/d),S.simplify((n[0]-m[0])/d)]
def exact_projection(f,A,B):
    v=sub(B,A); t=S.simplify(dot(sub(f,A),v)/dot(v,v))
    return [S.simplify(z) for z in add(A,mul(t,v))]
def exact_family(P,a,b,lam,label):
    N=len(P); c=S.sqrt(a*a-b*b)
    normals=[[S.simplify(x/(a*a)),S.simplify(y/(b*b))] for x,y in P]
    V=[exact_intersection(normals[j],normals[(j+1)%N]) for j in range(N)]
    for j in range(N):
        p=P[j]; before=P[(j-1)%N]; after=P[(j+1)%N]
        n=normals[j]
        exact_zero(p[0]**2/a**2+p[1]**2/b**2-1,label+" boundary")
        vi=sub(p,before); vo=sub(after,p)
        li=S.sqrt(S.factor(dot(vi,vi))); lo=S.sqrt(S.factor(dot(vo,vo)))
        ui=mul(1/li,vi); uo=mul(1/lo,vo)
        reflected=sub(ui,mul(2*dot(ui,n)/dot(n,n),n))
        for r,s in zip(reflected,uo): exact_zero(r-s,label+" unit reflection")
        h=[-vo[1],vo[0]]
        exact_zero(dot(h,p)**2-(a*a-lam)*h[0]**2-(b*b-lam)*h[1]**2,label+" common confocal tangent")
        exact_zero(dot(n,V[j])-1,label+" outer line endpoint")
        exact_zero(dot(n,V[(j-1)%N])-1,label+" outer previous endpoint")
        if all(S.simplify(t)==0 for t in sub(V[j],V[(j-1)%N])): raise AssertionError("collapsed side")
    feet={}; Bs={}
    for e in [1,-1]:
        f=[e*c,S.Integer(0)]
        Q=[exact_projection(f,V[(j-1)%N],V[j]) for j in range(N)]
        for j,q in enumerate(Q):
            p=P[j]; n=normals[j]; side=sub(V[j],V[(j-1)%N])
            expected=[a*a*(p[0]+e*c)/(a*a+e*c*p[0]),a*a*p[1]/(a*a+e*c*p[0])]
            for x,y in zip(q,expected): exact_zero(x-y,label+" independent side-foot map")
            exact_zero(dot(n,q)-1,label+" foot lies actual side")
            exact_zero(dot(sub(q,f),side),label+" foot perpendicular actual side")
            exact_zero(dot(q,q)-a*a,label+" auxiliary circle")
        feet[e]=Q
        Bs[e]=S.simplify(area(Q))
    chord_feet={e:[exact_projection([e*c,0],P[j],P[(j+1)%N]) for j in range(N)] for e in [1,-1]}
    inv={e:[mul(1/dot(sub(p,[e*c,0]),sub(p,[e*c,0])),sub(p,[e*c,0])) for p in P] for e in [1,-1]}
    return {"label":label,"N":N,"B_plus":str(Bs[1]),"B_minus":str(Bs[-1]),"product":str(S.simplify(Bs[1]*Bs[-1])),
            "chord_product":str(S.simplify(area(chord_feet[1])*area(chord_feet[-1]))),
            "inverse_product":str(S.simplify(area(inv[1])*area(inv[-1]))),
            "_Bs":Bs,"_inverse":{e:S.simplify(area(inv[e])) for e in [1,-1]}}
def exact_checks():
    a=S.sqrt(21); b=S.Integer(4); lam=S.Rational(336,25)
    H=[[a,0],[-3*a/5,S.Rational(16,5)],[-3*a/5,-S.Rational(16,5)]]
    V=[[0,b],[-S.Rational(21,5),-S.Rational(8,5)],[S.Rational(21,5),-S.Rational(8,5)]]
    rows=[exact_family(H,a,b,lam,"triangle H"),exact_family(V,a,b,lam,"triangle V")]
    for row in rows:
        exact_zero(row["_Bs"][1]*row["_Bs"][-1]-S.Rational(12544,25),"triangle target product")
        exact_zero(S.sympify(row["chord_product"])-S.Rational(7225344,390625),"original chord product")
        exact_zero(S.sympify(row["inverse_product"])-S.Rational(1,324),"original inverse product")
        for e in [1,-1]:
            exact_zero(row["_Bs"][e]-S.Rational(2016,5)*row["_inverse"][-e],"phasewise inverse transfer")
    # Resolve the focal sign assignment instead of presuming it.
    for e in [1,-1]:
        exact_zero(rows[0]["_Bs"][e]-(49*S.sqrt(21)+e*7*S.sqrt(5))/10,"H signed focus value")
        exact_zero(rows[1]["_Bs"][e]-S.Rational(112,5),"V signed focus value")
    t=1/S.sqrt(5)
    even=[exact_family([[2,0],[0,1],[-2,0],[0,-1]],S.Integer(2),S.Integer(1),S.Rational(4,5),"N4 diamond"),
          exact_family([[4*t,t],[-4*t,t],[-4*t,-t],[4*t,-t]],S.Integer(2),S.Integer(1),S.Rational(4,5),"N4 rectangle")]
    for row,val in zip(even,[4,5]):
        for e in [1,-1]: exact_zero(row["_Bs"][e]-val,"even area")
    # Symbolic foot and auxiliary circle hold for the complete real boundary.
    x,y,a,b,c,e=S.symbols("x y a b c e",nonzero=True)
    n=S.Matrix([x/a**2,y/b**2]); f=S.Matrix([e*c,0])
    q=f+(1-(n.dot(f)))/(n.dot(n))*n
    desired=S.Matrix([a*a*(x+e*c)/(a*a+e*c*x),a*a*y/(a*a+e*c*x)])
    substitutions={y**2:b*b*(1-x*x/(a*a)),c**2:a*a-b*b,e**2:1}
    # A Groebner remainder avoids informal use of the boundary relation.
    G=S.groebner([a*a*y*y+b*b*x*x-a*a*b*b,c*c-a*a+b*b,e*e-1],y,c,e,x,a,b)
    for z in list(q-desired)+[desired.dot(desired)-a*a]:
        num=S.together(z).as_numer_denom()[0]
        exact_zero(G.reduce(S.expand(num))[1],"universal focal-foot rational identity")
    for row in rows+even: row.pop("_Bs"); row.pop("_inverse")
    return rows+even

def checknum(x,tol,label):
    COUNTS["numeric_assertions"]+=1
    if abs(x)>tol: raise AssertionError((label,M.nstr(x,30),M.nstr(tol,8)))
def physics_next(p,d,a,b):
    normal=[p[0]/(a*a),p[1]/(b*b)]
    den=d[0]*d[0]/(a*a)+d[1]*d[1]/(b*b)
    t=-2*dot(p,[d[0]/(a*a),d[1]/(b*b)])/den
    q=add(p,mul(t,d))
    n=[q[0]/(a*a),q[1]/(b*b)]
    reflected=sub(d,mul(2*dot(d,n)/dot(n,n),n))
    return q,reflected
def launch(p,a,b,lam):
    # Solve directly for inner-ellipse tangent LINE NORMAL m with p.m=1.
    # Work in normal-angle-free homogeneous slope coordinates m=(1,z)
    # and select the tangent chord with positive oriented ellipse anomaly.
    alpha2=a*a-lam; beta2=b*b-lam
    px,py=p
    # m.p support squared = inner support. Tangency is (px+z*py)^2=alpha2+beta2*z^2.
    A=py*py-beta2; B=2*px*py; C=px*px-alpha2
    if abs(A)<M.mpf("1e-95"):
        roots=[-C/B]
        normals=[[1,roots[0]],[0,1]]
    else:
        disc=B*B-4*A*C
        if disc<0: raise AssertionError("nonreal caustic tangent")
        roots=[(-B+M.sqrt(disc))/(2*A),(-B-M.sqrt(disc))/(2*A)]
        normals=[[M.mpf(1),z] for z in roots]
    choices=[]
    for n in normals:
        raw=[-n[1],n[0]]
        raw=mul(1/M.sqrt(dot(raw,raw)),raw)
        # Choose inward sign.
        if dot(p,[raw[0]/(a*a),raw[1]/(b*b)])>0: raw=mul(-1,raw)
        q,dn=physics_next(p,raw,a,b)
        if det([p[0]/a,p[1]/b],[q[0]/a,q[1]/b])>0:
            choices.append(raw)
    # For star steps with angular gap >pi the sign rule may be wrong. Select by positive
    # tangent phase at the boundary: det(p,d)>0, which is always true for the branch.
    candidates=[]
    for n in normals:
        raw=[-n[1],n[0]]; raw=mul(1/M.sqrt(dot(raw,raw)),raw)
        if dot(p,[raw[0]/(a*a),raw[1]/(b*b)])>0: raw=mul(-1,raw)
        if det(p,raw)>0: candidates.append(raw)
    if len(candidates)!=1: raise AssertionError(("launch ambiguity",len(candidates)))
    return candidates[0]
def winding_lift(lam,a,b,N):
    p=[a,M.mpf(0)];d=[-M.sqrt(lam)/b,M.sqrt(1-lam/(b*b))]
    theta=M.mpf(0)
    for j in range(N):
        q,dn=physics_next(p,d,a,b)
        before=M.atan2(p[1]/b,p[0]/a)
        after=M.atan2(q[1]/b,q[0]/a)
        step=(after-before)%(2*M.pi)
        theta+=step;p,d=q,dn
    return theta/(2*M.pi)
def solve_lambda(a,b,N,tau):
    lo=b*b*M.mpf("1e-100");hi=b*b*(1-M.mpf("1e-100"))
    for j in range(430):
        mid=(lo+hi)/2
        if winding_lift(mid,a,b,N)<tau:lo=mid
        else:hi=mid
    lam=(lo+hi)/2
    checknum(winding_lift(lam,a,b,N)-tau,M.mpf("1e-80"),"physical winding closure root")
    return lam
def nintersect(n,m):
    z=det(n,m)
    return [(m[1]-n[1])/z,(n[0]-m[0])/z]
def nprojection(f,A,B):
    v=sub(B,A);return add(A,mul(dot(sub(f,A),v)/dot(v,v),v))
def orbit_geometry(a,b,lam,N,tau,theta):
    p=[a*M.cos(theta),b*M.sin(theta)]
    d=launch(p,a,b,lam)
    P=[];ds=[]
    for j in range(N):
        P.append(p);ds.append(d)
        p,d=physics_next(p,d,a,b)
    tol=M.mpf("1e-75")
    scale=max(a,b,M.mpf(1))
    for z in sub(p,P[0]):checknum(z,tol*scale,"direct reflection orbit closure")
    total_turn=M.mpf(0)
    minimum_distinct_separation=M.inf
    for i in range(N):
        q=P[(i+1)%N]; p=P[i]
        total_turn+=(M.atan2(q[1]/b,q[0]/a)-M.atan2(p[1]/b,p[0]/a))%(2*M.pi)
        for j in range(i):
            minimum_distinct_separation=min(minimum_distinct_separation,M.sqrt(dot(sub(p,P[j]),sub(p,P[j])))/scale)
    checknum(total_turn/(2*M.pi)-tau,tol,"every-phase coprime winding")
    COUNTS["numeric_assertions"]+=1
    if minimum_distinct_separation<M.mpf("1e-60"):raise AssertionError("numerical primitive-phase collision")
    normals=[[p[0]/(a*a),p[1]/(b*b)] for p in P]
    V=[nintersect(normals[j],normals[(j+1)%N]) for j in range(N)]
    c=M.sqrt(a*a-b*b)
    Bareas=[];Qall=[]
    maxres=M.mpf(0)
    for j,p in enumerate(P):
        d=ds[j];n=normals[j]
        vals=[p[0]**2/(a*a)+p[1]**2/(b*b)-1,dot(d,d)-1]
        h=[-d[1],d[0]]
        vals+=[(dot(h,p)**2-(a*a-lam)*h[0]**2-(b*b-lam)*h[1]**2)/(a*a)]
        vals+=[dot(n,V[j])-1,dot(n,V[(j-1)%N])-1]
        for z in vals:
            checknum(z,tol,"physical membership, unit, caustic, actual side")
            maxres=max(maxres,abs(z))
    for e in [1,-1]:
        f=[e*c,0]
        Q=[nprojection(f,V[(j-1)%N],V[j]) for j in range(N)]
        for j,q in enumerate(Q):
            p=P[j];side=sub(V[j],V[(j-1)%N])
            expected=[a*a*(p[0]+e*c)/(a*a+e*c*p[0]),a*a*p[1]/(a*a+e*c*p[0])]
            checks=[(q[i]-expected[i])/scale for i in range(2)]
            checks+=[(dot(q,q)-a*a)/(a*a),
                     dot(normals[j],q)-1,
                     dot(sub(q,f),side)/(scale*M.sqrt(dot(side,side)))]
            for z in checks:
                checknum(z,tol,"actual focal side foot")
                maxres=max(maxres,abs(z))
        Bareas.append(area(Q));Qall.append(Q)
    # Signed order, repeated traversal and reverse checked on literal feet.
    for Q,Bv in zip(Qall,Bareas):
        checknum(area(list(reversed(Q)))+Bv,tol*scale**2,"signed reversal")
        checknum(area(Q*3)-3*Bv,tol*scale**2,"literal triple traversal")
    return Bareas,maxres,{"min_caustic_axis_ratio":M.sqrt((b*b-lam)/(a*a-lam)),
                          "max_outer_vertex_norm":max(M.sqrt(dot(v,v)) for v in V),
                          "minimum_distinct_vertex_separation":minimum_distinct_separation}
def numerical_checks():
    M.mp.dps=125
    specifications=[
        ("near_circle","1.000001",3,1),("near_circle","1.000001",11,5),
        ("moderate","1.2",3,1),("moderate","1.2",5,1),("moderate","1.2",5,2),
        ("moderate","1.2",9,4),("elliptic","2",3,1),("elliptic","2",7,1),
        ("elliptic","2",7,2),("elliptic","2",7,3),("elliptic","2",9,2),
        ("elliptic","2",11,5),("elliptic","2",15,7),
        ("high_aspect","8",3,1),("high_aspect","8",5,1),("high_aspect","8",5,2),
        ("high_aspect","8",11,5),("thin_caustic","2",21,10),
        ("even_negative","2",4,1),("even_negative","2",6,1),("even_negative","2",8,3)]
    phases=["0","0.001","0.17","0.63","1.234","1.5707963267948966192313216916397514420985846996875529104874722961539082031431045","2.2"]
    out=[]
    for label,ratio,N,tau in specifications:
        if math.gcd(N,tau)!=1:raise AssertionError("nonprimitive fixture")
        a=M.mpf(ratio);b=M.mpf(1);lam=solve_lambda(a,b,N,tau)
        products=[];bvalues=[];res=M.mpf(0);thin=None;maxV=M.mpf(0);minsep=M.inf
        for theta in phases:
            Bs,r,geo=orbit_geometry(a,b,lam,N,tau,M.mpf(theta))
            products.append(Bs[0]*Bs[1]);bvalues.append(Bs);res=max(res,r)
            thin=geo["min_caustic_axis_ratio"];maxV=max(maxV,geo["max_outer_vertex_norm"]);minsep=min(minsep,geo["minimum_distinct_vertex_separation"])
        reference=products[0];spread=max(abs(x-reference) for x in products)
        if N%2:
            for x in products: checknum((x-reference)/max(1,abs(reference)),M.mpf("1e-70"),"odd focal product invariance")
        else:
            for Bs in bvalues:checknum((Bs[0]-Bs[1])/max(1,abs(Bs[0])),M.mpf("1e-70"),"even equal focal areas")
            if spread<M.mpf("1e-10"):raise AssertionError("even fixture failed to falsify constant square")
        out.append({"label":label,"a_over_b":ratio,"N":N,"tau":tau,"phases":len(phases),
                    "lambda_over_b2":M.nstr(lam,70),"caustic_axis_ratio":M.nstr(thin,35),
                    "base_product":M.nstr(reference,60),"max_absolute_product_spread":M.nstr(spread,15),
                    "max_normalized_geometric_residual":M.nstr(res,15),
                    "max_outer_vertex_norm":M.nstr(maxV,15),
                    "minimum_distinct_vertex_separation":M.nstr(minsep,15),
                    "expected_product_invariance":bool(N%2),
                    "diagnostic_only_not_interval_certified":True})
        print(label,ratio,N,tau,"PASS",M.nstr(spread,7),flush=True)
    return out
def main():
    result={"schema":"pr210-independent-physical-geometry-results-v1",
            "timestamp_UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "mechanism":"Direct Euclidean reflection and conic-support tangency; no Jacobi functions.",
            "dependencies":{"python":sys.version,"sympy":S.__version__,"mpmath":M.__version__}}
    result["exact"]=exact_checks()
    result["numerical"]=numerical_checks()
    result["assertion_counts"]=COUNTS
    result["numerical_limitation"]="125 decimal digit arbitrary precision; residual checks are noninterval diagnostics and do not certify general theorem."
    p=D/"RESULTS.json";p.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(COUNTS),flush=True)
if __name__=="__main__":main()
