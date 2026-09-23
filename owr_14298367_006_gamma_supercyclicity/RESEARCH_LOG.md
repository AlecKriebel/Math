# Research log: OWR-14298367-006

Goal: verify the supplied arbitrary-Gamma supercyclicity equivalence against the original problem, audit priority, and only if warranted publish a concise proof and reproducibility package.

## 2026-09-23T04:04:28Z — Initial verification checkpoint (35%)

- Working on `main` in a dedicated top-level folder. Pre-existing unrelated changes are excluded from this effort.
- The index page is unavailable (HTTP 429); recovered the official Oberwolfach Report 19/2024, DOI 10.4171/OWR/2024/19. Exact question is on printed p.1083.
- Target: for every fixed subset Gamma of the complex field, existence of a dense Gamma-scaled forward orbit is equivalent for the composition operator and its associated scalar weighted bilateral shift. This is not a claim that all such operators are supercyclic.
- Standing assumptions: 1 <= p < infinity, separable complex Lp space, bijective bimeasurable nonsingular map with bounded invertible composition operator, a finite positive-measure wandering generator, and uniform bounded distortion.
- Independent approach families: (1) adversarial audit of the supplied tail estimates and constructive proof; (2) primary-source matching and measure-theoretic conjugacy audit; (3) alternative Baire-category amplification argument. All three are in progress with distinct owned audit files.
- Preliminary direct check finds no gap in the scalar tail estimates or constructive amplification. Separability must be explicitly retained; sigma-finiteness alone does not imply it.
- Early literature triage finds that the scalar arbitrary-Gamma tail criterion predates this candidate. Its status as a claimed new by-product requires correction. A dedicated priority audit is now in progress; no novelty decision yet.
- Success criteria: checkable proof under the actual hypotheses; independent adversarial agreement; correct attribution and no located prior resolution; verified final artifacts. Computational checks, if included, will check finite identities and examples rather than purport to prove an infinite-dimensional theorem.
- No external individuals have been contacted and no outreach will be prepared.

## 2026-09-23T04:08:18Z — Verification and priority checkpoint (85%)

- All three initial independent approaches pass in the source's separable setting. Both the original construction and a shorter Baire-category proof are checked. The source/conjugacy audit gives an explicit counterexample if separability is dropped.
- Decisive priority finding: Abbar (2019) explicitly provides the scalar criterion and a general Gamma-supercyclicity criterion. Abbar–Kuznetsova (2020 preprint, 2021 journal article), Theorem B, also implies the entire amplification statement through Z, Z², and a bounded dense-range coefficient map.
- A separate source reviewer independently verified this prior-theorem deduction. It does not depend on the candidate's tail proof or amplification lemma, so there is no circular priority argument.
- Distinguish two claims: the full mathematical equivalence is verified; an explicit previously published answer to this particular Oberwolfach question has not been located. A new scalar criterion or new amplification theorem cannot responsibly be claimed here.
- User was informed of the overlap and offered an optional choice between audit-only delivery and an attributed explanatory package. In the absence of changed scope, the user's original clean-priority condition governs: no original-resolution paper/site/Zenodo package.
- Initial checkpoint committed and pushed as `aad71a7df`.

## 2026-09-23T04:11:29Z — Final audit checkpoint (100% of verification and priority decision)

- Exact original question on printed p.1083 visually inspected from the official PDF; source hashes and primary locators recorded.
- Final adversarial review rechecked both the prior theorem's hypotheses and the Z²/dense-range deduction. No material mathematical or reporting correction remains.
- All four exact-arithmetic check groups pass. They check finite identities and examples, not the infinite-dimensional theorem. Output is preserved in `verification/results.json`.
- Final status: proof PASS in the original setting; originality gate NOT CLEAR; conditional original-resolution publication does not proceed. The complete audit, analytic proof, source records, and verifier are the deliverable. An attributed application note would be a separate publication scope.
- Remaining gap is bibliographic/editorial, not a gap in the verified equivalence: who first explicitly observed the application to this 2024 question is not established. A claim of new criterion/amplification is blocked by the concrete older results; further keyword searching alone cannot remove that overlap.
- No GitHub release or Zenodo deposition is created, and no person is contacted.

