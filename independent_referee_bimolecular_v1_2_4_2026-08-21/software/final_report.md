# Final independent software and artifact referee report

**Manuscript:** *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*  
**Packet:** `bimolecular_positive_recurrence_ai_referee_packet_v1_2_4`  
**Report timestamp:** 2026-08-21T22:51:19-07:00 (America/Los_Angeles)  
**Scope:** complete static inspection, canonical execution, independent finite
oracles, fail-closed mutation testing, artifact consistency, and post-barrier
comparison with author records

## 1. Software-track conclusion

The supplied standalone packet is internally reproducible. Its exact runner
completed with exit status 0: all 57 verifier tests and all four release-tool
safety tests passed, no test was skipped, two regenerated canonical reports
were byte-identical to the committed report, all three report copies agreed,
the 82-entry durable-tree manifests agreed, all four PDFs rebuilt
byte-for-byte, and the 84-member ZIP rebuilt byte-for-byte. Independent
production-free oracles found no discrepancy in the finite mathematical
interfaces they tested. All requested content, source, golden, PDF, and archive
mutations failed closed at an appropriate layer.

There is, however, a **major release-provenance defect** separate from the
standalone packet checks. The manuscript claims an available v1.2.4 Git tag,
but that tag is absent both from the containing checkout and the public remote.
Moreover, `validation/replay_release.sh` only prints an exact tag (or “none”)
and never requires the expected tag. In a disposable clean Git repository with
no tag, that script printed `Exact tag: none`, completed every check, exited 0,
and printed `PASS: complete Version 1.2.4 release replay`. This contradicts the
packet README's statement that the Git replay has an exact-tag assertion.

Thus the computational claims are supported as **content verification**, but
the claimed v1.2.4 Git-tag provenance is not established. This defect does not
invalidate the mathematical theorem; it requires a release/provenance
correction.

## 2. Environment and immutable inputs

- Packet root:
  `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4`
- Submission root:
  `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4`
- OS: macOS 26.5.2 build 25F84; Darwin 25.5.0 arm64.
- Python: CPython 3.14.6.
- Tectonic: 0.16.9.
- The packet itself has no `.git` directory.
- Journal PDF SHA-256:
  `77b4f098a1f0655ed4e04423caccec79a051cf11297b17d5fa2d630d539e7c4d`.
- `paper_content.tex` SHA-256:
  `00c0d9f2b281d6f36a388ff45776d9f90f9d6388dce0e83d9eb7b6aa80a4deba`.
- `references.bib` SHA-256:
  `00bd5723e1c518841e94e8bd02637c709b0295891f191ed65dffbcc10a034e61`.
- `RUN_ALL_CHECKS.sh` SHA-256:
  `579383c84cae29c0b2c62e41bbbb0254dfa1cd0b5e3e968f6e85899c5bb4944e`.
- `code/reproduce.sh` SHA-256:
  `4dd4055c2e6d15e498589a0822a692d052c9f4468704ab7b00609b7118467fac`.

The complete static file inventory and its hashes are in
`software/preliminary_report.md`. No packet file was altered by mutation
testing; every mutation was made in a `mktemp` copy and removed afterward.
Post-test hashes of the canonical report, journal PDF, and ZIP still equalled
the canonical values below.

## 3. Canonical replay

### Command

From the packet root I ran exactly:

```bash
./RUN_ALL_CHECKS.sh
```

Tool wall time was 26.556 seconds and the command exited 0.

### Outcomes

| Stage | Independent observation |
|---|---|
| Packet integrity | Passed; 89 files covered, excluding the packet checksum file itself. |
| Verifier tests | 57 run in 6.920 seconds; 57 passed; 0 failed; 0 errored; 0 skipped. |
| Canonical generation | Two fresh reports had SHA-256 `dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586` and matched the committed report byte-for-byte. |
| Release-tool tests | Four run in 0.003 seconds; four passed; 0 failed; 0 errored; 0 skipped. |
| Durable manifest | Passed; 82 entries. Both copies are byte-identical with SHA-256 `e8562cfb54fd411e4c1926bd2e15cf394a1ece014def06d3621e12a0fcce5caf`. |
| Report copies | `code/verification_report.json`, `supplement/verification_report.json`, and `validation/VERIFICATION_REPORT.json` are byte-identical. |
| PDF rebuild | All four Tectonic 0.16.9 rebuilds matched the supplied bytes. |
| Release archive | Fresh 84-member stored ZIP matched the supplied ZIP byte-for-byte. |
| Skipped or unavailable steps | None. |

