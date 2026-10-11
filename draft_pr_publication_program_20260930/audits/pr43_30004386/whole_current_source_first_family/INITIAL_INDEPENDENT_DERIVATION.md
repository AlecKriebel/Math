# Initial independent derivation and exposure seal

This review starts on 2026-10-03 UTC. Before writing this note I received the
parent's task, including its description of the frozen candidate, its proposed
mathematical interpretation, earlier route verdicts, and its warning about
historical execution metadata. I listed file names and read the repository
AGENTS.md. I have not yet read any candidate or family mathematical source.
This is therefore an independent reconstruction conditional on the disclosed
target, not a claim of blind discovery or mathematical priority.

The target is a source-audit acceptance hypothesis: the exact PR43 snapshot is
faithfully archived, current evidence supports an already-published full weak
large-deviation theorem, and no new theorem or project-level full solution is
claimed. The acceptance gap is whole-source, dependency, capture and claim
verification; future ROOT approval is separate from this family's opinion.

For the mathematical check, let
W={a_1 >= a_2 >= ... >= 0: sum a_j^2 <= 1}, with coordinate topology.
It is closed in [0,1]^N by each finite ordering and norm constraint, hence
compact. Its elements obey a_j <= 1/sqrt(j). Let U_j be independent Uniform[-1,1]
and G standard normal. Define kappa(a) as the law of
sum a_j U_j + sqrt((1-||a||_2^2)/3) G. The sum exists in L2 by the exact variance
Var(U_j)=1/3. Its characteristic function is
exp[-(1-||a||_2^2)t^2/6] product_j sinc(a_j t).

Continuity cannot be deduced from continuity of the squared norm in coordinate
topology: that norm is not continuous there. Instead, split a finite head from
the tail. For fixed t, make |a_j t| small uniformly for j beyond M. The identity
log sinc(x)=-x^2/6+O(x^4) there and
sum_{j>M} a_j^4 <= (M+1)^-1 sum_{j>M} a_j^2 <= (M+1)^-1
show that the tail plus missing-variance Gaussian has characteristic function
exp[-t^2(1-sum_{j<=M}a_j^2)/6] with uniformly vanishing error.
Finite-head continuity, then M -> infinity and Levy continuity, establish
continuity of kappa. A quotient across sinc zeros is unnecessary and unsafe.

The whole deterministic limit set is kappa(W). Necessity follows by compactness
of sorted absolute unit vectors and continuity. For sufficiency, for every N
retain k(N)=floor(sqrt(N)) target coordinates (or fewer if N is tiny), then fill
the remaining N-k coordinates equally with sqrt((1-sum_{j<=k}a_j^2)/(N-k)).
Sorting these N nonnegative numbers gives a unit vector. The filler tends to
zero; every fixed positive target coordinate eventually outranks it, and zero
target coordinates tend to zero. Thus the sorted vector converges coordinatewise
to a. This covers every sufficiently large N and norm-one boundary points,
not merely a chosen subsequence or points of norm less than one.

For uniqueness, the characteristic functions are entire: the sinc product
converges uniformly on each compact subset of the complex plane by sum a_j^2.
When a_1>0, its smallest positive zero is pi/a_1, with multiplicity exactly the
number of occurrences of a_1. The Gaussian has no zeros and smaller coordinates
have first zeros later. Remove that finite multiplicity and repeat. This
recovers every nonzero coordinate. If no zeros remain, no positive coordinates
remain. The Gaussian factor then recovers the remaining variance. This is a
genuine injectivity mechanism, not an assumption hidden inside contraction.

For a uniform sphere vector in dimension N, its first m coordinates have density
C_{N,m}(1-||x||^2)^((N-m-2)/2) on the open unit ball; C has zero logarithmic rate
for fixed m. On a fixed ordered coordinate neighborhood, a union over coordinate
indices and signs supplies at most 2^m (N)_m possibilities. An exact chamber
count also has an m! factor if the labels are unordered, but the difference has
zero speed-N logarithmic rate. The upper bound gives local rate
J(a)=-1/2 log(1-||a||^2) when ||a||<1, and +infinity at norm one.

For the lower bound first perturb the finite constrained head to be strictly
decreasing and positive, while preserving norm <1 and staying in the target
neighborhood. Pin those coordinates inside a small positive wedge; conditional
on them, the remaining uniform sphere coordinates have a maximum tending to
zero in probability (a union bound on one-coordinate spherical tails suffices).
Consequently the designated head really is the ordered head with probability
tending to one. Then shrink the wedge and the perturbation. Ties and zero
constraints are handled by this perturbation; norm-one lower bounds are vacuous
because -J=-infinity. Compactness of W upgrades local bounds through finite
covers to the full LDP. This avoids relying on any unrestricted assertion that
a full LDP implies exponential tightness.

Contraction by continuous kappa gives a full speed-N LDP in P(R) with the weak
topology. Injectivity identifies its rate on kappa(W); outside this compact
image it is infinity. The rate is good because J is lower semicontinuous on
compact W (its sublevel sets bound the squared norm away from one).

These derivations are checks on the stated prior-result mechanism. They do not
establish novelty, satisfy the overall discovery goal, or replace source reads.
Estimated acceptance-review completion: 10%; estimated new mathematical
discovery completion for this audit: 0%.
