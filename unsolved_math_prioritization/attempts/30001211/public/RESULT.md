# 30001211 / OWR-3396-010: five-route partial investigation

**Disposition: unsolved. Five substantive author approaches; no full candidate.**

This is an AI-assisted, unrefereed mathematical investigation. Its elementary
lemmas have proofs below and bounded exact controls. No novelty or priority is
claimed. The complete existential IET question remains unresolved by this work.
Independent review and the publication gate are pending.

## 1. Exact target and source cautions

Let I=[0,1), and let T be a finite, orientation-preserving interval exchange:
a bijection obtained by translating the members of a finite half-open interval
partition. Minimality means every forward orbit is dense in I. Write

    Phi_T(x,y) = liminf_{n -> infinity} n |T^n x-y|.

The catalogue asks whether there EXISTS a minimal T such that Phi_T(x,y)=0 for
EVERY ordered pair (x,y) in I². Equivalently,

    exists T, for all x,y, for all epsilon>0 and N,
    exists n>=N with n |T^n x-y| < epsilon.

It is not a statement about every minimal T. Nor does it require one n to work
for all pairs simultaneously. The gauge is usually called connectivity; the
diagonal Phi_T(x,x) is recurrence. Refuting some classes of T is insufficient.

The original Boshernitzan–Chaika OWR contribution, pp.747–748, poses this as
Question 2, using circle distance ||u-v||=min(|u-v|,1-|u-v|). The later arXiv
paper, Section 13 Problem 3, uses the displayed Euclidean formula above.
For every fixed target 0<y<1 these gauges agree: once circle distance is less
than min(y,1-y), it equals Euclidean distance. A finite circle-gauge liminf is
obtained along such a subsequence, and the reverse inequality is automatic;
an infinite circle-gauge implies an infinite Euclidean gauge. The boundary
target y=0 needs separate care. No blanket equivalence at that endpoint is
assumed. Each negative IET result below supplies an interior target and thus
obstructs both formulations. Neither unrestricted formulation is settled.

The OWR report already excludes exchanges of at most three intervals. The
arXiv:0910.5422v2 text is internally inconsistent about the broader measurable
map problem: Section 4.2 announces an exclusion for maps admitting an invariant
probability measure, but Section 13 still asks for a 1-collapsing IET (which
preserves Lebesgue measure). No proof of that announced general exclusion was
located in the text. The publisher landing page was read, but the published
full text was not obtained. That sentence is not used as a theorem or as a
certificate that this target is already solved. Section 7 below also explains
why broadening the category of maps can drastically change the question.

## 2. Route 1: arithmetic norm obstruction

### Theorem 1 (quadratic translations)

Suppose all translation amounts h_1,...,h_r of an aperiodic IET belong to a
fixed real quadratic field Q(sqrt(d)), with d>1 squarefree. Choose an integer
D>=1 such that D h_i belongs to Z[sqrt(d)] for every i. Let sigma be the
nontrivial field embedding and H=max_i |sigma(h_i)|. Then H>0 and, for all
x in I and n>=1,

    n |T^n x-x| >= 1/(D² H).

For circle distance the uniform lower bound 1/(D²(H+1)) holds. In particular,
no such minimal IET answers the question affirmatively.

Proof. Set delta=T^n x-x. Telescoping along the actual itinerary gives

delta=sum_{j=0}^{n-1} h_{i(j)}, so D delta is in Z[sqrt(d)] and
|sigma(delta)|<=nH. Aperiodicity gives delta != 0. Consequently the algebraic
norm N(D delta) is a nonzero integer. Hence

    |delta sigma(delta)| >= D^(-2),

and the stated Euclidean inequality follows. H=0 would force every h_i=0,
which contradicts aperiodicity. For circle distance select m in {-1,0,1}
with ||delta||=|delta-m|. Since -1<delta<1 and delta !=0, delta-m !=0.
Also D(delta-m) is integral in Z[sqrt(d)] and
|sigma(delta-m)|<=nH+1. Therefore

    n ||delta|| >= n/[D²(nH+1)] >= 1/[D²(H+1)].

