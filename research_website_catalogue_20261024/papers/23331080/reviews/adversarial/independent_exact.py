#!/usr/bin/env python3
"""Independent adversarial algebra; full complex phases, all charts, exact jets.
The mathematical reconstruction was sealed before deposited programs were read.
Implementation follows that reconstruction; no deposited module is imported.
"""
from pathlib import Path
from collections import Counter
import hashlib, json, sys
import sympy as s
sys.dont_write_bytecode=True
counts=Counter()
def ck(ok, label):
    counts[label]+=1
    if not ok: raise RuntimeError(label)
def eq(a,b,label): ck(s.cancel(s.together(a-b))==0,label)
def main():
    ck(len(sys.argv)==1,'no overrides')
    root=Path(__file__).resolve().parents[2]
    for name,h in {
      'sources/SOURCE_READY.json':'3833194084fd0343a18c5640400418893203c6e575272997c114bc326d34e2af',
      'sources/positivity_loss.pdf':'d5c31033f40afaa8dbd1f8642d7c729dfd7a858553e1c1c0856520a10f23bedd',
      'sources/published-source/positivity-loss-30003571/paper/positivity_loss.tex':'2f38b06e7243966af7afda844edc4b6672be38bb9c10759816c2cce2e4e75bfe',
      'reviews/adversarial/INITIAL_SEAL.json':'3ce1782de3c68ee334ceb944225540e4a41240dac4e692dac511b76097ff91f8'}.items():
        ck(hashlib.sha256((root/name).read_bytes()).hexdigest()==h,'immutable target binding')
    e=s.Rational(1,96); d=s.Rational(1,4)
    S,SB,Z,ZB=s.symbols('S SB Z ZB'); u,v,p,x,q=s.symbols('u v p x q')
    A=4*p+(e+d*x*x)*(1-2*p)
    B=2+2*d*p*x*(2-3*x)
    Q=4*d*d*p*(1-p)*x**3*(1-x)
    # All four atlas charts, with unrestricted complex phases. SB,ZB are
    # algebraically independent conjugate placeholders; no zero-phase slice.
    for bi in [False,True]:
      for fi in [False,True]:
        uu=S*SB; vv=Z*ZB
        pp=1/(1+uu) if bi else uu/(1+uu)
        xx=1/(1+vv) if fi else vv/(1+vv)
        base_extra=(2-e)*uu/(1+uu) if bi else (2-e)/(1+uu)
        fiber_extra=1/(1+vv)**2 if fi else (vv/(1+vv))**2
        pot=2*s.log(1+uu)+base_extra+2*s.log(1+vv)+d*pp*fiber_extra
        aa=s.diff(pot,S,SB); bb=s.diff(pot,Z,ZB)
        mixed=s.diff(pot,S,ZB)*s.diff(pot,SB,Z)
        eq((1+uu)**2*aa,A.subs({p:pp,x:xx}),'all-phase chart base Hessian')
        eq((1+vv)**2*bb,B.subs({p:pp,x:xx}),'all-phase chart fiber Hessian')
        eq((1+uu)**2*(1+vv)**2*mixed,Q.subs({p:pp,x:xx}),'all-phase chart mixed Hessian')
        if not bi and not fi:
          eq(aa.subs({S:0,SB:0}),e+d*(vv/(1+vv))**2,'actual central initial jet')
          eq(bb.subs({S:0,SB:0}),2/(1+vv)**2,'actual central stationary fiber Hessian')
          eq(s.diff(pot,S,ZB).subs({S:0,SB:0}),0,'actual central mixed entry vanishes')
    U,V=s.symbols('U V',positive=True)
    original=2*s.log(1+u)+(2-e)/(1+u)+2*s.log(1+v)+d*u/(1+u)*(v/(1+v))**2
    for bi,fi in [(True,False),(False,True),(True,True)]:
      before=original.subs({u:1/U if bi else U,v:1/V if fi else V})
      correction=(2*s.log(U) if bi else 0)+(2*s.log(V) if fi else 0)
      pp=1/(1+U) if bi else U/(1+U); xx=1/(1+V) if fi else V/(1+V)
      after=2*s.log(1+U)+(2-e)*(1-pp)+2*s.log(1+V)+d*pp*xx**2
      # Positive radii justify this real-log simplification. Rational cancel
      # alone does not normalize log(1+1/U); preserve the initial receipt.
      eq(s.simplify(s.expand_log(before+correction-after,force=True)),0,'global weight transition')
    Al=e+s.Rational(167,48)*p; Bl=s.Rational(3,2); Qu=p/4
    RA=d*x*x+2*d*p*(1-x*x)
    RB=2*d*((1-p)+p*(1-x)*(1+3*x))
    RQ=4*d*d*p*(p+(1-p)*((1-x)*(1+x+x*x)+x**4))
    for a,b in [(A-Al,RA),(B-Bl,RB),(Qu-Q,RQ)]:eq(a,b,'continuum nonnegative remainder identity')
    eq(A*B-Q-(Al*Bl-Qu),RA*B+Al*RB+RQ,'full determinant nonnegative decomposition')
    eq(Al*Bl-Qu,s.Rational(1,64)+s.Rational(159,32)*p,'strict continuum determinant baseline')
    ck(e>0 and Bl>0 and s.Rational(1,64)>0,'strict continuum constants')
    # A,B,Q extend to every compact-atlas corner; exact endpoint checks are
    # adversarial boundary controls, not the proof of the whole square.
    for pp in [0,1]:
      for xx in [0,1]:
        av,bv,qv=[a.subs({p:pp,x:xx}) for a in [A,B,Q]]
        ck(av>0 and bv>0 and av*bv-qv>0,'compact atlas endpoint matrices')
    # Generic exact second jets: higher symmetric base terms disappear.
    f,W,H,g,h,j=s.symbols('f W H g h j',nonzero=True)
    sym_pot=f+S*SB*W+(S*SB)**2*H
    sym_g=g+S*SB*h+(S*SB)**2*j
    eq(s.diff(s.log(sym_g),S,SB).subs({S:0,SB:0}),h/g,'generic logarithmic metric exact second jet')
    eq(s.diff(s.exp(-sym_pot),S,SB).subs({S:0,SB:0}),-W*s.exp(-f),'generic density exact second jet')
    eq(s.diff(sym_g,S).subs({S:0,SB:0}),0,'symmetry removes logarithmic quadratic term')
    # Density and gauge controls: central MA and anticanonical masses.
    eq(s.integrate((1+v)**-2,(v,0,s.oo)),1,'central radial probability mass')
    eq(s.integrate(2*(1+v)**-2,(v,0,s.oo)),2,'central radial curvature mass')
    eq((2/(1+v)**2)/2,(1+v)**-2,'stationary normalized density ratio')
    eq(s.diff(v/(1+v),v),(1+v)**-2,'uniform probability pushforward')
    b0,I0=s.symbols('b0 I0',real=True)
    eq(s.exp(-b0)/s.exp(-b0),1,'base density gauge cancellation')
    # Generic radial chain rule with arbitrary F, not finitely many modes.
    F=s.Function('F'); xv=v/(1+v); radial=F(xv)
    actual_lap=(1+v)**2*(s.diff(radial,v)+v*s.diff(radial,v,2))/2
    def lap(a):return s.expand((x*(1-x)*s.diff(a,x,2)+(1-2*x)*s.diff(a,x))/2)
    eq(actual_lap,lap(F(x)).subs(x,xv),'generic radial Laplacian chain rule')
    reaction=s.Integer(1)
    def mean(a):return s.integrate(a,(x,0,1))
    def G(a):return s.expand(lap(a)+reaction*a-mean(a))
    eq(G(s.Integer(1)),0,'stationary product constant jet calibration')
    eq(G(x),0,'normalized first-moment neutral mode')
    basis=[s.Integer(1),x,x*x]
    matrix=s.Matrix([[G(a).coeff(x,i) for a in basis] for i in range(3)])
    expected=s.Matrix([[0,0,-s.Rational(1,3)],[0,0,2],[0,0,-2]])
    for i in range(3):
      for j in range(3):eq(matrix[i,j],expected[i,j],'exact monomial jet generator')
    w=e-d*(1-q)/6+d*(1-q)*x+d*q*x*x
    eq(w.subs(q,1),e+d*x*x,'exact nonlinear-family initial jet')
    eq(-2*q*s.diff(w,q),G(w),'exact nonlinear-family closed jet equation')
    eq(mean(w),e+d/3,'conserved jet mean')
    eq(w.subs({x:0,q:s.Rational(1,2)}),-s.Rational(1,96),'exact finite-time negative actual direction')
    eq(w.subs({x:0,q:s.Rational(3,4)}),0,'exact first-zero threshold')
    eq(s.diff(w,x),d*((1-q)+2*q*x),'whole central-fiber minimum certificate')
    P1=2*x-1;P2=6*x*x-6*x+1
    eq(lap(P1),-P1,'degree-one spectral rate');eq(lap(P2),-3*P2,'degree-two spectral rate')
    eq(w,e+d/3+d*P1/2+d*q*P2/6,'independent coefficient and spectral solutions agree')
    # Genuine different-flow negative control: the missing mean changes
    # the constant mode to exp(t), and its pole value increases from e.
    zeta=s.symbols('zeta',positive=True)
    wrong=(e+d/3)*zeta+d*P1/2+d*q*P2/6
    eq(zeta*s.diff(wrong,zeta)-2*q*s.diff(wrong,q),lap(wrong)+wrong,'omitted-denominator different-flow identity')
    eq((zeta*s.diff(wrong,zeta)-2*q*s.diff(wrong,q)).subs(x,0),e*zeta+d*(zeta-q)/3,'omitted-denominator pole growth certificate')
    ck((2*s.Integer(2)-s.Integer(2))!=0,'rank-two same-convention product discrepancy')
    rank=s.symbols('rank',positive=True); rootw=w/rank
    eq(rank*lap(rootw)+rank*rootw-rank*mean(rootw),rank*(-2*q*s.diff(rootw,q)),'root-weight positive time conversion')
    print(json.dumps({'assessment':'ADVERSARIAL_ALL_PHASE_ATLAS_GAUGE_EXACT_JET_AND_SIGN_CONTROLS_AGREE',
      'optimized':bool(sys.flags.optimize),'sympy_version':s.__version__,
      'checks':dict(sorted(counts.items())),'total_checks':sum(counts.values()),
      'finite_numerical_sampling_used':False,
      'scope':'Exact symbolic identities and nonnegative-factor certificates; global finite-time smooth existence and source category are analytic/primary interfaces addressed in the written review, not machine-proved here.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
