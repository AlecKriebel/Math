# Independent adversarial audit: equal-area plane triangulations

## Verdict

**PASS for the stated partial mathematics and the unsolved 5/5 disposition, with two documented verifier-hardening gaps.** No correction to the mathematical proof is required. The original Ziegler problem is neither proved nor disproved. This is a separate AI mathematical and computational review, not human peer review or formal proof-assistant certification. No historical novelty is asserted.

The main theorem is correct under the explicitly stated ordinary straight-line drawing convention: for the labeled cycle bipyramid with cycle length m >= 4, selected exterior face A,V0,V1, and those three fixed noncollinear coordinates, there are exactly m-2 equal-positive-area drawings. The classification permits collinear nonfacial triples, but no colliding vertices, collapsed faces, edge overlaps, or unwanted vertex-edge incidences.

The author packet is preserved byte-for-byte under `author/`. The top-level independent checker supplies stricter geometric and filesystem gates. `AUTHOR_HARDENING.patch` is a separate, tested four-line correction to the author verifier; it has **not** been applied to the frozen subtree. A successor author packet would need its own regenerated manifest and receipts. Do not silently replace the historical author results with the hardened counts.

## 1. Binding and scope

Reviewed author ZIP: 17,838 bytes, 10 members, SHA-256
`6c85983f217c64e1089496e0ccfc42ff4913984d98e0c4ad863450cb4e65afea`.

The exact proof is 11,394 bytes with SHA-256
`26c0464bdf08ecbd25b954d5b24b84168c302f4ca57bbd64597974f75f8b4849`.
The author manifest is 1,223 bytes with SHA-256
`1d99dd20f9ed095b3d199b2802f0198ccab4832654e65b27d35f0643e1fa5f3c`.
All ten extracted members, all nine inner-manifest entries, the archive checksum, and the complete corpus review hash were independently recomputed. The exact frozen code and proofs were read, rather than inferred from receipts.

The complete catalog row and full target record, including its background, literature assessment, nested metadata, statement variants, and verification fields, were inspected. There is no research-results entry for this catalog number; default sorted JSON serialization of `[record, {}]` produces 3,539 bytes and SHA-256
`b2d46c0a6ab60b93916096d38c89b7eaca3210cec9e61e4c0f49677cc21ecbfc`, exactly matching the catalog. All three complete corpus byte counts and hashes match. Only this public verification metadata is redistributed.

## 2. Independent mathematical reconstruction

### Family graph and outer-face convention

The graph has m+2 vertices and 3m edges. Its spherical embedding has 2m triangular faces; choosing one as exterior leaves 2m-1 bounded faces. Deleting at most three vertices cannot disconnect it: if an apex remains it connects every surviving cycle vertex, and any other surviving apex meets that component through a surviving cycle vertex; if both apices are deleted, the cycle loses at most one vertex. Since m >= 4, a surviving cycle vertex always exists. Thus the graph meets 4-connectivity, not merely 3-connectivity.

Fix C=V0=(0,0), E=V1=(1,0), A=(0,1). The normalized outer doubled area is one, so an equal-area drawing has common doubled face area a=1/(2m-1). No equality involving the unbounded face is imposed. A nondegenerate affine change of the outer labeled triangle preserves the conclusion. The cycle and apex symmetries carry every choice of exterior triangular face to this case; no extra solutions arise from changing the chosen outer face while pretending its labels stayed fixed.

### Why the classification is exhaustive

Set M=(A+B)/2. For every nonbase cycle edge UV, its two bounded incident faces have opposite orientations relative to the edge and equal positive areas. Their determinants therefore imply `[UVM]=0`. The base face CEB gives B_y=a, hence M_y=m/(2m-1)>0.

Consider the simple labeled path E,V2,...,V(m-1),C. At every change between distinct supporting lines, the common path vertex must be M. Distinct vertices allow at most one such change. There must be a change, since a path confined to one supporting line would have E and C on that line, forcing M onto y=0. Therefore the path consists of a chain E to M and a chain M to C, with one and only one labeled midpoint vertex.

An embedded straight chain cannot reverse direction without overlapping consecutive edges. If its two edge counts are r and s, then r,s > 0 and r+s=m-1. Equal face areas at A force each chain's subdivisions to be equal. Summing the s faces between A and the M-to-C chain yields M_x=s/(2m-1), and therefore B_x=2s/(2m-1). Every coordinate is forced. The possible r are precisely 1,...,m-2. They give different B coordinates and different labeled midpoint vertices, so the count is genuinely m-2 rather than an unlabeled quotient or a parameterization with repetitions.

This argument uses the embedding hypothesis exactly where it is needed and does not confuse roots of unsigned area equations with genuine drawings.

### Why each candidate is genuinely embedded

