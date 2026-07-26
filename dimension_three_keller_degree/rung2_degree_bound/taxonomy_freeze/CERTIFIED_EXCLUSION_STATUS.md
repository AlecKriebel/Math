# Certified exclusion status against frozen taxonomy v1

**Updated (UTC):** 2026-07-26T10:02:40Z.

This is the mutable status ledger for the immutable fourteen-leaf denominator
in `FROZEN_TAXONOMY_v1.md`.  Historical status strings in the hashed manifest
are not certification.  A row is promoted here only after a post-freeze
coverage bridge and an independent hostile replay both pass.

\[
\boxed{6/14\text{ certified excluded},\quad
       2/14\text{ provisional legacy exclusions},\quad
       6/14\text{ open}.}
\]

| Frozen row | Current status | Post-freeze certificate |
|---|---|---|
| `Q1` | open | -- |
| `Q2-E0-A4-B1-D1-N1` | open | -- |
| `Q2-E0-A2-B2-D1-N2` | provisional | -- |
| `Q2-E0-A2-B2-D2-N1` | **certified excluded** | `BRIDGE_Q2_E0_A2_B2_D2_N1_v1.md`; `audit_bridge_q2_e0_a2_b2_d2_n1_v1/REPORT.md` |
| `Q2-E0-A1-B4-D1-N4` | open | -- |
| `Q2-E0-A1-B4-D2-N2` | **certified excluded** | `BRIDGE_Q2_E0_A1_B4_D2_N2_v1.md`; `HOSTILE_BRIDGE_AUDIT_Q2_E0_A1_B4_D2_N2_v1.md` |
| `Q2-E0-A1-B4-D4-N1` | open | -- |
| `Q2-E1-A3-B1-D1-N1` | **certified excluded** | `BRIDGE_Q2_E1_A3_B1_D1_N1_v1.md`; `audit_bridge_q2_e1_a3_b1_d1_n1_v1/REPORT.md` |
| `Q2-E1-A1-B3-D1-N3` | open | -- |
| `Q2-E1-A1-B3-D3-N1` | **certified excluded** | `audit_bridge_q2_e1_a1_b3_d3_n1_v1/REPORT.md` |
| `Q2-E2-A2-B1-D1-N1` | **certified excluded** | `BRIDGE_Q2_E2_A2_B1_D1_N1_v1.md`; `audit_bridge_q2_e2_v1/REPORT.md` |
| `Q2-E2-A1-B2-D1-N2` | open | -- |
| `Q2-E2-A1-B2-D2-N1` | provisional | -- |
| `Q2-E3-A1-B1-D1-N1` | **certified excluded** | `BRIDGE_Q2_E3_A1_B1_D1_N1_v1.md`; `HOSTILE_BRIDGE_AUDIT_Q2_E3_A1_B1_D1_N1_v1.md` |

For `Q2-E0-A1-B4-D2-N2`, every nonempty frozen pivot stratum
`C00`--`C14` is covered pointwise; `C15`--`C44` are empty because the
three leading components are linearly independent.  Its lower exclusion
has exact SymPy and independently reconstructed PARI/GP checks.

For `Q2-E0-A2-B2-D2-N1`, every nonempty `C00`--`C14` piece routes
pointwise to the canonical conic embedding of a relatively closed
quadratic pencil; `C15`--`C44` are empty.  Relative closure excludes two
double-line pencil members, leaving the zero- and unique-double-line
branches.  The hostile replay independently reconstructs the missing
exact ranks, kernels, cokernels, compatibility ideals, and full affine
solution spaces in both lower branches.

For `Q2-E3-A1-B1-D1-N1`, `C00`--`C29` route pointwise through a uniform
normal form to an intrinsic binary/nonbinary split, while `C30`--`C44`
are division-free empty by the rank-two condition.  Both legacy exits
replay, and a new dependency-free hostile checker reconstructs the
unrestricted nonbinary coefficient solves that were missing as retained
standalone provenance.

For `Q2-E1-A3-B1-D1-N1`, `C00`--`C29` route without a frozen-coefficient
division to the intrinsic horizontal/unique-vertical split, while
`C30`--`C44` are empty by rank at most one.  The hostile bridge audit
expands the route into 48 disjoint atoms and 15 terminal groups, all with
independent PASS reports.  It also repaired the formerly aggregate-only
provenance of the unconditional quadratic-component exit.

For `Q2-E1-A1-B3-D3-N1`, `C00`--`C14` route without division to the
intrinsic node/cusp and aligned/transverse split, while `C15`--`C44` are
empty because every target component is nonzero.  The bridge replayed all
eight legacy exact checks and independently reconstructed the previously
unretained general-coefficient transverse-nodal solves, with exact ranks
\(24,16,9\) in degrees eight, seven, and six and the terminal degree-five
square.

For `Q2-E2-A2-B1-D1-N1`, `C00`--`C29` refine into 45 ordered intrinsic
rank-two minor charts, while `C30`--`C44` are empty by rank at most one.
The marked-equal branch and all thirteen frozen marked-distinct strata are
covered.  The independent bridge replay reconstructs both discrete `CO`
quotients and their lower exits with dependency-free exact arithmetic.
Three zero-companion terminals use the quadratic-component automorphism
theorem; the ten nonzero marked-distinct terminals force a singular linear
part.

This status record and its certificates were produced with substantial AI
assistance.  They are not peer review.  Exact checks are evidence about the
encoded algebra, not a verification by the mathematical community.
