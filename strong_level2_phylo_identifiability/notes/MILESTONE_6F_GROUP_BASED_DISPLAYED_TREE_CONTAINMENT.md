# Milestone 6F: every displayed tree is stochastically contained under K2P and K3P

## Outcome

This milestone proves a global one-sided-containment theorem.  It resolves the
ordinary-tree side of the three-port K2P/K3P atlas and gives exponential
topology fibers inside the strongly tree-child level-1 subclass.

The result is deliberately distinguished from `bowtie`: the tree image has
smaller dimension than the ambient network images.

## Main theorem

Let `T` be any displayed tree of a binary rooted phylogenetic network `N`.

**PROVED.** For each

\[
M\in\{\mathrm{K2P},\mathrm{K3P}\},
\]

there is complete open stochastic containment

\[
\boxed{
\mathcal M_T^M\subseteq\mathcal M_N^M.
}
\]

Thus every exact distribution obtained from strictly positive edge kernels on
`T` has a realization on `N` in which every network edge transition matrix is
strictly positive and every inheritance probability lies strictly between
zero and one.

**PROVED.** The theorem does not require level 2 or tree-child assumptions.  It
holds for every finite binary rooted network and therefore applies in
particular to `L_1`, `L_*`, and `S_2`.

**PROVED.** The same construction is absent from the stipulated JC domain: it
uses the uniform edge kernel, whose JC Fourier multiplier is `x=0`, while the
problem requires `0<x<1`.  Milestone 5E proves that already for a three-port
cycle, the open JC tree and reticulate interiors are disjoint.

## Uniform-edge collapse lemma

Fix a reticulation `r`, retain one parent edge with transition kernel `K`, and
let `p in (0,1)` be the inheritance probability of that parent.  Put the
uniform group-based kernel

\[
U=(1/4,1/4,1/4,1/4)
\]

on the other incoming edge.

Conditional on the two parent states, the transition law into `r` is

\[
\boxed{
K_{\rm eff}=pK+(1-p)U.
}
\]

It is independent of the state at the discarded parent.  Therefore the
reticulation and its discarded incoming edge may be removed and replaced by
one ordinary edge carrying `K_eff`, in an arbitrary surrounding network
context.

Let `a_K(g)` be the Fourier multiplier of `K`.  Since

\[
\widehat U(0)=1,
\qquad
\widehat U(g)=0\quad(g\ne0),
\]

we have

\[
\widehat K_{\rm eff}(0)=1,
\qquad
\widehat K_{\rm eff}(g)=p\,a_K(g)\quad(g\ne0).
\]

**EXACTLY COMPUTED.** The verifier expands all four probability-coordinate
identities and all four Fourier identities over `Q`.  It also verifies that
every equality defining any K2P character convention is preserved.

**PROVED.** `K_eff` is strictly positive, because every entry is
`p K_h+(1-p)/4>0`.  K2P is preserved by the mixture with `U`; K3P imposes no
further equality.  The uniform kernel itself is a strict interior stochastic
point for both models even though its three nonzero Fourier multipliers vanish.

This last observation is essential: a zero Fourier multiplier is not a
stochastic boundary under the K2P/K3P domains used here.

## Collapsing all reticulations

Choose one incoming parent at every reticulation according to the displayed
tree `T`.  Put `U` on every unchosen incoming edge and apply the local lemma
one reticulation at a time.

**PROVED.** The resulting ordinary tree is exactly the chosen displayed tree
before suppression of degree-two vertices.  Every retained reticulation edge
contributes an additional JC convolution factor `J_p`, whose nonzero Fourier
multipliers all equal its inheritance probability `p`.

No independence assumption between blobs is used: the local conditional law
has already lost all dependence on the discarded parent state, so the
replacement is valid inside arbitrary upstream and downstream contexts.

## Assigning strict parameters for every target tree point

It remains to realize an arbitrary strict target kernel on each edge of `T`
as the convolution of all network-edge and inheritance factors that collapse
onto it.

The positive factorization lemma from Milestone 5C says that for every strict
group-based kernel `R`, if `m` is its least probability coordinate and
`epsilon=2m`, then

\[
R=J_{1-\epsilon}*D,
\]

where `J_(1-epsilon)` is strict JC and `D` is a strict kernel in the same one
of JC, K2P, or K3P.  The formulas are rational on each of the four chambers
selecting the least coordinate.

**EXACTLY COMPUTED.** The verifier replays all four chambers, sixteen
probability-convolution identities, and twelve Fourier-product identities.

**PROVED.** Repeated factorization extracts one strict JC factor for every
inheritance probability and then enough additional strict factors for every
ordinary network edge on the corresponding suppressed path.  Assign the
Fourier multiplier of each extracted JC factor as the retained-parent
inheritance probability.  It lies in `[1/2,1)`, hence in `(0,1)`.  Assign the
uniform kernel to every discarded parent edge.

This constructs a valid open network parameter point for every open target
tree parameter point and proves complete stochastic containment, not merely
closure containment.

## Three-port atlas corollary

The two unlabelled three-port rooted cycle presentations are records `1` and
`2` in the exhaustive census.

**EXACTLY COMPUTED.** In record `1`, making edge `1` uniform gives the effective
three-star arms

\[
\begin{aligned}
A_0(g)&=a_0(g)a_2(g)a_4(g),\\
A_1(g)&=a_5(g),\\
A_2(g)&=(1-\lambda)a_3(g)a_6(g),\qquad g\ne0,
\end{aligned}
\]

with `A_i(0)=1`.  In record `2`, making edge `0` uniform gives the same formulas
except `A_0(g)=a_2(g)a_4(g)`.

