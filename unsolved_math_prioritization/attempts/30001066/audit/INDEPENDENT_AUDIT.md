# Independent adversarial audit: isolated line transversals

Problem 30001066, OWR-2090-019, rank 819. Audit date: 2026-10-06.

## Verdict

**Accept the mathematical partial result. Do not classify the original bounded-size question as solved.** The construction gives a minimal pinning of size `3d-3` by compact, full-dimensional, strictly pairwise-disjoint boxes for every `d>=2`. Consequently the numerical `2d-1` bound for balls does not extend to arbitrary disjoint convex sets when `d>=3`. Existence of some finite bound `h(d)` for that larger class is not established or refuted here.

The conditional `4d-4` theorem is also valid under its stated trivial-first-order-cone hypothesis. Pinning alone does not imply that hypothesis.

**One package-integrity correction is required:** the frozen directory verifier exempts everything under `__pycache__`. It accepts unlisted synthetic PDF and binary payloads. This does not affect the mathematics, and the actual frozen ZIP contains only its ten declared authored/metadata files. A separate strict verifier and minimal patch close the inventory gap. Earlier archives remain unchanged; this review is explicitly bound to the separately identified public derivative.

## Exact input and provenance

Reviewed public author derivative: `ISOLATED_TRANSVERSAL_30001066_AUTHOR_PUBLIC_SAFE_DERIVATIVE.zip`.

- Bytes: `17217`
- SHA-256: `be4dabaf22028561681c76c353bd537d0b240cfd67d52aa7ed9531f435905034`
- Manifest SHA-256: `138276ddbc5873201ae34791b35bb6a44575172074c8efaf4c43b5e4c4c1c363`
- Version: `1-reconstructed`

This is the public editorial derivative of a reconstructed author packet, not a claimed byte-identical restoration of an earlier freeze. An editorial metadata redaction leaves the mathematical proofs, geometry, verifier code, and author results unchanged. This re-bound audit independently checked the actual public derivative ZIP and reran the complete suite from disposable relocated copies. No remote mutation, publication, or third-party outreach was performed.

The three complete catalog/research files became available during this review. Fresh full-byte and full-target-record replay passed; see `CORPUS_REPLAY.json`. This new evidence is separate from the unchanged author's historically qualified metadata. Catalog rank, problem ID and OWR identifier match. The target research report is absent. No corpus content is included in this audit package.

## Independent geometric proof

Write `k=d-1`. For `j=0,...,k-1`, give the three boxes in block `j` the longitudinal intervals `[6j,6j+1]`, `[6j+2,6j+3]`, `[6j+4,6j+5]`. Their distinguished coordinate `x_(j+1)` has intervals `[0,1]`, `[-1,0]`, `[0,1]`; every other transverse interval is `[-1,1]`.

### Valid convex bodies and actual, varying-height intersections

Every interval has positive length. Therefore each box is compact, convex and full-dimensional. Every pair of longitudinal intervals is separated by a gap of at least one. The closed bodies, including their boundaries, are strictly disjoint.

A line with constant longitudinal coordinate cannot meet all the boxes. Thus any common transversal is globally expressible as `(a+b*t,t)`. For one block, let `t0<t1<t2` be its actual intersection heights. They need not be slab centers and can be endpoints. The relevant affine coordinate `f(t)` is nonnegative at `t0,t2` and nonpositive at `t1`. Its interpolation formula writes `f(t1)` as a strictly positive weighted average of `f(t0)` and `f(t2)`. Hence all three are zero. An affine function with two distinct zeros is identically zero. This applies independently to each transverse coordinate. The axis is therefore the unique global transversal.

This argument does not replace existential box intersection by a fixed-center linear constraint. The independent code uses exact rational clipping of the full permissible height interval. A separate test checks a line that meets a closed box only at a slab endpoint while failing its center condition.

### Continuous minimality, all dimensions

Delete the role `r` box of block `j`; set `s=6j`. Keep every transverse coordinate zero except the distinguished one, and set that coordinate to `epsilon*f_r(t)`, with

- `f_0(t)=t-s-4`
- `f_1(t)=1`
- `f_2(t)=s+1-t`

For all real `0<epsilon<=1/(6k+2)`, the values at each retained box's slab midpoint lie in that box. In the same block, the relevant values before scaling are `(-3/2,1/2)`, `(1,1)`, or `(1/2,-3/2)`, respectively. For every other block, the moving coordinate is an unrestricted transverse coordinate, and throughout `0<=t<=6k-1` its absolute value before scaling is less than `6k+2`. All remaining coordinates are zero. These are simultaneous intersection points in actual boxes, not independent necessary inequalities.

On the omitted slab, the moving coordinate has the strictly wrong sign: `f_0` and `f_2` range from `-4` to `-3`, while `f_1=1`. Thus every positive parameter also misses the omitted box. These distinct affine lines converge to the axis in the ordinary line chart as `epsilon` decreases to zero. The construction therefore destroys isolation after every one-box deletion. Any proper subfamily is contained in such a deletion and inherits its motion.

The near-axis graph chart is an open chart of unoriented affine-line space; choosing the representative directed toward increasing `t` does not change the underlying line. No orientation reversal, distant component, or parameterization-only motion enters the argument. The proof works for arbitrary `k>=1`; finite computational tests are supplementary.

## Conditional first-order theorem

