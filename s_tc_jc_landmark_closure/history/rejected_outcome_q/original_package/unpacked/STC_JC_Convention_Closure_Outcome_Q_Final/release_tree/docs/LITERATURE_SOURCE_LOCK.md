# Literature source and terminology lock

This note fixes the versions used by the convention theorem.

## Englander et al.

*Identifiability of Phylogenetic Level-2 Networks under the Jukes--Cantor Model*, bioRxiv 2025.04.18.649493, version 4 (2026).  Its directed input excludes parallel edges, 2-blobs, and non-leaf 1-blobs.  Its semi-directed network is obtained by removing non-reticulation directions, suppressing degree-two vertices, and identifying parallel edges.  Its restriction operation additionally suppresses 2-blobs.  The full-network operation, restriction, and displayed-network operation are distinct.

## Brits et al.

*On Tree--Network Distinguishability and Full Identifiability of Phylogenetic Networks*, arXiv:2607.12919v2, 29 July 2026.  Definition 2.1 uses a binary rooted DAG with no parallel edges and requires the root to be the only vertex lying on all root-to-leaf paths.  The full semi-directed topology undirects non-reticulation edges, suppresses the root, and exhaustively suppresses resulting parallel edges and degree-two vertices.  Definition 2.2 separately defines restriction; Definition 2.3 separately defines displayed networks.  Higher-level 2-blobs are not silently removed from restrictions.

## Holtgrefe et al.

*Characterizing Semi-Directed Phylogenetic Networks and Their Multi-Rootable Variants*, Theory in Biosciences 145 (2026), article 4.  Mixed graphs exclude parallel edges/arcs.  Semi-deorientation undirects arcs whose heads have indegree one and suppresses degree-two roots; outputs with parallel arcs are not admitted as mixed graphs.  In the one-root binary LSA-valid specialization this is the already-simple convention.  Strong tree-childness quantifies over all rootings and is characterized by absence of omnians.

## Sullivant

*Phylogenetic Network Models as Graphical Models*, arXiv:2507.23056v2 / 2026 journal version.  Degree-two and hidden 2-blob transformations are statistical results under closure and splittability hypotheses.  This release invokes the degree-two product map and proves the special root-created zipper directly.  It does not use arbitrary 2-sub-blob suppression as a definition.

## Terminology used in the revised manuscript

“Literature-standard” means the Englander/Brits root-suppression-plus-cleanup topology together with their complete rooting quantifier.  The notation `sd0` is retained for the already-simple presentation convention of the frozen baseline theorem.  Theorem Q, rather than an assertion of literal identity of rooting sets, transfers the statistical classification between them.
