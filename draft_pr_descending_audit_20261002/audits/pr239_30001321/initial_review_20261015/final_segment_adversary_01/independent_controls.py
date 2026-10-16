"""Independent exact controls for final-segment localization, not a proof.

Uses only Python standard library. Geometry is evaluated exactly in
Q(sqrt(2)), so irrational tilts are not floating-point approximations.
No imports from the submitted implementation.
"""
from fractions import Fraction as F
from collections import Counter, defaultdict
from itertools import product, combinations
from math import comb
import json

counts = Counter()
observations = Counter()

def ck(condition, family):
    assert condition, family
    counts[family] += 1

class S2:
    """Exact a+b*sqrt(2), supporting ordering and rational scaling."""
    def __init__(self, a=0, b=0): self.a, self.b = F(a), F(b)
    def __add__(self, other):
        other = as2(other)
        return S2(self.a + other.a, self.b + other.b)
    __radd__ = __add__
    def __neg__(self): return S2(-self.a, -self.b)
    def __sub__(self, other): return self + (-as2(other))
    def __rsub__(self, other): return as2(other) - self
    def __mul__(self, other):
        other = as2(other)
        return S2(self.a*other.a + 2*self.b*other.b,
                  self.a*other.b + self.b*other.a)
    __rmul__ = __mul__
    def __truediv__(self, other):
        other = as2(other)
        den = other.a*other.a - 2*other.b*other.b
        return self * S2(other.a/den, -other.b/den)
    def sign(self):
        a,b = self.a,self.b
        if not b: return (a > 0) - (a < 0)
        if not a: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        d = a*a - 2*b*b
        return ((d > 0) - (d < 0)) * (1 if a > 0 else -1)
    def __lt__(self, other): return (self - other).sign() < 0
    def __le__(self, other): return (self - other).sign() <= 0
    def __gt__(self, other): return (self - other).sign() > 0
    def __ge__(self, other): return (self - other).sign() >= 0
    def __eq__(self, other): return (self - other).sign() == 0
    def floor(self):
        # All control values are small; exact comparisons are intentional.
        z = self.a.numerator // self.a.denominator
        while self < z: z -= 1
        while z+1 <= self: z += 1
        return z

def as2(x): return x if isinstance(x, S2) else S2(x)

def normdiff(a,b):
    return sum((abs(a.get(x,F(0))-b.get(x,F(0)))
                for x in a.keys() | b.keys()), F(0))

def kernel(env, n, start, R=None, tilt=S2(0), endpoint_only=False):
    mu = {start:F(1)}
    for t in range(n):
        nxt = defaultdict(F)
        for y,w in mu.items():
            for z,p in [(y+1,env[t,y]),(y-1,1-env[t,y])]:
                centered = S2(z-start)-tilt*(t+1)
                check = R is not None and (not endpoint_only or t+1 == n)
                if not check or -R <= centered <= R:
                    nxt[z] += w*p
        mu = {x:p for x,p in nxt.items() if p}
    return mu

def mix(kernels, old):
    out = defaultdict(F)
    for x,w in old.items():
        for y,p in kernels[x].items(): out[y] += w*p
    return dict(out)

def coarse(mu, M, shift=S2(0)):
    out = defaultdict(F)
    for x,p in mu.items(): out[((S2(x)-shift)/M).floor()] += p
    return dict(out)

# Exact algebra sanity and half-open boundary contacts.
root2 = S2(0,1)
ck(root2*root2 == 2, 'exact_irrational_algebra')
ck(1 < root2 < F(3,2), 'exact_irrational_algebra')
ck((root2-1).floor() == 0 and (-root2).floor() == -2,
   'exact_irrational_floor')
for W in [1,2,3]:
    for t in range(4):
        for y in range(-8,9):
            k = ((S2(y)-S2(F(1,2))*t)/W).floor()
            ck(k*W <= S2(y)-S2(F(1,2))*t < (k+1)*W,
               'half_open_boundary_unique_membership')

# Fresh-strip controls. Enumerate every vertex value in the changed strip,
# keeping an interior-valued environment outside it. Compare all resulting
# outputs pairwise; p=0,1 here stress the deterministic analytic sensitivity
# statement on its closed-domain extension, not the theorem's assumptions.
old = {-2:F(1,7), 0:F(2,7), 2:F(4,7)}
n = 3
sites = sorted({(t,y) for t in range(n) for x in old
                for y in range(x-t,x+t+1,2)})
