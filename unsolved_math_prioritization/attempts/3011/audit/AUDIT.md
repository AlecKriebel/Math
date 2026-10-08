# Publication adaptation of the independent acceptance audit

The mathematical review below is unchanged. One packaging paragraph in the correction-provenance section is updated to identify the omitted rejected baseline and the narrower public-only replay. Historical execution and source-inspection claims describe the original audit, not fresh actions by the publication verifier.

# Independent acceptance audit: KP-5.4 / 3011

Audit date: 2026-10-08. Queue rank supplied for identification: 1056.

## Decision

**Accept as rigorously scoped partial mathematical work, with reproducibility and source-provenance limits below. The compact-manifold ANR problem is unresolved.** All five recorded approaches remain unsuccessful at resolving that problem. Neither the noncompact counterexample nor failure of the canonical interpolation changes this verdict. No new correction to the frozen mathematical text is required by this audit.

This was a second, independent review of the complete frozen report, extension note, checker, correction record, source manifest and verification claims. The earlier adversarial review was also read, but its verdict was not substituted for the present proof checks or executions. Frozen originals were not edited. No publication or queue changes were made.

The accepted input is the 10-file `frozen_v1` packet. Its original source-free ZIP is 34,103 bytes, SHA-256 `fec983f5339c26f18fdd4d7c9a9093f3255f445be051d68f2aded29b5a8536db`. In particular:

- REPORT.md: 25,883 bytes; `d57de7c98d615a70fea2bfd3e6b5a338ac83e497adede77034b85e78a3de610f`
- PARAMETRIC_EXTENSION.md: 17,261 bytes; `3aca28813feb496f55b238c1d1feccf3f9de044d213225f24b63554f12973e91`
- check_formulas.py: 11,887 bytes; `007d654317303a7817f72c04de6a9484e67b10a34f87ffc9b93d57d637b0aefb`

Every original file and ZIP member matches its declared byte count and SHA-256. The ZIP has exactly the expected ten members and passes its CRC check. It contains authored mathematics, code, correction metadata and public bibliographic metadata; no PDF or copied source-document body is included.

## Independent mathematical review

### 1. Topology and ambient retraction route

For compact metric M, uniform convergence to a homeomorphism implies uniform convergence of inverses by the modulus of continuity of that limiting inverse. Thus the forward metric and the maximum forward/inverse metric D induce the same topology. Completeness is valid for D, not assumed for the forward metric. The inverse-pair graph is closed, because forward and inverse limits remain inverse under uniform convergence on a compact domain. Boundary fixing is closed. The stated convex pair ambient space is an AR by the standard convex extension theorem.

The direct extension into the increasing interval group is valid: locally finite convex combinations preserve strict increase, endpoints and surjectivity. The nearby-anchor estimate proves continuity at the original closed set even with unbounded partition multiplicity. In n >= 2, tapered radius-preserving half-turns give arbitrarily small boundary-fixed homeomorphisms whose affine midpoint with the identity collapses an interval. This defeats the affine construction, not arbitrary nonlinear retractions.

### 2. Alexander contraction and ordered interpolation

The corrected domain 0 < t <= 1, with t = 0 separate, is essential and sufficient. Shrinking is a homomorphism because the inner disk is preserved; its semigroup law, inverse formula and exact metric scaling follow directly. Extension of h(x)-x by zero handles the moving gluing boundary, and the uniform 2t bound handles t = 0. The equiconnection estimate uses right invariance of the forward metric, not an unjustified bi-invariance claim for D.

The recursion is jointly continuous at a vanishing tail: its distance from the first vertex is at most twice the tail weight. Deleting zero-weight vertices preserves the answer. Induction gives the bound (2m+1) times the maximum vertex distance from a chosen center.

The ordered factorization is correct in the noncommutative group. Applying the outer shrinking to the normalized tail multiplies every tail scale by the same factor; it does not reverse factors or commute them. For m = 2 the factors expand in the order

    alpha(S2,h2) alpha(S2,h1)^(-1) alpha(S1,h1)
    alpha(S1,h0)^(-1) h0.

