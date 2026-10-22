# Independent audit: degenerate facets of polytopes

## Verdict

**PASS, with the stated bounded mathematical scope.** The original author archive is accepted unchanged as a prior partial-resolution correction, not as a solution of the complete extremal problem. No proof repair or derivative author packet is needed. Recommended queue treatment remains **stalled, 2/5**.

Accepted original: `DEGENERATE_POLYTOPE_3800003_AUTHOR_SAFE_FREEZE.zip`, 12,004 bytes, SHA-256 `1d82820c9e37d3d8118a8ddc5b2aa55bea0d0744b78b5594b85e23bb80e81f34`.

Its externally supplied author manifest is 3,250 bytes, SHA-256 `0cdd8ad3ad85c08c3d5905f107d44627f6969a8a0e698feb65b873aa2758b9cb`. Its inner member manifest is 1,435 bytes, SHA-256 `59c526e5013aec636862e5455400f056fc58b366222399f209174b4ff8c57481`.

## Identity and prior-work gate

The three complete exported corpora were independently byte-counted, SHA-256 checked and parsed. Both catalog and problem collection contain one exact record for ID 3800003 / AMR-037-0003; the catalog rank is 927. The complete record/report pair under the recorded canonical Python serialization is 3,881 bytes and SHA-256 `53c09f2d30d1c19a2cb903b1a75400bfcfe593074e64bd305035fb630a1c99c3`. The complete inherited report was read. It records literature searches and an unresolved classification, without a substantive original mathematical attempt. Its assertion that the specific 2n question was unresolved is contradicted by the checked primary literature.

This audit independently checks the corpus identity and literature-only characterization. The historical GitHub-search counts and failed live catalog access recorded in the author metadata are retained as author retrieval history, not silently represented as new audit searches. A failed live page request establishes no present mathematical status. No corpus record or source document is redistributed.

## Mathematics and imported results

The source-based details are in `MATH_SOURCE_REVIEW.md`; the concise accepted claims are:

1. “Degenerate” means a facet of a d-dimensional convex polytope with more than d vertices. In dimension four, these are exactly the nonsimplex three-dimensional facets. It does not mean zero volume.
2. Joswig–Ziegler's existence theorem, with dimension 4 and preserved skeleton dimension 1, supplies actual convex cubical polytopes having the m-cube graph for every integer m >= 4. The theorem's convex realization is an imported published result, not inferred from arithmetic or from the existence of an abstract sphere.
3. The graph gives 2^m vertices and m*2^(m-1) edges. Cubical facet/ridge incidence and Euler's relation then give the face vector (2^m, m*2^(m-1), 3(m-2)2^(m-2), (m-2)2^(m-2)). At m=10 this is (1024,5120,6144,2048). Every facet has eight vertices, so the historical existential 2n question has a positive answer. No minimality of 1024, construction for every prescribed vertex count, or new discovery is claimed.
4. Nevo–Santos–Wilson supplies a stronger convex-polytope lower construction with bipyramidal facets of order N^(3/2). Its quadratic sphere construction is not automatically a quadratic convex-polytope construction. Neither the author nor this audit asserts that all remaining facets of the lifted polytopes are simplices.
5. A common pulling order gives a coherent triangulation of the entire boundary without adding vertices. A nonsimplex original facet contains at least two resulting tetrahedra. With D such facets and t tetrahedra, 2D <= t. Every triangle of the boundary triangulation occurs in two tetrahedra, hence f2=2t. Euler gives t=f1-N, and f1 <= N(N-1)/2. Therefore D_4(N) <= floor(N(N-3)/4). Every step is valid for a convex four-polytope, necessarily N >= 5. Simplicial facets do not invalidate the inequality: they only add further tetrahedra.
6. Avvakumov–Hubard's cited 2025 result concerns cubical spheres; a convex realization of those particular examples is not supplied by its theorem. The source is not used as a convex lower theorem or as an exhaustive 2026 status survey.

The full maximum in general dimension, or even the sharp four-dimensional extremal function, is not determined here. The accepted checked four-dimensional exponents remain 3/2 below and 2 above. The elementary upper estimate carries no novelty or sharpness claim.

## Artifact audit

All 11 author ZIP members match the pinned external manifest and the loose author files. The ZIP has no duplicate members, unexpected paths, directories or symlinks. Both inner and outer manifests were checked before executing any author script. All four successful primary-source files match their published-input pins.

The independent replay extracts authenticated bytes into a fresh temporary directory whose name contains spaces, copies all three complete corpora and all four source inputs into separately renamed locations, and runs from an unrelated directory. Poisoned `json.py` and `fractions.py` files and a hostile PYTHONPATH ensure the `-I` subprocesses are not using the working directory as an import source. Every subprocess uses `-I -B`, in both normal and `-O` modes. Outputs must be identical between modes. No package bytecode files are left behind.

Four positive case families pass in both modes:

- The original exact arithmetic diagnostics: 21 cubical dimensions, nine rejected built-in mutants/invalid dimensions, 41,660 upper-bound integer pairs, and four regular-subdivision arithmetic checks.
- Complete source/corpus verification against the recorded pins and exact identity.
- Original packet integrity against the independently supplied member-manifest anchor.
- Independently expressed arithmetic over 97 cubical dimensions and 996 upper-bound vertex counts.

Twenty-two mutation case families are rejected in both modes: changed proof, extra and missing files, symlink, rebound manifest, rebound solved scope, forged-success script, rebound provenance metadata, duplicate manifest key, reanchored solved-scope gate, each of the three wrong complete corpus files, each of the four corrupted public-source files, incorrect cubical facet count, incorrect ridge incidence, incorrect threshold witness, incorrect upper-bound coefficient, and incorrect regular-subdivision cell count.

A rejection counts only with exit code 1, empty stdout, and the exact expected final ValueError message. An arbitrary crash, missing dependency or incidental failure cannot satisfy these tests. The audit replay itself is also executed under normal and optimized Python, with identical complete receipts. There are no optimization-sensitive assertion statements in the acceptance logic. Numerical checks verify consequences and implementation behavior; they do not independently establish convex realizability.

## Acceptance boundary

The immutable original author status says the independent audit was pending. This separate exact acceptance supersedes that historical pending marker for these pinned bytes; the original is deliberately not rewritten. No repository, branch, queue, PR or external service is modified by this audit. Publication is a separate authorized operation.

The audit does not claim a machine-checked proof, a full independent reconstruction of the imported existence constructions, novelty, exhaustive current literature coverage, or a full solution of the problem. The source review distinguishes inspected theorem statements and proof passages from those limits. Acceptance applies only to the exact hashes identified here and in `EXACT_ACCEPTANCE.json`.
