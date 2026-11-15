# Paper-first independent reconstruction — record23203732

This initial is written after the entire actual six-page PDF, all198 controlling TeX lines and all six fresh own individual rasters have been read. No current peer/root scientific finding, deposited scientific code/result, archived review/triage body, or new foreign scientific primary body has been read. Earlier neutral source-acquisition custody is disclosed separately. The source's embedded claims about prior audits are manuscript assertions, not proof. Root137 comparison gate is CLOSED. This is a substantial reconstruction and falsification plan, not a final scientific disposition.

## Exact target and success criteria

The group is fixed, not an arbitrary rank parameter in the claimed result:

A=F(a,b₁,…,b₉₉), w=ab₁ab₂⋯ab₉₉a, J=⟨b₁,…,b₉₉,w⟩, B=J×⟨t⟩ with t of infinite order, Γ=A*_J B. Its displayed presentation has101 generators and100 commutator relators [t,bᵢ],[t,w]. Let X be the invariant conull free part of the right Bernoulli action on[0,1]^Γ, (xg)(h)=x(gh). For χ(a)=1,χ(bᵢ)=χ(t)=0 and every positive integer M, Y_M=X×ℤ/M with(x,r)g=(xg,r+χ(g)).

The full claims are: these specified actions are free ergodic p.m.p.; the displayed finite two-dimensional presentation complex is a K(Γ,1); β_n^(2)(Γ)=0 for every n≥0 by a direct proof using neither cost bound; every essentially free p.m.p. action has all the same Betti numbers, including nonergodic actions; Cost(R_X)≥1+η with η=1/(100·2⁶¹); and the infimum Cost_*(Γ) over essentially free p.m.p. actions is1. The latter is an infimum, not an assertion that a cost-one action exists. The Bernoulli relation consequently has strict Cost(R)−1≥β₁^(2)(R)−β₀^(2)(R), whereas Cost_*(Γ)=1+β₁^(2)(Γ) does hold.

The substantial external positive-cost input is explicitly OpenAI's pinned theorem, not a new conclusion proved independently in this note. The classical comparison/action-invariance/dimension results are separate external interfaces. Success requires the exact group, action, constants, domains and versions to match actual primary statements, with every local deduction valid at the original full scope. A counterexample to a central local step, or an unavailable/mismatched central external premise, must be recorded rather than repaired by substituting a narrower statement. No firstness or current worldwide-openness conclusion is assumed.

## Family1 — group, subgroup and presentation

The bᵢ generate a free factor of A. Group a reduced word in the proposed J basis into nonzero powers of w separated by nonempty reduced b-words. A w block starts and ends in a of the corresponding sign. A neighbouring b-word cannot cancel those a endpoints. Opposite w letters adjacent with no intervening b-word would be a reducible J-basis word and are excluded. Thus a nonempty reduced J-basis word cannot become trivial in A. This supplies the injective J→A map needed for the amalgam, independently of the later ℓ² chain calculation. The J→J×ℤ map is tautologically injective. Normal form embeds both vertex groups. In particular A and t survive, and Γ is countably infinite with the displayed finite generating set.

The presentation of J×ℤ is the free J basis with t commuting with its100 generators; amalgamating those basis elements with bᵢ,w in A gives exactly the stated101-generator100-relator presentation. The exponent-sum map χ_A on A restricts to χ(w)=100 on J. On B define χ(jtⁿ)=χ_A(j). Agreement on J extends to Γ, and a maps to1, so χ is onto. No quotient making t finite or collapsing A is silently used.

Falsifiers: a nontrivial reduced J word vanishing in A; an unverified vertex inclusion; a presentation relator not in the amalgam; a wrong count of100 a letters in w; or a height character that fails a commutator relation. The intended independent controls can check basis substitutions and exact words, but finite checks alone cannot establish J freeness.

## Family2 — action law, measure, free set and ergodicity

For the right action, ((xg)h)(k)=x(ghk)=(x(gh))(k), fixing the convention. Coordinate permutations preserve product measure. For g≠1, a fixed x must satisfy x(g)=x(1), an event of probability zero because these are distinct independent continuous coordinates. Countability makes the union of stabilizer exceptions null. The free set is invariant, Borel, conull and standard atomless, so restricting to it does not change measured invariants.

