#!/usr/bin/env python3
"""Independent audit controls. No author functions are imported.

Exact controls use fractions and a first-removal dynamic program, not a
largest-first assumption. Floating-point checks are explicitly uncertified.
"""
import argparse
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import math
import random
import numpy as np
import sympy as sp

EXPECTED_MANIFEST = '2d657668c7f2b47f4429714e3e597baee441f32f58f262dc7bfb9d62dc5b4d8d'

def bind_author(author):
    manifest = (author / 'SHA256SUMS').read_bytes()
    assert hashlib.sha256(manifest).hexdigest() == EXPECTED_MANIFEST
    entries = {}
    for line in manifest.decode().splitlines():
        digest, name = line.split(maxsplit=1)
        name = name.lstrip('*')
        assert hashlib.sha256((author / name).read_bytes()).hexdigest() == digest
        entries[name] = digest
    assert len(entries) == 7
    return entries

def geometry(lengths):
    x = F(0)
    bands = []
    for k, length in enumerate(lengths):
        if k % 2 == 0:
            bands.append((x, x + length))
        x += length
    return bands

def optimal_by_first_removal(bands):
    """Maximise bottleneck over binary removal trees, exactly."""
    @lru_cache(None)
    def solve(left, right):
        if left == right:
            return math.inf
        choices = []
        for cut in range(left, right):
            gap = bands[cut + 1][0] - bands[cut][1]
            choices.append(min((bands[cut][1] - bands[left][0]) / gap,
                               (bands[right][1] - bands[cut + 1][0]) / gap,
                               solve(left, cut), solve(cut + 1, right)))
        return max(choices)
    return solve(0, len(bands) - 1)

def threshold_score(bands):
    if len(bands) == 1:
        return math.inf
    holes = [(a[1], b[0]) for a, b in zip(bands, bands[1:])]
    ratios = []
    for low, high in holes:
        width = high - low
        blockers = [(u, v) for u, v in holes if v - u >= width]
        l = max([bands[0][0]] + [v for u, v in blockers if v <= low])
        r = min([bands[-1][1]] + [u for u, v in blockers if u >= high])
        ratios.extend([(low - l) / width, (r - high) / width])
    return min(ratios)

def determinant(matrix):
    a = [list(row) for row in matrix]
    answer = F(1)
    for c in range(len(a)):
        p = next((r for r in range(c, len(a)) if a[r][c]), None)
        if p is None:
            return F(0)
        if p != c:
            a[p], a[c] = a[c], a[p]
            answer = -answer
        pivot = a[c][c]
        answer *= pivot
        for r in range(c + 1, len(a)):
            scale = a[r][c] / pivot
            for j in range(c + 1, len(a)):
                a[r][j] -= scale * a[c][j]
    return answer

def transfer_trace(word, energy, coupling):
    a,b,c,d = F(1),F(0),F(0),F(1)
    for bit in word:
        z = energy - coupling * bit
        a,b,c,d = z*a-c,z*b-d,a,b
    return a+d

