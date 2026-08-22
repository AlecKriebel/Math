# Adversarial audit of the K2P article and reader supplement

Date: 21 August 2026

Final audited source: article SHA-256 `f3fb2af88aa22ea237240e1f13623c6e465b057a18877d993564863da66b96f4`

Frozen theorem authority: `work/final_theorem_release/RELEASE_LOCK.json`

Verdict: **mathematical pass; submission packaging and human metadata remain**

## Executive result

I found no counterexample, false promoted theorem statement, K2P model/domain
error, stale rooted restriction argument, improper ordinary-triangle image
claim, count mismatch, or mutation/replay failure.  The final edit round closed
all load-bearing formal issues found during review.  The article now defines
the local projective ported-factor relation, uses a Nash/analytic
constant-rank argument for genericity, constructs the exceptional set in the
correct output space, displays the sharpness cherry observables, defines the
continuous-time image and maximal rank, states the full-dimensional sharpness
conclusion, and prints the completion-count formula.

The current manuscript is therefore aligned with the frozen `K2P-SAME`
promotion.  Remaining review notes are the rendering boundary of the
machine-readable crosswalk, one bibliographic-year convention, and metadata
that only the human author can supply.  None calls for reopening the atlas or
changing the theorem.

## 1. Load-bearing findings: all closed

### Local ported-factor relation — closed

The earlier draft used `H preceq_+ H'` without defining the ported quotient.
Article lines 643--670 now define `Theta_+(H)`, the normalized boundary tensor,
the two-sector incidence torus, an analytic slice map, `d_H`, the physical
analytic local relation, chart independence, port matching, and the local
ordinary-triangle relation.  This makes the localization proposition and
bounded theorem formally typed.

### Analytic target section and exceptional set — closed

Article lines 1172--1187 now choose Nash (real-analytic semialgebraic)
constant-rank strata and invoke the analytic constant-rank theorem before
pulling the section back to a regular source chart.  Lines 1192--1203 now
distinguish output zero sets `V_N intersect Z(P)` from Zariski closures of
images of parameter-space rank-drop loci.  The earlier smooth-to-analytic jump
and parameter/output-space type error are gone.

### Weak-sharpness cherry induction — closed

Article lines 1438--1477 now display the exact Fourier-coordinate ratios

\[
 R_s=Q_{j=C,a=C,b=0}/Q_{j=C,a=0,b=C}=u_s/v_s,
 \qquad P_s=Q_{a=C,b=C}=u_sv_s,
\]

and their `G` analogues, state nonvanishing on the positive germ, and recover
old tensor coordinates by division.  The four-dimensional rank increment is
now an actual tensor-observable argument rather than only a parameter change.

### Continuous-time notation and sharpness quantifier — closed

Article lines 1251--1268 define `M_CT(N)` and state
`d_CT,N=d_N` by openness and polynomial minors.  Lines 1304--1311 now state
that the weak-class common germ is full-dimensional, matching the promoted
theorem.

### Completion compression wording — closed

Article lines 847--867 print the exact binomial-sum formula, the five locked
core tuples, their stars-and-bars derivation, and the target totals.  Line 1011
uses “three certified transport families”, while lines 1023--1025 retain the
essential warning that these are not three literal polynomials.

### Final reader-precision edits — closed

The final narrow edit round makes the abstract say that the structural
triangle class is exactly reconstructible (article lines 89--91), replaces
the potentially ambiguous completion-canonicalization wording (supplement
lines 189--197), displays the cherry Fourier observables and separates their
analytic inverse from graph pruning (supplement lines 518--530), designates
the machine crosswalk as the field-rich authority (supplement lines 532--545),
and marks the author-contribution statement explicitly pending human
confirmation (article lines 1520--1526 and supplement lines 786--804).  The
post-edit static and build checks pass.

## 2. Remaining non-load-bearing findings

### P2 submission package: the reader crosswalk is not field-complete

Supplement lines 532--622 list primary and replay paths; lines 625--672 list
selected hashes; and lines 675--705 give general commands and honestly mark
final runtime/archive measurements pending.  The supplied feedback requested,
for every theorem layer, schema/version, producer command, replay command,
mutation command, file SHA-256, semantic-payload SHA-256, and expected runtime.
Those fields are not all rendered per layer in the reader supplement.

