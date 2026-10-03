# Independent audit of Kirby Problem 5.17 research note

Audit date: 2026-10-03. Problem 3024 / KP-5.17, queue rank 538.

## Verdict

**Accept the mathematical content as an unresolved five-attempt research note, with minor bibliographic errata.** No mathematical defect was found in the stated partial results. The explicit examples refute two proposed shortcuts; they do not refute Weinstein-homotopy uniqueness. No general proof, original-counterexample claim, historical novelty, or human peer-review certification is warranted.

The audited author packet has seven manifest entries. The SHA-256 of its `SHA256SUMS` is:

    20778293a818c31b05f974fd0fac9bc24135f93ae3e0115bab8be5aeca7b6585

All entries matched before and after review. The author packet was not edited. The verdict concerns that exact version, including the minor errors recorded below. A corrected author packet would need its own manifest. The audit result does not change the mathematical status: **unsolved, 5/5**.

## Minor findings

1. **K3 PDF locator.** `SOURCE_GATE.md` gives printed pp. 315–316 and physical PDF pp. 339–340. In the inspected 436-page primary PDF, the problem is on both printed and one-based physical PDF pages **315–316**, or zero-based pages **314–315**. Physical pages 339–340 are bibliography. The printed-page citation and problem identification are correct. Use `#page=315` for a PDF-page link.
2. **K3 title.** The reference title in `PROOF.md` is a descriptive variant. The title displayed by the primary author PDF is *K3: A New Problem List in Low-Dimensional Topology*. Use that title for a precise bibliography.

These corrections have no effect on any equation or conclusion. They can be recorded in an accompanying erratum without changing the frozen files. No mathematical revision is required by this audit.

## Target and source review

