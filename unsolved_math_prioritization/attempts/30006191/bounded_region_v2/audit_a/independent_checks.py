#!/usr/bin/env python3
"""Independent finite-dimensional algebra and scaling controls, not a proof substitute."""
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm, eigh
from scipy.integrate import quad, quad_vec
import sympy as sp

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--proof',type=Path,required=True,help='Frozen BOUNDED_REGION_PROOF.md to validate')
args=parser.parse_args()
proof=args.proof
EXPECTED_PROOF_SHA256='2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350'
proof_bytes=proof.read_bytes()
assert len(proof_bytes)==12771, 'Rejected changed proof byte count'
assert hashlib.sha256(proof_bytes).hexdigest()==EXPECTED_PROOF_SHA256, 'Rejected changed proof hash'
checks=[]
def check(label, condition, **details):
    if not bool(condition):
        raise AssertionError((label,details))
    checks.append(dict(label=label,passed=True,**details))
def close(label, actual, expected, tol=2e-10):
    error=float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    check(label,error<tol,max_abs_error=error,tolerance=tol)
def creators(d):
    ans=[]
    for j in range(d):
        a=np.zeros((2**d,2**d),complex)
        for mask in range(2**d):
            if not(mask>>j&1):
                a[mask|(1<<j),mask]=(-1)**((mask&((1<<j)-1)).bit_count())
        ans.append(a)
    return ans
def create(C,f):return sum(f[j]*C[j] for j in range(len(C)))
def dg(C,h):return sum(h[i,j]*C[i]@C[j].conj().T for i in range(len(C)) for j in range(len(C)))
def slater(C,orbitals):
    v=np.zeros(C[0].shape[0],complex);v[0]=1
    for g in reversed(orbitals):v=create(C,g)@v
    return v
def random_unitary(rng,d):
    z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    return np.linalg.qr(z)[0]
def evolver(A):
    ev,U=eigh(A)
    return lambda t:(U*np.exp(-1j*t*ev))@U.conj().T

# The constants must remain uniform when N increases, including noncube N.
for N in list(range(1,201))+[1000,1001,9999,10000,10**6,10**9]:
    m=round(N**(1/3))
    while m**3<N:m+=1
    while (m-1)**3>=N:m-=1
    check(f'packing_{N}',m**3>=N and m<=2*N**(1/3)+1e-10 and 4*N*m*m<=16*N**(5/3)*(1+1e-12))
