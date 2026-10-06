# Height counts for closed projective immersions: audited partial results

Problem 30002439 / OWR-12725-016, rank 842. Canonical status: **unsolved, 4/5 approaches**. Accepted only as partial results; no full resolution, novelty, best-known bound, or comprehensive literature-status certification.

Read [the proof](author/PROOF.md), [the independent audit](audit/INDEPENDENT_AUDIT.md), and [acceptance](audit/ACCEPTANCE.json). No correction was required. All original author and audit archives, manifests, bootstraps, receipts, and extracted members are unchanged. Statements that publication or audit had not yet occurred remain historical snapshots.

The coefficient-uniform coordinate-subset reduction gives m <= binomial(n+d,d)-1 and never increases primitive projective height. Known linear and curve cases, the Veronese benchmark, and the shear obstruction are distinguished. For surfaces the accepted exponents are 7/(2d)+epsilon and, at d=2, 43/28+epsilon, leaving fixed gaps from the conjectured 3/d. The shear disproves only a uniform pointwise height comparison, not the counting conjecture. The degree of the forms is d; the image degree is d^n. The degree-four conic-family exception retains its uniform constant.

## Authenticated replay

Obtain the SHA-256 of publication_bootstrap.py and PUBLICATION_MANIFEST.json from the draft PR acceptance record. In a trusted Python -I -S -B process, independently hash-check the bootstrap before compiling its already checked bytes. Pass this package root and the trusted manifest hash, optionally followed by --replay. The bootstrap validates strict inventory, all package bytes, immutable input pins, both ZIP inventories and every extracted member before any packet code executes. Normal and optimized Python are supported. publication_controls.py tests the outer boundary after authentication.

The replay executes the unchanged author and independent diagnostic bootstraps, the 65 author integrity controls, and 79 audit integrity controls. Outer processes use -I -S -B; the unchanged historical harnesses launch their child controls with their documented -I -S flags. Replay results are finite corroboration, not proofs of the cited deep theorems. External pins and a trusted interpreter/OS are assumed; no concurrent hostile filesystem replacement is modeled.

## Source and distribution boundary

Only authored mathematics, code, audits, and public verification metadata are included. Third-party PDFs, source excerpts, screenshots, dataset records, credentials, and private coordination are excluded. Historical and fresh Salberger PDFs have different hashes because of a timestamped cover; the audit verified identical extracted article text and printed p.1095 pixels, not entire-PDF byte equality. Public source identities and retrieval history remain separate in audit/PUBLIC_SOURCE_AUDIT.json.

No release, DOI, merge, deployment, or external outreach is part of this draft publication. Zero GitHub CI contexts or runs must not be described as a passing CI suite.
