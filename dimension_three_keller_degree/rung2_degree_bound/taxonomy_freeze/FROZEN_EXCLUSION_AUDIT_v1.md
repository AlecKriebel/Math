# Hostile audit of exclusions against the frozen quartic denominator

**Recorded (UTC):** 2026-07-25T20:32:23Z.

**Frozen object:** `FROZEN_TAXONOMY_v1.md`, with fourteen inclusive
leading leaves and forty-five coefficient-pivot strata in each leaf.

**Verdict:** the legacy record contains seven substantial row-level
*candidate* exclusions, but none yet satisfies the post-freeze coverage
gate in Section 5 of `FROZEN_TAXONOMY_v1.md`.  The honest frozen numerator
is therefore
\[
\boxed{0/14\text{ certified excluded},\quad
       7/14\text{ provisional},\quad
       7/14\text{ open}.}
\]

This is a certificate-level demotion, not a finding that the seven
mathematical arguments are false.  Several packages have unusually strong
exact and hostile-audit evidence.  What is missing is the bridge from the
pre-freeze normal-form/orbit atlases to the frozen inclusive leaves and
their `C00`--`C44` cover.  The frozen files were not altered.

## 1. Audit rule

A frozen row is called **certified excluded** here only if all four gates
pass.

1. The theorem statement quantifies over the entire inclusive frozen row,
   not a generic locus, normal-form slice, or named incidence sublocus.
2. The normal-form/orbit list is proved exhaustive, including every
   vanishing denominator, rank drop, stabilizer jump, and reclassification
   boundary.
3. The calculation is genuinely division-free in the original row
   coefficients, or the normal-form charts are explicitly routed back to
   every frozen pivot stratum `C00`--`C44`.
4. A retained independent hostile-audit artifact and a methodologically
   independent exact check cover the same full scope.

“SymPy and PARI both pass” does not by itself pass gate 4 when they encode
the same reduction.  Likewise, a report that every *named* orbit is closed
does not pass gate 2 unless the orbit list itself has an independent
completeness proof.

A repository-wide exact-text check found no reference outside
`taxonomy_freeze/` to `FROZEN_TAXONOMY_v1`, `C00`, `C44`,
“coefficient-pivot”, or “pivot strata”.  Thus no legacy exclusion contains
the required post-freeze bridge.

## 2. Fixed fourteen-row matrix

