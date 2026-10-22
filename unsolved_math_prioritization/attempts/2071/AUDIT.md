# Bounded audit of the EP357 partial bounds

## Edition and review scope

These AI-assisted authored documents and their independent internal AI audit are unrefereed. Acceptance here means the bounded mathematical assessment described below. No external human peer review, journal acceptance, formal proof-assistant certification, comprehensive priority search, novelty or priority certification is claimed. The two main bounds are prior results credited to Paratelligent Research Agent and Jeff Pickhardt.

This prose-only edition preserves the full mathematical audit. Finite-check statements report historical checks completed on 10 October 2026. Programs, detailed output files and copied source documents are not distributed. Edition preparation performs no new mathematical-program execution or scholarly-source inspection.

## Decision

The two principal bounds in the five-page version 1 manuscript by Paratelligent Research Agent and Jeff Pickhardt are accepted as mathematically justified prior partial results within this independent, bounded audit:

- liminf f(n)/sqrt(n) >= 4/sqrt(3).
- For every positive integer R,
  f(n) <= ceil(n/2) + floor(n/(2R)) + R(R-1)/2.
  Consequently f(n) <= n/2 + ((3/2) 2^(-2/3) + o(1)) n^(2/3).

No mathematical correction is needed in Theorem 2.1, Corollary 2.2, Lemma 3.1, or Theorem 3.2. Theorem 1.1 follows from those results. This is an authored mathematical audit, not formal certification or human peer review. It makes no novelty or priority claim. The results do not establish f(n)=o(n), do not determine the order of growth of f, and do not assert f(n)~n/2.

The historical attribution requires a qualification: the inspected Coppersmith–Phillips publisher abstract establishes its stated upper bound under an increasing-order hypothesis. It supports the corresponding bound for f, but by itself does not establish the manuscript's displayed bound for the arbitrary-order function g. The full CP96 proof was not accessible in this audit. Thus the g-bound is **not verified here**, rather than disproved. This qualification has no effect on the new proofs, which are self-contained.

## Source and exact target

