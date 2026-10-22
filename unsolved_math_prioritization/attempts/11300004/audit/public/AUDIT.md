# Independent audit: wild-knot quadrisecants

Problem 11300004 / AMR-112-0004; queue rank 1014. Audit date: 2026-10-08 UTC.

## Decision

**Accept the corrected packet as an unresolved five-approach report, with status `unsolved` and turns `5/5`.** All seven numbered lemmas, Proposition 8, the two introductory counting observations, and the subsidiary geometric arguments are correct under their stated hypotheses. None proves the universal wild-knot assertion. No novelty, independent human peer review, or formal certification is asserted.

The original packet is mathematically acceptable at the same unresolved scope, but required two narrow publication/validation repairs:

1. Its direct primary-source conjecture quotation conflicted with the requested source-free publication boundary. The corrected report uses authored paraphrase. The literal removal diff is excluded because it repeats the removed source text. The correction is implemented in the replacement file, not merely recommended.
2. The original direct verifier accepted a re-pinned ledger whose first turn was JSON `true` or `1.0`, since Python equality identifies those values with integer 1. It also omitted exact checks for the ledger's aggregate turn counts. The corrected verifier requires exact integer types and the expected values. The original externally pinned bootstrap already rejected these byte changes; this was a semantic-validation gap after deliberately replacing the manifest trust input, not a bypass of the original integrity boundary. The pure code patch is included as `LEDGER_TYPE_HARDENING.patch`.

The corrected status records completion of this audit. No mathematical statement or five-route ledger content was changed. Original bytes remain intact. The corrected archive is the publishable replacement; the original archive is retained as historical evidence and must not be published as a source-free corrected deliverable.

## 1. Identity, counting convention, and source versions

The target is infinitude of distinct unoriented affine lines meeting a wild embedded circle in Euclidean R³ in at least four distinct points. A line is counted once even if it contains an interval of the curve. The cached problem record matches this line-count target, with one matching ID and the expected code. Both corpus byte counts and SHA-256 identities were independently recomputed; only hashes, counts, and match results are included in `SOURCE_RECHECK.json`.

The published 1994 Kuperberg version has a wild-knot conjecture at p.49, numbered 21, while its p.42 definition treats a quadrisecant as a segment endowed with two interior contacts. The 2002 arXiv v2 has a wild-arc conjecture numbered 6.4 and retains the marked-segment convention. The change of domain is real. Neither the numbering nor the domain may be silently transferred between versions. The published pages were inspected, including fresh renderings of pp.42 and 49 from the hash-verified PDF. The revision's definitions, theorem statements and relevant proof text were independently re-extracted and inspected. [Published version](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Kuperberg/Kuperberg4.pdf), [arXiv v2](https://arxiv.org/pdf/math/9712205v2).

Kuperberg's quadrisecant theorem is for nontrivial **tame** links in R³. Its proof uses a homeomorphism taking the link to a smooth one and a normal tubular neighborhood. Those are not available for an arbitrary wild embedding. The strengthened component-segment conclusion does not remove this tameness hypothesis. [Kuperberg v2](https://arxiv.org/pdf/math/9712205v2).

Denne's opening convention restricts the knotted curves in Theorem 27 to nontrivial tame knots. Corollary 29 adds essentiality for finite-total-curvature knots. The 2016 survey's Theorem 8 preserves the distinction. Bai–Wang–Wang's counterexamples concern a quadrisecant-derived polygonal approximation, not the wild-knot infinitude problem. [Denne 2005](https://arxiv.org/pdf/math/0510561), [Denne 2016](https://arxiv.org/pdf/1608.02608), [Bai–Wang–Wang 2016](https://arxiv.org/abs/1605.00538).

The original five PDF hashes and sizes match independently. ArXiv landing-page version histories were checked. A fresh bounded search located no inspected primary theorem proving the required universal line-count claim or a wild counterexample. This is not a complete literature survey or a certificate of current open status. Secondary database labels and adjacent search snippets were not promoted into mathematical evidence.

