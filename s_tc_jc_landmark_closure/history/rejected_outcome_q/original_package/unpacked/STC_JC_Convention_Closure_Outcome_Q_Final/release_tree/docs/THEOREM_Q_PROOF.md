# Theorem Q: canonical cleanup quotient on the literature strong class

## Locked conventions

Let `sd0(D)` be the manuscript operation: retain only arrowheads on arcs entering reticulations, undirect every other arc, delete the binary root, join its two children, and accept only if the result is already a simple binary mixed graph. Let `clean(D)` perform the same root suppression and then exhaustively identify the resulting parallel copies and suppress resulting unlabelled degree-two vertices.

For a simple labelled mixed graph `N`, let `Root_0(N)` and `Root_clean(N)` be the binary LSA-valid rooted presentations admitted by the two operations. The Englander rooted inputs additionally have no 2-blobs and no non-leaf 1-blobs; this restriction is imposed whenever the phrase `literature strong class` is used below.

## Structural zipper lemma

Let `D` be a binary LSA-valid rooted network and let its root children be `p,q`.

* The children are distinct, because parallel root arcs are forbidden.
* If `p,q` are not adjacent, one-step root suppression preserves every total degree and creates no parallel copy. At most one child is reticulate: if both were reticulate, the two opposite root branches and their second parents would force a directed cycle. Hence `sd0(D)` is already defined.
* Suppose cleanup is needed. Then `p,q` are adjacent. Up to exchanging their names the arc is `p->q`; `q` is reticulate. The parent `p` cannot be reticulate, because then its unique child would be `q`, so every root-to-leaf path would pass through `q`, contradicting the LSA condition. Thus `p` is a tree vertex.

Write `a` for the other child of `p` and `b` for the child of `q`. The vertices `a,b` are distinct, again by the LSA condition. Identifying the two copies of `p-q` and suppressing the resulting degree-two vertices `p,q` replaces the whole root-created gadget by an edge `a-b`.

Delete the old root, `p,q`, insert a new root, and attach it to `a,b`. This produces another binary LSA-valid rooted network `D'`, and

`sd0(D') = clean(D)`.

If `D` is tree-child, then `a` and `b` are tree vertices or leaves: `p` already has the reticulate child `q`, and `q` is reticulate with unique child `b`. Hence `D'` is tree-child. In this case `a,b` cannot be adjacent, so the cleanup has exactly one zipper step.

For arbitrary LSA-valid inputs the same deterministic contraction can be iterated, removing two internal vertices and one root-created reticulation at each step. This proves structural equality of the final topology sets. The statistical assertion below is needed only on the tree-child fibres.

## Exact open-JC zipper identity

For one tree-child zipper use edge multipliers

`alpha : root->p`, `beta : root->q`, `gamma : p->q`, `u : p->a`, `v : q->b`,

and let `lambda` be the inheritance probability selecting `root->q`. For every nonzero boundary character the complete two-terminal Fourier tensor equals

\[
(1,\kappa,\kappa,\kappa),\qquad
\kappa=uv\{\lambda\alpha\beta+(1-\lambda)\gamma\}\in(0,1).
\]

This is exactly one ordinary JC edge with multiplier `kappa`. Conversely, for any `x in (0,1)` put

\[
c=\frac{1+x}{2},\qquad m=\frac{4x}{(1+x)^2},
\]

choose `u=v=c`, `gamma=m`, `lambda=1/2`, and the strict rational factorization

\[
\alpha=\frac{1+m}{2},\qquad \beta=\frac{2m}{1+m}.
\]

Then `kappa=x`, every parameter lies in `(0,1)`, and

\[
1-m=\frac{(1-x)^2}{(1+x)^2}>0,
\qquad
\frac{\partial\kappa}{\partial\gamma}=uv(1-\lambda)>0.
\]

Thus contraction and insertion have equal complete open two-boundary JC tensor images, with a positive analytic submersion and a strict analytic section. Equality survives arbitrary common tensor contexts, including a context reconnecting the two terminals.

## Class relations

The Holtgrefe binary one-root mixed-graph specialization has the same rootings as `sd0`: parallel outputs are outside its mixed-graph class. The cleanup convention has a larger rooting fibre.

\[
\mathsf{SD}_{0}=\mathsf{SD}_{H}=\mathsf{SD}_{clean}
\]

as sets of final simple labelled mixed graphs, while

\[
\operatorname{Root}_{0}(N)=\operatorname{Root}_{H}(N)
\subseteq \operatorname{Root}_{clean}(N).
\]

The weak classes agree because every tree-child cleanup rooting contracts to a tree-child `sd0` rooting and every `sd0` rooting is a cleanup rooting. The strong classes satisfy

\[
S_{TC}(clean)\subsetneq S_{TC}(0)=S_{TC}(H).
\]

The inclusion is strict: the released three-leaf witness has five `sd0` rootings, all tree-child, but also has a non-tree-child cleanup rooting in an allowed 3-blob.

## Convention-closure theorem

Define the intended literature class

\[
\mathcal S_2=
\mathsf{SD}_{clean}\cap S_{TC}(clean)\cap\{\text{binary LSA-valid level at most two}\},
\]

using the Englander/Brits root-suppression-and-cleanup convention and the Englander rooting restrictions when comparing directly with that paper.

For `N in S_2`, define `q(N)` to be the same final labelled mixed graph viewed with its canonical `sd0` rooting fibre. The zipper lemma gives at least one tree-child `sd0` rooting; strong cleanup tree-childness implies every `sd0` rooting is tree-child. The exact zipper identity shows that every cleanup rooting of `N` has the same complete open JC image as `q(N)`.

Therefore

\[
M^{JC}_{N}=M^{JC}_{q(N)},\qquad
N\preceq_{JC}N'\iff q(N)\preceq_{JC}q(N'),
\]

and likewise for symmetric regular overlap.

Because `q` is the identity on the final mixed graph, it preserves labels, retained arrowheads, reticulations of the cleaned topology, blobs, level, cut splits, bridge trees, projective local tensors, ports and their order, ordinary triangle redirection, and the proper algebraic exceptional set. No new finite-atlas core occurs.

Applying the verified `sd0` theorem to `q(N)` proves the full classification for `mathcal S_2`.

## Sharpness

The four-leaf Theta pair is already simple: `sd0` and `clean` give the same two mixed graphs. Each has five `sd0` rootings, exactly two tree-child; therefore each lies in `W_TC(clean) \ S_TC(clean)`. Their labelled graphs remain nonisomorphic and non-`T`-equivalent, and cleanup does not change their exact JC parameterizations. The all-`n` leaf-substitution theorem is unchanged.
