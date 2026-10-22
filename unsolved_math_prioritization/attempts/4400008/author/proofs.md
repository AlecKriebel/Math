# Authored proofs and exact obstructions

## Conventions and the unresolved question

Let `X ⊆ A^Z` and `Y ⊆ B^Z` be nonempty subshifts on finite alphabets. Write `S` and `T` for the left shifts, `(Sx)_j=x_{j+1}`. Suppose `S` is mixing and of finite type and `h:X→Y` is a homeomorphism with

`h({S^k x:k∈Z}) = {T^k h(x):k∈Z}` for every `x`.

The equality is onto, not merely an inclusion. A priori `h` need not commute with shifts, preserve forward directions, or possess continuous integer jump functions. The question is whether `T` is a mixing SFT. No assertion below settles this without an additional hypothesis.

An SFT means a subshift defined by finitely many forbidden finite words. Equivalently it is conjugate to a shift on bi-infinite paths of a finite directed graph. A subshift conjugate to an SFT is itself SFT: if a conjugacy and its inverse have finite coding radii, choose a window long enough both to check source constraints on inverse-coded windows and to check that the two local codings compose to the identity. Those finite checks characterize the image. Finite coding radii follow from uniform continuity of the central-coordinate maps and shift commutation.

If `X` is finite and mixing, it is one fixed point. Indeed a permutation on more than one point cannot send a singleton to a prescribed singleton for every sufficiently large time. Then `Y` is also one point and the answer is immediate. Hence the substantive discussion may assume `X` infinite. Such a mixing SFT has dense periodic and dense aperiodic points, and a dense forward orbit. For periodic density, extend any admissible path to a closed path by irreducibility. For aperiodic density, the finite strongly connected presentation of a nontrivial mixing SFT has branching; two distinct return paths can be extended to loops of a common length. Concatenating them according to uncountably many binary sequences after a prescribed admissible word produces uncountably many points in every nonempty cylinder, whereas periodic points form a countable set. A dense forward orbit is constructed by concatenating an enumeration of all admissible words with connecting paths.

## 1. Orbit invariants

### Lemma 1. Periods and transitivity

For every positive integer `n`, `h` maps the points of least period `n` bijectively onto the corresponding points of `T`. Consequently it maps `Fix(S^n)` bijectively onto `Fix(T^n)`. Periodic points and aperiodic points are each dense in `Y`, and `T` is topologically transitive in the forward-time sense.

**Proof.** An orbit of a point of least period `n` has exactly `n` elements. The restriction of the bijection `h` to an orbit is a bijection onto an entire target orbit, so cardinality is unchanged. A point fixed by the `n`th iterate has least period dividing `n`; taking the disjoint union proves the fixed-point assertion. Density follows because `h` is a homeomorphism. A dense full orbit is also transported to a dense full orbit.

To verify forward transitivity explicitly, let `U,V` be nonempty open subsets of `Y`. The dense full orbit gives an integer `k` with `T^k(U)∩V` nonempty. For `k≥0` this suffices. For `k=-l<0`, the open set `W=U∩T^l(V)` is nonempty. Choose a periodic point `p∈W`; a positive multiple `q` of its period can be chosen larger than `l`. Since `T^q p=p∈T^l(V)`, the point `T^{q-l}p` belongs to `V`. Thus `T^{q-l}(U)∩V` is nonempty with positive time. ∎

### Lemma 2. Once finite type is known, mixing follows

Under the standing hypotheses, if `T` is SFT, then it is mixing.

**Proof.** A transitive SFT has an irreducible essential finite graph presentation. In such a graph let `d` be the greatest common divisor of the lengths of all closed paths. Every periodic point has period dividing a closed-path length, and a fixed point of `T^n` is represented by a closed path of length `n`; in particular `Fix(T^n)` is empty unless `d` divides `n`.

For the mixing SFT `S`, a primitive graph presentation has closed paths of every sufficiently large length, so `Fix(S^n)` is nonempty for all sufficiently large `n`. Lemma 1 gives the same assertion for `T`, whence `d=1`.

For completeness, irreducibility and `d=1` imply that paths between any two vertices exist at all sufficiently large lengths. Fix a vertex `v`. The gcd of its return lengths equals the graph period, so finitely many return lengths have gcd one. All sufficiently large integers are nonnegative combinations of those lengths: take one return length `a`, choose nonnegative combinations representing every residue modulo `a` (integer combinations can be made nonnegative by adding multiples of `a` to the coefficients of the other generators), and then add sufficiently many copies of `a`. Attach a fixed path from the initial vertex to `v` and from `v` to the terminal vertex. This gives all sufficiently large connecting lengths, which is exactly mixing for cylinders. ∎