### Counting lemma and diameter control

For a line with exactly m curve contacts, an unordered marked quadrisecant is determined by a four-element subset: the extreme points give the segment endpoints and the remaining points give its two marks. There are exactly C(m,4) such sets if m≥4. If every line has finitely many contacts, finitely many supporting lines therefore support finitely many marked sets. Conversely infinitely many supporting lines supply infinitely many marked sets. Without the finite-contact hypothesis only the latter implication is automatic.

For the upper semicircle together with its diameter, the diameter line supports infinitely many marked sets but is the sole line with at least four contacts. In its plane the curve is the boundary of a convex half-disk. A line not supporting a boundary interval has at most two boundary contacts; the sole straight boundary interval is the diameter. A line outside the plane has at most one contact. The curve is tame: from an interior point of the half-disk, the positive radial boundary-distance function is continuous, and division of the radial coordinate by this function gives a planar homeomorphism carrying the boundary to a circle. Extend the homeomorphism by the identity in the normal coordinate. A similar radial map carries a circle to a polygon. Thus this is a tame counting countercontrol, never a wild counterexample.

## 2. Route 1: approximation compactness

### Lemma 1

Choose a subsequence of four parameter tuples in the compact space (S¹)⁴. Circular separation at least δ passes to the limit, so the limit parameters are distinct. Uniform convergence gives

|f_n(t_n)−f(t)| ≤ ||f_n−f||∞ + |f(t_n)−f(t)| → 0.

Injectivity of f separates the four limiting images. All cross products expressing collinearity pass to zero, so the limit consists of four distinct collinear points. No differentiability is used.

The hidden quantitative protection can be made explicit: on the compact set of pairs with circular distance at least δ, the continuous function |f(s)−f(t)| has a positive minimum mδ. The corresponding image distances for f_n are at least mδ−2||f_n−f||∞. Thus the supporting line has a nondegenerate pair of endpoints along a sufficiently late subsequence.

### Compact line representation and Lemma 2

For a nonzero direction vector v, put P=vvᵀ/|v|² and let c be the point of the line nearest the origin. Then P is a symmetric rank-one orthogonal projection and Pc=0. Projection matrices of this kind form a compact set. Lines meeting a fixed closed ball of radius R have |c|≤R, so they belong to a closed bounded, hence compact, set of pairs (P,c). The actual secant-line set need not itself be closed; the report correctly says that it lies in a compact family.

For distinct points a,b, P is the continuous expression based on v=b−a and c=(I−P)a. Consequently the separated witnesses in Lemma 1 have convergent supporting lines. If their line distances from every member of a fixed finite family F are at least ε, their limiting line remains at least ε away. The hypothesis of Lemma 2 therefore supplies a member of Q(K) outside every finite F. Taking F=Q(K) under the assumption that Q(K) is finite is a contradiction. The constants may depend on F; no uniform choice across all finite families is claimed.

### Collapse example and obstruction

The first coordinate makes every displayed piecewise-linear/parabolic graph an embedded arc. All interpolation heights and all values of t² on the modified interval lie between 0 and 25ε², giving the claimed uniform error bound everywhere. The four selected zero-height vertices are distinct for ε>0 and their x-span is 6ε. Every neighboring interpolation segment has positive height at at least one endpoint, so no nontrivial segment of that graph lies on the axis. The limit is the parabola. A nonvertical planar line leads to a quadratic equation with at most two roots; a vertical line has at most one contact. A spatial line outside the parabola's plane has at most one. Thus the limiting arc has no trisecants although the chosen four witnesses collapse to its origin.

This does not challenge noncollapse conclusions proved with additional essentiality and tame-neighborhood hypotheses. It only disproves unprotected witness passage. The report correctly leaves unresolved all of: suitable nontrivial tame approximants, persistent four-point separation, and escape from every finite line family. Wildness by itself is not proved to supply any of them.