### Canonical hashes reported

- Canonical verification report:
  `dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586`
- Durable manifest:
  `e8562cfb54fd411e4c1926bd2e15cf394a1ece014def06d3621e12a0fcce5caf`
- `main_arxiv.pdf`:
  `e68130c3c38024a1e88b47cfa2cf06b8ebbead46665e82903d5bc6f2ff61bbe9`
- `main_biorxiv.pdf`:
  `78373226d868c7067c172e329e63535bc5ff5ee317fbdb8eeb8eaede7be0a371`
- `main_jap.pdf`:
  `77b4f098a1f0655ed4e04423caccec79a051cf11297b17d5fa2d630d539e7c4d`
- `supplementary_note.pdf`:
  `85223b8099fc179b368e372be4e9fa1bda7d4e754421d8d10e78d436d977aa9e`
- Release ZIP:
  `66e1f89f97840650f400ae917ccb76ce5f08a9291a3a7692fe7bf2222d8af54f`
- Pinned Tectonic bundle digest printed by the build:
  `6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`.

The complete verbatim command output is retained in Appendix A.

## 4. Canonical report contents

After the first replay completed, I opened the committed report. It records:

- 3,318 exact factorial-identity cases;
- 172 exact entropy-signature cases;
- 36 scalar branch/monotonicity cases;
- 58 lifted-edge witnesses, eight finite population states, and 26 finite
  reachability pairs;
- 24 exact ACK example checks;
- a 98,261-case three-species top atlas over 1,013 nontrivial complex subsets,
  55 normalized rational weights, and 97 weight/divergent-set pairs; and
- 5,000 fixed-seed four-species stress cases.

The three-species cases split as 1,423 all-top invariants, 2,436 service
availabilities, 288 signed invariants, 86,373 two-divergent availabilities, and
7,741 unary-top availabilities. The seeded four-species cases split as 87, 34,
21, 4,640, and 218 respectively. Every listed calibration is `true`.

The report accurately classifies the four-species run as a seeded stress test
not used as proof. It also accurately describes the scalar check as branch
conditions and pointwise monotonicity, rather than the complete analytic
limiting lemma. The universal theorem remains a manuscript proof obligation.

## 5. Independent production-free oracles

Each oracle was a fresh standard-library program which asserted before and
after execution that `bimolecular_pr` was absent from `sys.modules`. None called
the verifier or any production mathematical helper.

| Oracle | Scope | Result |
|---|---|---|
| Residual factorial identity | Dimensions 1–4; all binary complexes; finite state boxes; every enabled carried target and source; every binary outcome | 528,810 exact `Fraction` comparisons; 0 failures. |
| Entropy rewrite | Dimensions 1–3; independently aggregated rational source rates including parallel additions; exact prime-factor log signatures | 1,153 cases; 0 failures. |
| Lifted return paths | 400 independently generated strongly connected complex graphs, seed 314159; boundary-enabled random states | 40,537 lifted edge witnesses; 0 missing return paths or residual/closure failures. |
| Three-species top alternative | Every one of the verifier's 98,261 subset/weight/divergent-set inputs, but with an independent brute-force search for any valid availability pair, all-top invariant, or signed invariant | 0 failures. Independent aggregate counts were 96,550 availability, 1,423 nonnegative invariant, and 288 signed invariant, exactly matching the production aggregate. |
| Four-species top alternative | 20,000 separately seeded cases, seed 20260821, not the production seed or generator range | 0 failures: 19,804 availability, 155 nonnegative invariant, 41 signed invariant. |
| Rate-degeneration episode | Direct source-propensity/event enumeration versus a separately coded closed form; 100 rational rate vectors, `m=2..30`, seed 8675309 | 2,900 exact signature comparisons; 0 failures. |
| ACK marked episode | Direct source-propensity/event enumeration versus separately coded manuscript coefficients; same 100 rational rate vectors, `n=2..30` | 2,900 exact signature comparisons; 0 failures. |
| Directed stationary cycles | Lengths 2–8, 100 independent rational rate vectors per length | 700 exact normalization/flux checks; 0 failures. |
| Scalar maximizer branch | Independent rational grid across 187 positive `q` values and 201 `M` values | 37,587 exact derivative/domain checks; 0 failures. |

