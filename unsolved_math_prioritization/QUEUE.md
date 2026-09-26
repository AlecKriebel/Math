# Prioritized research queue

Source: `37e53eabe540fb458758e198be61634bd02ee008`. Policy: `2.0-five-turn-proof`.

**Provisional expected-value ranking. Probabilities are subjective planning assumptions, not measured AI success rates.**
Budget per problem: Five substantive proof-attempt turns with ChatGPT6 Astra at ultra reasoning; modest exact checks only; no large exhaustive search. No problem is cleared for research until the readiness checks are recorded.

15,458 tracked; 1,951 eligible for triage; 13,507 with review holds.

| Rank | ID / code | Problem | EV | Difficulty | Proposed | Status | Turns | Chat | Findings | DOI |
|---:|---|---|---:|---:|---:|---|---|---|---| --- |
| — | KOU-16.45 | Kourovka Notebook Problem 16.45 | — | — | — | preprint_published | — |  | Published independently of the ranked catalogue; v1.0.1, 23 September 2026. Counterexample of order 100920 with b_f(G)=b(G)=3<4=mu′(G); manuscript and exact verification package in kourovka_16_45/. | [10.5281/zenodo.22929486](https://doi.org/10.5281/zenodo.22929486) |
| 1 | 30000990 / OWR-2040-002 | Gradient-Path Uniqueness in Persistence Pairings | 0.4602 | 3 | 2008 | preprint_published | 1/5 | https://chatgpt.com/c/6ab2984f-d808-83e8-a1e7-a64bec9f638a | 2026-09-22: turn 1/5 CLAIMS FULL NEGATIVE RESOLUTION (counterexample: 4 vertices/3 edges, persistence pair (b, ac) with ZERO gradient paths); slot freed, awaiting user verification | https://doi.org/10.5281/zenodo.22929556 |
| 2 | 6000011 / AMR-059-0011 | Integrable Radial Distributions and One-Conformal Flatness | 0.3994 | 3 | 1998 | claimed_solved | 1/5 | https://chatgpt.com/c/6ab2982f-e7a4-83e8-8320-31bc0b7010bf | 2026-09-22: turn 1/5 CLAIMS FULL NEGATIVE RESOLUTION (counterexample: M = S^2(1) x R, all radial distributions integrable but dual not 1-conformally flat); slot freed, awaiting user verification |  |
| 3 | 6700025 / AMR-066-0025 | Scalar Curvature Question [?24]: (i) It is unclear if the last step in the above argument is truly needed: conceivably, maps Φ ∶Sn−1→U(N) with | 0.3869 | 3 | 2017 | claimed_solved | 1/5 | https://chatgpt.com/c/6ab29832-39d4-83e8-84c6-b2151f11e558 | 2026-09-22: turn 1/5 CLAIMS FULL AFFIRMATIVE RESOLUTION (explicit strong deformation retraction of Lip<1/2 maps onto constant maps); slot freed, awaiting user verification |  |
| 4 | 30006217 / OWR-14299089-005 | Minimal Convex Difference Decompositions of CPWL Functions | 0.3681 | 3 | 2025 | queued | 0/5 |  | 2026-09-22 ~19:45 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — read-only chat inspection: no model attribution in the UI; registry: created with "Latest" + Extra High, 6 Pro absent from the picker all day). Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22: budget exhausted with NO resolution — final reply: "I cannot provide a correct proof of (A) or a correct counterexample of (B)". Transcript-grounded findings: turn 1/5 declined; turn 2/5 isolated the exact gap (unproved finite-representability theorem B(d,m)); turn 3/5 attempted a hidden-cancelling-ridges counterexample to finite representability but FAILED at certification (the 1-D Jordan-decomposition argument showed the 1-D candidate is arrangement-supported); turn 4/5 proved 1-D finite representability unconditionally (unique Jordan decomposition of the slope-jump measure) but could not close either (A) or (B) — decisive missing statement identified as a higher-dimensional Jordan theorem for signed polyhedral curvature; turn 5/5 (final) proved unconditionally only that for a FIXED polyhedral complex C the DC decompositions subordinate to C form a finite-dimensional polyhedron with a minimum-piece decomposition at a vertex (finite algorithm relative to C) — but could not prove or refute that a minimum-piece decomposition can always be chosen subordinate to f's own break complex Cf. Exact remaining gap: does there always exist a minimum-piece DC decomposition f=g−h with all ridges of g,h in Cf (is the global minimum always attained in the decomposition polyhedron of Cf)? Slot refilled with row 13. |  |
| 5 | 30000437 / OWR-1194-006 | Convex-Hull-Preserving Bloomings of Polytope Boundaries | 0.3517 | 3 | 2006 | queued | 0/5 |  | 2026-09-22 ~19:45 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — read-only chat inspection: no model attribution in the UI; registry: created with "Latest" + Extra High, 6 Pro absent from the picker all day). Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22: budget exhausted with NO resolution. Transcript-grounded findings: proved a local convex-hull-preserving blooming exists (continuity of supporting planes); proved dual-tree edge-cut unfolding reaches a planar endpoint (no rotational holonomy); proved separation cone nonempty for generic isolated contacts; reduced the problem to the infinitesimal contact-separation assertion (is the separation cone always nonempty at simultaneous first contacts? — Farkas positive dependencies compatible with convex normal equilibrium) — neither proved nor disproved. Slot refilled. |  |
| 6 | 30003895 / OWR-16407-007 | All-Order Expansion of the Noncommutative $\Phi^4$ Model | 0.3000 | 3 | 2018 | already_solved | 3/5 | https://chatgpt.com/c/6ab2b1af-4db4-83e8-9d7c-9e1f5ea0c501 | 2026-09-22: turn 3/5 CLAIMS FULL POSITIVE RESOLUTION — cites arXiv:1807.02945 eq. (31) as the definition of I_λ(a), proves the expansion holds to every order in λ via Lagrange–Bürmann inversion, derives exact functional equations (35),(36),(38),(39); slot freed, awaiting user verification |  |
| 7 | 30001163 / OWR-3389-016 | Equality Cases for Universal Eigenvalue Mean Inequalities | 0.2976 | 3 | 2009 | claimed_solved | 1/5 | https://chatgpt.com/c/6ab2b4d9-2d40-83e8-91b1-bf09ee520505 | 2026-09-22: turn 1/5 CLAIMS FULL NEGATIVE RESOLUTION — proves the inequality is ALWAYS STRICT at every finite J: derives exact remainder formula for Yang's inequality, shows the remainder cannot vanish (Fourier/unique-continuation argument on the ground state), concludes M₁(J)²−M₂(J)² > (E_{J+1}−E_J)²/4 for every J; slot freed, awaiting user verification |  |
| 8 | 30001385 / OWR-4136-011 | Simplex Equality Cases in Convex Geometric Inequalities | 0.2976 | 3 | 2009 | preprint_published | 1/5 | https://chatgpt.com/c/6ab2b529-dbfc-83e8-9dcc-e246207324e0 | 2026-09-22: turn 1/5 CLAIMS FULL AFFIRMATIVE RESOLUTION — equality forces K to be a simplex with all vertices on rS^{n−1}: proves extreme-point simplex decomposition lemma, exact second-moment identity, nonnegative deficit decomposition, interior-centroid argument forcing a single simplex; closes the equality-case gap left by Fradelizi–Paouris–Schütt; slot freed, awaiting user verification | [10.5281/zenodo.22983138](https://doi.org/10.5281/zenodo.22983138) |
| 9 | 30003646 / OWR-15956-012 | Odd-Density Limits for Multiplicative Functions | 0.2924 | 3 | 2017 | preprint_published | 1/5 | https://chatgpt.com/c/6ab2b6d0-8e40-83e8-9050-e88149812aa9 | 2026-09-22: turn 1/5 CLAIMS FULL RESOLUTION — limit always exists and equals 1/Σ f(2^k) (limsup argument via dilation by 2^K plus lower bound from monotonicity; A=∞ case gives 0); notes a likely source mismatch: the Oberwolfach report prints the slow-variation hypothesis but predicts the formula for the regular-variation version; slot freed, awaiting user verification; 2026-09-26: v1.0.1 preprint published on Zenodo after independent AI adversarial review; resolves the printed slow-variation question only, not the possible intended index-one formulation. | [10.5281/zenodo.22983161](https://doi.org/10.5281/zenodo.22983161) |
| 10 | 4700009 / AMR-046-0009 | A second-order differential equation | 0.2892 | 3 | 2020 | queued | 0/5 |  | 2026-09-22 ~19:45 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — read-only chat inspection: no model attribution in the UI; registry: created with "Latest" + Extra High, 6 Pro absent from the picker all day). Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22: budget exhausted with NO resolution. Transcript-grounded findings: turn 1 proved sign-changing and negative mean are necessary (Ureña's smooth p=5/3 counterexample shows they are not sufficient), gave an exact variational equivalence via scale-invariant functionals R_p and R_1; turn 2 proved a sharp local collision-accessibility criterion (integral condition at the zero — local vanishing rate decides collision accessibility but NOT existence), constructed same-quadratic-degeneracy solvable vs Ureña-nonsolvable weights, rigorously ruled out zero-pattern and hump-mass characterizations; turn 3 resolved the boundary-index subproblem NEGATIVELY (the true Poincaré map is intrinsically a partial map with nonempty-interior crash basin; canonical desingularization shows collision completion is an exit/stopping boundary — physical phase freezes, so no canonical time-T boundary return map and no intrinsic boundary index exist; the boundary index is not even a functional of f, requiring an added collision law); turn 4 gave the canonical survivor continuum, scalarization of the second shooting displacement as Dirichlet-energy crossing, the reach-energy-or-compactify-to-contact-measure dichotomy, "solvability can change only through Floquet degeneracy or collision", and the finite-Fourier blindness theorem (no finite Fourier truncation criterion can decide existence); turn 5 (final) proved the universal twist/monotonicity lemma FAILS (explicit conjugate-point degeneracy), showed degree theory cannot exclude extra survivor components (Ureña's argument selects one component, not uniqueness), and narrowed every extra component to either compact in the positive region or with inf min x = 0 — but could not exclude compact semiperiodic isolas or accumulating extra components. Final verdict: the requested elementary complete classification is not presently available. Slot refilled with row 12. |  |
| 11 | 2535 / KOU-21.26 | Kourovka Notebook Problem 21.26 | 0.2880 | 2 | 2026 | queued | 0/5 |  | 2026-09-22 ~19:45 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — read-only chat inspection: no model attribution in the UI; registry: created with "Latest" + Extra High, 6 Pro absent from the picker all day). Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22: turn 3/5 PARTIAL but very strong — NO resolution of KOU-21.26 claimed. Proves: (1) exact fiber formula through an elementary abelian chief factor, P ∩ P^{t+v} = C_{D̂}(a_p(t)+v) (point-stabilizer problem for the quotient overlap D acting on V); (2) proposition: every globally minimal p-intersection is realizable over a quotient-minimal stratum D ∈ 𝒟_p^min (coordinatewise sufficiency); (3) the joint-selection induction is EXACTLY equivalent to the necessary-and-sufficient affine intersection condition ⋂_{p≠r}(−a_p(t)+Ω_p(D_p(x̄))) ≠ ∅ for some simultaneously quotient-good x̄; (4) structural obstruction theorem: a general noncommuting fiber-synchronization theorem would contain the STILL-OPEN Alon–Jaeger–Tarsi conjecture over F₇ (p=7 remains unresolved; Nagy–Pach 2026 proves p>61, p≠79 only); (5) nonabelian minimal normal subgroup analogue: primes outside π(N) reduce to simultaneous centralizer minimization, but for p ∣ |N| the Schur–Zassenhaus mechanism genuinely breaks. Verdict: "The proposed minimal-counterexample induction cannot presently be completed by a general 'stratify and choose a common fiber vector' theorem." Exact remaining gap: the Sylow-overlap-specific assertion — a simultaneously quotient-good x̄ for which every D_p(x̄) is V-optimal and the affine sets −a_p(x̄)+Ω_p(D_p(x̄)) have nonempty total intersection — neither proved nor refuted. Message 4/5 sent pressing that exact gap; reply 4/5 RECEIVED (~11:54 PDT) — PARTIAL: no complete proof or counterexample to the full Sylow-overlap-specific assertion. Proves: Lemma 1 (optimal fiber sets Ω_p(D) are "affinely thick" — not contained in any proper affine subspace, ⟨Ω_p(D)⟩=V, via Maschke); Lemma 2 (cyclic effective overlap ⇒ Ω_p(D) = V \ C_V(Z), one proper linear bad subspace); Theorem 3 (two translated optimal strata always synchronize when one effective overlap is cyclic — offset-independent); consequence: for a two-prime quotient, joint selection can fail only if BOTH active quotient-minimal overlap groups have noncyclic effective actions on V; the F₃² ⋊ D₈ / order-360 mechanism cannot be promoted to a joint-selection counterexample. Also: for ≥3 quotient primes, individually V-optimal strata need not lie in one common diagonal Sylow orbit (transitivity fails from three primes on — Lisi–Sabatini Jan 2026 revision). Exact remaining gap: the first genuinely unresolved case — two simultaneously realizable V-optimal quotient-minimal overlaps D_p, D_q with both effective groups noncyclic; prove the translated optimal-vector sets always intersect, or exhibit a Sylow-overlap example with the covering (16) by a union of affine fixed-point subspaces. Message 5/5 (FINAL) CONFIRMED SENT (read-only check ~12:30 PDT); reply 5/5 RECEIVED (~12:28 PDT) — NO resolution claimed; 5/5 exhausted → UNSOLVED. Final verdict: "I cannot honestly close Kourovka 21.26." Problem remains OPEN; published 2026 Lisi–Sabatini paper and reviewed TheoremDB record list it as open conjecture. Full-session transcript-grounded results: (1) exact fiber formula through elementary abelian chief factor, P ∩ P^{t+v} = C_{D̂}(a_p(t)+v); (2) every globally minimal p-intersection is realizable over a quotient-minimal stratum (coordinatewise sufficiency); (3) joint-selection induction is EXACTLY the affine intersection condition ⋂_{p≠r}(−a_p(t)+Ω_p(D_p(x̄))) ≠ ∅; (4) Lemma 1: optimal fiber sets Ω_p(D) are "affinely thick" — not contained in any proper affine subspace; (5) Lemma 2: cyclic effective overlap ⇒ Ω_p(D) = V \ C_V(Z); (6) Theorem 3: two translated optimal strata synchronize when one effective overlap is cyclic (offset-independent); (7) commuting abelian effective overlaps always synchronize; (8) cocycle constraint: two-prime quotient shifts are not arbitrary translations — displacement lies in (1−t)V; (9) explicit K = (F₃² ⋊ D₈)² (|K|=5184) construction witnessing the structurally-real noncyclic, noncommuting configuration (D₂ ≅ C₂², D₃ ≅ C₃⁴, [D₂,D₃] ≠ 1); (10) F₃² ⋊ D₈ / order-360 mechanism cannot seed a joint-selection counterexample. Obstructions: a general noncommuting fiber-synchronization theorem would contain the still-open Alon–Jaeger–Tarsi conjecture over F₇; for ≥3-prime quotients, diagonal transitivity fails (Lisi–Sabatini Jan 2026 revision). Exact remaining gap: the elementary-abelian-chief-factor case where both effective overlap actions are noncyclic AND genuinely noncommuting — excluding (or realizing) the multi-affine-subspace covering Ω₂ ⊆ −(1−t)c + ⋃ C_V(B); plus, for ≥3-prime quotients, the diagonal-orbit correlation issue among V-optimal minimal strata. |  |
| 12 | 5200005 / AMR-051-0005 | Open Problems on Billiards and Geometric Optics | 0.2878 | 3 | 2021 | queued | 0/5 |  | 2026-09-22 ~19:45 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — read-only chat inspection: no model attribution in the UI; registry: created with "Latest" + Extra High, 6 Pro absent from the picker all day). Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22: slot refilled from row 10 (marked unsolved at 5/5); chat created ("Billiard Caustic Symmetry Proof", creation task's chat confirmed via read-only sidebar check ~12:06 PDT). Problem: smooth convex plane billiard table symmetric about axis l, convex caustic C — must C be symmetric about l? Turn 2/5 PARTIAL (~13:00 PDT) — no resolution claimed. Proves the "Finite-order non-obstruction theorem" / "Formal symmetry-breaking theorem": the qℤ Fourier modes generate a genuine formal degree of freedom, NOT an obstruction — second-order gives H₂ = −(S/(2cτ²))u² (a q-mode squares into a 2q-mode; with u=sin(qx), the second-order table has twice the rotational symmetry of the caustic); cubic asymmetry removable by v = −(2/(3cτ²))u²; induction via (20)–(24): every odd-order defect d_N ∈ O is solvable via A_N = d_N/(λu) using the Chebyshev identity sin((2k+1)X)/sin(X) = U_{2k}(cos X); truncated curves are honestly smooth and strictly convex, with exact-string-table symmetry defect O(ε^{2N+3}). Thus no finite-order perturbative rigidity proof is possible along this branch. Exact remaining gap: prove or disprove CONVERGENCE of the formal symmetry-breaking branch (18) — for q=3, show that for all sufficiently small nonzero ε there exists a smooth even π-periodic correction A_ε(X) with g_ε(θ) = 1 + ε sin 3θ + ε² A_ε(3θ) such that its exact string transform satisfies H_ε(m + π/3) = H_ε(m); a convergent/Nash–Moser construction gives a genuine smooth counterexample, a proof that the separatrix-splitting functional is nonzero for every ε ≠ 0 kills the branch despite vanishing to all algebraic orders. Message 3/5 SENT (~13:00 PDT) pressing the convergence question NOW (convergent/Nash–Moser construction → genuine smooth counterexample; or proof the separatrix-splitting functional is nonzero for every ε ≠ 0 → branch killed); reply 3/5 generating — classify next run. 2026-09-22 ~13:48 PDT: read-only check — reply 3/5 STILL GENERATING (Extra High thinking; prior replies took 24m and 39m; thinking covers reflection symmetry, quotient dynamics, smoothing, linearization, operator injectivity, inverse uniqueness, bifurcation, reversible dynamics; web search active). 2026-09-22 ~14:00 PDT: reply 3/5 RECEIVED (complete; "Worked for 57m 17s") — PARTIAL, no resolution claimed ("I cannot rigorously choose (a) or (b) yet"; "So I do not claim a smooth counterexample or a rigidity proof in message 3"). Key new results: (i) EXACT linearization of the string transform (28): feared B'-terms from B(x±η_g(x)) cancel identically — true linearized operator is a variable-window averaging operator, removing composition/derivative loss as the obstacle; (ii) exact q=3 symmetry operator (33) converges only STRONGLY, not in operator norm, to −4/3 I — for every fixed ε≠0, D_A Φ is not bounded below on C^0 (37), so hard Banach-space IFT genuinely fails and Nash–Moser would need an actual tame inverse; (iii) Borel realization: honest C^∞ family of genuine caustics/string tables whose asymmetry is flat in ε (38) — any rigidity theorem must detect something smaller than every power of ε; (iv) flat obstruction located exactly as a coupled two-window cohomological matching problem (41)–(43) with repelling endpoint (f'(0)=1+2/(3ε)) and attracting endpoint (f'(π)=1−2/(3ε)) — natural object is a smooth matching modulus. Cites 2026 Koudjinan–Ramírez-Ros high-order persistence paper (§6.2 asks convergence openly) and Arnold–Bialy rounded-Star-of-David undecided configuration. Exact remaining gap: global solvability theorem for Φ(ε,A)=0 despite high-frequency degeneration (37) — construct tame right inverse for coupled cohomological operator (39) and show matching modulus vanishes after allowed2026-09-22 ~14:25 PDT: reply 4/5 RECEIVED ("Worked for 20m 31s") — PARTIAL, no resolution claimed ("I cannot give a valid rigidity proof or counterexample here"; "I do not have a mathematically valid basis to announce either a counterexample or rigidity. The nonperturbative issue survives."). Major exact reformulation: (i) "EXACT PRESCRIBED-DYNAMICS REDUCTION" (44)–(55) — once the phase-locked quotient dynamics z (equivalently F) is prescribed, the exact counterexample problem becomes a LINEAR functional-differential equation (52) for H: H(X)cos s(X)+qH'(X)sin s(X) = H(F(X))cos s(F(X))−qH'(F(X))sin s(F(X)) — no nonlinear string equation, no implicit η_g, no composition derivative loss involving an unknown caustic; (ii) exact local theorem: hyperbolic fixed points create NO local convexity obstruction (56)–(59): H'(X₀)=0, H''(X₀)=−k²/q²·H(X₀), radius of curvature H(1−k²)>0 when |k|<1; (iii) explicit Gutkin constant-angle construction DEFINITIVELY ruled out at rational rotation number via Cyr's theorem (tan(lπp/q)=l tan(πp/q) has no rational solution |l|≥2 ⇒ only circle); (iv) existing Nash–Moser machinery (Koudjinan 2022 seminar; Koudjinan–Ramírez-Ros 2026, §6.2 convergence problem explicitly open) does not supply the missing theorem by citation. Exact remaining gap: find—or rule out—a nonzero z for which the linear equation (52) has a positive even π-periodic solution H; once such z,H exist, (53) reconstructs the caustic explicitly and the string equation is automatically satisfied — if G fails reflection symmetry about one of H's axes and (55) holds, that is a complete smooth counterexample; conversely, rigidity amounts to proving every sufficiently small solution of (52) with H(−X)=H(X)=H(X+π) forces reconstructed G to share those reflection axes. Only the global monodromy of the linear equation (52) remains. FINAL message 5/5 being sent demanding the resolution NOW. 2026-09-22 ~14:32 PDT (handoff from send-task): message 5/5 CONFIRMED PRESENT in transcript (dup 1/5–5/5; begins "This is message 5 of 5 — your FINAL message. There are no more messages after this."); the steer correctly did NOT send a duplicate. Assistant actively generating reply 5/5 (web search + thinking on the monodromy equation (52)); 2026-09-22 ~14:39 PDT: reply 5/5 RECEIVED ("Worked for 9m 31s") — NO RESOLUTION claimed ("Final verdict: I cannot rigorously close the problem"; "I do not have a valid smooth counterexample, and I do not have a rigidity proof"). Final sharpening: exact multiplicative coboundary identity R(x)=V(Fx)/V(x) (61) with W=V∘F (60); endpoint product (62); beyond-all-orders matching modulus M_{H,z}(x)=Σ_n log R(Fⁿx)=log(H(b)/H(a)) (63), with the q=3 branch requiring M_{H,z}=0 on every heteroclinic orbit (64); summand log R(x)=2 artanh(qH′(x)tan s(x)/H(x)) (65) has no fixed sign, so no positivity argument for rigidity; infinite-dimensional flat-correction space defeats naive transversality. Single missing ingredient: a theorem about the global matching operator — a zero on the admissible flat-correction space produces the smooth rounded-Star-of-David counterexample; a fixed-nonzero functional on its cokernel gives rigidity. Fresh literature check through Sept 2026: no published resolution; Arnold–Bialy rounded-Star-of-David configuration still open. 5/5 budget exhausted with NO resolution → UNSOLVED. Slot refilled with row 17. |  |
| 13 | 30005899 / OWR-14298367-006 | $\Gamma$-Supercyclicity of Composition Operators and Weighted Shifts | 0.2817 | 3 | 2024 | preprint_published | 1/5 | https://chatgpt.com/c/6ab2d948-71a0-83e8-beaf-67e2c3375863 | 2026-09-22: turn 1/5 CLAIMS FULL AFFIRMATIVE RESOLUTION — the Γ-supercyclicity equivalence (T_f Γ-supercyclic ⟺ B_w Γ-supercyclic) holds for EVERY Γ ⊆ ℂ with no additional hypothesis on Γ (affirmative answer to the Oberwolfach question); proof via topological conjugacy of T_f to an E-valued bilateral translation S_E, a general amplification lemma reducing scalar and E-valued versions of the same translation to identical Γ-supercyclic behavior, plus an exact arbitrary-Γ tail criterion (36)-(37); slot freed, awaiting user verification | [10.5281/zenodo.22983147](https://doi.org/10.5281/zenodo.22983147) |
| 14 | 30000798 / OWR-1590-008 | Square Values of Primitive Binary Cubic Forms | 0.2809 | 3 | 2007 | queued | 0/5 |  | 2026-09-22 ~19:50 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — created 2026-09-22, when 6 Pro was absent from the picker all day; registry: created with "Latest" + Extra High). A live three-dot-menu re-inspection of the real chat (https://chatgpt.com/c/6ab2d74b-07b8-83e8-95ae-39b4b8be44d5) is pending at the time of this edit; the invalidation stands regardless since 6 Pro was unavailable when the chat was created. Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22: slot refilled from row 11 (2535 / KOU-21.26, marked unsolved at 5/5); chat creation CONFIRMED (prior creation task had already created the chat "Resolve Cubic Square Problem"; initial prompt sent 1/5 with full-resolution framing, verbatim problem statement from unsolvedmath.com/problems/30000798, 5-message budget disclosed — messageId confirmed); no duplicate created; Reply 2/5 RECEIVED (~13:28 PDT) — PARTIAL, no resolution claimed ("I cannot honestly give either the requested affirmative proof or an explicit counterexample"). Major correction: identifies a genuine FLAW in reply 1's "2-adic globalization" reduction — the gcd-2 square from Simon's 2w²-alternative lives on a DIFFERENT quadratic twist E_{2d}: W²=2df(T), not E_d; scaling to (2u,2v) does NOT convert the rational point to E_d, it only gives a nonprimitive integral representative of the same rational direction. Replaces the gap with the correct finite descent/Selmer-selection problem: explicit genus-zero descent via Simon's ideal factorization (x−θz = κξ² ⇒ projective conic C_κ: Q₂=0; finitely many κ from Rˣ/Rˣ² × Cl(R)[2]); primitivity enters as the parity invariant v_p(gcd(x,z)) mod 2 on each local descent branch — Hasse–Minkowski solves one fixed twist but the quantifiers can't be interchanged: ∀p ∃κ_p with admissible point vs. ∃κ ∀p with admissible point. Nonmaximal-order case: different conductor branches give different κ's. Candidate F₀ = 7X³+10X²Z+5XZ²+6Z³ checked and is NOT a counterexample (F₀(−1,1)=4=2²), though it shows distinct 2-adic branches carry distinct descent data. Exact remaining gap: compute/control the finite admissible descent set Sel_F^prim (18) for the nonsplit (2,2,2) stack — prove at least one global conic twist simultaneously occupies all required primitive local components, or find an explicit cubic where every global conic twist fails at at least one bad prime. Message 3/5 CONFIRMED SENT (~13:50 PDT read-only check: transcript shows 3 user messages); 2026-09-22 ~14:07 PDT: reply 3/5 RECEIVED ("Worked for 35m 21s") — PARTIAL, no resolution claimed ("I have not produced a valid full affirmative proof or a counterexample in message 3"). Sharpens the endpoint: (i) Proposition (22) — in degree 3 the fake 2-Selmer set is EXACT (S_F(ℤ)≠∅ ⟺ Sel_fake_2(S_F)≠∅), because every degree-3 covering is a conic (genus formula g(C_δ)=0 + Hasse–Minkowski + weak approximation + Santens' adelic characterization of integral points); (ii) SYNCHRONIZATION THEOREM (23) — H¹(ℚ,M) → ∏_{v∈T} H¹(ℚ_v,M) is surjective for every finite T (via weak approximation in K, q=N(α) made a square at T so δ=α/q is a genuine global class); (iii) GOOD-PRIME LEMMA — at p∉S={∞}∪{p: p|2f₀Disc(F)}, a local twist class is admissible for a primitive ℤ_p-point iff UNRAMIFIED (necessity via étale group-scheme pullback; sufficiency via Hensel + smooth conic special fiber). So the ONLY possible obstruction: the synchronized global twist may acquire forbidden ramification at NEW primes outside S. Santens' relative (0;2,2,2) theorem closes the good-prime portion but leaves the bad-prime localization obstruction. Exact remaining gap: prove that for every primitive irreducible cubic the finite set loc_S(H_S) intersects ∏_{v∈S} B_v — equivalently, that among the primitive local squareclasses at the finitely many primes dividing 2f₀Disc(F), one tuple annihilates the dual unramified Poitou–Tate obstruction; or find an explicit cubic where every tuple has nonzero pairing with some dual Selmer character. Ordinary local incompatibility is now ruled out; the S-unit/2-class-group obstruction is the sole surviving target. Message 4/5 being sent pressing that finite intersection NOW. 2026-09-22 ~14:32 PDT: message 4/5 CONFIRMED present in transcript; reply 4/5 STILL GENERATING — classify next run. Turns → 4/5. 2026-09-22 ~15:12 PDT: reply 4/5 RECEIVED — NO RESOLUTION claimed ("Current verdict": neither a proof that (34) always holds, nor a verified cubic counterexample). Chat hit platform conversation-length limit ("You've reached the maximum length for this conversation") — message 4 of 5 was the LAST the chat could accept; no fifth message possible → chat exhausted at 4/5 → UNSOLVED. Final frontier (transcript-grounded): the finite obstruction is reframed as Poitou–Tate exact sequence (32) with dual Selmer pairing criterion (33)/(34) — determine whether the primitive local subsets B_v always contain a tuple in the kernel of the Poitou–Tate pairing; equivalently, prove a universal vanishing theorem for the primitive integral Brauer–Manin obstruction on the (2,2,2) cubic stack, or exhibit an explicit primitive cubic whose finite primitive Selmer set is empty. Key refinement: B_v are not subgroups but unions of local orbits (failure of primitive conditions to be cohomologically linear), so Poitou–Tate gives an obstruction criterion, not a vanishing theorem. A genuine counterexample must have H_S ≠ ∅, every global class locally obstructed at some bad prime, yet every completion primitively soluble with branches unchoosable compatibly. No further reduction remains — this is the final arithmetic obstruction. |  |
| 15 | 30001200 / OWR-3394-010 | Almost Input-to-State Stability of the Damped Pendulum | 0.2800 | 3 | 2009 | already_solved | 1/5 | https://chatgpt.com/c/6ab2e0ae-c4bc-83e8-9cf4-d502315ea89a | 2026-09-22: slot refilled from row 13 (30005899, marked claimed_solved at 1/5); chat created ("Resolve Pendulum Stability", Latest + Extra High thinking, model picker still has no "ChatGPT-6 Astra Pro"; creation task checked sidebar first — no existing chat, no duplicate). Turn 1/5 CLAIMS FULL AFFIRMATIVE RESOLUTION — "Resolution: Yes": the damped pendulum on S¹×ℝ is almost input-to-state stable; cites Angeli–Praly, IEEE Trans. Automatic Control 56(7):1582–1592 (2011), DOI 10.1109/TAC.2010.2091170, as having resolved the 2009 Oberwolfach problem affirmatively (paper reportedly motivated by this exact problem); self-contained verification via the Angeli–Praly almost-ISS criterion — strict proper Lyapunov function V=H+½ωsinθ with V̇≤−¼(ω²+sin²θ), downward equilibrium exponentially stable, upright (π,0) a hyperbolic saddle with λ₊=(√5−1)/2>0, ultimate boundedness limsup H ≤ 2+‖d‖∞², input-dependent null exceptional set via local rectifiability + Liouville pullback; slot freed, awaiting user verification |  |
| 16 | 30004195 / OWR-17130-011 | Hausdorff Absolute Continuity of PDE-Constrained Measures | 0.2733 | 3 | 2019 | queued | 0/5 |  | 2026-09-22 ~19:45 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — read-only chat inspection: no model attribution in the UI; registry: created with "Latest" + Extra High, 6 Pro absent from the picker all day). Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22: slot refilled from row 15 (30001200, marked claimed_solved at 1/5); chat created ("Resolve PDE Measure Problem", Latest + Extra High thinking, model picker still has no "ChatGPT-6 Astra Pro"; sidebar checked for all three identifiers first — no pre-existing chat, no duplicate). Initial prompt sent 1/5 (full-resolution framing, verbatim problem statement from unsolvedmath.com/problems/30004195 — A=∂_{x1}³+∂_{x2}³+∂_{x3}³, real Radon μ on ℝ³ with Aμ=0 distributionally: must μ≪ℋ²?; source: Oberwolfach Reports, PDEs (2020), DOI 10.4171/owr/2019/34, pp. 2033–2097; 5-message budget disclosed). Reply 1/5 RECEIVED (~13:48 PDT) — PARTIAL, no resolution claimed. Verdict: problem "still open"; refuses complete proof or rigorous counterexample. Proves: (1) 2-wave cone Λ_A²=ℝ² (every 2-plane meets Σ={ξ:ξ₁³+ξ₂³+ξ₃³=0} by odd-IVT) so existing theorem gives only the ℋ¹ bound; (2) Σ contains no 2-plane (a=b=−1 ⇒ 3a²b=−3≠0) ⇒ no nonzero 1-rectifiable part; (3) exponent 2 sharp via characteristic hyperplane measures (even with transverse Cantor measure — Tonelli keeps μ≪ℋ²); (4) Ayoush/Stolyarov/Spector–Stolyarov (Mar 2026) improvements don't close it — odd topology of Σ obstructs k=2 spectral separation. Exact remaining gap: a purely unrectifiable/fractal A-free measure charging an ℋ²-null set. Message 2/5 SENT (~13:50 PDT, send confirmed in transcript) pressing that exact gap NOW — explicit fractal counterexample construction with full A-free verification, or complete proof that Aμ=0 ⟹ μ≪ℋ²; required one-line closing verdict "FULL RESOLUTION"/"NO RESOLUTION"; 2026-09-22 ~15:10 PDT: reply 2/5 RECEIVED (finished; explicit verdict "NO RESOLUTION") — PARTIAL but sharply narrowed. Rigorous results: (1) Σ contains no 2-plane (a=b=−1 ⇒ 3a²b=−3≠0); (2) every A-free measure supported on a plane is smooth relative to ℋ²↾M — plane-supported ν satisfies the normal system C(D)ν=Q(D)ν=L(D)ν=0, and since a common real zero of C,Q,L would put a plane in Σ, the combined operator is elliptic ⇒ hypoellipticity ⇒ ν∈C^∞, killing Cantor-in-a-characteristic-plane counterexamples; (3) transverse Cantor measures μ=∫ ℋ²↾(n⊥+tn) dσ(t) with n∈Σ are still μ≪ℋ²; (4) Riesz-product mechanism killed algebraically: a,b,a+b,a−b ∈ Σ with a,b noncollinear forces a plane in Σ, contradiction — successive characteristic oscillations can only reproduce the slab measures of (3); (5) constant-density surface measures Aδ(z−f(x,y))=0 force D²f=0, i.e. collapse to characteristic planes. Exact remaining gap: the local Morrey bound |μ|(B_r(x)) ≤ C_{K,μ} r² (x∈K, 0<r<r_K) — Fourier division by p(ξ) loses control in arbitrarily small angular neighborhoods of Σ, and no two-dimensional elliptic slice exists to upgrade the one-dimensional control. Message 3/5 SENT (~15:03 PDT) pressing that gap NOW (prove the Morrey bound, or produce the purely unrectifiable A-free singular measure). 2026-09-22 ~15:24 PDT: read-only check CONFIRMED reply 3/5 FINISHED (3 user messages; exact verdict line "NO RESOLUTION") — PARTIAL. Reply 3/5 recasts the Morrey bound as the exact endpoint inequality (6) via exact duality (sup of total variation = dual norm / distance from range of A*); characteristic plane measures show the exponent sharp; remaining gap is inequality (14) — neither proved the matching upper bound nor produced an A-free sequence violating it. Message 4/5 being sent (~15:25 PDT; send-task with pre-send guard: abort unless transcript is exactly 3 user messages with finished reply 3/5) demanding ONE of: (1) prove (14) ⇒ Morrey bound ⇒ μ≪ℋ² (full affirmative), or (2) exhibit an A-free sequence violating (14) and construct the purely unrectifiable singular counterexample (full negative); FULL RESOLUTION / NO RESOLUTION verdict line required.  2026-09-22 ~15:53 PDT: reply 4/5 RECEIVED (finished; exact verdict line "NO RESOLUTION") — PARTIAL but decisive. Major result: auxiliary inequality (14) RIGOROUSLY DISPROVED (best possible uniform exponent at most 1, not 2) via exact real A-free smooth wave packets V_N dx whose total variation concentrates onto the line L={(ℓ,ℓ,0)} (|V_N|dx ⇀* (c_a/√2)ℋ¹↾L); but the signed measures converge distributionally to zero (μ_N ⇀ 0), so this does NOT yield a counterexample to the original problem — it only kills the (14) reduction as too strong. Exact remaining gap (single, sharply defined): can ONE real A-free Radon measure retain coherent mass through infinitely many concentration scales (no high-frequency sign cancellation) on an ℋ²-null set? Message 5/5 (FINAL) CONFIRMED SENT (~15:57 PDT; pre-send guard passed: exactly 4 user messages, reply 4/5 finished with NO RESOLUTION verdict); reply 5/5 now generating — classify next run. Budget exhausted after this reply. Turns → 5/5. Turns → 5/5. 2026-09-22 ~16:24 PDT: reply 5/5 RECEIVED ("Worked for 4m 53s"; 5 user messages confirmed) — NO RESOLUTION (closing: "A claim of 'FULL RESOLUTION' at this point would require inserting an unproved theorem at exactly that step."). 5/5 budget exhausted with NO resolution → UNSOLVED. Transcript-grounded final findings: round 4's Morrey-route is ruled out as too strong but yields no fixed singular solution; key obstruction is microlocal — WF_x(μ) ⊂ Σ={ξ:ξ₁³+ξ₂³+ξ₃³=0} and Σ has a 1-dimensional conic gap but no 2-dimensional gap (every real 2-plane through 0 meets the odd cubic cone), so the available microlocal dimension theorem gives only the known 1-dimensional bound and cannot establish μ≪ℋ²; the foundational paper frames the desired implication as the higher-order ℓ*_A=2 conjecture (not a theorem); later finite-configuration/dimension-stable-measure results improve dimensional tools but not this endpoint; recent literature still describes optimal general bounds as unresolved. Exact remaining gap (unproved AND unrefuted): (∂₁³+∂₂³+∂₃³)μ=0 ⟹ |μ|(E)=0 for every E with ℋ²(E)=0 — no uniform r² concentration estimate can prove it (normalized exact solutions can concentrate variation onto a line while signed mass escapes through oscillation); missing either a fixed-measure rigidity theorem or an explicit coherent multiscale construction. No counterexample claimed. Slot refilled with row 22. |  |
| 17 | 30004298 / OWR-17293-016 | Coefficient Normalization of Positive Definite Homogeneous Forms | 0.2733 | 3 | 2019 | preprint_published | 1/5 | https://chatgpt.com/c/6ab2f6e5-af8c-83e8-b792-f0b9e049f3c2 | 2026-09-22 ~14:55 PDT: turn 1/5 CLAIMS FULL AFFIRMATIVE RESOLUTION, verdict line "FULL RESOLUTION" (verified by read-only transcript check; chat title "Proof of Normalization Theorem"; 1 user message, reply finished "Worked for 2m 15s"). Proof: every positive-definite real homogeneous form of degree d is linearly equivalent to one satisfying Brandes's coefficient normalization, in fact the stronger absolute-value version \|n′(j₁,…,j_d)\| ≤ (n′(j₁,…,j₁)⋯n′(j_d,…,j_d))^{1/d} as actually printed in the Oberwolfach report (Problem 11, 2019 problem session). Mechanism: minimize ψ on an auxiliary Euclidean sphere (d necessarily even), normalize A(v^d)=1; the quadratic correction B=Q−L⊗L satisfies B≥0 with ker B=ℝv; key identity log R(ε) = −ε² Σ_{r<s} B(a_r−a_s,a_r−a_s)+O(ε³) for the normalized multilinear correlation R(ε)=A(y₁,…,y_d)/Π ψ(y_r)^{1/d}; a clustered basis x_i(ε)=v+εw_i near the minimizer makes R_J(ε)<1 for every mixed tuple, giving (16); S: e_i↦x_i yields ψ′ with the required inequality. Slot freed, awaiting user verification. NOTE: the abandoned duplicate chat (https://chatgpt.com/c/6ab2f694-5c00-83e8-9f15-0e8ed373a690) independently claimed the same result in its reply 1/5 — no follow-up messages may ever be sent to it. | 10.5281/zenodo.22982894 |
| 18 | 20002593 / AIM-PROBABILITY-0035 | Exact Potts censoring on one edge and a monotonicity obstruction | 0.2720 | 3 | unknown | already_solved | 1/5 | https://chatgpt.com/c/6ab2fa93-a918-83e8-81ff-b6215632c706 | 2026-09-22 ~15:10 PDT: slot refilled from row 17 (30004298, marked claimed_solved at 1/5); chat created (sidebar searched for all three identifiers — no pre-existing chat; "Potts censoring" hit was only a Library FILE "ph20_exact.pts", unrelated). Initial prompt sent 1/5 with full-resolution framing, verbatim problem statement from unsolvedmath.com/problems/20002593 (Censoring for the Potts model — q-state Potts, q=3, start from all green: does deterministically censoring a sequence of spin flips only increase total variation distance to stationarity? Peres–Winkler covers monotone chains; Potts q≥3 is not monotone), strict 5-message budget disclosed, FULL RESOLUTION / NO RESOLUTION verdict line required. Model picker showed NO named models (no "ChatGPT-6 Astra Pro", no "Latest") — only thinking-effort setting, already at Extra High (4 of 4), kept. NOTE: reported chat URL has a "local-chatgpt:" ID format (unusual; may be a not-yet-synced local chat) — VERIFY in the next run's read-only check; if unreachable, recreate. 2026-09-22 ~15:28 PDT: read-only check CONFIRMED the local-chatgpt URL is DEAD (redirects to the ChatGPT home page — not a real chat); the real designated chat was found via the sidebar ("Potts Censoring Counterexample", created today): https://chatgpt.com/c/6ab2fa93-a918-83e8-81ff-b6215632c706 — 1 user message (initial prompt 1/5, full-resolution framing), reply 1/5 FINISHED ("Worked for 2m 35s"). 2026-09-22: turn 1/5 CLAIMS FULL NEGATIVE RESOLUTION — verdict line "FULL RESOLUTION": on a 5-vertex graph, a deterministic nine-opportunity update word with the seventh update censored gives a rigorous counterexample — heat-bath Glauber dynamics, zero-field 3-state ferromagnetic Potts at β=3, started from all-green; recomputed by hand in exact rational arithmetic over all 3^5=243 states, so the sign of the TV-distance difference is an exact integer inequality (reported ~1.03e-5, proven exactly); the censored chain ends STRICTLY CLOSER to equilibrium, so censoring does NOT only increase total-variation distance. Key reduction: the fifth vertex is never updated, and after the six common initial updates the final coordinate factors out identically in both chains via global color symmetry, collapsing the TV difference to the (A,B,C) marginal, decided exactly via a 14-orbit color-swap decomposition of the 27 spin triples. Slot freed; awaiting user verification. |  |
| 19 | 30006597 / OWR-14299909-012 | Algebraicity Under Central-Binomial Untwisting | 0.2720 | 3 | 2026 | queued | 0/5 |  | 2026-09-22 ~19:45 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — read-only chat inspection: no model attribution in the UI; registry: created with "Latest" + Extra High, 6 Pro absent from the picker all day). Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22 ~15:15 PDT: slot refilled from row 14 (30000798, marked unsolved at 4/5 — chat hit platform conversation-length limit, no fifth message possible); chat-creation task launched (browser-task:434f2fab-0c88-47f8-ac00-4d4ff80df3b3). 2026-09-22 ~15:24 PDT: read-only check CONFIRMED the chat exists at the URL above ("Algebraicity Untwisting Problem"; initial prompt 1/5 with full-resolution framing present); reply 1/5 STILL GENERATING (deep-researching binomial coefficient integrality) — classify next run. Turns → 1/5. 2026-09-22 ~15:35 PDT: reply 1/5 RECEIVED — PARTIAL, verdict "NO RESOLUTION" ("I cannot honestly claim a complete proof or counterexample"). Strongest progress: (i) f must be a globally bounded G-function (D-finite + integer coefficients + exponential growth via regular-singular convergence); (ii) strong p-adic constraint — for every good odd prime p, half of first-level Cartier components vanish, Λ_r(F)≡0 mod p for (p+1)/2≤r≤p−1, via Kummer's theorem on v_p(C_n); (iii) COMPLETE theorem: the untwist is algebraic for every rational Gauss-hypergeometric F (new hypergeometric lemma via Christol's criterion + Fürnsinn–Yurkevich contraction; denominator set {γ,1/2} has at most one integer). Exact remaining gap: converting the Cartier vanishing restrictions into finite monodromy/algebraicity for arbitrary nonrigid rank-two Fuchsian equations with accessory parameters (hyperelliptic/Picard–Fuchs, arbitrarily high genus). Message 2/5 CONFIRMED sent; reply 2/5 RECEIVED (~15:55 PDT, "Worked for 17m 27s") — PARTIAL, verdict "NO RESOLUTION" ("I cannot give a valid full proof or counterexample without inventing a theorem that I cannot justify"). New completed results: (1) the motivating paper's arbitrarily-high-genus X_1(N) construction is provably NOT a counterexample — every L_{N,P} it produces has an explicitly algebraic untwist (including the genus-10 N=21 example); (2) COMPLETE positive theorem for the entire Beukers-Zagier three-term/Apery-Heun four-singularity rank-two family — central-binomial divisibility forces B=0 via prime descent, surviving hypergeometric untwist algebraic via Chebyshev identity. New exact gap: extend the prime-descent argument to arbitrary finite-width rank-two Fuchsian recurrences (accessory-parameter case); the requested Cartier rigidity would need the unsolved general Grothendieck-Katz p-curvature conjecture. Message 3/5 being sent pressing on the arbitrary-width prime descent or an explicit surviving transcendental untwist NOW. RESOLVED 2026-09-22 ~16:14 PDT: browser handoff confirmed message 3/5 WAS present and reply 3/5 RECEIVED (worked 17m 21s) — PARTIAL, verdict "NO RESOLUTION". New completed results: (1) finite-width prime-barrier theorem: outside a fixed finite set of bad primes, the reduction of Q_d mod p has a root in [m,(p-1)/2], hence Q_d splits completely over Q (irreducible quadratic trailing coefficient impossible), without Grothendieck-Katz; (2) descent determines a full zero interval: a_{rho_p+1}...a_h=0 mod p, the root is the only barrier; (3) corollary: both Q_d roots integral => f is a polynomial (a transcendental counterexample needs nonintegral rational exponents at infinity); (4) sharpening: a nonpolynomial example with linear Q_d needs a negative half-integral root (-1/2,-3/2,...), -1/2 being the central-binomial-twist value; (5) the root cannot be crossed by single-prime reduction: explicit certificate with F_0=2F1(1/2,1/2;1;16x), where mod p the root T=-1/2=h admits arbitrary x^p-constant data A(x^p), so NO single-prime argument can cross the obstruction; (6) general formulation F(x) in K_p tensor V_p with dim V_p <= 2; higher Kummer blocks mod p^s do not fix it either. Exact remaining gap: an inter-prime or characteristic-zero rigidity theorem controlling the x^p-constant series A_p,B_p in (15) (tried negative constructions all failed: rational Gauss, shifted hypergeometric, Apery/Zagier, high-genus motivating family). 2026-09-22 ~16:16 PDT: message 4/5 CONFIRMED sent; reply 4/5 RECEIVED — PARTIAL, explicit NO RESOLUTION (4th consecutive). Key new content: the inter-prime block-compatibility statement is NOT a consequence of the finite-width Fuchsian recurrence alone (p-block and q-block partitions are not refinements of one another; coefficientwise compatibility does not force A_p,B_p to constants; a further rigidity argument about the recurrence itself would be needed); route (B) negative constructions all remain eliminated (hypergeometric => algebraic via Christol, Apery/Heun => degenerate-algebraic, high-genus motivating family => explicitly algebraic radical untwists). Unresolved possibility narrowed to: rank-two Fuchsian recurrence with accessory parameters and an exceptional half-integral trailing root whose surviving characteristic-zero block data encode infinite monodromy after untwisting — neither existence disproved nor an example constructed. Precise unproved statement: whether every rank-two Fuchsian finite-width recurrence with central-binomial-divisible coefficients has an algebraic inverse central-binomial untwist, including the half-integral trailing-root barrier cases. 2026-09-22 ~16:19 PDT: FINAL message 5/5 CONFIRMED sent; reply 5/5 RECEIVED — NO RESOLUTION — budget exhausted at 5/5, marked UNSOLVED. Final-turn content: proved the sharp theorem of what the machinery actually implies (globally bounded G-function; half-Cartier vanishing; Q_d splits over Q; integral roots => polynomial; nonpolynomial => negative half-integral trailing root); disproved the "push the barrier to infinity" idea (forced zero interval has FIXED length m+1, not growing with p; for alpha=-1/2 the interval is EMPTY); established the p-curvature shortcut is unavailable (equation cannot distinguish A(x^p) from a scalar constant; any elimination must use cross-prime arithmetic, not available); all natural counterexample families concretely eliminated. Sharpest open lemma: the "Central-binomial Cartier rigidity lemma" — whether every rank-two Fuchsian finite-width recurrence with central-binomial-divisible integer coefficients, trailing polynomial with only rational roots and nonintegral ones negative half-integers, has an algebraic inverse central-binomial untwist. Slot freed; refilled with the next queued row. |  |
| 20 | 30006627 / OWR-14299911-029 | Corner Peeling in Cubical Subcomplexes of Integer Three-Space | 0.2720 | 3 | 2026 | queued | 0/5 |  | 2026-09-22 ~19:45 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — read-only chat inspection: no model attribution in the UI; created with "Latest" + Extra High, 6 Pro absent from the picker all day; remaining turns abandoned). Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22 ~15:28 PDT: slot refilled from row 18 (20002593, marked claimed_solved at 1/5). 2026-09-22 ~15:34 PDT: chat created ("Open Research Problem"; sidebar searched for all three identifiers — no pre-existing chat, so no duplicate; model picker had no "ChatGPT-6 Astra Pro", used "Latest" with Extra High thinking 4/4). Initial prompt sent 1/5 with full-resolution framing, verbatim problem statement from unsolvedmath.com/problems/30006627; 5-message budget disclosed; FULL RESOLUTION / NO RESOLUTION verdict line required. 2026-09-22 ~16:22 PDT: reply 1/5 RECEIVED (finished, "Worked for 36m 41s") — NO RESOLUTION. Transcript-grounded results: piece-incidence graphs Tx,Ty,Tz are trees (graph-of-spaces/Van Kampen) forcing X contractible; hypotheses hereditary under corner deletion (antistar-collapse) → reduces to "one-corner theorem"; exact planar curvature certificate κ(v)=1−d/2+q/4; leaf-piece criterion (planar corner v is a corner of X iff v∉A or D(v)⊆A, A=carrier footprint); planar-only protection realizable but cubical completion defeats simplest 3D attempt; positive curvature does not imply a corner (Q3-minus-opposite-vertex obstruction); small-box computational search found no corner-free example (evidence only, not used for verdict). Exact remaining gap: the "leaf-protection theorem" — prove a transverse carrier cannot protect every planar corner of every leaf piece, or exhibit a corner-free X(G) with full cubical completion verified. Message 2/5 being sent pressing that gap NOW (pre-send guard: exactly 1 user message + finished reply 1/5 with NO RESOLUTION verdict). 2026-09-22 ~16:53 PDT: reply 2/5 RECEIVED (finished) — PARTIAL, exact verdict "NO RESOLUTION". Transcript-grounded: does not close the leaf-protection lemma — has neither (a) a proof that every leaf piece contains an unprotected planar corner, nor (b) a fully verified corner-free cubical complex satisfying both hypotheses. States the exact unresolved lemma: leaf integer coordinate piece P with unique adjacent half-piece footprint A (P and all coordinate sections simply connected, X(G) full cubical completion of its 1-skeleton) ⇒ exists planar corner v of P with v ∉ A or D(v) ⊆ A, D(v) = unique maximal planar cell of P containing v. Only possible counterexample mechanism = finite full cubical complex where every leaf piece has every planar corner covered by a transverse carrier while the carrier omits the corner's planar maximal cell — neither ruled out nor constructed. Message 3/5 CONFIRMED SENT (~16:56 PDT; pre-send guard passed: exactly 2 user messages + finished NO RESOLUTION reply 2/5); reply 3/5 generating — classify next run. Turns → 3/5. |  |
| 21 | 9900005 / AMR-098-0005 | Setwise convergence versus total-variation convergence of shifted processes | 0.2720 | 3 | unknown | claimed_solved | 1/5 | https://chatgpt.com/c/6ab30d56-ce6c-83e8-8a9b-e082d8ad3229 | 2026-09-22 ~16:20 PDT: slot refilled from row 19 (30006597, marked unsolved at 5/5); chat-creation task launched (browser-task:91605a2b-0748-4d85-b5a6-80f139eb2a48). 2026-09-22 ~16:25 PDT: creation task reported a local-chatgpt-format URL (dead format, same as row 18 issue) — held as unverified pending sidebar check. 2026-09-22 ~16:28 PDT: task handoff returned the CANONICAL chat URL https://chatgpt.com/c/6ab30d56-ce6c-83e8-8a9b-e082d8ad3229 ("Setwise Versus Total Variation"), message 1/5 confirmed in thread, full reply extracted — turn 1/5 CLAIMS FULL NEGATIVE RESOLUTION. Claimed result: No — setwise convergence of shifted process laws does NOT imply total-variation convergence. Explicit counterexample: fair Bernoulli product measure nu on {0,1}^Z with left shift theta; perturbed measure mu via density f=1+a(2w_0-1), 0<a<1; mu_n = law of theta_n X under mu converges setwise to nu by strong mixing (mu_n(A) -> nu(A) for every measurable A), but ||mu_n - nu||_TV = a/2 > 0 for all n (d mu_n/d nu = f o theta^{-n}, |f-1|=a everywhere). Slot freed, awaiting user verification. |  |
| 22 | 30005619 / OWR-14297736-030 | Magnetic-Laplacian Eigenvalue Infima on Closed Surfaces | 0.2717 | 3 | 2023 | queued | 0/5 |  | 2026-09-22 ~19:45 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — read-only chat inspection: no model attribution in the UI; created with "Latest" + Extra High, 6 Pro absent from the picker all day; remaining turns abandoned). Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22 ~16:26 PDT: slot refilled from row 16 (30004195, marked unsolved at 5/5); chat-creation task launched. 2026-09-22 ~16:31 PDT: creation task COMPLETED — sidebar searched for all identifiers, no pre-existing chat, no duplicate. Chat created at the canonical URL above (NOT a dead local-chatgpt URL); initial prompt 1/5 sent with full-resolution framing, verbatim problem statement from unsolvedmath.com/problems/30005619 (closed Riemannian surface (M,g), i>1: prove inf_A λ̄_i(M,g,A) ≥ C(M,g) > 0 over all real magnetic potentials A, plus construction of critical metric-potential pairs; source: Geometric Spectral Theory (2024), Oberwolfach Reports DOI 10.4171/owr/2023/36); 5-message budget disclosed; FULL RESOLUTION / NO RESOLUTION verdict line required. Model: "Latest" (no "ChatGPT-6 Astra Pro" in picker; GPT-5.6 Sol / GPT-5.5 also shown, disabled "Pro"); Extra High thinking 4/4. 2026-09-22 ~16:52 PDT: reply 1/5 RECEIVED ("Worked for 44s") — PARTIAL, exact verdict "NO RESOLUTION". Transcript-grounded: gauge reduction (only the gauge class of A matters; Rayleigh-quotient formulation); compact-modulo-gauge proof that dim ker Δ_A ≤ 1 via unique continuation ⇒ λ₂(A)>0 for any fixed connection; unresolved = escaping families of potentials — the missing "magnetic compactness theorem" (i-dimensional almost-parallel sections forcing A_n to converge modulo gauge); critical-pair construction identified as a separate nonlinear variational problem (vanishing-current Euler–Lagrange condition), no general construction from the bound alone. Message 2/5 CONFIRMED SENT (~16:54 PDT; pre-send guard passed: exactly 1 user message + finished NO RESOLUTION reply 1/5). 2026-09-22 ~17:22 PDT: reply 2/5 RECEIVED ("Worked for 58s"; 2 user messages) — PARTIAL, exact verdict "NO RESOLUTION". Transcript-grounded: kills the proposed route — ‖(d−iA_n)u_{n,k}‖² → 0 does NOT force A_n bounded modulo gauge, because almost-parallel sections see A_n only where they have non-negligible mass and do not control curvature dA_n where low-energy states are small; polar-decomposition sharpening u_n=ρ_n e^{iφ_n} splits small energy into ρ_n almost-constant in H¹ plus A_n ≈ dφ_n in the ρ_n²-weighted norm, but the weight degenerates at nodal/concentration regions with no uniform positive lower bound for ρ_n; i-dimensional case would need quantitative nonvanishing |U_n(x)| ≥ c > 0, which ordinary and quantitative unique continuation cannot supply (quantitative constants depend on A_n itself); Bochner/Weitzenböck fails (curvature term i dA has no a priori sign or L^p control over all real potentials). Escape routes explicitly open: noncompact gauge orbits, flux concentration, curvature concentration. Exact remaining gap — one statement, unproved and unrefuted: every sequence of real potentials on fixed closed (M,g) with λ_i(A_n) → 0 (i ≥ 2) has a subsequence whose almost-kernel dimension collapses to ≤ 1 — equivalently dim{u : ‖(d−iA)u‖² ≤ ε} ≤ 1 uniformly over ALL real A for ε(M,g) small. Message 3/5 being sent pressing for the finished result NOW: (1) prove the uniform estimate, or (2) construct an explicit escaping A_n sequence with concentrating curvature and i linearly independent approximate parallel sections; FULL RESOLUTION / NO RESOLUTION verdict required. Turns → 3/5. |  |
| 23 | 10600039 / AMR-105-0039 | Virtual-knot problem 39 — We still do not know whether the free knot whose Gauss diagram is a heptagon (i.e. | 0.2700 | 3 | unknown | queued | 0/5 |  | 2026-09-22 ~19:45 PDT — MODEL AUDIT: attempt INVALIDATED (did not run on ChatGPT-6 Astra Pro — read-only chat inspection: no model attribution in the UI; created with "Latest" + Extra High, 6 Pro absent from the picker all day; remaining turns abandoned). Row reset to unattempted with a fresh 0/5 budget for a future 6-Pro attempt. Transcript-grounded findings from the invalidated attempt retained below for reference (not a 6-Pro attempt):  2026-09-22 ~17:01 PDT: slot refilled from freed rows (12 claimed_solved + 8 unsolved freed slots, only rows 20/22 active — third slot now filled). Chat created (sidebar searched for 10600039 / AMR-105-0039 / heptagon / virtual-knot — the only hit was a Library document FILE, not a chat, so no duplicate; no sign-in gate or CAPTCHA). Initial prompt sent 1/5 (full-resolution framing, verbatim problem statement from unsolvedmath.com/problems/10600039: "We still do not know whether the free knot whose Gauss diagram is a heptagon (i.e. consists of 7 chords each of which is linked with precisely two adjacent ones) is trivial."; 5-message budget disclosed; FULL RESOLUTION / NO RESOLUTION verdict line required). Model: "Latest" + Extra High thinking 4/4 (no "ChatGPT-6 Astra Pro" in picker; GPT-5.6 Sol / GPT-5.5 / disabled "Pro" also shown). Canonical chatgpt.com/c URL (not a dead local-chatgpt URL). Reply 1/5 generating at handoff — classify next run. Turns → 1/5. |  |
| 24 | 11000263 / AMR-109-0263 | Question 6 — DoesX3 equal 0 in Zn? | 0.2700 | 3 | unknown | queued | 0/5 |  |  |  |
| 25 | 30002145 / OWR-12008-005 | Rigidity of Symmetric-Gradient Differential Inclusions | 0.2693 | 3 | 2012 | queued | 0/5 |  |  |  |
| 26 | 30005795 / OWR-14298162-002 | Valuation Bounds When the Center Meets the Negative Part | 0.2693 | 3 | 2024 | queued | 0/5 |  |  |  |
| 27 | 30005473 / OWR-12697711-006 | Irreducibility of Exposed-Point Varieties of Generic Discotopes | 0.2675 | 3 | 2023 | queued | 0/5 |  |  |  |
| 28 | 30002867 / OWR-13678-008 | Matrix Characterization of Complete Intersections | 0.2675 | 3 | 2015 | queued | 0/5 |  |  |  |
| 29 | 30005897 / OWR-14298367-003 | Shadowing Without Bounded Distortion | 0.2651 | 3 | 2024 | queued | 0/5 |  |  |  |
| 30 | 30005934 / OWR-14298374-003 | Wishart Processes with Noninjective Semigroups | 0.2651 | 3 | 2024 | queued | 0/5 |  |  |  |
| 31 | 30000224 / OWR-824-008 | Set-Theoretic Cohen–Macaulay Ideals in Characteristic Zero | 0.2641 | 3 | 2005 | queued | 0/5 |  |  |  |
| 32 | 30000439 / OWR-1194-009 | Gaps Between Piecewise-Linear and Linear Embedding Dimensions | 0.2637 | 3 | 2006 | queued | 0/5 |  |  |  |
| 33 | 30000819 / OWR-1595-012 | Volume Bounds for Holes in Very Ample Semigroups | 0.2634 | 3 | 2007 | queued | 0/5 |  |  |  |
| 34 | 30001075 / OWR-2090-028 | Common Tangent Loci of Three Convex Bodies | 0.2630 | 3 | 2008 | queued | 0/5 |  |  |  |
| 35 | 30006390 / OWR-14299518-003 | Transversals in Random Subsets of Projective Planes | 0.2618 | 3 | 2025 | queued | 0/5 |  |  |  |
| 36 | 30001696 / OWR-4798-013 | Ball-Product Structure of Cross-Polytope Subcomplexes | 0.2616 | 3 | 2011 | queued | 0/5 |  |  |  |
| 37 | 30001947 / OWR-11454-005 | Nontrivial Witt Pairings in $\mathbb Z_2$-Witt Spaces | 0.2616 | 3 | 2011 | queued | 0/5 |  |  |  |
| 38 | 10000062 / AMR-099-0062 | Local metric homogeneity forcing periodic triangulations | 0.2611 | 3 | 2012 | queued | 0/5 |  |  |  |
| 39 | 10400115 / AMR-103-0115 | Problem 6.7 — (S.J. | 0.2600 | 3 | unknown | queued | 0/5 |  |  |  |
| 40 | 20002011 / AIM-GEOMETRY-0349 | Conformal-primitivity obstruction and curvature-only rigidity on surfaces | 0.2600 | 4 | unknown | queued | 0/5 |  |  |  |
| 41 | 20002052 / AIM-GEOMETRY-0390 | Local primitives versus divergence terms | 0.2600 | 3 | unknown | queued | 0/5 |  |  |  |
| 42 | 2800102 / AMR-027-0102 | 10 Lectures and 42 Open Problems — Gaussian singular-value monotonicity | 0.2594 | 3 | 2015 | queued | 0/5 |  |  |  |
| 43 | 30003713 / OWR-15987-026 | Homology of Free-Lie Current Algebras over Square-Zero Extensions | 0.2571 | 3 | 2018 | queued | 0/5 |  |  |  |
| 44 | 30003955 / OWR-16415-018 | Disconnected Preimages of Subsurfaces Under Finite Covers | 0.2571 | 3 | 2018 | queued | 0/5 |  |  |  |
| 45 | 6800007 / AMR-067-0007 | Manifolds modelled on flag manifolds — Question 2 | 0.2571 | 3 | 2018 | queued | 0/5 |  |  |  |
| 46 | 30004186 / OWR-17128-002 | Stability of Peaked Reduced Ostrovsky Waves | 0.2562 | 3 | 2019 | queued | 0/5 |  |  |  |
| 47 | 7000004 / AMR-069-0004 | Geometry of Curves and Surfaces — Problem 1.4 | 0.2562 | 3 | 2019 | queued | 0/5 |  |  |  |
| 48 | 7000019 / AMR-069-0019 | Geometry of Curves and Surfaces — Problem 4.3 | 0.2562 | 3 | 2019 | queued | 0/5 |  |  |  |
| 49 | 10000043 / AMR-099-0043 | Infinite-cluster intersections with vertical fibers | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 50 | 10000046 / AMR-099-0046 | Nonintersecting couplings of random walks in dimensions three and four | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 51 | 20001424 / AIM-DYNAMICAL_SYSTEMS-0082 | PCF descent and an odd postcritical-divisor criterion | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 52 | 2233 / EP-653 | Erdős Problem #653 | 0.2560 | 1 | unknown | queued | 0/5 |  |  |  |
| 53 | 2744 / KP-1.85 | Kirby Problem 1.85 | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 54 | 2765 / KP-2.17 | Kirby Problem 2.17 | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 55 | 2814 / KP-3.16 | Kirby Problem 3.16 | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 56 | 2849 / KP-3.51 | Kirby Problem 3.51 | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 57 | 2912 / KP-4.36 | Kirby Problem 4.36 | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 58 | 2961 / KP-4.85 | Kirby Problem 4.85 | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 59 | 3009 / KP-5.2 | Kirby Problem 5.2 | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 60 | 9500008 / AMR-094-0008 | Concatenated bounded Brownian pieces | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 61 | 9700035 / AMR-096-0035 | Expected length of a SIRSN spanning subnetwork | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 62 | 9900007 / AMR-098-0007 | Two-process coupling characterization of weak convergence | 0.2560 | 3 | unknown | queued | 0/5 |  |  |  |
| 63 | 30004386 / OWR-17469-011 | Large Deviations for Random High-Dimensional Projections | 0.2552 | 3 | 2020 | queued | 0/5 |  |  |  |
| 64 | 30004438 / OWR-17475-003 | Real Rational Maps with Exclusively Real Periodic Points | 0.2552 | 3 | 2020 | queued | 0/5 |  |  |  |
| 65 | 10600042 / AMR-105-0042 | Virtual-knot problem 42 — One can consider braids with even numbers of strands. | 0.2475 | 3 | unknown | queued | 0/5 |  |  |  |
| 66 | 30000166 / OWR-782-007 | Positivity of Saito's Eta Products | 0.2465 | 3 | 2005 | queued | 0/5 |  |  |  |
| 67 | 30000644 / OWR-1452-008 | Surjectivity of Reduction Maps for Special Polynomial Automorphisms | 0.2458 | 3 | 2007 | queued | 0/5 |  |  |  |
| 68 | 30000671 / OWR-1453-004 | Reconstructing Complete Local Rings from Finite Quotients | 0.2458 | 3 | 2007 | queued | 0/5 |  |  |  |
| 69 | 30000703 / OWR-1460-009 | Boundary Behavior under Asymptotic Schwarz–Pick Equality | 0.2458 | 3 | 2007 | queued | 0/5 |  |  |  |
| 70 | 30006309 / OWR-14299288-015 | Combinatorial Proof of Hurwitz and Discriminant Weight-Polytope Equality | 0.2454 | 3 | 2025 | queued | 0/5 |  |  |  |
| 71 | 30002061 / OWR-11786-016 | Collapse Preservation under Subdivision | 0.2437 | 3 | 2012 | queued | 0/5 |  |  |  |
| 72 | 30002298 / OWR-12339-004 | Polyhedra with Vertex-Factored Fantappiè Denominators | 0.2432 | 3 | 2013 | queued | 0/5 |  |  |  |
| 73 | 30003354 / OWR-15208-008 | Borderline Continuity of Conformal Metric Parametrizations | 0.2408 | 3 | 2017 | queued | 0/5 |  |  |  |
| 74 | 10300016 / AMR-102-0016 | Branched surfaces and triangulations — Question 7.1 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 75 | 10300025 / AMR-102-0025 | Leaf spaces and transverse structures — Question 8.2 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 76 | 10300054 / AMR-102-0054 | Numerical invariants — Question 13.1 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 77 | 10400033 / AMR-103-0033 | Conjecture 2.11 — (S. | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 78 | 2305051 / AMR-022-5051 | Research Problems in Function Theory — Problem 5.51 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 79 | 2715 / KP-1.56 | Kirby Problem 1.56 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 80 | 2722 / KP-1.63 | Kirby Problem 1.63 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 81 | 2725 / KP-1.66 | Kirby Problem 1.66 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 82 | 2772 / KP-2.24 | Kirby Problem 2.24 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 83 | 2853 / KP-3.55 | Kirby Problem 3.55 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 84 | 2861 / KP-3.63 | Kirby Problem 3.63 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 85 | 2869 / KP-3.71 | Kirby Problem 3.71 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 86 | 2919 / KP-4.43 | Kirby Problem 4.43 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 87 | 2935 / KP-4.59 | Kirby Problem 4.59 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 88 | 2985 / KP-4.109 | Kirby Problem 4.109 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 89 | 3012 / KP-5.5 | Kirby Problem 5.5 | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 90 | 3088 / OPG-56328 | Partitioning the Projective Plane | 0.2400 | 1 | unknown | queued | 0/5 |  |  |  |
| 91 | 3415 / OPG-37151 | Fundamental group torsion for subsets of Euclidean 3-space | 0.2400 | 1 | unknown | queued | 0/5 |  |  |  |
| 92 | 9700008 / AMR-096-0008 | Relaxation time of Metropolis chains on Cayley graphs | 0.2400 | 3 | unknown | queued | 0/5 |  |  |  |
| 93 | 30004845 / OWR-8415349-001 | Bubble-Free Criterion for Polygraphic and Nerve Homology | 0.2370 | 3 | 2021 | queued | 0/5 |  |  |  |
| 94 | 30000136 / OWR-761-003 | Nowhere-Zero Perturbations of Nonclosed One-Forms | 0.2292 | 3 | 2004 | queued | 0/5 |  |  |  |
| 95 | 30006461 / OWR-14299577-011 | Nonconstancy of the Multiplication-Table Limit Profile | 0.2290 | 3 | 2025 | queued | 0/5 |  |  |  |
| 96 | 30000177 / OWR-785-003 | LOCC Dense-Codeability of the Four-Qubit W State | 0.2289 | 3 | 2005 | queued | 0/5 |  |  |  |
| 97 | 30000252 / OWR-1050-001 | Critical-Exponent Polyharmonic Dirichlet Problems | 0.2289 | 3 | 2005 | queued | 0/5 |  |  |  |
| 98 | 30000991 / OWR-2040-003 | Realization of Persistence Pairings by Filtration Functions | 0.2279 | 3 | 2008 | queued | 0/5 |  |  |  |
| 99 | 30001203 / OWR-3394-020 | Global Observability from Negative Gramian Curvature | 0.2275 | 3 | 2009 | queued | 0/5 |  |  |  |
| 100 | 30001377 / OWR-4135-008 | Sensitivity Growth Under Boolean Conjunctions | 0.2275 | 3 | 2009 | queued | 0/5 |  |  |  |
| 101 | 30001804 / OWR-5158-001 | Mapping-Class-Group Presentations of Surface Steinberg Modules | 0.2267 | 3 | 2011 | queued | 0/5 |  |  |  |
| 102 | 30002203 / OWR-12172-006 | Lifting Pentagon-Arrangement Symmetries to Homotopy Invariants | 0.2263 | 3 | 2012 | queued | 0/5 |  |  |  |
| 103 | 30002278 / OWR-12331-002 | Lyapunov Functions for Three-Dimensional Acoustic PML Systems | 0.2258 | 3 | 2013 | queued | 0/5 |  |  |  |
| 104 | 30002300 / OWR-12339-006 | Weakening General Position in Signed Simplex Representations | 0.2258 | 3 | 2013 | queued | 0/5 |  |  |  |
| 105 | 10400094 / AMR-103-0094 | Problem 4.16 — (J. | 0.2250 | 3 | unknown | queued | 0/5 |  |  |  |
| 106 | 10400099 / AMR-103-0099 | Conjecture 5.3 — Let hX be as above. | 0.2250 | 3 | unknown | queued | 0/5 |  |  |  |
| 107 | 2800904 / AMR-027-0904 | 10 Lectures and 42 Open Problems — Stability conditions for tightness of k-median LP and k-means SDP | 0.2248 | 3 | 2015 | queued | 0/5 |  |  |  |
| 108 | 30002806 / OWR-13497-003 | Commutation of Variational Discretization and Optimal Control | 0.2248 | 3 | 2015 | queued | 0/5 |  |  |  |
| 109 | 30003052 / OWR-14215-004 | Spectra of Koopman Operators for Linear Maps | 0.2242 | 3 | 2016 | queued | 0/5 |  |  |  |
| 110 | 30003150 / OWR-14609-007 | Unique Nonequilibrium Invariant Measures for Resonant NLS | 0.2242 | 3 | 2016 | queued | 0/5 |  |  |  |
| 111 | 10300055 / AMR-102-0055 | Numerical invariants — Question 13.2 | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 112 | 10400015 / AMR-103-0015 | Problem 1.15 — (M. | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 113 | 10400016 / AMR-103-0016 | Problem 1.16 — (E. | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 114 | 10400120 / AMR-103-0120 | Conjecture 7.5 — For non-vanishing $\tau_r^G(M)$, the absolute value $/\tau_r^G(M)/$ depends only on the fundamental group $\pi_1(M)$. | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 115 | 10600020 / AMR-105-0020 | Virtual-knot problem 20 — Embeddings of Surfaces | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 116 | 20001380 / AIM-DYNAMICAL_SYSTEMS-0038 | Explicit size and wild ramification bounds for the 0-rooted tree of z^2+1 over Q_2 | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 117 | 2701 / KP-1.42 | Kirby Problem 1.42 | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 118 | 2728 / KP-1.69 | Kirby Problem 1.69 | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 119 | 2859 / KP-3.61 | Kirby Problem 3.61 | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 120 | 3092 / OPG-59984 | Chromatic number of associahedron | 0.2240 | 1 | unknown | queued | 0/5 |  |  |  |
| 121 | 600008 / AMR-005-0008 | Baker's Dozen — Chains of null geodesics | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 122 | 9700041 / AMR-096-0041 | Topological realization of compact Markov-chain limits | 0.2240 | 3 | unknown | queued | 0/5 |  |  |  |
| 123 | 30003709 / OWR-15987-020 | Recovering Toric Arrangement Posets from Complement Cohomology | 0.2229 | 3 | 2018 | queued | 0/5 |  |  |  |
| 124 | 30003996 / OWR-16633-013 | Hardness of Root-Dependent Spanning-Tree Optimization | 0.2229 | 3 | 2018 | queued | 0/5 |  |  |  |
| 125 | 30003997 / OWR-16633-014 | Hardness of Path-Cost Arborescence Optimization | 0.2229 | 3 | 2018 | queued | 0/5 |  |  |  |
| 126 | 5100032 / AMR-050-0032 | Elliptic-billiard invariant k_{603} | 0.2222 | 3 | 2021 | queued | 0/5 |  |  |  |
| 127 | 30004433 / OWR-17474-007 | Ends of Critical Long-Range Percolation Clusters | 0.2212 | 3 | 2020 | queued | 0/5 |  |  |  |
| 128 | 4900006 / AMR-048-0006 | Eden's conjecture on local Lyapunov dimension | 0.2200 | 3 | unknown | queued | 0/5 |  |  |  |
| 129 | 30005678 / OWR-14297744-011 | Fully Two-Segal Waldhausen S-Constructions | 0.2174 | 3 | 2023 | queued | 0/5 |  |  |  |
| 130 | 5300050 / AMR-052-0050 | Boundary entropy of an attracting basin | 0.2142 | 3 | 1992 | queued | 0/5 |  |  |  |
| 131 | 5900003 / AMR-058-0003 | Stability of Spherical Plateau Clusters | 0.2136 | 3 | 1995 | queued | 0/5 |  |  |  |
| 132 | 30005451 / OWR-12697708-004 | Local Limits of Preferential Attachment with Deterministic or Random Outdegree | 0.2116 | 3 | 2023 | queued | 0/5 |  |  |  |
| 133 | 6200049 / AMR-061-0049 | Boundaries of Groups and Kleinian Groups — Problem 49 | 0.2113 | 3 | 2005 | queued | 0/5 |  |  |  |
| 134 | 30000304 / OWR-1061-006 | Exceptional Regenerative Composition Structures | 0.2113 | 3 | 2005 | queued | 0/5 |  |  |  |
| 135 | 30002719 / OWR-13352-003 | Probabilistic Interpretation of Waring-Polynomial Series | 0.2113 | 3 | 2014 | queued | 0/5 |  |  |  |
| 136 | 30000697 / OWR-1458-003 | Injectivity Criteria for Upsilon Transforms | 0.2107 | 3 | 2007 | queued | 0/5 |  |  |  |
| 137 | 30001234 / OWR-3471-008 | Uniqueness in Linear Programs for Binomial Multiplier Ideals | 0.2100 | 3 | 2009 | queued | 0/5 |  |  |  |
| 138 | 30001410 / OWR-4199-003 | Crofton Measures in Hilbert Geometry | 0.2097 | 3 | 2010 | queued | 0/5 |  |  |  |
| 139 | 30001883 / OWR-11136-008 | Circle Free Convex Bodies Under Minkowski Addition | 0.2093 | 3 | 2011 | queued | 0/5 |  |  |  |
| 140 | 10400041 / AMR-103-0041 | Problem 2.19 — (Y. | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 141 | 10400117 / AMR-103-0117 | Problem 7.2 — (S.K. | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 142 | 10400229 / AMR-103-0229 | Problem 12.24 — (A. | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 143 | 10400231 / AMR-103-0231 | Conjecture 12.26 — (V. | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 144 | 10600021 / AMR-105-0021 | Virtual-knot problem 21 — Non-Commutativity and Long Knots | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 145 | 11000132 / AMR-109-0132 | Problem 2 — Given a tuple ×N i=1(mi,ti) ∈ ZN, give a tractable expression in terms of Dehn- Thurston or other coordinates for the… | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 146 | 11000147 / AMR-109-0147 | Question — Does there exist a set of at least three pseudo-Anosov homeomorpisms such that every pair satisfies a braid relation. | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 147 | 2000008 / AMR-019-0008 | Some Open Problems in Elasticity — Uniqueness of equilibrium | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 148 | 20001312 / AIM-CONVEX_GEOMETRY-0044 | Polynomial ridge completeness and switching obstructions for the four AIM directions | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 149 | 20001964 / AIM-GEOMETRY-0302 | Noncompact equivariant integration and the boundary at infinity | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 150 | 2306064 / AMR-022-6064 | Research Problems in Function Theory — Problem 6.64 | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 151 | 2770 / KP-2.22 | Kirby Problem 2.22 | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 152 | 2830 / KP-3.32 | Kirby Problem 3.32 | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 153 | 2840 / KP-3.42 | Kirby Problem 3.42 | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 154 | 3800014 / AMR-037-0014 | A dynamic-programming interval problem | 0.2080 | 3 | unknown | queued | 0/5 |  |  |  |
| 155 | 30002926 / OWR-13856-002 | Gamma Profiles of Waves Entering a Condensate | 0.2075 | 3 | 2015 | queued | 0/5 |  |  |  |
| 156 | 30005975 / OWR-14298584-008 | Brauer Groups of Tame Stacky Curves | 0.2071 | 3 | 2024 | queued | 0/5 |  |  |  |
| 157 | 5100023 / AMR-050-0023 | Elliptic-billiard invariant k_{405} | 0.2064 | 3 | 2021 | queued | 0/5 |  |  |  |
| 158 | 30003741 / OWR-15993-009 | Higher Multistationarity in T-Cell Activation Models | 0.2057 | 3 | 2018 | queued | 0/5 |  |  |  |
| 159 | 30003818 / OWR-16164-012 | Brownian First-Visit Cell Lengths on the Circle | 0.2057 | 3 | 2018 | queued | 0/5 |  |  |  |
| 160 | 4700016 / AMR-046-0016 | Reversible equivariant planar differential systems | 0.2041 | 3 | 2020 | queued | 0/5 |  |  |  |
| 161 | 30004539 / OWR-2654828-004 | Convergence Radii of Autoregressive and Moving Average Persistence Series | 0.2041 | 3 | 2020 | queued | 0/5 |  |  |  |
| 162 | 5000006 / AMR-049-0006 | Length ratios of parallel short trajectories | 0.2041 | 3 | 2020 | queued | 0/5 |  |  |  |
| 163 | 20000236 / AIM-ALGEBRAIC_GEOMETRY-0236 | Low-degree smoothness and a Wronskian kernel criterion for osculating Schubert curves | 0.2040 | 3 | unknown | queued | 0/5 |  |  |  |
| 164 | 2597 / KOU-21.88 | Kourovka Notebook Problem 21.88 | 0.2040 | 2 | 2026 | queued | 0/5 |  |  |  |
| 165 | 30004669 / OWR-7155442-002 | Depth Relative to K-Trivial Oracles | 0.2032 | 3 | 2021 | queued | 0/5 |  |  |  |
| 166 | 5100001 / AMR-050-0001 | Elliptic-billiard invariant k_{107} | 0.2032 | 3 | 2021 | queued | 0/5 |  |  |  |
| 167 | 5100002 / AMR-050-0002 | Elliptic-billiard invariant k_{108} | 0.2032 | 3 | 2021 | queued | 0/5 |  |  |  |
| 168 | 5100006 / AMR-050-0006 | Elliptic-billiard invariant k_{114} | 0.2032 | 3 | 2021 | queued | 0/5 |  |  |  |
| 169 | 5100010 / AMR-050-0010 | Elliptic-billiard invariant k_{120} | 0.2032 | 3 | 2021 | queued | 0/5 |  |  |  |
| 170 | 30005408 / OWR-12697689-004 | Gröbner-Cell Parametrization of Punctual Hilbert Schemes | 0.2007 | 3 | 2023 | queued | 0/5 |  |  |  |
| 171 | 30005432 / OWR-12697693-003 | The Property-s Elements of a Skew Brace | 0.2007 | 3 | 2023 | queued | 0/5 |  |  |  |
| 172 | 2306022 / AMR-022-6022 | Research Problems in Function Theory — Problem 6.22 | 0.2000 | 3 | unknown | queued | 0/5 |  |  |  |
| 173 | 30000229 / OWR-829-001 | Approximation Classes for Adaptive Finite Elements | 0.1981 | 3 | 2005 | queued | 0/5 |  |  |  |
| 174 | 30000264 / OWR-1050-015 | Topology of Yamabe Asymptotic Sets | 0.1981 | 3 | 2005 | queued | 0/5 |  |  |  |
| 175 | 30000585 / OWR-1327-001 | Force-Induced Phase Transitions in Self-Attracting Polymers | 0.1978 | 3 | 2006 | queued | 0/5 |  |  |  |
| 176 | 30001413 / OWR-4209-002 | Optimal Domain Conditions for Positivity of Hinged Plates | 0.1966 | 3 | 2010 | queued | 0/5 |  |  |  |
| 177 | 30006161 / OWR-14299082-003 | Generic Maximal Chains on Exceptional Surfaces | 0.1963 | 3 | 2025 | queued | 0/5 |  |  |  |
| 178 | 30006170 / OWR-14299082-017 | Chaining and Weak Mixing for Measure-Class-Preserving Actions | 0.1963 | 3 | 2025 | queued | 0/5 |  |  |  |
| 179 | 30006231 / OWR-14299094-001 | Unique Ground-State Representability under Linear Constraints | 0.1963 | 3 | 2025 | queued | 0/5 |  |  |  |
| 180 | 30006354 / OWR-14299511-003 | SU(3) Braided Fusion Spin Systems and Haah Nets | 0.1963 | 3 | 2025 | queued | 0/5 |  |  |  |
| 181 | 30001767 / OWR-5149-003 | Blocks of Symmetric-Group Centralizer Algebras | 0.1962 | 3 | 2011 | queued | 0/5 |  |  |  |
| 182 | 30002603 / OWR-12986-001 | Linear Segments in Optimal-Path Shape Functions | 0.1950 | 3 | 2014 | queued | 0/5 |  |  |  |
| 183 | 30002720 / OWR-13352-004 | Marginal Limits for Markov-Source Selection Processes | 0.1950 | 3 | 2014 | queued | 0/5 |  |  |  |
| 184 | 30002879 / OWR-13681-013 | Hochschild-Cohomology Lie Structure of a Stratified Algebra | 0.1945 | 3 | 2015 | queued | 0/5 |  |  |  |
| 185 | 30003069 / OWR-14221-005 | Plabic Newton–Okounkov Bodies and FFLV Polytopes | 0.1940 | 3 | 2016 | queued | 0/5 |  |  |  |
| 186 | 4800017 / AMR-047-0017 | Multiple ergodic averages — Problem 17 | 0.1940 | 3 | 2016 | queued | 0/5 |  |  |  |
| 187 | 30003390 / OWR-15214-002 | Exact Strong Approximation Rates for CIR Processes | 0.1935 | 3 | 2017 | queued | 0/5 |  |  |  |
| 188 | 30003480 / OWR-15428-003 | Single Polynomial Description of Binary Tensor Gram Loci | 0.1935 | 3 | 2017 | queued | 0/5 |  |  |  |
| 189 | 30003677 / OWR-15962-003 | Strategic Starting Vertices in Competing First-Passage Percolation | 0.1935 | 3 | 2017 | queued | 0/5 |  |  |  |
| 190 | 30000567 / OWR-1323-003 | Disjoint-Hypercyclic Operators on Banach Spaces | 0.1934 | 3 | 2006 | queued | 0/5 |  |  |  |
| 191 | 4300006 / AMR-042-0006 | Entropy and Deligne periods | 0.1934 | 4 | 2006 | queued | 0/5 |  |  |  |
| 192 | 30003935 / OWR-16413-006 | Strong Convergence of Ensemble Kalman Inversion | 0.1929 | 3 | 2018 | queued | 0/5 |  |  |  |
| 193 | 30001251 / OWR-3474-001 | Instability of Multi-Peaked Orientational Steady States | 0.1925 | 3 | 2009 | queued | 0/5 |  |  |  |
| 194 | 30001400 / OWR-4139-001 | Comparison of Majorization Relations for Probability Vectors | 0.1925 | 3 | 2009 | queued | 0/5 |  |  |  |
| 195 | 10300044 / AMR-102-0044 | Hyperbolic geometry — Question 10.6 | 0.1920 | 3 | unknown | queued | 0/5 |  |  |  |
| 196 | 10400049 / AMR-103-0049 | Problem 2.27 — (D. | 0.1920 | 3 | unknown | queued | 0/5 |  |  |  |
| 197 | 10400080 / AMR-103-0080 | Problem 4.2 — (J. | 0.1920 | 3 | unknown | queued | 0/5 |  |  |  |
| 198 | 10800007 / AMR-107-0007 | Problem 2A — What is the minimal number of open sets $U_{i}$ covering ${\mathbb{R}}^{6}$ such that for any $U_{i}$… | 0.1920 | 3 | unknown | queued | 0/5 |  |  |  |
| 199 | 11000213 / AMR-109-0213 | Problem 6 — (Purely cyclic). | 0.1920 | 3 | unknown | queued | 0/5 |  |  |  |
| 200 | 20002560 / AIM-PROBABILITY-0002 | Exact parity projection and a certified bracket for RBM(3,1) | 0.1920 | 3 | unknown | queued | 0/5 |  |  |  |
| 201 | 30006576 / OWR-14299907-001 | Mesh Structures Behind Even-Odd Superconvergence | 0.1920 | 3 | 2026 | queued | 0/5 |  |  |  |
| 202 | 30006587 / OWR-14299909-002 | Derivative Formula for Multiple Eisenstein Series | 0.1920 | 3 | 2026 | queued | 0/5 |  |  |  |
| 203 | 30001704 / OWR-4798-031 | Finiteness from Face-Number Bounds for Manifolds with Boundary | 0.1919 | 3 | 2011 | queued | 0/5 |  |  |  |
| 204 | 30001779 / OWR-5152-002 | Covariance Estimation Without Logarithmic Oversampling | 0.1919 | 3 | 2011 | queued | 0/5 |  |  |  |
| 205 | 30002105 / OWR-11793-003 | Density and Geometry Recovery from Nearest-Neighbor Graphs | 0.1915 | 3 | 2012 | queued | 0/5 |  |  |  |
| 206 | 30004526 / OWR-2654827-002 | Strong Lefschetz Property of the Zeroth Jordan Component | 0.1914 | 3 | 2020 | queued | 0/5 |  |  |  |
| 207 | 30004563 / OWR-2654831-006 | Maximum Central Points in Cube-Move $\alpha$-Immersions | 0.1914 | 3 | 2020 | queued | 0/5 |  |  |  |
| 208 | 5000005 / AMR-049-0005 | Types of parallel short trajectories | 0.1914 | 3 | 2020 | queued | 0/5 |  |  |  |
| 209 | 5000007 / AMR-049-0007 | Short geodesics on the regular dodecahedron | 0.1914 | 3 | 2020 | queued | 0/5 |  |  |  |
| 210 | 30002597 / OWR-12984-009 | Bounding Immersed Curves by Stable Singular Disk Maps | 0.1907 | 3 | 2014 | queued | 0/5 |  |  |  |
| 211 | 30004601 / OWR-4990374-004 | Degree Bounds for Generic Initial Ideals of Arrangements | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 212 | 30004676 / OWR-7155442-010 | Admissible Sets and Their Jump Structures | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 213 | 30004690 / OWR-7155446-005 | Nonsmooth Homogeneous Complex Monge–Ampère Solutions | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 214 | 30004757 / OWR-8415338-004 | Dirac-Mass Tangent Cones in Monge–Ampère Equations | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 215 | 5100004 / AMR-050-0004 | Elliptic-billiard invariant k_{110} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 216 | 5100005 / AMR-050-0005 | Elliptic-billiard invariant k_{111} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 217 | 5100007 / AMR-050-0007 | Elliptic-billiard invariant k_{115} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 218 | 5100008 / AMR-050-0008 | Elliptic-billiard invariant k_{117} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 219 | 5100011 / AMR-050-0011 | Elliptic-billiard invariant k_{203,a} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 220 | 5100012 / AMR-050-0012 | Elliptic-billiard invariant k_{203,b} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 221 | 5100014 / AMR-050-0014 | Elliptic-billiard invariant k_{303,a} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 222 | 5100015 / AMR-050-0015 | Elliptic-billiard invariant k_{303,b} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 223 | 5100030 / AMR-050-0030 | Elliptic-billiard invariant k_{601} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 224 | 5100033 / AMR-050-0033 | Elliptic-billiard invariant k_{605,a} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 225 | 5100044 / AMR-050-0044 | Elliptic-billiard invariant k_{804,a} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 226 | 5100062 / AMR-050-0062 | Elliptic-billiard invariant k_{903,a} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 227 | 5100063 / AMR-050-0063 | Elliptic-billiard invariant k_{904,a} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 228 | 5100009 / AMR-050-0009 | Elliptic-billiard invariant k_{118} | 0.1905 | 3 | 2021 | queued | 0/5 |  |  |  |
| 229 | 30003301 / OWR-15177-019 | Lifting Dehn-Twist Relations to Punctured Surfaces | 0.1897 | 3 | 2016 | queued | 0/5 |  |  |  |
| 230 | 30005244 / OWR-11101924-008 | Spectral Approximation of Discrete-Dipole Operators | 0.1894 | 3 | 2022 | queued | 0/5 |  |  |  |
| 231 | 30005299 / OWR-11695864-004 | Determinantal Quartics as Weddle Surfaces | 0.1894 | 3 | 2022 | queued | 0/5 |  |  |  |
| 232 | 30005310 / OWR-11695865-009 | Exhaustiveness of Threshold Scenarios for Colored Gaussian Graphical Models | 0.1894 | 3 | 2022 | queued | 0/5 |  |  |  |
| 233 | 30003518 / OWR-15436-004 | Multistationarity in Kinetic-Proofreading Networks | 0.1892 | 3 | 2017 | queued | 0/5 |  |  |  |
| 234 | 30003999 / OWR-16633-016 | Polynomial-Time Comparison of Sparse Algebraic Power Sums | 0.1886 | 3 | 2018 | queued | 0/5 |  |  |  |
| 235 | 30005449 / OWR-12697708-002 | Deterministic Limits of Trace-Reinforced Ant Walks | 0.1881 | 3 | 2023 | queued | 0/5 |  |  |  |
| 236 | 30005454 / OWR-12697708-007 | Critical Reinforcement Convergence on the Infinite Line | 0.1881 | 3 | 2023 | queued | 0/5 |  |  |  |
| 237 | 30005457 / OWR-12697708-010 | Reinforcement Counterexamples on Integer Lattices | 0.1881 | 3 | 2023 | queued | 0/5 |  |  |  |
| 238 | 30005731 / OWR-14298011-002 | Automatic Convexity of Optimal Spiral Strategies | 0.1881 | 3 | 2023 | queued | 0/5 |  |  |  |
| 239 | 7000013 / AMR-069-0013 | Geometry of Curves and Surfaces — Problem 2.4 | 0.1879 | 3 | 2019 | queued | 0/5 |  |  |  |
| 240 | 30006020 / OWR-14298589-005 | Intermediate-Area Cylinders on Large-Genus Square-Tiled Surfaces | 0.1864 | 3 | 2024 | queued | 0/5 |  |  |  |
| 241 | 30004786 / OWR-8415342-014 | Automorphic L-Functions from Sigma–Rho Poisson Summation | 0.1862 | 3 | 2021 | queued | 0/5 |  |  |  |
| 242 | 5100024 / AMR-050-0024 | Elliptic-billiard invariant k_{406,a} | 0.1852 | 3 | 2021 | queued | 0/5 |  |  |  |
| 243 | 5100035 / AMR-050-0035 | Elliptic-billiard invariant k_{607} | 0.1852 | 3 | 2021 | queued | 0/5 |  |  |  |
| 244 | 5100036 / AMR-050-0036 | Elliptic-billiard invariant k_{608} | 0.1852 | 3 | 2021 | queued | 0/5 |  |  |  |
| 245 | 5100037 / AMR-050-0037 | Elliptic-billiard invariant k_{609} | 0.1852 | 3 | 2021 | queued | 0/5 |  |  |  |
| 246 | 5100038 / AMR-050-0038 | Elliptic-billiard invariant k_{610} | 0.1852 | 3 | 2021 | queued | 0/5 |  |  |  |
| 247 | 5100064 / AMR-050-0064 | Elliptic-billiard invariant k_{905} | 0.1852 | 3 | 2021 | queued | 0/5 |  |  |  |
| 248 | 5100065 / AMR-050-0065 | Elliptic-billiard invariant k_{906} | 0.1852 | 3 | 2021 | queued | 0/5 |  |  |  |
| 249 | 30000661 / OWR-1452-025 | Generalized Tameness of an Explicit Polynomial Automorphism | 0.1844 | 3 | 2007 | queued | 0/5 |  |  |  |
| 250 | 30000708 / OWR-1461-003 | Cramér–Wold Uniqueness for Infinite Signed Measures | 0.1844 | 3 | 2007 | queued | 0/5 |  |  |  |
| 251 | 30006395 / OWR-14299518-013 | Detection-Threshold Transition for Planted Random Trees | 0.1841 | 3 | 2025 | queued | 0/5 |  |  |  |
| 252 | 30006492 / OWR-14299580-009 | Cocycle-Weighted Representations of Welded Braid Groups | 0.1841 | 3 | 2025 | queued | 0/5 |  |  |  |
| 253 | 30001321 / OWR-4081-005 | RWRE Concentration at Transverse Dimension One | 0.1838 | 3 | 2009 | queued | 0/5 |  |  |  |
| 254 | 30001626 / OWR-4533-004 | Centralizer Realization of Cartan Subalgebras in $L^*$-Algebras | 0.1835 | 3 | 2010 | queued | 0/5 |  |  |  |
| 255 | 30002291 / OWR-12337-002 | Variation Limits for Pure-Jump Semimartingales | 0.1824 | 3 | 2013 | queued | 0/5 |  |  |  |
| 256 | 30003084 / OWR-14222-012 | Wiseman–Wilson Theorem for Complex Conics | 0.1811 | 3 | 2016 | queued | 0/5 |  |  |  |
| 257 | 30003216 / OWR-14750-001 | Convergence of Adaptive Hybrid Finite Element Methods | 0.1811 | 3 | 2016 | queued | 0/5 |  |  |  |
| 258 | 30003403 / OWR-15216-007 | Strong Surjectivity of Countryman Derived Orders Under PFA | 0.1806 | 3 | 2017 | queued | 0/5 |  |  |  |
| 259 | 30003427 / OWR-15218-003 | Multiple-Maturity Consistency Under Bid–Ask Spreads | 0.1806 | 3 | 2017 | queued | 0/5 |  |  |  |
| 260 | 10300019 / AMR-102-0019 | Branched surfaces and triangulations — Question 7.4 | 0.1800 | 3 | unknown | queued | 0/5 |  |  |  |
| 261 | 10300057 / AMR-102-0057 | Numerical invariants — Question 13.4 | 0.1800 | 3 | unknown | queued | 0/5 |  |  |  |
| 262 | 10400105 / AMR-103-0105 | Problem 5.9 — Let the notation be as above. | 0.1800 | 3 | unknown | queued | 0/5 |  |  |  |
| 263 | 2665 / KP-1.6 | Kirby Problem 1.6 | 0.1800 | 3 | unknown | queued | 0/5 |  |  |  |
| 264 | 2676 / KP-1.17 | Kirby Problem 1.17 | 0.1800 | 3 | unknown | queued | 0/5 |  |  |  |
| 265 | 3413 / OPG-37131 | Realisation problem for the space of knots in the 3-sphere | 0.1800 | 1 | unknown | queued | 0/5 |  |  |  |
| 266 | 3900010 / AMR-038-0010 | Odd rep-tiling by a 14-omino | 0.1800 | 4 | unknown | queued | 0/5 |  |  |  |
| 267 | 9700040 / AMR-096-0040 | Stationary law of a drift-jump particle process | 0.1800 | 3 | unknown | queued | 0/5 |  |  |  |
| 268 | 30004313 / OWR-17294-014 | Yang–Baxter Solutions from Generalized Left Semi-Braces | 0.1794 | 3 | 2019 | queued | 0/5 |  |  |  |
| 269 | 30004630 / OWR-4990378-001 | Quadratic Growth without Quadratic Control Regularization | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 270 | 5100013 / AMR-050-0013 | Elliptic-billiard invariant k_{204} | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 271 | 5100016 / AMR-050-0016 | Elliptic-billiard invariant k_{304} | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 272 | 5100017 / AMR-050-0017 | Elliptic-billiard invariant k_{307} | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 273 | 5100020 / AMR-050-0020 | Elliptic-billiard invariant k_{403,a} | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 274 | 5100021 / AMR-050-0021 | Elliptic-billiard invariant k_{403,b} | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 275 | 5100022 / AMR-050-0022 | Elliptic-billiard invariant k_{404} | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 276 | 5100026 / AMR-050-0026 | Elliptic-billiard invariant k_{407} | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 277 | 5100046 / AMR-050-0046 | Elliptic-billiard invariant k_{805} | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 278 | 5100047 / AMR-050-0047 | Elliptic-billiard invariant k_{806,a} | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 279 | 5100060 / AMR-050-0060 | Elliptic-billiard invariant k_{817} | 0.1778 | 3 | 2021 | queued | 0/5 |  |  |  |
| 280 | 30005042 / OWR-9790363-001 | Weak Moment Conditions and Branching-Process Limit Laws | 0.1768 | 3 | 2022 | queued | 0/5 |  |  |  |
| 281 | 30005044 / OWR-9790363-003 | Explosion with Infinite-Mean Offspring | 0.1768 | 3 | 2022 | queued | 0/5 |  |  |  |
| 282 | 30005223 / OWR-11101920-009 | Limiting Vanishing Probability for Symmetric Group Characters | 0.1768 | 3 | 2022 | queued | 0/5 |  |  |  |
| 283 | 30000170 / OWR-783-002 | Prox-Regularity of Polynomial Stability Abscissas | 0.1761 | 3 | 2005 | queued | 0/5 |  |  |  |
| 284 | 10400036 / AMR-103-0036 | Problem 2.14 — (M. | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 285 | 10400139 / AMR-103-0139 | Problem 7.24 — (S. | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 286 | 10400196 / AMR-103-0196 | Question 10.21 — (F. | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 287 | 10400216 / AMR-103-0216 | Problem 12.11 — (D. | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 288 | 10400219 / AMR-103-0219 | Problem 12.14 — (N. | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 289 | 10400220 / AMR-103-0220 | Problem 12.15 — (M. | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 290 | 10400228 / AMR-103-0228 | Problem 12.23 — (A. | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 291 | 11000192 / AMR-109-0192 | Problem 2.5 — Construct an example of a pseudo-Anosov mapping class for a closed surface which is not ergodic on the SU(2)-characte… | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 292 | 11000296 / AMR-109-0296 | Question 5.4 — Is the image of the second Morita class in H8(GL(6, Z); Q)) non-trivial? | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 293 | 20001414 / AIM-DYNAMICAL_SYSTEMS-0072 | A Wasserstein rate dictionary for local-update generators | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 294 | 20001798 / AIM-GEOMETRY-0136 | Airy topological recursion, exact WKB, and the wild Hodge gap | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 295 | 20003006 / AIM-TOPOLOGY-0094 | Clique and cubical-nerve realizations of digital homotopy groups | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 296 | 2884 / KP-4.8 | Kirby Problem 4.8 | 0.1760 | 3 | unknown | queued | 0/5 |  |  |  |
| 297 | 30005460 / OWR-12697710-006 | Convexity of Odd-Power Sum-of-Squares Cones | 0.1756 | 3 | 2023 | queued | 0/5 |  |  |  |
| 298 | 30005468 / OWR-12697710-015 | Rational Certificates for Truncated Moment Nonrepresentability | 0.1756 | 3 | 2023 | queued | 0/5 |  |  |  |
| 299 | 30005584 / OWR-14297732-013 | Degrees of Asymptotically Conical Expanders Under Connected Sum | 0.1756 | 3 | 2023 | queued | 0/5 |  |  |  |
| 300 | 30002709 / OWR-13351-007 | Essential Finite Generation of Valuation Rings | 0.1733 | 3 | 2014 | queued | 0/5 |  |  |  |
| 301 | 30002960 / OWR-13940-008 | Three-Dimensional Coloring Number of the Sphere | 0.1729 | 3 | 2015 | queued | 0/5 |  |  |  |
| 302 | 6700069 / AMR-066-0069 | Scalar Curvature Question [?73]: [c] LetS be a Riemannian manifold homeomorphic to the connected sum of twenty copies ofS2× S2 | 0.1720 | 3 | 2017 | queued | 0/5 |  |  |  |
| 303 | 30000156 / OWR-768-006 | Limiting Cycle Distributions of Birational Maps | 0.1719 | 3 | 2004 | queued | 0/5 |  |  |  |
| 304 | 30001781 / OWR-5152-008 | Maximal Submatrix Bounds Without Unconditionality | 0.1717 | 3 | 2011 | queued | 0/5 |  |  |  |
| 305 | 30000849 / OWR-1729-002 | Scaling Profiles in Addition–Coagulation Models | 0.1712 | 3 | 2007 | queued | 0/5 |  |  |  |
| 306 | 30001080 / OWR-2093-003 | Transport Characterizations of Mass-Stationarity | 0.1709 | 3 | 2008 | queued | 0/5 |  |  |  |
| 307 | 30001557 / OWR-4425-012 | Pattern Characterization of Fractional Powers in Words | 0.1704 | 3 | 2010 | queued | 0/5 |  |  |  |
| 308 | 30001565 / OWR-4426-001 | Irreducible Coherent-Configuration Representations Without Polynomial Splitting | 0.1704 | 3 | 2010 | queued | 0/5 |  |  |  |
| 309 | 30001608 / OWR-4530-006 | Stability Beyond Unstable Population-Process Fluid Limits | 0.1704 | 3 | 2010 | queued | 0/5 |  |  |  |
| 310 | 30004437 / OWR-17475-002 | The Real-Zero Polynomial Amalgamation Conjecture | 0.1701 | 3 | 2020 | queued | 0/5 |  |  |  |
| 311 | 30001994 / OWR-11578-001 | Variational Eddy Currents with Degenerate Conductivity | 0.1697 | 3 | 2012 | queued | 0/5 |  |  |  |
| 312 | 30002011 / OWR-11581-002 | Corruption-Parameter Choice in Empirical-Bayes Estimation | 0.1697 | 3 | 2012 | queued | 0/5 |  |  |  |
| 313 | 30002163 / OWR-12012-001 | Minimum Distance in Spherical Fibonacci Lattices | 0.1697 | 3 | 2012 | queued | 0/5 |  |  |  |
| 314 | 30002792 / OWR-13494-011 | Non-ACM Line Configurations with Minimal Symbolic Initial-Degree Gap | 0.1686 | 3 | 2015 | queued | 0/5 |  |  |  |
| 315 | 30000048 / OWR-722-001 | Positive Characters of Simply Connected Groups | 0.1686 | 3 | 2004 | queued | 0/5 |  |  |  |
| 316 | 2305038 / AMR-022-5038 | Research Problems in Function Theory — Problem 5.38 | 0.1680 | 3 | unknown | queued | 0/5 |  |  |  |
| 317 | 3100085 / AMR-030-0085 | Let f(p;n,k) = C(n,k) p^(k) (1-p)^(n-k) | 0.1680 | 3 | unknown | queued | 0/5 |  |  |  |
| 318 | 3242 / OPG-46575 | Melnikov's valency-variety problem | 0.1680 | 1 | unknown | queued | 0/5 |  |  |  |
| 319 | 3356 / OPG-37396 | 3 is a primitive root modulo primes of the form 16 q^4 + 1, where q>3 is prime | 0.1680 | 1 | unknown | queued | 0/5 |  |  |  |
| 320 | 9700031 / AMR-096-0031 | Local finiteness of SIRSN traffic intensity | 0.1680 | 3 | unknown | queued | 0/5 |  |  |  |
| 321 | 30003472 / OWR-15427-014 | Exponential Probability Gaps Between Random Order Types | 0.1677 | 3 | 2017 | queued | 0/5 |  |  |  |
| 322 | 30003508 / OWR-15432-001 | Convergence of Spectral Estimators for Diffusion Tensors | 0.1677 | 3 | 2017 | queued | 0/5 |  |  |  |
| 323 | 30004434 / OWR-17474-008 | Uniform Coupling under Gibbs Uniqueness | 0.1675 | 3 | 2020 | queued | 0/5 |  |  |  |
| 324 | 30004022 / OWR-16636-004 | Commutator Models for Nonsymmetric Free Random Variables | 0.1671 | 3 | 2018 | queued | 0/5 |  |  |  |
| 325 | 30004365 / OWR-17466-004 | Derived Invariants from Gentle Quivers with Relations | 0.1659 | 3 | 2020 | queued | 0/5 |  |  |  |
| 326 | 5100034 / AMR-050-0034 | Elliptic-billiard invariant k_{606} | 0.1651 | 3 | 2021 | queued | 0/5 |  |  |  |
| 327 | 5100061 / AMR-050-0061 | Elliptic-billiard invariant k_{818} | 0.1651 | 3 | 2021 | queued | 0/5 |  |  |  |
| 328 | 30003338 / OWR-15206-017 | Positive Association in Random Proper Colorings | 0.1645 | 3 | 2017 | queued | 0/5 |  |  |  |
| 329 | 30003659 / OWR-15958-006 | Completeness of Cut-Free Kozen Modal Calculus | 0.1645 | 3 | 2017 | queued | 0/5 |  |  |  |
| 330 | 30003661 / OWR-15958-008 | Pathwise Connected Choice in Dimension Two | 0.1645 | 3 | 2017 | queued | 0/5 |  |  |  |
| 331 | 30005016 / OWR-9790358-014 | Universal Four-Point Polynomial Interpolation Subspaces | 0.1642 | 3 | 2022 | queued | 0/5 |  |  |  |
| 332 | 30005240 / OWR-11101924-003 | Rigorous Boundary-Layer Density Asymptotics | 0.1642 | 3 | 2022 | queued | 0/5 |  |  |  |
| 333 | 30005303 / OWR-11695865-001 | Total Positivity and Graphical Model Factorization | 0.1642 | 3 | 2022 | queued | 0/5 |  |  |  |
| 334 | 30004008 / OWR-16633-026 | Rainbow Arborescences Across Arc Partitions | 0.1639 | 3 | 2018 | queued | 0/5 |  |  |  |
| 335 | 30004033 / OWR-16763-006 | Fractional Coloring of Subcubic Triangle-Free Planar Graphs | 0.1633 | 3 | 2019 | queued | 0/5 |  |  |  |
| 336 | 30005425 / OWR-12697690-007 | Uniqueness of Surface Models for Locally Gentle Algebras | 0.1630 | 3 | 2023 | queued | 0/5 |  |  |  |
| 337 | 30005718 / OWR-14298007-013 | Ultra-Log-Concavity from a Matrix Recursion | 0.1630 | 3 | 2023 | queued | 0/5 |  |  |  |
| 338 | 30005935 / OWR-14298374-004 | Positivity and Convergence of a Splitting Scheme | 0.1616 | 3 | 2024 | queued | 0/5 |  |  |  |
| 339 | 30006017 / OWR-14298589-002 | Limiting Area Distribution of Random Self-Overlapping Polygons | 0.1616 | 3 | 2024 | queued | 0/5 |  |  |  |
| 340 | 10400078 / AMR-103-0078 | Problem 3.28 — (T. | 0.1600 | 3 | unknown | queued | 0/5 |  |  |  |
| 341 | 9900002 / AMR-098-0002 | Scaling total life in a null-recurrent renewal process | 0.1600 | 3 | unknown | queued | 0/5 |  |  |  |
| 342 | 30005751 / OWR-14298016-007 | Finite Axiomatizability of TEIP over Open Induction | 0.1599 | 3 | 2023 | queued | 0/5 |  |  |  |
| 343 | 4600032 / AMR-045-0032 | Embedding under a preimage bound | 0.1578 | 4 | 2008 | queued | 0/5 |  |  |  |
| 344 | 30001199 / OWR-3394-009 | Circular Assume–Guarantee Reasoning for General Systems | 0.1575 | 3 | 2009 | queued | 0/5 |  |  |  |
| 345 | 30006211 / OWR-14299088-013 | Real Components of Two Multi-Affine Polynomial Zero Sets | 0.1564 | 3 | 2025 | queued | 0/5 |  |  |  |
| 346 | 30006345 / OWR-14299292-007 | Modular Isomorphism for Class-Two Exponent-p Groups | 0.1564 | 3 | 2025 | queued | 0/5 |  |  |  |
| 347 | 30002323 / OWR-12481-012 | Hierarchical Refinement of Symmetric-Group Coset Partitions | 0.1564 | 3 | 2013 | queued | 0/5 |  |  |  |
| 348 | 30002545 / OWR-12872-015 | Combinatorial Proof of the Two-Thirds Leaf Limit | 0.1560 | 3 | 2014 | queued | 0/5 |  |  |  |
| 349 | 10400230 / AMR-103-0230 | Problem 12.25 — (A. | 0.1560 | 3 | unknown | queued | 0/5 |  |  |  |
| 350 | 159 / GREEN-071 | Uniform Random Variables with Uniform Sum | 0.1560 | 1 | unknown | queued | 0/5 |  |  |  |
| 351 | 20000207 / AIM-ALGEBRAIC_GEOMETRY-0207 | Extended-Kruppa constraints, realized conic ambiguity, and invariant eliminants for algebraic silhouettes | 0.1560 | 3 | unknown | queued | 0/5 |  |  |  |
| 352 | 20000450 / AIM-ALGEBRAIC_NUMBER_THEORY-0102 | The infinity 5-torsion line and Kummer quotient of the pentagonal quintic | 0.1560 | 3 | unknown | queued | 0/5 |  |  |  |
| 353 | 20000700 / AIM-ANALYTIC_NUMBER_THEORY-0064 | A finite local prime model for the Bogomolny--Keating Type-II input | 0.1560 | 3 | unknown | queued | 0/5 |  |  |  |
| 354 | 3000058 / AMR-029-0058 | Opposite vertices of base polyhedra | 0.1560 | 3 | unknown | queued | 0/5 |  |  |  |
| 355 | 3048 / OPG-37226 | Sequence defined on multisets | 0.1560 | 1 | unknown | queued | 0/5 |  |  |  |
| 356 | 2800404 / AMR-027-0404 | 10 Lectures and 42 Open Problems — OSNAP | 0.1556 | 3 | 2015 | queued | 0/5 |  |  |  |
| 357 | 30002820 / OWR-13498-010 | Discrete-Conformal Metric Subdivision Schemes | 0.1556 | 3 | 2015 | queued | 0/5 |  |  |  |
| 358 | 30002865 / OWR-13678-006 | Complete-Intersection Kernels of Ideal Projectors | 0.1556 | 3 | 2015 | queued | 0/5 |  |  |  |
| 359 | 30002928 / OWR-13856-004 | Uniqueness of Condensation-Model Parameters | 0.1556 | 3 | 2015 | queued | 0/5 |  |  |  |
| 360 | 30002957 / OWR-13940-005 | Delaunay Simplices in Flag Complexes of Random Triangulations | 0.1556 | 3 | 2015 | queued | 0/5 |  |  |  |
| 361 | 30003660 / OWR-15958-007 | Strong-Induction Admissibility in Cut-Free Modal Calculus | 0.1548 | 3 | 2017 | queued | 0/5 |  |  |  |
| 362 | 30003538 / OWR-15577-010 | Equivalence of Hardy Spaces on Noncompact Manifolds | 0.1548 | 3 | 2017 | queued | 0/5 |  |  |  |
| 363 | 30003688 / OWR-15986-003 | Finite Families with Two-Element Rogers Semilattices | 0.1543 | 3 | 2018 | queued | 0/5 |  |  |  |
| 364 | 30003973 / OWR-16627-005 | Higher-Color Equivalence of Two-Equivalent Graphs | 0.1543 | 3 | 2018 | queued | 0/5 |  |  |  |
| 365 | 2579 / KOU-21.70 | Kourovka Notebook Problem 21.70 | 0.1530 | 2 | 2026 | queued | 0/5 |  |  |  |
| 366 | 2594 / KOU-21.85 | Kourovka Notebook Problem 21.85 | 0.1530 | 2 | 2026 | queued | 0/5 |  |  |  |
| 367 | 30004678 / OWR-7155442-012 | Positive Degrees Within Truth Table and Many One Degrees | 0.1524 | 3 | 2021 | queued | 0/5 |  |  |  |
| 368 | 30004679 / OWR-7155442-013 | Weihrauch Reductions for Paths Through Ill-Founded Trees | 0.1524 | 3 | 2021 | queued | 0/5 |  |  |  |
| 369 | 30005278 / OWR-11695860-018 | Degree-Five Two-Superirreducible Polynomials | 0.1515 | 3 | 2022 | queued | 0/5 |  |  |  |
| 370 | 30005706 / OWR-14298004-014 | Embedding $\sigma$-Compact TDLC Groups | 0.1505 | 3 | 2023 | queued | 0/5 |  |  |  |
| 371 | 30005649 / OWR-14297740-021 | Self-Duality of Quasi-Supersingular Group Schemes | 0.1505 | 3 | 2023 | queued | 0/5 |  |  |  |
| 372 | 30005767 / OWR-14298158-012 | Generating-Function Field for Separable Permutation Subclasses | 0.1491 | 3 | 2024 | queued | 0/5 |  |  |  |
| 373 | 30005936 / OWR-14298374-005 | Splitting Schemes for Rough Stochastic Heat Equations | 0.1491 | 3 | 2024 | queued | 0/5 |  |  |  |
| 374 | 30006025 / OWR-14298589-010 | Geometric Chapuy Bijections for Random Surfaces | 0.1491 | 3 | 2024 | queued | 0/5 |  |  |  |
| 375 | 30006078 / OWR-14298795-018 | Characteristic Classes of Hodge–Tate Local Systems | 0.1491 | 3 | 2024 | queued | 0/5 |  |  |  |
| 376 | 30003128 / OWR-14604-003 | Discrepancy versus Spectral Expansion in Sparse Regular Graphs | 0.1455 | 3 | 2016 | queued | 0/5 |  |  |  |
| 377 | 30003210 / OWR-14749-002 | Sublinear Generator Growth of Higher-Rank Lattices | 0.1455 | 3 | 2016 | queued | 0/5 |  |  |  |
| 378 | 30003221 / OWR-14751-005 | Ball-Shaped Minimizers of Competing Nonlocal Energies | 0.1455 | 3 | 2016 | queued | 0/5 |  |  |  |
| 379 | 30000417 / OWR-1189-007 | List-Labeling Numbers of Paths | 0.1451 | 3 | 2006 | queued | 0/5 |  |  |  |
| 380 | 30000660 / OWR-1452-024 | Étale-Local Equivalence of Fiberwise Isomorphic Families | 0.1449 | 3 | 2007 | queued | 0/5 |  |  |  |
| 381 | 30001014 / OWR-2048-009 | Realizing Compact Spectra of Pathological Masas | 0.1446 | 3 | 2008 | queued | 0/5 |  |  |  |
| 382 | 30001202 / OWR-3394-018 | Optimal Feasible Sets from Quantized Trajectory Observations | 0.1444 | 3 | 2009 | queued | 0/5 |  |  |  |
| 383 | 30001370 / OWR-4132-003 | Common Basin Boundaries in a Transfer-Operator System | 0.1444 | 3 | 2009 | queued | 0/5 |  |  |  |
| 384 | 30001552 / OWR-4425-007 | Fine–Wilf Bounds for Antimorphic Periods | 0.1442 | 3 | 2010 | queued | 0/5 |  |  |  |
| 385 | 30001554 / OWR-4425-009 | Unbordered Factors and Alternating Involution Periods | 0.1442 | 3 | 2010 | queued | 0/5 |  |  |  |
| 386 | 30001563 / OWR-4425-020 | PVHH-Cube Avoidance in a Morphic Fixed Point | 0.1442 | 3 | 2010 | queued | 0/5 |  |  |  |
| 387 | 30004048 / OWR-16763-022 | Symmetry of Bidirectional Two-Step Path Density | 0.1441 | 3 | 2019 | queued | 0/5 |  |  |  |
| 388 | 30004320 / OWR-17295-004 | Descent of Rational Points from Laurent Series Fields | 0.1441 | 3 | 2019 | queued | 0/5 |  |  |  |
| 389 | 11000151 / AMR-109-0151 | Question — Consider the Artin group A5 (the braid group on six strings) divided by the relation (a1a2a3a4)5 = a5a4a3a2a2 1a2a3a4a5. | 0.1440 | 3 | unknown | queued | 0/5 |  |  |  |
| 390 | 11000228 / AMR-109-0228 | Problem 21 — (Exceptional Strata). | 0.1440 | 3 | unknown | queued | 0/5 |  |  |  |
| 391 | 20000728 / AIM-ANALYTIC_NUMBER_THEORY-0092 | Weight-only modularity recognition has a finite-data obstruction | 0.1440 | 3 | unknown | queued | 0/5 |  |  |  |
| 392 | 20001666 / AIM-GEOMETRY-0004 | Fixed-volume degeneration of Maxwell cavity eigenvalues | 0.1440 | 3 | unknown | queued | 0/5 |  |  |  |
| 393 | 2302055 / AMR-022-2055 | Research Problems in Function Theory — Problem 2.55 | 0.1440 | 3 | unknown | queued | 0/5 |  |  |  |
| 394 | 2303002 / AMR-022-3002 | Research Problems in Function Theory — Problem 3.2 | 0.1440 | 3 | unknown | queued | 0/5 |  |  |  |
| 395 | 2303016 / AMR-022-3016 | Research Problems in Function Theory — Problem 3.16 | 0.1440 | 3 | unknown | queued | 0/5 |  |  |  |
| 396 | 9400114 / AMR-093-0114 | Agrawal's conjecture | 0.1440 | 3 | unknown | queued | 0/5 |  |  |  |
| 397 | 9700034 / AMR-096-0034 | Integrability of all routes to random points in a SIRSN | 0.1440 | 3 | unknown | queued | 0/5 |  |  |  |
| 398 | 30004435 / OWR-17474-009 | Probabilistic Equality of Left and Right Tail Fields | 0.1435 | 3 | 2020 | queued | 0/5 |  |  |  |
| 399 | 30004811 / OWR-8415343-014 | Equality of Capacity–Volume and ADM Mass | 0.1429 | 3 | 2021 | queued | 0/5 |  |  |  |
| 400 | 30005116 / OWR-10252930-028 | Induced Four-Cycle Profiles Above Half Density | 0.1421 | 3 | 2022 | queued | 0/5 |  |  |  |
| 401 | 30004293 / OWR-17293-009 | Maximum Additive Multiplicity in Logarithmic Random Sets | 0.1409 | 3 | 2019 | queued | 0/5 |  |  |  |
| 402 | 30004322 / OWR-17296-003 | Seshadri Constants of Line Arrangement Singularities | 0.1409 | 3 | 2019 | queued | 0/5 |  |  |  |
| 403 | 30000590 / OWR-1381-005 | Finite Generation of Group-Ring Cohomology | 0.1401 | 3 | 2006 | queued | 0/5 |  |  |  |
| 404 | 7800012 / AMR-077-0012 | Optimal Flux for the Quarter-Filled Band | 0.1398 | 3 | 1998 | queued | 0/5 |  |  |  |
| 405 | 30002200 / OWR-12172-003 | Sharp Syzygy Bounds for Torus Actions | 0.1393 | 3 | 2012 | queued | 0/5 |  |  |  |
| 406 | 30002762 / OWR-13488-005 | Finitely Presented Counterexamples for Conjugation-Invariant Norms | 0.1378 | 3 | 2015 | queued | 0/5 |  |  |  |
| 407 | 6600013 / AMR-065-0013 | A. Julien: Relationship between Complexity and Cohomology — Problem | 0.1374 | 4 | 2016 | queued | 0/5 |  |  |  |
| 408 | 30003853 / OWR-16167-025 | Abelianizations of Finitely Presented Thompson $F$ Subgroups | 0.1366 | 3 | 2018 | queued | 0/5 |  |  |  |
| 409 | 30004047 / OWR-16763-021 | Two-Step Path Density in Tripartite Graphs | 0.1361 | 3 | 2019 | queued | 0/5 |  |  |  |
| 410 | 30004106 / OWR-16776-002 | Symmetry of Completed Finite-Group Representation Rings | 0.1361 | 3 | 2019 | queued | 0/5 |  |  |  |
| 411 | 30004656 / OWR-4990384-001 | Robustness-Driven Overparameterization in Two-Layer Neural Networks | 0.1355 | 3 | 2021 | queued | 0/5 |  |  |  |
| 412 | 2511 / KOU-21.2 | Kourovka Notebook Problem 21.2 | 0.1350 | 2 | 2026 | queued | 0/5 |  |  |  |
| 413 | 2518 / KOU-21.9 | Kourovka Notebook Problem 21.9 | 0.1350 | 2 | 2026 | queued | 0/5 |  |  |  |
| 414 | 2525 / KOU-21.16 | Kourovka Notebook Problem 21.16 | 0.1350 | 2 | 2026 | queued | 0/5 |  |  |  |
| 415 | 2531 / KOU-21.22 | Kourovka Notebook Problem 21.22 | 0.1350 | 2 | 2026 | queued | 0/5 |  |  |  |
| 416 | 30004865 / OWR-8415352-007 | Completeness of Realignment and SIC-POVM Entanglement Tests | 0.1333 | 3 | 2021 | queued | 0/5 |  |  |  |
| 417 | 6200004 / AMR-061-0004 | Boundaries of Groups and Kleinian Groups — Problem 4 | 0.1321 | 3 | 2005 | queued | 0/5 |  |  |  |
| 418 | 6200043 / AMR-061-0043 | Boundaries of Groups and Kleinian Groups — Problem 43 | 0.1321 | 3 | 2005 | queued | 0/5 |  |  |  |
| 419 | 6200082 / AMR-061-0082 | Boundaries of Groups and Kleinian Groups — Problem 82 | 0.1321 | 3 | 2005 | queued | 0/5 |  |  |  |
| 420 | 30005804 / OWR-14298163-008 | Dolnikov’s Colorful Transversal Conjecture | 0.1321 | 3 | 2024 | queued | 0/5 |  |  |  |
| 421 | 11000020 / AMR-109-0020 | Problem 2.19 — (Canonical basepoints for Mg). | 0.1320 | 3 | unknown | queued | 0/5 |  |  |  |
| 422 | 11000158 / AMR-109-0158 | Problem 2.1 — Assume, for this problem, that M is a 3-manifold with non-empty boundary. | 0.1320 | 3 | unknown | queued | 0/5 |  |  |  |
| 423 | 20000693 / AIM-ANALYTIC_NUMBER_THEORY-0057 | Multiplicity-sensitive moments of products of Dirichlet L-functions | 0.1320 | 3 | unknown | queued | 0/5 |  |  |  |
| 424 | 20002717 / AIM-PROBABILITY-0159 | A product criterion and a bowtie obstruction for Cayley interval lattices | 0.1320 | 3 | unknown | queued | 0/5 |  |  |  |
| 425 | 3031 / OPG-57824 | Graphs of exact colorings | 0.1320 | 1 | unknown | queued | 0/5 |  |  |  |
| 426 | 9700002 / AMR-096-0002 | Analytic toy model for a percolation-fragmentation congestion transition | 0.1320 | 3 | unknown | queued | 0/5 |  |  |  |
| 427 | 8000011 / AMR-079-0011 | The Toda lattice with random initial data | 0.1317 | 3 | 2007 | queued | 0/5 |  |  |  |
| 428 | 30000997 / OWR-2042-006 | Degenerate Versus Full Ma–Trudinger–Wang Conditions | 0.1315 | 3 | 2008 | queued | 0/5 |  |  |  |
| 429 | 30001070 / OWR-2090-023 | Circumscribed $2n$-Facet Polytopes around the Unit Ball | 0.1315 | 3 | 2008 | queued | 0/5 |  |  |  |
| 430 | 30001084 / OWR-2093-008 | Randomized-Transport Characterizations of Palm Measures | 0.1315 | 3 | 2008 | queued | 0/5 |  |  |  |
| 431 | 30001179 / OWR-3392-005 | Generation of Free Product Systems by Tensor Subsystems | 0.1313 | 3 | 2009 | queued | 0/5 |  |  |  |
| 432 | 30001568 / OWR-4426-005 | Symmetry-Preserving Evaluation of Orbitwise Generating Functions | 0.1311 | 3 | 2010 | queued | 0/5 |  |  |  |
| 433 | 30001895 / OWR-11136-027 | Exact Transversals for Families with the (p,q)-Property | 0.1308 | 3 | 2011 | queued | 0/5 |  |  |  |
| 434 | 30001957 / OWR-11570-002 | Entropy Production on Folded Hyperbolic Fractals | 0.1306 | 3 | 2012 | queued | 0/5 |  |  |  |
| 435 | 30002136 / OWR-12007-016 | Nonconjugate $\operatorname{SL}_3$-Character-Equivalent Free-Group Words | 0.1306 | 3 | 2012 | queued | 0/5 |  |  |  |
| 436 | 30006342 / OWR-14299292-003 | Common-Neighbor Conjecture for Generalized Saxl Graphs | 0.1304 | 3 | 2025 | queued | 0/5 |  |  |  |
| 437 | 30002637 / OWR-13106-010 | Instability of Nontrivial Compact Ricci Solitons | 0.1300 | 3 | 2014 | queued | 0/5 |  |  |  |
| 438 | 30002659 / OWR-13110-001 | Shortest Billiard Trajectories in Constant Width Bodies | 0.1300 | 3 | 2014 | queued | 0/5 |  |  |  |
| 439 | 30003813 / OWR-16164-005 | Combinatorics of Signed Adjacency Polytopes | 0.1286 | 3 | 2018 | queued | 0/5 |  |  |  |
| 440 | 30003786 / OWR-16160-016 | Embedding Independence of Congruence Subgroups | 0.1286 | 3 | 2018 | queued | 0/5 |  |  |  |
| 441 | 30003840 / OWR-16167-010 | Conjugacy in Braided Thompson Groups | 0.1286 | 3 | 2018 | queued | 0/5 |  |  |  |
| 442 | 6800004 / AMR-067-0004 | Biorthogonal curvature | 0.1286 | 3 | 2018 | queued | 0/5 |  |  |  |
| 443 | 6800009 / AMR-067-0009 | Bi-invariant metrics and multiplicity of conjugate points | 0.1286 | 3 | 2018 | queued | 0/5 |  |  |  |
| 444 | 6800014 / AMR-067-0014 | Ricci pinching on solvable Lie groups | 0.1286 | 3 | 2018 | queued | 0/5 |  |  |  |
| 445 | 30001005 / OWR-2045-001 | Mean-Curvature Flow from Isolated Conical Singularities | 0.1282 | 3 | 2008 | queued | 0/5 |  |  |  |
| 446 | 10000083 / AMR-099-0083 | Exponential upper bound for linear-time graph covering | 0.1280 | 3 | unknown | queued | 0/5 |  |  |  |
| 447 | 10400067 / AMR-103-0067 | Problem 3.17 — Find a topological construction of the 2-loop polynomial P θ K. | 0.1280 | 3 | unknown | queued | 0/5 |  |  |  |
| 448 | 10400167 / AMR-103-0167 | Problem 9.3 — (Y. | 0.1280 | 3 | unknown | queued | 0/5 |  |  |  |
| 449 | 11000048 / AMR-109-0048 | Problem 4.11 — (Coarse Schottky problem). | 0.1280 | 3 | unknown | queued | 0/5 |  |  |  |
| 450 | 2100406 / AMR-020-0406 | Open Problems in Integrable Systems — Geometry of caustics, invariant surfaces, and commuting billiard maps | 0.1280 | 3 | unknown | queued | 0/5 |  |  |  |
| 451 | 7200087 / AMR-071-0087 | Is there a non-convex polyhedron without self-intersections with more than seven faces, all of which share an edge with each other | 0.1280 | 3 | unknown | queued | 0/5 |  |  |  |
| 452 | 30004557 / OWR-2654830-012 | Constructive Definitional Extensions and Morita Equivalence | 0.1276 | 3 | 2020 | queued | 0/5 |  |  |  |
| 453 | 20001284 / AIM-CONVEX_GEOMETRY-0016 | Finite-dimensional local rigidity from central-section perimeters | 0.1275 | 3 | unknown | queued | 0/5 |  |  |  |
| 454 | 20001506 / AIM-GEOMETRIC_GROUP_THEORY-0015 | An explicit lamination-depth gap for the AIM free-by-cyclic pair | 0.1275 | 4 | unknown | queued | 0/5 |  |  |  |
| 455 | 20001515 / AIM-GEOMETRIC_GROUP_THEORY-0024 | Fast monodromy and the cocompact cubulation bottleneck | 0.1275 | 4 | unknown | queued | 0/5 |  |  |  |
| 456 | 20001546 / AIM-GEOMETRIC_GROUP_THEORY-0055 | A character-twist obstruction on the extended Deligne Helly graph | 0.1275 | 3 | unknown | queued | 0/5 |  |  |  |
| 457 | 20001670 / AIM-GEOMETRY-0008 | Attainment and a quantitative segment bound for planar p-capacity | 0.1275 | 3 | unknown | queued | 0/5 |  |  |  |
| 458 | 20001782 / AIM-GEOMETRY-0120 | Element-order reduction and short-span bounds for Delone cluster groups | 0.1275 | 4 | unknown | queued | 0/5 |  |  |  |
| 459 | 20001851 / AIM-GEOMETRY-0189 | A one-coordinate unlockability certificate for open chains in three-space | 0.1275 | 3 | unknown | queued | 0/5 |  |  |  |
| 460 | 20001939 / AIM-GEOMETRY-0277 | Affine rigidity and a mobility-two reduction on the Lorentz 3-sphere | 0.1275 | 3 | unknown | queued | 0/5 |  |  |  |
| 461 | 20002029 / AIM-GEOMETRY-0367 | Critical-weight conformal invariants built from Schouten jets | 0.1275 | 3 | unknown | queued | 0/5 |  |  |  |
| 462 | 20002237 / AIM-LOGIC-0013 | Addition with directed p-power divisibility | 0.1275 | 3 | unknown | queued | 0/5 |  |  |  |
| 463 | 20002290 / AIM-LOGIC-0066 | A positive-existential definition of nonzero rationals | 0.1275 | 3 | unknown | queued | 0/5 |  |  |  |
| 464 | 2561 / KOU-21.52 | Kourovka Notebook Problem 21.52 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 465 | 2566 / KOU-21.57 | Kourovka Notebook Problem 21.57 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 466 | 2569 / KOU-21.60 | Kourovka Notebook Problem 21.60 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 467 | 2580 / KOU-21.71 | Kourovka Notebook Problem 21.71 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 468 | 2607 / KOU-21.98 | Kourovka Notebook Problem 21.98 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 469 | 2609 / KOU-21.100 | Kourovka Notebook Problem 21.100 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 470 | 2611 / KOU-21.102 | Kourovka Notebook Problem 21.102 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 471 | 2622 / KOU-21.113 | Kourovka Notebook Problem 21.113 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 472 | 2628 / KOU-21.119 | Kourovka Notebook Problem 21.119 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 473 | 2637 / KOU-21.128 | Kourovka Notebook Problem 21.128 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 474 | 2643 / KOU-21.134 | Kourovka Notebook Problem 21.134 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 475 | 2645 / KOU-21.136 | Kourovka Notebook Problem 21.136 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 476 | 2650 / KOU-21.141 | Kourovka Notebook Problem 21.141 | 0.1275 | 2 | 2026 | queued | 0/5 |  |  |  |
| 477 | 2801 / KP-3.3 | Kirby Problem 3.3 | 0.1275 | 3 | unknown | queued | 0/5 |  |  |  |
| 478 | 30006560 / OWR-14299905-035 | Vertex Sets Meeting Every Edge Color | 0.1275 | 3 | 2026 | queued | 0/5 |  |  |  |
| 479 | 30006563 / OWR-14299905-038 | Colorings Without Disjoint Color-Isomorphic Triangles | 0.1275 | 3 | 2026 | queued | 0/5 |  |  |  |
| 480 | 30002737 / OWR-13355-001 | Absolutely Continuous Diffraction and Dynamical Spectra | 0.1268 | 3 | 2014 | queued | 0/5 |  |  |  |
| 481 | 30004980 / OWR-9790352-030 | Maximum Twin-Width of $n$-Vertex Graphs | 0.1263 | 3 | 2022 | queued | 0/5 |  |  |  |
| 482 | 30005041 / OWR-9790362-012 | Interval Structure of Cohomology-Vanishing Exponents | 0.1263 | 3 | 2022 | queued | 0/5 |  |  |  |
| 483 | 30005075 / OWR-9790367-005 | Affine–Virasoro Derivation of Nekrasov Blow-Up Identities | 0.1263 | 3 | 2022 | queued | 0/5 |  |  |  |
| 484 | 30005144 / OWR-10252937-007 | CMC Min–Max Width Under Nonnegative Scalar Curvature | 0.1263 | 3 | 2022 | queued | 0/5 |  |  |  |
| 485 | 30005220 / OWR-11101920-004 | Sylow Restrictions and Character Fields of Values | 0.1263 | 3 | 2022 | queued | 0/5 |  |  |  |
| 486 | 30005248 / OWR-11695855-001 | Local Complexity of Functional Estimation | 0.1263 | 3 | 2022 | queued | 0/5 |  |  |  |
| 487 | 2305057 / AMR-022-5057 | Research Problems in Function Theory — Problem 5.57 | 0.1260 | 3 | unknown | queued | 0/5 |  |  |  |
| 488 | 30005507 / OWR-13750328-012 | Frobenius–Schur Indicators in Real Nilpotent Blocks | 0.1254 | 3 | 2023 | queued | 0/5 |  |  |  |
| 489 | 30005508 / OWR-13750328-013 | Projective Characters and Square Roots in Real Blocks | 0.1254 | 3 | 2023 | queued | 0/5 |  |  |  |
| 490 | 30005717 / OWR-14298007-012 | Even-Dimensional Stress-Space Reconstruction | 0.1254 | 3 | 2023 | queued | 0/5 |  |  |  |
| 491 | 30005723 / OWR-14298009-001 | Modular Generators for Massive Double Cones | 0.1254 | 3 | 2023 | queued | 0/5 |  |  |  |
| 492 | 30005528 / OWR-13750333-009 | Periodic Minimizers in Compact Linear Domino Games | 0.1254 | 3 | 2023 | queued | 0/5 |  |  |  |
| 493 | 6000016 / AMR-059-0016 | Stability of Hessian Metrics | 0.1248 | 3 | 1998 | queued | 0/5 |  |  |  |
| 494 | 30005772 / OWR-14298158-017 | Combinatorial Interpretations of Negative k-Arrangements | 0.1243 | 3 | 2024 | queued | 0/5 |  |  |  |
| 495 | 30005832 / OWR-14298166-010 | Fractional Coefficient Savings in Algebraic Proof Systems | 0.1243 | 3 | 2024 | queued | 0/5 |  |  |  |
| 496 | 30004807 / OWR-8415343-010 | Weak Bianchi Identities Across Timelike Singularities | 0.1238 | 3 | 2021 | queued | 0/5 |  |  |  |
| 497 | 30000330 / OWR-1106-004 | Quasiconformal Homogeneity Gaps for Hyperbolic Surfaces | 0.1238 | 3 | 2005 | queued | 0/5 |  |  |  |
| 498 | 30000689 / OWR-1455-008 | Embedding Obstructions from Missing Simplicial Faces | 0.1235 | 3 | 2007 | queued | 0/5 |  |  |  |
| 499 | 30000999 / OWR-2042-008 | Inverse Wasserstein Stability of the Geodesic Radon Transform | 0.1233 | 3 | 2008 | queued | 0/5 |  |  |  |
| 500 | 30001148 / OWR-3388-006 | Local–Global Principles for Homogeneous Spaces over Semi-Global Fields | 0.1231 | 3 | 2009 | queued | 0/5 |  |  |  |
| 501 | 30006510 / OWR-14299586-001 | Typical Cells in Hyperbolic Tessellations with Unbounded Cells | 0.1227 | 3 | 2025 | queued | 0/5 |  |  |  |
| 502 | 30002086 / OWR-11789-007 | Gradient Lower Bounds for Shrinking Ricci Solitons | 0.1224 | 3 | 2012 | queued | 0/5 |  |  |  |
| 503 | 30002320 / OWR-12481-005 | Existence of Random-Graph Coloring Growth Rates | 0.1221 | 3 | 2013 | queued | 0/5 |  |  |  |
| 504 | 30005961 / OWR-14298581-008 | Positive-Entropy Automorphisms of Strict Calabi-Yau Threefolds | 0.1212 | 3 | 2024 | queued | 0/5 |  |  |  |
| 505 | 30003616 / OWR-15951-003 | Half-Line Spectra for Fibonacci Schrödinger Operators | 0.1209 | 3 | 2017 | queued | 0/5 |  |  |  |
| 506 | 30003656 / OWR-15958-003 | Wraith Redundancy for Algebraic Theories | 0.1209 | 3 | 2017 | queued | 0/5 |  |  |  |
| 507 | 10400136 / AMR-103-0136 | Problem 7.21 — (S. | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 508 | 10900004 / AMR-108-0004 | 1.4 (Danciger) — Convex projective structures on glued figure-eight complements | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 509 | 20001282 / AIM-CONVEX_GEOMETRY-0014 | A sharp product-prism family for Kuperberg's fixed-combinatorial-type question | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 510 | 20001287 / AIM-CONVEX_GEOMETRY-0019 | A sharp wedge-orthant family for the spherical simplex volume product | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 511 | 20001306 / AIM-CONVEX_GEOMETRY-0038 | Closedness, dimensional correction, and a dual certificate for polar-zonoid intersection bodies | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 512 | 20001353 / AIM-DYNAMICAL_SYSTEMS-0011 | A maximal dyadic-pair stabilizer in Thompson's group T | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 513 | 20001752 / AIM-GEOMETRY-0090 | Midpoint projection and modular-period reductions for the E8 and Leech magic functions | 0.1200 | 4 | unknown | queued | 0/5 |  |  |  |
| 514 | 20001754 / AIM-GEOMETRY-0092 | Symmetry obstruction and invariant-subprogram collapse for the AIM lattice three-point bound | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 515 | 20002370 / AIM-LOGIC-0146 | Exact alternation depth and variable bounds for two real rational-function fields | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 516 | 20002696 / AIM-PROBABILITY-0138 | Uniform heat convergence, spectral tails, and affiliated innerness | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 517 | 20003004 / AIM-TOPOLOGY-0092 | Digital pi_2, clique realization, and the octahedral sphere | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 518 | 2302005 / AMR-022-2005 | Research Problems in Function Theory — Problem 2.5 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 519 | 2302054 / AMR-022-2054 | Research Problems in Function Theory — Problem 2.54 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 520 | 2302058 / AMR-022-2058 | Research Problems in Function Theory — Problem 2.58 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 521 | 2304006 / AMR-022-4006 | Research Problems in Function Theory — Problem 4.6 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 522 | 2304025 / AMR-022-4025 | Research Problems in Function Theory — Problem 4.25 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 523 | 2305028 / AMR-022-5028 | Research Problems in Function Theory — Problem 5.28 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 524 | 2305039 / AMR-022-5039 | Research Problems in Function Theory — Problem 5.39 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 525 | 2305050 / AMR-022-5050 | Research Problems in Function Theory — Problem 5.50 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 526 | 2306017 / AMR-022-6017 | Research Problems in Function Theory — Problem 6.17 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 527 | 2306038 / AMR-022-6038 | Research Problems in Function Theory — Problem 6.38 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 528 | 2306052 / AMR-022-6052 | Research Problems in Function Theory — Problem 6.52 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 529 | 2306083 / AMR-022-6083 | Research Problems in Function Theory — Problem 6.83 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 530 | 2307054 / AMR-022-7054 | Research Problems in Function Theory — Problem 7.54 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 531 | 2863 / KP-3.65 | Kirby Problem 3.65 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 532 | 2897 / KP-4.21 | Kirby Problem 4.21 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 533 | 2902 / KP-4.26 | Kirby Problem 4.26 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 534 | 2914 / KP-4.38 | Kirby Problem 4.38 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 535 | 2924 / KP-4.48 | Kirby Problem 4.48 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 536 | 2940 / KP-4.64 | Kirby Problem 4.64 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 537 | 2972 / KP-4.96 | Kirby Problem 4.96 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 538 | 3024 / KP-5.17 | Kirby Problem 5.17 | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 539 | 3419 / OPG-37237 | Unsolvability of word problem for 2-knot complements | 0.1200 | 2 | unknown | queued | 0/5 |  |  |  |
| 540 | 9700001 / AMR-096-0001 | Martingale for practical purposes | 0.1200 | 3 | unknown | queued | 0/5 |  |  |  |
| 541 | 30004773 / OWR-8415341-012 | Character Degrees of Graph-Defined Exponent-$p$ Groups | 0.1191 | 3 | 2021 | queued | 0/5 |  |  |  |
| 542 | 5200008 / AMR-051-0008 | Open Problems on Billiards and Geometric Optics | 0.1191 | 3 | 2021 | queued | 0/5 |  |  |  |
| 543 | 30005558 / OWR-13750339-002 | Hodge Integrals over Genus-One Admissible Covers | 0.1176 | 3 | 2023 | queued | 0/5 |  |  |  |
| 544 | 30005598 / OWR-14297736-004 | de Gennes Bound for Magnetic Neumann Eigenvalues | 0.1176 | 3 | 2023 | queued | 0/5 |  |  |  |
| 545 | 5300049 / AMR-052-0049 | Accessibility of positive-exponent boundary points | 0.1171 | 3 | 1992 | queued | 0/5 |  |  |  |
| 546 | 6000015 / AMR-059-0015 | Stein Tangent Bundles of Complete Hessian Manifolds | 0.1165 | 3 | 1998 | queued | 0/5 |  |  |  |
| 547 | 30003571 / OWR-15582-005 | Relative Kähler–Ricci Flow on Projective-Space Fibrations | 0.1161 | 3 | 2017 | queued | 0/5 |  |  |  |
| 548 | 6200007 / AMR-061-0007 | Boundaries of Groups and Kleinian Groups — Problem 7 | 0.1155 | 3 | 2005 | queued | 0/5 |  |  |  |
| 549 | 30000552 / OWR-1319-022 | Asymptotically Equivalent Cocompact Metrics | 0.1154 | 3 | 2006 | queued | 0/5 |  |  |  |
| 550 | 30004064 / OWR-16766-003 | Dual Recovery of Binary Tomography Solution Intersections | 0.1153 | 3 | 2019 | queued | 0/5 |  |  |  |
| 551 | 30000679 / OWR-1453-013 | Solvability of Rank-Two NIP Groups | 0.1152 | 3 | 2007 | queued | 0/5 |  |  |  |
| 552 | 30001065 / OWR-2090-018 | Universal Optimality of Exceptional Spherical Codes | 0.1150 | 3 | 2008 | queued | 0/5 |  |  |  |
| 553 | 4000010 / AMR-039-0010 | Functional inequalities | 0.1150 | 3 | 2008 | queued | 0/5 |  |  |  |
| 554 | 30006272 / OWR-14299283-013 | Catalan Formulas for Ekedahl-Oort Intersection Cohomology | 0.1150 | 3 | 2025 | queued | 0/5 |  |  |  |
| 555 | 30006308 / OWR-14299288-014 | Deformation Spaces of Smooth Complete Toric Varieties | 0.1150 | 3 | 2025 | queued | 0/5 |  |  |  |
| 556 | 30006359 / OWR-14299511-008 | Irreducible Forest Decomposition of Consistency-Equation Varieties | 0.1150 | 3 | 2025 | queued | 0/5 |  |  |  |
| 557 | 30006363 / OWR-14299512-001 | Topological Invariance of Helicity | 0.1150 | 3 | 2025 | queued | 0/5 |  |  |  |
| 558 | 30001242 / OWR-3472-013 | Uniform Generic Degree Bounds for Ideal Membership | 0.1149 | 3 | 2009 | queued | 0/5 |  |  |  |
| 559 | 30001182 / OWR-3392-009 | Ambient-Algebra Independence of Exchangeable Independence | 0.1149 | 3 | 2009 | queued | 0/5 |  |  |  |
| 560 | 30004637 / OWR-4990379-007 | Fast Algorithms for Branching Brownian Unbalanced Transport | 0.1143 | 3 | 2021 | queued | 0/5 |  |  |  |
| 561 | 2700004 / AMR-026-0004 | Five Open Problems — Eternal finite-energy compressible Euler flow | 0.1142 | 4 | 2012 | queued | 0/5 |  |  |  |
| 562 | 30005215 / OWR-11101919-002 | Norm Estimation from Asymmetric Black-Box Linear Operators | 0.1136 | 3 | 2022 | queued | 0/5 |  |  |  |
| 563 | 20001587 / AIM-GEOMETRIC_GROUP_THEORY-0096 | A finite-gluing obstruction for amenable clopen restrictions | 0.1125 | 4 | unknown | queued | 0/5 |  |  |  |
| 564 | 2301039 / AMR-022-1039 | Research Problems in Function Theory — Problem 1.39 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 565 | 2302004 / AMR-022-2004 | Research Problems in Function Theory — Problem 2.4 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 566 | 2302069 / AMR-022-2069 | Research Problems in Function Theory — Problem 2.69 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 567 | 2302073 / AMR-022-2073 | Research Problems in Function Theory — Problem 2.73 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 568 | 2303003 / AMR-022-3003 | Research Problems in Function Theory — Problem 3.3 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 569 | 2303012 / AMR-022-3012 | Research Problems in Function Theory — Problem 3.12 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 570 | 2303015 / AMR-022-3015 | Research Problems in Function Theory — Problem 3.15 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 571 | 2303019 / AMR-022-3019 | Research Problems in Function Theory — Problem 3.19 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 572 | 2303022 / AMR-022-3022 | Research Problems in Function Theory — Problem 3.22 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 573 | 2303032 / AMR-022-3032 | Research Problems in Function Theory — Problem 3.32 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 574 | 2304009 / AMR-022-4009 | Research Problems in Function Theory — Problem 4.9 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 575 | 2305046 / AMR-022-5046 | Research Problems in Function Theory — Problem 5.46 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 576 | 2305055 / AMR-022-5055 | Research Problems in Function Theory — Problem 5.55 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 577 | 2305060 / AMR-022-5060 | Research Problems in Function Theory — Problem 5.60 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 578 | 2305065 / AMR-022-5065 | Research Problems in Function Theory — Problem 5.65 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 579 | 2305066 / AMR-022-5066 | Research Problems in Function Theory — Problem 5.66 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 580 | 2305070 / AMR-022-5070 | Research Problems in Function Theory — Problem 5.70 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 581 | 2306010 / AMR-022-6010 | Research Problems in Function Theory — Problem 6.10 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 582 | 2306031 / AMR-022-6031 | Research Problems in Function Theory — Problem 6.31 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 583 | 2306040 / AMR-022-6040 | Research Problems in Function Theory — Problem 6.40 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 584 | 2306044 / AMR-022-6044 | Research Problems in Function Theory — Problem 6.44 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 585 | 2306063 / AMR-022-6063 | Research Problems in Function Theory — Problem 6.63 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 586 | 2306065 / AMR-022-6065 | Research Problems in Function Theory — Problem 6.65 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 587 | 2306072 / AMR-022-6072 | Research Problems in Function Theory — Problem 6.72 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 588 | 2306080 / AMR-022-6080 | Research Problems in Function Theory — Problem 6.80 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 589 | 2306088 / AMR-022-6088 | Research Problems in Function Theory — Problem 6.88 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 590 | 2306111 / AMR-022-6111 | Research Problems in Function Theory — Problem 6.111 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 591 | 2307017 / AMR-022-7017 | Research Problems in Function Theory — Problem 7.17 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 592 | 2746 / KP-1.87 | Kirby Problem 1.87 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 593 | 2807 / KP-3.9 | Kirby Problem 3.9 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 594 | 2831 / KP-3.33 | Kirby Problem 3.33 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 595 | 2887 / KP-4.11 | Kirby Problem 4.11 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 596 | 2927 / KP-4.51 | Kirby Problem 4.51 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 597 | 2995 / KP-4.119 | Kirby Problem 4.119 | 0.1125 | 3 | unknown | queued | 0/5 |  |  |  |
| 598 | 30006605 / OWR-14299911-007 | Weighted Centers on Bounded-Dimensional Median Graphs | 0.1125 | 3 | 2026 | queued | 0/5 |  |  |  |
| 599 | 3341 / OPG-37448 | MSO alternation hierarchy over pictures | 0.1125 | 1 | unknown | queued | 0/5 |  |  |  |
| 600 | 30000080 / OWR-734-005 | Powers of Linearly Presented Primary Ideals | 0.1124 | 3 | 2004 | queued | 0/5 |  |  |  |
| 601 | 30000203 / OWR-793-006 | Minimal Subdegrees of Twisted-Wreath Permutation Groups | 0.1122 | 3 | 2005 | queued | 0/5 |  |  |  |
| 602 | 30004319 / OWR-17295-003 | Alternativity of Parameters for $A_2$-Graded Groups | 0.1121 | 3 | 2019 | queued | 0/5 |  |  |  |
| 603 | 30000583 / OWR-1326-004 | Projective Subspaces with Trivial Normal Bundle in Fano Manifolds | 0.1121 | 3 | 2006 | queued | 0/5 |  |  |  |
| 604 | 4300001 / AMR-042-0001 | Order of mixing | 0.1121 | 4 | 2006 | queued | 0/5 |  |  |  |
| 605 | 10400107 / AMR-103-0107 | Problem 5.11 — (C. | 0.1120 | 3 | unknown | queued | 0/5 |  |  |  |
| 606 | 30000706 / OWR-1460-013 | Four-Value-Sharing Meromorphic Functions with $\psi=1$ | 0.1119 | 3 | 2007 | queued | 0/5 |  |  |  |
| 607 | 30000707 / OWR-1460-014 | Exponential Auxiliary Systems for Four-Value-Sharing Meromorphic Functions | 0.1119 | 3 | 2007 | queued | 0/5 |  |  |  |
| 608 | 30000750 / OWR-1537-002 | Reduced Length and Mahler-Measure Inequality | 0.1119 | 3 | 2007 | queued | 0/5 |  |  |  |
| 609 | 30000971 / OWR-1971-004 | Eisenbud's Fiber-Regularity Conjecture | 0.1118 | 3 | 2008 | queued | 0/5 |  |  |  |
| 610 | 30001033 / OWR-2053-013 | Finite Width of the 14-Triangle Complex Group | 0.1118 | 3 | 2008 | queued | 0/5 |  |  |  |
| 611 | 30004404 / OWR-17471-010 | Free Subgroups Avoiding All Dehn-Surgery Kernels | 0.1116 | 3 | 2020 | queued | 0/5 |  |  |  |
| 612 | 30004456 / OWR-1703863-005 | $L^2$ Euler Characteristics and HNN Splittings | 0.1116 | 3 | 2020 | queued | 0/5 |  |  |  |
| 613 | 30001211 / OWR-3396-010 | Uniform Recurrence Rates for Minimal Interval Exchanges | 0.1116 | 3 | 2009 | queued | 0/5 |  |  |  |
| 614 | 30001232 / OWR-3471-006 | Lower Bounds for Seshadri Constants on Minimal Surfaces | 0.1116 | 3 | 2009 | queued | 0/5 |  |  |  |
| 615 | 30001388 / OWR-4137-004 | Escaping Boundary Points of Baker Domains | 0.1116 | 3 | 2009 | queued | 0/5 |  |  |  |
| 616 | 30001391 / OWR-4137-007 | Degree Bounds for Degenerate Herman Rings | 0.1116 | 3 | 2009 | queued | 0/5 |  |  |  |
| 617 | 30001393 / OWR-4137-010 | Complete Invariance of Singular-Value Basins | 0.1116 | 3 | 2009 | queued | 0/5 |  |  |  |
| 618 | 30003790 / OWR-16161-003 | Consistent Noisy Single-Index Regression | 0.1114 | 3 | 2018 | queued | 0/5 |  |  |  |
| 619 | 30001672 / OWR-4791-032 | High Influence Small Sets in Boolean Functions | 0.1112 | 3 | 2011 | queued | 0/5 |  |  |  |
| 620 | 30001687 / OWR-4793-001 | Spectral Thickness of Fibonacci Hamiltonians | 0.1112 | 3 | 2011 | queued | 0/5 |  |  |  |
| 621 | 30001721 / OWR-4800-012 | Tree Modules for Roots of Acyclic Quivers | 0.1112 | 3 | 2011 | queued | 0/5 |  |  |  |
| 622 | 30002048 / OWR-11784-007 | Exceptional-Unit Bounds by Algebraic Degree | 0.1110 | 3 | 2012 | queued | 0/5 |  |  |  |
| 623 | 30002497 / OWR-12866-004 | Irrational Local Maxima of the Fractional-Part Autocorrelation | 0.1105 | 3 | 2014 | queued | 0/5 |  |  |  |
| 624 | 30002508 / OWR-12866-018 | Continuity and Strict Monotonicity of Nyman–Beurling Distances | 0.1105 | 3 | 2014 | queued | 0/5 |  |  |  |
| 625 | 30002526 / OWR-12869-003 | Eliminating Whitney Umbrellas in Projective Group Realization | 0.1105 | 3 | 2014 | queued | 0/5 |  |  |  |
| 626 | 30004994 / OWR-9790354-005 | Entropy and Nondiagonal Asymptotic Pairs | 0.1105 | 3 | 2022 | queued | 0/5 |  |  |  |
| 627 | 30005253 / OWR-11695855-006 | Optimality of Monotonized Asymptotic Risk | 0.1105 | 3 | 2022 | queued | 0/5 |  |  |  |
| 628 | 30006276 / OWR-14299284-004 | Multiplicativity of Tautological Chow Projections | 0.1104 | 3 | 2025 | queued | 0/5 |  |  |  |
| 629 | 30006336 / OWR-14299291-005 | Prismatic Extension of Generic-Point Vanishing | 0.1104 | 3 | 2025 | queued | 0/5 |  |  |  |
| 630 | 30003296 / OWR-15177-013 | Complete Surfaces inside the Genus-Four Moduli Space | 0.1099 | 3 | 2016 | queued | 0/5 |  |  |  |
| 631 | 30003592 / OWR-15586-003 | Polyhedrality of Movable Cycle Cones on Toric Varieties | 0.1096 | 3 | 2017 | queued | 0/5 |  |  |  |
| 632 | 30003644 / OWR-15956-010 | Zero-Free Dirichlet Polynomials on the Unit Line | 0.1096 | 3 | 2017 | queued | 0/5 |  |  |  |
| 633 | 5300088 / AMR-052-0088 | Injectivity radius from the number of generators | 0.1089 | 4 | 1990 | queued | 0/5 |  |  |  |
| 634 | 5900029 / AMR-058-0029 | Finite Total Scalar Curvature and Planarity | 0.1085 | 3 | 1995 | queued | 0/5 |  |  |  |
| 635 | 4700001 / AMR-046-0001 | Low degree rigid systems | 0.1085 | 3 | 2020 | queued | 0/5 |  |  |  |
| 636 | 4700012 / AMR-046-0012 | A class of Hamiltonian systems | 0.1085 | 3 | 2020 | queued | 0/5 |  |  |  |
| 637 | 10400173 / AMR-103-0173 | Problem 9.9 — (N. | 0.1080 | 3 | unknown | queued | 0/5 |  |  |  |
| 638 | 1200023 / AMR-011-0023 | Some Questions — Question 23 | 0.1080 | 3 | unknown | queued | 0/5 |  |  |  |
| 639 | 20000185 / AIM-ALGEBRAIC_GEOMETRY-0185 | Compatibility via the epipolar fiber product and a gcd component law | 0.1080 | 3 | unknown | queued | 0/5 |  |  |  |
| 640 | 20000190 / AIM-ALGEBRAIC_GEOMETRY-0190 | A root-free focal-positivity certificate for a seven-point pencil | 0.1080 | 3 | unknown | queued | 0/5 |  |  |  |
| 641 | 20002720 / AIM-PROBABILITY-0162 | Units, central splitting, and filtration for multivariable boxed convolution | 0.1080 | 3 | unknown | queued | 0/5 |  |  |  |
| 642 | 2639 / KOU-21.130 | Kourovka Notebook Problem 21.130 | 0.1080 | 3 | 2026 | queued | 0/5 |  |  |  |
| 643 | 4200010 / AMR-041-0010 | The good, the bad, and the ugly | 0.1079 | 3 | 2000 | queued | 0/5 |  |  |  |
| 644 | 30004609 / OWR-4990374-015 | Supersolvability of Low-Exponent Free Hyperplane Arrangements | 0.1079 | 3 | 2021 | queued | 0/5 |  |  |  |
| 645 | 30004996 / OWR-9790354-007 | Hyper-Aperiodic Colorings from Aperiodic SFT Colorings | 0.1073 | 3 | 2022 | queued | 0/5 |  |  |  |
| 646 | 6200025 / AMR-061-0025 | Boundaries of Groups and Kleinian Groups — Problem 25 | 0.1073 | 3 | 2005 | queued | 0/5 |  |  |  |
| 647 | 6200083 / AMR-061-0083 | Boundaries of Groups and Kleinian Groups — Problem 83 | 0.1073 | 3 | 2005 | queued | 0/5 |  |  |  |
| 648 | 6200096 / AMR-061-0096 | Boundaries of Groups and Kleinian Groups — Problem 96 | 0.1073 | 3 | 2005 | queued | 0/5 |  |  |  |
| 649 | 5300076 / AMR-052-0076 | Thurston algorithm for power-law lift families | 0.1073 | 3 | 1990 | queued | 0/5 |  |  |  |
| 650 | 5300071 / AMR-052-0071 | Uniform access to roots for relaxed Newton maps | 0.1071 | 3 | 1992 | queued | 0/5 |  |  |  |
| 651 | 30001184 / OWR-3392-012 | Extending Dilated E0-Semigroups Beyond GNS Representations | 0.1067 | 3 | 2009 | queued | 0/5 |  |  |  |
| 652 | 30005479 / OWR-12697711-015 | Equality of Tropical and Matroidal Amoeba-Dimension Formulas | 0.1066 | 3 | 2023 | queued | 0/5 |  |  |  |
| 653 | 4400005 / AMR-043-0005 | Pingree open problems — Ledrappier problem 1 | 0.1065 | 4 | 2010 | queued | 0/5 |  |  |  |
| 654 | 30001988 / OWR-11575-015 | Splitting Sets Under Differential-Transcendental Extensions | 0.1061 | 3 | 2012 | queued | 0/5 |  |  |  |
| 655 | 30000403 / OWR-1188-004 | Optimal Descent Degrees in Reduced Hurwitz Spaces | 0.1055 | 3 | 2006 | queued | 0/5 |  |  |  |
| 656 | 30000492 / OWR-1274-008 | Settled Quadratic Polynomials and Markov Factorization Models | 0.1055 | 3 | 2006 | queued | 0/5 |  |  |  |
| 657 | 30000510 / OWR-1275-010 | Topology of Baby Teichmüller Spaces | 0.1055 | 3 | 2006 | queued | 0/5 |  |  |  |
| 658 | 30000576 / OWR-1323-013 | Chaos of Individual Operators in Chaotic Semigroups | 0.1055 | 3 | 2006 | queued | 0/5 |  |  |  |
| 659 | 30000700 / OWR-1460-004 | IM-Sharing Variants of Theorem H for Entire Functions | 0.1053 | 3 | 2007 | queued | 0/5 |  |  |  |
| 660 | 30000704 / OWR-1460-010 | Boundary Regularity for Complete Conformal Metrics | 0.1053 | 3 | 2007 | queued | 0/5 |  |  |  |
| 661 | 30000930 / OWR-1790-007 | Ext-Algebra Models for Crossingless Matchings | 0.1052 | 3 | 2008 | queued | 0/5 |  |  |  |
| 662 | 30001017 / OWR-2049-004 | Intersection Numbers on First Voronoi Compactifications | 0.1052 | 3 | 2008 | queued | 0/5 |  |  |  |
| 663 | 4000018 / AMR-039-0018 | L2 Bonnet–Myers and dimension | 0.1052 | 3 | 2008 | queued | 0/5 |  |  |  |
| 664 | 30003322 / OWR-15181-014 | Set-Sized Models of Initial Surreal Substructures | 0.1051 | 3 | 2016 | queued | 0/5 |  |  |  |
| 665 | 30001132 / OWR-3384-004 | Admissible Gelfand–Zetlin Faces Representing Smooth Schubert Cycles | 0.1050 | 3 | 2009 | queued | 0/5 |  |  |  |
| 666 | 30001138 / OWR-3385-009 | Linked Skeletons of Convex Four-Polytopes | 0.1050 | 3 | 2009 | queued | 0/5 |  |  |  |
| 667 | 30001155 / OWR-3389-006 | Area-Refined Spectral Gap Bounds for Convex Domains | 0.1050 | 3 | 2009 | queued | 0/5 |  |  |  |
| 668 | 30001222 / OWR-3400-006 | Rigidity Under Stable Equivalence of Quantum Complete Intersections | 0.1050 | 3 | 2009 | queued | 0/5 |  |  |  |
| 669 | 30001397 / OWR-4137-017 | Hausdorff Gauges for Conformal Measures of Elliptic Maps | 0.1050 | 3 | 2009 | queued | 0/5 |  |  |  |
| 670 | 10300062 / AMR-102-0062 | Immersed objects — Question 14.2 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 671 | 10400081 / AMR-103-0081 | Conjecture 4.3 — If every closed incompressible surface in M is parallel to ∂M, then S2,∞(M ) is torsion free. | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 672 | 10900010 / AMR-108-0010 | 3.2 (Agol) — A minimal-Thurston-norm surface from a tree action | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 673 | 20001730 / AIM-GEOMETRY-0068 | Compatibility of Gibbs leaf cocycles for commuting Anosov maps | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 674 | 2302019 / AMR-022-2019 | Research Problems in Function Theory — Problem 2.19 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 675 | 2302042 / AMR-022-2042 | Research Problems in Function Theory — Problem 2.42 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 676 | 2303014 / AMR-022-3014 | Research Problems in Function Theory — Problem 3.14 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 677 | 2303023 / AMR-022-3023 | Research Problems in Function Theory — Problem 3.23 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 678 | 2304029 / AMR-022-4029 | Research Problems in Function Theory — Problem 4.29 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 679 | 2305020 / AMR-022-5020 | Research Problems in Function Theory — Problem 5.20 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 680 | 2305033 / AMR-022-5033 | Research Problems in Function Theory — Problem 5.33 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 681 | 2305044 / AMR-022-5044 | Research Problems in Function Theory — Problem 5.44 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 682 | 2305073 / AMR-022-5073 | Research Problems in Function Theory — Problem 5.73 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 683 | 2306043 / AMR-022-6043 | Research Problems in Function Theory — Problem 6.43 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 684 | 2306046 / AMR-022-6046 | Research Problems in Function Theory — Problem 6.46 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 685 | 2306047 / AMR-022-6047 | Research Problems in Function Theory — Problem 6.47 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 686 | 2306078 / AMR-022-6078 | Research Problems in Function Theory — Problem 6.78 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 687 | 2306086 / AMR-022-6086 | Research Problems in Function Theory — Problem 6.86 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 688 | 2307004 / AMR-022-7004 | Research Problems in Function Theory — Problem 7.4 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 689 | 2307031 / AMR-022-7031 | Research Problems in Function Theory — Problem 7.31 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 690 | 2307045 / AMR-022-7045 | Research Problems in Function Theory — Problem 7.45 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 691 | 2570 / KOU-21.61 | Kourovka Notebook Problem 21.61 | 0.1050 | 2 | 2026 | queued | 0/5 |  |  |  |
| 692 | 2870 / KP-3.72 | Kirby Problem 3.72 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 693 | 2890 / KP-4.14 | Kirby Problem 4.14 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 694 | 2942 / KP-4.66 | Kirby Problem 4.66 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 695 | 2998 / KP-4.122 | Kirby Problem 4.122 | 0.1050 | 3 | unknown | queued | 0/5 |  |  |  |
| 696 | 30001408 / OWR-4199-001 | Invariant Homogeneous Valuations on Convex Bodies | 0.1048 | 3 | 2010 | queued | 0/5 |  |  |  |
| 697 | 30001599 / OWR-4527-003 | Alpha Bounds for Uniform Fat-Point Schemes | 0.1048 | 3 | 2010 | queued | 0/5 |  |  |  |
| 698 | 30001603 / OWR-4527-007 | Jet Spanning by Nef Toric Vector Bundles | 0.1048 | 3 | 2010 | queued | 0/5 |  |  |  |
| 699 | 30001631 / OWR-4535-006 | Curvature Negativity of the Takhtajan–Zograf Metric | 0.1048 | 3 | 2010 | queued | 0/5 |  |  |  |
| 700 | 4400001 / AMR-043-0001 | Pingree open problems — Hochman problem 1 | 0.1048 | 3 | 2010 | queued | 0/5 |  |  |  |
| 701 | 4400008 / AMR-043-0008 | Pingree open problems — Boyle problem 2 | 0.1048 | 3 | 2010 | queued | 0/5 |  |  |  |
| 702 | 6700060 / AMR-066-0060 | Scalar Curvature Question [?64]: Are all extremal convex polyhedraP are mean convexly extremal | 0.1048 | 3 | 2017 | queued | 0/5 |  |  |  |
| 703 | 6700077 / AMR-066-0077 | Scalar Curvature Question [?79]: C0-closeness of the spaces ofC0-metrics withVolumicallyPositiveScalarCurvatures | 0.1048 | 4 | 2017 | queued | 0/5 |  |  |  |
| 704 | 30001658 / OWR-4791-015 | Functional Inequality on the Boolean Cube | 0.1047 | 3 | 2011 | queued | 0/5 |  |  |  |
| 705 | 30001678 / OWR-4792-006 | Smoothness on Products of Perfect Sets | 0.1047 | 3 | 2011 | queued | 0/5 |  |  |  |
| 706 | 30001694 / OWR-4798-010 | Large Inscribed Lattice Squares in Polyomino Boundaries | 0.1047 | 3 | 2011 | queued | 0/5 |  |  |  |
| 707 | 30001860 / OWR-11129-006 | Asymptotic Proportion of $Q$ in Classical Groups | 0.1047 | 3 | 2011 | queued | 0/5 |  |  |  |
| 708 | 30001887 / OWR-11136-013 | Multiple Cover Decomposition Thresholds for Planar Sets | 0.1047 | 3 | 2011 | queued | 0/5 |  |  |  |
| 709 | 30001893 / OWR-11136-024 | Dimension of Convex Partition Spaces in Three Dimensions | 0.1047 | 3 | 2011 | queued | 0/5 |  |  |  |
| 710 | 30003703 / OWR-15987-013 | Equality of the Andreadakis and Representation-Ring Filtrations | 0.1045 | 3 | 2018 | queued | 0/5 |  |  |  |
| 711 | 10000069 / AMR-099-0069 | Distance exponent of random series-parallel graphs | 0.1044 | 3 | 2012 | queued | 0/5 |  |  |  |
| 712 | 30002003 / OWR-11580-009 | Stringy Euler Criteria for Smooth Spherical Varieties | 0.1044 | 3 | 2012 | queued | 0/5 |  |  |  |
| 713 | 30002046 / OWR-11784-003 | Real Fixed Points of the Minkowski Question-Mark Function | 0.1044 | 3 | 2012 | queued | 0/5 |  |  |  |
| 714 | 30002129 / OWR-12007-009 | Refined Slippery Bounds for Positive-Word Rotation Numbers | 0.1044 | 3 | 2012 | queued | 0/5 |  |  |  |
| 715 | 30002167 / OWR-12012-009 | Short Hamiltonian Cycles and Matchings in Convex Bodies | 0.1044 | 3 | 2012 | queued | 0/5 |  |  |  |
| 716 | 30002178 / OWR-12014-013 | Lower Bounds for Sums of Roots of Unity | 0.1044 | 3 | 2012 | queued | 0/5 |  |  |  |
| 717 | 30002180 / OWR-12015-001 | Jet Curvature and the First Chern Class | 0.1044 | 3 | 2012 | queued | 0/5 |  |  |  |
| 718 | 30004222 / OWR-17135-015 | Combinatorial Explanation of the Clasp Conjecture | 0.1041 | 3 | 2019 | queued | 0/5 |  |  |  |
| 719 | 30004279 / OWR-17292-002 | Equivalent Bicommutant Categories from Nonisomorphic Conformal Nets | 0.1041 | 3 | 2019 | queued | 0/5 |  |  |  |
| 720 | 30002692 / OWR-13347-011 | Hyperbolic Conformal Boundaries of Poincaré–Einstein Manifolds | 0.1040 | 3 | 2014 | queued | 0/5 |  |  |  |
| 721 | 30002468 / OWR-12861-019 | Biclique Partition Numbers of Random Graphs | 0.1040 | 3 | 2014 | queued | 0/5 |  |  |  |
| 722 | 30002507 / OWR-12866-017 | A Dirichlet Series with Exactly One Zero | 0.1040 | 3 | 2014 | queued | 0/5 |  |  |  |
| 723 | 30002533 / OWR-12870-003 | New Rational Lyapunov Exponents on Hilbert Modular Surfaces | 0.1040 | 3 | 2014 | queued | 0/5 |  |  |  |
| 724 | 30002653 / OWR-13109-004 | Indeterminacy Locus of the Perfect Cone Prym Map | 0.1040 | 3 | 2014 | queued | 0/5 |  |  |  |
| 725 | 30002711 / OWR-13351-010 | Minimal Coefficient Rings for Cyclic Local Lifts | 0.1040 | 3 | 2014 | queued | 0/5 |  |  |  |
| 726 | 30002753 / OWR-13359-003 | Optimal Geodesic Curvature for Random Transpositions | 0.1040 | 3 | 2014 | queued | 0/5 |  |  |  |
| 727 | 30002829 / OWR-13500-010 | Rationality of Ueno-Type Varieties | 0.1038 | 3 | 2015 | queued | 0/5 |  |  |  |
| 728 | 30002830 / OWR-13500-011 | Birational Modifications Proving Rationality of a Ueno Variety | 0.1038 | 3 | 2015 | queued | 0/5 |  |  |  |
| 729 | 30003070 / OWR-14221-006 | Birational Sequences for Plabic Newton–Okounkov Bodies | 0.1035 | 3 | 2016 | queued | 0/5 |  |  |  |
| 730 | 30003114 / OWR-14603-013 | Exponential Small-Value Bounds for Littlewood Polynomials | 0.1035 | 3 | 2016 | queued | 0/5 |  |  |  |
| 731 | 30003229 / OWR-14754-016 | Stringy Euler Numbers under Mori Flips | 0.1035 | 3 | 2016 | queued | 0/5 |  |  |  |
| 732 | 30003230 / OWR-14754-017 | Stringy Euler Numbers under Divisorial Contractions | 0.1035 | 3 | 2016 | queued | 0/5 |  |  |  |
| 733 | 30003264 / OWR-15173-001 | Third Homology and Pre-Bloch Groups of $S$-Arithmetic $\operatorname{SL}_2$ | 0.1035 | 3 | 2016 | queued | 0/5 |  |  |  |
| 734 | 6600014 / AMR-065-0014 | A. Navas: A Conjecture on Delone Sets BL to Lattices (after P. Alestalo, D.A. Trotsenko and J. V\"ais\"al\"a). — Problem | 0.1035 | 4 | 2016 | queued | 0/5 |  |  |  |
| 735 | 30003417 / OWR-15216-023 | Meager Ideal Equalities at Uncountable Regular Cardinals | 0.1032 | 3 | 2017 | queued | 0/5 |  |  |  |
| 736 | 30003442 / OWR-15219-012 | Largest Roots of Doubly Stochastic Stable Polynomials | 0.1032 | 3 | 2017 | queued | 0/5 |  |  |  |
| 737 | 30003649 / OWR-15957-002 | Rational and Integral Completely Positive Factorizations | 0.1032 | 3 | 2017 | queued | 0/5 |  |  |  |
| 738 | 30003676 / OWR-15962-002 | Sharp Virulence Thresholds for Stationary SIS Infection | 0.1032 | 3 | 2017 | queued | 0/5 |  |  |  |
| 739 | 30003759 / OWR-16157-001 | Uniform Minimal Control Time for Advection–Diffusion | 0.1029 | 3 | 2018 | queued | 0/5 |  |  |  |
| 740 | 30003791 / OWR-16162-003 | Linkage and Vanishing in Kato–Milne Cohomology | 0.1029 | 3 | 2018 | queued | 0/5 |  |  |  |
| 741 | 30003859 / OWR-16169-001 | Rigidity of Hirzebruch–Kummer Coverings | 0.1029 | 3 | 2018 | queued | 0/5 |  |  |  |
| 742 | 30003975 / OWR-16628-004 | Stable Symbolic-Power Containments from a Single Containment | 0.1029 | 3 | 2018 | queued | 0/5 |  |  |  |
| 743 | 30003978 / OWR-16628-010 | Irrational Seshadri Constants from the Nagata Conjecture | 0.1029 | 3 | 2018 | queued | 0/5 |  |  |  |
| 744 | 30005185 / OWR-11101915-009 | Modulo-Four Reduced Khovanov Rank of Ribbon Knots | 0.1026 | 3 | 2022 | queued | 0/5 |  |  |  |
| 745 | 30004169 / OWR-16941-010 | Zariski Descent for the Milnor–Witt Rost–Schmid Complex | 0.1025 | 3 | 2019 | queued | 0/5 |  |  |  |
| 746 | 30004324 / OWR-17296-007 | Characterizing Projective Space by Tangent Bundle Seshadri Constants | 0.1025 | 3 | 2019 | queued | 0/5 |  |  |  |
| 747 | 30004334 / OWR-17296-019 | Bounded Negativity for Root of Unity Blowups | 0.1025 | 3 | 2019 | queued | 0/5 |  |  |  |
| 748 | 7000003 / AMR-069-0003 | Geometry of Curves and Surfaces — Problem 1.3 | 0.1025 | 3 | 2019 | queued | 0/5 |  |  |  |
| 749 | 7000022 / AMR-069-0022 | Geometry of Curves and Surfaces — Problem 5.3 | 0.1025 | 3 | 2019 | queued | 0/5 |  |  |  |
| 750 | 30004425 / OWR-17473-001 | Wall Crossing Between Adjacent Tropical Toric Degenerations | 0.1021 | 3 | 2020 | queued | 0/5 |  |  |  |
| 751 | 30004429 / OWR-17474-001 | Discontinuities of Two-Sided Specifications | 0.1021 | 3 | 2020 | queued | 0/5 |  |  |  |
| 752 | 30004491 / OWR-1703871-006 | Infinite Transverse Actions on Codimension-One Foliations | 0.1021 | 3 | 2020 | queued | 0/5 |  |  |  |
| 753 | 30004494 / OWR-1703871-010 | Boundary-Corrected Ampleness of Extended Hodge Bundles | 0.1021 | 3 | 2020 | queued | 0/5 |  |  |  |
| 754 | 30004541 / OWR-2654828-006 | Extinction Criteria for the Derrida–Retaux Process | 0.1021 | 3 | 2020 | queued | 0/5 |  |  |  |
| 755 | 1200005 / AMR-011-0005 | Some Questions — Question 5 | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 756 | 1929 / EP-100 | Erdős Problem #100 | 0.1020 | 1 | unknown | queued | 0/5 |  |  |  |
| 757 | 20000276 / AIM-ALGEBRAIC_GEOMETRY-0276 | Existence for Noetherian filtrations and monomial graded families | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 758 | 20000809 / AIM-ARITHMETIC_GEOMETRY-0055 | A tangent-weight criterion for rational Hilbert components | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 759 | 20000814 / AIM-ARITHMETIC_GEOMETRY-0060 | A bad-surface and Rao-module reduction for smooth limits of complete intersections | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 760 | 20000817 / AIM-ARITHMETIC_GEOMETRY-0063 | Monomial signatures distinguish components through affine length eight | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 761 | 20000826 / AIM-ARITHMETIC_GEOMETRY-0072 | Connected toric and square-zero classes in three variables | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 762 | 20001757 / AIM-GEOMETRY-0095 | Five-point Riesz phase-transition status and an explicit high-exponent competitor | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 763 | 20002559 / AIM-PROBABILITY-0001 | Local surjectivity and the boundary-at-infinity gap for RBM(4,3) | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 764 | 2200006 / AMR-021-0006 | Problems Around Polynomials — Problem 3 | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 765 | 2235 / EP-655 | Erdős Problem #655 | 0.1020 | 1 | unknown | queued | 0/5 |  |  |  |
| 766 | 2515 / KOU-21.6 | Kourovka Notebook Problem 21.6 | 0.1020 | 2 | 2026 | queued | 0/5 |  |  |  |
| 767 | 2548 / KOU-21.39 | Kourovka Notebook Problem 21.39 | 0.1020 | 2 | 2026 | queued | 0/5 |  |  |  |
| 768 | 2551 / KOU-21.42 | Kourovka Notebook Problem 21.42 | 0.1020 | 2 | 2026 | queued | 0/5 |  |  |  |
| 769 | 2560 / KOU-21.51 | Kourovka Notebook Problem 21.51 | 0.1020 | 2 | 2026 | queued | 0/5 |  |  |  |
| 770 | 2599 / KOU-21.90 | Kourovka Notebook Problem 21.90 | 0.1020 | 2 | 2026 | queued | 0/5 |  |  |  |
| 771 | 2604 / KOU-21.95 | Kourovka Notebook Problem 21.95 | 0.1020 | 2 | 2026 | queued | 0/5 |  |  |  |
| 772 | 2623 / KOU-21.114 | Kourovka Notebook Problem 21.114 | 0.1020 | 2 | 2026 | queued | 0/5 |  |  |  |
| 773 | 2809 / KP-3.11 | Kirby Problem 3.11 | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 774 | 30006556 / OWR-14299905-031 | Two Low-Multiplicity Distances in Planar Point Sets | 0.1020 | 3 | 2026 | queued | 0/5 |  |  |  |
| 775 | 3086 / OPG-37327 | Covering a square with unit squares | 0.1020 | 1 | unknown | queued | 0/5 |  |  |  |
| 776 | 5500031 / AMR-054-0031 | Trapping Light Rays with Segment Mirrors | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 777 | 9500009 / AMR-094-0009 | Do peaks of random labelings repel each other? | 0.1020 | 3 | unknown | queued | 0/5 |  |  |  |
| 778 | 30005356 / OWR-12697685-001 | Definable Endomorphisms of Generic Multiplicative Fields | 0.1019 | 3 | 2023 | queued | 0/5 |  |  |  |
| 779 | 30005664 / OWR-14297742-004 | Aubin–Talenti Optimizers for Critical Dirac Potentials | 0.1019 | 3 | 2023 | queued | 0/5 |  |  |  |
| 780 | 30004594 / OWR-4990373-008 | Survival Versus Percolation Thresholds in the Contact Process | 0.1016 | 3 | 2021 | queued | 0/5 |  |  |  |
| 781 | 30004618 / OWR-4990375-010 | Kodaira Dimension of Odd Minimal Strata | 0.1016 | 3 | 2021 | queued | 0/5 |  |  |  |
| 782 | 30004620 / OWR-4990375-013 | Effective Surface Cone of Principally Polarized Abelian Threefolds | 0.1016 | 3 | 2021 | queued | 0/5 |  |  |  |
| 783 | 30004730 / OWR-8415335-002 | Consistent Conical Bicombings in Metric Spaces | 0.1016 | 3 | 2021 | queued | 0/5 |  |  |  |
| 784 | 30004831 / OWR-8415347-009 | Monoidal Invariance of Hopf-Algebra Cohomological Dimension | 0.1016 | 3 | 2021 | queued | 0/5 |  |  |  |
| 785 | 30004953 / OWR-8415364-011 | Optimal Great-Subsphere Concentration for the Negative-$p$ Aleksandrov Problem | 0.1016 | 3 | 2021 | queued | 0/5 |  |  |  |
| 786 | 30005012 / OWR-9790358-010 | Nonsingularity of Bernstein-Basis Collocation Matrices | 0.1010 | 3 | 2022 | queued | 0/5 |  |  |  |
| 787 | 30005024 / OWR-9790359-005 | Finite-Mean Coding Radius for Finitely Dependent Processes | 0.1010 | 3 | 2022 | queued | 0/5 |  |  |  |
| 788 | 30005026 / OWR-9790359-007 | Simultaneous Spatial and Informational Coding Efficiency | 0.1010 | 3 | 2022 | queued | 0/5 |  |  |  |
| 789 | 30005078 / OWR-10252925-002 | Algorithms for Multigraded Castelnuovo–Mumford Regularity | 0.1010 | 3 | 2022 | queued | 0/5 |  |  |  |
| 790 | 30005114 / OWR-10252930-024 | Spread Bounds for the Random Triangle-Removal Process | 0.1010 | 3 | 2022 | queued | 0/5 |  |  |  |
| 791 | 30005140 / OWR-10252936-003 | Gaussian-Free-Field Maxima on Percolation Clusters | 0.1010 | 3 | 2022 | queued | 0/5 |  |  |  |
| 792 | 30006031 / OWR-14298590-001 | Little Three-Disks Actions on Operadic Homotopy Centers | 0.1010 | 3 | 2024 | queued | 0/5 |  |  |  |
| 793 | 5300080 / AMR-052-0080 | Boundary fixed points in rank-zero Hénon components | 0.1006 | 3 | 1990 | queued | 0/5 |  |  |  |
| 794 | 5300014 / AMR-052-0014 | Non-equivalent compactifications of Blaschke-product space | 0.1004 | 3 | 1992 | queued | 0/5 |  |  |  |
| 795 | 5300056 / AMR-052-0056 | Bounded Jacobian cocycles and absolute continuity | 0.1004 | 3 | 1992 | queued | 0/5 |  |  |  |
| 796 | 5300062 / AMR-052-0062 | Smoothness of exponential-family parameter hairs | 0.1004 | 3 | 1992 | queued | 0/5 |  |  |  |
| 797 | 30005418 / OWR-12697689-014 | Koszulness from the Kähler Package | 0.1003 | 3 | 2023 | queued | 0/5 |  |  |  |
| 798 | 30005453 / OWR-12697708-006 | Unique Equilibria for Subcritical Reinforcement on Infinite Graphs | 0.1003 | 3 | 2023 | queued | 0/5 |  |  |  |
| 799 | 30005519 / OWR-13750332-001 | Real Subspaces in Zeros of Elementary Symmetric Polynomials | 0.1003 | 3 | 2023 | queued | 0/5 |  |  |  |
| 800 | 30005613 / OWR-14297736-021 | Dense Pure Point Spectrum on Quasi-Conical Domains | 0.1003 | 3 | 2023 | queued | 0/5 |  |  |  |
| 801 | 30005755 / OWR-14298157-005 | Canonical Decomposition Cones and TF Equivalence | 0.0994 | 3 | 2024 | queued | 0/5 |  |  |  |
| 802 | 30005902 / OWR-14298370-002 | Vanishing Lie Brackets for Non-Quasitriangular Hopf Algebras | 0.0994 | 3 | 2024 | queued | 0/5 |  |  |  |
| 803 | 30005995 / OWR-14298587-010 | Continuity of Gradient Distance for Monotone Equations | 0.0994 | 3 | 2024 | queued | 0/5 |  |  |  |
| 804 | 30006060 / OWR-14298592-014 | Concordance of an Explicit Pair of Positive Three-Braid Knots | 0.0994 | 3 | 2024 | queued | 0/5 |  |  |  |
| 805 | 30000120 / OWR-744-003 | Chern-Class Generators for Wonderful Compactifications | 0.0992 | 3 | 2004 | queued | 0/5 |  |  |  |
| 806 | 30000263 / OWR-1050-014 | Discrete Interaction-Matrix Inequalities in Three Dimensions | 0.0990 | 3 | 2005 | queued | 0/5 |  |  |  |
| 807 | 6200010 / AMR-061-0010 | Boundaries of Groups and Kleinian Groups — Problem 10 | 0.0990 | 3 | 2005 | queued | 0/5 |  |  |  |
| 808 | 6200014 / AMR-061-0014 | Boundaries of Groups and Kleinian Groups — Problem 14 | 0.0990 | 3 | 2005 | queued | 0/5 |  |  |  |
| 809 | 6200022 / AMR-061-0022 | Boundaries of Groups and Kleinian Groups — Problem 22 | 0.0990 | 3 | 2005 | queued | 0/5 |  |  |  |
| 810 | 6200061 / AMR-061-0061 | Boundaries of Groups and Kleinian Groups — Problem 61 | 0.0990 | 3 | 2005 | queued | 0/5 |  |  |  |
| 811 | 30000432 / OWR-1194-001 | Equal-Area Drawings of Plane Triangulations | 0.0989 | 3 | 2006 | queued | 0/5 |  |  |  |
| 812 | 30000433 / OWR-1194-002 | Five-or-Six Edge-Degree Triangulations of Three-Manifolds | 0.0989 | 3 | 2006 | queued | 0/5 |  |  |  |
| 813 | 30000573 / OWR-1323-010 | Chaotic Operators on Nuclear Fréchet Spaces | 0.0989 | 3 | 2006 | queued | 0/5 |  |  |  |
| 814 | 30000638 / OWR-1394-015 | Volume Bounds for Symmetric Lattice Polytopes | 0.0989 | 3 | 2006 | queued | 0/5 |  |  |  |
| 815 | 30000789 / OWR-1588-003 | Sharp Dimension Threshold for Ricci-Flow Curvature Conditions | 0.0988 | 3 | 2007 | queued | 0/5 |  |  |  |
| 816 | 30000801 / OWR-1591-003 | Strong Quantization for Fourth-Order Navier Problems | 0.0988 | 3 | 2007 | queued | 0/5 |  |  |  |
| 817 | 30001006 / OWR-2045-003 | Sharp Ricci-Flow-Invariant Curvature Cones | 0.0986 | 3 | 2008 | queued | 0/5 |  |  |  |
| 818 | 30001054 / OWR-2090-003 | Realizability of Allowable Double-Permutation Sequences | 0.0986 | 3 | 2008 | queued | 0/5 |  |  |  |
| 819 | 30001066 / OWR-2090-019 | Helly Numbers for Isolated Line Transversals | 0.0986 | 3 | 2008 | queued | 0/5 |  |  |  |
| 820 | 4600024 / AMR-045-0024 | Extension of a block code II | 0.0986 | 4 | 2008 | queued | 0/5 |  |  |  |
| 821 | 30001168 / OWR-3389-021 | Weighted Yamabe Heat-Trace Comparison | 0.0985 | 3 | 2009 | queued | 0/5 |  |  |  |
| 822 | 30001169 / OWR-3389-022 | Monotonicity of Weighted Yamabe Heat Traces | 0.0985 | 3 | 2009 | queued | 0/5 |  |  |  |
| 823 | 30001176 / OWR-3392-002 | Factorizations from Minimal Exchangeable Random Sequences | 0.0985 | 3 | 2009 | queued | 0/5 |  |  |  |
| 824 | 30001223 / OWR-3400-007 | Simple Tops of Young Modules | 0.0985 | 3 | 2009 | queued | 0/5 |  |  |  |
| 825 | 30001336 / OWR-4084-010 | Rooted-Tree Expansions of Renormalized Two-Point Functions | 0.0985 | 3 | 2009 | queued | 0/5 |  |  |  |
| 826 | 30001460 / OWR-4332-001 | Geometric Quotients of K-Sheets | 0.0983 | 3 | 2010 | queued | 0/5 |  |  |  |
| 827 | 30001478 / OWR-4335-003 | Prime Ideals and Coordinate-Ring Maps of $R(\alpha,\beta)$ | 0.0983 | 3 | 2010 | queued | 0/5 |  |  |  |
| 828 | 30001522 / OWR-4413-005 | Persistent Gaps between Free $p$-Rank and Toral Rank | 0.0983 | 3 | 2010 | queued | 0/5 |  |  |  |
| 829 | 30006162 / OWR-14299082-004 | Generic Point Property for Exceptional Surface Homeomorphisms | 0.0982 | 3 | 2025 | queued | 0/5 |  |  |  |
| 830 | 30006166 / OWR-14299082-012 | Hyperfiniteness of Generic Wreath-Product Actions | 0.0982 | 3 | 2025 | queued | 0/5 |  |  |  |
| 831 | 30006464 / OWR-14299577-017 | Short Coefficient Detection of Cusp-Form Norms | 0.0982 | 3 | 2025 | queued | 0/5 |  |  |  |
| 832 | 30001669 / OWR-4791-028 | Short Cycles in Highly Dominating Digraphs | 0.0981 | 3 | 2011 | queued | 0/5 |  |  |  |
| 833 | 30001702 / OWR-4798-027 | Minimal Facets in Triangulated Tori | 0.0981 | 3 | 2011 | queued | 0/5 |  |  |  |
| 834 | 30001707 / OWR-4799-003 | Multiplicity-Free Quantization and Orbit Counts | 0.0981 | 3 | 2011 | queued | 0/5 |  |  |  |
| 835 | 30001737 / OWR-4804-005 | The Converse Unitary Distinction Criterion | 0.0981 | 3 | 2011 | queued | 0/5 |  |  |  |
| 836 | 30001913 / OWR-11139-006 | Extremality of Hodge–Tate Laurent Polynomials | 0.0981 | 3 | 2011 | queued | 0/5 |  |  |  |
| 837 | 30002042 / OWR-11783-009 | Degrees and Finiteness of Stringy $E$-Polynomials | 0.0979 | 3 | 2012 | queued | 0/5 |  |  |  |
| 838 | 30002054 / OWR-11786-002 | Additivity of Triangulation Complexity under Connected Sum | 0.0979 | 3 | 2012 | queued | 0/5 |  |  |  |
| 839 | 30002218 / OWR-12175-007 | Perturbation Stability of Jiang–Su Absorption for $C^*$-Algebras | 0.0979 | 3 | 2012 | queued | 0/5 |  |  |  |
| 840 | 30002288 / OWR-12336-004 | Representation and Limits of Fractional Infinity Eigenfunctions | 0.0977 | 3 | 2013 | queued | 0/5 |  |  |  |
| 841 | 30002364 / OWR-12495-004 | Lefschetz-Class Properties Under CM Reduction | 0.0977 | 3 | 2013 | queued | 0/5 |  |  |  |
| 842 | 30002439 / OWR-12725-016 | Height Counts for Closed Projective Immersions | 0.0977 | 3 | 2013 | queued | 0/5 |  |  |  |
| 843 | 30002618 / OWR-13102-007 | Monodromy Exactness for Isocrystals on Semistable Curves | 0.0975 | 3 | 2014 | queued | 0/5 |  |  |  |
| 844 | 10300026 / AMR-102-0026 | Leaf spaces and transverse structures — Question 8.3 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 845 | 10300029 / AMR-102-0029 | Leaf spaces and transverse structures — Question 8.6 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 846 | 10400124 / AMR-103-0124 | Conjecture 7.9 — (Topological interpretations of the dj ’s) Let Mj be the union of components of the moduli space of flat connections… | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 847 | 10400215 / AMR-103-0215 | Conjecture 12.10 — (D. | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 848 | 11100062 / AMR-110-0062 | Unstable homotopy theory 3 — Suppose X is a simply connected finite complex. | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 849 | 20001938 / AIM-GEOMETRY-0276 | Regular-stratum curvature-jet tests for projective metrizability | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 850 | 20001955 / AIM-GEOMETRY-0293 | Finite-sector additive nonabelian orbifold Kirwan surjectivity | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 851 | 20002051 / AIM-GEOMETRY-0389 | Higher-even-dimensional Polyakov formulae | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 852 | 20002320 / AIM-LOGIC-0096 | Effective isolation and descent to the prime model | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 853 | 2303021 / AMR-022-3021 | Research Problems in Function Theory — Problem 3.21 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 854 | 2303030 / AMR-022-3030 | Research Problems in Function Theory — Problem 3.30 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 855 | 2305007 / AMR-022-5007 | Research Problems in Function Theory — Problem 5.7 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 856 | 2307028 / AMR-022-7028 | Research Problems in Function Theory — Problem 7.28 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 857 | 2307042 / AMR-022-7042 | Research Problems in Function Theory — Problem 7.42 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 858 | 2780 / KP-2.32 | Kirby Problem 2.32 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 859 | 2781 / KP-2.33 | Kirby Problem 2.33 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 860 | 2844 / KP-3.46 | Kirby Problem 3.46 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 861 | 2997 / KP-4.121 | Kirby Problem 4.121 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 862 | 3015 / KP-5.8 | Kirby Problem 5.8 | 0.0975 | 3 | unknown | queued | 0/5 |  |  |  |
| 863 | 30002888 / OWR-13682-010 | Forgetful Functors for Mixed Perverse Sheaves | 0.0973 | 3 | 2015 | queued | 0/5 |  |  |  |
| 864 | 30002904 / OWR-13687-003 | Generic Infinite Index Subgroups of Integral Special Linear Groups | 0.0973 | 3 | 2015 | queued | 0/5 |  |  |  |
| 865 | 30003060 / OWR-14218-004 | Koszulness from Vanishing Higher Koszul Homology | 0.0970 | 3 | 2016 | queued | 0/5 |  |  |  |
| 866 | 30003245 / OWR-15170-007 | Bounded-House Finiteness for Totally Real Algebraic Integers | 0.0970 | 3 | 2016 | queued | 0/5 |  |  |  |
| 867 | 30003521 / OWR-15437-003 | NLS Approximation on Periodic Nonlinear Wave Graphs | 0.0967 | 3 | 2017 | queued | 0/5 |  |  |  |
| 868 | 30003570 / OWR-15582-004 | Heegner Divisors and the Pseudo-Effective Cone | 0.0967 | 3 | 2017 | queued | 0/5 |  |  |  |
| 869 | 30003596 / OWR-15586-007 | Polyhedral Global Newton–Okounkov Bodies for Mori Dream Spaces | 0.0967 | 3 | 2017 | queued | 0/5 |  |  |  |
| 870 | 30003711 / OWR-15987-022 | Schwarz Genus of the Flex-Point Cover | 0.0964 | 3 | 2018 | queued | 0/5 |  |  |  |
| 871 | 30003771 / OWR-16158-014 | Nonabelian Torsors and Essentially Finite Parabolic Bundles | 0.0964 | 3 | 2018 | queued | 0/5 |  |  |  |
| 872 | 30003800 / OWR-16162-015 | Unramified Cohomology of Mixed-Type Classifying Spaces | 0.0964 | 3 | 2018 | queued | 0/5 |  |  |  |
| 873 | 30003902 / OWR-16408-015 | Virtual Cohomological Dimension of Surface Automorphism Groups | 0.0964 | 3 | 2018 | queued | 0/5 |  |  |  |
| 874 | 10000034 / AMR-099-0034 | Half-plane percolation for invariant FKG processes | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 875 | 10000036 / AMR-099-0036 | Invariant finite-energy percolation with internal threshold one | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 876 | 10400128 / AMR-103-0128 | Problem 7.13 — (H. | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 877 | 10400135 / AMR-103-0135 | Problem 7.20 — (S. | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 878 | 11000109 / AMR-109-0109 | Problem 2.4 — Let Γ be a subgroup of finite index in the mapping class group Mod1,2 and let φ: Γ → Γ be an automorphism. | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 879 | 136 / GREEN-048 | Balanced Ham Sandwich Line | 0.0960 | 1 | unknown | queued | 0/5 |  |  |  |
| 880 | 1392 / GRAPH-005 | Graph Coloring Game Monotonicity | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 881 | 1500006 / AMR-014-0006 | Algebraic Stories — The $k$-rank of monomials | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 882 | 1500024 / AMR-014-0024 | Algebraic Stories — Exterior algebras | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 883 | 1917 / EP-81 | Erdős Problem #81 | 0.0960 | 1 | unknown | queued | 0/5 |  |  |  |
| 884 | 20000280 / AIM-ALGEBRAIC_GEOMETRY-0280 | An extremal bracket, a Segre correction, and a cubic-scroll family | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 885 | 20000363 / AIM-ALGEBRAIC_NUMBER_THEORY-0015 | Density degrees under finite extension | 0.0960 | 4 | unknown | queued | 0/5 |  |  |  |
| 886 | 20000451 / AIM-ALGEBRAIC_NUMBER_THEORY-0103 | Rational descent obstructions for geometric elliptic powers in hyperelliptic Jacobians | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 887 | 20000461 / AIM-ALGEBRAIC_NUMBER_THEORY-0113 | A local-defect lower bound for the 3-Selmer group over cyclic cubic fields | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 888 | 20000702 / AIM-ANALYTIC_NUMBER_THEORY-0066 | Signed height weights that extract one moment coefficient | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 889 | 20001272 / AIM-CONVEX_GEOMETRY-0004 | Canonical homothety fields and rigidity of centered sections | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 890 | 20001283 / AIM-CONVEX_GEOMETRY-0015 | Exact radial gluing and symmetric star-body rigidity | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 891 | 20001436 / AIM-DYNAMICAL_SYSTEMS-0094 | A tame positive-characteristic form of Milnor's four-point criterion | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 892 | 20001438 / AIM-DYNAMICAL_SYSTEMS-0096 | Low-period multiplier-locus conspiracies | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 893 | 20002470 / AIM-PDES-0082 | A dense analytic rational skeleton for an analytic Aubry foliation | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 894 | 20002569 / AIM-PROBABILITY-0011 | A full-rank tropical RBM certificate for four visible units | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 895 | 20002573 / AIM-PROBABILITY-0015 | Exact dropout decomposition for RBM likelihoods and an ordinary-RBM no-go example | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 896 | 20002585 / AIM-PROBABILITY-0027 | Finite-N boundary and routing-miss Stein comparisons for JSQ approximations | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 897 | 20002597 / AIM-PROBABILITY-0039 | Dyck random transpositions and a sharp edgewise comparison obstruction | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 898 | 2193 / EP-584 | Erdős Problem #584 | 0.0960 | 1 | unknown | queued | 0/5 |  |  |  |
| 899 | 2200007 / AMR-021-0007 | Problems Around Polynomials — Conjecture 4 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 900 | 2228 / EP-642 | Erdős Problem #642 | 0.0960 | 1 | unknown | queued | 0/5 |  |  |  |
| 901 | 2303033 / AMR-022-3033 | Research Problems in Function Theory — Problem 3.33 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 902 | 2308014 / AMR-022-8014 | Research Problems in Function Theory — Problem 8.14 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 903 | 2315 / EP-810 | Erdős Problem #810 | 0.0960 | 1 | unknown | queued | 0/5 |  |  |  |
| 904 | 2487 / EP-1097 | Erdős Problem #1097 | 0.0960 | 1 | unknown | queued | 0/5 |  |  |  |
| 905 | 2724 / KP-1.65 | Kirby Problem 1.65 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 906 | 2731 / KP-1.72 | Kirby Problem 1.72 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 907 | 2733 / KP-1.74 | Kirby Problem 1.74 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 908 | 2756 / KP-2.8 | Kirby Problem 2.8 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 909 | 2769 / KP-2.21 | Kirby Problem 2.21 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 910 | 2811 / KP-3.13 | Kirby Problem 3.13 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 911 | 2816 / KP-3.18 | Kirby Problem 3.18 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 912 | 2832 / KP-3.34 | Kirby Problem 3.34 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 913 | 2839 / KP-3.41 | Kirby Problem 3.41 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 914 | 2851 / KP-3.53 | Kirby Problem 3.53 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 915 | 2868 / KP-3.70 | Kirby Problem 3.70 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 916 | 2875 / KP-3.77 | Kirby Problem 3.77 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 917 | 2894 / KP-4.18 | Kirby Problem 4.18 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 918 | 2910 / KP-4.34 | Kirby Problem 4.34 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 919 | 2928 / KP-4.52 | Kirby Problem 4.52 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 920 | 2931 / KP-4.55 | Kirby Problem 4.55 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 921 | 2950 / KP-4.74 | Kirby Problem 4.74 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 922 | 2986 / KP-4.110 | Kirby Problem 4.110 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 923 | 2999 / KP-4.123 | Kirby Problem 4.123 | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 924 | 30006628 / OWR-14299911-031 | Property T for Random Free-Product Quotients above One-Third Density | 0.0960 | 3 | 2026 | queued | 0/5 |  |  |  |
| 925 | 3075 / OPG-605 | Average diameter of a bounded cell of a simple arrangement | 0.0960 | 1 | unknown | queued | 0/5 |  |  |  |
| 926 | 3081 / OPG-2435 | Monochromatic empty triangles | 0.0960 | 2 | unknown | queued | 0/5 |  |  |  |
| 927 | 3800003 / AMR-037-0003 | Degenerate facets of polytopes | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 928 | 3900015 / AMR-038-0015 | Packing reciprocal rectangles in a square | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 929 | 5500072 / AMR-054-0072 | Polyhedron with Regular Pentagon Faces | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 930 | 600004 / AMR-005-0004 | Baker's Dozen — Periodic hyperbolic outer billiards | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 931 | 600011 / AMR-005-0011 | Baker's Dozen — Convex tangent-segment iteration | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 932 | 8500009 / AMR-084-0009 | Existence of a strong rational Diophantine quadruple | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 933 | 9600004 / AMR-095-0004 | Negative association for asymmetric exclusion | 0.0960 | 4 | unknown | queued | 0/5 |  |  |  |
| 934 | 9700026 / AMR-096-0026 | Stability dichotomy for the associated city dynamical system | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 935 | 9700033 / AMR-096-0033 | Unbounded component uniqueness in a SIRSN | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 936 | 9700036 / AMR-096-0036 | SIRSN subnetworks cannot be trees | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 937 | 9700042 / AMR-096-0042 | Near-one asymptotics for oriented-percolation flow | 0.0960 | 3 | unknown | queued | 0/5 |  |  |  |
| 938 | 9900008 / AMR-098-0008 | Mass-stationarity of diffuse random measures via allocations | 0.0960 | 4 | unknown | queued | 0/5 |  |  |  |
| 939 | 9900009 / AMR-098-0009 | Markovian-kernel characterization of mass-stationarity | 0.0960 | 4 | unknown | queued | 0/5 |  |  |  |
| 940 | 30004549 / OWR-2654829-012 | Generic Vanishing of Anti-Invariant Cohomology in Dimension Four | 0.0957 | 3 | 2020 | queued | 0/5 |  |  |  |
| 941 | 4700011 / AMR-046-0011 | Periodic rational difference equations | 0.0957 | 3 | 2020 | queued | 0/5 |  |  |  |
| 942 | 30004633 / OWR-4990379-003 | Lagrangian Schemes for Irregular Porous-Medium Solutions | 0.0952 | 3 | 2021 | queued | 0/5 |  |  |  |
| 943 | 30004711 / OWR-7155449-015 | Completed $\Theta$-Twisted Volumes of Bordered-Curve Moduli | 0.0952 | 3 | 2021 | queued | 0/5 |  |  |  |
| 944 | 30004818 / OWR-8415345-008 | Genus-Reducing Local-Knot Concordance in Orientable Three-Manifolds | 0.0952 | 3 | 2021 | queued | 0/5 |  |  |  |
| 945 | 30004938 / OWR-8415362-003 | Polyhedrality of Totally Nonnegative Critical Varieties | 0.0952 | 3 | 2021 | queued | 0/5 |  |  |  |
| 946 | 30005030 / OWR-9790360-001 | Spatial Regularity Versus Time Integrability for Fractional SDEs | 0.0947 | 3 | 2022 | queued | 0/5 |  |  |  |
| 947 | 30005079 / OWR-10252925-004 | Nondivisorial Valuations in Explicit Fano Degenerations | 0.0947 | 3 | 2022 | queued | 0/5 |  |  |  |
| 948 | 30005171 / OWR-11101913-005 | Stable Limits of Smooth Plane Curves | 0.0947 | 3 | 2022 | queued | 0/5 |  |  |  |
| 949 | 30005209 / OWR-11101918-009 | Stable Wulff Shapes for Crystalline Nonlocal Energies | 0.0947 | 3 | 2022 | queued | 0/5 |  |  |  |
| 950 | 30005353 / OWR-12697684-032 | Homotopical versus Homological Cycle-Filling Complexity | 0.0941 | 3 | 2023 | queued | 0/5 |  |  |  |
| 951 | 30005481 / OWR-12697711-017 | Extendability of Operators Associated with Hook-Shaped Polynomials | 0.0941 | 3 | 2023 | queued | 0/5 |  |  |  |
| 952 | 30005600 / OWR-14297736-006 | Conformal Spinorial Eigenvalue Infimum on the Torus | 0.0941 | 3 | 2023 | queued | 0/5 |  |  |  |
| 953 | 30005737 / OWR-14298013-001 | Post-Lie Structures with Semisimple Target | 0.0941 | 3 | 2023 | queued | 0/5 |  |  |  |
| 954 | 5300048 / AMR-052-0048 | Accessibility of basin-boundary periodic points | 0.0937 | 3 | 1992 | queued | 0/5 |  |  |  |
| 955 | 5900026 / AMR-058-0026 | Soap Film on a Regular Octahedral Frame | 0.0935 | 3 | 1995 | queued | 0/5 |  |  |  |
| 956 | 30005926 / OWR-14298373-004 | Distance and Diameter Constants of High-Genus Triangulations | 0.0932 | 3 | 2024 | queued | 0/5 |  |  |  |
| 957 | 30005960 / OWR-14298581-007 | Stability Conditions from Surface Degenerations | 0.0932 | 3 | 2024 | queued | 0/5 |  |  |  |
| 958 | 30005990 / OWR-14298587-002 | Boundary Frequency Gap for Optimal Partitions | 0.0932 | 3 | 2024 | queued | 0/5 |  |  |  |
| 959 | 30005994 / OWR-14298587-009 | Gradient-Constrained Ginzburg-Landau Minimizers | 0.0932 | 3 | 2024 | queued | 0/5 |  |  |  |
| 960 | 30006086 / OWR-14298797-002 | Algebraic Generators and Equivalence of Loop Invariants | 0.0932 | 3 | 2024 | queued | 0/5 |  |  |  |
| 961 | 30006099 / OWR-14298803-003 | Data-Driven Estimation of Maximal Time Averages | 0.0932 | 3 | 2024 | queued | 0/5 |  |  |  |
| 962 | 30000347 / OWR-1111-001 | Three-Terminal Distance-Interdiction Complexity | 0.0924 | 3 | 2005 | queued | 0/5 |  |  |  |
| 963 | 30000717 / OWR-1465-011 | Gradient-Tentacle Certificates for Polynomial Nonnegativity | 0.0922 | 3 | 2007 | queued | 0/5 |  |  |  |
| 964 | 30000853 / OWR-1730-006 | Boundary-Intersection Vanishing on Abelian-Variety Moduli | 0.0922 | 3 | 2007 | queued | 0/5 |  |  |  |
| 965 | 30000962 / OWR-1967-011 | Recursive Determination of Quantum Knot Invariants | 0.0920 | 3 | 2008 | queued | 0/5 |  |  |  |
| 966 | 30001052 / OWR-2089-013 | Functorial Maps Between p-Local Finite-Group Classifying Spaces | 0.0920 | 3 | 2008 | queued | 0/5 |  |  |  |
| 967 | 30006191 / OWR-14299085-005 | Counterexamples to Strongly Continuous Many-Fermion Dynamics | 0.0920 | 3 | 2025 | queued | 0/5 |  |  |  |
| 968 | 30006223 / OWR-14299092-002 | Expander Degree Under Boundary Connected Sums | 0.0920 | 3 | 2025 | queued | 0/5 |  |  |  |
| 969 | 30006419 / OWR-14299521-012 | Infinitesimal Quasiconformality of Harmonic Spheres | 0.0920 | 3 | 2025 | queued | 0/5 |  |  |  |
| 970 | 30001260 / OWR-3477-004 | Rank-One-Isotropy Actions of $S_{5}$ on Spheres | 0.0919 | 3 | 2009 | queued | 0/5 |  |  |  |
| 971 | 30001278 / OWR-3480-009 | Sharper Ramification Bounds for Local Galois Representations | 0.0919 | 3 | 2009 | queued | 0/5 |  |  |  |
| 972 | 30001285 / OWR-3481-002 | Comparison Maps in Motivic Cohomology of Central Simple Algebras | 0.0919 | 3 | 2009 | queued | 0/5 |  |  |  |
| 973 | 30001288 / OWR-3481-005 | Motivic Albanese and Walker Abel–Jacobi Targets | 0.0919 | 3 | 2009 | queued | 0/5 |  |  |  |
| 974 | 30001345 / OWR-4086-003 | Semicontinuity of the $M$-Number in Plane-Curve Deformations | 0.0919 | 3 | 2009 | queued | 0/5 |  |  |  |
| 975 | 30001405 / OWR-4196-003 | Homotopy Groups of Definable Quotients | 0.0917 | 3 | 2010 | queued | 0/5 |  |  |  |
| 976 | 30001518 / OWR-4412-008 | Existence of Perfect Billiard Retroreflectors | 0.0917 | 3 | 2010 | queued | 0/5 |  |  |  |
| 977 | 30001525 / OWR-4413-009 | Integral Skyline Bases for Symmetric-Group Cohomology | 0.0917 | 3 | 2010 | queued | 0/5 |  |  |  |
| 978 | 30001591 / OWR-4429-002 | Borderline Soliton–Potential Interactions | 0.0917 | 3 | 2010 | queued | 0/5 |  |  |  |
| 979 | 30001738 / OWR-4804-006 | Multiplicity Formulas for Galois-Invariant Induced Representations | 0.0916 | 3 | 2011 | queued | 0/5 |  |  |  |
| 980 | 30001810 / OWR-5158-010 | Ordinary Versus Immersive Simplicial Volume | 0.0916 | 3 | 2011 | queued | 0/5 |  |  |  |
| 981 | 30001840 / OWR-11127-008 | Galois Images in Genus-Two Real-Multiplication Families | 0.0916 | 3 | 2011 | queued | 0/5 |  |  |  |
| 982 | 30001917 / OWR-11139-010 | Normality of Varieties of Minimal Rational Tangents | 0.0916 | 3 | 2011 | queued | 0/5 |  |  |  |
| 983 | 6000001 / AMR-059-0001 | Realizing Statistical Manifolds in Dually Flat Manifolds | 0.0915 | 3 | 1998 | queued | 0/5 |  |  |  |
| 984 | 30002343 / OWR-12490-003 | Optimal Pluricanonical Bounds for Stable Log Surfaces | 0.0912 | 3 | 2013 | queued | 0/5 |  |  |  |
| 985 | 30002395 / OWR-12591-005 | Dini Spaces as Primitive Spectra of Amenable $C^*$-Algebras | 0.0912 | 3 | 2013 | queued | 0/5 |  |  |  |
| 986 | 30002495 / OWR-12866-002 | Real-Variable Proof of the Nyman Criterion | 0.0910 | 3 | 2014 | queued | 0/5 |  |  |  |
| 987 | 30002555 / OWR-12875-003 | Veech Groups with Prescribed End Spaces | 0.0910 | 3 | 2014 | queued | 0/5 |  |  |  |
| 988 | 10000051 / AMR-099-0051 | Crossings in random square tilings | 0.0908 | 3 | 2015 | queued | 0/5 |  |  |  |
| 989 | 2800903 / AMR-027-0903 | 10 Lectures and 42 Open Problems — Tightness of k-median LP | 0.0908 | 3 | 2015 | queued | 0/5 |  |  |  |
| 990 | 30002760 / OWR-13487-001 | Optimal Adaptive Approximation of Transport-Dominated Equations | 0.0908 | 3 | 2015 | queued | 0/5 |  |  |  |
| 991 | 30002842 / OWR-13673-012 | Finiteness of Automorphism Groups of Rational Vertex Operator Algebras | 0.0908 | 3 | 2015 | queued | 0/5 |  |  |  |
| 992 | 30003081 / OWR-14222-009 | Higher-Dimensional Theory of Unexpected Curves | 0.0905 | 3 | 2016 | queued | 0/5 |  |  |  |
| 993 | 30003116 / OWR-14603-015 | Quantitative Entropy of Rational Multiplicative Orbits | 0.0905 | 3 | 2016 | queued | 0/5 |  |  |  |
| 994 | 30003140 / OWR-14605-002 | Paramodularity of Antisymmetric Borcherds Products | 0.0905 | 3 | 2016 | queued | 0/5 |  |  |  |
| 995 | 30003235 / OWR-15169-009 | Weighted Bad Approximation on Affine Lines | 0.0905 | 3 | 2016 | queued | 0/5 |  |  |  |
| 996 | 30003279 / OWR-15174-012 | Minimal Separations Among Lattice Points on Circles | 0.0905 | 3 | 2016 | queued | 0/5 |  |  |  |
| 997 | 30003298 / OWR-15177-016 | Infinite Generation in Mapping-Class-Group Cohomology | 0.0905 | 3 | 2016 | queued | 0/5 |  |  |  |
| 998 | 30003467 / OWR-15427-009 | Proper Three-Colorings for Pseudo-Disk Arrangements | 0.0903 | 3 | 2017 | queued | 0/5 |  |  |  |
| 999 | 30003471 / OWR-15427-013 | Dihedral Angle Comparison for Combinatorially Equivalent Polytopes | 0.0903 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1000 | 30003533 / OWR-15576-002 | High-Frequency Coercivity on Nonconvex Nontrapping Domains | 0.0903 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1001 | 30003536 / OWR-15577-004 | Maximum Principle for Intermediate Riesz Kernels | 0.0903 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1002 | 30003634 / OWR-15955-011 | Derived Pure Braid Groups in the Solvable Filtration | 0.0903 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1003 | 10300008 / AMR-102-0008 | Minimal surfaces — Question 4.2 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1004 | 10300011 / AMR-102-0011 | Sublaminations and superlaminations — Question 6.1 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1005 | 10300034 / AMR-102-0034 | Classical 3-manifold theory — Question 9.1 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1006 | 10300037 / AMR-102-0037 | Classical 3-manifold theory — Question 9.4 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1007 | 10300039 / AMR-102-0039 | Hyperbolic geometry — Question 10.1 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1008 | 10300043 / AMR-102-0043 | Hyperbolic geometry — Question 10.5 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1009 | 10400013 / AMR-103-0013 | Problem 1.13 — (A. | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1010 | 10400145 / AMR-103-0145 | Conjecture 7.30 — (K. | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1011 | 10800003 / AMR-107-0003 | Problem 1C — Are there more refined restrictions to the collision of critical values? | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1012 | 11000112 / AMR-109-0112 | Problem 2.7 — Suppose that ta1ta2··· tan = 1 in Modg, where n≥ 1. | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1013 | 11000156 / AMR-109-0156 | Question 2.5 — Given two factorizations of the boundary twist δ as a product of positive Dehn twists along nonseparating curves in M… | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1014 | 11300004 / AMR-112-0004 | Quadrisecants of wild knots | 0.0900 | 4 | unknown | queued | 0/5 |  |  |  |
| 1015 | 1430 / GRAPH-043 | Word-Representable Graphs: Letter Copies Bound | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1016 | 1900002 / AMR-018-0002 | Geometry of Continued Fractions — Integer trigonometry and IKEA problem | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1017 | 1919 / EP-84 | Erdős Problem #84 | 0.0900 | 1 | unknown | queued | 0/5 |  |  |  |
| 1018 | 20000081 / AIM-ALGEBRAIC_GEOMETRY-0081 | Adjacent-power compression and gap states for nested full twists | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1019 | 20000093 / AIM-ALGEBRAIC_GEOMETRY-0093 | A complete rank-two central reconstruction and a higher-rank extension obstruction | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1020 | 20000316 / AIM-ALGEBRAIC_GEOMETRY-0316 | Frobenius contraction and a log-canonical non-F-pure stress test for the symbolic cube | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1021 | 20000610 / AIM-ANALYSIS-0142 | A three-nonzero-root theorem for Fisk's 3x3 Toeplitz-minor transform | 0.0900 | 4 | unknown | queued | 0/5 |  |  |  |
| 1022 | 20000640 / AIM-ANALYTIC_NUMBER_THEORY-0004 | Exact-conductor projectors as the finite bridge from trivial delta to automorphic kernels | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1023 | 20000704 / AIM-ANALYTIC_NUMBER_THEORY-0068 | Interior-frequency isolation of the genuine zeta triple term | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1024 | 20001437 / AIM-DYNAMICAL_SYSTEMS-0095 | A mod-2 criterion for rigid/flexible Lattes portrait overlap | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1025 | 20001454 / AIM-FUNCTIONAL_ANALYSIS-0013 | Block-line sections and a covariance criterion for diagonal ell_p dilations | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1026 | 20001977 / AIM-GEOMETRY-0315 | Integral and mod-p Kirwan maps for weighted projective orbifolds | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1027 | 20002589 / AIM-PROBABILITY-0031 | A uniform-in-q product-chain cutoff and the Potts lower-bound gap | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1028 | 20002735 / AIM-REPRESENTATION_THEORY-0007 | Fixed vectors as compact-torus distinction | 0.0900 | 4 | unknown | queued | 0/5 |  |  |  |
| 1029 | 20003105 / AIM-TOPOLOGY-0193 | The forced length-spectrum max norm and a compatible-geodesic criterion | 0.0900 | 4 | unknown | queued | 0/5 |  |  |  |
| 1030 | 2200009 / AMR-021-0009 | Problems Around Polynomials — Conjecture 5 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1031 | 2200013 / AMR-021-0013 | Problems Around Polynomials — Conjecture 8 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1032 | 2304003 / AMR-022-4003 | Research Problems in Function Theory — Problem 4.3 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1033 | 2304028 / AMR-022-4028 | Research Problems in Function Theory — Problem 4.28 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1034 | 2305005 / AMR-022-5005 | Research Problems in Function Theory — Problem 5.5 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1035 | 2305029 / AMR-022-5029 | Research Problems in Function Theory — Problem 5.29 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1036 | 2306113 / AMR-022-6113 | Research Problems in Function Theory — Problem 6.113 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1037 | 2508 / EP-1133 | Erdős Problem #1133 | 0.0900 | 1 | unknown | queued | 0/5 |  |  |  |
| 1038 | 2616 / KOU-21.107 | Kourovka Notebook Problem 21.107 | 0.0900 | 2 | 2026 | queued | 0/5 |  |  |  |
| 1039 | 2673 / KP-1.14 | Kirby Problem 1.14 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1040 | 2681 / KP-1.22 | Kirby Problem 1.22 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1041 | 2689 / KP-1.30 | Kirby Problem 1.30 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1042 | 2719 / KP-1.60 | Kirby Problem 1.60 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1043 | 2776 / KP-2.28 | Kirby Problem 2.28 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1044 | 2794 / KP-2.46 | Kirby Problem 2.46 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1045 | 2843 / KP-3.45 | Kirby Problem 3.45 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1046 | 2845 / KP-3.47 | Kirby Problem 3.47 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1047 | 2945 / KP-4.69 | Kirby Problem 4.69 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1048 | 2956 / KP-4.80 | Kirby Problem 4.80 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1049 | 2960 / KP-4.84 | Kirby Problem 4.84 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1050 | 2970 / KP-4.94 | Kirby Problem 4.94 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1051 | 2974 / KP-4.98 | Kirby Problem 4.98 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1052 | 2980 / KP-4.104 | Kirby Problem 4.104 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1053 | 2991 / KP-4.115 | Kirby Problem 4.115 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1054 | 30006624 / OWR-14299911-026 | Cartan-Hadamard Theorem without Uniform Local Medianity | 0.0900 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1055 | 30006636 / OWR-14299913-005 | Extending Trisection Invariants to Four-Dimensional TQFTs | 0.0900 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1056 | 3011 / KP-5.4 | Kirby Problem 5.4 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1057 | 3023 / KP-5.16 | Kirby Problem 5.16 | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1058 | 3091 / OPG-59923 | Generalised Empty Hexagon Conjecture | 0.0900 | 1 | unknown | queued | 0/5 |  |  |  |
| 1059 | 3422 / OPG-37293 | Sticky Cantor sets | 0.0900 | 1 | unknown | queued | 0/5 |  |  |  |
| 1060 | 3800015 / AMR-037-0015 | Shortest paths in line arrangements | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1061 | 3900016 / AMR-038-0016 | Triangulations with many distinct areas | 0.0900 | 4 | unknown | queued | 0/5 |  |  |  |
| 1062 | 5500016 / AMR-054-0016 | Simple Polygonalizations | 0.0900 | 4 | unknown | queued | 0/5 |  |  |  |
| 1063 | 5500054 / AMR-054-0054 | Traveling Salesman Problem in Solid Grid Graphs | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1064 | 7200057 / AMR-071-0057 | For each arrangement of points in which the rectilinear crossing number is minimized, is the number of halving lines maximized | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1065 | 9500005 / AMR-094-0005 | Convergence of synchronous reflected-Brownian couplings | 0.0900 | 3 | unknown | queued | 0/5 |  |  |  |
| 1066 | 9500007 / AMR-094-0007 | Are shy couplings necessarily rigid? | 0.0900 | 4 | unknown | queued | 0/5 |  |  |  |
| 1067 | 30003846 / OWR-16167-016 | Finiteness and Rigidity of Fast Bump Groups | 0.0900 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1068 | 30003937 / OWR-16414-001 | Convergence of Dynamic Monge–Kantorovich Systems | 0.0900 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1069 | 30003946 / OWR-16415-008 | Equality of Variationally Minimizing Maps | 0.0900 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1070 | 30004018 / OWR-16635-003 | Socle Filtrations from Duflo–Serganova Kernels | 0.0900 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1071 | 30004167 / OWR-16941-008 | Prismatic Cohomology from Topological Cyclic Homology | 0.0897 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1072 | 30004168 / OWR-16941-009 | Prismatic Cohomology of Local Complete Intersections | 0.0897 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1073 | 30004409 / OWR-17471-016 | Motion Groups of Hopf-Tree Links | 0.0893 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1074 | 6900004 / AMR-068-0004 | Configuration Spaces of Tensegrities — Problem 4 | 0.0893 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1075 | 30004710 / OWR-7155449-014 | Completed Masur–Veech Volumes of Odd Strata | 0.0889 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1076 | 30004788 / OWR-8415342-016 | Restriction of Unramified GL Representations to Iwahori Blocks | 0.0889 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1077 | 6700061 / AMR-066-0061 | Scalar Curvature Question [?65]: Is the regular Euclidean $3$-simplex mean-convexly extremal | 0.0887 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1078 | 30005082 / OWR-10252925-008 | Mutations of Higher Grassmannian Degenerations | 0.0884 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1079 | 30005199 / OWR-11101917-008 | Necessity of Z-Stability in KK-Uniqueness | 0.0884 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1080 | 30005388 / OWR-12697687-013 | Equality of Involutive and Arf Knot Invariants | 0.0878 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1081 | 30005421 / OWR-12697690-001 | Uniform Expansion Stability for Wild Quivers | 0.0878 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1082 | 30005735 / OWR-14298011-006 | Bounded-Variation Solutions for Continuum Traffic Models | 0.0878 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1083 | 30004454 / OWR-1703863-003 | Coxeter Quotients of Automorphism Groups of Coxeter Groups | 0.0877 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1084 | 5300074 / AMR-052-0074 | Continuous extension of external-ray rotation number | 0.0872 | 3 | 1990 | queued | 0/5 |  |  |  |
| 1085 | 30005906 / OWR-14298370-006 | Fractional Calabi–Yau Properties of Higher Representation-Finite Algebras | 0.0870 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1086 | 30005923 / OWR-14298372-006 | Uniform Determinant Integrals for Row Contractions | 0.0870 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1087 | 30005996 / OWR-14298587-012 | Pointwise Quadratic Bounds for Extremal Solutions | 0.0870 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1088 | 30006088 / OWR-14298799-001 | Two-Loop SLE and Loop-Model Measures | 0.0870 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1089 | 5900021 / AMR-058-0021 | Combinatorial Types of Equal-Pressure Foam Cells | 0.0868 | 3 | 1995 | queued | 0/5 |  |  |  |
| 1090 | 30000012 / OWR-704-006 | Algebraic Dimension from Positive Normal Bundles | 0.0859 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1091 | 30000127 / OWR-757-005 | Oleinik Entropy for the Leroux System | 0.0859 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1092 | 30006513 / OWR-14299587-002 | Finite Length of Permutation Modules over Arbitrary Fields | 0.0859 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1093 | 30000268 / OWR-1050-019 | Global Stability Thresholds in Two-Species Migration Models | 0.0858 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1094 | 30000323 / OWR-1063-006 | Nonvanishing Euler Classes in Topological Bordism | 0.0858 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1095 | 30000630 / OWR-1394-006 | Generalized Covariograms of Planar Convex Bodies | 0.0857 | 3 | 2006 | queued | 0/5 |  |  |  |
| 1096 | 30000779 / OWR-1586-003 | $K(\pi,1)$ Theorems without Cyclotomic Class-Number Conditions | 0.0856 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1097 | 30000813 / OWR-1595-005 | Normality and Smoothness of Truncated Hadamard Simplices | 0.0856 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1098 | 30000977 / OWR-1971-010 | Degree Bounds for Canonical Covers of Minimal-Degree Surfaces | 0.0855 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1099 | 30001092 / OWR-2487-003 | Action Dependence of Free Indecomposability | 0.0855 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1100 | 30001100 / OWR-2489-004 | Convex-Hull Decomposition for Mixed-Integer Bipartite Systems | 0.0855 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1101 | 30001102 / OWR-2489-008 | Linear Optimization over Mixed-Integer Bipartite Systems | 0.0855 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1102 | 30001113 / OWR-2492-004 | Prorepresentable Obstructions for Local Action Deformations | 0.0855 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1103 | 4600046 / AMR-045-0046 | Periodic and finite configurations | 0.0855 | 4 | 2008 | queued | 0/5 |  |  |  |
| 1104 | 30001407 / OWR-4197-005 | Genus Three Hecke Trace Formula | 0.0852 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1105 | 30001576 / OWR-4427-011 | Triple-Point Theta Divisors at Odd Two-Torsion Points | 0.0852 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1106 | 30001739 / OWR-4804-007 | Multiplicity of Galois-Invariant Imprimitive Products | 0.0850 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1107 | 30001812 / OWR-5158-013 | Simplicial-Volume-Generated Seminorms in Third Homology | 0.0850 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1108 | 30001894 / OWR-11136-026 | Colored Transversals for Translates of Convex Sets | 0.0850 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1109 | 30001934 / OWR-11451-007 | Greedy Decomposition of the Spanning-Tree Polytope | 0.0850 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1110 | 30001946 / OWR-11454-004 | Topological Isolation of Singularities in Witt Bordism | 0.0850 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1111 | 30002070 / OWR-11786-027 | Triangulations of 3-Manifolds with Edge Valences Five and Six | 0.0849 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1112 | 30002676 / OWR-13113-001 | Gradient Flows for $N$-Species Reactive Cahn–Hilliard Systems | 0.0845 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1113 | 30002813 / OWR-13497-011 | Trigonometric-Polynomial Feedback for Nonlinear Stabilization | 0.0843 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1114 | 30002816 / OWR-13498-004 | Linear Sum-of-Squares Representations on Grassmann Orbitopes | 0.0843 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1115 | 30002908 / OWR-13687-007 | Nontrivial Actions on Invariant Prym Homology | 0.0843 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1116 | 30002966 / OWR-13941-006 | Core Points of Transitive Permutation Groups | 0.0843 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1117 | 30003032 / OWR-14211-007 | Bounds for Quaternary Local–Global Representation Exceptions | 0.0841 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1118 | 30003141 / OWR-14605-003 | Failure of Faber’s Conjecture in Genus Five | 0.0841 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1119 | 6600011 / AMR-065-0011 | A. Haynes: Gaps Problems — Problem | 0.0841 | 4 | 2016 | queued | 0/5 |  |  |  |
| 1120 | 30000584 / OWR-1326-005 | Packing Numbers of Automorphism Graphs on Curves | 0.0841 | 3 | 2006 | queued | 0/5 |  |  |  |
| 1121 | 10300002 / AMR-102-0002 | Existence questions — Question 2.2 | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1122 | 10300004 / AMR-102-0004 | Existence questions — Question 2.4 | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1123 | 10300046 / AMR-102-0046 | Hyperbolic geometry — Question 10.8 | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1124 | 10400035 / AMR-103-0035 | Question 2.13 — (T. | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1125 | 10400112 / AMR-103-0112 | Problem 6.4 — (S.J. | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1126 | 10600038 / AMR-105-0038 | Virtual-knot problem 38 — The Kauffman bracket polynomial of a virtual diagram can have the leading term, i.e., the term having the highest pos… | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1127 | 10600057 / AMR-105-0057 | Virtual-knot problem 57 — Is it true that two equivalent realizable graph-links are equivalent in the class of realizable graph-links? | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1128 | 10800002 / AMR-107-0002 | Problem 1B — Let a non-simple singularity $f$ be given and the Dynkin diagram of it be defined by an easily disting… | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1129 | 10800014 / AMR-107-0014 | Problem 5D — Do non-singular real plane projective curves of an odd degree consisting of a single connected compone… | 0.0840 | 2 | unknown | queued | 0/5 |  |  |  |
| 1130 | 10900062 / AMR-108-0062 | 8.8 (Taylor) — Hyperbolic knots not arising from complicated bands | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1131 | 11000026 / AMR-109-0026 | Question 3.5 — Is Teich(Σg), endowed with the Teichm¨ uller metric, almost convex? | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1132 | 11000099 / AMR-109-0099 | Question I — s there a constant NS, depending only on S, such that the following holds? | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1133 | 11000139 / AMR-109-0139 | Problem 9 — [Bounded Distortion Conjecture] Given a hyperbolic structure on F, associate its combinatorial invariant, namely, an… | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1134 | 20000369 / AIM-ALGEBRAIC_NUMBER_THEORY-0021 | All-valuation isotropy of a quadratic pencil and the limits of Boolean local tests | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1135 | 20000899 / AIM-COMBINATORICS-0024 | A variational energy core for stronger BSG | 0.0840 | 4 | unknown | queued | 0/5 |  |  |  |
| 1136 | 20000925 / AIM-COMBINATORICS-0050 | The exceptional three-color path problem: star-forest and triangle-density reductions | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1137 | 20001185 / AIM-COMPUTATION-0023 | Unique minimal Markov bases, bipartite cycles, and padding monotonicity | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1138 | 20002495 / AIM-PHYSICS-0003 | Exact zero-Kerr spectrum and high-energy Kerr localization | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1139 | 20002661 / AIM-PROBABILITY-0103 | Relative free-difference-quotient constants and spectral gaps | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1140 | 20002677 / AIM-PROBABILITY-0119 | Scalar circular resolvent estimate and the sharp two-thirds obstruction | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1141 | 2175 / EP-557 | Erdős Problem #557 | 0.0840 | 1 | unknown | queued | 0/5 |  |  |  |
| 1142 | 2309011 / AMR-022-9011 | Research Problems in Function Theory — Problem 9.11 | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1143 | 2723 / KP-1.64 | Kirby Problem 1.64 | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1144 | 2729 / KP-1.70 | Kirby Problem 1.70 | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1145 | 2743 / KP-1.84 | Kirby Problem 1.84 | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1146 | 2860 / KP-3.62 | Kirby Problem 3.62 | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1147 | 2882 / KP-4.6 | Kirby Problem 4.6 | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1148 | 2907 / KP-4.31 | Kirby Problem 4.31 | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1149 | 30006601 / OWR-14299910-006 | Universal $F$-Polynomial Configuration-Space Identities | 0.0840 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1150 | 3100030 / AMR-030-0030 | What is the (homogeneous adjacency) spectrum of the Fano plane | 0.0840 | 2 | unknown | queued | 0/5 |  |  |  |
| 1151 | 3152 / OPG-801 | Nearly spanning regular subgraphs | 0.0840 | 2 | unknown | queued | 0/5 |  |  |  |
| 1152 | 3261 / OPG-46279 | Antidirected trees in digraphs | 0.0840 | 1 | unknown | queued | 0/5 |  |  |  |
| 1153 | 3800007 / AMR-037-0007 | Tangent pairs of pseudocircles | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1154 | 3800012 / AMR-037-0012 | Complex collinearities | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1155 | 5500022 / AMR-054-0022 | Minimum-Link Path in 2D | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1156 | 5500042 / AMR-054-0042 | Vertex-Unfolding Polyhedra | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1157 | 5500049 / AMR-054-0049 | Planar Euclidean Maximum TSP | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1158 | 5500076 / AMR-054-0076 | Equiprojective Polyhedra | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1159 | 8400008 / AMR-083-0008 | O7b — Factoring from a squarefree-part oracle | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1160 | 9700007 / AMR-096-0007 | Constant-factor online scheduling of subadditive batches | 0.0840 | 3 | unknown | queued | 0/5 |  |  |  |
| 1161 | 30000659 / OWR-1452-023 | Contractibility of Quotient Curves from Additive-Group Actions | 0.0839 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1162 | 30003626 / OWR-15954-007 | Sharp Eigenvalue Bounds for Nonselfadjoint Jacobi Perturbations | 0.0838 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1163 | 30003635 / OWR-15955-012 | Pure Braid Squares in the Symmetric Grope Filtration | 0.0838 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1164 | 30003636 / OWR-15955-013 | Characteristic Varieties of Divisors Beyond Line Arrangements | 0.0838 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1165 | 6700023 / AMR-066-0023 | Scalar Curvature Question [?22]: It seems not impossible, at least for compactX, that, in fact, K-area(X×R) =K-area(X×S1) | 0.0838 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1166 | 6700028 / AMR-066-0028 | Scalar Curvature Question [?28]: For instance, letX be homomorphic to CP 2 and letvol(Uδ(S)) ≥δ2 for allT(X)-non-spin surfacesS ⊂X and 0<δ ≤1 | 0.0838 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1167 | 6700030 / AMR-066-0030 | Scalar Curvature Question [?30]: On the other hand, there probably exist compact simply connected n-dimensional manifolds for alln ≥4 with arbi | 0.0838 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1168 | 30001077 / OWR-2091-007 | Orbifold Lifts of Deligne Mostow Forgetful Maps | 0.0838 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1169 | 30003767 / OWR-16158-008 | Quantitative Thin-Set Descriptions of Reducible Specializations | 0.0836 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1170 | 30003822 / OWR-16164-020 | Catalan-Power Divisibility of a Set-Partition Transition Determinant | 0.0836 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1171 | 30003934 / OWR-16413-005 | Uniqueness of Equilibria in Rank-One Bimatrix Games | 0.0836 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1172 | 30003942 / OWR-16415-001 | Good Curve Graphs with Unbounded Mapping-Class Orbits | 0.0836 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1173 | 30003968 / OWR-16418-001 | Weak Tumor-Invasion Solutions Without Growth Compatibility | 0.0836 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1174 | 30004000 / OWR-16633-017 | Degree-Utility Optimization in Graphs | 0.0836 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1175 | 30004077 / OWR-16768-009 | Coordinate Realization of Characteristic-Polyhedron Multiplicity | 0.0833 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1176 | 30004182 / OWR-17127-008 | Ranks of Reeb Action Spectra | 0.0833 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1177 | 30004198 / OWR-17132-001 | Normed Algebra Lifts of the Motivic Tau Cofiber | 0.0833 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1178 | 30004361 / OWR-17464-021 | Balanced Three-Colorings of Six-Uniform Hypergraphs | 0.0829 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1179 | 30004489 / OWR-1703871-002 | Brauer Groups of Smooth Models of Symmetric Powers | 0.0829 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1180 | 30004518 / OWR-1703876-012 | Simple Spatial Polygon Realizations from Angle Sequences | 0.0829 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1181 | 30004524 / OWR-1703876-018 | Continuous Selection of Piecewise Linear Planar Extensions | 0.0829 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1182 | 6900006 / AMR-068-0006 | Configuration Spaces of Tensegrities — Problem 6 | 0.0829 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1183 | 30004587 / OWR-4990370-005 | Tensor Stability of Quantum Markov Gradient Estimates | 0.0825 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1184 | 30004878 / OWR-8415354-004 | Pole Orders and Extensions of Kirillov–Reshetikhin Modules | 0.0825 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1185 | 30004886 / OWR-8415355-007 | Splitting Subgroups of General Linear Supergroups | 0.0825 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1186 | 30004900 / OWR-8415356-006 | Extension Complexity of Inscribed Fixed-Dimensional Polytopes | 0.0825 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1187 | 30004903 / OWR-8415356-014 | Linear Bounds for Minimally Integer-Infeasible Systems | 0.0825 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1188 | 30004909 / OWR-8415356-020 | Approximating Submodular Functions by Matroid Rank Functions | 0.0825 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1189 | 30004914 / OWR-8415356-025 | Deterministic Optimization of Top-$k$ Perfect-Matching Edges | 0.0825 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1190 | 10400062 / AMR-103-0062 | Question 3.12 — (C. | 0.0825 | 3 | unknown | queued | 0/5 |  |  |  |
| 1191 | 10400170 / AMR-103-0170 | Problem 9.6 — (Y. | 0.0825 | 3 | unknown | queued | 0/5 |  |  |  |
| 1192 | 20003131 / AIM-TOPOLOGY-0219 | The dual Wilking bound and singular join tests | 0.0825 | 3 | unknown | queued | 0/5 |  |  |  |
| 1193 | 2301040 / AMR-022-1040 | Research Problems in Function Theory — Problem 1.40 | 0.0825 | 3 | unknown | queued | 0/5 |  |  |  |
| 1194 | 2303011 / AMR-022-3011 | Research Problems in Function Theory — Problem 3.11 | 0.0825 | 3 | unknown | queued | 0/5 |  |  |  |
| 1195 | 2304015 / AMR-022-4015 | Research Problems in Function Theory — Problem 4.15 | 0.0825 | 3 | unknown | queued | 0/5 |  |  |  |
| 1196 | 2306058 / AMR-022-6058 | Research Problems in Function Theory — Problem 6.58 | 0.0825 | 3 | unknown | queued | 0/5 |  |  |  |
| 1197 | 2306099 / AMR-022-6099 | Research Problems in Function Theory — Problem 6.99 | 0.0825 | 3 | unknown | queued | 0/5 |  |  |  |
| 1198 | 2307034 / AMR-022-7034 | Research Problems in Function Theory — Problem 7.34 | 0.0825 | 3 | unknown | queued | 0/5 |  |  |  |
| 1199 | 30003087 / OWR-14222-015 | Explicit Formula for Absolute Linear Harbourne Constants | 0.0825 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1200 | 30005118 / OWR-10252930-031 | Efficient Recognition of Cyclic Sumsets | 0.0821 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1201 | 30005233 / OWR-11101922-005 | Continuous-Time Extensions of Attractive Percolation Models | 0.0821 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1202 | 30003862 / OWR-16169-009 | Polar Cylinders and Affine Complements of Del Pezzo Surfaces | 0.0820 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1203 | 30005477 / OWR-12697711-012 | Stable Division and Arveson–Douglas Essential Normality | 0.0815 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1204 | 30005580 / OWR-14297732-007 | Flow Limits of Local Mass Invariants | 0.0815 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1205 | 30005651 / OWR-14297741-001 | Equivariant Stable Connectivity in Higher Representation Dimension | 0.0815 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1206 | 30005656 / OWR-14297741-006 | Balmer Spectra for Constant Mackey Functors | 0.0815 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1207 | 30005695 / OWR-14298004-003 | Rational Duality among Crystallographic Coxeter Groups | 0.0815 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1208 | 30005734 / OWR-14298011-005 | Occupational Measures for Tonelli Hamilton–Jacobi Equations | 0.0815 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1209 | 30005909 / OWR-14298370-009 | Heisenberg Actions on Hochschild–Serre Cohomology | 0.0808 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1210 | 30005922 / OWR-14298372-005 | Unitary Integral Identity for Noncommutative Polynomials | 0.0808 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1211 | 30006051 / OWR-14298592-002 | Completeness of Unzipped-Link Invariants for Spatial Theta Graphs | 0.0808 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1212 | 30006105 / OWR-14298804-007 | Fixed-Parameter Tractability of Zonotope Containment | 0.0808 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1213 | 30006403 / OWR-14299518-027 | Zero Submatrices in Sparse Low-Rank Matrices | 0.0798 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1214 | 30006465 / OWR-14299577-018 | Difference Sets of Signed Representatives | 0.0798 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1215 | 3700008 / AMR-036-0008 | Number of degenerate Herman rings | 0.0798 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1216 | 30000005 / OWR-701-001 | Uniqueness for Spatially Dependent Two-Phase Diffusion | 0.0793 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1217 | 30000114 / OWR-741-008 | A Weakened Wills Inequality for Convex Bodies | 0.0793 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1218 | 30000160 / OWR-782-001 | Congruences for Extremal Modular Forms | 0.0792 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1219 | 30000200 / OWR-792-017 | Stationary and Optimal Linear Differential Behaviors | 0.0792 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1220 | 30000217 / OWR-823-001 | Weak-Solution Uniqueness for Coupled Thermomechanical Systems | 0.0792 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1221 | 30000267 / OWR-1050-018 | Category Bounds for Positive Nonlinear Schrödinger Solutions | 0.0792 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1222 | 6200011 / AMR-061-0011 | Boundaries of Groups and Kleinian Groups — Problem 11 | 0.0792 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1223 | 30000391 / OWR-1183-011 | Infinite Transversals from Points to Spanned Hyperplanes | 0.0791 | 3 | 2006 | queued | 0/5 |  |  |  |
| 1224 | 30000485 / OWR-1272-009 | Euler-Characteristic Growth of Stable Quiver Moduli | 0.0791 | 3 | 2006 | queued | 0/5 |  |  |  |
| 1225 | 30000640 / OWR-1452-004 | Nontame Automorphisms with Point-Centered Sarkisov Factorizations | 0.0790 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1226 | 30000773 / OWR-1543-004 | Attracting Edges in Strongly Reinforced Random Walks | 0.0790 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1227 | 30000784 / OWR-1587-003 | Optimal Algebraic Immunity of Boolean Functions | 0.0790 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1228 | 30000822 / OWR-1596-004 | Category-Weight Constructions for Nonsimply Connected Spaces | 0.0790 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1229 | 30001048 / OWR-2089-004 | Geodesicity of Core Tunnels in Compression Bodies | 0.0789 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1230 | 30001073 / OWR-2090-026 | Permanent Bounds for Diffuse Doubly Stochastic Matrices | 0.0789 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1231 | 4000003 / AMR-039-0003 | Nilpotent groups | 0.0789 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1232 | 4600045 / AMR-045-0045 | Sparse jointly periodic points | 0.0789 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1233 | 30001149 / OWR-3388-008 | Almost-Rational Automorphisms of Higher Prime-Power Order | 0.0788 | 3 | 2009 | queued | 0/5 |  |  |  |
| 1234 | 30001192 / OWR-3393-004 | Complexity Drops for p-by-p Specht Modules | 0.0788 | 3 | 2009 | queued | 0/5 |  |  |  |
| 1235 | 30001496 / OWR-4340-007 | EPW Sextics from Fano Models of Enriques Surfaces | 0.0786 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1236 | 30001654 / OWR-4791-010 | Semisaturation Number of the Five-Cycle | 0.0785 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1237 | 30001931 / OWR-11451-004 | Integer Carathéodory Property for Intersecting Matroid Base Polytopes | 0.0785 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1238 | 30001933 / OWR-11451-006 | Integer Carathéodory Property for Arborescence Polytopes | 0.0785 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1239 | 30002170 / OWR-12013-003 | Lower Bounds for Fractional Lévy-Area Approximation | 0.0783 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1240 | 30002367 / OWR-12495-007 | Topological Nilpotence Degree of Finite-Group Chow Rings | 0.0782 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1241 | 30002401 / OWR-12592-003 | Mass Growth Versus Categorical Entropy | 0.0782 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1242 | 30002481 / OWR-12862-007 | Projective Determinacy and Zero Sharp over Third-Order Arithmetic | 0.0780 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1243 | 30002633 / OWR-13106-006 | Sharp $hat A$-Genus Bound for the $kappa$-Invariant | 0.0780 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1244 | 30002729 / OWR-13353-017 | Additive Integrality Gap for Ring Loading | 0.0780 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1245 | 10000025 / AMR-099-0025 | Isoperimetric dimension and connective constants | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1246 | 10000030 / AMR-099-0030 | Three-dimensional sphere packing from a planar height function | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1247 | 10300012 / AMR-102-0012 | Sublaminations and superlaminations — Question 6.2 | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1248 | 10300018 / AMR-102-0018 | Branched surfaces and triangulations — Question 7.3 | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1249 | 10300020 / AMR-102-0020 | Branched surfaces and triangulations — Question 7.5 | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1250 | 10400018 / AMR-103-0018 | Problem 1.18 — (A. | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1251 | 10400181 / AMR-103-0181 | Problem 10.6 — (M. | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1252 | 10400209 / AMR-103-0209 | Problem 12.3 — (H.R. | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1253 | 10600027 / AMR-105-0027 | Virtual-knot problem 27 — Study concordance and cobordism invariants of virtual knots. | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1254 | 11000037 / AMR-109-0037 | Conjecture 3.16 — d(Ig) = 0. | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1255 | 11000049 / AMR-109-0049 | Problem 4.12 — (Distortion of the Schottky locus). | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1256 | 11000150 / AMR-109-0150 | Question (Smith) — Let αi, i = 1,...,n be a configuration of curves on a surface S of genus g with one boundary component δ such that ev… | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1257 | 11000298 / AMR-109-0298 | Question 6.2 — Can Out(Fn) and Mod±(Sg) be obtained as a pushout of a finite subsystem of their finite subgroups, i.e. | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1258 | 11000312 / AMR-109-0312 | Problem 4.5 — Prove (or disprove) that the natural homomorphism H 4(OutF4; Q)∼= Q−→H 4(IOut4; Q)GL is an isomorphism where the righ… | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1259 | 1435 / GRAPH-048 | Crown Graphs and Longest Word-Representants | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1260 | 171 / GREEN-083 | Pyjama Set Covering | 0.0780 | 1 | unknown | queued | 0/5 |  |  |  |
| 1261 | 20000029 / AIM-ALGEBRAIC_GEOMETRY-0029 | Odd-prime solution and completion-transfer reduction | 0.0780 | 4 | unknown | queued | 0/5 |  |  |  |
| 1262 | 20000032 / AIM-ALGEBRAIC_GEOMETRY-0032 | The filtered geometric-fixed-point model and an odd-primary answer for a-inverted real Artin--Tate spectra | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1263 | 20000061 / AIM-ALGEBRAIC_GEOMETRY-0061 | Explicit K3 models and fine-moduli equivalences for discriminants 26 and 38 | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1264 | 20000075 / AIM-ALGEBRAIC_GEOMETRY-0075 | A residual parity-defect criterion for the fourth grading on HHH | 0.0780 | 4 | unknown | queued | 0/5 |  |  |  |
| 1265 | 20000079 / AIM-ALGEBRAIC_GEOMETRY-0079 | A sharp two-strand full-twist threshold for HHH-parity | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1266 | 20000088 / AIM-ALGEBRAIC_GEOMETRY-0088 | Rank-two equality and the all-rank coherence obstruction | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1267 | 20000123 / AIM-ALGEBRAIC_GEOMETRY-0123 | Fixed points in dimension two and wild fixed-scheme multiplicities | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1268 | 20000289 / AIM-ALGEBRAIC_GEOMETRY-0289 | Ambient adjoint Cartier test ideals and an intrinsic curve model | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1269 | 20000488 / AIM-ANALYSIS-0020 | All-coupling Robin bound states for compact graph deformations in dimensions two and three | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1270 | 20000770 / AIM-ARITHMETIC_GEOMETRY-0016 | Order-three fineness obstructions on degree-two and degree-four K3 surfaces | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1271 | 20000886 / AIM-COMBINATORICS-0011 | Expansion can hide only global Sidorenko obstructions | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1272 | 20000976 / AIM-COMBINATORICS-0101 | Periodic Laplacian certificates for robustness and explosion | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1273 | 20001078 / AIM-COMBINATORICS-0203 | Defect feedback sets and a fractional obstruction for four-order majority digraphs | 0.0780 | 4 | unknown | queued | 0/5 |  |  |  |
| 1274 | 20001104 / AIM-COMBINATORICS-0229 | An anchor-container reduction for imbalanced restricted sumsets | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1275 | 20001204 / AIM-COMPUTATION-0042 | Quartic Markov bases and saturated simplicial leaves | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1276 | 20001251 / AIM-COMPUTATION-0089 | A norm obstruction for Agrawal's conjecture | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1277 | 20001374 / AIM-DYNAMICAL_SYSTEMS-0032 | Two square-class tests for finite-level agreement of quadratic arboreal representations | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1278 | 20001400 / AIM-DYNAMICAL_SYSTEMS-0058 | Martingales from sequential transfer contraction | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1279 | 20002675 / AIM-PROBABILITY-0117 | Smooth-witness and semicircular-attractor obstructions to free strong unimodality | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1280 | 20002973 / AIM-TOPOLOGY-0061 | A Jacobian criterion for the Soergel counit on Hochschild (co)homology | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1281 | 2100509 / AMR-020-0509 | Open Problems in Integrable Systems — Nijenhuis operators: singular points and global properties | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1282 | 2157 / EP-522 | Erdős Problem #522 | 0.0780 | 1 | unknown | queued | 0/5 |  |  |  |
| 1283 | 2305064 / AMR-022-5064 | Research Problems in Function Theory — Problem 5.64 | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1284 | 2330 / EP-831 | Erdős Problem #831 | 0.0780 | 1 | unknown | queued | 0/5 |  |  |  |
| 1285 | 2687 / KP-1.28 | Kirby Problem 1.28 | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1286 | 2716 / KP-1.57 | Kirby Problem 1.57 | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1287 | 2951 / KP-4.75 | Kirby Problem 4.75 | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1288 | 2964 / KP-4.88 | Kirby Problem 4.88 | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1289 | 2976 / KP-4.100 | Kirby Problem 4.100 | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1290 | 3000001 / AMR-029-0001 | Achieve global rigidity by pinning nodes | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1291 | 3000007 / AMR-029-0007 | Binary matroid representation of cyclic families | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1292 | 3000009 / AMR-029-0009 | Capacitated packing of k-arborescences | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1293 | 3000016 / AMR-029-0016 | Complexity of the chip-firing reachability problem for general digraphs | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1294 | 3000018 / AMR-029-0018 | Complexity of the halting problem for simple digraphs | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1295 | 3000028 / AMR-029-0028 | Decomposition of oriented k-partition-connected digraphs | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1296 | 3000029 / AMR-029-0029 | Destroying rigidity | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1297 | 3000044 / AMR-029-0044 | Independent arborescences in acyclic digraphs | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1298 | 3000061 / AMR-029-0061 | Orientation with shortest round trip | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1299 | 30006658 / OWR-14299915-021 | Vanishing for Non-$p$-Nilpotent Compact Lie Groups | 0.0780 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1300 | 3100060 / AMR-030-0060 | If F is a finite field with at least 4 elements and A is an invertible n by n matrix over F, then there are vectors x, y | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1301 | 3100062 / AMR-030-0062 | Is it true that, for every n, there is an integer M(n), so that whenever a linear homogeneous equation in n variables is | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1302 | 3400 / OPG-474 | Linear-size circuits for stable $0,1 < 2$ sorting? | 0.0780 | 1 | unknown | queued | 0/5 |  |  |  |
| 1303 | 3900001 / AMR-038-0001 | Antipodes of symmetric convex bodies | 0.0780 | 4 | unknown | queued | 0/5 |  |  |  |
| 1304 | 5500029 / AMR-054-0029 | Hamiltonian Tetrahedralizations | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1305 | 5500040 / AMR-054-0040 | The Number of Pointed Pseudotriangulations | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1306 | 5500066 / AMR-054-0066 | Reflexivity of Point Sets | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1307 | 8700045 / AMR-086-0045 | Question 3.27 — Mahler | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1308 | 8800026 / AMR-087-0026 | Algebraic independence in multivariate elimination | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1309 | 8800067 / AMR-087-0067 | SVP-to-CVP reduction within ideal lattices | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1310 | 9700022 / AMR-096-0022 | Percolation of planar empires at unit merger rate | 0.0780 | 3 | unknown | queued | 0/5 |  |  |  |
| 1311 | 4500001 / AMR-044-0001 | Periods of Pseudo-Integrable Billiards | 0.0778 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1312 | 30003033 / OWR-14211-008 | Indefinite Theta Series and Real Jacobi Representations | 0.0776 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1313 | 30003161 / OWR-14612-002 | Flux Stability for Multidimensional Conservation Laws | 0.0776 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1314 | 30003308 / OWR-15178-016 | Gorenstein Monomial Curves from Principal Matrices | 0.0776 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1315 | 30003362 / OWR-15208-016 | Positive Ricci Observer Homotopy Beyond Spheres | 0.0774 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1316 | 30003421 / OWR-15217-001 | Support Ideals in Constructible-Function Convolution Algebras | 0.0774 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1317 | 30003439 / OWR-15219-008 | Negatively Curved Barriers Beyond Hyperbolicity Cones | 0.0774 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1318 | 30003590 / OWR-15586-001 | Openness of Cones Generated by Ample Subvarieties | 0.0774 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1319 | 30003863 / OWR-16169-010 | Polar Cylinders and Complement Automorphisms | 0.0771 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1320 | 30003952 / OWR-16415-015 | Smooth Lifts of the Dehn-Twist Braid Relation | 0.0771 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1321 | 30003976 / OWR-16628-005 | Symbolic-Power Noncontainments for Reflection Arrangements | 0.0771 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1322 | 30003993 / OWR-16633-010 | Integrality Gaps for Directed Linear k-Cut | 0.0771 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1323 | 30004007 / OWR-16633-025 | Decomposition of Representable Polymatroids into Matroid Ranks | 0.0771 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1324 | 30004127 / OWR-16931-012 | Sample Complexity of Vertex-Distribution-Free Graph Testing | 0.0769 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1325 | 30004185 / OWR-17128-001 | Higher-Dimensional Frenkel–Kontorova Traveling Waves | 0.0769 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1326 | 30004196 / OWR-17130-012 | Ancient Ovals as Post-Singularity Limit Flows | 0.0769 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1327 | 30004231 / OWR-17135-028 | Shellability and Homology of Totally Mixed Face Posets | 0.0769 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1328 | 30004311 / OWR-17294-011 | Simple Braces as Asymmetric Products | 0.0769 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1329 | 30004329 / OWR-17296-014 | Rationality of Seshadri Constants from Plane-Curve Singularities | 0.0769 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1330 | 30004368 / OWR-17466-007 | Completion of Presilting Complexes | 0.0766 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1331 | 30004486 / OWR-1703869-006 | Energy-Angular Momentum Relations for Rotating Skyrmions | 0.0766 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1332 | 30004513 / OWR-1703876-006 | Sharp Constrained-Drawing Bounds for Closure Operators | 0.0766 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1333 | 30004575 / OWR-2654836-008 | Sharp Fractional Brownian Density Estimates with Drift | 0.0766 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1334 | 5000004 / AMR-049-0004 | Reachable points on lines through a unitary pair | 0.0766 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1335 | 20000225 / AIM-ALGEBRAIC_GEOMETRY-0225 | Proper-point defects and the degree-21 bottleneck | 0.0765 | 3 | unknown | queued | 0/5 |  |  |  |
| 1336 | 20000822 / AIM-ARITHMETIC_GEOMETRY-0068 | A fixed-locus criterion and an obstruction in the standard nonreduced toric chart | 0.0765 | 4 | unknown | queued | 0/5 |  |  |  |
| 1337 | 20003226 / AIM-OTHER-0033 | The tropical quotient and equality for unions of chains | 0.0765 | 3 | unknown | queued | 0/5 |  |  |  |
| 1338 | 2032 / EP-289 | Erdős Problem #289 | 0.0765 | 1 | unknown | queued | 0/5 |  |  |  |
| 1339 | 30004661 / OWR-7155441-002 | Rigidity of Morphisms to Wound Unipotent Groups | 0.0762 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1340 | 5100043 / AMR-050-0043 | Elliptic-billiard invariant k_{803} | 0.0762 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1341 | 30004736 / OWR-8415336-005 | Accumulation Points of Convex Billiard Length Spectra | 0.0762 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1342 | 30004912 / OWR-8415356-023 | Compact Representations of Four-Thirds Near-Mincuts | 0.0762 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1343 | 30005263 / OWR-11695859-006 | Dimension-Free Lipschitz Optimal Transport Maps | 0.0758 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1344 | 30005275 / OWR-11695860-014 | Recovering Polynomials from Fourier-Magnitude Data | 0.0758 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1345 | 30005298 / OWR-11695864-003 | Dimensions of General Weddle Loci | 0.0758 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1346 | 30005683 / OWR-14297746-003 | Diffraction Scaling and Mahler-Function Asymptotics | 0.0752 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1347 | 30005455 / OWR-12697708-008 | Sharp Reinforcement Thresholds for Tree and Whisker Components | 0.0752 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1348 | 30005461 / OWR-12697710-007 | Mixed Odd Powers of Sum-of-Squares Polynomials | 0.0752 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1349 | 30005534 / OWR-13750334-004 | Quadratically Enriched Tropical Curve Invariants | 0.0752 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1350 | 10400072 / AMR-103-0072 | Conjecture 3.22 — [357, 139] The map (29) is injective. | 0.0750 | 3 | unknown | queued | 0/5 |  |  |  |
| 1351 | 2302066 / AMR-022-2066 | Research Problems in Function Theory — Problem 2.66 | 0.0750 | 3 | unknown | queued | 0/5 |  |  |  |
| 1352 | 2307037 / AMR-022-7037 | Research Problems in Function Theory — Problem 7.37 | 0.0750 | 3 | unknown | queued | 0/5 |  |  |  |
| 1353 | 30005752 / OWR-14298157-001 | Positivity Criterion for Quantum Greedy Bases | 0.0746 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1354 | 30005793 / OWR-14298161-003 | Stability and Alternative Costs in Spherical Optimal Transport | 0.0746 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1355 | 30005952 / OWR-14298580-008 | Strong Geography for Rational Homology Spheres | 0.0746 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1356 | 30006113 / OWR-14298804-016 | Half-Integral Extreme Points for a Feedback-Vertex-Set Relaxation | 0.0746 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1357 | 30000052 / OWR-723-005 | Expected Discrepancy of Generalized Lattice Point Sets | 0.0744 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1358 | 30000374 / OWR-1116-002 | Dense-Order-Preserving Preorders on Ordinal-Valued Functions | 0.0743 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1359 | 30000515 / OWR-1276-008 | Simple Connectivity of Godeaux Surfaces | 0.0742 | 3 | 2006 | queued | 0/5 |  |  |  |
| 1360 | 30000664 / OWR-1452-028 | Kernels of Completed Locally Nilpotent Derivations | 0.0741 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1361 | 30001095 / OWR-2488-001 | Zero-Regularity Stochastic Burgers Equations with Lévy Noise | 0.0740 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1362 | 3700038 / AMR-036-0038 | Rectangular-lattice Landau extremal | 0.0738 | 3 | 2009 | queued | 0/5 |  |  |  |
| 1363 | 30001611 / OWR-4531-003 | Optimal Inverse-Growth Conditions for Bicyclic Operator Cyclicity | 0.0737 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1364 | 30006210 / OWR-14299088-012 | Inverse-Polynomial Influence Thresholds on the Boolean Cube | 0.0736 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1365 | 30002009 / OWR-11580-019 | Perfect Weyl-Group Complexes of Flag Varieties | 0.0734 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1366 | 30002058 / OWR-11786-011 | Finite-Ring Solutions of Thurston Equations | 0.0734 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1367 | 30002112 / OWR-12005-004 | Additive Eigenvalue Bounds for Domain Boundaries | 0.0734 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1368 | 5900019 / AMR-058-0019 | Product Partitions of Slabs and Long Cylinders | 0.0734 | 3 | 1995 | queued | 0/5 |  |  |  |
| 1369 | 30002326 / OWR-12481-016 | Sublinear Bounds for Disjoint Homometric Vertex Sets | 0.0733 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1370 | 30002450 / OWR-12732-002 | Potentials for Quivers from Twice-Punctured Surfaces | 0.0733 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1371 | 30002379 / OWR-12583-002 | Rational Points on Prime-Level Modular Curves | 0.0733 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1372 | 30002482 / OWR-12863-001 | Symplectic Periods of Essentially Speh Representations | 0.0731 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1373 | 30002562 / OWR-12975-007 | Zero Thresholds for Positive Semidefinite Ternary Forms | 0.0731 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1374 | 30002668 / OWR-13110-017 | Long Alternating Paths in Colored Line Arrangements | 0.0731 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1375 | 30002714 / OWR-13351-013 | Complete Integral Closures of Total Blow-Up Rings | 0.0731 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1376 | 30002950 / OWR-13860-007 | Orbit Structure of Generic A-Number-One Loci | 0.0730 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1377 | 30003045 / OWR-14213-012 | Cohomology Kernels for Inseparable Pfister Composita | 0.0728 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1378 | 30003059 / OWR-14218-002 | Hochschild Regularity Under Separable Equivalence | 0.0728 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1379 | 30003321 / OWR-15181-013 | Discrete Initial Subgroups of the Surreal Numbers | 0.0728 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1380 | 30000047 / OWR-721-002 | Far-Field Solvability in Electromagnetic Inverse Scattering | 0.0727 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1381 | 30000214 / OWR-822-005 | Homology-Sphere Factors in Simplicial Decompositions | 0.0726 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1382 | 30000336 / OWR-1106-011 | Nonstabilized Weakly Reducible Heegaard Splittings | 0.0726 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1383 | 30003650 / OWR-15957-003 | Extremal Completely Positive Plus-Rank | 0.0726 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1384 | 30000879 / OWR-1738-004 | Trivial Restrictions of Twists in Nilpotent Group Algebras | 0.0724 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1385 | 30001128 / OWR-2495-005 | Nonlinear Stability of Periodic Reaction–Diffusion Waves | 0.0723 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1386 | 4000006 / AMR-039-0006 | Sharp Lichnerowicz theorem | 0.0723 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1387 | 30001214 / OWR-3397-002 | Local Closedness of Symplectic Cores | 0.0722 | 3 | 2009 | queued | 0/5 |  |  |  |
| 1388 | 30001551 / OWR-4425-006 | Independent Word Equations with Nonperiodic Solutions | 0.0721 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1389 | 102 / GREEN-012 | Tuples in Dense Sets | 0.0720 | 2 | unknown | queued | 0/5 |  |  |  |
| 1390 | 10400178 / AMR-103-0178 | Question 10.3 — (C. | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1391 | 10600028 / AMR-105-0028 | Virtual-knot problem 28 — Biquandles | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1392 | 11000008 / AMR-109-0008 | Question 2.1 — (Ends spectrum). | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1393 | 11000187 / AMR-109-0187 | Conjecture 2.2 — Suppose C∞(Hom(π,G )/G) D− →C∞(Hom(π,G )/G) is a diﬀerential operator which commutes with the ModΣ-action on Hom(π,G… | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1394 | 11000196 / AMR-109-0196 | Problem 3.3 — Determine the ergodic behavior of the ModΣ-action on the level sets ( iR× R×iR ) ∩κ−1(t) wheret> 2. | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1395 | 11000197 / AMR-109-0197 | Problem 3.4 — Find a point ρ∈ Hom(π, SL(2, C)) such that the closure of its orbit ModΣ· [ρ] meets both the image of the unitary cha… | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1396 | 11000313 / AMR-109-0313 | Problem 4.6 — Determine the homomorphisms H 8(M3,∗; Q) i∗ ←−H 8(OutF6; Q) p∗ ←−H 8(GL(6, Z); Q) (10) induced by the above homomorph… | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1397 | 1389 / GRAPH-002 | Eternal Domination vs Domination Number | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1398 | 1889 / EP-25 | Erdős Problem #25 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1399 | 1900013 / AMR-018-0013 | Geometry of Continued Fractions — Combinatorial structure of sails | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1400 | 1903 / EP-51 | Erdős Problem #51 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1401 | 1910 / EP-68 | Erdős Problem #68 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1402 | 1954 / EP-143 | Erdős Problem #143 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1403 | 1988 / EP-197 | Erdős Problem #197 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1404 | 1992 / EP-203 | Erdős Problem #203 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1405 | 2000004 / AMR-019-0004 | Some Open Problems in Elasticity — Lavrentiev phenomena | 0.0720 | 4 | unknown | queued | 0/5 |  |  |  |
| 1406 | 20000624 / AIM-ANALYSIS-0156 | Stability-preserving Markov semigroups on three bits | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1407 | 20000821 / AIM-ARITHMETIC_GEOMETRY-0067 | A support-deficit criterion and the fold-singularity test family | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1408 | 20000970 / AIM-COMBINATORICS-0095 | Exact block-product sampling of maximal G-parking functions | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1409 | 20000973 / AIM-COMBINATORICS-0098 | Naturality as an affine automorphism action | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1410 | 20001131 / AIM-COMBINATORICS-0256 | Compact Freiman models and relation peeling | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1411 | 20001148 / AIM-COMBINATORICS-0273 | Perfect contractility and 1-amalgam blocks | 0.0720 | 4 | unknown | queued | 0/5 |  |  |  |
| 1412 | 20001157 / AIM-COMBINATORICS-0282 | Safe edge deletion, modular unichord certificates, and the 3-core | 0.0720 | 4 | unknown | queued | 0/5 |  |  |  |
| 1413 | 20001394 / AIM-DYNAMICAL_SYSTEMS-0052 | A gap-optimized Poisson approximation bound with a clustering obstruction | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1414 | 20001406 / AIM-DYNAMICAL_SYSTEMS-0064 | Gluing blockwise martingale decompositions across seams | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1415 | 20001410 / AIM-DYNAMICAL_SYSTEMS-0068 | Flux normalization and clustering tests for billiard strip targets | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1416 | 20002023 / AIM-GEOMETRY-0361 | A variational test and a family of conformal primitives | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1417 | 20002420 / AIM-PDES-0032 | Quadratic-growth complex Monge-Ampere rigidity with a completeness gap | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1418 | 20002650 / AIM-PROBABILITY-0092 | Stationary gaps and a second-class gap discrepancy for two-sided q-ASEP | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1419 | 20003150 / AIM-TOPOLOGY-0238 | Reduction, holonomy, and symplectic-pencil obstructions | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1420 | 2004 / EP-243 | Erdős Problem #243 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1421 | 2009 / EP-252 | Erdős Problem #252 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1422 | 2016 / EP-263 | Erdős Problem #263 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1423 | 2019 / EP-267 | Erdős Problem #267 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1424 | 2020 / EP-269 | Erdős Problem #269 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1425 | 2033 / EP-291 | Erdős Problem #291 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1426 | 2037 / EP-302 | Erdős Problem #302 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1427 | 2041 / EP-312 | Erdős Problem #312 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1428 | 2062 / EP-341 | Erdős Problem #341 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1429 | 2065 / EP-346 | Erdős Problem #346 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1430 | 2066 / EP-348 | Erdős Problem #348 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1431 | 2070 / EP-354 | Erdős Problem #354 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1432 | 2071 / EP-357 | Erdős Problem #357 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1433 | 2083 / EP-377 | Erdős Problem #377 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1434 | 2087 / EP-385 | Erdős Problem #385 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1435 | 2100204 / AMR-020-0204 | Open Problems in Integrable Systems — Topology of integrable systems, Lagrangian fibrations, and their invariants | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1436 | 2100404 / AMR-020-0404 | Open Problems in Integrable Systems — Around the Birkhoff conjecture | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1437 | 2104 / EP-413 | Erdős Problem #413 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1438 | 2112 / EP-423 | Erdős Problem #423 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1439 | 2129 / EP-461 | Erdős Problem #461 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1440 | 2131 / EP-463 | Erdős Problem #463 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1441 | 2132 / EP-467 | Erdős Problem #467 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1442 | 2141 / EP-486 | Erdős Problem #486 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1443 | 2142 / EP-488 | Erdős Problem #488 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1444 | 2150 / EP-509 | Erdős Problem #509 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1445 | 2164 / EP-535 | Erdős Problem #535 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1446 | 2166 / EP-538 | Erdős Problem #538 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1447 | 2214 / EP-616 | Erdős Problem #616 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1448 | 2248 / EP-676 | Erdős Problem #676 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1449 | 2249 / EP-677 | Erdős Problem #677 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1450 | 2259 / EP-689 | Erdős Problem #689 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1451 | 2271 / EP-708 | Erdős Problem #708 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1452 | 2272 / EP-709 | Erdős Problem #709 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1453 | 2273 / EP-710 | Erdős Problem #710 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1454 | 2274 / EP-711 | Erdős Problem #711 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1455 | 2282 / EP-727 | Erdős Problem #727 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1456 | 2283 / EP-730 | Erdős Problem #730 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1457 | 2291 / EP-757 | Erdős Problem #757 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1458 | 2300 / EP-778 | Erdős Problem #778 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1459 | 2307033 / AMR-022-7033 | Research Problems in Function Theory — Problem 7.33 | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1460 | 2334 / EP-839 | Erdős Problem #839 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1461 | 2343 / EP-854 | Erdős Problem #854 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1462 | 2364 / EP-885 | Erdős Problem #885 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1463 | 2366 / EP-887 | Erdős Problem #887 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1464 | 2389 / EP-933 | Erdős Problem #933 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1465 | 2398 / EP-944 | Erdős Problem #944 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1466 | 2440 / EP-1016 | Erdős Problem #1016 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1467 | 2447 / EP-1033 | Erdős Problem #1033 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1468 | 2461 / EP-1060 | Erdős Problem #1060 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1469 | 2499 / EP-1112 | Erdős Problem #1112 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1470 | 2503 / EP-1122 | Erdős Problem #1122 | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1471 | 2678 / KP-1.19 | Kirby Problem 1.19 | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1472 | 3000008 / AMR-029-0008 | Bounded degree matroid basis | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1473 | 3000017 / AMR-029-0017 | Complexity of the halting problem for Eulerian multigraphs | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1474 | 3000043 / AMR-029-0043 | Incomplete splitting-off in digraphs | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1475 | 3000050 / AMR-029-0050 | Making the union of two directed spanning trees strongly connected | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1476 | 3000065 / AMR-029-0065 | Partitioning a bipartite graph into proportional factors | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1477 | 3000088 / AMR-029-0088 | Weighted bipartite edge colouring | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1478 | 30006523 / OWR-14299904-005 | Weak-Order Convexity of Grothendieck Schubert Supports | 0.0720 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1479 | 30006666 / OWR-14299916-004 | Cross-Entropy Dynamics Beyond Hadamard Initialization | 0.0720 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1480 | 3100034 / AMR-030-0034 | Is it possible for a permutation on n symbols to contain exactly n | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1481 | 3142 / OPG-60055 | Chromatic number of $\frac{3}{3}$-power of graph | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1482 | 3348 / OPG-819 | A discrete iteration related to Pierce expansions | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1483 | 3377 / OPG-156 | Few subsequence sums in Z_n x Z_n | 0.0720 | 1 | unknown | queued | 0/5 |  |  |  |
| 1484 | 5500046 / AMR-054-0046 | 3D Minimum-Bend Orthogonal Graph Drawings | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1485 | 5500074 / AMR-054-0074 | Slicing Axes-Parallel Rectangles | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1486 | 8500006 / AMR-084-0006 | Triples having property D(n) for several parameters | 0.0720 | 4 | unknown | queued | 0/5 |  |  |  |
| 1487 | 8800050 / AMR-087-0050 | Monotonicity of maximal curve point counts in genus | 0.0720 | 3 | unknown | queued | 0/5 |  |  |  |
| 1488 | 30001671 / OWR-4791-031 | Monochromatic Concatenations of Permutation Words | 0.0719 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1489 | 30001907 / OWR-11138-004 | Koszul Differentials in Bousfield–Kuhn Homology | 0.0719 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1490 | 7500115 / AMR-074-0115 | Metrization of Proper MF Spaces | 0.0719 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1491 | 2700003 / AMR-026-0003 | Five Open Problems — Compressible Navier–Stokes near vacuum | 0.0718 | 4 | 2012 | queued | 0/5 |  |  |  |
| 1492 | 30002132 / OWR-12007-012 | Translated-Point Bounds for Small Contact Isotopies | 0.0718 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1493 | 5000002 / AMR-049-0002 | Types of vertices of reachable polygons | 0.0718 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1494 | 5000003 / AMR-049-0003 | Reachable points lie on reachable polygons | 0.0718 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1495 | 30002471 / OWR-12861-022 | Chromatic Uniqueness of Nonrepresentable Matroids | 0.0715 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1496 | 30004602 / OWR-4990374-005 | Third Weak Lefschetz Property for Arrangement Jacobian Quotients | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1497 | 30004615 / OWR-4990375-005 | Descent of Freeness for Orthogonal Modular Form Algebras | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1498 | 30004665 / OWR-7155441-008 | Exponent Criterion for Nonredundant String-Cone Inequalities | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1499 | 30004839 / OWR-8415347-017 | Gaussian Functionals on q-Deformed Compact Lie Groups | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1500 | 30004842 / OWR-8415347-020 | Genuine Finite-Growth Nichols Algebras over Nonabelian Groups | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1501 | 5100027 / AMR-050-0027 | Elliptic-billiard invariant k_{501} | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1502 | 5100028 / AMR-050-0028 | Elliptic-billiard invariant k_{502} | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1503 | 5100029 / AMR-050-0029 | Elliptic-billiard invariant k_{503} | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1504 | 5100039 / AMR-050-0039 | Elliptic-billiard invariant k_{701} | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1505 | 5100040 / AMR-050-0040 | Elliptic-billiard invariant k_{702} | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1506 | 5100041 / AMR-050-0041 | Elliptic-billiard invariant k_{703} | 0.0714 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1507 | 30005197 / OWR-11101917-006 | Cartan Subalgebras from Twisted Groupoid Subgroupoids | 0.0710 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1508 | 30003454 / OWR-15222-001 | Sampling Complexity of Hyperbolic-Cross Approximation | 0.0709 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1509 | 30003819 / OWR-16164-013 | Stanley Rank-Size Bounds for Differential Posets | 0.0707 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1510 | 30005411 / OWR-12697689-007 | Independent Defects and Rough Deep Ramification | 0.0705 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1511 | 30005741 / OWR-14298013-005 | Poisson Nilpotency and Solvability in Small Characteristics | 0.0705 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1512 | 30004190 / OWR-17130-003 | Mean-Curvature Blowup Limits of Wings and Pitchfork Translators | 0.0705 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1513 | 30004235 / OWR-17135-033 | Triangle Equation Hyperplane Arrangements | 0.0705 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1514 | 30004528 / OWR-2654827-004 | Universal Lefschetz Parameters for Neighborly Spheres | 0.0702 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1515 | 30004562 / OWR-2654831-005 | Bilinear Forms behind Resistor and Ising Integrable Equations | 0.0702 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1516 | 30004779 / OWR-8415342-007 | Component-Group Factorization on Dualizing Cohomology | 0.0698 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1517 | 30004898 / OWR-8415356-002 | Complexity of Submodular $k$-Partition | 0.0698 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1518 | 30004906 / OWR-8415356-017 | Approximating Maximum Nonsymmetric Principal Subdeterminants | 0.0698 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1519 | 30000294 / OWR-1058-002 | Uniform Difference-Quotient Estimates on Adaptive Meshes | 0.0693 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1520 | 30000418 / OWR-1189-008 | List-Labeling Equality for Trees | 0.0692 | 3 | 2006 | queued | 0/5 |  |  |  |
| 1521 | 30000732 / OWR-1536-002 | Fast Maker Constructions of Regular Graphs | 0.0691 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1522 | 30000921 / OWR-1787-006 | Polynomial Stability of Hypercyclic Entire Functions | 0.0690 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1523 | 30000973 / OWR-1971-006 | Equality of Alternate Moduli Spaces of Pointed Elliptic Curves | 0.0690 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1524 | 30006433 / OWR-14299523-005 | Degree of Topological Subalgebra Zeta Functions | 0.0690 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1525 | 30006435 / OWR-14299523-007 | Coincidence of Reduced and Topological Zeta Invariants | 0.0690 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1526 | 30005364 / OWR-12697686-002 | Trisection Distance Bounds from Nonseparating Hypersurfaces | 0.0690 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1527 | 30002007 / OWR-11580-014 | Verma-to-Wakimoto Isomorphisms for Jet-Level Characters | 0.0685 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1528 | 30002024 / OWR-11780-003 | Real Orbit Counts on Wonderful Varieties | 0.0685 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1529 | 30002297 / OWR-12339-003 | Frame Property of the Gaussian Gabor System on $\Lambda_3$ | 0.0684 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1530 | 30002453 / OWR-12732-005 | Recovery of Support $\tau$-Tilting Orders from $g$-Vectors | 0.0684 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1531 | 30006111 / OWR-14298804-014 | Two-Coloring Light Tournaments | 0.0684 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1532 | 30002522 / OWR-12868-007 | Periodicity of Stable Auslander Algebras | 0.0683 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1533 | 30002821 / OWR-13498-011 | Optimality of Greedy Circle Packings | 0.0681 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1534 | 30002968 / OWR-13943-002 | Snake-Graph Models for Generalized Cluster Variables | 0.0681 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1535 | 30002981 / OWR-13946-012 | Coranks of Modified Wahl Maps for Nodal Curves | 0.0681 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1536 | 30003030 / OWR-14211-005 | Geometry of Lattices from Finite Abelian Groups | 0.0679 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1537 | 30003317 / OWR-15181-008 | Distinct Extensions of Surreal Derivations | 0.0679 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1538 | 30003623 / OWR-15954-001 | Totik–Widom Bounds Beyond Parreau–Widom Sets | 0.0677 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1539 | 10400205 / AMR-103-0205 | Question 11.9 — (1) Find a surgery formula for the Kuperberg-Thurston in- variant [237] in terms of the Chern-Simons series of Questi… | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1540 | 1986 / EP-195 | Erdős Problem #195 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1541 | 20000044 / AIM-ALGEBRAIC_GEOMETRY-0044 | Odd-stem exponent two at C2 and a C4 transfer-kernel reduction | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1542 | 20000139 / AIM-ALGEBRAIC_GEOMETRY-0139 | A four-dimensional repair for symmetric surface classes on Mbar_0,7 | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1543 | 20000832 / AIM-ARITHMETIC_GEOMETRY-0078 | The generic very-compressed point for Hilbert function (1,4,10,a) | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1544 | 20002219 / AIM-LINEAR_ALGEBRA-0013 | Schur-ratio minima on bounded interval boxes | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1545 | 20002817 / AIM-REPRESENTATION_THEORY-0089 | Automorphism coarsenings and the reversal-quotient theory of U_n(q) | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1546 | 20002925 / AIM-TOPOLOGY-0013 | Essential tight bypasses in Ustilovsky five-sphere layers | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1547 | 20003198 / AIM-OTHER-0005 | All size moments for simultaneous cores with one modulus two | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1548 | 20003252 / AIM-OTHER-0059 | A finite four-generator target for a diagrammatic Haagerup-vine obstruction | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1549 | 2007 / EP-249 | Erdős Problem #249 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1550 | 2015 / EP-261 | Erdős Problem #261 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1551 | 2017 / EP-264 | Erdős Problem #264 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1552 | 2039 / EP-306 | Erdős Problem #306 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1553 | 2074 / EP-361 | Erdős Problem #361 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1554 | 2095 / EP-396 | Erdős Problem #396 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1555 | 2097 / EP-404 | Erdős Problem #404 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1556 | 2102 / EP-411 | Erdős Problem #411 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1557 | 2256 / EP-686 | Erdős Problem #686 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1558 | 2266 / EP-700 | Erdős Problem #700 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1559 | 2302 / EP-783 | Erdős Problem #783 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1560 | 2306112 / AMR-022-6112 | Research Problems in Function Theory — Problem 6.112 | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1561 | 2307057 / AMR-022-7057 | Research Problems in Function Theory — Problem 7.57 | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1562 | 2307058 / AMR-022-7058 | Research Problems in Function Theory — Problem 7.58 | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1563 | 2339 / EP-850 | Erdős Problem #850 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1564 | 2344 / EP-856 | Erdős Problem #856 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1565 | 2355 / EP-872 | Erdős Problem #872 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1566 | 2424 / EP-983 | Erdős Problem #983 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1567 | 2460 / EP-1059 | Erdős Problem #1059 | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1568 | 30006567 / OWR-14299906-003 | Quantum Automorphisms in Limiting Cuntz-Krieger Isometry Groups | 0.0675 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1569 | 30006660 / OWR-14299915-023 | Steenrod-Closed Parameter Ideals at Every Prime | 0.0675 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1570 | 3132 / OPG-49795 | Minimum number of arc-disjoint transitive subtournaments of order 3 in a tournament | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1571 | 3141 / OPG-60046 | 3-Edge-Coloring Conjecture | 0.0675 | 2 | unknown | queued | 0/5 |  |  |  |
| 1572 | 3169 / OPG-500 | Geodesic cycles and Tutte's Theorem | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1573 | 3194 / OPG-46533 | Coloring the union of degenerate graphs | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1574 | 3252 / OPG-59927 | List Colourings of Complete Multipartite Graphs with 2 Big Parts | 0.0675 | 1 | unknown | queued | 0/5 |  |  |  |
| 1575 | 3347 / OPG-791 | Quartic rationally derived polynomials | 0.0675 | 2 | unknown | queued | 0/5 |  |  |  |
| 1576 | 9700016 / AMR-096-0016 | Shortest Eulerian excursion on the Hamming cube | 0.0675 | 3 | unknown | queued | 0/5 |  |  |  |
| 1577 | 30004021 / OWR-16635-009 | Exceptional Isomorphism of Two W-Algebras | 0.0675 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1578 | 30006182 / OWR-14299084-004 | Information-Theoretic Additive Randomized Encodings | 0.0675 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1579 | 30006412 / OWR-14299521-004 | Angle Dependence of One-Phase Bernoulli Singularities | 0.0675 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1580 | 30004266 / OWR-17289-007 | Singular Loci of Maximal Flat Flag Degenerations | 0.0673 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1581 | 30004267 / OWR-17289-008 | Orbit Structure of Maximal Flat Flag Degenerations | 0.0673 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1582 | 30004272 / OWR-17290-002 | Self-Adjointness for Degenerate No-Tangency Metrics | 0.0673 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1583 | 30004677 / OWR-7155442-011 | Zigzagging Skips of Arithmetical Degrees | 0.0667 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1584 | 30004879 / OWR-8415354-005 | Invariant Involutions for Quantum Affine Evaluation Modules | 0.0667 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1585 | 30005309 / OWR-11695865-008 | Recursive Degree Formulas in Likelihood Geometry | 0.0663 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1586 | 30000107 / OWR-741-001 | Integrality of Constrained Polytope Families | 0.0661 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1587 | 30000035 / OWR-720-001 | Translation Invariance of Finitely Generated Shift-Invariant Spaces | 0.0661 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1588 | 6200063 / AMR-061-0063 | Boundaries of Groups and Kleinian Groups — Problem 63 | 0.0660 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1589 | 10000079 / AMR-099-0079 | Noise sensitivity under the Schaeffer bijection | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1590 | 10400031 / AMR-103-0031 | Problem 2.9 — (X.-S. | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1591 | 10400152 / AMR-103-0152 | Problem 8.6 — (V. | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1592 | 10600014 / AMR-105-0014 | Virtual-knot problem 14 — Brauer algebra | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1593 | 10800008 / AMR-107-0008 | Problem 2B — The same questions concerning the approximate solutions. | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1594 | 11000082 / AMR-109-0082 | Question 7.6 — Does spec(Ig(k)) have bounded multiplicity for k≥ 3? | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1595 | 11000091 / AMR-109-0091 | Problem 4.6 — Compute H • ∞(T c 3 ). | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1596 | 11000163 / AMR-109-0163 | Problem 2.6 — Schleimer has proved in [42] that each fixed 3-manifold M has a bound on the distances of its Heegaard splittings. | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1597 | 11000262 / AMR-109-0262 | Question 5 — Is there a homological definition of representations of the Birman-Wenzl- Murakami algebra? | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1598 | 11000308 / AMR-109-0308 | Problem 3.5 — Find explicit way of calculating d1(ϕ) for any given element ϕ ∈ Kg. | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1599 | 1101206 / AMR-010-1206 | Questions in Geometric Group Theory — Q 12.6 | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1600 | 1900010 / AMR-018-0010 | Geometry of Continued Fractions — Combinatorial structure of sails | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1601 | 20000092 / AIM-ALGEBRAIC_GEOMETRY-0092 | Crossed-product HHH enhancements and the component-collapse obstruction | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1602 | 20000115 / AIM-ALGEBRAIC_GEOMETRY-0115 | A separable odd-degree parametrization of the characteristic-2 Fermat cubic | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1603 | 20001003 / AIM-COMBINATORICS-0128 | Recognizing undirected reduced Laplacian lattices | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1604 | 20001175 / AIM-COMPUTATION-0013 | Coordinate-covariant orientation laws for no-trade regions | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1605 | 20001256 / AIM-COMPUTATION-0094 | Irreducible line sections: exact convention-sensitive counts and monodromy status | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1606 | 20002465 / AIM-PDES-0077 | Quadratic-chain characterization of the Aubry set | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1607 | 20002477 / AIM-PDES-0089 | Exact-energy reachability at the universal Mañé critical value | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1608 | 20002656 / AIM-PROBABILITY-0098 | A quantitative near-equilibrium threshold for KPZ-scale fluctuations | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1609 | 20002960 / AIM-TOPOLOGY-0048 | Circle gluing as balanced endomorphism extraction | 0.0660 | 4 | unknown | queued | 0/5 |  |  |  |
| 1610 | 2100405 / AMR-020-0405 | Open Problems in Integrable Systems — Geometry of caustics, invariant surfaces, and commuting billiard maps | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1611 | 2100502 / AMR-020-0502 | Open Problems in Integrable Systems — Bi-Poisson vector spaces | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1612 | 2307027 / AMR-022-7027 | Research Problems in Function Theory — Problem 7.27 | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1613 | 3000015 / AMR-029-0015 | Complexity of computing the rotor-router action | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1614 | 3000021 / AMR-029-0021 | Covering a crossing supermodular function with graph edges | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1615 | 3000026 / AMR-029-0026 | Deciding the validity of the score sequence of a soccer tournament | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1616 | 30006533 / OWR-14299904-015 | Optimization over Nonzero Littlewood–Richardson Coefficients | 0.0660 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1617 | 30006570 / OWR-14299906-007 | Quantum Advantage in Threefold Repetition of Feige’s Game | 0.0660 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1618 | 3064 / OPG-369 | Bases of many weights | 0.0660 | 2 | unknown | queued | 0/5 |  |  |  |
| 1619 | 3309 / OPG-1757 | Negative association in uniform forests | 0.0660 | 1 | unknown | queued | 0/5 |  |  |  |
| 1620 | 5500058 / AMR-054-0058 | Monochromatic Triangles | 0.0660 | 3 | unknown | queued | 0/5 |  |  |  |
| 1621 | 30000607 / OWR-1386-014 | Codegree Thresholds for Hypergraph Matchings | 0.0659 | 3 | 2006 | queued | 0/5 |  |  |  |
| 1622 | 30000889 / OWR-1739-003 | Multiplicity Decoding for Order-Domain Codes | 0.0658 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1623 | 30005416 / OWR-12697689-012 | Arc Hilbert–Poincaré Series of ADE Surface Singularities | 0.0658 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1624 | 30005436 / OWR-12697693-007 | Structure Groups of Anisotropic Bilinear Forms | 0.0658 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1625 | 30005476 / OWR-12697711-010 | Spectrality of Infinite Symmetric Orbit-Space Quotients | 0.0658 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1626 | 30005533 / OWR-13750334-003 | Patchworking and Twisted Real Quintics | 0.0658 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1627 | 4000008 / AMR-039-0008 | Isoperimetric profile and curvature at infinity | 0.0657 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1628 | 30001703 / OWR-4798-030 | Equality Cases in Lower Bounds for Triangulated 3-Manifolds | 0.0654 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1629 | 30001876 / OWR-11135-003 | Restriction Spectra of $\operatorname{GL}_3$ Maass Forms | 0.0654 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1630 | 30002859 / OWR-13677-003 | Baire Category of Purely Singular Copulas | 0.0648 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1631 | 30000041 / OWR-720-009 | Sharp $L^1$ Bounds for Approximate Convolution Idempotents | 0.0645 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1632 | 30000254 / OWR-1050-003 | Interior-Layer Peaks in Singularly Perturbed Elliptic Problems | 0.0644 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1633 | 30003729 / OWR-15991-001 | Perturbed Ergodic Constants in Hamilton–Jacobi Equations | 0.0643 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1634 | 30003990 / OWR-16633-006 | Convergence Rates for Convex-Body Bounds | 0.0643 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1635 | 30000663 / OWR-1452-027 | Unramified Quotients of Equivariant Endomorphisms | 0.0642 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1636 | 30000918 / OWR-1787-002 | Universal Faber Series Versus Universal Taylor Series | 0.0641 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1637 | 30000964 / OWR-1970-002 | Moderate Deviations for Chaotic Analytic Zeros | 0.0641 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1638 | 30001110 / OWR-2492-001 | Principality of Artin–Schreier Deformation Ideals | 0.0641 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1639 | 3700021 / AMR-036-0021 | Small components of subharmonic level sets | 0.0641 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1640 | 30001248 / OWR-3473-009 | Triangle-Count Equidistribution and Local Limits | 0.0640 | 3 | 2009 | queued | 0/5 |  |  |  |
| 1641 | 30002005 / OWR-11580-012 | Height Bounds for Covering Relations in Wonderful Varieties | 0.0636 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1642 | 30002318 / OWR-12481-003 | Concentration of Largest Triangular Submatrices in Random Matrices | 0.0635 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1643 | 30002470 / OWR-12861-021 | Spanning Near-Squares of Odd Cycles | 0.0634 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1644 | 10000003 / AMR-099-0003 | Equilibrium point configurations on the line | 0.0632 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1645 | 30002880 / OWR-13681-014 | Bilax Monoidal Structures for Stable Morita Equivalences | 0.0632 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1646 | 30002949 / OWR-13860-006 | Agreement of Affine Deligne–Lusztig Stratifications | 0.0632 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1647 | 30002969 / OWR-13943-004 | Lamination Realization of Higher Tropical Friezes | 0.0632 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1648 | 30005241 / OWR-11101924-004 | Infinite Tails of Multiple-Scattering Series | 0.0631 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1649 | 30005317 / OWR-11695867-002 | Twenty-Vertex Models and Pachter-Triangle Tilings | 0.0631 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1650 | 2900001 / AMR-028-0001 | Betti Posets and the Stanley Depth | 0.0631 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1651 | 30003042 / OWR-14213-008 | Schubert Classes in the Gamma Filtration | 0.0631 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1652 | 10900050 / AMR-108-0050 | 7.2 (Long) — Clique numbers in unit- and prime-difference graphs | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1653 | 155 / GREEN-067 | Affine Translates of {0,1,3} | 0.0630 | 1 | unknown | queued | 0/5 |  |  |  |
| 1654 | 20000689 / AIM-ANALYTIC_NUMBER_THEORY-0053 | Asymmetric lengths: a safe-range obstruction and conductor-matched boundary cancellation | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1655 | 20002813 / AIM-REPRESENTATION_THEORY-0085 | Canonical supercharacter products: an exact divisibility criterion | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1656 | 20002846 / AIM-SEVERAL_COMPLEX_VARIABLES-0004 | A weighted planar reduction for the logarithmic test function on the smooth worm | 0.0630 | 4 | unknown | queued | 0/5 |  |  |  |
| 1657 | 20003213 / AIM-OTHER-0020 | An elementary gap-swap bijection for the dihedral row and a path reduction of AJ | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1658 | 2026 / EP-278 | Erdős Problem #278 | 0.0630 | 1 | unknown | queued | 0/5 |  |  |  |
| 1659 | 2118 / EP-432 | Erdős Problem #432 | 0.0630 | 1 | unknown | queued | 0/5 |  |  |  |
| 1660 | 2200014 / AMR-021-0014 | Problems Around Polynomials — Conjecture 9 | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1661 | 2200015 / AMR-021-0015 | Problems Around Polynomials — Conjecture 10 | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1662 | 2306062 / AMR-022-6062 | Research Problems in Function Theory — Problem 6.62 | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1663 | 2307072 / AMR-022-7072 | Research Problems in Function Theory — Problem 7.72 | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1664 | 2307073 / AMR-022-7073 | Research Problems in Function Theory — Problem 7.73 | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1665 | 2307081 / AMR-022-7081 | Research Problems in Function Theory — Problem 7.81 | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1666 | 2308008 / AMR-022-8008 | Research Problems in Function Theory — Problem 8.8 | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1667 | 2308024 / AMR-022-8024 | Research Problems in Function Theory — Problem 8.24 | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1668 | 2309012 / AMR-022-9012 | Research Problems in Function Theory — Problem 9.12 | 0.0630 | 3 | unknown | queued | 0/5 |  |  |  |
| 1669 | 2390 / EP-934 | Erdős Problem #934 | 0.0630 | 1 | unknown | queued | 0/5 |  |  |  |
| 1670 | 2430 / EP-995 | Erdős Problem #995 | 0.0630 | 1 | unknown | queued | 0/5 |  |  |  |
| 1671 | 2497 / EP-1110 | Erdős Problem #1110 | 0.0630 | 1 | unknown | queued | 0/5 |  |  |  |
| 1672 | 3223 / OPG-323 | Antichains in the cycle continuous order | 0.0630 | 1 | unknown | queued | 0/5 |  |  |  |
| 1673 | 3295 / OPG-46817 | Simultaneous partition of hypergraphs | 0.0630 | 1 | unknown | queued | 0/5 |  |  |  |
| 1674 | 3317 / OPG-34915 | 3-Colourability of Arrangements of Great Circles | 0.0630 | 1 | unknown | queued | 0/5 |  |  |  |
| 1675 | 30003386 / OWR-15212-005 | Deterministic Transport Under Mutual Multiphase Domination | 0.0629 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1676 | 30003446 / OWR-15219-016 | Shortest Moment Extensions and Minimal Atomic Measures | 0.0629 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1677 | 30003561 / OWR-15581-008 | Relations Between Arithmetic Milnor Invariants | 0.0629 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1678 | 30003587 / OWR-15585-006 | Strong Approximate Innerness of Quasi-Free Actions | 0.0629 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1679 | 30005349 / OWR-12697684-028 | Biased Sub-Balanced Slices of Boolean Functions | 0.0627 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1680 | 30005379 / OWR-12697687-001 | Slice-Genus Bounds for Homogeneous Braid Quasimorphisms | 0.0627 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1681 | 30004097 / OWR-16773-003 | Inner Automorphisms in the Fourth Antipode Formula | 0.0625 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1682 | 30004145 / OWR-16933-007 | Embedding Spaces of Divisors on Real Cubics | 0.0625 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1683 | 30004269 / OWR-17289-010 | Dyck-Path Inequalities for Newton–Okounkov Polytopes | 0.0625 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1684 | 30004270 / OWR-17289-013 | Hasse-Graph Descriptions of Valuation Semigroups | 0.0625 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1685 | 30004503 / OWR-1703872-011 | Plancherel Volumes of Rankin–Selberg Metric Balls | 0.0622 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1686 | 30005893 / OWR-14298366-005 | Global Convergence of Low-Rank Multi-Penalty Optimization | 0.0621 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1687 | 30006107 / OWR-14298804-009 | Finite Strategies in the Distance Game | 0.0621 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1688 | 30006109 / OWR-14298804-012 | Approximating Fare-Zone Assignment on Trees | 0.0621 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1689 | 30004608 / OWR-4990374-014 | Unexpected Curves from Plus-One Generated Arrangements | 0.0619 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1690 | 30004664 / OWR-7155441-007 | Redundant Inequalities in String Cones | 0.0619 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1691 | 30004888 / OWR-8415355-010 | Operator Relations on Yified Khovanov–Rozansky Homology | 0.0619 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1692 | 30005019 / OWR-9790358-018 | Relations among Adjoint Curves from Cyclic Point Orders | 0.0616 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1693 | 30005126 / OWR-10252931-004 | Coincidence of Degeneration Orders for Representation-Directed Algebras | 0.0616 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1694 | 30005434 / OWR-12697693-005 | Semilattice Realizations by Wedge Semibraces | 0.0611 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1695 | 30005925 / OWR-14298372-008 | Free Polar Decomposition Under a Nondegeneracy Condition | 0.0606 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1696 | 10000041 / AMR-099-0041 | Ends of transient branching random walk | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1697 | 10400214 / AMR-103-0214 | Problem 12.8 — Construct an invariant of KTG’s from configuration space in- tegrals in a natural way. | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1698 | 11000286 / AMR-109-0286 | Question 3.6 — Is there a map Out(Fn)→ Out(Fm) that induces an isomorphism on homology in the stable range? | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1699 | 1900017 / AMR-018-0017 | Geometry of Continued Fractions — Sail statistics | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1700 | 20000157 / AIM-ALGEBRAIC_GEOMETRY-0157 | Ordinary thick closure of representation spheres for finite groups | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1701 | 20000996 / AIM-COMBINATORICS-0121 | A diagonal-lattice reduction for the tropical Picard group of a product of graphs | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1702 | 20003174 / AIM-TOPOLOGY-0262 | Quotient Ricci flow as a coupled and weighted super-Ricci flow | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1703 | 2100702 / AMR-020-0702 | Open Problems in Integrable Systems — Integrability and Quantisation | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1704 | 2100706 / AMR-020-0706 | Open Problems in Integrable Systems — Integrability and Quantisation | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1705 | 2100708 / AMR-020-0708 | Open Problems in Integrable Systems — Integrability and Quantisation | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1706 | 9500004 / AMR-094-0004 | Efficient couplings in acute triangles | 0.0600 | 3 | unknown | queued | 0/5 |  |  |  |
| 1707 | 30003925 / OWR-16412-005 | Smooth Stein Neighborhood Domains Beyond One H Convexity | 0.0600 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1708 | 30003953 / OWR-16415-016 | Rectifiable Nonsmooth Limit Curves of Anosov Representations | 0.0600 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1709 | 6000010 / AMR-059-0010 | Tangent-Bundle Symplectic and Almost Complex Structures | 0.0599 | 3 | 1998 | queued | 0/5 |  |  |  |
| 1710 | 30006265 / OWR-14299283-001 | Representation-Theoretic Meaning of Steinberg Quotient Characters | 0.0598 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1711 | 30001058 / OWR-2090-008 | Optimal Dilation Thresholds for Ehrhart $\delta$-Polynomials | 0.0592 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1712 | 4000005 / AMR-039-0005 | Non-reversible spectral gap | 0.0592 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1713 | 30001514 / OWR-4412-004 | Boundary Gradient Attainment in the Affine Plateau Problem | 0.0590 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1714 | 30001560 / OWR-4425-017 | Nonvanishing Hankel Determinants of Morphic Sequences | 0.0590 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1715 | 30001617 / OWR-4531-020 | Law-of-Iterated-Logarithm Bounds for Dyadic Martingales | 0.0590 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1716 | 30001764 / OWR-5148-006 | Undetermined Coefficients in Universal Residual Polynomials | 0.0589 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1717 | 30001869 / OWR-11133-003 | Newton–Okounkov Bodies of Bott–Samelson Varieties | 0.0589 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1718 | 7500120 / AMR-074-0120 | Well-Ordered Linearizations | 0.0589 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1719 | 30002198 / OWR-12170-005 | Hilbert-Series Factorization for Finite-Dimensional Nichols Algebras | 0.0588 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1720 | 30002233 / OWR-12176-001 | Surjectivity on Component Groups of Semistable Curves | 0.0588 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1721 | 30002303 / OWR-12339-009 | Muckenhoupt Thresholds for Integer-Translate Schauder Bases | 0.0586 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1722 | 10000049 / AMR-099-0049 | Liouville extensions by an isometric integer action | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1723 | 10400226 / AMR-103-0226 | Problem 12.21 — (Y. | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1724 | 10600051 / AMR-105-0051 | Virtual-knot problem 51 — Prove or disprove the conjecture about the non-uniqueness of minimal representative of a free link, i.e. | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1725 | 1901 / EP-44 | Erdős Problem #44 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1726 | 1987 / EP-196 | Erdős Problem #196 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1727 | 20000125 / AIM-ALGEBRAIC_GEOMETRY-0125 | Smooth hypersurfaces beyond the Chevalley--Warning range | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1728 | 20000357 / AIM-ALGEBRAIC_NUMBER_THEORY-0009 | Density degrees under finite covers | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1729 | 20000440 / AIM-ALGEBRAIC_NUMBER_THEORY-0092 | A finite binary criterion for Brauer-compatible lifts to an Enriques K3 cover | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1730 | 20000735 / AIM-ANALYTIC_NUMBER_THEORY-0099 | A Bailey-Chebyshev-Bloch dictionary and terminal-choice blindness | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1731 | 20003203 / AIM-OTHER-0010 | Measure-sensitive resonance and PL-versus-birational period rigidity | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1732 | 2035 / EP-295 | Erdős Problem #295 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1733 | 2052 / EP-326 | Erdős Problem #326 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1734 | 2091 / EP-389 | Erdős Problem #389 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1735 | 2110 / EP-421 | Erdős Problem #421 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1736 | 2152 / EP-513 | Erdős Problem #513 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1737 | 2165 / EP-536 | Erdős Problem #536 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1738 | 2252 / EP-681 | Erdős Problem #681 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1739 | 2307078 / AMR-022-7078 | Research Problems in Function Theory — Problem 7.78 | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1740 | 2309008 / AMR-022-9008 | Research Problems in Function Theory — Problem 9.8 | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1741 | 2350 / EP-864 | Erdős Problem #864 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1742 | 2376 / EP-906 | Erdős Problem #906 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1743 | 2449 / EP-1038 | Erdős Problem #1038 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1744 | 2450 / EP-1039 | Erdős Problem #1039 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1745 | 2485 / EP-1095 | Erdős Problem #1095 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1746 | 3047 / OPG-37222 | Dividing up the unrestricted partitions | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1747 | 3100047 / AMR-030-0047 | Is the 1/3-2/3 Conjecture for Pressing Sequences true | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1748 | 3100082 / AMR-030-0082 | Consider p(v, t), the probability that a walk beginning from the origin ends at the point v on the d-dimensional integer | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1749 | 3100089 / AMR-030-0089 | Let G be a bicolored graph, and let H be the graph whose vertices are the valid pressing sequences of G and whose edges | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1750 | 3109 / OPG-37182 | Odd cycles and low oddness | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1751 | 3200 / OPG-388 | List colorings of edge-critical graphs | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1752 | 3209 / OPG-434 | Weak pentagon problem | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1753 | 3251 / OPG-56230 | 2-colouring a graph without a monochromatic maximum clique | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1754 | 3276 / OPG-1808 | Monochromatic reachability or rainbow triangles | 0.0585 | 2 | unknown | queued | 0/5 |  |  |  |
| 1755 | 3326 / OPG-596 | Linear Hypergraphs with Dimension 3 | 0.0585 | 1 | unknown | queued | 0/5 |  |  |  |
| 1756 | 3327 / OPG-172 | Consecutive non-orientable embedding obstructions | 0.0585 | 2 | unknown | queued | 0/5 |  |  |  |
| 1757 | 5500059 / AMR-054-0059 | Most Circular Partition of a Square | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1758 | 5500068 / AMR-054-0068 | Rolling a Die over a Labeled Board | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1759 | 8800049 / AMR-087-0049 | Detecting Jacobians via criteria and Deligne modules | 0.0585 | 3 | unknown | queued | 0/5 |  |  |  |
| 1760 | 2800905 / AMR-027-0905 | 10 Lectures and 42 Open Problems — Positive PCA tightness | 0.0584 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1761 | 30002861 / OWR-13678-002 | Cubic Spline Interpolation on General Triangulations | 0.0584 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1762 | 3700039 / AMR-036-0039 | Median inequality for three subharmonic functions | 0.0584 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1763 | 30003185 / OWR-14745-003 | Complexity of Bray’s Involution-Centralizer Algorithm | 0.0582 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1764 | 30003208 / OWR-14748-016 | Von Neumann Generation of the Algebra T-Psi | 0.0582 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1765 | 30003225 / OWR-14754-011 | Contact Loci and Nash Sets of Prime Divisors | 0.0582 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1766 | 30003375 / OWR-15208-029 | Harmonic Fibrations of Exotic Complex Projective Space Bundles | 0.0580 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1767 | 30003527 / OWR-15575-006 | Movable Invariant Neighborhoods of Compact Flow Sets | 0.0580 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1768 | 30003758 / OWR-15999-007 | Extrapolating Clusterings from Semidefinite Subsamples | 0.0579 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1769 | 30003809 / OWR-16163-011 | Distributions of Self-Adjoint Bimonotone Limit Operators | 0.0579 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1770 | 30003821 / OWR-16164-019 | Pattern-Avoidance Inequalities on Digitally Convex Shapes | 0.0579 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1771 | 30003992 / OWR-16633-009 | Fast Low-Rank Maximum-Weight Assignment | 0.0579 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1772 | 30004307 / OWR-17294-007 | Second-Cohomology Torsion of Finite Abelian Quandles | 0.0576 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1773 | 30004316 / OWR-17294-017 | Bijectivity of the Quantum Symmetrizer | 0.0576 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1774 | 30004534 / OWR-2654827-016 | Eventual Lefschetz Dichotomies for Symmetric Ideal Chains | 0.0574 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1775 | 30004611 / OWR-4990374-017 | Exact Sequences for Logarithmic Derivation Sheaves | 0.0571 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1776 | 30005160 / OWR-11101912-009 | Strict Majorant Properties at Fixed Noneven Exponents | 0.0568 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1777 | 30005572 / OWR-13750341-006 | Eisenstein Maps from Bianchi Homology to K2 | 0.0564 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1778 | 30005770 / OWR-14298158-015 | Diagonal Permuton Limits for Skew-Sum Avoidance | 0.0559 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1779 | 30004514 / OWR-1703876-007 | Barycentric Hyperplanes Through Convex Body Centroids | 0.0553 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1780 | 30006230 / OWR-14299093-005 | Converse Bessel-Pair Criterion for Grushin Operators | 0.0552 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1781 | 30000043 / OWR-720-011 | Wavelet Structure of Canonical Tight Frames | 0.0545 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1782 | 30000215 / OWR-822-007 | Theoretical Certification of Crossing-Number Optimality | 0.0545 | 3 | 2005 | queued | 0/5 |  |  |  |
| 1783 | 30000386 / OWR-1183-006 | The Two-Dimensional Time-Bomb Conjecture | 0.0544 | 3 | 2006 | queued | 0/5 |  |  |  |
| 1784 | 30001101 / OWR-2489-006 | Alcuin Numbers and Recognition of Small Boat Graphs | 0.0542 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1785 | 10000037 / AMR-099-0037 | Uniqueness of percolation on graphs roughly isometric to lattices | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1786 | 10400007 / AMR-103-0007 | Problem 1.7 — (J. | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1787 | 10400168 / AMR-103-0168 | Problem 9.4 — (Y. | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1788 | 11000165 / AMR-109-0165 | Problem 2.8 — Recall that we noted, earlier, that every genus g Heegaard splitting of every homology 3-sphere is obtained by allowi… | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1789 | 169 / GREEN-081 | Covering by Random Translates | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1790 | 1970 / EP-168 | Erdős Problem #168 | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1791 | 2000006 / AMR-019-0006 | Some Open Problems in Elasticity — A positive Jacobian bound | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1792 | 20000188 / AIM-ALGEBRAIC_GEOMETRY-0188 | Joint-monodromy degree classification and branch-overlap smoothness budget | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1793 | 20000200 / AIM-ALGEBRAIC_GEOMETRY-0200 | Torsion-logarithmic obstructions and realizable Euclidean signature lines | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1794 | 20000698 / AIM-ANALYTIC_NUMBER_THEORY-0062 | A square-root shifted-divisor hypothesis for the Conrey--Keating one-swap block | 0.0540 | 4 | unknown | queued | 0/5 |  |  |  |
| 1795 | 20000699 / AIM-ANALYTIC_NUMBER_THEORY-0063 | A quantitative Möbius–ratios–prime bridge | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1796 | 20000709 / AIM-ANALYTIC_NUMBER_THEORY-0073 | High moments of a prime Dirichlet polynomial: collision corrections and a finite-height cutoff | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1797 | 20002190 / AIM-INFRASTRUCTURE-0090 | Fixed-ambient extraction of roots of finite Frobenius modules | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1798 | 20002863 / AIM-SEVERAL_COMPLEX_VARIABLES-0021 | A polar-edge uniqueness criterion for removable meromorphic singularities | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1799 | 20002951 / AIM-TOPOLOGY-0039 | Explicit peripheral relations for 2-bridge knots | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1800 | 2047 / EP-321 | Erdős Problem #321 | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1801 | 2307062 / AMR-022-7062 | Research Problems in Function Theory — Problem 7.62 | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1802 | 2308013 / AMR-022-8013 | Research Problems in Function Theory — Problem 8.13 | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1803 | 2319 / EP-817 | Erdős Problem #817 | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1804 | 2320 / EP-819 | Erdős Problem #819 | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1805 | 2358 / EP-876 | Erdős Problem #876 | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1806 | 2413 / EP-963 | Erdős Problem #963 | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1807 | 2419 / EP-973 | Erdős Problem #973 | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1808 | 2463 / EP-1062 | Erdős Problem #1062 | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1809 | 2501 / EP-1117 | Erdős Problem #1117 | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1810 | 2506 / EP-1131 | Erdős Problem #1131 | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1811 | 3000010 / AMR-029-0010 | Changing conservative weightings in bipartite graphs | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1812 | 3000053 / AMR-029-0053 | Maximum weight bounded fractional matching | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1813 | 3000064 / AMR-029-0064 | Partition median problem | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1814 | 3000080 / AMR-029-0080 | Smooth well-balanced orientations with prescribed in-degrees | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1815 | 30006626 / OWR-14299911-028 | Characterization of Graphical Apiculate and Generalized Median Algebras | 0.0540 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1816 | 3039 / OPG-478 | Rainbow AP(4) in an almost equinumerous coloring | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1817 | 3100003 / AMR-030-0003 | For every non-equilateral triangle T, show that it is possible to color the plane with three colors so that there is no | 0.0540 | 2 | unknown | queued | 0/5 |  |  |  |
| 1818 | 3227 / OPG-401 | Circular coloring triangle-free subcubic planar graphs | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1819 | 3264 / OPG-46432 | Ádám's Conjecture | 0.0540 | 2 | unknown | queued | 0/5 |  |  |  |
| 1820 | 3700006 / AMR-036-0006 | Completely invariant Fatou components | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1821 | 8700065 / AMR-086-0065 | Question 5.2 — Bugeaud | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1822 | 8800068 / AMR-087-0068 | Worst cases for LLL on ideal lattices | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1823 | 98 / GREEN-006 | Sum-Free Subsets of [N]^d | 0.0540 | 1 | unknown | queued | 0/5 |  |  |  |
| 1824 | 9900006 / AMR-098-0006 | Coupling characterization of setwise asymptotic stationarity | 0.0540 | 3 | unknown | queued | 0/5 |  |  |  |
| 1825 | 30002421 / OWR-12723-007 | Discrepancy Lower Bounds for Line Unions in Three Dimensions | 0.0537 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1826 | 30002547 / OWR-12872-018 | Growth Rate of Quadrant Loops | 0.0536 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1827 | 30002723 / OWR-13353-006 | Complexity of Extremality Testing in Infinite Group Problems | 0.0536 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1828 | 30002726 / OWR-13353-012 | Complexity of Maximizing Initial Odd Ears | 0.0536 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1829 | 30003094 / OWR-14226-001 | Low-Rank Splitting Error Analysis for Discretized PDEs | 0.0534 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1830 | 30003253 / OWR-15170-020 | Differential Criteria for Low-Genus Curves on Surfaces | 0.0534 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1831 | 30003547 / OWR-15579-004 | Composition of Positive-Scalar-Curvature Concordance Classes | 0.0532 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1832 | 30003773 / OWR-16158-016 | Geometric Chern Classes in Arakelov Cobordism | 0.0530 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1833 | 30003983 / OWR-16629-009 | Decomposition of Equiangular Tight Frames | 0.0530 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1834 | 30004154 / OWR-16938-002 | Exact Higher-Order Matrix Decomposability | 0.0528 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1835 | 30000859 / OWR-1731-004 | RSW Theory for Anisotropic Square-Lattice Percolation | 0.0527 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1836 | 30002028 / OWR-11781-001 | Supersaturation Blow-Ups in Uniform Hypergraphs | 0.0522 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1837 | 30002123 / OWR-12006-004 | Shellability of Barycentric Subdivisions of Convex Complexes | 0.0522 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1838 | 30002169 / OWR-12013-001 | Intrinsic Viscosity Solutions for Rough Hamilton–Jacobi Equations | 0.0522 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1839 | 30005048 / OWR-9790364-002 | Elementary Proofs of Laguerre–Pólya Total Positivity | 0.0521 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1840 | 30005111 / OWR-10252930-021 | Elementary Proof of the Closed Walk Stacking Criterion | 0.0521 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1841 | 30003131 / OWR-14604-008 | Quadratic-Length Universal Random Permutations | 0.0517 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1842 | 30003172 / OWR-14741-004 | Simultaneously Adaptive Universal Source Coding | 0.0517 | 3 | 2016 | queued | 0/5 |  |  |  |
| 1843 | 30005478 / OWR-12697711-014 | Algorithms for Amoeba Dimensions from Tropical Fans | 0.0517 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1844 | 30005529 / OWR-13750333-010 | Compatible Geodesic and Horocycle Symbolic Codings | 0.0517 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1845 | 30005732 / OWR-14298011-003 | Well-Defined Trajectories in Controlled Set Motions | 0.0517 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1846 | 30005740 / OWR-14298013-004 | BV Structures with Nonsemisimple Nakayama Automorphisms | 0.0517 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1847 | 30003654 / OWR-15957-007 | Certificates of Polynomial Nonnegativity in Copositive Optimization | 0.0516 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1848 | 30005757 / OWR-14298158-002 | Rationality of Separable Permutation Subclasses | 0.0513 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1849 | 30004262 / OWR-17288-004 | Finite-Dimensional Uniform Embeddings of Compact Metric Spaces | 0.0512 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1850 | 30004632 / OWR-4990379-002 | Global Optimality of Domain-Decomposition Transport Algorithms | 0.0508 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1851 | 30005646 / OWR-14297740-018 | Strict Higher Étale-Homotopy Obstructions over Global Fields | 0.0502 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1852 | 30005647 / OWR-14297740-019 | Next-Most-Probable Galois Groups of Random Polynomials | 0.0502 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1853 | 6000013 / AMR-059-0013 | Affine Vertices and Inflection Points | 0.0499 | 3 | 1998 | queued | 0/5 |  |  |  |
| 1854 | 30005762 / OWR-14298158-007 | Rationality Below Growth Rate Four | 0.0497 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1855 | 30006081 / OWR-14298796-001 | Adjoint-Free Approximation of Nonsymmetric Low-Rank Matrices | 0.0497 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1856 | 1963 / EP-156 | Erdős Problem #156 | 0.0495 | 1 | unknown | queued | 0/5 |  |  |  |
| 1857 | 20000012 / AIM-ALGEBRAIC_GEOMETRY-0012 | Cox-chart Morse theory for cellular virtual resolutions | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1858 | 20000143 / AIM-ALGEBRAIC_GEOMETRY-0143 | Exact boundary mobility counts and explicit mixed-face estimates | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1859 | 20000204 / AIM-ALGEBRAIC_GEOMETRY-0204 | Edge and tritangent surfaces are the only generic smooth visual-hull event types | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1860 | 20000566 / AIM-ANALYSIS-0098 | Fixed-diagonal geometry and an exact 4x4 two-paving profile | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1861 | 20000691 / AIM-ANALYTIC_NUMBER_THEORY-0055 | Quadratic moments, Poisson squares, and swap terms | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1862 | 20000707 / AIM-ANALYTIC_NUMBER_THEORY-0071 | Smoothed second moments and the sigma=1 boundary term | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1863 | 20000721 / AIM-ANALYTIC_NUMBER_THEORY-0085 | Orbifold expansions of the mirror-quintic free energies | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1864 | 20001237 / AIM-COMPUTATION-0075 | Saturation-aware exceptional likelihood fibers and the 2x2 independence locus | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1865 | 20001341 / AIM-CRYPTOGRAPHY-0028 | Explicit near-minimal units from the golden-ratio radical | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1866 | 2218 / EP-624 | Erdős Problem #624 | 0.0495 | 1 | unknown | queued | 0/5 |  |  |  |
| 1867 | 2225 / EP-635 | Erdős Problem #635 | 0.0495 | 1 | unknown | queued | 0/5 |  |  |  |
| 1868 | 2285 / EP-734 | Erdős Problem #734 | 0.0495 | 1 | unknown | queued | 0/5 |  |  |  |
| 1869 | 2299 / EP-776 | Erdős Problem #776 | 0.0495 | 1 | unknown | queued | 0/5 |  |  |  |
| 1870 | 2401 / EP-949 | Erdős Problem #949 | 0.0495 | 1 | unknown | queued | 0/5 |  |  |  |
| 1871 | 3000040 / AMR-029-0040 | Gonality and edge subdivisions | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1872 | 3000062 / AMR-029-0062 | Orientation-compatible w-vertex cover | 0.0495 | 3 | unknown | queued | 0/5 |  |  |  |
| 1873 | 30006522 / OWR-14299904-004 | Weak-Order Growth of Grothendieck Schubert Supports | 0.0495 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1874 | 30006595 / OWR-14299909-010 | Modularity of Higher-$t$ Generating-Function Coefficients | 0.0495 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1875 | 3154 / OPG-36933 | Asymptotic Distribution of Form of Polyhedra | 0.0495 | 1 | unknown | queued | 0/5 |  |  |  |
| 1876 | 3321 / OPG-322 | Drawing disconnected graphs on surfaces | 0.0495 | 1 | unknown | queued | 0/5 |  |  |  |
| 1877 | 30001258 / OWR-3476-007 | Sublinear Lane–Emden Ground-State Asymptotics | 0.0492 | 3 | 2009 | queued | 0/5 |  |  |  |
| 1878 | 30001414 / OWR-4209-004 | Boundary Conditions Preserving Optimal Hardy–Sobolev Constants | 0.0491 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1879 | 30001553 / OWR-4425-008 | Sharp Bounds for Alternating Involution Periods | 0.0491 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1880 | 30001558 / OWR-4425-014 | Fragile and Robust Squarefree Infinite Words | 0.0491 | 3 | 2010 | queued | 0/5 |  |  |  |
| 1881 | 30002208 / OWR-12173-004 | Additive Sets Preserving Piecewise Syndeticity | 0.0490 | 3 | 2012 | queued | 0/5 |  |  |  |
| 1882 | 30002506 / OWR-12866-016 | Bohr-Radius Characterization of $\ell^1$ | 0.0488 | 3 | 2014 | queued | 0/5 |  |  |  |
| 1883 | 30002965 / OWR-13941-005 | Volume of the Boolean Quadric Polytope | 0.0486 | 3 | 2015 | queued | 0/5 |  |  |  |
| 1884 | 10400211 / AMR-103-0211 | Conjecture 12.5 — (Y. | 0.0480 | 3 | unknown | queued | 0/5 |  |  |  |
| 1885 | 10400212 / AMR-103-0212 | Problem 12.6 — Find a new proof of the existence of a universal Vassiliev in- variant of knots, presenting them by KTG’s and their o… | 0.0480 | 3 | unknown | queued | 0/5 |  |  |  |
| 1886 | 11000031 / AMR-109-0031 | Problem 3.10 — Find a finitely presented subgroup H < Modg for which there are infinitely many conjugacy classes of finite subgroups… | 0.0480 | 3 | unknown | queued | 0/5 |  |  |  |
| 1887 | 30004758 / OWR-8415338-005 | Monge–Ampère Singularities for Nonpolyhedral Obstacles | 0.0476 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1888 | 30004800 / OWR-8415343-001 | Weighted Sobolev Stability Under Nonlinear Composition | 0.0476 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1889 | 30005097 / OWR-10252929-010 | Hermite and GL2 Equivalence Classes of Number Fields | 0.0474 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1890 | 30005760 / OWR-14298158-005 | Inversion Monotonicity in the Domino Subclass | 0.0466 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1891 | 30000903 / OWR-1782-017 | Real-Rooted Barycentric h-Polynomials and g-Theorem Conditions | 0.0460 | 3 | 2008 | queued | 0/5 |  |  |  |
| 1892 | 11000162 / AMR-109-0162 | Problem 2.5 — Knowing that d(φ)≥ 1, can we decide whether it is ≥ 2? | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1893 | 1200024 / AMR-011-0024 | Some Questions — Question 24 | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1894 | 158 / GREEN-070 | Sets with No Unique Sum Representations | 0.0450 | 2 | unknown | queued | 0/5 |  |  |  |
| 1895 | 20000022 / AIM-ALGEBRAIC_GEOMETRY-0022 | Immaculate line bundles as unit-orthogonal toric branes | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1896 | 20000162 / AIM-ALGEBRAIC_GEOMETRY-0162 | A modern étale criterion and an all-characteristic constant-functor test | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1897 | 20000726 / AIM-ANALYTIC_NUMBER_THEORY-0090 | A rational j-equation for a mixed mock Kaneko-Zagier solution | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1898 | 20000750 / AIM-ANALYTIC_NUMBER_THEORY-0114 | Alternative GPY weights: exact perturbation geometry and a radial escape | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1899 | 20001232 / AIM-COMPUTATION-0070 | Arbitrary logistic cell gaps with positive margins and ordinary-margin obstructions | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1900 | 20002401 / AIM-PDES-0013 | A two-level validated certificate for Maslov indices of planar elliptic problems | 0.0450 | 4 | unknown | queued | 0/5 |  |  |  |
| 1901 | 20002454 / AIM-PDES-0066 | Branch-aware well balancing and a resonance obstruction for oscillatory forcing | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1902 | 2308019 / AMR-022-8019 | Research Problems in Function Theory — Problem 8.19 | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1903 | 2361 / EP-881 | Erdős Problem #881 | 0.0450 | 1 | unknown | queued | 0/5 |  |  |  |
| 1904 | 2464 / EP-1063 | Erdős Problem #1063 | 0.0450 | 1 | unknown | queued | 0/5 |  |  |  |
| 1905 | 3000085 / AMR-029-0085 | Strongly minimal edge cover | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1906 | 30006520 / OWR-14299904-002 | Upward Closure of Grothendieck Schubert Supports | 0.0450 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1907 | 8800088 / AMR-087-0088 | Converting between divisor-class and infrastructure discrete logarithms | 0.0450 | 3 | unknown | queued | 0/5 |  |  |  |
| 1908 | 30005119 / OWR-10252930-032 | Uncommon Pairs of Linear Equations | 0.0442 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1909 | 30001941 / OWR-11453-002 | Sharp Free-Energy Decay for Fast Diffusion | 0.0441 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1910 | 30002271 / OWR-12330-013 | Counterexamples to Averaged Local Fractional-Coloring Bounds | 0.0440 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1911 | 30003699 / OWR-15987-008 | Coefficient Complexity of Braid-Matroid Kazhdan–Lusztig Polynomials | 0.0434 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1912 | 30004105 / OWR-16775-009 | Theta Invariants and New Families of MRD Codes | 0.0432 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1913 | 30004511 / OWR-1703875-003 | Sharp Waiting-Time Estimates for Variational PDE Discretizations | 0.0431 | 3 | 2020 | queued | 0/5 |  |  |  |
| 1914 | 30004931 / OWR-8415360-010 | Optimal Neural-Network Depth for Sparse Recovery | 0.0429 | 3 | 2021 | queued | 0/5 |  |  |  |
| 1915 | 2308009 / AMR-022-8009 | Research Problems in Function Theory — Problem 8.9 | 0.0420 | 3 | unknown | queued | 0/5 |  |  |  |
| 1916 | 5300089 / AMR-052-0089 | Critically finite maps with hyperbolic postcritical complement | 0.0419 | 3 | 1990 | queued | 0/5 |  |  |  |
| 1917 | 30003717 / OWR-15988-004 | Shortest Piecewise-Smooth Scaling–Rotation Curves | 0.0418 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1918 | 10000012 / AMR-099-0012 | Uniform expansion bounds for graph nets | 0.0405 | 3 | unknown | queued | 0/5 |  |  |  |
| 1919 | 11000140 / AMR-109-0140 | Problem 10 — Though the (virtual) Euler characteristics are already known [28,56], devise a matrix model using screens to calculat… | 0.0405 | 3 | unknown | queued | 0/5 |  |  |  |
| 1920 | 20002195 / AIM-INFRASTRUCTURE-0095 | Degree-local Hom computation and certified corner reuse | 0.0405 | 3 | unknown | queued | 0/5 |  |  |  |
| 1921 | 3000013 / AMR-029-0013 | Compatible Euler-tours | 0.0405 | 3 | unknown | queued | 0/5 |  |  |  |
| 1922 | 30006527 / OWR-14299904-009 | Monotonicity of Hook Counts in Symmetric Partitions | 0.0405 | 3 | 2026 | queued | 0/5 |  |  |  |
| 1923 | 3052 / OPG-58213 | Roller Coaster permutations | 0.0405 | 2 | unknown | queued | 0/5 |  |  |  |
| 1924 | 3071 / OPG-404 | Concavity of van der Waerden numbers | 0.0405 | 1 | unknown | queued | 0/5 |  |  |  |
| 1925 | 3248 / OPG-48583 | Bounding the on-line choice number in terms of the choice number | 0.0405 | 1 | unknown | queued | 0/5 |  |  |  |
| 1926 | 8800009 / AMR-087-0009 | Globalizing prescribed local Brauer classes | 0.0405 | 3 | unknown | queued | 0/5 |  |  |  |
| 1927 | 30000155 / OWR-768-005 | Asymptotic Goodness of Function-Field-Tower Codes | 0.0397 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1928 | 30000740 / OWR-1536-011 | Picker–Chooser and Maker–Breaker Strategy Transfers | 0.0395 | 3 | 2007 | queued | 0/5 |  |  |  |
| 1929 | 3361 / OPG-37413 | Alexa's Conjecture on Primality | 0.0390 | 1 | unknown | queued | 0/5 |  |  |  |
| 1930 | 30003820 / OWR-16164-014 | Positive Polynomial Comparisons for Unitriangular Conjugacy Classes | 0.0386 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1931 | 30004187 / OWR-17128-003 | Nonlocal Water Waves with Generalized Vorticity | 0.0384 | 3 | 2019 | queued | 0/5 |  |  |  |
| 1932 | 30005255 / OWR-11695855-008 | Cancellation-Sensitive Norms for Two-Layer Networks | 0.0379 | 3 | 2022 | queued | 0/5 |  |  |  |
| 1933 | 30005523 / OWR-13750332-005 | Vanishing-Viscosity Limits for Transport Equations | 0.0376 | 3 | 2023 | queued | 0/5 |  |  |  |
| 1934 | 30005769 / OWR-14298158-014 | Moment Sequences from Matching Pattern Avoidance | 0.0373 | 3 | 2024 | queued | 0/5 |  |  |  |
| 1935 | 30002437 / OWR-12725-014 | Subpolynomial Bounds for an Additive Multiplicative Equation | 0.0369 | 3 | 2013 | queued | 0/5 |  |  |  |
| 1936 | 11000137 / AMR-109-0137 | Problem 7 — Devise a matrix model (cf. | 0.0360 | 3 | unknown | queued | 0/5 |  |  |  |
| 1937 | 1200028 / AMR-011-0028 | Some Questions — Question 28 | 0.0360 | 3 | unknown | queued | 0/5 |  |  |  |
| 1938 | 20000211 / AIM-ALGEBRAIC_GEOMETRY-0211 | A framed quotient and a regular compactification of Carlsson-Weinshall duality | 0.0360 | 3 | unknown | queued | 0/5 |  |  |  |
| 1939 | 3000054 / AMR-029-0054 | Maximum weight k-element subsets of perfect matchings | 0.0360 | 3 | unknown | queued | 0/5 |  |  |  |
| 1940 | 8800014 / AMR-087-0014 | Improved Frobenius lifts for nondegenerate curves | 0.0360 | 3 | unknown | queued | 0/5 |  |  |  |
| 1941 | 9700009 / AMR-096-0009 | Spectral gap of a Bayesian graph Laplacian | 0.0360 | 3 | unknown | queued | 0/5 |  |  |  |
| 1942 | 30001686 / OWR-4792-017 | Rectangular Partition Relations on $\omega_3$ | 0.0349 | 3 | 2011 | queued | 0/5 |  |  |  |
| 1943 | 30000050 / OWR-723-002 | Power-Law Fixed-Radius Circle Discrepancy | 0.0347 | 3 | 2004 | queued | 0/5 |  |  |  |
| 1944 | 30003705 / OWR-15987-016 | Symmetric-Group Characters Determined by Reflection Length | 0.0337 | 3 | 2018 | queued | 0/5 |  |  |  |
| 1945 | 30001245 / OWR-3473-002 | Coloring $F$-Free Uniform Hypergraphs | 0.0328 | 3 | 2009 | queued | 0/5 |  |  |  |
| 1946 | 30006169 / OWR-14299082-016 | Cardinal-Preserving Namba-Type Forcing | 0.0327 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1947 | 11000251 / AMR-109-0251 | Question 4.3 — Does there exist a closed hyperbolic 4-manifold that is a surface bundle over a surface where the genus of the fiber… | 0.0325 | 3 | unknown | queued | 0/5 |  |  |  |
| 1948 | 30006294 / OWR-14299287-005 | Predicting Topographically Pinned Vortices | 0.0322 | 3 | 2025 | queued | 0/5 |  |  |  |
| 1949 | 139 / GREEN-051 | Axis-Parallel Rectangles in Dense Sets | 0.0320 | 1 | unknown | queued | 0/5 |  |  |  |
| 1950 | 30003406 / OWR-15216-010 | Equality of Canonical Models from Universal Projective Sets | 0.0301 | 3 | 2017 | queued | 0/5 |  |  |  |
| 1951 | 30002067 / OWR-11786-023 | Dual-Diameter Bounds for Triangulated Surfaces | 0.0294 | 3 | 2012 | queued | 0/5 |  |  |  |

Equal scores are ties; numeric ID order has no mathematical significance. Scores are subjective priorities, not guarantees of a solution.
Full list: [ranking.csv](ranking.csv). Holds and every score component: [catalog.json](catalog.json).
Individual reasoning and next experiments: [SHORTLIST.md](SHORTLIST.md).
