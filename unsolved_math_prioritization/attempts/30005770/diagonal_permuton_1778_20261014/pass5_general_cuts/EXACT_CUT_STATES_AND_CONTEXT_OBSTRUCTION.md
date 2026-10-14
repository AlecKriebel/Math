# Exact diagonal-cut states and an exponential context obstruction

Shared final PASS5, 14 October 2026. This note gives an exact state compression, finite transfers for bounded crossing width, and an actual-class obstruction to dropping closed-interior context. It does **not** prove the universal diagonal limit or produce a uniform-law counterexample. No novelty or human peer-review claim is made.

## 1. Setup and results

Fix α∈S_m with m≥2, let τ=α skew-sum 1, and put C_n=Av_n(τ), a_n=|C_n|. Let λ=lim a_n^(1/n). For π∈S_n and 0≤r≤n define

 k_r(π)=|{i≤r:π(i)>r}|,
 W(π)=max_r k_r(π).

The two crossing directions have equal size k_r. The grid-cut permuton crossing mass is k_r/n. Thus the desired weak diagonal limit is equivalent to W(Π_n)/n→0 in probability under the exactly uniform C_n law. That equivalence is background, not a result established by this note.

The proved advances are:

1. Closed-interior gridded patterns of size at most m, together with the two crossing endpoint orders, suffice for an exact time-homogeneous diagonal-exposure state. There are finitely many states at each fixed width, but not a finite total state space for fixed α.
2. For each fixed integer K≥0, the class C^(K)={π∈C:W(π)≤K} has a rational counting generating function. Its growth rate λ_K satisfies

   λ_K<λ,       λ_K nondecreasing,       sup_K λ_K=λ.           (1)

   In particular, P(W(Π_n)≤K) has negative exponential rate for each fixed K. This says width cannot stay bounded; it does not determine its scale relative to n.
3. Even with crossing width one and identical exact row/column boundary allocations, omitting the closed-interior profile can change positive completion counts by an exponential factor. A concrete example uses α=2143, τ=32541.

The case α=1 has only increasing avoiders of 21 and is separately trivial. It is excluded from the strict inequalities in (1).

## 2. Fixed-coordinate completion equivalence

At a cut r, separate the known partial permutation into

- F: closed points with i≤r and π(i)≤r;
- B: upper crossing points with i≤r<π(i);
- D: lower crossing points with π(i)≤r<i.

Write k=|B|=|D|. The remaining unknown points lie in the northeast square i>r, π(i)>r. If n and all coordinates of B,D are fixed, the free row and value sets for the unknown completion G are fixed. The row/value sets for F are fixed as well. Assume the known partial permutation F∪B∪D already avoids τ; otherwise its completion count is zero.

The row coordinates of B cut [1,r] into k+1 strips. The low values of D cut [1,r] into k+1 value strips. None of those cuts coincides with a coordinate of F. For each h≤m, record the following Boolean data for every h-point subsequence of F, in position order:

- its standardized pattern ρ∈S_h;
- the row-strip index of **each** selected point;
- the value-strip index of **each** selected point.

The empty descriptor is included. Call this the profile P_m(F;B,D). It records occurrence/existence, not the number of witnesses, and does not retain F itself. There are at most

 N_m(k)=sum_(h=1)^m h!(k+1)^(2h)                             (2)

possible nonempty descriptors, so at most 2^(N_m(k)) profiles. Some formal descriptors or profiles are unrealizable; this is only an upper bound.

**Completion-equivalence lemma.** Suppose F and F' have the same prescribed row/value supports, both known configurations are τ-free, and their profiles coincide. Then for every bijection G between the remaining northeast row and value sets,

 F∪B∪D∪G avoids τ  iff  F'∪B∪D∪G avoids τ.                  (3)

**Proof.** Any forbidden occurrence in a completed configuration must use a point of G, since the known part was τ-free. It therefore uses at most m points of F. The descriptor of those selected F points supplies an equally patterned selection in F'. Its row-strip assignments preserve all comparisons with B's positions; its value-strip assignments preserve all comparisons with D's values. All selected F points precede D and G, and have smaller values than B and G. Thus every position and value comparison with the unchanged exterior points is preserved. The same τ occurrence exists after replacement. The reverse argument is identical. QED.

This proves equality of the actual completion languages, not just equality of counts. Counts of witnesses inside F are irrelevant to this existential avoidance test. Multiplicities of histories leading to the same profile remain relevant when counting entire permutations.

## 3. Relative-order exposure and exact transitions

Absolute future endpoint coordinates are unnecessary. At step r retain:

- k;
- the permutation b∈S_k giving future-value ranks of B's points listed in past-row order;
- the permutation d∈S_k giving future-position ranks of D's points listed in past-value order;
- the profile P_m defined above using these ordered row/value cuts.

The state represents only τ-free known configurations. Relative orders of all known boundary points are specified: B is above the cut and left of it; D is below and right. Neither their future endpoint distances nor the sizes of gaps between past cuts are retained. A closed descriptor supplies precisely the comparisons needed with those boundary points.

