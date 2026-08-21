# Second adversarial review: global bridge/cut/localization

Date: 2026-08-09

Write scope: `reviews/global_bridge/` only

Definitions lock SHA-256:
`c3382650fa004d90b2122aff1c95524590b31e436d77d4b804293184aa925b09`

Bridge/cut proof SHA-256:
`1b821810c50769bca4eaa719b79b2627b03cc821e97ee2ba5f4f32c929be64be`

Published cut certificate SHA-256:
`da47733278a74690f6a55bccb1aec2771cc14960a286f45e526461f45aca41b5`

Global draft SHA-256 at final mathematical audit:
`a7defc76948b44f2afafc9184548469e6d38b1511e7aaca327e09a73b9134f82`

## Executive verdict

The scoped bridge/cut package passes.  I found no counterexample to its exact
incidence fiber, slice, no-compensation, or pointwise cut theorem.  A fresh
verifier that imports none of the package implementation reconstructed all
147 nonordinary published graph witnesses, all 77 endpoint cases, all 204
strict one-active minors, and the complete two-active symbolic crossing.

The global bridge/cut skeleton also passes, with two important distinctions:

1. The package writes down only
   `Cut(source) subset Cut(target)`.  The reverse inclusion is nevertheless
   valid under the locked definition of source-relative containment and is
   required for the equality used in `GLOBAL_THEOREM_DRAFT.md`.
2. A finite target-role union need not contain the *entire* focal source germ
   in one member.  What is true, and sufficient, is that one member contains a
   source-relative open full-dimensional *subgerm*.

The current global draft already uses a sufficiently small common interval of
effective bridge scales.  That is correct.  The stronger phrase “arbitrary
positive effective scales,” present in an earlier draft during this review,
is false for a fixed sliced local point and is not needed.

The final classification theorem remains **UNRESOLVED** because its bounded
local atlas, arbitrary-word coherence, and root-reduction dependencies are
outside this package and are still listed as unverified dependencies.  This
is not a bridge/cut failure.

## Status ledger

| Claim | Status | Review conclusion |
|---|---|---|
| Exact zero-sum bridge fiber is the full incidence action | **VERIFIED** | Sectorwise positive rank-one uniqueness and an independent log-linear kernel replay agree. |
| Character scales collapse to one scale per incidence | **VERIFIED** | The six `Aut(Z_2 x Z_2)` maps act transitively on the three nonzero characters. |
| Local stabilizers and exclusion of unmarked bivalent factors | **VERIFIED** | The only nontrivial unmarked degree-two theta is `K4-e`, excluded from nonvacuous `S_TC`. |
| Positive analytic incidence slices | **VERIFIED** | Marked anchors give an identity exponent matrix; unmarked pair anchors have full rank. |
| Physical bridge multipliers are identifiable | **FALSE** | The equal-product fixture has physical multipliers `1/2` and `25/72`. |
| Every positive effective scale is physical at a fixed slice point | **FALSE** | With unit normalizers, `j=x`; `j=2` is positive but violates `0<x<1`. |
| A sufficiently small common effective-scale interval glues | **VERIFIED** | Positivity of all incidence representatives gives a uniform nonempty interval after shrinking the local germs. |
| Full strong completions may induce weak selected marginals | **VERIFIED** | The compiler checks strongness on the dummy-restored full graph and imposes no strongness claim on the selected tensor. |
| Dummy completion leaves imply selected weakness | **FALSE** | Dummy leaves encode omitted roles at character zero; their presence does not classify the reduced selected marginal. |
| Three-port endpoint dichotomy, including the ordinary endpoint | **VERIFIED AFTER CORRECTION** | In the projective central-signature normalization the counts are `67` with $\Delta>0$, `2` with $\Delta=0,\Gamma>0$, `7` with $\Delta=\Gamma=0$, plus the ordinary record.  Restoring the positive central factor makes the seven nonordinary weak cases strict in the physical tensor. |
| One-active strict noncut minors | **VERIFIED** | All 204 minors independently reconstruct and have the certified strict open-cube sign. |
| Two-active crossing | **VERIFIED** | Twenty minors up to sign regenerate; `f_1,...,f_4` and all three identities have zero remainder. |
| Pointwise rank-at-most-four iff cut | **VERIFIED** | True cuts have four rank-one blocks; every noncut has a strict block minor at every open point. |
| `Cut(source) subset Cut(target)` under `source preceq target` | **VERIFIED** | This is the direction stated in the package. |
| `Cut(target) subset Cut(source)` under `source preceq target` | **VERIFIED** | The target cut equation holds on the shared source-open set and contradicts pointwise source-noncut rank. |
| Equality of reduced labelled bridge trees | **VERIFIED** | Both cut inclusions hold, and unmarked bivalent components are absent. |
| Localization without continuous target parameter choice | **VERIFIED** | Intrinsic extraction is a function of the distribution, not of a selected target preimage. |
| Entire focal source germ lies in one finite-union member | **FALSE** | A finite cover only forces a full-dimensional member, not whole-germ containment. |
| Some source-open focal subgerm lies in one finite-union member | **VERIFIED** | Finite semialgebraic dimension plus the regular source stratum gives nonempty relative interior. |
| Cross-blob compensation after cut equality | **VERIFIED** | A distant factor cannot change the intrinsically extracted focal projective orbit. |
| Simultaneous gluing of compatible local `T` germs | **VERIFIED** | Conditional on the stated local regular projective germs and valid `T` endpoints; bridge parameters are independent. |
| Final global classification in the candidate draft | **UNRESOLVED** | Still conditional on separate local-atlas, probe-coherence, and root-reduction gates. |

