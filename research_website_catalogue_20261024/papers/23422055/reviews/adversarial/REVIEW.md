# Independent adversarial review — Zenodo 23422055

**Verdict: PASS for the stated mathematical construction, with bounded historical scope.** No substantive mathematical defect was found in Theorem 1 or its proof. This is an AI-assisted mathematical review, not human peer review or formal proof certification.

## Exact reviewed object and scope

The entire five-page published PDF, `anti-invariant-four-manifold-v1.0.pdf`, version 1.0, was read as extracted text and rendered pages. Its corresponding `paper/note.tex` and the author's archived construction and local checker were inspected. The PDF SHA256 is `14063ce9fef470a6a3875dc429a1c3d34372d60cbd73eb7e22e77b46b1639f60`; the published verification ZIP SHA256 is `ae7d51ded2f03cd307ec394728a94f3e2e6e568903905713da8bfdf0007a24d6`. The fresh acquisition receipt and all top-level input hashes are preserved in `inputs.json`.

The strongest verified claim is the existence of a jointly smooth family on the closed connected real four-manifold Σ₂ × E, equal to the product complex structure outside one coordinate ball and converging to it in C∞, with three fixed independent real de Rham classes admitting closed anti-invariant representatives, and nonintegrable for every sufficiently small nonzero real parameter. The conclusion is **h⁻ ≥ 3**, not equality or a complete classification.

The review tried to break the compact construction at branching/infinity, the simultaneous local normal form, full cutoff derivatives, positivity, kernel rank and reality, smooth patching, cohomological independence, and the nonintegrability test. It also checked whether the cited integrability and genericity results actually prohibit the construction.

## Independence and incidental exposure

The source inventory exposed filenames of archived audits and acceptance reports. No such report, archived verdict, sibling review, or current reviewer conclusion was read. The published manuscript necessarily describes its own prior checking; those statements supplied no evidence of validity here.

The fresh exact script `independent_checks.py` was written from the published equations before reading any archived checker. Its 34 controls passed, and the independent mathematical conclusion was logged at 75% completion before reading the two archived algebra checkers and the author's earlier candidate proof. Those later reads were for reproducibility and consistency. The candidate's author-only status sentence and the package verifier's pinned archive names/hashes were incidental support metadata, not reviewer opinions. Archived audit report contents were never used.

## Mathematical reconstruction

### 1. Closed connected four-manifold and global forms — verified

The polynomial z⁶−1 has no repeated roots. The degree-two compact cover has six simple finite branch points and two unramified points at infinity. The defining polynomial is not a square in C(z), so the cover is connected. Riemann–Hurwitz gives genus two. Its product with C/(Z+iZ) is a closed connected smooth real four-manifold.

At a finite branch root r, r is nonzero and y is a local parameter; differentiating y²=z⁶−1 gives dz/y=dy/(3z⁵). At infinity, s=1/z and q=y/z³ satisfy q²=1−s⁶, with q nonzero at s=0, so the published formulas −s ds/q and −ds/q show regularity of both differentials. Their ratio z on a nonempty coordinate patch proves linear independence. The product holomorphic top forms Ω₀, Ω₁ are closed. No global nowhere-vanishing assumption is needed.

### 2. Independence of the three real cohomology classes — verified globally

For real a,b,c, let H=(a−ib)Ω₀+cΩ₁. Its real part is F=aα+bβ+cγ. In any complex-oriented chart, F∧F=(H∧conj(H))/2 is a nonnegative volume density, strictly positive on an open set if H is nonzero. Thus a nonzero F cannot be exact on this closed manifold: if F=dλ, closedness gives F²=d(λ∧F), whose integral vanishes by Stokes. If H=0, the independence of the two holomorphic differentials forces a=b=c=0. This is a proof of cohomological independence; pointwise independence of three forms is neither claimed nor needed.

### 3. Simultaneous coordinates and full cutoff correction — verified

