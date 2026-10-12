# Independent audit: unrestricted prefix reductions and one-exception binary hybrids

## Decision and scope

The two accepted mathematical notes pass independent review within their stated scopes:

1. [UNRESTRICTED_PREFIX_REDUCTION.md](UNRESTRICTED_PREFIX_REDUCTION.md) gives an exact one-step extension criterion and count, proves that universal extension first fails when attempting degree 7, derives an exact sign-constrained linear system through degree 2M+1 from a fixed degree-M prefix, and gives a constant-size exact two-step criterion.
2. [ONE_EXCEPTION_HYBRID_OBSTRUCTION.md](ONE_EXCEPTION_HYBRID_OBSTRUCTION.md) proves that if every factor is binary-digit multiplicative except possibly one factor of index a≥3, some coefficient fails the bound by degree 94. Degree 94 is sharp for this union of classes. For fixed exceptional index, the first empty degrees are 94 for a=3, 78 for a=4, and 76 for every a≥5.

The original model keeps every positive-integer factor, has constant coefficient 1 in each factor, and independently chooses every nonconstant factor coefficient from {−1,1}. The target bound is exactly |coefficient|≤1. Neither note resolves the full unrestricted problem. The hybrid obstruction does not cover exception index 1 or 2, nor two or more arbitrary factors. Finite witnesses and finite tree levels do not supply an infinite construction.

The acceptance covers the complete editions, including the final two-step section. The programs, raw labelled states, complete frontier certificates and exploratory outputs used in the historical verification are not distributed in this appendix. This is independent AI-assisted review, not external human peer review.

## 1. One-step unrestricted extension

A degree-(n−1) prefix assigns precisely the signs ε(m,j) with mj<n. At degree n there are d(n) new signs, one for each positive divisor m of n. A new term can only multiply constants at its own degree, so

 a_n = A_n + Σ_{m|n} ε(m,n/m).

Each partition contributes one sign. Reducing modulo 2 therefore gives a_n≡p(n) and A_n≡p(n)−d(n). The fresh sum ranges over every integer of parity d(n) between −d(n) and d(n). Consequently the exact extension condition is

 |A_n|≤d(n)+(p(n) mod 2).

For each permitted target t, the number of labelled choices is binom(d(n),(d(n)+t−A_n)/2), with the usual zero convention outside the integer domain. No labels are lost in this count, and every fresh sign is independent.

The displayed degree-6 example has first-factor signs (−1,−1,−1,−1,+1,+1) and every other assigned sign positive. Direct multiplication of the truncated original factors gives coefficients (1,−1,0,−1,−1,−1,−1) through degree 6 and residual −5 at degree 7. The two fresh signs can only produce −7, −5 or −3 there. The note correctly removes the as-yet-unassigned pure degree-7 term when using the positive tail as an auxiliary calculation.

The algebra excluding earlier dead ends is correct. In particular, feasibility at degree 2 forces x₂+y₁=0; this cancels the relevant terms at degrees 5 and 6. The degree-3 condition implies z₁(x₃+x₁y₁)∈{−2,0}, giving −5≤A₆≤3, within the exact degree-6 threshold. Degrees 1 through 5 satisfy their respective thresholds as claimed. Thus attempted degree 7 is the first possible failure of universal prefix extension; this is not a claim that the entire feasible tree dies there.

An independent enumeration represented coefficients as signed monomials indexed directly by ordinary partitions. It did not call the author's factor-division or polynomial-update routine. The feasible level sizes through degree 9 are exactly

 1, 2, 4, 12, 60, 160, 1268, 2848, 10784, 21354.

The numbers of dead parents when attempting degrees 7, 8 and 9 are respectively 80, 120 and 1446. Every lower attempted degree has zero dead parents. Residual and completed-coefficient parity were also checked explicitly.

## 2. Half-prefix linearization and two-step compression

Fix all signs of weighted degree at most M. Write B for their product and H_m for the product with original factor m deleted. For m>M, H_m=B. Every newly assigned coefficient has degree at least M+1. A product of two new terms from distinct factors therefore has degree at least 2M+2; terms from the same factor are never multiplied at all. Hence for M<N≤2M+1 the exact expansion is

 P ≡ B + Σ_{M<mj≤N} u(m,j) q^(mj) H_m modulo q^(N+1).

Using the factor-deleted cofactor is essential: substituting B for every H_m would introduce illegal same-factor products. The integer system in the note is precisely the coefficient form of this identity. The target is 0 at even partition parity and an independent choice of ±1 at odd parity. It has no relaxation gap because every sign-variable solution gives actual factor coefficients and conversely every completion gives such variables.

