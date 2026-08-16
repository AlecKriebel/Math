# Comparison of semi-directed conventions

## Sources and version lock

This crosswalk uses the following sources.

1. **Baseline manuscript (`sd0`)**: *Strong Tree-Childness Is a Sharp Identifiability Boundary for Level-2 Jukes--Cantor Networks*, August 2026, Section 2.1.
2. **Englander et al.**: *Identifiability of Phylogenetic Level-2 Networks under the Jukes--Cantor Model*, bioRxiv 2025.04.18.649493, cited manuscript version 4 (2026).  The publicly indexed full-text definition says that the rooted input is a binary DAG without parallel edges and without 2-blobs or non-leaf 1-blobs; the semi-directed graph is obtained by removing directions from non-reticulation edges, suppressing degree-two vertices, and identifying parallel edges.  Strongly tree-child means that every directed network from which the semi-directed graph is obtained is tree-child.
3. **Brits--Holtgrefe--van Iersel--Martin**, arXiv:2607.12919v2, 29 July 2026. Definition 2.1 uses a binary rooted DAG with no parallel edges and the LSA condition. The full semi-directed topology is obtained by undirecting non-reticulation edges, suppressing the root, and exhaustively suppressing resulting parallel edges and degree-two vertices. Definitions 2.2 and 2.3 separately define restriction and displayed networks.
4. **Holtgrefe--Huber--van Iersel--Jones--Moulton**, version of record, *Theory in Biosciences* 145, article 4 (2026). Semi-deorientation replaces an arc by an edge when its head has indegree one and suppresses degree-two roots. Outputs having parallel arcs are not treated as mixed graphs. A rooting is a rooted network whose semi-deorientation is exactly the mixed graph. Weak and strong tree-childness quantify over these rootings; Theorem 5 characterizes strong tree-childness by absence of omnians.
5. **Sullivant**, *Phylogenetic Network Models as Graphical Models*, arXiv:2507.23056 and the 2026 journal version. Proposition 4.6 treats degree-two contraction for multiplicatively closed and splittable models. Proposition 5.4 treats suppression of an entire hidden 2-blob under multiplicative closure, convex closure, and splittability. These are statistical model transformations, not the definition of the full standard semi-directed topology.

## Three operations that must not be conflated

| Operation | `sd0` baseline | Englander et al. | Brits et al. v2 | Holtgrefe et al. | Sullivant |
|---|---|---|---|---|---|
| **Form the full semi-directed topology** | Retain arrowheads into reticulations; undirect all other arcs; delete the binary root and join its children; accept only if the result is already a simple binary mixed graph. No later cleanup. | Remove non-reticulation directions; suppress degree-two vertices; identify parallel edges. The rooted input is additionally stated to have no 2-blobs and no non-leaf 1-blobs. | Undirect non-reticulation edges; suppress the root; exhaustively suppress resulting degree-two vertices and identify resulting parallel edges. | Replace arcs whose head has indegree one by edges; suppress degree-two roots. A parallel output is not a mixed graph and is outside the considered class. | No single standard-topology definition is imposed; graph-local statistical equivalences are proved. |
| **Restrict to a leaf subset** | The classification proof uses Fourier marginalization and exact serial-edge products; this is not a second definition of the full topology. | Union of up-down paths, then exhaustively suppress degree-two vertices, identify parallel edges, and suppress 2-blobs. | Union of up-down paths, then exhaustively suppress degree-two vertices and identify parallel edges. Higher-level 2-blobs are not automatically suppressed. | Not the identifiability restriction convention studied in that paper. | Degree-two and 2-blob transformations are justified under model hypotheses. |
| **Form a displayed network/tree** | Choose one incoming parent at every reticulation; the Fourier formula is evaluated on the resulting tree. | A switching may have degree-two vertices and non-taxon leaves; displayed trees are obtained after contraction. | Delete selected reticulation edges, take the union of up-down paths, then suppress degree-two vertices and identify parallel edges. | Not used as the definition of semi-deorientation. | The displayed-tree model is the principal statistical object. |

## Locked classes

### `SD0`

A labelled simple binary mixed graph belongs to `SD0` when it is the one-step `sd0` image of a binary LSA-valid rooted network. No post-root cleanup is allowed.

### `SDclean`

A labelled simple binary mixed graph belongs to `SDclean` when it is obtained from a binary LSA-valid rooted network by the Brits-style operation: root suppression followed by exhaustive identification of newly parallel copies and suppression of newly unlabelled degree-two vertices.

### `SDH`

`SDH` is the binary single-root LSA-valid specialization of the Holtgrefe semi-deorientation framework, restricted to outputs that are mixed graphs (hence no parallel output).

For each convention, `Root_*(N)` is the complete set of rooted presentations admitted by that convention. `W_TC(*)` means that at least one member of `Root_*(N)` is tree-child. `S_TC(*)` means that `Root_*(N)` is nonempty and every member is tree-child.

## Exact relationship proved in this release

For already-simple outputs, \(\mathsf{SD}_0=\mathsf{SD}_{\mathrm H}\).  The broader cleanup presentation class contains additional rooted presentations, but deterministic zipper contraction sends every cleanup output that is a simple binary mixed graph to the same final graph with an \(sd_0\) presentation.  In particular, on the weak and strong tree-child classes relevant here, every cleanup topology has a canonical already-simple representative. Their rooting sets do not coincide:

\[
\operatorname{Root}_0(N)=\operatorname{Root}_{\mathrm H}(N)
\subseteq \operatorname{Root}_{\mathrm{clean}}(N).
\]

Consequently, on the binary LSA-valid simple-output class,

\[
W_{\mathrm{TC}}(\mathrm{clean})=W_{\mathrm{TC}}(0)=W_{\mathrm{TC}}(\mathrm H),
\qquad
S_{\mathrm{TC}}(\mathrm{clean})\subsetneq S_{\mathrm{TC}}(0)=S_{\mathrm{TC}}(\mathrm H).
\]

The strictness is witnessed by the explicit three-leaf root-cleanup presentation in `certificates/primary_convention_frontier.json`: its cleaned graph has five `sd0` rootings, all tree-child, but the displayed cleanup rooting itself is not tree-child.

Thus literal convention equivalence in the sense of preserving every admissible rooting is false. The correct closure is Outcome Q: a canonical model-preserving quotient from cleanup presentations to their already-simple topology.