The finite-height formula obeys the action law because χ is a homomorphism and preserves product measure because each group element permutes the uniformly distributed heights. Its first coordinate makes every Y_M action free. Since t has infinite order, for any two finite coordinate supports, their tⁿ-translates intersect for only finitely many n. Cylinder events are therefore eventually independent; approximation in measure proves mixing of x↦xt. This proves Bernoulli ergodicity. In a Γ-invariant measurable subset of Y_M, each height section is t-invariant and has measure0 or1. The a-action cycles all M heights and equates these measures; the whole set is null or conull. No coprimality of M and100 is needed, and M=1 is included for the action lemma, though not for the later stated upper-bound construction.

Falsifiers: reversing right-action order; a nonfree finite-height extension; an assumption that B itself acts transitively on all heights; use of finite-group mixing; or a missing invariant-conull restriction. Infinite-order t, not merely infinitude of Γ, is essential to this particular mixing argument.

## Family3 — the triangular free basis and invariant subspace decomposition

Define u₀=1 and uᵢ=uᵢ₋₁abᵢ. The proposed new basis is a,u₁,…,u₉₉. Its inverse substitutions bᵢ=a⁻¹uᵢ₋₁⁻¹uᵢ recover old generators immediately; substituting the old definitions into the inverse formula telescopes, while substituting inverses into the recurrence recovers uᵢ by induction. Both homomorphism compositions are the identity on generators. Thus this is a free basis, and F=⟨u₁,…,u₉₉⟩ is a free subgroup of rank99 in A and Γ.

Set S=∑ᵢ₌₀⁹⁹uᵢ. Right multiplication by S preserves each left coset gF, not a right coset chosen in the wrong direction. Consequently ℓ²(Γ) decomposes as the orthogonal direct sum of the spaces on gF, and an operator kernel on Γ reduces to the kernel on F. No finite-index or amenability assumption is involved.

Falsifiers: an inverse substitution with a in the wrong position; omission of u₀=1; or a coset decomposition not invariant under the chosen right multiplication.

## Family4 — the bipartite graph is an infinite regular tree

Take two copies F_L,F_R and edges g_L—(guᵢ)_R for i=0,…,99. Distinct labels give distinct endpoints, and every vertex has degree100. The label0 edges join the two copies of each group element; two-step paths using0 and a nonzero label give the generators of F, so the graph is connected.

A nonbacktracking cycle has an alternating word uᵢ₁uⱼ₁⁻¹⋯uᵢₖuⱼₖ⁻¹=1 with consecutive edge labels different, including at the join. Delete the zero-label factors. Adjacent zeros are prohibited by nonbacktracking. A deletion joins factors of the same sign, so creates no inverse cancellation. Opposite-sign neighbours that remain were already adjacent with different nonzero indices. A nonzero factor remains in any nonempty such cycle. The resulting freely reduced nonempty word cannot be1 in F. Thus no cycle exists, and connectedness gives the infinite100-regular tree.

The argument concerns the actual two-layer graph and does not assert that a finite ball's adjacency matrix is invertible. Finite trees can have zero adjacency eigenvectors at their boundary. Such finite kernels would not falsify an assertion about a square-summable function on the full infinite regular tree.

Falsifiers: an identity reduced cyclic alternating word, duplicate labelled neighbours, disconnected layers, or an invalid cancellation after deleting0. A bounded small-rank word enumeration could test the combinatorics without substituting for this uniform proof.

## Family5 — zero is not an ℓ² adjacency eigenvalue

For a rooted infinite d-regular tree, d≥2, let E_n sum |f|² on the n-th sphere. If Af=0, at a vertex v of depth n≥1, the sum of f on its d−1 children is−f(parent(v)). Cauchy–Schwarz gives |f(parent(v))|²≤(d−1)∑children|f|². Summing over all v of depth n≥2 counts every parent at depth n−1 exactly d−1 times and every child at depth n+1 once. Hence E_(n−1)≤E_(n+1). Both odd levels and strictly positive even levels form nonnegative nondecreasing subsequences. Square summability makes their sums finite, so each level in these subsequences is0. A neighbour equation then gives f(root)=0 as well. This also covers d=2; no spectral gap or bounded inverse at zero is claimed.

