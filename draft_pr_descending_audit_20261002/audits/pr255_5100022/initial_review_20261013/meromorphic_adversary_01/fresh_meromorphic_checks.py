"""Independent k404 algebra/Laurent certificates and labeled diagnostics.

No campaign verifier is imported. Exact checks do not stand in for torus analysis.
Run with Python and SymPy/mpmath. JSON output is written alongside this script.
"""
from pathlib import Path
import json, math, time
import sympy as sp
import mpmath as mp

OUT = Path(__file__).resolve().parent
began = time.time()
exact = []
k, t, s, c, d, C, D, b0 = sp.symbols("k t s c d C D b0")
rels = [(c, 1-s*s), (d, 1-k*k*s*s), (C, 1-t*t),
        (D, 1-k*k*t*t), (b0, 1-k*k)]

def reduce_poly(expr):
    expr = sp.expand(expr)
    for x, square in rels:
        expr = sp.rem(expr, x*x-square, x)
    return sp.factor(expr)

def certify(label, expr):
    numer = sp.together(expr).as_numer_denom()[0]
    remainder = reduce_poly(numer)
    assert remainder == 0, (label, remainder)
    exact.append(label)

def dot(x,y): return x[0]*y[0]+x[1]*y[1]
def det(x,y): return x[0]*y[1]-x[1]*y[0]
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
L = 1-k*k*t*t*s*s
E = 1-2*k*k*t*t+k*k*t**4
sm, spv = (s*C*D-t*c*d)/L, (s*C*D+t*c*d)/L
cm, cp = (c*C+s*d*t*D)/L, (c*C-s*d*t*D)/L
Pm, Pp = (-D*sm/C,b0*cm/C), (-D*spv/C,b0*cp/C)
F = (k,0)
U = (-(E*s+k*(C*C-D*D*s*s))/(C*C*L),
     c*(2*b0*b0-E*(1+k*s))/(b0*C*C*L))
for name,P in [("minus",Pm),("plus",Pp)]:
    certify("antipedal line equation "+name, dot(sub(P,F),sub(U,P)))
certify("focal ray determinant", det(sub(Pm,F),sub(Pp,F)) -
        2*b0*D*t*d*(1+k*s)/(C*L))
n = (-s,c/b0)
certify("chord tangent minus",dot(n,Pm)-1)
certify("chord tangent plus",dot(n,Pp)-1)
q = ((k-s)/(1-k*s), b0*c/(1-k*s))
certify("pedal foot lies on chord",dot(n,q)-1)
certify("pedal foot displacement normal",det(sub(q,F),n))
certify("original edge-area dn relation",det(Pm,Pp)-
        2*D*b0*t*d/(C*L))

# Direct imaginary-shift rationalization: only X=+/-t can be poles.
X,Y,Z=sp.symbols("X Y Z")
ui = tuple(sp.cancel(x.subs({s:1/(k*X),c:-sp.I*Z/(k*X)})) for x in U)
ui_expected = (-(E*X/k+k*C*C*X*X-D*D/k)/(C*C*(X*X-t*t)),
               -sp.I*Z*((2*b0*b0-E)*X-E)/(k*b0*C*C*(X*X-t*t)))
for i in range(2):
    certify("imaginary-shift antipedal rationalization "+str(i), ui[i]-ui_expected[i])

# Residue vectors at v,-v and their +2K translates. Derivative of sn
# at +/-v is CD; after +2K it is -CD. This is independent of N.
def residue_at(sign, antipode):
    xx=sign*t*(-1 if antipode else 1)
    deriv=C*D*(-1 if antipode else 1)
    den_deriv=2*xx*deriv
    return tuple(sp.cancel(sp.together(x*(X*X-t*t)).subs({X:xx,Z:D})/den_deriv)
                 for x in ui_expected)
rp,rm=residue_at(1,False),residue_at(-1,False)
rpa,rma=residue_at(1,True),residue_at(-1,True)
for i in range(2):
    certify("antipedal residue pairing plus "+str(i),rpa[i]+rm[i])
    certify("antipedal residue pairing minus "+str(i),rma[i]+rp[i])
