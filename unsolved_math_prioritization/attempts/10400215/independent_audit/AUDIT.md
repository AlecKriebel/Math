# Independent audit: shadow number and Gromov norm

## Decision and exact object reviewed

**ACCEPT_UNCHANGED_AS_SCOPED_PARTIAL_RESULTS.** Problem 10400215, AMR-103-0215, selection rank 847 remains **unsolved by this attempt, 5/5 approaches**. No mandatory mathematical or executable correction was found. This acceptance is an independent AI audit, not human peer review or proof-assistant certification.

The original nine-file author ZIP is 12,105 bytes, SHA-256 `5662c3bf4ce0dd4760f50a8c41a854f95bb7fbc1d4eacd7e9dadedf653809e66`. Its external manifest and executable bootstrap were read in full, authenticated, and left unchanged. Every source-code file inside the packet was read before isolated execution. The author's generation and validation scripts were also inspected as provenance, but were not trusted as a substitute for independently rebuilding the tests. The original author-freeze pending-review language is historical; this separate acceptance supplies the later review. No correction patch is needed or claimed.

## Identity and source checks

The complete target catalog record, complete problem record, and complete associated research-result record were freshly located in the three authorized full corpora. There was one matching catalog entry and one matching problem entry. The rank, problem number, statement hash, and complete-pair default-JSON hash all match. The review hash is `07ef7ee146a8f5e545bd862d88516628a9d0293df79d6aa517c10f5f5c06e301`. The prior review is a generic literature triage, not a substantive proof attempt. Only hashes, byte counts, match results, and the assessment are retained here; no record contents are redistributed.

Ohtsuki's original printed page 536, PDF page 164, was independently rendered from the matched PDF and visually inspected. The surrounding definition on printed page 535 was inspected in text. The target is Conjecture 12.10, attributed to D. Thurston, concerning ordinary shadow number and simplicial volume with a homogeneous two-sided comparison. It is not a question about the Thurston norm on homology. Neighboring Problem 12.11 is a different shadow-diagram volume question. The verified public description of PR 274 addresses that different problem, ID 10400216; it does not establish an earlier attempt on this target.

All five local source PDFs were independently rehashed, and all sizes and hashes match the author metadata. The Costantino--Thurston v3 and Ishikawa--Koda v1 version headers and relevant theorem texts were inspected. Ishikawa--Koda printed page 40 was independently rendered and visually checked, including the old sufficient cutoff and the cusp-length lemma. Versioned primary URLs were also opened independently. The published Ishikawa--Koda article was not inspected, and numbering in this audit refers to v1. The live catalog page remained unreadable through the independent web request; its failure did not establish a fresh HTTP status code. The author's earlier HTTP 403 report is not relabeled as a new observation.

A fresh bounded repository search returned no exact-target code, PR, branch, or commit hit on the queried surfaces. A fresh bounded literature search located no full resolution. Neither absence establishes completeness, historical novelty, or present global openness. Naoe--Ogawa's 2025 paper studies four-dimensional weighted shadow complexity and trisection genus; it is not evidence resolving this three-dimensional question.

## Mathematical audit

### 1. Domain, complexity, and constants

The accepted domain is compact connected oriented 3-manifolds with empty or torus boundary, with the geometric decomposition assumed in the author text. A cusped hyperbolic piece means its compact core with torus boundary; its Gromov norm is the relative simplicial volume. Write `G` for that norm and `s` for the minimum true-vertex count of an ordinary shadow. This differs from requiring a special shadow, from a branched-shadow minimum, and from any four-dimensional invariant.

Costantino--Thurston Theorem 3.37 gives `a G <= s` with `a = v3/(2 v8)`. For a hyperbolic interior, `Vol = v3 G`, so the same lower bound is `Vol/(2 v8) <= s`. There is no missing factor of two or interchange of ideal tetrahedron and octahedron volumes. Their Theorem 5.5 supplies a uniform positive `C` for `s <= C G^2` in the stated class. The proof uses geometrization, triangulation, and filling inputs; this audit verifies the cited statements and their use, rather than independently reproving those foundational theorems.

