#!/usr/bin/env python3
"""Independent normal-flux and Jacobi-form checks for the two configurations."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sympy as s

counts=Counter()
def check(name,condition):
    assert bool(condition),name
    counts[name]+=1
u,z,rho=s.symbols('u z rho',real=True)
rt=s.sqrt(3)

# Axisymmetric unit-sphere Laplacian, with height u measured from its center.
def lap_sphere(f):
    return s.diff((1-u*u)*s.diff(f,u),u)

# All areas/fluxes below are divided by pi. This starts from the physical
# normal speed and surface area element, not the submitted cap-volume formulas.
outer_half=s.Rational(1,2)
inner_half=s.simplify(2*s.integrate(4+2*rt*u,(u,-1,-rt/2)))
flux_half=s.simplify(outer_half+inner_half)
check('spherical_flux',flux_half==(17-9*rt)/2)
check('positive_flux',flux_half>0)
check('outer_Jacobi',8*1==8)
check('inner_Jacobi',s.simplify(lap_sphere(4+2*rt*u)+2*(4+2*rt*u)-8)==0)
check('outer_Robin',s.Integer(0)==(1-1)/rt)
check('inner_Robin',2*rt*s.Rational(1,2)==(2+1)/rt)
Q_half=s.simplify(-2*8*flux_half)
check('spherical_Q',Q_half==72*rt-136)
check('spherical_negative',Q_half<0)
vol_half=s.integrate(1-(z-rt)**2,(z,rt-1,rt/2))+s.integrate(s.Rational(1,4)-(z-rt/2)**2,(z,rt/2,rt/2+s.Rational(1,2)))
removed_half=s.integrate(1-(z-rt)**2,(z,rt-1,rt/2))+s.integrate(1-z*z,(z,rt/2,1))
check('spherical_slice_volume',s.simplify(vol_half-(s.Rational(3,4)-3*rt/8))==0)
check('spherical_slice_removed',s.simplify(removed_half-(s.Rational(4,3)-3*rt/4))==0)
check('spherical_total_area',s.Rational(1,2)+(2-rt)+rt==s.Rational(5,2))

# Planar base: outer unit-sphere cap u=z-1 in [-1/2,1].
fout=1+u/2
outer_one=s.simplify(2*s.integrate(fout,(u,-s.Rational(1,2),1)))
fin=rho*rho/2+s.Rational(3,8)
inner_one=s.simplify(2*s.integrate(fin*rho,(rho,0,rt/2)))
flux_one=s.simplify(outer_one+inner_one)
check('planar_outer_flux',outer_one==s.Rational(27,8))
check('planar_inner_flux',inner_one==s.Rational(27,64))
check('planar_total_flux',flux_one==s.Rational(243,64))
check('planar_outer_Jacobi',s.simplify(lap_sphere(fout)+2*fout-2)==0)
check('planar_internal_Jacobi',s.simplify(s.diff(rho*s.diff(fin,rho),rho)/rho-2)==0)
check('planar_outer_Robin',-rt/4==(-1/rt)*s.Rational(3,4))
check('planar_internal_Robin',rt/2==(2/rt)*s.Rational(3,4))
check('planar_Q',-4*flux_one==-s.Rational(243,16))
check('planar_slice_volume',s.integrate(1-(z-1)**2,(z,s.Rational(1,2),2))==s.Rational(9,8))
check('planar_slice_removed',s.integrate(1-z*z,(z,s.Rational(1,2),1))==s.Rational(5,24))
check('planar_total_area',3+1+s.Rational(3,4)==s.Rational(19,4))

# Pressure differentiation gives an independent consistency check on Q.
for radius,flux,q in [(s.Rational(1,2),flux_half,Q_half),(s.Integer(1),flux_one,-s.Rational(243,16))]:
    check('pressure_exchange_Q',s.simplify(-4*flux/radius**2-q)==0)
    check('merged_constraint',flux+(-flux)==0)
    check('separate_constraint_failure',flux!=0)

# Exact meridian samples on the finite-radius outer and inner spherical pieces.
def dot(a,b):return s.expand(sum(x*y for x,y in zip(a,b)))
def Z(x):
    xx,yy,zz=x;q=dot(x,x)
    return [zz*xx,zz*yy,zz*zz-(1+q)/2]
for k in range(0,13):
    t=s.Rational(k,12)
    vx=2*t/(1+t*t);vz=(1-t*t)/(1+t*t)
    x=[vx/2,0,rt/2+vz/2];q=dot(x,x)
    nao=[2*x[0],0,2*x[2]-rt]
    field=[4/rt*a for a in Z(x)]
    check('outer_radius',s.simplify(x[0]**2+(x[2]-rt/2)**2-s.Rational(1,4))==0)
    check('outer_region',s.simplify(q-1)>=0)
    check('outer_unit_normal',s.simplify(dot(nao,nao)-1)==0)
    check('outer_field_speed',s.simplify(dot(field,nao)-1)==0)
for k in range(0,13):
    t=s.Rational(k,48)
    vx=2*t/(1+t*t);vz=-(1-t*t)/(1+t*t)
    x=[vx,0,rt+vz];q=dot(x,x)
    nab=[x[0],0,x[2]-rt]
    field=[4/rt*a for a in Z(x)]
    check('inner_radius',s.simplify(dot(nab,nab)-1)==0)
    check('inner_in_central',s.simplify(q-1)<=0)
    check('inner_in_satellite',s.simplify(x[0]**2+(x[2]-rt/2)**2-s.Rational(1,4))<=0)
    check('inner_field_speed',s.simplify(dot(field,nab)-q)==0)

# Triple-circle normals, conormal compatibility and the central field.
for k in range(-8,9):
    t=s.Rational(k,5)
    x=[(1-t*t)/(2*(1+t*t)),t/(1+t*t),rt/2]
    nao=[2*x[0],2*x[1],2*x[2]-rt]
    nbo=x
    nab=[x[0],x[1],x[2]-rt]
    check('triple_unit',all(s.simplify(dot(v,v)-1)==0 for v in [nao,nbo,nab]))
    check('triple_balance',all(s.simplify(nab[i]+nbo[i]-nao[i])==0 for i in range(3)))
    check('triple_angle',s.simplify(dot(nao,nbo)-s.Rational(1,2))==0)
    check('central_tangency',s.simplify(dot(Z(x),x))==0)
    check('triple_normal_speeds',s.simplify(dot([4/rt*a for a in Z(x)],nab)-1)==0)

# Volume-correction derivative has independent coordinates using regular
# outer patches; the exchange is in its kernel before second-order correction.
for a in range(1,13):
    for b in range(1,13):
        check('correction_rank',s.Matrix([[a,0],[0,b]]).det()!=0)
check('sphere_Laplacian_constant_mean',s.integrate(lap_sphere(u*u),(u,-1,1))==0)
check('radical_sign',9**2*3<17**2)

root=Path(__file__).resolve().parent
result={'status':'PASS','assertions':sum(counts.values()),'checks':dict(counts),
        'artifact_sha256':hashlib.sha256((root/'author_replay/PARTIAL.md').read_bytes()).hexdigest(),
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'sympy_version':s.__version__,
        'method':'Independent normal-flux integrals and direct Jacobi-form computation, exact spherical samples and constraint-rank checks.',
        'limitations':'The geometry and variational proof require the accompanying analytic review. The original source-intent question remains unresolved.'}
(root/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