### Lemma 3. Entropy lower bound and periodic measures

Let `p_n(U)=|Fix(U^n)|`. Then `p_n(S)=p_n(T)` for all `n`, so the formal zeta functions agree. Moreover `h_top(T)≥h_top(S)`.

**Proof.** The equality is Lemma 1, and the zeta function is defined by `exp(Σ_{n≥1} p_n z^n/n)`. Every `n`-periodic point of a finite-alphabet subshift is determined by its coordinates `0,…,n-1`. Thus `p_n(T)≤|L_n(Y)|`. For a primitive finite graph with adjacency matrix `M`, `p_n(S)=tr(M^n)` and Perron–Frobenius theory gives `lim n^(-1)log p_n(S)=log λ=h_top(S)`. Taking limits in the inequality gives the claim, using `h_top(T)=lim n^(-1)log|L_n(Y)|`. ∎

If `μ_n` is the uniform probability on `Fix(S^n)`, its pushforward is exactly the uniform probability on `Fix(T^n)`. Whenever the former converges, the latter converges to its pushforward, by continuity of `h`. This is not an argument that the limiting measure is maximal-entropy for an arbitrary `T`.

### Lemma 4. Invariant probabilities correspond

Pushforward by `h` is an affine bijection between the invariant Borel probabilities of `S` and `T`.

**Proof.** Put `R=h^(-1)Th`. It has the same full orbits as `S`. Enumerate the integers and partition `X` into Borel sets `D_k` on which `Rx=S^k x`, selecting the first eligible integer in that enumeration. These are Borel because the equality sets of the two continuous maps are closed. For an `S`-invariant probability `μ` and a Borel set `E`, injectivity of `R` makes the images of the disjoint pieces disjoint, and

`μ(RE)=Σ_k μ(S^k(E∩D_k))=Σ_k μ(E∩D_k)=μ(E)`.

Thus `μ` is `R`-invariant, and `h_*μ` is `T`-invariant. Apply the same argument to the inverse orbit equivalence for surjectivity. Pushforward is affine and has inverse pushforward by `h^(-1)`. ∎

**Route-1 gap.** These proofs give no bound on the memory of `Y`. In particular, they do not justify replacing target word counts by target periodic counts or treating a transported invariant probability as an entropy maximizer.

## 2. Cocycle regularity

### Lemma 5. Dense local regularity is weaker than global regularity

For a homeomorphism `R` with the same full orbits as `S`, the union of the interiors of the closed sets `E_k={x:Rx=S^k x}` is dense and open. A locally constant jump can be selected in a neighborhood of each point of that union. This does not yield a globally bounded jump.

**Proof.** The closed sets `E_k` cover `X`. For any nonempty open `U⊆X`, if every `E_k∩U` had empty interior in `U`, the Baire space `U` would be a countable union of relatively closed nowhere dense sets. This is impossible. Some `E_k` therefore contains a nonempty open subset of `U`. On that subset the constant `k` is a valid jump. Taking all such interiors proves density and openness. No compactness argument extracts a finite subcover, because these interiors need not cover all of `X`. ∎

**Conditional primary theorem.** Boyle–Tomiyama, Theorem 3.2, says that topologically free homeomorphisms of a compact Hausdorff space with the same orbits and a continuous integer jump function are flip conjugate if one is topologically transitive. Applied to `S` and `R=h^(-1)Th`, this proves the desired answer under the extra continuous-jump hypothesis. Their bounded-jump Theorem 2.3 and Corollary 2.7 instead yield flip conjugacy after removing a closed exceptional set of periodic points of bounded period. For a finite-alphabet subshift that set is finite. It cannot simply be omitted from the required global conclusion.

Source: https://www.jstage.jst.go.jp/article/jmath1948/50/2/50_2_317/_pdf

### Lemma 6. An explicit expansive self-orbit-equivalence with unbounded jumps

Let `X={0,1}^Z`, `S` its left shift, and `o=0^Z`. For `n≥1`, define the clopen cylinder

`U_n={x: x_n=1 and x_j=0 for -3n≤j≤3n, j≠n}`,

and let `V_n=S^(2n)U_n`. Equivalently `V_n` prescribes a single `1` at `-n` on the interval `[-5n,n]`. Define

