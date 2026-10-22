## Accepted restricted result

This authored prose edition proves simultaneous proportional edge
factorization for every finite loopless bipartite multigraph whose connected
components each have empty or regular nonempty 2-core. For arbitrary
positive real fractions summing to one, the same partition satisfies every
color's floor/ceiling quota at every original vertex degree. Core degrees
may vary between components, and arbitrary finite trees may be attached.
Parallel edges, forests, bipartite pseudoforests, isolated vertices, the null
graph, and one color are covered. Irregular surviving 2-cores are outside
the sufficient hypothesis. No mathematical correction was required.

## Complete general proofs

The finite quota-word lemma includes its lower-bound circulation reduction
and integral augmenting-flow proof; it uses the original real fractions.
The complete multiplicity-aware core-structure argument and alternating-path
proof of the perfect-matching decomposition are retained. Monotone prefix
counts extend core colors to attachment edges, and one-precolored-edge
completion propagates through trees. Quotas use original degrees throughout.

The fixed-instance rational-cell lemma preserves both integer threshold
equalities and strict inequalities, including zero-degree and zero/one
unfixed-coordinate cases. It gives no bounded-denominator testing guarantee.
The main theorem treats arbitrary real fractions directly and uses no
finite computation as a premise.

## Authored obstructions and omitted finite premises

A historically checked ten-vertex tree shows that an arbitrary valid first
proportional factor need not extend, even with unrestricted choice of the
remaining colors. The authored local forcing contradiction and its real
parameter region are retained. A historically checked six-cycle point
shows a fractional vertex and non-total-unimodularity of the natural
joint-color LP. The authored odd-cycle determinant and tight-rank arguments
are retained. Both underlying graphs have full valid partitions; neither
obstruction refutes the target.

Explicit graph/factor and coordinate witness packages, indexed rows and
columns, raw matrix certificates, executable code, and raw certificates are
omitted. Realization of each obstruction's stated finite premises is a
historical checked fact, not a self-contained reconstruction in this prose
edition. The general theorem and rational-cell lemma are complete and do
not depend on either obstruction. This is not a computational reproduction
package.

## Historical checks and stream-hash qualification

The independent historical audit checked 15,674 in-scope K3,3 partitions,
4,323 labeled-tree partitions, six retained concrete partitions, both
obstructions, and multiplicity, exact irrational, rational-cell boundary,
endpoint, and negative controls. Normal, -O, and -OO receipts agree.
Candidate programs were not used as implementation source, imported, or
executed by the independent audit.

The candidate's unretained full generated stream hash is authenticated
author-reported metadata only. The audit constructed its own valid
partitions; it did not recreate that stream and claims no byte-identical
reproduction. Edition preparation performed editorial and byte-integrity
checks only, with no new mathematical run or scholarly-source inspection.

## Sources and status

J. R. Correa and M. X. Goemans,
[*Improved bounds on nonblocking 3-stage Clos networks*](https://doi.org/10.1137/060656413),
SIAM Journal on Computing 37(3), 870–894 (2007), Section 2, supplies
two-factor and relaxed-decomposition context. Public author PDF:
https://www.dii.uchile.cl/~jcorrea/papers/Journals/CG2007.pdf .

U. Feige and M. Singh,
[*Edge Coloring and Decompositions of Weighted Graphs*](https://doi.org/10.1007/978-3-540-87744-8_34),
June 25, 2008 preprint corresponding to ESA 2008, Conjecture 1.4,
Theorem 1.5, and Sections 1.1–1.2 and 3, records the target and contextual
bounds. Public research-site PDF:
https://www.microsoft.com/en-us/research/wp-content/uploads/2008/09/edgecoloring.pdf .

The retained Egres Open revision 2419,
[*Partitioning a bipartite graph into proportional factors*](https://oldlemon.cs.elte.hu/egres/open/Partitioning_a_bipartite_graph_into_proportional_factors),
is the target formulation, not a current-status certification. The audit's
live opening of that page failed; both public PDFs opened successfully,
without a live PDF byte-identity claim. SOURCES.json distinguishes the
retained hashes and historical passage inspection from those live openings.

The unrestricted same-partition target remains unresolved by this work.
No novelty, priority, exhaustive later-literature survey, or current global
problem-status certification is claimed. This AI-assisted manuscript is
unrefereed. Acceptance means an independent internal AI audit, not external
human peer review, journal acceptance, or formal proof-assistant certification.

Exactly eight authored proof/audit/acceptance/provenance/verification files
are added under unsolved_math_prioritization/attempts/3000065. QUEUE.md and
unrelated paths are unchanged. Copied source bodies, dataset contents,
private sources, private personal data, and private coordination are excluded.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,709 bytes; SHA-256 `dedcd1197dde074f43c77026fe373b5f9dbae662ca2412bc0cb8ec2af284df7b`.
- `ACCEPTANCE.md`: 5,095 bytes; SHA-256 `692f73af2d1d6089fc3adf390113869647a6979ed2d21253a72b0363c65d2d39`.
- `AUDIT.md`: 17,918 bytes; SHA-256 `28091b6c5bcd4f1748f36193121dd02ed0ba53e95f422c67c169024c8f2fb176`.
- `MANIFEST.json`: 1,351 bytes; SHA-256 `726480d3560d7e4ab9fa8681d7861210bd341a9286e59fa4cf9adf646cee083f`.
- `PROOF.md`: 21,766 bytes; SHA-256 `6451725be9d994f74accaacfc7eceb9bb2442fd4e1b1f6b733665656cdca72ac`.
- `README.md`: 2,648 bytes; SHA-256 `685711ec5d65e7cadf93d74f7d120b564cf844b1be4d3015ee9e58a766ee879e`.
- `SOURCES.json`: 3,554 bytes; SHA-256 `dadec1f757c36af3dee42cbeb914f6dde1b1e90ce628770f62bdd7e946a5da90`.
- `VERIFICATION.json`: 5,227 bytes; SHA-256 `af246e4c3cf89593254a308d413890ffa64e5385dbe361f73dfe42f8bc59f0a1`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.

