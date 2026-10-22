# Independent audit: KP-3.11 / ID 2809 / rank 773

## Verdict

**Required literature correction before v2 acceptance. The scoped mathematical propositions pass. The universal maximal-cusp meridian bound remains unresolved, with the original five approaches exhausted (5/5).**

The exact changes are in `REQUIRED_CORRECTIONS.json` (C1). The frozen author record describes a universal good-pair route as merely unproved, although a known obstruction already excludes that route in full generality. This does not invalidate the conditional inequalities, finite-dimensional optimization theorem, numerical non-realization warning, or conditional filling transfer. It does not refute the original meridian conjecture.

This is an independent AI-assisted mathematical and artifact audit, not human peer review, editorial acceptance, formal proof-assistant certification, or a novelty/priority determination. No new proof-search approach, external communication, or remote write was performed.

## Inputs and preservation

- Original ZIP: `KIRBY_MERIDIAN_2809_AUTHOR_SAFE_FREEZE.zip`
- Bytes: 19,953
- SHA-256: `14809993ffccbb97cc3510d7a17df91ad375bc85cf02bd6a9c430c31c12673c3`
- Original manifest SHA-256: `fd2b78b2834c2f97b4c3afa92fe049ba0de7e40bddf16043b6dd5f54cf941688`

All eight archive members match the live author-safe files byte-for-byte. All seven author manifest entries pass length/hash checks. Exact archive membership, CRCs, path names, and non-symlink file types pass. The archive and author files were not edited; all mutation work used temporary copies. The original receipt's ordinary/optimized replay claims and four integrity-mutation claims were independently reproduced.

## Complete mathematical audit

### Marking and credited geometric input

The target is the non-strict bound 4 for the meridian measured on the maximal cusp of a hyperbolic knot in S³. The dataset statement and primary problem agree on this scope. Knot, maximal cusp, meridian, and ambient sphere assumptions cannot be discarded. The printed primary has a harmless “ever”/“every” typographical difference.

A spanning boundary curve meets the meridian once. Orienting its longitude coefficient positively gives L+aM, including for a nonorientable spanning surface. Thus two different coefficients yield determinant magnitude |a-b|A and difference (a-b)M. The boundary orientation does not assert orientability of the surface.

