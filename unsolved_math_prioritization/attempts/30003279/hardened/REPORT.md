# Minimal separations on squarefree split circles

Problem 30003279 / OWR-15174-012; queue rank 996. Author checkpoint, 7 October 2026.

## Disposition

**UNSOLVED, five substantive routes.** The three-point subquestion has an affirmative answer, including the sharp limiting arc constant, by a fully specified consequence of existing published results. The four-point and general-cardinality squarefree questions are not resolved here. No novelty, exhaustive literature coverage, human peer review, or formal proof certification is claimed. Independent audit is pending.

## Exact target and quantifiers

The primary source is Andrew Granville's Problem 7 in the problem session of *Analytic Number Theory*, Oberwolfach Report 53/2016, printed p.3025, DOI 10.4171/OWR/2016/53. The meeting took place 6–12 November 2016. Its introductory restriction is explicit: n is a product of distinct rational primes congruent to 1 modulo 4. The count of prime factors in that introduction must not be confused with the number of points in a cluster. Here r denotes the former and m the latter.

Write A for the positive integers n>1 that are squarefree and have only prime factors 1 modulo 4. Put R=sqrt(n), and E(n)={(x,y) in Z²:x²+y²=n}. For an m-element subset S of E(n), let D(S) be its maximum pairwise Euclidean distance, and L(S) the length of its shortest containing circle arc. The source asks for attainability of the stated powers 1/3 for m=3,4; 2/5 for m=5,6; and 3/7 for m=7. We interpret an asymptotic construction as: for fixed m, there are a constant C_m and infinitely many n in A, tending to infinity, with some m-element S_n having L(S_n)≤C_m R^e. It does not mean every n, or every cluster, or one fixed bound on all m. The report itself uses informal separation language; L is the convention of the cited circle paper. D≤L, and for D=o(R) a cluster is contained in an arc of length (1+o(1))D, so the exponent question is unchanged. To see the latter, place one point at angle zero. Every other point lies in the two small angular intervals next to zero modulo 2π, and lifting their angles into a common small interval gives the result by the chord formula.

The source's general m analogue is naturally the exponent e_m=E_m/binom(m,2), where E_m=floor((m−1)²/4). This is (m−1)/(2m) for odd m, and (m−2)/(2(m−1)) for even m. Route 3 proves the lower bound in exactly the restricted class. No global formula for the optimal attainable exponent is asserted.

## Prior work, chronology, and scope checks

- Cilleruelo–Granville, *Close Lattice Points on Circles*, Canadian Journal of Mathematics 61 (2009), 1214–1238, DOI 10.4153/CJM-2009-057-2, is earlier than the 2016 problem session. Its Theorem 1.2 and opening construction settle the unrestricted three-point sharp arc constant; its four-point results also concern unrestricted integer n. Their squarefree admissibility cannot be inferred merely from their norm identities. Section 12 explicitly asks about five points at scale R^(2/5) without the squarefree restriction.
- Booker–Browning, *Square-free Values of Reducible Polynomials*, Discrete Analysis 2016:8, DOI 10.19086/da.732, was published 1 June 2016. The inspected arXiv v3 was posted 18 January 2017 and identifies the same publication. Theorem 1.1 supplies the squarefree-value bridge used below. Neither this dependency nor the construction should be called a new theorem discovered here. We do not assert that this exact combined consequence was previously written down.
- Temur, *Discrete fractional integrals, lattice points on short arcs, and diophantine approximation*, arXiv:2012.10784, initially posted in 2020, was inspected as later work. Its Theorem 5 fixes coordinate offsets in advance and its Theorem 6 treats a specified near-square range. These do not establish attainability at the unrestricted sharp five-point exponent, or the squarefree four-point infinitude needed here. Its explicit discussion preserves the distinction between fixed patterns and uniform moving offsets.
- Targeted web checks through 7 October 2026 located no later theorem resolving the full target. This is a bounded search result, not a certification that no such theorem exists.

The exact-ID/source-code PR, branch, commit and default-branch artifact checks found no substantive earlier attempt. Semantic PR/branch/code searches covered lattice, circles, separation and Cilleruelo. The public corpus has no exact OWR-15174-012 research-results record. The nearby OWR-12725-015 concerns uniform point counts on arbitrary short arcs, and AIM-COMBINATORICS-0244 concerns sumsets of squares; neither is a previous attempt at the present extremal fixed-cardinality construction. Related PR #487 concerns an optimization bound in sphere packing, rather than integer circle clusters. Search coverage is bounded and does not assert inspection of every file on every remote branch.

