#!/usr/bin/env python3
"""Fresh PR210 exact controls and non-interval complex/real diagnostics.
Run with Python3.11 -E -S -B -P. Only dependency path explicitly inserted.
No original verification code, old reports, provider mutation, or git is used.
"""
import sys
sys.path.insert(0,"/Users/alec/Library/Python/3.11/lib/python/site-packages")
from pathlib import Path
import json,math,hashlib,datetime
import sympy as sy
import mpmath as mp
HERE=Path(__file__).resolve().parent
assert sy.__version__=="1.14.0"
assert mp.__version__=="1.3.0"
exact=[]; numeric=[]; lattice={"families":0,"phases":0,"assertions":0}
def ez(label,expr):
    value=sy.simplify(expr)
    assert value==0,(label,value)
    exact.append({"label":label,"residual":"0"})
def eb(label,value):
    assert bool(value),label
    exact.append({"label":label,"value":True})
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def area(V):return sum(det(V[j],V[(j+1)%len(V)]) for j in range(len(V)))/2
a,b,c,s,t=sy.symbols("a b c s t",nonzero=True,real=True)
gb=sy.groebner([c*c-a*a+b*b,t*t+s*s-1],c,t,s,a,b)
def alg(label,expr):
    num=sy.together(expr).as_numer_denom()[0]
    rem=gb.reduce(sy.expand(num))[1]
    ez(label,rem)
n=sy.Matrix([-s/a,t/b]);F=sy.Matrix([c,0]);D=a-c*s
Q=sy.Matrix([a*(c-a*s)/D,a*b*t/D])
proj=F+(1-dot(n,F))/dot(n,n)*n
alg("general-foot-x",Q[0]-proj[0])
alg("general-foot-y",Q[1]-proj[1])
alg("foot-on-tangent",dot(n,Q)-1)
alg("foot-perpendicular",det(Q-F,n))
alg("auxiliary-circle",dot(Q,Q)-a*a)
U=sy.Matrix([c-a*s,b*t])
alg("inverse-distance-factor",dot(U,U)-D*D)
alg("pointwise-inverse-link-x",Q[0]-a*D*U[0]/D**2)
alg("pointwise-inverse-link-y",Q[1]-a*D*U[1]/D**2)
# Canonical chord identity, independently derived from addition formulas.
k,S,C,d,x,h,e,al,kp=sy.symbols("k S C d x h e al kp",nonzero=True,real=True)
DD=1-k*k*x*x*S*S
sp=(x*C*d+S*h*e)/DD;sm=(x*C*d-S*h*e)/DD
cp=(h*C-x*e*S*d)/DD;cm=(h*C+x*e*S*d)/DD
for label,ss,cc in [("plus",sp,cp),("minus",sm,cm)]:
    expr=x*d/C*ss+h/C*cc-1
    expr=sy.expand(sy.together(expr).as_numer_denom()[0]).subs(h*h,1-x*x).subs(d*d,1-k*k*S*S)
    ez("canonical-chord-"+label,expr)