The essential-surface length cap is used as a credited theorem. Its required meaning includes incompressibility and boundary-incompressibility of the appropriate orientable double/regular-neighborhood boundary; the negative Euler characteristic permits pleating. An arbitrary spanning surface is insufficient. A maximal cusp may have tangencies; shrinking or taking the limit handles the boundary convention. These inputs were checked against [Burton–Kalfagianni](https://arxiv.org/pdf/1608.05035v2), Definitions 2.1–2.2, Lemma 2.3, Theorems 2.4 and 4.1. Their underlying geometric results were not independently re-proved.

### Section 1: exceptional filling and crossing threshold

PASS. The strict length>6 hypothesis of [Agol's Theorem 6.2](https://arxiv.org/pdf/math/9906183v2) would force an infinite fundamental group after meridional filling; S³ has trivial group. Shrinking a hypothetically longer-than-six maximal cusp preserves the needed strict inequality. This proves at most 6, without misidentifying the original hyperbolike conclusion.

The crossing-dependent inequality in [Adams et al., Theorem 3.1](https://kisonecat.github.io/research/cusp-size-bounds.pdf), is correctly quoted. Solving 6−7/c≤4 for positive c gives c≤7/2, so integral c≥4 is not covered by this inequality alone. Boundary-compression treatment and the He-surface budget were inspected. No equality-realization inference is made.

### Proposition 2.1 and Corollary 2.2

PASS. From u=L+aM and v=L+bM, the Gram identity gives (u·v)²=|u|²|v|²−n²A². Positive caps and A≥A₀ imply the nonnegative radicand is at most P²Q²−n²A₀². Substituting into |u−v|² establishes exactly the displayed upper bound. Nonzero determinant excludes equality in the difference triangle inequality, giving the strict cap-only bound.

Euclidean sharpness is correctly limited to marked abstract flat tori: vectors with prescribed lengths and nonpositive dot product attain the cap expression; M=(u−v)/n and L=v generate a lattice of area A₀. This supplies no knot or essential surface realization.

The rational comparison requires both the radicand and D_B to be nonnegative before squaring. The weak and strict cases are separated correctly, including R=0 and D_B=0. Inconsistent inputs are not positive certificates; a failed certificate is not evidence that the actual meridian is too long.

The displayed area-aware example has the stated arithmetic. The adequate-diagram specialization uses the published essential state surfaces and intersection 2c; its crossing/Turaev-genus criterion is conditional, not universal. The cap-only strictness is an elementary consequence of noncollinearity and is not presented as a novelty claim.

### Proposition 3.1

PASS for the exact method stated. A feasible signed coefficient vector has equal positive and negative mass T>0. The product coupling has the claimed row/column sums, moment 1, and weighted cost. Pairwise comparison with the minimum ratio, followed by the absolute-value triangle inequality for the moment, gives the lower bound. A minimizing pair attains it, including when other slopes are repeated. Finiteness and positive caps ensure a positive finite minimum when two slopes differ.

The conclusion applies to arbitrary real coefficients and slopes, not just the sampled integers. It excludes improvement by signed linear combinations plus independent caps and the triangle inequality; it does not exclude additional geometric/topological information. Independent LP-dual interval witnesses also support the finite controls.

C1 concerns the surrounding universal-route discussion, not this theorem. The exact primary reference and replacement wording are specified in `REQUIRED_CORRECTIONS.json`; [Burton–Kalfagianni §5](https://arxiv.org/pdf/1608.05035v2#page=16) expressly warns of the obstruction. A bound for knots without distinct essential spanning slopes needs other input.

### Section 4: numerical torus

PASS with the stated non-realization limitation. On the rectangular lattice, p≠0 gives length at least 5; p=0 and q≠0 gives length at least 6/5. This proves the systole globally; the finite square search merely checks examples. The longitude-coefficient-one minimum and all displayed c=8 inequalities are correct. The parameter c has not become a crossing number, and neither hyperbolicity, maximality, an S³ filling, nor a knot cusp is constructed. This is an obstruction to a selected numerical inference only.

### Proposition 5.1 and limit warning

PASS. For L₀>4, convergence supplies a positive margin above 4 on sufficiently late embedded horotori. Enlargement to the one-cusped maximal horocusp cannot decrease the marked length. Hyperbolicity, the S³-knot topology, peripheral meridian identification, and the embedded/convergent horotori are all explicit hypotheses, not established construction outputs.

[Purcell's Theorem 3.4](https://users.monash.edu/~jpurcell/papers/jpurcell-slope.pdf) concerns the knotting-strand cusp of a hyperbolic generalized augmented link. A fixed-parent limiting bound cannot alone control every filling or all parents uniformly. The scalar sequence is a valid counterexample to that inference, not a statement about knot deformations. No long S³-preserving filling sequence for the cited long-slope links has been established here.

## Independent calculations and artifact challenges

`independent_controls.py` was written without importing or executing author code. It reconstructs all **10,768** original-domain checks with exact matching category counts, using its own integer-cap construction, vector arithmetic, transport implementation, and half-gap comparison. Another **3,399** checks cover rational/repeated-slope LP-dual intervals, sharp Pythagorean boundaries, a nonorthogonal equality case, the area example, and inconsistent area caps.

Ordinary and optimized Python produce byte-identical independent results. The author verifier has zero `assert` AST nodes and uses active exceptions. Both author modes reproduce the saved `RESULTS.json` exactly, from unrelated extraction directories.

Four integrity mutations are rejected in both modes: altered proof, unexpected top-level file, removed proof, and altered saved results. Six semantic mutations are also rejected in both modes after recomputing each temporary manifest: omitted sign guard, omitted second-cap square, excess determinant scaling, maximum instead of summed caps, equality mislabeled strict, and an injected impossible runtime check. This tests semantic checks separately from mere hash rejection. It is finite mutation coverage, not exhaustive correctness assurance.

Two nonblocking guard limits are explicit: the author verifier accepts a missing manifest and ignores added nested files. This matches its optional-manifest design, but makes it unsuitable as a mandatory recursive archive validator. The independent exact archive-member checks cover the actual frozen archive; `verify_audit.py` uses a mandatory recursive manifest for this audit packet.

## Sources, datasets, and actual prior-attempt search

`SOURCE_AUDIT.json` gives exact byte counts, SHA-256 hashes, URLs, inspection scope, current-source status checks, and limits. All six author-cited PDFs were independently re-downloaded and exactly matched their claimed hashes and retained bytes. The omitted seventh source was separately retrieved for C1. No source PDF, extract, image, raw dataset, or coordination record is included in this safe packet.

Both complete dataset files were rehashed and matched a freshly fetched repository manifest at the pinned revision. The full selected statement/background was read. The numeric ID occurs once; its statement hash matches the catalog. The full 6,701-entry prior-report dictionary lacks the exact key, rather than containing it with null. The full catalog matches the fresh repository blob identity. No new full-dataset download or successful live-row check is claimed.

Fresh main stayed at 0b27fa5396166e4e9fab43474146bb7fba7973a9. The selected queue row was queued at 0/5 before this investigation. Fresh full state, history, assessment history, related-group data, and the untruncated 62-entry immediate attempts tree had no selected attempt. ID/code/topic PR searches, ID commit search, ID/topic branch searches, and default-branch ID code search found no verified prior attempt. The code search omitted known queue/catalog matches too, so it is weak corroboration only. No verified previous attempt was skipped; deleted/private/unindexed or differently named material is not ruled out.

The bounded literature searches did not locate a full resolution of the original meridian question. They did reveal C1. No exhaustive literature or priority assertion follows, and source search timestamps were not publication dates. The 2024 conference abstract located by the author concerns restricted classes, not a universal theorem. Geometric/computational source ingredients were credited; no SnapPy, Regina, normal-surface, or Görner certificate rerun was performed.

## Acceptance gate and audit log

V2 must preserve the original freeze, implement C1, regenerate affected metadata/manifests, and receive a separate in-context delta review. If verification code changes, its execution and mutation acceptance must be renewed. Until then this audit is **not** acceptance of an amended package. Preserve unresolved 5/5; no solution, knot counterexample, novelty, human-review, or editor-review claim is justified.

- 19:15–19:18 UTC: original freeze, ordinary/optimized replay, primary scope, fresh source hashes, datasets, and repository search checked
- 19:20 UTC: independent 10,768-check reconstruction and 3,399 supplementary checks complete
- 19:21 UTC: archive and semantic-mutation replay complete
- 19:22–19:24 UTC: C1 verified from the omitted primary source and already-cited paper; exact correction gate recorded
- 19:25–19:28 UTC: safe report, metadata, manifest, and relocated audit replays prepared

Audit completion: 100% for this original freeze once its final manifest replay passes. Original universal theorem completion: 0% proved here.
