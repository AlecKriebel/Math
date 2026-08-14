# Theorem-to-certificate crosswalk

Status: **VERIFIED — FINAL OUTCOME A**

The persistent archive is sealed in two layers: this core crosswalk and the
core artifact manifest are inside the archive, while
`release_artifacts/RELEASE_ENVELOPE.json` records the immutable source commit,
clean-clone transcript hashes, and final archive digest.

Manuscript: **Strong Tree-Childness Is a Sharp Identifiability Boundary for
Level-2 Jukes–Cantor Networks**

Counts below are deterministic checksums of theorem-derived finite universes,
not substitutes for their exhaustiveness proofs.

| Node | Mathematical role | Primary proof | Independent evidence and replay |
|---|---|---|---|
| `D` | Fixed `sd_0`, LSA rootings, `W_TC/S_TC`, no omnians | `docs/DEFINITIONS_LOCK.md` | `reviews/final_standard_convention/`; `bash reviews/final_standard_convention/verify_all.sh` |
| `U` | Cycle/four-theta cores, repairs, supports, unique triangle | `docs/GENERATOR_AND_SUPPORT_THEOREM.md` | `reviews/root_probe/`; `python reviews/root_probe/verify_active_structural.py` |
| `C` | Pointwise cut iff and both cut inclusions | `docs/SHARP_BOUNDARY_THEOREM.md` | `reviews/global_bridge/`; `bash reviews/global_bridge/verify_all.sh --with-upstream-replay` |
| `B` | Full incidence bridge fibre, slices, localization | manuscript bridge section | same independent global bridge replay |
| `A3` | Three-outgoing decorated relation universe | primitive completion grammar | `reviews/n3_universe_generator/` and `reviews/bounded_directed_relation_cleanroom/` |
| `A4` | Four-outgoing theta filter, transports, restoration cover | primitive completion grammar | `reviews/theta2_signature_gate/`, `reviews/final_hard_cover_cleanroom/`, and adversary |
| `S` | Submersion, restoration, common anchor, coherent words | `docs/HARD_COVER_THEOREM.md` | `reviews/compact_probe_clean_clone_gate/` and `reviews/direct_anchor_probe_closure/` |
| `T` | Ordinary triangle common strict regular germ | `docs/TRIANGLE_MOVE_LOCK.md` | `reviews/triangle_redirection_cleanroom/` |
| `G` | Global necessity and converse gluing | `docs/SHARP_BOUNDARY_THEOREM.md` | `reviews/global_bridge/` and `reviews/final_theorem_logic/` |
| `O` | Triangle-free Omega topology, equality, rank 9, all-`n` inverse | `omega_audit/reports/OMEGA_GATE_REPORT.md` | frozen-orbit import checked by `omega_audit/runtime_compat/verify_orbit_constant.py`; primary historical replay plus `omega_audit/independent/verify_omega_release.py` and `verify_omega_rank_readability.py`; adversarial O6 PASS |
| `W` | Triangle-containing Theta rank-8 family for all `n` | `s_tc_jc_sharp_boundary/source/paper/main.tex` | frozen independent verifier in `s_tc_jc_sharp_boundary/` |
| `V_final` | Whole-paper adversarial logic and release review | unified manuscript | active final referee packet and clean-clone transcripts |
| `V_hold` | Post-HOLD structural, cut, exposition, disclosure, and Figure 4 repairs | `reviews/post_hold_revision/REPORT.md` | revised clean replay, exact Omega rank certificate, two-renderer PDF audit, and immutable public tag |

## Exact local checksums

- Three-outgoing gate: 10,826 raw and 10,466 canonical decorated directed
  relations; 5,284 strict; 5,344 raw restoration roots; 62 direct residuals.
- Three-outgoing restoration forest: 68,584 states, ending in 120 labelled
  isomorphism and 24 ordinary-`T` terminals after exact separation.
- Four-outgoing gate: 6,138 completion records and 192 raw survivors,
  intrinsically partitioned as 18 direct isomorphisms, 42 incoming-rooting
  duplicates, and 132 restoration roots.
- Four-outgoing restoration forest: 2,106 states, with 1,860 generic
  separations, 114 refinements, and 132 isomorphism terminals.
- Coherent probes: 101,148 three-outgoing and 168,582 theta-2 relations;
  exact maximum ten tensor ports.
- Direct residuals: 2,642 one-port and 18,224 two-port relations, no unresolved
  relation, and 12/12 mutations rejected.
- Omega: four fixed rooted presentations; seven admissible rootings and two
  tree-child rootings per mixed graph; all 256 Fourier and 256 inverse-pattern
  entries; exact model/intersection dimension nine; readable core-rank
  determinant `-723/8589934592`; 12/12 mutations rejected.
- Theta: all 256 Fourier coordinates, strict quadratic point, two rank-eight
  minors, and positive analytic leaf-substitution inverse.

## Explicit exclusions

No active theorem uses a reciprocal-only bridge chart, a hidden cleanup-fibre
rooting convention, a weak-class gadget as a move in `S_TC`, a root-presentation
move as a distinct semi-directed topology, target-only counts, equality of
complete stochastic images under `T`, physical bridge-parameter recovery, or
K2P/K3P claims.
