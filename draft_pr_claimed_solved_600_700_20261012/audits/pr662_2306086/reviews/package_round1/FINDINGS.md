# Fresh whole scientific-package review, round 1

Reviewer: `/root/pr662_package_round1`. Immutable original head: e31701151c331a6eed9224fb37a75a374ea1043e. Problem2306086 / Hayman–Lingham6.86, PR662. This reviewer authored neither the candidate, paper, package helpers nor earlier review reports. Only this review directory was written.

**PASS for the narrowly scoped qualitative scientific package. Mandatory findings:0. Optional findings:0.** This accepts the stated mathematical note and its honest evidence boundaries. It does not certify historical firstness, current openness, an explicit or sharp radius, or unfinished publication/integration/tracker operations.

## Reviewed result and source match

The exact statement is that M(z)=max over normalized real-coefficient schlicht f of |(1−|z|²)f''(z)/f'(z)−2 conjugate(z)| exists, is below4 at every fixed nonreal interior point, equals4 on the real diameter, and has a positive uniform gap on each compact nonreal set. The original displayed source expression is separately zero at z=0. The paper's TeX lines33–76 state these quantifiers and exceptions accurately.

I freshly rendered and visually read the complete original normalization and target pages, Hayman–Lingham arXiv1809.07200v2 printed114 and147. The target fixes the evaluation point and asks whether reality improves the estimate; it does not explicitly demand an effective or sharp formula. The qualitative interpretation is therefore defensible. The note does not pretend to settle a stronger unspoken quantitative formulation. Its source/rho interpretation and the 2018 update's historical nature are stated in the packet.

## Mathematical attacks

The full paper was checked, with an independent reconstruction in DERIVATION.md. In particular:

- TeX88–110: the odd exterior square-root map has a normalized logarithm, is genuinely single valued and injective, and the Green-area limit is justified by finite partial sums. Saturation forces the complete coefficient equality case, not just a suggestive extremal shape.
- TeX113–147: equality for a Koebe transform gives an affine ray-complement image of the original function. The proof correctly avoids identifying the original map prematurely. Real symmetry fixes both the ray endpoint and its direction; inverse composition and conformal-radius normalization then force the two real Koebe maps. Their strict nonreal norm deficit is exact.
- TeX149–172: growth is deduced from the already established universal bound. Montel, derivative normalization, and zero-free divided differences/Hurwitz show compactness of the actual normalized injective class. Nonzero limiting derivatives and moving-point derivative convergence justify joint continuity. Thus strictness passes to an attained maximum uniformly over functions, and over compact nonreal sets. There is no circular strict-bound assumption or quantifier swap.
- TeX189–220: the real-transform inverse and covariance phase are correct; δ is invariant and in[0,1/2). The explicit orbit parameter lies inside the real disk diameter, sends the point to ±it, and the inverse δ/t relation selects0≤t<1. The second lower-bound example is univalent, and real transforms transport it to every orbit. Both global-gap limiting obstructions are valid.
- TeX223–228: the crossing, i/2 exact values, and distinction between δ→0 and merely Im z→0 near±1 are correct. The real-axis endpoint pair rules out a smaller containing disk even after recentering. Affine normalization with negative real derivative is harmless.

My 18 new exact controls pass with identical ordinary/optimized output. These include a distinct complex inverse-transform equality example and a stronger test of the entire Koepf extreme family. For F_u=z/(1−2uz+z²), −1≤u≤1, at i/2:

    |A_Fu|²=16(289u²+36)/[25(16u²+9)]≤208/25,

whereas the admissible h=z/(1−z²) has |A_h|²=256/25. Thus naive evaluation of this nonlinear quotient on the whole linear extreme family fails. This is supporting analysis, not a requested paper addition or a universal impossibility statement about further uses of Koepf.

Two initial comparisons in this review's own new harness needed symbolic simplification/cancellation before equality comparison. The corrected harness passes; these were check-design issues and did not indicate a target defect.

## Priority and attribution

I read the complete Koepf1986 source text and visually inspected original printed578; independently inspected the complete recovered Rodemich1979 A68, including a fresh rendering from the full scan; and read Jenkins's own1962 complete p7 and bibliography. The original statement, normalization and functional distinctions in the note match those sources.

The Rodemich addendum's countermodel satisfies the argument envelope with local normalization but violates the universal schlicht pre-Schwarzian bound by an exact81/5 squared lower margin. It is not globally univalent, so it does not refute the note. The paper's TeX238–249 accurately distinguishes the tested shortcut from deductions that might use global univalence. The full continuum proof and its elementary interval margins were checked, rather than interpreting nine rational controls as a proof over a continuum.