These oracles materially strengthen finite falsification evidence. They do not
establish compactification, finiteness/nonemptiness of `K`, stopped-process
integrability, trace-chain return, CTMC nonexplosion, or universal positive
recurrence.

## 6. Fail-closed mutation results

Every mutation below used a fresh disposable copy outside the packet.

| Mutation | Check invoked | Observed result |
|---|---|---|
| Changed committed canonical JSON from status `pass` to `fail` | `code/reproduce.sh` | Exit 1 after all 57 tests and two fresh reports passed; exact error: regenerated JSON differs from `verification_report.json`; golden was not overwritten. |
| Added unlisted `src/bimolecular_pr/injected_probe.py` | Full report generation | Exit 1 with `source allowlist mismatch; ... unexpected=['src/bimolecular_pr/injected_probe.py']`. |
| Reversed the numerator logic in `exp_potential_increment` | Full 57-test suite | Exit 1; two residual-identity tests and the frozen-wheel digest test failed. |
| Changed one durable byte sequence in `code/README.md` | Durable manifest verifier | Exit 1; `CHANGED: code/README.md`. |
| Added unlisted non-Python `src/bimolecular_pr/injected_probe.dat` | Inner source hash then outer manifest | Inner 22-file source allowlist accepted it, as statically predicted; outer durable manifest exited 1 with `UNEXPECTED`. This confirms the intended layered boundary. |
| Altered the journal TeX title and rebuilt | Tectonic builder plus supplied/rebuilt comparison | Rebuild succeeded but `cmp` exited 1. Supplied journal PDF hash remained `77b4...c4d`; altered rebuild was `2c1bd470...c454`. |
| Flipped one byte of the supplied journal PDF in a full packet copy | Exact standalone packet runner | Exit 1 at stage 1 with `packet checksum mismatch: .../manuscript/main_jap.pdf`. |
| Flipped one byte of the supplied ZIP | Archive `--check` | Exit 1 with `ValueError: rebuilt archive differs from the committed archive`; mutated hash `8aa4a377...53be8` versus canonical `66e1f89f...f54f`. |
| Put the exact package and archive in a clean Git repository with no tag | `validation/replay_release.sh` | **Exit 0.** It printed `Exact tag: none`, ran all checks, and printed `PASS: complete Version 1.2.4 release replay`. This is a fail-open provenance defect, not a successful negative test. |

## 7. Artifact consistency and coverage

The source-to-artifact chain is internally consistent:

1. Tectonic rebuilt all four PDFs from the supplied TeX/bibliography inputs and
   obtained the supplied bytes. This establishes PDF/source consistency for the
   pinned build route.
2. The two 82-line manifest copies are byte-identical and the verifier walked
   the durable tree, detecting no missing, changed, unexpected, or symlinked
   durable file.
3. The manifest categories contain: six `audit`, 24 `code`, 11 `manuscript`, 12
   `preservation`, nine `submission`, nine `supplement`, four `validation`, and
   six root-level files. The two manifest copies are intentionally excluded
   from their own 82-entry contents.
4. The deterministic archive contains those 82 files plus both manifest copies,
   for 84 canonical members.
5. The packet checksum covers the 84 package files, four packet-root handoff
   files, and the adjacent ZIP: 89 files total, excluding its own checksum list.
6. All three canonical report copies are byte-identical.

The report's limitations agree with the manuscript: computation does not prove
recurrence or enumerate the analytic `K`. The package version `1.2.0` within
outer release 1.2.4 is explicitly explained post-barrier as an unchanged
verifier component (`validation/REPRODUCTION_RECORD.md:3-5`), so this is not a
version mismatch.

## 8. Findings, severity-ranked

### Major SW-1 — The claimed public v1.2.4 tag is unavailable