For T f(g)=∑f(guᵢ), adjacency on the two copies has off-diagonal blocks T,T*. Its trivial kernel implies both T and T* are injective: apply it to(0,f) or(f,0). Right group-ring multiplication by S on coefficient functions is T*, because(fS)(g)=∑f(guᵢ⁻¹). The left-coset decomposition in Family3 transfers this to Γ.

Right multiplication by t−1 is injective separately: a killed vector is constant on each right orbit of the infinite cyclic subgroup⟨t⟩, and a nonzero constant on such an orbit is not square summable. Both operators are bounded finite sums of unitary translations.

Falsifiers: a reversed Cauchy–Schwarz inequality; counting the root as having d−1 children in the wrong step; treating dense range as bounded invertibility; interchanging T and T* without identifying coefficient action; or finite t-orbits. The proof specifically uses n≥2 for the clean layer count, then a separate neighbour equation at the root.

## Family6 — noncommutative cellular boundary and kernel

For ri=tbᵢt⁻¹bᵢ⁻¹ and rw=twt⁻¹w⁻¹, lift cells with coefficients on the left. A positive letter contributes its prefix to the relevant edge coordinate; a negative letter contributes minus the prefix after that letter. This directly derives the boundary without needing to trust a symbolic Fox programme. For an arbitrary word j commuting with t in Γ, the derivative in an A-generator x evaluates to(t−1)D_xj, and the t derivative to1−j. For w, D_aw=S and D_bᵢw=Pᵢ=uᵢ₋₁a.

Thus the completed left-Γ-equivariant chain maps use right multiplication, with

(d₂q)_a=q_w(t−1)S,
(d₂q)_bᵢ=qᵢ(t−1)+q_w(t−1)Pᵢ,
(d₂q)_t=∑qᵢ(1−bᵢ)+q_w(1−w),
and d₁(f)=∑f_x(x−1).

The telescoping identity S(a−1)+∑Pᵢ(bᵢ−1)=w−1 holds in the free group ring before adjoining t, and checks d₁d₂=0 after the commutator relations. From d₂q=0, the a coordinate and injectivity of right S imply q_w(t−1)=0; injectivity of t−1 gives q_w=0. Each bᵢ coordinate then gives qᵢ=0. No factor is commuted through S or Pᵢ. Composition of these two injective right operators needs no commutativity.

Falsifiers: a reversed prefix order, t coefficient w−1 instead of1−w, multiplication on the wrong side, use of t commuting with all of A, or cancellation of a noninjective operator. An independent exact free-word-ring telescoping check is a useful finite control; a commutative polynomial check would miss the ordering issue.

## Family7 — asphericity is stronger than an Euler-characteristic count

The ℓ² boundary injection restricts to finitely supported integral cellular chains. The universal cover of the presentation complex is simply connected and two-dimensional. Its H₁ vanishes by simple connectedness, H₂ vanishes by d₂ injection, and higher cellular homology vanishes because there are no higher cells. Together with reduced H₀=0, it is acyclic. If a simply connected CW complex with zero reduced homology had a first nonzero higher homotopy group, Hurewicz would identify it with a nonzero homology group. Hence all homotopy groups vanish, and Whitehead makes it contractible. The original finite complex is consequently a two-dimensional K(Γ,1).

A separate possible topological route is the tree-of-spaces description of the HNN form centralizing the injected J. The vertex graph is a K(A,1), and the edge graph is a K(J,1); lifted vertex and edge spaces are trees. One would need to give the precise CW/mapping-cylinder identification with the displayed presentation and the finite-subtree contraction argument. This route is distinct from deriving asphericity through ℓ² injection, but is not yet promoted as completed evidence in this initial.

Falsifiers: acyclicity of only rational rather than integral universal-cover chains; forgetting simple connectedness; or asserting contractibility solely from χ=0. The source's101/100 cell count by itself proves neither d₂ injectivity nor asphericity.

## Family8 — von Neumann dimensions and all degrees

