# Independent audit: connected-sum triangulation complexity

Problem 30002054 / OWR-11786-002. Audit date: 2026-10-06.

## Verdict

**Accept the corrected derivative as rigorous partial results and a scope correction. The intended closed-manifold / boundary-connected-sum additivity problem is unresolved by this work.**

The immutable author archive has SHA-256 `b61e853074b015a1b3c3723aed57d6055586e18a64522e1a6b376c8c38a697c2` and 12,848 bytes. All six members match the separately pinned manifest. The author code and external bootstrap were read in full before execution. The original archive and original authored directory were not edited.

A narrow proof correction makes local-flatness hypotheses explicit in the broad TOP category, separates TOP and PL minimization domains, explains minimum attainment, and proves the multi-puncture upper bound directly by disjoint inner facets. This repairs a justification gap; this audit does not exhibit a counterexample to the original unrestricted facet-gluing assertion. The accepted formulas and unresolved target are unchanged. The correction is a repair within the existing capping/puncture route, not a fifth research approach.

No publication was performed. Neither archive contains downloaded papers, extracted paper text, source screenshots, corpus records, or private coordination material.

## 1. Exact target and source reconciliation

The complete problem record, rather than its shortened catalog entry, was matched to problem ID 30002054. Its statement digest is `7afe3d7f0897a40b66249a86417b769aa38eaccb6667f4188fe1d4d7f249c780`. The complete-record/review serialization reproduces `7b51cc30f3ddd65bc242771e59fe8e42c1e061ed23bfd2bdf855c65f463d4909` using default Python `json.dumps([record, reports.get(problem_number,{})], sort_keys=True).encode()`. The report lookup is empty, as expected. The catalog match is unique and has rank 838. Dataset hashes and byte counts are in `SOURCE_CHECKS.json`; no dataset contents are included.

