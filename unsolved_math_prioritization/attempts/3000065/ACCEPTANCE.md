# Acceptance of the regular-core proportional-factor theorem

## Decision and exact guarantee

Accept the restricted theorem without mathematical correction. For any finite loopless bipartite multigraph whose connected components each have empty or regular nonempty 2-core, every positive real fraction vector of sum one admits one partition of the same edge set into all colors. Every color count at every vertex lies simultaneously between the floor and ceiling of its fraction times the original vertex degree. Regular core degrees may vary between components; arbitrary attached finite trees and parallel edges are allowed.

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

Forests, bipartite pseudoforests, isolated vertices, the null graph, and the one-color case are included. An irregular surviving 2-core is outside the sufficient hypothesis. Joining regular blocks can create such an irregular core, so the theorem does not cover arbitrary block assemblages.

## Proof and audit basis

The finite quota-word lemma starts with a feasible real circulation but uses integer lower and upper capacities. Its lower-bound reduction and integral augmenting-flow proof are included in full. Monotone prefix counts then connect the common regular-core counts to the original, possibly unequal vertex degrees. The complete multiplicity-aware 2-core argument and the alternating-path proof of perfect matching decomposition are retained. One-precolored-edge completion propagates outward through attached trees. The forest argument also extends a prescribed color on one chosen edge; it does not extend arbitrary multiple-edge precolorings.

The separate rational-cell lemma retains every integer threshold equality and all strict threshold inequalities. It is proved for every fixed graph and color count, including zero degrees and zero or one unfixed coordinate. It gives no bounded-denominator testing guarantee. The main theorem already treats real fractions directly and does not rely on this reduction or on computation.

The complete general mathematical proofs are retained, including the integer-circulation argument, multiplicity-aware core structure, alternating-path proof of the matching decomposition, tree propagation, and boundary-preserving rational-cell lemma. This is not a computational reproduction package. Explicit finite witness lists, edge and coordinate packages, indexed constraint rows, matrix certificates, raw certificates, and executable code are omitted. The two finite obstructions retain their authored logical arguments conditional on explicitly stated, historically checked finite premises; this edition does not independently reconstruct those omitted premises. Neither obstruction is used to prove the regular-core theorem.

The ten-vertex obstruction defeats arbitrary valid first-factor extraction, even when the remaining colors may be assigned by any method. The authored local forcing contradiction and full real parameter region remain, with the omitted graph/factor inputs identified as historical finite premises. The six-cycle obstruction defeats total unimodularity and automatic integral-vertex rounding for the natural simultaneous LP. Its authored odd-cycle determinant and full-rank vertex arguments remain conditional on the omitted, historically verified coordinate-to-row realization. Both graphs admit valid complete partitions; neither obstruction refutes the target.

## Historical verification and provenance

The independent audit used exact arithmetic, dynamic programming for quota words, and separate finite matching construction. Candidate programs were not used as implementation source, imported, or executed. It checked 15,674 in-scope labeled K3,3 partitions, 4,323 labeled-tree partitions, six retained partitions, both obstruction certificates, and additional multiplicity, irrational, boundary, and negative controls under normal Python, -O, and -OO. These are historical results. Edition preparation performs no new mathematical runs or scholarly-source retrieval.

The candidate's unretained full generated stream hash is authenticated author-reported metadata only. The independent audit constructed and checked its own valid partitions; it did not recreate the candidate stream and does not claim byte-identical reproduction.

ACCEPTANCE.json binds the accepted original identities and public proof, audit, and acceptance files separately. SOURCES.json records public source titles, URLs, retained identities, and the precise historical inspection boundaries. The publication makes no mathematical correction and distributes no copied source documents, raw witness packages, matrix certificates, code, or private coordination material.

## Remaining question

The unrestricted same-partition proportional-factor target remains unresolved by this work. No novelty, priority, exhaustive later-literature survey, or certification of current global problem status is claimed.
