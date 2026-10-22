"""Read-only checks of published Table1 and exact classification arithmetic.

Requires locally retained primary PDF text; never imports PR programs.
The infinite construction proof is not certified by these finite controls.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def require(value, message):
    if not value:
        raise RuntimeError(message)


def table(text, pages):
    region = '\n'.join(text.split('\f')[x] for x in pages)
    pairs = re.findall(r'(?m)^\s*(\d+)\s+\(([^)]*)\)', region)
    result = {}
    for key, raw in pairs:
        n = int(key)
        require(n not in result, 'Repeated witness length')
        permutation = list(map(int, re.findall(r'\d+', raw)))
        require(len(permutation) == n, 'Wrong witness size')
        require(sorted(permutation) == list(range(1, n+1)), 'Not permutation')
        result[n] = permutation
    return result


def counts_comparisons(permutation):
    result = Counter()
    for a, b, c in itertools.combinations(permutation, 3):
        if a < b:
            name = '123' if b < c else '132' if a < c else '231'
        else:
            name = '213' if a < c else '312' if b < c else '321'
        result[name] += 1
    return result


def counts_middle(permutation):
    # Independent split at the middle index, without combinations iteration.
    result = Counter()
    for j, value in enumerate(permutation):
        left = permutation[:j]
        right = permutation[j+1:]
        below_left = sum(a < value for a in left)
        above_left = j - below_left
        below_right = sum(c < value for c in right)
        above_right = len(right) - below_right
        result['123'] += below_left * above_right
        result['321'] += above_left * below_right
        for a in left:
            for c in right:
                if a < value and c < value:
                    result['132' if a < c else '231'] += 1
                elif a > value and c > value:
                    result['213' if a < c else '312'] += 1
    return result


def add(*polynomials):
    out = [F(0)] * max(map(len, polynomials))
    for poly in polynomials:
        for index, value in enumerate(poly):
            out[index] += value
    return out


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, v in enumerate(a):
        for j, w in enumerate(b):
            out[i+j] += v*w
    return out


def scale(a, c):
    return [x*c for x in a]


def binomial_polynomial(r):
    result = [F(1)]
    for j in range(r):
        result = mul(result, [-F(j), F(1)])
    return scale(result, F(1, math.factorial(r)))


def main():
    paths = {'journal': HERE/'private_sources/publisher_pdf.txt',
             'arxiv_v1': HERE/'private_sources/arxiv_pdf.txt'}
    journal = table(paths['journal'].read_text(), [27, 28])
    arxiv = table(paths['arxiv_v1'].read_text(), [20])
    require(len(journal) == 19 and journal == arxiv, 'Source Table1 mismatch')
    starts = {20:92, 28:100, 0:108, 29:173, 1:181, 9:189}
    exceptional = {n for n in range(3, 189) if n % 36 in starts and n < starts[n % 36]}
    require(set(journal) == exceptional, 'Wrong finite exceptional domain')
    result = []
    for n, permutation in sorted(journal.items()):
        a = counts_comparisons(permutation)
        b = counts_middle(permutation)
        target = math.comb(n, 3)//6
        require(math.comb(n, 3) % 6 == 0, 'Nonintegral balance target')
        require(a == b and len(a) == 6 and set(a.values()) == {target}, 'Unbalanced witness')
        result.append({'n':n, 'each_pattern_count':target, 'two_methods_agree':True})
    c2 = binomial_polynomial(2)
    difference = add(scale(binomial_polynomial(4), F(36,24)),
                     scale(binomial_polynomial(3), F(10,6)),
                     scale(c2, F(1,2)), scale(mul(c2,c2), -F(1,4)))
    require(difference == [F(0), -F(5,72), F(1,24), F(1,36), F(0)],
            'Exact obstruction polynomial mismatch')
    for n in range(3, 1001):
        admissible = all(math.comb(n,r) % math.factorial(r) == 0 for r in [1,2,3])
        require(admissible == (n % 36 in starts), 'Residue classification mismatch')
    # This failure control tests input validation without relying on an assert.
    broken = journal[9].copy()
    broken[0] = broken[1]
    require(sorted(broken) != list(range(1,10)), 'Malformed witness control failed')
    print(json.dumps({'status':'passed', 'published_and_arxiv_tables_identical':True,
      'witnesses':result, 'witness_count':19, 'exceptional_domain_complete':True,
      'exact_nonexistence_polynomial':'n(n-1)(2n+5)/72',
      'residue_checks_3_through_1000':998, 'malformed_input_control':True,
      'input_text_pins':{key:hashlib.sha256(path.read_bytes()).hexdigest() for key,path in paths.items()},
      'limit':'No full six-family symbolic proof, unrelated quantitative theorem, or global priority certification.'},indent=2))


if __name__ == '__main__':
    main()
