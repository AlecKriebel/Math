# A uniform pattern-packing theorem and its spatial obstruction

Shared PASS4, 14 October 2026. This is general fixed-pattern partial progress and an explicit limitation of the packing route. The universal diagonal-permuton target remains **UNSOLVED**. No novelty or human peer-review claim is made.

## 1. Setup and precise conclusions

Fix a permutation α of length m≥2, put τ=α skew-sum 1, and write

- C_n=Av_n(τ), a_n=|C_n|;
- b_n=|Av_n(α)|;
- λ=lim a_n^(1/n), μ=lim b_n^(1/n);
- P_α(π) for the maximum number of pairwise vertex-disjoint classical α occurrences;
- D_α(π) for the minimum number of entries whose deletion makes π α-avoiding.

Both counts at size zero are one. The case α=1 is excluded from the following growth formulas: Av_n(21) consists only of the increasing permutation, so its target conclusion is already immediate.

The following statements hold for **every** fixed α with m≥2:

1. The accepted minimum-insertion frontier estimate implies the strict growth gap

   μ ≤ λ / C(1/λ) < λ,

   where C(z)=(1−√(1−4z))/(2z) is the Catalan series.

2. There is a constant δ>0 such that, for the exactly uniform Π_n∈C_n,

   P(D_α(Π_n)≤δn) ≤ exp(−c n),
   P(P_α(Π_n)≤δn/m) ≤ exp(−c n)

   for all sufficiently large n and some c>0. A quantitative entropy rate is given below. Thus typical permutations contain linearly many disjoint α occurrences and remain α-containing after deletion of a sufficiently small fixed fraction of their entries.

3. Nevertheless, for every such α there are deterministic π_k∈C_(n_k) admitting a **perfect partition of all entries into α occurrences**, with minimal possible frontier L(π_k)=m and correct localization of every smallest o(n_k) values, but with a fixed positive crossing mass and non-diagonal permuton distance. Therefore even the strongest possible global disjoint-packing conclusion cannot replace spatial localization.

Statement 3 is a deterministic obstruction to an inference, **not** a counterexample under the uniform law.

## 2. Growth limits and a strict gap

A pattern ending in its minimum is direct-sum indecomposable. Consequently C is direct-sum closed, a_(p+q)≥a_p a_q, and a_n≤λ^n. Fekete's lemma and the fixed-pattern Marcus–Tardos bound give existence and finiteness of λ. The accepted frontier argument gives λ≥4 when m≥2.

For completeness, every permutation of length at least two is either direct-sum indecomposable or skew-sum indecomposable. Indeed, suppose it has a direct-sum cut at p and a skew-sum cut at q. If p≤q, an entry from the first p positions and one from positions after q would have to be both increasing and decreasing across those cuts. If q<p, use an entry from the first q positions and one after p for the same contradiction. The cuts are nontrivial, so those choices exist. Thus a permutation cannot have both kinds of decomposition. Avoidance of a pattern indecomposable under one sum operation is closed under that operation. Therefore b_(p+q)≥b_p b_q, the finite growth limit μ exists, and b_n≤μ^n. Also μ≥1, since α of length at least two cannot occur in at least one of the two monotone permutations at every size.

Let γ=log C(1/λ)>0. The accepted frontier theorem in `pass1_concentration/ACTIVE_FRONTIER_PROOF.md` applies to the exact uniform C_n law. Every α-free member has L=n+1, so its event is contained in {L≥n}. Consequently

limsup_(n→∞) (1/n) log(b_n/a_n) ≤ −γ.

The growth limits identify the left side as log(μ/λ). Thus

 g := log(λ/μ) ≥ γ > 0.                                      (1)

This is a consequence of the accepted frontier estimate, not an independent assertion about all proper subclasses of arbitrary permutation classes. No ratio-limit theorem is needed.

## 3. Exact deletion encoding and uniform packing

Fix n and 0≤h≤n. Let E_(n,h) be the permutations π∈C_n admitting deletion of exactly h entries to leave an α-avoiding subpermutation. For each such π select the lexicographically first successful h-element position set. Record:

- that position set P;
- the value set V occupying P;
- the standardized deleted subpermutation σ∈C_h;
- the standardized retained subpermutation η∈Av_(n−h)(α).

