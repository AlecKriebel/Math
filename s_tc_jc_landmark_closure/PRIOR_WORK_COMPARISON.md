# Prior-work comparison

Status: **VERIFIED — FINAL OUTCOME A**

This is the deliberately narrow comparison used by the manuscript.  It is
not a priority survey.  Source versions were checked again against the
official records through 2026-08-17.  Englander et al. v4 was additionally
checked line by line against the author-supplied 31-page PDF with SHA-256
`3c140c36aae45cd07040b0f1e03b55b40f7c61f14a04b9fbe9cd8c48112e8ba5`.
The exact Englander,
Holtgrefe, and Brits source files, versions, and hashes are locked in
`reviews/final_standard_convention/source_metadata.json`; the other official
version identifiers are recorded below.

| Source | Exact point used | Relation to the proved theorem |
|---|---|---|
| Ardiyansyah, arXiv:2104.12479v1 (2021-04-26) | Four-leaf level-2 JC invariants and distinctions among small labelled/oriented cases | **Related finite local work.**  It does not state the present arbitrary-subdivision, one-sided-containment, or local-to-global theorem.  The manuscript makes no priority claim based on an unsuccessful search. |
| Englander et al., bioRxiv 10.1101/2025.04.18.649493, v4 (2026-07-04) | Definitions 2.1--2.3 lock the already-simple reticulation-preserving semi-directed class and its strong incidence criterion; Theorem 3.2 gives generic JC identifiability for triangle-free strongly tree-child binary level-2 networks; Proposition 2.15 supplies the trinet sign polynomial | **Strict extension, with a resolved small-network crosswalk.**  The present theorem removes the triangle-free hypothesis, quotients exactly by ordinary triangle redirection, and also excludes proper one-sided generic containment.  The trinet polynomial is attributed rather than claimed as new; the new use is within the complete restored level-2 atlas.  Up to reflection, both Omega networks are differently labelled type-(2c) quarnets in their Figure 5. Their Lemma 2.14 has no type-(2c)-versus-type-(2c) claim, Corollary 2.17 does not compare two type-(2c) labellings, and the Omega pair lies outside their strong class by the incidence criterion at `U`.  Thus Omega is consistent with Theorem 3.2 and every applicable finite result. |
| Sullivant, arXiv:2507.23056v2 (2026-07-14) | Graphical-model formulations and local network modifications, including stacked-reticulation and two-port phenomena | **Different scope and complementary method.**  Those phenomena motivated an explicit bridge-kernel and locality audit; none is imported as a theorem input, and no weak or stacked-reticulation example is promoted into `S_TC`. |
| Currie et al., arXiv:2606.26673v1 (2026-06-25) | Semialgebraic distinctions and overlaps for triangle-bearing level-1/three-sunlet models | **Compatible local geometry.**  The ordinary-`T` common-germ statement is the necessary local quotient here; the theorem adds two-reticulation blobs, one-sided containment, and global reconstruction. |
| Brits et al., arXiv:2607.12919v2 (2026-07-29) | Definition 2.1, restricted open parameter conventions, level-1 full-identifiability theorem (Theorem 4.9), and 2-sub-blob suppression (Lemma 5.1) | **Parallel but convention-sensitive.**  Its post-root exhaustive cleanup is broader than the active `sd_0` map.  The theorem is not claimed for every preimage of that cleanup and does not rebrand ordinary root or 2-sub-blob suppression as a new move. |
| Cox, Gross, and Martin, arXiv:2409.17894v1 (2024-09-26) | Algebraic geometry of group-based models on three-sunlet networks | **Local precursor.**  The release independently certifies the strict-JC three-orientation common rank-four germ needed for `T`; it makes no K2P/K3P claim and no novelty claim about the full three-sunlet varieties. |
| Holtgrefe et al., arXiv:2507.18772v2 (2025-11-14), published in *Theory in Biosciences* 145 (2026), article 4 | Semi-deorientation/rootability framework and Theorem 5, the no-omnian characterization of strong tree-childness | **Definition-level foundation.**  On binary LSA-valid networks, the active `sd_0` class is its already-simple specialization. |
| Holtgrefe, Allman, Baños, van Iersel, Moulton, Rhodes, and Wicke, *Bulletin of Mathematical Biology* 87 (2025), article 168 | Reconstruction of outer-labeled-planar, galled level-2 networks from displayed quartets and inter-taxon quartet distances | **Complementary combinatorial result.**  The present theorem concerns full-dimensional containment of open JC model images, does not assume galledness, and recovers the fixed mixed topology modulo ordinary triangle redirection. |

## Exact convention reconciliation

There is no single literal reduction map common to Englander v4, Holtgrefe,
and Brits v2.  The active theorem uses:

1. a binary LSA-valid rooted presentation;
2. undirection of non-reticulation arcs;
3. suppression of the former root; and
4. admission only when the resulting mixed graph is already simple and
   retains every reticulation arrowhead.

This is the Englander v4 convention and the binary LSA-valid specialization
of Holtgrefe et al.  The broader Brits cleanup is used only where explicitly
stated for restrictions, never to enlarge the topology class.  The exact
regressions and source mapping are in
`reviews/final_standard_convention/SOURCE_COMPARISON.md`.

## Novelty statement safe for submission

The independently verified combined statement is:

> In the already-simple standard strongly tree-child binary level-2 class,
> open-JC source-relative full-dimensional containment is possible only
> between topologies with the same labelled bridge tree and corresponding
> blobs equal modulo ordinary triangle redirection.  Strong tree-childness is
> sharp, because the frozen weak-but-not-strong family has non-`T`
> full-dimensional ambiguity for every number of taxa at least four.  This
> sharpness can already occur in triangle-free weakly tree-child networks.

The following are **not** claimed as new or proved here: the existence of
triangle-redirection ambiguity itself, level-1 identifiability, K2P/K3P
classification, physical bridge-length recovery, or a theorem for the
broader exhaustive-cleanup class.
