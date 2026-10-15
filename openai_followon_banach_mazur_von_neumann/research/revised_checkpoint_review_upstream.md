# Independent scoped audit of the pinned family295 mathematical input

Audit completed: 2026-10-07 05:34 UTC. Scope-review completion estimate: **100%**. This is a supporting proof-input review for the revised conditional checkpoint, not a final publication certification and not a new mathematical result.

## Verdict and exact scope

I found **no concrete internal defect** in the inspected manuscript's walk, Liouville, rigidity, or ordinary bounded self-cohomology assembly arguments. This is the outcome of an independent adversarial hand-check, not a claim that the entire upstream result has been independently certified. The strongest checked statement is that the displayed arguments support the stated vanishing conclusion **assuming the established operator-algebra inputs listed below**. Several important input statements were checked against their primary sources; their full published proofs were not independently reconstructed.

The reviewed mathematical source is the pinned directory

`sources/upstream/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/build`

within `/Users/alec/Documents/Math/openai_followon_banach_mazur_von_neumann`. I read all five section files, the bibliography, and the adjacent README. I did not read or rely on earlier favorable reviews. I read `/Users/alec/Documents/Math/AGENTS.md`. Reviewed inputs were not changed; no Git actions, builds, local downloads, outreach, or external messaging were performed. Primary-source web retrieval was read-only.

An independently delegated adversarial check covered Section 05 and the ordinary-complex/classical-reduction boundary. It independently reached the same local no-defect finding and checked the central homotopy by exact symbolic expansion in degrees 1–9. That finite check supplements, rather than replaces, the all-degree cancellation proof.

## Source identity

All line references below are one-based lines in the actual source files, not PDF pagination.

| Input | SHA-256 |
|---|---|
| `sections/01-introduction.tex` | `ddec01dc15fa257e3f1e85004b54225dd43df633bbdfa957de98353c069ce4b2` |
| `sections/02-walk.tex` | `3d1015a1c20d2cfc8a4c8991652d93eed756763cd982cbc28a53fd625b7b3314` |
| `sections/03-liouville.tex` | `7782c390e534a15d35d7aee470ff425fcb6823c4073b29886f3dbffbc8d31622` |
| `sections/04-rigidity.tex` | `9cf9cf2b11fc838326321b4c0384904a303ecec43d732cd748c9204059f4ea60` |
| `sections/05-cohomology.tex` | `c6c8e63bac0e543624ac63fd50a046878ba7082a531115111563455682e4d437` |
| `references.bib` | `c176b67594bb8852e2dd2dbb93e622e576092fbf3ad6e20a2939de0806d800f1` |
| `paper.tex` | `61e1696d7f1413e492de8d7f5516312506d062297fc1e7fe485056ee88c0042d` |
| adjacent `README.md` | `d1305a1c1c16c51f6165e32c37c90911379ed1b4505b179a5ff77c7eb422e70f` |

## The central chain: attempted falsifications and what was checked

### Walk and finite freeness

