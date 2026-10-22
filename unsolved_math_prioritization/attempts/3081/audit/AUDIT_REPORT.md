# Independent acceptance audit: Monochromatic empty triangles

Problem ID 3081; OPG-2435; queue rank 926. Audit date: 2026-10-06.

## Verdict and exact accepted object

**ACCEPT the unchanged frozen author package for its stated bounded-obstruction conclusions. The original asymptotic conjecture remains unresolved. Two substantive approaches were investigated out of a five-approach ceiling; no new asymptotic lower bound or asymptotic counterexample is established.** No mathematical or packaging repair is required. This audit adds independent verification; it does not silently substitute a corrected author derivative.

The accepted author ZIP is `EMPTY_MONOCHROMATIC_3081_AUTHOR_SAFE_FREEZE.zip`, exactly 15,603 bytes, SHA-256 `0edf7b3e9c4b7cfc72c0f194cc9a62da4ecf6d946b63e7d1b74e6c4afda41fd1`. Its external manifest is exactly 1,917 bytes, SHA-256 `5d974f4db3baa61297b08dfb753550956951b6c983b5cefe937ec6cc8efec885`. Both original files are reproduced byte-for-byte in this audit package. The author ZIP has exactly ten regular, nonencrypted, flat-path members, all matching the external manifest and its nine-entry internal manifest plus the internal manifest itself. There are no duplicate names, traversal paths, source PDFs, source text, raw datasets, or private coordination documents.

This acceptance covers the two obstruction proofs, the finite certificates, source alignment, complete-corpus identity gate, and replay behavior described below. It does not certify novelty, exhaustive literature coverage, correctness of every theorem in cited papers, a future version of any source, or any changed/resealed package.

## 1. Target, definitions, and inherited-work gate

For a finite planar point set P in general position, E_s(P) counts unordered monochromatic vertex triples whose open triangular interior contains exactly s other points of P. All other points count regardless of color. General position excludes boundary points on triangle edges, so this agrees with the Open Problem Garden's closed-convex-hull definition of emptiness after excluding the three vertices. The color classes need not be balanced, and triangles need not be disjoint.

The intended target is the existence of c > 0 and N such that E_0(P) >= c |P|^2 whenever |P| >= N. The literal imported statement omits positivity and the sufficiently-large-size quantifier. The known tiny-set objection is already present in the inherited discussion; it is not a new refutation of the intended problem. The frozen report correctly makes both quantifiers explicit.

The auditor independently read and hashed all three complete supplied corpora, then inspected the complete unique exact-ID record and catalog entry. Verified metadata:

- Catalog: 21,735,099 bytes; 15,458 entries; SHA-256 `891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566`.
- Problems: 68,931,837 bytes; 15,458 entries; SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`.
- Research reports: 80,334,822 bytes; 6,701 entries; SHA-256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.
- Unique exact ID 3081 matches OPG-2435 and rank 926; its research report is absent.
- SHA-256 of the unprojected `[complete_record, {}]` using `json.dumps(..., sort_keys=True).encode()` with default options is `5c2608c784d0abc1d2ec337e74134f071eca944d2e7236eba83923af8c9caa7e`, matching both the gate and catalog review hash.

The inherited material is literature triage and proposed directions, without a completed substantive proof attempt. Author-reported bounded repository searches are not elevated into a proof of absence or novelty. The live aggregator's reported HTTP 403 remains a disclosed author retrieval limitation; the actual Open Problem Garden statement and discussion were independently read. Complete corpus files were also copied into a fresh temporary location and passed the original verifier there in both isolated interpreter modes. No corpus content is included in the safe deliverable.

## 2. Source audit and current-version disambiguation

All eight successfully retrieved source files listed by the author were rehashed independently, including five PDFs and three HTML files. Every byte count and SHA-256 matched. Fresh downloads from the explicit v2 PDF URLs reproduce exactly the author’s unversioned PDF bytes, resolving the version ambiguity. Fresh official unversioned abstract pages also identify v2 as their current versions. Version/date labels were independently checked in PDF text; the almost-empty theorem and remark pages and the many-colors first page were also visually inspected.

1. [Aichholzer et al., Empty Monochromatic Triangles, CCCG 2008](https://cccg.ca/proceedings/2008/paper18.pdf): four pages, 123,429 bytes, SHA-256 `88b1178df4d98d7e993dad0a697f36931a1e5df101475a5dbd708bddead22da7`. The conference paper supplies the 5/4 exponent, discrepancy argument, and quadratic Horton-set special case. The seven-page [2009 author manuscript](https://www.matem.unam.mx/~urrutia/online_papers/Trimono.pdf), 121,986 bytes, SHA-256 `4093e29e3c1185a4ff679f84918ec05790b6bf6c915512ec721ae292099ca333`, was separately inspected; these are not conflated versions.
2. [Pach and Tóth, Monochromatic empty triangles in two-colored point sets, author PDF](https://www.renyi.hu/~pach/publications/emptytriangle102408.pdf): four pages, 121,536 bytes, SHA-256 `1085d7e52d4281e4cfb43f7fb8e5610016d3bdf156d83251ae621ca67e91f0db`. The stated theorem concerns truly empty triangles and exponent 4/3. Its discrepancy lemma agrees with the author report's normalized formula. The published citation is [Discrete Applied Mathematics 161 (2013), 1259–1261](https://doi.org/10.1016/j.dam.2011.08.026).
3. [Bhattacharya et al., On the Number of Almost Empty Monochromatic Triangles, arXiv:2601.18951v2](https://arxiv.org/pdf/2601.18951v2): 17 pages, 429,476 bytes, SHA-256 `384eb73eb7582c524851bb46ea84627bff52ad7bbe9c5d4f7123ee7d5b42b194`; dated 2026-09-11. Theorem 1 allows at most c-1 interior points and is quadratic. Theorem 2 allows at most c-2 and has exponent 4/3. Thus c=2 gives E_0+E_1 quadratic, but only E_0 of order n^(4/3). Remark 1 explicitly leaves improving the truly empty bound open. The star proof in section 2.2 was inspected. The separately pinned author HTML is v1 and is accurately labeled as such; the v2 claims here are supported by the v2 PDF.
4. [Bhattacharya et al., Almost Empty Monochromatic Triangles With Many Colors, arXiv:2609.12325v2](https://arxiv.org/pdf/2609.12325v2): 13 pages, 350,316 bytes, SHA-256 `3cfc47fcd97618e887889301d004ad219741d2bd5e69ae54930c88a974d3b0d6`; dated 2026-09-21. Theorems 1.1 and 1.3 concern allowed-interior-point thresholds and Horton-set existence, respectively. Its introduction still distinguishes the two-color empty 4/3 counting bound. This preprint is not a quadratic solution to the present problem.

The two 2026 papers are treated as preprints; no peer-review status is asserted. Retrieval metadata and bounded inspection history are in `SOURCE_AUDIT.json`. Source bytes and rendered pages remain outside the safe package.

## 3. First approach: discrepancy fan and all-k blocker reuse

### Known bound

Let red and blue class sizes be r >= b. For each red pivot and r >= 3, the remaining red rays have r-1 cyclic angular gaps. At most one gap is at least pi. Each gap smaller than pi determines a red triangle whose interior lies in that gap and contains no other red point. These interiors are disjoint within the pivot's fan. Therefore there are at least r-2 candidate triangles and at most b contain blue points. Summing at least max(r-b-2,0) empty incidences per pivot and dividing by at most three pivots per triangle proves

E_0 >= r max(r-b-2,0)/3.

For r < 3 the asserted lower bound is zero and needs no fan construction. For fixed positive fractional color imbalance the bound is quadratic. For balanced or nearly balanced classes its deficit is real. The independent finite checker also verifies the bound on all 256 colorings of the witness; those finite checks do not prove the general lemma.

### Parametric construction and general position

For integer k >= 1, let a_i=(2i,2i^2), -k <= i <= k, all red, and q=(0,1), blue. Put r=2k+1.

- At a_i the affine tangent expression y-2ix+2i^2 equals zero, while at a_j it equals 2(j-i)^2 > 0 for j != i. Hence every red point is an exposed extreme point, and their cyclic polygon order is increasing i followed by the closing upper edge.
- For i < j < l, the orientation determinant of a_i,a_j,a_l is 4(j-i)(l-i)(l-j), nonzero.
- The line a_i a_j has equation y=(i+j)x-2ij. At q its residual is 1+2ij, an odd nonzero integer. Equivalently orient(a_i,a_j,q)=2(j-i)(1+2ij), nonzero. Thus no red-red-blue triple is collinear; there is only one blue point.
- q has barycentric weights (1/4,1/2,1/4) in a_-1,a_0,a_1. It is strictly inside that triangle and therefore inside the red polygon, for every k >= 1.

The diagonal fan at each red pivot triangulates this convex polygon. Since q lies on no red-pair line, it lies on no fan edge, so exactly one fan face strictly contains it. A single blue point consequently blocks exactly r=2k+1 pivot-face incidences. This is unbounded with k. Reusing a geometric triangle at different pivots is precisely what an incidence count means here; there is no mistaken identification of these incidences with r distinct triangles.

### Exact total triangle counts

Any red triangle containing q must use a_0, because all other red vertices have y >= 2 and q has y=1. Its two other vertices must be on opposite sides of x=0; otherwise q cannot lie strictly inside. Conversely, in a_-i,a_0,a_j, where 1 <= i,j <= k, q has barycentric weights

1/[2i(i+j)], 1-1/(2ij), 1/[2j(i+j)].

These sum to one, are all positive, and give coordinates (0,1). Thus exactly k^2 red triangles contain q. All red points are extreme, so no red point lies inside a red triangle; there cannot be a blue monochromatic triple. Therefore E_1=k^2 and E_0=binom(2k+1,3)-k^2. In particular E_0=(4/3)k^3-k^2-k/3, cubic as k grows. The construction decisively refutes constant blocker capacity for these repeated pivot fans, while leaving the quadratic conjecture untouched. It does not forbid selecting a different controlled family or a different charging scheme.

The independent barycentric implementation checked all triangles and all pivot fans for k=1,...,30; the original implementation checked k=1,...,15. These checks support the explicit all-k argument, rather than replacing it.

## 4. Second approach: balanced local conversion obstruction

The eight original integer-coordinate points and color labels were independently parsed from the pinned certificate. All 56 unordered triple determinants are nonzero; the minimum absolute determinant is 6. The four red and four blue vertices produce exactly binom(4,3)+binom(4,3)=8 monochromatic triples. Independent rational barycentric solutions give precisely these unique interior points:

- (0,3,6) -> 4; (0,3,7) -> 4.
- (0,6,7) -> 2; (3,6,7) -> 2.
- (1,2,4) -> 6; (1,2,5) -> 6.
- (1,4,5) -> 3; (2,4,5) -> 3.

Every stated barycentric coordinate is strictly positive, and every other point was tested and excluded. Full rational weights are in the independent results. Each sole interior point has the opposite color. Thus E_0=0 and E_1=8 exactly. No boundary point or same-color interior point is being ignored.

For any one of these triangles, its three vertices plus its blocker have a single monochromatic triple, namely the nonempty original triple. Inserting the opposite-colored blocker produces three bichromatic triangles. Even access to all eight witness points gives no empty monochromatic replacement. This refutes an unrestricted local rule that always replaces an almost-empty monochromatic triangle with an empty one using only the available local points. It does not give arbitrarily large empty-free sets, does not refute a replacement theorem with additional size or structural hypotheses, and does not establish any asymptotic upper bound.

For independent retention with probability p, a fixed monochromatic triple becomes empty in the retained set exactly when its three vertices survive and its s original interior points do not. Exterior points are irrelevant. Linearity of expectation gives p^3 sum_s (1-p)^s E_s(P). This is a statement about the induced subset, not the original P. At p=1/2, independent enumeration rebuilt the triangles in every one of the 256 subsets of the witness. Empty-count frequencies are 170 subsets with zero, 60 with one, 18 with two, and eight with four; the mean is (60+36+32)/256=1/2. The original E_0 is zero, so the positive expected count cannot itself lower-bound E_0(P).

## 5. Replay, adversarial tests, and trust boundary

`independent_check.py` does not import or execute the author's geometry routines. It uses exact rational solutions of a two-variable linear system, checks strict positivity of all barycentric weights, recomputes subset geometry, and validates the immutable original archive and external manifest before reading its certificate. It has explicit exceptions, no removable validation assertions.

`replay_author.py` extracted the exact original ZIP into fresh temporary directories, changed the working directory, disabled bytecode writing, and ran both `python -I -B` and `python -I -B -O`. A hostile PYTHONPATH and unrelated HOME were supplied and ignored by isolated mode. The complete private corpus and source files were copied to new temporary paths for actual relocated input replay.

There are 38 direct recorded cases: six expected successes and 32 expected failures. Successes cover normal/optimized geometry replay, complete relocated private-input replay, and the original self-test launched under each mode. Each original self-test internally executes 12 additional relocation/tamper cases. Direct failure cases in both modes cover:

- altered, missing, unexpected, hidden, and symlinked members;
- duplicate internal-manifest rows;
- re-sealed false interior, duplicate geometry, collinear geometry, unbalanced colors, false E_0, and wrong claim scope;
- incomplete corpus arguments, mutated complete-corpus bytes, and mutated source bytes;
- a repacked original archive with recomputed external metadata, rejected by immutable trusted pins.

The independent checker also rejects six altered semantic certificates and four boundary-point controls, while accepting a positive interior control. Its normal and optimized full outputs are byte-identical. These negative results were observed from actual executions and explicit nonzero exit statuses; they are not inferred from reading code and cannot disappear with Python optimization.

Internal manifests alone are not authentication against an adversary who rewrites both the checker and manifest. The acceptance boundary is the externally supplied original ZIP and manifest hashes, and separately the final audit ZIP and its external manifest hashes. An edited or repacked archive needs a fresh audit. The safe package contains authored analysis, verification programs, public metadata, and the unchanged safe original packet only. No repository or queue write occurred during this audit.

## 6. Final classification

Accepted: precise local obstructions; complete frozen-object verification; public-source alignment; no repair required.

Remain unresolved: a quadratic lower bound for empty monochromatic triangles, or a subquadratic asymptotic counterexample. Record the work as **unsolved, 2/5 substantive approaches**. Do not label the all-k fan example or the eight-point certificate a solution or asymptotic refutation.
