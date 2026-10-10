# Independent audit: rank 549 / 30000552 / OWR-1319-022

## Verdict

**ACCEPT.** The frozen reconstruction gives a valid negative answer to the original complete-length-space question. The proposed classification `already_solved`, with one substantive verification turn (`1/5`), is justified by the published prior construction. No mathematical correction or author-package revision is required. This is an independent assistant audit, not external peer review and not a new-result claim.

The audit was performed on 2026-10-04 UTC by a reviewer uninvolved in preparing the author package. The review used the eight frozen public files and the locally available primary sources. No remote repository operation, live catalogue request, source upload, or author-file modification was performed. The public artifact hashes were checked before and after review.

## Frozen object and reproducibility

- Author manifest SHA-256: `205adc5c3b51ca9ee4b362decfdc24eeafb81578b13641c51f9166cfc06abe65`
- Proof SHA-256: `14a0c2af3f42910818a20c5ce4aa752ff780576a08841563dcef6708454491f6`
- The author manifest contains seven content hashes; its own hash identifies the eighth public file. All entries passed `sha256sum -c SHA256SUMS`.
- `python3 verify.py --check checks.json` passed and reproduced exactly 16,003 assertions. The output is retained in `author-replay.json`.
- `independent_checks.py` uses exponential coordinates and exact rational arithmetic to cross-check the normalization, the actual lattice, the pullback horizontal basis, and the coordinate change. Its receipt is `independent-results.json`.
- `FROZEN_MANIFEST.json` records all eight author files. This audit directory has a separate `SHA256SUMS`; it does not alter or extend the author's frozen manifest.

The finite controls are supplemental. None is treated as proof of completeness, the length property, a universal area inequality, an all-pairs limit, or unboundedness.

## Primary-source alignment

The original question was read in the complete relevant problem-session entry and visually checked on printed p. 2048 of Oberwolfach Report 33/2006, PDF page 58. It concerns two metrics on the same complete length or coarse-length space, one group acting cocompactly by isometries for both, the limit of their ratio as the first distance diverges, and whether the additive discrepancy is bounded. There is no additional Riemannian hypothesis or requirement concerning all possible rough isometries.

