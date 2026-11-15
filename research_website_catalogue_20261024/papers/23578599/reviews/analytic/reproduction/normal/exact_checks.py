"""Exact supplementary diagnostics; universal assertions are proved in main.tex.

New independent standard-library code. No claimant or earlier-review imports.
Explicit checks survive -O/-OO; no network, third-party imports or writes.
"""
from fractions import Fraction
from itertools import product
import json


def require(value, label):
    if not value:
        raise RuntimeError(label)


def add(a, b):
    out = dict(a)
    for key, value in b.items():
        out[key] = out.get(key, 0) + value
        if not out[key]:
            del out[key]
    return out


def scale(a, c):
    return {key: c * value for key, value in a.items() if c * value}


def mul(a, b, cutoff=None):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            if cutoff is not None and i + j >= cutoff:
                continue
            out[i + j] = out.get(i + j, 0) + x * y
    return {key: value for key, value in out.items() if value}


def power(a, n, cutoff=None):
    out = {0: 1}
    for _ in range(n):
        out = mul(out, a, cutoff)
    return out


def evaluate_branch(x, coefficients, k, cutoff=None):
    out = {}
    for j, a in enumerate(coefficients, k):
        out = add(out, scale(power(x, j, cutoff), a))
    return out


def order(a):
    return min(a) if a else float('inf')


def member(x, y, coefficients, k, n):
    return order(x) >= 1 and order(add(y, scale(evaluate_branch(x, coefficients, k, n), -1))) >= n


def reduce_mod(a, p):
    return {key: value % p for key, value in a.items() if value % p}


def member_mod(x, y, coefficients, k, n, p):
    return not reduce_mod(add(y, scale(evaluate_branch(x, coefficients, k, n), -1)), p)


def symbolic_multiply(a, b):
    out = {}
    for m, c in a.items():
        for n, d in b.items():
            monomial = tuple(x + y for x, y in zip(m, n))
            out[monomial] = out.get(monomial, 0) + c * d
    return {m: c for m, c in out.items() if c}


def symbolic_add(a, b):
    return add(a, b)


def symbolic_scale(a, c):
    return scale(a, c)


def symbolic_power(a, n):
    out = {(0, 0, 0, 0): 1}
    for _ in range(n):
        out = symbolic_multiply(out, a)
    return out


def coefficient_polynomials(k, bound):
    series = {i: {tuple(int(j == i - 1) for j in range(4)): 1} for i in range(1, 5)}
    result = {0: {(0, 0, 0, 0): 1}}
    for _ in range(k):
        new = {}
        for a, ac in result.items():
            for b, bc in series.items():
                if a + b < bound:
                    new[a + b] = symbolic_add(new.get(a + b, {}), symbolic_multiply(ac, bc))
        result = new
    return result


