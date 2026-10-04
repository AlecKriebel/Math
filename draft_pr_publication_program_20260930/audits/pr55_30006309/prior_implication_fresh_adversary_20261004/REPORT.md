# Fresh adversarial verification of the Esterov prior implication

**Verdict: the prior implication is mathematically sufficient for the exact scoped model comparison asserted by PR55. Recommend treating that comparison as a consequence of prior machinery and blocking promotion as a newly resolved open target.** This is not a finding that an earlier publication printed the candidate's exact proof or explicitly answered the later OWR question. The underlying geometric equality was already known; that fact alone would not have settled a request for a new proof.

## Binding, independence, and precise question

Target: PR55 / numeric upstream 30006309 / OWR-14299288-015. Parent supplied the literal open draft head `85c78d0cf3959d9d492a637cb90835ebc6a0e828` and the live claimed_solved 1/5 state. This child did not independently refresh GitHub or change any live/native/index/Git/PR/publication state. The original custody source, rather than an unpromoted corrected source, is the subject of this audit.

I read the original source record, candidate, source manifest and custody SELF_MANIFEST. All 127 file entries in the custody manifest match their recorded byte counts and SHA-256 digests. Important bindings are:

| Input | SHA-256 |
|---|---|
| original/CANDIDATE.md, 13,632 bytes | `4931eccbb464b53af07b90e24b72060e681b9a7f1769c0030a9d7090e59b129c` |
| original/source_record.json, 4,368 bytes | `927e3a9d72eeb17901bd84e979384b323c9f2f97ff7caf5118d2ddc19f6bfda1` |
| original/status.json, 1,643 bytes | `1daf50597d694945ee6e8e956863478536d69d70a4cacc53d60bf9f66b4c7ef6` |
| original custody SELF_MANIFEST.json | `b1124133d9c9cd88206c8a61755d36e16ca94a90a91a512b99fb755f2ee6a270` |
| previous ESTEROV_SPECIALIZATION.md | `75514b024c794a07f2024145f40b246dab36a79fe185880ac2380580221f1d9b` |
| previous prior_newton_formula_audit/DERIVATION.md | `9d8b1c264c88bf4ab782f9787eeda8957497c013a2da89e57e6e33f2549455be` |

SOURCE_BINDINGS.json gives absolute paths and the comparison-verdict hashes. The independently reconstructed mechanism was saved in INDEPENDENT_RECONSTRUCTION.md at 04:18:57 UTC on 4 October 2026, before reading either old derivation or old verdict. Only then were the previous claims compared. The new audit is a mathematical challenge of existing deductions, not an extra central proof-search turn.

The claim tested is exactly

\[
\pi\operatorname{Newt}(D_{A\times\operatorname{Vert}(\Delta_{n-1})})
=\operatorname{conv}\{n\eta_{T,n}-\eta_{T,n-1}:T\text{ regular}\},
\]

with n≥1, a smooth polarized toric variety, its complete very ample embedding, degree≥2, and A consisting of all lattice points of the Delzant polytope Q. The massive (n−1)-simplices are boundary simplices. This is the candidate's explicit theorem, with the ordinary product discriminant and the first-factor coefficient-weight projection.

## Primary statements actually checked

