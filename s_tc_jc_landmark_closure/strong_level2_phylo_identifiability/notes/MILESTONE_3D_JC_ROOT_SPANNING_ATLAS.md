# Milestone 3D: complete JC observational atlas for the root-spanning four-port slice

## Scope

This milestone classifies the finite class obtained as follows:

1. start with every reduced level-2 theta core derived in Milestone 2;
2. orient it as a binary strongly tree-child rooted network with the global
   root in the blob;
3. place exactly four outgoing ports, each represented by one labelled leaf;
4. require the blob to be simple, so every leaf is incident to the blob.

The semi-directed convention suppresses only the degree-two artifact created
by forgetting the global root, forgets tree-edge directions, and retains the
directions entering reticulations.

This is a complete theorem for that finite slice.  It is **not** yet a
classification of all four-leaf level-2 networks, of nonroot port tensors, or
of the global classes `L_1`, `L_*`, and `S_2`.

## Primary theorem

**PROVED.** Let `A` be the root-spanning simple four-leaf class above.  For
two networks `N,N' in A` under Jukes--Cantor,

\[
N\bowtie_{\rm JC}N'
\quad\Longleftrightarrow\quad
N,N'\text{ are connected by reversible root placement and the moves }
T,\Theta,\Psi,\Omega.
\]

Here reversible root placement includes rooted presentations of the same
leaf-labelled semi-directed topology.  The four nontrivial move names are:

- `T`: ordinary redirection of the unique triangle;
- `Theta`: the inherited theta pendant transfer;
- `Psi`: the four-way root-collapsed path-placement move from Milestone 3B;
- `Omega`: the root path-reversal move from Milestone 3C.

**PROVED.** No additional full-dimensional regular stochastic ambiguity
occurs in this slice.  In particular, the apparent degree-four collision
between census networks 9 and 10 is false: a degree-five invariant separates
the two relevant labelled semi-directed topologies exactly.

**UNRESOLVED.** The theorem above classifies the symmetric relation
`bowtie_JC`.  It does not finish the separately defined one-sided relation
`preceq_JC` between models of unequal dimension.

## Exhaustive counts

**EXACTLY COMPUTED.** Direct generation from the four reduced rooted theta
cores gives:

| object | count |
|---|---:|
| raw distributions of ordinary ports over directed core segments | 112 |
| unlabelled rooted networks | 27 |
| leaf-labelled rooted isomorphism classes | 612 |
| leaf-labelled semi-directed isomorphism classes | 216 |
| observational move components | 108 |
| move components modulo simultaneous `S_4` leaf relabelling | 8 |

The 108 component sizes are

\[
2^{36},\quad4^{24},\quad5^{12},\quad7^{12},\quad
8^{12},\quad17^{12},
\]

where an exponent denotes the number of components of that size, not a
power.  These account for all 612 rooted labelled networks.

**EXACTLY COMPUTED.** The 216 semi-directed classes have rooted-presentation
size distribution

\[
1^{48},\quad2^{108},\quad5^{36},\quad7^{24}.
\]

The graph audit finds exactly 60 triangle-redirection relations between
semi-directed classes before adding `Theta`, `Psi`, and `Omega`.

## The eight classes modulo leaf relabelling

**EXACTLY COMPUTED.** The table records the census indices occurring in each
simultaneous-`S_4` orbit of observational components.

| orbit | dimension | rooted models per labelled component | semi-directed models | census indices | source of ambiguity |
|---:|---:|---:|---:|---|---|
| 0 | 8 | 8 | 4 | `0,4,13,22` | `Theta` and `T` |
| 1 | 8 | 17 | 3 | `1,6,8,11,14,15,20,21,23` | `T` |
| 2 | 9 | 2 | 1 | `2` | reversible root placement |
| 3 | 9 | 7 | 1 | `3,5,7,12` | reversible root placement |
| 4 | 9 | 2 | 1 | `9,10` | reversible root placement only |
| 5 | 9 | 4 | 2 | `16,26` | `Omega` |
| 6 | 9 | 5 | 1 | `17,24,25` | reversible root placement |
| 7 | 7 | 4 | 4 | `18,19` | `Psi` |

Orbit 4 is the important correction to the degree-four discovery probe:
indices 9 and 10 are rooted presentations of one semi-directed topology only
for the matched labellings.  The reflected candidate topology belongs to a
different observational component and is separated in degree five.

## Exact dimension certificate

Set the four pendant Fourier multipliers to one.  For a nontrivial Fourier
coordinate `q_g`, the derivative in the pendant multiplier at leaf `i` is

\[
\mathbf 1[g_i\ne0]q_g.
\]

Thus the generic full-model Jacobian rank equals the rank of a `14 x 14`
matrix consisting of:

1. ten core columns: eight internal-edge derivatives and two inheritance
   derivatives; and
2. four pendant support columns
   `1[g_i != 0] q_g`.

This normalization changes the matrix only by invertible row and column
scalings on the nonzero pendant torus.

**EXACTLY COMPUTED.** Fraction-free Bareiss elimination over the exact
multivariate polynomial ring over `Q` gives the dimensions

```text
(8,8,9,9,8,9,8,9,8,9,9,8,9,8,
 8,8,9,9,7,7,8,8,8,8,9,9,9).
```