## 2026-09-23T13:58:09Z — Attributed-note publication checkpoint (90%)

- The user explicitly authorized a concise attributed note, commitment to the repository, website publication, and a manual Zenodo upload package after the critical discussion of novelty. This supersedes the earlier audit-only deliverable; it does not establish new priority for the scalar criterion or amplification mechanism.
- Prepared a five-page note with a direct finite-tail/Baire proof, the composition conjugacy, a separability caveat, and an explicit deduction from Abbar–Kuznetsova. Attribution includes Abbar (2019), Abbar–Kuznetsova (2020/2021), Charpentier–Ernst–Menet, D'Aniello–Darji–Maiuriello, D'Aniello–Maiuriello, and the original Oberwolfach report.
- Independent adversarial manuscript and attribution reviews passed. Two optional precision edits specify the fair Bernoulli product and justify the large-time requirement in the prior-theorem deduction. Final source review is being bound to the resulting manuscript hash.
- Compiled all five pages and visually inspected the final PDF. The compact source archive contains no third-party full texts; the standalone note requires no supplemental proof or computational premise.
- Created the source archive, manual Zenodo kit with complete metadata and copy-and-paste fields, a dedicated website page, and download checksums. No Zenodo deposition, DOI, or GitHub release has been created.
- Remaining work: independent package QA, archive compilation replay, homepage integration, commit/push, and live deployment verification. Estimate: 90% of the newly authorized publication task; mathematical verification remains complete within the stated scope.

## 2026-09-23T14:01:18Z — Publication readiness checkpoint (95%)

- Final mathematical approval is bound to TeX SHA-256 `5950e74b23cb2be12626cb0c8d266cf3e3d6040c0dcfe8908a1fb49741796c94`. All five final PDF pages pass visual review.
- Compiling the extracted source archive reproduced the release PDF byte for byte (SHA-256 `cbc84a37bc7735675d833236c68c8194c99389b1398b21175f43998b9926e171`). The note's proof requires no code execution.
- Independent package QA caught an invalid top-level article type in the optional Citation File Format metadata. Replaced that file with a preprint BibTeX citation, regenerated both archives and all website copies, and rechecked archive integrity and member equality. The source and PDF are unchanged.
- The dedicated page is linked from the website homepage and sitemap. Only this effort's files and these scoped site additions will be committed. Unrelated working-tree changes remain untouched.
- Publication task is 95% complete: local materials are ready; final package sign-off and remote deployment verification remain. No Zenodo deposition or GitHub release is authorized by this manual-package step or has been created.

## 2026-09-23T14:08:53Z — Publication completed (100%)

- Committed the attributed note, source, audits, website, and manual Zenodo package as `47ab4e2c05be7e2c56f6083eea07765292f52e2b` and pushed to `main`. Final independent package QA passes; its citation-format finding was corrected before publication.
- GitHub Pages run `35871476450` completed successfully. The public paper page, CSS, PDF, source ZIP, Zenodo upload kit, and checksum file all return HTTP 200 and match the reviewed local bytes. The homepage link and sitemap entry are present. Evidence is recorded in `audit/live-deployment.json`.
- Website: https://aleckriebel.github.io/Math/papers/gamma-supercyclicity/ . All original research materials are retained in this dedicated top-level effort folder; the compact upload kit includes the five-page note and source rather than the longer internal audit history.
- Refreshed and verified the effort-wide SHA-256 manifest after final documentation and audit changes. A final evidence-only commit preserves this publication checkpoint; it does not change the website or deposit files.
- Authorized publication task is 100% complete. The priority assessment remains limited: this is an explicit attributed application of earlier results, not a new scalar criterion or amplification mechanism. Journal suitability and priority for the explicit application remain editorial/bibliographic questions.
- No person was contacted. No GitHub release, Zenodo deposition, reserved DOI, or registered DOI was created. The human user can upload the provided kit's PDF and source using its metadata and instructions.

## 2026-09-23T14:58:01Z — Fresh adversarial preprint-review cycle (10%)