| Frozen row | Honest status | Primary theorem and exact-check artifacts | Independent-audit status | Division-free or frozen-pivot coverage | Scope mismatch / surviving locus |
|---|---|---|---|---|---|
| `Q1` | **open** | `dimension_three_keller_degree/rung2_degree_bound/WORKING_RANK_ONE_QUARTIC.md`; `dimension_three_keller_degree/rung2_degree_bound/WORKING_RANK_ONE_QUOTIENT_CUBIC.md`; `dimension_three_keller_degree/rung2_degree_bound/WORKING_RANK_ONE_PRIMITIVE_EXIT.md`; `dimension_three_keller_degree/rung2_degree_bound/WORKING_RANK_ONE_COMPOSITE_EXIT.md`; `dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md` | Aggregate audit prose exists in `VERIFICATION.md`; no retained full-`Q1` hostile report. | No `C00`--`C44` map. Some displayed identities are division-free only after a projected-cubic stratification. | Primitive projected cubic pencils are treated; the nonprimitive/common-ramification locus and other inclusive rank-one configurations remain. |
| `Q2-E0-A4-B1-D1-N1` | **open** | `dimension_three_keller_degree/rung2_degree_bound/WORKING_LINE_TYPE_LEADING_NET.md`; `dimension_three_keller_degree/rung2_degree_bound/verify_quartic_strata_sympy.py`; `dimension_three_keller_degree/rung2_degree_bound/verify_quartic_strata_pari.gp`; `dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md` | Partial calculations are described in the aggregate record; no full-row hostile audit. | No frozen-pivot map and no global division-free row exclusion. | Only the exceptional \(L^4/L^3\) shape is forced; it is not eliminated. |
| `Q2-E0-A2-B2-D1-N2` | **provisional** | `dimension_three_keller_degree/rung2_degree_bound/WORKING_LINE_TYPE_22.md`; component checks and audits catalogued in Section 3.1 below; `dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md` | Many component audits pass. `dimension_three_keller_degree/rung2_degree_bound/audit_line22_fg/REPORT.md` explicitly failed the first full-moduli claim and passed only a narrow chart; later packages cover the identified omissions, but no independent post-assembly audit starts from the frozen row. | Branchwise certificates are often specialization-safe, but the assembly is not division-free in the original 45 coefficients and has no `C00`--`C44` routing. | The theorem claims the full row, but its completeness currently rests on a union of pre-freeze joint-orbit lists rather than a frozen-row coverage certificate. |
| `Q2-E0-A2-B2-D2-N1` | **provisional** | `dimension_three_keller_degree/rung2_degree_bound/WORKING_CONIC_TYPE_22.md`; `dimension_three_keller_degree/rung2_degree_bound/verify_conic_doubleline_sympy.py`; `dimension_three_keller_degree/rung2_degree_bound/verify_conic_doubleline_pari.gp`; `dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md` | Detailed independent reconstruction is asserted in `VERIFICATION.md`, but no standalone hostile report or post-freeze replay was retained. | The invariant first-integral steps are division-free; the no/unique/two-double-line normal-form routing is not mapped to `C00`--`C44`. | The theorem statement is row-sized. The certification gap is coverage provenance, not an explicit surviving mathematical sublocus. |
| `Q2-E0-A1-B4-D1-N4` | **open** | `dimension_three_keller_degree/rung2_degree_bound/WORKING_LINE_TYPE_14.md`; `dimension_three_keller_degree/rung2_degree_bound/WORKING_LINE_TYPE_14_RAMIFICATION.md`; `dimension_three_keller_degree/rung2_degree_bound/verify_quartic_strata_sympy.py`; `dimension_three_keller_degree/rung2_degree_bound/verify_quartic_strata_pari.gp` | Partial ramification audit is summarized in `dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md`; no row audit. | No frozen-pivot map and no global division-free exclusion. | The gcd-one locus is treated and ramification shapes are classified, but the ramified shapes are not all eliminated. |
| `Q2-E0-A1-B4-D2-N2` | **provisional** | `dimension_three_keller_degree/rung2_degree_bound/WORKING_CONIC_DOUBLE_COVER_EXIT.md`; `dimension_three_keller_degree/rung2_degree_bound/verify_conic_double_cover_exit_sympy.py`; `dimension_three_keller_degree/rung2_degree_bound/audit_conic_double_cover_hostile/audit_conic_double_cover_pari.gp`; `dimension_three_keller_degree/rung2_degree_bound/audit_conic_double_cover_hostile/RESEARCH_LOG.md` | Strong PASS: the hostile log reconstructs the degree-two-cover normalization, stabilizer quotient, raw determinants, zero patterns, and fail-closed wrapper independently. | The lower calculation is branchwise division-free after the global normal form, but there is no explicit map from an arbitrary frozen pivot stratum to that normal form. | No mathematical survivor is exhibited. This is the cheapest row to promote once the frozen coverage bridge is written and audited. |
| `Q2-E0-A1-B4-D4-N1` | **open** | `dimension_three_keller_degree/rung2_degree_bound/WORKING_RATIONAL_QUARTIC_IMAGE.md`; `dimension_three_keller_degree/rung2_degree_bound/verify_quartic_strata_sympy.py`; `dimension_three_keller_degree/rung2_degree_bound/verify_quartic_strata_pari.gp`; `dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md` | A partial adversarial audit is summarized in `VERIFICATION.md`; no full-row report. | No frozen-pivot map and no division-free treatment of all ramification strata. | Only the gcd-one normal-minor locus is excluded; a nonconstant ramification divisor remains. |
| `Q2-E1-A3-B1-D1-N1` | **open** | `dimension_three_keller_degree/rung2_degree_bound/fixed_linear_cubic_pencil/WORKING_HORIZONTAL_FIXED_LINEAR_CUBIC_PENCIL.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_linear_cubic_pencil/audit_hostile/REPORT.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_linear_cubic_pencil/vertical_locus/WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_linear_cubic_pencil/vertical_locus/audit_vertical_hostile/REPORT.md` | Horizontal and vertical-top audits pass on their stated scopes. | The valuation exclusions are division-free on their scopes; there is no frozen-pivot map, and the lower triple-vertical frontier is not excluded. | On vertical multiplicity \(m=3\), the two companions \(G_3=h^3\) and \(G_3=q\) survive the top identities; an explicit witness survives through \(E_5\) and fails first at \(E_4\). |
| `Q2-E1-A1-B3-D1-N3` | **open** | `dimension_three_keller_degree/rung2_degree_bound/fixed_linear_line_triplecover/WORKING_NONBINARY_FIXED_LINEAR_LINE_TRIPLECOVER.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_linear_line_triplecover/audit_hostile/REPORT.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_linear_line_triplecover/binary_locus/RESEARCH_LOG.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_linear_line_triplecover/binary_locus/DELTA1_COMPLETE_CANDIDATE.md` | Nonbinary audit passes. Most binary incidence notes explicitly say hostile audit pending; one narrow unmarked-double component has a PASS report. | No frozen-pivot map; the binary leaf collection is not independently complete or uniformly division-free. | The entire binary locus is still a candidate case tree, with multiple provisional exact-\(\delta\) pieces and incomplete hostile coverage. |
| `Q2-E1-A1-B3-D3-N1` | **provisional** | Four theorem/check pairs catalogued in Section 3.4 below; aggregate record `dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md` | Independent raw reconstructions are described in the aggregate record for nodal/cuspidal and transverse/aligned branches, but no standalone full-row hostile report was retained. | Several decisive certificates are explicitly division-free in the marked parameter, but the four normal-form atlases are not routed to `C00`--`C44`. | The four notes jointly claim the row. The remaining issue is a frozen coverage and audit-provenance certificate, not a named surviving branch. |
| `Q2-E2-A2-B1-D1-N1` | **provisional** | `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_verticality/WORKING_FIXED_DIVISOR_VERTICALITY_PRINCIPLE.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_verticality/all_vertical_top_obstruction/NOTE.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_e2_quadratic_pencils/NOTE.md`; supporting audits/checks catalogued in Section 3.5 | Strong component-level PASS reports exist for verticality, the all-vertical obstruction, mixed companions, and both triple companions. | The valuation steps are global and division-free, but the later normal-form tree uses branch pivots (including explicit \(1/d\) formulas) and has no `C00`--`C44` routing. No independent audit reassembles the complete chain from an arbitrary frozen-row point. | No mathematical survivor is recorded after the assembled chain. Formal promotion requires only a complete frozen bridge and an assembly audit, but that bridge is presently absent. |
| `Q2-E2-A1-B2-D1-N2` | **open** | `dimension_three_keller_degree/rung2_degree_bound/fixed_quadratic_line_doublecover/WORKING_NONBINARY_FIXED_QUADRATIC_LINE_DOUBLECOVER.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_quadratic_line_doublecover/audit_hostile/REPORT.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_quadratic_line_doublecover/binary_locus/WORKING_BINARY_LOCUS.md`; `dimension_three_keller_degree/rung2_degree_bound/fixed_quadratic_line_doublecover/binary_locus/DELTA2_11_LEAF_REGISTRY.md` | Nonbinary PASS. The abstract binary Hilbert--Burch lemma has a PASS report, but most lower binary leaves explicitly await hostile audit. | No frozen-pivot map and no complete division-free binary-row proof. | The binary fixed-quadratic locus remains an expanding provisional incidence tree; the active \(\delta=2,\{1,1\}\) elimination is not certified complete. |
| `Q2-E2-A1-B2-D2-N1` | **provisional** | `dimension_three_keller_degree/rung2_degree_bound/WORKING_FIXED_CONIC_ROW.md`; `dimension_three_keller_degree/rung2_degree_bound/WORKING_NONBINARY_FIXED_CONIC_ROW.md`; `dimension_three_keller_degree/rung2_degree_bound/verify_fixed_conic_row_sympy.py`; `dimension_three_keller_degree/rung2_degree_bound/verify_fixed_conic_row_pari.gp`; `dimension_three_keller_degree/rung2_degree_bound/verify_nonbinary_fixed_conic_sympy.py`; `dimension_three_keller_degree/rung2_degree_bound/verify_nonbinary_fixed_conic_pari.gp` | Raw audits of the two binary and five nonbinary forms are described in `dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md`; no standalone combined hostile report was retained. | Many terminal certificates are division-free, but the seven parabolic normal forms are not mapped to `C00`--`C44`; normalizations use casewise nonzero pivots. | The two notes jointly claim the full row. The gap is frozen coverage and retained audit provenance, not a stated survivor. |
| `Q2-E3-A1-B1-D1-N1` | **provisional** | `dimension_three_keller_degree/rung2_degree_bound/WORKING_FIXED_CUBIC_LINE_ROW.md`; `dimension_three_keller_degree/rung2_degree_bound/WORKING_BINARY_FIXED_CUBIC_LINE_ROW.md`; `dimension_three_keller_degree/rung2_degree_bound/verify_fixed_cubic_line_sympy.py`; `dimension_three_keller_degree/rung2_degree_bound/verify_fixed_cubic_line_pari.gp`; `dimension_three_keller_degree/rung2_degree_bound/verify_binary_fixed_cubic_complete.py`; `dimension_three_keller_degree/rung2_degree_bound/verify_binary_fixed_cubic_complete_pari.gp` | Binary half has a retained PASS at `dimension_three_keller_degree/rung2_degree_bound/audit_binary_fixed_cubic_hostile/REPORT.md`. The nonbinary hostile reconstruction is described only in the aggregate `VERIFICATION.md`. | Nonbinary valuation steps are division-free; the binary orbit tree is specialization-aware but not globally division-free in frozen coefficients, and neither half maps to `C00`--`C44`. | Binary/nonbinary is an exhaustive conceptual split, but the post-freeze chart bridge and a retained full-row assembly audit are missing. |

