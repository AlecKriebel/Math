"""Validated positive-radius Green gaps; global fourth-derivative-measure bound."""
import json,time,argparse
from fractions import Fraction
from pathlib import Path
from mpmath import iv
from certify_entropy_quadrature import rational,conj,enclosure
iv.dps=45
OUT=Path(__file__).parent

def bounds(L,rho,N):
    r2=rho*rho
    G1=(iv.log(1/r2)+r2-1)/2
    G2=1/(8*r2);G3=1/(2*r2*r2);G4=2/(r2*r2*r2)
    S1=2*L;S2=2*L*L+2*L;S3=6*L*L+2*L;S4=14*L*L+2*L
    M=G4*S1**4+6*G3*S1*S1*S2+3*G2*S2*S2+4*G2*S1*S3+G1*S4
    J=G3*S1**3
    TV=2*iv.pi*M+4*J
    error=iv.pi**3*TV/(90*N**4)
    return M,J,TV,error

def green(s,r2):
    u=s/r2;u=iv.mpf([max(1,u.a),max(1,u.b)])
    return r2*((u+1)*iv.log(u)/2+1-u)

def certify(case,N):
    c=Fraction(case['c']);a=list(map(Fraction,case['a']));b=list(map(Fraction,case['b']));s=case['signs'];R=c+sum(a)+sum(b)
    cn=rational(str(c/R));an=list(map(lambda v:rational(str(v/R)),a));bn=list(map(lambda v:rational(str(v/R)),b))
    rho=rational(case['rho_over_support']);r2=rho*rho
    assert rho.a>0 and rho.b<1
    eps=iv.mpf(0);bs=[]
    for j in range(2):
        M,J,TV,e=bounds(an[j]+bn[j],rho,N);eps+=2*e
        bs.append({'M4':enclosure(M),'jump_bound':enclosure(J),'fourth_derivative_total_variation_bound':enclosure(TV)})
    zs=[]
    for k in range(N):
        t=2*iv.pi*(iv.mpf(k)+rational('1/2'))/N
        zs.append(iv.mpc(iv.cos(t),iv.sin(t)))
    increments_p=[[an[j]*z+bn[j]*conj(z) for z in zs] for j in range(2)]
    increments_m=[[an[j]*z+s[j]*bn[j]*conj(z) for z in zs] for j in range(2)]
    acc=iv.mpf(0)
    # Conjugation symmetry makes half the first-angle midpoint rows sufficient.
    assert N%2==0
    for k in range(N//2):
        for l in range(N):
            up=cn+increments_p[0][k]+increments_p[1][l]
            vm=cn+increments_m[0][k]+increments_m[1][l]
            acc+=green(up.real*up.real+up.imag*up.imag,r2)-green(vm.real*vm.real+vm.imag*vm.imag,r2)
    quadrature=2*acc/(N*N)
    result=quadrature+iv.mpf([-eps.b,eps.b])
    return {'case':case,'support_bound_without_noise':str(R),'N_each_angle':N,'interval_dps':iv.dps,'coordinate_derivative_bounds':bs,'midpoint_gap':enclosure(quadrature),'error_bound':enclosure(eps),'normalized_green_gap':enclosure(result),'unnormalized_green_gap':enclosure(result*rational(str(R*R))),'positive_certified':bool(result.a>0),'negative_certified':bool(result.b<0)}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--N',type=int,default=128);parser.add_argument('--output',default='green_rational_certificate.json');args=parser.parse_args()
    case={'name':'rational_near_noisy_optimizer','c':'39/200','a':['1','99/100'],'b':['197/200','19503/20000'],'signs':[-1,1],'rho_over_support':'17/20'}
    t=time.time();res=certify(case,args.N);res['seconds']=time.time()-t
    (OUT/args.output).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res),flush=True)