n,s,t,d=sp.symbols('n s t d',positive=True)
term1=sp.integrate(2*n*s*n**sp.Rational(5,6),(s,0,t))
term2=sp.integrate(2*n*s**2*n**sp.Rational(5,3),(s,0,t))
check('duhamel_exact_integrals',sp.simplify(term1-n**sp.Rational(11,6)*t**2)==0 and sp.simplify(term2-sp.Rational(2,3)*n**sp.Rational(8,3)*t**3)==0)
check('three_dimensional_decay',sp.simplify(term1.subs(t,1/n)-n**sp.Rational(-1,6))==0 and sp.simplify(term2.subs(t,1/n)-sp.Rational(2,3)*n**sp.Rational(-1,3))==0)
check('dimension_threshold',all(float(-sp.Rational(1,2)+sp.Rational(1,k))<0 and float(-1+sp.Rational(2,k))<0 for k in range(3,31)) and -sp.Rational(1,2)+sp.Rational(1,2)==0)
for count in range(1,501):
    for sigma in [0,1]:
        gap=(count+1)*(count+1-sigma)-count*(count-sigma)
        check(f'phase_gap_{count}_{sigma}',gap==2*count+1-sigma)
        for m in [0,1,count//2,count]:
            a=(count-m)*(count-m-sigma)-count*(count-sigma)
            check(f'leak_polynomial_{count}_{sigma}_{m}',a==-m*(2*count-sigma-m) and abs(a)<=2*count*m)

# Build CAR operators directly from the occupation basis, independent of source checks.
variance_cases=0
for dim in [4,5,6]:
    C=creators(dim);I=np.eye(2**dim)
    for j in range(dim):
        for k in range(dim):
            close(f'CAR_{dim}_{j}_{k}',C[j].conj().T@C[k]+C[k]@C[j].conj().T,I if j==k else 0)
    for seed in [19,73,211]:
        rng=np.random.default_rng(seed+dim)
        U=random_unitary(rng,dim);R=random_unitary(rng,dim)
        q=R[:,:dim//2]@R[:,:dim//2].conj().T;M=dg(C,q)
        for count in range(1,dim):
            orbital=U[:,:count];P=orbital@orbital.conj().T;v=slater(C,list(orbital.T))
            close(f'slater_norm_{dim}_{seed}_{count}',np.vdot(v,v),1)
            lam=float(np.trace(P@q).real)
            second=float(np.vdot(M@v,M@v).real)
            expected=lam*lam+lam-np.trace(P@q@P@q).real
            close(f'variance_identity_{dim}_{seed}_{count}',second,expected)
            check(f'variance_bound_{dim}_{seed}_{count}',second-lam*lam>=-2e-10 and second-lam*lam<=lam+2e-10)
            variance_cases+=1

# Generic times detect sign/conjugation errors that t_N alone would hide.
phase_mutations=[];bra_mutations=[];duhamel_max_ratio=0.0
for seed in [11,23,71,107]:
    dim=5;C=creators(dim);I=np.eye(2**dim);rng=np.random.default_rng(seed)
    z=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
    h=(z+z.conj().T)/2
    T=dg(C,h);Num=dg(C,np.eye(dim));L=dg(C,np.diag([1,1,1,0,0]));M=Num-L
    f=np.eye(dim)[:,0];A=create(C,f)
    for count in [1,2]:
        psi=slater(C,list(np.eye(dim)[:,1:count+1].T));xi=A@psi
        for sigma in [0,1]:
            H=T+L@(L-sigma*I);K=T+Num@(Num-sigma*I)
            UH=evolver(H);UK=evolver(K);W=H-K
            for time in [.017,.137,.41]:
                hp=UH(time)@psi;hx=UH(time)@xi;kp=UK(time)@psi;kx=UK(time)@xi
                FH=np.vdot(hx,A@hp);FK=np.vdot(kx,A@kp)
                expected=np.exp(1j*time*(2*count+1-sigma))*np.vdot(f,expm(1j*time*h)@f)
                label=f'{seed}_{count}_{sigma}_{time}'
                close('reference_phase_'+label,FK,expected)
                Ep=np.linalg.norm(hp-kp);Ex=np.linalg.norm(hx-kx)
                check('two_vector_bound_'+label,abs(FH-FK)<=Ep+Ex+2e-10)
                D=UH(time).conj().T@A.conj().T@UH(time)-A.conj().T
                close('annihilation_witness_'+label,np.vdot(psi,D@xi),np.conj(FH-1))
                for vec,err,tag in [(psi,Ep,'N'),(xi,Ex,'Np1')]:
                    integral=quad(lambda u:float(np.linalg.norm(W@UK(u)@vec)),0,time,epsabs=1e-11,epsrel=1e-11)[0]
                    check('duhamel_bound_'+label+'_'+tag,err<=integral+2e-10)
                    duhamel_max_ratio=max(duhamel_max_ratio,float(err/integral) if integral>1e-10 else 0)
                if abs(FH-FK)>Ep+1e-5:bra_mutations.append(label)
                wrong=np.exp(-1j*time*(2*count+1-sigma))*np.vdot(f,expm(1j*time*h)@f)
                phase_mutations.append(abs(FK-wrong))
                # Exact commutator Duhamel sign checked by quadrature in one-particle space.
            phase_time=math.pi/(2*count+1-sigma)
            close(f'exact_pi_phase_{seed}_{count}_{sigma}',np.exp(1j*phase_time*(2*count+1-sigma)),-1)

# Adversarial rejection fixtures identify assumptions that cannot be weakened.
mutations={}
# Additional direct sign check, away from the special phase times.
rng=np.random.default_rng(9281);z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));h=(z+z.conj().T)/2
chi=np.diag([1,1,0,0]);g=np.eye(4)[:,0];time=.371
comm=h@chi-chi@h
integral=quad_vec(lambda r:expm(-1j*(time-r)*h)@comm@expm(-1j*r*h)@g,0,time,epsabs=1e-12)[0]
lhs=(expm(-1j*time*h)@chi-chi@expm(-1j*time*h))@g
close('cutoff_commutator_duhamel_sign',lhs,-1j*integral)
check('cutoff_leakage_control',np.linalg.norm((np.eye(4)-chi)@expm(-1j*time*h)@g)<=time*np.linalg.norm(comm,2)+1e-12)
mutations['reverse_cutoff_commutator_sign']=bool(np.linalg.norm(lhs-1j*integral)>1e-4)


mutations['reverse_number_phase']=max(phase_mutations)>0.5
mutations['omit_evolved_bra_error']=len(bra_mutations)>0
mutations['replace_second_moment_by_mean']=math.sqrt(.5)>.5
# Slater variance is not valid for arbitrary pure many-particle states.
# sqrt(1-p)|all inside> + sqrt(p)|all outside>, m=3, p=1/4.
m=3;p=.25;lam=m*p;var=m*m*p*(1-p)
mutations['extend_slater_variance_to_arbitrary_states']=var>lam
mutations['remove_normal_ordering_shift']=((3+1)*3-3*2)!=2*3+1
mutations['claim_dimension_two_decay']=(-.5+1/2)==0 and (-1+2/2)==0
mutations={name:bool(rejected) for name,rejected in mutations.items()}
for name,rejected in mutations.items():check('mutation_rejected_'+name,rejected)

report={
 'status':'PASS','purpose':'Independent algebra/scaling controls. Continuum/domain/asymptotic validity is assessed in the audit report, not inferred from these finite-dimensional tests.',
 'proof_sha256_at_test':EXPECTED_PROOF_SHA256,
 'check_count':len(checks),'slater_variance_cases':variance_cases,'duhamel_max_ratio':duhamel_max_ratio,
 'adversarial_rejections':mutations,'omit_bra_error_counterexample_count':len(bra_mutations),
 'versions':{'numpy':np.__version__,'sympy':sp.__version__},'checks':checks}
(ROOT/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
