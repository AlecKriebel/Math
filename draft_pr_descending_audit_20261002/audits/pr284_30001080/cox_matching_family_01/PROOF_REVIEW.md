# Independent Cox/matching and conditional-law review of PR 284

This review binds head `391cb662b1599ef564ff15b63cd8ed73c7d1f125`, problem 30001080, and the entire 22-body outer snapshot. It verifies the existing two-turn candidate only. The independent criteria and initial deductions were frozen in BASELINE.md before either author proof or the original PASS review was read. No current sibling-family or parent conclusion was read. The original review was read later as another claim to audit, not as authority.

**Finding:** the explicit Cox singleton matching theorem is mathematically sound under its stated canonical-law, original-intensity-background assumptions. The abstract all-Markov theorem also survives the conditional-law and hidden-state checks considered here. The OWR conclusion remains source-qualified: the verified Cox family sees the intensity measure, and no assertion about a class restricted to observing the Cox counting measure alone follows. The literal imported all-preserving-Markov distribution-of-ξ question is covered on the formal locally compact second countable Abelian/nonzero/locally finite framework. This family does not provide novelty clearance or authorize promotion.

## Exact statements verified

Let G be locally compact, second countable, Hausdorff and Abelian. Write θ_sµ(B)=µ(B+s). Let M be its standard Borel Radon-measure space, and let Q be a σ-finite measure on M\{0}. Choose a compatible proper translation-invariant metric d. For s≠t set

    U(s,t) = closed_ball(s,d(s,t)) ∪ closed_ball(t,d(s,t)).

For every Borel indicator b(µ,t) with b(θ_tµ,−t)=b(µ,t), the candidate defines a deterministic, translation-covariant involution τ_b on the pair (µ,η). It exchanges singleton atoms s,t of the locally finite integer-valued η only when η(U(s,t))=2 and b(θ_sµ,t−s)=1. It fixes everything else. Given µ, let ζ be ordinary Poisson with intensity µ, and define

    K_b(µ,s,A) = E_µ 1_A(τ_b(µ,ζ+δ_s,s)).

The verified assertion is that Q is mass-stationary precisely when Q is invariant under every K_b in this explicit family. The quantifier is over all measurable symmetric gates, not just a fixed geometric matching. µ is retained and observable as background. A constant gate alone is not the proved generating family.

Separately, for an arbitrary jointly measurable flow (Ω,F,θ), σ-finite Q and covariant locally finite ξ with Q(ξ(G)=0)=0, TURN_2 Theorem A assumes preservation of the *full Q law* under every invariant ξ-only preserving Markov kernel. Its test f may depend on every coordinate of ω. It concludes the full joint Mecke equation, not merely the canonical marginal version. Ω need not be standard Borel, and the ξ marginal need not be σ-finite. Theorem B has the canonical law as its state and does not make that stronger joint Cox claim.

## Matching validity, including multiplicity and ties

The candidate condition includes both endpoints because U contains s and t. If a singleton s had two distinct partners t,u, choose d(s,t)≤d(s,u). Then t is in the closed s-ball for pair (s,u); the union for that pair would contain the three distinct singleton sites s,t,u and have count at least three. Equal distances have the same obstruction. Thus partners are unique. The symmetric gate either retains or rejects both directions of the same pair. Transposing disjoint singleton pairs and fixing multiple atoms preserves η exactly and is an involution on all locations, including those outside η's support.

The pairing test is measurable, rather than just geometrically described. The set `{(s,t,u):d(u,s)≤d(s,t) or d(u,t)≤d(s,t)}` is Borel. Integrating its indicator against η makes η(U(s,t)) measurable in (η,s,t). Singleton evaluations η{s} are measurable by integrating the diagonal indicator. The proposed partner kernel is the integral of the Borel pairing indicator against η(dt); its mass is either zero or one because the potential partner is unique and a singleton. A unit-mass kernel on standard Borel G identifies a measurable point on the positive branch. Its zero branch is the measurable identity s. Translation invariance of d and the gate identity give covariance. This supplies the needed measurable allocation, with no hidden global selection.

The proper metric is essential. It makes U compact; local finiteness of µ makes µ(U)<∞. The checked Struble theorem provides the metric with bounded closed balls under second countability; closed bounded spheres are compact in the stated locally compact setting. Abelian commutativity turns left invariance into the simultaneous translation invariance used here. A nonproper arbitrary compatible metric would not justify the strictly positive void factors.

