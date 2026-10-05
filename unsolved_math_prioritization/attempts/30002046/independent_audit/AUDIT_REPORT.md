# Independent adversarial audit: 30002046 / OWR-11784-003

## Verdict

PASS WITH SCOPE LIMITS. The frozen packet's stated partial results and exact calculations pass independent review. The intended solution-count question remains unresolved within this investigation after five substantive approaches (5/5). This is neither an exact-count solution nor a uniqueness, transcendence, novelty, or current-global-openness certificate.

The audited input is the eight-file packet bound by the 1493-byte MANIFEST.json with SHA-256 `faf4f5f3d6069420dd4a975a6320e704bdb6f190f64a1626863c5ff1e08bd045`. All payload hashes matched before and after the independent computation. No originals were changed, no helpers were delegated, and no remote writes were performed.

## Problem and source boundary

The [OWR primary report](https://ems.press/content/serial-article-files/46395), printed page 1323, was independently checked in text and visually. Its question concerns the number of solutions of the question-mark fixed-point equation. The paragraph itself does not specify a real-line extension. This audit follows the standard function on [0,1], consistently with the paper and the frozen packet. Counting integer-translated roots of a different real-line extension would not answer this intended problem. Transcendence and computability are also different questions.

Fresh retrievals of OWR, the [Gayfulin–Shulga arXiv v2](https://arxiv.org/abs/1811.10139), and the [2025 Hussain–Smith–Zhang paper](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.699.pdf) exactly reproduce the recorded PDF sizes and SHA-256 values. Relevant rendered pages were inspected. The exact aggregator page again returned HTTP 403. Its wording and all unavailable raw corpus content/hashes remain unverified. The reported earlier repository-history search was not independently rerun.

Gayfulin–Shulga's Theorem 4 is a conditional sufficient criterion: eventual displacement greater than 1/(2q²), interpreted for reduced nontrivial rational arguments in the unit interval. Its literal abbreviated integer quantifiers omit this necessary context; arbitrary unreduced presentations of 1/2 would violate the inequality for arbitrarily large denominators. The Appendix examines an orbit limit, alternation of convergents and their digits, then invokes a derivative theorem. The packet does not claim to reprove that sharper result. Its own 1/q² theorem is separately proved. The first three imported theorems concern the smallest or greatest lower-half fixed points, not every fixed point. The source's 5400-digit and denominator-30000 experiments are reported evidence, not independently replayed here. The [publisher page](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/195/4/113663/diophantine-properties-of-fixed-points-of-minkowski-question-mark-function) verifies the 2020 publication; the journal PDF was not read.

The 2025 paper's cited digit-sum restriction likewise concerns extremal fixed points. Its exceptional-set dimension statements impose their own digit-growth conditions; they cannot be converted into a count of the fixed set. Its historical statement that the conjecture was unproved is not a 2026 literature-completeness certificate. Other source-inspection boundaries are recorded in SOURCE_AUDIT.json.

## Definition, continuity and arithmetic

The finite continued-fraction formula is correctly normalized, including Q(0)=0 and Q(1)=1. A final digit split a into a−1,1 preserves the value; the terminal numerator is odd over denominator 2^(S−1). The independent verifier uses an accelerated subtractive-Euclid binary address, not the author's series routine, and compares that construction against an independently coded reversed continued-fraction evaluation for every scanned rational and both finite expansions.

The ordered Stern–Brocot endpoint assignment has shrinking meshes in both domain and range. At depth n the domain interval length is at most 1/(n+1), and every image interval has length 2^−n. These facts give a continuous strictly increasing homeomorphism. No jump discontinuity or lost limit point is being hidden in the use of the intermediate value theorem. Reflection and the left-branch identity are correct.

The Fibonacci denominator bound at tree depth S−1 gives q ≤ f_(S+1) < 2^(S−1) when S ≥ 3. Thus the exact rational fixed set is {0,1/2,1}. Boundary cases S=1,2 and x=0 were checked separately. The proof uses the standard Fibonacci convention consistently. An eventually periodic continued-fraction tail maps to a rational geometric series, so Lagrange's theorem excludes every quadratic irrational fixed point. This does not exclude algebraic degree at least three and does not prove transcendence.

## Global signs and complete root coverage

The negative partition covers every point in (0,2/5], including the infinite tail at zero. The n=3 equality possibility in the bound is explicitly resolved by Q(1/4)=1/8. The remaining negative pieces meet without gaps. The positive partition covers [3/7,1/2), including the infinite sequence n/(2n+1) approaching 1/2. Its initial equality endpoint is also correctly resolved. The tail inequalities follow by induction; finite checks through n=1000 are only implementation controls.

Consequently the lower-half fixed set K is nonempty, compact and contained in (2/5,3/7). Reflection and the rational endpoint classification give the full set {0,1/2,1} ∪ K ∪ (1−K). There are at least five distinct roots. A finite cardinality m for K would give 3+2m roots, but finiteness and m=1 are not established.

For each terminal [a,b], monotonicity places every graph point inside [a,b] × [Q(a),Q(b)]. A recorded negative certificate Q(b)<a or positive certificate Q(a)>b excludes every root in that interval, including boundary roots and contacts without a change of sign. The full leaf partition has matching successive endpoints, no omitted segment, and exact first/last endpoints 2/5 and 3/7. Mediant determinants, endpoint images, subdivision depths and strict exclusion reasons were independently checked, and the entire subdivision was rebuilt breadth first.

Result: 275 nodes, 138 terminal intervals, 137 excluded intervals, and one retained interval at depth 128:

- Left: 196891866281783104237450 / 468374932927154430517551
- Right: 73080867820262788865501 / 173847946133977969489589
- Width: 1 / 81426020110025487843678548887211712316576276539

All of K lies there. Exact endpoint signs also prove it contains at least one root. Exact integer floors verify the common 44 decimal digits 42037233942322307564099300664622187394918986. No floating-point sign, approximate arithmetic, derivative estimate or assumed one-crossing behavior was used.

One interval is not one root. The checker includes a strictly increasing synthetic graph with three fixed points within this same tiny interval and opposite endpoint signs. A normalized strictly increasing polynomial with an even-order, sign-preserving contact verifies that the exclusion logic retains such a root. Analytic multiplicity is not assigned to the singular question-mark function. Multiple roots, tangencies and infinite fixed subsets are not eliminated by the certificate.

## Computable selection and the remaining approaches

Arithmetic bisection is valid because each midpoint is rational in (2/5,3/7), and the rational classification proves its displacement is nonzero. Evaluating that displacement uses terminating integer arithmetic; there is no undecidable equality test on an arbitrary computable real. Each retained half has opposite endpoint signs and width 1/(35·2^n). Nestedness and this explicit modulus determine one computable limit. Continuity makes it a fixed point; the arithmetic and periodic-tail proofs make it irrational and nonquadratic. Every step of the separate 160-step run was replayed and its trace retained. The final bracket lies within the complete-root enclosure. The selected limit need not be the least, greatest or sole root.

The orbit argument between two hypothetical roots is sound. A rational starting point cannot be fixed. Strict monotonicity keeps its iterates inside the two-root bracket; they converge monotonically to a root, with no root in the intervening one-sided basin. Hence secant slopes there lie between zero and one. This proves the stated conditional uniqueness implication if every point of K has derivative +infinity; that hypothesis is not proved.

The rational derivative proof also passes. Successive parent mediants have distance 1/[q(nq+v)] while their Q-distance decreases by 2^−n. The given bound covers every sufficiently small one-sided increment, not merely the displayed sequence. Both parents give Q'(r)=0 at each interior rational. Therefore F cannot be nondecreasing on any open interval. The exact local decrease control is valid. The branch correction term is correctly negative, so graph self-similarity does not preserve the diagonal fixed-point equation.

The separate 1/q² displacement criterion follows from infinitely many upper or lower convergents entering that basin, with errors strictly less than 1/q². Reduced denominators grow without bound, allowing the eventual assumption to be applied. The gcd separation estimate follows from a nonzero integer numerator; its exponentially large dyadic denominator prevents an unproved polynomial lower bound from being inferred.

## Exact tests, negatives and reproducibility

All 342090 reduced rationals with 0<p/q<1/2 and q≤1500 were independently enumerated. The only scaled displacements q²|Q(p/q)−p/q|≤1/2 are 3/7 (value 7/16) and 8/19 (value 19/64). Values strictly below one occur at 1/3, 2/5, 3/7, 8/19 and 66/157. These are finite results; no all-denominator or eventual estimate follows.

Six deliberately corrupted certificates were rejected: an omitted leaf, a false endpoint image, a false exclusion of the retained interval, a false width, an invalid depth and an incorrect node count. Additional negatives check same-sign endpoints surrounding a genuine root, sign-preserving contact, three roots inside the tiny interval, unreduced trivial exceptions, local nonmonotonicity and the noninvariant diagonal.

The author verifier also reproduced EXACT_RESULTS.json byte for byte (56064 bytes, SHA-256 f834dcd981bbe6c97408139b1a7bce1ee7631f4e1d94e2b7c3d5e9bb63c4c728). The independent verifier imports no author functions and uses explicit checks that remain active under Python optimization. Its output includes the full independently regenerated certificate and all bisection midpoint signs.

## Controlling audit clarification

PROOFS.md says that strict rectangle inequalities are required. More precisely, the implementation uses strict inequalities, which are sufficient and sound. Since Q is strictly increasing and [a,b] is nondegenerate, even Q(b)=a or Q(a)=b excludes a root, by treating the relevant endpoint separately. The controlling reading is “The implemented tests use strict inequalities,” not a claim that strictness is mathematically necessary. This clarification does not change any retained proof or numerical certificate. The frozen original was preserved; the audit governs this overstatement. No uniqueness inference is licensed.

## Final boundary

All five approaches have genuine retained results and explicit remaining gaps. None proves the exact fixed-point count, uniqueness or transcendence. The certificate and finite scan must not be promoted to such a claim. Source PDFs, extracts, images, raw records, private sources, personal data and coordination files are excluded from the deliverable. The audit is AI-assisted, unrefereed verification of this bounded packet, not a formal proof-assistant certificate or independent verification of every cited external theorem.