Near (0,i,0), y(z) is holomorphic and nonzero. The coordinate change ζ=z, ξ=w/y(z) has Jacobian 1/y(z). The dz∧dz term cancels in dζ∧dξ, giving Ω₀=dζ∧dξ and Ω₁=ζΩ₀. Consequently γ=uα−vβ, with exactly the signs printed in equation (1).

For every smooth R—not merely the core polynomial—the identity d(Rv dv)=v d(R dv) holds because the extra R dv∧dv term is zero. Therefore the three globally closed forms in (2) satisfy γ_ε=uα−vβ_ε throughout the cutoff region. Both perturbation primitives have compact support in the coordinate ball, so their zero extensions are globally smooth and exact. The three de Rham classes are unchanged for every parameter.

### 4. Positive plane, real almost-complex structure and smooth extension — verified

Independent exterior algebra reproduces α²=2vol, α∧β_ε=R_t vol and β_ε²=2(1−R_x)vol. The coefficient R_u creates no extra Gram term; the R_v term vanishes before this calculation. Since R is ε times a fixed smooth compactly supported function, both derivative bounds follow uniformly for sufficiently small |ε|. They give D=1−R_x−R_t²/4≥1/2 for positive and negative parameters alike.

Orthogonalization and normalization produce α∧B_ε=0 and B_ε²=2vol. Thus Ψ²=0 and Ψ∧conj(Ψ)=4vol. The nonzero skew form Ψ has complex rank two. Its kernel and conjugate are complementary: a shared vector would contract the nonzero top form Ψ∧conj(Ψ) to zero. Their smooth complementary splitting defines a real J with J²=−Id. It gives the original product J at ε=0.

As an independent matrix check, if A and E represent α and β_ε, then

`J = −A⁻¹(E − (R_t/2)A) / sqrt(D)`.

The fresh script verifies J²=−Id and JᵀAJ=−A, JᵀEJ=−E for unconstrained symbolic first derivatives, rather than only on the core. It likewise checks the third representative using the full variable-coefficient relation.

Compact support gives an actual collar on which every derivative of R is zero, so J equals J₀ there and extends smoothly. Joint smooth dependence and D≥1/2 on the fixed compact support give convergence in every finite derivative norm, hence C∞ convergence. The zeros of Ω₀ over infinity lie outside this local construction and cause no kernel-rank problem: J is assigned to be J₀ there.

### 5. Nonintegrability — verified by two independent formulations

On the core where ρ=1, k=1−εx is positive, and the stated factorization gives a (1,0) coframe. Direct differentiation reproduces

`dφ₁ ∧ φ₁ ∧ φ₂ = −ε/[2(1−εx)] vol`.

If J were integrable, dφ₁ could have only (2,0) and (1,1) components, neither of which can wedge nontrivially with a (2,0) form in complex dimension two. The displayed coefficient therefore rules out integrability.

A separate coordinate Lie-bracket calculation using the reconstructed J gives

`N_J(∂u,∂x) = −ε/[2(1−εx)] ∂u`.

In particular, at the center of the actual cutoff core, it is −ε∂u/2. This proves nonintegrability even though J equals J₀ pointwise at that center; first derivatives differ. The ε=0 control vanishes as required. No boundary phenomenon or large-parameter behavior is used.

## Imported results and potential obstructions

Reference PDFs were freshly retrieved from primary sources; hashes and URLs are in `reference-receipts.json`. Reading was targeted to the assertions used, not a claim to have audited entire cited papers.

