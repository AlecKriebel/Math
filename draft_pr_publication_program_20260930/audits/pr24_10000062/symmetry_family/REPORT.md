# Complete independent symmetry and aperiodicity audit

**Verdict: PASS for the original explicitly scoped Euclidean noncocompact construction. Full source classification and novelty remain unestablished. No candidate edits are required by this family.**

This audit concerns PR24, record 10000062 / AMR-099-0062, original head `6b702110d1bd4b9220e2033fa5eed030911ce8c6`, and the 16 frozen files in `../source_snapshot`. The candidate SHA256 is `3df33716dab169f07c9ff24434023d2945fc8121e03519f91a0a3fdb1ea30f84`. The complete criterion and initial reconstruction were sealed in `INDEPENDENT_RECONSTRUCTION.md` before reading old reviewer reports or either historical checker. No root or sibling findings were used to derive this verdict. The family wrote only its assigned folder, made no Git/PR/publication changes, contacted no outside individual, and added **0 proof-attempt turns**.

## 1. Original statement, source context, and scope

I independently downloaded [the archived original *Euclidean vs. Graph Metric*](https://arquivo.pt/noFrame/replay/20201231041538id_/http://www.wisdom.weizmann.ac.il/~itai/erd100.pdf), extracted the full text, read the relevant section, and visually inspected printed page 7. Question 5.7, attributed there to Benjamini with Romain Tessera, concerns triangulations of either ambient plane, a non-strict upper triangle-diameter bound r, and ambient congruences of every pair of vertex-centered metric radius-r balls preserving the triangulation. It does not restrict the isometries to direct ones. Its periodicity conclusion is undefined; there is also no explicit open/closed-ball convention. The candidate proves the closed-cell restriction interpretation, including singleton intersections, which also gives the open-ball version. It does not claim to map the complete external portions of triangles merely touching the disk.

The exact source-level success criterion was preserved before reviewer evidence: the conclusion must be stated with a periodicity convention, the two ambient alternatives and all-vertex quantifier retained, and the diameter and full metric-ball hypotheses verified. A Euclidean example suffices to refute a universal implication if its intended conclusion is cocompactness. The frozen record nevertheless properly withholds a source-level solved classification because that convention is not specified; its example has a nonzero translation and supplies no hyperbolic construction.

The strongest verified statement is: the submitted ordinary straight, face-to-face Euclidean triangulation has maximum triangle diameter r=sqrt(10), all complete closed vertex-centered radius-r cell restrictions are ambient-congruent, and its full ambient symmetry group is

\[
G=\{(x,y)\mapsto(x+2n,y),\quad(x,y)\mapsto(-x+\tfrac12+2n,1-y):n\in\mathbb Z\}.
\]

Thus its translation subgroup is exactly 2Z x {0}; G is noncocompact. The example is 1-periodic in the cited prior paper's terminology, and is not a no-translation example.

## 2. Actual prior family and definitions

I independently obtained the [published Frettloh-Garber paper](https://dmtcs.episciences.org/2142/pdf), read Definitions 1.1-1.4, Theorems 2.1/2.2, Remark 2.3, the relevant full Section 2.3 body, and Appendix A.1.2. Figures 8 and 17 were visually inspected on PDF pages 11 and 19 (printed pages 213 and 221). A temporary rendering of PDF page 21 had initially shown unrelated figures and was not used as Figure 17 evidence; the correct page was then read.

Their definition of k-periodicity counts independent translations; their crystallographic definition requires a compact fundamental domain. Their Theorem 2.2 permits reflected vertex coronae and gives either rank-one or rank-two translations. Section 2.3 expressly gives arbitrary bi-infinite sequences of chiral triangle strips alternating with isosceles-triangle strips, including the Figure 17 triangulations. Remark 2.3 already names the single-defect symbolic pattern. The candidate's underlying family and its noncrystallographic symbolic mechanism are consequently prior work, as credited. Its separate full-ball shielding calculation cannot be inferred merely from vertex-corona congruence. This audit does not certify priority for the metric specialization.

The source PDFs and extracted text are retained as temporary foreign-source audit material with hashes, not as an asserted redistributable research result. Their mathematical bodies, rather than snippets alone, supplied the context above.

## 3. Full construction and diameter prerequisites

Use delta_j in {1/2,3/2}, a_0=0, a_(j+1)=a_j+delta_j+1 for every integer j. The lower and upper rows are respectively

\[
(a_j+2k,4j),\qquad(a_j+\delta_j+2k,4j+1).
\]

Each strip is tiled by parallelograms joining equal-index vertices of its two equally spaced rows; the stated diagonal gives the submitted two triangle families. Parallelograms partition the whole strip and share complete edges. Neighboring strips agree on their row edges. This proves coverage, no crossings or overlaps of triangle interiors, and the face-to-face property throughout the plane. Horizontal spacing 2 and minimum vertical spacing 1 give local finiteness. The determinants give positive areas 1 and 3.

In a short strip, cross-edge vectors have horizontal displacements delta_j and delta_j-2, with vertical displacement 1. Their squared lengths are 5/4 and 13/4 in either chirality; the row edge has squared length 4. In a tall strip, cross-edge vectors are (1,3) and (-1,3), with squared length 10; its row edge again has squared length 4. All triangle diameters are therefore at most sqrt(10), with equality in the tall strips. In particular **every edge of length 2 is horizontal**, and every horizontal triangulation edge has length 2. There is no accidental cross-edge length 2. This intrinsic metric recognition is crucial to the complete symmetry exclusion below.

## 4. Universal whole-ball reduction, with boundaries

Translate a lower-row center to (0,0). The relevant row heights and horizontal phases modulo 2 are

\[
(-4,-1-\delta_{-1}),\ (-3,-1),\ (0,0),\ (1,\delta_0),\ (4,\delta_0+1).
\]

Since sqrt(10)<4, no strip wholly above 4 or below -4 can touch the disk. The tall strip below the root, central short strip, and tall strip above it depend only on delta_0. The preceding short strip can affect only the cap at y<=-3; the succeeding short strip begins above the disk.

At y=-3 the disk chord has endpoints p=(+-1,-3). An outgoing downward edge vector is (h,-1), |h|<=3/2. Then p dot (h,-1)>=3/2, so its squared distance is 10+2t[p dot (h,-1)]+t^2(h^2+1)>10 for t>0. The entire edge, not merely its endpoint, stays outside the closed disk after p. Other outgoing upper endpoints have |x|>=3; on their downward edges |x|>=3/2 and |y|>=3, so squared distance is at least 45/4>10. The lower row y=-4 misses the disk.

The only positive-area cap piece is the one triangle with fixed upper base [(-1,-3),(1,-3)]. Its changing remote apex lies below the disk; since its two side edges miss the disk except at the base endpoints, its clipped piece is exactly that fixed circular cap. At either chord endpoint, the six incident edges split into three positive-length traces and three singleton traces; the six incident faces split into four positive-area and two singleton traces. The two downward edges have one negative and one positive horizontal displacement in either chirality, so their order around the endpoint and their adjacency to the cap and the two singleton faces remain the same. Thus equality includes abstract incidence of distinct parent traces, rather than identifying all singleton traces indiscriminately.

Inside the open disk the fixed embedded edge traces partition its interior into the clipped face interiors. Each triangle-disk intersection is convex and connected. The incident half-plane side of a visible edge and the circle determine the clipped piece. Edges and their incident sides therefore recover positive-area face pieces; the explicit cap and endpoint incidences handle the closed boundary. This establishes the full face statement, not only equality of vertex and edge sets or total face counts.

Vertical reflection switches the central short-strip chirality. An explicit family representative after reflection has a'_j=-a_j+4j and delta'_j=2-delta_j. These offsets obey the required recurrence, and their row sets equal the reflected row sets modulo period 2; the tall cross-edge pair (+-1,3) is preserved. This is a family-to-family congruence, not generally a global symmetry of a particular sequence.

For an upper-root center (delta_0,1), the halfturn (x,y)->(delta_0-x,1-y) gives the new family

\[
a'_i=\delta_0-a_{-i}-\delta_{-i},\qquad\delta'_i=\delta_{-i}.
\]

Here a'_0=0 and a'_(i+1)-a'_i=1+delta'_(i), including negative indices. It fixes the central chirality and reverses surrounding choices. The locality calculation makes those choices irrelevant. Arbitrary lower/upper centers first reduce to these roots by translation. Composing these maps proves the quantified all-vertex ball congruence.

The historical finite enumeration is complete only after these universal bounds. There is no claim that its tested finite windows alone prove invisibility of infinitely many remote cells. Every triangle meeting a radius-r disk has all vertices within distance 2r, because its diameter is at most r. Together with the explicit guard rows, this also bounds the horizontal indices needed by the historical checks.

## 5. All Euclidean symmetries: translations, reflections, glides, rotations

Let g(x,y)=(s x+b_x,t y+b_y) after showing its linear part is diagonal. This reduction is exhaustive: every global isometry maps intrinsic length-2 edges to length-2 edges, so preserves their horizontal supporting-line direction. An orthogonal matrix preserving a one-dimensional horizontal subspace is exactly diag(s,t), s,t in {+1,-1}. It cannot be an oblique reflection, a non-halfturn rotation, or an isometry swapping horizontal and vertical directions.

The row set has successive height gaps 1 and 3. If t=+1, a lower row (a short gap above) maps to a lower row, hence b_y=4m. If t=-1 it maps to an upper row, hence b_y=4m+1. These facts exclude possible shifts by one row spacing without assuming preservation of labels.

Define epsilon_j=2(delta_j-1). This is the **actual submitted sequence variable**, not a binary-digit parity sequence. The shortest upward cross-edge has horizontal displacement d_j=-epsilon_j/2. A symmetry preserves this intrinsic short-edge direction according to its s,t signs. It necessarily satisfies

\[
\begin{array}{c|c|c}
(s,t)&\text{condition for every integer j}&\text{map type}\\
(+,+)&\epsilon_{j+m}=\epsilon_j&\text{translation}\\
(-,+)&\epsilon_{j+m}=-\epsilon_j&\text{vertical-axis reflection or glide}\\
(+,-)&\epsilon_{m-j}=-\epsilon_j&\text{horizontal-axis reflection or glide}\\
(-,-)&\epsilon_{m-j}=\epsilon_j&\text{halfturn}.
\end{array}
\]

These conditions are also sufficient after matching row phases. For t=+1 choose b_x=a_m modulo 2. Put D_j=a_(j+m)-s a_j. The sequence condition gives D_(j+1)-D_j=2-2s, an even integer, and delta_(j+m)-s delta_j=1-s, also even. Thus both rows match. For t=-1 choose b_x=a_m+delta_m modulo 2. Put D_j=a_(m-j)+delta_(m-j)-s a_j. Then D_(j+1)-D_j=-2-2s, and delta_(m-j)+s delta_j=1+s, again even. Both row types match. The shortest-cross-edge relation and the complementary long cross-edge recover exactly the submitted triangles; the tall strip is determined by the same row alignment. This proves the affine characterization universally, rather than by checking a finite grid of candidate isometries.

## 6. Exact concrete sequence and noncocompactness

The frozen candidate chooses epsilon_0=-1 and epsilon_j=+1 for **every** j!=0, including every negative j. Its offsets are a_j=5j/2 for j<=0 and a_j=5j/2-1 for j>=1. They agree with the bi-infinite recurrence; in particular a_-1=-5/2. There is no Thue-Morse, digit-parity, or undefined negative-index extension in the submitted construction.

Its negative-symbol set is the singleton {0}. Shift invariance sends that singleton to itself only for m=0. Shift-complement or reversal-complement invariance is impossible, since complementing exchanges a singleton negative set with an infinite negative set. Reversal invariance under j->m-j sends {0} to {m}, and hence requires m=0. These arguments apply to **all integers m**, positive, zero, and negative.

The exhaustive affine characterization therefore leaves only (+,+,m=0) and (-,-,m=0). Row phases give b_x=2n in the first case and b_x=1/2+2n in the second. This proves the exact full group stated above. All surviving nontranslation elements are halfturns about (1/4+n,1/2); no orientation-reversing symmetry, including any glide reflection, survives.

The translations have index 2 in G. More directly, the height of any image of a point is either y or 1-y. For any compact K, both possible height sets are bounded, so G K cannot cover points of arbitrarily large height. **The full group**, not merely its translation subgroup, is therefore noncocompact. The candidate's weaker finite-index-at-most-four proof is also correct: the linear-part homomorphism has at most four values and its kernel consists exactly of translations.

## 7. Reproduction, controls, and adversarial mutations

`HISTORICAL_REPRODUCTION.json` records all 16 frozen SHA256, byte-count, and Git-blob hash matches against the root snapshot manifest. The three historical scripts were copied into isolated `tmpforeign/runs/historical` and run there; all exited 0. Their generated receipts equal the saved receipts **byte-for-byte**, including all 16 submitted rooted cases and the historical 212 assertions over 64 rooted cases. The family intentionally made no Git calls; original-head extraction provenance is supplied by the parent snapshot manifest. This limitation is explicit, rather than claiming a separate remote-head verification.

The new `exact_checks.py` imports no historical code. It passed **888 exact rational assertions**, with **64 rooted disk cases**, enlarged guard windows, all visible face half-plane descriptors, boundary multiplicities/incidences, and **216 affine controls** across six symbolic families. It reproduces 8 closed-disk vertices, 28 positive-length edges, 23 positive-area faces, and two singleton-trace locations with 3 edges and 2 faces at each. Its finite controls support, but do not replace, the universal proofs above.

Adversarial controls include:

- A constant sequence passes a transverse translation and hence has rank-two translations; the code does not incorrectly infer noncocompactness for every family member.
- An alternating sequence has a vertical-axis glide; a step sequence has a horizontal-axis glide. The tests recognize both orientation-reversing classes rather than rejecting glides globally.
- Moving the defect to j=-3 changes the surviving halfturn index to m=-6, checking reversal and negative indices.
- Increasing squared comparison radius to 1001/100 exposes a preceding-layer choice under the prescribed canonical maps. This is not a claim that no other congruence of the enlarged disks exists.
- Deleting an incident face changes the full face descriptor; this prevents an edge/count-only certificate from silently standing in for the triangulation.
- Increasing the tall height to 301/100 violates the claimed diameter bound at r=sqrt(10).
- Requiring comparison radius squared 999/100 violates the unchanged tall-triangle diameter bound. This detects any attempt to promote the note to a strict-diameter version.
- The bi-infinite offsets are checked for negative as well as positive indices and the incorrect continuation a_-1=-3/2 is excluded.

Reproduction commands from this folder are `python3 exact_checks.py`, and, within the isolated historical directory, `python3 verify.py`, `python3 submitted_verify.py`, and `python3 independent_checks.py`. Only Python's standard library is needed. Source download and rendering used existing curl/Poppler tools; no installation occurred.

## 8. Verdict, exact gap, and disposition

No mathematical defect was found in the original scoped theorem, its metric-ball prerequisites, its exact translation conclusion, or its full-symmetry noncocompactness argument. The stronger group description above is an audit deduction, not an authorized rewrite or novelty claim.

Remaining gaps are the original source's intended meaning of periodicity, any hyperbolic full-ball construction or classification, historical priority of the metric specialization, and any strict-diameter variant. Under the weak Euclidean meaning of at least one nonzero translational period, the candidate is not a counterexample; moreover the diameter/full-ball hypothesis gives congruent incident coronae and the cited planar monocoronal theorem already supplies at least one translation for ordinary straight face-to-face triangulations. That does not resolve the undefined combined original formulation.

The frozen status/turn ledger correctly retain a partial result, false full-source-solved and new-discovery flags, and one historical substantive turn of five. Validation adds no attempts and changes no canonical state. This family recommends **PASS_SCOPED_RESULT_ONLY**, with the existing source/novelty limits preserved. Audit completion estimate: **100% for this family's assigned review**; source-level discovery remains unresolved.
