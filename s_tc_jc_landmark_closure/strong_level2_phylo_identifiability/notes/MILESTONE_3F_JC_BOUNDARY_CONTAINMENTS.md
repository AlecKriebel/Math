# Milestone 3F: exact stochastic separation and algebraic boundary containment

## Scope

Milestone 3E leaves 1,152 of the 40,320 ordered dimension-10-to-dimension-11
component pairs unrefuted by its compact quartet signatures.  This milestone
first resolves every surviving direction for which the two lifted models
have the same four-leaf root marginal, then combines the result with the root
atlas to sharpen the exhaustive directed-containment audit.

The class remains the 612 five-port incoming lifts from Milestone 3E.  Thus
the result is exact for that finite atlas; it is not yet a theorem for every
ported subdivision in `L_1`.

## Seven same-root pair orbits

**EXACTLY COMPUTED.** There are 168 surviving ordered pairs with equal root
marginal.  Simultaneous relabelling of the four outgoing ports acts freely,
and the pairs form exactly seven `S_4` orbits of size 24.  Representatives,
written as `(smaller component, larger component)`, are

```text
(96,1), (96,414), (144,25), (144,265),
(144,366), (144,438), (144,440).
```

The certificate stores the corresponding census indices and leaf
assignments, not only these component identifiers.

## Strict open-stochastic separation

For six pair orbits, one fixed relabelling of the cubic root-atlas invariant
template 2 is evaluated on an incoming quartet.  For the seventh orbit, one
fixed relabelling of quartic template 4 is used.  In every case the pullback
on the smaller model is the zero polynomial.

**EXACTLY COMPUTED.** Direct symbolic contraction and factorization give a
nonzero target pullback of the form

\[
 c\,m(\mathbf x,\boldsymbol\lambda)
 \prod_j (u_j-1)^{e_j}
 \prod_k (v_{k,1}\cdots v_{k,r_k}-1)^{f_k},
\]

or the same expression times one factor

\[
x\bigl(\lambda y+(1-\lambda)z\bigr)-1.
\]

Here `c` is a nonzero integer, `m` is a monomial in edge multipliers and
inheritance probabilities, and every displayed variable lies strictly in
`(0,1)` on the open JC domain.

**PROVED.** Every monomial factor is positive.  Each factor `u-1` and each
product-minus-one factor is strictly negative.  The convex-combination
factor is also strictly negative because

\[
0<x<1,
\qquad
0<\lambda y+(1-\lambda)z<1.
\]

Consequently the target invariant never vanishes anywhere in its complete
open stochastic parameter cube.

**PROVED.** All 168 same-root dimension-10-to-dimension-11 pairs have
disjoint open stochastic images.  In particular, no same-root one-sided
generic stochastic containment occurs in this atlas.

This conclusion is stronger than generic separation outside an exceptional
set: the two open stochastic images are disjoint in each directed pair.

## Two proper algebraic boundary containments

The first two `S_4` pair orbits behave differently after passing to complex
closures.

Normalize the smaller model by fixing edge parameters with indices

```text
6, 7, 10
```

and both inheritance probabilities to `1/2`.  Ten source variables remain.
For each of the first two orbit representatives, the verifier supplies an
explicit rational map from those ten variables to the fifteen target
parameters.

**EXACTLY COMPUTED.** Under both maps, target edge parameter 1 is identically

\[
b_1=1.
\]

Direct substitution proves equality of all 51 zero-sum JC character-orbit
coordinates on five leaves.  At the source point where all ten free
parameters equal `1/2`, every mapped target parameter other than `b_1` lies
strictly in `(0,1)`.

**EXACTLY COMPUTED.** On coordinate rows

```text
1, 2, 3, 4, 5, 6, 7, 8, 15, 18
```

the two exact source-gauge Jacobian determinants at that point are

\[
\frac{99}{18014398509481984}
\quad\text{and}\quad
-\frac{99}{562949953421312},
\]

respectively.  Both are nonzero.

**PROVED.** Each ten-variable source gauge is dominant onto its irreducible
dimension-10 model closure.  The coordinate identities therefore give a
proper containment of that closure in the corresponding irreducible
dimension-11 target closure.  Relabelling propagates the construction to
`2*24=48` directed pairs.

**PROVED.** These 48 directions are algebraic containments realized on the
zero-length-edge boundary `b_1=1`, but they are not stochastic containments:
the strict incoming-quartet invariant from the preceding section separates
the complete open images.

This is a concrete exact warning that Zariski containment alone does not
classify observational compatibility.

**UNRESOLVED.** The algebraic boundary-containment status of the other five
same-root pair orbits is not determined here.  Their open stochastic images
are nevertheless already proved disjoint.

## Combined directed-containment audit

There are 40,320 ordered pairs from a dimension-10 component to a
dimension-11 component.

**EXACTLY COMPUTED.** They now partition as follows:

| exact disposition | directions |
|---|---:|
| rejected by compact incoming-quartet signatures | 39,168 |
| additionally rejected by root-marginal certificates | 384 |
| additionally rejected by same-root strict factors | 168 |
| unresolved cross-root directions | 600 |
| total | 40,320 |

Thus 39,720 directions are proved not to be one-sided stochastic
containments.  Every one of the remaining 600 pairs crosses two distinct
root-marginal components whose lower-to-higher relation was already left
unresolved in Milestone 3D.

**UNRESOLVED.** No containment or overlap is inferred for those 600 pairs.
They are recorded explicitly in the machine certificate and are the next
finite-atlas closure target.

## Machine replay

- `src/verify_jc_boundary_containments.py` regenerates all seven orbit
  representatives, contracts and factors the exact incoming-quartet
  invariants, checks the two rational boundary maps on all 51 coordinates,
  and verifies both exact rank determinants.
- `certificates/jc_boundary_containments.json` records every factorization,
  rational map, mapped boundary point, rank certificate, and all 600
  unresolved cross-root component pairs.
- The replay also consumes the two preceding deterministic atlas
  certificates to check the exhaustive counts rather than accepting them as
  handwritten input.

No numerical optimization, approximate algebra, specialized phylogenetic
software, or external literature is used in the theorem.

## Consequence and next step

**PROVED.** Within the incoming-port finite slice, all unequal-dimensional
ambiguities sharing a root marginal are now stochastically classified: none
is an interior one-sided containment.  Two exact algebraic containments exist
only after a zero-length edge reaches the boundary.

**UNRESOLVED.** The immediate finite task is to resolve the remaining 600
cross-root directions.  The structural task remains to lift the local atlas
from reduced port placements to arbitrary strong port subdivisions and then
recover the blob tree from generic Fourier data.
