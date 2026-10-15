#!/usr/bin/env python3
"""Independent exact controls for the 3009 review, not topology certificates."""
import json
from fractions import Fraction as F
from pathlib import Path
import sympy as s
out={}
def check(name, value):
    assert bool(value), name
    out[name]="PASS"

# Derive the spherical metric independently from the embedding.
x,y,u,v=s.symbols("x y u v", real=True)
def embed(a,b):
    d=1+a*a+b*b
    return s.Matrix([2*a/d,2*b/d,(a*a+b*b-1)/d])
a,b=embed(x,y),embed(u,v)
check("embedding_norm",s.factor(a.dot(a)-1)==0)
check("chordal_square",s.factor((a-b).dot(a-b)-4*((x-u)**2+(y-v)**2)/((1+x*x+y*y)*(1+u*u+v*v)))==0)
check("distance_to_infinity",s.factor((a-s.Matrix([0,0,1])).dot(a-s.Matrix([0,0,1]))-4/(1+x*x+y*y))==0)
d,z=s.symbols("d z", positive=True)
tail=4*d*d/((1+(d+z)**2)*(1+z*z))
check("tail_vanishes",s.limit(tail,z,s.oo)==0)
negative=-tail*(2*(d+z)/(1+(d+z)**2)+2*z/(1+z*z))
check("tail_strict_decrease_formula",s.factor(s.diff(tail,z)-negative)==0)
check("tail_denominator_positive",tail.is_positive is True)

# Exact rational vector cases, including tangential and inward perturbations.
directions=[(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(-3,5),F(4,5))]
perturb=[(F(i,2),F(j,2)) for i in range(-2,3) for j in range(-2,3) if i*i+j*j<=4]
n_metric=n_proper=0
for D in (F(1,2),F(1),F(3)):
    for R in (2*D,3*D,7*D):
        for radius in (R,R+D,2*R):
            for vx,vy in directions:
                X=(radius*vx,radius*vy)
                for dx,dy in perturb:
                    E=(D*dx,D*dy); Y=(X[0]+E[0],X[1]+E[1])
                    yy=sum(c*c for c in Y)
                    disp2=sum(c*c for c in E)
                    q2=4*disp2/((1+radius*radius)*(1+yy))
                    B=4*D*D/((1+R*R)*(1+(R-D)**2))
                    check(f"metric_{n_metric}",q2<=B); n_metric+=1
                    for t in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
                        H=(X[0]+t*E[0],X[1]+t*E[1])
                        check(f"proper_{n_proper}",sum(c*c for c in H)>=(radius-D)**2)
                        n_proper+=1

# Hypothesis controls: full-iterate uniformity cannot be dropped.
# A radial twist by angle 2*pi*r on the unit disk, identity outside, fixes
# the boundary and has all full orbits of diameter <=2. For any m>=1,
# r=1-1/(2m) has m-th iterate angle 2*pi*m-pi and displacement 2r>=1.
m=s.symbols("m", integer=True, positive=True)
r=1-1/(2*m)
check("twist_angle_mod_two_pi",s.simplify(m*r-(m-s.Rational(1,2)))==0)
check("twist_displacement_lower_formula",s.simplify(2*r-1-(m-1)/m)==0)
for k in range(1,25):
    check(f"twist_no_return_{k}",2*r.subs(m,k)>=1)
# Nontrivial recurrent S^3 maps can have a whole fixed circle.
M=s.diag(-1,-1,1,1)
check("S3_rotation_orthogonal",M.T*M==s.eye(4))
check("S3_rotation_orientation",M.det()==1)
check("S3_rotation_period_two",M*M==s.eye(4) and M!=s.eye(4))
check("S3_fixed_plane_dimension",len((M-s.eye(4)).nullspace())==2)
# Every orbit of a plane irrational rotation is individually bounded, but
# diameters cannot have one global bound; already its first displacement
# squared is radius^2 times a positive constant for a nonzero angle.
rho,c,t=s.symbols("rho c t", real=True)
check("rotation_displacement_scale",s.expand((rho*c-rho)**2+(rho*t)**2-rho*rho*((c-1)**2+t*t))==0)
check("disjoint_fixed_point_regions",F(7)>F(3)+F(3))

result={
    "passed":len(out),"failed":0,"metric_vector_cases":n_metric,
    "proper_homotopy_vector_cases":n_proper,"sympy_version":s.__version__,
    "scope":"Exact algebraic controls and explicit hypothesis countercontrols; no finite computation certifies the imported planar theorems or the higher-dimensional problem.",
    "checks":out
}
Path(__file__).with_name("independent_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="checks"},indent=2))
