# Fixed start distinct multiple matching and a barrier to smooth tail tests

## Publication edition: finite numerical certificate omitted

This prose-only edition preserves the complete general divisibility-closure
and rough-part derivations and reports the accepted finite claim. The numerical
Hall witness, its neighbor lists, matching assignments, full finite slack-table
entries, supplementary exact-value dataset, executable code and raw certificates
are omitted. The finite claim, including E(16)=40 and H(16)=24 and the success
of every tail in the defined family at endpoint 39, cannot be independently
reproduced from this edition alone. It is not a complete self-contained proof
of the finite claim or a full computational reproduction package. Published
hashes, aggregate counts and match results identify separately audited evidence;
hashes alone do not prove the omitted arithmetic. The general structural
arguments are written out in full and do not depend on finite regression tests.

## Result and scope

This note gives an elementary structural reduction of the Hall obstructions for fixed-start distinct-multiple matching, and an exact finite obstruction to a proposed simplification of that reduction. It does not determine an asymptotic equivalent, improve the known asymptotic bounds, or claim novelty for the elementary structural observations.

For a positive integer n, let H(n) be the least integer H for which there are distinct integers a_1,...,a_n in (n,n+H] with k dividing a_k for every 1 <= k <= n. Write E(n)=n+H(n) for the least absolute right endpoint.

The finite result is as follows.

**Accepted finite claim (numerical certificate omitted).** In the fixed interval (16,39], every set of the form

    T(d,y,u) = {d s : s is a positive integer, d s <= 16,
                         s > u, and P^+(s) <= y}

satisfies the Hall cardinality inequality |N(T)| >= |T|, for every positive integer d and every real y >= 1 and u >= 0. Here P^+(1)=1 and N(T) is the set of integers in (16,39] divisible by at least one member of T. Nevertheless, the whole divisibility graph has no matching of 1,...,16. In fact E(16)=40 and H(16)=24.

Thus even checking every smoothness cutoff, every size cutoff, and every integer dilation of these sets is not an exact sufficient test for matching. This is a finite counterexample to that reduction. It is not a counterexample to eventual or asymptotic versions of such a principle.

## The known fixed start gap

Erdos and Pomerance [1] use f(n) for E(n), an absolute endpoint, and f(n,m) for an interval length. Their Theorem 2 and their sharpened upper bound (11), on printed pages 150 and 154-155 respectively, give

    (2/sqrt(e) + o(1)) n sqrt(log n / log log n)
        <= H(n)
        <= (c + o(1)) n sqrt(log n),

where c = sqrt(r)/(1-r) = 1.7398... and r is the positive solution of exp(-r)=r. Subtracting n from their endpoint bounds does not change the leading constants on these scales. Their stated Theorem 3 first proves the weaker upper constant 2.

The original paper also proves H(n)/n -> infinity. Its lower-bound mechanism uses a smooth-number Hall obstruction, and a dilation argument transfers bounds at selected smaller inputs to all sufficiently large inputs. These results already imply

    H(n) = n (log n)^(1/2 + o(1)).

That last statement records a logarithmic exponent; it is not the asymptotic equivalent requested in EP710. In particular, it does not decide the missing factor between the two displayed bounds.

Erdos [2], printed page 36, repeats the fixed-start asymptotic question using open right endpoints. With integer lengths the open-endpoint minimum is exactly H(n)+1. This note consistently uses a closed right endpoint.

The uniform-over-start function considered in [3] and [4] has different quantifiers. Their improvements for that function do not settle this fixed-start problem. No live-status or exclusivity conclusion about other researchers is asserted here.

## Hall formulation and divisibility closure

Fix integers x >= n >= 1. Let G(n,x) be the bipartite graph with left vertices [1,n], right vertices (n,x], and an edge k--j exactly when k divides j. For S contained in [1,n], write

    N(S) = {j : n < j <= x and k divides j for some k in S}.

Hall's theorem says E(n) <= x if and only if |N(S)| >= |S| for every S contained in [1,n]. This is the same matching formulation used in [1].

**Lemma 1.** If G(n,x) fails Hall's condition, it has a deficient set that is upward closed under divisibility within [1,n].

**Proof.** Starting with a deficient S, define

    U = {b <= n : a divides b for some a in S}.

