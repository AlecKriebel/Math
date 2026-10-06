# PR16: independent probability and combinatorial audit

Audit date: 2026-10-01 UTC. Frozen target supplied by the parent audit:
`3aa15b4ab70ddddf556c84cbba7d6528910dfceb`, problem 30000439 / OWR-1194-009.
The inspected candidate has SHA-256
`23705f2868d66526eeded2cf644d36138acd8223af13d5202ee22da415753502`.

**Independent verdict: PASS for this family.** No counterexample or missing
probability/combinatorial step was found. The strongest verified result is a
positive-probability finite construction of an edge-disjoint family of triangles
with more than n retained triangles, whose generated complex admits no linear
embedding in R^4, including nongeneric embeddings. This audit does not establish
PL inflation, novelty, the complete exact-dimension theorem, or publication
readiness. Those remain separate gates.

## Claim under test and imported boundaries

The tested proposition is that, for n=2^256, selecting each triple independently
with p=2^-384 has positive probability of simultaneously satisfying:

1. For every labeled general-position placement of [n] in R^4 and every deletion
   set F of at most m=2^320 triples, at least one disjoint crossing triangle pair
   survives in the selected family outside F.
2. At most m pairs of selected triangles share an edge.
3. The selected triangle count is at least half its expectation, and after at
   most m deletions more than n triangles remain.

The proposition uses the affine seven-point balanced-Radon theorem, a finite
order-type bound, and Janson's lower-tail theorem. The audit verifies their
applicability and conventions, rather than claiming new proofs of those imported
theorems. The balanced-Radon input is an even-dimensional R^4 statement; no
withdrawn odd-dimensional threshold statement is used.