certify("paired adjacent antipedal double coefficient cancels",
        det(rm,rp)+det(rma,rpa))

# Pedal Laurent coefficients from the quarter-period chart r=K+iK'.
z=sp.symbols("z")
cs=1-z*z/2+(1+4*k*k)*z**4/24
ds=1-k*k*z*z/2+k*k*(4+k*k)*z**4/24
qr=((k*k*cs-ds)/(k*(cs-ds)),
    -sp.I*(1-k*k)/(k*(cs-ds)))
for i,target in enumerate([2/k,2*sp.I/k]):
    certify("pedal double Laurent coefficient "+str(i),
            sp.limit(z*z*qr[i],z,0)-target)
    certify("pedal absent simple Laurent coefficient "+str(i),
            sp.limit(sp.diff(z*z*qr[i],z),z,0))

# Differentiate the exact quarter-period chart using the Jacobi ODE.
e=c-d
qq=((k*k*c-d)/(k*e),-sp.I*b0*b0/(k*e))
diffop=lambda expr: -s*d*sp.diff(expr,c)-k*k*s*c*sp.diff(expr,d)
qp=tuple(diffop(x) for x in qq)
qp_expected=(-b0**4*s/(k*e*e),
             -sp.I*b0*b0*s*(d-k*k*c)/(k*e*e))
for i in range(2):
    certify("quarter-chart pedal derivative "+str(i),qp[i]-qp_expected[i])
p_expr=b0*b0*s*(d-k*k*c-b0*b0)/(k*k*e*e)
certify("pedal trace residue coefficient",
        sp.I*det((1,sp.I),qp)/k-p_expr)
certify("strict pedal coefficient sign identity",
        d*d-(k*k*c+b0*b0)**2-k*k*b0*b0*(1-c)**2)
certify("normal angular determinant",
        det((-s,c/b0),(-c*d,-s*d/b0))-d/b0)
sn_series=z-(1+k*k)*z**3/6
cn_series=1-z*z/2
certify("dn imaginary residue",
        sp.limit(z*(-sp.I*cn_series/sn_series),z,0)+sp.I)

# Complete finite group arithmetic, exact integers; this is a diagnostic of
# the generic Bezout proof, not a substitute for that proof.
arithmetic=0
for N in range(6,302,4):
    m=N//2
    for tau in range(1,m):
        if math.gcd(tau,N)!=1: continue
        assert tau%2==1 and m%2==1 and math.gcd(tau,m)==1
        residues={(j*tau)%m for j in range(m)}
        assert residues==set(range(m))
        assert sum((j*tau)%m==0 for j in range(N))==2
        assert (m+tau)%2==0
        # 2*(K+v)/h = m+tau; no parity can be silently dropped.
        assert (m+tau)//2*2==m+tau
        # q poles occur once modulo the full real 4K period.
        assert sum((j*tau)%N==0 for j in range(N))==1
        arithmetic+=1

mp.mp.dps=90
diagnostics=[]
worst=mp.mpf(0)
def js(u,mod):
    return (mp.ellipfun("sn",u,mod**2),mp.ellipfun("cn",u,mod**2),
            mp.ellipfun("dn",u,mod**2))
def area(vs):
    return sum(det(vs[j],vs[(j+1)%len(vs)]) for j in range(len(vs)))/2
def relerr(x,y):
    return abs(x-y)/max(mp.mpf(1),abs(x),abs(y))
def assert_close(label,x,y,tol=mp.mpf("1e-65")):
    global worst
    error=relerr(x,y); worst=max(worst,error)
    assert error<tol,(label,mp.nstr(error,12))