The primary [2012 report](https://ems.press/content/serial-article-files/46393), printed pp. 1427-1429, distinguishes genuine simplicial complexes from semi-simplicial face-pairing objects. The displayed minimum on p. 1429 is over the genuine simplicial class. Its puncture dimension is typographically inconsistent with the surrounding dimension convention: an ambient n-manifold requires an n-ball, where n=d-1. The final additivity question follows its closed-manifold discussion. The same page reports the boundary lower bound attributed to Kalai.

The [2011 report](https://ems.press/content/serial-article-files/46323), pp. 411-412, records the three-dimensional puncture shift of four, asks explicitly about boundary connected sum, and states the nonnegative higher-dimensional boundary invariant. The source therefore supports distinguishing interior sum from boundary sum rather than reporting the two-ball example as a resolution of the intended question.

[Lutz-Sulanke-Swartz](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v16i2r13/pdf/) begins with compact boundaryless 3-manifolds. Its pp. 7-8 give the closed g2 gluing identity, subadditivity in Lemma 9, and additivity as Conjecture 11. Its special sharp families do not establish general additivity.

The sources were freshly opened through their public URLs. Hashes of the retained PDFs were independently computed; the key pages of the pinned PDFs were independently rendered and visually inspected. Web screenshot retrieval failed for the two OWR PDFs, so local rendering of their hash-verified PDF bytes was used. No source image or source text is included in the public packages. A bounded current search did not locate a general resolution; that is not an exhaustive openness or novelty claim.

## 2. Definitions, categories, and existence

For n=d-1 >= 3, with v vertices, e edges and i interior vertices,

    gamma(Delta) = e - n v + C(n+1,2) - i.
    g2(K) = e - (n+1)v + C(n+2,2).

The h-vector definition gives h2=e-nv+C(n+1,2). The other identity can also be checked without a manifold-recognition algorithm: expanding h_(d-1)+d h_d gives the sum over vertices of `(-1)^d` times the reduced Euler characteristic of the vertex link. Each interior link is a homology (d-2)-sphere and contributes one; each boundary link is homologically a ball and contributes zero. Thus h_(d-1)+d h_d=i in the stated manifold domain.

A finite simplicial triangulation is required. Pseudotriangulations, minimum-vertex complexity, minimum-facet complexity, and Matveev complexity are different invariants. No equality between them is used.

Triangulability in the selected category makes the minimization set nonempty. The boundary lower bound reported by the OWR sources makes the integer-valued gamma set bounded below, so its infimum is a minimum. For the punctured manifolds actually used in the principal result, existence is established independently by the cap bound and explicit construction below.

For closed K, [Novik-Swartz, Theorem 5.2](https://sites.math.washington.edu/~novik/publications/socle.pdf) supplies g2 >= C(n+2,2) beta1 for connected orientable homology n-manifolds, n>=3. The positive-characteristic extension is explicitly addressed in the proof. Taking an infinite characteristic-two field, for example F2(t), covers nonorientable topological manifolds as well. This supplies g2>=0 and attainment of G(N). No equality-case classification is needed.

TOP minima range over finite simplicial triangulations of a fixed topological manifold. PL minima range over compatible PL triangulations of a fixed PL manifold. A topological triangulation is not silently treated as combinatorial or PL, and the two minima are not identified.

## 3. Caps and the exact puncture formula

Let N_b be a closed connected n-manifold N with b>=1 standard disjoint open n-balls removed. Each boundary component is an (n-1)-sphere. Cone each component using its own new vertex. Cone realizations are balls, and collars supply the manifold gluing. In the PL version the spheres and collars are PL. The cap gluing recovers N: a sphere boundary identification extends across a ball in the relevant category.

There are v-i boundary vertices and b cap vertices, hence

    f0(K)=v+b,   f1(K)=e+v-i,
    g2(K)=gamma(Delta)-(n+1)(b-1).

Therefore every triangulation satisfies gamma(Delta)>=G(N)+(n+1)(b-1). The distinct-apex condition matters: collapsing all apices into one can create a singular vertex, invalidating this application of the closed-manifold theorem.

For the upper bound, begin with a G-minimizer. A stellar subdivision of a top facet adds one vertex and n+1 edges and leaves g2 unchanged. Carry out n+1 nested facet subdivisions, omitting a different original vertex at each step. The retained facet uses entirely new vertices and lies strictly inside the original affine facet. It is a standard locally flat ball in a Euclidean chart, including when the ambient triangulation is not PL.

The corrected argument repeats this procedure in unprotected facets until b protected facets have pairwise disjoint vertex sets. Each new protected facet uses newly created vertices, so it is disjoint from all earlier ones; every subdivision increases the supply of unprotected facets. Removing all their interiors preserves v and e, creates exactly b(n+1) boundary vertices, and yields

    gamma = g2 + (n+1)(b-1).

The universal lower bound and explicit upper bound coincide:

    Gamma(N_b)=G(N)+(n+1)(b-1).

The independent diagnostic verifies strict positive barycentric coordinates using exact rational arithmetic, simultaneous disjoint punctures, and the corresponding counts on simplex-boundary and cross-polytope spheres. This checks the finite construction and does not substitute for the general topological argument.

## 4. Cylinder, gluing, and the literal scope counterexample

The staircase triangulation of the boundary of an n-simplex times an interval has 2(n+1) vertices, 3C(n+1,2)+(n+1) edges, and no interior vertices. Thus gamma=n+1. Separately capping both boundary components yields a sphere with g2=0, proving minimality.

Consequently Gamma(B^n)=0 and Gamma(S^(n-1) x I)=n+1. The standard interior sum of two balls is the latter cylinder, so the broadened interior-sum reading for arbitrary bounded manifolds is false. Boundary-summing two balls yields a ball. The example does not refute the intended closed or boundary-sum conjecture.

A boundary-facet identification removes n vertices and C(n,2) edges from the sum of the two disjoint counts. Every glued vertex remains on the boundary, so i is additive and gamma is exactly additive for this fixed construction. In the TOP category the selected disk must be locally flat in the boundary to identify the quotient with standard boundary connected sum. The correction states this condition explicitly and does not infer topology from face counts. It proves the usual upper bound directly for PL triangulations, or for TOP minimizers with such gluing disks; no unrestricted TOP facet-gluing assertion is required for the main puncture theorem.

For closed sum, the correction first prepares locally flat inner facets without changing either g2. Identifying n+1 vertices and C(n+1,2) edges and removing facet interiors then gives the sum of the two g2 values. Hence G(N1#N2)<=G(N1)+G(N2) in each consistently chosen category.

The formulas for interior sums of punctured closed manifolds and boundary sums follow by counting the surviving boundary components. The former has b1+b2 components and carries an extra n+1 in its defect relative to the closed defect; the latter has b1+b2-1 and has exactly the closed defect. Standard gluing choices, and orientation-reversing identifications when appropriate, are retained.

## 5. Separator defect and the unrepaired gap

Suppose the separating simplicial sphere S is locally flat, the complementary subcomplexes intersect exactly in S, and their caps realize the proposed factors. With s=f0(S), t=f1(S), the two caps have total vertex count f0(K)+s+2 and edge count f1(K)+t+2s. Therefore

    g2(K1)+g2(K2)=g2(K)+g2(S)+s-(n+1).

For n=3, the sphere's Euler relation gives g2(S)=0 and defect s-4. For n>=4, the sphere lower bound gives g2(S)>=0, while s>=n+1. The minimal simplex-boundary separator has zero defect. Independently checked cross-polytope separators test positive g2 as well as stacked examples.

A minimizing triangulation containing a separating missing facet with the stated topology and factor-identification hypotheses would yield equality. No argument establishes the existence of such a minimizing triangulation. Neither a prime decomposition nor an uncontrolled subdivision supplies the missing zero-defect separator. This is why the general reverse inequality remains unsupported.

## 6. Code and packaging acceptance

The author checker is a finite enumerator of examples, h-values, mod-two homology, and selected vertex links. It does not identify arbitrary manifolds. Its explicit `require` checks survive optimization. Its exact-face and GF(2) calculations were reviewed, including that the selected boundary-link tests are only used on all-boundary-vertex product examples.

The independent checker imports no author code. It adds cross-polytope examples with positive g2, simultaneous protected-facet punctures, exact barycentric-coordinate checks, independent set-based GF(2) elimination, and separator and cap algebra. It passes 1,377 checks identically with and without optimization. The author checker passes its reported 914 checks in both forms.

Thirty controls are run against each archive: isolated and optimized replay, relocation, import-shadow files, caches, extra directories, missing and modified members, replacement entrypoint, symlink and FIFO members, bad roots, changed and symlinked manifests, missing isolation/site flags, and hostile cwd/PYTHONPATH. All expected positive and negative outcomes pass, including a second run of each
30-control suite under an optimized outer harness (120 controls total). The exact
three-file correction patch applies with zero fuzz to a fresh immutable extraction and reproduces every corrected member byte-for-byte. The author checker itself is unchanged.

The trusted external bootstrap pins its manifest and checks the complete inventory before invoking the package entrypoint with -I -S. Direct execution of an unchecked package is not the trust boundary. Hash checks assume trusted bootstrap bytes and no concurrent hostile filesystem replacement; this is not a claim of an OS-level sandbox or race-proof verifier.

## Deliverables and stopping point

`CORRECTION.patch` is the actual applied correction. `ACCEPTANCE.json` records replay results. `SOURCE_CHECKS.json` records public verification metadata. `INDEPENDENT_DIAGNOSTICS.json` and the two diagnostic/replay scripts make the tested scope explicit. The corrected package retains the original author's validation file as historical author-side evidence; the companion independent acceptance report is authoritative for this audit.

The result remains four research approaches, rigorous normalization partial results, and an unresolved intended additivity target. No full proof, no intended-conjecture disproof, no novelty claim, and no publication are represented.