Hence the 27 unlabelled census models have dimension distribution

\[
7^2,\qquad8^{13},\qquad9^{12}.
\]

**PROVED.** In characteristic zero, the generic Jacobian rank of a polynomial
map equals the transcendence degree of its coordinate functions.  The exact
elimination therefore supplies both the upper and lower dimension
certificates; the dimensions are not inferred from sampled ranks.

## Exact separating invariants

Let

\[
(q_0,\ldots,q_{14})
\]

be ordered by the fifteen JC character orbits in
`src/probe_four_leaf_jc_atlas.py`; `q_0=1`.  Six invariant templates, together
with all distinct `S_4` leaf relabellings, suffice.  Their degrees, supports,
and orbit sizes are:

| template | degree | support | distinct `S_4` images |
|---:|---:|---:|---:|
| 0 | 3 | 6 | 6 |
| 1 | 2 | 4 | 3 |
| 2 | 3 | 18 | 3 |
| 3 | 5 | 25 | 24 |
| 4 | 4 | 19 | 12 |
| 5 | 4 | 8 | 12 |

For example, the quadratic template is

\[
q_0q_9-q_1q_8-q_2q_6+q_3q_5,
\]

and the six-term cubic template is

\[
q_0q_1q_9-2q_0q_1q_{10}+2q_0q_4q_7
+q_1^2q_8-q_1q_2q_6-q_1q_3q_5.
\]

The complete integer templates are stored in
`src/jc_root_spanning_atlas_data.py` and in the replay certificate.

**EXACTLY COMPUTED.** For every one of the 612 labelled rooted models, the
verifier substitutes the complete displayed-tree parameterization into all
60 relabelled invariants and expands the result as an exact multivariate
polynomial over `Q`.

**EXACTLY COMPUTED.** The zero/nonzero polynomial signature is constant on
each proposed move component and different for all 108 components.  Its
deterministic component-signature digest is

```text
c9f8e6826fae432d14d54822866f45d2cfae8d96dcfe644f9372862122b25355
```

Consequently every two different components have different irreducible model
closures.  The computation separates all 2,898 pairs of different
components having equal dimension.

## Why the invariant certificate proves the if-and-only-if theorem

**PROVED.** Every network parameter space is irreducible, so the Zariski
closure of its polynomial image is irreducible.

**PROVED.** Within a proposed component, full-dimensional regular stochastic
overlap follows from the already certified correspondences:

1. uniform JC is reversible, so moving the root within one semi-directed
   topology preserves the complete distribution;
2. `T` has an exact positive rational port correspondence; choosing the
   external arm multipliers sufficiently small makes all finite triangle
   redirections simultaneously stochastic on an open set;
3. the four-network `Theta`/`T` component has one exact common regular point;
4. all four `Psi` models share one explicitly parameterized regular open box;
5. all four rooted `Omega` models share one exact common regular point and a
   rational correspondence.

**PROVED.** Conversely, suppose two equal-dimensional models had a
full-dimensional regular stochastic intersection.  Its Zariski closure would
be an irreducible subvariety of the same dimension dense in both model
closures, forcing those closures to be equal.  The exact signatures rule
this out for different components.

Models of different dimensions cannot satisfy `bowtie_JC` by definition.
This proves the stated biconditional for the finite slice.

## One-sided containment audit

There are 2,880 ordered component pairs `(lower,higher)` with strictly
different dimensions.

**EXACTLY COMPUTED.** A containment `V_lower subseteq V_higher` is refuted
whenever an invariant of the higher model is nonzero on the lower model.  The
six signature templates refute 2,304 directions.  One additional
degree-five, 54-term template and its leaf orbit refute another 108, for a
total of 2,412 exact noncontainment certificates.

**UNRESOLVED.** The remaining 468 directions are not classified here.  Their
survival means only that these degree-at-most-five certificates do not refute
containment.  It is neither evidence nor a claim that any containment exists.

## Replay artifacts

- `src/verify_jc_root_spanning_atlas.py` regenerates the topology census,
  exact symbolic ranks, invariant signatures, and directed audit.
- `src/jc_root_spanning_atlas_data.py` stores the seven symmetry-reduced
  integer invariant templates.
- `certificates/jc_root_spanning_atlas.json` contains all 27 machine-readable
  networks, all 108 components, all 612 labelled memberships, dimensions,
  signatures, and the 468 unresolved directed pairs.

No numerical optimization, sampled rank, or unsaturated ideal equality is
used in the theorem.

## Consequence and next boundary

**PROVED.** Even in this smallest root-spanning simple slice, generic JC data
identify neither the rooted topology nor always the semi-directed topology.
The complete root-local ambiguity set consists of `T`, `Theta`, `Psi`, and
`Omega`; there is no fifth move in this finite atlas.

**UNRESOLVED.** The next mandatory step is to expose the incoming state port
for every atlas class and classify the resulting nonroot tensors.  The
existing lift theorems already eliminate `Psi` and `Omega` as primitive
nonroot moves and restrict the known strong nonroot theta family to `T`, but
the remaining generator orientations still require an exhaustive exact port
audit before a theorem for `L_1` can be claimed.
