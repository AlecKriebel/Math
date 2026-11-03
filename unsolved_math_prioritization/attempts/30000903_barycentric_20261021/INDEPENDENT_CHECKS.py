from math import comb, factorial
from fractions import Fraction
from itertools import combinations_with_replacement
import hashlib, json

# Written independently for this audit; no author-supplied script is imported.
def macaulay(a, k):
    if a == 0:
        return 0
    rem, prev, ans = a, None, 0
    for j in range(k, 0, -1):
        if not rem:
            break
        lo = j
        hi = j + rem if prev is None else min(j + rem, prev - 1)
        assert comb(lo, j) <= rem
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if comb(mid, j) <= rem:
                lo = mid
            else:
                hi = mid - 1
        n = lo
        assert n >= j and (prev is None or n < prev)
        rem -= comb(n, j)
        ans += comb(n + 1, j + 1)
        prev = n
    assert rem == 0
    return ans

assert macaulay(3, 1) == 6
assert macaulay(2, 3) == 2
assert macaulay(5, 2) == 7
assert macaulay(13, 3) == 19

# All comparisons below use arbitrary-precision integers, not floats.
def check_D(a, k):
    m = macaulay(a, k)
    assert (factorial(k + 1) * m) ** k >= (factorial(k) * a) ** (k + 1), (a, k, m)

D_dense = 0
for k in range(1, 33):
    for a in range(1, 10001):
        check_D(a, k)
        D_dense += 1

D_boundary = 0
for k in range(1, 65):
    for n in sorted(set([k, k+1, k+2, 2*k, 5*k, 10*k, 100*k])):
        for a in sorted(set([comb(n,k)-1, comb(n,k), comb(n,k)+1,
                             comb(n+1,k)-2, comb(n+1,k)-1])):
            if a > 0:
                check_D(a, k)
                D_boundary += 1

# Check sufficient inequality (10) using rational arithmetic and integer powers.
# P^(1/k) <= R is equivalent to P <= R^k because R >= 0.
bound10 = 0
for k in range(2, 65):
    gamma = Fraction((k+1)*(k-1)**(k-1), k**k)
    for n in sorted(set(range(k+1, k+101)) | {100*k, 1000*k, 10000*k}):
        P = factorial(k)*comb(n,k)
        R = Fraction(n+1) - gamma*Fraction(n+1,n-k+1)
        assert R > 0 and R**k >= P, (k,n)
        bound10 += 1

# All monotone sequences from this rational grid satisfy ULC by construction.
# h_i=lambda_1...lambda_i/i!, with lambda_i nonincreasing.
grid = [Fraction(1,2), Fraction(1), Fraction(3,2), Fraction(2),
        Fraction(5,2), Fraction(3), Fraction(4), Fraction(5),
        Fraction(6), Fraction(8), Fraction(12)]
C_sequences = C_checked = C_positive_next = C_nonpositive_next = 0
for d in range(2,9):
    for asc in combinations_with_replacement(grid,d):
        lambdas = asc[::-1]
        h = [Fraction(1)]
        for i,L in enumerate(lambdas,1):
            h.append(h[-1]*L/i)
        assert all(i*h[i]**2 >= (i+1)*h[i-1]*h[i+1] for i in range(1,d))
        C_sequences += 1
        for k in range(1,d):
            g = h[k]-h[k-1]
            if g <= 0:
                continue
            nxt = h[k+1]-h[k]
            if nxt > 0:
                assert (factorial(k+1)*nxt)**k < (factorial(k)*g)**(k+1), (h,k)
                C_positive_next += 1
            else:
                C_nonpositive_next += 1
            C_checked += 1

# Exhaust all positive integer sequences h0=1, d=1..7, hi<=24 satisfying ULC.
A_sequences = A_inequalities = A_plateaus = 0

def check_A(h):
    global A_sequences, A_inequalities, A_plateaus
    d = len(h)-1
    r = 0
    while r < d and h[r+1] > h[r]:
        r += 1
    assert all(h[i+1] <= h[i] for i in range(r,d)), h
    if r == 0:
        assert h == [1,1], h
    if r < d and h[r+1] == h[r]:
        A_plateaus += 1
    g = [1] + [h[i]-h[i-1] for i in range(1,r+1)]
    for k in range(1,r):
        assert g[k+1] <= macaulay(g[k],k), (h,g,k)
        A_inequalities += 1
    A_sequences += 1

def visit(h):
    if len(h) > 1:
        check_A(h)
    if len(h) == 8:
        return
    if len(h) == 1:
        upper = 24
    else:
        i = len(h)-1
        upper = min(24, i*h[-1]**2 // ((i+1)*h[-2]))
    for nxt in range(1,upper+1):
        visit(h+[nxt])
visit([1])

result = {
    'lemma_D_dense': {'k_min':1,'k_max':32,'a_min':1,'a_max':10000,'cases':D_dense,'failures':0},
    'lemma_D_binomial_boundaries': {'k_min':1,'k_max':64,'cases':D_boundary,'failures':0},
    'inequality_10': {'k_min':2,'k_max':64,'cases':bound10,'failures':0},
    'proposition_C': {'rational_grid':[str(x) for x in grid],'dimensions':[2,8],
                      'sequences':C_sequences,'checked_positive_gk':C_checked,
                      'positive_next':C_positive_next,'nonpositive_next':C_nonpositive_next,'failures':0},
    'theorem_A': {'dimensions':[1,7],'coefficient_max':24,'sequences':A_sequences,
                  'macaulay_inequalities':A_inequalities,'plateau_sequences':A_plateaus,'failures':0},
    'arithmetic':'Python arbitrary-precision int and fractions.Fraction only',
    'source_script_sha256': hashlib.sha256(open(__file__,'rb').read()).hexdigest(),
}
print(json.dumps(result, indent=2))