## 3. Route 2: local straightening

### Lemma 3

Extend u,v continuously beyond the interval by their endpoint values. For every s∈[0,1], the displayed shear H_s has inverse

(x,y,z) ↦ (x,y+s u(x),z+s v(x)).

Both H_s and the inverse depend continuously on s and space. Thus H is an ambient isotopy and its endpoint sends the graph arc to a straight segment. This proves tameness without any smoothness assumption on u,v. A strictly monotone continuous coordinate can be used as the parameter because its inverse on a compact interval is continuous; a mere bound on line intersections supplies no such coordinate.

### Lemma 4

Under the stated extra finite-contact hypothesis, the union E of contacts on the finitely many exceptional lines is finite. For any curve point p, choose a small closed parameter interval around its preimage that excludes all other points of f⁻¹(E). Its image meets every exceptional line in at most one point. A line containing four points of the subarc would be exceptional for the whole curve, an immediate contradiction.

The parameter interval is chosen with p in its interior, so this is a genuine compact neighborhood arc in the circle. The argument does not require a smooth chart and it also covers E empty.

### Unproved links

Absence of quadrisecants is not shown to imply a graph coordinate or local flatness. The report explicitly marks that proposed local theorem as missing. Nor does it use a global local-flatness-to-tameness theorem to obtain a result. Endpoint wildness of an arc is a separate issue from interior local flatness. Infinite contacts on even one exceptional line defeat the finite set E argument; the diameter example shows why finiteness of the line set cannot replace the finite-contact hypothesis. There is no illicit contrapositive theorem here.

## 4. Route 3: stable local transversals

### Lemma 5 and its determinant

Use variable order (t₀,t₁,t₂,t₃,A,B,C,D) and rows (y₀,z₀,y₁,z₁,y₂,z₂,y₃,z₃). The first two arcs have y-derivative 1, and the last two have z-derivative 1. The coefficients of the line variables are −1 and −i in the respective coordinate rows. Independent signed subset-expansion of the resulting matrix gives determinant **1**, without using the packet's elimination routine.

More generally at distinct positions x₀,x₁ for the first pair and x₂,x₃ for the second, this row/column convention gives (x₁−x₀)(x₃−x₂). The direct nullspace proof is simpler: the first pair's z-equations force C=D=0, the second pair's y-equations force A=B=0, and then the four remaining equations force every t_i=0. Duplicate positions in either of those pairs, or making every model tangent parallel, yields singular negative controls. Nondegeneracy is a real condition, not an assumption silently supplied by four arbitrary arcs.

For perturbed C¹ parametrizations, form the eight-coordinate constraint function F. At the unperturbed model its derivative is the constant invertible matrix J. Restrict all t_i to a closed ball lying inside their arc domains and all line variables to a small neighborhood of zero. Sufficiently small C¹ perturbations make ||I−J⁻¹DF||≤1/2 throughout that ball and |J⁻¹F(0)|≤r/2. Hence x↦x−J⁻¹F(x) maps the closed radius-r ball into itself and is a contraction. Its fixed point is the desired transversal. The four intersection x-coordinates remain in disjoint neighborhoods of 0,1,2,3, which guarantees four distinct points. This argument establishes precisely the claimed C¹ persistence; it is not a C⁰ persistence theorem for wild arcs.

The independent finite controls additionally solve a small rational affine-offset model exactly and verify the resulting four points' collinearity. Perturbing one of those points off the line is rejected.

### Lemma 6 and localization

Pairwise disjoint subsets of line space cannot contain the same line, so one quadrisecant chosen from each such subset gives infinitely many distinct lines. This is a direct injectivity argument. Translation and dilation act continuously and invertibly on line space. Distinct prescribed parallel model lines can be assigned pairwise disjoint sufficiently small neighborhoods, and the local construction can be translated and scaled into corresponding positions. No assertion that arbitrary wild knots contain those configurations follows. Disjoint spatial regions alone do not separate line families.

### Artificial closure

