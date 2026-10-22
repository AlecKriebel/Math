# Independent audit: fixed-variable Rado boundedness partial

## Decision

**ACCEPT AS A CORRECT PARTIAL RESULT. THE GENERAL FIXED-ARITY TARGET REMAINS UNRESOLVED.**

The complete submitted proof was independently read and checked. No mathematical defect requiring a correction was found. This accepts the stated conditional bounds, obstruction to one proposed completion, and credited exact-degree example; it does not certify novelty or a resolution of Rado's boundedness conjecture.

Public proof edition: [PROOF_PARTIAL.md](PROOF_PARTIAL.md), 12,562 bytes, SHA-256 `45bcd6f0df116909961fe28b08d498e6ef174922f694416c071bb3e7f6ee6248`.

This is the publication edition of the recorded independent AI-assisted audit. The complete analytic review is preserved. The author proof required no mathematical corrections. Editorial changes reconcile acceptance, bind the public proof bytes, and distinguish historical computational/source observations from edition preparation. No mathematical computation or scholarly-source retrieval was rerun during edition preparation. The manuscript and audit are unrefereed; external human peer review, journal acceptance, and formal proof-assistant certification are not claimed.

## 1. Domain, zero coefficients, and the exact question

All variables range over positive integers and need not be distinct. Colors are allowed to be unused. These conventions are used consistently by the proofs and by the quoted exact-degree construction.

For at least one active coefficient, restriction of a monochromatic solution to active coordinates preserves the equation. Conversely, assign every zero-coefficient coordinate the value of one chosen active coordinate. This gives an extension with the same color. Thus deleting zero coefficients preserves every finite regularity property. If all coefficients vanish, the equation is automatically partition regular. The example with coefficients `(1,0)` correctly prevents treating a zero coefficient alone as a sufficient Rado witness.

For a nonempty active vector, the stated one-equation Rado criterion is exact. Golowich's introduction explicitly states the nonzero-coefficient hypothesis and the nonempty zero-subset-sum criterion. Permutations, nonzero common scaling, and global sign do not affect solutions or monochromaticity.

There is no off-by-one mismatch: if the first avoiding color count is `c`, every coloring with at most `c-1` colors has a monochromatic solution, whereas one `c`-coloring avoids. Hence `M`-regularity forces partition regularity precisely when all finite avoiding numbers in the class are at most `M`. Allowing inactive coordinates makes the at-most-arity and exact-arity versions equivalent after padding. The two problem identifiers are treated as a single mathematical target, not as two independent breakthroughs.

## 2. Finite-distance greedy coloring

At vertex `u`, the greedy construction considers at most one predecessor for each positive distance. It therefore excludes at most `|D|` colors and leaves one of `|D|+1` available. Every forbidden-distance pair is checked at its larger endpoint. Recursion over all nonnegative integers is a genuine infinite-domain construction. The empty distance set is valid and requires just one color. A maximum-degree bound of `2|D|+1` is unnecessary because only earlier neighbors matter.

## 3. Separated valuations

If all coefficient valuations at a single prime are distinct, equality of any two term valuations forces the corresponding variable valuations to differ by a forbidden positive distance. A monochromatic tuple therefore has pairwise different term valuations. Its minimum is unique, so dividing by its prime power leaves precisely one nonzero term modulo the prime. Cancellation is impossible.

There are at most one distance per unordered coefficient pair, so the bound is exactly the asserted `binom(n,2)+1`. Neither the value of the prime nor the sizes of the differences appears in the number of colors. A common coefficient factor merely translates all coefficient valuations and does not change this argument. Separated valuations also imply nonzero sums for every nonempty coefficient subset.

The concrete vector `(1,2,-8)` and its valuation-modulo-four coloring are valid. The large-gap example is covered by the distance graph, without assuming that reduction modulo the variable count always works. That latter shortcut is false: `(1,2,-16)` has the monochromatic solution `(64,8,5)` under `v_2(x) mod 3`. The recorded independent checks included this as a mandatory negative control.

For one active coefficient there is no positive solution, so the least positive admissible universal threshold is `M(1)=1`. For two active coefficients, equal opposing magnitudes give partition regularity, equal signs give avoiding number one, and unequal magnitudes have unequal valuations at some prime by unique factorization. The separated bound then gives avoiding number at most two. The equation with coefficients `(1,-2)` establishes that threshold two is necessary. This verifies `M(2)=2`, including zero-coordinate reductions.

## 4. Cancellation depth and the near-minimum argument

For each nonempty subset, the valuation of its nonzero coefficient sum is at least the minimum coefficient valuation in that subset. Thus the defined depth is a finite integer at least one. For any chosen subset `S`, it gives

`v_p(s_S) <= min_{i in S} alpha_i + kappa - 1`.

The stated distance cardinality is correct. Equal coefficient levels supply at most `kappa-1` positive distances. For each unordered pair of unequal levels, the two ordered differences produce the same absolute-distance set because the offset interval is symmetric. Each such pair contributes at most `2*kappa-1` distances. Overlap can only reduce the count.

In a hypothetical monochromatic solution, let `w` be the minimum term valuation and use the strict set `S={i: w_i < w+kappa}`. This is nonempty. Two term valuations in `S` differ by at most `kappa-1`. Subtracting the coefficient valuations shows that unequal variable valuations would differ by an element of the prescribed distance set. Hence all variables indexed by `S` have a common valuation `v`, and `w=v+beta`, where `beta` is the minimum coefficient valuation in `S`.

The common unit residue can be represented by an ordinary integer `r` coprime to `p`; no unproved p-adic existence statement is needed. The decomposition `x_i=p^v(r+p^kappa z_i)` is integral. Its leading subset contribution has valuation at most `w+kappa-1`. The correction term has valuation at least `w+kappa`, as does every outside term. Consequently the total cannot vanish. This proves the product-color count