Ordinary true-vertex counting is appropriate with toroidal boundary: Ishikawa--Koda Remark 1.1 explicitly relates its counting convention to Costantino--Thurston's. Their branched invariant counts true and boundary vertices. In the long-slope argument the special shadow has no boundary vertices, so its candidate count is exactly `n` for both purposes. The conclusion concerns `s`, `bsc`, and `smc`; it does not identify an unrestricted special-shadow-complexity invariant.

### 2. Decomposition and gluing

Costantino--Thurston Lemma 3.22 gives connected-sum subadditivity. Proposition 3.27 and Corollary 3.28 permit oriented torus reconstruction without increasing the summed vertex count. Their Theorem 5.5 explicitly uses this for JSJ reconstruction. Gluing includes the boundary identifications needed for cycles in the decomposition graph; no unproved shadow-additivity assertion or restriction to a tree of pieces is substituted. Orientations are glued compatibly, equivalently with orientation reversal on the induced boundary orientations. The isolated orientation-preserving word in the v3 Proposition 3.27 statement is not used to contradict its proof and the following corollary.

Nonhyperbolic graph pieces have zero ordinary shadow complexity by Proposition 3.31. Zero-complexity prime contributions remain zero under connected sums. Simplicial volume is additive across the incompressible JSJ tori and connected sums in this setting. Therefore, for hyperbolic-piece norms `g_i`,

    s(M) <= sum_i s(H_i) <= C sum_i g_i^2.

Let `B = max_i g_i`, with `B=0` for an empty hyperbolic list. The difference `B sum_i g_i - sum_i g_i^2` equals `sum_i g_i(B-g_i) >= 0`. This proves the claimed refinement, including the empty and zero-norm cases. In particular `G=0` forces `s=0`. Allowing arbitrary numbers of bounded-volume pieces and arbitrary graph pieces does not change the linear constant `C B`.

For positive total norm, dividing subadditivity by `G` gives a weighted mean of the piece ratios, bounded by their maximum. Hence an unbounded sequence of total ratios contains selected hyperbolic-piece ratios tending to infinity; the credited bound `s(H)/G(H) <= C G(H)` forces their volumes to infinity. This is a necessary condition, not a realized counterexample. The claimed equivalence uses both closed and torus-cusped hyperbolic pieces. A result for closed hyperbolic manifolds alone is not enough for the sufficiency argument as written.

### 3. Fixed families and affine estimates

If `G <= V`, the quadratic estimate yields `s <= C V G`. Simplicial volume cannot increase under torus filling, so the same statement applies to fillings of finitely many fixed parents, subject to the same geometric-domain hypotheses. Exceptional fillings are not discarded; at zero norm their shadow count is zero. Ratios are taken only where `G>0`.

The positive norm gap is valid: `aG>0` makes the nonnegative integral `s` at least one; `s<=C G^2` then implies `G>=1/sqrt(C)`. An assumed affine estimate `s<=A G+D`, with universal nonnegative `A,D`, therefore implies `s<=(A+D sqrt(C))G` for positive norm. The zero-norm case follows separately. This proves equivalence of the proposed affine and homogeneous upper bounds in the stated domain; it proves neither bound exists.

### 4. Long slopes and integrality

Retain a closed oriented manifold, an actual branched special shadow, `n>=1` true vertices, its compatible gleams, and the specific simultaneous cusp neighborhoods in Ishikawa--Koda Lemma 5.3. The slope length is the minimum over all filled region cusps, using their metric and the vertex-passage count with multiplicity. It cannot be substituted by a length on an arbitrarily rescaled horotorus or by a slope on only some cusps. The construction supplies a hyperbolic parent of volume `2 v8 n`; `L>2 pi` places the filling in the stated hyperbolic estimate.

With `f(L)=(1-(2 pi/L)^2)^(3/2)`, Proposition 5.1 and the ordinary-shadow lower bound give

    n f(L) <= Vol(M)/(2 v8) <= s(M) <= n.

Thus a fixed `L0>2 pi` gives `s <= (a/f(L0))G`. This constant is uniform only under that extra cutoff. Existence of a branched special shadow does not imply existence with a uniform positive slope margin for arbitrary manifolds.

