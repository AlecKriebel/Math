# Five substantive approaches

These are five mathematical approaches undertaken on 3 October 2026, not a claim about separate external chat sessions or model attribution. Source verification and bounded duplicate checking preceded them and are not counted as proof attempts.

## 1. Fixed-point recurrence and sign-aware recursive objects

Starting with the fixed-point polynomial, derive the exponential generating function and the first-order recurrence. Eliminating its inhomogeneous term gives equation (14), with coefficients `N-r` and `r(N-1)`, where `r=1-k`.

Outcome: for `k=-1`, the two eight-object seeds at sizes four and five yield a nonnegative recursive class at every subsequent size. This construction correctly preserves the two earlier negative odd terms. It does not provide a uniform structural interpretation for arbitrary negative `k`: the small-size coefficients and necessary seeds can have mixed signs. The sign sequence is not `(-1)^N`, as the exact values at sizes three and five demonstrate. These recurrences are credited as prior art, including OEIS at `k=-1`.

## 2. Symmetric histories and integer square decomposition

Construct the permutation-to-history map by maintaining two lists of open arcs and prove its inverse. Move one label from each downstep to its matched upstep to obtain a reversal-invariant labeling. The resulting signed matrix has diagonal `2h+k` and adjacent entries `h+1`.

Outcome: a fully specified signed bijection, the matrix identity `A(N,k)=(J^N)00`, and the even square sum (8). The explicit coefficient formula (9) is checked independently. This explains even positivity combinatorially at the linear-algebra level, but a square of a signed count is not yet an explicit unsigned family. That gap motivated approach 3. The classical history and Laguerre ingredients are not presented as new.

## 3. Global prefix cancellation and a transported almost-bijection

Order equal-length/equal-endpoint prefixes lexicographically and cancel opposite signs by a stack. All surviving prefixes at a given endpoint have the same sign. Cutting a closed even history in half then allows a sign-reversing involution: change the first matched half, or, if none, the second matched half. Its fixed points are positive ordered pairs of survivors. Transport the involution back through the explicit permutation bijection.

Outcome: Theorem 1, a complete algorithmic finite-set answer to the even-size subquestion for every integer `k`, without defining a set as an initial segment of `[A(2n,k)]`. The cancellation is nevertheless generic and global. It does not assert naturalness, efficiency, or a local permutation rule. The packet retains an overall partial status rather than silently treating this weak interpretation as a resolution of every intended aspect.

## 4. Local two-step contraction and its exact obstruction

Compute `J^2` symbolically. At `k=-1` it is entrywise nonnegative, yielding an explicit finite-band colored graph. Compute `J^5e0` and use its positive terminal weights to cover all odd sizes at least five in the same graph. Try to extend the model by diagonal sign switching for more negative integers.

Outcome: Theorem 2 and the odd extension give local walk models for every nonnegative value in the `k=-1` sequence. Proposition 3 supplies a negative-product triangle for even negative `k` and a four-cycle for odd negative `k<=-3`, proving that diagonal sign switching cannot fix `J^2` in those cases. This is a method-specific obstruction, not a counterexample to any broad interpretation claim.

## 5. Laguerre linearization, eventual transfer positivity, and odd boundaries

Compute the triple Laguerre generating function `1/(1-uv-uw-vw-2uvw)`, giving nonnegative integer linearization coefficients with a direct word model. Bound the negative portion of the Rodrigues integral uniformly in endpoint height and show `c(N,h;k)>0` for `N>=4(1-k)-1`. This implies entrywise nonnegativity of `J^N` at the same threshold. Use fixed blocks of size `4(1-k)` and finite nonnegative terminal vectors to define an unsigned graph model for every larger size.

Outcome: Theorem 6 and (19), covering all negative integers in an eventual size range. Independently, the derivative and odd-partial-sum increments establish a unique real root at each odd size and at most one odd-size sign crossing for each fixed negative parameter. The unequal-half residual products can still have mixed signs, even when their total is positive. The remaining all-size structural question is not closed.

## Verification and final boundary

The deterministic standard-library checker passes 124,917 assertions on the final author files. It tests the actual forward/inverse maps and the full cancellation involution, not merely a recurrence copied from the manuscript. It also compares direct polynomial factorial integrals with the Laguerre word coefficients and checks the eventual graph formulation. Finite checks support the universal arguments; they do not supply their proofs.

Final author status: **partial, original all-size interpretation problem unresolved; five approaches complete**. No claim of historical novelty or human peer review. Freeze the author files and obtain a fresh independent audit before any remote mutation or acceptance.