For d₁, the perpendicular complement of its image is the intersection of the kernels of its coordinate adjoints. These equations make a function invariant under the generator translations. Because the generators generate infinite Γ, it is constant on Γ and therefore0 in ℓ². Thus closure(im d₁)=ℓ²Γ, without an assertion that im d₁ is closed.

Dimension additivity for finite Hilbert Γ-modules then gives dimΓ ker d₁=101−1=100. Since d₂ is injective, dimΓ closure(im d₂)=dimΓ ℓ²Γ¹⁰⁰=100. The reduced first homology has dimension0; the second has zero kernel, and reduced zeroth homology has dense-image quotient dimension0. Asphericity supplies a group resolution with no cells in higher degrees. This gives β_n^(2)(Γ)=0 for all n≥0, including degree0. Ordinary integral homology of the base complex is not being identified with these Hilbert-module homology groups.

A Mayer–Vietoris or Euler-characteristic shortcut is not an independent proof unless it controls the relevant map from the J contribution. The free edge group has nonzero β₁, so “the B vertex has an infinite cyclic factor” does not alone force all Betti numbers of the amalgam to vanish. That shortcut merely relocates the injectivity question and remains unsupported without a materially new mechanism.

Falsifiers: using ordinary dimension instead of von Neumann dimension, failing to close an image, forgetting β₀, or applying a cellular resolution before proving asphericity. Actual primary dimension statements must still be inspected for their conventions and hypotheses.

## Family9 — direct graphing upper bound, with exceptional points retained

For0<p<1 let C_p be the identity-coordinate event x(1)<p together with the set where every x(tⁿ)≥p, times all heights. The second event has measure0 because the tⁿ coordinates are infinitely many distinct independent coordinates. Including it ensures C_p meets every t-orbit, not just almost every orbit. The set is Borel and has product measure p.

Use the full t map, cost1, and b₁,…,b₉₉,w restricted to C_p, total added cost100p. Given z and a J-basis generator j, take n with ztⁿ∈C_p. The graphing relation contains the path z→ztⁿ→ztⁿj→zj because j commutes with t and the t map is available everywhere. Hence it contains the full B relation, even though j need not preserve C_p.

Add a on source heights0,…,98, costing99/M when M>100. If a edges from heights k through k+98 are already in the generated relation, take z at height k+99 and y=zu₉₉⁻¹ at height k. The path through u₁,…,u₉₉ uses only those a edges plus the full bᵢ edges, and ends at z. The full w edge connects y to yw=za. Hence the next a edge z→za is in the relation. Induction for k=0,…,M−100 supplies all source heights99,…,M−1, with the last edge wrapping to0. No height is omitted, and no M-coprimality is assumed. Every Γ generator edge is therefore generated. Cost≤1+100p+99/M for every p>0 implies Cost≤1+99/M by the defining infimum, not by claiming a measure-zero complete section.

Falsifiers: neglecting the null exceptional set while asserting every orbit, assuming C_p is J-invariant, missing the last wraparound edge, using an a edge before induction supplies its height, or taking p=0 as an actual chosen graphing. This argument is independent of the positive Bernoulli lower bound.

## Family10 — exact coefficient, inequality direction and small parameters

The external input is stated for K=e⁹⁶·96⁹⁹/95⁹⁵,0<α<1/200,Kα³<1/2. The chosen α=2⁻⁶¹ must satisfy strict inequalities. Factor K=e⁹⁶·96⁴(1+1/95)⁹⁵. The elementary strict inequalities(1+1/95)⁹⁵<e and e<3 imply K<3⁹⁷·96⁴. It is then enough to establish the exact integer comparison2·3⁹⁷·96⁴<2¹⁸³ and2⁶¹>200. Both are finite integer questions; no floating-point exponential evaluation is needed. The paper's rational gap is exactly α/100=1/(100·2⁶¹), not1/(100²·2⁶¹) or2⁻⁶¹ as an unscaled gap.

An independent exact integer result should be frozen before reading the deposited receipt. That result verifies admissibility only; it cannot validate the measure/graphing/shortening argument of the external lower-bound theorem.