`phi(p^kappa) * (|D|+1) <= (p-1)*p^(kappa-1) * [kappa+binom(t,2)*(2*kappa-1)]`.

Every factor has a stated purpose: the distance coordinate synchronizes the near-minimum variable valuations, and the residue coordinate controls cancellation of their coefficient sum. Both the strict cluster boundary and the full residue precision matter. Recorded independent negative controls show failure when the boundary is made closed, the offset distances are omitted, the unit coordinate is dropped, or the depth is reduced by one. These are controls against altered arguments, not defects in the submitted proof.

For the layer corollary, the lowest coefficient-valuation layer in any subset contributes a nonzero unit sum modulo `p`, while all other layers disappear modulo `p` after normalization. Hence every excess valuation is zero and `kappa=1`. At prime two, a repeated layer contains two odd normalized coefficients whose sum is zero modulo two, so the condition is equivalent to having at most one coefficient per level. The prime-independent separated argument is indeed sharper than unnecessarily retaining the unit-color factor.

## 5. Obstruction and scope

For integer `H>=1`, let `P` be the product of `p^H` over primes at most `B`. With coefficients `(1,-(1+P))`, every indicated prime divides neither coefficient, and the only nonsingleton coefficient sum is `-P`, of valuation exactly `H`. Thus the cancellation depth is exactly `H+1` simultaneously at all those primes. The vector is primitive and has no zero subset sum.

The tuple `(1+P,1)` is a positive solution, so one color does not avoid the equation. Every prime divisor of `1+P` is greater than `B` and separates the coefficient valuations, supplying an avoiding two-coloring. This proves the exact avoiding number two. It is an obstruction to uniformly bounded depth over a bounded collection of primes, not an unbounded avoiding-number family. The note preserves this distinction correctly.

The Alexeev--Tsimerman example is explicitly credited. Its odd-denominator clearing, valuation ordering, and pair-based monochromatic substitution agree with the source and were independently checked. Its variable count grows with the avoiding number. It gives the lower bound `M(n)>=n` but says nothing of unbounded avoiding numbers at a single fixed arity. Golowich's simpler-family result is described with the same limitation. No previously known theorem is recast as an original conjecture resolution.

## 6. Recorded source and provenance review

These are observations from the proof review and independent audit on 10 October 2026. Edition preparation performed no new scholarly-source retrieval, source-file rehash, visual inspection, or literature search.

- [Joshua Cooper, Combinatorial Problems I Like](https://people.math.sc.edu/cooper/combprob.html): the Rado paragraph states the threshold formulation used here. The retained complete HTML has the exact submitted hash and byte count.
- [Ben Green, 100 Open Problems](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf): Problem 21 and comments give the fixed-arity formulation, credit the three-variable bound 24 to Fox--Kleitman, and describe higher arities as open. The retained PDF identity matches; the relevant page was also visually inspected.
- [Alexeev and Tsimerman, Equations resolving a conjecture of Rado on partition regularity](https://arxiv.org/html/0812.1314v2): Theorem 1 and its proof support the credited family. [The abstract record](https://arxiv.org/abs/0812.1314) confirms the 2009 version date and 2010 journal citation. The experimental HTML's later rendered date is not mistaken for a new result.
- [Golowich, Resolving a Conjecture on Degree of Regularity of Linear Homogeneous Equations](https://arxiv.org/html/1404.3384v1): the introduction, Theorem 1.1, and conclusion support the applicable criterion, simpler family, and quantifier distinction. [The version record](https://arxiv.org/abs/1404.3384) confirms 13 April 2014.
- The submitted Fox--Kleitman URL did not supply full text in this audit either. The author's specific historical HTTP-404 result is retained as its reported retrieval history; this independent tool returned an internal retrieval error, which is not relabeled as 404. The bound is supported by Green, and neither package claims independent full-paper inspection.

No copied source documents, dataset contents, or private coordination material are distributed. Public source metadata and inspection limits are recorded in SOURCE_METADATA.json and SOURCE_REVIEW.md. These recorded targeted source checks do not establish global literature completeness, novelty, bibliographic priority, or current worldwide openness.

## 7. Recorded exact checks and acceptance limits

During the recorded independent audit, the original checker was replayed normally and with Python optimization; both outputs matched its sealed output bytes exactly. The independently written checker imported no author code and separately reconstructed valuations, subset enumeration, distance sets, and a descending-palette coloring. Its normal and optimized outputs also matched byte for byte. These are recorded results, not computation performed during edition preparation. Programs and raw generated outputs are excluded from this proof-only edition.

Independent coverage includes 258 coefficient vectors and 1,032 prime configurations; 23,608 exact positive-solution coloring checks; 40,708 near-minimum and exact noncancellation checks; 128 distance graphs; 810 distance-cardinality cases; 56 separated-level cases; 88 zero-coordinate extensions; 132 all-small-prime obstruction checks; and 1,330 credited-family pair witnesses through arity 20.

In the recorded checks, nine mandatory mathematical negative controls rejected their altered assumptions. Five additional tamper controls rejected a changed proof byte, unlisted file, missing evidence, altered manifest, and a falsely solved status even after a forged re-seal. The author's own scope guard rejected the forged solved state both normally and under optimization. The checkers used explicit exceptions rather than optimization-removable assertions.

The analytic arguments establish the infinite results; the finite checks diagnose implementations and selected arithmetic instances. The analytic verdict depends on no omitted program, raw output, or dataset. Acceptance does not strengthen the partial hypotheses, infer novelty, certify a full conjecture proof, or imply external human peer review.
