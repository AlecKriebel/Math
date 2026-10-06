# Ricci-flow dimension threshold: audited partial results

**Problem 30000789 / OWR-1588-003, rank 815. Status: UNSOLVED, 5/5 substantive approaches.**

The sharp threshold n_0 = 12 is not established. The accepted result is a closed-cone ODE tangency criterion, explicit failure in dimensions 4–11, and restricted exact tests in dimension 12. The [source clarification S1](SOURCE_CLARIFICATION.md) is mandatory and operative together with the [independent audit](independent_audit/AUDIT_REPORT.md).

## Accepted mathematical scope

- The complete closed-cone invariance criterion includes the nonsmooth scalar-zero apex. Differentiating a squared cone inequality alone is insufficient there.
- In even dimensions the only possible cone parameter is c = n/(n-2). Explicit necessary intervals exclude dimensions 4–11.
- The balanced two-block tensor is a strict local maximum in the 54-dimensional diagonal Weyl subspace at n = 12, with 53-dimensional norm-sphere tangent space. This does not establish maximality in the 1,638-dimensional full Weyl space.
- Four specified two-dimensional pencils satisfy the target cubic inequality globally on those spans. They do not cover arbitrary rotations, multiple simultaneous perturbations, or all Weyl tensors.

The missing global bound is beta_n^2 <= 2(n-1)(n-2)/n^2 in every even n >= 12, with a strict inequality in every odd n >= 13. At n = 12 the bound is 55/36. Proving only that case would not settle the all-dimensions threshold.

The 2008 report defines a strict cone, but its theorem is for the closure. It states PDE sufficiency, whereas the 2007 target concerns ODE equivalence; PDE necessity remains separate and conjectural. The 2007 parity repair is inferred, not an official erratum. Related target 30001006 has a distinct PDE formulation, and this package does not settle its necessity gap or claim a separate discovery for shared algebra.

## Artifacts and historical status

Read [author/README.md](author/README.md), all five authored approach files, [independent_audit/AUDIT_REPORT.md](independent_audit/AUDIT_REPORT.md), and [SOURCE_CLARIFICATION.md](SOURCE_CLARIFICATION.md). Acceptance is scoped partial mathematics, not a solution of the threshold. Neither formal proof-assistant certification, human peer review, novelty, historical priority, nor exhaustive literature clearance is claimed.

Both original ZIPs are preserved byte for byte under archives/. The audit also includes its original nested AUTHOR_FREEZE.zip. Extracted copies match their ZIP members exactly. Historical audit-pending and no-publication statements within the freezes retain their preparation-time meanings; this wrapper records the later scoped acceptance.

## Reproduce

Requires Python 3 and SymPy; observed versions are Python 3.12.14 and SymPy 1.14.0. With a trusted, externally retained SHA-256 of PUBLICATION_MANIFEST.json, run:

    python -I -B verify_publication.py --expected-manifest EXTERNAL_SHA256
    python -I -O -B verify_publication.py --expected-manifest EXTERNAL_SHA256
    python -I -B test_publication_integrity.py --expected-manifest EXTERNAL_SHA256

The external archive/manifest hashes authenticate transport; do not silently derive your trust anchor from a package you have not authenticated. Receipts mentioned inside the freezes refer to externally retained artifact-authentication information, not an additional required public file.

The verifier checks all files and directories, both archives and extracted members, nested freeze equality, both inner manifests, actual correction-patch application, and exact author and independent checker output. The outer harness exercises relocation and deliberate corruptions under normal and optimized Python. Additional original harnesses are author/test_integrity.py and independent_audit/audit_harness.py.

The author reports 85,363 exact checks (mostly componentwise identities) and five mathematical negative controls. The independent implementation uses so(n) structure constants and 2-by-2 minors, performs 69 named aggregate checks and four mathematical negative controls, and has ten deliberate code-corruption controls. These counts are different units, not independent cases proving the global inequality. See the frozen result files and audit for precise coverage.

Only authored mathematical material, code, results and public verification metadata are included. No source PDF, source extract, image, underlying corpus or dataset content is distributed. No release, DOI or external outreach is part of this draft.
