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
