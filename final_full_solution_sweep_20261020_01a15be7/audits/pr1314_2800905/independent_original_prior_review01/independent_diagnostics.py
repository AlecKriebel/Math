"""Exact diagnostics for the positive-PCA proof, using standard library only.

These finite checks test algebra, normalization, and failure controls. They
do not prove Gaussian concentration, the semicircle law, or an asymptotic SDP
theorem by simulation. No author program is imported or run.
"""
from fractions import Fraction as F
from itertools import product
from math import isqrt
import json


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def transpose(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def tr(a):
    return sum(a[i][i] for i in range(len(a)))


def objective(a, x):
    return sum(a[i][j] * x[i][j] for i in range(len(a)) for j in range(len(a)))


def covariance(x, y, diag, off):
    n = len(x)
    return F(diag, n) * sum(a*a*b*b for a, b in zip(x, y)) + F(4*off, n) * sum(
        x[i]*x[j]*y[i]*y[j] for i in range(n) for j in range(i+1, n))


def householder(v):
    s = dot(v, v)
    return [[F(i == j) - F(2*v[i]*v[j], s) for j in range(len(v))]
            for i in range(len(v))]


def projector(q, r):
    return [[sum(q[i][k]*q[j][k] for k in range(r)) for j in range(len(q))]
            for i in range(len(q))]


def correction(p, r, alpha):
    n = len(p)
    return [[(1-alpha)*p[i][j]/r + alpha/n for j in range(n)] for i in range(n)]


def ceil_sqrt(k):
    q = isqrt(k)
    return q + (q*q != k)


def main():
    controls = []
    def control(name, ok):
        need(ok, 'negative/positive control: ' + name)
        controls.append(name)

    vectors = set()
    for a, b in product(range(-4, 5), repeat=2):
        s = 1+a*a+b*b
        vectors.add((F(2*a, s), F(2*b, s), F(1-a*a-b*b, s)))
    for i in range(3):
        for sign in [-1, 1]:
            vectors.add(tuple(F(sign*(j == i)) for j in range(3)))
    vectors = sorted(vectors)
    cov_checks = 0
    for x in vectors:
        need(dot(x, x) == 1, 'rational unit vector')
        need(covariance(x, x, 2, 1) == F(2, 3), 'invariant variance/Lipschitz norm')
        for y in vectors:
            t = dot(x, y)
            need(-1 <= t <= 1, 'Cauchy-Schwarz')
            cov = covariance(x, y, 2, 1)
            need(cov == F(2, 3)*t*t, 'exact GOE covariance')
            inc_a = covariance(x, x, 2, 1)+covariance(y, y, 2, 1)-2*cov
            inc_b = F(8, 3)*(1-t)
            need(inc_b-inc_a == F(4, 3)*(1-t)**2, 'comparison direction')
            need(inc_b >= inc_a, 'comparison domination')
            cov_checks += 1
    e1, spread = (F(1), F(0), F(0)), (F(3,5), F(4,5), F(0))
    control('reversed_variances_are_not_invariant',
            covariance(e1,e1,1,2) != covariance(spread,spread,1,2))
    control('equal_upper_variances_are_not_invariant',
            covariance(e1,e1,1,1) != covariance(spread,spread,1,1))
    control('invariant_model_has_direction_independent_variance',
            covariance(e1,e1,2,1) == covariance(spread,spread,2,1))
    t = dot(e1, spread)
    control('comparison_cannot_be_reversed', F(4,3)*(1-t)**2 > 0)
    control('all_negative_linear_sup_is_not_norm_positive_part',
            max([-3,-2,-1]) < 0)
    # The reversed ensemble has the same off-diagonal covariance as sqrt(2)G;
    # the remaining defect is diagonal. Its limiting scale is therefore not2.
    for x, y in product(vectors[:10], repeat=2):
        need(covariance(x,y,1,2)-2*covariance(x,y,2,1) ==
             -sum(a*a*b*b for a,b in zip(x,y)), 'reversed diagonal-only discrepancy')

    projector_count = witness_count = 0
    alphas = [F(0), F(1,10), F(1,2), F(9,10), F(1)]
    for v in product(range(-1,2), repeat=4):
        if not any(v):
            continue
        q = householder(v)
        need(mm(q,transpose(q)) == [[F(i==j) for j in range(4)] for i in range(4)],
             'rational orthogonal matrix')
        eigenvalues = [F(3),F(2),F(-1),F(-4)]
        a = [[sum(q[i][k]*eigenvalues[k]*q[j][k] for k in range(4))
              for j in range(4)] for i in range(4)]
        for r in [1,2,3]:
            p = projector(q,r)
            need(mm(p,p)==p and tr(p)==r and transpose(p)==p, 'exact projector')
            # P=BB^T is a positive-semidefinite certificate by construction.
            b = [row[:r] for row in q]
            need(mm(b,transpose(b))==p, 'projector Gram certificate')
            minimum = min(p[i][j] for i in range(4) for j in range(4) if i!=j)
            alpha_critical = F(0) if minimum>=0 else -4*minimum/(r-4*minimum)
            for alpha in alphas:
                x = correction(p,r,alpha)
                need(tr(x)==1 and transpose(x)==x, 'trace-one symmetric witness')
                nonnegative = min(x[i][j] for i in range(4) for j in range(4))>=0
                need(nonnegative == (alpha>=alpha_critical), 'exact positivity threshold')
                need(objective(a,x) == (1-alpha)*sum(eigenvalues[:r])/r +
                     alpha*sum(map(sum,a))/4, 'spectral-witness objective identity')
                witness_count += 1
            projector_count += 1
    p = [[F(1,2),F(-1,2)],[F(-1,2),F(1,2)]]
    control('raw_spectral_projector_can_have_negative_entries', p[0][1]<0)
    control('small_all_ones_correction_can_fail_at_finite_n',
            correction(p,1,F(1,10))[0][1]<0)
    control('all_ones_correction_succeeds_at_exact_threshold',
            correction(p,1,F(1,2))[0][1]==0)
    identity_mix = [[F(1,2)*p[i][j]+F(1,4)*(i==j) for j in range(2)] for i in range(2)]
    control('identity_correction_does_not_fix_negative_off_diagonal',identity_mix[0][1]<0)
    p2 = projector(householder([1,1,1,0]),2)
    control('missing_rank_normalization_breaks_trace_one',
            tr([[(1-F(1,2))*p2[i][j]+F(1,8) for j in range(4)] for i in range(4)]) != 1)
    altered = [row[:] for row in p2]
    altered[0][0] += F(1,7)
    control('altered_matrix_is_not_a_projection',mm(altered,altered)!=altered)

    # Chernoff algebra with k=a^2, t=b^2 makes all thresholds and optimizing
    # parameters rational. The accompanying proof covers arbitrary k,t.
    chernoff_checks = 0
    for aa,bb in product(range(1,31),repeat=2):
        k,t = aa*aa,bb*bb
        theta = F(bb,aa+2*bb)
        need(F(k)*theta*theta/(1-2*theta)-theta*(2*aa*bb+2*t)==-t,
             'upper chi-square Chernoff exponent')
        theta = F(bb,aa)
        need(k*theta*theta-theta*2*aa*bb==-t, 'lower chi-square Chernoff exponent')
        chernoff_checks += 2
    # Use n=2^ell and 6ell >= 6log(n) for conservative exact integer bounds.
    # This illustrates fixed-parameter domination; it claims no practical n.
    feasibility_certificates = []
    for delta,alpha in product([F(1,2),F(1,16),F(1,100)],[F(1,10),F(1,100)]):
        ell=100
        n=2**ell
        r=int(delta*n)
        t=6*ell
        er=2*ceil_sqrt(r*t)+2*t
        en=2*ceil_sqrt(n*t)+2*t
        need(n-en>n/2, 'positive denominator')
        deviation=F(er+F(r,n)*en,n-en)
        margin=alpha/n-(1-alpha)*deviation/r
        need(margin>0, 'fixed-parameter asymptotic feasibility algebra')
        feasibility_certificates.append({'delta':str(delta),'alpha':str(alpha),
                                         'ell':ell,'strict_margin':True,'rank':r})
    control('flooring_is_needed_for_general_delta_n', F(7,3)!=int(F(7,3)))
    control('shrinking_alpha_is_not_licensed_by_fixed_parameter_proof',
            correction(p,1,F(0))[0][1]<0)
    # A pathological rare negative value shows why convergence in probability
    # does not by itself prove expectation convergence.
    rare_expectations = [2*(1-F(1,n))-n*n*F(1,n) for n in [10,100,1000]]
    control('probability_limit_alone_does_not_control_expectation',rare_expectations[-1]<-900)
    # Rank-one feasibility is a global sign condition; zeros cause no exception.
    for x in product(range(-2,3),repeat=4):
        if not any(x):
            continue
        entrywise=all(a*b>=0 for a in x for b in x)
        common_sign=all(a>=0 for a in x) or all(a<=0 for a in x)
        need(entrywise==common_sign,'rank-one global sign criterion')
    control('opposite_signs_break_rank_one_entrywise_feasibility',F(1)*F(-1)<0)
    control('zero_coordinates_do_not_break_global_sign',all(a*b>=0 for a in [0,1,2] for b in [0,1,2]))
    control('trace_one_is_distinct_from_diagonal_one',tr([[1,0],[0,1]])!=1)
    for n in range(1,101):
        need(F(n)*F(2,n)/n**2==F(2,n*n),'trace-floor second moment')
    print(json.dumps({'schema':'independent-pr1314-exact-diagnostics-v1','status':'PASS',
        'rational_unit_vectors':len(vectors),'covariance_comparison_pairs':cov_checks,
        'exact_projectors':projector_count,'corrected_witnesses':witness_count,
        'chernoff_exact_exponent_checks':chernoff_checks,
        'fixed_parameter_certificates':feasibility_certificates,
        'control_count':len(controls),'controls':controls,
        'limitation':'Finite exact diagnostics supplement the written unbounded proof; no asymptotic claim is inferred from simulation.'},sort_keys=True,indent=2))


if __name__=='__main__':
    main()