## 1. Exact incidence kernel with the zero-sum constraint

Let `G=Z_2 x Z_2`.  For a bridge-component tree `T`, a component tensor is
defined only on

\[
D_v=\{(g,h):\mathop\oplus_{i\in X_v}g_i\oplus
                  \mathop\oplus_{e\ni v}h_e=0\}.
\]

For a global physical assignment of total zero, `h_e` is the character total
on either side of `e`; the two totals are equal because every element of `G`
is self-inverse.  The contraction is

\[
\Gamma(P,x)(g)=\prod_v P_v(g_v,h_v)
                 \prod_e x_e^{[h_e\ne0]}.
\]

Suppose `Gamma(P,x)=Gamma(Q,y)`.  Cut the component tree at one bridge `e`.
For each fixed separator sector `h`, the flattening is a positive rank-one
matrix

\[
L_e^P x_e^{[h\ne0]}(R_e^P)^T
=L_e^Q y_e^{[h\ne0]}(R_e^Q)^T.
\]

Leaf support is exactly what makes both the row and column index sets nonempty
for every `h`.  In particular, when `h` is nonzero, one must put total `h` on
*both* sides.  Setting the complementary side to zero would violate global
zero-sum conservation and is not used.  Positive rank-one uniqueness gives

\[
L_e^Q=c_e(h)L_e^P.
\]

The all-zero entry gives `c_e(0)=1`.  Simultaneous JC symmetry under all six
group automorphisms gives a common value `c_e` on the three nonzero sectors.
Expanding subtree contractions from the leaves toward a chosen root gives,
at every component,

\[
\frac{Q_v}{P_v}
=c_e(h_e)\prod_{f=vw}
  \left(c_f(h_f)^{-1}(x_f/y_f)^{[h_f\ne0]}\right).
\]

Assigning the parent- and child-endpoint factors separately yields precisely

\[
Q_v=P_v\prod_{e\ni v}a_{v,e}^{[h_e\ne0]},
\qquad
y_e=\frac{x_e}{a_{u,e}a_{v,e}}.
\]

The reverse implication is direct cancellation.  This proves the complete
positive fiber.  The independent verifier also built the logarithmic design
matrix for five different leaf-supported component trees and found
`ker(Gamma)=im(incidence)` exactly in every case.  Removing leaf support
created two additional kernel dimensions, as it should.

## 2. Stabilizers and analytic slices

For a local incidence action, a stabilizer satisfies

\[
\prod_{e\ni v}a_e^{[h_e\ne0]}=1
\quad\text{for every allowed local zero-sum assignment.}
\]

If the component has a physical block, put one nonzero `s` on that block and
on one chosen incidence.  This forces that incidence scale to one.  If it has
no physical block, put `s` on any pair of incidences; then `a_i a_j=1`.
Consequently:

- `m>=1`: trivial stabilizer;
- `m=0,d>=3`: trivial stabilizer;
- `m=0,d=2`: `(t,t^{-1})`;
- `m=0,d=1`: the whole one-dimensional action.