Falsifiers: a weak inequality where strict admissibility is needed, arithmetic overflow, the wrong exponent3·61, omission of the factor2, a reversed bound on e, or confusing p in C_p with the unrelated α parameter.

## Family11 — measured invariants and the three different cost assertions

The main comparison has a zeroth Betti term. A free action of a finite group of order q gives β₀=1/q,β₁=0 and cost1−1/q, so dropping β₀ would already fail in that boundary case. Here Γ and all its free orbits are infinite, so β₀ is0. The desired primary interface is Gaboriau's invariance of relation Betti numbers under essentially free p.m.p. Γ actions, including nonergodic ones, plus the cost comparison for the relevant countable p.m.p. relations. Restriction to invariant conull sets must preserve these invariants.

Independently of the all-degree cellular proof, applying comparison/invariance to Y_M and the direct upper bound gives0≤β₁(Γ)≤99/M for every integer M>100. For any ε>0, choose M>max(100,99/ε), so β₁(Γ)=0. This only proves degree1, not all degrees. Every free action then has cost≥1, and the Y_M sequence gives Cost_*≤1+99/M for every M>100. Thus Cost_*=1 as an infimum. Cost(R_X)>1, obtained from the positive external lower bound, is compatible with that infimum, and must not be restated as every free action having cost1.

Falsifiers: action invariance only at one action while taking a limit over different groups, an unverified ergodicity restriction on the imported theorem, infimum/minimum conflation, or mistaking an orbit relation of a free action for an asserted treeing. The manuscript does not supply a treeing of R_X.

## Family12 — central positive-cost dependency, editions and credit

The exact foreign body still to be obtained is OpenAI's “A group without fixed price”, pinned to adc7f1241b42e322a6451854ab7e4b4c146bf78a, with the exact group and right Bernoulli/height actions. The actual Theorem1.1 must supply the stated α-domain and lower bound, rather than a related finite model or a different action. Its proof interfaces need inspection: graphing compression/deployment, finite permutation rank transfer and coefficient-sensitive planar shortening. No old audit narrative or supplied computed result will substitute for those bodies.

Gaboriau's comparison/action-invariance/dimension statements, the group-infimum definition and the precise historical question must be read in actual critical primary passages, with edition/page limits recorded. The earlier Popa–Shlyakhtenko–Vaes Remark6.6 is relevant to credit for the fixed-price implication; the target already credits it and disclaims novelty certification. The historical author triage body is an archived opinion and will not be imported as evidence merely because the manuscript cites it. Fox's path-prefix rule is reconstructed above; actual original-body access, if unavailable, must be qualified rather than invented.

Falsifiers: a mismatched original group, relative rather than ordinary cost, a lower bound requiring an unproved hypothesis, a different α normalization, or an imported proof bridge that transfers the central difficulty to an unsupported assertion. The main positive-cost conclusion remains an unverified external premise at this initial stage. No agreement with a current peer will count as proof.

## Family13 — chronology, source integrity and follow-up boundaries

Native version is ABSENT. The printed first page says October6,2026 and has no version line. Historical source acquisition UNREAD false/null fields stay unchanged even though this new review has now read the manuscript. The source is101 files=98 payloads+3 exact terminal controls, with35 original ZIP regular occurrences and one actual native PDF. The archived PDF is byte-identical to the standalone native PDF; there is no additional distinct manuscript or controlling TeX. All source files remain unchanged.

The source-only acquisition role and unrelated older excluded-row134 opinion exposure are disclosed. They provide no record137 scientific opinion or discovery evidence. The source helper programmes are custody code; none was rerun in this scientific lane. Own preparation used only an authenticated file inventory and ordinary Poppler metadata/text/raster operations. The original paper necessarily contains author statements about prior audits and preliminary triage; those assertions are not used as independent evidence. No supplied scientific programme, result object, archived review/triage or current peer/root finding has been read at this freeze.

Follow-up defaults null. A family-wide graph-of-spaces observation, a sharper admissible α, or a generalization of the rank parameter is not automatically a substantial publishable new question. The initial does not certify priority or replace the original theorem. The final decision must retain the strongest actually supported original statement and an exact remaining gap if one is found.
