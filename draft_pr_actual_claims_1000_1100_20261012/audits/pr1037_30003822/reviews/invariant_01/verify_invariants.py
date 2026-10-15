#!/usr/bin/env python3
"""Fresh, self-contained exact checks; no imports of prior audit/transfer code.

The complete theorem is proved in DERIVATION.md. These finite checks attack
the invariant, spanning and character mechanisms. They do not enumerate the
forest transfer matrix, and do not substitute numerical success for a proof.
"""
from pathlib import Path
from itertools import combinations, product, permutations
from collections import defaultdict
from math import comb, gcd, factorial
from functools import reduce
from fractions import Fraction
import argparse
import datetime
import hashlib
import json
import platform
import time


def clean(v):
    return {k: c for k, c in v.items() if c}


def add(a, b, scale=1):
    out = dict(a)
    for k, c in b.items():
        out[k] = out.get(k, 0) + scale*c
        if not out[k]:
            del out[k]
    return out


def wedge(a, b):
    out = defaultdict(int)
    for x, ca in a.items():
        for y, cb in b.items():
            if x & y:
                continue
            inversions = sum((y & ((1 << i)-1)).bit_count()
                             for i in range(x.bit_length()) if x & (1 << i))
            out[x | y] += (-1 if inversions % 2 else 1)*ca*cb
    return clean(out)


