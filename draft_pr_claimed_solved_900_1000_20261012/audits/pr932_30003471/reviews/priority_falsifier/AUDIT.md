# Fresh adversarial priority audit

Target: eligible PR932 / problem 30003471 only. Audit family: priority falsifier. Original immutable head: c09ef9df8b1f4642be0396ba6343344be8fa25b0. The exact selected prefix has 29 files, all authenticated from actual Git objects and the original on-disk snapshot at start and end. The proof's SHA256 is 6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415. Original author proof-search accounting remains 1/5; this verification adds zero positive proof-search turns.

## Scope and independence

The complete research charter, selected private source record, and original public proof were read. INITIAL_RECONSTRUCTION.md was written before consulting any current or historical sibling priority verdict. No sibling verdict was needed or read. After the independent reconstruction, the root's proposed closure text was reviewed only for the priority claims within this audit's scope. This audit did not repeat the complete smooth-boundary/Dirac audit and does not certify the candidate's entire proof from scratch.

All writes were confined to this review folder. No original file, Git index, branch, HEAD, PR, external tracker, or publication record was changed. The only project coordination was with the root agent. Sources were retrieved read-only; no individual was contacted and no outreach was drafted.

## Finding

The meaningful priority finding survives this fresh attempt to falsify it. The exact full-normal-Gram strengthening is already Theorem 1 in Martin Winter's author-hosted two-page note, *Stoker's theorem from polytopal tensegrities*. The note states the stronger orthogonal identification of every labelled outward facet normal for combinatorially equivalent full-dimensional bounded convex polytopes in arbitrary dimension d>=2. It permits weak angle domination and imposes no simplicity restriction. Its three-dimensional case covers the exact original target and the candidate's full Gram-matrix conclusion.

PRIOR_IMPLICATION.md supplies a checkable independent proof of the bridge, plus an independent reconstruction of the material content and equality case of published Theorem 3.2. The exact foundational input retained is Izmestiev's polar-volume Hessian signature/kernel theorem, together with the established generalized Wachspress coordinate properties. The foundational signature argument uses the second Minkowski inequality and Bol's equality condition. It is not replaced by numerical evidence or silently promoted into an elementary theorem proved from scratch here.

## Specific falsification attempts

| Potential failure | Check and outcome |
| --- | --- |
| Scaled target normals fail to realize the source polar | True in general, but irrelevant: published Definition 4.2 / Theorem 3.2 allow arbitrary target graph points. The source coordinate map remains defined. Controls explicitly give nonplanar radially rescaled cube faces while the degree remains one. |
| Homotopy crosses zero on a nonsimplicial face | For corresponding target-polar face vertices w_i, choose its supporting functional y with y.w_i=1. Positive radial factors give y.phi_t>=min_i min(1,k_i/h_i)>0. The argument applies simultaneously to every vertex of that face. |
| Need a common global hemisphere | No: each boundary face has its own strict halfspace. These estimates prove pointwise nonvanishing of one globally continuous map, which is exactly what homotopy invariance of degree requires. |
| Need an orientation-preserving matching | No: the boundary degree is +1 or -1. Either is nonzero. A fixed arbitrary face-lattice isomorphism is retained throughout. |
| Need equal support numbers | No: lambda_i(t)=(1-t)+t k_i/h_i remains strictly positive for arbitrary h_i,k_i>0. |
| Wrong angle or edge-contraction direction | Interior angle pi-arccos(n_i.n_j) increases with the dot product. The exact squared-distance difference is 2(m_i.m_j-n_i.n_j)/(h_i h_j)>=0. |
| Zero might occur only on the boundary | The strict halfspace estimate excludes this. A nonzero-degree boundary map forces an interior zero. |
| Nonsimple vertices invalidate source coordinates | The coordinate statement in published Remark 3.7 is general. Positivity and linear precision force face support; three-dimensional edge and vertex limits are unique, even at nonsimple vertices. Only the established coordinate continuity theorem is imported, not a nonexistent smooth combinatorial map. |
| Contraction equality gives only an affine map | Theorem 3.2 indeed first gives an affine map with equal edge lengths. Equal vertex radii add a quadratic polynomial that vanishes on all vertices and edges, hence on each face and the full space. This forces an origin-preserving orthogonal map. This step is proved explicitly in PRIOR_IMPLICATION.md. |
| Hidden same-metric or Dirac assumption | None in this route. It uses polars, generalized barycentric coordinates, a matrix theorem, and topological degree. No singular-index theorem or claimed Wang-Xie-Yu theorem is required. |
| Degenerate or limiting families | Full-dimensionality, boundedness, positive supports, and actual facets are used explicitly. No uniform bound or conclusion is claimed at a collapsed, unbounded, or zero-support limit. |

## Material published proof access