## 3. Dossiers for the seven legacy excluded rows

### 3.1 `Q2-E0-A2-B2-D1-N2`: genuine line double cover

The row-sized synthesis is
`dimension_three_keller_degree/rung2_degree_bound/WORKING_LINE_TYPE_22.md`.
Its exact and hostile component packages include:

- `dimension_three_keller_degree/rung2_degree_bound/audit_line22_fg/REPORT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/line22_marked_critical_infinity/audit_hostile/REPORT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/line22_outer_infinity_remaining/audit_hostile/REPORT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/line22_companion_infinity/audit_hostile/REPORT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/line22_rankone_restriction/audit_hostile/REPORT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/line22_rankone_restriction/marked_mixed_orbits/audit_hostile/AUDIT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/line22_rankone_restriction/marked_triple_orbit/audit_hostile/independent/AUDIT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/line22_rankone_restriction/unmarked_triple_c0/audit_hostile/AUDIT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/line22_rankone_restriction/unmarked_resonance_c3/audit_hostile/REPORT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/line22_rankone_restriction/unmarked_companion_infinity/audit_hostile/REPORT.md`.

The exact runners are indexed in the “Completion of the genuine
line-\((2,2)\) row” section of
`dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md`.
This is strong evidence for every named package.  It is not an independent
proof that the union of named packages equals every point of all 45 frozen
pivot strata.  The earlier full-moduli failure makes that missing assembly
audit material rather than cosmetic.

