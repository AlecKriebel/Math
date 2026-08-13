# Proof-dependency audit of the final two-linkage union

**Proof-first audit, 2026-08-12 PDT.**  The exact finite target is
`src/global_t3_2_final_union.py` at SHA-256

```text
7edccbf34c37f923c80662a852075d3426d1d94a08b9bdf8c59cbe509fdc674d
```

This audit does not enumerate orientations, reaction histories, or
populations.  The executable was used only to replay equality and
disjointness of finite support-pair sets.  Every stochastic conclusion below
is charged to an analytic theorem.

## 1. Verdict

**Finite union: PASS.**  The fourteen displayed branches are pairwise
disjoint and their union is the exact 2,511-pair post-interface residual,
whose fingerprint is

```text
0c57f530eb44a688520cc1706f830afa18063f4d08d24e5006f47a5666edd0b3
```

The frozen row and payload hashes are respectively

```text
9e9c6be443216f3a6d05795fcf0dcf25170ce020371c6bffde25eb316e52ad27
4a1542367400376de42fec24ddabe328bd3489c91c246e8d70def32bcd78cb33
```

**Analytic branch coverage: no branch is supported only by selector
arithmetic.**  Each branch has a later classwise arbitrary-strong-graph,
arbitrary-positive-rate theorem.  In particular, three claim-neutral or
withdrawn selector modules with false flags are superseded by later theorem
certificates; their pair sets agree exactly.

**Publication dependency chain: NOT YET A STRICT PASS.**  One current theorem
file is not the bytes targeted by its recorded independent audit, the
151-pair affine branch has no located independent audit, and several earlier
branches contain only an embedded audit attestation rather than a separately
frozen audit artifact.  Finally, the exact union has not itself been composed
with the pre-residual reductions in one repaired, independently audited
two-linkage theorem.  These are exact provenance/composition gaps; no new
analytic counterexample was found.

## 2. Branch map

Here “embedded” means that the theorem note itself records an independent
replay, but no separate full-scope audit artifact was located.  A pair
fingerprint certifies membership only, never recurrence.