## Ordinary Poisson calculation, not conditional Palm guessing

For fixed µ and s, the root is *inserted* before evaluating the allocation. A distinct candidate t in ζ is selected only if its addition as the Mecke point, together with δ_s, produces singleton endpoints and no other point in U. Since the two inserted endpoints already contribute two counts, that event is exactly `{ζ(U(s,t))=0}`. Ordinary Poisson Mecke therefore gives

    K_b(µ,s,dt) = 1_{t≠s} b(θ_sµ,t−s) e^{−µ(U(s,t))} µ(dt)
                 + (1−r_b(µ,s)) δ_s(dt),

where r_b is the off-diagonal integral. The expectation definition makes K_b a probability and r_b≤1. This is not a supposition that a Campbell-rooted Cox process still has the unaugmented conditional law Poi(µ).

For two sites with masses a,b>0, the jump probability from the first site is `b e^{−a−b}`: the original Poisson count at the starting site must be zero and that at the partner must be exactly one. The reverse is `a e^{−a−b}`. Their mass fluxes both equal `ab e^{−a−b}`. Dropping the starting atom factor would produce fluxes `ab e^{−b}` and `ab e^{−a}`, unequal when a≠b. The candidate retains both factors. The diagonal candidate t=s is excluded, because it would not be a distinct endpoint; all staying probability, including multiple-root counts, is in the holding atom.

The finite Poisson series derivation permits coincident locations. At the coefficient level it uses n/n!=1/(n−1)!, so it applies to atomic intensity as well as diffuse intensity. For partners within distance R of s, U(s,t) is contained in the compact 2R ball around s. Restricting ζ to that ball reduces to finite intensity; monotone exhaustion and Tonelli recover the complete off-diagonal integral. No Q-Palm assumption is used. Measurability of the averaged kernel can either be obtained from the Poisson probability kernel µ↦Poi(µ) on the canonical counting space or directly from the displayed integral density and holding term.

Define the symmetric density `a_b(µ;s,t)=1_{s≠t}b(θ_sµ,t−s)e^{−µ(U(s,t))}`. Interchanging s,t gives the same value. Thus, for nonnegative φ, Tonelli gives

    ∫µ(ds)∫a_b(µ;s,t)φ(t)µ(dt) = ∫φ(t)r_b(µ,t)µ(dt).

Adding the holding mass (1−r_b) restores ∫φ dµ. All terms are nonnegative; no subtraction of infinite spatial integrals is required. This verifies µK_b=µ pathwise, for atomic, diffuse, mixed, finite-total and infinite-total locally finite µ.

## Why the Cox family suffices on the canonical law

Let R(µ,t)=(θ_tµ,−t), a measurable involution, and

    m(dµ,dt)=Q(dµ) 1_{t≠0} e^{−µ(U(0,t))} µ(dt).

The row bound gives m's first marginal ≤Q, hence σ-finiteness. Apply the assumed K_b-invariance to a finite-Q test f. The incoming and outgoing jump terms are both finite: the first is bounded by the full invariant Markov expectation Q(f), the second by Q(f) using r_b≤1. Removing the finite holding part is therefore justified.

For a Borel set A of M let F_A contain (µ,t) with µ∈A and θ_tµ∉A. For any Borel displacement set B let F=F_A∩(M×B). The two orientations F and RF are disjoint. The allowed gate 1_F+1_RF and finite-Q test 1_D1_A isolate exactly

    m((D×B)∩F_A)=R_*m((D×B)∩F_A).

A finite-Q partition and B=G give a common σ-finite rectangle cover on each F_A. Product-measure uniqueness extends equality from rectangles to all measurable subsets. A countable separating family of canonical measure sets, closed under complements, covers all pairs where θ_tµ≠µ. Only M's standard Borel property is required.

The remaining graph H contains pairs with t in the closed period subgroup H_µ={t:θ_tµ=µ}. On it R fixes µ and sends t to −t. Restriction µ|H_µ is a locally finite translation-invariant measure on this subgroup: subgroup shifts preserve µ and the subgroup. It is zero or a multiple of Haar. Haar inversion is valid on an Abelian group. The weight is even on H_µ because its reversal invariance and θ_tµ=µ imply a(µ;0,t)=a(µ;0,−t). Therefore m and R_*m also agree on H, pointwise in µ before Q integration. No measurable Haar normalization is selected.