### 3.2 `Q2-E0-A2-B2-D2-N1`: genuine conic embedding

The entire claim is in
`dimension_three_keller_degree/rung2_degree_bound/WORKING_CONIC_TYPE_22.md`.
The two exact implementations are
`dimension_three_keller_degree/rung2_degree_bound/verify_conic_doubleline_sympy.py`
and
`dimension_three_keller_degree/rung2_degree_bound/verify_conic_doubleline_pari.gp`.
The independent reconstruction is described in
`dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md`.

The mathematical split into no, one, or two double-line fibres is the
right prospective coverage theorem: two fibres reclassify to the
conic-double-cover row.  However, that split and its unique-double-line
normal forms have not been replayed against the frozen coefficient cover by
a retained auditor.  The row is therefore provisional.

### 3.3 `Q2-E0-A1-B4-D2-N2`: conic double cover

This is the strongest and shortest promotion candidate.  The row theorem is
`dimension_three_keller_degree/rung2_degree_bound/WORKING_CONIC_DOUBLE_COVER_EXIT.md`.
The primary exact calculation is
`dimension_three_keller_degree/rung2_degree_bound/verify_conic_double_cover_exit_sympy.py`.
The independent raw reconstruction and fail-closed wrapper are:

- `dimension_three_keller_degree/rung2_degree_bound/audit_conic_double_cover_hostile/audit_conic_double_cover_pari.gp`;
- `dimension_three_keller_degree/rung2_degree_bound/audit_conic_double_cover_hostile/audit_conic_double_cover_pari_strict.sh`;
- `dimension_three_keller_degree/rung2_degree_bound/audit_conic_double_cover_hostile/audit_conic_double_cover_wrapper_selftest.sh`;
- `dimension_three_keller_degree/rung2_degree_bound/audit_conic_double_cover_hostile/RESEARCH_LOG.md`.