The [OWR report](https://ems.press/content/serial-article-files/51856), printed pp.919–921, distinguishes the known Cayley identification from a request for a combinatorial reproof. Its introduction uses a general lattice-generating A. The short Hurwitz theorem/problem does not restate smoothness or a complete embedding. The cited [Sano preprint](https://arxiv.org/pdf/2302.09801), Introduction, Definition 1.3 and Theorem 1.4, supplies those hypotheses and the boundary convention. Accordingly this audit establishes the prior implication in the candidate's recovered smooth regime. It does not prove that every possible intended case of the abbreviated OWR wording is covered. An unrestricted full-source statement still needs a separately justified scope interpretation.

The inspected mathematical prior is [Esterov, arXiv:0810.4996v3](https://arxiv.org/pdf/0810.4996v3), dated 31 July 2010: global passage in the Introduction; Definitions 1.8 and 1.11; Proposition 1.27; Definitions 2.7 and 2.22; Theorem 2.31; Theorem 4.10; Definition 5.5; Theorem 5.10; and Definition 5.12. The detailed theorem numbering is bound to that preprint, not an independently inspected journal full text. The [arXiv bibliographic page](https://arxiv.org/abs/0810.4996) associates the work with its 2010 journal publication. Fresh source retrieval hashes and UTC times are in PRIMARY_RETRIEVAL.json. The Esterov PDF matches `95f028d12b52dedeab8ab43f2b58e814a48287b8c6d627c70b1e25a65bfb0442`; the OWR PDF matches the original source-manifest hash `0511e00aa5e3c1b778f66f0e5b8fb00ab02b1103550bbd7941e2bd0c1bb62442`; and the Sano PDF matches `8f579f65fbb653c8543533910a62567de5a3d469acb9cbcf270e7ca32b652e8b`.

The published facts needed are a generic reduced-system Newton formula in mixed fiber polytopes, its unmixed face coefficients, a hypersurface face-integral Newton formula, and signed smooth Euler coefficients. The following target specialization and conversion to the ξ_T hull are deductions made and checked here; I do not attribute these exact paragraphs, Hurwitz notation, or target-specific proof to the old article.

## Genericity and projection: the potential central gap is repaired

There are two valid routes; confusing either one with identical rows would invalidate the inference.

**Independent-parameter route.** Let F_i=∑_a t_{ia}x^a for i=0,…,n−1, with independent parameters t_{ia}. Each Newton polytope is Γ_i=conv{(e_{ia},a)}. Every nonempty face truncation in row i has a nonzero derivative with respect to an active t_{ia}. Selected distinct rows use disjoint parameter variables, so a corresponding Jacobian minor is diagonal and nonzero. This proves the general-position condition of Definition 5.5, even beyond its injective-face requirement.

Now apply the coefficient-space linear map L(e_{ia})=e_a to the resulting polytopes. This is the definition of the restricted weight polytope; no polynomial evaluation occurs, so no cancellation occurs. Every LΓ_i becomes Γ=conv{(e_a,a)}. Fiber integrals commute with L, since evaluation at any covector w after projection equals evaluation at L* w before projection. For graph polytopes the minimizing sections are piecewise affine. Equality of all support functions proves the diagonal identity; polarization proves the mixed identity. Signed Minkowski identities also commute with L. This route verifies ESTEROV_SPECIALIZATION.md.

**Generic-constant diagonal route.** The old DERIVATION takes F_i=∑_a κ_{ia}t_a x^a. Every Γ_i now equals Γ before projection. Choose κ in the nonempty open set where every rectangular row/column submatrix has maximal rank. Compatible faces of the identical polytopes select the same active column set I. For q selected rows, q≤|I| gives full row rank of the parameter Jacobian. For q>|I|, full column rank means the equations have no simultaneous zero in the parameter torus. Thus zero is a regular value in every required case.

Writing the ordinary product discriminant as D_B(c)=∑_β C_β c^β, the coefficient of t^z under this substitution is ∑_(πβ=z) C_β κ^β. The distinct β give distinct κ-monomials, so this coefficient polynomial is not identically zero. Avoid finitely many zero sets, intersect with the rank open set, and obtain Newt(D_B(κt))=π Newt(D_B). The proof is valid; it does not assert survival for arbitrary κ. In particular, κ=1 makes rows identical and can annihilate the polynomial. Theorem 5.10(2) supplies only containment in such nongeneric situations. This route verifies the old DERIVATION's actual genericity/cancellation step.

## Face coefficients, normalization, and support-to-vertices

Identical full-dimensional supports are analogous. Primitive Delzant edge steps at one vertex belong to A and form a lattice basis. Holding other summands fixed shows the pairwise-difference lattice of nA is the full Z^n. The divisor in Theorem 5.10 is therefore one. Induced face lattices are full too; no triangulation-simplex unimodularity is assumed. The affine differences of B generate Z^n⊕Z^(n−1), so Esterov's possible power in Definition 2.7 is one and the ordinary discriminant convention is recovered.

Let Σ_F be the Minkowski integral of Γ_F=conv{(e_a,a):a∈A∩F}, in the coefficient coordinates. With k=n and l=n−1, faces below dimension n−1 contribute nothing. The positive exponent tuples in the top-face term have total n+1 and n entries: exactly one entry is two, giving n copies of Σ_Q after projection. A facet has total n and exactly one tuple, all entries one. Signed smooth obstruction is (−1)^(n−dim F), by Proposition 1.27. Thus the prior theorem yields an **actual** compact convex polytope K with

\[
K+\sum_{F\text{ facet}}\Sigma_F=n\Sigma_Q.\tag{1}
\]

Its difference notation is a Minkowski difference, not arbitrary set subtraction. Existence and convexity come from the old Newton theorem.

Definition 1.8 uses (j+1)! times ordinary lattice measure on a j-face. On a j-simplex σ of normalized volume V, the integral of each barycentric coordinate with this measure is (j+1)!·(V/j!)/(j+1)=V. This gives the exact GKZ coordinate, including j=0. For a generic lower height w with triangulation T, restrictions to supporting faces use only their own A-points. Consequently

\[
\min_K\langle w,z\rangle=\langle w,n\eta_{T,n}-\eta_{T,n-1}\rangle.\tag{2}
\]

Equation (2) holds on the full open height chamber for T. The lower support of an actual polytope is linear there, so its gradient is its unique minimizing vertex ξ_T. This proves ξ_T∈K; it is not the invalid assertion that a difference of arbitrary independently chosen vertices is a vertex. Conversely each vertex has an exposing covector in an open normal cone, which can avoid the finitely many circuit hyperplanes. Every vertex is therefore some ξ_T. Equivalently density and continuity of support minima establish K=conv{ξ_T}. Unused A-points, nonunimodular simplices and multiple triangulations labeling the same vertex cause no gap.

For the old generic-diagonal route, the identification with π Newt(D_B) follows from Cayley Theorem 2.31: codim J=n−|J| for a nonempty row subset. Every proper subset fails the required inequality after adding a row; only the full-row Cayley configuration remains. For n=1 the one-equation discriminant definition applies directly. This is an algebraic identity used as an established input, plus a stronger combinatorial Newton computation; the latter is the additional content beyond invoking the known equality alone.

## An independent product-formula cross-check

There is also a way to compare the face expressions without explicitly equating the polynomials in the deduction. Theorem 4.10, applied to the universal independent coefficients of B, expresses the ordinary product discriminant in face integrals. Its product variety is smooth, so the signed coefficient of F×E is (−1)^(2n−1−j−l). Projection sends its graph polytope to Γ_F×E. A j-face F and a standard-simplex l-face E give

\[
L\Sigma_{F\times E}=\frac{(j+l+1)!}{(j+1)!\,l!}\Sigma_F
=\binom{j+l+1}{j+1}\Sigma_F.\tag{3}
\]

There are binom(n,l+1) such E. Hence the coefficient on each j-face integral is

\[
c_{n,j}=\sum_{l=0}^{n-1}(-1)^{2n-1-j-l}
\binom n{l+1}\binom{j+l+1}{j+1}.
\]

The n-th finite difference of binom(j+r,j+1) gives 0 for j<n−1, −1 for j=n−1 and n for j=n. Therefore π Newt(D_B) equals the actual K in (1). Its triangulation model is the candidate's exact hull by (2). Applying the same support-gradient reasoning on B gives the massive alternating m_U model, without borrowing the old GKZ/fan adversary's verdict. This checks the requested implication through a materially independent expression of the same published machinery. It does not claim a foundational proof of Theorem 4.10 or 5.10.

## What the priority finding does and does not establish

The known geometric equality alone is insufficient to settle a proof request. The checked stronger prior formula, however, supplies the full all-dimensional model equality and a support computation using lattice normalization and barycentric integration. It does not use Sano's analytic equality as a support identity. Under the candidate's stated meaning of combinatorial proof—comparison inside established algebraic-combinatorial/GKZ foundations—the prior implication is complete. **No substantive mathematical defect remains within that regime, and no step transfers the target to an equally difficult unsupported claim.**

There is an essential wording limit. Theorem 5.10's own proof uses Cayley trick and elimination; related inputs use Euler characteristics. Thus this audit does not certify an elementary proof independent of all algebraic/topological foundations. If the intended OWR request excluded any theorem whose proof uses Cayley, this implication would not prove that stronger proof-type claim. The candidate also expressly permits foundational GKZ theorems, so such a stricter criterion must be stated and applied consistently before either route is accepted. No explicit such foundational prohibition appears in the inspected target sentence.

No inspected old publication prints the candidate's exact product-refinement/centroid/binomial/equal-column normal-fan algorithm, or explicitly names and resolves the later OWR question. A prior general theorem sufficient to derive an endpoint is different evidence from a prior printed target-specific proof. The present finding is the former. Candidate Section 3's arbitrary-product-refinement vector identity may be a useful distinct presentation or intermediate statement, but its originality has not been established. The support-function endpoint is already accessible from the older formula; a different presentation alone does not establish that the mathematical task was genuinely open.

For the user's publication rule, this is enough to reject promotion of the existing scoped target as a newly solved open problem. Recommend `already_solved` **for the prior-theorem-implied smooth model comparison**, with the exact qualification preserved. ROOT subsequently confirmed that it treats the cited Sano theorem's smooth complete very ample degree≥2 hypotheses as the scientifically restored model-comparison regime, rather than every introductory A. Under that restoration the prior implication is sufficient for disposition. If a separate unrestricted question is later defined, retain its gap separately; neither prior implication nor candidate proves the singular/sparse version. There is no PR55 human exception known to this child.

Required repairs before any future disposition: cite the precise 2010 theorem and specialization; replace any claim of newly resolved equality or first non-Kähler proof; distinguish prior-implied target from exact prior printed proof; preserve smooth/complete/very-ample/full-lattice/degree≥2 scope; qualify the current full_source_solved field against the abbreviated source; and keep novelty of the exact alternative presentation unestablished. Root alone decides and performs status reconciliation, preservation, merge or publication actions.

## Validation and remaining gap

check_controls.py passed all bounded controls: exact product coefficients through n=20, factorial factors, barycentric normalization through j=8 including nonunit volumes, the quadratic Q=[0,2] sign/translation control, and a two-row bilinear cube eliminant. Generic row constants retain all three projected exponents of that cube polynomial; identical rows annihilate it. CONTROL_RESULTS.json has actual UTC start/end times and individual results. The infinite-family reasoning is the written support/formula deduction, not the count of 3,355 controls.

No mathematical missing claim remains in the prior implication for the specified candidate theorem. Remaining uncertainty concerns unrestricted OWR scope, exact candidate-mechanism historical priority, and any stricter interpretation of proof type. No exhaustive literature-absence claim, earlier printed Hurwitz proof claim, human/refereed/formal certification, outside contact, DOI, release or publication claim is made.