This proves the theorem. In particular, take any interior x and set y=x. □

The theorem covers arbitrarily many intervals, but only a restricted arithmetic
class. For example, rotation by sqrt(2)-1 has D=1 and H<4; its diagonal cannot
collapse. It is a minimal IET by irrationality, not by a numerical orbit test.

### Degree barrier

More generally suppose the translations belong to a number field K of degree
q, choose D making D h_i algebraic integers, and let H_j be an upper bound
for |sigma_j(h_i)| at each nonidentity embedding. If the displacement is nonzero,
the norm argument gives

    n^(q-1) |T^n x-x| >= D^(-q) product_{j=2}^q H_j^(-1).

Use positive upper bounds H_j if necessary. The algebraic norm is a nonzero
rational integer, and each conjugate displacement is bounded by n H_j, proving
the formula. For q>2 this does not bound n|T^n x-x| away from zero. For
transcendental lengths this norm mechanism does not apply at all. Thus it does
not resolve the unrestricted target.

## 3. Route 2: bounded first-return clocks

### Lemma 2 (induction transfers a bad pair)

Let S act on a metric space, let A be a return section, and suppose T=S_A has
successive return times q_k(x) satisfying k<=q_k(x)<=Hk. If x,y belong to A and

    liminf_m m d(S^m x,y) = c > 0,

where c may be infinite, then

    liminf_k k d(T^k x,y) >= c/H.

Proof. T^k x=S^{q_k(x)}x, q_k(x)->infinity, and k/q_k(x)>=1/H. Restricting a
liminf to a subsequence cannot decrease it. Apply these observations, or use
any fixed lower bound c'<c eventually if c is infinite. □

If a Euclidean interval of length L is rescaled to unit length, the gauge is
also divided by L. Circle lower bounds on the ambient rotation still give
Euclidean lower bounds on the section; for interior section targets they also
obstruct its rescaled circle gauge by Section 1.

### Corollary 3 (all minimal exchanges of at most three intervals)

The external input is Bugeaud–Harrap–Kristensen–Velani (2010), Corollary 1:
for every irrational alpha there is b with

    inf_{n>=1} n ||n alpha-b|| > 0.

In fact their theorem gives Hausdorff dimension one. We need only nonemptiness.
The set with positive LIMINF is invariant under b -> b+k alpha modulo one,
for every integer k: replace n by n-k and use n/(n-k)->1. It is consequently
dense, since the orbit of any such b under an irrational rotation is dense.
Thus for any x and any nonempty open interval A there is an interior y in A
with liminf_n n||R_alpha^n x-y||>0.

An irrational circle rotation induced on a nonempty interval has bounded
return times. Indeed, the open sets R_alpha^(-j)(interior A), j>=1, cover the
compact circle by minimality; take a finite subcover and its largest j.
Lemma 2 excludes 1-collapse for this induced map.

For completeness the three-interval reduction is explicit. Reducible
permutations cannot be minimal because they preserve a proper initial interval.
The irreducible permutations of three intervals are the two cyclic orders and
the reversal. The cyclic orders are rotations after merging adjacent pieces.
For the reversal, write the three lengths as a,b,c>0 with a+b+c=1. Its
translations are

    b+c on [0,a), c-a on [a,a+b), and -a-b on [a+b,1).

This is exactly the first-return map to [0,1) of rotation by b+c on the circle
of circumference 1+b. Return times are respectively 1,2,1, as direct
substitution shows. If (b+c)/(1+b) were rational, that rotation and hence its
induced map would be periodic, contradicting minimality. It is therefore
irrational, and Lemma 2 applies with H=2. Two intervals are the rotation case;
one interval is the identity and not minimal. □

This recovers a known obstruction, not a new solution. A general higher-genus
IET is not thereby a bounded induced rotation. Establishing such a reduction
for all IETs would be false in that form; no such assumption is made.

