# Fresh finished-preprint adversarial review 01

**PASS — no actionable mathematical, reproducibility, metadata, source-credit, or PDF findings.**

Completed 2026-10-13 UTC for PR256 / problem 5100017 / AMR-050-0017 / k307. Review completion estimate: **100%**. This is a fresh AI adversarial review of the finished candidate, not external human peer review or proof-assistant formalization. No external individual was contacted; no provider, Git, manuscript or original package write was performed. All review work is in `preprint/review_01/`.

## Exact object and independence

I read the complete five-page preprint source and PDF, both deposit metadata files, README, requirements, portable runner and the complete ZIP inventory. I recorded my independent mechanism and falsifiers in `INDEPENDENT_MECHANISM.md` before reading earlier mathematical reports, proofs or verification programs. Neither root acceptance nor prior review conclusions were premises of my proof check. The completed fresh derivation is `INDEPENDENT_DERIVATION.md`; `fresh_exact_checks.py` reproduces 73 exact coefficient and Cartesian checks.

The accepted statement assumes `a>b>0`, `0<lambda<b²`, a confocal elliptic caustic, primitive even period `N>=4`, trajectory ordering, full tangent-line feet and signed moments. It asserts centroid phase independence on the exact nonzero signed-area domain. It does not silently replace this by an unsigned-region centroid or an arithmetic vertex mean.

## Mathematical audit

- **Topology and stars:** I independently reconstructed the finite cyclic group argument for antipodal pairing. Commutation and primitive even order are sufficient, including stars. The origin-left chord condition and half-turn-equivariant Gauss map give `0<delta_i<pi`; consequently `S(0)>0` and neighboring outer tangents meet finitely. Repeating an odd primitive orbit is correctly excluded as a substitute hypothesis.
- **All-period moment:** The fresh checker starts with the projected edge itself and its formal conjugate, averages antipodal edges, then extracts all polynomial terms. It independently obtains both printed linear coefficients and the full cubic term. Their exact endpoint differences, the doubled-normal telescope, and a separately recorded translation endpoint potential check. This is an all-period algebraic proof mechanism; numerical enumeration is not used as its proof.
- **Denominators and exact domain:** `F±ed>0` controls `F` and `F²-e²d²`; `S(0)>0` and the derived area ratio make `2F+d|M|²` precisely the signed-area zero condition. Negative `d` gives exactly the stated fixed circle. The domain excludes that circle even if an individual numerator also vanishes. No division by the pedal area occurs in the polynomial identities.
- **Four-period and simple boundary:** The two antipodal support identities establish `N=4 => d=0`; the normal increment proves the converse. Unrestricted rectangle shoelace confirms `C=M/3`. For simple winding one with `N>=6`, the squared half-orbit normals form a distinct convex polygon traversed twice, giving `S_Z>0`, hence `d>0`. The excluded circular, hyperbolic and degenerate caustic boundaries are not used to enlarge the theorem.
- **Exact star:** Direct Cartesian checks certify all eight points, all chord tangencies, actual unit-vector specular reflection, positive orientation, eight distinct points and exact ray-crossing winding three. Unrestricted symbolic `X,Y` projection/shoelace reproduces all three printed polynomials. The diagnostic point has exactly zero area and the stated nonzero first moment. The reuse and nonnovel-construction credit is explicit.
- **Final formula:** The moment-to-centroid reduction, conversion from `D=F/d` to the printed `F,d` expression, parameter `v`, area ratio and four-period formula limit check exactly.

No central step transfers the problem to an equivalent unsupported invariant. The strongest verified result is the stated all-period signed theorem and its exact domain, under its explicit hypotheses.

## Portable package replay and completeness

A fresh extraction under `review_01/extracted/` passed ZIP CRC, path-safety and symlink checks. Its content is **exactly 37 manifested files plus MANIFEST.json**; each manifested byte count and SHA-256 matched. The archived LaTeX source equals the reviewed preprint source byte for byte. README, metadata, requirements, license and runner copies also equal their outer copies. The deposit metadata equals `metadata.json` exactly, and its two named files exist.

The complete portable runner `run_verification.py --full` passed all seven programs in **72.495 seconds**, using the supplied disposable runtime at the absolute `initial_review_20261013/reproduction_environment/bin/python` path. The observed runtime was Python 3.14.6 with exactly SymPy 1.14.0, mpmath 1.3.0, NumPy 2.3.4 and SciPy 1.16.3. Each archived script was copied into a fresh temporary directory under this review folder. Every archived evidence file retained its hash after replay.

