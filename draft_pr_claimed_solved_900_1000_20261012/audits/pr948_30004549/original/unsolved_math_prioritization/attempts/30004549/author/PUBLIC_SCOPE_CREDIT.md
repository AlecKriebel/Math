# Scope, credit, and verification status

Problem: 30004549 / OWR-2654829-012, *Generic Vanishing of Anti-Invariant Cohomology in Dimension Four*.

## Mathematical scope

This packet preserves the exact authored construction of a nonintegrable smooth almost-complex structure on a closed connected four-manifold with at least three independent closed anti-invariant real two-forms. The manifold is a genus-two hyperelliptic curve times an elliptic curve. The proposed construction preserves three independent de Rham classes by compactly supported exact changes and supplies a direct nonzero Nijenhuis tensor calculation.

It addresses only the integrability implication. The other clause, generic vanishing, is prior work of Qiang Tan, Hongyu Wang, Ying Zhang, and Peng Zhu, *On cohomology of almost complex 4-manifolds*, arXiv:1112.0768v3, DOI 10.1007/s12220-014-9477-2. No new proof of generic vanishing is claimed.

The integrability target is Conjecture 2.5 in Draghici-Li-Zhang, arXiv:1104.2511, and OWR 33/2020, printed page 1687. The withdrawn Lejmi-Upmeier arXiv:1507.00282 is not used in the construction.

## Exact proof identity and current count

The proof file is unchanged from its author freeze: 9,997 bytes, SHA-256 50a267656e6a5412a2e14208ada5aec203df4c5385be63b831029188cb1cf39e. Its author-only review label is retained as a historical label. Independent review reports and their exact scope are supplied separately; read the final review status from those reports.

The current author-turn count is 4/5: one earlier substantive turn and three resumed turns, of which this construction is the third. This corrects the frozen proof's statement that the inherited count was unknown when it was written. The two preceding resumed partial notes are not part of this proof packet and are not needed for the construction.

One notation clarification: in the formula T=C/(Z+iZ), C denotes the complex plane ℂ, and Z denotes the integers ℤ. The genus-two curve elsewhere named C is a different object. No proof bytes were changed to make this clarification.

## Checks and limitations

The included SymPy checker verifies local exterior-algebra identities for a general cutoff, normalization, and two nonintegrability calculations. It also rejects an intentional sign error. It passed under ordinary Python and python -O with SymPy 1.14.0. It does not certify global geometry, smooth patching, independence of cohomology classes, literature status, or novelty.

This is AI-authored, unrefereed mathematical work. Independent AI review is not human peer review, formal verification, a journal acceptance, or a novelty certificate. Targeted source checks are not an exhaustive literature search.

Only authored mathematics, local verification code/results, and public verification metadata are included. Corpus contents, copied scholarly PDFs or extracted source text, historical missing archives, private recovery records, and unrelated partial notes are omitted. Newly computed source hashes identify the accessible bytes inspected for this packet; they do not stand in for any missing earlier artifact.

Primary public sources:
- https://arxiv.org/abs/1104.2511
- https://publications.mfo.de/bitstream/handle/mfo/3805/OWR_2020_33.pdf?isAllowed=y&sequence=4
- https://arxiv.org/abs/1112.0768
- https://arxiv.org/abs/1507.00282