Section 02:78–104 is the nonlocal freeness input. The specialization sets every coordinate ambient algebra and coordinate subalgebra equal to the same II₁ factor P. The factor's nonzero corners are diffuse and cannot embed into a scalar algebra or finite matrix amplification. The full ultrapower is a factor; its commutant in itself is scalar. Thus relative freeness becomes scalar freeness. Finite repeated adjunction preserves a separable coefficient algebra. I checked this specialization against the actual statement and definitions of [Popa's Theorem 0.1(a), §§1.5–1.6](https://arxiv.org/html/1308.3982v3). The theorem supplies the required diffuse algebra for a separable centered subspace, without an amenability assumption in case (a). **The full incremental-patching proof of Popa's theorem was not re-proved in this audit.**

Section 02:112–162 withstands the distinguished-letter attack. The labels unique to the paths are distinct. After grouping all other free algebras into the coefficient algebra, each path has the form Aᵢuᵢ^{±1}Bᵢ. A reduced word in paths has a reduced distinguished-letter string. Expanding coefficients into scalar and centered parts produces nonempty reduced Haar blocks alternating with centered coefficient blocks. Ordinary reducedness suffices; cyclic reducedness is not silently assumed.

Section 02:180–263 moves finite tests from the factor ultrapower to actual coordinate unitaries and then to a general separable tracial II₁ algebra. Finite intersections along the ultrafilter give simultaneous coordinate choices. The central-fiber route uses countably many measurable unitary sections and first-successful-candidate selection. Polynomial exponentials give fiberwise density, and the telescoping estimate proves the required open conditions. The patching gives uniformly norm-one measurable sections. The direct-integral structure and trace disintegration are standard inputs, not newly proved here.

Section 02:267–382 gives a single measure, fixed before the map is chosen. I recomputed its parameter scales: nℓpℓ=pℓ^{-1/2} diverges, nℓ∑_{j>ℓ}pⱼ is O(pℓ^{1/2}), and the repeated-label probability is bounded by O(Kℓ^{-2}). The base-alphabet and missed-level bounds also vanish. Labels are counted on the sampling space before evaluating their unitary values, so accidental coincidences of values do not invalidate the union bounds. Each stage imposes finitely many tests. The concluding assertion is scalar moment convergence, not an unjustified finite-coordinate norm convergence.

### Liouville and two ultrapowers

Section 03:33–93 correctly turns bounded-ball sequential continuity into a uniform modulus and transfers it to the tracial ultrapower, using bounded representatives and the same modulus. This does not need separability. The second ultrapower is permitted by repeating the same argument; no unsupported global L²-boundedness of the map is assumed.

Section 03:119–174 constructs an L²-valued bounded martingale. Orthogonality gives a uniform mean-square Cauchy estimate for every later time. The operator-norm ball is L²-closed, so support endpoints belong to M. A deterministic limit forces the module identity on all positive-mass atoms, then on every unitary by bounded-ball continuity, then on all of M by linearity.

Section 03:183–226 uses independent disjoint halves of one increment string. The products G and G⁻¹ themselves are not asserted independent. Symmetry makes each reversed inverse prefix have the original walk law. The two replacement errors are controlled separately. Thus two distinct support points give a positive endpoint-event mass for every fixed tolerance, uniformly for sufficiently late times.

Section 03:229–305 concatenates blocks only with pairwise distinct **unsigned** indices. This avoids reusing a block together with its inverse. For each fixed m the endpoint-event mass cₘ is obtained first; the subsequence index is then chosen so that the finite moment/block failures have probability less than cₘ/2. A rapidly shrinking cₘ is harmless. Section 03:309–346 produces exact free Haar joint moments and exact multiplier identities in the first ultrapower. It does not assert freeness from a or b, which the later proof does not require.

### Rigidity, polar transfer, and arbitrary multipliers

Section 04:68–121 supplies the length estimate and norm transfer. Grouping exact cancellations by the fixed number of canceled letters gives orthogonal input/output decompositions with suffix h fixed. Each block matrix has Hilbert–Schmidt norm bounded by the coefficient ℓ² norm. Faithful positive spectral moments determine the norm, so exact free Haar scalar moments transfer the regular-representation norm to the containing tracial algebra. This uses exact moments after the first ultrapower, not moment convergence to infer coordinate norm convergence.

Section 04:173–262 handles the central distinct-index obstruction. Each internally reduced block z(z* z)^d is nonempty with positive endpoint signs; boundaries between blocks cannot cancel. The noncrossing cancellation matching yields coefficient bound C_L r^{-q/2}. The number of surviving reduced words with a repeated unsigned index is O_L(r^{q-1}); orthogonality and the length estimate give total operator-norm error O_L(r^{-1/2}). Repetitions that disappear during reduction remain in the retained coefficients. No hypothesis is incorrectly imposed on original, rather than surviving, indices. The adjoint case uses the separate negative-multiplier identity and complex linearity, not preservation of adjoints by the map.

Section 04:281–363 derives the Catalan moments of s* s. Terms with d distinct paired labels give C_d(r)_d; assignments using fewer labels give lower-order terms. Compact moment determinacy identifies the displayed probability density, which has no zero atom. Faithfulness gives zero kernel, and finite traciality makes the polar isometry unitary. Section 04:365–419 uses literal **ordered** polynomial block expansions, norm approximation for each fixed regularization, then uniformly bounded L² approximation to powers of the polar unitary. No commutation of the blocks is assumed.

Section 04:428–543 provides the final spectral argument. I checked the uniform sine bound, the real-part lower bound on each rotated short arc, and the right inverse F supported on that arc. Right multiplication by F yields a bound on (a−b)e without requiring a or b to commute with the spectral algebra. The trace weights each compression by τ(e); there is no factor equal to the number of arcs. Faithfulness then gives a=b. No Haar distribution for the polar unitary is required. The infinite-algebra counterexample at 04:556–565 confirms why the finite trace is material.

## Ordinary bounded self-cohomology and full assembly

Section 01:13–39 defines ordinary bounded complex multilinear self-cochains, the usual Hochschild differential, and quotient by its **actual image**. The argument constructs genuine primitives; it never substitutes a closed image or imposes complete boundedness.

Section 05:31–98 gives a direct proof of normal linear maps' bounded-ball L² continuity. Summable small two-sided supports yield decreasing tail projections. Normality and ultraweak lower semicontinuity allow orthogonal compressions whose images stay large. Random signs contradict the operator-norm bound. Consequently Akemann's citation is not an omitted central proof step here.

Section 05:112–214 averages the last input, takes pointwise ultraweak cluster limits on a common norm ball, and preserves the continuity modulus through unitary invariance and lower semicontinuity. The half-tolerance step restores a strict modulus. Averaging the original equation df=0 gives dh=(−1)^k f, so g=(−1)^k h is a primitive of norm at most ‖f‖. This requires neither P commuting with d nor normality of the averaged limit. The independent Section 05 reviewer checked the signs and modulus separately.

Section 05:230–292 handles nonseparable tracial algebras with finite input sets, separable tracial hulls, and conditional expectations. Adding unital matrix systems of every finite size rules out every homogeneous finite type I summand of the hull. The hull need not be a factor. Including f(E^k) makes the extended primitive's coboundary exactly f on E^k. A subnet indexed cofinally by finite sets eventually includes any fixed tuple, so compactness preserves exact equality. Nested hull choices and uniform normality of the primitives are unnecessary.

Section 05:301–387 supplies the required mixed-input correction. Expanding each input into zM and qM parts makes the first qM input determine the sole insertion. Its merger with the inserted q contributes +ψ; every other term cancels or vanishes. Degrees zero and one are explicitly valid. Independent exact symbolic expansion checked all 1,022 central input patterns in degrees 1–9 with no failure; the textual cancellation argument covers arbitrary degree. The bound (k−1)‖ψ‖ is uniform in z.

Section 05:406–488 handles unrestricted-cardinality central partitions. Supports of normal states on the center form a maximal orthogonal partition. Faithful normal center-valued traces yield faithful normal scalar tracial states on each II₁ piece, even if that piece is nonseparable. All such pieces have the uniform primitive bound. The entire non-II₁ complement is kept as one piece, so its finite primitive norm does not need a uniform estimate over further summands. For an uncountable partition, bounded finite partial sums converge strongly as a **net**, giving the bounded direct product. Coordinatewise cochain construction and finitely many differential terms produce an actual bounded G with dG=f. This does not impose a bound on the cardinality of the index set.

The cited classical reductions at Section 01:192–211 remain external mathematical inputs. I checked their statement/category boundaries against [JKR1972, Lemma 5.4 and Theorem 5.6](https://www.numdam.org/article/BSMF_1972__100__73_0.pdf), and [CPSS2003, equation (1.1) and Section 2](https://arxiv.org/pdf/math/0107078). They concern bounded continuous cochains, ordinary self-coefficients, and actual coboundaries. A von Neumann algebra acting on itself is a dual normal bimodule; no separability or scalar-trace hypothesis is introduced by this reduction. **The complete proofs of JKR's reduction and the classical complementary-summand vanishing theorem were not independently reconstructed.**

## Limited inspection of actual Lean declaration semantics

I read four actual copied source files under `research/lean_audit/build`; this was not a build or a complete dependency audit:

| File | SHA-256 |
|---|---|
| `OAI/Analysis/BoundedHochschild/Cochains.lean` | `4db4ea41b9776365b4eb7119e628b0e6a1110af20fc1e9256228667a2641392a` |
| `OAI/Analysis/TracialCohomology/Cohomology.lean` | `94dca90b822e6cfba8dd8d62668df39331295b69ada0736d886d2e62e14b1f77` |
| `OAI/Analysis/BoundedHochschild/Main.lean` | `f6a3d901a2b0b4ea9a212c8d77e52933b4d34c8f1ab88217c7f9429ec3465e3f` |
| `OAI/Analysis/BoundedHochschild/MainResult.lean` | `aded34dc78d6d8c7cf78bdeded8ec41acf99c1138ae4ac12aa7e217c04c6f7b8` |

`Cochains.lean`:12–27 uses `ContinuousMultilinearMap ℂ (fun _ : Fin n => M) M` and the displayed Hochschild signs. `Cohomology.lean`:43–61 uses `LinearMap.range`, without closure. `MainResult.lean`:13–30 states the actual existential primitive result for arbitrary such cocycles on its W*-algebra class; `Main.lean`:79–103 has proof bodies for the primitive and cohomology declarations. These declarations do not request complete boundedness, normality, separability, or a faithful scalar trace of the input algebra. The `n+2` degree parameter covers all degrees at least two.

I did **not** inspect every imported declaration, authenticate the copied Lean tree to its upstream commit, re-elaborate the source, run an axiom check, or verify the full semantics of the W*-algebra library class. Those tasks belong to the parent's separate formal/source-authentication review. Reading a proof body or a meaningful final declaration does not by itself establish its successful compilation or the absence of hidden premises in its dependencies.

## Remaining proof-input and certification limits

1. The new manuscript's displayed local chain was checked by hand and attacked for the named failure modes; this is not an exhaustive independent proof of every underlying operator-algebra theorem.
2. Popa's theorem, JKR's normal reduction, and the classical no-II₁ vanishing input have matching primary statement boundaries, but their full original proofs remain assumed in this scoped review.
3. Direct-integral disintegration, center-valued trace structure, existence of matrix systems and tracial conditional expectations, spectral functional calculus, and tracial ultrapower structure were checked for use with the stated hypotheses, not rederived from foundational definitions. Blackadar's referenced sections and the original conditional-expectation papers were not reopened here.
4. No quantitative construction was executed for the extremely large rare-level tests. The proof needs only finite existence and does not promise practical computability.
5. No current-build or complete formal-certification claim follows from this report. A conditional downstream consequence remains conditional even when no local upstream defect is located.

No route was marked blocked: I did not find a step transferring the central problem to an unsupported equivalent claim. No proposed mathematical repair follows from this audit. If the checkpoint describes the upstream input, it should say that the pinned manuscript's relevant displayed arguments and limited final Lean semantics have been inspected with no concrete defect found, while preserving the separate source-authentication, compilation, dependency, and independent-certification boundaries above.