| Replayed program | Result |
|---|---|
| original independent exact controls | PASS, 4,355 assertions |
| independent real Cartesian certificate | PASS |
| independent exact winding certificate | PASS, least period 8, winding 3 |
| author controls | PASS |
| original independent 85-digit controls | PASS, 34 families and 6,108 diagnostic assertions |
| independent Laurent and 90-digit tangent-generated controls | PASS, 141 families, 564 phases, 2,520 pedal cases and 264 zero-area cases |
| independent 110-digit physical-reflection controls | PASS, 84 phase cases including `N=200`, near-circle and strongly eccentric examples, primitive stars and near-degenerate caustics |

The full runner includes every default-run task, so a second identical default run was unnecessary. Replay receipts and outputs are in `PORTABLE_FULL_RECEIPT.json`, `portable-full.stdout.txt`, `portable-full.stderr.txt` and the extracted package's `replay-output/`. `EXTRACTION_RECEIPT.json` records the integrity/completeness checks. Platform-dependent diagnostic maxima and new timestamps were not mistaken for a requirement of byte-identical generated output.

Earlier audit reports contain pending-stage/publication-stage statements and private-machine source paths. README explicitly explains their historical status and intentionally excluded private copyrighted sources/bulk search receipts. They are not contradictory current theorem claims and are not required by any replayed program. The reconstructed floating-point failure history is labeled as reconstructed rather than an authenticated original; successful high-precision controls and the finite-evidence limitation are preserved. The package does not claim exhaustive historical evidence or supply private literature PDFs.

## Source credit, metadata and presentation

I directly checked the original final journal paper's signed definition and [Table 4 k307 / Section 3.4, printed page 346](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf). The source defines the same signed first-moment quotient and lists the even/all-M outer-pedal area-centroid observation. The originating credit to Reznik, Garcia and Koiller is correct. The preprint adds the natural denominator qualification; it does not claim that the historical question mark establishes current open status or firstness.

Bialy–Tabachnikov's Theorem 4.1 is the adjacent arithmetic-mean invariant k306, and Theorem 4.3 recalls the classical even-period symmetry. Schwartz–Tabachnikov's signed centroid-locus work is credited without being substituted for this theorem. The two included bounded priority reports support the limited account of their own searches; the manuscript and metadata expressly decline historical-firstness certification. No new open-ended literature sweep was undertaken. `SOURCE_AND_FINAL_INTEGRITY_RECEIPT.json` pins the three inspected primary PDFs and records the bounded web/source check.

Title, author, ORCID, affiliation, version 1.0, publication date 2026-10-13, preprint status, license, theorem scope, original-source credit and AI/unrefereed disclosure agree among the manuscript, PDF, README, metadata and deposit wrapper. The exact absence of unsigned-centroid or all-star/all-M definedness claims is maintained throughout.

I rendered and visually inspected every PDF page. Equations, overbars, subscripts, bibliography and pagination are legible; no clipping, overlap, unresolved references or missing glyphs were found. PDF text and source agree. The existing compilation log contains no warning/overfull/undefined-reference finding.

## Pinned reviewed candidate

These hashes bind this report to the candidate and ZIP reviewed before this report was added to any future package. A later archive that incorporates this report will necessarily have a different ZIP hash.

| File | Bytes | SHA-256 |
|---|---:|---|
| outer_pedal_centroid.tex | 14,859 | `c740565076e9a1aa67ce6cb9a4ec64d4110ac55adaeb339d9d1b16089cabd88a` |
| outer_pedal_centroid.pdf | 69,903 | `988ff679538849d4bfaa6c7bdd60077e35533aa24baa17cf1e386ec57fb40411` |
| metadata.json | 1,892 | `9cb5db7dd13fc98085bcb8e1395de4613912fb0b43dd16b763766a6685d5a483` |
| zenodo-deposit.json | 2,096 | `f32f9684f61e6d05ab21b2fafb1876672e37c594c1106585fa9c11bf102e49bb` |
| README.md | 3,639 | `83b8151f0d1c9332b97bbab90869cef54b3623a39126a3b00aa8a9a05a1e4788` |
| outer-pedal-centroid-verification.zip | 103,747 | `7c2a3ce49e095b4d0e045cf60c1c19d7137dc6a659a699d922b400493f07bf33` |

The reviewed candidate was rehashed unchanged at review close. The machine-readable full paths, sizes and hashes are in `REVIEWED_HASHES.json`.

**Remaining issues:** none. **Optional preferences:** none promoted. This PASS is for this exact scientific candidate and checked package; it is neither historical exclusivity nor external human peer review.