The actual reduced bridge tree has no last two cases.  An ordinary unmarked
component has degree three, a cycle has at least three ports, and a simple
theta has at least two ports.  Equality at two ports forces path lengths
`(1,2,2)`, namely `K4-e`; every reticulation placement violates the locked
nonvacuous strong criterion.  Thus every unmarked retained component has
degree at least three.

For a marked component, the one-physical/one-incidence anchors transform one
at a time, so their log-exponent matrix is the identity.  For an unmarked
degree-`d` component, use pairs

\[
(1,2),(1,3),(2,3),(1,4),\ldots,(1,d).
\]

The first three rows have determinant `-2`, and each later row adds one new
coordinate.  The matrix has rank `d`; the positive square-root formulas give
a unique real-analytic normalizer.  Positivity keeps every denominator and
root away from a branch singularity.

The intrinsic edge coordinate is an *effective* scale after these endpoint
normalizations.  It is not a physical edge multiplier.  All subsequent
arguments must use local positive intervals in the effective coordinate, not
claim global recovery of a physical `x_e`.

## 3. Full strong factors versus selected marginals

This distinction survives the audit and is essential.

The three- and four-port tensors in the cut proof are selected marginals of a
full `S_TC` factor.  Such a selected marginal can be weak after the broader
`red_*` reduction.  The compiler therefore restores omitted roles before it
tests the topology:

- an unselected reticulation-sink port is represented by a dummy leaf;
- an omitted repair occupancy on an otherwise empty segment is represented
  by at most one dummy leaf;
- a marginalized incoming boundary is represented by a dummy incoming leaf;
- every dummy character is set to zero when the selected tensor is compiled.

The rooted and rooting-independent strong tests are applied to this *full
dummy-restored graph*.  They are not applied to the selected reduced object.
Additional omitted ports on an occupied segment duplicate a descendant-mask
row and enter only through a serial product; on an empty segment, one dummy is
enough to retain the occupancy condition.  Hence this compression preserves
the selected tensor and the existence of a full strong completion.

The independent replay checked 147 nonordinary full witnesses; 129 contain
at least one dummy leaf.  Every one passes the full rooted, LSA, narrow
standard, and rooting-independent `S_TC` tests, and every one reconstructs
its published selected tensor.  No strong/weak label was assigned to a
selected marginal.  In particular, dummy presence is not evidence that the
selected marginal is weak.

## 4. Pointwise cut-rank characterization

### True cuts

Order a Fourier flattening by the total character `h` on one side.  It is
block diagonal with four blocks.  At a true bridge split, each block is an
outer product of the two side tensors, with one bridge multiplier in the
three nonzero blocks.  Thus every block has rank one and the total rank is at
most four.

### Endpoint inequality, including the ordinary endpoint

For a three-port JC-symmetric endpoint write

\[
a=P(1,1,0),\quad b=P(1,0,1),\quad c=P(0,1,1),
\quad t=P(1,2,3),
\]

and set $\Delta=abc-t^2$, $\Gamma=a-bc$.  The complete effective central
singleton-signature edge class is identified and normalized to multiplier
one before these polynomials are evaluated.  Independent graph-to-polynomial reconstruction
gave:

- 67 nontrivial endpoints with $\Delta>0$ on the whole open cube;
- 2 nontrivial endpoints with $\Delta=0$ and $\Gamma>0$;
- 7 nontrivial endpoints with $\Delta=\Gamma=0$;
- the ordinary trivalent median with $\Delta=\Gamma=0$.

For arbitrary terminal arms `u,v in (0,1)` and `w in (0,1]`, the coordinates
scale as

\[
(a,b,c,t)\mapsto(uv,a,uw,b,vw,c,uvw,t).
\]

Therefore $\Delta$ acquires the positive square of the appropriate arm
factor.  On the $\Delta=0$ branch,

\[
\Gamma\mapsto uv(a-w^2bc)\ge uv(a-bc).
\]

For the ordinary median this is $uv(1-w^2)\ge0$.  The exact universal endpoint
statement is consequently

\[
F>0\quad\text{or}\quad F=0\text{ and }a\ge bc.
\]

The weak inequality is necessary; deleting the ordinary endpoint is rejected
by the mutation suite.

### Two-active crossing