- `h(x)=S^(2n)x` for `x∈U_n`;
- `h(x)=S^(-2n)x` for `x∈V_n`;
- `h(x)=x` outside all those cylinders.

This is a homeomorphic involution taking each `S`-orbit onto itself. Yet the unique integer `a(x)` at aperiodic points determined by `h(Sx)=S^(a(x))h(x)` is unbounded.

**Proof.** Each point of `U_n∪V_n` has its nearest nonzero coordinate at absolute distance exactly `n`; in `U_n` it is on the right, in `V_n` on the left. Thus all the named cylinders are pairwise disjoint. The two displayed shift maps exchange `U_n` and `V_n` inversely, so `h²=id`. Every image lies in its original `S`-orbit; bijectivity then gives equality of orbit sets.

Away from `o`, fix a nonzero coordinate of the point. A cylinder fixing that coordinate meets only finitely many of the `U_n,V_n`. On this neighborhood `h` is a map on a finite clopen partition by continuous shifts or the identity, hence is continuous. At `o`, for any `r`, a point agreeing with `o` on `[-r,r]` either is unchanged or belongs to `U_n∪V_n` with `n>r`. Its image belongs to the partner cylinder and still agrees with `o` on that interval. This proves continuity at `o`. The inverse is the same map and is continuous.

For the unboundedness, let `x^(n)` have exactly two `1`s, at coordinates `n+1` and `3n+2`. Its nearest `1` is at `n+1`, but it is not in `U_(n+1)` because the second `1` occurs in that cylinder's prescribed zero interval. It is not in `V_(n+1)` or any other named cylinder. Thus `h(x^(n))=x^(n)`. On the other hand, `Sx^(n)` has `1`s at `n` and `3n+1`, hence lies in `U_n`. Therefore

`h(Sx^(n))=S^(2n+1)x^(n)=S^(2n+1)h(x^(n))`.

The point `x^(n)` is aperiodic: a nonempty finite set of nonzero coordinates is not invariant under any nonzero translation. Thus its jump is uniquely `2n+1`, proving unboundedness. ∎

This example uses two mixing SFTs (indeed the very same full shift). It refutes the proposed inference about an arbitrary orbit map; it does not refute finite-type preservation, and does not rule out the existence of a different, well-behaved orbit equivalence.

## 3. Shadowing and finite-language reconstruction

Equip a subshift with `d(x,y)=2^(-r)` when `r=min{|j|:x_j≠y_j}`, and `d(x,x)=0`. It has two-sided shadowing if for every `ε>0` some `δ>0` has this property: every sequence `(x^i)_(i∈Z)` in the subshift with `d(Sx^i,x^(i+1))<δ` is traced by some `z`, meaning `d(S^i z,x^i)<ε` for all integers `i`.

### Lemma 7. SFT if and only if shadowing

For a finite-alphabet subshift `Y`, shadowing is equivalent to finite type. It is also equivalent to `Y=Y_m` for some `m`, where `Y_m` consists of all bi-infinite configurations whose every length-`2m+1` word belongs to `L_(2m+1)(Y)`.

**Proof, shadowing implies stabilization.** Take shadowing accuracy `ε=1/2` and a corresponding `δ`. Choose `m≥1` with `2^(-m)<δ`. For any `w∈Y_m` and each integer `i`, choose `x^i∈Y` with `x^i_j=w_(i+j)` on `[-m,m]`; such a point exists by the definition of the language. Then `Sx^i` and `x^(i+1)` agree on `[-m+1,m-1]`, so their distance is at most `2^(-m)<δ`. A tracing point `z∈Y` has `z_i=x^i_0=w_i` for all `i`, since distance below `1/2` in particular forces equality at coordinate zero. Hence `w=z∈Y`. The reverse inclusion is immediate, so `Y=Y_m`, which is SFT.

**Proof, SFT implies shadowing.** Suppose membership in `Y` is determined by permitted words of length `R+1`. Given `ε>0`, choose `q≥1` with `2^(-q)<ε` and let `L≥q+R+1`. Choose `δ=2^(-(L+1))`. A `δ`-pseudo-orbit has the exact consistency relations `x^(i+1)_j=x^i_(j+1)` whenever `|j|≤L+1`. Define `z_i=x^i_0`. Repeatedly using these relations forward and backward gives `z_(i+j)=x^i_j` for `|j|≤L`: for positive `j` iterate through indices `j-1,…,0`; for negative `j` iterate the same relation backward through indices `-1,-2,…,j`.

