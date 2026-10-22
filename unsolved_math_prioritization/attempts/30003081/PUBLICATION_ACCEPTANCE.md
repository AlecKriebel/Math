# Publication acceptance: logarithmic deletion

Problem 30003081 / OWR-14222-009, queue rank 992. Review date: 7 October 2026.

## Decision

Accept the five precisely scoped partial results and their independent AI mathematical audit. The broad primary-source problem remains **unsolved, 5/5 approaches used**. No mathematical correction is required. No sixth proof-search turn has been spent on publication. The only derived change is the optional diagnostic catch described below.

This decision incorporates the complete [independent written report](independent_audit/REPORT.md), all five [authored approaches](original/RESULT.md), and the independent exact computations. It does not upgrade finite computations into universal proofs. It is not human peer review, proof-assistant verification, a novelty certificate, or an exhaustive literature search.

## Target fidelity

The official source is Schenck's logarithmic-vector-field contribution, printed pp. 687–689 of [Oberwolfach Reports 14/2016](https://doi.org/10.4171/owr/2016/14), especially Theorem 1 on p. 688 and Question 1 on p. 689. It asks for a higher-dimensional version of a logarithmic deletion sequence using logarithmic Chern, CSM and Jacobian Segre classes. The catalogue's unexpected-curve title and unexpected-hypersurface interpretation are a mismatch with that question. The title and other catalogue/source fields remain historically intact; the Findings cell explains the distinction.

The relevant map uses actual logarithmic tangent sheaves. With smooth X and H, reduced A sharing no component with H, and R=(A|H)_red, it is G=Der_X(-log(A+H)) to i_*E=i_*Der_H(-log R), with kernel F(-H), where F=Der_X(-log A). The packet constructs this map and proves the kernel rather than assuming a desired exact sequence.

## Accepted mathematics and limits

1. **Product/SNC exactness.** Explicit local product coordinates give surjectivity onto E, of rank dim(X)-1. The original curve line bundle is the dimension-two case, not the higher-rank quotient in all dimensions. This does not extend to arbitrary quasihomogeneous pairs.
2. **Credited seven-plane obstruction.** The arrangement is [Abe–Kawanoue's Example 4.3(3)](https://arxiv.org/abs/2406.00305), not a new discovery. The reconstructed quadratic field x(x-y) partial_x does not lift in the affine chart at [0:0:0:1] in P^3. A homogeneous-jet argument covers germ lifts. This disproves the specified natural unrestricted quotient sequence, not all higher-dimensional analogues or the full open-ended source request.
3. **Local defect criterion.** The restriction cokernel equals the image of the constructed obstruction into z-torsion in the Tjurina module. The obstruction need not fill that torsion. A non-zero-divisor cut suffices but is not necessary. No untwisted global Tjurina identification is asserted.
4. **Full Chern-character defect.** On P^n the difference of the three specified sheaf classes is the actual cokernel class. GRR and projective Hilbert positivity imply complete Chern-character defect zero if and only if restriction is onto. Low-degree Chern information alone can miss a point defect. The packet does not prove the required vanishing under the broad source hypotheses.
5. **Depth/reflexivity criterion.** Local freeness of both ambient logarithmic sheaves and codimension-one surjectivity imply exactness everywhere. Both hypotheses remain explicit. Local quasihomogeneity alone does not provide them.

The audit checks the signs, ranks, local arguments, dimensions, hypotheses and projective interpretation, and independently reconstructs the finite linear systems. Standard general theorems such as GRR, Serre vanishing and Auslander–Buchsbaum remain imported inputs.

## Separate subsequent literature

[Abe–Denham](https://arxiv.org/abs/2203.04816) supplies credited hyperplane-multiarrangement free-surjection and defect results, without proving the broad smooth-hypersurface statement. [Trok's Corollary 4.15](https://arxiv.org/abs/2003.02397) concerns multiplicity along a general codimension-two linear space. For n>2 this is not a general fat point. The accepted deduction uses the elementary dimension nd+1 and the imported duality in exactly that scope. Theorem 5.27 is not relied on. The [Janasz–Malara–Tutaj-Gasińska preprint](https://arxiv.org/html/2511.10772v1) provides a related sufficient criterion, not an audited unrestricted equivalence or a resolution of Schenck's question. Relevant sections and statements were inspected; full general proofs and all literature were not reverified.

## Immutable and derived material

- `original/` contains all 16 frozen author files unchanged, manifest SHA-256 7cec8ef8716ab0e930d6c03f2cd4d8559214d9329ccde8ef258cd9a8d3c7ae55.
- `independent_audit/` contains all 16 frozen audit files unchanged, manifest SHA-256 4f5950d90f5b2db1d69ed83760bec88dbeeb28005340e325c688567277f470de.
- `corrected/` preserves every author byte except one SyntaxError catch in `verify_packet.py` and its mechanically rebound manifest row. Its manifest SHA-256 is 178ee6e7b46973dae0286b07184f1ca2c3456f8270c812302869c7d31ebba3a9. The preserved audit `HARDENING.patch` has an off-by-one hunk header: its context begins at line 76, while it declares line 77. It remains unchanged. The separate `HARDENING_REPLAY.patch` changes only that old/new start offset from 77 to 76. The wrapper verifies this exact header-only derivation, then applies the canonical patch with exact positions and context, without fuzzy matching or offsets, and reconstructs the entire derived manifest. This optional change standardizes a REJECT diagnostic. The original already rejects malformed Python in normal, -O and -OO modes.

Historical author wording about awaiting independent review and no remote publication remains unchanged. The audit's pre-publication wording likewise records its own stage. This acceptance records the subsequent scoped acceptance; none of those historical statements is a current claim that no audit exists.

## Reproduction and privacy boundary

The publication wrapper authenticates an externally pinned outer manifest, validates a strict recursive inventory and immutable inner anchors, rejects symlinks/special files, rejects ill-typed, duplicate-key and nonfinite JSON, parses executable files without optimization-removable assertions, and replays exact diagnostic outputs. Its executable bytes must themselves be authenticated externally before execution. Mutation tests exercise that bootstrap and deliberately malformed disposable fixtures, including re-pinned malformed manifests and rebound frozen checkers.

Normal, -O and -OO replay supports relocated read-only inputs. The historical mutation programs receive an exact writable temporary staging copy because they mutate disposable fixtures without changing copied file modes. Frozen packet bytes are checked before and after; no frozen-source write is part of replay. Exact source/PDF checks are **NOT_RUN** in portable replay because the original bytes are deliberately absent. Requesting missing PDF or corpus input must fail closed. Optional source programs and prior checks remain preserved as metadata and code, without source redistribution.

All included computations are bounded diagnostics. They are not an arbitrary-hostile-code sandbox, a filesystem-race guarantee, a resource-exhaustion defense, or a substitute for the written proofs. Public source titles/URLs, hashes, byte counts and inspection metadata are included. Source PDFs, extracted source documents, dataset contents and private coordination material are excluded. The only repository changes are this problem's packet and its three authorized queue cells. No merge, release, outreach or unrelated-hold change is part of this publication.
