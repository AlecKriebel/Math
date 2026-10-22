# Research log: 30005078

All times UTC on 5 October 2026. Percentages describe preparation of this
bounded research packet, not probabilities of a theorem being true. The
general-module proof remains incomplete throughout.

## 20:54–20:56: source readiness

Requested the numeric landing page first; it was inaccessible. Recovered the
publisher report, the complete supplied corpus record and the current papers.
Verified the selected statement hash against the catalogue. The governing
question is 3.1 on printed p. 873, in the products-of-projective-spaces setup;
question 3.2 is a separate toric-variety issue. Initial actual repository ID,
code, PR, commit and branch searches found no prior attempt.

Packet completion estimate: 20%. General-module resolution: not established.

## 20:56–20:58: approach families 1–3

1. Reviewed exact membership via quasilinear truncations. This is a usable
   finite test at each degree under the stated torsion hypothesis; it does not
   certify when enumeration of all minimal degrees is finished.
2. Reviewed inner and outer bounds and finite-generation results. A finite
   antichain existence theorem does not supply its largest coordinates. The
   explicit family U_T in PROOF.md isolates the missing termination information.
3. Examined monomial degeneration and current bigraded Gröbner-basis results.
   Full regularity is not generally preserved, so applying a monomial algorithm
   to an initial ideal would not resolve the target. Current Macaulay2 source
   explicitly confirms that its default upper search limit lacks a universal
   correctness guarantee.

Decision: preserve these as exact blocked routes, not full solutions.
Packet completion estimate: 40%. General-module resolution: not established.

## 20:58–21:03: approach families 4–5

4. Constructed the finite-cell Cech algorithm for monomial quotients. Derived
   the whole regularity formula from support-cell upper endpoints. Proved that
   every minimal element is at a threshold and derived the explicit input-based
   box. Implemented exact rational/prime-field linear algebra and replay tests.
5. Distinguished sheaf and module regularity. The diagonal sheaf gives the
   half-space a+b>=0 with infinite minimal antichain; its Cox module instead
   has regularity N^2. Added zero-sheaf and torsion examples so an empty or
   incomplete minimal list is not mistaken for an empty full region.

The monomial theorem is a separate scoped result. The diagonal disproves the
unrestricted finite-list sheaf interpretation; it does not establish an
impossibility theorem for alternative symbolic output formats.

Packet completion estimate: 75%. General-module resolution: not established.

## 21:03–21:09: author validation and freeze

Read the actual current main attempts directory: 63 entries, none for the
selected target. Checked the queue row and related-target groups, without
using the queued status as proof of no prior work. Corpus byte counts and
SHA-256 hashes match the independently read pinned repository manifest.
The complete prior-report dictionary lacks the selected exact key. Catalogue
Git blob matches the remote listing. The full corpus, source records and
source files remain outside the distribution.

The neighboring target 30005077 merits a separate precise-hypothesis review
against the 2026 uniqueness/truncation theorem. No new proof-search budget or
automatic status change was applied to that target.

Authored proof and reference implementation replay passed. The tests include
independent singly graded Koszul comparisons, multiple characteristics, and
degenerate cases. No external computer algebra system was executed. Final
archive is allowlisted and excludes source material and private coordination.

Stop after five approach families. Packet completion estimate: 100% for the
author deliverable. General-module resolution: not established. Independent
mathematical audit is pending; author checks are not an independent audit.
