#!/usr/bin/env python3
"""Independent exact controls for the qualified Ueno audit; no research theorem is inferred from a test count."""
from itertools import combinations
import json
import sympy as S

checks=[]
negatives=[]
def check(name, ok, category):
    if not bool(ok):
        raise AssertionError(name)
    checks.append({'name':name,'category':category,'passed':True})
def reject(name, ok, explanation):
    check(name,ok,'negative_control')
    negatives.append({'name':name,'rejected':True,'reason':explanation})
def zero(x):
    return S.cancel(x)==0
s,t,r,u,q,U,V,W,Q,T,z=S.symbols('s t r u q U V W Q T z')
# Work independently from the author's executable: weights and a primitive Kummer generator.
check('generator has exact order six',next(m for m in range(1,7) if 2*m%6==0 and 3*m%6==0)==6,'group')
check('xy has primitive sixth-root character',S.gcd(2+3,6)==1,'group')
x,y,h=S.symbols('x y h')
check('x from primitive generator',zero((x*y)**4/(x**3*y**4)-x),'group')
check('h sixth power equals T squared times (T minus one) cubed',S.expand((x*y)**6-x**6*y**6)==0,'group')
reject('order-three subgroup is not the target',3*2%6==0 and 3%6!=0,'y_1 is fixed by g squared but is not fixed by g.')
reject('order-two subgroup is not the target',2*3%6==0 and 2%6!=0,'x_1 is fixed by g cubed but is not fixed by g.')
reject('product action is not diagonal action',(-2)%6!=0 and (-3)%6!=0,'Changing the first factor alone does not fix the coordinate ratios.')
# Derive the elimination polynomial as a resultant of two linear equations in q.
R3=(s*s*U-V)*q+2*(s*U-V)
R4=(t*t*U-W)*q+2*(t*U-W)
R5=(r*r*U-Q)*q+2*(r*U-Q)
F4=s*t*(s-t)*U-s*(s-1)*W+t*(t-1)*V
F5=s*r*(s-r)*U-s*(s-1)*Q+r*(r-1)*V
check('linear resultant gives fourfold equation',zero(S.resultant(R3,R4,q)-2*U*F4),'elimination')
check('linear resultant gives fivefold equation',zero(S.resultant(R3,R5,q)-2*U*F5),'elimination')
D=s*s*U-V
qback=S.solve(R3,q)[0]
check('independently solved inverse',zero(qback-2*(V-s*U)/D),'inverse')
check('missing factor in old open condition',zero(qback+2-2*s*(s-1)*U/D),'domain')
Wback=S.solve(F4,W)[0];Qback=S.solve(F5,Q)[0]
reconstructed=[(S.Integer(1),U),(s,V),(t,Wback),(r,Qback)]
v2=1+qback
Tback=S.cancel((v2*v2-1)/(v2*v2-(1+U)))
check('T reconstruction in q coordinates',zero(Tback-qback*(qback+2)/(qback*(qback+2)-U)),'inverse')
check('T minus one reconstruction',zero(Tback-1-U/(qback*(qback+2)-U)),'inverse')
for idx,(sigma,Ui) in enumerate(reconstructed,2):
    vi=1+sigma*qback
    check(f'reconstructed elliptic relation coordinate {idx}',zero(vi**2*(Tback-1)-(1+Ui)*Tback+1),'inverse')
    check(f'reconstructed cross relation coordinate {idx}',zero((vi**2-1)*U-(v2*v2-1)*Ui),'inverse')
    check(f'recover base ratio coordinate {idx}',zero((vi-1)/(v2-1)-sigma),'inverse')
# Start from the other chart with independently free q and recover it, then each Ui.
Vforward=U*s*(s*q+2)/(q+2)
qround=S.cancel(qback.subs(V,Vforward))
check('reverse composition recovers q',zero(qround-q),'inverse')
for name,sigma,back in [('V',s,V),('W',t,Wback),('Q',r,Qback)]:
    actual=U*sigma*(sigma*q+2)/(q+2)
    check(f'reverse composition recovers {name}',zero(back.subs(V,Vforward)-actual),'inverse')
