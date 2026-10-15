# Independent complete adversarial package review R5

## Verdict and exact inputs

**ACCEPT_AS_QUALIFIED_UNREFEREED_PREPRINT. No actionable correction identified.** The exact sealed note and package are internally consistent, analytically justified and reproducible to the stated standard. This is a bounded mathematical/package acceptance, not a claim of first priority, currently open-problem status, human peer review, formal certification, or actual publication.

Source scope: PR810, problem2307042 / AMR-022-7042; original immutable commit `5820e9784dbcfeda0acabaa435cb38cf6a4576df`. Its QUEUE row has exact status `claimed_solved`. Other PRs excluded. Nine current inputs are those in `PACKAGE_SEAL_R5.json`; start and end SHA256/size checks both pass. No input was mutated. Work stayed on `main`; no Git reference, PR, remote service or publication state was changed, and no individual or other project chat was contacted.

## Independence and strongest verified mathematics

`PROOF_FIRST.md` was saved before any supplied mathematical review verdict was read. It reconstructs the current smooth-annulus theorem, original Problem7.42 quantifiers and scope from the note and original arXiv1809.07200v2 printed pp173–174. `PUNCTURE_INDEPENDENT.md` separately records the punctured-disc triangle calculation and primary-source judgment. An acceptance label in an external identity manifest was incidentally encountered while checking manifest schema after the annulus proof and initial Bear–Smith/Herron source judgment had been saved, before the later Köhn scan inspection; it was not used as mathematical or source authority. Substantive historical review reading followed the completed Köhn source-judgment checkpoint. No package_review_01..04 files or parent acceptance summaries were opened.

Strongest independently verified theorem: on D={1<|z|<e}, at a=exp(1/2), the normalized minimal Martin kernel at the inner-boundary point -1 equals the normalized periodization of sin(πx)/[2(cosh(πt)-cos(πx))], and is strictly below the normalized positive-harmonic envelope on a deleted neighborhood of a. At the base both equal one. Consequently no equality curve with nonbase points tending to a exists, including equality throughout a Green line issuing from a.

The independently checked mechanisms are:

* Strip Green function has the correct positive logarithmic singularity and zero values on both sides. Exponential image decay justifies periodization and each fixed-order derivative; finite-cylinder boundary uniqueness identifies the Green function.
* Uniform source-boundary Taylor expansion g=2πsPη+O(s²), denominator bounded below by a positive multiple of s, proves the Martin ratio limit under arbitrary tangential approaches η→π, s→0. No nontangential restriction or rounding argument is hidden here.
* Dominated positive minorant v has zero boundary values away from ξ. P=x/(πr²)+O(x) uniformly near ξ. Odd reflection has O(1/r) growth, so Fourier/Laurent coefficients exclude higher poles, oddness excludes the logarithmic and tangential terms, and cancellation of the remaining normal dipole gives continuous zero boundary data on the compact annulus. Maximum principle proves minimality. Reflection is applied only to a dominated harmonic v with the required zero boundary data.
* Gradient=(-c,0), c=πΣq²/Σq, with exact 0<c<8/83<1/10. All four competitors are periodic, harmonic, globally positive and normalized. Their support comparison gives a uniform >75ρ/664>ρ/10 first-order gap, with a common quadratic Taylor remainder for the finite family. Envelope differentiability is never assumed.
* The source’s universal per-kernel extension is falsified by one prescribed kernel in one smooth doubly connected Green domain. The source’s disc example explicitly has equality along a radius. The note explicitly disclaims the weaker remote-contact question; local isolation proves no theorem about isolated contact farther away.

No central difficulty has been transferred to an unsupported equivalent claim. No mathematical gap was found in this stated theorem.

## Primary source and attribution checks

Primary originals obtained afresh, stored only in ignored `private_sources/`:

* Hayman–Lingham arXiv1809.07200v2, printed pp173–174: correct problem and Arsove–Johnson attribution; 2018 update is bounded editorial history, not certification of worldwide openness in 2026.
* Köhn1966 original journal scan, printed p63 (visually inspected): explicitly classifies punctured-disc minimal positive harmonic functions, up to positive factors, as disc Poisson kernels and -log|z|. Correct p63 locator. Its symmetric-metric example does not assert the current prescribed-kernel local-isolation or Green-line conclusion.
* Herron1987 primary article, Theorem3 and printed p17: polar-removal representation/metric context and punctured-disc formula. Its symmetric metric does not directly imply contact for every fixed kernel.
* Bear–Smith full author manuscript dated23 May2005, printed p4 Proposition2.6: proof explicitly uses Bôcher representation v+b log(1/|z|), b≥0, and disc/logarithmic minimal alternatives. Current bibliography explicitly attaches the proposition number to this inspected manuscript, while giving corresponding 2006 publication metadata.
* Shiga2016 primary article: §§2.2–3, Theorems3.2/3.4 and Proposition5.1 p455 support the note’s description of Martin-kernel Harnack metric formulations and equality results. Bounded-harmonic annulus statements concern a different function class.
* Leutwiler1987 primary article: one-sided-envelope and symmetrized-metric framework is relevant background; it supplies no independently verified prescribed-annulus gradient calculation.

