# Exact class relations

## Topology sets

The already-simple and Holtgrefe single-root output classes agree, \(\mathsf{SD}_{0}=\mathsf{SD}_{H}\).  The cleanup convention admits additional rooted presentations.  Whenever cleanup yields a simple binary mixed graph, deterministic zipper contraction constructs an \(sd_0\) presentation of that same final labelled graph.  Thus the final topology sets agree on the binary LSA-valid simple-output domain, while the presentation fibres need not agree. The nontrivial inclusion is obtained by deterministic root-zipper contraction. This equality is structural; the open-model statement below is asserted on tree-child cleanup fibres, which are the fibres relevant to the landmark class.

## Rooting fibres

\[
\operatorname{Root}_{0}(N)=\operatorname{Root}_{H}(N)
\subseteq \operatorname{Root}_{clean}(N).
\]

The inclusion is proper. Cleanup can hide a root-created reticulation gadget that Holtgrefe excludes as a parallel semi-deorientation output and `sd0` rejects before cleanup.

## Weak and strong tree-childness

\[
W_{TC}(0)=W_{TC}(H)=W_{TC}(clean),
\]

because a tree-child cleanup rooting contracts to a tree-child already-simple rooting.

\[
S_{TC}(clean)\subsetneq S_{TC}(0)=S_{TC}(H).
\]

The primary and independent rooting censuses give a strict witness: its cleaned mixed graph has five `sd0` rootings and all five are tree-child, while an additional admissible cleanup rooting is not tree-child.

## Landmark class

\[
\mathcal S_2=
\mathsf{SD}_{clean}\cap S_{TC}(clean)\cap\{\text{level at most two}\}.
\]

The canonical representative `q(N)` is the same final mixed graph viewed through its `sd0` rooting fibre. It belongs to the baseline strong class and has the same complete open JC image. Hence the baseline classification transfers exactly to `mathcal S_2`.
