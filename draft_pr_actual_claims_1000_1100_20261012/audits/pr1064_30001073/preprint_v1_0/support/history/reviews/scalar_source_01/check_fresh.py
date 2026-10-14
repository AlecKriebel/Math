"""Fresh reviewer controls; exact rational inputs plus Decimal transcendental diagnostics.

These finite checks supplement, and do not replace, the analytic proof. No historical
omitted computation is imported or claimed replayed. Writes only beside this file.
"""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import datetime
import hashlib
import json
import platform
import subprocess

OUT = Path(__file__).resolve().parent


def dec(x):
    if isinstance(x, F):
        return D(x.numerator) / D(x.denominator)
    return D(x)


def g(b):
    if b == 0:
        return D(0)
    if b == 1:
        return D(1)
    return -b * b * b.ln() / (1 - b)


def h(a):
    return a * a * (1 - a.ln()) if a else D(0)


def d(b, a):
    if b == 0:
        return a
    if a == 0:
        raise ValueError("inadmissible support")
    return b * (b / a).ln() - b + a


def ent(weights):
    return -sum((dec(p) * dec(p).ln() for p in weights if p), D(0))


def scalar_checks(precision):
    with localcontext() as ctx:
        ctx.prec = precision
        e2, e4 = D(2).exp(), D(4).exp()
        tiny = [D(10) ** (-k) for k in [1, 3, 10, 30, 100, 500, 1000]]
        near_one = [1 - D(10) ** (-k) for k in [1, 10, 50, 120]]
        values = sorted(set([D(i) / 40 for i in range(41)] + tiny + near_one))
        count = 0
        max_ratio = D('-Infinity')
        max_pair = None
        branches = {'large': 0, 'small_b_le_a': 0, 'small_a_lt_b': 0, 'zero': 0}
        for a in values:
            bs = values if a else [D(0)]
            if a and a * e2 <= 1:
                bs = sorted(set(bs + [a * e2, a * e2 * (1 - D('1e-100')), a * e2 * (1 + D('1e-100'))]))
            for b in bs:
                if b > 1:
                    continue
                count += 1
                lhs = g(b) - d(b, a)
                rhs = e4 * h(a)
                assert lhs <= rhs, (a, b, lhs, rhs)
                assert g(b) <= b + D(10) ** (-precision + 5)
                assert g(b) <= h(b) + D(10) ** (-precision + 5)
                if not a or not b:
                    branches['zero'] += 1
                elif b >= e2 * a:
                    branches['large'] += 1
                    assert lhs <= 0
                elif b <= a:
                    branches['small_b_le_a'] += 1
                else:
                    branches['small_a_lt_b'] += 1
                if a:
                    ratio = lhs / h(a)
                    if ratio > max_ratio:
                        max_ratio, max_pair = ratio, [str(a), str(b)]
        return {'precision': precision, 'pairs_checked': count, 'branches': branches,
                'max_normalized_lhs': str(max_ratio), 'max_pair': max_pair,
                'claimed_constant': str(e4), 'zero_endpoint': str(g(D(0)) - d(D(0), D(0))),
                'unit_endpoint': str(g(D(1))), 'all_pass': True}


def law_check(name, n, weights):
    total = sum(weights.values(), F(0))
    law = {s: w / total for s, w in weights.items() if w}
    b = [[sum((w for s, w in law.items() if s[i] == j), F(0)) for j in range(n)] for i in range(n)]
    assert all(sum(row, F(0)) == 1 for row in b)
    assert all(sum((b[i][j] for i in range(n)), F(0)) == 1 for j in range(n))
    lhs = ent(law.values())
    rhs = sum((ent(row) for row in b), D(0)) - n + sum((g(dec(x)) for row in b for x in row), D(0))
    slack = rhs - lhs
    assert slack >= -D('1e-200'), (name, slack)
    hist_count = 0
    min_z = F(1)
    for order in permutations(range(n)):
        chain = D(0)
        for step, i in enumerate(order):
            histories = {}
            for s, w in law.items():
                hist = tuple(s[k] for k in order[:step])
                q = histories.setdefault(hist, [F(0) for _ in range(n)])
                q[s[i]] += w
            for hist, masses in histories.items():
                hist_count += 1
                mass = sum(masses, F(0))
                q = [x / mass for x in masses]
                available = set(range(n)) - set(hist)
                z = sum((b[i][j] for j in available), F(0))
                assert z > 0
                min_z = min(min_z, z)
                cross = sum((dec(q[j]) * dec(b[i][j]).ln() for j in range(n) if q[j]), D(0))
                local_slack = dec(z).ln() - ent(q) - cross
                assert local_slack >= -D('1e-200')
                chain += dec(mass) * ent(q)
        assert abs(chain - lhs) <= D('1e-200')
    return {'name': name, 'n': n, 'positive_law_states': len(law), 'positive_histories_checked': hist_count,
            'minimum_exact_available_reference_mass': str(min_z), 'entropy_slack': str(slack)}