## 4. Route 3: invariant-measure potential obstruction

### Lemma 4 (finite reciprocal-distance potential)

Let S:I->I be Borel and preserve a Borel probability measure mu. If for some
y in I,

    P_mu(y) = integral_I |z-y|^(-1) dmu(z) < infinity,

then for mu-almost every x,

    n |S^n x-y| -> infinity.

Proof. For every positive integer a, Tonelli's theorem gives

    sum_{n>=1} mu({z: |z-y|<a/n})
      = integral # {n>=1: n<a/|z-y|} dmu(z)
      <= a P_mu(y) < infinity.

The integral hypothesis in particular excludes an atom at y. Invariance makes
the same sum for events {x: |S^n x-y|<a/n} finite. The first Borel–Cantelli
lemma says almost every x belongs to only finitely many of these events.
Intersecting over integer a shows n|S^n x-y| tends to infinity. □

For an interior y this also obstructs the circle formulation. Hence a necessary
condition for a 1-collapsing IET is infinite P_mu(y) at EVERY y for EVERY
invariant probability mu. This condition uses other invariant measures if they
exist, not just the preserved Lebesgue measure.

A sufficient local condition for finite potential is
mu(B(y,r))<=C r^(1+eta) for all sufficiently small r, eta>0. Partition a small
ball into annuli 2^(-j-1)<|z-y|<=2^(-j); their potential contributions are
at most 2^(j+1) C 2^(-j(1+eta)), a summable geometric series. The complement
has bounded integrand. This is a genuine conditional exclusion.

Gap: Lebesgue measure has infinite potential at every y in I. Unique ergodicity
therefore removes the obvious alternative-measure route. No theorem here
produces a finite-potential target for every remaining minimal IET.

## 5. Route 4: two-sided endpoint geometry

Let D be {0} together with the internal left endpoints of the original
continuity intervals of T. Put

    E_n = union_{-n<=j<=n} T^j D,
    e_n = min{|u-v|: u,v in E_n, u!=v}.

Use DISTINCT points; endpoint connections do not create artificial zero gaps.
For a minimal IET, E_n has at least two points.

### Lemma 5 (endpoint-separation obstruction)

For every x in I and n>=1,

    |T^n x-x| >= e_n.

Consequently, if inf_{n>=1} n e_n = c>0, no minimal T is 1-collapsing.

Proof. The discontinuities of T^n are among union_{j=0}^{n-1} T^(-j)D.
This follows inductively: a composition can gain a discontinuity only at a
previous discontinuity or a preimage of one of the new outer map. These cuts
partition I into half-open intervals on which T^n is translation. Let u be the
left endpoint of the interval containing x. Right continuity ensures

    T^n x-x = T^n u-u.

For some d in D and 0<=j<n, u=T^(-j)d, including u=0. Thus both u and
T^n u=T^(n-j)d belong to E_n. They are distinct, since a minimal interval
exchange has no periodic point. Their distance is at least e_n. □

For any fixed interior x the conclusion gives a positive diagonal gauge under
the stated spacing assumption, for both metrics. In particular an affirmative
example must have inf_n n e_n=0. That condition alone is not sufficient.

The attempted extension was to choose a point surviving every shrinking
neighborhood of an orbit. For a fixed x, put

    K(c,N) = intersection_{n>=N} {y in [a,b]: |T^n x-y|>=c/n},

where 0<a<b<1. These sets are compact and nonempty precisely when every finite
intersection is nonempty (nested compactness). A surviving y would be a bad
pair. General minimality does not supply the required finite-intersection
bounds. Small endpoint gaps and highly unbalanced return towers are exactly
where the above geometric argument loses a positive constant. No claim that
the finite survivor intersections always remain nonempty is made.

## 6. Route 5: constructive covering and its structural barrier

### Lemma 6 (necessary horizon for a complete tail cover)

If a finite collection of balls with centers z_n, N<=n<=M, and radii epsilon/n
covers [a,b] of length L>0, then

    2 epsilon sum_{n=N}^M 1/n >= L.