The identical-column quotient is exact only within the selected horizon. At a fresh degree k, any divisor m> N−k has F_m≡1 through degree N−k, so its column equals the shifted B-column. Replacing r such labelled signs by their sum in {−r,−r+2,…,r} preserves existence; binom(r,(r+s)/2) preserves the multiplicity of labelled assignments. These labels must not be forgotten when continuing beyond the horizon. The proof does not do so.

The weighted inequality follows by the triangle inequality applied to an actual sign solution. Considering all weights describes membership in the corresponding real zonotope/box image. That convex condition is only a necessary condition for the discrete sign problem, as the note explicitly states.

Independent original-factor multiplication matched the affine identity on 67,042 assignments: every old/new sign assignment for M=1,2,3 at N=2M+1, and 50 deterministic pseudorandom assignments for each M=4,…,12. Negative controls detect both replacing a factor-deleted cofactor by B and extending the affine formula to degree 2M+2: at M=1, the omitted interaction between the new terms in original factors 1 and 2 contributes exactly one unit at degree 4 in an all-positive example.

For the two-step test, let n≥2. A new degree-n term in factor 1 has no degree-one cofactor contribution. A new degree-n term in any other factor contributes x=ε(1,1) times its sign at degree n+1. Thus only the sum s of the new signs outside factor 1 affects the next residual, which is D+xs. Two new degree-n terms cannot interact because 2n>n+1. Testing the at most four pairs consisting of a permitted degree-n target t and the new factor-1 sign e, with s=t−A−e in its exact parity interval, is therefore necessary and sufficient.

This two-step statement was checked against complete labelled descendants of all 4,354 feasible prefixes at degrees 1 through 7. The check compared the exact number of grandchildren, including the binomial multiplicity of each sum s, rather than merely a yes/no result. Every comparison passed.

The compactness argument is also correctly delimited: the tree is finitely branching, so nonemptiness at every degree would give a coherent infinite path. Nonemptiness at one fixed finite degree does not establish the premise, and arbitrary feasible prefixes need not extend.

## 3. Hybrid grouping preserves all allowed products

For a fixed arbitrary factor a, the other factors have independent binary digit signs indexed by (m,r), m≠a. At exponent n=m2^r there are precisely

 d_n^(a)=1+v₂(n)−1_{n=a2^r for some r≥0}

remaining labelled binomials. Counting their positive signs gives the grouped factor (1+q^n)^c_n(1−q^n)^(d_n^(a)−c_n). Every legal count sequence lifts to labelled digit signs by choosing exactly c_n of the available labels independently in each exponent group. Each label belongs to one group only. Rearrangement is valid formally because only finitely many relevant labels exist below any fixed degree.

Crucially, the arbitrary factor's coefficient signs are retained individually, and its entire assigned history is part of each state. They are not substituted by binary digits or collapsed into counts. The state retains the complete count vector as well. Thus correlations needed for later coefficients are preserved; grouping does not identify merely similar product prefixes or unrelated count histories.

As a direct label-control test, every raw labelled assignment through degree 7 was enumerated for a=1,2,3,4,5. The respective raw search sizes were 32,768; 4,096; 2,048; 2,048; 2,048. The feasible labelled counts were 1,710; 448; 280; 280; 280, and their numbers of grouped states were 754; 212; 52; 58; 32. These grouped state counts agree with independent enumeration. Every fibre had exactly the product of binomial multiplicities dictated by its counts. The a=1,2 controls validate the finite encoding only; they are not obstruction claims for those indices.

## 4. Hybrid recurrence, completeness and independent arithmetic

At degree N the new binary group contributes 2b−d_N^(a), and a new arbitrary-factor coefficient contributes e∈{−1,1} exactly when a divides N; otherwise e=0. Both fresh pieces have degree N, so they do not interact at that degree. Testing every legal pair (b,e) against |R_N+2b−d_N^(a)+e|≤1 is exact. Restricting any feasible child gives a feasible parent. Induction therefore proves complete enumeration, without heuristic cutoffs, random pruning, symmetry pruning, or product-prefix merging.

The author's certificate producer multiplies the group polynomials. Independently, a C++ depth-first traversal was written from the grouped definitions before the producer implementation was inspected. It uses the logarithmic derivative of the binary cofactor:

 h_k=Σ_{m|k} m·(2c_m−d_m^(a)) for odd k/m contributions, and m·(−d_m^(a)) for even k/m contributions;

 n b_n=Σ_{k=1}^n h_k b_(n−k).