**EXACTLY COMPUTED.** Direct displayed-tree contraction verifies all nine K2P
orbit coordinates and all sixteen K3P zero-sum coordinates for both records.
Port labelling and the two root presentations cover all nine rooted and all
three semi-directed triangle orientations.

Therefore

\[
\boxed{
\mathcal M_{\rm tree}^{\rm K2P}
\subsetneq
\mathcal M_{\rm cycle}^{\rm K2P},
\qquad
\mathcal M_{\rm tree}^{\rm K3P}
\subsetneq
\mathcal M_{\rm cycle}^{\rm K3P}.
}
\]

**PROVED.** The dimensions are respectively

\[
6<9\quad\text{and}\quad9<14.
\]

Thus `tree preceq cycle` in both models, but `tree bowtie cycle` is impossible
by unequal dimension.  The reverse one-sided containment is impossible by the
same dimension comparison.

**EXACTLY COMPUTED.** At the common rational tree tensor with all three
effective arm multiplier vectors equal to `1/8`, every pair coordinate is
`1/64` and every all-distinct triple coordinate is `1/512`.  The ordinary tree
has exact regular ranks six and nine, with minors

\[
-1/65536,
\qquad
-1/268435456.
\]

Both cycle realizations have minimum transition probability `1/8`.  Their
parameterization ranks at these containment witnesses are eight under K2P and
twelve under K3P, with explicit nonzero minors recorded in the certificate.
These are critical strata of the larger cycle models, whose generic
dimensions are nine and fourteen.

**EXACTLY COMPUTED.** The K3P quartic from Milestone 6D vanishes identically on
the full symbolic three-port tree parameterization, as required by the
containment in the `H14` cycle class.

## Exponential strong family

For `m>=1`, begin with the rooted labelled caterpillar on

\[
L_0,L_1,\ldots,L_{m+1}.
\]

At its `i`-th nonroot branching site, independently choose either the ordinary
tree vertex or the triangle gadget

\[
A_i\to B_i,qquad A_i\to C_i,qquad B_i\to C_i,
\]

where `C_i` is reticulate, `B_i` carries side leaf `L_i`, and `C_i` continues
down the caterpillar.  Denote the resulting network by `E_epsilon`, with
`epsilon in {0,1}^m`.

**PROVED.** Every `E_epsilon` is binary, acyclic, strongly tree-child, and
level 1, hence level 2.  Its nontrivial blobs are exactly the
`sum(epsilon_i)` edge-disjoint triangles.  Every other edge is a bridge, and
both sides of every bridge contain a labelled leaf.

**PROVED.** Choosing the direct edge `A_i->C_i` in every present triangle and
suppressing degree-two vertices gives the same labelled caterpillar tree for
all bit vectors.

**PROVED.** The `2^m` rooted and semi-directed topologies are pairwise
nonisomorphic and pairwise non-triangle-equivalent.  The labelled descendant
cluster at site `i` identifies that site, while triangle redirection can
neither create nor delete its three-cycle.  Thus the bit vector is a complete
isomorphism invariant within this family.

Combining this graph construction with the displayed-tree theorem gives:

**PROVED.** For every `m>=1`, every strict K2P or K3P distribution on the base
caterpillar has at least

\[
\boxed{2^m}
\]

pairwise non-triangle-equivalent compatible strongly tree-child level-2
topologies on only `m+2` leaves.

The common tree-image dimensions are

\[
4m+2\quad\text{under K2P},
\qquad
6m+3\quad\text{under K3P}.
\]

To see these dimensions from first principles, a binary unrooted tree on
`n=m+2` leaves has `2n-3` edges.  For each independent character class, the
two-leaf Fourier coordinates recover all path products; the tree path-incidence
matrix has rank `2n-3`.  K2P has two independent classes and K3P has three.

**PROVED.** The multiplicity statement holds on the complete open tree image,
and hence at every generic regular tree parameter point.  It is a one-sided
generic ambiguity: the common tree image is not full-dimensional in network
members having reticulations.  No pairwise `bowtie` claim is made for this
family.

**EXACTLY COMPUTED.** The verifier generates every member for `m=1,2,3,4`,
checks the binary and strong degree conditions, identifies every triangle and
bridge, verifies the displayed caterpillar, and obtains exactly `2^m` rooted
and semi-directed canonical codes.  Complete machine-readable vertices,
edges, leaves, bit vectors, and topology hashes are stored in the certificate.

## Scientific consequence

**PROVED.** Model enrichment is not monotone for topology identifiability.
K2P and K3P separate the JC-specific `Theta` and `Omega_chain` moves, but their
larger strict Markov domains include the uniform kernel as an interior point.
That single fact creates universal displayed-tree containment and exponential
one-sided topology fibers that are absent from the stipulated positive-
multiplier JC model.

In particular, exact infinite-data K2P or K3P sequence distributions generated
on a tree cannot generically certify the absence of any reticulate history
that displays that tree.

## Classification boundary

**PROVED.** This theorem supplies the requested cross-generator one-sided
containment alternative and closes ordinary tree versus triangle-cycle
relations under all three models.

**UNRESOLVED.** It does not classify `bowtie` between arbitrary K2P/K3P blobs,
nor does it prove that every network compatible with a generic tree
distribution must display that tree.  Exact topology multiplicity may
therefore exceed the certified lower bound.

## Replay

Run

```sh
PYTHONPATH=src .venv/bin/python src/verify_group_based_displayed_tree_containment.py
```

The exact machine-readable certificate is
`certificates/group_based_displayed_tree_containment.json`.