For every permitted r,s, the stated M has positive barycentric coordinates in ACE. The three coarse triangles CEM, AEM, AMC partition the exterior triangle. In CEM, the coefficients of B relative to C,E,M are r/m, s/m, 1/m. They are strictly positive and sum to one. Hence B's spokes triangulate CEM; A's spokes triangulate the two other coarse triangles. Their boundaries are compatible. All cycle subdivisions are monotone with distinct vertices. The two coarse boundary lines intersect only at M, and A,M,B occur in that order on the separate apex-midpoint line. No illegal vertex incidence or overlapping spoke is introduced.

The independent symbolic checker multiplies all coordinates by D=r*s*(2r+2s+1), works in a sparse polynomial ring over Q, and proves the base and both chain face determinants equal D^2/(2m-1). It also proves the endpoint and midpoint identities. Together with the positivity and partition argument, this verifies existence for every m, not just the finite sample.

### Continuation, harmonic placement, weighted induction, and symmetry

- The independently derived seven polynomial face areas agree with the author's map and sum identically to one. Analytic differentiation, followed by a separate Leibniz determinant calculation, gives determinants +8/49 and -8/49 at the two octahedron solutions. At their midpoint the rank is exactly five, with the displayed nonzero kernel direction. The midpoint is separately checked as an actual positive-area embedding. This refutes everywhere-regular continuation and any same-positive-local-sign argument of the indicated kind. It does not rule out more sophisticated degree or continuation methods.
- The harmonic coordinates satisfy all three neighbor-mean equations. Their exact area pattern is unequal. The maximum-principle uniqueness argument is valid because every interior component connects to the fixed boundary. This only refutes the unmodified equal-neighbor choice; it is not a disproof of adjustable positive weights.
- The prescribed weighted octahedron assignment has positive entries summing to one. The three boundary equations, both product equations, the remaining equation, and the polynomial elimination are independently derived from the original area determinants. The final polynomial is `2*(11*b-5)^2+1`, strictly positive over the reals. There was no illicit division by b or L-b. The obstruction is valid and credited to the existing Firsching/Ringel line; its stellated equal-area relative has separating triangles and cannot answer the 4-connected question negatively.
- Reflection sends the split r,s to s,r with the stated reversal of cycle labels. Thus precisely one reflection-equivariant equal-area drawing exists for odd m and none for even m. The latter still have m-2 nonsymmetric drawings. The octahedral average retains an embedding but loses equal areas. This defeats the proposed symmetric ansatz and naive averaging, not arbitrary asymmetric variational methods.

The five sections are substantive scoped approaches. They do not give five proofs of the universal conjecture, and computation/source review are not counted as additional author approaches.

## 3. Independent verification and adversarial findings

The frozen author's entire harness reproduces its recorded result: 56,815 exact checks, 77 family drawings, 1,036 connectivity deletion controls, 20 rejected integrity-mutation runs, and 16 rejected semantic-mutation runs. Normal, optimized, and relocated outputs match. These advertised checks are genuine; they simply do not exhaust all possible corruptions.

The independent checker imports no author module. It reconstructs the abstract graph and oriented face list, checks exact fixed exterior coordinates and vertex labels, vertex distinctness and strict containment, face-edge incidences, positive and equal oriented areas, Euler counts, and **every pair of edges**, including incident overlapping edges. Its segment test uses exact intersection parameters, unlike the author's orientation-sign implementation. It tests all splits for m=4,...,24 plus nine stress cases at m=37,64,101, totaling 261 drawings. It also checks all candidate labels and reflection behavior in the exhaustive range. Fourteen direct bad-geometry and intersection controls ensure geometric gates are exercised.

Formal polynomial checks cover the infinite family and octahedral identities. Their inequalities and global geometric implications are justified by the written argument; finite sampling is not presented as an all-graph theorem. Final exact counts, normal/optimized/relocated equality, and independent mutation results appear in `RESULTS.json` and `CHECKS.json`.

### Finding V1: fixed exterior coordinates were not checked at runtime

Severity: verification coverage gap; no defect in the frozen coordinates or proof.

In a temporary copy, add the vector (1/1000,-1/500) to **all** vertices returned by `family`, then regenerate that copy's manifest. Every original author mathematical check still passes, in both Python modes, even though C,E,A have moved. The translation commutes with the selected reflection, preserves determinants, preserves the midpoint condition, and is small enough that the tested interior vertices still meet the old absolute containment inequalities. The author checker excludes the three exterior labels from those inequalities but never compares their coordinates to the prescribed values.

The untouched archive hash would of course detect this source edit; the regenerated manifest intentionally bypasses integrity to test semantic coverage. The independent validator rejects this translated drawing explicitly. The separate patch adds one fixed-coordinate check per geometric validation. No change to any actual theorem or witness is needed.