To expose the next diagonal index r+1, a past upper point can close only if it has the smallest future-value rank, and a past lower point can close only if it has the smallest future-position rank. The five exhaustive cases are:

1. **Open both:** the new row opens an upper point, and the new value opens a lower point. Insert their future endpoints in the existing orders, independently choosing ranks 1,...,k+1. There are (k+1)^2 candidate choices; width becomes k+1.
2. **Close both:** close the least-future-value B point and the least-future-position D point. This is one candidate choice when k≥1; width becomes k−1.
3. **Close upper, open upper:** close the least-future-value B point, then put the point from the new row into the remaining upper future-value order at one of k ranks. Width remains k. This case requires k≥1.
4. **Close lower, open lower:** the symmetric operation on D, with k ranks and k≥1. Width remains k.
5. **Diagonal point:** create the point (r+1,r+1), leaving all old crossing endpoints open. Width remains k. There is one candidate choice.

Distinct choices are retained with multiplicity even if they lead to the same compressed state. At width zero only cases 1 and 5 are available. Some candidates create τ and are rejected.

### Why the compressed state determines the update

First distinguish two operations. A closing B or D point was already part of the known configuration: it is merely reclassified as closed. An opening point or the diagonal point is newly exposed. Any new forbidden occurrence must use at least one newly exposed point. It can therefore contain at most m old F points. Its presence is decided from the old profile and the finitely many boundary/new points, by exactly the comparison argument in (3). Reclassification alone introduces no new forbidden occurrence.

At most two points join the closed interior. A closing B point has a row at a retained old row cut and a new value above all old closed values. A closing D point has a value at a retained old value cut and a new row after all old closed rows. Their mutual order, if both close, is fixed. A new diagonal point is above and to the right of every old closed point.

For every subset of at most m points in the new closed interior, separate its old closed points from its newly closed points. The old subset's descriptor, together with the chosen new points, determines its pattern and new strip assignments. Old cuts are only removed (merging adjacent strips), or new exterior cuts are appended when a point opens. Thus one computes the new profile by taking all old descriptors and all appropriate subsets of the at most two newly closed points. No multiplicity or hidden coordinate is needed for this update. Conversely, every descriptor produced in this way is realized by the corresponding old witness and new points. This proves exactness in both directions.

### Bijection with exposure histories

A permutation gives a unique sequence of the five cases and insertion ranks. An opened endpoint's relative rank is fixed by its eventual value or position. Conversely, a history starting from the empty state and ending at width zero assigns each open endpoint its exact future coordinate when it closes. The resulting points form a permutation: each row and value is assigned exactly once. At every step all order comparisons used in the profile tests agree with those eventual coordinates. Ending at width zero means no unassigned endpoint remains.

Avoidance is exact because a forbidden occurrence would be rejected at the step when its last previously unknown point becomes known. Conversely, a τ-avoiding permutation never produces such a rejection. Thus legal length-n histories from the empty state to width zero are in bijection with C_n.

In particular, profiles are genuine transition states, rather than an assumed sufficient statistic inferred from finite data. The exact induced law must nevertheless retain the number of incoming histories and outgoing completions. Uniformity of a compressed state is never asserted.

## 4. Finite transfers and a strict bounded-width growth gap

At fixed width k, there are at most

 (k!)^2 2^(N_m(k))                                         (4)

states. The α-specific avoidance test reduces this bound; for example, if k>0 the upper crossing permutation is α-free because any lower crossing point supplies a terminal minimum. No analogous general α-free assertion is made about D.

For fixed K, explore reachable legal states of widths at most K. The finite upper bound (4) proves that this exploration terminates. Put the exact transition multiplicities into a finite nonnegative integer matrix M_K. Let e denote the initial empty state and let v have entry one at every width-zero state. Then the ordinary counting series is exactly

 A_K(z)=sum_n a_n^(K) z^n = e^T(I−zM_K)^(-1)v.               (5)

It is rational. The multiple terminal profiles are intentional: different completed permutations need not have the same small-pattern profile.

Direct sum takes the maximum of the two crossing widths. Hence C^(K) is direct-sum closed, and its counts are supermultiplicative. It contains every increasing permutation, so 1≤λ_K≤λ<∞, the growth limit exists, and its radius is ρ_K=1/λ_K.

### Strictness for every fixed K

Let I_K(z) count direct-sum indecomposable members of C^(K). The unique direct-sum decomposition stays inside this class, giving

 A_K(z)=1/(1−I_K(z)).                                      (6)

A rational series with nonnegative coefficients and finite positive radius has a pole at its positive radius (Pringsheim), and its values tend to infinity there. Consequently I_K(z) increases to 1 as z increases to ρ_K.

There is an explicit sum-indecomposable member γ_K of C with width K+1 and size L=2K+2:

- If α≠I_m, take γ_K=I_(K+1) skew-sum I_(K+1). It has one descent, whereas τ has at least two. Descents cannot increase under taking a pattern, so γ_K avoids τ.
- If α=I_m, take γ_K=J_(2K+2). It avoids τ because τ has an ascent when m≥2.

