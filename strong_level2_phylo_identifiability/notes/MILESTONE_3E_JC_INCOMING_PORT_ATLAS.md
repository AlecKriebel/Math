# Milestone 3E: exact incoming-port JC atlas and exhaustive root-locality

## Scope

Take every one of the 612 labelled root-spanning networks classified in
Milestone 3D.  Rename its old root `S` as a tree vertex `IN`, add a new root
`RHO`, add a new leaf labelled `5`, and add

```text
RHO -> IN,    RHO -> 5.
```

The new leaf represents the incoming state block.  Suppressing the new global
root combines its two incident multipliers into one effective positive
incoming/outgroup multiplier.  Leaves `1,2,3,4` remain the four outgoing
ports.

**PROVED.** Every resulting network is binary, acyclic, strongly tree-child,
and level 2.  Adding the new root and leaf introduces only cut edges.  Inside
the nontrivial blob, `IN` simply unsuppresses the old root edge, so the blob
still has exactly two reticulations.  No parallel arc or directed 2-cycle is
introduced.

This is an exact five-port tensor classification for every incoming-port lift
of the root-spanning simple four-port census.  It does not yet enumerate
larger subdivisions carrying six or more ports.

## Primary theorem

**PROVED.** Let `A_in` be this 612-network incoming-port class.  For
`N,N' in A_in` under JC,

\[
\boxed{
N\bowtie_{\rm JC}N'
\quad\Longleftrightarrow\quad
N=N'\text{ up to labelled isomorphism, or }N,N'\text{ differ by }T.
}
\]

Thus ordinary triangle redirection is the complete nonroot move system in
this finite atlas.

**PROVED.** The root-local moves `Theta`, `Psi`, and `Omega` all disappear
after the incoming state port is exposed.  Any surviving pair inherited from
one of those root components is either an ordinary `T` pair or is separated
from full-dimensional overlap.

This is an exhaustive root-locality theorem for every reduced strong
level-2 generator represented in the root-spanning four-port slice, not only
for the individual `Psi` and `Omega` gadgets studied earlier.

## Topological census

**EXACTLY COMPUTED.** The 612 lifted rooted networks are pairwise
nonisomorphic.  Their 612 leaf-labelled semi-directed topologies are also
pairwise nonisomorphic: the labelled incoming leaf records the attachment
site that root suppression previously hid.

Exhaustive underlying-graph comparison finds exactly 96 `T` pairs and no
larger `T` component.  Therefore the lifted atlas has

\[
420+96=516
\]

candidate observational classes:

| component size | number |
|---:|---:|
| 1 | 420 |
| 2 | 96 |

The 96 triangle-redirection pairs occur in four census-index families:

```text
(4,13), (6,14), (8,15), (18,19),
```

with 24 leaf relabellings in each family.

**PROVED.** Marginalizing leaf `5` recovers the corresponding root-spanning
four-leaf model exactly.  Hence no lifted full-dimensional ambiguity can
cross two root components already separated in Milestone 3D.  The direct
five-port certificate below is stronger: it gives different signatures to
all 516 lifted components without relying on that reduction.

## Exact dimensions

There are 51 nonzero-character symmetry orbits for zero-sum JC assignments on
five leaves, including the all-zero coordinate.

Normalize the five pendant multipliers to one.  The complete tangent matrix
then has:

1. ten core columns, from eight internal edge multipliers and two inheritance
   probabilities; and
2. five pendant support columns
   `1[g_i != 0] q_g`, one for each port.

As in Milestone 3D, this normalization differs from the complete Jacobian on
the open pendant torus only by invertible row and column scalings.

**EXACTLY COMPUTED.** Fraction-free Bareiss elimination over the exact
multivariate polynomial ring over `Q` gives the dimensions

```text
(11,11,11,11,10,11,10,11,10,11,11,11,11,10,
 10,10,11,11,10,10,11,11,11,11,11,11,11).
```

Thus eight unlabelled parameterizations have dimension 10 and nineteen have
dimension 11.  At the component level there are 96 dimension-10 components
and 420 dimension-11 components.

