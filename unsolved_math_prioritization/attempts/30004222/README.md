# Corrected prior type-A clasp formula: qualified dossier

**Rank 718 · ID 30004222 / OWR-17135-015 · unsolved · 1/5 substantive author turns.**

## Current accepted proof

Read the [corrected result](corrected_release_20261005/RESULT.md), the complete [normalization reconstruction](corrected_release_20261005/NORMALIZATION_RECONSTRUCTION.md), and the final independent [delta acceptance](delta_audit_20261005/safe/DELTA_AUDIT.md). Acceptance is bound to corrected manifest SHA-256 `e4d60b6104abc8ad609d6b9ce5af8ca5796ba48c139b10a59f0181b560706914`.

The all-rank type-A formula is attributed to Stuart Martin and Robert A. Spencer, *Cell modules for type A webs*, Math. Z. 312, 119 (2026), Theorem 5.11 ([published article](https://doi.org/10.1007/s00209-026-03990-0)). The accepted bridge is a corrected, dependency-aware reconstruction:

    kappa = (N')^(-2) = B = K,
    1 = (N')^2 kappa.

Here B is the fixed terminal-step divided-power norm quotient and K is the selected 01-root product. A written all-rank telescoping and q-factorial proof gives B=K. Actual form compatibility, the coefficient-one divided-power/light-ladder comparison, and orthonormality give the norm equation without assuming the desired scalar. Quantum skew Howe duality, extremal-projector/clasp identification and the cited orthonormal-basis theorem remain explicit external dependencies.

This does not certify literal consistency of every printed proof label or an unqualified purely combinatorial explanation of the [original 2019 question](https://doi.org/10.4171/owr/2019/39). The queue deliberately remains **unsolved, 1/5** under that qualitative standard. There is no novelty claim.

## Supersession and source corrections

**The original `release/` is preserved historical evidence, still REVISE_REQUIRED. Its old normalization assertions are retracted and must not be treated as current claims.** The [first full audit](audit_20261005/safe/AUDIT.md) identified the defects and supplied the complete replacement proof. The separate corrected release incorporates that proof unchanged. The [exact old-to-new diff](correction_binding_20261005/safe/OLD_TO_NEW.diff), full file inventory and later delta acceptance bind the repair. Removed diff lines and labeled old-claim fields retain history only.

The corrected release's frozen pending-review language records its state at preparation. The separate later delta acceptance supplies final review without rewriting any frozen bytes. All five trees are retained byte for byte.

- Eq. (5.15) gives the inverse square; the contrary square label in Lemma 5.10 is substantive.
- Eq. (5.38)'s all-j product cannot stand for a terminal step unless divided by the parent product. The proof fixes j=s and also verifies parent-path cancellation.
- Eq. (2.15) needs both the correct increment condition and old-shape axial distances. Fixing only one is insufficient.
- Under the standard left-action convention the Weyl direction is inconsistent. The proof specifies the intended root set by explicit 01 pairs.

Scope: generic q, all type-A ranks, integral dominant endpoints, an exterior-power increment, and the specified preferred-basis normalization. The regular characteristic-zero q=1 specialization is included. Other Lie types, arbitrary roots of unity, positive characteristic and unrestricted highest-weight increments are outside the claim.

## Reproduce and interpret checks

Requires Python 3.10+ (standard library) and GNU patch. From this directory:

```sh
python3 -B verify_publication.py [optional_external_manifest_sha256]
python3 -O -B verify_publication.py [optional_external_manifest_sha256]
```

The wrapper uses explicit exceptions rather than assertions for integrity checks. It launches frozen verifiers with assertions enabled even when invoked under -O or with PYTHONOPTIMIZE set, verifies exact membership and five independently supplied manifest anchors, checks the final qualified verdict, replays the complete old/new binding and delta (including patch application in a temporary directory), and rehashes every public input afterward. It neither writes to the evidence trees nor needs a network.

The 11-file correction has 8 modified and 3 added files. Replays reproduce 7,085 admissible vertical strips, 10,935 inadmissible cases, 7,085 central shifts, 12,173 horizontal inverse-square matches, 36,519 rational-q and 14,170 q-sign evaluations. Fresh independent terminal controls additionally cover 7,274 strips, including 3,108 with a nonzero last row and 14,548 rational evaluations. These are bounded formula diagnostics. The universal product identity is established by the written proof, while identification with the actual form uses the stated dependencies.

The exact live UnsolvedMath page and upstream raw statement/AI report were not inspected. The original 2019 primary contribution was inspected. Scholarly public URLs, source PDF hashes and sizes, retrieval/inspection history, source-specific findings and limitations are preserved in the bound metadata. There is no claim that dataset hashes substitute for source inspection. Independent AI audit is not conventional human peer review or proof-assistant certification.

## Included and excluded material

The five preserved trees contain authored analysis, proof, audits, code, public verification metadata and the correction diff. Source PDFs, extracts, images, raw dataset records and private coordination files are excluded.

This is one draft PR, changing only the target row's Status, Turns and previously blank Findings. Chat, DOI, all other queue bytes and the existing embedded queue header are preserved. No queue regeneration, merge, release, new DOI or outreach is included.