For N>=2 it follows that M >= (N-1) exp(L/(2 epsilon)).

Proof. The measure of a union is at most the sum of lengths, at most
2 epsilon sum 1/n. Also sum_{n=N}^M 1/n <= integral_{N-1}^M dt/t. □

For an orbit with zero gauge at every target in [a,b], the open tail balls
cover [a,b], and compactness gives a finite subcover for each epsilon,N. The
lemma explains why those cover horizons must grow rapidly. It does NOT give a
contradiction: the target permits arbitrarily large and target-dependent n.
Nor does it assume a uniform hitting time for all initial x.

### Proposition 7 (an explicit all-target sequence)

There is a sequence of distinct rational z_n in (0,1) such that

    for every y in [0,1], liminf_n n|z_n-y| = 0.

Proof. Construct stages k=1,2,..., keeping a global index n and starting each
stage with left endpoint a=0. Until a reaches 1, set

    ell = min(1-a, 1/(k n)).

Choose z_n in [a+ell/3,a+2ell/3], rational and different from all earlier
terms, and replace a by a+ell and n by n+1. This choice is possible because
only finitely many rational points have been forbidden. One deterministic
choice is the first unused member of

    a+ell*(1/2+1/(8m)), m=1,2,... .

A stage ends after finitely many indices because the harmonic tail diverges.
Its intervals partition [0,1]. For every y, one interval in stage k contains y,
and at its index n,

    n|z_n-y| <= 2 n ell/3 <= 2/(3k).

The selected indices tend to infinity because each finite stage uses at least
one new index. The displayed bounds prove the proposition. □

This explicitly defeats a proposed proof that *every* sequence has a target
with positive liminf at scale n. It does not construct an IET orbit.

## 7. An instructive Borel-map control, outside the target

Proposition 7 even gives a Borel map F:I->I with every forward orbit dense and
with Phi_F(x,y)=0 for ALL x,y, but F is not an IET and has no invariant
probability measure. This is recorded as a boundary-case control only. No
historical priority is asserted for this elementary observation.

Let Z={z_1,z_2,...} and define F(z_j)=z_(j+1), while F(x)=z_1 for x not in Z.
The map is Borel: the preimage of any Borel set is a subset of the countable
set Z, possibly union I\Z. For x outside Z, F^n(x)=z_n. For x=z_j,
F^n(x)=z_(n+j). A fixed index shift preserves the zero liminf, since
n/(n+j)->1. Thus every orbit has the all-target property and is dense.

If mu were invariant, F(I) subset Z would imply mu(Z)=1. But
F^(-1){z_1}=I\Z and F^(-1){z_j}={z_(j-1)} for j>=2. Invariance first gives
mu({z_1})=0, then every singleton z_j has measure zero, contradicting
mu(Z)=1. Finally, F is noninjective (all points outside Z map to z_1) and
therefore is not an interval exchange.

The construction underscores why an argument using only Borel measurability
and dense orbits cannot settle the IET question. It also makes the unreconciled
arXiv question about general measurable maps unsafe as a stand-alone status
source. It does not disprove that text's separate assertion about maps with
invariant probability measures, nor prove that assertion.

## 8. Exact remaining gap

A full affirmative answer needs a single finite IET, a proof of minimality,
and a proof of the critical zero gauge for every ordered pair, including
boundary targets and exceptional orbits. No such example is supplied.

A full negative answer needs, for every minimal IET, at least one interior bad
pair (or another complete endpoint-aware obstruction). The present arguments
cover quadratic arithmetic, bounded induced rotations, specified endpoint
separation, and a specified invariant-measure potential condition. They do not
cover all minimal exchanges of four or more intervals with unrestricted lengths.

No argument promotes almost-everywhere connectivity to all pairs, mistakes a
golden rotation counterexample for a refutation of the existential question,
or treats finite-time computation as an asymptotic certificate. The target
therefore remains **unsolved, 5/5 author approaches**.
