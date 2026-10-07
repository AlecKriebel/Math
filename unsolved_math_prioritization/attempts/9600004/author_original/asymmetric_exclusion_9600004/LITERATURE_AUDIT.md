# Statement and literature boundary audit

Checked October 6, 2026. Exact problem: 9600004 / AMR-095-0004, rank 933.

## Statement

Liggett's archived author manuscript is dated October 15, 2012 and has three PDF pages. Problem 4 is on page 2, which was both extracted and visually inspected. The starting state has occupied sites on the left and empty sites on the right. Fixing the interface between 0 and 1 is only a translation convention. The question concerns the full law at each fixed time on the infinite integer lattice. It is not a question about stationary distributions, a finite path or cycle, arbitrary deterministic initial states, or arbitrary directed graphs. The source explicitly distinguishes the reversed step, for which its claimed conclusion fails. Its general introductory irreducibility convention excludes the totally asymmetric endpoint; the local theorem here separately covers that endpoint.

The live UnsolvedMath item could not be read: the web fetch failed and a direct HTTP request returned 403. A current indexed category listing matched the ID, title, and step orientation. The fully hash-matched supplied corpus was used for the exact ID association, not as an independent proof of mathematical status.

## Relevant primary results

- Borcea, Branden and Liggett, Negative dependence and the geometry of polynomials (2009), arXiv:0707.2340v2, Section 5, especially Theorem 5.2 and Remarks 5.1-5.3. Their preservation theorem requires symmetric exclusion rates and a strongly Rayleigh initial law. Deterministic and product laws satisfy the initial-law requirement. Arbitrary negative association is not itself preserved even by symmetric exclusion. Their two-site asymmetric obstruction starts from a nondegenerate product law; it does not refute the deterministic infinite-step question. Strong Rayleigh implies negative association, but the converse and generic determinantal representations must not be assumed.
- Conroy and Sethuraman, Gumbel laws in the symmetric exclusion process (2023), author PDF, Sections 1.4 and 3.2. The negative-dependence machinery is for symmetric dynamics. The ASEP discussion treats extremal-particle asymptotics and, with the opposite drift, a limiting distribution; it is not a proof of full finite-time NA for the target step.
- Conroy, Gonzalez Casanova and Sethuraman, Point process convergence of extremes in K-symmetric exclusion, arXiv:2506.12632v1 (June 14, 2025), Sections 1.2, 2.1 and 5. The model imposes symmetric jump rates; Section 5 retains symmetry even when dropping translation invariance. Its semigroup comparison cannot be imported into p>q ASEP without an additional argument.
- Conroy and Sethuraman, Poisson statistics, vanishing correlations, and extremal particle limits for symmetric exclusion in d>1, arXiv:2501.10522v2 (February 26, 2025), Section 3.2. This is a symmetric process on higher-dimensional lattices, with strong-Rayleigh input and asymptotic Poisson/extremal conclusions. It does not supply the missing one-dimensional asymmetric preservation theorem.

The search was bounded and is not evidence of novelty or a definitive current-open-status certification. No inspected primary result settles the exact all-time problem. The unsupported broad preservation language in earlier triage must not be treated as a theorem.

## Three bounded approaches

1. Exact statement and primary-literature audit: identified the symmetric/strong-Rayleigh assumptions and the mismatch with stationary, reversed-step, or random-initial-law results.
2. Finite-window Rayleigh probes: a numerical search at selected times and fields on eight- and twelve-site reflecting chains found no counterexample in the tested central marginal. This is only an unsuccessful diagnostic; no infinite-volume or all-field claim rests on it.
3. Exact increasing-event expansion: replaced floating-point evidence with a complete 174-case rational-polynomial certificate and a uniform infinite-volume Taylor remainder. This proves the local theorem in PROOF.md.

Stopping point: a precise local partial result with the all-coordinate/all-time gap stated explicitly. Further empty computational searches would not settle that gap.

## Primary URLs

- https://web.archive.org/web/20150919235903id_/http://www.math.ucla.edu/~tml/open.pdf
- https://arxiv.org/abs/0707.2340
- https://arxiv.org/abs/2210.15550
- https://archive.math.arizona.edu/sethuram/papers/LeadingParticle_last.pdf
- https://arxiv.org/abs/2506.12632
- https://arxiv.org/abs/2501.10522

Only bibliographic and verification metadata are packaged. Source PDFs and extracted source text are excluded.
