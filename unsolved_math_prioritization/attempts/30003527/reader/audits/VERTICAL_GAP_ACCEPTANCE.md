# Independent acceptance of the vertical short-gap counterexample

13 October 2026. Problem 30003527 / queue row 1767. Independent audit of the complementary result within shared substantive pass 2; this audit does not constitute another substantive pass.

## Verdict and exact scope

**Accepted.** The frozen proof establishes a compact nonmovable set A in R³ whose vertical fibers have at most two components and whose bounded fiber gaps all have length 1. For the bounded globally Lipschitz vertical-slowing field F_A = min(1, dist(·,A))e₃, A is the stationary set and G_ε(A)=A for every 0<ε<1. Consequently, the proposed implication from short-gap filling or a uniform fiber-component bound to movability is false.

There is no mathematical gap in the direct nonmovability argument requiring a change to the frozen construction. Two clarifications are supplied below: the supplementary slab assertion has an elementary deformation-retraction proof, and one of the optional secondary paper's corollaries concerns shape realization rather than embedding.

**This is not a counterexample to the full invariant-enlargement problem.** It excludes one specific family of proposed enlargements, not every compact invariant B with A⊆B⊆U. Neither movability nor nonmovability of M_δ(A)=Inv(N_δ(A)) has been established by this argument.

Audited artifact: VERTICAL_GAP_COUNTEREXAMPLE.md, 11,970 bytes, SHA-256:

85ab6a5e1b948ebc8f83f6506cb04a1d9e8fa644826261fcc40247567b695403

The frozen original was read in full and left unchanged. This report is an authored mathematical audit and clarification; it does not reproduce imported source bodies.

## 1. The embedding input really is an embedding

R. H. Bing, *Embedding Circle-Like Continua in the Plane*, Canadian Journal of Mathematics 14 (1962), 113–128, Theorem 8, printed pp.121–122, gives an embedding of every circle-like continuum in the product of a triod and an arc. The theorem statement and the entire short proof were inspected, including their rendered pages. The proof's concluding limit is homeomorphic to the input continuum. Thus applying it to the dyadic solenoid gives an actual homeomorphic copy K⊂T. No passage from mere shape realization to embedding is being assumed.