For `m=2d-2`, suppose finitely many differentiable necessary body constraints `g_i(u)>=0` vanish at zero, and the common feasible cone of their differentials is `{0}`. Their gradients positively span `R^m`, by finite-dimensional separation.

A minimal positive dependence has support `S` with `|S|=r+1`, where `r=dim(span S)`: a larger nullspace would allow a positive dependence to be perturbed until one coefficient becomes zero. Also `cone(S)=span(S)`. Projecting the other generators to the quotient of dimension `m-r`, and inducting, selects at most `2(m-r)` further vectors. The total `r+1+2(m-r)` is at most `2m`. This independently verifies the positive-spanning lemma used by the author.

Select the corresponding inequalities. If nonzero feasible parameters converged to zero, their normalized directions would have a subsequence converging to a unit vector feasible for all selected differentials, a contradiction. At most `2m=4d-4` associated bodies therefore isolate the line. Multiple selected inequalities from one body only reduce the body count.

The proof uses the additional hypothesis essentially. Higher-order isolation can leave a nontrivial first-order cone, and facet contacts may produce a disjunction. Neither the abstract quadratic warning nor the conditional theorem supplies a general geometric reduction. The five attempted approaches correctly expose these gaps; none resolves the unrestricted problem.

## Primary-source and problem-scope checks

The OWR contribution's ball theorem uses `2d-1`; its following paragraph asks about broader classes, without explicitly proposing the identical number for all convex bodies. The restored catalog adds that number as an illustrative candidate. The accepted result refutes that numerical extension, not the broader request for some bounded-size witness. [Goaoc, OWR Report 44/2008, printed p. 2543](https://doi.org/10.4171/owr/2008/44).

The known six-cylinder example is credited to Guenter Rote. In the printed coordinates, the two same-side cylinders of a block touch as closed sets. The source does not claim strict disjointness there. The present boxes establish separation and compactness independently; neither this audit nor the author claims novelty for the lower-bound phenomenon or coordinate-block construction. [Cheong et al., section 6, inspected 2006 preprint](https://www.ens-lyon.fr/LIP/Arenaire/SYMB/teams/vegas/vegas2.pdf).

Aronov et al.'s bound six concerns disjoint polytopes in three dimensions with no facet coplanar with the pinned line. The boxes here have coplanar facet-contact segments. Their unbounded examples allow intersecting polytopes; neither statement answers the unrestricted disjoint-body question. [Aronov et al., Theorem 1 and section 7](https://arxiv.org/abs/1002.3294).

All three primary PDF byte counts and hashes independently match the author's fresh retrieval metadata. Relevant text and rendered pages were inspected. Limited current searches located no later resolution; that negative search is not a proof of present-day open status. Details and public URLs are in `SOURCES.json`; no PDFs, extracts, or screenshots are distributed.

## Confirmed inventory defect and correction

In the frozen `verify_package.py`, lines 42-43 skip every path with a `__pycache__` component after merely excluding symlinks. A synthetic `__pycache__/unexpected-source.pdf` and an arbitrary binary payload therefore pass the supposed exact-inventory check in both normal Python and `-O`. The mathematical verifier is unaffected.

`verify_package_strict.patch` removes the exemption. Its tested clean-tree workflow uses `PYTHONDONTWRITEBYTECODE=1` or `python -B` so that running tests does not create unmanifested local bytecode. When applying the patch to a derived packet, regenerate its manifest and identify it as a new version; do not relabel the frozen archive.

Alternatively, `strict_inventory.py` validates the unchanged ZIP directly, checks exact members before reading payloads, rejects duplicate/nested/unlisted members and symlinks, and optionally pins the external archive digest. Directory checking is also fail-closed. Manifests establish internal consistency; the external SHA-256 establishes which exact reviewed archive is being checked.

The patch was applied only to disposable test copies, with their derived manifests recomputed. Clean replay passed and synthetic cache/root additions were rejected under normal and optimized Python. See `PATCH_REPLAY.json`.

## Independent replay coverage

- Independent exact geometry in dimensions `2,3,4,5,8,12,16,24,32`: 16,944 whole-real-parameter interval checks and 34,470 exact line/box clipping checks.
- A 625-line rational near-axis grid: only the axis meets all six boxes; this is supplementary, not the uniqueness proof.
- Author `verify_package.py`, `verify.py`, and `test_verifier.py`: fresh normal and optimized replay from a relocated directory.
- Author generator/verifier at the supported upper implementation dimension 64: normal and optimized replay. The written theorem has no implementation dimension cap.
- Thirty independently selected malformed/semantic mutations rejected per mode. Four valid transformed certificates accepted per mode: permuted rows, smaller motion interval, translated slabs, and longitudinal rescaling.
- Eighteen independent strict-inventory mutations rejected, including the original cache bypass, duplicate ZIP members, traversal names, manifest corruption, and a directory symlink.
- The whole independent suite was rerun under optimized Python from another relocated directory. The normal and optimized result receipts remain separate.

## Acceptance boundary

Accepted: the strict compact-box lower bound, genuine continuous minimality, and the conditional first-order upper bound. Rejected: treating this as a full solution, treating the original directory checker as a sufficient clean-archive gate, treating finite tests as an all-dimensional proof, or claiming a new lower-bound phenomenon. Fresh corpus identity is now verified, without retroactively changing the author freeze's historical provenance.
