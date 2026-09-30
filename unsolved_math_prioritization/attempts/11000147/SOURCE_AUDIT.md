# Source and current-literature audit

Audit date: 2026-09-30 UTC. This document records the scope checked, rather than a claim of an exhaustive bibliography or historical priority.

## Exact source

B. Wajnryb, *Relations in the mapping class group*, Chapter 8 of Benson Farb (ed.), *Problems on Mapping Class Groups and Related Topics* (2006). The source selected by the dataset is the [full author-hosted book manuscript](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

The complete chapter was read in that copy. The introduction and question were also visually checked: printed pages 122 and 124 correspond to PDF pages 129 and 131. The chapter's published pagination is different: later primary references cite pages 115–120, so page 124 here refers specifically to the linked manuscript.

The source permits compact surfaces, with or without boundary, and uses orientation-preserving mapping classes in the oriented case. Its explicit torus example immediately after the question confirms that torus Anosov maps are relevant. The candidate uses the closed torus, so there is no puncture-versus-boundary ambiguity and no boundary-fixing lift problem.

The question asks for a set, hence three distinct elements are necessary. The preceding question emphasizes noncommuting maps and alternating Artin relations of length greater than two. The candidate satisfies those stricter pairwise conditions too. It makes no assumption that distinct means nonconjugate: length-three braid-related elements are necessarily conjugate. Nor does the source require the set to be a minimal generating set.

The preceding discussion separately asks about embeddings and homomorphisms of Artin groups. The specific three-map question does not impose faithfulness. Our construction supplies a nonabelian image but does not solve those embedding questions.

The referee's pair construction is explicitly credited in the source. The matrices used in the candidate are an exact instance: with
\[
X=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
Y=\begin{pmatrix}-2&-1\\3&1\end{pmatrix},
\]
one has \(X^2=-I\), \(Y^3=I\), \(A=XY\), and \(B=YX\). Thus the proof does not claim a new mechanism for obtaining a pair.

## Literature and novelty limits

A bounded primary-source search on the audit date used the question's exact wording and combinations of Wajnryb, pseudo-Anosov, braid relations, pairwise, and triangular Artin groups.

- [Jamil Mortada, *Artin Relations in the Mapping Class Group*, arXiv:1008.0124v3](https://arxiv.org/abs/1008.0124v3), revised 23 September 2011. The complete PDF was available; its introduction and Theorems 1.1–1.4 were inspected. It explicitly addresses the preceding two-element question and constructs Artin relations of arbitrary length using products of twists. Those theorem statements do not assert the three pseudo-Anosov conclusion audited here. This is a scope distinction, not a certification that no related result appears anywhere in the literature.
- [B. Szepietowski, *Embedding the braid group in mapping class groups*, Publ. Mat. 54 (2010), 359–368](https://ddd.uab.cat/pub/pubmat/02141493v54n2/02141493v54n2p359.pdf) provides related nongeometric-embedding context and verifies the published Wajnryb citation. It is not used as an ingredient of the proof.
- Searches also returned work on nongeometric braid-group embeddings and Artin triangle groups. No retrieved source was identified as a later explicit answer to this precise three-map question. Search absence is not proof of novelty.

The new write-up is an elementary deduction from the already discussed pair mechanism, with a fully explicit realization. It must retain “historical priority unconfirmed” and must not be described as a newly discovered deep mapping-class-group theorem.

## Prior-attempt and duplicate gate

Before research, the current remote main was fetched at commit c6975ca76f9f667f1250ba403d0e6da2aafe14d0. Its QUEUE row 146 listed ID 11000147 as queued with 0/5 turns. The exact ID/code were absent from state, attempt history, assessment history, related-target groups, and all fetched attempt-path history. Searches for the ID in all GitHub PR states and remote branch names found no prior publication.

The full pinned dataset contained only this ID among statements containing both “pseudo-Anosov” and “braid relation”; its problem code was not ambiguously joined. The prior upstream research report only repeated the question and recorded that the statement was read. It supplied no mathematical attempt or resolution. Repository desk-review metadata proposed studying triangle Artin representations, with an explicit unresolved-target gap.

The dataset landing page was attempted first but was unavailable through the web tool. The immutable local dataset and its specified complete primary source were used instead.

## Source access and reuse

The primary book PDF was reused from an existing source cache and not added to the public attempt folder. Its SHA-256 is f37c6a1dbc875105c2b294196de1a03a88595b75e8705e6077e9d48f066e402a. Screenshots used for scope verification stay outside the publication folder.

Dataset attribution: *UnsolvedMath: A Curated Collection of Open Mathematics Problems*, UnsolvedMath Contributors (2026), [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), revision 37e53eabe540fb458758e198be61634bd02ee008; curation and metadata [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Underlying mathematical sources retain their own rights.
