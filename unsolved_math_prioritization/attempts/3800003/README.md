# Degenerate facets: audited prior partial resolution

Problem **3800003 / AMR-037-0003**, queue rank **927**. Canonical queue status: **unsolved, 2/5**. The full sharp extremal problem and the restricted quasisimplicial case are unresolved by this packet. No novelty or sharpness is claimed.

## Accepted claims and precise scope

For a full-dimensional convex four-polytope with exactly **N >= 5** vertices, let D4(N) be the maximum number of nontetrahedral facets. Here degenerate means more than four vertices, not zero volume.

- [Joswig and Ziegler, Neighborly cubical polytopes](https://arxiv.org/abs/math/9812033v2), Theorem 16, supplies convex cubical four-polytopes with the m-cube graph. At m=10, incidence and Euler counting give 1024 vertices and 2048 cubical, hence degenerate, facets. This is a theorem-dependent prior positive answer to the existential 2N subquestion, not a new coordinate certificate or a minimality claim.
- [Nevo, Santos and Wilson, Many triangulated odd-dimensional spheres](https://link.springer.com/article/10.1007/s00208-015-1232-x) gives a published convex Omega(N^(3/2)) lower bound; the inspected preprint's Theorem 4.6 and Corollary 4.8 provide the regular-subdivision and convex-lifting bridge. A quadratic sphere result is not a quadratic convex-polytope result.
- The authored common-pulling-triangulation argument proves the coarse elementary upper bound D4(N) <= floor(N(N-3)/4). The exponents 3/2 and 2 do not match.
- [Avvakumov and Hubard, Cubulating the sphere with many facets](https://arxiv.org/abs/2503.18047v1) states: for each fixed sphere dimension d >= 3 and every N >= 2^(d+1), a cubulation has at most N vertices and at least c(d) N^(5/4) facets. This lower-bound statement is not a matching Theta result or a convex realization theorem.

The cubical witness has square ridges and does not settle the quasisimplicial restriction. No complete sharp maximum, formal proof certificate, independent reconstruction of the external existence constructions, exhaustive current-literature survey, or global 2026 openness theorem is claimed.

## Unchanged accepted artifacts

Read [original proof](author_original/PROOF.md), [original report](author_original/REPORT.md), [full independent audit](independent_audit/AUDIT_REPORT.md), [mathematical source review](independent_audit/MATH_SOURCE_REVIEW.md), and [exact acceptance](independent_audit/EXACT_ACCEPTANCE.json).

The original author and independent-audit archives, their external manifests, and the independent acceptance receipt are preserved byte for byte in `archives/`. Their 11 members each are unpacked unchanged in `author_original/` and `independent_audit/`. The audit contains another unchanged copy of the author archive and external manifest. No repair or derivative author packet was needed.

This README is a separate publication supplement. It does not silently edit historical claims: the frozen author's pending-audit marker records its earlier state; the independent audit separately accepts the original exact bytes. The audit's historical recommendation of stalled is mapped to the canonical queue value unsolved, with Turns 2/5. Only the target row's Status, Turns and Findings cells change; all unrelated queue bytes and existing links remain intact. No fresh proof-attempt turn is added.

## Reproduction and trust boundary

Independently authenticate the SHA-256 of `verify_publication.py` and `PUBLICATION_MANIFEST.json` using the publication receipt before executing the wrapper. A replaceable manifest cannot authenticate itself. The wrapper requires the independently supplied manifest hash, authenticates every publication file, archive and member, and checks all complete corpus and source inputs before executing any packet script.

    python -I -B verify_publication.py --expect-manifest MANIFEST_SHA256 --catalog CATALOG --problems PROBLEMS --reports REPORTS --sources SOURCES
    python -I -B -O verify_publication.py --expect-manifest MANIFEST_SHA256 --catalog CATALOG --problems PROBLEMS --reports REPORTS --sources SOURCES

Use exact complete inputs identified by public hashes and byte counts in the frozen metadata. The wrapper and audit make no network requests. They replay isolated normal and optimized arithmetic/source/integrity tests in relocated directories with an unrelated poisoned working directory. Four positive and 22 negative audit case families, plus nine freeze case families, are reproduced; negative controls require the exact rejection state, not just a crash. Counts and hashes do not constitute formal proof or establish the imported realization theorems.

The package is AI-assisted and unrefereed. Independent AI review is not conventional human peer review. Only authored reports/code and public bibliographic or verification metadata are published; no source PDFs, extracted third-party source text, dataset contents, private sources, or private coordination material are included. A draft PR and local/retrieved-byte test results do not imply passing GitHub CI. Publication does not include merging, a GitHub release, DOI creation, or outreach.