Both displayed permutations are direct-sum indecomposable and have maximum crossing width K+1, so neither belongs to C^(K). Direct sums of the old indecomposables together with the additional block γ_K form a subclass of C with counting series

 1/(1−I_K(z)−z^L).                                       (7)

The decomposition is unique, and the extra block is distinct from every old indecomposable, so this is an injective subclass count. Continuity gives a positive r_*<ρ_K with I_K(r_*)+r_*^L=1. Thus the subclass has radius at most r_*, forcing λ≥1/r_*>λ_K. This proves strictness without a conjecture about a spectral gap in the infinite transfer.

### Exhaustion of the full growth rate

For fixed h, concatenate arbitrary members of C_h. Each block has crossing width at most floor(h/2); direct sum preserves that bound. At sizes qh, the choices give at least a_h^q distinct members of C^(floor(h/2)). Hence λ_floor(h/2)≥a_h^(1/h). Taking the supremum over h and using direct-sum supermultiplicativity of C gives sup_K λ_K=λ. Monotonicity follows by inclusion.

For fixed K, the exact uniform law therefore satisfies

 lim_(n→∞) (1/n)log P(W(Π_n)≤K)=log(λ_K/λ)<0.                (8)

This does not imply W/n→0 or its failure. It establishes only that uniformly bounded crossing width is exponentially atypical.

## 5. Width-one states with exponentially different completions

Take α=2143 and τ=32541. Let N≥0, n=N+4, r=3, and let σ∈S_N. Consider

 π_+(σ)=(n,2,3,σ(1)+3,...,σ(N)+3,1),
 π_−(σ)=(n,3,2,σ(1)+3,...,σ(N)+3,1).                       (9)

At the cut r=3, both have exactly the same upper crossing point (1,n) and lower crossing point (n,1), so k=1. All boundary coordinates, free row/value sets, relative crossing orders, and row/column allocation words agree. Their known parts contain only four points and therefore avoid τ. Only the closed interior order differs: 12 versus 21.

Because the final entry is 1, either full permutation avoids τ precisely when the preceding n−1 entries avoid α. Its first entry n cannot participate in an α occurrence: it is first in position but α's first entry is not its maximum. Thus the question reduces to α-avoidance of 12 direct-sum σ, or 21 direct-sum σ.

The pattern α=21 direct-sum 21 gives

 π_+(σ)∈C_n  iff  σ avoids 2143,
 π_−(σ)∈C_n  iff  σ is increasing.                         (10)

Indeed, the increasing initial pair cannot supply the first decreasing pair of a crossing α occurrence, so every occurrence in 12 direct-sum σ lies in σ. The initial decreasing pair in 21 direct-sum σ supplies the first half of α whenever σ has any inversion; if σ is increasing no second decreasing pair exists.

The exact positive completion counts are therefore b_N(2143) and 1. Their ratio is exponential: the 2^(N−1) skew sums of increasing blocks, indexed by compositions of N for N≥1, all avoid 2143. Across their skew blocks all comparisons decrease, and within a block they increase, so two decreasing pairs with the second pair higher than the first cannot occur. The block decomposition is unique. Hence b_N(2143)≥2^(N−1).

The repaired profile distinguishes the two states through their two-point closed pattern. The example proves that boundary crossing patterns and allocation data alone do not determine even positive completion counts up to a subexponential factor. It is an actual principal-class obstruction, not an abstract generating tree. It is not a uniform-law limit counterexample: its cut has only one crossing point, of mass 1/n.

## 6. What remains after the exact repair

The number of profiles is bounded when both α and crossing width k are fixed. Fixed α alone does not bound k. The explicit γ_K above and the earlier perfect-packing examples realize arbitrarily large, even linear, crossing widths inside the actual avoidance class. The surviving state variables are the two active endpoint orders and the gridded closed-pattern profile indexed by those unboundedly many cuts. No finite total transfer matrix or width-uniform bound follows from (2)–(5).

The strict growth gap between Av(α) and C can bound the internal order choices of the upper crossing block, but does not remove the other endpoint order, profile compatibility, or the incoming/outgoing completion factors. The width-one example shows that this omission can already be exponentially costly. The finite-width rates in (1) have no established convergence rate here; their strictness and convergence alone do not control width proportional to n.

A positive-mass estimate for the exact infinite transfer remains missing. This lane therefore stops at the exact state theorem, rational bounded-width enumeration and strict growth gaps, and the explicit completion-context obstruction. No sixth mathematical pass or additional universal claim is proposed.

## Verification boundary

The finite checker independently enumerates small permutations, reconstructs the exposure state and transition data, tests profile-based completion equivalence and transition sufficiency, checks bounded-width counts against the transfer, and verifies the two completion fibers in (9)–(10). Those checks are finite regression evidence, not substitutes for the all-size arguments above. Earlier proofs and receipts are unchanged. No copied primary-source text or PDFs are included.