**PROVED.** In characteristic zero, these exact generic symbolic ranks equal
the transcendence degrees of the coordinate fields.  They provide upper and
lower dimension proofs, not sampled lower bounds.

## Quartet witness theorem

For each outgoing label `i in {1,2,3,4}`, marginalize that leaf and retain the
quartet

\[
\{1,2,3,4,5\}\setminus\{i\}.
\]

Every retained quartet contains the incoming block `5` and three outgoing
blocks.

**PROVED.** Two invariant templates from Milestone 3D suffice:

| root-atlas template | degree | support | `S_4` orbit size |
|---:|---:|---:|---:|
| 2 | 3 | 18 | 3 |
| 4 | 4 | 19 | 12 |

Applying all 15 relabelled invariants to each of the four incoming quartets
gives 60 exact zero/nonzero pullbacks per lifted model.

**EXACTLY COMPUTED.** Every pullback is expanded as a multivariate polynomial
over `Q` in the complete displayed-tree parameterization.  The 60-bit
signature is constant on each of the 96 `T` pairs and different on all 516
candidate components.  Its deterministic digest is

```text
d1b2c37e78fb83725aabd16d5d72dd410e159dce7a0f170efdb8e9c388efcbae
```

The signatures separate all 92,550 pairs of distinct components having equal
dimension.

**PROVED.** Therefore every non-`T` full-dimensional local distinction in
this atlas is witnessed on four descendant blocks.  No intrinsically
five-leaf invariant is needed.  This establishes witness bound `k=4` for the
incoming-port slice.

## Proof of the biconditional

**PROVED.** Every `T` pair has a full-dimensional regular stochastic overlap.
The exact triangle port-tensor correspondence allows arbitrary positive
components at all ports.  The arm multipliers can be chosen sufficiently
small that both redirected parameter sets lie in the open cube; exact model
dimensions agree across each pair.  The inverse-function argument gives a
common regular open region.

**PROVED.** Every network model closure is irreducible, being the closure of
the polynomial image of an irreducible parameter space.  If two
equal-dimensional models had a full-dimensional regular stochastic
intersection, their irreducible closures would be equal.  The distinct exact
signatures rule this out for different components.

Models of dimensions 10 and 11 cannot satisfy `bowtie_JC` because that
relation requires equal local dimensions.  This proves the theorem.

No claim of equality of complete stochastic images is made for `T` pairs.

## Directed containments

There are

\[
96\cdot420=40{,}320
\]

ordered dimension-10 to dimension-11 component pairs.

**EXACTLY COMPUTED.** The two quartet-template families refute 39,168 of
these directions: in each case an invariant vanishing on the proposed larger
model is a nonzero polynomial on the proposed smaller model.

**UNRESOLVED.** The remaining 1,152 directions are not classified here.  The
failure of this finite invariant set to refute them does not imply
containment.  They do not affect the `bowtie_JC` biconditional.

## Machine replay

- `src/verify_jc_incoming_port_atlas.py` regenerates all lifted networks,
  checks strong binarity, computes all exact dimensions, finds every `T`
  relation, and replays all quartet signatures.
- `certificates/jc_incoming_port_atlas.json` records all 612 lifted network
  encodings, all 516 component memberships, symbolic-rank hashes, signatures,
  and unresolved directed pairs.
- The invariant templates are stored in
  `src/jc_root_spanning_atlas_data.py`; no coefficients were fitted during
  exact replay.

The discovery probe used finite fields only to select the two compact
template families.  No modular or numerical result appears in the theorem.

## Consequence and next step

**PROVED.** For every reduced strongly tree-child level-2 generator visible
with one incoming and four outgoing ports, exact generic JC data determine
the complete labelled semi-directed topology modulo triangle redirection.
The three extra root moves are artifacts of suppressing the distinguished
incoming attachment at the global root.

**UNRESOLVED.** To promote this to `L_1`, the next tasks are:

1. prove that every larger port subdivision has a distinguishing induced
   incoming quartet unless it is a local `T` or the inherited root `Theta`;
2. reconstruct the cut-edge/blob tree from generic Fourier data; and
3. exclude coordinated ambiguity between a root-local move and a distant
   blob.