[Newman's current paper](https://arxiv.org/pdf/2212.09576), Section 4,
Theorem 9 and Corollary 10, supplies the seven-point input; Theorem 11 and Lemma
12 state the relevant order-type reduction. The original
[Goodman–Pollack paper](https://doi.org/10.1007/BF02187696), Theorem 1, printed
p. 220, directly bounds labeled simple order types by n^{d(d+1)n}. Its definition
requires n>d and no hyperplane containing more than d points. These conditions
hold here with d=4. This is a finite bound, not a bound with an unspecified
asymptotic constant.

[Frieze–Karoński's author-hosted book](https://www.math.cmu.edu/~af1p/BOOK.pdf),
Section 34.6, Theorem 34.13 and (34.34)–(34.36), applies to events that fixed
subsets of an independent Bernoulli ground set are present. The proof's identity
sum_i E(I_i Y_i), where Y_i=sum_{j:j~i} I_j, confirms that the denominator counts
ordered pairs and diagonal terms. Its final lower-tail bound gives exactly the
conservative inequality used below.

## 1. Uniform potential witnesses after deletion

Let T be all triples, M=binom(n,3), and fix one GP placement π. Let W_π be the
set of unordered pairs {σ,τ} of disjoint triples with intersecting convex hulls.
Each seven-set has at least one witness. A witness occupies exactly six distinct
vertices, so is contained in exactly n-6 seven-sets. Counting witness/seven-set
incidences gives

    |W_π| >= binom(n,7)/(n-6) = binom(n,6)/7.

This does not require uniqueness of the witness in a seven-set. A triangle has
at most M-1 possible partners; using M is a safe upper bound. For an arbitrary
F⊆T, |F|≤m, discard all witnesses incident with F. Double-counting witnesses
with both ends in F can only make the upper bound on discarded witnesses larger.
Consequently, for every π and every F,

    |W_{π,F}| >= binom(n,6)/7 - mM.

For n≥12, all six factors n,n-1,…,n-5 are at least n/2. Thus the first term is at
least n^6/322560. With m=n^{5/4}, M≤n^3/6, the removed term is at most
n^{17/4}/6. If n^{7/4}≥107520, this is at most n^6/645120. Hence

    |W_{π,F}| >= c n^6,   c=1/645120.

The hypothesis and the full binomial inequality were checked exactly for the
finite proposed n. No deletion is assumed independent of the sampled family.

## 2. The Bernoulli ground set and the Janson convention

There is one independent Bernoulli variable X_σ for each whole triangle σ∈T.
For a witness w={σ,τ}, its indicator is I_w=X_σ X_τ. Thus μ=|W_{π,F}|p^2.
Geometric vertex or edge overlap between different triangles does not identify
Bernoulli variables. Distinct indicators share a variable precisely when their
witness pairs share a whole triangle.

Regard W_{π,F} as a simple graph on the M triangle variables, with degree d_σ.
Two distinct graph edges can share at most one endpoint. Therefore the exact
ordered distinct dependence sum is

    Δ = p^3 sum_σ d_σ(d_σ-1)
      <= M(M-1)(M-2)p^3 <= M^3 p^3.

The joint expectation is p^3, not p^4, because the two events require three
distinct whole triangles. The diagonal sum is μ, because I_w^2=I_w. Since
|W_{π,F}|≤M(M-1)/2≤M^2/2,

    μ >= c n^6 p^2 = c n^3,
    μ+Δ <= (M^2/2)p^2 + M^3p^3
         <= n^3/72 + n^{9/2}/216 <= n^{9/2}.

Janson with t=μ now yields

    P(Z_{π,F}=0) <= exp[-μ^2/(2(μ+Δ))]
                 <= exp[-a n^{3/2}],   a=c^2/2.

An unordered off-diagonal convention requires compensating for the factor two;
it cannot silently replace the ordered sum in this derivation. The candidate
uses the ordered convention correctly. Its M^3 estimate is deliberately loose.

## 3. Continuum, quantifiers, and adaptive deletion

For any six GP points in R^4, the 5×6 matrix of augmented coordinates has rank
five and a one-dimensional nullspace. Its signed 5×5 cofactors, all nonzero,
determine the unique Radon partition. The positive and negative supports are
determined by the determinant signs of the five-subsets. A disjoint triple pair
crosses exactly when it is that circuit's balanced positive/negative partition.
Thus the labeled simple order type determines every W_π, and therefore every
W_{π,F}. Counting at most n^{20n} representatives covers the continuum of GP
placements; it is not a discretization or a coordinate-size assumption.

There are at most

    sum_{j=0}^m binom(M,j) <= (m+1)M^m <= (m+1)n^{3m}

sets F of size at most m. They are subsets of the full ground set, not only of
the selected triangles. A union bound, with no independence requirement among
these events, gives

    P(there exist π,F with Z_{π,F}=0)
       <= (m+1)n^{20n+3m} exp[-a n^{3/2}].

Its exponent tends to minus infinity: n log n and n^{5/4} log n are both
o(n^{3/2}). On the complementary outcome, the universal statement holds for
every F. Therefore a deterministic or random cleaning procedure may choose F
after observing the whole sample. There is no hidden conditioning step.

A finite example in the receipt explains why this universal step matters. With
two disjoint potential witnesses on four independent variables and p=1/2, the
failure probability for a particular one-variable deletion is 3/4; the failure
probability for some adaptive deletion of at most one variable is 15/16. A
fixed-F estimate alone would not suffice. The candidate includes the necessary
union over F.

## 4. Nongeneric placements, simplex degeneracy, and common faces

Suppose a finite simplicial complex has a linear embedding. For each pair of
disjoint nonempty abstract faces, its two convex hulls are compact and disjoint.
The minimum of their distances over finitely many such pairs is positive. If
each vertex moves by less than one third of this minimum, every point of each
convex hull moves by at most that amount, so all these separations persist.

These conditions suffice for global injectivity, including faces with a common
face: if two distinct points have the same affine image, express each in its
face's barycentric coordinates, subtract, and cancel coefficients on common
vertices. The positive and negative remaining coefficients have equal positive
total mass. After normalization they yield equal convex combinations supported
on disjoint subfaces. Both are faces of the complex, contrary to their preserved
separation. The same argument excludes an affine degeneracy of one simplex.

Consequently small generic perturbations preserve the embedding. The GP set is
dense because finitely many nonzero determinant polynomials have a zero set with
empty interior. If K uses fewer than n vertices, add positions for the unused
labels avoiding the finitely many forbidden hyperplanes. This gives a full
n-label GP placement. The universal witness event consequently rules out all
linear embeddings of the retained complex, not only initially generic ones.

## 5. Cleaning and joint success

Each unordered pair of distinct triples sharing an edge is specified uniquely
by its common edge and its two different third vertices. If B counts selected
such pairs, linearity of expectation gives

    E B = binom(n,2)binom(n-2,2)p^2 <= n/4.

Collision indicators need not be independent for this calculation or Markov's
inequality. Thus P(B>m)≤E B/m≤1/(4n^{1/4}). On B≤m, choose one endpoint of
each offending pair and let F be the union of the chosen triangles. Then |F|≤B.
Every originally offending pair loses an endpoint, so the retained triangles
share no edge. They share at most one vertex, as required for a linear
3-uniform hypergraph. The first event in the audit still supplies a crossing
pair in every placement for this specific adaptive F.

The count T of selected triangles is Bin(M,p), with λ=Mp and variance
λ(1-p)≤λ. Chebyshev gives P(T<λ/2)≤4/λ. If λ/2-m>n, then |H\F|>n.
Every retained triangle contributes three distinct edges; hence the generated
complex's one-skeleton has more than 3n edges on at most n vertices. It has at
least three vertices and violates the planar graph edge bound. This proves its
nonplanarity. No assumption that the three favorable events are independent is
needed: another union bound gives a common realization when the sum of their
failure bounds is less than one.

## 6. A finite calculation independent of the asymptotic claim

The receipt derives n,m,p from r=2^64 via n=r^4, m=r^5, p=r^-6. All calculations
use exact integers and fractions. In particular:

    a > 2^-41,            a n^{3/2} > 2^343,
    log(m+1)+(20n+3m)log n
       <= m+256(20n+3m) < 770m+5120n < 2^331.

Here log(m+1)≤m follows from e^m≥1+m, and log n=256 log 2<256. The net exponent
is greater than 2^342, so the robust failure is less than 1/8. To avoid even an
exponential floating-point calculation, the independent receipt also uses
e^{-x}≤1/(1+x) and the exact lower witness count and stronger denominator.
Further,

    E B/m <= 2^-66,       λ > 2^379,
    4/λ < 2^-377,         λ/2-m > n.

The exact sum 1/8+2^-66+2^-377 is below one. This verifies the explicit finite
existence parameter, without taking an asymptotic limit or generating a huge
sample. The finite certification cannot certify the imported theorems on its own.

## 7. Independent artifacts and falsification probes

The original scripts were copied into separate ignored scratch directories and
executed there. The candidate's 16-check receipt and the earlier review code's
396-check receipt both reproduce exactly. Earlier REVIEW.md and verdict.json
prose were not read before, or in obtaining, this verdict.

`independent_probability_checks.py` imports neither earlier script. It records
3,852 exact assertions, including cofactor-derived circuits for all six-subsets
of eight moment-curve points, twelve additional integer GP seven-point
placements, and all 1,024 triangle samples on five vertices. The small samples
check collision counts, the deletion construction, retained edge counts, and
exact binomial moments. They are consistency and corruption probes, not a proof
by finite testing of the universal geometric input.

The ten recorded mutations distinguish wrong exponents, dropping the adaptive
deletion union, unordered versus ordered dependence coefficients, a p^4 joint
expectation for events sharing a triangle, omitting diagonal terms, and falsely
identifying binomial variance with the mean. Exponent mutations are rejected
for failing the displayed proof's conditions, not declared counterexamples to
every possible construction using those exponents. In general p=n^-α and
m=n^β require 1<α<2 and 4-2α<β<3-α for all the same high-probability
steps. Placement entropy remains O(n log n) when β<1; this is still dominated
because 3-α>1. The candidate α=3/2, β=5/4 lies strictly inside that region.

No candidate repair is necessary in this family. Clarifying “general position”
as labeled simple order types and including the degree formula for Δ would make
a later paper easier to check, but the existing proof has the needed substance.
The exact remaining gap to the full target theorem is outside this family's
assigned scope: establish the PL-inflation/topology gate and complete a bounded,
primary-source priority review before any solved or publication promotion.