| branch | pair set | analytic theorem, current SHA-256 | independent audit evidence, SHA-256 | dependency verdict |
|---|---:|---|---|---|
| `affine_stoichiometric_151` | 151; `55e243945f86d106b920a27e2249a20b7077b5dc718ec06918cca4368e4a6c96` | `stoichiometric_gate_feasibility.md`, `27b40b61903ae6c2e223d007ec08323ec9aec10e9198deb99d2d7c60d878d007` | none located | Theorem 2.1 plus Corollary 4.1 give the analytic fixed-class Foster result; independent-audit gate remains open. |
| `rank_two_14` | 14; `d169edd59dd5acbead528a02cb14e9fcc00cc6ff4fb0203e97139844226d07b6` | `rank_two_global_return_all14.md`, `2abe5e1266286a90853a952be71706329c7869277f9b64c3c07965919725a597` | embedded in Section 8; no separate full-return audit located | Unconditional theorem.  `two_active_rank_two_window_audit.md` at `f2b9a9196b0d6ca52d1c31d567fcfdffb364b7325ad089520a0cef7f3c027e38` is only a local Riccati-window audit and explicitly leaves the outer return open, so it is not the required full audit. |
| `all_active_only_51` | 51; `cc1d4b0941588f7b664a3266076789e548ae1f675924854eff18c9552d86e3ea` | `all_active_only_reversible_top.md`, `3f8c3662ed55d13133ef67f5e4e75e7ef9057075fa6e755faf33420e71ea0a26` | embedded in Section 5 | Unconditional pair theorem; separate pinned audit absent. |
| `rank_one_no_promotion_141` | 141; `bc3540674c5ec8eef96fe4272e15c1f3d220a06fe7ad890189d2f745e6c22e67` | `rank_one_no_promotion_pair_branch.md`, `adc325b740dd18bfa4cc9ee53c2a3632f3660df589369a14cc4d9c3ce16992c1` | embedded after Theorem 2.1 | Unconditional pair theorem; separate pinned audit absent. |
| `post_rank_one_one_active_92` | 92; `ef71d06b7ca9b9f1ef9049f37cb8047f96eb6e4def93c031302b65847edf5c8c` | `post_rank_one_one_active_repair.md`, `b4944d0bed95f92978a0eaf08336744813804ca7ddd6af0c4cd84005361c6113` | embedded in Sections 1 and 6 | Unconditional repair of the 92 pairs; separate pinned audit absent. |
| `two_active_promotion_36` | 36; `f2ad8cbe4b9ca7f36c39bed4bfe5aaafc6a9152eaf300390b5c25ba546519137` | `two_active_promotion_36_pair_theorem.md`, `2f52d0ed580c70916fbe75f13e8ea09d77af53940bdf21048b43423830620f97` | dormant 16-row audit `dormant_promotion_priority_macrochain_audit.md`, `d342db13f800a08a8f84a81bac86c92481876a010cca043ea7cdc0adca8a6dc8`; full-scope replays embedded in theorem | Unconditional theorem, but the separate artifact covers only the dormant subbranch; no separate full 36-pair audit was located. |
| `suppressed_promotion_4` | 4; `20aae4680ad31e03b96c2c633833d1d6612f902b136154dbc012537e4352e584` | `suppressed_promotion_orbit_full_proof.md`, `edbe0c4affe9735fb7cb650f9e0e3d653c75e7b37df5b5c8c8b838f43565a518` | `suppressed_promotion_orbit_independent_audit.md`, `4ff20ae0ba6443d14a25f4bed3337e5cacc880b0e42044d717a5644ce2b7b509` | PASS at the four-pair scope. |
| `critical_one_active_15` | 15; `6ec74f95e50e39ecda002b988d8233ae74c040ff9bb3518892dfd980bfad06d3` | `critical_one_active_q_trace.md`, `01a7827e96874171bc0f96be4fd05edb2a7ce607398be312b1378e762f62ea82` | embedded in Section 8 | Unconditional exact 15-pair theorem; separate pinned audit absent. |
| `universal_one_active_net_1212` | 1,212; `a7784a1f98da2fbadd70a62bc97fe852393cb410a24e666a6d6c246998f0f579` | `one_active_fourth_power_pair_composition.md`, current `0ab1cff97dee0594db9981db451a9f26799a6f2cdd5cf5d00a19f03e12c6ea9c` | `one_active_fourth_power_pair_composition_current_independent_audit.md`, `119918037899e9af543f321d3d019006abcbcf947b34c51b0af611c74b017db7` | STRICT PASS on current exact bytes.  The older SHA attestation embedded in the theorem/certificate is historical and was not inherited by the fresh audit. |
| `exact_common_w_26` | 26; `393474671be0bf095868e66cbcbf3164d941b99191517f172a41f157e20b21af` | `prospective_26_candidate_pair_theorem.md`, `c78e53f11aeb981b415a90a486583b409608ef2256b73b9e063db48ac8d4fc88` | embedded PASS; theorem certificate `src/prospective_26_candidate_theorem.py`, `45e42904072bb1cd451a98fdfd2750c0bb8ed442e028a9a1198193f1b91abff5` | Unconditional theorem supersedes the false flags in the claim-neutral selector.  Separate pinned audit absent. |
| `easy_common_w_416` | 416; `8c3325983568c53772f024080c0b95d37873cfe0a149386ec9829d1d9323e186` | `two_active_easy_943_common_w_theorem.md`, `4764849b05915b9005d68ac885c512a906af439430e8db8a7131f04645224e29` | `two_active_easy_416_independent_audit.md`, `c07f9d9d79574d1c590b03d552de574882c141c84f35fdf452508689e46743f6` | PASS at the exact 416-pair scope. |
| `rank_two_scalar_13` | 13; `f089ad4dbf064da8512d4854e824c36216e3eb74655ec435d06eecc69fb4f27e` | `rank_two_linear_switch_13_common_scalar.md`, `0be8e4e0bb28fa2086c434ee459b7d2f2ab061c67f9d45d2ecdb6a059a764478` | `rank_two_linear_switch_13_independent_audit.md`, `4946686c9c19703216662fa00044b6c80e0673e294ef1beb7ee0725233de9bd4` | PASS; later theorem/certificate supersede the false flag in the claim-neutral selector. |
| `rank_two_stopped_7` | 7; `93717536ce82eceefe6909c62568afab31e06695dada8b69defb93335d576957` | `rank_two_mixed_profile_7_stopped_service_theorem.md`, current `e8045791f98334d706e058adab0f838f4bf902a71b08bc1b24a4f3493474355b` | `rank_two_mixed_profile_7_stopped_service_independent_audit.md`, `6dc2bb7eb94b88f39e395c4a9afe5cb464d9e99df90b143d6326f5cbddc5838a`, pins theorem `9f8622ae324ac1ea099a75dca834bbacafadd353e311cb8d20bf35d299ca00a1` | Analytic theorem is unconditional, but exact-byte inheritance fails.  The current source is `2130fe04800e26911d470bdb20e2703f9c12834ef3c7d4bacd9ab96fc28f1fc5` with payload `0c06d14f1ad53c357d0c3ba0127e0c0ce3bac12db8c866523dedd3b5fb401eee`; the audit pins source `bee3003a034763efb2958ab1410a59d6bde258c1e5590925d9acdbf6baac1366` and payload `15920ec2ab510bab87b4e4b778cd998f7bbf7622b606bda383014dd5d6add2e3`.  Fresh audit is required. |
| `hard_common_w_333` | 333; `d3c9dad6e8510a81efee6c56873de0f1f2cf6f24d3f50b46d4cf22abb2ad9484` | `hard333_common_w_fixed_class_theorem.md`, `ddcc1f054febae9f08bb4d78bd66569ff4eebdd367b5cb4479b9029c960ecf84` | `hard333_final_composition_independent_audit.md`, `8bba33d321e7812a22b2422ca06c33d0abe2e4736c68e9c11be037d8a8819fd6` | STRICT PASS on exact bytes.  The theorem's introductory “candidate” sentence is stale and is superseded by this exact hostile audit. |

