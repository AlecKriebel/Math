# Independent audit of the step ASEP certificate

Date: 2026-10-06. Problem 9600004, AMR-095-0004, rank 933.

## Decision

ACCEPT the frozen author package as a proved local partial result. No mathematical repair was required. This is independent AI-assisted mathematical and artifact review, not human peer review, formal proof verification, or a novelty certification.

The accepted theorem concerns the actual infinite nearest-neighbor exclusion system on the integers, started from occupation 1 exactly at sites x <= 0. For right rate p > 0 and left rate 0 <= q <= p, its marginal on {-1,0,1,2} is negatively associated whenever 0 <= p t <= 1/10837981440. Two nonconstant increasing functions on disjoint coordinate supports in this marginal have strictly negative covariance for positive times in that interval. Constant functions and time zero give covariance zero.

This does not solve Liggett's all-coordinate, all-time asymmetric question. The appropriate proposed queue disposition remains `unsolved`, `3/5`, with the precise local theorem in Findings. The work contains three bounded approaches; the audit is verification of those approaches, not a fourth attempt at the open problem. No GitHub changes were made in this audit.

## Frozen input and exact acceptance boundary

The reviewed author ZIP is 18,052 bytes, SHA-256 733056f2e46581e6082d1cc320273ecccad48e62efdb1063ebafdad60adf502b. Its external manifest is 2,000 bytes, SHA-256 a0d7aa3a6e4feaccdb9dde972f3d5456d860a7baf6301c683c1a9c9ec5a21b44. All eight member sizes and hashes match that manifest. The archive has no extra members. The `original` directory preserves those eight files byte for byte. Acceptance applies to that exact package, together with the review evidence in `audit`; it does not extend to unreviewed later edits.

The author certificate has 118,294 bytes and SHA-256 c583cce094b53104febffceb90b7c5e781b254de1aa19858a744680d9813e03f. The complete source/corpus/member comparison is in SOURCE_CORPUS_ARTIFACT_REPLAY.json.

## Independent mathematical recomputation

The separate implementation `independent_recompute.py` imports no author code. Its state space is the infinite step plus a finite set of flipped sites. A state is represented by that finite deviation set, rather than a bit string in a reflecting window. All active bonds are obtained from the interface and bonds touching deviations. Transition and diagonal contributions are accumulated as signed integer coefficients of powers of r = q/p; division by j! occurs only when expectations are formed.

After orders 0 through 6, the respective numbers of states with nonzero polynomial weights are 1, 2, 4, 7, 12, 19, 30. The possible deviation sites at order 6 lie in [-5,6]. This calculation independently matches every rational polynomial in every coefficient c_0 through c_6 in all 174 author cases. It also reproduces the entire leading-order histogram and the exact minimum time bound.

Increasing events are generated independently by their antichains of minimal cube elements. This gives 1, 4, and 18 nonconstant increasing Boolean functions on supports of sizes 1, 2, and 3. All unordered disjoint nonempty support pairs in the four sites are covered:

- 6 singleton/singleton cases;
- 48 singleton/two-site cases;
- 72 singleton/three-site cases;
- 48 two-site/two-site cases.

There are 174 support-labelled tests, corresponding to 78 distinct pairs after lifting the events to the full four-site cube and discarding redundant coordinate labels. Redundancy is harmless. No overlapping support pair is used, and no possible pair is omitted. A support of size four can occur only opposite a constant function, whose covariance is zero.

For a real increasing function f on its finite cube, list its distinct values v_1 < ... < v_m. Then f = v_1 + sum_{i=2}^m (v_i-v_{i-1}) 1_{f >= v_i}. These level sets are increasing and retain the same coordinate support. Applying bilinearity to two such decompositions proves full negative association from the indicator inequalities. If both functions are nonconstant, at least one strictly positive weight occurs in each decomposition, and every contributing nonconstant event pair is strictly negative at positive times. Thus the strictness statement is also justified.

## Generator and infinite volume

In normalized time tau = p t, a bond with configuration 10 swaps right at rate 1; a bond with configuration 01 swaps left at rate r. The author bit numbering, initialization, and four-site extraction agree with this orientation: the 16 sites are [-7,8], and the observed bits are exactly [-1,0,1,2]. The 18-site cross-check uses [-8,9]. The diagonal includes the full sum of active rates, so it is not an embedded jump-chain calculation.