The hostile log explicitly certifies the unique global degree-two-cover
normal form and every lower zero pattern.  A short new lemma routing each
frozen pivot point through this normal form, followed by a clean-room check
of that lemma, should be enough for promotion.

### 3.4 `Q2-E1-A1-B3-D3-N1`: rational plane cubic

The four necessary geometric pieces are:

- `dimension_three_keller_degree/rung2_degree_bound/WORKING_NODAL_CUBIC_CURVE_EXIT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/WORKING_SCALAR_ALIGNED_NODAL_CUBIC_EXIT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/WORKING_CUSPIDAL_CUBIC_CURVE_EXIT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/WORKING_SCALAR_ALIGNED_CUSPIDAL_CUBIC_EXIT.md`.

Their exact pairs are:

- `dimension_three_keller_degree/rung2_degree_bound/verify_nodal_cubic_exit_sympy.py` and
  `dimension_three_keller_degree/rung2_degree_bound/verify_nodal_cubic_exit_pari.gp`;
- `dimension_three_keller_degree/rung2_degree_bound/verify_scalar_aligned_nodal_sympy.py` and
  `dimension_three_keller_degree/rung2_degree_bound/verify_scalar_aligned_nodal_pari.gp`;
- `dimension_three_keller_degree/rung2_degree_bound/verify_cuspidal_cubic_exit_sympy.py` and
  `dimension_three_keller_degree/rung2_degree_bound/verify_cuspidal_cubic_exit_pari.gp`;
- `dimension_three_keller_degree/rung2_degree_bound/verify_scalar_aligned_cusp_sympy.py` and
  `dimension_three_keller_degree/rung2_degree_bound/verify_scalar_aligned_cusp_pari.gp`.

The aggregate verification record describes independent raw
reconstructions and the nodal/cuspidal plus transverse/aligned exhaustion.
There is no retained standalone report auditing the four-way union as a
frozen row, so it remains provisional.

### 3.5 `Q2-E2-A2-B1-D1-N1`: fixed quadratic, primitive pencil

The coverage chain is:

1. horizontal components excluded by
   `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_verticality/WORKING_FIXED_DIVISOR_VERTICALITY_PRINCIPLE.md`;
2. all-vertical leading shapes reduced by
   `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_verticality/all_vertical_top_obstruction/NOTE.md`;
3. the two remaining canonical pencils and their mixed/triple companions
   excluded by
   `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_e2_quadratic_pencils/NOTE.md`.

Retained hostile reports include:

- `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_verticality/audit_hostile/REPORT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_verticality/all_vertical_top_obstruction/audit_hostile/REPORT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_e2_quadratic_pencils/audit_hostile/REPORT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_e2_quadratic_pencils/ranktwo_triple/audit_hostile/REPORT.md`;
- `dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_e2_quadratic_pencils/rankone_triple/audit_hostile_external/REPORT.md`.