Every length-`R+1` block of `z` occurs in a suitable `x^i`, so `z∈Y`. The same consistency gives agreement of `S^i z` and `x^i` on `[-q,q]`, hence distance at most `2^(-(q+1))<ε`. Thus `z` traces the pseudo-orbit. The remaining equivalence follows because every `Y_m` is SFT, and any finite forbidden list is detected by all sufficiently long windows. ∎

### Lemma 8. Exact nonstabilization control

Let `E` be the binary even shift, forbidding `10^(2k+1)1` for all `k≥0`. For every `m≥1`, put `w^(m)=(10^(2m+1))^Z`. Then `w^(m)∉E` but `w^(m)∈E_m`. In particular `E` is not SFT and does not have shadowing.

**Proof.** Adjacent `1`s in `w^(m)` enclose an odd number `2m+1` of zeros, so the point is forbidden. Each length-`2m+1` window has at most one `1`, and every finite binary word with at most one `1` occurs in a point of `E` having at most one `1` globally. Therefore every required window is in the language of `E`, giving membership in `E_m`. Lemma 7 gives the conclusion. ∎

The even shift is expansive, as every finite-alphabet subshift is. This control disproves inference of finite type from expansivity plus membership in all finitely tested approximations; it is not presented as an orbit-equivalence counterexample.

**Route-3 gap.** The pulled-back map `R=h^(-1)Th` is conjugate to `T`, so transferring shadowing between those two causes no problem. The missing implication is from shadowing of `S` to shadowing of `R` merely because their full orbits agree. Pullbacks of `T`-pseudo-orbits have approximate jumps `S^(a(x^i))x^i≈x^(i+1)`. They are not ordinary `S`-pseudo-orbits. Filling each jump with source iterates can revisit earlier indices, reverse directions, or create arbitrarily long excursions. No proof here controls a tracing point at the required `R` times.

## 4. Positive-speed counterexample construction fails

### Lemma 9. One-orbit positive speed is trivial

Let `S,R` be homeomorphisms of the same space with the same full orbits. On an infinite orbit, suppose `Rx=S^(c(x))x` with `c(x)>0` at every point. Then `R=S` on that orbit. If positivity holds on every aperiodic orbit and the aperiodic points are dense, `R=S` everywhere. Negative jumps throughout instead give `R=S^(-1)`.

**Proof.** Identify the source orbit of a point with the integers by `k↦S^k x`. The map `R` induces a bijection `p:Z→Z` with `p(k)>k`. Because the full `R`-orbit is the entire source orbit, `a_i=p^i(0)`, for `i∈Z`, enumerates every integer exactly once. It is strictly increasing, including for negative indices since `p^(-1)(k)<k`. If `a_(i+1)≥a_i+2`, the integer `a_i+1` would be missing from this strictly increasing enumeration. Thus `a_(i+1)=a_i+1` for every `i`. Since `a_0=0`, it follows that `a_i=i` and `p(k)=k+1` for all `k`. The equality on a dense set extends by continuity. Replace `S` by `S^(-1)` for the negative case. ∎

No continuity or boundedness of `c` was used. A positive speedup such as `R=S²` evades the lemma only by splitting every aperiodic `S`-orbit into two `R`-orbits, so the identity is not a TOE with the required onto-orbit property. On a finite cycle, a coprime positive step can generate the same orbit, but this does not defeat the dense-aperiodic extension argument.

**Route-4 gap.** Nonmonotone orbit permutations are not covered by the lemma. Producing a counterexample by them would still require a homeomorphism with continuous inverse, a finite generating clopen partition (expansivity), and a rigorous failure of finite type. None has been supplied here.

## 5. Return maps, finite towers, and flow equivalence

### Lemma 10. Finite return and roof constructions preserve SFT

(a) If `C` is a clopen global discrete cross section of an SFT `S`, with finitely many iterates of `C` covering the entire space, the first-return map on `C` is SFT.

(b) A discrete suspension of an SFT under a continuous positive integer-valued roof is SFT.

**Proof of (a).** First-return times are uniformly bounded: if `⋃_(j=-N)^N S^j C=X`, then applying this cover to `S^(N+1)x` gives a future visit to `C` within `2N+1` steps from any `x`. Clopenness makes each bounded-return-time level set clopen. Recode the SFT by sufficiently long blocks so its constraints are one-step and membership in `C` is determined by the current vertex. Let `M` be the marked vertices specifying `C`.