At most six actual swaps from the step cannot reach a window boundary. Diagonal factors in a generator product change no state. The author's finite-window computation of the first six derivatives is therefore exact for the infinite system. Independent infinite-deviation recomputation supplies a second, differently represented verification of the same fact; agreement between two finite windows alone would not establish it.

For an interval-supported bounded function h of support length m, at most m+1 bonds affect h. At each configuration only one of the two possible directed swaps on a given unequal bond is effective, and its normalized rate is at most 1. Consequently ||G h|| <= 2(m+1)||h||. The support grows by at most one site at each end. For initial support contained in a four-site interval, this gives

D_j = 2^j product_{ell=0}^{j-1}(5+2 ell).

The independently checked values D_0 through D_7 are 1, 10, 140, 2520, 55440, 1441440, 43243200, 1470268800. The product inequality D_i D_{j-i} <= D_j follows by comparing the increasing factors in the second product with the later factors of D_j. The same bounds hold for a, b, and ab.

In a reflecting finite system the semigroup is a sup-norm contraction, so each order-j expectation derivative is bounded by D_j at every nonnegative time. Leibniz's rule therefore bounds the j-th covariance derivative by D_j + sum_i binom(j,i)D_iD_{j-i} <= (1+2^j)D_j. Taylor's theorem at the first nonzero coefficient c_k = -a yields

H(tau) <= -a tau^k + ((1+2^(k+1))D_(k+1)/(k+1)!) tau^(k+1).

To pass this inequality to the infinite process, couple through the nearest-neighbor graphical construction. A discrepancy affecting one of the four observed sites from a boundary at distance d requires a chronological nearest-neighbor path with at least d clock rings. There are at most 4*2^n site-path choices of length n and each unoriented edge-clock rate is at most 2. A conservative bound on the discrepancy probability on [0,T] is thus 4 sum_{n>=d}(4T)^n/n!, which tends to zero. This establishes convergence of cylinder expectations. The stabilized Taylor coefficients and uniform finite-volume inequality then pass directly to the limit. It is unnecessary to interchange derivatives with an infinite-volume limit or assume analyticity of the infinite semigroup.

The sufficient bound for each case is tau <= a(k+1)!/[2(1+2^(k+1))D_(k+1)]. Its minimum occurs in the two order-six cases with a=1/144. Their seventh-order remainder constant is 37,631,880, giving 1/(288*37631880) = 1/10837981440 exactly. This is a sufficient, deliberately conservative time bound, not a claim of optimality.

## Endpoint and scope checks

The formal parameter r is not sampled. Every leading coefficient is a negative rational constant and every preceding polynomial vanishes identically. The remainder is uniform on the entire closed interval 0 <= r <= 1. The proof consequently includes q=0 and q=p, and deterministic time zero separately. The normalization requires p>0 as stated. Negative q, q>p, and p=0 are not part of the accepted theorem.

There is no deduction of strongly Rayleigh dependence for asymmetric dynamics, no restart from the evolved law, and no uniform time interval over arbitrary finite site sets. A local four-site result cannot decide the full question. The symmetric endpoint is already covered much more broadly by established symmetric-exclusion results; including it here does not imply novelty.

## Non-vacuous computational controls

The author checker passed normal, optimized, isolated/no-site, and combined isolated/optimized execution from a relocated directory, with the 16/18-site cross-window comparison. All 12 author negative-control executions were rejected at the intended coefficient/certificate check.

The independent checker also passed all four execution modes from a directory containing spaces. Its independent controls rejected nine certificate/model-metadata mutations in both ordinary and combined isolated/optimized modes, plus reversed jump rates and a reversed initial step in both modes: 22 rejected executions. The rejection reasons were mathematical coefficient, coverage, or parameter mismatches, not missing-file or import failures. The entire independent control suite was itself rerun under isolated/optimized Python with identical results.

A separate probability-law control is uniform even parity on three coordinates with the fourth fixed at zero. Its six pairwise occupation covariances are all zero, but Cov(X1, X2 OR X3)=1/8. The independently generated event family includes this witness. This demonstrates concretely that the all-event audit is stronger than pairwise covariance testing. This diagnostic law is not claimed to be an ASEP law.

## Source and inherited-work audit

