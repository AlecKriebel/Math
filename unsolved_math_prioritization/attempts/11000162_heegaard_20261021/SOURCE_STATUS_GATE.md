# Heegaard-distance thresholds: source and status gate

Identity: ordered row 1892, ID 11000162, AMR-109-0162. Gate date: 2026-10-21 UTC. Disposition: eligible for a new bounded attempt; no complete published solution verified in this search. This is not a proof of worldwide openness or a mathematical resolution.

## Correct target

Joan S. Birman, *The topology of 3-manifolds, Heegaard distance and the mapping class group of a 2-manifold*, in Benson Farb's edited volume. The editor-hosted compilation puts Problem 2.5 on its printed page 149, PDF page 156 (one-based). These page labels refer to that compilation, not necessarily the final publisher pagination. The chapter preprint is arXiv:math/0502545 (2005); the published volume is 2006. The author is Birman, not Farb.

Given a closed orientable Heegaard splitting and its gluing mapping class, let d be the minimum curve-graph distance between the two full disk sets. The two promised-input questions ask for algorithms distinguishing distance 1 from distance at least 2, and distance 2 from distance at least 3. The first promise is d >= 1; the second is d >= 2. Genus at least two is the ordinary curve-graph setting; exceptional low genus needs separate conventions. One must not substitute distance between the finitely many curves of the input cut systems for distance between the full disk sets.

Primary sources:
- https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf
- https://arxiv.org/abs/math/0502545

## Literature gate

1. Howard Masur and Saul Schleimer, *The geometry of the disk complex*, JAMS 26 (2013), 1–62, electronically published 2012. Theorem 21.1 supplies an algorithm with an additive error bounded in terms of genus. Inspected introduction and Section 21, especially Theorems 21.1–21.2 and Algorithm 21.3. This is not an exact low-threshold decision procedure. Fixed-vertex curve-graph algorithms also do not directly minimize over the infinite disk sets.
   https://sschleimer.warwick.ac.uk/Maths/2012geom_disk_complex.pdf

2. Yuya Koda and Kazuto Takao, *Diagrammatic criteria for strong irreducibility of Heegaard splittings and finiteness of Goeritz groups*, arXiv:2402.06849v2, 21 April 2024. The criteria certify strong irreducibility when satisfied; no necessity or complete recognition algorithm is supplied by the inspected statements. Introduction, definitions and Theorem 1 proof entry inspected. Latest arXiv listing observed v2; no journal-status inference made.
   https://arxiv.org/abs/2402.06849

3. Bo-hyun Kwon, Sungmo Kang and Jung Hoon Lee, *The rectangle condition does not detect the strong irreducibility*, arXiv:2509.11701v1, 15 September 2025. Theorem 1.7 claims a genus-two strongly irreducible splitting that admits no rectangle-condition certificate, not merely one bad choice of disk systems. Introduction/Theorems 1.4–1.7 inspected, not a full independent proof audit. Treat as an observed preprint claim. This obstructs a proposed completeness argument based only on enumerating rectangle certificates. It is not a counterexample to decidability.
   https://arxiv.org/abs/2509.11701

4. Ennes–Maria, *Hardness of computation of quantum invariants on 3-manifolds with restricted topology*, ESA 2025 and arXiv:2503.02814v2: constructs high-distance outputs for a quantum-invariant reduction; the abstract/introduction inspected do not furnish exact recognition of arbitrary input splitting distance.
   https://arxiv.org/abs/2503.02814
   https://doi.org/10.4230/LIPIcs.ESA.2025.37

## Duplicate and prior-work gate

Full retained problem corpus and research report checked by exact ID. The prior report merely marked the statement truncated and left literature review undone. No substantive prior solution is present there. Related entries 11000160 (full distance computation), 11000161 (zero versus positive distance under a low-distance promise), 11000163 (a fixed-manifold upper bound), and 10900058 (reducibility recognition) are distinct targets, not substitutes for this two-part question.

All-state AlecKriebel/Math pull-request searches on 2026-10-21 for 11000162 and AMR-109-0162 returned no matches. A Heegaard search returned PRs 566, 860, 839 and 606, all different targets. A Hempel search returned PR 765, an unrelated spectral-theory paper. This is bounded indexed-search evidence, not an exhaustive branch-content audit. No publication or queue edits performed.

## Author handoff restrictions

Preserve both promises and both thresholds. Enumeration of disk witnesses gives only one-sided detection of small distance unless a terminating complementary method is proved. Coarse error bounds cannot be silently rounded to exact thresholds. Sufficient diagram criteria need a completeness theorem before being used as the other half of a decision algorithm. Hyperbolicity recognition of the underlying manifold is not equivalent to distance >= 3 of its specified splitting.

No mathematical attempt turns are consumed by this source/status gate. All copied source documents, source extracts and corpus records remain private. Only this authored discussion and public hash/size/provenance metadata are candidates for later publication under separate workflow review.