**Locations:** journal PDF p. 14; `paper_content.tex:1139-1145`;
`validation/GIT_TAG_AND_COMMIT.txt:1-20`;
`validation/REPRODUCTION_RECORD.md:1-22`.  
**Evidence:** the copied packet has no Git metadata; the containing checkout has
no v1.2.4 tag; a direct public-remote query for
`refs/tags/bimolecular-positive-recurrence-v1.2.4` returned no ref.  
**Effect:** local bytes are reproducible, but the present-tense statement that
they are available in a tagged repository directory and the tag-based commit
provenance are not verifiable.  
**Repair:** publish an annotated v1.2.4 tag resolving to the exact released tree
and verify its peeled commit from a fresh clone, or change the manuscript and
records to describe an untagged standalone candidate.

### Major SW-2 — The Git release replay does not assert the expected tag

**Locations:** `validation/replay_release.sh:12-18,49-56`; packet
`README.md:52-54`.  
**Evidence:** the script's `if` branch prints the result of `git describe
--exact-match`; its `else` prints `Exact tag: none` and continues. It never
compares a discovered tag to `bimolecular-positive-recurrence-v1.2.4`. A clean
no-tag disposable repository completed the script with exit 0 and final PASS.  
**Effect:** the script verifies content and cleanliness but cannot establish
that it is running at the claimed release tag. The packet README incorrectly
calls this an exact-tag assertion.  
**Repair:** require both successful exact-match resolution and exact equality to
the expected tag before any replay work, for example by terminating on missing
or wrong tag; add tests for no tag and wrong tag; correct the README until this
is implemented.

### Minor SW-3 — An all-self-channel network is outside the reduction helper

**Locations:** manuscript `paper_content.tex:285-305`;
`code/src/bimolecular_pr/network.py:50-53,82-92`;
`code/tests/test_network.py:58-68`.  
`combined_parallel()` removes self-channels and then requires at least one
remaining channel. The test covers a self-channel only alongside genuine
birth/death channels. This is an auxiliary data-model edge, not a theorem
counterexample. Document the bypass-to-absorbing behavior or permit an empty
reduced network and test it.

### Minor SW-4 — Scalar and zero-length episode checks cover narrower interfaces

**Locations:** manuscript `paper_content.tex:520-616`;
`episode_bounds.py:13-68`; `verification.py:241-271,729-730`.  
The scalar code checks the branch maximizer and pointwise monotonicity but not
the two exact `F_q` values, branch continuity, or limit to minus infinity. The
zero-length check is only an empty product equal to one, not the required final
ordinary jump. The canonical report phrases the scalar scope accurately, but
these checks should not be cited as validation of the complete analytic
lemmas.

### Note SW-5 — The inner source allowlist and outer manifest have different scope

An unlisted `.py` file fails the inner report; an unlisted non-Python file does
not. The outer manifest rejects either durable addition. This is consistent
with `code/README.md:63-66`, which promises inner rejection only for unlisted
Python source/test files. No correction is necessary if the layered model stays
explicit.

### Note SW-6 — Most probabilistic proof obligations remain analytic

The code does not implement augmented-class irreducibility/projection,
properness, the general episode stopping construction, compactification,
finiteness/nonemptiness of `K`, optional-stopping integrability, trace-chain
conversion, general nonexplosion, or the regenerative CTMC theorem. The
manuscript and README explicitly acknowledge this boundary. Passing tests are
not a mathematical validity conclusion.

## 9. Comparison with author-generated audits and records

### Agreements

- The Version 1.2.4 editorial audit's stated 57+4 tests, 82-entry manifests,
  four deterministic PDFs, and 84-member archive were independently reproduced
  (`audit/publication_v1_2_4_editorial_audit.md:52-60`).
- The submission audit and expert note correctly describe the finite checks as
  falsification aids rather than proof
  (`audit/publication_v1_2_submission_audit.md:35-41`;
  `expert_audit_note.md:221-227`).
- The reviewer checklist accurately lists analytic interfaces not supplied by
  the finite verifier, including the scalar limit, compactification, `K`,
  Foster integrability, trace conversion, and CTMC occupation.
- The reproduction record's report-copy, manifest, PDF, archive, and supported
  version descriptions agree with the observed content replay.

### Omissions and disagreements

- None of the supplied audits identifies that `validation/replay_release.sh`
  accepts `Exact tag: none` and still passes.
- Packet `README.md:52-54` says the Git replay has an exact-tag assertion; this
  is false.
- The validation records name a canonical v1.2.4 tag and give commands that
  assume it exists, but the public ref is absent at this checkpoint.
- Existing audit summaries do not distinguish the scalar maximizer checks from
  the unimplemented value/limit parts as sharply as this report, nor do they
  mention the all-self-channel reduction boundary.

### Circularity assessment

The committed canonical reports, fixed digests, validation summaries, and
author audit statements are mutually consistent but author-generated. A golden
comparison proves that a run reproduces the chosen golden bytes; it cannot by
itself prove that the golden mathematical answers are correct. The independent
oracles above reduce this circularity for the finite factorial, entropy,
state-cycle, top-complex, episode, scalar, and stationary-cycle interfaces. No
finite computation removes the need for independent proof review of the
universal theorem.

## 10. Final software recommendation and residual uncertainty

**Software/computation assessment:** the advertised finite checks and artifact
rebuilds are valid and reproducible on the tested environment. I found no
discrepancy between regenerated mathematical-check counts and the committed
canonical report, and the mutation behavior is substantially fail closed.

**Required revision:** repair Git-tag availability and make the Git replay
enforce the exact expected tag. Until then, describe the packet as standalone
content verification, not verified v1.2.4 tag provenance.

**Residual uncertainty:** only CPython 3.14.6 was independently run in this
environment; the claimed 3.11–3.13 matrix and hosted CI artifacts were not
replayed. The Tectonic build printed the configured bundle digest but the shell
script does not itself hash the downloaded/cached bundle. These do not affect
the successful byte comparisons observed here.

**Completion estimate:** 100% of the assigned software/artifact audit. This is
a software-track conclusion only and does not choose the manuscript's final
mathematical status or journal recommendation.

## Appendix A. Complete output of the canonical packet replay

```text
AI REFEREE PACKET REPLAY
Python: Python 3.14.6
Tectonic: Tectonic 0.16.9
Platform: Darwin 25.5.0 arm64