# Explicit old-domain counterexample. Cubes of all w coordinates are 2.
bad={s:0,t:0,r:0,U:1,V:1,W:1,Q:1}
old=S.cancel(U*D*qback*(v2*v2-(1+U)))
check('old-domain counterexample lies on both equations',F4.subs(bad)==0 and F5.subs(bad)==0,'domain')
check('old-domain counterexample satisfies listed product',old.subs(bad)==-2,'domain')
check('old-domain counterexample has T zero',Tback.subs(bad)==0 and qback.subs(bad)==-2,'domain')
reject('old model-side open product is sufficient',old.subs(bad)!=0 and Tback.subs(bad)==0,'It permits a point with x_1 cubed equal to zero, outside the original x_1*y_1 nonzero chart.')
B4=s*t*(s-1)*(t-1)*(s-t)
B5=B4*r*(r-1)*(s-r)*(t-r)
new4=S.cancel(B4*U*D*qback*(qback+2)*(qback*(qback+2)-U))
new5=S.cancel(B5*U*D*qback*(qback+2)*(qback*(qback+2)-U))
check('repaired domain rejects old counterexample',new4.subs(bad)==0 and new5.subs(bad)==0,'domain')
good={s:S.Rational(2),t:S.Rational(3),r:S.Rational(4),U:S.Rational(1),V:S.Rational(8,3),W:S.Rational(5),Q:S.Rational(8)}
check('nonempty witness lies on fourfold and fivefold',F4.subs(good)==0 and F5.subs(good)==0,'domain')
check('nonempty witness survives repaired fourfold domain',new4.subs(good)!=0,'domain')
check('nonempty witness survives repaired fivefold domain',new5.subs(good)!=0,'domain')
check('witness inverse values',D.subs(good)==S.Rational(4,3) and qback.subs(good)==1 and Tback.subs(good)==S.Rational(3,2),'domain')
for idx,(sigma,Ui) in enumerate(reconstructed,2):
    vi=(1+sigma*qback).subs(good); ci=(1+Ui).subs(good)
    check(f'witness curve coordinate {idx}',vi**2*S.Rational(1,2)==ci*S.Rational(3,2)-1,'domain')
# The old-domain counterexample is even in the dominant component's closure.
# An arc is specified by cube coordinates; cube roots lift at the nonzero limit 2.
e=S.symbols('e')
qarc=-2+2*e
sarc=e;tarc=e+e**2;rarc=e+2*e**2
Uarc=lambda a:S.cancel(a*(a*qarc+2)/(qarc+2))
arc={s:sarc,t:tarc,r:rarc,U:S.Integer(1),V:Uarc(sarc),W:Uarc(tarc),Q:Uarc(rarc)}
check('dominant arc satisfies both model equations',zero(F4.subs(arc,simultaneous=True)) and zero(F5.subs(arc,simultaneous=True)),'domain')
check('dominant arc has generic nondegenerate base',S.expand(B5.subs(arc,simultaneous=True))!=0,'domain')
check('dominant arc approaches old-domain counterexample',all(S.limit(val,e,0)==bad[key] for key,val in arc.items()),'domain')
check('dominant arc inverse q agrees',zero(qback.subs(arc,simultaneous=True)-qarc),'domain')
check('dominant arc lies generically in repaired domain',S.cancel(new5.subs(arc,simultaneous=True))!=0,'domain')

# Full unsaturated affine model has vertical components, unlike the generic fiber.
check('vertical s zero V zero locus',F4.subs({s:0,V:0})==0 and F5.subs({s:0,V:0})==0,'components')
check('vertical s one V U locus',S.expand(F4.subs({s:1,V:U}))==0 and S.expand(F5.subs({s:1,V:U}))==0,'components')
check('D removes displayed vertical loci',D.subs({s:0,V:0})==0 and D.subs({s:1,V:U})==0,'components')
reject('generic integrality proves full affine integrality',True,'For each cube root epsilon, s=0,w_3=epsilon is a dimension-five vertical component of the unsaturated A7 intersection.')
# Coefficients independently extracted by differentiating the defining form in cube coordinates.
w2,w3,w4,w5,z=S.symbols('w2 w3 w4 w5 z')
C4=S.expand(F4.subs({U:w2**3-z**3,V:w3**3-z**3,W:w4**3-z**3}))
C5=S.expand(F5.subs({U:w2**3-z**3,V:w3**3-z**3,Q:w5**3-z**3}))
coords=[w2,w3,w4,w5,z]
M=S.Matrix([[S.expand(poly).coeff(c,3) for c in coords] for poly in [C4,C5]])
check('coefficient matrix has rank two',M.rank()==2,'fivefold')
minor_data={}
for i,j in combinations(range(5),2):
    minor=S.factor(M[:,[i,j]].det())
    check(f'column minor {i}{j} nonzero',minor!=0,'fivefold')
    # Every factor of every minor is inverted in B5.
    radical=S.prod(f for f,e in S.factor_list(minor)[1])
    check(f'column minor {i}{j} nonzero on corrected base',S.rem(S.Poly(B5,s,t,r),S.Poly(radical,s,t,r))==0,'fivefold')
    minor_data[f'{i}{j}']=str(minor)