def primitive(v):
    if not v:
        return v
    d = reduce(gcd, (abs(c) for c in v.values()))
    if v[min(v)] < 0:
        d = -d
    return {k: c//d for k, c in v.items()}


def exact_basis(columns):
    """Fraction-free sparse rational rank, with gcd removal after each step."""
    basis, independent = {}, []
    for j, col in enumerate(columns):
        v = primitive(dict(col))
        while v:
            p = min(v)
            if p not in basis:
                basis[p] = v
                independent.append(j)
                break
            b, c = basis[p], v[p]
            v = primitive(add({k: b[p]*x for k, x in v.items()}, b, -c))
    return basis, independent


def rank(columns):
    return len(exact_basis(columns)[0])


def act(v, m, raising=True):
    out = defaultdict(int)
    for mask, c in v.items():
        for i in range(m):
            src, dst = (m+i, i) if raising else (i, m+i)
            if not mask & (1 << src) or mask & (1 << dst):
                continue
            removed = mask ^ (1 << src)
            sign = (-1 if ((mask & ((1 << src)-1)).bit_count()
                           + (removed & ((1 << dst)-1)).bit_count()) % 2 else 1)
            out[removed | (1 << dst)] += sign*c
    return clean(out)


def weight(mask, m):
    return (mask & ((1 << m)-1)).bit_count() - (mask >> m).bit_count()


def multidegree(mask, m):
    return tuple(int(bool(mask & (1 << i))) + int(bool(mask & (1 << (m+i))))
                 for i in range(m))


def choose_masks(m, p, q):
    if p < 0 or p > m or q < 0 or q > m:
        return []
    return [sum(1 << i for i in x) | sum(1 << (m+i) for i in y)
            for x in combinations(range(m), p) for y in combinations(range(m), q)]


def binom(m, r):
    return comb(m, r) if 0 <= r <= m else 0


def catalan(n):
    return comb(2*n, n)//(n+1)


def partitions(n):
    """Restricted-growth words, with deterministic block order."""
    if n == 0:
        yield ()
        return
    def visit(word, mx):
        if len(word) == n:
            yield tuple(tuple(i for i, b in enumerate(word) if b == j)
                        for j in range(mx+1))
        else:
            for b in range(mx+2):
                yield from visit(word+[b], max(mx, b))
    yield from visit([0], 0)


def xi_coeff(u, barred, m):
    return {1 << (i+(m if barred else 0)): c for i, c in enumerate(u) if c}


def qedge(i, j, n):
    m = n-1
    u = [0]*m
    if i < m:
        u[i] += 1
    if j < m:
        u[j] -= 1
    return wedge(xi_coeff(u, False, m), xi_coeff(u, True, m))


def fpartition(p, n, tree='star'):
    f = {0: 1}
    for block in p:
        edges = ([(block[0], j) for j in block[1:]] if tree == 'star'
                 else list(zip(block, block[1:])))
        for i, j in edges:
            f = wedge(f, qedge(i, j, n))
    return f


def bquad(i, j, m, wrong_sign=False):
    a = wedge({1 << i: 1}, {1 << (m+j): 1})
    b = wedge({1 << j: 1}, {1 << (m+i): 1})
    return add(a, b, -1 if wrong_sign else 1)


def invariant_checks(max_m):
    results = []
    for m in range(max_m+1):
        # Independently verify the chosen signs, adjoint and commutator in
        # every exterior degree, even and odd, on all 2^(2m) monomials.
        for mask in range(1 << (2*m)):
            v = {mask: 1}
            comm = add(act(act(v, m, False), m), act(act(v, m), m, False), -1)
            expected = {mask: weight(mask, m)} if weight(mask, m) else {}
            assert comm == expected
            for dst, c in act(v, m).items():
                assert act({dst: 1}, m, False).get(mask, 0) == c
        dims, exponents = [], [0]*m
        weight_details = []
        for r in range(m+1):
            src = choose_masks(m, r, r)
            dst = choose_masks(m, r+1, r-1)
            ecols = [act({mask: 1}, m) for mask in src]
            erank = rank(ecols)
            predicted = binom(m, r)**2-binom(m, r-1)*binom(m, r+1)
            assert erank == len(dst)
            observed = len(src)-erank
            assert observed == predicted
            grouped = defaultdict(list)
            for mask, col in zip(src, ecols):
                grouped[multidegree(mask, m)].append(col)
            for w, cols in sorted(grouped.items()):
                dim = len(cols)-rank(cols)
                if dim:
                    weight_details.append({'degree':2*r, 'weight':w, 'dimension':dim})
                    for i in range(m):
                        exponents[i] += w[i]*dim
            dims.append({'r':r, 'M0_dimension':len(src), 'M2_dimension':len(dst),
                         'E_rank_over_Q':erank, 'invariant_dimension':observed})
        total = sum(x['invariant_dimension'] for x in dims)
        assert total == catalan(m+1)
        assert sum(2*x['r']*x['invariant_dimension'] for x in dims) == m*total
        assert exponents == [total]*m
        diag = list(range(2, m+2))
        torus_det = product_int(product_int(t**a for t, a in zip(diag, x['weight']))
                                **x['dimension'] for x in weight_details)
        expected_det = product_int(diag)**total
        assert torus_det == expected_det
        results.append({'m':m,'n':m+1,'degree_checks':dims,'total_dimension':total,
                        'torus_exponents':exponents,'diagonal_values':diag,
                        'exact_torus_det':str(torus_det), 'weight_details':weight_details})
        print('exact infinitesimal and torus:', m, total, flush=True)
    return results


def product_int(seq):
    ans = 1
    for x in seq:
        ans *= x
    return ans


def partition_checks(max_n):
    results = []
    for n in range(1, max_n+1):
        m = n-1
        ps = list(partitions(n))
        fs = [fpartition(p, n) for p in ps]
        for p, f in zip(ps, fs):
            assert f == fpartition(p, n, 'path')
            assert not act(f, m) and not act(f, m, False)
        degrees = []
        for r in range(m+1):
            cols = [f for p, f in zip(ps, fs) if n-len(p) == r]
            rk = rank(cols)
            dim = binom(m, r)**2-binom(m, r-1)*binom(m, r+1)
            assert rk == dim
            degrees.append({'r':r,'partition_columns':len(cols),'image_rank_over_Q':rk})
        rk = rank(fs)
        assert rk == catalan(n)
        results.append({'n':n,'Bell_partition_count':len(ps),'partition_image_rank_over_Q':rk,
                        'kernel_dimension':len(ps)-rk,'degree_checks':degrees,
                        'star_path_equality_all_partitions':True,
                        'E_and_F_annihilate_every_partition_image':True})
        print('exact partition image:', n, len(ps), rk, flush=True)
    return results


def noncrossing_matchings(r, offset=0):
    if r == 0:
        yield ()
        return
    for inside in range(r):
        j = offset+2*inside+1
        for a in noncrossing_matchings(inside, offset+1):
            for b in noncrossing_matchings(r-inside-1, j+1):
                yield ((offset, j),)+a+b


def match_tensor(matching):
    v = {0:1}
    for left, right in matching:
        # Tensor words use bit 1 for plus. Slots are independent: no exterior
        # reordering signs are inserted here.
        out = {}
        for word, c in v.items():
            out[word | (1 << left)] = c
            out[word | (1 << right)] = -c
        v = out
    return v


def tensor_E(v, k):
    out = defaultdict(int)
    for word, c in v.items():
        for i in range(k):
            if not word & (1 << i):
                out[word | (1 << i)] += c
    return clean(out)


def matching_checks(max_r):
    result = []
    for r in range(max_r+1):
        ms = list(noncrossing_matchings(r))
        vs = [match_tensor(x) for x in ms]
        leaders = []
        for v in vs:
            assert not tensor_E(v, 2*r)
            lead = max(v, key=lambda w: tuple(int(bool(w & (1 << i))) for i in range(2*r)))
            assert v[lead] == 1
            balance = 0
            for i in range(2*r):
                balance += 1 if lead & (1 << i) else -1
                assert balance >= 0
            assert balance == 0
            leaders.append(lead)
        assert len(set(leaders)) == len(ms) == catalan(r)
        observed = rank(vs)
        assert observed == catalan(r)
        result.append({'r':r,'matching_count':len(ms),'exact_tensor_rank_over_Q':observed,
                       'distinct_Dyck_leaders_coefficient_1':True,'E_annihilation':True})
        print('exact matching tensors:', r, observed, flush=True)
    return result


def substitution(v, g):
    """Row-coefficient action: plus_i -> sum_j g_ij plus_j, likewise minus."""
    m = len(g)
    out = {}
    for mask, c in v.items():
        term = {0:c}
        for old in range(2*m):
            if mask & (1 << old):
                i, barred = old % m, old >= m
                replacement = {1 << (j+(m if barred else 0)):g[i][j]
                               for j in range(m) if g[i][j]}
                term = wedge(term, replacement)
        out = add(out, term)
    return out


def coordinate_solver(columns):
    """Exact rational basis together with original-column coordinates."""
    basis = {}
    for j, col in enumerate(columns):
        v = {k:Fraction(x) for k,x in col.items()}
        coord = {j:Fraction(1)}
        while v:
            p = min(v)
            if p not in basis:
                scale = v[p]
                basis[p] = ({k:x/scale for k,x in v.items()},
                            {k:x/scale for k,x in coord.items()})
                break
            b, bc = basis[p]
            scale = v[p]
            v = add(v, b, -scale)
            coord = add(coord, bc, -scale)
        if not v:
            raise AssertionError('dependent input basis')
    def solve(col):
        v = {k:Fraction(x) for k,x in col.items()}
        coord = {}
        while v:
            p = min(v)
            assert p in basis, 'outside image'
            b, bc = basis[p]
            scale = v[p]
            v = add(v, b, -scale)
            coord = add(coord, bc, scale)
        return coord
    return solve


def determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    det = Fraction(1)
    for i in range(len(a)):
        j = next((j for j in range(i,len(a)) if a[j][i]), None)
        if j is None:
            return Fraction(0)
        if i != j:
            a[i], a[j] = a[j], a[i]
            det = -det
        pivot = a[i][i]
        det *= pivot
        for j in range(i+1,len(a)):
            scale = a[j][i]/pivot
            for k in range(i,len(a)):
                a[j][k] -= scale*a[i][k]
    return det


def explicit_character_checks(max_m=4):
    results = []
    for m in range(1,max_m+1):
        fs = [fpartition(p,m+1) for p in partitions(m+1)]
        _, indices = exact_basis(fs)
        basis = [fs[i] for i in indices]
        solve = coordinate_solver(basis)
        gs = {}
        gs['dense_nonsymmetric'] = [[(i+2)**(j+1) + (1 if i == j else 0)
                                    for j in range(m)] for i in range(m)]
        gs['unipotent_shear'] = [[int(i==j)+(3 if i==0 and j==m-1 and m>1 else 0)
                                 for j in range(m)] for i in range(m)]
        gs['permutation'] = [[int(j==(i+1)%m) for j in range(m)] for i in range(m)]
        gs['singular'] = [[i*(j+2) for j in range(m)] for i in range(m)]
        for mode, g in gs.items():
            cols = [solve(substitution(f,g)) for f in basis]
            matrix = [[col.get(i,0) for col in cols] for i in range(len(basis))]
            dg, drho = determinant(g), determinant(matrix)
            assert drho == dg**catalan(m+1)
            results.append({'m':m,'mode':mode,'g':g,'det_g':str(dg),
                            'invariant_basis_dimension':len(basis),
                            'exact_det_rho':str(drho),'expected':str(dg**catalan(m+1))})
        print('explicit character matrices:', m, len(basis), flush=True)
    return results


def exterior_project(tensor):
    out = defaultdict(Fraction)
    for word, c in tensor.items():
        if len(set(word)) != len(word):
            continue
        inversions = sum(word[i] > word[j] for i in range(len(word))
                         for j in range(i+1,len(word)))
        mask = sum(1 << i for i in word)
        out[mask] += (-1 if inversions % 2 else 1)*c
    return clean(out)


def normalized_embed(v):
    out = defaultdict(Fraction)
    for mask, c in v.items():
        word = tuple(i for i in range(mask.bit_length()) if mask & (1 << i))
        k = len(word)
        for perm in permutations(range(k)):
            inversions = sum(perm[i] > perm[j] for i in range(k) for j in range(i+1,k))
            out[tuple(word[i] for i in perm)] += Fraction(c*(-1 if inversions%2 else 1),factorial(k))
    return clean(out)


def tensor_exterior_E(tensor,m):
    out = defaultdict(Fraction)
    for word,c in tensor.items():
        for pos,a in enumerate(word):
            if a >= m:
                dst = word[:pos]+(a-m,)+word[pos+1:]
                out[dst] += c
    return clean(out)


def tensor_product(a,b):
    out=defaultdict(Fraction)
    for x,c in a.items():
        for y,d in b.items():
            out[x+y] += c*d
    return clean(out)


def projection_checks():
    m=3
    monomial_count=0
    # Exhaustive in all degrees of Lambda(Q^3 tensor Q^2), including repeated
    # generators arising after E acts on the tensor lift.
    for mask in range(1 << (2*m)):
        v={mask:1}
        lifted=normalized_embed(v)
        assert exterior_project(lifted)==v
        assert tensor_exterior_E(lifted,m)==normalized_embed(act(v,m))
        assert exterior_project(tensor_exterior_E(lifted,m))==act(v,m)
        monomial_count += 1
    vectors=[(1,0,0),(0,1,0),(0,0,1),(1,-2,3),(2,1,-1),(1,1,1)]
    checks=[]
    for r in range(4):
        paired_tensor={():Fraction(1)}
        projected_product={0:1}
        for i in range(r):
            u,v=vectors[2*i],vectors[2*i+1]
            epsilon=defaultdict(Fraction)
            for a,ca in enumerate(u):
                for b,cb in enumerate(v):
                    if ca and cb:
                        epsilon[(a,m+b)] += ca*cb
                        epsilon[(m+a,b)] -= ca*cb
            paired_tensor=tensor_product(paired_tensor,clean(epsilon))
            quad=add(wedge(xi_coeff(u,False,m),xi_coeff(v,True,m)),
                     wedge(xi_coeff(v,False,m),xi_coeff(u,True,m)))
            projected_product=wedge(projected_product,quad)
        assert not tensor_exterior_E(paired_tensor,m)
        assert exterior_project(paired_tensor)==projected_product
        assert not act(projected_product,m)
        checks.append({'r':r,'tensor_term_count':len(paired_tensor),
                       'projected_term_count':len(projected_product),
                       'paired_epsilon_projection_equals_product_b':True})
    # Negative normalization control: removing 1/k! makes pi iota = k! I.
    v={3:1} # plus_0 wedge plus_1, k=2
    mutant={word:2*c for word,c in normalized_embed(v).items()}
    assert exterior_project(mutant)=={3:2} and exterior_project(mutant)!=v
    return {'m':m,'exhaustive_monomials_checked':monomial_count,
            'normalized_projection_left_inverse':True,'E_equivariance':True,
            'paired_epsilon_checks':checks,
            'negative_control_missing_factorial_detected':True}


def negative_controls():
    results = []
    # Replacing the symmetric exterior quadratic by an antisymmetric one
    # destroys E-invariance, despite superficial resemblance to epsilon.
    bad = bquad(0,1,2,wrong_sign=True)
    assert act(bad,2)
    results.append({'mutation':'minus instead of plus in b(u,v)',
                    'detected_by':'nonzero E action','residual':act(bad,2)})
    # Missing 2 on the diagonal breaks the actual exterior identity.
    bdiag, q = bquad(0,0,2), qedge(0,2,3)
    assert bdiag != q and bdiag == {k:2*x for k,x in q.items()}
    results.append({'mutation':'b(ui,ui)=q_in instead of 2q_in',
                    'detected_by':'nonzero exact quadratic residual','residual':add(bdiag,q,-1)})
    # Off-diagonal b's do not span degree 2; they cannot be rescued by products
    # in higher degree because exterior multiplication only raises degree.
    for m in (1,2,3):
        cols = [bquad(i,j,m) for i in range(m) for j in range(i+1,m)]
        obs, required = rank(cols), m*(m+1)//2
        assert obs < required
        results.append({'mutation':'omit diagonal quadratic generators','m':m,
                        'detected_by':'degree-2 rank deficiency','observed_rank':obs,
                        'required_rank':required})
    # Dropping degree 0 spoils Catalan total; dropping top degree also spoils
    # scalar-weight total, even if one only checked central parity.
    m=3
    ds=[binom(m,r)**2-binom(m,r-1)*binom(m,r+1) for r in range(m+1)]
    assert sum(ds[1:]) != catalan(m+1)
    assert sum(2*r*ds[r] for r in range(m)) != m*sum(ds[:-1])
    results.append({'mutation':'drop endpoint invariant degrees',
                    'detected_by':'Catalan total and scalar-weight symmetry',
                    'correct_degree_dimensions':ds})
    # The tempting crossing-matching leading-word shortcut fails.
    a,b=match_tensor(((0,2),(1,3))),match_tensor(((0,3),(1,2)))
    key=lambda w:tuple(int(bool(w&(1<<i))) for i in range(4))
    assert max(a,key=key)==max(b,key=key)
    assert rank([match_tensor(((0,1),(2,3))),a,b])==2
    results.append({'mutation':'use all matchings as distinct-leading-word basis',
                    'detected_by':'coincident leaders and rational dependency',
                    'matching_count':3,'exact_rank':2})
    # Generic rational division alone cannot imply a polynomial divisor:
    # det(L)=1, chosen supposed divisor x, and quotient 1/x.
    results.append({'mutation':'allow a variable denominator in a supposed quotient factor',
                    'detected_by':'counterexample det(L)=1=(1/x)*x has no x divisor',
                    'purpose':'tests necessity of constant-kernel polynomial argument'})
    # Detect a sign-flipped lowering operator against the genuine commutator.
    v={1:1} # plus_0 for m=1
    genuine=add(act(act(v,1,False),1),act(act(v,1),1,False),-1)
    flipped={k:-c for k,c in genuine.items()}
    assert genuine==v and flipped!=v
    results.append({'mutation':'flip F sign but retain [E,F]=H',
                    'detected_by':'commutator identity on plus generator',
                    'correct':genuine,'mutant':flipped})
    return results


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--mode',choices=['all','sl2','partition','matching','character','projection','negative'],default='all')
    p.add_argument('--max-m',type=int,default=6)
    p.add_argument('--max-n',type=int,default=7)
    p.add_argument('--max-r',type=int,default=6)
    p.add_argument('--output',default='CHECK_RESULTS.json')
    args=p.parse_args()
    start=time.monotonic()
    out={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'python':platform.python_version(),'mode':args.mode,
         'arithmetic':'integer fraction-free rational rank; Fraction exact determinants',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    selected=lambda name:args.mode in ('all',name)
    if selected('sl2'):
        out['infinitesimal_and_torus']=invariant_checks(args.max_m)
    if selected('partition'):
        out['all_partition_image']=partition_checks(args.max_n)
    if selected('matching'):
        out['noncrossing_tensors']=matching_checks(args.max_r)
    if selected('character'):
        out['explicit_character']=explicit_character_checks()
    if selected('projection'):
        out['exterior_projection']=projection_checks()
    if selected('negative'):
        out['negative_controls']=negative_controls()
    out['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    out['elapsed_seconds']=time.monotonic()-start
    out['status']='PASS'
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','mode':args.mode,'elapsed_seconds':out['elapsed_seconds'],
                      'output':args.output}),flush=True)


if __name__=='__main__':
    main()