[1/7] Packet-level file integrity
packet checksum verification passed: 89 files

[2/7] Mathematical verifier, 57 tests, and repeated canonical report
test_coordinate_face_is_closed_under_reachable_transitions (test_boundary_lattice.BoundaryLatticeTests.test_coordinate_face_is_closed_under_reachable_transitions) ... ok
test_parity_restricted_path (test_boundary_lattice.BoundaryLatticeTests.test_parity_restricted_path) ... ok
test_singleton_absorbing_class_is_separate (test_boundary_lattice.BoundaryLatticeTests.test_singleton_absorbing_class_is_separate) ... ok
test_two_state_finite_irreducible_class (test_boundary_lattice.BoundaryLatticeTests.test_two_state_finite_irreducible_class) ... ok
test_entropy_identity_aggregates_parallel_source_rates (test_episode.EpisodeTests.test_entropy_identity_aggregates_parallel_source_rates) ... ok
test_exact_entropy_identity_with_zero_source (test_episode.EpisodeTests.test_exact_entropy_identity_with_zero_source) ... ok
test_invalid_episode_probability_is_rejected (test_episode.EpisodeTests.test_invalid_episode_probability_is_rejected) ... ok
test_scalar_envelope_all_branches_and_boundary (test_episode.EpisodeTests.test_scalar_envelope_all_branches_and_boundary) ... ok
test_scalar_envelope_is_pointwise_nondecreasing_in_M (test_episode.EpisodeTests.test_scalar_envelope_is_pointwise_nondecreasing_in_M) ... ok
test_target_following_path_probability (test_episode.EpisodeTests.test_target_following_path_probability) ... ok
test_zero_length_path_probability (test_episode.EpisodeTests.test_zero_length_path_probability) ... ok
test_disabled_falling_factorial_and_successor (test_network.NetworkTests.test_disabled_falling_factorial_and_successor) ... ok
test_mark_actual_channel_not_displacement (test_network.NetworkTests.test_mark_actual_channel_not_displacement) ... ok
test_null_self_channel_is_removed_on_combination (test_network.NetworkTests.test_null_self_channel_is_removed_on_combination) ... ok
test_parallel_and_same_displacement_channels (test_network.NetworkTests.test_parallel_and_same_displacement_channels) ... ok
test_residual_identity_for_distinct_outcome (test_network.NetworkTests.test_residual_identity_for_distinct_outcome) ... ok
test_residual_identity_with_zero_carried_target (test_network.NetworkTests.test_residual_identity_with_zero_carried_target) ... ok
test_strong_connectivity (test_network.NetworkTests.test_strong_connectivity) ... ok
test_target_following_cycle_has_zero_increment (test_network.NetworkTests.test_target_following_cycle_has_zero_increment) ... ok
test_zero_pure_binary_and_mixed_falling_factorials (test_network.NetworkTests.test_zero_pure_binary_and_mixed_falling_factorials) ... ok
test_absorbing_singleton_has_point_mass_stationary_law (test_publication_v1.PublicationV1CalibrationTests.test_absorbing_singleton_has_point_mass_stationary_law) ... ok
test_rate_degeneration_asymptotic_coefficient (test_publication_v1.PublicationV1CalibrationTests.test_rate_degeneration_asymptotic_coefficient) ... ok
test_rate_degeneration_exact_finite_recursion (test_publication_v1.PublicationV1CalibrationTests.test_rate_degeneration_exact_finite_recursion) ... ok
test_stopped_random_time_foster_increment (test_publication_v1.PublicationV1CalibrationTests.test_stopped_random_time_foster_increment) ... ok
test_two_state_return_cycle_occupation_is_stationary (test_publication_v1.PublicationV1CalibrationTests.test_two_state_return_cycle_occupation_is_stationary) ... ok
test_ack_carried_target_A_is_explicitly_reachable (test_publication_v1_1.PublicationV11AlgebraTests.test_ack_carried_target_A_is_explicitly_reachable) ... ok
test_ack_complete_episode_formula_matches_generic_factorial_identity (test_publication_v1_1.PublicationV11AlgebraTests.test_ack_complete_episode_formula_matches_generic_factorial_identity) ... ok
test_ack_episode_has_strict_negative_logarithmic_coefficient (test_publication_v1_1.PublicationV11AlgebraTests.test_ack_episode_has_strict_negative_logarithmic_coefficient) ... ok
test_ack_example_unshifted_drift (test_publication_v1_1.PublicationV11AlgebraTests.test_ack_example_unshifted_drift) ... ok
test_corrected_fixed_m_rate_limit_is_a_times_one_plus_p (test_publication_v1_1.PublicationV11AlgebraTests.test_corrected_fixed_m_rate_limit_is_a_times_one_plus_p) ... ok
test_rate_example_log_coefficient_is_exact (test_publication_v1_1.PublicationV11AlgebraTests.test_rate_example_log_coefficient_is_exact) ... ok
test_scalar_envelope_monotonicity_on_exact_grid (test_publication_v1_1.PublicationV11AlgebraTests.test_scalar_envelope_monotonicity_on_exact_grid) ... ok
test_three_state_stationary_return_cycle_normalization (test_publication_v1_1.PublicationV11AlgebraTests.test_three_state_stationary_return_cycle_normalization) ... ok
test_absorbing_singleton_is_closed_reachability_class (test_publication_v1_1.PublicationV11StateCycleTests.test_absorbing_singleton_is_closed_reachability_class) ... ok
test_finite_reachability_is_symmetric_with_boundary_and_parity_classes (test_publication_v1_1.PublicationV11StateCycleTests.test_finite_reachability_is_symmetric_with_boundary_and_parity_classes) ... ok
test_lifted_cycles_allow_multiple_linkages_parallel_channels_and_same_displacement (test_publication_v1_1.PublicationV11StateCycleTests.test_lifted_cycles_allow_multiple_linkages_parallel_channels_and_same_displacement) ... ok
test_lifted_return_cycle_handles_zero_complex_and_boundary (test_publication_v1_1.PublicationV11StateCycleTests.test_lifted_return_cycle_handles_zero_complex_and_boundary) ... ok
test_all_qJ_one_is_already_the_all_top_case (test_top_complex.TopComplexTests.test_all_qJ_one_is_already_the_all_top_case) ... ok
test_all_top_nonnegative_invariant (test_top_complex.TopComplexTests.test_all_top_nonnegative_invariant) ... ok
test_service_availability (test_top_complex.TopComplexTests.test_service_availability) ... ok
test_shared_service_species (test_top_complex.TopComplexTests.test_shared_service_species) ... ok
test_slower_divergent_weight_zero_is_retained (test_top_complex.TopComplexTests.test_slower_divergent_weight_zero_is_retained) ... ok
test_species_absent_from_complexes (test_top_complex.TopComplexTests.test_species_absent_from_complexes) ... ok
test_two_divergent_particles (test_top_complex.TopComplexTests.test_two_divergent_particles) ... ok
test_unary_top (test_top_complex.TopComplexTests.test_unary_top) ... ok
test_validator_rejects_constant_invariant_with_wrong_divergent_sign (test_top_complex.TopComplexTests.test_validator_rejects_constant_invariant_with_wrong_divergent_sign) ... ok
test_validator_rejects_false_availability_witness (test_top_complex.TopComplexTests.test_validator_rejects_false_availability_witness) ... ok
test_validator_rejects_false_invariant (test_top_complex.TopComplexTests.test_validator_rejects_false_invariant) ... ok
test_validator_rejects_removed_redundant_case (test_top_complex.TopComplexTests.test_validator_rejects_removed_redundant_case) ... ok
test_validator_rejects_weight_support_outside_divergent_set (test_top_complex.TopComplexTests.test_validator_rejects_weight_support_outside_divergent_set) ... ok
test_zero_weight_divergent_species_still_counts_for_availability (test_top_complex.TopComplexTests.test_zero_weight_divergent_species_still_counts_for_availability) ... ok
test_built_wheel_carries_the_mit_license (test_verification.VerificationTests.test_built_wheel_carries_the_mit_license) ... ok
test_canonical_json_is_independent_of_mapping_insertion_order (test_verification.VerificationTests.test_canonical_json_is_independent_of_mapping_insertion_order) ... ok
test_entropy_verifier_executes_substantive_cases (test_verification.VerificationTests.test_entropy_verifier_executes_substantive_cases) ... ok
test_exhaustive_three_species_atlas_matches_fixed_result (test_verification.VerificationTests.test_exhaustive_three_species_atlas_matches_fixed_result) ... ok
test_seeded_random_stress_matches_fixed_result (test_verification.VerificationTests.test_seeded_random_stress_matches_fixed_result) ... ok
test_source_hashes_use_closed_allowlist (test_verification.VerificationTests.test_source_hashes_use_closed_allowlist) ... ok

