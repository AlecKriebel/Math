# Theorem-to-certificate crosswalk

Status: **CANDIDATE PENDING FINAL WHOLE-PROOF REFEREE**

This is the active evidence map for Outcome P.  Historical artifacts are not
theorem inputs unless named here.  Counts below are deterministic checksums of
structurally proved finite universes, never substitutes for exhaustiveness
proofs.

| Theorem node | Mathematical role | Primary proof | Independent evidence | Exact replay |
|---|---|---|---|---|
| `D` | Locked `sd_0`, LSA rootings, `W_TC/S_TC`, no-omnian criterion | `docs/DEFINITIONS_LOCK.md` | `reviews/final_standard_convention/` | `bash reviews/final_standard_convention/verify_all.sh` |
| `U` | Cycle/four-theta primitive cores, repairs, rigid supports, automatic unique triangle | `docs/GENERATOR_AND_SUPPORT_THEOREM.md` | convention census and `reviews/root_probe/` | `python3 reviews/root_probe/verify_all.py` |
| `Q` | Root factor to independently chosen real incoming boundary | `docs/ROOT_REDUCTION_THEOREM.md` | `reviews/root_probe/REVIEW.md` | same root/probe replay |
| `C` | Pointwise cut iff flattening rank at most four; both cut inclusions | bridge/cut proof summarized in `docs/SHARP_BOUNDARY_THEOREM.md` | `reviews/global_bridge/` | `bash reviews/global_bridge/verify_all.sh --with-upstream-replay` |
| `B` | Exact full incidence-scaling bridge fiber, slices, no compensation | Section 4 of the theorem proof | `reviews/global_bridge/REVIEW.md` | same global bridge replay |
| `A3` | Complete three-outgoing directed local relation universe | theorem-derived primitive cores, repairs, supports, completions, and assignments | `reviews/n3_universe_generator/` independently regenerates the raw and merged universes; `reviews/bounded_directed_relation_cleanroom/` independently checks every decorated relation and algebraic label | `bash reviews/n3_universe_generator/verify.sh` and `bash reviews/bounded_directed_relation_cleanroom/verify_n3.sh` |
| `A4-filter` | Complete five-port theta-2 invariant filter and presentation binding | theorem-derived completion grammar | `reviews/theta2_signature_gate/` | `bash reviews/theta2_signature_gate/verify.sh` |
| `A4-cover` | All 132 five-port nonretaining roots terminate in separation/isomorphism | schema-3 hard-cover streams | `reviews/final_hard_cover_cleanroom/` and `reviews/final_hard_cover_adversary/` | `bash reviews/final_hard_cover_cleanroom/verify_schema3_n4_full.sh` |
| `S` | Marginal submersion, restoration direction, common anchor, coherent arbitrary words, ten-port bound | `docs/HARD_COVER_THEOREM.md` and `docs/GENERATOR_AND_SUPPORT_THEOREM.md` | `reviews/arbitrary_subdivision_promotion_referee/` and `reviews/compact_probe_format/` | `bash reviews/arbitrary_subdivision_promotion_referee/verify_all.sh` plus compact full replays |
| `T` | Ordinary triangle redirection has a common regular projective germ | `docs/TRIANGLE_MOVE_LOCK.md` | `reviews/triangle_redirection_cleanroom/` | `bash reviews/triangle_redirection_cleanroom/verify_all.sh` |
| `G` | Local-to-global necessity and simultaneous converse gluing | `docs/SHARP_BOUNDARY_THEOREM.md` | `reviews/global_bridge/` and `reviews/final_theorem_logic/` | bounded semantic replay in the global bridge package |
| `W` | All-`n` weak-but-not-strong sharpness pair | frozen `../s_tc_jc_sharp_boundary/source/paper/main.tex` | frozen independent verifier | `python3 ../s_tc_jc_sharp_boundary/reproducibility/verify_release.py` |
| `V_final` | Whole-proof adversarial attack | integrated theorem and manuscript | `reviews/final_outcome_p_referee/` | included in active quick gate after final verdict |

## Exact local checksums

- Three-outgoing gate: 10,826 raw and 10,466 canonical decorated directed
  relations; 5,284 strict; 5,120 pending canonical with 5,344 raw root
  coverages; 62 direct residuals, all isomorphism or ordinary `T`.
- Independent three-outgoing universe regeneration gives exactly the same raw
  and merged normalized multisets, with 10,106 singleton and 360 double
  canonical multiplicities; six relation-deletion, duplication, transport,
  orientation, and assignment mutations are rejected.
- Three-outgoing hard cover: 68,584 states, comprising 56,055 generic
  separations, 8,349 refinements, 4,036 strict separations, 120 isomorphism
  terminals, and 24 ordinary-`T` terminals.
- Theta-2 five-port gate: 6,138 completion records; three necessary equal
  signature pairs; 192 raw survivor presentations partitioned as 18 direct
  isomorphisms, 42 incoming-root duplicates, and 132 restoration roots.
- Theta-2 hard cover: 2,106 states, comprising 1,860 generic separations, 114
  refinements, and 132 isomorphism terminals.
- Common-anchor probes: 101,148 three-outgoing and 168,582 theta-2 relations;
  exact maximum ten tensor ports.

## Quarantined claims

The following are explicitly not ancestors of Outcome P:

- the reciprocal-only bridge chart;
- physical bridge-parameter recovery;
- Theta as a move inside `S_TC`;
- Omega and Omega-chain;
- `R_root`, `C_root`, `Psi`, and non-`T` portions of historical `R3`;
- schema-2 relation streams that merged rooted presentations;
- target-only counts 1,152 and 1,686;
- equality of complete stochastic images under `T`;
- pointwise realization of every `T` orientation at every generic
  distribution.

Preserved failed certificates and mutation-design failures are evidence of
the fail-closed process, not positive theorem inputs.