This agrees with E2 E1 E0, and continuity extends the identity to faces. As a genuinely separate finite check, the accompanying independent program implements actual rational piecewise-linear interval homeomorphisms and composition, without importing the original checker. It verifies 400 group/scale cases and 29 simplex cases in each Python mode, including 17 zero-face cases. Reversing the factor order changes the actual resulting map in 22 cases. This strengthens the symbolic-order check without pretending to prove all group identities computationally.

For bounded-multiplicity parameter covers, the anchor estimates are correct: every active anchor lies within 4 rho(y,a) of a. A uniform bound m+1 on active coordinates combines with the fixed factor 2m+1 to prove continuity at A. Off A, local finiteness plus face compatibility suffices. The covering-dimension corollary uses the standard bounded-order refinement theorem for metric spaces; the core extension lemma explicitly assumes that cover property. No forward-metric completeness is used.

The radial-twist obstruction is valid for every n >= 2. Its two interior radial nodes are strictly ordered, the angle functions stay in the prescribed interval, and radius preservation gives inverse control as well as forward control. At radius 1/4 each nontrivial factor adds pi/N, so N factors rotate through pi and displace the chosen point by exactly 1/2. The vertices are within pi/(2N) of the identity for D defined as a maximum. Hence m/pi <= A_m <= 2m+1 for positive m; these are growth bounds, not optimal constants. The compact shrinking-simplex parameter space is a valid metric compactum, its vertex set plus limit point is closed, and the prescribed boundary map is continuous while this canonical extension is not.

The replacement uniform-smallness property in Section 6 really is sufficient for extension over every metrizable parameter space. It is not proved to exist and is not asserted to be necessary in that exact global format. Failure of the present construction, even in the already-solved spatial dimension two, cannot imply non-ANR.

### 3. Conditional fragmentation

The finite-product/local-section argument is correct with the stated subgroup topologies. Extending each component over a neighborhood, intersecting finitely many neighborhoods, multiplying, and restricting to the inverse image of U gives the promised neighborhood extension. Equivalently, multiplication and its section make U a retract of an open subset of a finite ANR product. Neither argument mistakes a continuous image for a retract.

The continuous factor maps and ANR status of the disk factors remain hypotheses. Individual isotopy factorizations alone do not supply them. Boundary-adapted factors are still needed for manifolds with boundary. The disk/boundary decomposition in the extension note is a homeomorphism of spaces using the conical section, not a direct-product assertion about the group law.

The separability restriction matches the Hanner source category. More precisely, Hanner declares all spaces separable metrizable, including ambient spaces. Inspection of his proof shows that the use of separability in this local-to-global argument is the countable cover of the target; the two-open-set gluing and disjoint-union retraction steps work for arbitrary metric ambient spaces. With the local pieces already ANEs for arbitrary metrizable parameters, the application in this packet is legitimate. The modern ANR/ANE equivalence remains a standard foundational dependency.

### 4. Hilbert-cube stabilization

Reindexing identifies I^n x Q with Q. The product subgroup is closed: both a limit and its inverse have the asserted coordinate independence, preserve the Q-coordinate, and retain boundary fixing. A neighborhood retraction would transfer ANR to the disk group, but none is constructed. The tapered rotation mixing a base coordinate with one cube coordinate is a homeomorphism, tends uniformly to the identity with its inverse, and collapses an interval under slice projection. Thus raw slice projection fails in every identity neighborhood.

### 5. Hilbert-cube embedding and Baire obstruction

The cube fiber formula has derivative at least 1/2 and fixes every boundary face. The center detects its parameter. Disjoint shrinking cubes support a continuous Q-family: the tail displacement of each map and its inverse is bounded by the largest remaining cube diameter. Compactness of Q and Hausdorffness of the group give an embedding into any prescribed identity neighborhood.

