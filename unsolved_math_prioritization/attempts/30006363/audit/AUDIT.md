# Independent adversarial audit: topological invariance of helicity

Problem 30006363 / OWR-14299512-001, catalogue rank 557.
Review date: 4 October 2026 UTC.

## Verdict

**Accept the frozen packet as an unresolved investigation after five substantive approaches.** No blocking mathematical error was found in its restricted propositions, quantitative estimates, or examples. This is not approval of a solution of the general problem. The proposed status `unsolved`, with `5/5` attempts, accurately describes this investigation and does not erase the known nonsingular theorem.

No correction to the reviewed public files is required. Their SHA-256 manifest remains

`3cea69df13cb1c9605b22cdbda7d9b0a454f8e3fc92b20ea759099557643e3ff`.

All seven entries in that manifest were checked before and after testing. The manifest itself is the eighth frozen file. No reviewed file was modified, and no remote write was made.

## 1. Source and scope gate

The exact Question 1 and preceding definition on printed page 1664 of [Oberwolfach Report 31/2025](https://ems.press/content/serial-article-files/52240) were read in text and in the rendered page. They require a closed three-manifold, exact volume-preserving fields, and an orientation- and volume-preserving homeomorphism intertwining the flows with the same time parameter. Zeros are not excluded. The broader extension question is also present.

The matching catalogue record agrees on the ID, code, and title. Its compressed statement and generated literature assessment were not used to replace the primary mathematical formulation. The packet transparently records its catalogue-access failure and the alternative pinned dataset source. Repository search outcomes in SOURCE_GATE.md are historical provenance supplied by the packet; this audit does not claim to have rerun those remote repository searches.

[Edtmair and Seyfaddini, arXiv:2508.10609v1](https://arxiv.org/abs/2508.10609v1), Theorem 1.3, retains the nowhere-vanishing hypothesis; Remark 1.7(3) explicitly leaves flows with fixed points open. Its complete relevant printed proof chain was inspected: Theorem 3.1; Sections 4–5, including Lemmas 4.6, 4.8–4.10, 5.7–5.8; Theorems 6.1 and 6.11 and their internal lemmas; Sections 7.1–7.3; and Section 8 through the final deduction of Theorem 1.3. This is inspection of the actual arguments, not reliance on the abstract. Their cited foundations and explicitly omitted or sketched arguments are not independently certified here.

At a zero, the two-form obtained by contraction with volume is zero, so its kernel is three-dimensional. It therefore falls outside the everywhere one-dimensional foliation framework used in that paper. Passing to the punctured complement loses the closed-manifold hypothesis. Neither maneuver supplies the missing extension.

The [current arXiv record](https://arxiv.org/abs/2508.10609) listed only v1 during this audit. The authors' [Edtmair research list](https://oedtmair.github.io/) and [Seyfaddini publication list](https://people.math.ethz.ch/~sseyfaddini/publications) still link that work. Bounded searches for the title, authors, singularities, fixed points, and 2026 helicity invariance did not locate a full singular-case resolution. This negative search result is not a proof of worldwide absence or a priority claim.

The inspected source PDF hashes agree with those recorded in SOURCE_GATE.md:

- OWR: `8ba4df2a9edad4311ff99a7f9d03d15ab7873869c81990233ac6f65f54848ca2`
- Edtmair–Seyfaddini v1: `fcbe11426065224c39471d8ca02c89e47a11087e4d848f85c5c38f0e6e54c432`

No source PDF, extracted source text, or rendered source page is part of this audit's publication payload.

## 2. Bi-Lipschitz invariance

Proposition 2.1 withstands the regularity and cohomology challenges.

1. **Generator identity.** At every point where the Lipschitz map is differentiable, substituting the smooth orbit expansion into the differentiability estimate gives `Dh X1 = X2 ∘ h`. Time conjugacy is essential here. The remainder is small compared with time; the argument does not assume differentiability of the homeomorphism along every transverse curve.
2. **Signed volume Jacobian.** The bi-Lipschitz bounds imply an invertible derivative at almost every differentiability point. At such a point, the derivative's local degree has the homeomorphism's orientation sign. The area formula and measure preservation force the absolute volume Jacobian to be one, and the orientation hypothesis makes the signed Jacobian positive. Coordinate volume densities must be included; the packet correctly expresses the result as `h*μ = μ` rather than merely a Euclidean determinant assertion.
3. **Two-form identity.** Pullback commutes with contraction with the related vectors by pointwise exterior algebra, yielding `h*ω2 = ω1` almost everywhere. No nonsingularity of either vector field is needed.
4. **Weak chain rule.** The pulled-back primitive is essentially bounded. In a smaller coordinate chart, mollifications of the coordinate map converge uniformly and strongly in every finite local Sobolev exponent, with a uniform first-derivative bound. The one-form pullbacks converge strongly, as do the two-form pullbacks: their coordinate coefficients are sums of smooth coefficients composed with the maps, multiplied by one or two first derivatives. Strong convergence and the uniform bounds justify passage to the distributional exterior derivative. It is unnecessary for these local mollifications to be diffeomorphisms or measure preserving.
5. **Gauge and cohomology.** The difference between the pulled-back primitive and the source primitive is only required to be distributionally closed, not exact. Testing its exterior derivative against the smooth source primitive gives zero. Thus nontrivial first cohomology is not an unaddressed obstruction, and no global potential for that closed one-form has been assumed.
6. **Final change of variables.** The products are integrable, and the oriented area formula converts the target helicity to the integral of the weak pullback. This step uses both orientation and volume assumptions.

The signs agree: for a closed one-form γ, `d(γ ∧ α) = −γ ∧ dα`. On a closed manifold this gives the required vanishing integral. The proof does not extend automatically to an arbitrary homeomorphism: the needed transverse weak derivatives and integrable pullbacks have not been established there.

## 3. Continuity and approximation

Lemma 3.1 correctly uses the Hodge right inverse on exact two-forms. Exactness removes the harmonic projection, closedness eliminates the complementary Hodge term, and the positive spectral gap on the harmonic orthogonal complement bounds the primitive operator in L2. The bilinear expansion has both terms, producing the stated product of the difference norm and the sum of the two norms. No continuity in the topology of flows is being smuggled into this estimate.

Smooth orientation- and volume-preserving pushforwards remain exact and preserve helicity. Therefore strong L2 convergence of their generators is a valid sufficient condition. Uniform convergence of maps and their inverses alone is not that condition.

The shear example checks out independently:

- Its Jacobian is one and its inverse subtracts the same shear.
- The pushed generator is evaluated in target coordinates correctly; the shear leaves its relevant x and z coordinates unchanged.
- The displayed primitive differentiates to the required two-form, and its helicity density vanishes pointwise.
- Integrating the squared difference gives exactly π² for every positive integer n.
- The explicit target flow solves its generator equation at every time and satisfies the same-time conjugacy identity.
- Its additional y displacement is at most 2/n, so uniform flow convergence is compatible with the failure of strong generator convergence.

This only refutes an automatic implication from the weaker convergence. It does not show that every carefully chosen approximation sequence fails, and it is not a counterexample to helicity invariance.

## 4. Indexed zeros and exact cutoffs

The cyclic sine field is globally exact and divergence free. Its eight zeros are nondegenerate, with signs alternating according to the number of half-period coordinates; their sum is zero. The origin has index +1. On the Euclidean coordinate sphere of radius 1/8, each coordinate is within the range of the elementary sine bound, so the field's norm is at least 1/2. A uniform perturbation strictly smaller than 1/2 cannot change the boundary degree. A continuous nowhere-zero extension over the ball would force degree zero. Thus the claimed open uniform neighborhood is valid even without imposing divergence-free or exactness conditions on the competitor.

The cutoff estimate also has the correct order. A smooth field vanishing at the center gives a closed two-form of size O(r). The radial homotopy primitive is O(r²). The difference of this local primitive from a global primitive is exact on the ball, allowing the cutoff of its potential to make the gauges agree on a smaller ball without changing the two-form. For a cutoff at scale ε:

- The original-form term is O(ε).
- The derivative-of-cutoff term is O(ε⁻¹) times O(ε²), hence also O(ε).
- The support volume is O(ε³).
- The L2 norm is therefore O(ε^(5/2)).

The construction deliberately creates an open zero region and does not preserve the given conjugacy when applied independently on the two sides. It cannot invoke the nowhere-vanishing theorem as written.

## 5. Isolated-zero defect formula and growth condition

Proposition 5.1 withstands all of the following checks.

**Zero correspondence and gauges.** Same-time conjugacy identifies fixed points, hence identifies the zero sets. Finitely many disjoint coordinate balls permit simultaneous gauge changes. The formula for the radial primitive has the correct factor of t for a two-form and yields second-order vanishing. This uses only local closedness and the vanishing of the two-form at the center.

**Integrability despite an unbounded primitive.** The one-form β = h*α2 may be unbounded near punctures. The proof never estimates its full norm in the volume integral. Instead, β ∧ ω1 is the pullback of a smooth three-form fμ and equals `(f ∘ h)μ` on the regular complement. It is bounded relative to μ. Subtracting the smooth source helicity density preserves integrability. Since the omitted finite sets have zero measure, their removal costs no integral. This is sufficient for dominated convergence of the truncated volume integrals.

**Stokes and every boundary term.** On the punctured manifold, γ = β − α1 is smooth and closed. Consequently

`d(γ ∧ α1) = −γ ∧ ω1`.

The boundary orientation points into the removed balls. Applying Stokes gives the minus sign in (5.3) and (5.6). There is no discarded `dγ` term, because it is zero on this domain. There is no surviving `α1 ∧ α1` term, because a one-form wedges with itself to zero. No derivative of a cutoff or of the boundary parametrization is being omitted in this argument.

**Boundary exponent.** On a source sphere of radius r, the source primitive contributes r² and the area contributes r². Pulling back the target one-form costs one factor of `‖Dh‖`, not a two-dimensional Jacobian, because the other factor in the boundary wedge is the source primitive. The target primitive contributes `d(h(x),h(p))²`. Thus the claimed bound is exactly

`C r⁴ sup(‖Dh‖ d(h(x),h(p))²)`.

Under the additional power bounds, its order is `r^(4+2b−a)`, so the stated strict inequality `a < 4+2b` is sufficient. Equality of the exponents alone only gives a bounded estimate and does not imply decay. The separate condition that `r⁴ sup ‖Dh‖` remains bounded is sufficient because continuity of h supplies uniform decay of the target-distance factor on shrinking spheres.

**Unconditional identity within the restricted setting.** Even when the growth condition fails, the total boundary integral has a limit because the corresponding truncated volume integral converges. This proves the defect identity under smoothness off finitely many zeros. It does not prove the defect is nonzero in any example, nor that each puncture's contribution separately converges. The packet makes neither unsupported claim.

## 6. Asymptotic linking and the rough shear

The conditional reduction on S3 is correct: transport the entire source cycles, including the closing paths, use orientation preservation for linking and product-measure preservation for the average, and bound the difference from a target admissible closure system by the stated L1 error divided by T². The requisite error estimate is explicitly left unproved. Measurability, integrability, admissibility, and the helicity limit are stated as hypotheses rather than claimed for arbitrary transported paths.

The torus rough-shear example has its separate scope clearly identified. Its inverse exists continuously; fiberwise translation preserves volume by Fubini; its explicit isotopy gives the correct orientation. It commutes with the exact smooth field in the y direction. On a sufficiently short coordinate arc, there is no torus-wrapping ambiguity in the length calculation. The sampled values alternate with magnitudes comparable to k^(-1/2), so finite partitions give unbounded total variation and therefore infinite graph length.

An ambient homeomorphism still preserves the topological linking of the transported cycles. Nonrectifiability obstructs simply reusing metric length estimates; it does not itself invalidate their linking numbers or disprove the required averaged error bound. In particular, the torus example is not a purported S3 counterexample to the conditional reduction, and neither example contradicts the source question.

## 7. Reproducibility and computational limits

Run `python independent_checks.py` from this directory, with the packet's pinned SymPy 1.14.0 dependency installed.

The audit script:

1. Checks the expected frozen manifest and all its file hashes.
2. Replays the submitted verifier in temporary storage so its generated JSON does not rewrite the frozen packet.
3. Confirms all 38 submitted checks pass and reproduce verification.json exactly.
4. Recomputes the same 38 controls using a separate exterior-form implementation rather than the packet's curl helper.
5. Runs 12 additional controls: both shear inverse compositions; pullback of the explicit primitive; flow initial condition, generator equation and conjugacy; rough-shear commutation; a radial primitive and its quadratic scaling; the boundary and cutoff exponents; and the closed-form Stokes sign.
6. Checks that every frozen file is unchanged.

All 38 replayed checks, 38 independently reimplemented controls, and 12 additional controls passed. Results are recorded in audit_results.json. Passing these tests is evidence for the explicit algebra and examples only. The analytic propositions were reviewed separately; the tests do not prove Rademacher's theorem, the area formula, weak chain rules, Hodge estimates, degree persistence, linking-limit existence, or the unrestricted conjecture.

## 8. Publication decision and remaining gap

The public packet is appropriately limited to original exposition, cited provenance, restricted mathematics, and small reproducible tests. The audit files likewise contain no source copies, private source locations, corpus extracts, or conversation records.

The unresolved step is not a hidden sign or missing elementary estimate. The arbitrary homeomorphism in the original question need not meet the weak-pullback, strong-generator, punctured smoothness/growth, or transported-linking error hypotheses used by the partial results. Five distinct substantive approaches have been documented with their residual gaps. None constructs a qualifying counterexample or proves the full singular case. The packet consistently acknowledges these limits.

**Final recommendation: publishable as an audited unresolved 5/5 investigation, with no full-resolution or novelty claim.**