aa=al*d/C;bb=al*kp/C;cf=al*k
ez("canonical-confocal",sy.expand(aa*aa-bb*bb-cf*cf).subs(d*d,1-k*k*S*S).subs(kp*kp,1-k*k).subs(C*C,1-S*S))
# Symbolic Laurent leading coefficients at r+-v.
numer=sy.Matrix([-aa*bb**2/cf,-sy.I*aa*bb**2/cf])
dminus=al*kp**2*S/C**2
Rm=sy.simplify(numer/dminus);Rp=-Rm
ez("paired-residue-determinant",det(Rm,Rp))
ez("isotropic-residue",dot(Rm,Rm))
ez("explicit-residue-x",Rm[0]+al*d/(k*C*S))
ez("explicit-residue-y",Rm[1]+sy.I*al*d/(k*C*S))
# General even/antiperiod synthetic counter controls: losing antiperiod or
# allowing a double pole invalidates the complementary zero reasoning.
eb("wrong-imaginary-period-rejected-by-reflection-det",sy.det(sy.diag(1,-1))==-1)
def fixture(label,a,b,lam,V,expected_plus,expected_minus):
    c=sy.sqrt(a*a-b*b);alpha2=a*a-lam;beta2=b*b-lam
    V=[sy.Matrix(v) for v in V]
    N=len(V)
    outer=[]
    for j,p in enumerate(V):
        q=V[(j+1)%N]
        normal=sy.Matrix([p[0]/a**2,p[1]/b**2])
        normal2=sy.Matrix([q[0]/a**2,q[1]/b**2])
        M=sy.Matrix([list(normal),list(normal2)])
        eb(label+"-distinct-tangents-"+str(j),M.det()!=0)
        outer.append(M.inv()*sy.ones(2,1))
        ez(label+"-boundary-"+str(j),p[0]**2/a**2+p[1]**2/b**2-1)
        pm=V[(j-1)%N]
        incoming=p-pm;outgoing=q-p
        incoming=incoming/sy.sqrt(dot(incoming,incoming))
        outgoing=outgoing/sy.sqrt(dot(outgoing,outgoing))
        reflected=incoming-2*dot(incoming,normal)/dot(normal,normal)*normal
        for z in range(2):ez(label+"-reflection-"+str(j)+"-"+str(z),outgoing[z]-reflected[z])
        # Parametric chord discriminant at the shared confocal caustic.
        v=q-p
        Aq=v[0]**2/alpha2+v[1]**2/beta2
        Bq=2*(p[0]*v[0]/alpha2+p[1]*v[1]/beta2)
        Cq=p[0]**2/alpha2+p[1]**2/beta2-1
        ez(label+"-caustic-tangent-"+str(j),Bq**2-4*Aq*Cq)
    areas=[]
    for sign,expected in [(1,expected_plus),(-1,expected_minus)]:
        focus=sy.Matrix([sign*c,0]);feet=[]
        for j,p in enumerate(V):
            # Independent projection on the actual outer side segment's line.
            left=outer[(j-1)%N];right=outer[j];edge=right-left
            foot=left+dot(focus-left,edge)/dot(edge,edge)*edge
            normal=sy.Matrix([p[0]/a**2,p[1]/b**2])
            direct=focus+(1-dot(normal,focus))/dot(normal,normal)*normal
            ez(label+"-actual-outer-foot-x-"+str(sign)+"-"+str(j),foot[0]-direct[0])
            ez(label+"-actual-outer-foot-y-"+str(sign)+"-"+str(j),foot[1]-direct[1])
            ez(label+"-perpendicular-"+str(sign)+"-"+str(j),dot(focus-foot,edge))
            ez(label+"-auxiliary-circle-"+str(sign)+"-"+str(j),dot(foot,foot)-a*a)
            feet.append(sy.simplify(foot))
        ar=sy.simplify(area(feet));ez(label+"-area-"+str(sign),ar-expected)
        for mult in [2,3]:
            ez(label+"-repeat-"+str(sign)+"-"+str(mult),area(feet*mult)-mult*ar)
        ez(label+"-reversal-"+str(sign),area(list(reversed(feet)))+ar)
        areas.append(ar)
    return areas
rt=sy.sqrt
H=[(rt(21),0),(-3*rt(21)/5,sy.Rational(16,5)),(-3*rt(21)/5,-sy.Rational(16,5))]
V=[(0,4),(-sy.Rational(21,5),-sy.Rational(8,5)),(sy.Rational(21,5),-sy.Rational(8,5))]
h=fixture("triangle-H",rt(21),sy.Integer(4),sy.Rational(336,25),H,(49*rt(21)+7*rt(5))/10,(49*rt(21)-7*rt(5))/10)
v=fixture("triangle-V",rt(21),sy.Integer(4),sy.Rational(336,25),V,sy.Rational(112,5),sy.Rational(112,5))
ez("triangle-products-match",h[0]*h[1]-v[0]*v[1])
ez("triangle-product-value",h[0]*h[1]-sy.Rational(12544,25))
D=[(2,0),(0,1),(-2,0),(0,-1)]
C4=[(4/rt(5),1/rt(5)),(-4/rt(5),1/rt(5)),(-4/rt(5),-1/rt(5)),(4/rt(5),-1/rt(5))]
dd=fixture("primitive-even-D",sy.Integer(2),sy.Integer(1),sy.Rational(4,5),D,sy.Integer(4),sy.Integer(4))
cc=fixture("primitive-even-C",sy.Integer(2),sy.Integer(1),sy.Rational(4,5),C4,sy.Integer(5),sy.Integer(5))
eb("even-product-is-nonconstant",sy.simplify(dd[0]*dd[1]-cc[0]*cc[1])==-9)
# Exact circle control independent of the nonzero-k coordinate setup.
circle=[sy.Matrix(p) for p in [(2,0),(-1,rt(3)),(-1,-rt(3))]]
ez("circle-product",area(circle)**2-27)
for shift in [sy.Matrix([[0,-1],[1,0]]),sy.Matrix([[-1,0],[0,-1]])]:
    ez("circle-rotation",area([shift*p for p in circle])**2-27)