The deleted pattern is in C_h by hereditary avoidance. Given the tuple, put the ordered values of V into P according to σ and put the complementary values into the complementary positions according to η. This uniquely recovers π. The canonical choice gives one tuple per permutation, so

 |E_(n,h)| ≤ binom(n,h)^2 a_h b_(n−h).                         (2)

No independence after conditioning, uniform-restriction law, or omission of a completion factor occurs here. The tuples form an ambient upper count, not a model asserted for the actual law.

Let H(x)=−x log x−(1−x)log(1−x), with endpoint values zero. Combining (2), a_h≤λ^h, b_(n−h)≤μ^(n−h), and binom(n,h)≤exp(nH(h/n)) yields

 |E_(n,h)| ≤ λ^n exp{n[2H(h/n)−(1−h/n)g]}.                   (3)

For 0<δ<1/2, the function f(x)=2H(x)−(1−x)g is increasing on [0,δ], since f'(x)=2log((1−x)/x)+g>0 in its interior. Summing (3) over h≤floor(δn), and using log a_n=n logλ+o(n), gives

 limsup (1/n)log P(D_α(Π_n)≤δn)
 ≤ 2H(δ)−(1−δ)g.                                           (4)

There exists δ>0 making this negative, because its right side tends to −g as δ↓0. More conservatively, it suffices to choose δ<1/2 with 2H(δ)<(1−δ)γ. Any c smaller than (1−δ)g−2H(δ) then gives the exponential probability bound for all sufficiently large n.

The elementary packing/deletion inequalities are

 P_α(π) ≤ D_α(π) ≤ m P_α(π).                                (5)

The left inequality holds because every successful deletion must meet every occurrence in a disjoint packing. For the right inequality, choose a maximum packing and delete its union. Any remaining α occurrence would be disjoint from that packing and enlarge it, a contradiction. The union has mP_α entries. Therefore {P_α≤δn/m} is contained in {D_α≤δn}, proving the second assertion with exactly the same rate bound. More generally the same union argument applies to any inclusion-maximal packing, but maximum packing is used in (5).

## 4. Why inversions alone do not produce α occurrences

Except for α=21 (and the separately trivial α=1), a positive inversion density does not even force one α occurrence deterministically:

- If α is not decreasing, the decreasing permutation J_n avoids α and has inversion density tending to 1/2.
- If α=J_m with m≥3, the skew sum I_floor(n/2) skew-sum I_ceil(n/2) has inversion density tending to 1/4 but no decreasing subsequence of length three, hence avoids α.

All these α-free permutations also avoid τ. Their existence does not contradict (4): they belong to an exponentially rare subclass under the exact uniform C_n law. For α=21, inversions themselves are the relevant occurrences, and a maximal matching in the inversion graph supplies a linear disjoint packing from a quadratic number of inversions; that special observation does not address general α.

## 5. Perfect packing still permits macroscopic crossing

### 5.1 Any α distinct from I_m

Let Q_k be the increasing-block inflation of α: replace each entry of α by an increasing block of k consecutive values, with the order of the blocks prescribed by α. Its size is mk. Let A_k be the direct sum of k copies of α, also of size mk, and define

 π_k = A_k direct-sum Q_k,       n_k=2mk.                     (6)

A permutation pattern cannot have more descents than the permutation containing it: each descent between successive selected entries requires a descent in the intervening segment, and those segments are disjoint. Increasing-block inflation preserves the number of descents. Thus Q_k has des(α) descents, whereas τ has des(α)+1; Q_k avoids τ. Each copy of α avoids τ by size, and C is direct-sum closed, proving π_k∈C_(n_k).

The k α blocks in A_k give a disjoint packing of its entire prefix. For each r=1,...,k, choose the r-th entry in every increasing block of Q_k. Those m points form α. The k resulting occurrences partition all entries of Q_k. Altogether P_α(π_k)=n_k/m, the largest value possible.

The first m entries of π_k form α, so L(π_k)=m. If s_k=o(n_k), the smallest s_k values eventually lie in A_k. Their positions satisfy M_(s_k)(π_k)≤s_k+m−1. Thus the earlier frontier and small-value conclusions, regarded as deterministic geometric properties, hold for this sequence.