[K3, Problem 5.17](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf#page=315) and all five remarks were read, including visual inspection of both relevant pages. The question fixes the actual symplectic form at its two endpoints. The remarks discuss boundary-outward fields, a common-complex-structure case, flexibility, a symplectic mapping-class case, and closed primitive differences. The stated open range is dimension greater than two. That is a dated source statement, not a present-day nonresolution theorem. The proposer and scribe in the note agree with the source.

The repeated endpoint in the printed interpolation is visible in the PDF: both terms use V₂. Interpreting the intended interpolation as the segment between the two endpoint fields is explicitly disclosed in the note and is appropriate. This source typo cannot itself supply an argument.

The relevant definitions and homotopy conventions in [Cieliebak–Eliashberg, *Flexible Weinstein manifolds*](https://arxiv.org/abs/1305.1635) were checked, together with Lemma 3.1 and its proof, Theorem 2.10, Proposition 4.4, Theorems 5.4 and 5.6, the deformation arguments in Sections 5.3–5.4, and Theorem 6.1 / Corollary 6.2. In particular, the proof's use of loose attaching data is real and cannot be removed by declaring the symplectic forms equal.

[Eliashberg, *Weinstein manifolds revisited*](https://arxiv.org/abs/1707.03442v2), pp. 1–5, was checked for its broader working definition, completed Liouville transport discussion, and Problems 1.4–1.5. The note appropriately avoids turning completed transport into an endpoint-preserving fixed-form result on an unchanged compact domain.

The book *From Stein to Weinstein and Back* was not independently inspected in full for this audit. The fixed-J claim remains an attribution to K3. The accessible author survey supplies the flexible result actually used. The loose Legendrian h-principle, two-index theorem, and other imported theorem dependencies have not been formally rederived here.

The abstract of [Iida, arXiv:2608.09361v2](https://arxiv.org/abs/2608.09361v2) describes nonsymplectomorphic exact forms. Consequently that announcement cannot settle the fixed-actual-form question. Its full proof is not a dependency of this audit. A bounded primary-source search produced no replacement general resolution; this is not an exhaustive literature certification. Repository-history claims in the source gate are not independently recertified here and are not used to prove mathematics.

## Compact annulus and affine obstruction

Write x = sin q, y = cos q. With the constants in equation (3), independent differentiation gives

    U_s' = 1/8 + (7s/18)x − (2/9)x² = w_s(1 − (8/9)w_s).

For Z = A ∂p + B ∂q and ω = dp∧dq, the contraction is A dq − B dp. Thus the sign convention in λ_s is correct, and dλ_s = ω follows from cancellation of the q derivatives. This confirms actual equality of the symplectic forms, not equality only in cohomology.

On p = 2, the outward p-component is 2(1 − w_s') ≥ 1. On p = −2, its component along the outward direction −∂p is again at least 1. Both boundary components are convex. The function is constantly 2 on the whole boundary, has no interior value as large as 2, and has nonzero outward derivative there. A complete flow on the compact manifold with boundary is not required; outward escape would in fact prevent such completeness. The note correctly uses the domain convention at this point.

The global gradient-like check goes beyond strict positivity away from critical points. Equation (4), the bounds on U_s and w_s, and |p| ≤ 2 give

    dφ_s(Z_s) ≥ (199/576)p² + (4/9)w_s²
               ≥ (1/3)(p² + w_s²).

The potentially adverse term here is −p²w_s²/9; using w_s² ≤ 25/64 accounts for it with the correct sign. The norm estimate is valid because |1 − p²/4| ≤ 1 on this compact annulus. Together the estimates give δ = 1/12 for the full quantitative criterion, including at and near both critical points. The same compact-domain norm estimate must not be reused for unrestricted p.

The critical set is exactly p = 0 and sin q = −s/4. The mixed Hessian entry vanishes there; its diagonal entries have signs given by 1 − U_s/2 > 0 and w_s' = ±√15/8. There are two nondegenerate points, with indices zero and one. No Morse-Bott critical circle has been overlooked.

The mean field is p∂p + (1/8)∂q. Its p = 0 orbit closes after time 16π. Any gradient-like function would strictly increase along this nonzero orbit, contradicting its return to the initial point. Allowing birth–death critical points in a family does not permit this recurrent orbit: the obstruction is to every Lyapunov function for this particular field, not merely to Morse functions.

The primitive difference equals −d(p sin q), globally, since sin q is a well-defined function on the circle. Its periods all vanish. Hence the obstruction to this affine segment survives the exact-difference restriction.

Conversely, q ↦ q + πt is a smooth symplectic rotation of the same compact domain. At t = 1 it takes w_+ to w_− and U_+ to U_− under pullback. It therefore supplies the asserted endpoint-preserving, fixed-form Weinstein homotopy. This directly rules out interpreting the example as a counterexample to the original question.

For the open comparison, ψ_s = p²/2 + U_s has a different derivative estimate:

    dψ_s(Z_s) = p²(1 − w_s') + w_s²(1 − (8/9)w_s)
               ≥ (1/2)p² + (4/9)w_s².

This establishes the required global inequality without the compact-annulus factor. The bounded angular component and linear radial equation imply existence of the flow for all positive and negative times. Adding the standard complex factor preserves the inequality, properness, completeness, and critical indices. The midpoint orbit remains at p = z = 0. These higher-dimensional open examples test the shortcut only. They are subcritical for n ≥ 2 and give no nonflexible counterexample.

## Exact perturbations and changing cohomology

The supported-perturbation result has the needed exclusions. On the compact support K, dφ(Z) has a positive minimum because K avoids Crit(φ). The estimate involving B is valid for positive and negative parameter values. A bounded parameter interval gives a finite norm bound, while outside K the original quantitative inequality survives. If B = 0, any chosen bounded interval works. Boundary data and critical points remain unchanged. This local result does not imply global path-connectedness. The note identifies that missing inference rather than asserting it.

For the cohomology family, putting r = p − c gives

    λ_c = r(1 + ε cos q)dq + ε sin q dp,
    Z_c = r(1 + ε cos q)∂p − ε sin q∂q.

The signs agree with dp∧dq. The derivative of φ_c is the sum of the two nonnegative terms in equation (10). A global usable constant is

    δ = (1 − ε) / max{(1 + ε)² + 1, 2} > 0.

The two critical Hessians are diag(1, −ε) and diag(1, ε). The critical values are ε and −ε; the function is proper and bounded below. Its q equation is bounded and r solves a linear equation with bounded coefficient, establishing completeness in both directions.

For c(t) on a compact interval, the family is uniformly proper and all critical values stay in [−ε, ε]. Constant levels above ε tending to infinity therefore give the regular exhausting levels required by the open homotopy definition. Merely having a pointwise complete family would not by itself be an adequate substitute for that check.

The closed difference has period −2π(c₁ − c₀), as asserted. As an additional consistency check, the symplectic isotopy

    h_t(q,p) = (q, p + c(t) − c₀)

satisfies h_t*λ_c(t) = λ_c₀ exactly. Thus nonzero primitive-difference cohomology is perfectly consistent with exactness after a symplectic pullback; there is no conflict with Proposition 4.4. The family is not asserted to be fixed near infinity, Hamiltonian, or confined to exact primitive differences on the original coordinates.

## Isotopy, Moser, formal data, and flexibility

Pullback by a symplectic isotopy preserves the complete domain data, including the outward normal direction and a pulled-back metric for the quantitative inequality. Assuming such an isotopy for every endpoint symplectomorphism would assume away the mapping-class issue. The note does not do that.

In the Moser calculation, ι_Yω = −dot λ has the correct sign. Cartan's formula yields the exact derivative in equation (13), and Y is symplectic because d(dot λ) = 0. Boundary tangency or completeness of its flow is a separate question. Even a successful exact transport statement does not produce Lyapunov functions. None of these distinctions has been used as an illicit equivalence.

The compatible almost-complex construction has the correct sign and endpoints: g_i(J_i u,v) = ω(u,v), so A_i = J_i. For the interpolated metric, A commutes with the positive square root B of −A²; J = AB⁻¹ has J² = −1 and ω(u,Jv) = g(Bu,v). Thus compatible Chern classes cannot distinguish the endpoints.

The flexible special case is properly limited to real dimension 2n > 4 and the same formal symplectic class. Empty negative boundary removes the relative constraint for domains. The output theorem allows the symplectic form to vary. The universal claim for nonflexible endpoints and the stronger fixed-form path problem do not follow. The dimension-four variants of the survey have additional hypotheses and are not silently substituted for an unrestricted result.

All five recorded approaches have distinct mathematical content and explicit stopping points. Counting them as five attempts is reasonable; it does not certify five independent proofs or five independent research sessions.

## Exact replay and limitations

The unmodified `verify.py` was executed in isolation with Python 3.12.14 and assertions enabled. All **44** controls passed. The generated JSON was byte-for-byte identical to the frozen `verification.json`, with SHA-256:

    8870e37dddc2e05ee532bbf080b89a23c013d910f4430488ae5855e4162dd211

The verifier's sparse polynomial arithmetic and reduction by sin²q + cos²q = 1 are suitable for these identities. Its rational comparisons correctly reproduce the displayed coefficient calculations. Several of those controls check arithmetic inside estimates; the domain restrictions, global bounds, periodic-orbit argument, Morse property, completeness, and theorem applicability still require the written mathematics examined above.

The replay does not verify universal quantifiers over Weinstein structures, prove a homotopy classification, or formally certify external theorems. The status remains unresolved. This is an automated mathematical audit, not human peer review.

Only original audit text, structured audit metadata, and exact replay output are included with this report. No source PDFs, extracted publication text, or raw research records are included.
