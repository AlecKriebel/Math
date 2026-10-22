# Independent reader-preservation and dependency acceptance

Date: 14 October 2026.

## Verdict and exact scope

**QUALIFIED ACCEPTANCE of the frozen reading edition identified below.** The original full fixed-exponent classification remains **UNSOLVED**; novelty and priority remain **unestablished**. This report accepts preservation, exposition scope, dependency inclusion, navigation, and release-content boundaries. It is not another mathematical research pass, a new proof audit, or a publication claim.

The reviewer inspected the original-to-reader changes for all 45 proof chapters, checked every selected source against an accepted pin and its current original bytes, read the main manuscript against the relevant accepted theorem statements, checked the local links and complete package inventory, and inspected the allowed-content boundary. The 15 original computational dependencies were compared byte-for-byte. Certificate re-execution and primary-source citation checking are separately reported.

The reviewed package contains 72 files and 771030 bytes. Its exact paths, sizes, and hashes are in `FROZEN_READER_INVENTORY.json`; the canonical file-record digest is `dd3f5ef95f0934b89420a34f3abad0768537bf9d593099107f886e40e6da4016`. The inventory file itself has SHA-256 `b95e7b56b1ce8de2683d25ab036e97193846f6b4dae805362c3220fda3e26949`. `PRESERVATION_CHECKS.json` records all 60 original/reader bindings and the local navigation checks.

The editor’s `FILE_MANIFEST.json` has SHA-256 `5663aa4e767bd0810b8d013f1c44acb070a8eb729996bcb9212dad917c37d288` (11,924 bytes). Its 70 entries and all 71 entries in `SHA256SUMS` were independently checked. `REVIEW_CANDIDATE.tar.gz` has SHA-256 `dc1b057abef6ad99e3030c6411a47287f2f8699b0af2c5b4e8591f4554d712cf` (269,012 bytes); its 72 ordinary-file members exactly match the reviewed package, with no extra files, duplicates, links, or special members.

## Mathematical preservation

The presentation changes are titles, navigation, attribution, ordinary formula formatting, removal of dated or exploratory framing, and reconciliation of surrounding scope with separately accepted later theorems. No changed proof calculation, hypothesis, error estimate, analytic tail bound, or witness quantifier was found after the corrections below.

- P01 restores the positive noneven-exponent assumption explicitly before the circuit obstruction and states the real, finitely supported convention. The manuscript applies that convention to arbitrary frequency sets and does not define unexamined infinite Fourier sums. Its coefficient-box convexity argument is restricted to the appropriate exponent range.
- P29 preserves the complete bounded-mass theorem, both parity cases, maximal-mass necessary patterns, two-scale coefficient and multinomial factor, eventual negative tail, and order of choosing the fixed coefficient before the small parameter. Its finite rational-affine grid remains a necessary candidate reduction, with no sufficient criterion or exact universal decision procedure asserted. The fresh independent acceptance of its original has SHA-256 `84f700cbf5014aeed1503f5a3cef655b94769a4f6895514b6715f4e58a21123c`.
- The low-exponent block and join statements retain their necessary ranges and radial-noise robustness. The mixed unequal centered-cross gap on `2<p<3` is not declared closed. Strong-center Green-cone results remain sufficient restrictions on prescribed coefficients.
- P30 and P31 exclude the stated supports for each fixed exponent and allow the witness coefficients to depend on that exponent. The separate P19, P20, P32 and P33 uniform-witness assertions retain their stronger, different quantifiers. The enormous explicit threshold in P33 is not presented as a remaining support-classification cutoff.
- P26 and P34 use only the corrected cubic sources. The former retains its corrected `17/20` estimate; the latter retains the missing-factor correction, `1/6` estimate, finite rational calculation, and analytic infinite tail. Rejected cubic drafts and their rejected computational outputs are not selected or included.
- Dominant cones, symmetric slices and explicit neighborhoods on the cubic and K5 supports remain partial coefficient-box conclusions. P39 remains the double-flip comparison only, not an unrestricted quartet box theorem.
- P05, P16, P28, P41 and P45 distinguish failures of stronger auxiliary approaches from actual target counterexamples. In particular the compression example retains its positive actual entropy gap, and P45 explicitly states that its convex-order obstruction does not settle the cubic power comparison.

## Dependencies and source lineage

All 45 selected proofs and all 15 unchanged certificate artifacts are present. Their source hashes resolve to accepted original artifacts, including the inherited circuit and structure acceptances and the closed second through fifth pass manifests. The final source-audit pin is SHA-256 `f261e2ae1b3f0f623710c7d7112d3419a066aca668a41a56eb6a198cd0360fa6`.

The substantial authored prerequisites are included as linked chapters. Omission of the weaker diagonal-support theorem and the shorter all-odd version does not remove a required argument: the stronger full-cone proof and the accepted expanded all-odd proof are included. Standard background and the externally invoked affine-independent sufficient theorem are identified in References. Related-result navigation is not being treated as proof of a circular dependency.

The additional portable replay checker has SHA-256 `40778d137c46771a985a63987043e106cea4574a0f7e71e8c1524eed346588b9`. It is clearly separated from the 15 accepted source artifacts. It checks pins, uses scratch copies, converts source assertions into explicit in-memory gates, rejects stale outputs, and compares exact output payloads while excluding only timing fields. Its role is reproducibility, not a new mathematical argument. The trusted mpmath interval-primitive dependency remains disclosed; no formal verification of that library is claimed. Ordinary direct execution of the original assertion-bearing programs, not optimized execution, remains their documented validation mode.

The separate reproducibility report has SHA-256 `79da76263f93d0a94eb354bf6ebf9415ef3b50e1b6b67b6f9842dead43513c6c`; it records eight successful jobs and optimization-safe checks. The separate citation review has SHA-256 `db347eb4e44814958e16429ecee770197a881377f614e835190eb64d9db48d65`; it records the corrected Baernstein–Culverhouse locator, version/quantifier boundaries, and source-access limits. This reviewer read both reports and verified those hashes but does not represent their independent executions or primary-source retrievals as its own.

## Editorial corrections and navigation

The following corrections were requested during this review and verified in the frozen copy: the malformed P32 shell command was replaced with an executable command and working-directory instruction; P01's opening scope was restored; P45's explicit auxiliary-obstruction warning was restored; unprotected operator-bracket formulas were formatted to avoid accidental Markdown links; and reader hashes were refreshed after the changes.

All 414 intended package-relative Markdown links resolve to included files without escaping the package. Mathematical expressions protected as code or display math were not treated as navigation links. The machine-readable source selection and the human-readable source/reader bindings match the frozen files.

## Public-content boundary

The frozen package contains authored mathematical exposition, authored computational certificates and their outputs, editorial/dependency metadata, public scholarly citations, and hashes. Inspection found no copied third-party source documents, problem datasets, private sources, personal data, conversation links, external message bodies, private coordination material, optimizer logs, or rejected proof drafts. The bibliography links to external primary sources rather than bundling their texts. The exact file inventory, not a broad workspace-directory upload, defines this verdict's release scope.

## Qualifications and change control

This is a preservation-and-presentation acceptance grounded in the existing mathematical acceptances. It does not claim a typeset or PDF rendering review. It does not independently re-prove all 45 chapters, establish priority, resolve the remaining classification, or authorize a new mathematical claim. The interval-library trust and all recorded unresolved mathematical scopes remain. Citation verification and fresh certificate replay retain their own separately stated scopes.

The package's conservative review-candidate status is compatible with this external acceptance report. Any later content change requires checking its diff and refreshing the exact file binding. No original accepted proof or certificate was edited by this reviewer.
