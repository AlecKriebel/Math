#!/usr/bin/env python3
"""Independent finite and symbolic regressions. These do not prove an asymptotic theorem."""
from collections import Counter
from functools import lru_cache
from fractions import Fraction
from itertools import permutations, combinations, product
from math import factorial, prod
from pathlib import Path
import hashlib, json, sys, time
import sympy as sp
import mpmath as mp

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PINS = {
    'pass1_uncovered_case/TWO_SUBCASE_THEOREM.md': '3afd21739fdb296393c21cc232130d94315d035434d98f7cb6e07b670a9af7ce',
    'pass1_entropy/KERNEL_ENUMERATION_APPENDIX.md': 'a57401941f3ec1296e7880d791a495c4daec92d8c714e92435c1e73d443c5181',
    'pass2_protected_tail_extension/MERGE_TRANSFER_THEOREM.md': 'd8a88fb75f5f2c78509e0610420cb8701d5445de0ae1be856d2c0e0b9d919d34',
}

def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def rank(p):
    return tuple(sorted(p).index(x) + 1 for x in p)


def split_skew(p):
    n = len(p)
    last = 0
    result = []
    # Every prefix cut whose value set is the top interval is a skew cut.
    for end in range(1, n + 1):
        if min(p[:end]) == n - end + 1:
            result.append(rank(p[last:end]))
            last = end
    require(last == n, ('skew split failed', p))
    return tuple(result)


def minima(p):
    return tuple((i, x) for i, x in enumerate(p) if x == min(p[:i + 1]))


def normalization(p):
    fixed = dict(minima(p))
    used = set()
    q = []
    current_min = None
    for i in range(len(p)):
        if i in fixed:
            v = current_min = fixed[i]
        else:
            v = next(v for v in range(current_min + 1, len(p) + 1) if v not in used)
        used.add(v)
        q.append(v)
    return tuple(q)


@lru_cache(None)
def tree_of_normalization(q):
    require(q and q[-1] == len(q), ('normalization not tree rooted', q))
    return tuple(tree_of_normalization(block) for block in split_skew(q[:-1])) if len(q) > 1 else ()


@lru_cache(None)
def size(t):
    return 1 + sum(size(c) for c in t)


@lru_cache(None)
def depth_profile(t):
    result = [1]
    for c in t:
        ds = depth_profile(c)
        result += [0] * max(0, len(ds) + 1 - len(result))
        for d, v in enumerate(ds, 1):
            result[d] += v
    return tuple(result)


@lru_cache(None)
def relaxed_labels(t):
    if not t:
        return ((0, 1),)
    sums = Counter({0: 1})
    for c in t:
        new = Counter()
        for x, a in sums.items():
            for y, b in relaxed_labels(c):
                new[x + y] += a * b
        sums = new
    out = Counter()
    for s, v in sums.items():
        for label in range(s + 2):
            out[label] += v
    return tuple(sorted(out.items()))


@lru_cache(None)
def proper_count(t):
    return prod(sum(v for _, v in relaxed_labels(c)) for c in t)


@lru_cache(None)
def ordered_forests(n):
    if not n:
        return ((),)
    return tuple((t,) + tail for k in range(1, n + 1) for t in ordered_trees(k)
                 for tail in ordered_forests(n - k))


@lru_cache(None)
def ordered_trees(n):
    return tuple(ordered_forests(n - 1))


def avoids_1342(p):
    n = len(p)
    for j in range(1, n - 2):
        low = min(p[:j])
        for k in range(j + 1, n - 1):
            if p[j] < p[k] and any(low < p[l] < p[j] for l in range(k + 1, n)):
                return False
    return True


@lru_cache(None)
def patterns(p, m):
    return frozenset(rank(tuple(p[i] for i in ids)) for ids in combinations(range(len(p)), m))


