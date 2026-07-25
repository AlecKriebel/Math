# Certified exclusion status against frozen taxonomy v1

**Updated (UTC):** 2026-07-25T20:50:37Z.

This is the mutable status ledger for the immutable fourteen-leaf denominator
in `FROZEN_TAXONOMY_v1.md`.  Historical status strings in the hashed manifest
are not certification.  A row is promoted here only after a post-freeze
coverage bridge and an independent hostile replay both pass.

\[
\boxed{1/14\text{ certified excluded},\quad
       6/14\text{ provisional legacy exclusions},\quad
       7/14\text{ open}.}
\]

| Frozen row | Current status | Post-freeze certificate |
|---|---|---|
| `Q1` | open | -- |
| `Q2-E0-A4-B1-D1-N1` | open | -- |
| `Q2-E0-A2-B2-D1-N2` | provisional | -- |
| `Q2-E0-A2-B2-D2-N1` | provisional | -- |
| `Q2-E0-A1-B4-D1-N4` | open | -- |
| `Q2-E0-A1-B4-D2-N2` | **certified excluded** | `BRIDGE_Q2_E0_A1_B4_D2_N2_v1.md`; `HOSTILE_BRIDGE_AUDIT_Q2_E0_A1_B4_D2_N2_v1.md` |
| `Q2-E0-A1-B4-D4-N1` | open | -- |
| `Q2-E1-A3-B1-D1-N1` | open | -- |
| `Q2-E1-A1-B3-D1-N3` | open | -- |
| `Q2-E1-A1-B3-D3-N1` | provisional | -- |
| `Q2-E2-A2-B1-D1-N1` | provisional | -- |
| `Q2-E2-A1-B2-D1-N2` | open | -- |
| `Q2-E2-A1-B2-D2-N1` | provisional | -- |
| `Q2-E3-A1-B1-D1-N1` | provisional | -- |

The certified row is covered pointwise on every nonempty frozen pivot
stratum `C00`--`C14`; `C15`--`C44` are empty because the three leading
components are linearly independent.  Its lower exclusion has exact SymPy
and independently reconstructed PARI/GP checks.

This status record and its certificates were produced with substantial AI
assistance.  They are not peer review.  Exact checks are evidence about the
encoded algebra, not a verification by the mathematical community.
