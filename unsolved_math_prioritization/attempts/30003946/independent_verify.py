#!/usr/bin/env python3
"""Independent exact finite checks. No imported candidate code, source corpus or PDE certification."""
import argparse
from fractions import Fraction as F
from itertools import product
import json
import os
import sys

MUTATIONS = ('flat_laplacian', 'flat_orientation', 'area_normalization',
             'curvature_sign', 'cusp_amplitude', 'cusp_harmonicity',
             'collapsed_trace_injectivity', 'weak_lower_semicontinuity_direction',
             'quotient_trace_equals_side_incidence')


def run(mutation=None):
    checks = []
    def check(name, ok, evidence):
        if not ok:
            raise ValueError(name)
        checks.append({'name': name, 'evidence': evidence})
    # A cubic's centered first derivative has a quadratic step error. Richardson
    # cancellation below is exact, and the centered second derivative is exact.
    def d1(fn, z, j):
        def central(h):
            a,b=list(z),list(z); a[j]+=h; b[j]-=h
            return (fn(*a)-fn(*b))/(2*h)
        return (4*central(F(1,2))-central(F(1)))/3
    def d2(fn, z, j):
        a,b=list(z),list(z); a[j]+=1; b[j]-=1
        return fn(*a)-2*fn(*z)+fn(*b)
    mixed = -2 if mutation=='flat_laplacian' else -3
    linear = 1 if mutation=='flat_orientation' else -1
    first = lambda x,t:x
    second = lambda x,t:t*t*t+linear*t+mixed*t*x*x
    grid = [F(-2),F(-1,2),F(0),F(1,3),F(2)]
    laps=[]; flux=[]; jac=[]
    for z in product(grid,repeat=2):
        laps.append(d2(first,z,0)+d2(first,z,1))
        laps.append(d2(second,z,0)+d2(second,z,1))
        det=d1(first,z,0)*d1(second,z,1)-d1(first,z,1)*d1(second,z,0)
        jac.append(det-(3*z[1]**2-1-3*z[0]**2))
    for t in grid: flux.append(d1(second,(F(0),t),0))
    check('flat_harmonicity_by_exact_differences', all(v==0 for v in laps), {'evaluations':len(laps),'degree_bound':3})
    check('flat_edge_flux_by_exact_differences', all(v==0 for v in flux), {'edge_tests':len(flux)})
    check('flat_jacobian_polynomial_interpolation', all(v==0 for v in jac), {'grid_points':len(jac),'degree_per_variable_at_most':2})
    det=lambda z:d1(first,z,0)*d1(second,z,1)-d1(first,z,1)*d1(second,z,0)
    neg,pos=det((F(1,4),F(0))),det((F(1,4),F(1)))
    check('flat_opposite_orientation_inside_domain',neg==F(-19,16) and pos==F(29,16),{'negative':str(neg),'positive':str(pos),'largest_radius_squared':'17/16 < 4'})
    # An independent tensor-grid identity test. Both sides are quadratic in four
    # variables, so three distinct values per variable determine the polynomial.
    alpha=1 if mutation=='area_normalization' else 2
    matrix_cases=0
    for a,b,c,d in product([F(-2,3),F(0),F(5,4)],repeat=4):
        e=a*a+b*b+c*c+d*d; J=a*d-b*c
        check_value=e-alpha*J-(a-d)**2-(b+c)**2
        if check_value!=0: raise ValueError('energy_area_exact_interpolation')
        matrix_cases+=1
    check('energy_area_exact_interpolation',matrix_cases==81,{'points':matrix_cases,'degree_bound':2,'energy_prefactor':1})
    # Strict curvature sign at a full-rank point: sum_i det(V,A_i)^2.
    curvature = -1 if mutation=='curvature_sign' else 1
    positive_cases=0
    for a,b,c,d in product([F(-1),F(0),F(1)],repeat=4):
        if a*d-b*c==0: continue
        for vx,vy in product([F(-1),F(0),F(1)],repeat=2):
            if vx==vy==0: continue
            gram=(vx*vx+vy*vy)*(a*a+b*b+c*c+d*d)-(vx*a+vy*c)**2-(vx*b+vy*d)**2
            wedges=(vx*c-vy*a)**2+(vx*d-vy*b)**2
            if gram!=wedges or curvature*gram<=0: raise ValueError('negative_curvature_strict_rank_two_term')
            positive_cases+=1
    check('negative_curvature_strict_rank_two_term',positive_cases>0,{'nondegenerate_rational_cases':positive_cases})
    # Basis [1,sin(2r),cos(2r)] and the exact differentiation matrix; this does
    # not use the candidate's polynomial differentiation implementation.
    D=((0,0,0),(0,0,-2),(0,2,0))
    mat=lambda z:tuple(sum(F(D[i][j])*z[j] for j in range(3)) for i in range(3))
    amp=F(1,4) if mutation=='cusp_amplitude' else F(2)
    bump=(amp/2,F(0),-amp/2)
    qp=tuple(a+b for a,b in zip((F(1),F(0),F(0)),mat(bump)))
    qpp=mat(mat(bump))
    low,high=qp[0]-abs(qp[1]),qp[0]+abs(qp[1])
    check('cusp_remote_folds_and_upper_derivative',low==-1 and high==3,{'min_qprime':str(low),'max_qprime':str(high)})
    check('cusp_seam_exact_regularities',sum((bump[0],bump[2]))==0 and qp[0]+qp[2]==1 and qpp[0]+qpp[2]==4,{'bump_at_seam':'0','first_derivative':'1','right_second_derivative':'4','left_second_derivative':'0'})
    check('cusp_energy_majorant',1+max(low*low,high*high)==10,{'density_bound':'10/y^2','tail_bound':'10*w/Y'})
    at_quarter=1 if mutation=='cusp_harmonicity' else qp[0]+qp[1]
    residual_numerator=1-at_quarter**2
    check('cusp_is_not_harmonic',qpp[0]+qpp[1]==0 and residual_numerator==-8,{'q_times_residual_at_r_pi_over_4':str(residual_numerator)})
    # On a collapsed source interval, target-pulled tests see only the zero
    # total mass of B(s)=2s-1. The domain test s(1-s)(2s-1) has a nonzero pairing.
    # Product B*test = -4s^4+8s^3-5s^2+s, integrated exactly on [0,1].
    mass=F(2,2)-1
    pairing=-F(4,5)+F(8,4)-F(5,3)+F(1,2)
    if mutation=='collapsed_trace_injectivity': pairing=F(0)
    check('collapsed_trace_tests_have_nontrivial_kernel',mass==0 and pairing==F(1,30),{'total_flux':str(mass),'domain_pairing':str(pairing)})
    # The two vertical sides of the standard ideal triangle can be identified.
    # i and 1+i then have the same quotient-edge value, but their hyperbolic
    # midpoint has x=1/2 and y^2=5/4, strictly inside that triangle.
    midpoint_x, midpoint_y2 = F(1,2), F(5,4)
    side_preserved = midpoint_x in (0,1)
    if mutation=='quotient_trace_equals_side_incidence': side_preserved=True
    check('quotient_trace_is_not_side_incidence',not side_preserved and midpoint_y2>F(1,4),{'midpoint_x':str(midpoint_x),'midpoint_y_squared':str(midpoint_y2),'bottom_boundary_y_squared_at_midpoint':'1/4','scope':'local geometric obstruction only'})
    # Pure logical control: l.s.c. permits E(limit)=0, liminf E(sequence)=1.
    # It cannot by itself imply energy recovery. This is not a map construction.
    E_limit,E_sequence=F(0),F(1)
    if mutation=='weak_lower_semicontinuity_direction': E_limit,E_sequence=E_sequence,E_limit
    check('lower_semicontinuity_is_only_one_sided',E_limit<E_sequence,{'limit_energy':str(E_limit),'sequence_energy':str(E_sequence),'scope':'numerical inequality witness only'})
    return {'status':'pass','uid':os.getuid(),'optimization_level':sys.flags.optimize,'checks':checks,'check_count':len(checks),'scope':'finite exact identities and logical witnesses, not analytic theorem certification'}


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--mutation',choices=MUTATIONS); a=p.parse_args()
    try: output=run(a.mutation)
    except (ValueError,ArithmeticError,TypeError) as ex:
        print(json.dumps({'status':'fail','mutation':a.mutation,'failed_check':str(ex),'uid':os.getuid(),'optimization_level':sys.flags.optimize},sort_keys=True)); return 1
    output['mutation']=a.mutation
    print(json.dumps(output,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