def labeled_image(p, t):
    # Source F: child-before-parent vertex order, reachability labels on nonroots,
    # and the root-sum rule in Definition 1. No preprint count formula is used.
    nodes = []
    def visit(tree, depth):
        start = len(nodes)
        roots = [visit(c, depth + 1) for c in tree]
        idx = len(nodes)
        nodes.append((start, idx, tuple(roots), depth))
        return idx
    root = visit(t, 0)
    reach = [set() for _ in p]
    for j in range(len(p) - 1, -1, -1):
        low = min(p[:j], default=len(p) + 1)
        for k in range(j + 1, len(p)):
            if low < p[k] < p[j]:
                reach[j].add(k)
                reach[j].update(reach[k])
    labels = []
    for a, i, children, _ in nodes:
        if i == root:
            label = sum(labels[c] for c in children)
        else:
            label = sum(any(k > i for k in reach[j]) for j in range(a, i + 1))
        if not children:
            require(label == 0, ('nonzero leaf', p, i, label))
        else:
            require(label <= 1 + sum(labels[c] for c in children), ('invalid label', p, i, label))
        labels.append(label)
    return tuple(labels), nodes


def geometry_and_shape_law():
    rows = []
    for n in range(1, 9):
        by_forest = Counter()
        images = set()
        indecomp = 0
        for p in permutations(range(1, n + 1)):
            if not avoids_1342(p):
                continue
            blocks = split_skew(p)
            forest = []
            for block in blocks:
                q = normalization(block)
                t = tree_of_normalization(q)
                forest.append(t)
                require(minima(block) == minima(q), ('minima changed', block, q))
                labels, nodes = labeled_image(block, t)
                leaves = tuple((i, q[i]) for _, i, children, _ in nodes if not children)
                require(leaves == minima(q), ('leaf minima mismatch', block, q, leaves))
                h = len(depth_profile(t)) - 1
                for _, i, children, d in nodes:
                    if not children:
                        require(i + 1 + q[i] == len(q) + 1 - d, ('leaf formula', q, i, d))
                require(min(i + 1 + v for i, v in enumerate(block)) >= len(block) + 1 - h,
                        ('component envelope', block, h))
                if len(blocks) == 1:
                    indecomp += 1
                    key = (t, labels)
                    require(key not in images, ('noninjective labeled map', p, key))
                    images.add(key)
            forest = tuple(forest)
            by_forest[forest] += 1
            H = max(len(depth_profile(t)) - 1 for t in forest)
            require(min(i + 1 + v for i, v in enumerate(p)) >= n + 1 - H,
                    ('forest envelope', p, H))
        # Compare multiplicities for every shape, including absent shapes.
        all_forests = ordered_forests(n)
        require(len(all_forests) == len(by_forest), ('missing forest shape', n))
        for forest in all_forests:
            expected = prod(proper_count(t) for t in forest)
            require(by_forest[forest] == expected, ('wrong exact labeled shape law', n, forest,
                                                 by_forest[forest], expected))
        expected_trees = sum(proper_count(t) for t in ordered_trees(n))
        require(indecomp == expected_trees == len(images), ('tree bijection count', n))
        rows.append({'n': n, 'avoiders': sum(by_forest.values()), 'skew_indecomposable': indecomp,
                     'forest_shapes': len(by_forest), 'distinct_labeled_images': len(images)})
    return rows


