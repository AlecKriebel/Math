# Exact planar clique pinning in tractable regimes

This is an accepted partial result for problem 3000001 / AMR-029-0001. The
objective is the minimum cardinality of a vertex set S such that adding the
missing edges of its clique makes a finite simple graph generically globally
rigid in the plane. The general arbitrary-input optimum remains unresolved
by this work. There is no hardness, novelty, FPT, or current-openness claim.

## Results and credited prior work

The [complete partial-result proof](PARTIAL_RESULTS.md) gives a sharp
rigidifying-subset bound delta+1 and an exact n^(delta+O(1)) XP algorithm in
planar rigidity deficiency, using the established constrained rigid-input
optimizer. It also proves the sparse redundancy criterion, equality with
feedback vertex number for simple 3-connected cubic graphs of order at least
twelve, the exact forest formula, all stated small-order exceptions, and a
two-separator negative control. The original 3-connectivity hypothesis in
the cubic theorem is essential.

The [staging appendix](STAGING_OBSTRUCTION.md) proves analytically that an
arbitrary minimum ordinary-rigidifying seed need not extend to an optimal
global pin set. On m disjoint copies of K_(2,3), the displayed ordinary,
global and retained-seed optima are 2m, 3m and 5m for every positive integer m.
The ratio 5/3 concerns this allowed first-stage choice; it is neither a
hardness result nor a lower bound for every possible first-stage selection.
The appendix also includes the accepted diamond-plus-isolate example.

Király–Mihálykó are credited for exact rigid-input optimization, constrained
completion and the factor-two approximation for arbitrary inputs. Jordán is
credited for the sparse rank formula and prior M-connected formulation.
Ueno–Kajitani–Gotoh are credited for polynomial subcubic feedback vertex set.
These are used as prior results, without a discovery claim.

## Source and review boundaries

The [source metadata](SOURCE_METADATA.json) distinguishes the inspected
repository review manuscript from the final publisher PDF. The revised
Mihálykó dissertation retains the needed planar theorem for simple rigid
graphs of order at least six; the proof handles n<=5 directly and explicitly
covers already-global and single-edge-completion exceptions.

The Ueno–Kajitani–Gotoh primary publisher abstract was inspected, but its
full PDF endpoint returned HTTP 403. The polynomial cubic corollary relies
on the established cited theorem; the original reduction and complexity
proof were not independently re-audited. Recorded source and check history
is not a new retrieval, inspection, literature search or computation rerun
by edition preparation.

This AI-assisted manuscript and its separate mathematical audits are
unrefereed. Acceptance means the analytic arguments passed those audits;
it is not external human peer review, journal acceptance, formal
proof-assistant certification, bibliographic priority, or proof of current
openness.

## Contents

- [PARTIAL_RESULTS.md](PARTIAL_RESULTS.md): full analytic partial-result proof
- [STAGING_OBSTRUCTION.md](STAGING_OBSTRUCTION.md): full analytic appendix
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md) and [ACCEPTANCE.json](ACCEPTANCE.json): main mathematical audit and its exact scope
- [STAGING_AUDIT.md](STAGING_AUDIT.md) and [STAGING_ACCEPTANCE.json](STAGING_ACCEPTANCE.json): separate appendix audit and acceptance
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public citations, recorded source hashes, inspection history and limitations
- [STATUS.json](STATUS.json): partial status and unchanged one-of-five attempt accounting
- [MANIFEST.json](MANIFEST.json): ten-member inventory and hashes of the other nine files; the draft PR body independently pins the manifest

Finite exact checks are corroboration only. Programs, raw generated outputs,
dataset contents, copied third-party source bodies or images, and private
coordination material are excluded. No excluded file is a mathematical
premise. This edition changes no QUEUE entry or unrelated repository content
and adds no substantive proof attempt. It requests no merge, release, DOI,
journal submission, or outside outreach.