def matrix_check(name, rows):
    n = len(rows)
    a = [[F(x) for x in row] for row in rows]
    assert all(sum(row, F(0)) == 1 for row in a)
    weights = {}
    for s in permutations(range(n)):
        w = F(1)
        for i, j in enumerate(s):
            w *= a[i][j]
        weights[s] = w
    per = sum(weights.values(), F(0))
    S = sum((x*x for row in a for x in row), F(0))
    assert S >= 1
    W = sum((h(dec(x)) for row in a for x in row), D(0))
    assert W <= dec(S) * (1 + D(n).ln()) + D('1e-200')
    ans = {'name': name, 'n': n, 'exact_permanent': str(per), 'exact_S': str(S),
           'frobenius_sum_slack': str(dec(S)*(1+D(n).ln())-W)}
    if per:
        entropy = law_check(name + '_Gibbs', n, weights)
        law = {s: w / per for s, w in weights.items() if w}
        b = [[sum((w for s, w in law.items() if s[i] == j), F(0)) for j in range(n)] for i in range(n)]
        cross = sum((dec(b[i][j])*dec(a[i][j]).ln() for i in range(n) for j in range(n) if b[i][j]), D(0))
        assert abs(ent(law.values()) + cross - dec(per).ln()) <= D('1e-200')
        bare = sum((dec(b[i][j])*(dec(b[i][j])/dec(a[i][j])).ln() for i in range(n) for j in range(n) if b[i][j]), D(0))
        scalar = sum((d(dec(b[i][j]), dec(a[i][j])) for i in range(n) for j in range(n)), D(0))
        assert abs(bare - scalar) <= D('1e-200')
        assert dec(per).ln() <= -n + D(4).exp()*W
        ans.update({'entropy': entropy, 'Gibbs_identity_pass': True, 'KL_total_mass_pass': True,
                    'log_permanent_bound_slack': str(-n+D(4).exp()*W-dec(per).ln())})
    else:
        ans['zero_permanent_branch_pass'] = True
    return ans


def main():
    result = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'python_version': platform.python_version(), 'transcendental_engine': 'Python stdlib Decimal; not interval-certified',
              'proof_role': 'Finite diagnostics plus deliberate fault controls; analytic derivation is the proof',
              'historical_omitted_code_replayed': False,
              'scalar': [scalar_checks(224), scalar_checks(384)]}
    with localcontext() as ctx:
        ctx.prec = 256
        laws = [law_check('deterministic_n1', 1, {(0,):F(1)})]
        for n in [2, 3, 4, 5]:
            laws.append(law_check('uniform_permutations_n'+str(n), n, {s:F(1) for s in permutations(range(n))}))
        laws.append(law_check('two_supported_matchings_with_greedy_trap',3,{(0,1,2):F(1),(1,2,0):F(1)}))
        result['arbitrary_law_entropy'] = laws
        result['matrices'] = [
            matrix_check('n1', [[1]]),
            matrix_check('row_stochastic_not_column', [[F(1,3),F(2,3)],[F(1,4),F(3,4)]]),
            matrix_check('support_zero_trap', [[F(1,2),F(1,2),0],[0,F(1,2),F(1,2)],[F(1,2),0,F(1,2)]]),
            matrix_check('non_matching_positive_entries', [[F(1,2),F(1,2),0],[0,0,1],[0,0,1]]),
            matrix_check('irregular_doubly_stochastic', [[F(1,2),F(1,4),F(1,4)],[F(1,3),F(1,3),F(1,3)],[F(1,6),F(5,12),F(5,12)]]),
            matrix_check('zero_permanent', [[1,0],[1,0]])]
        faults = []
        a,b=D('1e-50'),D(1)
        assert g(b) > D(4).exp()*h(a)
        faults.append({'variant':'omit scalar divergence d', 'counterexample':{'a':str(a),'b':str(b)}, 'detected':True})
        assert D(1) > (-D(1)).exp()
        faults.append({'variant':'assert prefactor-free n^C exp(-n) at n=1', 'exact_permanent':'1','false_upper':str((-D(1)).exp()), 'detected':True})
        assert D(0) > -D(1)
        faults.append({'variant':'set g(1)=0 in entropy lemma','deterministic_n1_false_RHS':'-1','actual_H':'0','detected':True})
        trap=[[F(1,2),F(1,2),0],[0,F(1,2),F(1,2)],[F(1,2),0,F(1,2)]]
        assert trap[0][0] > 0 and trap[1][2] > 0 and trap[2][1] == 0
        faults.append({'variant':'greedy marginal sampler asserted well-defined on every sparse history', 'positive_greedy_history':'row0->col0,row1->col2','next_available_mass':'0','detected':True,
                       'submitted_conditional_proof':'only supported Gibbs histories consumed; it passes'})
        n,gamma=1000,D(2)
        t=((gamma-1)/(n-1)).sqrt()
        diagonal=(1-t)/n+t
        assert diagonal > gamma/n
        faults.append({'variant':'replace Frobenius condition by entrywise gamma/n', 'n':n,'gamma':str(gamma),'exact_S_formula':'1+(n-1)t^2=gamma','diagonal':str(diagonal),'entrywise_threshold':str(gamma/n),'detected':True})
        result['fault_controls']=faults
        blocks=[]
        for k in [1,2,3,5]:
            for m in [1,2,10,100,1000]:
                n=k*m
                log_per=k*(sum((D(j).ln() for j in range(1,m+1)),D(0))-m*D(m).ln())
                blocks.append({'k':k,'m':m,'n':n,'exact_S':k,'log_per_plus_n':str(log_per+n),'predicted_growth_power':str(D(k)/2),
                               'pure_power_upper_n_at_least_two_pass': None if n==1 else bool(log_per<=3*D(4).exp()*k*D(n).ln()-n)})
        result['block_family_diagnostics']=blocks
    result['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result['all_checks_pass']=True
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT/'FRESH_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_checks_pass':True,'scalar_pairs_each_precision':result['scalar'][0]['pairs_checked'],
                      'arbitrary_laws':len(result['arbitrary_law_entropy']),'matrices':len(result['matrices']),
                      'fault_controls':len(result['fault_controls']),'output':'FRESH_CHECKS.json'},indent=2))


if __name__=='__main__':
    main()