def tree_algebra_and_depth():
    z, u, b, c = sp.symbols('z u b c')
    P = (1-u)*(b-z)*(1-b) - z*c*(1-b) + z*u*u*b
    Pb, Pu = sp.diff(P,b), sp.diff(P,u)
    require(sp.expand(P + (1-b)*Pb - ((1-u)*(1-b)**2 + z*u*u)) == 0, 'kernel addition')
    beta = sp.symbols('beta')
    subs = {z: beta*(1-2*beta), u: (1-beta)/(1-2*beta),
            b: beta, c: beta*(1-3*beta)/(1-2*beta)**2}
    for expression in (P,Pb,Pu):
        require(sp.factor(expression.subs(subs)) == 0, ('kernel point', expression))
    s = sp.symbols('s', positive=True)
    z_s = (1-s*s)/8
    c_s = (1-s)*(1+3*s)/(4*(1+s)**2)
    b_s = (s**3+3*s*s+2*s+2-s**sp.Rational(3,2)*sp.sqrt(s**3+6*s*s+33*s+24))/(8*(1+s))
    require(sp.simplify(P.subs({z:z_s,u:sp.Rational(3,2),b:b_s,c:c_s})) == 0,
            'selected u=3/2 branch is not root')
    require(sp.simplify(b_s.subs(s,1)) == 0, 'wrong branch at z=0')
    t = sp.symbols('t', positive=True)
    b_t = b_s.subs(s,t*t)
    b_exp = sp.series(b_t,t,0,6)
    M = sp.Rational(9,2)*z_s/(1-b_s)**2
    M_exp = sp.series(M.subs(s,t*t),t,0,6)
    require(sp.expand(b_exp.removeO()).coeff(t,3) == -sp.sqrt(6)/4, 'b critical coefficient')
    require(sp.expand(M_exp.removeO()).coeff(t,3) == -2*sp.sqrt(6)/3, 'M critical coefficient')
    require(sp.limit(b_s,s,0) == sp.Rational(1,4), 'b critical value')
    T = (8*z*z+12*z-1+(1-8*z)**sp.Rational(3,2))/(32*z)
    Tcoeff = sp.series(T,z,0,31).removeO().expand()
    for n in range(1,31):
        formula = 1 if n == 1 else 3*2**(n-2)*factorial(2*n-2)//(factorial(n+1)*factorial(n-1))
        require(Tcoeff.coeff(z,n) == formula, ('T coefficient',n))
    require(sp.limit(T,z,sp.Rational(1,8),dir='-') == sp.Rational(5,32), 'T critical value')
    # Exact weighted depth profiles from plane shapes, not the marked recurrence being tested.
    N = 9
    B = [Fraction(0)]*(N+1)
    W = [[Fraction(0)]*(N+1) for _ in range(N)]
    proper = []
    for n in range(1,N+1):
        total = 0
        for tree in ordered_trees(n):
            weight = sum(Fraction(v)*Fraction(3,2)**label for label,v in relaxed_labels(tree))
            B[n] += weight
            total += proper_count(tree)
            for h,v in enumerate(depth_profile(tree)):
                W[h][n] += v*weight
        require(total == Tcoeff.coeff(z,n), ('shape enumeration',n))
        proper.append(total)
    # 1/(1-B), squared, and multiplied by 9z/2.
    seq = [Fraction(1)] + [Fraction(0)]*N
    for n in range(1,N+1):
        seq[n] = sum(B[k]*seq[n-k] for k in range(1,n+1))
    Mcoef = [Fraction(0)] + [Fraction(9,2)*sum(seq[k]*seq[n-1-k] for k in range(n))
                                    for n in range(1,N+1)]
    inequalities = 0
    for h in range(N-1):
        for n in range(N+1):
            bound = sum(Mcoef[k]*W[h][n-k] for k in range(n+1))
            require(W[h+1][n] <= bound, ('marked-depth inequality',h,n,W[h+1][n],bound))
            inequalities += 1
    mp.mp.dps = 80
    rates = []
    for eps_text in ('0.5','0.1','0.01','0.001'):
        eps = mp.mpf(eps_text)
        delta = (eps/10)**4
        sval = mp.sqrt(delta)
        bv = (sval**3+3*sval**2+2*sval+2-sval**mp.mpf('1.5')*mp.sqrt(sval**3+6*sval**2+33*sval+24))/(8*(sval+1))
        zv = (1-delta)/8
        mv = (mp.mpf(9)/2)*zv/(1-bv)**2
        lograte = mp.log(mp.mpf(1)/8/zv) + eps*mp.log(mv)
        require(lograte < 0, ('height rate sample',eps_text))
        rates.append({'epsilon':eps_text,'delta':mp.nstr(delta,15),'log_rate':mp.nstr(lograte,15)})
    return {'kernel_polynomial_identities':True,'u_3_over_2_branch':True,
            'puiseux_parameter':'t=(1-8z)^(1/4)', 'b_expansion':str(b_exp), 'M_expansion':str(M_exp),
            'closed_form_coefficients_checked_through':30,'shape_tree_counts':proper,
            'marked_depth_coefficient_inequalities_checked':inequalities,
            'weighted_relaxed_coefficients':[str(x) for x in B[1:]], 'height_rate_samples':rates}


