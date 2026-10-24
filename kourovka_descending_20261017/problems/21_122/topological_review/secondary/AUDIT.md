# Independent secondary audit: metrizable and inverse-limit reductions

UTC: 2026-10-24T23:19:37.412915+00:00

Frozen input: `topological/METRIZABLE_REDUCTION_AND_OBSTRUCTION.md`, SHA256
`a7dafdf2d8cd189c64c7924c29104cf6b80e391199a075e4d1367951dcbd8661`.

**PASS for sections 1–2 only.** These supporting reductions were independently
derived before reading the frozen note, then compared against it. No other
family conclusions were read. This audit establishes neither a solution of
21.122 nor originality. Audit completion estimate: 100%; no discovery percentage
or publication approval is inferred.

## 1. The quotient really has a countable local basis

Let `w` use finitely many variables and let `X=G_w` be infinite. Choose distinct
`x_i in X`. For every `i<j`, residual finiteness in the profinite topology gives
an open normal subgroup `U_ij` separating `x_i` and `x_j`. Enumerate these
countably many subgroups, put `N_n=intersection_(k<=n) U_k`, and put
`N=intersection_n N_n`. All `N_n` are open normal and `N` is closed normal.

The induced homomorphism

`G/N -> product_n G/N_n`

is continuous and injective. Its domain is compact and its codomain Hausdorff,
so it is a homeomorphism onto its image. The countable product of finite
discrete spaces is metrizable and second countable. Because `N_n` decreases,
the finite intersections of coordinate identity neighborhoods reduce to the
single neighborhoods `N_n/N`. Hence these form a countable local basis.

Equivalently, if `V` is any open neighborhood of `N` in `G`, then some `N_n`
is contained in `V`: otherwise the decreasing nonempty compact sets
`N_n \ V` would intersect in `N \ V`, a contradiction. Thus the basis claim
does not merely assume that a countable intersection is sufficient.

The images of the selected `x_i` stay distinct. Every tuple in `G/N` lifts
coordinate by coordinate to `G`, and evaluation commutes with homomorphisms.
Consequently the quotient sends `G_w` **onto** `(G/N)_w`. This latter set is
infinite and its cardinality is at most `|X|`.

## 2. The cardinality conclusion uses no continuum hypothesis

The image `Y=(G/N)_w` is compact metrizable, since it is the continuous image
of the finite power `(G/N)^d`. Every uncountable compact metrizable space has
cardinality exactly continuum. Here is an elementary proof of the needed
lower bound. With respect to a countable basis, delete the union of all basic
open sets whose intersection with `Y` is countable. Only countably many points
are deleted. If `Y` was uncountable, the remaining closed set `P` is nonempty.
It has no isolated point: an isolating neighborhood in `P` would meet `Y` in
at most the countable deleted set together with one point, contrary to the
non-deletion of that point. Recursive binary splitting in this perfect compact
metric set gives disjoint nested compact neighborhoods with diameters tending
to zero and injects `{0,1}^N` into `P`. A countable basis also gives the upper
bound continuum for the cardinality of a metrizable separable space.

Therefore, if `|X|<2^aleph_0`, then the infinite set `Y` must be countably
infinite. This is a conditional reduction; it does **not** construct an actual
word map with countably infinite image. Conversely, such an image in a
countably based profinite group would itself violate the target implication.
Nothing here makes the quotient topologically finitely generated.

## 3. Exact word images in a finite inverse sequence

Let `Q=lim Q_n`, where all `Q_n` are finite groups and all bonding maps are
surjective. Write `Y_n=(Q_n)_w`. Every projection `Q -> Q_n` is onto: finite
compatible initial segments can be lifted from their highest level, and
compactness of the product supplies an infinite compatible sequence.
Likewise, every restricted bonding map `Y_(n+1) -> Y_n` is onto, by lifting a
tuple realizing any prescribed word value.

Evaluation immediately gives `Q_w subset lim Y_n`. Conversely, for a coherent
sequence `(y_n)`, define

`C_n={g in Q^d : w(g) projects to y_n in Q_n}`.

These are closed, nonempty (lift a realizing tuple in `Q_n`), and nested
(coherence of `y_n`). Compactness of `Q^d` gives a point in their intersection.
Its word value realizes `(y_n)`. Thus the frozen equality

`Q_w = lim (Q_n)_w`

is correct as an equality of subsets of `Q`.

**Essential trap checked:** the sets of tuples realizing `y_n` need not have
surjective transition maps. For `w(x)=x^2`, the quotient `C4 -> C2`, and the
identity target, the roots are `{0,2}` in additive `C4` and `{0,1}` in additive
`C2`; the first set projects only to `{0}`. The frozen argument correctly uses
nested compact subsets of `Q^d`, not this false tuple-lifting shortcut.

## 4. Finite-image boundedness is exactly equivalent

The projections `Q_w -> Y_n` are onto, so finite `|Q_w|=M` bounds every
`|Y_n|` by `M`. Conversely, if all `|Y_n|<=M`, any `M+1` distinct points of the
limit would be distinguished pairwise at finitely many coordinates. At the
maximum of these finitely many levels their images would all be distinct,
contradicting the bound. Equivalently, the nondecreasing integer sequence
`|Y_n|` eventually stabilizes, and all later surjective transition maps of
word-value sets are bijective. The limit is finite with the eventual
cardinality. This is about value sets, not the subgroup they generate.

Unbounded finite image sizes therefore mean an infinite inverse-limit value
set. They alone do not imply continuum cardinality for arbitrary inverse
systems of finite sets. For example, take `Y_n={0,...,n}`, fix each old label,
and send the new label `n+1` to zero. An infinite branch is either the zero
branch or switches once from zero to some positive label `k` and stays there.
There are countably many branches, despite `|Y_n|=n+1`. This control is not a
word-map counterexample.

## Reproduction and limits

`independent_controls.py` checks eight stages of the square-value inverse
sequence `C_(2^n)`, the non-surjective tuple-fiber counterexample, and eleven
thin-branch prefix extensions through depth twelve. The run passes. These
finite controls falsify a tempting shortcut; the unbounded statements rest
on the proofs above, not a finite search.

No substantive defect was found in the assigned frozen sections. This audit
does not review sections 3–4, the literature ledger, or a hypothetical proof
of the remaining fixed-word branching assertion. The open mathematical step
is still to exclude a countably infinite genuine word image, rather than to
establish this topological reduction.
