"""Fresh finite adversarial controls; no theorem/priority certificate.

Distinct checks: nonabelian S3 free-product multiplication; arbitrary irregular
graph generalized min-max; fixed-parameter boundary degeneration.
No published code or prior verdicts imported. Explicit checks survive -O.
"""
from itertools import permutations, product
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import numpy as np
from scipy.linalg import eigh

def need(b, msg):
    if not b:
        raise RuntimeError(msg)

cnt = Counter()
identity = (0, 1, 2)
perms = tuple(permutations(range(3)))
alphabet = tuple((0, p) for p in perms if p != identity) + ((1, 1), (2, 1), (2, 2))

def multiply(a, b):
    i, x = a
    j, y = b
    need(i == j, 'factor multiplication domains')
    if i == 0:
        z = tuple(x[y[k]] for k in range(3))
        return None if z == identity else (i, z)
    z = (x + y) % (2 if i == 1 else 3)
    return (i, z) if z else None

def invletter(a):
    i, x = a
    if i == 0:
        return i, tuple(x.index(k) for k in range(3))
    return i, (-x) % (2 if i == 1 else 3)

def inverse(w):
    return tuple(invletter(a) for a in reversed(w))

def normal(w):
    stack = []
    for a in w:
        if stack and stack[-1][0] == a[0]:
            a = multiply(stack.pop(), a)
        if a is not None:
            stack.append(a)
    return tuple(stack)

def words(t, pre=()):
    if not t:
        yield pre
    else:
        for a in alphabet:
            if not pre or a[0] != pre[-1][0]:
                yield from words(t-1, pre+(a,))

fixed = {}
for t in range(1, 6):
    f = 0
    for w in words(t):
        need(normal(w) == w and normal(w+inverse(w)) == (), 'nonabelian normal/inverse')
        if w == inverse(w):
            f += 1
            need(t % 2 and w[t//2] == invletter(w[t//2]), 'palindrome characterization')
        cnt['nonabelian_normal_words'] += 1
    fixed[t] = f
reps = {i: next(a for a in alphabet if a[0] == i) for i in range(3)}
for length in range(4, 31):
    for a, b in product(alphabet, repeat=2):
        c = next(i for i in range(3) if i not in (a[0], b[0]))
        d, e = [i for i in range(3) if i != c]
        pattern = ((c, d, e, c)+(d, c)*((length-5)//2)) if length % 2 else tuple(c if j % 2 == 0 else d for j in range(length-1))
        v = tuple(reps[i] for i in pattern)
        x, y = (a,)+v, (invletter(b),)+v
        need(len(x) == length and normal(x) == x and normal(y) == y, 'suffix lengths/reduction')
        need(x != inverse(x) and y != inverse(y), 'suffix deletion avoidance')
        need(normal(x+inverse(y)) == normal((a,b)), 'noncommutative common suffix identity')
        cnt['nonabelian_suffix_pairs'] += 1
for a,b,c in product(alphabet, repeat=3):
    need(normal((c,a,b,invletter(c))) == normal(normal((c,a))+normal((b,invletter(c)))), 'K conjugation decomposition')
    cnt['nonabelian_normality_identities'] += 1
aa, bb = (0, (1,0,2)), (0, (0,2,1))
need(multiply(aa,bb) != multiply(bb,aa), 'noncommuting control actually noncommuting')
negative = ['commutative factor multiplication falsified']

rng = np.random.default_rng(23390181)
worst_margin = float('inf')
max_residual = 0.0
for n in range(3, 20):
    for trial in range(30):
        # Every edge positive, so connectivity is independent of eigenvalue tests.
        w = np.exp(rng.uniform(-5,5,size=(n,n)))
        w = np.triu(w,1); w += w.T
        d = w.sum(axis=1); lap = np.diag(d)-w
        dbar = np.exp(rng.uniform(-4,4,size=n))
        # Exact algebraic basis of g^T Dbar 1=0; unlike D-centering.
        b = np.vstack((np.eye(n-1), -dbar[:-1]/dbar[-1]))
        need(np.linalg.norm(dbar@b) < 1e-11, 'Dbar centered basis')
        mu = eigh(b.T@lap@b, b.T@(dbar[:,None]*b), eigvals_only=True)[0]
        ev = eigh(lap,np.diag(d),eigvals_only=True)
        need(abs(ev[0])<1e-10, 'constant nullspace')
        gap = ev[1]
        upper_ratio = max(d/dbar)
        bound = mu/upper_ratio
        margin = gap-bound
        need(margin >= -1e-9, 'generalized minmax lower bound fails')
        need(np.linalg.norm(d@b)>1e-4, 'centering mismatch negative control missing')
        normlap = lap/np.sqrt(d[:,None]*d[None,:])
        common = np.sqrt(d)
        max_residual=max(max_residual,float(np.linalg.norm(normlap@common)))
        need(np.linalg.eigvalsh(normlap)[0] < 1e-10, 'unrestricted expectation minimum zero')
        worst_margin=min(worst_margin,margin)
        cnt['irregular_graph_minmax_trials'] += 1
negative += ['Dbar-centered vectors are not generally D-centered',
             'unrestricted normalized Laplacian has zero minimum; Chernoff needs complement']

boundary = []
with localcontext() as ctx:
    ctx.prec=70
    for m in (1,10,1000,10**12,10**30):
        s=(Decimal(1)+8*Decimal(m)).sqrt()
        rho=(s-1)/(s+1) if m>=1 else None
        margin=(1-rho)/4
        boundary.append({'part_sizes':[1,1,m],'rho':str(rho),'gamma_minus_half':str(margin)})
    need(Decimal(boundary[-1]['gamma_minus_half'])<Decimal('1e-14'), 'growing alphabets degeneration')
for n in range(3,30,2):
    a=np.array([[0,1],[1,0]],dtype=object)
    need(np.trace(np.linalg.matrix_power(a,n))==0,'two factor odd universe')
    cnt['two_factor_odd_lengths']+=1
negative += ['growing alphabet spectral margin can approach zero',
             'two-factor odd-length cyclic universe is empty']
for ell in range(3,301):
    need(Fraction(ell,3)-(ell+2)//3 <= 0, 'critical density exponent boundary')
    cnt['critical_density_exponents'] += 1
negative += ['density exponent is not strictly positive at d=1/3']
print(json.dumps({'status':'PASS','counts':dict(cnt),'inverse_fixed_nonabelian_counts':fixed,
                  'negative_controls':negative,'minmax_min_margin':worst_margin,
                  'max_common_kernel_residual':max_residual,'growing_parameter_boundary':boundary,
                  'scope':'Finite exact algebra and floating minmax diagnostics; not proof of limiting theorem.'},indent=2))
