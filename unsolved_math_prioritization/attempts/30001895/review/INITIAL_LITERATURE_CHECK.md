Historical bounded literature check before the author attempts. The later r=2 theorem is credited in the current README; this file does not describe final r=2 coverage.

# Bounded prior-coverage check: r-element component

Checked 2026-10-03 UTC. Target: OWR 44/2011 Problem 8(2′), imported in record 30001895 / OWR-11136-027. No new proof or counterexample search; no author turn used.

## Result

No direct full resolution was located. This says only that the examined sources and bounded search did not establish full coverage. It is not a certification of current openness, absence of unpublished work, or novelty of any future proof.

The residual is a family of r-element sets with r+1≤q≤p and the common-intersection (p,q)-property, asking for τ≤p−q+1. The original does not explicitly specify finite F or |F|≥p. Use the nonvacuous convention explicitly and preserve the family-cardinality qualification when reporting the residual.

## Direct primary sources and coverage boundaries

1. [OWR 44/2011, pp. 2540–2541](https://ems.press/content/serial-article-files/46358), Problem 8. The r-element question is independently numbered 2′ and called a corollary of 2. No separate resolution is supplied there.

2. [Chelnokov–Dol’nikov, arXiv:1312.4110v1](https://arxiv.org/abs/1312.4110v1), Definition 7, Theorem 4, PDF pp. 3–4; the local PDF and extracted text were checked. Definition 7 includes |F|≥p. In the relevant q≥3 range, Theorem 4 gives τ(F)≤p−q+1 for F∈QA¹₁ with

   |F| ≥ binom(p−q+3,2) × [binom(p−q+2,2)−1] + p−q+4.

   QA¹₁ means linear families: distinct members meet in at most one element. This includes restricted coverage for sufficiently large families of 2-element sets. Arbitrary r-uniform families need not be linear, and the size threshold is stronger than merely |F|≥p. Theorem 4 is not a full resolution of 2′. The same paper's Helly–Gallai theorems have a different local-transversal hypothesis and are not directly asserted to solve the requested (p,q) bound.

3. [OWR 40/2014, pp. 2246–2249](https://publications.mfo.de/bitstream/handle/mfo/3430/OWR_2014_40.pdf?isAllowed=y&sequence=1), Dol’nikov with Bogdanov, *On a (p,q)-property for hypergraphs*. The initial definition on families matches the usual common-intersection property and includes |F|≥p. However, the subsequent hypergraph definition on p. 2247 requires every sufficiently large vertex subset to contain an independent q-vertex subset. That is not the original condition on q intersecting members of an r-uniform edge family. Consequently, its chromatic/transversal bounds for r-graphs cannot simply be substituted as a resolution of 2′. This report is a particularly close false-positive match.

4. [OWR 19/2017, pp. 1153–1154](https://ems.press/content/serial-article-files/46683), Dol’nikov with Didin and Grigorev, *On lines and points and the (p,q)-property*. Definition 2 again includes |F|≥p. Its Theorem 6 supplies τ(F)≤p−2 for combinatorial-line families with the (p,3)-property and p≤6. The linear-incidence restriction and small-p range exclude full coverage of arbitrary r-element families. Its general planar-line conjecture is superseded in the large-p range by Keller–Smorodinsky; that does not determine the r-element question.

## Search bounds and exclusions

A separate read-only coverage pass reported 23 targeted queries combining Dolnikov/Dol’nikov, r-element/finite sets, uniform hypergraphs, (p,q)-property, p−q+1, and Bogdanov. Its exact query strings were not frozen; only its bounded scope and source-backed findings are used above. All principal 2014/2017 definition/theorem claims were rechecked against the primary reports during this audit.

The following ten exact additional queries are preserved from this audit:

- "Dolnikov" "r-element" "transversal"
- "Dol’nikov" "r-element" "p" "q"
- "p-q+1" "r-element"
- "Dolnikov" "Polyakova" "property"
- "r-uniform" "(p,q)" "transversal"
- "r-element sets" "transversal" "p"
- "Coloring" "Polyakova" "Ramsey"
- "Дольников" "Полякова" "p, q"
- "r-element sets" "(p, q)"
- "uniform hypergraphs" "p-q+1"

Hits about student lecture notes, chain intersection, convex-set Hadwiger–Debrunner bounds, uniform linear systems, finite projective planes, independent-set/vertex versions of (p,q), and generic transversal bounds were not counted as full coverage without matching hypotheses and conclusion. The 2006 Dol’nikov–Polyakova survey cited in Chelnokov–Dol’nikov was bibliographically identified there; no copy establishing the r-element assertion was obtained. A 1998 same-author graph Ramsey paper surfaced, but its graph independent-set property did not provide direct coverage of the target.

## Safe consequence

Preserve part 2′ as a separate unresolved-by-this-review component. Do not transfer the planar-line counterexample to r-element sets without a separate theorem or verified argument. Do not charge a new author turn or claim a new result on the basis of this search.