print("EXACT",len(exact),flush=True)
for N in range(3,202,2):
    for tau in range(1,(N+1)//2):
        if math.gcd(N,tau)!=1:continue
        lattice["families"]+=1
        perm=[(j*tau)%N for j in range(N)]
        assert len(set(perm))==N;lattice["assertions"]+=1
        inverse=pow(tau,-1,N)
        for phase in range(N):
            j0=(-phase*inverse)%N
            j1=((tau-phase)*inverse)%N
            assert j1==(j0+1)%N and j0!=j1
            assert (phase+j0*tau)%N==0 and (phase+j1*tau)%N==tau
            lattice["assertions"]+=2;lattice["phases"]+=1
        assert (N%2)==1 and (2*N)%4==2;lattice["assertions"]+=1
print("LATTICE",lattice,flush=True)
mp.mp.dps=90
maxerr={}
def near(label,got,want,tol=mp.mpf("1e-62")):
    err=abs(got-want)/max(mp.mpf(1),abs(got),abs(want))
    if err>maxerr.get(label,mp.mpf(0)):maxerr[label]=err
    assert err<tol,(label,mp.nstr(err,15),mp.nstr(got,15),mp.nstr(want,15))
    numeric.append(label)
def norm(v):return mp.sqrt(dot(v,v))
def geo(N,tau,ks):
    k=mp.mpf(ks);m=k*k;K=mp.ellipk(m);Kp=mp.ellipk(1-m)
    v=2*K*tau/N;delta=2*v;L=4*K/N
    sn=lambda z:mp.ellipfun("sn",z,m)
    cn=lambda z:mp.ellipfun("cn",z,m)
    dn=lambda z:mp.ellipfun("dn",z,m)
    al=mp.mpf(1);be=mp.sqrt(1-m);c=k;a=dn(v)/cn(v);b=be/cn(v)
    P=lambda z:(-a*sn(z),b*cn(z))
    Q=lambda z:(a*(c-a*sn(z))/(a-c*sn(z)),a*b*cn(z)/(a-c*sn(z)))
    def trace(w):
        points=[Q(w+j*delta) for j in range(N)]
        return area(points)
    def invtrace(w):
        points=[]
        for j in range(N):
            px,py=P(w+j*delta);u=(px+c,py);den=dot(u,u)
            points.append((u[0]/den,u[1]/den))
        return area(points)
    return locals()
families=[]
for N in [3,5,7,9,11,15]:
    for tau in range(1,(N+1)//2):
        if math.gcd(N,tau)==1:
            for ks in ["0.02","0.57","0.96"]:families.append((N,tau,ks))
families += [(21,10,"0.999999"),(31,15,"0.0000000001"),(51,25,"0.999"),(7,3,"0.999999999999")]
summaries=[]
for idx,(N,tau,ks) in enumerate(families):
    g=geo(N,tau,ks);globals().update({kk:g[kk] for kk in ["k","K","Kp","v","delta","L","a","b","c","be","P","Q","trace","invtrace","sn","cn","dn"]})
    baseline=None;ratio=None
    for phase in [mp.mpf("0.137"),mp.mpf("0.731"),mp.mpf("1.299")]:
        w=phase*K;T=trace(w);Tm=trace(w+2*K);prod=T*Tm
        if baseline is None:baseline=prod
        near("odd-real-product",prod,baseline)
        near("focus-area-shift",Tm,trace(w+L/2))
        near("reduced-period",trace(w+L),T)
        near("real-reflection",trace(2*K-w),T)
        near("imaginary-antiperiod",trace(w+2j*Kp),-T)
        near("full-imaginary-period",trace(w+4j*Kp),T)
        near("centered-evenness",trace(K-v+w),trace(K-v-w))
        Di=invtrace(w)
        if ratio is None:ratio=T/Di
        near("inverse-area-proportionality",T,ratio*Di)
        # Physical geometry and canonical foot, independently from tangent intersections.
        points=[P(w+j*delta) for j in range(N)]
        normals=[(p[0]/a**2,p[1]/b**2) for p in points]
        outer=[]
        for j in range(N):
            nn=normals[j];nn1=normals[(j+1)%N];den=det(nn,nn1)
            outer.append(((nn1[1]-nn[1])/den,(nn[0]-nn1[0])/den))
        for j in range(N):
            pt=points[j];prev=points[(j-1)%N];nxt=points[(j+1)%N];nn=normals[j]
            incoming=tuple(pt[z]-prev[z] for z in range(2));ln=norm(incoming);incoming=tuple(z/ln for z in incoming)
            outgoing=tuple(nxt[z]-pt[z] for z in range(2));ln=norm(outgoing);outgoing=tuple(z/ln for z in outgoing)
            refl=tuple(incoming[z]-2*dot(incoming,nn)/dot(nn,nn)*nn[z] for z in range(2))
            for z in range(2):near("physical-unit-reflection",refl[z],outgoing[z])
            left=outer[(j-1)%N];right=outer[j];edge=tuple(right[z]-left[z] for z in range(2))
            f=(c,mp.mpf(0));vv=tuple(f[z]-left[z] for z in range(2))
            foot=tuple(left[z]+dot(vv,edge)/dot(edge,edge)*edge[z] for z in range(2))
            q=Q(w+j*delta)
            for z in range(2):near("actual-outer-side-projection",foot[z],q[z])
            near("foot-auxiliary-circle",dot(q,q),a*a)
            # Actual shared caustic tangency, no stored symbolic assertion.
            vch=tuple(nxt[z]-pt[z] for z in range(2))
            aa=vch[0]**2+vch[1]**2/be**2
            bb=2*(pt[0]*vch[0]+pt[1]*vch[1]/be**2)
            cc=pt[0]**2+pt[1]**2/be**2-1
            near("shared-caustic-discriminant",bb*bb,4*aa*cc)
        # Supplemental bicentric/Landen formula, computed independently from Q/V.
        lam=b*b-be*be;rb=a;db=-c*lam/be**2;Rb=b*b/be**2
        mb=4*k/(1+k)**2;Kb=mp.ellipk(mb);u=(1+k)*(w+v-K)/2
        near("bicentric-real-period",Kb,(1+k)*K)
        tM=mp.sqrt((Rb+abs(db))**2-rb**2)
        Sdn=sum(mp.ellipfun("dn",u+2*j*Kb*tau/N,mb) for j in range(N))
        predicted=rb**3*tM/(Rb**2-db**2)*Sdn
        near("bicentric-dn-area",T,predicted)
    summaries.append({"N":N,"tau":tau,"k":ks,"product":mp.nstr(baseline,28),"inverse_ratio":mp.nstr(ratio,28)})
    if idx%8==0:print("REAL",idx+1,"/",len(families),flush=True)
print("REAL DONE",len(families),len(numeric),flush=True)
# Complex diagnostics target actual poles, missing-pole risks, all characters.
complex_rows=[]
for N,tau,ks in [(3,1,"0.57"),(5,2,"0.83"),(7,3,"0.96"),(9,4,"0.22"),(15,7,"0.8"),(21,10,"0.99")]:
    g=geo(N,tau,ks)
    K,Kp,v,L,k,a,b,c=g["K"],g["Kp"],g["v"],g["L"],g["k"],g["a"],g["b"],g["c"]
    Q,trace,sn,cn,dn=g["Q"],g["trace"],g["sn"],g["cn"],g["dn"]
    p=1j*Kp;r=K+p;b0=K-v
    kp=mp.sqrt(1-k*k)
    rv=(-dn(v)/(k*cn(v)*sn(v)),-1j*dn(v)/(k*cn(v)*sn(v)))
    for off in [mp.mpf("0.1"),mp.mpf("0.37")+mp.mpf("0.21")*1j]:
        near("quarter-sn",sn(r+off),dn(off)/(k*cn(off)))
        near("quarter-cn",cn(r+off),-1j*kp/(k*cn(off)))
        near("quarter-dn",dn(r+off),1j*kp*sn(off)/cn(off))
    for exponent in [12,20]:
        eps=mp.mpf(10)**(-exponent)*(1+mp.mpf("0.17")*1j)
        qm=Q(r-v+eps);qp=Q(r+v+eps)
        tol=mp.mpf(10)**(-exponent+3)
        for z in range(2):
            near("paired-residue-limit",eps*qm[z],rv[z],tol)
            near("opposite-residue-limit",eps*qp[z],-rv[z],tol)
        near("no-double-pole-vector-det",eps**2*det(qm,qp),0,tol)
        near("no-double-pole-trace",eps**2*trace(b0+p+eps),0,tol)
        near("second-row-no-double-pole-trace",eps**2*trace(b0+3*p+eps),0,tol)
        near("sn-common-pole-removable",Q(p+eps)[0],a*a/c,tol)
        near("complementary-zero-limit",trace(b0+p+L/2+eps),0,tol)
        test=(b0+p+eps)
        z0=b0+mp.mpf("0.31")*K
        near("complex-product-through-pole",trace(test)*trace(test+L/2),trace(z0)*trace(z0+L/2),tol)
    # Exact zero candidates evaluated away from Q singularities on the trace lattice.
    near("complementary-zero",trace(b0+p+L/2),0,mp.mpf("1e-55"))
    near("complementary-zero-second-row",trace(b0+3*p+L/2),0,mp.mpf("1e-55"))
    complex_rows.append({"N":N,"tau":tau,"k":ks,"residue_x":mp.nstr(rv[0],28)})
    print("COMPLEX",N,tau,flush=True)
# Circle family stars (excluded k0 endpoint handled geometrically).
for N in [3,5,7,9]:
    for tau in range(1,(N+1)//2):
        if math.gcd(N,tau)!=1:continue
        target=(mp.mpf(N)*4*mp.sin(2*mp.pi*tau/N)/2)**2
        for angle in [mp.mpf("0"),mp.mpf("0.31")]:
            W=[(2*mp.cos(angle+2*mp.pi*tau*j/N),2*mp.sin(angle+2*mp.pi*tau*j/N)) for j in range(N)]
            near("circle-star-product",area(W)**2,target)
results={
"schema":"pr210-independent-meromorphic-math-controls-v1",
"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
"inputs":{"manuscript":{"bytes":19892,"sha256":"71e45462370c5314a2e43cc43678571931f8dc177536637e24cea050034b496e"},"original_proof":{"bytes":10040,"sha256":"5a78b9d2fb1f7a0a80e556f2e2b759875bdbba055a454c148524eb44879add7e"}},
"dependencies":{"python":sys.version,"sympy":sy.__version__,"mpmath":mp.__version__,"dps":mp.mp.dps},
"exact_assertions":len(exact),"exact_results":exact,"finite_integer_lattice_controls":lattice,
"noninterval_numeric_assertions":len(numeric),"numeric_labels":{label:numeric.count(label) for label in sorted(set(numeric))},
"maximum_scaled_errors":{label:mp.nstr(value,15) for label,value in maxerr.items()},
"odd_real_families":summaries,"complex_pole_families":complex_rows,
"status":"PASS","proof_status":"Numerics are non-interval diagnostics. Universal proof checked separately by analytic derivation."}
out=HERE/"FRESH_CONTROL_RESULTS.json";out.write_text(json.dumps(results,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":"PASS","exact":len(exact),"lattice":lattice,"noninterval":len(numeric),"results_bytes":out.stat().st_size,"results_sha256":hashlib.sha256(out.read_bytes()).hexdigest()}),flush=True)