The supplement now explicitly identifies the machine-readable JSON as the
field-rich authority and explains deliberately null runtimes.  The residual
note is only that the requested fields are delegated rather than rendered per
row in the reader PDF.  The static audit conservatively retains this as a
moderate submission item, not a mathematical failure.

### Bibliography year reconciliation

All citation keys resolve and every bibliography entry is used.  The entry
`EnglanderEtAl2026` at bibliography lines 139--150 uses year 2026 because the
cited theorem numbering is from version 4 dated 4 July 2026; Crossref records
the DOI as issued/posted on 24 April 2025.  Either convention is defensible if
made explicit.  A conventional alternative is year 2025 plus the version-4
date in the note.  This is a reconciliation item, not a theorem issue.

The supplement's refusal at lines 767--769 to cite the provisional local
K2P/K3P collision manuscript as a published result is prudent.  The feedback
should not be satisfied by inventing publication metadata.

### Human-only submission gates

The corresponding email, author-contribution statement, funding statement,
competing-interests declaration, public repository/tag, licenses, archive
SHA-256, DOI decision, and final full-run performance are visibly pending at
article lines 1511--1555 and supplement lines 786--804.  This is the correct
non-inventive treatment, but those fields block submission until the author
supplies them.

## 3. Independent validation

| Check | Result |
|---|---|
| frozen release lock and promotion-ready guard | PASS |
| unified quick release replay | PASS, all 19 layers, 334.712 s |
| compressed family-coverage equivalence | PASS |
| restoration-archetype replay | PASS: 997 parents, 2,540 roots, 36,824 edges, zero assignment problems |
| probe word replay | PASS: 176 anchors, 29,964 one-port, 544,571 two-port, 67,741 transports |
| fail-closed article static audit | PASS with only the three review items above |
| optimized-Python static-audit mutation | correctly rejected |
| deterministic static-audit output | PASS; repeated output SHA-256 `1432795c691537a44fc6c1925a1074c158db8cfe3917772c4c0c4361c53b93a3` |
| clean Tectonic article build | PASS, 22 pages |
| clean Tectonic supplement build | PASS, 15 pages |
| undefined references/citations or overfull boxes | zero |

The article has four underfull-box warnings in the PC-PARTIAL table.  The
supplement has 126 underfull-box warnings, concentrated in narrow path/hash
tables, especially the theorem-to-artifact crosswalk.  They are cosmetic, but
a ragged-right list, landscape table, or wider path column would read better.

## 4. Frozen count reconciliation

Every audited census agrees with the corrected release:

- four-port raw directions: `405,216`;
- five-port `theta2` directions: `2,946,240`;
- three-port cycle directions: `13,440`;
- terminal presentations/classes: `1,472 / 934`;
- restoration members/parents: `2,540 / 997`;
- restoration forest: `36,568 + 256 = 36,824` edges, `36,792` leaves;
- direct high-degree layer: `36` records, `27` directional bodies, three
  certified families;
- equality anchors: `176`;
- probes: `29,964` one-port and `544,571` two-port rows; and
- unresolved mathematical records: zero.

## 5. Final content-hash freeze

| Source | SHA-256 |
|---|---|
| `article/main.tex` | `f3fb2af88aa22ea237240e1f13623c6e465b057a18877d993564863da66b96f4` |
| `article/references.bib` | `95cd4ecda54495b8f7f7a465ab3ae6e24f06123375695f8d4af8af0609945968` |
| `supplement/supplement.tex` | `455d613ade6994a81d8b30e09b8ffadbdc82abfff80b9487c5d79f58d5d0f9a5` |
| `supplement/compression_tables.tex` | `5679e1064e8ed8713288a3d842df197260e5e005721165eb5b3fa8ca81bae225` |

The frozen release-lock SHA-256 is
`0c17eeaa3344f0982998ea694c1eb92f72f5ced0841e2acad0d39566e2ec71c3`.
The four manuscript-source hashes were unchanged across the final static
audit, repeated deterministic check, and both clean builds.

## Final recommendation

Retain `K2P-SAME`; do not rerun or redesign the atlas in response to this
review.  Decide whether the machine-crosswalk delegation is sufficient for the
target journal, reconcile the Englander year convention, and obtain the human
metadata/signoff.  After those packaging changes, rerun the static checker and
one source-bound release verification.  No load-bearing mathematical patch is
currently outstanding.
