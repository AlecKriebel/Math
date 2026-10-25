#!/usr/bin/env python3
"""Independent exact radial-integral and failed-inference controls.

No imports from the submitted tests, no PDE discretization and no aperture
claim. The H^2 compact bump below is an alternative valid Weyl test; it need
not be C-infinity because its first two derivatives match zero at its edge.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json

def need(b,s):
    if not b:raise RuntimeError(s)
def mul(a,b):
    z=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return z
def deriv(a):return [F(i)*a[i] for i in range(1,len(a))]
def at(a,x):return sum(v*x**i for i,v in enumerate(a))
def integrate(a,power=0,lo=F(0),hi=F(1)):
    return sum(F(v,i+power+1)*(hi**(i+power+1)-lo**(i+power+1)) for i,v in enumerate(a))

def main():
    result={};count=0
    theta=list(map(F,[0,0,3,-2]))
    need(at(theta,0)==0 and at(theta,1)==1 and at(deriv(theta),0)==at(deriv(theta),1)==0,'cutoff boundary jets')
    energy=integrate(mul(deriv(theta),deriv(theta)))
    need(energy==F(6,5),'one-dimensional cutoff integral')
    # This C1 piecewise cutoff suffices for H1-capacity; smooth approximations
    # preserve its limiting estimate. The manuscript uses a smooth theta.
    result['logarithmic_cutoff']={'theta':'3s^2-2s^3 on [0,1], constant outside','integral_theta_prime_squared':str(energy),'two_dimensional_energy':'12*pi/(5*log(1/r))','at_r_exp_minus_N_energy_over_pi':[str(F(12,5*n)) for n in (1,2,4,8,16,32)]}
    # theta(rho-1)= -2rho^3+9rho^2-12rho+5 on [1,2].
    annulus=list(map(F,[5,-12,9,-2]));annulus_grad=mul(deriv(annulus),deriv(annulus))
    radial=[]
    for d in range(1,11):
        constant=integrate(annulus_grad,d-1,F(1),F(2))
        need(constant>0,'positive annular energy')
        ratios=[F(1,2**k)**(d-2) for k in (1,2,4,8)]
        if d>=3:need(all(x>y for x,y in zip(ratios,ratios[1:])),'vanishing higher-dimensional energy')
        elif d==2:need(len(set(ratios))==1,'linear cutoff fails in d2')
        else:need(all(x<y for x,y in zip(ratios,ratios[1:])),'point energy grows in d1')
        radial.append(dict(dimension=d,energy_over_sphere_area=f'{constant} * r^{d-2}',scale_ratios=list(map(str,ratios))))
        count+=1
    result['linear_scale_cutoffs']=radial
    # chi(rho)=(1-rho^2)^3_+. Its value and first two derivatives vanish at 1.
    chi=list(map(F,[1,0,-3,0,3,0,-1]));grad=deriv(chi)
    need(at(chi,1)==at(grad,1)==at(deriv(grad),1)==0,'compact H2 bump boundary jets')
    constants=[]
    for d in range(2,11):
        lap=[F(-6*d),0,F(12*d+24),0,F(-6*d-24)]
        direct=deriv(grad)
        for i,v in enumerate(grad[1:]):direct[i]+=F(d-1)*v
        need(direct==lap,'radial Laplacian expression')
        norm=integrate(mul(chi,chi),d-1)
        g=integrate(mul(grad,grad),d-1)/norm
        l=integrate(mul(lap,lap),d-1)/norm
        for lam in (F(0),F(1,3),F(7),F(100)):
            values=[l/F(2**k)**4+F(4)*lam*g/(d*F(2**k)**2) for k in range(1,31)]
            need(all(x>y>0 for x,y in zip(values,values[1:])),'exact Weyl residual decay')
            # Real Laplacian part and imaginary plane-wave gradient part have
            # zero cross term; radial symmetry contributes the factor 1/d.
            for k,value in enumerate(values,1):
                need(value==l*F(1,2**(4*k))+4*lam*g*F(1,d*2**(2*k)),'Weyl scale identity')
                count+=1
        constants.append(dict(dimension=d,gradient_norm_squared=str(g),laplacian_norm_squared=str(l),residual_squared='L/R^4 + 4*lambda*G/(d*R^2)'))
    result['normalized_radial_Weyl_tests']=constants
    # Failed shortcut: finite-rank compressions P_n M_(1+x) P_n converge
    # strongly to an absolutely continuous multiplication operator on L2[0,1].
    # The normalized first dyadic-cell vectors at consecutive levels have
    # squared inner product 1/2, so their rank-one projectors never get close.
    controls=[]
    for n in range(1,65):
        h=F(1,2**n);small=h/2
        overlap_squared=small*small/(h*small)
        norm_difference_squared=1-overlap_squared
        need(norm_difference_squared==F(1,2),'unprotected eigenvectors not Cauchy')
        variance=integrate([F(1,4)*h*h,-h,F(1)],0,0,h)/h
        need(variance==h*h/12>0,'compressed cell does not reduce the limiting multiplication operator')
        controls.append(dict(level=n,cell_width=str(h),rank_one_projection_step_norm_squared=str(norm_difference_squared),limit_commutator_on_cell_norm_squared=str(variance)))
        count+=2
    result['strong_limit_countercontrol']={'operator':'M_(1+x) on L2[0,1], purely absolutely continuous','finite_approximants':'P_n M_(1+x) P_n, P_n dyadic conditional-expectation projection; finite rank, extended by zero','failure':'No fixed-rank eigenprojection trajectory has the required summable small motion; dense approximate eigenvalues and strong convergence do not establish pure point type.','exact_rows':controls}
    # If the limiting positive operator is not injective, a protected fixed
    # direction may have eigenvalue zero and cannot be inverted to an A-eigenvector.
    result['injectivity_countercontrol']={'operators':'R_n=diag(1/n,1), P=diag(1,0), R=diag(0,1)','identities':'P commutes at every stage and has a fixed rank-one limit; restriction of R to Ran P has eigenvalue zero.','purpose':'Demonstrates why the actual Dirichlet resolvent must be injective in the proof.'}
    result['status']='PASS';result['counted_exact_conditions']=count
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['limits']='No verification of a chosen domain, no numerical admissible apertures, no finite-test proof of the infinite-dimensional theorem. Exact constants and logical negative controls only.'
    Path(__file__).with_name('fresh_exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'counted_exact_conditions':count,'radial_dimensions':len(constants),'projection_negative_controls':len(controls),'source_sha256':result['source_sha256']},indent=2))

if __name__=='__main__':main()
