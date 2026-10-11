# Simultaneous-core size moments: normalization and prior-result reconciliation

Target: 20003198 / AIM-OTHER-0005, the 2015 AIM request for higher raw size sums over all simultaneous (a,b)-core partitions with positive coprime moduli.

Verdict: PRIOR_RESULT_RECONCILIATION_ACCEPTED_NO_NEW_SOLUTION.

The accepted findings are source-level normalization corrections, correct conversions between raw sums and normalized moments, a reconstruction of prior polynomiality mechanisms, and an accurate account of the published theorem-status updates. This edition does not present a new compact arbitrary-order formula or accept a new resolution of the full open-ended AIM problem.

This is an AI-assisted, unrefereed authored mathematical audit and correction edition. Acceptance records an internal AI audit of prior-result status, normalization and written deductions. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored mathematical audit, every written formula and example, the full correction patch and all substantive acceptance qualifications are retained. Executable code, raw partition or moment datasets, copied source PDFs or text, source renderings, raw search responses and private coordination material are not distributed. Historical finite checks cannot be reproduced from this edition alone.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution.

## Main findings

- The original AIM mean visibly prints a+b−1. The correct factor is a+b+1; this is a source typo rather than merely OCR loss.
- The inspected full arXiv Thiel–Williams Theorem 1.6 omits 1/N on physical pages 2 and 25. The official FPSAC version includes it. For (3,5), the central cubic sum is 90, whereas the normalized third moment is 90/7.
- Ekhad–Zeilberger's September 1, 2015 update states that all its theorems are rigorously proved, superseding older conjectural wording inside the same paper. General formulas through order six and consecutive-modulus formulas through order nine are credited as prior work. Independent all-coefficient recertification is not claimed.
- Normalized moments have bivariate polynomial extensions of degree at most 2i in each variable, and at most 4i total. The raw sums retain the rational-Catalan factor N and are not themselves bounded-degree bivariate polynomials.
- The complete audit explicitly derives the type-A quadratic and falling-factorial average, handles the parameter-dependent weight and the coprime-domain interpolation step, and distinguishes central moments from cumulants.
- The modulus-two Bernoulli formula is an elementary special case. It does not solve the all-coprime-moduli target and carries no novelty claim.

## Reading order

1. PROOF.md contains the complete authored mathematical audit once, including all seven sections and references, the exact (3,5) witness, every written raw/central/cumulant conversion, the complete type-A and falling-factorial polynomiality derivation, coprime bivariate interpolation, and the modulus-two calculation.
2. AUDIT.md contains the complete standalone authored correction patch, preserving its replacement wording and mathematical qualifications.
3. ACCEPTANCE.md preserves the complete substantive acceptance report. ACCEPTANCE.json binds the three authored reports and makes the accepted and excluded claims machine-readable.
4. SOURCES.json preserves historical public-source identities, retrieval and page-level inspection scope. The full 2017 journal text was not inspected; its abstract and bibliographic metadata were checked. The later limit-law status update concerns a distinct problem and is not a proof audit.
5. VERIFICATION.json preserves historical supporting-check metadata and receipt identities without distributing raw rows. MANIFEST.json lists exactly eight members and hashes the other seven; its own digest is independently pinned in the publication description.

The historical checker covered 32 coprime pairs and 9,246 directly hook-checked partitions, including 21 size-distribution comparisons against the coweight quadratic. Finite tests and integrity hashes do not establish universal mathematical truth. The exact witness and written algebraic derivations stand separately.

## Principal sources

AIM, *Problems for 2015 AIM Workshop on Dynamical Algebraic Combinatorics*, Problem 2.2: https://aimath.org/pastworkshops/dac_preworkshop.pdf .

Paul Johnson, *Lattice points and simultaneous core partitions*: https://arxiv.org/abs/1502.07934v2 .

Marko Thiel and Nathan Williams, *Strange Expectations*: https://arxiv.org/abs/1508.05293v1 ; official FPSAC version: https://fpsac2016.sciencesconf.org/file/final_102.pdf .

Shalosh B. Ekhad and Doron Zeilberger, *Explicit Expressions for the Variance and Higher Moments of the Size of a Simultaneous Core Partition and its Limiting Distribution*: https://arxiv.org/abs/1508.07637v2 .
