# Milestone 3G: complete stochastic-containment classification of the incoming-port JC atlas

## Scope

Milestone 3F proves strict stochastic separation for all 168 surviving
dimension-10-to-dimension-11 pairs having the same four-leaf root marginal.
It leaves 600 cross-root directions.  This milestone resolves all 600 and
thereby closes one-sided generic stochastic containment for the complete
612-network incoming-port atlas of Milestone 3E.

The theorem remains a finite reduced five-port result.  Arbitrary port
subdivisions and global blob-tree reconstruction are not yet included.

## Symmetry reduction

**EXACTLY COMPUTED.** The 600 cross-root directions form 25 free orbits of
size 24 under simultaneous relabelling of the four outgoing ports.  Their
root marginals depend on only ten directed `S_4` pair orbits.

Using the root-atlas component identifiers, those ten representatives and
their lifted direction multiplicities are:

| lower root | higher root | lifted directions |
|---:|---:|---:|
| 0 | 24 | 48 |
| 0 | 48 | 48 |
| 0 | 49 | 48 |
| 12 | 36 | 144 |
| 12 | 48 | 48 |
| 12 | 74 | 48 |
| 12 | 86 | 96 |
| 96 | 3 | 24 |
| 96 | 14 | 72 |
| 96 | 84 | 24 |
| **total** |  | **600** |

The root dimensions are `8 -> 9` for the first seven orbits, `7 -> 8` for
the next two, and `7 -> 9` for the last.

## Strict root-marginal certificates

For each directed root pair, choose an invariant from the exact 60-feature
root atlas.  The selected feature indices, degrees, and supports are:

| pair | feature | degree | support |
|---:|---:|---:|---:|
| `(0,24)` | 2 | 3 | 6 |
| `(0,48)` | 6 | 2 | 4 |
| `(0,49)` | 10 | 3 | 18 |
| `(12,36)` | 56 | 4 | 8 |
| `(12,48)` | 8 | 2 | 4 |
| `(12,74)` | 5 | 3 | 6 |
| `(12,86)` | 8 | 2 | 4 |
| `(96,3)` | 31 | 5 | 25 |
| `(96,14)` | 2 | 3 | 6 |
| `(96,84)` | 7 | 2 | 4 |

**EXACTLY COMPUTED.** Direct symbolic substitution proves that every selected
invariant pulls back to the zero polynomial on the smaller root model.

On nine larger models, the exact pullback factors as a nonzero integer, a
positive monomial in all edge and inheritance parameters, and products of
factors among

\[
x-1,\qquad x+1,\qquad xy-1.
\]

Repeated factors and longer products occur, but no unfactored polynomial
remains.

On pair `(96,3)`, the only additional factor is

\[
\lambda x_0x_1x_2+(1-\lambda)x_3.
\]

The certificate stores every complete factorization with the exact edge and
inheritance parameter indices.

**PROVED.** On the open JC cube, all monomial factors are positive,
`x-1<0`, `xy-1<0`, and `x+1>0`.  The exceptional displayed factor is a
strictly positive convex combination because every multiplier and
inheritance weight lies strictly between zero and one.  Thus every selected
target pullback is nonzero throughout the complete open parameter space.

**PROVED.** The two root models in each directed pair have disjoint complete
open stochastic images.  This is strict full-cube separation, not merely
generic noncontainment outside an exceptional algebraic set.

## Lifting the separation

Marginalizing incoming leaf `5` from any network in the five-port atlas
recovers its four-leaf root-spanning model exactly.

**PROVED.** If one of the 600 lifted source and target distributions were
equal, their root marginals would be equal.  The corresponding relabelled
strict invariant would then be simultaneously zero and nonzero, a
contradiction.  Hence all 600 cross-root lifted pairs have disjoint complete
open stochastic images.

Together with Milestone 3F, the full unequal-dimensional audit is:

| certificate source | directions separated |
|---|---:|
| compact incoming-quartet signatures | 39,168 |
| additional root-marginal algebraic certificates | 384 |
| same-root strict factors | 168 |
| cross-root strict factors | 600 |
| **total** | **40,320** |

**PROVED.** Every dimension-10 component and every dimension-11 component in
the incoming-port atlas have disjoint complete open stochastic images.
Consequently there are no unequal-dimensional one-sided generic stochastic
containments.

## Complete generic observational classification for this finite atlas

Milestone 3E already proves that two equal-dimensional networks have a
full-dimensional regular stochastic overlap if and only if they are
labelled-isomorphic or differ by ordinary triangle redirection `T`.

**PROVED.** For any two networks `N,N'` in the 612-network incoming-port
atlas,

\[
N\bowtie_{\rm JC}N'
\quad\Longleftrightarrow\quad
N,N'\text{ are labelled-isomorphic or differ by }T.
\]

**PROVED.** No pair of distinct unequal-dimensional models satisfies
one-sided generic stochastic containment in either direction.  Thus the same
move system also completely describes the generic containment relation in
this finite atlas.

This theorem does not assert that every distinct equal-dimensional pair has
empty stochastic intersection; lower-dimensional intersections and all
boundary components are outside the generic relation classified here.

## Algebraic versus stochastic behavior

Milestone 3F gives 48 proper algebraic containments among the same-root
pairs, all realized with one edge multiplier equal to one.  The present
strict theorem proves those open stochastic images disjoint.

**PROVED.** Therefore the completed atlas contains exact examples where

\[
V_N\subsetneq V_{N'}
\quad\text{but}\quad
\mathcal M_N\cap\mathcal M_{N'}=\varnothing.
\]

This distinction is part of the classification, not a boundary technicality.

**UNRESOLVED.** The algebraic containment status of the remaining same-root
and cross-root unequal-dimensional pairs is not completely classified.

## Machine replay

- `src/verify_jc_cross_root_separation.py` reconstructs all ten root-pair
  orbits, verifies every exact zero pullback and target factorization, and
  assigns all 600 lifted directions to those orbits.
- `certificates/jc_cross_root_separation.json` records the selected
  invariants, all exact factors, orbit multiplicities, and the closed audit.
- The verifier consumes and cross-checks the root, incoming-port, and boundary
  certificates rather than accepting the 600-direction list as independent
  input.

No numerical optimization, approximate algebra, specialized phylogenetic
software, external generator catalogue, or literature search enters the
theorem.

## Next structural step

**PROVED.** In the complete reduced nonroot five-port slice, ordinary
triangle redirection is the only generic ambiguity, and unequal model
dimensions never create stochastic containment.

**UNRESOLVED.** Promoting this finite theorem to `L_1` now requires a
subdivision-reduction theorem: every arbitrary strong ported level-2 blob
must expose a bounded incoming quartet that reduces to the certified atlas,
unless the local change is `T`.  A separate exact argument must reconstruct
the cut-edge/blob tree and rule out nonlocal coordination.