- The user requested fresh sequential adversarial subagent reviews, with worthwhile findings addressed throughout the paper and distribution materials before each new review. Scope is mathematical soundness and preprint readiness; no journal submission work is requested.
- A new reviewer begins from the actual manuscript and PDF without relying on earlier audit conclusions. Its remit includes the full proof, boundary cases, original hypotheses, primary-source attribution, and material package consistency.
- Parent baseline checks verified all 50 manifest entries and both archive CRCs. Reviewed baseline: TeX SHA-256 `5950e74b23cb2be12626cb0c8d266cf3e3d6040c0dcfe8908a1fb49741796c94`; PDF SHA-256 `cbc84a37bc7735675d833236c68c8194c99389b1398b21175f43998b9926e171`.
- Success criterion: resolve all substantiated mathematical or preprint-material issues; use a new independent reviewer on the resulting artifacts; repeat if further actionable findings remain. At least two fresh review rounds will be recorded. A clean internal review is not a guarantee of journal acceptance or a formal proof certificate.
- Completion estimate: 10% of this additional review cycle. Existing mathematical and publication conclusions remain hypotheses to challenge, not premises of the new review. Work remains on `main`; unrelated changes will not be included.

## 2026-09-23T15:04:21Z — Round 1 resolved; fresh round 2 started (60%)

- Fresh adversary `preprint_adversary_r1` found no blocking mathematical issue or material distribution inconsistency. Its report, `audit/preprint-adversary-r1.md`, independently checks the original and prior sources and records one worthwhile clarification: the conversion from Abbar's single-offset criterion to finite blocks uses boundedness of the shift.
- Accepted R1-1: the note now states the choice of offset `q` and the explicit bound `c_(j±n)^(1/p) <= ||S||^(q-j) c_(q±n)^(1/p)`. The parent also replaced the potentially ambiguous word "integrable" by explicit membership in `L^p(X,mu)` in the gluing argument. The theorem and hypotheses are unchanged.
- Rebuilt version 1.0.1 globally: manuscript/PDF, source README and citation, website version, source ZIP, manual Zenodo instructions and metadata, upload kit, and Pages copies. Historical audit records retain their original version bindings.
- Final TeX hash for this revision: `3b16fbb6a78491f117dd2d50345c1863dad7b6486863a403ecccf74d6b4a9794`; PDF: `671cf6be89c45cbda49c207c2a656064958494fce60f05619d63a3061ee123c7`. All five newly rendered pages pass parent visual inspection. Compiling the newly extracted source archive reproduces that PDF byte for byte.
- A genuinely new adversarial subagent, `preprint_adversary_r2`, is reviewing these revised artifacts from a counterexample-driven route without using earlier review conclusions. Its report will determine whether another revision/review round is necessary.
- Additional review cycle is 60% complete. Remaining work is the fresh second verdict, any required corrections, final consistency checks, and publication of the reviewed revision. No journal submission, DOI creation, external outreach, or GitHub release is part of this task.

## 2026-09-23T15:09:54Z — Fresh round 2 clean; revision approved (95%)

- The new second adversary completed an independent counterexample-driven review without reading earlier review conclusions. Its verdict on version 1.0.1 is "No actionable findings" at blocking, worthwhile, and cosmetic grades. The complete evidence is in `audit/preprint-adversary-r2.md`.
- Both written proof routes, the exact primary-source hypotheses, the new single-offset explanation, empty/zero/pathological scalar sets, the endpoint p=1, bounded translations with unbounded inverses, infinite-dimensional coefficient spaces, measurable gluing, and the separability counterexample passed. All five pages and 35 artifact-consistency checks also passed.
- All substantiated first-round and parent findings are addressed. No new mathematical or preprint-material issue remains to fix, so no further review round is triggered. `audit/preprint-revision-response.md` records decisions and the exact four principal artifact hashes.
- Additional review task is 95% complete: the paper is ready as an attributed, unrefereed preprint; commit/push and live verification of the revised downloads remain. The remaining publication work does not alter the reviewed manuscript. No journal-submission work was done.