----------------------------------------------------------------------
Ran 57 tests in 6.920s

OK
{"python": "3.14.6", "sha256": "dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586", "status": "pass"}
{"python": "3.14.6", "sha256": "dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586", "status": "pass"}
verification_report.json sha256: dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586
environment (not part of the canonical report): CPython 3.14.6 on macOS-26.5.2-arm64-arm-64bit-Mach-O
PASS: tests, repeated generation, and committed golden comparison all agree.

[3/7] Release-tool safety tests
test_archive_parser_rejects_windows_separator (supplement.test_release_tools.ReleaseToolSafetyTests.test_archive_parser_rejects_windows_separator) ... ok
test_manifest_parser_rejects_windows_separator (supplement.test_release_tools.ReleaseToolSafetyTests.test_manifest_parser_rejects_windows_separator) ... ok
test_manifest_walk_ignores_virtual_environment_symlinks (supplement.test_release_tools.ReleaseToolSafetyTests.test_manifest_walk_ignores_virtual_environment_symlinks) ... ok
test_manifest_walk_rejects_broken_symlink (supplement.test_release_tools.ReleaseToolSafetyTests.test_manifest_walk_rejects_broken_symlink) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.003s

OK

[4/7] Complete release manifests and report copies
manifest verification passed: 82 files