def construct(mod,N,tau,w):
    K=mp.ellipk(mod**2); v=2*K*tau/N; delta=2*v
    tv,Cv,Dv=js(v,mod); bb=mp.sqrt(1-mod**2)
    aa=Dv/Cv; bo=bb/Cv
    points=[(-aa*js(w+j*delta,mod)[0],bo*js(w+j*delta,mod)[1]) for j in range(N)]
    out={}
    for sign in [1,-1]:
        focus=(sign*mod,mp.mpf(0)); anti=[]; pedal=[]
        for j in range(N):
            P=points[j]; Q=points[(j+1)%N]
            r1=sub(P,focus); r2=sub(Q,focus)
            rr1=dot(r1,P);rr2=dot(r2,Q);den=det(r1,r2)
            anti.append(((rr1*r2[1]-r1[1]*rr2)/den,
                         (r1[0]*rr2-rr1*r2[0])/den))
            tangent=sub(Q,P)
            lam=dot(sub(focus,P),tangent)/dot(tangent,tangent)
            pedal.append((P[0]+lam*tangent[0],P[1]+lam*tangent[1]))
        out[sign]=(area(anti),area(pedal))
    trace=sum(js(w+j*delta,mod)[2] for j in range(N))
    sd,cd,dd=js(delta,mod)
    p=(bb**2*sd*(dd-mod**2*cd-bb**2)/(mod**2*(cd-dd)**2))
    assert_close("explicit pedal residue coefficient",out[1][1],p*trace)
    assert_close("two focus anti areas",out[1][0],out[-1][0])
    assert_close("two focus pedal areas",out[1][1],out[-1][1])
    return out,trace

# Falsification matrix covers simple and highly winding primitive classes,
# almost-circular and almost-degenerate eccentricities, and complex phases.
families=[(N,tau) for N in [6,10,14,18,22,26,50]
          for tau in sorted({1,N//2-2})
          if math.gcd(N,tau)==1]
for mod in map(mp.mpf,["0.02","0.71","0.999999"]):
    K=mp.ellipk(mod**2)
    for N,tau in families:
        h=2*K/(N//2)
        base,Sbase=construct(mod,N,tau,mp.mpf(0))
        Bbase,Pbase=base[1]
        for f in [mp.mpf("0.143"),mp.mpf("0.499")]:
            out,S=construct(mod,N,tau,f*h)
            assert out[1][1]>0
            assert_close("antipedal dn trace",out[1][0]*Sbase,Bbase*S)
            assert_close("constant target ratio",out[1][0]*Pbase,Bbase*out[1][1])
        out,S=construct(mod,N,tau,h*mp.mpc("0.21","0.37"))
        assert_close("complex antipedal trace",out[1][0]*Sbase,Bbase*S)
        diagnostics.append({"k":str(mod),"N":N,"tau":tau,"real_phases":3,"complex_phases":1})

local_diagnostics=[]
mod=mp.mpf("0.71"); Kp=mp.ellipk(1-mod**2); p0=mp.j*Kp
for N,tau in [(6,1),(14,5),(26,11)]:
    base,Sbase=construct(mod,N,tau,mp.mpf("0.017"))
    Bbase=base[1][0]
    for eps in map(mp.mpf,["1e-4","1e-7"]):
        op,Sp=construct(mod,N,tau,p0+eps)
        om,Sm=construct(mod,N,tau,p0-eps)
        assert_close("antipedal oddness about pole",op[1][0],-om[1][0])
        assert_close("near-pole antipedal trace",op[1][0]*Sbase,Bbase*Sp)
        assert_close("trace oddness about pole",Sp,-Sm)
        shifted,_=construct(mod,N,tau,p0+eps+2*mp.j*Kp)
        assert_close("antipedal imaginary anti-period",shifted[1][0],-op[1][0])
        assert_close("pedal imaginary anti-period",shifted[1][1],-op[1][1])
        local_diagnostics.append({"N":N,"tau":tau,"epsilon":str(eps)})

result={"status":"PASS","exact_symbolic_checks":len(exact),
        "exact_check_names":exact,"period_arithmetic_families":arithmetic,
        "diagnostic_precision_digits":mp.mp.dps,"diagnostic_families":len(diagnostics),
        "diagnostic_matrix":diagnostics,
        "near_complex_pole_cases":local_diagnostics,
        "worst_scaled_numeric_error":mp.nstr(worst,18),
        "elapsed_seconds":time.time()-began,
        "limitations":"Exact certificates support the independent all-N derivation; finite arithmetic and mpmath diagnostics do not alone prove the theorem."}
(OUT/"FRESH_CHECK_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
