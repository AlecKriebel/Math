#!/usr/bin/env python3
"""Independent exact controls. The geometric proof is prose, not finite enumeration."""
from fractions import Fraction
import hashlib
import json

INVERSE = dict(zip('aAbB', 'AaBb'))

def need(ok, why):
    if not ok:
        raise ValueError(why)

def normal(word):
    stack = []
    for ch in word:
        need(ch in INVERSE, 'bad letter')
        if stack and stack[-1] == INVERSE[ch]:
            stack.pop()
        else:
            stack.append(ch)
    return ''.join(stack)

def length(word, b_weight):
    return sum(b_weight if c.lower() == 'b' else 1 for c in normal(word))

def initial(word, distance, b_weight):
    out = ''
    for c in word:
        w = b_weight if c.lower() == 'b' else 1
        if distance < w:
            return out, c if distance else '', Fraction(distance, w)
        distance -= w
        out += c
    need(distance == 0, 'outside segment')
    return out, '', Fraction(0)

def main():
    counts = {'general_weight_midpoints': 0, 'completed_square': 0,
              'integer_minimum': 0, 'off_segment_vertices': 0,
              'enumerated_minima': 0, 'boundary_endpoint_estimate': 0}
    minima = []
    for r in range(2, 7):
        for n in range(1, 31):
            word = 'a' * (2*r*n) + 'b' * (2*r*n)
            m = (r-1)*n
            need(initial(word, length(word, 1)//2, 1) == ('a'*(2*r*n), '', 0), 'unit midpoint')
            need(initial(word, Fraction(length(word, r), 2), r) == ('a'*(2*r*n)+'b'*m, '', 0), 'weighted midpoint')
            counts['general_weight_midpoints'] += 2
            centre = Fraction(r*r*m, 1+r*r)
            constant = Fraction(r*r*m*m, 1+r*r)
            observed = []
            for k in range(m+1):
                v = k*k + r*r*(m-k)**2
                need(v == constant + (1+r*r)*(k-centre)**2, 'square completion')
                need(2*v >= m*m, 'coarse lower bound')
                counts['completed_square'] += 2
                observed.append(v)
            k = centre.numerator // centre.denominator
            near = min(abs(centre-k), abs(centre-(k+1)))
            need(min(observed) == constant+(1+r*r)*near*near, 'rounded minimum')
            counts['integer_minimum'] += 1
            minima.append([r,n,min(observed)])
    # Exhaust all reduced words of length at most six independently of path gates.
    words, frontier = [''], ['']
    for _ in range(6):
        frontier = [w+c for w in frontier for c in 'aAbB' if not w or c != INVERSE[w[-1]]]
        words.extend(frontier)
    need(len(words) == 1457, 'enumeration count')
    for n in range(1, 8):
        expected = min(k*k+4*(n-k)**2 for k in range(n+1))
        values = []
        for word in words:
            v = length(word, 1)**2+length('B'*n+word, 2)**2
            need(v >= expected, 'off-segment shorter')
            values.append(v)
            counts['off_segment_vertices'] += 1
        need(min(values) == expected, 'minimizer not represented')
        counts['enumerated_minima'] += 1
    # Exact scalar algebra in the surjectivity estimate, not a CAT(0) geometry test.
    for R in range(0, 6):
        for n in range(max(R+1, 2), 41):
            for delta in range(-R, R+1):
                ell = n+delta
                for u in (Fraction(1, 3), Fraction(min(n,ell), 2)):
                    need(abs(u*Fraction(ell,n)-u) <= Fraction(R,n)*u,
                         'normalized segment radial error')
                    counts['boundary_endpoint_estimate'] += 1
    result = {'problem_id':'6200022', 'status':'pass', 'counts':counts,
              'total_checks':sum(counts.values()), 'reduced_words':len(words),
              'general_weight_range':[2,6], 'general_midpoint_n_range':[1,30],
              'minimum_digest':hashlib.sha256(json.dumps(minima,sort_keys=True).encode()).hexdigest(),
              'scope':'Exact finite auxiliary arithmetic only; AUDIT.md contains conventional infinite geometric arguments.'}
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
