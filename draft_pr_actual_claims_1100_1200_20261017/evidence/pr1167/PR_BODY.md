## Scoped prior result and endpoint audit

For Ball 2002 Problem 4 / 2000004 / AMR-019-0004, this draft credits the Almi–Krömer–Molchanova Lavrentiev-gap result in its exact two-component Ciarlet–Nečas setting. The accepted ranges are d=2 with p>2 and 1<q<p/(p−2), and d=3 with 3<p<4 and 2<q<p/(p−2). The homogeneous polyconvex energy forces continuity; both comparison classes have the same partial Dirichlet data and CN constraint.

The prior source is [A new example for the Lavrentiev phenomenon in nonlinear elasticity](https://doi.org/10.1007/s00033-023-02132-4), ZAMP 75, article 2 (2024). The inspected versions are the publisher PDF and [arXiv:2309.08288v2](https://arxiv.org/abs/2309.08288v2), revised 8 November 2023. Existence, finite-distortion, change-of-variables and topological results remain external cited dependencies; their deep proofs were not independently reconstructed.

### Two-dimensional endpoint qualification

The logarithmic competitor printed after (3.9) in arXiv pages 10–11 and publisher page 9 has infinite inverse-Jacobian energy at q=p/(p−2). The exact lower-triangular determinant is J=A t^(alpha+beta−1)(alpha L+1)/L^4. At the endpoint it gives J^(−q) comparable above and below to t^(−1)L^(3q), whose reference-coordinate integral diverges. Both printed logarithmic denominator powers are preserved. This is a failed construction/proof step, not a disproof of the endpoint theorem. The strict-range 2D and 3D arguments do not use that endpoint construction.

The complete authored theorem summary, source/hypothesis audit, endpoint/proof notes and bounded acceptance are retained. The proof notes include the normalized distortion term W(I)|Omega_s| and the integrated positive-part/Hölder repair with coefficient 2^(1−p). Two precision edits say that the gradient is lower triangular and that the slice excess quantity is the integral of D(x_1)^p.

No unqualified solution to Ball's connected-domain, boundary-only formulation, no everywhere-injective homeomorphism-class result, and no novelty are claimed. Remark 3.1 does not supply the missing connector estimates or preserve boundary-only constraints by itself. The bounded correction search on 10 October 2026 found no repair; it was not exhaustive. No author was contacted.

This AI-assisted exposition and independent internal AI mathematical/source audit are unrefereed. Bounded acceptance does not mean external human peer review, journal acceptance of these authored documents, or formal proof-assistant certification.

Editorial changes add review framing, remove local workflow references, make the two precision edits above and preserve every source title, version, URL, PDF identity, inspection range and bounded-search qualification. Preparation adds no new source-inspection claim. The edition consists only of authored mathematical prose and public verification metadata. It includes no copied source documents, dataset contents, executable code, private sources, private personal data or private coordination material.

This is an addition-only draft containing nine public files. QUEUE.md and every unrelated path are unchanged.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,696 bytes; SHA-256 `4500593ee905bb112a8630e699244a26ff34f6675e098926cbc19be45a8ace9d`.
- `ACCEPTANCE.md`: 4,608 bytes; SHA-256 `061cb2206eddd49d5b1d3844bb06adbc61d9f85b543daa4ca5ee15809c852518`.
- `ENDPOINT_AND_PROOF_NOTES.md`: 9,851 bytes; SHA-256 `e33605ce503e32a5d0bf7e94451d8eea6b4463ad222d49297e5806165fbaf37f`.
- `MANIFEST.json`: 1,737 bytes; SHA-256 `e4685389e31fff413762ff5d0be7fa075c3f6e7b78c134f222f7ca703b4dacd8`.
- `README.md`: 3,097 bytes; SHA-256 `297c974894802052097f57c24ba88718d1286ff564a6bee2d4ddb8a8978c6040`.
- `SOURCE_HYPOTHESIS_AUDIT.md`: 17,163 bytes; SHA-256 `12c05abb88e19db455a0bccc684c633b6c7aab279f7fcb7a6a1cf0d2806aab39`.
- `SOURCE_METADATA.json`: 4,522 bytes; SHA-256 `43bc85765bc67ddc90cf45fa132d245a701824115409a7f96087bbf0eddd1966`.
- `THEOREM_SUMMARY.md`: 8,260 bytes; SHA-256 `4b594deb41938c6fe2b40902aca6ffe2e6e73a30140bb73b10a3b58c24525020`.
- `VERIFICATION_SUMMARY.md`: 3,081 bytes; SHA-256 `cd6065e2c4d05ed87ea32ca5dbac9ddb2132ac6c60b60822cab3dc489f342b67`.

MANIFEST.json lists all nine public members and hashes the other eight. Its separate identity above avoids self-reference.