For the exact strict threshold, `L>L_*(n)` is equivalent to `f(L)>1-1/n`. Integrality then forces `s=n`. Forgetting branching and the candidate bound give `s<=bsc<=n`, and Theorem 2.2 gives `bsc=smc`, so all three equal `n`. At `n=1`, `L_*(1)=2 pi` and the strict inequality is essential for this argument. At the exact threshold equality the weak volume chain by itself need not exclude `n-1`; the author correctly makes no endpoint assertion.

For the simpler inclusive cutoff `L>=2 pi sqrt(3n/2)`, put `q=(2 pi/L)^2`. Then `0<q<=2/(3n)<1` and

    (1-2/(3n))^3 - (1-1/n)^2 = (9n-8)/(27n^3) > 0.

All quantities square-rooted are nonnegative; taking square roots preserves the strict inequality. This includes `n=1`, where the margin is `1/27`, and `n=2`, where it is `10/216`. The sufficient cutoff itself is strictly above `2 pi` in every allowed case. Its equality case therefore genuinely works. It is smaller than the old convenient `2 pi sqrt(2n)` cutoff. The asymptotic coefficient follows by the derivative of `(1-x)^(2/3)` at zero. This is an algebraic sharpening of credited inputs, not an independently new geometric estimate, a universal existence result, or a claimed optimal cutoff for actual manifolds.

### 5. Routes that do not close the conjecture

The drilled triangulation has a linear volume bound, but the supplied shadow converter has a quadratic tetrahedron bound. Their composition remains quadratic. Dehn filling adds no vertices and does not repair that exponent.

The quantum comparison uses upper bounds on quantum growth from both shadow count and norm. These directions do not upper-bound shadow count by norm. The numerical model `G=m`, `s=m^2`, `Q=m` satisfies those inequalities while its ratio diverges. It is only a logical countermodel; no realization as manifolds is claimed. BDKY's terminology for volume normalization is not imported into the author's definition of `G`.

## Executable verification and its limits

The original archive, manifest, and bootstrap passed fresh exact-byte authentication and strict ZIP inventory checks. Four positive author replays covered extracted and relocated roots, normal and optimized Python, hostile import names in the current directory, and hostile `PYTHONPATH`, startup, and optimization environment values. Their output was byte-identical, with 45,810 controls per replay.

Forty negative probes were actually run and rejected before packet-code execution. They include proof/code mutation, a resealed manifest, missing/extra entries, import-shadow files, cache and nested directories, symlink/FIFO/directory members, symlinked roots and ancestors, wrong or absent roots, entrypoint overrides, invalid manifest types, and missing interpreter restrictions. Altered duplicate-key manifests are rejected by the manifest pin; this test does not pretend to reach the duplicate-key parser through an invalid pin. Sentinels detected no untrusted payload execution.

The separately authored independent checker performs 68,324 exact controls. It covers the empty JSJ list, deficit identities, denominator-cleared cubic rounding, all candidate integers for small `n`, strictly long slopes at `n=1`, varied rational norm-gap/affine cases, and the quantum countermodel. These computations corroborate the written algebra; finite cases do not certify topology or prove the universal conjecture. Both normal and optimized/relocated acceptance replay are required by the separate audit bootstrap and recorded in the external validation receipt.

The boundary is a pinned static artifact verification model. It is not a defense against concurrent hostile filesystem writers, compromised Python, or a malicious trusted bootstrap. No remote publication, commit, push, merge, release, external communication, or new DOI was performed by this audit.

## Public references

- Ohtsuki (editor), Problems on invariants of knots and 3-manifolds: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
- Costantino--Thurston, 3-manifolds efficiently bound 4-manifolds, inspected v3: https://arxiv.org/pdf/math/0506577v3
- Ishikawa--Koda, Stable maps and branched shadows of 3-manifolds, inspected v1: https://arxiv.org/pdf/1403.0596v1
- Belletti--Detcherry--Kalfagianni--Yang, Growth of quantum 6j-symbols and applications to the volume conjecture: https://par.nsf.gov/servlets/purl/10323860
- Naoe--Ogawa, Shadow-complexity and trisection genus: https://afst.centre-mersenne.org/item/10.5802/afst.1830.pdf
- Different neighboring target: https://github.com/AlecKriebel/Math/pull/274