[5/7] Four deterministic PDF rebuilds
Building canonical PDFs with Tectonic 0.16.9
Tectonic bundle digest: 6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c
note: reading from standard input; outputs will appear under the base name "texput"
note: Running TeX ...
note: Running BibTeX on texput.aux ...
note: Rerunning TeX because bibtex was run ...
note: Rerunning TeX because "texput.aux" changed ...
note: Rerunning TeX because "texput.aux" changed ...
note: Running xdvipdfmx ...
note: Writing `/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T//bimolecular-tex.PeuP0R/main_arxiv/texput.pdf` (153.765625 KiB)
note: Skipped writing 3 intermediate files (use --keep-intermediates to keep them)
note: reading from standard input; outputs will appear under the base name "texput"
note: Running TeX ...
note: Running BibTeX on texput.aux ...
note: Rerunning TeX because bibtex was run ...
note: Rerunning TeX because "texput.aux" changed ...
note: Rerunning TeX because "texput.aux" changed ...
note: Running xdvipdfmx ...
note: Writing `/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T//bimolecular-tex.PeuP0R/main_biorxiv/texput.pdf` (153.7998046875 KiB)
note: Skipped writing 3 intermediate files (use --keep-intermediates to keep them)
note: reading from standard input; outputs will appear under the base name "texput"
note: Running TeX ...
note: Running BibTeX on texput.aux ...
note: Rerunning TeX because bibtex was run ...
note: Rerunning TeX because "texput.aux" changed ...
note: Rerunning TeX because "texput.aux" changed ...
note: Running xdvipdfmx ...
note: Writing `/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T//bimolecular-tex.PeuP0R/main_jap/texput.pdf` (152.67578125 KiB)
note: Skipped writing 3 intermediate files (use --keep-intermediates to keep them)
note: reading from standard input; outputs will appear under the base name "texput"
note: Running TeX ...
note: Rerunning TeX because "texput.aux" changed ...
note: Running xdvipdfmx ...
note: Writing `/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T//bimolecular-tex.PeuP0R/supplementary_note/texput.pdf` (37.1875 KiB)
note: Skipped writing 2 intermediate files (use --keep-intermediates to keep them)