## 3. False and stale flags

The three imported false-flag modules are safe only as selectors:

1. `prospective_no_promotion_26.py` says its analytic flags are false, but
   its 26-pair set is exactly the set certified by
   `prospective_26_candidate_theorem.py`.
2. `rank_two_linear_switch_13.py` says common-potential closure is false,
   but its 13-pair set is exactly the set certified by
   `rank_two_linear_switch_13_common_scalar.py` and the independent audit
   above.
3. `two_active_dormant_407_certificate.py` retains withdrawn candidate
   claims and false pair-recurrence flags, but its 333-pair set is exactly
   the set in `hard333_final_descriptor_coverage.py` covered by the frozen
   strict hard-333 theorem and audit.

Thus none of these booleans is an analytic premise.  The finite union uses
only the selected pair sets.  Conversely, it would be invalid to promote the
global theorem merely by changing those booleans: the superseding theorem
and audit hashes must be cited explicitly.

The three booleans in `global_t3_2_final_union.py` itself remain false:

```text
hard333_pair_recurrence_input_certified = false
global_t3_2_theorem_independently_audited = false
global_t3_2_certified = false
```

The first is now stale relative to the strict hard-333 audit.  The latter two
remain correct release-status statements because the union is only a set
identity and no repaired global theorem has yet been independently replayed.

## 4. Exact global composition gap

The existing skeleton
`proof_first_global_t3_2_classwise_composition.md` is frozen at

```text
37a8a395797dabb86659d877020c137554f1bb0b6c7b5f97bdd57a0d563e1edf
```

and its scoped audit
`proof_first_global_t3_2_classwise_skeleton_scoped_audit.md` is at

```text
3d45867b4dd07a92ce43054767b7e7a680fa77035b7f2e1021dcb5004097f962
```

That audit gives a strict conditional gluing lemma but explicitly does not
audit two-linkage coverage, and the skeleton itself still lists the hard
family and the single-linkage carrier as pending.  It is therefore stale as
a final composition target.

The required repair is finite and conceptual, not a new search:

1. freeze or freshly audit the current seven-pair theorem bytes;
2. separately audit the 151-pair affine theorem, and preserve or create
   byte-pinned full-scope audit records for the embedded-audit branches;
3. write one fixed-class two-linkage theorem which cites the pre-residual
   invariant/deficiency-zero/exact-seam/tier reductions, the exact 2,511-set
   identity, and the fourteen analytic branch theorems;
4. apply the repaired common-potential Foster lemma pairwise, without
   attempting to select one potential across different support pairs; and
5. independently replay that exact composition target.

Subject to those audit/provenance repairs, this dependency audit found no
unfilled analytic branch in the two-linkage residual and no need for an
orientation or population search.
