# Exact transversals: audited partial results, full record unresolved

Record 30001895 / OWR-11136-027, original rank 433. Date: 2026-10-03 UTC.
**Status: unsolved, 5/5 substantive author attempts used.** The full original
record has not been solved. No further proof-search turn is included here.

The record asks two distinct questions. The hyperplane assertion is false
by credited prior work of Keller and Smorodinsky on actual planar affine
lines. The separately requested assertion for r-element sets remains
unresolved in general. The r=2 case is credited to the existing graph
theorem of Alfaro, Rubio-Montiel and Vázquez-Ávila, together with the stated
reductions. No novelty claim or certification of present worldwide
openness is made. See [source status](SOURCE_STATUS.md).

For every stated (p,q) application, members are distinct nonempty sets,
the family has at least p members, and some q of every p members share a
common point. The proposed transversal has **at most** p−q+1 points.
The r-element component requires r+1≤q≤p. Exactly-r and rank-at-most-r
families are related by the proved private-padding reduction; finite
positive results extend to arbitrary nonvacuous families by the proved
finite-obstruction argument. Neither convention is silently omitted.

## Audited partial mathematics

- The full finite r-set question is equivalent to
  ν_r(H) ≥ min(|H|, τ(H)+r−1), where ν_r is the maximum size of a distinct
  edge subfamily of maximum degree at most r. The reduction does not prove
  that inequality. [Turn 1](TURN1.md).
- Every maximal r-packing yields τ≤ν_r. A minimal counterexample to the
  stronger target is connected, τ-critical and packing-stable under edge
  deletion, with τ=ν_r−r+2. An explicit Fano extension blocks the proposed
  stronger saturation certificate. [Turn 2](TURN2.md).
- For rank at most three, τ(H)≥3 implies ν₃(H)≥min(|H|,5). The finite
  proof uses a fully stated incidence encoding and 15 independently
  replayed exhaustive trees. Consequently the original bound holds for
  r=3, p=q+1, q≥4; p=q holds in every rank. [Turn 3](TURN3.md).
- Credited set-pair equality cases give strict critical edge/degree
  bounds for a minimal counterexample. At rank three and τ=4, complete
  link and trace certificates exclude maximum degrees nine and eight,
  in addition to the extremal degree-ten case. Exact counting leaves
  twenty parameter pairs; nine complete trees exclude nine of them.
  [Turn 4](TURN4.md), [Turn 5](TURN5.md).

The exact eleven remaining (edge count, maximum degree) pairs at rank
three and τ=4 are (11,5); (11,6), (12,6), (13,6), (14,6); and (12,7),
(13,7), (14,7), (15,7), (16,7), (17,7). Larger transversal numbers at rank
three and general ranks at least four also remain unresolved. A timeout,
node limit, or failure to find a counterexample is not an impossibility proof.

## Review and reproduction

The [independent audit](review/INDEPENDENT_AUDIT_REPORT.md) passes the
stated partial claims and holds any full-resolution designation. Its
[separate reductions review](review/REVIEW_T1_T2_T4_SECTION1.md), fresh
checker, independent finite controls and mutation controls are included.
These are AI-assisted mathematical and computational reviews, not human
peer review or formal proof-assistant certification.

Run from this directory with Python 3.10+ and assertions enabled:

```sh
python3 verify_public_package.py
python3 review/independent_certificate_audit.py
python3 review/adversarial_controls.py
python3 review/reviewer_reduction_controls.py
python3 verify_tau3_certificate.py
python3 verify_link_certificate.py
python3 verify_degree8_certificate.py
python3 verify_tau4_certificate.py
```

The independent checker fixes the exact 15-case and nine-case domains.
Do not use `python -O` with the author checkers or reviewer reduction
controls. To regenerate the already completed certificates with a C++17
compiler, use `python3 reproduce_turn3.py` and `python3 reproduce_turn5.py`.
These reproduction scripts do not resume any unfinished search.

## Package identity and historical records

All 53 author payload files and their [final manifest](FINAL_AUDIT_MANIFEST.json)
are byte-identical to the reviewed five-turn checkpoint. In particular,
[FINAL_REPORT.md](FINAL_REPORT.md) and the earlier turn notes preserve their
historical pending-review wording. This README and the completed audit
give the current partial-result disposition. The five-turn ledger remains
`exhausted_unfinished`; the queue's display status is `unsolved`, 5/5.

[PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) binds the portable public
package. [PROJECTION_CHANGES.json](PROJECTION_CHANGES.json) records each
review projection's original and published hashes. The original review
manifest is retained as [provenance](review/AUDIT_SOURCE_MANIFEST.json);
its hashes describe the original review files, not path-adjusted copies.
Only machine-specific paths and administrative wording were adjusted;
the frozen author mathematics and all certificate bytes are unchanged.

Raw foreign PDFs, extracted source text, page images, corpus caches,
compiled programs and discarded pilot data are omitted. Primary source
links and precise theorem locations permit independent retrieval. The
published package does not claim to authenticate omitted source bytes
from the package alone. The earlier source gate is identified by hash
in historical manifests; its full administrative report is not included.
The mathematical scope review and credited negative certificate are
available in [the initial scope excerpt](review/INITIAL_SCOPE_REVIEW.md).

AI tools were used extensively. These are unrefereed partial research
results; no new paper, DOI, release or external researcher communication
is part of this proposal.
