# Research log: radial statistical counterexample

Completion estimates concern verification and delivery of this particular negative answer, not a probability of historical priority. All checkpoint times are UTC.

## 2026-09-23T03:34:00Z — source gate and independent checks (45%)

- Target: disprove the implication in Kurose's Problem 3(e), printed in Furuhata–Matsuzoe–Urakawa (1998), p.126, indexed as AMR-059-0011 / 6000011.
- Success criteria: all centers and admissible convex neighborhoods have integrable radial orthogonal distributions, but the dual structure fails statistical 1-conformal flatness locally. A single positive-definite three-dimensional example suffices.
- Candidate: the product of the unit round two-sphere and the real line with its product metric and Levi–Civita connection. Extension: conformal metric exp(t)h with a projective change of connection.
- Visually inspected the original pp.125–126 and Kurose (1994), p.428. The original does not exclude Levi–Civita structures; item 3(a) expressly includes them. The stated alpha=1 transformation agrees with the source.
- The first-variation identity proves integrability; an algebraic curvature obstruction gives incompatible values for A(e1). An independent adversarial proof reviewer has confirmed these deductions, with a written review pending.
- Independent families: intrinsic first variation and connection-difference calculation (main); adversarial intrinsic/projective review (proof_audit); coordinate symbolic derivation (coordinate_verifier). Priority is separately audited by priority_audit. No result is being inferred from search silence.
- The two named gradient-path files concern OWR-2040-002 and discrete Morse theory, not this question. They are excluded from this effort and left untouched.
- The live database page was inaccessible (HTTP 429); the repository's catalog snapshot records `partially_solved`. Its current annotations are not verified. The original printed problem is the controlling source.
- Existing repository changes belong to other efforts. All new research lives in this dedicated top-level directory; only deployment copies and index entries will be added under the existing GitHub Pages site.
- No external communication, release, DOI, or Zenodo deposit has been initiated.

## 2026-09-23T03:47:03Z — proof, priority, and artifact checkpoint (92%)

- Independent intrinsic proof audit and final manuscript adversarial audit both pass with no mathematical gap found. The checked PDF is four pages.
- Exact standard-library linear systems have ranks 9/10, 16/17, and 25/26 in dimensions 3, 4, and 5. Compatible flat/constant-curvature and dimension-two boundary controls pass.
- Independent coordinate derivation passes 403 checks in normal and optimized Python. An intentionally unscaled metric mutation is rejected.
- Priority audit completed 43 substantive search queries across seven primary-source families. No direct anticipation located. Known deformation mechanism is explicitly credited to Ueno's divisible-cubic-form construction. Historical priority and live database annotations remain unverified; publication wording is restricted accordingly.
- Four PDF pages visually inspected; final manuscript reviewer recorded matching source/PDF hashes. The static page was inspected in the browser, including its proof and verification sections.
- Upload kit includes readable PDF, source/verifier ZIP, checksums, copyable guide and JSON metadata. Metadata base fields pass the official legacy schema; version/language match the current documentation but are absent from that old schema. No server validation or deposit is claimed.
- Package audit corrected an over-specific provenance statement: only the manuscript and audit work, not the original supplied candidate, is attributed specifically to Codex.
- Remaining delivery work: publish the approved files on main, confirm GitHub Pages serves the intended bytes, and log the deployment. Mathematical verification complete; publication checks still in progress.

## 2026-09-23T03:51:05Z — final metadata and publication checkpoint (100% mathematical verification; 97% delivery)

- Published the paper and initial package in commit 70fbc44f6cae708bda1840de8269222ee851abdb and pushed main successfully. Later independent repository commits superseded the initial Pages build; the current build includes this work.
- Final independent package audit passes: clean extraction, normal and optimized runs of both verifiers, all manifest layers, exact archive contents, and deterministic rebuilds for fixed inputs.
- Corrected the optional CITATION.cff file after checking the official schema: top-level CFF describes the MIT verification software; preferred-citation identifies the CC BY 4.0 unpublished manuscript. The corrected file passes the official CFF 1.2.0 schema. No mathematical or PDF change.
- Final metadata and package documentation are being published in a follow-up commit. This checkpoint records the package before the remote-served-byte check; deployment confirmation is a delivery step, not a mathematical assumption.
- All requested research artifacts and the manual Zenodo kit are prepared. Remaining work at this timestamp: verify the successful Pages deployment and equality of its served download bytes. Historical priority remains unproved, as disclosed throughout.

## 2026-09-23T13:40:44Z — deeper priority audit (60% of follow-up)

- User requested a renewed attempt to inspect the live database and stronger priority evidence. An ordinary browser visit succeeded; the full research report was expanded and read. Its partial-status label refers to machine-generated research progress, with no verified proof/counterexample or named partial theorem and zero discussion comments. See DATABASE_RECHECK.md.
- The live report's description of 1-conformal flatness is incomplete: it omits the simultaneous connection change. It is not being treated as mathematical validation or authoritative evidence of current open status.
- Independent follow-up routes: forward citations through OpenAlex/Semantic Scholar/Crossref (proof_audit); older primary papers and subsequent problem lists (priority_audit); specialized-index accessibility and adversarial wording review (coordinate_verifier); Japanese workshop/grant records and database inspection (main).
- The main route located Kurose's 2016 Gauss-lemma/generalized-Hessian talk and two related grant reports. No explicit negative answer appears in the inspected reports; the program links no notes for that talk. This is a specific remaining historical gap.
- Publication plan: add a dated priority addendum and correct the live website's access statement. Preserve the original paper and version 1.0.0 download archives as historical snapshots; no mathematical revision, new version claim, release, DOI, or deposit is required by these findings.

## 2026-09-23T13:46:06Z — deeper priority findings complete (100% audit; 95% delivery)

- All four bounded follow-up routes are complete. No explicit earlier answer was found. The synthesis distinguishes 175 raw citation records screened by title from nine complete PDFs screened for relevant passages; Google Scholar independently supplied eight visible FMU citing records and bounded subsets of Kurose citations. No zbMATH record was inspected because access failed.
- Prior radial-gradient results were located in Henmi–Kobayashi (2000), Ay–Amari (2015), and Felice–Ay. These reinforce attribution of the main lemma as established background, not a new general theorem.
- Older-source work read four further primary texts, including the 2002 continuation and 1996 precursor problem lists. Kurose 1999, Matsuzoe 1999/2010, Binder–Simon 2000, the actual 2016 talk, and Kurose's 2023/2024 full article remain specific unresolved leads. Their absence from the inspected results is not clearance of their contents.
- The specialized-index reviewer adversarially checked the synthesis and website wording and found no material overclaim. The supported historical statement remains only that no earlier explicit answer was found in the documented search.
- Preserved a public 175-record citation inventory and nine-paper screening manifest, without redistributing third-party PDFs. Added a database recheck and four route reports. Updated the webpage and README to link the addendum; the manuscript and original archives are unchanged.
- Remaining delivery step: verify the additive files and current manifests, commit/push only this effort's changes, and check the live webpage. No external person was contacted and no release or DOI was created.