The audited source is [New Bounds for Sequences with Distinct Consecutive Sums in Erdős Problem 357](https://paratelligent.com/research/papers/new-bounds-for-sequences-with-distinct-consecutive-sums-in-erds-1hwQTOM4/pdf), five PDF pages, dated July 14, 2026 on its title page. The public landing page records August 31, 2026, 03:34:29 UTC as its publication timestamp. The PDF has 61,836 bytes and SHA256:

632302d4350145aa1b3970bd37b35f01cabc733ddafda191af959a5f5f43e411

The PDF byline names both Paratelligent Research Agent and Jeff Pickhardt; the landing-page structured author field lists Jeff Pickhardt. The distinct date and authorship fields are reported separately, not normalized into a fictional journal publication. All five PDF pages were read and visually inspected. No source-supplied code was executed.

For n a positive integer, a candidate is an integer sequence

1 <= a_1 < ... < a_k <= n.

It is valid when the k(k+1)/2 indexed sums a_u+...+a_v, 1<=u<=v<=k, are all different. The extremum f(n) is the maximum possible k. Singleton blocks are included; the empty block is not. Intervals may overlap, and collisions between different lengths are forbidden as well as collisions within one length.

The finite question appears on printed page 58, PDF page 54, of [Erdős and Graham's 1980 book](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf). The related infinite-sequence questions on printed page 70, PDF page 28, of [Erdős 1977](https://www.renyi.hu/~p_erdos/1977-27.pdf) are not substituted for this uniform finite extremal statement. Both decisive pages were visually checked.

A useful logical clarification is that a weakly increasing sequence satisfying this exact all-blocks condition is necessarily strictly increasing: repeated terms already collide as singleton blocks. Thus replacing strict increase by weak increase while retaining every singleton does not change f. Dropping order is genuinely different. For example (1,3,2) has six different block sums, whereas sorting it gives 1+2=3. Neither sorting an unordered construction nor imposing a different convention about singleton blocks is an authorized reduction of the target.

## Reconstruction of the lower construction

Fix positive integers k and B. Starting at zero, list the first k nonnegative integers y_i with y_i not congruent to -B modulo 3, and put a_i=B+y_i. These are positive integers in strictly increasing order. The actual a_i alternate between residues 1 and 2 modulo 3; their adjacent gaps alternate between 1 and 2. No assumption about which retained residue appears first is needed.

### Equal and adjacent lengths

For a fixed block length L, moving the starting index one step to the right changes the sum by a_(j+L)-a_j>0. Therefore equal-length blocks cannot collide, including the length-one blocks.

An even-length block has sum 0 modulo 3, while an odd-length block has sum 1 or 2 modulo 3, since pairs of consecutive retained residues sum to 0. In particular blocks whose lengths differ by one cannot collide. This is a direct reconstruction of the manuscript's offset congruence argument; it also makes clear that every odd length difference is excluded. This observation is used only to audit the reported result, not to claim a new bound.

### Larger length differences

Suppose, for contradiction, that a block of length r and a block of length ell have the same sum, where r=ell+h and h>=2. Let Y_r and Y_ell be their offset sums. Then

hB=Y_ell-Y_r.

Because all offsets are nonnegative, any r-block has offset sum at least that of the first ell offsets. The largest ell-block uses the last ell offsets. Thus

hB <= sum_(j=1)^ell (y_(k-ell+j)-y_j).

Alternating gaps give, for every permitted j,d,

y_(j+d)-y_j <= ceil(3d/2) <= 3d/2+1/2.

Consequently the preceding right-hand side is at most

Q(ell)=ell(3(k-ell)/2+1/2).

The exact completed-square identity is

Q(ell)=3k^2/8+k/4+1/24 - (3/2)(ell-k/2-1/6)^2.

It follows that every such collision would require

B <= 3k^2/16+k/8+1/48.

The manuscript assumes the stronger strict inequality B>3k^2/16+k/8+1, so this is impossible. This proves Theorem 2.1 exactly as stated. The slack between 1 and 1/48 is harmless. The proof covers all interval positions, including intersecting blocks and blocks touching either endpoint. For k=1 the condition is sufficient but unnecessarily strong; no exception is needed.

### Passage to all n

For any fixed 0<c<4/sqrt(3), take a large integer N, set k=floor(cN), and choose B=N^2-4N. B is a positive integer for N>=5. Since 3c^2/16<1, the quadratic term in B eventually dominates the sufficient threshold. Also y_k<=3k/2+O(1), and 3c/2<2sqrt(3)<4, so B+y_k<=N^2 for all sufficiently large N. The construction therefore gives f(N^2)>=floor(cN).

For arbitrary large n use N=floor(sqrt(n)) and the inclusion [1,N^2] subset [1,n]. This yields f(n)/sqrt(n)>=c-o(1). Letting the fixed c approach 4/sqrt(3) proves the asserted liminf bound. One must not set c equal to the endpoint in the displayed choice of B, since the leading-order strict margin would then disappear. The manuscript correctly uses c below the endpoint.

## Reconstruction of the upper bound

Let a be any valid sequence in [1,n], and let A(x) count its terms not exceeding x. For real 0<=U<V and integer r>=1, define

m_r=A(V/r)-A(U/r).

These are precisely the terms in (U/r,V/r]. Increasing order places them in one consecutive index range. If m_r>=r, that range contains m_r-r+1 indexed r-blocks; otherwise it contains none. Each selected block has sum strictly greater than U and at most V. Across all selected lengths 1 through R, all these indexed blocks have different sums, by validity. They occupy integer values in (U,V], whose number is floor(V)-floor(U). Hence

sum_(r=1)^R max(m_r-r+1,0) <= floor(V)-floor(U).

This proves Lemma 3.1. The half-open endpoints are correct even when U or V is an integer, and the proof allows R to exceed k. Positivity, integrality, monotone order, and cross-length uniqueness each have a specific role; counting many distinct sums without full uniqueness would not justify the sum of the layer counts.

Set U=n/2 and V=n, and write M_r for the number of terms in

I_r=(n/(2r), n/r].

For consecutive r, the intervals touch or overlap because n/(2r)<=n/(r+1). Their union for 1<=r<=R is exactly (n/(2R),n]. At most floor(n/(2R)) terms lie outside that union: terms are distinct positive integers. Multiple coverage inside the union only increases the sum of the counts. Therefore

k <= floor(n/(2R)) + sum_(r=1)^R M_r.

For each r,

M_r <= max(M_r-r+1,0)+(r-1).

Applying the proved lemma bounds the sum of the maxima by n-floor(n/2)=ceil(n/2). The remaining loss is sum_(r=1)^R(r-1)=R(R-1)/2. This is exactly the finite inequality in Theorem 3.2, for every R>=1 and every positive integer n. Its occasionally weak small-n values cause no problem; the separate trivial bound k<=n remains available.

Finally let t=(n/2)^(1/3) and R=ceil(t)=t+O(1). The nonconstant terms of the finite bound satisfy

n/(2R)+R(R-1)/2 = (3/2)t^2+O(t).

Rounding the floor and ceiling contributes only O(1). Since t^2=2^(-2/3)n^(2/3), the coefficient is (3/2)2^(-2/3), approximately 0.9449407874. Thus the upper statement is justified with an O(n^(1/3)) remainder after the displayed leading error term, which certainly implies the manuscript's o(n^(2/3)) remainder. This is an algebra check of its choice of R, not a separate improvement claim.

## Dependencies and historical scope

The lower theorem uses only integer arithmetic, the two retained residues, strict increase, nonnegative offsets, and a quadratic maximum. Its corollary uses only monotonicity of the extremal function and elementary limits. The layer lemma and upper theorem use only elementary interval counting and the exact uniqueness hypothesis. No cited external theorem enters either proof. Therefore unresolved bibliographic scope questions do not create a missing logical dependency in Theorem 1.1.

The stronger admissible-set condition in the introduction concerns sums of different numbers of distinct elements, without requiring those elements to form a block. An admissible set, sorted increasingly, is indeed valid: unequal lengths are separated by admissibility and equal-length block sums increase with their starting index. The top-interval lower constant 2 can also be checked directly. For k consecutive integers ending at n, the minimum sum of r+1 terms minus the maximum sum of r terms equals

n+r^2+r+1-(r+1)k >= n+1-(k+1)^2/4.

For k=(2-epsilon)sqrt(n)+O(1), this is eventually positive. All consecutive cardinality layers are then separated, which suffices for admissibility. The [Deshouillers–Freiman 1995 publisher abstract](https://link.springer.com/article/10.1007/BF02762069) confirms the matching asymptotic upper constant 2 for admissible sets and credits the sharp lower constant to Straus. Their full 1995 proof and Straus's 1966 proof were not re-audited. The 1999 sequel's introduction independently corroborates the attribution; its later arguments are outside this audit.

The [Hegyvári 1986 publisher record](https://doi.org/10.1007/BF01949064) verifies the title, year, journal, and pages. Its full proof was not inspected. The manuscript's historical g(n) bounds are therefore reported as prior attributions rather than independently reconstructed theorems here.

The [Coppersmith–Phillips 1996 publisher abstract](https://epubs.siam.org/doi/10.1137/S0895480193244139) states its restriction for an increasing sequence and obtains the coefficient 2/3-1/512. A valid EP357 sequence satisfies that weaker restriction, because any equality of a multi-term block to a singleton would violate validity. This gives the old bound for f. The inspected source does not establish the transfer to arbitrary-order g. A full-proof argument or a separate source is needed before retaining that stronger attribution as verified. Failure of sorting, exhibited above, rules out a silent sorting reduction; it does not disprove the asymptotic g-bound.

[Beker 2023, arXiv:2311.10087](https://arxiv.org/abs/2311.10087), concerns EP356, the existence of increasing sequences having a positive constant times n^2 different block sums. Its Proposition 1.5 bounds the number of different sums by ((e^2-1)/(2(e^2+1))+o(1))n^2. Combining that statement with full uniqueness gives the weaker bound f(n)<=(sqrt(tanh(1))+o(1))n, whose coefficient is about 0.8726936209. That deduction is legitimate as a consequence of the stated proposition, but it is neither sublinearity nor stronger than the older CP96 bound for f. This audit checked Beker's statement and scope, not all of his proofs. The original paper explicitly identifies EP356.

## Finite validation and limitations

The historical authored checker used exact integers and fractions. It enumerates every indexed block, including singletons, and independently checks its incremental enumeration against direct enumeration of all subsets for n<=10. It checks the residue construction for every k from 1 through 300 and six bases immediately above the stated sufficient threshold; checks neighboring residue layers over a separate low-base range; checks the exact quadratic identity; exhausts valid increasing subsets for n<=22; verifies the finite upper inequality for each such subset and each R<=n+3; and checks the layer inequality on a half-integer endpoint grid for n<=10. Negative controls detect repeated singletons and sorting-induced collisions. Aggregate counts, output identities and match results are reported in VALIDATION_SUMMARY.json. Detailed outputs and witnesses are not distributed in this prose-only edition.

The historical checker used explicit runtime conditions, not Python assert statements. The recorded normal, -O, and -OO runs all passed and have identical output bytes, a match rechecked from their retained historical output files during edition preparation. Those programs were not rerun for this edition. These tests provide finite edge-case evidence; the infinite statements rest on the written arguments above, not on finite testing. No Lean build or other formal-proof check was performed. The original finite computations cannot be executed from the distributed prose-only files alone.

This audit is bounded to the pinned five-page manuscript, its proof dependencies, the exact source interface, and selected public attribution checks. It is not a comprehensive current-literature search. The tracker returned HTTP 403 during this audit; no claim of freshly verified tracker status is made. The manuscript itself explicitly leaves f(n)=o(n) open. No evidence in the inspected material closes that residual question.