Because α≠I_m, there exists 1≤ℓ<m with

 c_α(ℓ) := |{i≤ℓ : α(i)>ℓ}| ≥1.

Otherwise each initial segment would contain exactly its own smallest values, forcing α=I_m. At the grid cut r_k=mk+ℓk in π_k, the number of crossing points is exactly k c_α(ℓ). Hence its normalized crossing mass at the fixed cut t=(m+ℓ)/(2m) is

 c_(μ_(π_k))(t)=c_α(ℓ)/(2m) ≥1/(2m).                        (7)

### 5.2 Increasing α=I_m

Set

 π_k = I_((m−1)k) direct-sum J_k,       n_k=mk.               (8)

It avoids τ=I_m skew-sum 1. An increasing m-subsequence uses at most one point from the decreasing tail, so at least one of its entries lies in the smaller-valued increasing prefix. Every later point exceeds that prefix entry; it cannot be a terminal minimum completing τ. There is no increasing m-subsequence entirely inside the tail for m≥2.

Partition the prefix into k consecutive groups of m−1 entries and append one distinct tail entry to each group. These k increasing m-subsequences partition all entries. Again P_α=n_k/m and L=m. Every smallest o(n_k) values lies eventually in the increasing prefix in its identical position. At a cut halfway through the tail, the normalized crossing mass tends to 1/(2m).

### 5.3 Fixed weak deviation and the boundary of the example

For any permuton μ, write c_μ(t)=μ([0,t]×(t,1]) and M=sup_t c_μ(t). Uniform marginals make c_μ 1-Lipschitz with zero endpoint values, and give

 ∫|x−y|dμ = 2∫c_μ(t)dt ≥2M².

The test function |x−y|/√2 is admissible for d_BL and has diagonal integral zero. Thus

 d_BL(μ,μ_I) ≥√2 M².

The two constructions satisfy

 liminf d_BL(μ_(π_k),μ_I) ≥1/(2√2 m²)>0.                     (9)

Their inversion densities are also positive: for (6) the limit is inv(α)/(4m²), and for (8) it is 1/(2m²). These are fixed-pattern deterministic sequences, not claims of a positive probability event under uniform sampling.

## 6. The exact missing spatial estimate

There is an additional actual-class fact that goes in the opposite direction from a hoped-for crossing packing. For π∈C_n and any 0≤r≤n define

 A_r=(π(i): i≤r and π(i)>r), in their original position order.

If A_r is nonempty, there is also a point (j,π(j)) with j>r and π(j)≤r: the two crossing sets have equal cardinality. Every point of A_r precedes that point and exceeds its value. Therefore the standardized pattern induced by A_r **must avoid α**, or an α occurrence there followed by (j,π(j)) would form τ.

Thus every crossing rectangle is automatically α-free. Perfect global packings can use vertices inside it only by completing their occurrences with vertices outside it, as the explicit constructions demonstrate. No purely global packing count forbids this.

To establish the desired diagonal limit one still needs, for every fixed t∈(0,1) and ε>0,

 #{π∈C_n: |{i≤floor(tn): π(i)>floor(tn)}|≥εn} / a_n →0.        (10)

The new deletion-distance estimate only excludes permutations that become α-free after a *small* fractional deletion. It does not control an α-free crossing subset of arbitrary positive size whose complement is still macroscopic. Bounding that event by independent position/value allocations incurs the same entropy cost exposed in the earlier quadrant calculation. Nor does (4) make an ancestor after deletion of a linear number of minima uniform: its law remains proportional to its actual completion count D_(n−j)(σ).

Accordingly, this lane establishes the general growth/packing theorem, but supplies neither a universal proof nor a target counterexample. A successful packing-based continuation needs spatial or conditional information beyond perfect global coverage, while preserving the exact finite-class law.

## Dependencies and reproducibility

The strict gap uses the accepted all-α frontier theorem. The crossing metric identities and the completion-weight caution were independently rechecked against their elementary derivations; they are also recorded in the earlier entropy and bulk-bottleneck notes. The finite checker for this lane independently tests the deletion encoding, packing/deletion inequalities, crossing α-avoidance, and the perfect-packing constructions. Finite tests support indexing and inverse reconstruction only; the all-size proofs are the arguments above. No copied scholarly source text or PDF is included.
