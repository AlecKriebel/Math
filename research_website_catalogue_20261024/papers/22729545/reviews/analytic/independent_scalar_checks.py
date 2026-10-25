"""Fresh symbolic derivations of selected scalar inverse identities.
No manuscript implementation or output imported; bounded algebra controls only.
"""
from pathlib import Path
import hashlib,json
import sympy as s
out=Path(__file__).resolve().parent
v,w,t=s.symbols('v w t', nonnegative=True)
a,b,c,q,p,z=s.symbols('a b c q p z', positive=True)
g,r=s.symbols('g r', positive=True)
checks=[]
def zero(expr,name):
    assert s.simplify(expr)==0,name
    checks.append(name)
# Build the killed two-state partition dynamics for three initially co-located
# blocks: before any merger total rate 3a, specified ab merger rate a, afterward
# no second merger for w with rate a. The ab|z state has killed rate a and no
# possible second merger in the frozen population schedule.
F=p*a*s.exp(-a*v)+z*a*s.exp(-3*a*v-a*w)
zero(s.integrate(s.limit(F,w,s.oo),(v,0,s.oo))-p,'triple grouped mass by frozen-generator integral')
G=p+q*s.exp(-a*t)+z*s.exp(-a*t)
zero(G.subs(t,0)-s.limit(G,t,s.oo)-(q+z),'repeated positive pair rates retain separated atom')
# Given literal first and second density for earlier arm, solve both survival
# words and both rates, treating initial masses as unnormalized.
D=q*g**2*a*s.exp(-a*t)*c*s.exp(-c*w)
g1=s.limit(D,w,0)/(q*g**2*c)
A1=1-s.integrate(g1,(t,0,v))
zero(g1.subs(t,v)/A1-a,'first arm density divided by surviving mass')
f=q*(g**2*a*s.exp(-a*t)+(1-g)**2*b*s.exp(-b*t))
g2=(f/q-g**2*g1)/(1-g)**2
A2=1-s.integrate(g2,(t,0,v))
zero(g2.subs(t,v)/A2-b,'second arm recovered after first arm subtraction')
# Earlier-route mass passes through already known ancestral reticulation r.
# Its split component remains separated, while original later arm is isolated.
q1=p*(r**2*s.exp(-a*t)+(1-r)**2*s.exp(-b*t))
q2=q*s.exp(-c*t)
qt=q1+q2
zero(-s.diff(qt-q1,t)/(qt-q1)-c,'longer arm through ancestral reticulation')
# Added bypass mass must be included in the earlier-route initial mass.
qt=(p+z)*s.exp(-a*t)+q2
zero(-s.diff(qt-(p+z)*s.exp(-a*t),t)/(qt-(p+z)*s.exp(-a*t))-c,'longer arm with bypass entrants')
# Two-epoch bi-unary marked density and survival depend on the entire word.
u,d=s.symbols('u d', positive=True)
Ksurv=1-g+g*s.exp(-a*u-b*d)
zero(s.diff(Ksurv,d)+g*b*s.exp(-a*u-b*d),'whole donor word second-epoch density')
# Hostile controls: separated atom cannot vanish at balanced equal-rate point;
# replacing gamma^2 by gamma, or losing bypass mass, changes the inverse.
neg={
 'balanced_equal_rate_routing_not_single_Kingman':s.simplify((2*g*(1-g)+g*g*s.exp(-a*t)+(1-g)**2*s.exp(-a*t)-s.exp(-a*t)).subs({g:s.Rational(1,2),a:1,t:1})),
 'missing_gamma_square':s.simplify((s.limit(D,w,0)/(q*g*c)-a*s.exp(-a*t)).subs({q:1,g:s.Rational(1,3),a:1,t:1})),
 'lost_bypass_mass':s.simplify((-s.diff(qt-p*s.exp(-a*t),t)/(qt-p*s.exp(-a*t))-c).subs({p:1,z:1,q:1,a:1,c:2,t:1})),
 'discarding_donor_breakpoint':s.simplify((Ksurv-(1-g+g*s.exp(-a*(u+d)))).subs({g:s.Rational(1,2),a:1,b:2,u:1,d:1}))
}
assert all(x!=0 for x in neg.values())
result={'status':'PASS','symbolic_identities':checks,'rejected_wrong_formulas':{k:str(v) for k,v in neg.items()},'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':__doc__}
(out/'independent_scalar_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