Source: [Oberwolfach Report 33/2006](https://doi.org/10.4171/OWR/2006/33). The locally inspected PDF has SHA-256 `7d804faae085643743cee507a9d911337d9f4bc5ab5a77e67811e2d17cd891f7`.

The full relevant counterexample, Section 8.3(A), was read and visually checked across printed pp. 724–725 of Emmanuel Breuillard, *Geometry of locally compact groups of polynomial growth and shape of large balls*, Groups, Geometry, and Dynamics 8 (2014), 669–732. The title page, its definition of the sub-Finsler metric in Section 2.1, Remark (2) after Theorem 6.2, and reference [7] were also inspected. Section 8.3(A) uses the group R × H3(R), the standard lattice, horizontal bases (V,X,Y) and (V+Z,X,Y), their ℓ¹ norms, and the same central-coordinate shear and witness used in the frozen proof.

Source: [Breuillard, DOI 10.4171/GGD/244](https://doi.org/10.4171/GGD/244). The locally inspected published PDF has SHA-256 `2609b126b535ae674438c8b4be3dd613d297bf976db5dda4929c760ac68eb0fc`.

The paper's source proof obtains the asymptotic equivalence from a general theorem. The reconstruction supplies a direct square-root bound instead; this is sufficient and removes that theorem as a necessary proof dependency. Reading the theorem's statement and remark is not represented here as auditing the entire general theorem. No claims from Sections 8.3(B), 8.3(C), or the stronger subsequent rough-isometry result are needed.

## Adversarial mathematical checks

### 1. Coordinates, signs, and the ℓ¹ constant

The reconstruction uses matrix coordinates with product

    (x,y,z)(a,b,c) = (x+a,y+b,z+c+xb).

The left-invariant horizontal fields are X = ∂x and Y = ∂y+x∂z. Their bracket is Z = ∂z, with no factor of two. A horizontal path consequently satisfies z′=xy′, and its prescribed ℓ¹ control length is the integral of |x′|+|y′|.

The source's first-kind exponential central coordinate is ζ=z−xy/2. Under this change the product has central term (xb−ya)/2, and horizontality is ζ′=(xy′−yx′)/2. On a closed projected path, the integral is still ∫x dy, since ∫d(xy)=0. Thus the convention changes neither the central endpoint nor the constant in the central distance. The shear ζ↦ζ−v is exactly z↦z−v in matrix coordinates.

For a horizontal path to (0,0,u), its projection is closed. Set A=Var(x), B=Var(y), and Rx=max(x)−min(x). Closure implies A≥2Rx. After subtracting the midpoint of the x-range inside the integral, one obtains

    |u| ≤ Rx B/2 ≤ AB/4 ≤ (A+B)²/16.

This reasoning applies to arbitrary admissible piecewise C¹ paths, including self-intersections, varying speeds, zero-width projections, and either orientation. It uses total variation, not an unjustified simple-Jordan-curve isoperimetric claim. Therefore the control length is at least 4√|u|. An axis-aligned square with side √|u|, oriented according to the sign of u, has horizontal lift ending at that central point and length 4√|u|. Hence

    D(e,(0,0,u)) = 4√|u|

holds for every real u. A Euclidean horizontal norm would give a different constant, but it is not the norm used here. The ℓ¹ normalization in the source and frozen proof matches exactly.

### 2. Genuine finite metrics and topology

Horizontal motion first in x and then in y reaches (x,y,xy). A translated central square then reaches (x,y,z), establishing

    D(e,(x,y,z)) ≤ |x|+|y|+4√|z−xy|.

This constructs a finite path for every endpoint. Path reversal preserves admissibility and length; concatenation supplies the triangle inequality; and left translation preserves z′=xy′ and the control length. These facts establish symmetry, the triangle inequality, and left invariance.

Every admissible path from the identity with control length L has |x|+|y|≤L and |z|≤L². Taking an approximating sequence of lengths yields these endpoint bounds with L replaced by D. Thus zero distance forces all three coordinates to vanish. Conversely, the explicit upper bound tends to zero when the coordinates tend to zero. These two implications establish the Euclidean topology at the identity; group translations establish it at every point. There is no reliance on an assumed pre-existing metric or on Chow's theorem to prove separation or topology.

The path class used in the reconstruction suffices for its own construction. It also agrees with the standard source normalization: smooth horizontal paths are admissible; piecewise C¹ controls may be approximated by smooth controls in their integral norm, and the vanishing endpoint error can be corrected at vanishing cost using the displayed finite-path upper bound. No regularity convention invalidates the identified example.

### 3. Properness, completeness, and the length property

A closed D-ball is Euclidean closed, by the established equality of topologies, and lies in a Euclidean bounded set |x|+|y|≤R, |z|≤R². It is therefore compact. Every D-Cauchy sequence lies in such a ball and has a D-convergent subsequence, which makes the full Cauchy sequence converge. This proves both properness and completeness without assuming existence of a minimizing path.

For a horizontal admissible path, the D-length of each restricted segment is at most its control length; the supremum over partitions has the same upper bound. For every pair of endpoints and positive ε, the defining infimum gives such a path of control length below D+ε. All continuous paths have metric length at least their endpoint distance. The two inequalities establish that D is a length metric. They do not require the control length to have been proved equal to the metric length of every horizontal path.

The ℓ¹ product metric d1 on R × H is finite, complete, and has the product Euclidean topology. Joining the real coordinates and then following an almost-minimizing H-path proves its length property. Its balls are also compact, as closed subsets of a bounded real interval times a compact D-ball. Pullback through the bijective homeomorphism F preserves completeness, properness, and the length property, giving the same properties for d2. The frozen proof explicitly establishes the properties required by the question; product properness is an additional consequence.

### 4. The shear and the common group action

Let F(v,x,y,z)=(v,x,y,z−v). The v-coordinates add independently of the Heisenberg cross term, so F(gh)=F(g)F(h). Its inverse adds v. Thus the pullback d2(p,q)=d1(Fp,Fq) is invariant under the same original left translations as d1:

    d2(ap,aq) = d1(F(a)F(p),F(a)F(q)) = d2(p,q).

This is stronger than having two unrelated cocompact actions. At the Lie-algebra level, F sends V+Z to V and fixes X,Y. It therefore pulls the first ℓ¹ horizontal metric back to the second source metric, with the correct shear sign.

The lattice used in the proof consists of integer matrix-coordinate quadruples. It is a subgroup, is discrete in the common topology, and F and F⁻¹ both preserve it. In first-kind coordinates its central coordinate may be a half-integer; the set of all integer first-kind quadruples is generally not a subgroup. The frozen proof correctly avoids that common coordinate error. Lattice preservation by F is true, although left invariance alone already suffices to prove the common action preserves both metrics.

For any g, the specified choices m=floor(v), a=floor(x), b=floor(y), c=floor(z−a(y−b)) give

    γ⁻¹g = (v−m,x−a,y−b,z−c−a(y−b)) ∈ [0,1)⁴.

All four coordinates, including the noncommutative correction to z, are correct. The compact set [0,1]⁴ consequently has translates covering M, giving cocompactness in both metrics. Compact K1,K2 can intersect through only lattice elements in the compact set K2K1⁻¹; the integer lattice has finitely many such elements. The additional assertion that the action is proper is valid as well.

### 5. Uniform quantifiers over identical pairs

For a fixed g=(v,x,y,z), the H-endpoints used by the two distance formulas differ by the central element (0,0,−v). The reverse triangle inequality and the exact central distance give

    |d1(e,g)−d2(e,g)| ≤ 4√|v|.

Both distances are at least |v|. Applying their common left invariance with g=p⁻¹q gives, for every pair,

    |d1(p,q)−d2(p,q)| ≤ 4√min(d1(p,q),d2(p,q)).

In particular, if r=d1(p,q)≥64 and s=d2(p,q), then s≥r−4√r≥r/2. Therefore

    |r/s−1| ≤ 8/√r.

For any ε>0, choosing R≥max(64,(8/ε)²) gives this bound uniformly whenever d1(p,q)≥R. Replacing ≥ by > as needed gives the strict epsilon formulation. The denominator is positive for distinct points, and the bound forces the second metric to diverge whenever the first does. This establishes exactly the original limit; no selected-ray, orbit-only, or asymptotic-cone substitution is involved.

### 6. Unbounded discrepancy and the isometry objection

For t>0, set gt=(t,0,0,t). The shear sends gt to (t,0,0,0), so

    d1(e,gt)=t+4√t,     d2(e,gt)=t.

Thus the discrepancy on the very same pair (e,gt) is 4√t. Taking positive integers t gives unbounded discrepancy on the lattice itself. The real-coordinate contribution cannot cancel the central excursion because the first product metric is an ℓ¹ sum; it is removed in the second metric by precisely the chosen shear.

F is an isometry between the two metric spaces. That does not contradict or weaken the counterexample: the original question compares the two numerical distance functions on identical pairs in the already fixed space. It does not ask whether some other map produces a bounded-error or exact isometry. The frozen proof explicitly observes this distinction and makes no unsupported stronger rough-isometry claim.

## Findings and limits

No blocker, incorrect constant, missing hypothesis, incorrect universal quantifier, or necessary unproved external theorem was found. No author-package edits are requested.

The published year, venue, DOI, construction, original question, and page references were independently checked against the local primary documents. The exact publisher day-of-publication assertions, current catalogue HTTP response, current catalogue annotations, and historical repository searches were not repeated. They are author-reported provenance, not fresh results of this audit. The queue rank/ID/code mapping is the supplied assignment and recorded gate mapping; no new remote queue read was made. These scope limits do not affect the counterexample's validity or the existence of its 2014 published source.

The finite Python scripts are not a formal proof assistant or a proof of universal analytic claims. This audit's acceptance rests on the mathematical arguments above and their correspondence to the exact primary question. The turn count records one substantive prior-resolution verification, not five proof attempts. Integration, queue mutation, publication, merge, and any remote checks remain outside this audit's actions.

Only original audit prose, program text, hashes, and machine-readable receipts are included in this directory. The primary-source PDFs, page images, and extracted source text remain excluded.