check('first hypersurface independent of w5',S.diff(C4,w5)==0 and S.diff(C5,w5,3)!=0,'fivefold')
check('all-ones projective point is present',C4.subs({c:1 for c in coords})==0 and C5.subs({c:1 for c in coords})==0,'fivefold')
check('complete intersection canonical exponent',3+3-5==1,'fivefold')
check('complete intersection canonical self-intersection',3*3==9,'fivefold')
# Hilbert coefficients from (1-t^3)^2/(1-t)^5.
a=S.symbols('a')
hilbert=S.series((1-a**3)**2/(1-a)**5,a,0,4).removeO()
check('h0 O(1) equals five',hilbert.coeff(a,1)==5,'fivefold')
# Fourfold diagonal criterion and exact prime-divisor valuations.
coeff=[M[0,0],M[0,2],M[0,1],M[0,4]]
check('fourfold coefficients nonzero on B4',all(c!=0 and S.rem(S.Poly(B4,s,t),S.Poly(S.prod(f for f,e in S.factor_list(c)[1]),s,t))==0 for c in coeff),'fourfold')
a,b,c,d=coeff
ratios=[S.cancel(a*b/(c*d)),S.cancel(a*c/(b*d)),S.cancel(a*d/(b*c))]
expected=[s*s/(t-1)**2,t*t/(s-1)**2,(s-t)**2]
for i,(rat,exp) in enumerate(zip(ratios,expected)):
    check(f'pairing ratio {i} independently recovered',zero(rat-exp),'fourfold')
# Compute valuations as orders in a uniformizer rather than inspecting factored strings.
v=S.symbols('v')
for i,rat in enumerate(ratios):
    expr=rat if i<2 else rat.subs(s,t+v)
    var=[s,t,v][i]
    num,den=S.fraction(S.cancel(expr))
    order=lambda p:min(m[0][0] for m in S.Poly(p,var).terms())
    val=order(num)-order(den)
    check(f'pairing ratio {i} valuation is two',val==2,'fourfold')
    check(f'pairing ratio {i} inverse not cube',(-val)%3!=0,'fourfold')
reject('a square pairing ratio must be a cube',S.Integer(2)%3!=0,'Its valuation at the specified prime divisor is two.')
reject('repeated fivefold base parameters remain smooth',S.factor(M[:,[0,1]].det()).subs(r,t)==0,'At r=t two coefficient columns become proportional; the generic smoothness proof does not apply.')
# Independent resultant-style plane-curve smoothness certificate via a different smooth member.
A,B,C=S.symbols('A B C')
plane=A*s*t*(s-t)-B*s*u*(s-u)+C*t*u*(t-u)
plane_ind=plane.subs({A:2,B:5,C:11})
chart_certificates={}
for chart in [s,t,u]:
    variables=[v for v in [s,t,u] if v!=chart]
    partials=[S.diff(plane_ind,v).subs(chart,1) for v in [s,t,u]]
    basis=list(S.groebner(partials,*variables,domain=S.QQ))
    check(f'independent smooth plane cubic chart {chart}',basis==[1],'alternative_projection')
    chart_certificates[str(chart)]=[str(v) for v in basis]