Primary source: [Bing's paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4BF9863EDD2DC1E32E1BD90E11790F4E/S0008414X00017569a.pdf/embedding_circlelike_continua_in_the_plane.pdf), [DOI](https://doi.org/10.4153/CJM-1962-009-3).

The optional corroborating paper is J. Olędzki and S. Spież, *On embedding curves in two-dimensional polyhedra*, Fundamenta Mathematicae 122 (1984), 47–55. Its introduction explicitly identifies Bing's solenoid embedding. Theorem 2.2 and Corollary 3.4 are embedding results. **Corollary 3.5, by contrast, gives a pointed shape realization of a general pointed one-dimensional compactum.** It should not be cited as a general homeomorphic embedding theorem. The frozen proof does not need it: Bing's theorem already provides K, and Corollary 3.4 also applies to a solenoid's circle inverse system. The relevant existing PDF and rendered pages were inspected; a fresh request to the supplied PDF URL returned HTTP 403.

Reference: [Olędzki–Spież DOI](https://doi.org/10.4064/fm-122-1-47-55).

## 2. Solenoid nonmovability

The nested solid-torus argument has the correct direction of inference. Fix an outer torus neighborhood U_i. If the solenoid were movable, choose its movability neighborhood V for U_i, then a later torus neighborhood U_j⊂V. For each k≥j, movability with target U_k gives a homotopy of the inclusion U_j→U_i to a map factoring through U_k. Therefore

im[H₁(U_j;Z)→H₁(U_i;Z)] ⊆ im[H₁(U_k;Z)→H₁(U_i;Z)].

Nested inclusions give the reverse containment. Thus the images would stabilize. For the dyadic solenoid they are 2^(j−i)Z and 2^(k−i)Z and do not stabilize. This contradicts movability. Open interiors can be used throughout, so the proof concerns actual neighborhoods.

This is also directly supported by K. Borsuk, *On movable compacta*, Fundamenta Mathematicae 66 (1969/1970), 137–146, Example (1.3), printed pp.138–139. Its definition on p.137 has the full neighborhood-homotopy quantifiers. Corollary (3.11), p.142, establishes shape invariance, hence homeomorphism invariance. Corollary (5.5), p.145, gives movability of every planar compactum, including disconnected ones. These passages and the solenoid proof were inspected in the original scanned article; pp.137 and 144–145 were also visually checked.

Primary source: [Borsuk's paper](https://matwbn.icm.edu.pl/ksiazki/fm/fm66/fm66115.pdf), [DOI](https://doi.org/10.4064/fm-66-1-137-146).

## 3. Audit of the stretched book and the explicit near-homeomorphisms

The three defining pieces of T* are closed. The formulas for q agree at both common edges, so the pasting lemma gives continuity. The bottom rectangle maps identically to the two horizontal pages of T, the upward rectangle collapses onto the common edge E, and the top rectangle maps onto the third page. Therefore q is onto, every fiber outside E is a point, and every fiber over E is exactly the stated vertical interval.

For 0<t<1, h_t is likewise continuous on the pieces and agrees at their junctions. On the bent third arm it sends the upward part increasingly onto [0,t] and the top part increasingly onto [t,1]. It fixes the other two arms and the x-coordinate. It is consequently a continuous bijection between compact T* and Hausdorff T, hence a homeomorphism. There is no unaddressed collision at the branch point.

The uniform bound |h_t−q|≤t follows separately on each piece: the differences are zero on the bottom, tz on the upward segment, and t(1−y) on the top. On the third arm, f_t=q h_t⁻¹ has the stated formula

f_t(r)=0 for 0≤r≤t, and f_t(r)=(r−t)/(1−t) for t≤r≤1.

It is continuous at r=t and satisfies |f_t(r)−r|≤t. Interpolation (1−s)r+s f_t(r) stays on that same arm, fixes its common endpoint, and is compatible with the identity on the other arms. It is therefore a continuous homotopy on all T, with displacement at most t.

The explicit inverse-image description gives exactly the listed vertical fibers of A=q⁻¹(K): empty; {0}; {1}; {0,1}; or [0,1]. At y=0, one cannot obtain only part of a vertical interval because the entire interval has the same q-image. No other heights can occur when y≠0.

## 4. Relative-ANR neighborhoods and quantifier order

The use of relative neighborhoods in finite polyhedra is legitimate. Here is a direct justification sufficient for this argument.

Let C⊂P⊂R³ be compact, with P a finite polyhedron. There is an open neighborhood D of P and a retraction r:D→P. If C is movable in R³, apply ambient movability to D∩r⁻¹(O_P), where O_P is a relative neighborhood of C. Restrict the resulting domain to P and postcompose its homotopies with r. Targets D∩r⁻¹(W_P) give every relative target W_P. This proves relative movability in P.

Conversely, suppose C is movable relative to P and let O be an ambient neighborhood of C. Use relative movability in O∩P to choose V_P. By continuity of r and compactness of C, there is an ambient neighborhood V of C with r(V)⊂V_P and with every segment from x to r(x), x∈V, contained in O. For an arbitrary ambient target W, use relative movability with W∩P. Prepend the straight homotopy from x to r(x), and then apply the relative homotopy to r(x). The neighborhood V was fixed before W. This proves ambient movability. Thus no replacement of ordinary movability by a weaker relative notion is occurring.

Now fix the frozen proof's relative neighborhood O⊃K in T. Movability of A would supply V* for q⁻¹(O). The compact set q(T*\V*) is disjoint from K. Choose a positive separation parameter η and a positive ρ for which the relative ρ-neighborhood of K is contained in O. If a complement is empty, its restriction is simply unnecessary. Choose t<min(1/2,η/3,ρ/3) and a relative open V containing K within distance min(η/3,ρ/3) of K.

If a∉V*, then q(a) is at least η from K, whereas h_t(a) is within t of q(a). Hence h_t(a) cannot belong to V, proving h_t⁻¹(V)⊂V*. All these choices depend on O and V*, **not on the subsequent target W**.

For any relative neighborhood W⊃K, movability of A now supplies H:V*×[0,1]→q⁻¹(O) ending in q⁻¹(W). The composite q H(h_t⁻¹(y),s) starts at f_t(y) and ends in W. Prepend the explicit homotopy from y to f_t(y). Its points remain within t of V and thus within 2ρ/3 of K, so it stays in O. The concatenation proves movability of K with the required order

for every O, there exists V, for every W, there exists a homotopy.

That contradicts Section 2. This direct proof establishes nonmovability of A without invoking any general cell-like-map theorem.

## 5. Short-gap construction, component bound, and the flow

The compact parameter-space proof of compactness of G_ε(C) is valid. Its continuous image includes C via a=b. It is exactly C together with every bounded complementary fiber gap of length at most ε: a segment between two fiber points cannot meet a longer complementary gap, and each eligible gap has both endpoints in the compact fiber. The endpoint estimate gives dist(G_ε(C),C)≤ε/2. Thus G_ε(C) lies in any prescribed neighborhood of C for sufficiently small positive ε.

Let the total height range of C be R=M−m. Distinct remaining fiber components are separated by gaps of length greater than ε. Any collection of n components supplies n−1 disjoint such separating gaps in [m,M]. Consequently (n−1)ε<R whenever n≥2. An infinite number of components is impossible, and the frozen bound floor(R/ε)+1 is valid, although not always sharp. Empty and one-point fibers cause no problem.

The distance function to a nonempty closed set is 1-Lipschitz. Taking its minimum with 1 preserves that property, so F_C is globally Lipschitz and bounded. Its ODE has a unique full flow. Its stationary set is precisely C.

On a fiber complement the scalar vertical velocity is positive. An orbit is monotone, cannot converge in either time direction to an interior point where velocity is positive, and cannot reach a finite endpoint in finite time by uniqueness. Its image is therefore the entire open complementary interval. Unbounded complementary intervals give unbounded full orbits. A compact invariant set containing C can include a bounded gap only by including its whole orbit; conversely a closed union of C and selected bounded gaps is bounded and invariant. This verifies the stated classification and the invariance of G_ε(C).

For the constructed A, every bounded gap is (0,1). Thus G_ε(A)=A for 0<ε<1. Compactness, invariance, small neighborhood containment, and a uniform component bound do not supply the missing movability.

## 6. Direct slab clarification, avoiding the cell-like-map theorem

This supplies a simpler proof of the supplementary slab statement without modifying the frozen report.

Let S={x∈[0,1]:(x,0,0)∈K}. The points of A at heights strictly between 0 and 1 are exactly S×{0}×(0,1). Let J=[a,b] have b−a<1, and put P_J=A∩(R²×J). If P_J is nonempty, there are three possibilities.

1. If 0∈J, then 1∉J. Every point of P_J above height 0 lies on a full vertical interval over S. The homotopy (x,y,z)↦(x,y,(1−s)z) stays in P_J and fixes its bottom slice. It is a strong deformation retraction to the planar compactum P_J∩{z=0}.
2. If 1∈J, then 0∉J. The homotopy (x,y,z)↦(x,y,(1−s)z+s) is a strong deformation retraction to the planar compactum P_J∩{z=1}.
3. If neither 0 nor 1 belongs to J, nonemptiness forces J⊂(0,1). Then P_J=S×{0}×J and vertical interpolation to any chosen height c∈J is a strong deformation retraction to S×{0}×{c}.

The formulas remain valid for degenerate slabs. A nonempty finite intersection of the slabs is another closed slab of thickness less than 1, so exactly the same proof applies to intersections. Each piece and each nonempty finite intersection is homotopy equivalent to a planar compactum. Borsuk's planar-movability theorem and shape invariance therefore give their movability. Their finite union can nevertheless be the nonmovable A.

The original cell-like-map route also has the necessary finite-dimensional hypotheses: each source is a compact subset of R³, the projected target is a compact subset of R², and the nonempty fibers are points or intervals. But a general cell-like equivalence theorem is unnecessary for accepting either the main argument or this supplement. No claim about arbitrary interval-fiber maps, outside the displayed slab geometry, is needed.

## 7. Preserved boundary of the result

For δ>0, N_δ(A) is compact, and Inv(N_δ(A)) is a closed invariant subset of it. The fiber-orbit classification shows that it is precisely A plus all bounded gaps whose entire closed segments lie in N_δ(A). Thus the formula for M_δ(A), its compactness, invariance, and eventual containment in a prescribed U are correct.

Large gap length alone provides no positive lower bound on the segment's distance from A. More precisely, if a unit-gap base p is within d of S×{0}, its entire closed vertical segment is within d of the corresponding full columns of A. This is a conditional geometric estimate; the acceptance does not require an additional assertion about which gap bases accumulate on the spine in a particular Bing embedding. A neighborhood may admit such long-gap additions, even though the length-based rule excludes them. No separate maximum-distance equality is used in this audit.

There is still no all-enlargements obstruction for a specified U and no proof that M_δ(A) is movable. Promoting the accepted counterexample to either conclusion would be an unsupported new step.

## Verification record

- Frozen artifact hash checked before and after the audit; original unchanged.
- Bing's exact embedding theorem and proof checked independently from the publisher PDF, including rendered printed pp.121–122.
- Borsuk's original movability definition, solenoid argument, shape-invariance corollary, and planar-movability corollary inspected in the scanned primary paper.
- Optional Olędzki–Spież embedding/shape distinction checked from the existing source PDF's rendered pages and text.
- Explicit maps, full quantifier order, relative/ambient transfer, fiber list, component estimate, flow completeness, invariant-set classification, and M_δ formula checked mathematically.
- Direct strong-deformation-retraction clarification supplied for slab pieces and their intersections.
- No remote mutations, additional substantive pass, source-body publication, or external outreach performed.

Acceptance is conditional only on the clearly identified established topology inputs; the authored construction and transfer argument pass this audit.