Jenkins1960 remains a genuine original-source gap: his own survey explicitly refers to derivative bounds, so a point-value-only dismissal would be wrong. Aleksandrov–Popova1973 exact solved cases remain another original-source gap. The prior independent families' reports and controlling current-status document retain these gaps. Four additional targeted searches in this fresh review produced no verified exact earlier implication; secondary summaries were not used as theorem evidence. This outcome cannot establish absence of earlier work.

The note's title, abstract, TeX230–249, README, current-status document, machine-readable scope and deposit metadata consistently frame a qualitative application of classical methods and explicitly decline historical firstness, new-general-method, exhaustive-novelty and current-openness guarantees. There is no verified precise positive prior implication being waived. These accurate limitations support acceptance of this scoped preprint, while preventing an unqualified claim of the first new resolution of a currently open problem.

## PDF, metadata and disclosures

All five PDF pages were independently rendered to this review's ignored tmp and visually inspected. Equations, margins, references and page numbers are readable; the main theorem is intact on page2 and the related-work paragraph is intact on page5. No clipping, overlap, missing glyph, placeholder or broken citation was found. The split between sections is acceptable for a concise mathematical note. The PDF and TeX match the root paper-QA pins.

The title, author, ORCID, date, scope, file list, preprint type, open-access/CCBY4 metadata and references are consistent. The paper and metadata explicitly disclose extensive AI use and unrefereed status. Internal AI reviews are explicitly distinguished from human peer review. There is no claim that numerical evidence is a formal proof or a human-review endorsement.

## Archive and reproducibility

The exact 307142-byte ZIP has SHA256945c5e52a136bd0187d51661140b617965c064c880628bdbeff3324516b9bc04. Its 101 sorted members have regular-file0644 Unix modes and fixed timestamps, with no duplicate or unsafe path. Every member was independently preflighted before extraction. Its manifest has100 payload files and correctly includes both helpers and all24 original native files with the controlling scope note. The two inner authored archives have exact inventories; no raw third-party source PDF, image, temporary environment, operational credential or later review report is present. A bounded credential-pattern check found no suspect file. Checksums establish this packet's integrity and provenance; they are not a signature against replacing the entire packet/verifier.

All24 native files were independently read from the actual immutable Git blobs and matched the local snapshot's byte counts, SHA256 values, Git blob identities and recorded modes. The package preserves their original historical labels with the controlling clarification attached.

I read both helper sources and the actual replay scripts before execution. The embedded verifier was run from the extracted package, with pinned Python3.12.14, SymPy1.14.0, mpmath1.3.0, NumPy2.2.6 and SciPy1.15.3. All computation used temporary copies and retained the supplied interpreter path. The full replay passed3558 candidate exact controls per ordinary/optimized mode,32 supplied symbolic controls,48 supplied preservation/binding checks,24 native negative controls,87 separately authored algebra/binding checks per mode, seven geometric checks and nine Rodemich exact margins per mode. Normal/optimized agreement passed where promised.

Optional numerical replay passed all four saved evaluations via supplied RK45 and separately authored alternative-state DOP853. The largest alternative-state discrepancy is1.3322676295501878e−14. These are floating-point reproductions, remain uncertified, and neither optimization nor interval certification ran. They play no role in the written proof.

My own28 outer-package hostile controls all failed closed: changed or rehashed PDF/native/gates, omitted proof, rehashed unlisted extra file, duplicate JSON keys/manifest entries, unsafe paths, file/directory symlinks, empty directories, boolean/integer substitution, NaN, manifest-count/size type violations, and inflated explicit-gap/sharp-radius/firstness/numerical/human-review claims. An isolated reconstruction of the documented audit layout and fresh builder execution produced the exact original ZIP SHA256. The publication originals were not overwritten.

## Disposition and remaining limits

No mandatory or optional repair is requested for the frozen scientific package. The explicit/sharp radius, general extremizers, full variability region, numerical interval enclosures, historical priority and current-openness certification remain unproved, exactly as disclosed. The Jenkins1960 and Aleksandrov–Popova1973 original-source limits remain open audit leads, not hidden defects or disproved overlaps. Future inspection could change priority conclusions; no outreach was prepared or initiated.

All114 reviewed publication, archive, source-receipt, earlier-family and helper-author inputs remained unchanged at the final recheck. Source fulltexts and renderings remain only under ignored tmp; source hashes and original comparison arguments are safe report artifacts. This review excludes unfinished integration/tracker/Zenodo operational helpers. No merge, upload, external mutation or communication with individuals was performed. A new fresh sequential package reviewer is still required by the user's process before final promotion; this report does not bypass that loop.
