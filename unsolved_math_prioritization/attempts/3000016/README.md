# CoNP-completeness of binary directed chip-firing reachability

## Accepted result

Legal chip-firing reachability is coNP-complete for finite loopless strongly
connected directed multigraphs with binary adjacency entries and nonnegative
binary-encoded initial and target configurations. The full mathematical
report gives an explicit polynomial-time many-one reduction from NONHALTING
to REACHABLE. Target: problem 3000016 / AMR-029-0016.

The construction uses a gate and marker, a finite-state cutoff, and a large
but polynomial-bit cleanup budget. The reverse proof handles arbitrary
target-reaching firing counts, rather than assuming the designated odometer.
The full report retains the source-loop relay construction, the one-vertex
edge case, optional signed normalization, exact thresholds, both directions,
nonnegativity, strong connectivity, and bit-complexity analysis.

Source NP-completeness is credited to Farrell–Levine,
[CoEulerian graphs](https://arxiv.org/abs/1502.04690), Corollary 3.2.
Target coNP membership is credited to Hujter–Kiss–Tóthmérész,
[On the complexity of the chip-firing reachability problem](https://arxiv.org/abs/1507.03209),
Theorem 12. Tóthmérész's earlier
[polynomial-hierarchy consequence](https://arxiv.org/abs/2102.11970),
Theorem 2.3, remains a distinct prior result.

## Scope and review limits

The result answers the directed hardness question already on its nonnegative
subclass. CoNP-completeness here means the exact nonnegative binary-multigraph
language just stated. There is no simple-graph, unary-encoding, bounded-degree,
bounded-total-chip, or first-in-literature claim.

This is an AI-assisted, unrefereed manuscript with a separate mathematical
audit. Acceptance means that the complete written proof passed that audit;
it does not mean external human peer review, journal acceptance, formal
proof-assistant verification, or certification of bibliographic priority or
preexisting present-day openness. The analytic proof is complete within its
stated scope and does not depend on any omitted program or computation.

## Contents

- [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md): full accepted reduction
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): separate derivation, edge-case
  and arbitrary-odometer review, aggregate supporting checks and acceptance
- [ACCEPTANCE.json](ACCEPTANCE.json): exact public proof/audit identities and verdict
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): primary-source conventions, attribution
  and the distinction from the earlier complexity barrier
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public PDF hashes and sizes,
  locators, and recorded retrieval/inspection history
- [STATUS.json](STATUS.json): exact accepted scope and review limits
- [MANIFEST.json](MANIFEST.json): complete eight-file inventory and hashes of
  the other seven members; the draft PR body independently pins the manifest

Finite checks are aggregate supporting metadata only, not the mathematical
proof. Recorded source inspections and test results are historical evidence;
editorial preparation claims no new source retrieval, source-file rehash,
page inspection, literature search, or mathematical test rerun. Programs,
raw generated outputs, datasets, source PDFs, copied third-party source text,
source-derived images, and private coordination material are excluded.

This edition changes no QUEUE entry or unrelated repository content and adds
no substantive proof-attempt response. Preparation does not constitute a
merge, journal submission, release, DOI, or outside outreach.