A return word is a directed finite path starting and ending in `M` with no interior visit to `M`. Uniform boundedness makes the set of return words finite. Use these words as a new alphabet; a word may be followed by another precisely when its terminal vertex equals the other's initial vertex. This is a one-step finite graph shift. The return itinerary of `x∈C` records its successive return words in both time directions. The itinerary is continuous, injective, and onto this graph shift: concatenating any compatible itinerary gives a unique bi-infinite allowed original path, with the prescribed cut at coordinate zero. It is a conjugacy with the return map. Compactness gives continuity of its inverse as well.

**Proof of (b).** A continuous integer roof on a compact space has finite range and depends on finitely many coordinates. After a higher-block recoding it is a function `r(v)≥1` of the current vertex of a one-step presentation. Replace each vertex `v` by `r(v)` consecutive levels. Within each chain the next level is forced; from its top there is an edge to level zero of `w` exactly when the original graph allows `v→w`. This finite graph codes the discrete suspension, with a bijective continuous itinerary whose inverse reconstructs the base path and current level. ∎

### Lemma 11. Conditional closing route through flows

If `T` is flow equivalent to `S`, then `T` is SFT and hence, under the standing TOE hypotheses, mixing. Under those hypotheses, the assertion that `T` is SFT is equivalent to the assertion that `T` is flow equivalent to `S`.

**Proof.** Use the Parry–Sullivan common-section theorem in the form stated in Boyle–Handelman §1.4: two return maps to cross sections of the same suspension flow are each conjugate to discrete suspensions over a common return map `Q`. Apply this to the assumed flow equivalence. The base of a discrete suspension is a clopen global discrete cross section. Since `S` is SFT, Lemma 10(a), transported through the conjugacy, implies that `Q` is SFT. Lemma 10(b) then shows that the other suspension, conjugate to `T`, is SFT. Lemma 2 proves mixing.

For the converse under the original TOE hypotheses, if `T` is SFT, Lemmas 1–2 make both systems irreducible SFTs. Boyle–Handelman Theorem 1.12 then applies and gives flow equivalence. The hypotheses are checked here only after assuming the desired finite-type conclusion; this is an equivalence/reduction, not an independent proof of that conclusion. ∎

Sources: Boyle–Handelman, §§1.4 and 1.10–1.12, https://terpconnect.umd.edu/~mboyle/papers/bhoemaster.pdf . The complete dynamical proofs of the finite constructions needed for this conditional application are above; the general topological common-section theorem is an explicitly cited external dependency.

**Exact negative control for changing equivalence relations.** Expand each symbol `1` of the binary full shift to the two-symbol block `1a`. The resulting graph shift on `0,1,a` has transitions `0→0,1`, `1→a`, `a→0,1`. This expansion is flow equivalent to the original system: regard it as the discrete suspension with roof one on `0` and two on `1`; the suspensions with their continuous real-time flows are related by rescaling each base interval. The full binary shift has two fixed points, whereas the expanded shift has only `0^Z`. By Lemma 1 they cannot be TOE. Therefore flow equivalence cannot simply be used as the definition of the question's equivalence relation.

**Route-5 gap.** The known TOE-to-flow theorem assumes both systems irreducible SFT. For a general target subshift, no flow equivalence or common-section realization has been obtained here. An ordered-invariant calculation without a valid reconstruction theorem does not fill that gap.

## Scope of newer nearby results

Salo (2023), Theorem 1, extends conjugacies of the aperiodic parts when both ambient shifts are infinite transitive SFTs. His Theorem 3 permits certain broader subshifts but assumes synchronizing periodic points and dense aperiodic one-sided projections on both sides. The present hypotheses give no such target synchronization, and the starting map is an orbit map rather than a conjugacy of free parts. His result solves the neighboring Hochman question, not this one. https://doi.org/10.1112/plms.12567

Matsumoto (2023), Proposition 6.5, preserves finite type for continuous orbit equivalence of the associated one-sided subshifts of normal subshifts. This is a different orbit-equivalence notion with extra hypotheses; no application to unrestricted two-sided TOE has been justified. https://ems.press/content/serial-article-files/28864

## Final mathematical conclusion

The packet establishes necessary invariants, a mixing reduction, exact conditional routes, and explicit obstructions to several tempting shortcuts. It establishes neither universal finite-type preservation nor a counterexample. The original problem remains unresolved by this investigation.
