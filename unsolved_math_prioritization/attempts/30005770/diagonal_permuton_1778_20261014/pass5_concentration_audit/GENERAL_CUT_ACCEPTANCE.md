# Independent acceptance: exact cut states and bounded-width gaps

Final shared PASS5, 14 October 2026.

Reviewed: `pass5_general_cuts/EXACT_CUT_STATES_AND_CONTEXT_OBSTRUCTION.md`, SHA-256 `01040a02521559ea6015e1928db860c7d6921f288b23cb356b8948ac0afa4fbc`.

**Accepted as an exact state theorem, a fixed-width growth theorem and a completion-context obstruction.** None determines the scale of crossing width relative to n.

## Completion equivalence and state sufficiency

The profile remembers the standardized pattern and every selected point's row-strip and value-strip labels for all closed subsets of size at most m. A new forbidden occurrence must involve at least one point outside the old closed interior, so it uses at most m old closed points. The descriptor preserves comparisons with the crossing points: only upper crossing positions and lower crossing values require strip data; all other comparisons with the closed interior are forced by quadrants. This proves equality of the full completion languages under the stated fixed supports, not merely an approximate count.

The two endpoint permutations retain the future-value order of upper crossings and the future-position order of lower crossings. No comparison between these two different coordinate orders is needed: the upper crossings lie left and above the lower crossings. A closing endpoint must have least future rank. The five cases exhaust the possibilities for the new row and new value, and all stated insertion-rank multiplicities are correct, including k=0 and k=1.

Opening and diagonal points are newly known; closing points were already known. Testing any new forbidden occurrence therefore requires at most m old closed points, together with the finite boundary and new set. In the profile update, old row/value cuts only disappear or receive an appended final cut. A newly closed upper point is at an old row cut and above all old closed values; a newly closed lower point is at an old value cut and after all old closed rows. Their mutual relation is forced. Hence an old descriptor plus the chosen newly closed points determines the new pattern and strip labels, and every produced descriptor has a genuine old witness. Boolean existence suffices; multiplicities are carried by the number of histories, not by the profile.

The inverse exposure history assigns exact future coordinates when endpoints close. Termination at width zero leaves every row and value assigned once. A forbidden pattern would be detected when its last previously unknown point first becomes known; actual avoidance never triggers a rejection. Thus the history count is exact and quotient transitions retain their necessary multiplicities. It would be incorrect to put a uniform law on the compressed states, and the note does not do so.

## Rationality and strictness

At fixed K, the finite state bound is explicit. Initial and terminal vectors are different: every reachable width-zero profile is a valid terminal state, not just the empty profile. The finite matrix resolvent therefore gives the exact rational series A_K.

Direct sum preserves the maximum crossing width and target avoidance. The bounded-width counts are positive and supermultiplicative, so their growth limit exists with 1<=lambda_K<=lambda. The unique direct-sum decomposition remains inside the bounded-width class, which gives A_K=1/(1-I_K) coefficientwise and analytically below rho_K.

A rational nonnegative series of finite positive radius has a singularity at its positive radius; because it is rational, this is a pole. Its values on the positive real axis tend to infinity. Consequently I_K(z) increases to one as z increases to rho_K. This step does not suppose a simple pole, an irreducible matrix, or a uniform spectral gap.

The proposed new block is valid in each alpha case. If alpha is not increasing, it has at least one descent, and alpha skew-sum1 has at least two. Patterns cannot gain descents, so the two increasing blocks in skew order avoid the target. If alpha is increasing of length at least two, the decreasing block avoids the target's ascent. Both blocks are sum indecomposable, have size 2K+2 and width K+1, and are genuinely absent from the old indecomposable set.

Thus 1/(1-I_K-z^(2K+2)) counts an injective actual subclass. Its positive denominator vanishes at an r strictly below rho_K, since I_K tends to one there and the additional monomial is positive. The subclass radius is at most r, proving lambda>lambda_K. No assertion about the full infinite transfer's spectrum is needed.

For each fixed h, fixed-length concatenation of arbitrary C_h blocks is injective and has crossing width at most floor(h/2). Taking the growth limit along multiples of h gives lambda_floor(h/2)>=a_h^(1/h); supermultiplicativity of the full class yields sup_K lambda_K=lambda. This supremum need not be attained, and no convergence rate is claimed.

The exact logarithmic probability limit is log(lambda_K/lambda), since both counting sequences have growth limits. It proves exponential rarity of every fixed bounded width. It neither proves nor disproves W/n tending to zero.

## Exponentially different positive completion counts

For alpha 2143, the last singleton 1 makes avoidance of 32541 equivalent to 2143-avoidance of the preceding entries. The initial maximum cannot participate in 2143, whose first entry is not its maximum. The increasing initial pair cannot be part of the first descending pair of a crossing 2143 occurrence, while the decreasing initial pair creates 2143 with any later inversion. Thus the two completion counts are exactly b_N(2143) and one.

Skew sums of increasing blocks supply 2^(N-1) distinct 2143-avoiders for N>=1: their unique skew decomposition indexes compositions, and a later decreasing pair cannot lie above an earlier pair. This proves an exponential ratio while both counts are positive. The two cut states have identical width-one crossing coordinates, free supports, endpoint orders and boundary allocations. Their two-point closed profiles differ, as the repaired state correctly records.

This refutes a subexponential comparison based on the boundary alone, even at width one. It does not produce macroscopic crossing mass or a uniform-limit counterexample. The upper crossing order is alpha-free; no unproved alpha-free condition on the lower crossing order is used.

## Unresolved estimate

The number of profile states is bounded only after fixing width as well as alpha. The exact infinite transfer still has incoming-history and outgoing-completion weights, and its finite-width rates have no established width-uniform approximation. The missing theorem concerns width proportional to n. Rationality at each fixed K and exhaustion of the growth constant do not establish it.
