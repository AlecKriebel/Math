# Acceptance of corrected partial results

Date: 2026-10-08. Target: **30006636 / OWR-14299913-005**, rank 1055. Mathematical verdict: **unresolved / accepted partial results**. Queue status: **exhausted, 5/5 substantive approaches**.

## Accepted scope

The unchanged first-stage proof and corrected five-approach report are accepted at their explicit restricted mathematical scope. Both independent mathematical audits are retained. No resolution of the original normalization-unspecified extension question for general source input is claimed.

For the standard untwisted finite-group/transitive-set construction with ordinary traces and identity pivotal functor, let `N=|B||C|`, `m=|M|` and let `a^3=N` be the chosen normalization root. On connected closed oriented four-manifolds, the exact formula is

    I_a(X) = m a^(2-chi(X)).

There exists an ordinary complex oriented four-dimensional TQFT having these unchanged connected closed values **if and only if N is a perfect cube and a is its positive real cube root**. The factor `m` cannot repair a noncubic `N` or a nonpositive/nonreal root. For `N=r^3` and `a=r`, the explicit boundary-color functor has `n=m r^2` colors on each connected closed three-manifold and Euler weight `q=1/r`. It counts assignments of one color to each connected bordism component, subject to matching boundary colors, and multiplies by `q^chi`. This is an existence classification for the stated subclass, not uniqueness or a classification of all extension functors.

The admissible `C2` example has `(I(S1 x S3))^3=4`, excluding every allowed normalization root from the integer-dimension trace condition. Dividing by `m a^2` per connected closed component gives the explicit Euler theory `a^(-chi)`, so the unchanged-value obstruction does not establish failure after all normalization changes.

The remaining accepted partial results are:

- A two-boundary Gram-rank defect for the canonical universal construction, even in a cube-order example where a different ordinary extension exists. It is not a general nonextension theorem.
- A regular `D8` example obstructing a proposed central-lift shortcut while satisfying the source hypotheses and admitting an unchanged ordinary extension with 32 colors.
- A finite-order connected mapping-torus Fourier criterion. Nonzero Fourier coefficients must lie on one positive rational ray to admit a common scalar making them nonnegative integral multiplicities. This necessary trace test leaves the required general-source mapping-torus evaluations unproved.

## Material correction preserved

The original five-approach report omitted **connectedness of Y** in the mapping-torus normalization discussion. For disconnected `Y`, the identity and component-permuting mapping tori can have different numbers of connected components and hence different powers of the normalization scalar. The two-`S3` component-swap example invalidates the original uniform-scalar scope.

The full rejected original report is **not distributed**. Its public provenance is 16,445 bytes and SHA-256 `706122a31f7e3fdcf6b45d2220b5c498cd2d23c50937e2c0f37489b7862ce7ce`. Only the accepted `evidence/FIVE_APPROACH_REPORT.md` (16,612 bytes; SHA-256 `e3c128de7015148827e998dbc5ac779e4167963dfa0fa1f95650f521244eb79c`) and the explicitly contextualized correction patch are published. The patch's removed line is a rejected historical claim, and connectedness is mandatory in its replacement. The original exact unified diff follows the new explanatory preamble unchanged; both original and published patch hashes are recorded in `evidence/PUBLIC_SLICE.json`.

The publication verifier authenticates the corrected report and contextualized patch directly and checks that the replacement appears in the corrected report. It does not require distribution or reconstruction of the full rejected report. The original release README and superseded author inventory are omitted. Historical receipts and audit metadata are provided only as labeled public derivatives with stale artifact inventories removed; all arithmetic outputs, diagnostics and accepted findings are unchanged. Seventeen original release members remain byte-identical. The first-stage proof remains 14,820 bytes, SHA-256 `ea1692e3304a67d1051192bfaba974a8aaead3821bd2f38b7826cbfc00d29cf3`.

## Execution defects and repairs preserved

The original independent normalization checker used assertions, which disappear under `-O`/`-OO`. Removing a stabilizer crossing then produces an incorrect evaluation 32 rather than 16 while still printing PASS. The original follow-up checker explicitly refuses optimized execution and does not falsely claim those checks passed. Both original scripts write results beside themselves and fail on genuinely read-only input.

The separately frozen hardened variants replace assertions with always-active guards, default to stdout, and require explicitly external new output paths. Exact historical-to-hardened execution patches are retained and mechanically reconstructed by the publication verifier. Their complete positive arithmetic output bytes remain identical to the historical results. The historical false pass, explicit refusal, normal assertion controls and read-only failures are all reproduced, not reclassified as fresh mathematical validation.

The labeled public derivative of the historical combined author receipt reports genuine UID/EUID 1000 read-only normal/-O/-OO execution: 12 positives, 81 semantic rejections, 12 explicit external-output successes and 36 path/overwrite rejections. The public hardening receipt derivative additionally records 18 historical controls. PUBLIC_SLICE records exact original/derived hashes and the narrow metadata edits; it cannot authorize an excluded payload. The publication wrapper independently repeats the controls, binds full outputs and exact file inventory, and tests hostile-import isolation. Test inputs and cwd are demonstrably read-only; temporary explicit outputs and disposable historical controls use separate writable locations.

## Source dependencies and remaining gap

The MMT general constructor, finite-set evaluation and transitive-set reduction are external mathematical dependencies: [Categorical 4-manifold invariants from trisection diagrams](https://arxiv.org/abs/2511.19384v1), especially Theorem 4.28 and Section 6.2. The source question is in [Oberwolfach Report 12/2026](https://doi.org/10.4171/OWR/2026/12); [Trisecting 4-manifolds](https://msp.org/gt/2016/20-6/gt-v20-n6-p02-s.pdf) supplies standard trisection background. Exact historical source metadata and inspection locators are retained in `evidence/SOURCES.json` and the audits.

No general normalization-flexible extension/nonextension theorem, general fusion-2-category construction, proof of new priority, or external peer acceptance is established. The finite arithmetic tests supplement written proofs and do not settle those gaps. Fresh source/corpus rebinding is **NOT_RUN**. No additional proof-search turn is represented by this acceptance or execution hardening.
