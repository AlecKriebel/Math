# Convex-set independent arborescences: accepted structural partial

Problem 3000044 / AMR-029-0044. This proof-only edition contains an accepted
structural partial; the unrestricted arbitrary-root/arbitrary-overlap
conjecture remains unresolved. No target counterexample or novelty is claimed.

## Exact result

In a finite loopless acyclic directed multigraph with convex prescribed
vertex sets containing their roots, assume that every overlap between
indices with different roots, after parallel arcs are collapsed, has at
most one directed vertex-sequence path between any ordered pair. Same-root
overlaps are unrestricted. Then the original simultaneous terminalwise
independent-path hypothesis, the stated local bipartite-matching condition,
and coherent independent prescribed-set out-arborescences are equivalent.

The self-contained base theorem imposes uniqueness on all pairwise overlaps,
deleting the common root for equal-root pairs, and permits arbitrary local
matching choices. The stronger theorem reconstructs within root groups
using the credited common-root existence theorem of Frank–Fujishige–Kamiyama–Katoh,
Theorem 4. Its use of their Theorem 5 algorithm explicitly removes singleton
sets, checks weak connectivity of the remaining reachable pools, and charges
membership preprocessing separately. Parallel arcs, repeated roots and sets,
zero root paths, singleton sets, arbitrary overlap multiplicity and unbounded
depth are handled within the stated structural class.

The full proof includes the depth-at-most-two corollary, the unbounded shared
chain example and a nine-vertex independent prefix that cannot be extended
greedily even though a valid global family exists. That example refutes an
arbitrary-prefix extension shortcut, not the conjecture. Different-root
overlaps with alternative directed paths remain outside the accepted theorem.

## Files and review meaning

- [PROOF.md](PROOF.md): complete structural proofs, matching criterion, corollaries and obstruction
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): complete analytic review and recorded supplementary evidence
- [ACCEPTANCE.json](ACCEPTANCE.json): exact public proof/audit identities, partial verdict and aggregate check metadata
- [STATUS.json](STATUS.json): result, unresolved case and review limits
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): source dependencies, exact scope and inspection history
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public bibliography, PDF identity and recorded source observations
- [MANIFEST.json](MANIFEST.json): exact inventory and non-manifest SHA-256 hashes

This manuscript and its accompanying independent audit are AI-assisted and
unrefereed. Acceptance does not mean external human peer review, journal
acceptance or formal proof-assistant certification. Bibliographic priority
and current worldwide openness are not certified.

## Editorial and distribution boundary

The complete analytic base theorem, stronger root-group theorem, corollaries,
examples, obstruction and source-dependent algorithm qualifications are
preserved from the corrected accepted proof. Public edits reconcile review
status, replace private provenance with public file identities, remove
references to unavailable programs, and clearly mark historical computational
and source observations. All mathematical arguments and limitations remain.

Finite census, stress and sampled-search counts are supplementary metadata
only. The analytic verdict is independent of any omitted code. Programs,
raw outputs, datasets, copied third-party source text, PDFs, images and private
coordination material are excluded. Edition preparation performed no new
scholarly-source retrieval, source-file rehash, source inspection, literature
search or mathematical computation rerun.

QUEUE.md and unrelated repository content remain unchanged. This target is
distinct from the rainbow-arborescence problem 30004008. No merge, release,
DOI, journal submission or external outreach is implied.
