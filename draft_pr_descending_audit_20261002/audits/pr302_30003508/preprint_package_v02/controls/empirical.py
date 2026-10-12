"""Independent finite controls, not a numerical substitute for the analytic proof."""
from fractions import Fraction as Q
import itertools
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
assert sys.flags.optimize == 0
checks=[]

def check(label, assertion):
    if not assertion:
        raise AssertionError(label)
    checks.append(label)

def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matpow(a,n):
    result=[[Q(int(i==j)) for j in range(len(a))] for i in range(len(a))]
    for _ in range(n): result=matmul(result,a)
    return result

models=[]
for pi in ([Q(1,2),Q(1,2)],[Q(1,3),Q(2,3)]):
    for rho in [Q(0),Q(1,2),Q(99,100),Q(999,1000)]:
        p=[[rho*int(i==j)+(1-rho)*pi[j] for j in range(2)] for i in range(2)]
        check("stationarity_%s_%s"%(pi[0],rho), all(sum(pi[i]*p[i][j] for i in range(2))==pi[j] for j in range(2)))
        check("reversibility_%s_%s"%(pi[0],rho), all(pi[i]*p[i][j]==pi[j]*p[j][i] for i,j in itertools.product(range(2),repeat=2)))
        maximum_ratio=Q(0)
        for fi,values in enumerate(itertools.product([-1,1],repeat=4)):
            f=[[Q(values[2*i+j]) for j in range(2)] for i in range(2)]
            mean=sum(pi[i]*p[i][j]*f[i][j] for i,j in itertools.product(range(2),repeat=2))
            z=[[f[i][j]-mean for j in range(2)] for i in range(2)]
            var=sum(pi[i]*p[i][j]*z[i][j]**2 for i,j in itertools.product(range(2),repeat=2))
            r=[sum(pi[i]*p[i][j]*z[i][j] for i in range(2))/pi[j] for j in range(2)]
            s=[sum(p[i][j]*z[i][j] for j in range(2)) for i in range(2)]
            check("endpoint_center_%s_%s_%s"%(pi[0],rho,fi),sum(pi[i]*r[i] for i in range(2))==sum(pi[i]*s[i] for i in range(2))==0)
            check("projection_contraction_%s_%s_%s"%(pi[0],rho,fi),sum(pi[i]*r[i]**2 for i in range(2))<=var and sum(pi[i]*s[i]**2 for i in range(2))<=var)
            covs=[]
            for lag in range(1,9):
                pp=matpow(p,lag-1)
                endpoint=sum(pi[b]*r[b]*pp[b][c]*s[c] for b,c in itertools.product(range(2),repeat=2))
                direct=sum(pi[a]*p[a][b]*pp[b][c]*p[c][d]*z[a][b]*z[c][d] for a,b,c,d in itertools.product(range(2),repeat=4))
                if lag==1:
                    overlap=sum(pi[a]*p[a][b]*p[b][c]*z[a][b]*z[b][c] for a,b,c in itertools.product(range(2),repeat=3))
                    check("literal_overlap_%s_%s_%s"%(pi[0],rho,fi),overlap==endpoint)
                check("covariance_identity_%s_%s_%s_%s"%(pi[0],rho,fi,lag),endpoint==direct)
                check("covariance_gap_%s_%s_%s_%s"%(pi[0],rho,fi,lag),abs(direct)<=rho**(lag-1)*var)
                covs.append(direct)
            for n in range(1,10):
                empirical_variance=(n*var+2*sum((n-lag)*covs[lag-1] for lag in range(1,n)))/n**2
                check("sample_variance_bound_%s_%s_%s_%s"%(pi[0],rho,fi,n),0<=empirical_variance<=(1+2/(1-rho))/n)
                maximum_ratio=max(maximum_ratio,n*empirical_variance)
        models.append({"stationary_pi":list(map(str,pi)),"rho":str(rho),"all_sign_functions":16,"lags":8,"sample_sizes":9,"max_n_variance_over_sign_functions":str(maximum_ratio)})