This is the strongest multi-package chain, but there is no independent
assembly proof that starts with an arbitrary point in the frozen row and
routes it through every chain boundary.  The absence of a `C00`--`C44`
bridge therefore remains a formal blocker.

### 3.6 `Q2-E2-A1-B2-D2-N1`: fixed quadratic times a conic

The binary and nonbinary halves are
`dimension_three_keller_degree/rung2_degree_bound/WORKING_FIXED_CONIC_ROW.md`
and
`dimension_three_keller_degree/rung2_degree_bound/WORKING_NONBINARY_FIXED_CONIC_ROW.md`.
The four exact implementations are:

- `dimension_three_keller_degree/rung2_degree_bound/verify_fixed_conic_row_sympy.py`;
- `dimension_three_keller_degree/rung2_degree_bound/verify_fixed_conic_row_pari.gp`;
- `dimension_three_keller_degree/rung2_degree_bound/verify_nonbinary_fixed_conic_sympy.py`;
- `dimension_three_keller_degree/rung2_degree_bound/verify_nonbinary_fixed_conic_pari.gp`.

The seven parabolic normal forms and raw hostile reconstructions are
described in `dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md`.
No standalone combined audit artifact or frozen-pivot routing exists.

### 3.7 `Q2-E3-A1-B1-D1-N1`: fixed cubic times a line

The exhaustive conceptual split is binary versus nonbinary:

- `dimension_three_keller_degree/rung2_degree_bound/WORKING_FIXED_CUBIC_LINE_ROW.md`;
- `dimension_three_keller_degree/rung2_degree_bound/WORKING_BINARY_FIXED_CUBIC_LINE_ROW.md`.

The exact implementations are:

- `dimension_three_keller_degree/rung2_degree_bound/verify_fixed_cubic_line_sympy.py`;
- `dimension_three_keller_degree/rung2_degree_bound/verify_fixed_cubic_line_pari.gp`;
- `dimension_three_keller_degree/rung2_degree_bound/verify_binary_fixed_cubic_complete.py`;
- `dimension_three_keller_degree/rung2_degree_bound/verify_binary_fixed_cubic_complete_pari.gp`.

The binary hostile audit is retained at
`dimension_three_keller_degree/rung2_degree_bound/audit_binary_fixed_cubic_hostile/REPORT.md`.
The nonbinary reconstruction is described only in the aggregate
`dimension_three_keller_degree/rung2_degree_bound/VERIFICATION.md`.
There is no post-freeze full-row assembly audit or coefficient-pivot map.

## 4. Consequences

1. The strings `excluded-audited` in the frozen manifest must be treated as
   historical candidate labels, exactly as Section 7 of
   `FROZEN_TAXONOMY_v1.md` warns.  They are not the certified numerator.
2. No new fifteenth row was found.  This audit does not challenge the
   frozen denominator.
3. The most efficient certification experiment is
   `Q2-E0-A1-B4-D2-N2`: construct a post-freeze coverage lemma from an
   arbitrary row point (on each nonempty `C00`--`C44`) to
   \(H_4=(x^4,x^2y^2,y^4)\), record every invertibility condition, and have
   a fresh hostile auditor reconstruct only that bridge.  The lower
   exclusion is already independently strong.
4. Until at least one such bridge passes, future progress reports should
   say “seven candidate row exclusions, zero frozen-certified exclusions,”
   not “7/14 closed.”

## 5. Integrity and disclosure

The three principal frozen hashes were rechecked and still equal:

```text
41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d  FROZEN_TAXONOMY_v1.md
5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23  frozen_manifest_v1.json
750ca4e23757c697c894166b0a7d02e12464680dc9ba3cffc81b4ff3138a1042  verify_frozen_manifest_v1.py
```

This audit was produced with substantial AI assistance.  It is not peer
review.  Exact checks are evidence about encoded algebra; they do not prove
the geometric completeness of a case split.