### Finding V2: a special filesystem node escaped recursive inventory

Severity: low-level inventory hardening gap; no nonregular member is present in the delivered ZIP.

An added unlisted FIFO is neither a regular file nor a directory and is not a symlink. The original inventory loop silently ignores it, so both normal and optimized author runs pass. The independent gate uses `lstat` and rejects all nonregular members. The separate patch adds an analogous rejection before the author's file/directory handling. The test never reads from the FIFO.

The harness reproduces both original acceptances and the patched rejections in both modes. It also reruns the author's complete original regression harness with the patch applied only to a temporary copy. The corrected baseline count is 56,896: one new fixed-coordinate check at each of 81 geometry calls. This is a separate hardened result, not a retroactive change to the frozen author's 56,815 count.

### Integrity limits

The top-level mandatory manifest covers all other packet files recursively, including the inner author manifest; unlisted directories, files, symlinks, and nonregular nodes are rejected. The outer ZIP hash in the receipt authenticates the manifest itself. A fully malicious party able to replace both checker and trusted receipt is outside what self-contained hash checks can protect against. Corruption tests are targeted controls, not a proof of complete software correctness.

## 4. Sources and current prior-work boundary

The original source is [Ziegler's Problem 2, OWR 12/2006](https://ems.press/journals/owr/articles/1194), printed p.692, PDF page index 39. This page was independently rendered and visually inspected as well as read as text. Its hypotheses match the imported target: fixed outer face, 4-connected plane triangulation, straight edges, equal bounded triangle areas. The adjacent Whiteley discussion is generic local rigidity and explicitly contains the midpoint quadratic observation; it does not establish global equal-area existence. The four supplied public PDF hashes and sizes were rechecked. Live opening of the numeric UnsolvedMath page failed, so no live target text is claimed.

[Firsching's dissertation](https://refubium.fu-berlin.de/bitstream/handle/fub188/7447/FirschingDiss.pdf?isAllowed=y&save=y&sequence=1), Proposition 45 and Theorems 50-52 with Conjecture 53, was independently checked. Theorem 50 is the exact result through 11 vertices. Theorems 51 and 52 have numerical-error conclusions for 12 and 13-15, respectively. His [current project page](https://firsching.ch/equiarea) labels solutions through 12 as exact algebraic and those for 13-15 as numerical. Neither review independently audits that coordinate dataset, so the website claim is not silently promoted to a verified additional theorem here.

Kleist's [2018 prescribed-face-area paper](https://doi.org/10.20382/jocg.v9i1a9) distinguishes equiareal drawings from area universality. The [accordion manuscript](https://arxiv.org/abs/1808.10864), its definition and Theorem 2, supports the odd-m consequence and Ringel credit in the author packet. One bibliographic enrichment is available: the publisher confirms a [GD 2018 proceedings chapter](https://link.springer.com/chapter/10.1007/978-3-030-04414-5_23), LNCS 11282, pp.333-346, first online 18 December 2018. The author-hosted manuscript was inspected for the mathematics; the subscription chapter's full text was not obtained. Describing the inspected source as an author manuscript is not a mathematical error, but future bibliographies can include this verified publication metadata.

Fresh searches for the target's exact wording, 4-connected equiareal triangulations, accordion/bipyramid terminology, and recent-year variants located no later universal resolution. This is a bounded negative search as of 6 October 2026, not a certified statement that no solution exists. Broader area-universality results concern a stronger quantifier over face areas and cannot be substituted for an answer to equal-area existence.

Read-only searches of AlecKriebel/Math by exact target ID and catalog number found no matching earlier code or PR investigation; exact-ID branch search also returned none. Exact-title code search and a paginated broader branch search found no matching attempt. Broader equal-area PR results were unrelated. Local target-named artifacts were the present author/audit packets. This is bounded prior-artifact evidence, not an exhaustive search of every historical commit or unindexed branch. Generic queue and desk-review rows are not counted as actual prior proof attempts.

## 5. Accepted disposition and use

Accepted original-problem disposition: **unsolved; 5/5 substantive author approaches used**. Accepted mathematical partial: the full cycle-bipyramid classification and the four precisely scoped route obstructions. No historical priority, general-graph solution, arbitrary weighted realizability, noncollinear general-position drawing, or human-peer-review status is asserted.

Use the top-level checker and retain this report with the author packet. If the optional verifier patch is adopted in a successor version, keep the original freeze, produce new versioned checks and manifest, and label the new 56,896 baseline separately. The audit archive contains only authored proofs, code, results, hashes, public source metadata, and this report; no primary PDF, source extract/image, complete corpus record, dataset contents, or private coordination material is included.
