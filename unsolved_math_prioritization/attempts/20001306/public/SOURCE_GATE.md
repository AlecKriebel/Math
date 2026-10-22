# Source and scope gate

Checked 3 October 2026. Problem 20001306 / AIM-CONVEX_GEOMETRY-0038.

## Original source

The problem landing page was unavailable to the web reader. The pinned catalog and previous report identified the source, but the authoritative mathematical target was recovered directly from the official AIM workshop PDF, printed page 3, Problem 10:

https://aimath.org/WWN/fourierconvex/fourierconvex.pdf

The target is the Baire-generic failure of IK to be a polar zonoid for origin-symmetric convex K. The imported title about closedness and a dual certificate is not the target. Schneider's 2001 primary formulation supplies n >= 3 and the Banach–Mazur compactum, with the equivalent Hausdorff version explained in the note. The unrestricted planar interpretation is false.

## Primary literature inspected

1. R. Schneider, *On the Busemann Area in Minkowski Spaces*, Beitr. Algebra Geom. 42 (2001), 263–273. Page 264 explicitly states that openness is known and density is unknown; Lemma 1 identifies the relevant zonoid criterion, and pp. 270–272 give the cube obstruction. The paper was retrieved from the EMIS mirror at https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.42/no.1/b42h1rsc.pdf . Its original ETH link failed.
2. M. A. Alfonseca, *Intersection bodies that are not polar zonoids: a flat top condition in dimensions four and six*, J. Math. Anal. Appl. 404 (2013), 326–337, https://arxiv.org/abs/1303.3813 and https://doi.org/10.1016/j.jmaa.2013.03.032 . Proposition 1/Corollary 2 and Proposition 4/Corollary 5 were read with their derivations. The four-dimensional truncation theorem in this note is a direct corollary, not an independent novelty claim. The six-dimensional cylinder's displayed integrals in arXiv v1 yield h=5/4 and k=5/6; the printed h-value differs. Local rendering of that page confirmed this is present in the PDF rather than an extraction artifact. The failure of the sufficient test remains the same.
3. R. Schneider, *Crofton measures in projective Finsler spaces* (2005), Section 5: https://home.mathematik.uni-freiburg.de/rschnei/Wuhan.pdf . This is the correct title of the work, more specific than the previous report's citation. It again treats full density as conjectural.
4. D. Ryabogin and A. Zvavitch, September 2026 preprint, https://arxiv.org/abs/2609.10852 . The abstract and full Section 7.1 were checked. It answers a different AIM question about zonoids and their polars staying away from Euclidean balls as dimension grows. Its intersection-body remarks concern the larger radial-closure class; they do not provide convex preimages or a genericity proof for IK.

Targeted searches covered the original wording, “polar zonoid” with density/genericity, the Busemann-area formulation, flat-top bodies, and Schneider/Wieacker. No later full resolution of this exact problem was located. This is a bounded literature search, not an exhaustive proof that the problem remains open worldwide.

## Prior work and duplication

The complete imported prior report was read. It already proves closedness, the planar exception, the signed-measure separation criterion, and affine invariance, and explicitly leaves density open. Those ingredients are background, not relabeled as new results.

Live main-branch queue rank 511 was still queued at the source check. Same-ID code, PR and branch searches returned no matches. Searches for zonoid/polar-zonoid work, the repository root, the attempts directory, and paper-page names found no mathematically identical previous repository attempt. The related-target-groups file had no occurrence of this ID. Code search indexing is incomplete, so empty search results are not an exhaustive history guarantee. The other catalog record mentioning generalized intersection bodies, 20001301, concerns a different linear-generation/approximation problem.

## Claims permitted by this package

- Full target: unresolved; proposed queue classification is exhausted after five substantive attempts, with partial results.
- Restricted four-dimensional revolution-body genericity: proved by published theorem plus explicit cap construction, with an independent normalized analytic derivation included.
- Finite rational certificates and quantitative stability: elementary consequences, no claim of absolute novelty.
- Cube computations: exact finite-dimensional instances of a published witness, not an all-dimensional theorem.
- Harmonic linearization: formula proved; the uniform convexity-preserving sign-changing perturbation is not proved.

The author-stage work made no remote edits, queue changes, commits, branches, PRs, releases, or external communications. The proposed public files are authored notes and exact verification code/output only; downloaded PDFs, source transcriptions and catalog/report extracts are excluded. The frozen package requires fresh adversarial review before any publication.