# Independent observations STILL give correlated overlapping pairs.
overlap_control=[]
for n in range(1,10):
    true=Q(1,n)-Q(1,2*n*n)
    independent_pairs=Q(1,2*n)
    check("iid_overlap_variance_%d"%n, true==Q(1,2*n)+Q(n-1,2*n*n))
    if n>=2: check("reject_pair_independence_%d"%n,true>independent_pairs)
    overlap_control.append({"n":n,"exact_variance":str(true),"incorrect_pair_independence_variance":str(independent_pairs)})

# Finite reflection can reproduce derivatives through six, not all orders.
alpha=[28,-112,210,-224,140,-48,7]
moments=[sum(Q(a)*(-j)**k for j,a in enumerate(alpha,1)) for k in range(8)]
for k in range(7): check("normal_polynomial_jet_%d"%k,moments[k]==1)
check("finite_extension_not_C_infinity",moments[7]!=1)
for p in range(7):
    for q in range(7-p):
        # Tangential monomials factor unchanged, so mixed jets use normal moment q.
        check("tangential_normal_mixed_jet_%d_%d"%(p,q),moments[q]==1)
for qx,qy in itertools.product(range(3),repeat=2):
    check("two_variable_mixed_jet_%d_%d"%(qx,qy),moments[qx]*moments[qy]==1)
reflection_norm_bound=Q(1)+sum(abs(Q(a,j)) for j,a in enumerate(alpha,1))

def bump(t):
    return math.exp(-1/(1-t*t)) if abs(t)<1 else 0.

# In the flat local collar, at x_d=0,z_d=5h, K_h has negative sign.
# j<=5 terms vanish, so the sign is exactly exp(-49/24)-8 exp(-36/11).
# Negativity follows from 36/11-49/24=325/264 < log(8).
check("negative_boundary_kernel_analytic",Q(325,264)<Q(3,2) and Q(27)<Q(64))
boundary_kernel=bump(-5)+sum(a/j*bump(5/j) for j,a in enumerate(alpha,1))
check("negative_boundary_kernel_numerical",boundary_kernel<0)

# Exponent controls for every d, represented exactly, plus fixed numeric cases.
for d in [2,3,10,100]:
    mesh_exponent=Q(1,4*d)
    check("pair_net_cardinality_exponent_%d"%d,2*d*mesh_exponent==Q(1,2))
    check("one_state_net_cardinality_exponent_%d"%d,d*mesh_exponent==Q(1,4))
    check("chebyshev_power_%d"%d,2*(2*d+4)+2==4*d+10)
    # For A_j=(j+1)^p 2^{-j/2}, ratio eventually <=2^{-1/4}.
    p=4*d+10
    j0=math.ceil(8*p/math.log(2))
    check("summable_tail_%d"%d,p/(j0+1)<=math.log(2)/8)
    # Bound log interpolation error <=(2d+5)log(j+1)-j log(2)/(4d).
    j1=max(j0,10_000*d*d)
    check("interpolation_decay_control_%d"%d,(2*d+5)*math.log(j1+1)-j1*math.log(2)/(4*d)<0)

# Normalization lower bound and identity-interval slack use no sample lower bound.
for c,C,volume in [(Q(1,2),Q(2),Q(1)),(Q(1,10),Q(10),Q(3)),(Q(1),Q(1),Q(1))]:
    check("positivity_normalization_%s_%s_%s"%(c,C,volume),(c/2)/(2*C*volume)==c/(4*C*volume)>0)
    check("identity_interval_slack_%s_%s"%(c,C),c-Q(3,4)*c>0 and Q(3,2)*C-C>0)

out={"status":"PASS","check_count":len(checks),"checks":checks,"chain_models":models,"iid_shared_endpoint_control":overlap_control,"reflection_moments":list(map(str,moments)),"reflection_sup_norm_factor_bound":str(reflection_norm_bound),"signed_kernel_value_at_x0_z5h":boundary_kernel,"scope":"Exact finite Markov and reflection controls, analytic exponent/positivity checks. Universal convergence is audited in REPORT.md; no finite test proves it.","runtime":{"version":sys.version,"optimization":sys.flags.optimize}}
(HERE/"INDEPENDENT_CONTROLS_RESULT.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