for tilt in [S2(0),S2(F(1,2)),root2-1,1-root2]:
    for R in [1,2,3]:
        strip = {(t,y):((S2(y)-tilt*t)/R).floor() for t,y in sites}
        keys = sorted(set(strip.values()))
        weights = {k:sum(w for x,w in old.items()
                         if k*R-R-1 <= x <= (k+1)*R+R+1)
                   for k in keys}
        ck(sum(weights.values()) <= 6, 'irrational_strip_weight_sum')
        ck(sum(w*w for w in weights.values()) <= 6*max(weights.values()),
           'irrational_strip_square_sum')
        base = {site:[F(1,1000000),F(4,5),F(1,5),F(999999,1000000)][i%4]
                for i,site in enumerate(sites)}
        originals = {x:kernel(base,n,x,R,tilt) for x in old}
        for k in keys:
            changed_sites = [s for s in sites if strip[s] == k]
            outputs = []
            losses = set()
            for bits in product([F(0),F(1)], repeat=len(changed_sites)):
                env = dict(base)
                env.update(zip(changed_sites,bits))
                kernels = {x:kernel(env,n,x,R,tilt) for x in old}
                for x in old:
                    if not k*R-R-1 <= x <= (k+1)*R+R+1:
                        ck(kernels[x] == originals[x],
                           'arbitrary_strip_change_outside_influence_invariant')
                killed = mix(kernels,old)
                full = mix({x:kernel(env,n,x) for x in old},old)
                loss = 1-sum(killed.values())
                losses.add(loss)
                ck(all(p <= full.get(y,F(0)) for y,p in killed.items()),
                   'arbitrary_strip_subkernel_domination')
                ck(normdiff(full,killed) == loss,
                   'arbitrary_strip_restoration_exact_mass')
                for M,shift in [(F(3,2),S2(F(1,3))),
                                (F(7,3),root2/3),
                                (F(1,2),S2(0))]:
                    ck(normdiff(coarse(full,M,shift),coarse(killed,M,shift)) == loss,
                       'real_and_irrational_alignment_restoration')
                outputs.append(killed)
            for left,right in combinations(outputs,2):
                ck(normdiff(left,right) <= 2*weights[k],
                   'all_vertex_pairs_single_strip_sensitivity')
            if len(losses) > 1:
                observations['changed_strip_changes_killing_mass_witness'] += 1

ck(observations['changed_strip_changes_killing_mass_witness'] > 0,
   'changing_one_strip_really_can_change_killing_sets')

# A genuine negative control: endpoint-only localization lets a path leave
# its tube, use a distant strip, and return. The all-times killing in the
# candidate removes this dependence.
n = 8
sites8 = {(t,y) for t in range(n) for y in range(-t,t+1,2)}
env = {s:F(0) for s in sites8}
# Deterministic initial path 0,1,2,3,4,3,2,1,0.
for t,y in enumerate([0,1,2,3,4,3,2,1]): env[t,y] = F(t < 4)
altered = dict(env)
# Change only strip [4,5); x=0 lies outside enlarged J_4=[2,7].
altered[4,4] = F(1)
ck(kernel(env,n,0,1,S2(0)) == kernel(altered,n,0,1,S2(0)) == {},
   'all_times_killing_blocks_excursion')
ck(kernel(env,n,0,1,S2(0),True) != kernel(altered,n,0,1,S2(0),True),
   'endpoint_only_killing_negative_control')

# Parity negative control: a homogeneous simple symmetric walk started at
# opposite parities has disjoint endpoint supports forever, hence L1 = 2.
for n in range(1,21):
    a = {2*j-n:F(comb(n,j),2**n) for j in range(n+1)}
    b = {x+1:p for x,p in a.items()}
    ck(normdiff(a,b) == 2, 'opposite_parity_kernel_l1_equals_two')

# Replacement with sparse old weights, clipped boundary cells, null cells,
# and genuine one-site H=1 cells on the unreachable parity.
for m in range(0,7):
    for q in [F(1,1000000),F(1,3),F(1,2),F(999999,1000000)]:
        alpha = {2*j-m:F(comb(m,j))*q**j*(1-q)**(m-j)
                 for j in range(m+1)}
        old = {min(alpha):F(1,3),max(alpha):F(2,3)} if m else {0:F(1)}
        for H in range(1,10):
            for shift in range(H):
                ca,cm = coarse(alpha,H,S2(shift)),coarse(old,H,S2(shift))
                prime = {x:cm.get(((S2(x)-shift)/H).floor(),F(0))*p /
                         ca[((S2(x)-shift)/H).floor()] for x,p in alpha.items()}
                ck(sum(prime.values()) == 1, 'sparse_replacement_preserves_mass')
                ck(normdiff(prime,alpha) == normdiff(cm,ca),
                   'sparse_clipped_replacement_exact_identity')
                for cell in range(-m-12,m+13):
                    if ca.get(cell,F(0)) == 0:
                        ck(cm.get(cell,F(0)) == 0,
                           'null_annealed_cells_have_zero_reachable_old_mass')

# Deliberate domain violation: mass placed outside the annealed reachable
# support cannot be normalized by its null conditional cell law.
ck(coarse({10:F(1)},1).get(10) == 1 and
   coarse({0:F(1)},1).get(10,F(0)) == 0,
   'unsupported_old_mass_negative_control')

# Quantitative near-arrow warning. For p in {eps,1-eps}, every environment
# has an arrow path whose quenched mass is >=1-n*eps. The coarse L1 error
# is thus >=2*(1-n*eps-max_cell_annealed_mass). This can stay near 2 if eps
# is allowed to depend on n, which the candidate explicitly excludes.
for n in [16,32,64]:
    alpha = {2*j-n:F(comb(n,j),2**n) for j in range(n+1)}
    eps = F(1,n**3)
    for M in [2,3,4]:
        for shift in range(M):
            peak = max(coarse(alpha,M,S2(shift)).values())
            ck(2*(1-n*eps-peak) > 1,
               'varying_near_arrow_law_cannot_have_uniform_threshold')

print(json.dumps({
    'status':'PASS', 'exact_assertions':sum(counts.values()),
    'families':dict(sorted(counts.items())),
    'observations':dict(sorted(observations.items())),
    'scope':'Exact independent finite controls; does not establish an asymptotic theorem.',
    'new_features':['Exact Q(sqrt(2)) irrational moving strips and real alignments',
                    'Every changed-strip vertex and pairwise sensitivity',
                    'Changing killing sets and near-arrow interior values',
                    'Endpoint-only killing and opposite-parity negative controls',
                    'Sparse old weights, support-clipped and null parity cells']
},indent=2,sort_keys=True))