If such a neighborhood were a countable union of finite-dimensional compact sets, intersecting with this Q would cover Q by closed finite-dimensional sets. Any one with nonempty interior would contain closed cubes of arbitrarily high dimension, contradicting monotonicity of covering dimension on closed subspaces. Baire then contradicts the cover. There is no need for a common dimension bound. This is a failure of the proposed exhaustion criterion, including for the known low-dimensional AR examples.

### 6. Noncompact scope check

The escaping-twist construction is valid for the stated connected orientable surface. A compact dual curve certifies the nonzero homology class; a Dehn transvection changes homology and therefore cannot be homotopic to the identity. Escaping supports give compact-open convergence to the identity. Local compactness makes a continuous path of homeomorphisms a jointly continuous homotopy. Consequently the full group cannot be locally path connected. Projection and section preserve the homology obstruction on S x S^(n-2), so the extension to n >= 3 is correct.

This is explicitly a known Edwards–Kirby phenomenon. It does not address compact manifolds, a different noncompact topology, or the identity component considered by itself.

## Primary-source scope and status

The eight available local PDFs were independently rehashed; all declared sizes and hashes match. This is verification of existing bytes, **not a claim of eight fresh downloads or independent authentication of the author's historical retrieval sequence**. The source-free receipt records that distinction. Public web pages and the K3 PDF endpoint were also reopened during this audit; web-tool viewing did not supply a separately hashed network download.