## Route 1: area and parity, with the prime-radius obstruction

This route tries to improve the lower bound geometrically or make the squarefree restriction force a stronger one.

For three distinct lattice points P,Q,T on a circle centered at the origin, the triangle is nondegenerate: a line meets a circle in at most two points. Let its area be Δ and side lengths a,b,c. All three points have the same norm modulo 2; hence at most two coordinate-parity classes occur. Two points have the same coordinate parities, so their difference is even in both coordinates. The determinant giving twice the area is therefore a nonzero even integer. Consequently Δ≥1.

The circumradius identity gives abc=4RΔ≥4R. Order the three points along a shortest containing arc, with consecutive subarc lengths s,t and L=s+t. Each nonzero chord is strictly shorter than its corresponding positive arc, including the chord between the arc endpoints. Thus abc<st(s+t)≤L³/4. Therefore L³>16R. This argument does not use squarefreeness. It is the credited classical mechanism, included to make the normalization unambiguous.

Squarefreeness cannot improve this asymptotic constant for triples, by Route 2. However it matters substantially if the number of prime factors is prescribed. If n is a single prime 1 modulo 4, all eight points form the signed coordinate permutations of (a,b), where 0<a<b. In angular order, their successive gaps alternate 2θ and π/2−2θ, for θ=arctan(a/b) in (0,π/4). Hence every arc containing three points has length at least πR/2, and equality is attained by any three consecutive points. The assertion follows from unique factorization in Z[i], which gives exactly these eight points. A uniform assertion over every admissible n is therefore false. This prime case is an obstruction to the wrong quantifier, not a counterexample to the intended infinitude question.

**Gap after this route:** area alone controls only triples and does not construct larger sharp clusters.

## Route 2: a squarefree sieve bridge for the classical triple

For an integer t≥1 define

P_−=(4t³−1,2t²+2t), P_0=(4t³,2t²+1), P_+=(4t³+1,2t²−2t).

These are the classical points displayed by Cilleruelo–Granville. Direct expansion gives their common squared norm

H(t)=16t⁶+4t⁴+4t²+1=(4t²+1)(2t²+2t+1)(2t²−2t+1).

The three factors have negative discriminants −16,−4,−4, and are distinct irreducible polynomials over Q. They share no polynomial factor; their pairwise resultants are 20,20,32. The product is therefore a squarefree polynomial, despite sometimes having nonsquarefree integer values. Also H(0)=1, so H has no fixed prime divisor.

We invoke Booker–Browning Theorem 1.1 as a published dependency: a nonconstant squarefree integer polynomial with no fixed prime divisor and all irreducible factors of degree at most three takes infinitely many squarefree positive values (indeed, values with a uniformly bounded number of prime factors). Every hypothesis has just been checked. It follows that H(t) is squarefree for infinitely many positive t. The theorem is not re-proved here; no computation of sieve constants is needed for its existential conclusion.

Each of the three factors is an odd primitive sum of two squares:

4t²+1=(2t)²+1²,
2t²+2t+1=t²+(t+1)²,
2t²−2t+1=t²+(t−1)².

If an odd prime p≡3 modulo 4 divided a primitive sum u²+v², either v is invertible and −1 would be a square modulo p, or p divides both u and v. Both are impossible. Thus all prime divisors of H(t) are 1 modulo 4, for every integer t. On the infinite squarefree subsequence, H(t) belongs to A.

The squared pair distances are 4t²−4t+2, 4t²+4t+2, and 16t²+4. The endpoint distance d_t=sqrt(16t²+4) is the largest. The points lie in the right half-plane and their polar angles are ordered P_+,P_0,P_−. Thus their containing minor arc has length

L_t=2R_t arcsin(d_t/(2R_t)), where R_t=sqrt(H(t)).

As t→∞, R_t~4t³ and d_t~4t; since d_t/R_t→0, L_t~d_t. Consequently

L_t/R_t^(1/3) → 16^(1/3).

Together with Route 1, this proves that the infimal limiting three-point arc constant over A is exactly 16^(1/3). The same constant is attained asymptotically for the diameter construction; we do not claim the elementary diameter lower bound alone is sharp. A finite admissible example is t=2, H(2)=1105=5·13·17. By contrast t=1 yields 25 and is inadmissible. These examples prevent silently forgetting the sieve step.

