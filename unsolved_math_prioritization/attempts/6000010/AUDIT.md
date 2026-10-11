# Mathematical audit: local tangent-line models of symplectic surfaces

**Verdict: PASS for the bounded local real-dimension-two theorem under the explicit canonical symplectic/statistical Codazzi interpretation.** The result completely characterizes this stated subclass. The original item does not define compatibility, and this audit does not claim a solution under every possible interpretation or in unrestricted dimension. No novelty assertion is certified.

## Exact identity and inputs

- Numeric problem ID: **6000010**.
- List identifier: **AMR-059-0010**.
- Original proposer and location: **Takashi Kurose, item 3(d), printed p. 126**, in Furuhata-Matsuzoe-Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, IIS 4 (1998), 125-127.
- Candidate inspected: 3865 bytes, SHA-256 `c0923affc41dd0fb7fa574a39b29ffc497de970d416546535ea498ad280176e8`.
- The frozen source PDF is 400903 bytes, SHA-256 `fa552d73c0f1e1017608102a7a80eff048cd3d95ed413ae04c2fdf710da3b8f5`.
- Both entries match the frozen candidate and source records. A fresh retrieval during the mathematical audit from the original public URL matched the PDF byte-for-byte.

## Findings

1. **Forward construction passes.** The induced tensor is positive definite with determinant `a^2`; the symplectic and almost complex sign conventions agree. The integrating-factor substitution produces a nowhere-zero Killing field at every point of an open tangent patch, without a zero-section assumption.
2. **Converse passes.** Flow-box coordinates are legitimate precisely when the Killing field is nonzero at the distinguished point. Starting with every possible cross term, the change `z=t+integral(C/B) dx` gives `a=A-C^2/B>0` and `b=B>0`. Then `y=sqrt(b/a) z` and `Gamma=-(log sqrt(b/a))'` recover both tensors. The proof includes every derivative and cross-term cancellation.
3. **Orientation and J pass.** Coordinates can be chosen in the symplectic orientation; both subsequent coordinate maps have positive Jacobian. The symplectic form is the metric area form. Pullback equality of the metric and symplectic form uniquely determines equality of J. An unoriented metric isometry alone would be insufficient.
4. **Statistical scope passes.** The original item uses the word compatible without spelling out its tensor definition there. The interpretation is substantiated independently by the canonical-form computation and by Satoh's Definition 2.1, equation (2.3), and Theorem 3.1. In dimension one, every affine connection satisfies the statistical condition. Imposing metric parallelism would be a substantive and unjustified narrowing.
5. **Zeros and the obstruction pass with their stated limits.** Nontrivial is not interchangeable with nonvanishing. The added rotational example proves the distinction and proves that the curvature-wedge obstruction is not sufficient. An explicit nonzero-wedge example demonstrates that not every compatible symplectic surface is represented.
6. **Constant-curvature special cases pass.** Every constant-curvature surface has a local model at every point. The choice of a Killing field matters: a zero of one rotational field does not exclude a different nonvanishing local one. The Levi-Civita-only model subclass is precisely locally flat, whereas statistical connections yield positive and negative constant-curvature examples.
7. **Higher-dimensional formula passes.** With conventions fixed, the Nijenhuis formula includes a horizontal torsion term and a vertical curvature term. Torsion is zero under the candidate's standing assumption. No higher-dimensional characterization follows.

## Editorial clarifications, not a failed proof

- Read "near that point" as **a field defined on a neighborhood with X(p) not equal to zero**, then shrink to make it nowhere zero.
- Prefer "Levi-Civita-only Sasaki construction" to an unqualified exclusion of "Sasaki metrics": the name Sasaki metric is also used for the broader metric built using an arbitrary affine connection, as in Satoh's paper.
- The original source does not itself print a definition of compatibility. The audit makes that interpretation explicit rather than treating it as a verbatim definition from item 3(d).
- Classical forward-construction results alone are not evidence that Kurose's unrestricted inverse problem is solved. This audit makes no such claim.

## Deliverables and evidence limits

[PROOF.md](PROOF.md) is a full self-contained proof with sharpness examples. [SOURCE_PINS.json](SOURCE_PINS.json) supplies public bibliographic URLs, exact PDF bytes and hashes, version information, and inspection scope. [CHECK_RESULTS.json](CHECK_RESULTS.json) records aggregate results of actual normal, -O, and -OO executions checking the frozen inputs, independent source match, artifact inventory, and symbolic identities. The accepted mathematical body and all displayed equations are preserved in full; the interpretation qualification is explicit.

The original problem and relevant Satoh definitions and formulas were read directly, with visual checks of the original scanned page and Satoh PDF pp. 4 and 8. Satoh's unrelated curvature and Einstein results were not independently audited. No exhaustive novelty or current-status literature search was attempted. Symbolic checks support, but do not replace, the proof.

The public packet contains authored mathematics and public bibliographic and aggregate verification metadata. It excludes copied source documents, extracted source text, page images, datasets, and executable checking code. This is an assistant-prepared mathematical audit, not external human peer review or formal proof certification.
