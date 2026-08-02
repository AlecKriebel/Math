# Milestone 6E: triangle redirection is universal across JC, K2P, and K3P

## Scope and status

This milestone extracts the ordinary triangle move from the complete
three-port root atlases and proves that it survives all three requested
group-based substitution models.  It does **not** assert equality of complete
open stochastic images.

Every substantive claim below has one of the required status labels.

## Formal local move

Let a labelled semi-directed network contain a three-cycle with one external
attachment port at each of its vertices.  Retain the labelled underlying
graph, retain every arrowhead outside the three-cycle, and change which one of
the three triangle vertices receives the two reticulation arrowheads.  When
the resulting orientation is acyclic and binary, this is the local move `T`.

**PROVED.** This definition is independent of a drawing or vertex naming.  In
the certificate it is checked by enumerating leaf-colour-preserving
isomorphisms of the underlying undirected graphs, transporting all directed
edges outside the unique triangle, and allowing only the directed edges inside
that triangle to change.

## Theorem

**PROVED.** Under each model

\[
M\in\{\mathrm{JC},\mathrm{K2P},\mathrm{K3P}\},
\]

the three labelled semi-directed orientations of a three-port triangle are
pairwise related by `\bowtie_M`.  More precisely, all three model images pass
through one strict regular stochastic tensor and contain the same relatively
open neighborhood of that tensor in their common local model locus.  The
local dimensions are

\[
\dim_M(T)=
\begin{cases}
4,&M=\mathrm{JC},\\
9,&M=\mathrm{K2P},\\
14,&M=\mathrm{K3P}.
\end{cases}
\]

For K3P the common locus is the irreducible quartic hypersurface `V(I)` from
Milestone 6D, rather than the whole normalized fifteen-dimensional tensor
space.

**PROVED.** Replacing corresponding ports by identical rooted components
preserves the overlap.  On a nonempty strict neighborhood in which every
nonzero Fourier arm multiplier is positive, characterwise tripod inversion is
analytic, so regularity and dimension propagate as well as tensor equality.

**UNRESOLVED.** The complete open stochastic images of the three orientations
may be unequal.  Only the full-dimensional regular relation `\bowtie_M` is
claimed.

## Exact topology census

The exhaustive three-port generator census has two unlabelled rooted cycle
records, numbered `1` and `2`.  Applying all six labels to their three ports
gives twelve record-label presentations.

**EXACTLY COMPUTED.** Canonical rooted graph reduction gives nine distinct
rooted topologies.  Root suppression and canonical mixed-graph reduction give
exactly three distinct semi-directed topologies.

**EXACTLY COMPUTED.** In these three mixed graphs, the external labelled port
incident to the reticulation is respectively `L1`, `L2`, and `L3`.  Every graph
has exactly one triangle, and each of the three unordered graph pairs passes
the formal `T` predicate.  Thus the census contains all possible choices of
the reticulation vertex and no additional semi-directed change.

## JC certificate

Write the normalized nonconstant JC three-port tensor as

\[
(r_{12},r_{13},r_{23},u_{123}).
\]

The common target is

\[
r_{12}=r_{13}=r_{23}=\delta^2,
\qquad
u_{123}=\frac45\delta^3,
\qquad
\delta=2^{-30}.
\]

**EXACTLY COMPUTED.** For each of the two cycle records, the equal-internal-
edge section has a unique simple algebraic root `h` in `(1/8,7/8)`.  Its three
positive pendant arms are determined by the exact squared formulas in
`certificates/jc_root_three_port_saturation.json` and lie below `2^-9`.

**PROVED.** The logarithmic Jacobian of the four section parameters

\[
(a_1,a_2,a_3,h)
\]

to the four displayed coordinates is nonzero at that root.  The inverse
function theorem therefore produces a common regular four-dimensional
stochastic neighborhood.  The same target is leaf-symmetric, so all three
labelled semi-directed orientations meet there.

## K2P certificate

The convention is

\[
a_e(1)=s_e,\qquad a_e(2)=a_e(3)=t_e,
\]

with transition probabilities

\[
\frac{1+s_e+2t_e}{4},\quad
\frac{1+s_e-2t_e}{4},\quad
\frac{1-s_e}{4},\quad
\frac{1-s_e}{4}
\]

all strictly positive.

**EXACTLY COMPUTED.** Both cycle records realize the same nine-coordinate
target on the JC diagonal: the six pair orbits equal `delta^2` and the three
triple orbits equal `(4/5)delta^3`.  Their prescribed `9 x 9` Jacobian
determinants factor into nonzero pendant monomials, powers of `h`, powers of
`1-h`, and univariate factors having no zero in `(1/8,7/8)` by exact Sturm
counting.