[6/7] Deterministic release archive
manifest verification passed: 82 files
wrote 84 files to /var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T/bimolecular-v124-archive-q_rd4v82/bimolecular_positive_recurrence_submission_v1_2_4.zip
archive sha256: 66e1f89f97840650f400ae917ccb76ce5f08a9291a3a7692fe7bf2222d8af54f
archive verification passed: 66e1f89f97840650f400ae917ccb76ce5f08a9291a3a7692fe7bf2222d8af54f
manifest verification passed: 82 files

[7/7] Canonical hashes
dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586  /Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4/code/verification_report.json
e8562cfb54fd411e4c1926bd2e15cf394a1ece014def06d3621e12a0fcce5caf  /Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4/supplement/MANIFEST.sha256
e68130c3c38024a1e88b47cfa2cf06b8ebbead46665e82903d5bc6f2ff61bbe9  /Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4/manuscript/main_arxiv.pdf
78373226d868c7067c172e329e63535bc5ff5ee317fbdb8eeb8eaede7be0a371  /Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4/manuscript/main_biorxiv.pdf
77b4f098a1f0655ed4e04423caccec79a051cf11297b17d5fa2d630d539e7c4d  /Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4/manuscript/main_jap.pdf
85223b8099fc179b368e372be4e9fa1bda7d4e754421d8d10e78d436d977aa9e  /Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4/manuscript/supplementary_note.pdf
66e1f89f97840650f400ae917ccb76ce5f08a9291a3a7692fe7bf2222d8af54f  /Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4.zip

PASS: all standalone mathematical, code, manifest, PDF, and archive checks agree.
```

## Appendix B. Final research checkpoint

- **2026-08-21T22:51:19-07:00 — full software/artifact checkpoint.** Static
  review, exact replay, report/manifest inspection, production-free oracles,
  mutation suite, deterministic PDF/ZIP rebuild, Git-provenance challenge, and
  comparison with author records completed. Best-guess completion: 100% of the
  assigned software track. Strongest verified result: all supplied content
  artifacts are internally reproducible and finite mathematical calibrations
  survived extensive independent exact oracles. Exact remaining defect: the
  claimed v1.2.4 Git tag is unavailable and the Git replay accepts no tag.
