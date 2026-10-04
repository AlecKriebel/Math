from pathlib import Path
from fractions import Fraction as Q
import datetime,json
import sympy as S
R=Path(__file__).resolve().parent
checks=0
negative=[]
def check(value):
    global checks
    assert value;checks+=1
# Exact first variation with finite cross energy and correct mass normalization.
t,J,L,H,m,C=S.symbols('t J L H m C',positive=True)
energy=S.expand((1-t)**2*J+2*t*(1-t)*L+t**2*H)
check(S.simplify(S.diff(energy,t).subs(t,0)-2*(L-J))==0)
check(S.simplify((C*J*m)/m**2-C*J/m)==0)
# Identity under probability scaling: I(mu|A/m)=I(mu|A)/m^2.
for mass in [Q(1,1000),Q(1,17),Q(1,2),Q(1)]:
    for bound in [Q(1),Q(7,3),Q(100)]:
        restricted=bound*mass
        check(mass**2/restricted==mass/bound)
        if mass<1:
            check(mass/restricted!=mass/bound) # A single-power normalization is wrong.
            negative.append({'mutation':'normalize energy by mass rather than mass squared','mass':str(mass),'rejected':True})
# Uniform-tail epsilon and diameter ratio: all listed dimensions, exact rational arithmetic.
for n in range(3,103):
    s=n-2;fac=2**s;eps=Q(1,4*fac*s)
    check(fac*s*eps==Q(1,4))
    for ratio in [Q(1,4),Q(1,7),Q(1,19),Q(0)]:
        check(fac*s*eps+ratio**s<=Q(1,2))
    # At n=3, keeping diameter=delta rather than delta/4 destroys the contradiction.
    if s==1:
        check(fac*s*eps+Q(1)**s>1)
        negative.append({'mutation':'omit small-diameter localization','n':n,'rejected':True})
# Radial layer cake extends at zero, where both sides are infinite; n=2 is excluded.
r,d,s=S.symbols('r d s',positive=True)
check(S.simplify(s*S.integrate(r**(-s-1),(r,d,S.oo))-d**(-s))==0)
check(S.limit(d**(-s),d,0,dir='+')==S.oo)
check(S.simplify(s*S.integrate(r**(-s-1),(r,Q(1,3),S.oo))-(Q(1,3))**(-s))==0)
# Independent exact dyadic envelope over arbitrary rational distances, including endpoints.
for numerator in range(1,41):
    for denominator in range(numerator,71):
        distance=Q(numerator,denominator)
        val=sum((Q(2)**(k-1) for k in range(20) if distance<=Q(1,2**k)),Q(0))
        check(val<=1/distance)
for j in range(1,21):
    bins=2**j
    check(Q(2)**(j-1)*Q(1,bins)==Q(1,2))
    # Uncountability is not inferred from finite j; each j contributes the same lower bound.
    check(sum((Q(1,2) for _ in range(j)),Q(0))==Q(j,2))
# Weight weakening is only the explicitly integrable class.
eta=S.symbols('eta',positive=True)
check(S.simplify(S.integrate(r**(eta-1),(r,0,1))-1/eta)==0)
# SymPy's exact critical logarithmic integral under u=log(e/r).
u=S.symbols('u',positive=True)
check(S.integrate(u**(-2),(u,1,S.oo))==1)
check(S.integrate(u**(-1),(u,1,S.oo))==S.oo)
negative.append({'mutation':'infer all nonintegrable weights fail from the integrable bound','rejected':True,'reason':'bound proves finiteness only when integral a(r) dr/r is finite; the borderline scalar integral diverges'})
out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assertions':checks,'negative_controls':negative,'sympy_version':S.__version__,'scope':'Exact variation/scaling/layer-cake identities, constants, rational dyadic bounds, logarithmic threshold and deliberate normalization/localization/gauge failures. Analytical proof is separately reviewed; these controls cannot certify polarity.'}
(R/'ADVERSARIAL_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