**PROVED.** Each orientation is therefore a submersion onto a common open
neighborhood in normalized K2P tensor space.  Its local dimension is nine.

## K3P certificate

The convention is three independent nonzero multipliers `(x_e,y_e,z_e)`,
restricted by strict positivity of

\[
\frac{1+x_e+y_e+z_e}{4},\quad
\frac{1+x_e-y_e-z_e}{4},\quad
\frac{1-x_e+y_e-z_e}{4},\quad
\frac{1-x_e-y_e+z_e}{4}.
\]

The common leaf-symmetric rational tensor is

\[
q_{000}=1,
\]

with singleton pair coordinates `101/1000000`, doubleton pair coordinates
`1/10000`, and every all-distinct triple coordinate `1/1250000`.

**EXACTLY COMPUTED.** The tensor lies on the sparse irreducible eight-term
quartic `I=0`, and `dI/dq123=-37/10^14` there.  Both cycle records have exact
generic rank fourteen and annihilate `I` identically.

**INTERVAL CERTIFIED.** Exact rational Krawczyk boxes of radius `10^-30`
isolate one real-algebraic preimage in each cycle record.  Every transition
probability exceeds `1/20`; the Krawczyk contraction is below `10^-20`; and
the inclusion margin exceeds `9*10^-31`.

**INTERVAL CERTIFIED.** Exact interval inverse bounds certify a nonsingular
`14 x 14` output block at each of those same preimages.  Since the omitted
quartic coordinate has nonzero partial derivative, the selected fourteen
coordinates are local coordinates on `V(I)`.  Both orientations consequently
cover the same relatively open fourteen-dimensional neighborhood in `V(I)`.

## Exact local parameter correspondences

Let `phi_i^M` denote the polynomial tensor map for orientation `i`, and let
`theta_i^*` be its certified common preimage.  Fix every parameter outside the
recorded nonsingular column block at its value in `theta_i^*`.  Let `pi_M`
select all four JC coordinates, all nine K2P coordinates, or the recorded
fourteen K3P local coordinates.

**PROVED.** The square map

\[
\pi_M\circ\phi_i^M
\]

has nonzero Jacobian at `theta_i^*`.  It therefore has a unique real-analytic
inverse germ `psi_i^M`.  Because its defining equations are polynomial and
its Jacobian is nonzero, this is an algebraic-function germ.  The exact local
parameter correspondence from orientation `i` to orientation `j` is

\[
\boxed{
F_{i\to j}^M(\theta)
=
\psi_j^M\!\left(\pi_M\phi_i^M(\theta)\right).
}
\]

For JC and K2P the branch is selected by the exact root-isolating interval and
positive arm roots.  For K3P it is selected by the exact rational Krawczyk
box.  Thus this is an exact branch specification, not a numerical matching
rule, although no global rational closed form is claimed.

## Grafting proof

For a group-based port tensor, gluing through a bridge multiplies the Fourier
coordinate of character `g` by the bridge multiplier `a_e(g)` and contracts
equal characters.  Equal local port tensors therefore remain equal after any
identical contraction.

**PROVED.** At the certified witnesses all nonzero arm multipliers are
positive.  For each nonzero character `g`, the three positive glued entries
`U_g,V_g,W_g` recover

\[
a_e(g)=\sqrt{U_gV_g/W_g}.
\]

This is one scalar equation for JC, two independent equations for K2P, and
three for K3P.  Hence the gluing map has a positive analytic inverse in the
certified neighborhood.  Tensor equality, strict stochastic positivity,
regularity, and the expected rank addition all survive iterative port
substitution.  The argument applies whenever both resulting networks satisfy
the required binary and acyclic conditions.

## Model hierarchy consequence

**PROVED.** `T` is universal across JC, K2P, and K3P.  Therefore richer
character-specific edge information does not identify which vertex of an
ordinary triangle is the reticulation.

**PROVED.** Combined with Milestones 4A and 6B, the currently certified
hierarchy is strict but not total recovery: K2P and K3P separate the inherited
`Theta` and every `Omega_chain`, while preserving `C_root`, `T`, and at least
the model-specific root-three-port ambiguities classified in Milestones 6C
and 6D.

**UNRESOLVED.** Complete K2P/K3P move systems and global if-and-only-if
theorems are not yet established.

## Replay

Run

```sh
PYTHONPATH=src .venv/bin/python src/verify_group_based_triangle_redirection.py
```

The verifier checks the complete graph census, all three pairwise formal `T`
relations, exact dependency hashes, common-point data, and rank assertions.
The machine-readable result is
`certificates/group_based_triangle_redirection.json`.
