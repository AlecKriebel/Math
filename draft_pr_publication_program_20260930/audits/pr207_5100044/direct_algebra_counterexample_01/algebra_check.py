"""Independent symbolic audit; no submitted programs imported or executed."""
import json
import sympy as s
from pathlib import Path

k,t,z,U,V,W=s.symbols('k t z U V W')
q=1-t
uv={U:1-2*k*k*t+k*k*t*t,V:1-2*t+k*k*t*t,W:1-k*k*t*t}
D=1-k*k*t*z*z
checks={}
def check(name, expr):
    residual=s.factor(s.together(expr).subs(uv))
    checks[name]={'residual':str(residual),'passed':residual==0}

# Every check is an identity in independent indeterminates k,t,z.
check('Eq9_UplusV',U+V-2*q*(1-k*k*t))
check('Eq9_U2_minus_k2V2',U*U-k*k*V*V-(1-k*k)*W*W)
check('Eq9_double_argument_cn',V-(q-t*(1-k*k*t)))
check('Eq9_double_argument_dn',U-((1-k*k*t)-k*k*t*q))
# Focal-distance product after substitution of addition formulas, divided by alpha^2.
check('Eq11_distance_product',(1-k*k*t)/q +2*k*z*(1-k*k*t)/D+k*k*(z*z-t)/D-(1+k*z)*(U+k*V*z)/(q*D))
# Determinant: base determinant + focus translation, / (2 alpha b h dn(v) dn(u)).
check('Eq12_translated_det',(1+k*z)/D-(1/D+k*z/D))
# Explicit Jacobi endpoint determinant. Reduce its polynomial numerator in
# the defining quadrics, rather than assuming the desired cross product.
c0,d0,h,cv,dv=s.symbols('c0 d0 h cv dv')
DD=1-k*k*h*h*z*z
sminus=(z*cv*dv-h*c0*d0)/DD
splus=(z*cv*dv+h*c0*d0)/DD
cminus=(c0*cv+z*h*d0*dv)/DD
cplus=(c0*cv-z*h*d0*dv)/DD
det_over_b=(-dv/cv*sminus-k)*cplus-cminus*(-dv/cv*splus-k)
num=s.together(det_over_b-2*h*dv*d0*(1+k*z)/DD).as_numer_denom()[0]
G=s.groebner([c0*c0+z*z-1,d0*d0+k*k*z*z-1,cv*cv+h*h-1,dv*dv+k*k*h*h-1],c0,d0,cv,dv,h,z,k)
res=s.factor(G.reduce(s.expand(num))[1])
checks['Eq12_explicit_endpoint_determinant']={'residual':str(res),'passed':res==0}
# The unshifted shoelace edge and the dn endpoint average.
# det/b=2 a h cv d0/DD=2 h dv d0/DD.
num=s.together(dv/cv*(splus*cminus-sminus*cplus)-2*h*dv*d0/DD).as_numer_denom()[0]
res=s.factor(G.reduce(s.expand(num))[1])
checks['Eq4_explicit_endpoint_cross_product']={'residual':str(res),'passed':res==0}
# E+/(C dn(u)D) is the quoted rational function.
# Pair E(z)+E(-z), multiply by dn(u), use dn(u)^2=1-k^2 z^2.
check('Eq14_pairing',(1-k*k*z*z)*(1/((1+k*z)*(U+k*V*z)**2)+1/((1-k*z)*(U-k*V*z)**2))-2*(U*U+k*k*V*(V+2*U)*z*z)/(U*U-k*k*V*V*z*z)**2)
# V=0 reduction of B: D/dn(u) = q/dn(u)+t dn(u).
check('Eq19_N4_reduction',D-(q+t*(1-k*k*z*z)))
# Squared ordinary focal distance: (Px-c)^2+Py^2=(a+c sn(w))^2.
a,b,c=s.symbols('a b c')
expr=(-a*z-c)**2+b*b*(1-z*z)-(a+c*z)**2
res=s.factor(expr.subs(b*b,a*a-c*c))
checks['Eq6_focal_distance_squared']={'residual':str(res),'passed':res==0}
# Confocal nesting from canonical coordinates.
check('canonical_confocal_difference',(1-k*k*t)/q-(1-k*k)/q-k*k)
check('canonical_outer_minus_caustic_major',(1-k*k*t)/q-1-(1-k*k)*t/q)
check('canonical_outer_minus_caustic_minor',(1-k*k)/q-(1-k*k)-(1-k*k)*t/q)
# N4 shoelace, exact axial inverse vertices.
axial=[(-c/a**2,b/a**2),(-1/(a+c),0),(-c/a**2,-b/a**2),(1/(a-c),0)]
area=s.factor(sum(axial[j][0]*axial[(j+1)%4][1]-axial[j][1]*axial[(j+1)%4][0] for j in range(4))/2)
res=s.factor(s.together(area-2/(a*b)).as_numer_denom()[0].expand().subs(c*c,a*a-b*b))
checks['N4_inverse_area_2_over_ab']={'residual':str(res),'passed':res==0,'computed_before_confocal_substitution':str(area)}
result={'sympy_version':s.__version__,'checks':checks,'all_passed':all(x['passed'] for x in checks.values())}
Path(__file__).with_name('algebra_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert result['all_passed']
