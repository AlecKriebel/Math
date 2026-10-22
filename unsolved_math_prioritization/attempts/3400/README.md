# Stable ternary compaction: accepted proved partial

Problem 3400 / OPG-474. This proof-only edition does not resolve whether
linear-size general circuits exist. The unconditional bounds remain Omega(n)
and O(n log n). Theta(n log n) holds only under the undirected k-pairs
conjecture in the precise form used by AFKL.

## Exact result

The complete proof gives an explicit Boolean rank-parity construction of
O(n log n) size and O(log^2 n) depth, including per-pair gates, prefix parity,
fixed wiring and power-of-two padding. It also supplies the linear-overhead
all-terminal fan-out conversion, counting and threshold gadgets, bit-shift
restrictions, and balanced-promise equivalence with its necessary output mask.

A three-wire counterexample disproves the actual stability assertion in
Regan's Theorem 1 for 0,1<2. The comparator Omega(n log n) bound survives by
the ordinary total-order 0–1 principle and comparison-outcome counting; it
is not a general Boolean-circuit lower bound. The prior conditional barrier
is explicitly credited to Asharov–Lin–Shi and AFKL. No novelty is claimed.

## Files and review meaning

- [PROOF.md](PROOF.md): full construction, accounting, reductions and source correction
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): full analytic review and recorded supplementary checks
- [ACCEPTANCE.json](ACCEPTANCE.json): public proof/audit identities, exact partial verdict and aggregate metadata
- [STATUS.json](STATUS.json): freshly authored accepted status, conditional premise and unresolved gap
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): precise source dependencies and claim boundaries
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public bibliography, byte identities and recorded inspection history
- [MANIFEST.json](MANIFEST.json): exact eight-file inventory and hashes of the other seven members

This manuscript and accompanying independent audit are AI-assisted and
unrefereed. Acceptance does not mean external human peer review, journal
acceptance or formal proof-assistant certification. Bibliographic priority
and current worldwide openness are not certified.

## Editorial and distribution boundary

All mathematical statements, analytic arguments, examples and qualifications
are preserved. Public edits reconcile completed review status, explicitly
credit the pre-existing conditional barrier, replace private provenance with
public file identities, and distinguish recorded checks from distributed
proofs. The fresh status and manifest describe exactly this edition.

Finite checks are supplementary metadata; no analytic claim requires an
omitted program or raw output. Programs, raw outputs, datasets, copied
third-party source bodies, PDFs, images and private coordination material
are excluded. Edition preparation rechecked frozen byte identities and
publication integrity, but performed no new scholarly retrieval,
source-text inspection, literature search or mathematical computation rerun.

QUEUE.md and unrelated repository content remain unchanged. No merge,
release, DOI, journal submission or external outreach is implied.
