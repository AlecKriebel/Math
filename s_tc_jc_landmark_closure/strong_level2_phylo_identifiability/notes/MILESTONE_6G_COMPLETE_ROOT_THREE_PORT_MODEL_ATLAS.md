# Milestone 6G: complete JC/K2P/K3P root three-port observational atlas

## Scope

The exhaustive root three-port census consists of one ordinary-tree record,
two cycle records, and five theta records.  Across all port labels these are
three rooted tree topologies and thirty-nine rooted reticulate topologies;
after root suppression they are one tree and twenty-one reticulate
semi-directed topologies.

This milestone classifies `bowtie` and one-sided generic containment for every
ordered pair under JC, K2P, and K3P.  It combines the earlier exact rank,
separation, and common-point certificates with Milestone 6F.

## The complete class table

**PROVED.** The observational classes and dimensions are

| model | class | unlabelled records | dimension | rooted | semi-directed |
|---|---|---:|---:|---:|---:|
| JC | `T3` | `0` | 3 | 3 | 1 |
| JC | `R4` | `1,...,7` | 4 | 39 | 21 |
| K2P | `T6` | `0` | 6 | 3 | 1 |
| K2P | `R9` | `1,...,7` | 9 | 39 | 21 |
| K3P | `T9` | `0` | 9 | 3 | 1 |
| K3P | `H14` | `1,2,4` | 14 | 15 | 9 |
| K3P | `A15` | `3,5,6,7` | 15 | 24 | 12 |

The K3P `H14` class is the irreducible quartic hypersurface from Milestone 6D;
`A15` has complete affine normalized closure.

## JC relation

**PROVED.** Every pair inside `R4` has a common regular four-dimensional
stochastic neighborhood.  The three rooted presentations inside `T3` have the
same complete semi-directed tree image by reversibility.

**PROVED.** `T3` and `R4` have disjoint open stochastic images.  The tree
invariant

\[
r_{12}r_{13}r_{23}-u_{123}^2
\]

is zero on `T3` and strictly positive on every reticulate open parameter cube.
Thus neither one-sided containment occurs.

Hence the JC class picture is two incomparable nodes:

```text
T3       R4
```

## K2P relation

**PROVED.** All seven reticulate records belong to one regular
nine-dimensional class `R9`.  The ordinary tree has dimension six.

**PROVED.** Milestone 6F gives complete open stochastic containment

\[
\boxed{T6\preceq R9.}
\]

This holds for every one of the thirty-nine rooted and twenty-one
semi-directed reticulate topologies, not only for the two cycle records,
because each displays the unique three-leaf semi-directed tree.

**PROVED.** The reverse containment and `bowtie` are absent by the strict
dimension inequality `6<9`.

The K2P class poset is

```text
T6  --->  R9
```

where the arrow is complete stochastic image containment.

## K3P relation

**PROVED.** Pairwise `bowtie` holds inside `H14` and inside `A15`.  Milestone
6D proves one-sided regular containment

\[
H14\preceq A15,
\]

while the reverse direction and `bowtie` are impossible by `14<15`.

**PROVED.** Every reticulate record displays the unique three-leaf
semi-directed tree, so Milestone 6F gives complete image containments

\[
T9\preceq H14,
\qquad
T9\preceq A15.
\]

All reverse directions and all unequal-class `bowtie` relations are absent by
the dimension chain

\[
\boxed{9<14<15.}
\]

Thus the K3P class poset is

```text
T9  --->  H14  --->  A15
 \-------------------->
```

The first and long arrows are complete open tree-image containments.  The
`H14 -> A15` arrow is the certified local one-sided regular containment from
Milestone 6D; complete image containment is not claimed there.

## Exact simultaneous intersections

Because the ordinary tree is itself one of the eight unlabelled models, any
simultaneous intersection is a subset of its image.

**PROVED.** Under JC, the intersection of all eight open stochastic images is
empty.

**PROVED.** Under K2P, the intersection of all eight images is exactly the
complete ordinary-tree image and has dimension six:

\[
\bigcap_{i=0}^7\mathcal M_i^{\rm K2P}
=
\mathcal M_{T}^{\rm K2P}.
\]

**PROVED.** Under K3P, the analogous intersection is exactly the complete
ordinary-tree image and has dimension nine:

\[
\bigcap_{i=0}^7\mathcal M_i^{\rm K3P}
=
\mathcal M_{T}^{\rm K3P}.
\]

These are stochastic equalities, not deductions from Zariski closures.

## Classification consequence

**PROVED.** The root three-port `bowtie` and `preceq` atlases are now complete
under all three models.  In particular, the ordinary-tree question left open
in Milestones 6C and 6D is closed.

**UNRESOLVED.** Equality versus inequality of the complete open stochastic
images inside the equal-dimensional reticulate `bowtie` classes is not needed
for the observational relation and remains open.

**UNRESOLVED.** The corresponding arbitrary-port K2P/K3P atlases and their
global local-to-global completeness theorems remain open.

## Replay

Run

```sh
PYTHONPATH=src .venv/bin/python src/verify_group_based_root_three_port_complete_atlas.py
```

The verifier checks every dependency hash, record assignment, topology count,
dimension, relation, and simultaneous-intersection conclusion against the
exact source certificates.  Its machine-readable output is
`certificates/group_based_root_three_port_complete_atlas.json`.