Suppose an arc A and one straight closing segment S form a tame knot, and a quadrisecant has no consecutive component segment contained in that knot. Two selected contacts in S would force every selected contact between them to lie in S as well, since S is a straight interval. Among those contacts an adjacent selected pair would then span a component segment contained in S, a contradiction. Thus at most one of the four chosen points lies in S, and at least three lie in A. In the nonsupporting-line case one can instead use the fact that two different lines intersect in at most one point. Neither argument supplies a fourth point on A.

The missing general tangle decomposition, closure-point elimination, and distinct-support mechanism are accurately disclosed. No wild knot decomposition theorem is smuggled into the local construction.

## 5. Route 4: the trisecant locus

### Lemma 7

The parameter domain is compact. Add a coefficient λ∈[0,1] and impose γ(c)=(1−λ)γ(a)+λγ(b), the endpoint order, and the three distance lower bounds. These define a closed subset of I³×[0,1]; its projection Tδ is compact. The distance bounds ensure distinct endpoints and ensure that the third point differs from both endpoints.

If two different c-values had the same pair (a,b), injectivity of γ and those separation bounds would give four distinct collinear image points. The quadrisecant-free hypothesis forbids this. Thus the endpoint projection is continuous and injective from a compact space into the Hausdorff space I². Its inverse onto its image is continuous, establishing the claimed homeomorphism.

This lemma supplies neither a manifold structure nor an essential cycle. It gives no uniform control as δ↓0. Exceptional lines with infinite contacts can support many different middle points and entire families of marked configurations, so the finite-line target cannot be replaced by a configuration-counting assertion. A continuous disk filling does not by itself verify a locally flat boundary collar; the report does not claim otherwise. The remaining configuration-space and collar arguments are genuine unsolved links in this route.

## 6. Route 5: rectifiable infinite-curvature countercontrol

### Function and rectifiability

Choose a smooth cutoff equal to 1 near the positive side of zero and vanishing well before π. On the negative side set f=0; on the positive side use the report's cutoff times θ³sin(1/θ²), and extend periodically. At zero f is continuous and f(θ)/θ→0. On a sufficiently small positive interval its derivative has magnitude at most 3a²+2. On the remaining compact cutoff region it is smooth with bounded derivative. The mean value theorem, including intervals with endpoint zero, gives a Lipschitz function. Periodic joining causes no discontinuity because f vanishes near ±π.

The map θ↦(cosθ,sinθ,f(θ)) is a continuous embedding of the circle: its projection already identifies only the periodic endpoint pair. It is Lipschitz on a compact parametrization interval and therefore rectifiable, with finite length bounded by the integral or Lipschitz estimate for its speed.

### No trisecants and tameness

A nonvertical spatial line projects to a planar line with at most two contacts on the unit circle. Each such contact has a unique lift to the graph. A vertical line has at most one graph contact. Hence there are no three distinct collinear points.

For a continuous radial cutoff ρ supported away from radius zero, define F(r cosθ,r sinθ)=ρ(r)f(θ). Periodicity makes this well-defined and the cutoff makes it continuous at zero and outside the annulus. The vertical shear (x,y,z)↦(x,y,z−sF(x,y)) has its continuous inverse obtained by changing the sign. It is an ambient isotopy flattening the curve to a standard circle. The curve is therefore a tame unknot even though its derivative fails to be continuous at zero.

### Infinite polygonal total curvature

At θ_k=(kπ)^−1/2, sufficiently far into the cutoff-one region, the derivative is v_k=(−sinθ_k,cosθ_k,−2(−1)^k), with norm √5. Consecutive normalized tangents have inner product

[cos(θ_k−θ_(k+1))−4]/5 ≤ −3/5.

They are separated by an angle at least arccos(−3/5)>π/2; the limiting value asserted in the report also follows. Arrange any finite string in increasing angular-parameter order (the reversal of increasing k). At each selected smooth point choose a sufficiently short chord interval, with all intervals disjoint and ordered, so that its oriented chord direction differs from the unit tangent by less than π/8. Consecutive selected chord directions are then separated by more than π/4.

