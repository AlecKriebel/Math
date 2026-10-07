# Cycle-filling complexity: accepted partial results

Problem **30005353 / OWR-12697684-032**, queue rank **950**. Current disposition: **unsolved, 5/5 substantive approaches used**, 7 October 2026. The full unbounded-ratio question remains unresolved. The bounded five-approach investigation is complete; verified completion of the full target is 0%.

## Read the accepted version

Start with [the corrected proof](audit/PROOF.reviewed.md) and [the full independent mathematical audit](audit/ACCEPTANCE.md). The original 27,223-byte [author proof](authored/PROOF.md), all twelve author-manifest inputs, the [correction patch](audit/PROOF_SCOPE_CORRECTION.patch), and all audit-manifest artifacts are preserved byte for byte. The correction inserts exactly **nontrivial** before the auxiliary finite quotient Q; no main result changes.

The frozen author README, source audit, verification notes and manifest retain their historical pending-review and unpublished wording. Those are preparation records. This wrapper records the later accepted-partial disposition. The mathematical audit was performed independently of the original derivation within an AI-assisted investigation; it is not human peer review or formal proof-assistant certification.

## Accepted scope

For finite connected simple unweighted graphs with positive cycle rank, a₂ denotes minimum total mod-2 homology-killing cycle length, and aπ denotes minimum total fundamental-group-killing cycle length.

1. Explicit odd Moore-complex graphs have a₂=162p and aπ=162p+3 for odd p≥3; p=3 gives **486 versus 489**. Their ratios tend to one.
2. Articulation/bridge sums and uniform subdivisions cannot amplify bounded ratios. Fixed-building-block sums give additive gaps, which do not settle the ratio question.
3. The supremum of aπ/a₂ is unchanged on restricting to maximum degree three. This equivalence transfers a ratio; it does not construct an unbounded family.
4. A field-homology/systole criterion gives sufficient conditions for unbounded ratios. The required family is missing. The auxiliary finite-quotient statement uses a **nontrivial** quotient.
5. A credited Rizzi/Kavitha–Rizzi deletion argument yields a logarithmic upper bound, with explicit cycle-rank bookkeeping. Planar equality follows using the survey's planar minimum-basis theorem. Neither conclusion decides the general question.

The primary report's printed-p.84 RP²/F₂ additive example has a verified **coefficient-specific inconsistency** under the stated interpretation. The qualification concerns that example; it neither refutes nor solves the main ratio question. For simplicial RP² triangulations the packet proves a₂=aπ; odd-characteristic homology behaves differently.

Credit: [Kavitha et al., *Cycle Bases in Graphs: Characterization, Algorithms, Complexity, and Applications*](https://doi.org/10.1016/j.cosrev.2009.08.001), inspected author-version Theorems 4.4 and 5.34. The deletion proof is credited there to Rizzi and Kavitha–Rizzi. The target is [Karim Adiprasito's Question 12, *Combinatorics*, Oberwolfach Reports 2023/1](https://doi.org/10.4171/OWR/2023/1). See [source audit](authored/SOURCE_AUDIT.md) for the bounded search record and [public source metadata](authored/SOURCE_METADATA.json) for public URLs and document hashes. No novelty or exhaustive current-openness certification is asserted.

## Source-free verification

From this directory run:

    python3 verify_publication.py

Only the Python standard library is needed. No network, scholarly documents or corpus files are used. The verifier checks exact inventory and file hashes, the author and audit manifests, the literal one-word correction, and application of the preserved patch. It runs all five author/auditor programs in an isolated temporary copy and checks their generated JSON byte for byte against the frozen outputs. It always launches assertion-based controls in ordinary Python mode, even if the wrapper is called with `python3 -O`.

The independent finite controls certify the two p=2,3 examples with exact binary optima, short-cycle obstructions and explicit group-presentation certificates; other finite cases are supplemental controls. Finite checks do not prove universal statements, provide a general group-triviality algorithm, establish novelty, or supply the missing family.

[PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) pins the entire public packet except itself. Copied source PDFs, extracted text, page images, corpus records and coordination material are excluded. The only repository file changed outside this packet is the existing queue, with only this problem's Status, Turns and Findings cells changed; all other bytes are preserved.