**What this settles:** the three-point existential subquestion, with all the source's arithmetic restrictions. **What it does not settle:** m≥4, or prime values of H(t), or sharp asymptotics for the number of such radii.

## Route 3: Gaussian Vandermonde divisibility and imbalance

This independent route addresses all m by arithmetic divisibility, rather than planar area.

Let z_1,…,z_m be distinct Gaussian integers of norm n in A, and set M=binom(m,2) and V=product_{i<j}(z_i−z_j). For each p|n write p=π_p conjugate(π_p). Since n is squarefree, exactly one of π_p and its conjugate divides each z_i, once. Let a_p count those divisible by π_p. Every difference of two points of that type is divisible by π_p, and similarly for the conjugate type. Therefore the integer norm N(V) is divisible by

product_{p|n} p^[binom(a_p,2)+binom(m−a_p,2)].

The minimum of the exponent, for 0≤a≤m, is E_m=floor((m−1)²/4), attained at the most balanced split. All z_i have odd norm, so their real-plus-imaginary coordinate sums are odd. Each difference is divisible by 1+i. As p is odd, the two divisibilities combine to give

2^M n^E_m B | N(V),
B=product_{p|n}p^[binom(a_p,2)+binom(m−a_p,2)−E_m].

Every factor |z_i−z_j|² is at most D², and V≠0. Hence

D ≥ sqrt(2) R^(E_m/M) B^(1/(2M)).

This proves the source's exponents 1/3,1/3,2/5,2/5,3/7 for m=3,…,7 in the restricted class, as a direct special-case proof of the classical Gaussian-product method. More precisely, when m=2s the excess exponent at p is (a_p−s)²; when m=2s+1 it is (a_p−s)(a_p−s−1).

If D≤C R^(E_m/M), then B≤(C/sqrt(2))^(2M). Thus every prime factor exceeding this constant must split the m points as evenly as possible. The proof gives a concrete necessary arithmetic condition on a hypothetical sharp construction. It does not show that all required balanced assignments can coexist geometrically, and it supplies no construction attaining the bound. Finite checks verify exact integer divisibility, not real-power approximations.

## Route 4: the four-point Fibonacci family and its missing arithmetic step

The 2009 paper gives, with F_0=0,F_1=1,F_{j+2}=F_{j+1}+F_j, a four-point family whose squared radius is

N_u=(5/2)F_{2u−1}F_{2u+1}F_{2u+3}.

The points are (F_{3u+3},F_{3u})/2+(−1)^u w_j, with

w_1=2(−F_{u−1},F_{u+2}), w_2=(−F_{u−2},F_{u+1}),
w_3=(F_{u−1},−F_{u+2}), w_4=(F_u,−F_{u+3}).

We use u≥2, so no negative Fibonacci index is needed. The norm identity and O(R^(1/3)) arc bound are credited published results. The middle factor F_{2u+1} is essential; one search-engine transcription omitted it. The inspected publisher PDF includes it, and the exact controls reject that omission.

The three odd indices 2u−1,2u+1,2u+3 have pairwise gcd one. By gcd(F_a,F_b)=F_gcd(a,b), the corresponding Fibonacci numbers are pairwise coprime. Exactly one index is a multiple of three. Fibonacci recurrence modulo 4 has period six, with F_3≡2 modulo 4 and F_1,F_5 odd, so the Fibonacci number at that odd multiple of three has 2-adic valuation exactly one. Divide that factor by 2, obtaining pairwise coprime odd integers G_1,G_2,G_3. Then N_u=5G_1G_2G_3, and N_u is squarefree exactly when all G_j are squarefree and none is divisible by 5.

The recurrence modulo 5 gives 5|F_j exactly when 5|j. Thus the necessary avoidance of 5 occurs exactly for u≡0 or 4 modulo 5. This congruence is not sufficient for squarefreeness: other prime squares must still be excluded. If N_u is squarefree, the norm identity itself makes every prime divisor 1 modulo 4, since N_u is odd and a squarefree sum of two squares. Hence the missing hypothesis is precisely infinite simultaneous squarefreeness of these three Fibonacci-derived factors along the permitted residues.

For u=4 one obtains N_4=98345=5·13·17·89 and the four points (301,88),(304,77),(307,64),(308,59), with squared diameter 890. This is a valid finite example. It is not an infinite admissible subsequence. The polynomial squarefree-value theorem in Route 2 does not apply to recurrence values indexed by u. No claim is made that this criterion is necessary for all possible four-point constructions, or that the unresolved recurrence statement has been proved impossible.

