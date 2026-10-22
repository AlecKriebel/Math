# Independent adversarial audit: jet curvature and real first Chern class

Audit date: 2026-10-05. Problem 30002180, catalog code OWR-12015-001, queue rank 717.

## Verdict and binding

**PASS as an unsolved five-attempt research packet.** The packet does not solve the general implication. Its five retained statements are valid with their stated hypotheses and external inputs. No counterexample to the original question has been constructed. This verdict is neither a novelty judgment nor a claim that the question is globally open.

The audited target is `safe_packet_v2`, whose MANIFEST.json has SHA-256 `e9b0934c31eb18e76e4c99f3bdca5c362ce5519f4ecc4efe551eeef6ea4b6019`. Every listed file and the complete directory allowlist were independently checked. The original packet was also checked and preserved. Only STATEMENT.md and MANIFEST.json differ between them; none of the five attempted proofs changed. PACKET_BINDING.json contains the complete byte-level binding.

There is no mandatory mathematical correction to the five retained statements. The main point requiring additional explanation was restriction of singular curvature in Attempts 2 and 5. The local argument below supplies that explanation using exactly the packet's quasi-plurisubharmonic and local-boundedness assumptions. It does not upgrade directed positivity to total positivity.

## Original question and conventions

The publisher's OWR PDF was independently fetched, hashed, rendered and inspected. Printed pages 2612–2613 identify compact projective complex manifolds, the tautological line on the Semple tower, negativity along the directed subbundle, regular-jet nondegeneration, and nonvanishing of the real first Chern class. The nearby focus on threefolds is context; the displayed question does not expressly impose a dimension-three restriction. The packet's positive-dimensional interpretation is appropriate. [Original report](https://ems.press/content/serial-article-files/46414)

The lines convention for projectivization is consistent: L_j is a subline of pi_j^*V_{j-1}, V_j is the inverse image of that line under the tangent map, rank V_j=n, and dim X_j=n+j(n-1). Thus curvature of L_j with the required negative sign is equivalent to positive curvature of L_j^* on V_j. The boundary called X_j^sing is the nonregular-jet locus, not a singularity locus of the smooth tower.

For complete sign clarity, in a local holomorphic frame e of L_k write |e|_h^2=exp(phi). Then, with a consistent positive normalization of dd^c, the curvature of the dual line is dd^c phi. It is this phi that is quasi-psh in the jet-metric convention. One must not use the exponent with the opposite sign from an unrelated line-metric convention.

A compact smooth manifold has finitely generated integral cohomology. Consequently the kernel of H^2(X,Z)→H^2(X,R) is torsion. The v2 correction is exact: real nonvanishing is equivalent to the integral class being non-torsion. A nonzero torsion class is insufficient. None of the arguments requires holomorphic triviality of K_X merely from vanishing real c1.

## Singular-potential restriction: the critical analytic check

The quasi-psh and degeneration-set conventions were independently checked in Demailly, Definitions 7.3–7.4. Outside the degeneration set the local potential is bounded on a neighborhood, not just finite pointwise. [Demailly source](https://www-fourier.univ-grenoble-alpes.fr/~demailly/source_files/hyperbolic.pdf)

Here is an explicit local justification of the restriction used in the two retained proofs. Let W be a holomorphic subbundle of TY, let alpha=dd^c phi locally, with phi quasi-psh and locally bounded, and suppose alpha(xi,bar xi)≥epsilon omega(xi,bar xi) distributionally for sections xi of W. Let gamma be an immersed holomorphic disc tangent to W.

1. On a sufficiently small neighborhood, extend the nonzero tangent vector field of the embedded disc holomorphically as a section Z of W. This is possible by taking a holomorphic frame of W and extending its coefficient functions from the disc. Shrink so that Z is nonzero.
2. Straighten Z by holomorphic flow coordinates. The disc becomes a coordinate leaf, Z=partial/partial z_1, and the contracted inequality has constant differential operator partial_1 partial_bar1 on phi. Its smooth lower-bound coefficient is a positive function b.
3. Convolve phi with a nonnegative radial smooth approximate identity in all these coordinates on smaller neighborhoods. Constant-coordinate differentiation commutes with convolution, so the regularized restriction satisfies its second-derivative inequality with lower bound b convolved with the same kernel.
4. The canonical quasi-psh representative converges pointwise under this regularization. Local boundedness gives a uniform bound on compact neighborhoods, so restrictions converge in L^1 on the coordinate leaf. Passing to distributions proves the required inequality for phi composed with gamma. The lower bound converges locally uniformly.

Thus gamma^*alpha means dd^c(phi composed with gamma), glued with the line-bundle transition functions. It is not an undefined pullback of an arbitrary current. The same flow argument works along the images of the constant-vector leaves in the torus construction. A locally bounded function without the quasi-psh canonical representative would not justify this argument: changing its values on a submanifold leaves the ambient distribution unchanged but can change a proposed restriction.

This proof fills in the compressed restriction sentence in Attempt 2. Smoothing an already restricted subharmonic potential would by itself be circular if its subharmonicity had not first been established. No added smoothness assumption is needed, and the source definition already supplies the needed quasi-psh convention.

## Route 1: Kähler scalar trace

**PASS for the stated Kähler-induced subcase; not a general jet-metric proof.** The unit-sphere fourth moment has both pairings. Independent coefficient checks use the factorial formula for complex sphere monomials and additional symmetric-tensor examples. The Kähler symmetries identify the two contractions, giving average holomorphic sectional curvature 2S/[n(n+1)]. Strict negativity makes S negative. The trace-wedge identity then yields a strictly negative pairing of c1(T_X) with the closed form omega^(n-1).

Compactness, closedness of the Kähler form, and the Kähler curvature symmetries all matter. An arbitrary Hermitian/Finsler or higher-jet metric has not been converted to the base tensor needed here. The packet correctly stops before making this unsupported conversion.

## Route 2: immersed curves and genus

**PASS, including the full dimension-one case.** For a holomorphic immersion f:C→X, projection of every lifted map to f guarantees that the lifts remain immersions. They are regular jets. The derivative at level k-1 is an isomorphism T_C≅f_k^*L_k, without a ramification divisor because f is an immersion. Consequently f_k^*L_k^*≅K_C.

The preceding local lemma gives a well-defined curvature inequality on C. Compactness supplies a uniform bound for the norm of d pi_{k,0}; integrating proves the stated genus-to-area estimate with a positive constant independent of f. For dim X=1, the identity map gives negative degree of T_X directly.

The normal-bundle identity also has the correct sign: if c1(T_X)_R=0, then deg N_f=2g(C)-2. This is compatible with high genus. Complete intersections of n-1 members of |dH| have canonical-degree/degree ratio (n-1)d under the assumed real-c1 vanishing. The finite parameter grid checks formal intersection arithmetic, not existence of a variety for every integer tuple. No low-genus or entire curve on every projective real-c1-zero manifold is supplied. The separate entire-curve exclusion uses the explicitly identified Demailly theorem, not these arithmetic checks.

## Route 3: total positivity and bigness

**PASS as a stronger-hypothesis comparison.** Directed positivity is strictly weaker as a pointwise linear-algebra condition: an identity form on V with a negative block on a complement can have negative full trace or top determinant. Such forms are negative controls for an inference, not globally constructed Semple-tower metrics.

The bigness lemma is sound: Kodaira's lemma supplies a positive power of L as an ample bundle times an effective divisor; sufficiently large powers of the ample factor still have a section after twisting by a fixed pullback A^-1; multiplication by the effective-divisor section gives the desired section. Projection formula and the invariant-jet direct-image identity then apply. In rank one the same identity follows directly because the tower is X and invariant one-variable jet polynomials are powers of the first derivative.

Golota's inspected theorem has the additional total-curvature/nondegeneration hypothesis and concludes canonical ampleness. It is not a proof for arbitrary directed negativity. Mere bigness must not be conflated with the nondegeneration condition of that ampleness theorem. [Golota manuscript](https://arxiv.org/abs/1708.02866)

The missing implication is still directed positivity→bigness, or directed positivity→a nonzero ample-negatively-twisted jet differential. No change of metric weight is shown to fix uncontrolled transverse curvature.

## Route 4: Ricci-flat twisted-jet vanishing

**PASS relative to the stated Calabi–Yau existence theorem and standard differential/sheaf identities.** Projectivity supplies compact Kählerness and an ample A. Real-c1 vanishing permits a Ricci-flat metric in the positive class c1(A); torsion in integral c1 does not obstruct this. The dd^c lemma adjusts a smooth metric on A to this curvature class.

For the induced cotangent metric, the contracted Chern curvature is zero because Ricci is zero and the metric is Kähler. Contraction commutes with the sum formula for tensor-product curvature. Twisting any cotangent tensor power by A^-1 gives a strictly negative scalar mean-curvature operator. The displayed integrated Bochner identity has the correct sign and forces any holomorphic section to vanish. The q=0 case is included.

Characteristic-zero symmetrization embeds each product of symmetric powers into the appropriate cotangent tensor power. The jet filtration uses weighted degree sum j ell_j=m, whereas the tensor degree is sum ell_j; these are correctly distinguished. Its finite successive quotients have no sections after twisting, and the elementary exact-sequence induction gives vanishing for the entire Green–Griffiths bundle. The invariant sheaf injects, so it too has no sections. No splitting of the jet filtration or flatness of the tangent bundle is required.

Yau's announcement was independently retrieved and visually inspected; the long PDE proof was not re-audited. The packet transparently treats existence as an established external theorem. [Yau announcement](https://www-fourier.univ-grenoble-alpes.fr/~demailly/source_files/bourbaki_190316/PNAS-1977-Yau-1798-9.pdf)

The vanishing statement becomes a contradiction only after producing a forbidden section. Directed positivity alone has not produced it. Neither the code nor Bochner vanishing closes that gap.

## Route 5: all-order torus obstruction and currents

**PASS for complex tori and finite étale torus quotients.** The recursive maps j_r are holomorphic sections over the torus. Their projection is the identity, so d j_r(v) never vanishes. Local affine curves yield these regular lifts at every order, and d j_r(v) belongs to V_r. The nonzero holomorphic frame d j_{r-1}(v) trivializes j_r^*L_r.

The logarithmic squared norm is therefore a global locally bounded potential on the torus. The local restriction lemma transfers the positive directed lower bound to the constant v direction; compactness makes it uniformly positive. The directional second derivative of any periodic distribution has integral zero, contradicting that lower bound. This works even for irrational directions without a compact elliptic leaf.

The current T_v is genuinely positive and closed: its coefficients relative to translation volume are constant, and integration by parts kills derivatives of test forms. Pushforward by the holomorphic section preserves closedness and gives a directed current. Its cohomological pairing with the tautological class is zero by the trivialization. The analytic positive pairing is interpreted through the pulled-back potential as above; no product of arbitrary singular currents is being taken. Finite étale pullback identifies tangent bundles and towers, so it preserves all the hypotheses.

Ricci-flatness on a general manifold does not give the global nonzero translation field, affine jet sections or flat tangent connection needed by this construction. The algebraic trace-zero tensor correctly demonstrates that the sectional curvature may have both signs. It is not a compact geometric counterexample.

The 2026 manuscript's Theorem 7.6 was independently inspected, including its nondegeneration hypothesis. Its conclusion concerns geometric hyperbolic indices; it is not a c1(T_X) nonvanishing theorem. Its arXiv record identifies a first draft. This audit verifies its stated scope, not its full regularization/current-theory proof. [Dinh–Nguyen–Vu manuscript](https://arxiv.org/abs/2607.07054v1)

## Computation, provenance and privacy limits

The author's verifier reproduces the frozen result with 3,274 assertions. The independently written control program, without importing the author's program, passes 8,705 assertions, including 260 graded-rank/generating-series comparisons. These are finite algebraic and arithmetic controls only. They do not certify Yau's theorem, Bochner's analytic identity, current restrictions, source correctness, or the full conjecture.

All five source PDFs were independently retrieved with HTTP 200, and every byte count and SHA-256 matches the packet's record. Freshly rendered OWR pages 16–17 (one-based PDF numbering) correspond to printed 2612–2613. Demailly page 39, Golota page 2, the 2026 manuscript page 34, and Yau page 1 were also visually inspected. Source PDFs, extracted text and rendered pages remain outside both safe packets and this safe audit.

The exact problem webpage and raw AI corpora remain uninspected in this audit. The catalog ID/rank mapping and the author's prior-repository search history are reported metadata, not independently re-proven facts about all repositories or conversations. The original question itself is independently bound to the OWR source. No broad literature absence, global-openness, novelty, priority, journal-publication or peer-review claim follows.

The target packet's frozen pending-audit wording is a historical statement at its freeze. This separately bound audit records the subsequent completed review; it does not rewrite the preserved packet.

## Final unresolved dependency

The general c1_R=0 case still requires either an actual nonzero ample-negatively-twisted jet differential forced by the exact directed metric, or a suitable nonzero directed lifted current with controlled nonpositive tautological pairing. None of the five routes supplies this implication. The appropriate outcome remains **unsolved, five approaches completed, no general solution claimed**.