Include all chord endpoints in an inscribed closed polygon. Along the polygonal edge-direction sequence, the spherical triangle inequality bounds the accumulated turning between any two selected chord edges below by their angular separation. The portions between successive selected edges are disjoint, so these lower bounds add. With N selected chords the polygon has total curvature greater than (N−1)π/4. As N is arbitrary, the supremum of inscribed-polygon total curvatures is infinite. This is a proof for the actual continuous curve, not an inference from finitely many tangent samples.

Thus the geometric shortcut from infinite turning to any quadrisecant fails even for rectifiable tame closed curves. No wild counterexample is constructed, and no claim that wildness is equivalent to infinite curvature is used.

## 7. Scope and five-turn assessment

The five mathematical routes have different prospective mechanisms: noncollapsing approximation, local tameness, internal tangle witnesses, topology of the trisecant locus, and curvature forcing. Each contains a valid auxiliary result or explicit countercontrol and states its unresolved link. Source retrieval, algebraic calculation, literature searches, and package testing are not counted as extra mathematical turns. The five-turn ledger is therefore supported as a record of five approaches, not five proofs or five newly discovered theorems.

Every knot-theoretic target and source theorem here is in R³. No tame-knot theorem is applied to a wild embedding, no ambient homeomorphism is presumed to preserve Euclidean collinearity, and no higher-dimensional extension is asserted. In particular the transversal system has eight equations in eight variables because lines in R³ have four local degrees of freedom and the four curve points contribute four parameters. This balance is not a reason to assume the same generic persistence in larger ambient dimensions.

## 8. Reproducibility and acceptance evidence

`ORIGINAL_REPLAY.json` and `CORRECTED_REPLAY.json` independently authenticate the supplied external archive, manifest, bootstrap and verifier pins before execution. Each archive is inspected for duplicate/unsafe members and source-free inventory, manually extracted to a fresh unrelated temporary directory, and replayed there with Python `-I -B`, both normally and with `-O` and `-OO`.

The real and effective UIDs are both 1000. Files and directories are set to read-only modes. Five actual write/create attempts fail with permission denials, including the extraction root. The hash-and-mode snapshot of the frozen extraction is unchanged afterward. No root-process imitation of a read-only test is involved.

For each archive, the distributed author harness is replayed from the extracted archive and reproduces 31 hostile cases / 93 mode-specific runs. The independent harness adds 43 cases / 129 runs: 42 expected rejection cases and one successful external-module-shadow isolation control, each in three modes. It also runs four ledger regression cases in three modes. The original direct verifier accepts those 12 deliberately re-pinned regressions; the corrected direct verifier rejects all 12. Both pinned bootstraps reject unauthorized rehashed content.

`EXACT_CONTROLS.json` records independent arithmetic controls in all three optimization modes: signed subset determinant expansion, three singular Jacobian controls, an exact affine-offset transversal, an off-line rejection, marked-set versus support counts, 680 exact interpolation samples, 286 rational lifted-circle triples, and the tangent cluster cosine. These finite calculations support diagnostics; the continuous lemmas are audited by the proofs above.

No checks rely on Python assertions. The fixed-file, externally trusted pin, trusted Python/standard-library threat model is retained. This is not a defense against concurrent filesystem substitution, compromise of every trust anchor, or a compromised interpreter. Passing frozen hashes does not establish mathematical truth. The verifier validates specified scope fields and is not a complete semantic checker for every prose or metadata field.

The public receipts contain symbolic member names and hashes, never execution-time temporary paths. `SOURCE_RECHECK.json` contains no PDF text, images, extracts, corpus records, or dataset contents. The corrected archive contains only authored report/code/metadata and replay tooling. The public audit directory is explicitly inventoried by its delivery manifest; private inspection material and the source-bearing literal diff are excluded.