- [K3, April 2026 preliminary version](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf): printed p. 304 was inspected in extracted text and rendered pixels. The higher-dimensional question remains listed as unknown. Its short formulation leaves compactness/topology implicit. The preliminary publication status is preserved; this is not described as a final AMS publication.
- [Edwards–Kirby](https://www.maths.gla.ac.uk/~mpowell/Edwards%20Kirby.pdf): Corollary 1.1 requires compact M. The inspected p. 77, also checked in rendered pixels, expressly discusses the escaping torus/twist obstruction and separately states Corollary 6.1 for interiors of compact manifolds. These are local-contractibility results. This source prevents silently using the unrestricted wording as a new solution.
- [Ferry's notes](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/ferrygt.pdf), Question 13.10, p. 90: the compact question and relative-disk reduction are supported. The notes are historical, and do not authenticate current status or replace a verified continuous-fragmentation theorem.
- [Dijkstra](https://www.cs.vu.nl/~dijkstra/research/papers/2005compactopen.pdf): all three pages were read. The historical higher-dimensional relative-cube AR gap and the compact-open group-topology distinctions are accurately used. Its date is 2005, not a 2026 result.
- [Yagasaki](https://arxiv.org/abs/math/0010223): Theorem 1.1, Corollary 1.1, Fact 2.1, the definitions, and the ANR portion of Section 4 were inspected. The noncompact hypotheses concern a connected separable surface and the identity component; the relative version fixes a compact subpolyhedron. This is not an ANR theorem for every full noncompact surface group.
- [Ferry 1977](https://annals.math.princeton.edu/1977/106-1/p07): the publisher abstract was independently reopened and confirms the compact Hilbert-cube-manifold input. The full original proof is not independently reconstructed here.
- [Hanner](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/hanner.pdf): the category convention and Theorems 3.2–3.3 with proof on pp. 392–394 were read. The conditional application is sound with the qualification explained above.
- [Cauty 2005](https://www.math.bas.bg/serdica/2005/2005-309-354.pdf): abstract and introduction support the distinction between algebraic ANRs and topological ANRs, and record metric linear non-AR examples. Cauty's 1994 original construction is not reconstructed here; its EuDML page returned HTTP 403 in this independent pass.
- Mason 1971, Luke–Mason 1972 and Haver 1973 remain external dependencies at the inspection depth disclosed by the author. No original full proof was obtained in this audit. The first two low-dimensional conclusions are corroborated by the inspected primary K3/Yagasaki statements; no positive ANR conclusion here depends on applying Haver's theorem.

A bounded independent web search used the phrases “homeomorphism group manifold ANR 2026”, “homeomorphism group manifold absolute neighborhood retract higher dimensions open”, and exact 2025/2026 variants. No verified later general resolution was found. That negative outcome is neither exhaustive nor evidence against unindexed or unpublished results. The primary dated status evidence remains K3, April 2026.

## Program and reproducibility audit

The complete original checker and both author-side preparation programs were read. Only the checker was rerun directly; the preparation programs intentionally refuse an existing frozen tree or trial tree, and rerunning them would be inappropriate. The independent harness reproduced their pertinent checks without changing the input.

The checker has no Python assert nodes, external dependencies beyond the standard library, subprocess/network calls, or default file output. Its explicit output write occurs only after the mathematical checks, and rejects a resolved destination inside its own packet. The non-root and read-only guards remain ordinary require/raise branches under optimization. These are finite test helpers rather than a fully validated general-purpose PL or matrix API; malformed arbitrary inputs outside the generated test domains are not broadly certified.

The independent receipt preserves full stdout and stderr for 49 subprocess executions, with only workspace path prefixes normalized to stable labels:

- Original frozen checker and separately copied read-only checker: normal, -O and -OO, UID 1000, Python 3.12.14
- Actual create-file, open-existing-file-for-write and mkdir probes: all three operations denied with EACCES in each mode on the read-only copy
- Explicit external output succeeds; an internal output request is rejected; the writable-tree guard rejects its writable control, all in each mode
- Nine semantic mutants are rejected in all three modes: non-strict inverse acceptance, incorrect Alexander scaling, identity substituted for quarter-turn, trivialized homology twist, damaged boundary formula, reversed factor order, retained zero-scale word symbols, wrong radial sign, and halved radial angle
- Invalid PL-domain, shrinking-parameter, barycentric-total and radial-domain inputs are rejected under every mode
- The correction patch replays exactly with fuzz zero

Each successful original execution reports the full original counts: 1,280 Alexander pair-distance cases, 900 interval-convexity cases, two rotation witnesses, 78 homology twists, 270 cube-family checks, 30 noncommutative symbolic cases and eight radial-amplification cases. These counts match the freeze receipt. Both original and copied packet inventories remain unchanged after all runs. The separate actual-map PL program also passes normal/-O/-OO with the counts above.

These executions establish finite consistency, active checks and actual read-only behavior. They cannot establish ANR/non-ANR, every homeomorphism, arbitrary parameter-space extension, novelty, or comprehensive literature coverage.

## Correction provenance and remaining limits

The supplied reconstructed baseline has SHA-256 `c88e169dbdca92b29a5508d04bb4939cd418c04b2bfa6e38e6aff8be03a72f5c`. Applying the pinned patch with fuzz zero reproduces the frozen report exactly. This proves a reproducible relation between those bytes. It does **not** authenticate that baseline as the live historical pre-edit file, and no such claim is accepted.

Publication-slice qualification: the reconstructed full baseline is omitted here because it contains rejected superseded statements. Removed lines in the authored correction patch remain explicitly rejected. The corrected report and extension note are controlling. The historical audit above did check the patch against the reconstructed baseline; the new public-only verifier does not replay that omitted baseline or assert that this slice is the complete original audit package. It reruns all included mathematical programs, public input guards, semantic mutants, CLI branches and physical read-only checks. Fresh source retrieval, source inspection and PDF-byte bindings are NOT_RUN.

The substantive open gaps are unchanged: arbitrary metrizable parameter extension in n > 2, or an equivalent actual neighborhood retraction/counterexample; continuous factorization when invoking fragmentation; factor ANR hypotheses; and boundary localization when relevant. No further mathematical attempt is counted for tests, source retrieval or this audit.

**Final acceptance:** acceptable for reporting and archiving as source-free, non-novelty-claiming partial work with five exhausted routes. It must retain an unresolved compact-core status and all source/provenance qualifications. It is not an acceptance report for a solution of KP-5.4.