Independent punctured-disc deduction: at a=1/2, target normalized pole -1 has gradient(-8/3,0); normalized poles±i have gradients(-32/15,±8/5); normalized logarithm has gradient(-2/log2,0). Exact log2<3/4 places target strictly inside their triangle. Positivity, normalization, minimal Martin eligibility and common Taylor remainder give local isolation. This is elementary derivability from classical representations. It does not establish who first recognized or published this consequence and does not yield the smooth-annulus construction. The note, README, current priority addendum and metadata retain those distinctions. Historic frozen inspection limits are transparently superseded by dated records, not silently rewritten. Inaccessible/full-text gaps in the priority packet are disclosed. No first-resolution claim is promoted.

## Code, diagnostics and archive findings

Normal and optimized runs of the current standard-library diagnostic pass and agree exactly except timestamps. Forced diagnostic failure rejects under both. Reproduced Poisson-image/Fourier comparison, independent Fourier derivative, Green-image/Fourier comparison and symmetry, normal/slanted/extreme tangential approaches, uniform singularity stress and direction mesh. The analytic tails are consistent with the formulas; finite precision is not interval-rounded. Values c≈0.00032498636, b≈0.443409442, diagnostic minimum first-order slope≈0.405216489, sampled smallest gap/radius≈0.195976850. These diagnostics hunt errors; they establish neither a numerical contact-free radius nor a rounding certificate or proof.

Independent archive checker `audit_archives.py` passes24 checks. `verification.zip` has66 exact members; every manifest has its asserted closed inventory and correct SHA256/size (including source Git blob hashes where supplied). Three nested historical ZIP archives each match their expanded source directory byte for byte and their external inventories. All40 original source snapshot files match the original immutable Git objects. Selected current public files match sealed input bytes; the selected public supplement is exact. All recursive ZIP wrappers are closed: no unlisted local-record gaps, prefixes, suffixes, comments, extras, executable members, symlinks, encrypted members or unsafe paths.

Supplied integrity verifiers pass normal/optimized runs; altered extracted bytes and an unlisted extracted member are rejected under optimization. The second-review bootstrap passes normal/optimized. Integrity replay is explicitly distinct from mathematical proof.

A clean extraction rebuilds `verification.zip`, `zenodo-deposit.json` and `zenodo-upload-kit.zip` byte for byte when supplied the sealed PDF. No side files beyond the declared selected tree were needed. Recompiling the sealed TeX source independently succeeds with five pages and identical extracted text. Recompiled PDF binary differs, consistently with the README’s explicit no-byte-reproduction promise for compilation timestamps. All five sealed PDF pages were visually inspected: clean equations, glyphs, margins, page numbers, title/ORCID and references; no clipping/overlap/placeholders found.

The upload kit has exactly the declared four members. Its PDF and supporting ZIP are exact sealed bytes. Metadata is byte-identical in kit and supplement, and semantically identical in both deposit descriptions; only intended kit filename paths differ. ORCID0009-0001-9320-500X, author identity, title, version1.0.0, date2026-10-12, preprint type and CC BY4.0 agree. AI-use and unrefereed/no-human-peer-review/no-proof-assistant disclosures are conspicuous in note, README and metadata. Recursive payload review/scanning found authored proof/review/diagnostic/provenance material, no third-party PDFs/raw source extracts, credentials, private coordination records or other-project payloads. Local diagnostic path strings are bounded reproducibility provenance, not private communications.

## Actionable issues and exact remaining gaps

Required corrections: **none**. Severity list: empty.

Remaining limitations are correctly scoped, not obstacles to this package: recognized historical priority/first resolution and current worldwide openness remain unverified; no human peer review or formal assistant certification has occurred; no numerical radius/rounding certificate is claimed; remote isolated contact is outside the theorem; publication receipt is absent because this is a prepublication package. This review does not certify that every inaccessible historical text lacks a predecessor.

Completion estimate:100% of this independent sealed whole-package review.