All three complete corpus files were independently hashed, rather than trusting an extracted row: catalog.json (21,735,099 bytes), problems.json (68,931,837 bytes), and research_results.json (80,334,822 bytes). The exact target problem record is unique. Canonical JSON serialization of that complete record and its associated report is 4,717 bytes with SHA-256 a5d34b275787b44a3df2be2c3d3839f0d507c5b84843e7e1430f886b7e864090, matching the catalog review hash and frozen source metadata.

The inherited report is literature-only triage. It does not contain an authored proof, reduction, or exact computation; unsupported broad preservation and unspecified small-time-progress language cannot substitute for a theorem. The corpus gate records rank 933, zero prior turns, and queued status. A fresh read of the public queue at blob 03f0ef6adc2b8d550f8b2b370f63689d72757553 agrees. Fresh bounded repository queries by ID and code found no PR, and default-branch code search by ID returned no result. These absence results have limited scope and do not certify novelty or absence of work elsewhere. The original package's other historical search counts were not independently replayed.

All five supplied primary PDF files were independently byte-counted, hashed, and freshly text-extracted. Their pins match SOURCES.json. Relevant sections were read, and Liggett's page 2 was visually inspected:

- [Liggett, Some Open Problems, October 15, 2012](https://web.archive.org/web/20150919235903id_/http://www.math.ucla.edu/~tml/open.pdf), page 2, Problem 4: the infinite left-full/right-empty step with rightward drift is the target, and the reversed step is expressly distinguished. Page 1 supplies the irreducible transition-kernel convention. The archived web URL could not be refetched by the web tool in this audit; inspection used the locally pinned three-page PDF.
- [Borcea, Branden, and Liggett, Negative dependence and the geometry of polynomials](https://arxiv.org/abs/0707.2340), Section 3.5, Theorem 5.2, and Remarks 5.1-5.3: symmetric dynamics preserve strongly Rayleigh initial laws. Arbitrary NA preservation is false even in the symmetric setting. The asymmetric two-site counterexample uses a random product initial law and does not refute the specified infinite deterministic step. The public arXiv page independently confirms version 2 and the JAMS publication details.
- [Conroy and Sethuraman, Gumbel laws in the symmetric exclusion process](https://arxiv.org/abs/2210.15550), Sections 1.4 and 3.2: the NA/strong-Rayleigh input belongs to the symmetric model; the ASEP discussion concerns tagged-particle asymptotics and the opposite-drift limiting distribution.
- [Conroy, Gonzalez Casanova, and Sethuraman, Point process convergence of extremes in K-symmetric exclusion](https://arxiv.org/abs/2506.12632), Sections 1.2, 2.1, and 5: the correlation comparison remains under a symmetric kernel even when translation invariance is dropped. The public page confirms arXiv version 1 submitted June 14, 2025; the PDF's displayed manuscript date is June 17, 2025. These are different date conventions, not inconsistent version metadata.
- [Conroy and Sethuraman, Poisson statistics, vanishing correlations, and extremal particle limits for symmetric exclusion in d > 1](https://arxiv.org/abs/2501.10522), model definition and Section 3.2: the process is symmetric and the results do not imply finite-time NA for one-dimensional ASEP. The public page confirms version 2 dated February 26, 2025.

A bounded fresh public search found no primary source resolving the precise all-time problem. The live individual UnsolvedMath page was inaccessible; its indexed category listing matched the ID and orientation. None of these searches establish current open status conclusively or establish novelty of the local theorem.

## Reproduction and payload safety

From the extracted package root, run:

    python original/asymmetric_exclusion_9600004/check_certificate.py --cross-window
    python original/asymmetric_exclusion_9600004/test_mutations.py
    python audit/independent_recompute.py
    python audit/test_independent.py
    python -I -S -O audit/test_independent.py

Optional input-byte verification requires separately supplied original corpus/PDF files:

    python -I -S -O audit/verify_inputs.py --corpus-dir CORPUS_DIRECTORY --pdf-dir PDF_DIRECTORY

The safe ZIP contains only preserved authored proof/checker/certificate files, authored audit text and code, generated verification results, and public-source/corpus metadata. It excludes all third-party PDFs, extracted third-party text, dataset records or contents, raw repository/room-history responses, private coordination, and Python bytecode. Its external manifest records each included member, the final archive bytes and hash, and this limited acceptance decision. The frozen author files were rechecked after packaging.