## Route 5: balanced Gaussian products give larger admissible clusters

We now seek a constructive upper bound for arbitrary fixed cardinality. This is a squarefree adaptation of the balanced-sign product idea in Cilleruelo–Granville Section 12, with a deliberately chosen spacing to remove local obstructions.

Fix s≥2, put d=2s, and let B be the product of all rational primes at most 2d. For t≥1 and j=1,…,d define a_j=B(t+j), q_j=a_j²+1 and H_s(t)=product_j q_j. Each q_j is an irreducible quadratic over Q. Their roots −j±i/B are disjoint, so H_s is a squarefree polynomial. For p≤2d, B≡0 modulo p and H_s(t)≡1 modulo p. For p>2d, its degree 2d is less than p and its leading coefficient is nonzero modulo p, so it has fewer than p roots. Hence H_s has no fixed prime divisor. Booker–Browning applies and yields infinitely many t for which H_s(t) is squarefree.

All q_j are odd primitive sums of two squares, so those squarefree values belong to A. For each sign vector σ in {−1,1}^d satisfying sum σ_j=0, define

z_σ(t)=product_{j=1}^d(a_j+iσ_j).

Its norm is H_s(t). There are binom(2s,s) such vectors. On the squarefree subsequence the q_j are pairwise coprime; within each factor, a_j+i and a_j−i are coprime in Z[i], since any common prime would divide 2i and the norm is odd. A Gaussian prime dividing one of these factors occurs nowhere else in the product. Changing σ_j switches that prime to its conjugate, so unique factorization proves that all z_σ are distinct.

Expand in t. The leading coefficient B^d is the same for every σ. The next coefficient is B^(d−1)(B sum j+i sum σ_j)=B^d sum j, also the same. Therefore every difference z_σ−z_τ is a polynomial of degree at most d−2. There are finitely many vectors for fixed s, giving D=O_s(t^(d−2)); all points have positive real part comparable to t^d and small arguments for large t, so the chord-to-arc comparison yields L=O_s(t^(d−2)). Since R=sqrt(H_s(t))~B^d t^d, this is

L=O_s(R^(1−1/s)).

Any fixed m≤binom(2s,s) is covered by selecting m points. In particular, infinitely many admissible circles have six points in an arc O(R^(1/2)). This leaves a real exponent gap from the 2/5 lower bound for five or six points. For m=4 the same route gives 1/2, weaker than the desired 1/3. For larger m the gap remains. The argument is unconditional but uses the published sieve theorem; neither a density formula nor optimality is claimed.

## Remaining target and verification limits

The triple subquestion is settled by a credited consequence. The existence of infinitely many squarefree split radii with four points at scale R^(1/3), or five/six at R^(2/5), and the corresponding optimal general exponents remain unproved in this packet. Route 4 isolates one sufficient recurrence problem; Route 3 supplies necessary balancing conditions; Route 5 supplies a weaker unconditional construction. These are five distinct mathematical routes, not five repetitions of the literature search.

The included standard-library checker performs exact algebraic, divisibility, parity, primitive-norm, Fibonacci and balanced-product tests. It also rejects false mathematical claims and malformed data using explicit exceptions, so normal, -O and -OO runs have the same force. It does not prove Booker–Browning, certify the literature search, or replace the written universal arguments. The separate package validator checks exact inventory and hash pins. Source PDFs, extracts, screenshots, raw datasets and private coordination files are excluded from the public packet. Public source titles, URLs, sizes, hashes and inspection history are provided separately.

## Public references

1. OWR 53/2016, Problem 7, p.3025: https://publications.mfo.de/bitstream/handle/mfo/3557/OWR_2016_53.pdf?isAllowed=y&sequence=1
2. Cilleruelo–Granville (2009), publisher PDF: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/E14DBCBF07B4B98FECF3282E2BA672B5/S0008414X00004296a.pdf/close-lattice-points-on-circles.pdf
3. Booker–Browning (2016), journal: https://discreteanalysisjournal.com/article/732-square-free-values-of-reducible-polynomials ; inspected article version: https://arxiv.org/pdf/1511.00601v3
4. Temur, inspected preprint: https://arxiv.org/pdf/2012.10784 ; version/status page: https://arxiv.org/abs/2012.10784