Every division is checked for exact divisibility. The traversal updates the h-coefficients and backtracks them exactly, retains the arbitrary-factor sign history, and visits every legal count/sign choice. It contains no state cap or branch reduction. The parent coefficient is then computed by convolution with the retained arbitrary-factor coefficients.

Arithmetic is exact. For a retained prefix, writing P=A_a B and using |[q^r]P|≤1 gives |b_r|≤2^floor(r/a) by induction. The implementation's domain is N≤100; its logarithmic coefficients satisfy |h_k|≤Σ_{m≤100}7m=35,350. Consequently its intermediate recurrence numerator has absolute value at most 100·35,350·2^100<2^122, safely within signed 128-bit range. Complete written state files have their lengths counted separately with Python integers. An undefined-behaviour-sanitized C++ build reproduced every result.

The independent traversal wrote every retained state. All 1,791 complete frontier sets in the 23 author certificates were compared exactly against those independently generated states, including root and terminal empty levels. In total, 5,360,203 nonempty states were compared. The checks enforce state lengths, sign/count domains, sortedness, uniqueness, complete level coverage, all counts and every terminal residual. Hashes are integrity checks, not substitutes for complete-set or arithmetic comparison.

The first empty levels are 94 for a=3, 78 for a=4, and 76 for a=5,…,25. The corresponding total state counts for the two large cases are 1,709,525 and 2,887,957. Their largest frontiers are 108,684 and 182,540. All remaining counts and maxima match the table in the frozen note.

## 5. Index reduction and sharpness

For a≥26, only multiplicities 1 and 2, or fewer, can appear from the arbitrary factor through degree 76. Those signs always agree with some binary-digit choice. The earliest possible violation of binary-digit multiplicativity is multiplicity 3, whose degree is 3a≥78. Thus the hybrid matches an all-binary product through degree 76 and is excluded by the prior sharp all-binary theorem. This is a matching argument for a finite prefix, not a claim that an arbitrary sign series is globally binary.

The prior [all-binary proof](../BINARY_CLASS_OBSTRUCTION.md) was authenticated, and the new independent logarithmic enumeration reproduced its entire frontier-count sequence and first empty degree 76. A common all-binary witness through degree 75 proves lower-bound sharpness for every fixed a≥5. The newly checked frontiers give witnesses through degree 77 for a=4 and through degree 93 for a=3.

For every completed finite hybrid case, one terminal surviving prefix was lifted back to labelled binary digits, each original factor's coefficients were reconstructed using binary expansion, and the original factors were directly convolved. All bounds through the claimed last feasible degree hold. All next-degree choices for each reconstructed witness fail.

The standalone a=3 witness, both printed arrays in the note, and its arbitrary-factor positive-sign positions were checked. Its degree-93 prefix is feasible. All four complete degree-93 states have residual R₉₄=−6. Because 3 does not divide 94 and d₉₄^(3)=2, the possible next coefficients are exactly −8, −6 and −4. All later choices can be assigned arbitrarily without changing the verified degree-93 prefix. This establishes sharpness of degree 94 for the stated union of hybrid classes.

## 6. Integrity controls and source limits

Seven malformed-certificate controls were rejected: omission of a feasible state, duplicate state, wrong level, invalid exceptional sign, illegal group count, shortened state, and unsorted frontier. A same-length alteration of the accepted proof was rejected by the integrity check. The independent block controls separately reject the wrong cofactor and an excessive affine horizon.

Normal Python and optimization levels 1 and 2 produced identical complete-certificate verification results. Verification failures use explicit conditions, not removable assertions. The reviewed statements and independent verification evidence were authenticated before acceptance. Those undistributed input inventories and their identities are not included here.

The [Open Problem Garden problem](https://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions) and [Newman's 2013 MathOverflow formulation](https://mathoverflow.net/questions/146359/a-product-related-to-unrestricted-partitions) were independently inspected on 12 October 2026. They confirm the unrestricted sign model and the parity observation. Open Problem Garden reports historical computations to approximately degree 110, so the new degree-93 hybrid witness is not an unrestricted search record. These historical statements do not establish current novelty, and no exhaustive literature-priority claim is certified.

No result is accepted for incomplete exploratory searches at a=1 or a=2. No conclusion about arbitrary two-factor exceptions, the whole unrestricted tree, or an infinite unrestricted solution follows from this audit. No broader mathematical conclusion is implied by acceptance.