We have S contained in U. Moreover N(U)=N(S): a multiple of any b in U is a multiple of the corresponding a in S, and the reverse inclusion follows from S contained in U. Therefore |U|-|N(U)| >= |S|-|N(S)| > 0. The definition makes U upward closed. This proves the lemma.

Equivalently, to establish the required upper bound one must control every divisibility upper set, not merely an interval of integers or a full smooth-number tail.

## Exact decomposition by large prime factors

For a prime q define the q-rough part of a positive integer k by

    R_q(k) = product over primes p >= q of p^(v_p(k)).

Thus k/R_q(k) has all prime factors strictly below q.

**Lemma 2.** Restrict the left side of G(n,x) to k > x/q. Every edge in this restricted graph preserves R_q. For each q-rough integer d, put

    N_d = floor(n/d),   X_d = floor(x/d).

The fiber with rough part d is, after division by d, precisely the divisibility graph between

    {s : X_d/q < s <= N_d and P^+(s) < q}

and

    {t : N_d < t <= X_d and P^+(t) < q}.

Isolated right vertices may be included without effect.

**Proof.** If k > x/q and k divides j <= x, then the positive integer j/k is strictly smaller than q. Consequently multiplying k by j/k changes no exponent of any prime p >= q. This proves preservation of R_q and disjointness of the fibers.

Write k=d s and j=d t in a fixed fiber. Membership in the intervals becomes s <= floor(n/d), floor(n/d) < t <= floor(x/d). Also

    d s > x/q  iff  d s q > x  iff  s q > floor(x/d),

because s q is an integer. This gives s > X_d/q exactly, with no lost endpoint. Finally k divides j if and only if s divides t. These observations prove both directions of the claimed graph identification.

**Corollary.** Every Hall failure can be expressed, after an integer dilation is removed, as a deficient divisibility upper set inside one of these smooth fibers. The set need not be the whole smooth tail.

**Proof.** Use Lemma 1 and let m be the least member of a deficient upper set U. Choose any prime q > x/m; then U is contained in the restricted left side of Lemma 2. Partition U by R_q. Their neighborhoods are disjoint, so a positive sum of deficiencies forces a deficient fiber U_d. Upward closure stays in this fiber: if a in U_d divides b <= n, then b/a <= x/a < q, so R_q(b)=R_q(a)=d. Divide by d and apply Lemma 2.

This is an exact structural reduction. It provides no useful uniform bound on q by itself, since q is chosen using the unknown witness. Replacing arbitrary upper sets inside the fibers by their full tails is the step tested next.

## Reported finite verification and retained quantifier reductions

The separately audited numerical evidence at n=16, x=39 contains an upward
closed left set with seven elements and an actual neighborhood with six
elements. It therefore gives E(16)>39. A separately audited matching of all
sixteen left vertices at endpoint 40 gives E(16)<=40. The accepted exact result
is E(16)=40, equivalently H(16)=24. The maximum matching sizes at endpoints 39
and 40 were independently checked to be 15 and 16 respectively. These are
reported match results; the witness, neighborhoods and assignments needed to
check them directly are not distributed here.

### Reduction of all real cutoffs to finitely many cases

For any positive integer d<=16, put N=floor(16/d). On the possible integer
values of s, every real y>=1 defines the same smoothness class as one of 1 or
the primes at most N. This includes s=1 when y=1 because P^+(1)=1. Every real
u>=0 defines the same strict tail as h=min(floor(u),N): for integral s,
s>u is equivalent to s>floor(u), and the tail is empty when u>=N. Thus no
cutoff equality, nonintegral cutoff, or empty-tail case is omitted.

For d=1, define the actual-neighborhood slack

    S(p,h) = {k : h < k <= 16 and P^+(k) <= p},
    D(p,h) = |{j : 16 < j <= 39 and some k in S(p,h) divides j}| - |S(p,h)|.

The original numerical table contains all 119 canonical values D(p,h). An
independent check matched every entry and found every entry nonnegative. The
entries themselves are omitted. Conditional on this reported numerical check,
the finite-cutoff reduction above establishes the assertion for every real
y>=1 and u>=0 when d=1. These slacks count actual neighborhoods, rather than
possibly larger sets arising from a smooth-number estimate.