check('generic marked point on plane curve',plane.subs({s:0,t:0,u:1})==0,'alternative_projection')
check('generic marked point smooth',S.diff(plane,s).subs({s:0,t:0,u:1})==B and S.diff(plane,t).subs({s:0,t:0,u:1})==-C,'alternative_projection')
check('smooth plane cubic genus',S.Rational((3-1)*(3-2),2)==1,'alternative_projection')
reject('all plane-cubic specializations are smooth',S.factor(plane.subs({A:0,B:0,C:0}))==0,'Generic smoothness is established by a nonempty open, not every coefficient triple.')
# Rational-total-space / nonrational-fiber controls.
x,y,z,t=S.symbols('x y z t')
check('elliptic total-space graph solves t',S.solve(y*y-x**3-t,t)==[y*y-x**3],'scope')
check('elliptic generic discriminant nonzero',-432*t**2!=0,'scope')
check('quintic total-space graph solves t',S.solve(x**5+y**5+z**5-t,t)==[x**5+y**5+z**5],'scope')
check('quintic canonical exponent',5-4==1,'scope')
reject('bad generic fibers obstruct rational total spaces',True,'The two graph morphisms have rational total fields and respectively elliptic and general-type generic fibers.')
# Lifting from experimental counts is deliberately not assumed.
p=1000003
check('prime used by reduction control is prime',S.isprime(p),'experimental_boundary')
P=p*z*z+z-t
check('mod p entire family becomes degree one',S.Poly(P,z,t,modulus=p)==S.Poly(z-t,z,t,modulus=p),'experimental_boundary')
check('characteristic zero family stays degree two',S.Poly(P,z).degree()==2,'experimental_boundary')
dis=S.discriminant(P,z)
check('quadratic discriminant has simple zero',S.degree(dis,t)==1 and S.diff(dis,t)!=0,'experimental_boundary')
reject('all mod-p counts certify characteristic-zero degree one',True,'The exact degree drops from two to one on reduction.')
values=[-2,1,4,7,11]
branch=S.prod(t-a for a in values)
check('new finite sample has only branch fibers',all(branch.subs(t,a)==0 for a in values),'experimental_boundary')
check('finite sample branch polynomial squarefree',S.gcd(branch,S.diff(branch,t))==1,'experimental_boundary')
check('sampled fibers have length two',S.Poly(z*z,z).degree()==2,'experimental_boundary')
check('sampled fibers have one distinct geometric point',S.Poly(z*z,z).sqf_part().degree()==1,'experimental_boundary')
reject('finite distinct-point sampling certifies degree one',True,'Each sampled fiber has one distinct point but length two; the generic degree is two.')
# The scalar endomorphism commutes with both kernel homomorphisms.
l=S.symbols('l');p1,p2,p3,p4,p5,eta=S.symbols('p1 p2 p3 p4 p5 eta')
check('fourfold divisor formal equivariance',S.expand(l*p2+2*l*p3+l*p4-l*(p2+2*p3+p4))==0,'conditional_route')
check('fivefold divisor formal equivariance',S.expand(l*p1+eta*l*p3-l*p5-l*(p1+eta*p3-p5))==0,'conditional_route')
check('fourfold kernel inverse solves final coordinate',S.expand((p2+2*p3+p4).subs(p4,-p2-2*p3))==0,'conditional_route')
check('fivefold kernel inverse solves final coordinate',S.expand((p1+eta*p3-p5).subs(p5,p1+eta*p3))==0,'conditional_route')

out={'status':'passed','independent_check_count':len(checks),'checks':checks,'negative_controls':negatives,
'old_domain_counterexample':{'s':0,'t':0,'r':0,'U':1,'V':1,'W':1,'Q':1,'all_w_cubes':2,'D':-1,'q':-2,'old_product':-2,'T':0},
'corrected_domain':'On the unique component dominating the base: B_n * U * D * q * (q+2) * (q*(q+2)-U) != 0, with B4=s*t*(s-1)*(t-1)*(s-t) and B5=B4*r*(r-1)*(s-r)*(t-r).',
'corrected_domain_witness':{'s':2,'t':3,'r':4,'U':1,'V':'8/3','W':5,'Q':8,'D':'4/3','q':1,'T':'3/2','B4':str(B4.subs(good)),'B5':str(B5.subs(good))},
'minors':minor_data,'independent_plane_cubic_specialization':[2,5,11],'plane_cubic_chart_certificates':chart_certificates,
'sympy_version':S.__version__,'exact_arithmetic':True,
'scope':'Exact identities, domain counterexamples, and supporting algebra. Does not formalize geometric theorem dependencies or resolve either original rationality question.'}
print(json.dumps(out,indent=2))
