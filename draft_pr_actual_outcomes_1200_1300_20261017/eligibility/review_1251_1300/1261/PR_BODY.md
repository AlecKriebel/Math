## Scoped result

For each fixed compact convex body K in R^n with nonempty interior and each fixed real polynomial f, the normalized n-dimensional Lebesgue hierarchy

    H_r = inf { integral_K f q dx : q is a global sum of squares,
                degree(q) <= 2r, integral_K q dx = 1 }

satisfies 0 <= H_r - min_K f <= C_{K,f}/r^2 for every integer r >= 1. The explicit witness is one global square. The proof uses a quadratic Taylor upper estimator, homothetic sublevel-volume growth, a fixed even power of an endpoint polynomial kernel, and a dyadic tail estimate relative to the normalizing core mass.

The accepted exact moment supplement treats the nonsimple apex of a square pyramid through rational moments and a full SOS generalized-eigenvalue formulation. A numerical SDP is not used as a certificate for the general theorem.

This is an upper-rate claim for the normalized Lebesgue global-SOS hierarchy. It does not cover arbitrary reference measures or generally prove the same rate for densities restricted to s(f(x)); it is not a two-sided rate for every objective, nor an efficient algorithm for finding the minimizer. The original Oberwolfach display has an incomplete integral constraint; this result explicitly imposes unit mass, consistent with the full probability-density papers.

## Review, attribution and literature limits

The final proof and supplement received independent AI mathematical acceptance. This is not a machine-checked formal proof, conventional human peer review, journal acceptance, or certification of novelty, priority or current-open status. No first-solution claim is made.

Slot and Laurent already use the quadratic upper-estimator reduction, and polynomial concentration kernels are classical. Their inspected Theorem 11 gives O(log^2(r)/r^2) for general convex bodies with Lebesgue measure, and the final 2026 Laurent–Slot overview still lists that rate. These source statements identify the source-matched improvement, without establishing historical priority.

- [Original Oberwolfach report, contribution OWR-16633-006](https://ems.press/journals/owr/articles/16633)
- [Slot–Laurent, Improved convergence analysis of Lasserre's measure-based upper bounds for polynomial minimization on compact sets](https://arxiv.org/abs/1905.08142)
- [Laurent–Slot, An Overview of Convergence Rates for Sum of Squares Hierarchies in Polynomial Optimization, final 2026 chapter](https://ir.cwi.nl/pub/36052/36052.pdf)

SOURCE_VERIFICATION.json records public source titles, URLs, versions, PDF hashes and byte counts, and the specific inspected passages. Whole-PDF retrieval is not full reading. The literature search was bounded, source proofs were not exhaustively audited, and no source-author code was executed.

## Publication and verification boundary

This draft adds exactly seven authored mathematical or public-verification files (36,411 bytes) under unsolved_math_prioritization/attempts/30003990/. All seven files retain their approved bytes. Fields such as publication_performed=false in the preserved acceptance artifact describe its pre-publication snapshot; this pull request is the separate publication event.

No copied source documents or source text, dataset contents, private sources, private personal data, private coordination material, or executable code are included. QUEUE.md, main, and existing sibling content are unchanged by this branch publication. No merge, release or external outreach is requested.

Before publication, all seven SHA-256 hashes and byte counts matched; native Git tree reconstruction verified exactly seven added regular files and no other changes. The base commit is 4b27092a448d53b61408355ce44ec38d103a1ce4, with base tree dbba6b34103d99a47776dc898331284464b8a5d5. The expected publication tree is 6c3e240317618801acfd49b3c7dfe131897757fb.

Those are local pre-upload checks. Remote readback and CI state are separate checks; an empty check suite is NOT_RUN, not PASS. No machine proof-assistant verification is claimed.

## Exact file pins

All paths below are relative to unsolved_math_prioritization/attempts/30003990/.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| ACCEPTANCE.json | 1678 | aa8d2447f40791320b2314ea15419be1f9317c807e1b5064ba6454896d43d5f8 |
| AUDIT.md | 13368 | a4d445ea2fd7423247ee6ab69b0806b483866b657954d9947964d329daf18b27 |
| MOMENT_FORMULATION.md | 3099 | b1988e13ab99ba0614d0695c67448bbf6538267ed75c271c5be48eb7c8f3cc37 |
| PROOF.md | 8867 | a49d5c37e132810d22219271cd225f9519618b1eb8ae8b63ce424e5eaa00a03a |
| PUBLIC_MANIFEST.json | 1368 | 5a6ea4735a0b419504181a9e4c408e454aae0f75f5c53da4cf649b85ba300129 |
| RESULT.md | 2924 | 15b5b9f100b71a62de98a24317eb3e2b93a7003b7fe269f96427808c03abc5da |
| SOURCE_VERIFICATION.json | 5107 | acc0a74ffb316684a54fa7c2de73e8c7f16090b2db0fbdaddc9af6b2eccbc8f7 |