The weight is strictly positive at every t≠0, so equality can be divided by it through increasing nonnegative truncations. This recovers reversal for c(dµ,dt)=Q(dµ)µ(dt) off t=0. At t=0, R is the identity, including when µ has a root atom. Hence c=R_*c everywhere. The classical Mecke characterization and Palm/mass-stationarity equivalence now apply. This is a direct verified path; it does not defer the crucial sufficiency to an unsupported point-stationarity theorem.

## Hidden auxiliary states and the all-Markov theorem

Canonical invariance cannot simply be promoted to joint invariance. Our G=Z/3 countercontrol takes ξ to counting measure at every hidden state u and Q=δ_{u=0}. Every shift has the same ξ marginal. The test `g(u,t)=1_{u=0,t=1}` has joint Campbell right side 1 and reversed left side 0. This is a concrete countermodel to discarding the hidden state; it is not a counterexample to Theorem A, whose assumption tests the full state.

Theorem A avoids that shortcut. The off-base-diagonal orientation gates separate only ξ states, while 1_D may inspect the full ω. The product argument above therefore gives full-state equality off J={θ_tξ=ξ} even when Ω is not countably generated. Its local jump weights are bounded by one. Campbell σ-finiteness follows from finite-Q pieces intersected with bounds on ξ(C_n), crossed with compact C_n. This argument never conditions on the potentially non-σ-finite ξ marginal.

On J the candidate needs extra period-subgroup kernels; canonical Haar symmetry alone would not control hidden-state shifts. Its κ_B is the normalized restriction of θ_sµ to H_µ∩B, with the identity when the denominator is zero. Parameter integration over the Borel period graph proves measurability; relative compactness of B and local finiteness prove the denominator finite. For fixed µ, every restriction (θ_sµ)|H_µ is zero or c_s times one fixed Haar measure. The coefficient c_s may vary by coset; the proof correctly does not assume it constant globally. Wherever positive, normalization yields the same restricted-Haar probability. That positive set is H_µ-invariant, so convolution preserves µ on it, and the complement is fixed.

The multiplier w_B(ξ)=ξ(H_ξ∩B) is unchanged by these period shifts. Testing full-law invariance against w_B f is a nonnegative identity and is valid without integrability of Q(w_B f). Inversion and −B give full joint Campbell reversal on J. The same finite-mass rectangle cover justifies product uniqueness. Thus this section genuinely supplies the missing hidden-state information and is compatible with σ-finite Q whose canonical pushforward is not σ-finite. No additional conditioning claim is needed.

## Boundary cases and exact remaining gap

- **Zero:** exclusion is essential. With ξ=0 Campbell mass vanishes and arbitrary auxiliary laws satisfy canonical marginal transport preservation, while the source's mass-stationarity definition requires no zero component. The verified theorem is about nonzero ξ only; it does not decide an unqualified zero-inclusive variant.
- **Atoms/multiplicity:** singleton counts are required after insertion; all higher multiplicities are fixed. Root atoms are included in the void probability. Tests and derivation agree.
- **Diffuse/mixed:** singleton Cox points and µ-background gates are measurable without marks. The same strictly positive density works; no positive density relative to Haar is assumed.
- **Periodic/subgroup-supported:** the period restriction can be zero. If positive it is Haar; the zero branch in the full-state kernels is the identity. T=0 reversal needs no division by zero.
- **Infinite mass/intensity:** only local finiteness is used in void events and compact exhaustion; no global mean-intensity assumption enters. σ-finite Q and the finite covers control subtraction and uniqueness.
- **Marked or arbitrary backgrounds:** Theorem A preserves the full ω by hypothesis. Theorem B preserves the µ law after averaging away ζ. It does not establish a Cox characterization for every hidden marked state from marginal µ invariance.

The exact visibility boundary is checkable. On G=Z/2, let η=(1,1), and let b(µ,t) accept when µ(G) is odd. This gate is invariant and symmetric. It exchanges the identical Cox configuration for µ=(1,2) but fixes it for µ=(2,2). Therefore the proved family is not measurable from η alone. A stricter Cox-count-only class cannot be asserted covered by renaming these matchings. The unsupported route “erase the intensity background and invoke the same gates” is blocked by this explicit dependency, not reopened here. There is no counterexample here to the strict class's characterization; that separate theorem is unverified.