The main Oxford article endpoint and publisher PDF endpoint returned 403 in direct retrieval; the public publisher CDN article body returned 200 and 317590 bytes, SHA256 0075c5ccda2fe18accfad9bc0b42b82bf3407f179f318328249436071d9a8413. It contains the actual complete mathematical body. Theorem 3.2 and its full proof, Theorem 3.3, the row-sum calculation, Remark 3.7, and Lemma 4.3 were checked there, and compared with arXiv:2302.14194v2. Thus this is actual published-body inspection, not just a journal metadata check. The version-pinned author PDF has SHA256 781bf1927041f40ae15a4ce39c9ee5aee98873b2e3c73aaec60ec0cd82adb3ca and 842724 bytes.

The independent reconstruction replaces the published proof's positive-eigenvector centering by the equivalent positive semidefinite matrix A=alpha alpha^T-M. The trace identity, edge signs, kernel, affine equality case, and origin-preserving orthogonality were all checked. The published Lemma 4.3 compresses its final all-pair-isometry claim; that compression is filled explicitly, rather than accepting the conclusion on trust.

Both note pages and relevant author-manuscript proof pages were rendered. The theorem, radial homotopy, coordinate property, and equality pages were visually inspected. All source bodies, extracts, and renders stay private and are excluded from the public manifest.

## Timing and exact priority claim

The note's current bytes are 289110 bytes, SHA256 520aed6feadfdda0906f61a3d780830142d36fbbd93bca80678533ee321610e1. A fresh author-repository API request records addition of this file at commit 766c313bc2187a5eafd5757dca43ffefc6a9ced6. Both author and committer dates are 2026-09-04T20:55:42Z. A separate historical raw-commit retrieval returned the identical bytes; its Git blob SHA1 agrees with the API's 592725cde9a0783de0f4a6216f241ab07db2518b. The commit is unsigned. This is primary historical repository-date evidence, not an independent platform push-time or archival timestamp. The historical claim is not inferred merely from the mutable PDF's September 4 date.

The original candidate itself says prepared October 8, 2026. Actual Git metadata for the original immutable head records 2026-10-07T17:48:11-07:00, equivalently 2026-10-08T00:48:11Z. The recorded prior-note date precedes that candidate.

The publisher's actual article record states publication December 21, 2023, with IMRN volume 2024, issue 9, May 2024, pages 7721-7747, DOI 10.1093/imrn/rnad298. Crossref independently agrees with these bibliographic details. The explicit dihedral theorem is the September 2026 note; the 2023 publication supplies the prior machinery. This audit does not claim the IMRN paper explicitly stated the dihedral theorem, and it does not adopt the note's broad remark about a theorem since 2023.

## Required and optional issues

Required for any next publication framing: do not present this exact comparison theorem, its nonsimple three-dimensional case, or its full normal-Gram consequence as a newly resolved open problem. The explicit prior theorem already covers them. Attribution repairs credit but cannot create novelty. An attributed alternative proof may be valuable, but no independent new theorem or new-method priority claim has been established in this finite audit.

No unresolved mathematical defect in the prior polar/degree/Wachspress/contraction implication was found. No required correction remains in the priority paragraphs of the root's final reviewed closure draft. Its whole-candidate mathematical and historical floating-point-replay assertions depend on other reviews and were not independently recertified here.

Optional exposition corrections in the prior note: its page-2 supporting-hyperplane sentence should refer to the corresponding face of Q-polar, rather than the source face as though it lay in Q-polar. Its reference to the IMRN paper's Theorem 2.3 appears to mean Theorem 3.2. Also, degree should be allowed to be -1 for an orientation-reversing fixed correspondence; nonzero degree is sufficient. These are not counterexamples or missing mathematical mechanisms.

The root accepted two precision edits to the draft: full-dimensional bounded convex scope; and repository-commit-date wording with an explicit missing independent push-time/archive certificate. Its final reviewed SHA256 is recorded in RESULT.json. No external closure, merge, publication, or tracker decision is made by this review.

## Reproducible checks and limits

CONTROLS.py uses only Python's standard library. It verifies the cube matrix spectrum and expansion inequality using exact fractions; tests 100 deterministic edge contractions; detects an affine edge-preserving map that fails radial preservation; checks positive radial boundary degree numerically at five times; exhibits nonplanarity under radial scaling; checks a square-pyramid apex with four incident facets; and catches zero radial scaling as a negative control. All pass. These are diagnostics. The universal proof is the deduction in PRIOR_IMPLICATION.md and its clearly stated prior foundations.

The public manifest is an explicit curated allowlist. It excludes private source material, copied article bodies, extracts, renders, temporary files, the private selected-source record, and the manifest itself. VERIFY.py checks its exact files, hashes, original 29-file Git/disk authentication, and reproducible controls. The external final manifest pin/count are reported to the root outside the manifest to avoid a self-hash cycle.

Finite scoped priority audit completion: 100%. This percentage measures completion of this verification assignment, not a claim to have proved a new research discovery.