### Reduction of every integer dilation

Every neighbor j of an input ds is divisible by d. Division by d therefore
identifies its actual neighborhood exactly with the neighborhood of s in

    (floor(16/d), floor(39/d)].

Indeed, writing j=dt, the inequalities 16<dt<=39 are equivalent to
floor(16/d)<t<=floor(39/d), and ds divides dt if and only if s divides t.
For each d=2,...,16, the separately audited finite evidence supplies a full
matching of [1,floor(16/d)] into this normalized interval. Restrict any such
matching to a smooth tail and multiply its images by d. The images remain
distinct, lie in (16,39], and are divisible by their corresponding inputs.
This proves the tail inequality from the reported full-matching premise.
For d>16 the tail is empty. The actual finite matching assignments and the
full table of normalized numerical cases are omitted.

Independent verification directly checked all 249 canonical dilated-tail
parameter cases and all 15 normalized full dilation graphs. It also checked
all 65536 left subsets at endpoint 39. Those counts and the accepted outcomes
are verification metadata, not substitutes for the omitted numerical
certificate. Together with that separate certificate, the reductions above
cover every positive integer d and every real y>=1 and u>=0. Without the
certificate, this edition alone does not complete the finite proof.

## What the attempt establishes and where it stops

The smooth counting obstruction from [1] is a necessary-condition tool, not an asserted sufficient condition in that paper. The theorem above does not correct or contradict the published proof. It blocks the proposed stronger shortcut in this attempt: applying only one-dimensional smooth-tail tests, even with exact neighborhoods and all integer dilations, cannot give an exact matching criterion.

The reduction that remains valid is Lemma 2 together with arbitrary divisibility upper sets in its smooth fibers. Proving an asymptotic upper bound on the lower-bound scale would require controlling those general sets, or a separate argument showing why their excess obstruction is asymptotically negligible. Neither has been established here. Likewise, the finite example does not rule out asymptotic sufficiency of smooth-tail tests, and it does not locate the true leading scale or constant of H(n).

Consequently the asymptotic question remains unresolved in this note. The deliverable is a checked structural reduction and a precise, small failure of one proposed simplification.

## References

[1] Paul Erdos and Carl Pomerance, *Matching the natural numbers up to n with distinct multiples in another interval*, Proceedings A 83(2) / Indagationes Mathematicae 42 (1980), 147-161. Definition and Hall formulation: printed 147-148. Smooth obstruction and lower bounds: 148-153. Fixed-start upper bounds: 153-155. Author-hosted full text: https://math.dartmouth.edu/~carlp/PDF/matching.pdf

[2] Paul Erdos, *Some of my forgotten problems in number theory*, Hardy-Ramanujan Journal 15 (1992), 34-50; fixed-start question on printed page 36. Full text: https://hrj.episciences.org/125/pdf

[3] Wouter van Doorn, *On the length of an interval that contains distinct multiples of the first n positive integers*, Integers 26 (2026), A7. Uniform-over-start variant. DOI: https://doi.org/10.5281/zenodo.18154085

[4] Kaizhe Chen and Samuel Korsky, *Improved Bounds for Distinct Multiples in Intervals*, arXiv:2607.26450v2 (2026). Uniform-over-start variant. https://arxiv.org/abs/2607.26450v2

## Edition and review statement

This AI-assisted work is unrefereed. Acceptance refers to an independent
internal AI audit of the original note and its separate numerical evidence.
No external human peer review, journal acceptance or formal proof-assistant
certification is claimed. No mathematical correction was required. No novelty,
priority, asymptotic improvement, eventual obstruction, or full solution is
claimed. The fixed-start asymptotic question remains unresolved by this work.

This edition preserves the complete general structural proofs, the exact finite
claim and all substantive scope qualifications. It omits numerical proof
payloads and explicitly distinguishes the reported finite verification from
the written general arguments. Original sealed candidate and audit packages
are unchanged. Historical source inspection and verification are reported as
such; preparation of this edition checks byte integrity and publication
structure only, without new mathematical computation or scholarly-source
retrieval/inspection. Copied source documents, source text and images, datasets,
raw certificates, executable code and private coordination material are not
distributed.