def main(author):
    hashes = bind_author(author)
    exact = {}
    checked = 0
    for blocks, values in [(7, range(1,4)), (11, range(1,3))]:
        for lengths in product(values, repeat=blocks):
            bands = geometry(tuple(map(F, lengths)))
            assert optimal_by_first_removal(bands) == threshold_score(bands)
            checked += 1
    exact['new_exhaustive_finite_configurations'] = checked
    rng = random.Random(30001687)
    rational_count = 0
    for gaps in range(1, 13):
        for _ in range(30):
            lengths = [F(rng.randint(1,20),rng.randint(1,13)) for _ in range(2*gaps+1)]
            bands = geometry(lengths)
            optimal = optimal_by_first_removal(bands)
            assert optimal == threshold_score(bands)
            shift, scale = F(-7,11), F(13,7)
            assert threshold_score([(shift+scale*a,shift+scale*b) for a,b in bands]) == optimal
            assert threshold_score([(-b,-a) for a,b in reversed(bands)]) == optimal
            rational_count += 1
    exact['rational_configurations_and_affine_reflection_checks'] = rational_count
    swaps = ties = 0
    for A,g,M,h,C in product(map(F,range(1,6)),repeat=5):
        if g > h:
            continue
        old = min(A/g,(M+h+C)/g,M/h,C/h)
        new = min((A+g+M)/h,C/h,A/g,M/g)
        assert new >= old
        if g == h:
            assert old == new
            ties += 1
        swaps += 1
    exact['adjacent_exchange_checks'] = swaps
    exact['equal_length_exchange_checks'] = ties
    x,y,z = sp.symbols('x y z')
    invariant = lambda a,b,c: a*a+b*b+c*c-2*a*b*c
    assert sp.expand(invariant(2*x*y-z,x,y)-invariant(x,y,z)) == 0
    exact['symbolic_trace_invariant_identity'] = True
    fib = [1,1]
    for _ in range(12):
        fib.append(sum(fib[-2:]))
    floquet = traces = 0
    for k, energy, coupling in product([3,4,5],map(F,[-2,-1,0,1,2]),[F(1,3),F(1,2),F(1),F(3)]):
        q,p = fib[k],fib[k-1]
        word = [((n+1)*p)//q-(n*p)//q for n in range(1,q+1)]
        tr = transfer_trace(word,energy,coupling)
        for sign in [-1,1]:
            m = [[F(0) for _ in range(q)] for _ in range(q)]
            for i in range(q):
                m[i][i] = energy-coupling*word[i]
            for i in range(q-1):
                m[i][i+1] = m[i+1][i] = F(-1)
            m[0][-1] = m[-1][0] = F(-sign)
            assert determinant(m) == tr-2*sign
            floquet += 1
        xs = [F(1),energy/2,(energy-coupling)/2]
        for _ in range(k-1):
            xs.append(2*xs[-1]*xs[-2]-xs[-3])
        assert tr == 2*xs[k+1]
        traces += 1
    exact['exact_floquet_characteristic_identities'] = floquet
    exact['rational_word_trace_recursion_matches'] = traces
    # The nonempty condition is necessary: the empty-gap score is constant infinity.
    assert optimal_by_first_removal([(F(0),F(1))]) == math.inf
    exact['empty_gap_strict_decrease_counterexample'] = True
    # A family of single-gap examples has g_n=t/(1+n^2*t^2),
    # Phi_n=1/t+n^2*t-1/2, whose derivative becomes positive at 2/n.
    for n in range(3,103):
        t = F(2,n)
        assert -1/t**2+n*n > 0
    exact['no_uniform_delta_examples'] = 100
    source = json.loads((author/'control_results.json').read_text())
    differences = []
    checked_free = []
    def merge(intervals):
        result = []
        for low,high in sorted(intervals):
            if result and low <= result[-1][1]+1e-12:
                result[-1][1] = max(high,result[-1][1])
            else:
                result.append([low,high])
        return result
    def bands(k, coupling):
        q,p = fib[k],fib[k-1]
        word = [((n+1)*p)//q-(n*p)//q for n in range(1,q+1)]
        endpoints=[]
        for sign in [-1,1]:
            matrix=np.zeros((q,q))
            for i in range(q):
                matrix[i,i] = coupling*word[i]
                if i+1<q:
                    matrix[i,i+1] = matrix[i+1,i] = 1
            matrix[0,-1]=matrix[-1,0]=sign
            endpoints.extend(np.linalg.eigvalsh(matrix))
        endpoints.sort()
        return list(zip(endpoints[::2],endpoints[1::2]))
    for k in range(3,12):
        result=merge(bands(k,0))
        assert len(result)==1 and max(abs(result[0][0]+2),abs(result[0][1]-2))<1e-12
        checked_free.append(fib[k])
    new_grid=[]
    for row in source['grid']:
        k,lam=row['k'],row['lambda']
        intervals=merge(bands(k,lam)+bands(k+1,lam))
        score=float(threshold_score(intervals))
        assert len(intervals)==row['bands']
        diff=abs(score-row['score'])
        assert diff < 1e-6*max(1,abs(row['score']))
        differences.append(diff)
        new_grid.append({'k':k,'lambda':lam,'bands':len(intervals),'score':score,'absolute_difference':diff})
    for k in [6,8,10,11]:
        scores=[r['score'] for r in new_grid if r['k']==k]
        assert all(a>=b for a,b in zip(scores,scores[1:]))
    return {'author_manifest_sha256':EXPECTED_MANIFEST,'author_file_hashes':hashes,
            'exact':exact,'floating_point':{'method':'NumPy eigvalsh, independently constructed matrices; no interval certification',
            'free_periods':checked_free,'spectral_cases':len(new_grid),'max_absolute_score_difference':max(differences),
            'sampled_increases':0,'grid':new_grid},
            'infinite_spectrum_certified':False,'originals_unchanged':bind_author(author)==hashes}

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--author',type=Path,default=Path(__file__).resolve().parent.parent/'author')
    p.add_argument('--output',type=Path,default=Path(__file__).with_name('independent_results.json'))
    args=p.parse_args()
    result=main(args.author)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='floating_point'},indent=2))
    print('Floating-point cases:',result['floating_point']['spectral_cases'])
    print('Maximum absolute score difference:',result['floating_point']['max_absolute_score_difference'])
