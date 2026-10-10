# Directed linear k-cut: accepted lower-bound partial

Problem 30003993 / OWR-16633-010. The original constant-versus-unbounded
integrality-gap question remains OPEN.

For every k>=2 the construction gives a finite simple unit-edge-cost directed
graph with k distinct ordered terminals. Put

C_k = sum_{l=1}^k (k-l+1) floor(k/l).

Its exact integral optimum is C_k-k^2, and a feasible vector for the original
edge path-distance LP has objective C_k/3. Consequently the gap lower bounds
3(1-k^2/C_k) tend to 3 and the actual gaps have liminf at least 3. This does
not prove convergence of the actual gaps to 3, an exact LP optimum, an
unbounded gap or a universal constant upper bound.

## Files

- [PROOF.md](PROOF.md): full accepted universal construction and proof
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): complete mathematical audit, including arbitrary-cut and terminal-visit arguments and historical supplementary checks
- [ACCEPTANCE.json](ACCEPTANCE.json): precise accepted scope and distributed proof/audit identities
- [STATUS.json](STATUS.json): partial acceptance and the original open question
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): attribution, source roles and inspection limits
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public source titles/URLs, recorded PDF hashes/sizes and historical inspection metadata
- [MANIFEST.json](MANIFEST.json): exact eight-file inventory, hashing the seven other members

## Attribution and review limits

The originating question is Chekuri's Oberwolfach contribution. Bérczi,
Chandrasekaran, Király and Madan report general-k bounds ceil(log2 k) above
and 2(1-1/k) below; their tight sqrt(2) result is for three terminals.
Aprile, Drescher, Fiorini and Huynh's earlier gap-3 result for the general
induced-P3 covering LP is related context and is credited. The construction
here is self-contained. No novelty or priority is claimed.

This AI-assisted manuscript and audit are unrefereed. Acceptance refers to
the accompanying independent mathematical audit; it is not external human
peer review, journal acceptance or formal proof-assistant certification.

The complete proof and substantive audit findings are retained. Edition edits
are editorial. An earlier packaging-checker correction was authored by the
independent audit, not by the original proof author; it changed no mathematical
proof, source record or mathematical certificate. That correction is accurately
recorded without distributing the internal checker diff.

No mathematical claim requires an omitted program or output. Original exact
computations are historical supplementary checks. This proof-only edition
excludes programs, raw outputs, generated certificates, datasets, copied
third-party source documents/text/images and private coordination material.
Edition preparation rechecked frozen accepted file identities and publication
integrity, without rerunning original mathematical programs or performing new
scholarly retrieval, source-PDF rehashing, source-text inspection or literature
search. QUEUE.md and unrelated repository content remain unchanged. No merge,
release, DOI, journal submission or external outreach is implied.