## Source and question disposition

The relevant original OWR talk and the adjacent full transport talk were read from the whole pinned report. The talk discusses the pair (ξ,ζ+δ_0) and then asks about the distribution of ξ under Cox-derived kernels. Its short allocation description does not give a full formal observation-class definition. This supports the candidate's explicitly stated joint-object reading, but should not be represented as proving that every possible “Cox-only” convention is equivalent. The author itself retains this qualification. [Original OWR report](https://ems.press/content/serial-article-files/46189).

The formal 2009 body supplies the jointly measurable flow, LCSC Abelian group, nonzero condition, full-state Mecke criterion and Markov-versus-weighted distinction used above. Theorem A directly answers its Problem 7.3. It does not by logic answer Problems 7.4–7.7, whose weaker or different hypotheses are not implied in the needed direction. [Complete 2009 electronic reprint](https://arxiv.org/pdf/0906.2062v1).

The 2015 body retains a Markov gap after its weighted characterization; that is dated source context rather than current novelty evidence. The final 2011 formal Cox definitions remain unread: ordinary public requests yielded challenge HTML and the old author URL yielded HTML. No unread theorem is used in the matching derivation. [2015 author edition](https://arxiv.org/pdf/1405.7566v2), [2011 primary metadata](https://repository.lsu.edu/cosa/vol5/iss2/1/).

| Original or candidate question | This family's disposition |
|---|---|
| Canonical distribution of nonzero locally finite ξ under all invariant preserving Markov kernels, in formal LCSC Abelian setting | Mathematical PASS |
| Full abstract Q under ξ-only preserving Markov kernels (2009 Problem 7.3) | Mathematical PASS under its stated full-Q invariance |
| Canonical Cox matchings observing (µ,ζ+δ_s), the candidate's explicit reading of OWR closing question | Mathematical PASS, source-qualified |
| Cox allocations required to observe ζ+δ_s alone | Not settled by this proof; precise missing generating/observation-class reduction |
| Full joint auxiliary law inferred only from canonical ξ law | Invalid inference; explicit Z/3 countermodel |
| 2009 Problems 7.4–7.7, non-Abelian or non-second-countable groups, non-locally-finite measures, zero-inclusive versions | No resolution certified here |

## Artifact and replay audit

All 21 original attempt bodies, the complete QUEUE, and the nested author/turn/review manifests were read in full bytes and validated against the outer snapshot. ORIGINAL_BODY_CATALOG.json records the full absolute and repository-relative paths, bytes, SHA256, original modes, line counts and complete-body reads. The outer manifest is 12,008 bytes, SHA256 `9654108c98409ccb88b0ab9e448bb6075f852b138723b5178d8a4b8567f868ce`. The final author proof is 16,558 bytes, SHA256 `87664cd4c83fd77f0835165189a99119f936c5e1df14408cfaffb2ad8044bf21`.

All supplied code and JSON reports were inspected; the programs are finite controls, not formal proof checkers. Native execution in the pre-existing project Python environment reproduced 18,814 author-turn-1, 75,172 author-turn-2 and 186,869 original-review assertions, with stdout byte-identical to each original receipt. Own conditional_controls.py adds 142 exact symbolic and finite checks of the targeted failure mechanisms. REPLAY_COMPARISONS.json and streams retain actual argv, source hashes before launch, native child PIDs, full stdout/stderr, exit codes, timeout status and completed communicate/reap. No raw tool-parent waitpid status is invented.

Four essential primary PDFs reproduced their declared original bytes and hashes: OWR, 2009, 2015 author edition and Struble. The old 2007 native body returned maintenance text, so the original review's five-source hash claim is not falsely reported as fully reproduced now. PRIMARY_BODY_PINS.json distinguishes these cases. FAILURES.md preserves this, the 2011 HTML failures, environment probes, the corrected audit-driver schema error and the instruction inventory's absent live attempt. None caused an uncaptured mathematical failure to be reclassified as success.

Research work, code and captures stayed in this family folder. No branch, Git, publication, DOI, API write, cloud document or external-individual communication occurred. Discovery novelty and broader priority clearance remain the parent's separate gates.