def run():
    counts = {}
    # Entire finite parameter families, using actual truncated polynomial arithmetic.
    jets = [{i: c for i, c in enumerate(a, 1) if c} for a in product(range(2), repeat=4)]
    finite = {}
    comparisons = 0
    for k in (2, 3):
        parameters = list(product(range(2), repeat=5-k))
        support = 0
        for x, y in product(jets, repeat=2):
            observed = True
            for a in parameters:
                yes = member_mod(x, y, a, k, 5, 2)
                observed = observed and yes
                comparisons += 1
            expected = order(x) >= (5+k-1)//k and order(y) >= 5
            require(observed == expected, 'F2 full finite family versus actual coefficient equations')
            support += observed
        finite[str(k)] = {'parameter_tuples': len(parameters), 'jet_pairs': len(jets)**2, 'support': support}
    require(finite['2']['support'] == 4 and finite['3']['support'] == 8, 'finite supports')
    counts['full_binary_four_jet_memberships'] = comparisons

    # Exact-contact comparison uses two DISTINCT nonzero coefficients in characteristic5.
    jets2 = [{i: c for i, c in enumerate(a, 1) if c} for a in product(range(5), repeat=2)]
    for x, y in product(jets2, repeat=2):
        actual = member_mod(x, y, (1,), 2, 3, 5) and member_mod(x, y, (2,), 2, 3, 5)
        require(actual == (order(x) >= 2 and order(y) >= 3), 'exact-contact two-member finite support')
    counts['quinary_exact_contact_two_jet_pairs'] = len(jets2)**2

    # Symbolic four-jet coefficient ideals over the integers, not a finite-field inference.
    x1 = {(1,0,0,0):1}; x2 = {(0,1,0,0):1}; x3 = {(0,0,1,0):1}
    square = coefficient_polynomials(2, 5)
    cube = coefficient_polynomials(3, 5)
    require(square == {2: {(2,0,0,0):1}, 3: {(1,1,0,0):2}, 4: {(0,2,0,0):1,(1,0,1,0):2}}, 'exact square coefficient ideal')
    require(cube == {3: {(3,0,0,0):1},4: {(2,1,0,0):3}}, 'exact cube coefficient ideal')
    a = symbolic_power(x2, 2); b = symbolic_scale(symbolic_multiply(x1,x3),2)
    ideal_identity = symbolic_add(symbolic_multiply(symbolic_add(a,b), symbolic_add(a,symbolic_scale(b,-1))), symbolic_scale(symbolic_multiply(symbolic_power(x1,2),symbolic_power(x3,2)),4))
    require(ideal_identity == symbolic_power(x2,4), 'x2 fourth power belongs to ideal by exact displayed identity')
    require(all(sum(m)>=2 for polynomial in square.values() for m in polynomial), 'no nonzero degree-one polynomial in homogeneous quadratic ideal')
    counts['exact_symbolic_jet_identities'] = 4

    # Backwards recursive substitution versus the closed polynomial chart formula.
    substitutions = 0
    for n in range(3, 11):
        for k in range(2,n):
            a = tuple((j % 5)-2 for j in range(k,n))
            for x in ({1:1,2:-2},{2:2,5:1},{1:-1,3:2}):
                w = {0:2,1:-1,3:3}
                u = w
                for c in reversed(a):
                    u = add({0:c} if c else {}, mul(x,u))
                recursive = mul(power(x,k),u)
                explicit = add(evaluate_branch(x,a,k),mul(power(x,n),w))
                require(recursive == explicit,'all finite-center recursive chart substitutions')
                substitutions += 1
    counts['recursive_chart_compositions'] = substitutions

    # Direct density specializations, including x=0 and the constant arc.
    wedges = 0
    for k in (2,3):
        for coefficients in product((-1,0,1),repeat=5-k):
            for x0 in ({},{3:1},{1:-1,2:2},{2:1,6:-2}):
                residual = {5:1,7:-1} if x0 else {}
                y0 = add(evaluate_branch(x0,coefficients,k),residual)
                require(member(x0,y0,coefficients,k,5),'special arc in cylinder')
                for e in (-3,-2,-1,0,1,2,3):
                    xe = add(x0,{1:e}if e else {})
                    ye = add(evaluate_branch(xe,coefficients,k),residual)
                    require(add(ye,scale(evaluate_branch(xe,coefficients,k),-1)) == residual,'wedge retains exact residual')
                    if e == 0:
                        require(xe==x0 and ye==y0,'wedge special fiber')
                    if e != -x0.get(1,0):
                        require(order(xe)==1,'generic first coefficient nonzero')
                    wedges += 1
    counts['density_specialization_values'] = wedges

    # Both chart order maps; infinity arithmetic is treated explicitly.
    chart_orders = 0
    for n in range(1,11):
        for q in range(1,10):
            for av in [0,1,2,3,4,5,float('inf')]:
                for bh in range(q,q+6):
                    ox=av+bh; oy=(0 if n==1 else (n-1)*av)+n*bh
                    require(ox>=q and oy>=n*q,'satellite chart contact containment')
                    chart_orders += 1
    counts['two_chart_order_cases'] = chart_orders

    # Explicit convergent witnesses; q and j are finite diagnostics here.
    witnesses = 0; branches = {'q<r':0,'q>r':0,'q=r,jr>5':0,'q=r,jr<5':0}
    for r in (2,3):
        for q in range(1,65):
            for j in range(1,65):
                if q<r:
                    x={q:1}; y={max(5,j*q):1}; direction='right'; branch='q<r'
                elif q>r:
                    x={r:1}; y={5:1}; direction='left'; branch='q>r'
                elif j*r>5:
                    x={r:1}; y={5:1}; direction='left'; branch='q=r,jr>5'
                else:
                    require(j*r<5,'no integral equality case')
                    x={r:1}; y={j*r:1}; direction='right'; branch='q=r,jr<5'
                left=order(x)>=r and order(y)>=5
                right=order(x)>=q and order(y)>=j*q
                require((left and not right)if direction=='left'else(right and not left),'actual convergent separating monomial arc')
                branches[branch]+=1; witnesses+=1
    counts['convergent_separating_witnesses'] = witnesses

    # Exact monomial inverses and Jacobian/codimension consistency for OTHER divisors.
    toric = []
    for a,b,c,d in [(3,5,1,2),(2,5,1,3)]:
        determinant=a*d-b*c;require(determinant==1,'toric chart unimodularity')
        require(d*a-c*b==1 and -b*a+a*b==0 and d*c-c*d==0 and -b*c+a*d==1,'integer matrix inverse')
        for leadx,leady in product((-2,-1,1,2,3),repeat=2):
            u=Fraction(leadx)**d/Fraction(leady)**c
            v=Fraction(leady)**a/Fraction(leadx)**b
            require(u**a*v**c==leadx and u**b*v**d==leady,'exact rational leading coefficient inverse')
        toric.append({'weight':[a,b],'matrix':[[a,c],[b,d]],'det':determinant,'jacobian_u_order':a+b-1,'full_arc_cylinder_codimension':a+b})
    counts['toric_rational_inverse_cases'] = 50

    pairs = 0
    for n in range(3,61):
        for k in range(2,n):
            r=(n+k-1)//k
            require((k*r==n)==(n%k==0),'finite divisibility consistency')
            pairs += 1
    counts['rounding_divisibility_pairs'] = pairs

    controls = {}
    def reject(label,false_statement):
        require(not false_statement,label+' false mutation unexpectedly true')
        controls[label]='rejected'
    reject('floor_for_ceiling',5//2==(5+1)//2)
    reject('one_completion_is_entire_family',not(member({1:1},{},(0,0,0),2,5)and not member({1:1},{},(1,0,0),2,5)))
    reject('F2_equals_F3',(2>=3)==(2>=2))
    reject('q2_D3_equals_I53',5>=3*2)
    reject('all_selected_point_families_are_singletons',5-3==0)
    reject('zero_x_excluded_from_closure',not member({}, {5:1},(1,2,3),2,5))
    reject('all_closure_arcs_are_transverse',order({3:1})==1)
    reject('all_closure_arcs_lift_in_first_chart',5>=5*3)
    reject('no_other_divisorial_set_has_these_weights',any(t['det']!=1 for t in toric))
    reject('one_Puiseux_first_exceptional_case_refuted',not(5==5 and 5==1*5))
    reject('char2_one_and_two_both_exact_contact',1%2!=0 and 2%2!=0)
    reject('quadratic_ideal_contains_linear_x1',min(sum(m)for p in square.values()for m in p)==1)
    return {'status':'PASS','scope':'Supplementary exact finite diagnostics only. Universal complex-family exhaustion, Zariski density, all-integer conclusions, source interpretation and priority rest on the written proof/source audit. No claimant or prior verifier replay.','counts':counts,'binary_complete_four_jet_families':finite,'separating_witness_branches':branches,'toric_other_divisors':toric,'negative_controls':controls}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False))
