# Version-locked prior-work comparison

Audit date: 2026-08-09

This comparison is deliberately narrow.  It supports the claims made in the
sharpness manuscript and does not claim priority from unsuccessful keyword
searches.

## Exact sources read

| Source | Version used | SHA-256 |
|---|---|---|
| Ardiyansyah, *Distinguishing Level-2 Phylogenetic Networks Using Phylogenetic Invariants* | arXiv:2104.12479 | `fd54745ef618a23c45371f09d65ae6362fb9b04d8566cf0cc07d151c0bd88d75` |
| Englander et al., *Identifiability of Phylogenetic Level-2 Networks under the Jukes--Cantor Model* | bioRxiv v4, posted 2026-07-04 | `260a977d9629eeb1b9ea0b7afa6d8179625609748ce20a2007927df5aa6e874f` |
| Holtgrefe et al., *Characterizing Semi-Directed Phylogenetic Networks and Their Multi-Rootable Variants* | arXiv:2507.18772; checked against the 2026 journal metadata | `4f995cdf0022ae8a098cd2f2e9408bc9ad857ed0d0de7295c455ecc0e2105aa3` |
| Currie et al., *Semialgebraic Conditions for Identifying Triangles in Phylogenetic Networks* | arXiv:2606.26673v1 | `0cbd173c7c60e63a7b1606d85f290449367c887c479e1eb939f234d4f0ef27ef` |
| Sullivant, *Phylogenetic Network Models as Graphical Models* | arXiv:2507.23056v2, dated 2026-07-16 | `9d2d188f20c1325723621b2da5c231595033d3c9ddf30a232a429df4df6bc614` |
| Brits et al., *On Tree--Network Distinguishability and Full Identifiability of Phylogenetic Networks* | arXiv:2607.12919v2 | `9ace8164beaf1bac82c5fd5b450df85b59adf5de5d57cd3832ba199a0a8fc5e2` |

The files were read locally from the audit cache.  Public metadata and version
dates were rechecked on arXiv, bioRxiv, and the TU Delft journal record.

## Claim-by-claim relation

| Earlier result | Relation to the submitted theorem |
|---|---|
| Ardiyansyah, Proposition 5.4 and conclusion | The paper explicitly states that its methods did not settle distinguishability for two four-leaf simple networks belonging to the same type.  The present theorem supplies one exact labelled, triangle-containing same-type pair with full-dimensional **stochastic** overlap.  It does not classify every same-type pair and is therefore an instance-level resolution, not a complete resolution of Ardiyansyah's broader open problem. |
| Englander et al., Definition 2.1, Definition 2.2, and Theorem 3.2 | Their theorem gives generic JC identifiability for binary, triangle-free, strongly tree-child, level-2 semi-directed networks.  The present pair contains a triangle and, more importantly, is weakly but not strongly tree-child: each topology has five admissible LSA-valid rootings, of which three are not tree-child.  There is no contradiction.  The present result shows why the strong/weak distinction cannot be dropped without additional ambiguity. |
| Holtgrefe et al., Section 5 and Theorem 5 | This is the source of the weakly/strongly tree-child terminology and the omnian criterion.  The present pair gives a concrete statistical consequence of lying in the weak-but-not-strong difference.  The paper's graph theorem does not itself establish JC model overlap. |
| Currie et al. | They give a complete semialgebraic analysis of three-leaf JC triangle models and show full-dimensional intersections and differences among triangle orientations.  The present pair has four leaves, a level-2 theta blob with two reticulations, and changes a labelled pendant attachment in the underlying semi-directed graph.  It is not merely a triangle-orientation instance. |
| Sullivant, Sections 4--5 | The local-modification framework yields model equivalences involving stacked reticulations and studies two-port/2-blob phenomena.  The present rooted witnesses have no reticulation child and the exhibited move is a leaf-placement transfer in a six-vertex theta blob.  The audited version did not state this exact pair or all-taxa cherry extension.  This is a scope comparison, not a categorical priority claim. |
| Brits et al., Theorem 4.9 and Section 5 | Their full-identifiability theorem concerns level-1 networks modulo triangle redirection, and their later results address suppression/detection of 2-sub-blobs.  The present networks are level 2 and the two topologies are not related by triangle redirection.  No 2-sub-blob equivalence is used in the submitted proof. |

## Terminology and convention lock

The manuscript uses the LSA-valid rooted-network and simple semi-directed
root-suppression conventions of Englander et al.  It makes the reduction map
explicit as `sd_0` and admits a rooting only when root suppression already
produces the stated simple binary mixed graph while preserving every
reticulation and incoming arrowhead.  It does **not** use a broader induced-
subnetwork cleanup that merges parallel edges or subsequently erases
reticulation vertices.

This distinction matters: the withdrawn positive manuscript mixed those two
operations and thereby changed the set of rootings quantified over by strong
tree-childness.  The sharpness pair and its rooting census survive the locked
narrow convention.

## Safe novelty statement

The evidence supports the following restrained statement:

> The manuscript gives an exact four-leaf, level-2, weak-but-not-strong
> tree-child JC ambiguity that is not explained by ordinary triangle
> redirection, and proves that the ambiguity persists for every number of
> leaves by an analytic leaf-substitution inverse.

The audit does not support claiming the first level-2 nonidentifiability
result of any kind, the first local-modification equivalence, or a completed
classification of weakly or strongly tree-child level-2 networks.
