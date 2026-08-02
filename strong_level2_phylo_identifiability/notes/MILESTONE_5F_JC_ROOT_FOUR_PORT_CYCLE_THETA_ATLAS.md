# Milestone 5F: complete four-port root blobs and the collapse of `Psi`

## Primary theorem

**PROVED.** The complete JC `bowtie` classification of every nontrivial
binary strongly tree-child level-2 root blob with exactly four labelled
outgoing ports is obtained by adjoining the root cycles to the theta atlas of
Milestone 3D.

There is no new primitive cross-generator move.  The only cycle--theta
collision consists of the twelve old dimension-seven `Psi` classes, and each
is exactly an application of the already proved two-port root-cycle move
`C_root` inside a larger tensor context.

**PROVED.** Consequently, `Psi` is not needed as a primitive move:

\[
\boxed{
\Psi
=
C_{\rm root}^{-1}
\circ(\text{reversible root placement})
\circ C_{\rm root}.
}
\]

The equality is an equality of complete open stochastic images, not merely a
common regular region.

## Complete root-cycle census

A four-port root cycle has one sink-reticulation port and three ordinary
ports distributed over its two directed sides.  Exact strong-tree-child and
side-symmetry reduction leaves the side counts

\[
(1,2),\qquad(0,3).
\]

**EXACTLY COMPUTED.** These give:

| object | count |
|---|---:|
| unlabelled rooted root cycles | 2 |
| leaf-labelled rooted root cycles | 48 |
| leaf-labelled semi-directed root cycles | 12 |
| rooted presentations per semi-directed topology | 4 |

**PROVED.** The two rooted layouts are reversible root placements on the
same semi-directed cycle.  Uniform JC reversibility therefore gives equality
of their complete open images.

**EXACTLY COMPUTED.** Exact symbolic Jacobian elimination gives dimension
seven for both unlabelled root-cycle parameterizations.

## Exact cross-generator atlas

Pull back the same sixty exact invariant polynomials used in the complete
four-port theta atlas.

**EXACTLY COMPUTED.** The 48 cycle presentations form twelve distinct exact
signatures, four rooted presentations per signature.  Those signatures agree
with precisely theta components

\[
96,97,\ldots,107,
\]

which are all and only the twelve dimension-seven theta components.  No
cycle signature agrees with any of the other 96 theta components.

**PROVED.** Different cycle signatures have different irreducible closures.
A cycle cannot be `bowtie_JC` with a theta component of dimension eight or
nine because `bowtie` requires equal local dimensions.  Milestone 3D already
separates every pair of distinct theta components.  These observations prove
exhaustiveness of the combined equal-dimensional atlas once overlap inside
the twelve matching classes is established.

## The graph identity behind `Psi`

Take the balanced root cycle `(1,2)`.  Its ordinary root has two tree
children, one beginning each directed side.  Replace that root fork by

\[
S\to U,qquad S\to V,qquad U\to V,
\]

where `U` is a tree vertex and `V` is a reticulation, and attach the two old
cycle sides below `U` and `V`.  Choosing which side lies below `U` gives the
two unlabelled theta census networks 18 and 19.

**EXACTLY COMPUTED.** For every one of the 24 labelled balanced cycles and
both side choices, exact coloured-DAG canonicalization identifies the
inserted network with one of the 48 theta presentations in components
96--107.  Every such theta presentation occurs exactly once.  For either
side choice, the insertion belongs to the same invariant component as its
source labelled cycle.

Thus the former `Psi` theta consists of a two-port root cycle sitting above a
second cycle whose two sides later reconnect.  Collapsing the upper root
cycle leaves the ordinary four-port root cycle.

## Contextual closure of `C_root`

Milestone 5C proves equality of the complete two-state port tensor for an
ordinary root fork and the two-port root cycle under JC, K2P, and K3P.

**PROVED.** This equality survives contraction with an arbitrary common
two-port tensor context.  If the local tensors are `P(x,y)=P'(x,y)` and the
remainder of the network contributes the conditional tensor `Q(x,y;g)`,
then

\[
\sum_{x,y}P(x,y)Q(x,y;g)
=
\sum_{x,y}P'(x,y)Q(x,y;g)
\]

for every leaf assignment `g`.  The two downstream continuations may be
separate components or may reconnect later inside the same blob; contraction
uses only equality at the two open state indices.

**PROVED.** Both directions of the positive parameter factorization remain
local and leave the entire downstream context unchanged.  Therefore each
four-port root cycle and each matching `Psi` theta have equal **complete open
stochastic images** under JC, K2P, and K3P.

This strengthens the earlier component-substitution statement: `C_root` is a
contextual tensor rewrite, not only a cut-edge gluing move.

## Combined component counts

Before adding cycles, every one of the twelve `Psi` components contained four
rooted and four semi-directed theta topologies.

**EXACTLY COMPUTED.** Each matching cycle signature contributes four rooted
presentations representing one semi-directed cycle.  Hence every combined
component contains

\[
\boxed{8\text{ rooted topologies and }5\text{ semi-directed topologies}.}
\]

All twelve components have complete-image equality between their cycle and
theta members.  The remaining 96 theta observational components are exactly
those from Milestone 3D.

The combined four-port atlas therefore has 660 labelled rooted topologies,
228 labelled semi-directed topologies, and 108 `bowtie_JC` components.

## Consequences for the move system

**PROVED.** At four root ports, the primitive JC move list can omit `Psi`.
The observed relations are generated by:

- reversible root placement;
- ordinary triangle redirection `T`;
- `Theta`;
- `Omega`; and
- contextual `C_root`.

No additional cycle--theta move occurs.

**PROVED.** The cycle/`Psi` class is triangle-free after suppressing the
global-root artifact.  Thus it does not create an additional ambiguity among
the one-triangle four-port root blobs in `L_1`; those remain covered by the
theta part of Milestone 3D.

**UNRESOLVED.** One-sided containments between dimension-seven cycle/`Psi`
models and dimension-eight or dimension-nine theta models are not classified
here.  Arbitrarily subdivided root blobs with five or more outgoing ports
also remain to be reduced to a bounded atlas.

## Machine replay

- `src/verify_jc_root_four_port_cycle_theta_atlas.py` regenerates both cycle
  topologies, all 48 labellings, exact rank-seven certificates, all sixty
  invariant pullbacks, the twelve cross-generator signature classes, and all
  48 graph insertions.
- `certificates/jc_root_four_port_cycle_theta_atlas.json` records the complete
  cycle networks, insertions, and combined observational components.

No numerical evidence, external catalogue, specialized phylogenetic
software, or literature search is used.