def starts_one_deletion():
    qs = tuple(q for length in (2,3,4) for q in permutations(range(1,length+1)) if q[0] == 1)
    rows = []
    for n in range(1,8):
        tested = 0
        for p in permutations(range(1,n+1)):
            deleted = {i for i,_ in minima(p)}
            remainder = rank(tuple(v for i,v in enumerate(p) if i not in deleted))
            P = tuple(i for i in range(n) if i not in deleted)
            V = tuple(sorted(p[i] for i in P))
            recon = [None]*n
            for i,sval in zip(P,remainder):
                recon[i] = V[sval-1]
            other = iter(sorted(set(p)-set(V),reverse=True))
            for i in range(n):
                if recon[i] is None:
                    recon[i] = next(other)
            require(tuple(recon)==p, ('canonical injection reconstruction',p))
            for q in qs:
                qp = (1,) + tuple(v+1 for v in q)
                lhs = qp not in patterns(p,len(qp))
                rhs = q not in patterns(remainder,len(q))
                require(lhs == rhs, ('starts1 equivalence',p,q,remainder))
                tested += 1
        rows.append({'n':n,'permutation_pattern_pairs':tested})
    p=(3,4,1,2)
    require((1,3,2) not in patterns(p,3), 'starts1 counterexample avoids132')
    require(rank(tuple(v for i,v in enumerate(p) if i not in {j for j,_ in minima(p)})) == (2,1),
            'starts1 counterexample residual')
    return {'rows':rows,'patterns_q_checked':[list(q) for q in qs],
            'without_starts1_equivalence_fails':{'q':[2,1],'q_prime':[1,3,2],'pi':[3,4,1,2],'remainder':[2,1]}}


def discrepancy_numerator(P,n):
    k=len(P)
    return max(abs(n*sum(x<=j for x in P)-k*j) for j in range(n+1))


def merge_geometry():
    rows=[]
    for n in range(1,8):
        tested=0
        for k in range(n+1):
            subs=tuple(combinations(range(1,n+1),k))
            errors={P:discrepancy_numerator(P,n) for P in subs}
            complements={P:tuple(x for x in range(1,n+1) if x not in P) for P in subs}
            for P in subs:
                require(errors[P] == discrepancy_numerator(complements[P],n),'complement discrepancy')
            for sigma in permutations(range(1,k+1)):
                Ssigma=sum(abs(i+v-k-1) for i,v in enumerate(sigma,1))
                for P,V in product(subs,repeat=2):
                    pi=[0]*n
                    for i,v in zip(P,sigma): pi[i-1]=V[v-1]
                    for i,v in zip(complements[P],reversed(complements[V])): pi[i-1]=v
                    Spi=sum(abs(i+v-n-1) for i,v in enumerate(pi,1))
                    if k:
                        require(k*Spi <= n*Ssigma+2*k*(errors[P]+errors[V])+n*k,
                                ('merge inequality',n,k,P,V,sigma,pi))
                    else:
                        require(Spi==0,'empty merge')
                    tested+=1
        rows.append({'n':n,'ambient_triples_tested':tested})
    return rows


def main():
    start=time.time()
    for path,expected in PINS.items():
        require(hashlib.sha256((BASE/path).read_bytes()).hexdigest()==expected,('input hash',path))
    out={'status':'PASS','scope':'Finite and symbolic regression evidence only; asymptotic audit is separate.',
         'input_sha256':PINS,'python':sys.version,'sympy':sp.__version__,'optimization_level':sys.flags.optimize}
    out['exact_shape_law_and_geometry']=geometry_and_shape_law()
    print('Exact shape/labeled law and geometry passed.',flush=True)
    out['catalytic_algebra_and_depth']=tree_algebra_and_depth()
    print('Catalytic algebra and marked-depth checks passed.',flush=True)
    out['minima_deletion']=starts_one_deletion()
    print('Minima deletion and injective reconstruction passed.',flush=True)
    out['deterministic_merge_geometry']=merge_geometry()
    print('Exhaustive ambient merge geometry passed.',flush=True)
    out['elapsed_seconds']=round(time.time()-start,3)
    path=HERE/f'CHECK_OPTIMIZATION_{sys.flags.optimize}.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(path),'status':'PASS','elapsed_seconds':out['elapsed_seconds']}))

if __name__=='__main__': main()
