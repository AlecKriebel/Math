# Source and readiness audit

Checked 2026-09-30. The problem URL https://www.unsolvedmath.com/problems/2861 was requested first but did not expose its contents in the reader. The full pinned corpus record and research report are preserved in source_record.json. The precise statement and all remarks were read in K3, printed pp.176–177. This is a closed oriented spin hyperbolic three-manifold problem; neither a cusp problem nor only a reduced invariant.

The inherited queued row was rank84, 0/5. Numeric and descriptive all-state PR searches, matching remote branch search, existing attempt-folder search, state.json, and related_target_groups.json exposed no previous Alec/campaign attempt. Corpus searches found no identical statement. Record30003894 concerns delocalized invariants on universal covers and is distinct. The source-status correction was not a new construction search.

## Primary mathematical source

Lin–Lipnowski, *Closed geodesics and Frøyshov invariants of hyperbolic three-manifolds*, [JEMS article](https://ems.press/journals/jems/articles/14297701), DOI10.4171/JEMS/1452. Official metadata: received17January2022, accepted30October2023, online10April2024, JEMS27(2025), no.10, pp.4201–4281. The [arXiv record](https://arxiv.org/abs/2105.04675) currently lists v1,10May2021. The published PDF was obtained in full. Relevant parts actually read: introduction and p.4206 scope caveat; §§2.1–2.2 spin lifts and geometric input; §3.4 Theorem3.3; §3.5 Gaussian applicability; §4 including Lemma4.1 and formula14; §5 local Weyl estimates; §7 Weeks computation and precision caveats; AppendixC.2 trace-formula scope and orientation; AppendixD extension to Gaussians. Critical displayed formulas on pp.4206 and4226 were also visually checked.

This is a validation of the published theorem's applicability and a direct consequence of it. It is not a fresh derivation of the representation-theoretic Selberg theorem from first principles, and the paper's entire Floer-theoretic computation is not independently replayed. The explicit convergence argument in SOURCE_STATUS.md does not infer an effective convergence modulus from existence of a fixed-manifold nonzero spectral gap.

The source input is a Dirichlet domain and complete finite length-spectrum data, which the authors obtain with SnapPy. Their spin-lift algorithm is elementary finite linear algebra and terminating group-word reduction. This package does not certify the numerical geometric input supplied by SnapPy in arbitrary cases.

## Current-source check

The authors' [arXiv2506.07238](https://arxiv.org/abs/2506.07238), submitted8June2025, current v1, develops Dirac spectral flow for b1=1 and explicitly treats the difficulty of small eigenvalues crossing zero. Its abstract was read as a current-scope check; its full proof is not a dependency of this package. No withdrawal or correction of the imported 2025 JEMS trace theorem was found in the bounded primary-source search. This is not an exhaustive literature search or priority claim.

## Source repair and classification boundary

The old zero-examples-only remark is contradicted by the published Weeks example with its stated numerical caveat. The literal method request has a credited geometric method valid for every closed oriented spin hyperbolic three-manifold. A stronger interpretation requiring a uniform certified stopping algorithm from arbitrary triangulated input is not established here and must not be silently substituted into the status claim.
