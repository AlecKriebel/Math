# Independent mathematical audit: high-genus triangulation distances

Problem 30005926, OWR-14298373-004; queue rank 956. Audit date: 2026-10-07.

## Verdict

**Accept the twelve numbered results within their stated scopes. The full target remains unresolved. No mathematical correction to the frozen author report is required.**

This is an independent mathematical and executable-check audit, not human peer review or proof-assistant certification. The typical-distance theorem remains credited to Tanguy Lions; the logarithmic diameter bound and strict diameter-versus-typical-distance gap remain credited to Budzinski, Chapuy and Louf. None of the authored results proves the diameter limit or the factor three for uniform high-genus triangulations. No novelty assessment is made.

The most sensitive claims were checked beyond replaying the author's script: the exact oriented-certificate count, repeated boundary vertices and edges in tube insertion, uniformity of the one-step enumeration estimate over logarithmic windows, and the conditional transfer from extreme decorations to a uniform pair of slots.

The author files were not changed. No patch or corrected reading copy is included because no claim-changing error was found. The details below supply additional justification and specify the scope of acceptance.

## 1. Frozen input and replay

The audited report has SHA-256:

`6bb6b843148e43497d4be8cc1ab8734c9f96b22e9a8215d1c16002037fb2419a`

The author's `MANIFEST.json` has SHA-256:

`78b14d14c630370528d17eda1cc82dd7a4f707f7643288fb85153ba52ac09866`

The author's immutable `AUTHOR_FREEZE.zip` is 19,670 bytes, SHA-256:

`aefc84ee9e468a4c39bdf06a4938948f34e98c939365023bba30f903cd771a4f`

All seven payload files listed in that manifest match their recorded sizes and hashes. The three locally supplied primary-source PDFs also match the public source manifest. This verifies the supplied bytes, not a new network byte-for-byte comparison of those PDFs or the full problem datasets.

The author verifier was run without modification in normal and optimized Python modes. Both outputs match the frozen `RESULTS.json` exactly: 57,292 exact finite controls and 12 Decimal diagnostics, 57,304 controls in total. The latter twelve are numerical diagnostics, not interval-certified inequalities. The finite checks do not prove the asymptotic statements.

A separately written standard-library verifier uses combinatorial maps, retaining edge occurrences and vertex identifications that ordinary simple-graph meshes omit. It passes **15,042 checks** in both normal and optimized modes. These counts should not be interpreted as numbers of independent mathematical theorems.

## 2. Source alignment and imported hypotheses

The exact target is the graph metric on rooted orientable type-I triangulations with `2n` faces, `3n` edges and `n+2-2g` vertices, in the interior regime `g/n -> theta in (0,1/2)`. The author consistently uses `n` as half the number of faces. The paper notation `T_(2n,g)` in BCL and `T_(n,g)` in Lions denotes the same size convention.