- [DLZ, arXiv:1104.2511v1](https://arxiv.org/pdf/1104.2511v1), Conjecture 2.5, explicitly states the unrestricted compact four-dimensional implication from h⁻≥3 to integrability. Its Theorem 1.1 concerns structures admitting a common compatible metric with an integrable structure. Here no such metric can exist with the specified J₀: on the core compatibility would require g_uu=g_vv=k⁻¹g_vv where k≠1. The construction meets the conjecture's compact dimension assumptions and escapes the theorem's additional metric hypothesis.
- [Tan–Wang–Zhang–Zhu, arXiv:1112.0768v3](https://arxiv.org/pdf/1112.0768v3), Theorem 1.1, makes h⁻=0 open and dense among all smooth almost-complex structures on a closed four-manifold. An exceptional one-parameter family is consistent with this statement; the paper does not claim an open set of h⁻≥3.
- [Donaldson, arXiv:math/0607083v1](https://arxiv.org/pdf/math/0607083v1), opening geometric dictionary, identifies an almost-complex structure with an oriented positive real two-plane subbundle of two-forms. The manuscript also proves the needed local realization directly, so an unexamined global existence theorem is not being imported.
- [Bande–Kotschick, arXiv:math/0703348v2](https://arxiv.org/pdf/math/0703348v2), Theorem 6, assumes two symplectic forms whose recursion operator squares to −Id. The normalized B_ε is not closed: its core exterior derivative has nonzero coefficient ε/(2k^(3/2)). The unnormalized closed pair does not satisfy the required normalization. Thus this integrability result supplies no contradiction.
- [Hind–Tomassini, arXiv:1908.03016v3](https://arxiv.org/pdf/1908.03016v3), Proposition 4.2, gives h⁻=2 for its compact Kodaira–Thurston family. The paper accurately distinguishes that assertion from larger noncompact/further-dimensional constructions.
- Chen–Zhang accepted manuscripts [I, §6.3](https://wrap.warwick.ac.uk/id/eprint/164863/1/WRAP-Kodaira-dimensions-almost-complex-manifolds-I-Zhang-2022.pdf) and [II, §5.1](https://wrap.warwick.ac.uk/id/eprint/163848/1/WRAP-Kodaira-dimensions-almost-complex-manifolds-II-Zhang-2022.pdf) were inspected at the relevant passages. They discuss nonintegrable products T²×S and plurigenera. II expressly treats the anti-invariant cohomology calculation for those examples as a question. This supports the manuscript's careful distinction, without excluding deductions from older work or establishing firstness.

The main construction is elementary once smooth manifolds, complex forms, Stokes, and Riemann–Hurwitz are available. No withdrawn theorem is required. The historical Oberwolfach date/page locator, all journal-final comparisons, and exhaustive priority were not independently certified in this review; the directly checked DLZ conjecture suffices to identify the mathematical target.

## Fresh controls and archived replay

`independent_checks.py` passed **34** checks with Python 3.14.6 and SymPy 1.14.0. The retained outputs are `independent-results.json` and `independent-run.txt`. They include general-R closedness and the third-form identity; Gram identities; a generic derivative-jet reconstruction of J; anti-invariance; core factorization; Frobenius and Nijenhuis obstructions; ε=0; nine Gram-bound corner controls; simple branch roots; and the coordinate Jacobian. Negative controls detect leaving the third form uncorrected and using an unnormalized complex form.

Default and bundled Python initially lacked SymPy. An ignored review-local virtual environment was created with SymPy pinned to 1.14.0; this was an environment issue, not a failed mathematical test. The environment setup log is retained.

The published strict package profile passed against the manifest extracted from the freshly acquired, hash-bound ZIP, with 258 files, 24 original files and seven members of the inner author archive. All three pinned algebra programs replayed with exact expected output and assertions enabled; its intentionally false assertion was rejected. The author's 13-check program also passed under `python -O`. `replay-results.json`, `package-profile.stdout.txt` and `author-optimized.stdout.txt` retain evidence. This is byte/replay authentication, not a signature or a proof of the global theorem. No archived audit verdict was used to decide the mathematical result.

## Remaining gap and disposition

**Exact remaining mathematical gap found: none.** The full written argument establishes the stated construction; finite calculations corroborate local identities but do not replace the global cohomological and patching arguments reviewed above.

Not established here: the exact value of h⁻, a fixed-symplectic-form compatibility theorem, analyticity, a classification, historical firstness, continued openness before this paper, or journal acceptance. Those are not conclusions of Theorem 1. No repair, publication, browser interaction, website edit, spreadsheet edit, Git action, or external communication was performed.