Join two endpoint tensors by a bridge `z in (0,1)`.  If the crossing
flattening had total rank at most four, positivity would force all four
character blocks to have rank one.  Four actual block minors are

\[
\begin{aligned}
f_1&=aA-z^2bcBC,\\
f_2&=zTt-z^2bcBC,\\
f_3&=zC(At-zTbc),\\
f_4&=zc(zBCt-Ta).
\end{aligned}
\]

The independent construction found 20 nonzero minors up to sign and contains
all four.  It also rederived the identities

\[
\begin{aligned}
aA-zTt &= f_1-f_2,\\
z^2CT(abc-t^2)&=zCt(f_1-f_2)-af_3,\\
z^2ct(ABC-T^2)&=Af_4+zcT(f_1-f_2).
\end{aligned}
\]

If all minors vanished, both endpoint `F` values would vanish.  Hence
`a>=bc` and `A>=BC`, so

\[
aA\ge bcBC>z^2bcBC,
\]

contradicting `f_1=0`.  The strict step comes from the physical bridge
`0<z<1`; no boundary specialization is present.

### One-active and arbitrary noncuts

The independent replay regenerated the selected minor for every one of the
204 non-displayed directions among the 72 canonical four-port tensors.  Each
minor has a strict exact sign on the complete open cube.  Positive outside
arm factors act by invertible diagonal row/column scaling and cannot annul a
minor.

The arbitrary-word reduction is sound.  A color word with two transitions on
one directed segment is already interlaced and cannot be separated by an edge
of any switching.  Otherwise one representative of each run suffices; if a
color becomes a singleton, duplicate its adjacent representative.  Occupied
segments stay occupied, so a full strong completion stays represented.  A
split displayed by every full switching would remain displayed after this
balanced restriction.  The exact compressed census has no survivor.  A
failed displayed-tree split has a failed balanced quartet restriction, whose
possibly weak selected tensor is covered by the dummy-restored four-port
universe above.

Finally, in the bridge-component tree, either some bridge has both colors on
both sides, giving the two-active crossing, or there is a unique central
component with monochromatic incident branches.  A balanced noncut has at
least two branches of each color there, giving the one-active case.  Singleton
splits are pendant cuts.  Thus every noncut flattening has rank at least five
at every open parameter point.

## 5. Both cut-set inclusions under one-sided containment

Let `W` be the nonempty source-relative open set witnessing
`N preceq_JC N'`.  Every point of `W` is an open source-model point and lies
in the open target image.

**Source cut implies target cut.**  If `S` is a source cut, its flattening has
rank at most four on `W`.  If it were a target noncut, the pointwise theorem
would give rank at least five at every target point of `W`, a contradiction.

**Target cut implies source cut.**  If `S` is a target cut, its rank-at-most-
four equations hold at every target point and hence on all of `W`.  If it were
a source noncut, the pointwise theorem would give rank at least five at every
source point of `W`, again a contradiction.

Therefore