- **Oberwolfach target.** Printed page 1398 defines the size/genus convention; page 1399 asks for a typical-distance constant and a diameter constant in ratio three. The target page was inspected visually. [Official report](https://publications.mfo.de/bitstream/handle/mfo/4220/OWR_2024_25.pdf?sequence=1)
- **Lions.** Theorem 1.1, PDF page 2, has the required interior genus regime, constant `D_theta = 1/log(1/m_theta)`, convergence in probability, and both uniform-vertex and uniform-oriented-edge-start sampling. The theorem page was inspected visually; Section 2.1, PDF pages 6–7, explicitly allows loops and multiple edges. The arXiv record lists v1, submitted June 25, 2026. The author's research page describes the work as submitted. This audit imports the theorem; it does not independently re-prove the 42-page paper. [Versioned record](https://arxiv.org/abs/2606.27357v1), [author's research page](https://sites.google.com/view/tanguylions/research)
- **Budzinski–Chapuy–Louf.** In the inspected November 8, 2023 author preprint, Theorem 1 supplies logarithmic diameter bounds; Lemma 2 supplies the one-step counting ratio, including a stated uniformity consequence; Proposition 17 supplies the positive logarithmic gap for independent uniform oriented-edge starts. The last two statements were inspected visually on PDF pages 7 and 20. The global interior-genus assumption applies. Journal metadata is confirmed by the publisher's September 2025 issue information: volume 53, number 5, pages 1645–1667. Numbering in this audit follows the inspected preprint. [Author preprint](https://perso.ens-lyon.fr/thomas.budzinski/papers/diameter_high_genus.pdf), [publisher metadata](https://www.imstat.org/publications/aop/aop_53_5/aop_53_5.pdf)

A bounded current search, including the arXiv version record and the author's research page, did not locate a later diameter-constant resolution. This is not an exhaustive literature-status certification. The report correctly distinguishes the established typical-distance portion from the remaining diameter question.

## 3. Result-by-result mathematical assessment

### Proposition 1: parameter elimination and endpoint expansions

**Accepted.** For `s = sqrt(1-4h)`, the substitution `m=(1-s)/(1+s)` gives `h=m/(1+m)^2`. Substituting into both the Boltzmann parameter and the equation defining theta yields exactly the displayed rational expression for lambda and the hyperbolic expression for theta. All denominators are positive in the stipulated interior regime.

The Taylor division is correct. Independently, symbolic expansion gives

`theta = t^4/240 - t^6/4032 - t^8/172800 + t^10/798336 + O(t^12)`.

In particular, the author's terms through degree eight and the asymptotic `D_theta ~ (240 theta)^(-1/4)` are correct. At the other endpoint, `delta=6t exp(-t)(1+O(exp(-t)))` implies `t-log t = log(1/delta)+log 6+o(1)`. First obtaining `t/L -> 1` and then substituting into `log t` justifies the stated second-order inversion. These are asymptotics of a deterministic constant. They do not extend the random-map theorem uniformly to either endpoint.

### Proposition 2: comparison of lambda and m

**Accepted.** For `0<m<1`,

`m^2+10m+1 > (1+m)^2`

implies `lambda/m < (1+m)^(-2) < 1`. Since `log(1/lambda)>log(1/m)>0`, the comparison of reciprocal logarithms has the stated direction. The strict rigid-tube cutoff `a_theta < D_theta/3` follows.

### Corollary 3: strict diameter gap

**Accepted as a credited deduction.** Lions's edge-start sampling matches BCL Proposition 17 exactly; there is no unsupported conversion from uniform vertices to degree-biased vertices. The lower-tail event for the sampled distance and the BCL gap event each have probability tending to one. Their intersection does too, without independence. The resulting event concerns the map's diameter alone. Nothing identifies the extra constant with `2D_theta`.

### Proposition 4: geodesic witness bound

**Accepted.** On a geodesic of length greater than `r+2s`, the first and last `s+1` vertices are disjoint, including when `r=0`. Every selected cross-pair is farther than `r`, since a geodesic's subpaths are geodesic. Ordered pairs count both directions and give the factor `2(s+1)^2`. For deterministic vertex count `N`, the expected ordered-pair count is exactly `N^2 p(r)`. This proves the inequality for real `r>=0` and integer `s>=0`. The discussion correctly avoids upgrading an unspecified `o(1)` pair tail to a uniform diameter bound.

### Proposition 5: a large subset of bounded ambient diameter

**Accepted.** Markov's inequality bounds the random fraction of bad ordered pairs by `sqrt(p)` outside an event of probability at most `sqrt(p)`. Averaging rows produces a ball with at least `(1-sqrt(p))N` vertices. The ambient triangle inequality bounds its diameter by `2r`. The `p=0` case is valid separately. No statement about intrinsic distances in the induced subgraph is inferred.

### Proposition 6: tube insertion

**Accepted, including non-simple original face boundaries.** The operation replaces a face's abstract characteristic disk, retaining its boundary identifications. It does not require the closure of the face in the original surface to be an embedded closed disk. The replacement is another disk with the same boundary occurrence data, so the surface genus is unchanged.

Each annulus adds six faces, three vertices and nine nonboundary edges. Every path between old vertices can have a patch excursion replaced by an old boundary edge or a constant path: any two old boundary vertices are equal or adjacent because there are only three corner occurrences. Old paths remain present. These two inequalities prove exact preservation of old distances. The layer function is zero outside the patch and 1-Lipschitz on edges, including after outer-boundary identifications. It proves the depth lower bound; the vertical edges attain it.

The additional permutation-map tests verify these facts with one-, two- and three-vertex face boundaries, loops, parallel edges and repeated boundary edges. They strengthen the author's simple-face controls but are not substitutes for the disk-replacement argument.

### Corollary 7: preservation of typical scale under a nonuniform modification

**Accepted.** Because the original vertex number is deterministic and asymptotic to `(1-2theta)n`, inserting `3 ell_n=o(n)` vertices makes the probability that two uniform modified vertices are both old tend to one. Conditioning on this event does not size-bias the base map: its probability depends only on the deterministic counts. The pair is conditionally uniform on old vertices, whose distances are unchanged. The logarithmic normalization and genus ratio then converge as claimed.

The superlogarithmic and prescribed logarithmic lower bounds on diameter follow directly from the deterministic depth bound. The resulting maps are generally nonuniform; this result does not disprove the uniform-model conjecture.

### Proposition 8: exact certificate expectation and upper cutoff

**Accepted with the stated certificate convention.** The factor `6n` is correct. It would not be the correct factor for an unspecified count of unmarked geometric subsets. Section 4 below gives an automorphism-aware proof and the independent finite controls.

The logarithmic-window uniformity is valid, including along arbitrary admissible genus sequences. The resulting error is `exp(o(log n))=n^(o(1))`, not relative `1+o(1)`. This is sufficient for the claimed expectation exponent and for the upper cutoff. Markov's inequality is applied only when the exponent is strictly negative.

The simultaneous exclusion of longer tubes is justified by taking the innermost prescribed number of annuli and the cap. If the containing tube is longer, that inner boundary is a simple internal triangle; if lengths are equal, the given removal certificate already supplies admissibility. Thus no additional union bound over all possible heights is needed.

The conclusion concerns this one rigid pattern family. It does not bound all possible deep planar decorations or the entire graph diameter.

### Proposition 9: one-step ratio precision is insufficient

**Accepted.** The blocks are disjoint for sufficiently large indices. All adjacent differences of the piecewise-linear sequence tend to zero, including at block endpoints. Therefore the adjacent ratios of `b_n` tend to `q`. At the selected three indices, the linear term from `q^(-n)` cancels and the logarithm of the second ratio is exactly `2 sqrt(j)`, which diverges. Also `j` is asymptotic to `log n_j`.

This example is a positive real sequence, not an enumeration sequence for actual maps. That is exactly the necessary scope: it disproves the proposed inference from only the one-step ratio hypothesis. It neither proves irregularity of triangulation counts nor prevents stronger enumeration results from supplying missing precision.

### Lemma 10: two large heights

**Accepted.** Here `M_n` is interpreted in the usual sense as a deterministic sequence comparable to `n`, as in the lemma's indexing. Exchangeability gives the required common first and second indicator moments. The lower-threshold mean diverges; the joint-tail upper bound makes the variance `o(mu^2)+O(mu)`. Chebyshev then forces at least two exceedances with high probability. The upper threshold follows by the union bound. This proves convergence of both largest order statistics. Independence is not needed, but a marginal tail alone is insufficient.

Application to a random number of slots would require an appropriate conditional or uniformly controlled formulation; this audit does not silently add that extension to the lemma or claim it for the random-map model.

### Lemma 11: bounded-boundary metric decomposition

**Accepted.** Every path from one decoration interior to another encounters the first attachment set before its last encounter with the second. Prefix and suffix lengths dominate the two depths. Core isometry makes the middle segment at least the core distance between its boundary endpoints. Moving each endpoint to its anchor loses at most `b`, giving the lower bound. The reverse constructed route gives the upper bound.

Pairs within one decoration can be joined through their boundary at cost at most the two depths plus `b`; core vertices have zero depth. These cases yield the global diameter bound. Clique attachments guarantee core isometry by replacing excursions with an edge or constant path. For arbitrary attachment sets, isometry must remain an explicit assumption.

### Theorem 12: conditional diameter constant

**Accepted as an abstract sufficient-condition theorem.** Lemma 10 and the diameter inequality give the upper bound. The two selected large decorations must be chosen independently of their assigned slots. Conditional uniform permutation then sends them to a uniform ordered distinct pair of slots. No independence of the core and the multiset of heights is required; Section 5 makes this point precise.

The selected depths, anchor separation, bounded-boundary metric lower bound and `b=o(log n)` give the displayed lower bound, with the stated `3 epsilon` loss. Taking arbitrarily small fixed epsilon proves convergence.

The theorem's hypotheses are not established for uniform high-genus triangulations. In particular, the report has not proved the sharp generic depth tail, the needed joint-tail estimate under size/genus conditioning, the core-diameter constant, or the required exchangeable assignment/decomposition. The theorem is not a solution to the diameter conjecture.

## 4. The certificate count in detail

Write `n_0=n-3 ell`. A certificate includes an orientation-compatible marked boundary side and the patch occurrence with its corner identifications. Boundary sides are face-side occurrences: even when an edge occurs twice on the boundary, these occurrences are distinct darts.

Deleting the patch while retaining its marked boundary side produces a size-`n_0`, genus-`g` map rooted at that side. Conversely, inserting the fixed patch in the root face of such a rooted map produces a map with an oriented removal certificate. These operations are inverse before assigning the host's separate root.

A connected oriented map automorphism fixing a dart fixes the whole map: it commutes with edge reversal and cyclic face or vertex succession, whose action connects all darts. Thus the marked certificate has trivial stabilizer. Each unrooted map-with-oriented-certificate admits exactly `6n` distinct choices of a separate host root. There are `tau(n_0,g)` possible certificate-rooted deletion outputs. Consequently the total number of pairs

`(rooted size-n map, oriented removal certificate)`

is exactly `6n tau(n_0,g)`. Dividing by `tau(n,g)` proves the first-moment formula. Equivalently, restricting the host root to the `6n_0` surviving darts gives the author's factor `6n_0`; removing that restriction multiplies by `n/n_0`. Nontrivial automorphisms of the underlying unmarked map do not change either argument.

For uniformity, set `k_n=3 ell_n=O(log n)`. A failure of uniform convergence of the adjacent ratio over `0<=j<k_n` would produce a subsequence and indices `j_n` such that `n-j_n -> infinity`, `g_n/(n-j_n)->theta`, but the ratio fails to approach `lambda(theta)`. This contradicts the sequential source theorem. A further subsequence can make `n-j_n` strictly increasing, and the corresponding genus values can be extended to an admissible full sequence if necessary. Since lambda is positive, logarithms also converge uniformly. Summing `k_n` errors gives `o(k_n)`, exactly the precision used by the author.

### Independent finite map controls

The independent program enumerates all edge pairings for face permutations with two or four triangular faces, retains connected maps, and canonicalizes rooted maps by deterministic dart traversal. It finds 65 rooted base maps:

- Two faces: 4 of genus zero, 1 of genus one
- Four faces: 32 of genus zero, 28 of genus one

Across every marked face side and heights one and two, it performs 1,500 surgeries. The cases include 348 one-vertex boundaries, 900 two-vertex boundaries and 252 three-vertex boundaries; 396 cases repeat a boundary edge. Genus, all face degrees, connectedness, old vertex identifications, old distances and exact layer depths are checked.

After rerooting and canonicalizing, certificate totals are:

- Base size 1, height 1: 96 for genus zero and 24 for genus one
- Base size 1, height 2: 168 for genus zero and 42 for genus one
- Base size 2, height 1: 960 for genus zero and 840 for genus one
- Base size 2, height 2: 1,536 for genus zero and 1,344 for genus one

Each equals `6(n_0+3 ell) tau(n_0,g)`. Restricted totals are respectively 24, 6, 24, 6, 384, 336, 384 and 336, agreeing with `6n_0 tau(n_0,g)`.

A separate detector starts at every candidate cap-side dart of every generated rooted host and matches the patch using only face succession and internal edge pairing. It does not use insertion history or old-dart labels. It verifies that deletion leaves a connected same-genus map. Its certificate sets agree exactly with the insertion-and-rerooting sets. This checks both overlaps/multiplicities and boundary degeneracies. It is a finite enumeration of the small-base insertion classes, not an exhaustive enumeration of every larger host map or an asymptotic experiment.

## 5. Why extreme-decoration conditioning is legitimate

Let `E_n` denote the core and its slots, and let `q_n(E_n)` be the fraction of ordered distinct slot pairs whose anchor distance is below `(beta-epsilon) log n`. Hypothesis 3 says `E[q_n(E_n)] -> 0`. Let `A_n` be the event that the multiset contains two sufficiently large decorations.

Choose two of those decorations by a rule using the multiset and independent auxiliary randomness only. On `A_n`, hypothesis 4 gives a uniform ordered distinct pair of assigned slots, even after conditioning on the multiset. Therefore

`P(A_n and selected anchors are too close) = E[1_(A_n) q_n(E_n)] <= E[q_n(E_n)] -> 0`.

This is the required transfer. The equality allows arbitrary dependence between the core and the height multiset; the inequality uses only nonnegativity. Conditioning on the rare bad-core event is unnecessary. The high-decoration event itself has probability tending to one by Lemma 10. The independent checker includes an exact rational example with deliberately correlated environment/height data, and a negative control showing why slot-dependent selection would invalidate the argument.

## 6. Remaining scope and reproduction

The five mathematical approaches are genuinely distinct: parameter analysis, typical-to-extreme inequalities, deterministic surface surgery, fixed-pattern enumeration/precision analysis, and an abstract extreme-decoration reduction. Retrieval, finite checking and this audit are not additional authored approaches.

No stronger result may be inferred from this acceptance:

- No diameter constant or ratio-three theorem is proved for the uniform model
- No counterexample to that model is supplied
- No high-probability rigid-tube existence theorem follows from its diverging first moment
- No relative second-moment estimate is supplied by the logarithmic-window ratio argument
- No endpoint or simple-triangulation extension is established
- No re-proof or peer-review certification of imported papers is claimed
- No full-dataset hash or duplicate-gate re-verification was undertaken in this audit

Reproduction from the audit directory:

`python checks/independent_checks.py`

`python -O checks/independent_checks.py`

Both produce the recorded independent result. The author's verifier is reproduced separately from its frozen folder with `python verify.py` and `python -O verify.py`. `AUDIT_MANIFEST.json` records the distributable audit-file hashes. Source PDF copies, extracted text and source-page renders are excluded from the distributable audit files.