\[
\operatorname{Cut}(N)=\operatorname{Cut}(N').
\]

This reverse direction does not follow by reversing `preceq`; it follows by
pulling the *target cut equation* back to the shared source-open set.  The
package should state it explicitly.  With unmarked bivalent components
excluded, the complete labelled split set reconstructs the same reduced
leaf-labelled bridge tree on both sides.

## 6. Local-to-global necessity

After cut equality, apply the positive analytic extraction map to the common
distributions.  In source slice coordinates the local model germ is

\[
\prod_v \mathcal L_v\times\prod_e I_e.
\]

A source-relative open containment set pulls back to a relative-open subset
of this product and therefore contains a smaller product box around a regular
source point.  Fix every coordinate but one focal `v` coordinate and vary
that coordinate across its box.

For each resulting distribution, a target preimage exists.  No preimages need
be chosen continuously.  The exact bridge fiber says that every target
factorization has the same extracted projective factor, so the focal box lies
in the union of the finitely many target local role/completion images.

The finite-union conclusion must be phrased carefully.  For example,

\[
(-1,1)=(-1,0]\cup[0,1)
\]

but neither member contains the whole interval.  Thus the sentence in
`PROOF.md` that can be read as putting the whole focal germ into one member is
too strong.  What finite semialgebraic dimension gives is a member whose
intersection with the regular source germ has full source dimension and hence
nonempty relative interior.  That relative-open subgerm is exactly the locked
definition of local one-sided containment.

This argument also handles weak selected target marginals correctly.  The
finite union ranges over selected role/completion tensors induced by the full
strong target; it must not filter the selected marginal by `S_TC` membership.

No distant blob can compensate for a focal projective separator.  The focal
slice coordinate is an intrinsic function of the observed distribution.
Changing a distant factor may change the distribution, but it cannot give the
same distribution a different focal projective orbit.  The direct marginal
calculation agrees: with one selected taxon in each incident branch,

\[
z_i=x_{e_i}\kappa_i,\qquad
D_{(x_{e_i})}(z_i)=\operatorname{diag}(\kappa_i),
\]

and every `kappa_i` is positive.  Independent adjacent physical bridge
parameters give full arm rank.  Coupling them is a rejected mutation.

The deduction from these local containments to “isomorphic or `T`” remains
conditional on the separate bounded atlas and arbitrary-word coherence gates.
The localization mechanism itself is **VERIFIED**.

## 7. Converse gluing and simultaneous `T` germs

Assume, as a local input, that every corresponding pair of projective factors
has a common full-dimensional germ `U_v` regular for both parameterizations.
This is automatic for an isomorphic pair and is the stated local `T`
certificate for a valid redirected pair.

Shrink each `U_v` so that both networks admit positive analytic incidence
representatives.  Write a physical representative schematically as

\[
P_v^{(k)}=A_v^{(k)}S_v,
\]

where `S_v` is the common sliced tensor and `A_v^(k)` supplies one positive
factor at every incidence.  On a bridge `e=uv`, choose a common effective
scale `z_e` and set

\[
x_e^{(k)}=
\frac{z_e}{a_{u,e}^{(k)}a_{v,e}^{(k)}}.
\]

All denominators are positive and, after shrinking, bounded away from zero.
Hence each bridge has a nonempty open interval `0<z_e<epsilon_e` on which
both physical multipliers lie in `(0,1)`.  The intervals are independent.
This proves exactly the sufficiently-small-interval formulation in the
current global draft.  It does not prove that every positive `z_e` is
physical.

The bridge graph is a tree, so there is no scaling holonomy.  Parameters of
distinct blobs and distinct bridges are disjoint.  Consequently the product

\[
\prod_v U_v\times\prod_e(0,\epsilon_e)
\]

contracts to the same global distributions in both networks.  Extraction is
an analytic inverse on the sliced product, so the product has the full global
local dimension.  Local regularity plus the independent bridge directions
gives a point regular for both global parameterizations.

Compatible `T` germs can be chosen simultaneously: there is at most one
triangle per blob, the local certificate is port-labelled and survives
corresponding port grafting, and different blobs use disjoint parameters.
The all-three-orientations common local germ also prevents a transitivity gap
within one triangle.  No global continuous target-parameter selector is used.

Thus the converse *gluing lemma* is **VERIFIED conditional on its stated local
regular-germ premises**.  Promotion of the final theorem still awaits proof of
those premises for every local atlas case and the separate root/coherence
gates.

## 8. Exact artifacts and replay

`exact_audit.py` imports no package implementation.  It independently:

- constructs zero-sum JC orbit coordinates and bridge log-design matrices;
- computes incidence kernels, stabilizers, and anchor ranks over `Q`;
- enumerates the 102 theta and 12 cycle primitive orientations;
- checks every published full completion as rooted, LSA-valid, narrow
  standard, and rooting-independently strong;
- reconstructs every graph-to-switching-to-mask transport;
- rebuilds endpoint polynomials and one-active minors;
- proves their signs by an independent exact Bernstein/factor routine; and
- rebuilds all two-active blocks and identities.

`mutation_tests.py` rejects 15 mutations, including the ordinary-endpoint
deletion, illegal zero-sum anchoring, altered graph transport/minor, `z^2` to
`z`, reciprocal-only gauge, physical-edge recovery, selected weakness inferred
from a dummy, coupled arms, both finite-union errors, and omission of the
reverse cut inclusion.

Reproduction from `s_tc_jc_landmark_closure/`:

```bash
PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python \
  reviews/global_bridge/exact_audit.py

PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python \
  reviews/global_bridge/mutation_tests.py
```

The generated certificates are `exact_audit_certificate.json` and
`mutation_certificate.json`.  Package replays were directed into this review
folder so that no source artifact was modified.
