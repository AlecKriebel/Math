# Independent software and reproducibility referee report

Target: commit `6f68ad3e795c`, preserved in `../source_snapshot/`. Audit date: 2026-09-05 Pacific / 2026-09-06 UTC. All execution and mutations used disposable copies under `software/scratch/`; no submitted source was edited, no Git operation wrote history, and no person was contacted.

## Verdict

The shipped mathematical computations passed the substantive checks completed here. I found **one real certificate-verifier acceptance defect**, affecting malformed added/duplicate polynomial terms. It does not invalidate the genuine shipped certificates or any theorem. The full-source printed-table checks and fixed release manifest contain the demonstrated mutation; the minimal verifier aggregate does not.

The release is **not yet submission-qualified by this audit**: the manuscript asserts an immutable v1.0.9 source tag that does not exist, and actual full portable/detached TeX builds were not completed because of host storage limits. The root referee separately found overlapping fraction rows in submitted PDFs despite the semantic audit passing; that visual defect is not assessed away by any software PASS here.

## Exact completed scope

| Stage | Result | Evidence and limit |
|---|---|---|
| Full source manifest | **PASS** | All **1,108** entries hash correctly. Fresh `git archive 6f68ad3e795c <project>` contains **1,109** files, exactly equal to the preserved source. The sole unlisted file is the manifest itself; there are no omitted/extra tracked files. |
| Portable manifest | **PASS** | All **212** entries hash correctly before generators run. |
| Seven released ZIPs | **PASS** | All **7** advertised SHA-256 hashes, ZIP CRCs, path safety, full member contents and ordering checked. Rebuilt all seven with the recorded Python/zlib route; **all seven byte-identical**. |
| Direct verifiers | **39/39 PASS** | Every direct entrypoint executed with its default arguments in an unmodified disposable source. Total final-run command time **93.375 s**. |
| Optimized-Python controls | **39/39 REJECTED** | Every entrypoint under `python -O` returned nonzero and an assertion-mode error. Total **1.600 s**. This is 39 normal runs plus 39 negative runs, not 78 independent proofs. |
| Supplied tests | **28 passed, 1 skipped** | **9.745 s** command time. The skipped test is the actual pinned-TeX lock negative-control test. A claim of 29 passed is not made for this audit. |
| Minimal replay | **PASS** | Clean `external_audit/minimal_verifier` copy; **45.326 s**, final `MINIMAL_VERIFIER_PASS`. No discovery-side files needed. |
| All non-TeX portable stages | **PASS** | Exact data/table generation, source audit, symbolic/integrated verifiers, exports, full numerical route, and three Python figures executed individually from a fresh portable copy. This is explicitly a partial replay, not `PUBLIC_REPLAY_PASS`. |
| Deterministic exact artifacts | **13/13 MATCH** | Regenerated current JSON, four TeX tables, six unit instances and two scaled instances match the initially downloaded baseline byte-for-byte. |
| Numerical illustrations | **15/15 completed** | Full route, no quick substitution; **8.026 s**. Refinement maximum **1.4095038570570294e-8**, below the declared **2e-8**. All **33** simulation CSVs have identical numeric values to the shipped CSVs (maximum absolute difference **0**). Final profiles are finite, strictly positive and conserve the mean mass within `1e-10`. These are floating numerical illustrations, not proofs. |
| Additional exact reconstruction | **PASS** | Fresh differentiation of the displayed polynomial reaction field, Hessians, constrained zero-mode and second-harmonic solves, and scaled cubic contraction at **m=3,7,11**, with **L=2/3,3/5,1/2** respectively. Negative cubic signs and supplied formulas agree. |
| Additional negative controls | **PASS**, except defect below | Reaction multiplicity, diffusion constant, zero-mode formula, Fourier contraction factor, scaled gauge sign and exact numerical source changes rejected; injected child-process failure propagates without wrapper PASS. A regenerated self-manifest cannot repair a mismatch to the shipped baseline. |
| Original full/journal PDF semantic audits | **PASS** | **1.536 s / 1.252 s**. Producer, page counts, embedded fonts and text anchors checked. These checks cannot detect the row-overlap defect found by visual inspection. |
| Actual pinned toolchain preflight | **PASS with environmental warnings** | A selectively extracted official TinyTeX 2022.04 returned `TOOLCHAIN_LOCK_PASS`, pdfTeX 1.40.24 and Biber 2.17 after **40.925 s**. Biber had emitted disk-full extraction errors. This narrow probe does not establish a reliable completed document build. |
| All 28 TeX lock-field shell controls | **28/28 REJECTED** | Controlled executable stubs supplied baseline TeX banners/logs while the real Python dependency checker ran. Each of the **28** lock values was separately replaced with an impossible value; all rejected. These are protocol-level unit controls, explicitly **not 28 actual TeX builds**. |
| Full portable replay with actual TeX | **NOT COMPLETED** | Base-host literal replay exited **2** for missing TeX commands. Toolchain recovery encountered disk exhaustion; workflow was stopped and its temporary installation/cache removed. No full portable completion marker is claimed. |
| Three detached source builds | **NOT CHECKED dynamically** | ZIP contents equal canonical sources after the documented relative-path changes, journal-mode marker and arXiv BBL omission. Supplement stabilization and rendered-text comparisons were inspected in the scripts but not executed in this audit. |
| Top-level provenance replay | **NOT COMPLETED** | Base-host executable preflight exited **2**. All five lineage archives are absent from the documented default `/mnt/data`; no full lineage claim is made and their hashes were not independently available to verify. The top-level replay requires them; the portable route does not. |

## S1. Malformed certificate terms can receive a false PASS

Severity: **minor software correctness / certificate checkability**. Fix before final qualification, especially because the specialist/minimal verifier is advertised as a detached check.

`independent_verifier/frontier_verify_mode_certificates.py:193–201,210–218` converts term lists to dictionaries, then compares only the expected monomials. It compares the declared `term_count` with the generated polynomial count, but never with the supplied list length. Thus unexpected monomials are ignored, and earlier duplicate entries are overwritten. The corresponding spatial check at `frontier_verify_exposition_identities.py:359–371` has the same omission. The unit-profile set comparison at `verify_mode_isolation.py:27–45` also collapses identical duplicate entries.

Two explicit counterexamples, preserved as JSON artifacts:

- Append `{"powers":[99,99],"coefficient_in_U_ascending":["-1"]}` to the 22-term homogeneous list and `{"powers":[99,99,99],"coefficient_in_A_ascending":["-1"]}` to the 84-term spatial list, leaving declared counts unchanged. The new polynomials have negative high-degree terms; nevertheless the CLI exits **0** with `VERIFY_MODE_CERTIFICATES_PASS`.
- Insert an opposite-sign copy of an existing term **before** its genuine row. The later row overwrites it; the CLI again exits **0**. Move the same negative duplicate **after** the genuine row and it is rejected. The mathematical sum of listed terms is independent of list order, but this parser's acceptance is not.

An identical positive duplicate in each unit-profile list also receives `MODE_ISOLATION_PASS`. This further demonstrates the lack of list cardinality/uniqueness enforcement.

Containment was measured, not assumed:

| Enclosing check / control | Actual outcome |
|---|---|
| Direct scaled CLI, added negative terms | **0, false PASS** |
| Direct scaled CLI, opposite duplicate first | **0, false PASS** |
| Direct scaled CLI, opposite duplicate last | **1, rejected** |
| Declared counts changed to 23 and 85 | **1, rejected** |
| Unknown extra block outside the two checked polynomials | **0, ignored metadata**; not itself a defect, since general JSON Schema validation is explicitly unclaimed |
| Full-tree exposition checker with malformed JSON and unchanged printed table | **1**, `STALE_GENERATED_MODULUS_TABLE` |
| Full-tree symbolic aggregate | **1**, same printed-table containment |
| Minimal symbolic aggregate, which intentionally lacks printed tables | **0**, `ALL_SYMBOLIC_CERTIFICATES_PASS` — false acceptance survives the aggregate |
| Portable replay's fixed manifest gate | **1**, before stage `[1/8]`; malformed file detected. This gate was isolated after a synthetic protocol preflight, not an actual TeX qualification. |

The genuine certificates have the correct 35/77/22/84 term lists and passed all normal runs. There is **no counterexample to the manuscript's polynomial identities or positivity assertions** here. The defect concerns the verifier's acceptance of malformed alternative objects. Require each raw list length to equal its declared and generated counts; reject duplicate monomials; compare exact supplied and generated monomial sets and every coefficient. Add both insertion and duplicate-order mutations for unit and scaled certificates. The shared copies and minimal/public packages should receive the same repair when packaging is refreshed.

## S2. v1.0.9 availability is still prospective

`manuscript/main.tex:1252–1253` says the sources “are frozen” in the v1.0.9 tagged tree. On **2026-09-06 04:35 UTC**, a successful `git ls-remote --tags` returned no matching v1.0.9 tag; the GitHub release API returned **404**. The researcher explicitly said the tag had not been created. This is an unresolved release dependency, not a DOI that should be invented.

Before submission, either make the reviewed immutable archive actually available after authorized final repairs/approval, or revise availability language and references to an existing exact snapshot. This audit created no tag or release. The exact preceding v1.0.8 DOI and concept DOI are not substitutes for the absent claimed v1.0.9 tag.

## Semantic audit and independence

All 39 entrypoints were read. `ENTRYPOINT_AUDIT.md` gives the individual mechanism and evidence boundary. The four support modules were also inspected. `common.py` and `core.py` are byte-identical, and the eight `dd_*` scripts duplicate corresponding regression logic. Aggregate wrappers merely launch children with `check=True`. These facts are properly disclosed in the shipped verifier README; none was counted as new independent evidence.

The live generators, exports, simulations, figure scripts, source/PDF audits, package builder, manifest builder and replay orchestration were inspected. Current generators deliberately import verifier helpers, so generator/checker agreement alone can share an error. That risk is materially reduced by `verify_current_numerical_provenance.py`, which independently reconstructs reactions and solves linear systems, and the standalone symbolic cubic recurrence bridge, which imports no project helper. My additional polynomial differentiation/linear-solve check used m=7 and m=11 outside the standard six-dimension contraction regression.

Exact matrix/certificate arithmetic uses SymPy rationals/integers. The two complementary-spectrum checks use ordinary NumPy eigenvalues and discard near-zero roots at `1e-7`; they are correctly identified as finite floating regression, not nonlinear proofs. Certificate polynomial identities are exact, but their parameter domains and all-dimensional graph/functional-analytic conclusions still depend on the human proofs. The independent algebra referee additionally reconstructed the near-threshold m=3 cubic from the actual Hessians, closing the linkage that its small dedicated script merely assumes.

The test suite includes useful mutation controls, but also literal-source and orchestration-marker tests. Its count is not a count of mathematical theorems verified. The shell uses `set -euo pipefail`, checks the downloaded baseline before generators and keeps it distinct from a regenerated self-manifest. The repaired tracked-file manifest is genuinely repaired, as the fresh archive comparison shows. The detached supplement logic compares successive AUX/TOC files with a bounded five-pass stabilization loop and compares rendered text with the appropriate canonical/journal PDFs; source inspection supports this mechanism but does not replace the omitted build run.

## Environment, failures and retained evidence

Executed numerical environment: macOS 26.6.2 arm64, CPython **3.9.6**, zlib **1.2.12**, Matplotlib **3.7.1**, NumPy **1.24.3**, pandas **2.3.3**, pypdf **6.10.0**, pytest **8.4.2**, SciPy **1.10.1**, SymPy **1.14.0**; assertion mode enabled, BLAS threads fixed to one, UTC/C locale and fixed source epoch. pypdf was installed only into this audit's disposable target.

Two early verifier batches lost logging capability during storage exhaustion and were rerun completely; the final 39+39 results are the retained successful batch. The first fresh-archive attempt and full TinyTeX extraction also failed from storage exhaustion; the archive comparison was subsequently completed. The official 2022.04 download was hashed, then removed, together with this audit's temporary TeX installation and newly generated Biber cache. No unrelated user files were deleted. The original failed attempts are not quietly counted as successful build runs; some initial failures have no separately retained runtime because logging itself failed.

Compact evidence files are `COMMANDS.tsv`, raw `COMMAND_RESULTS.jsonl`, `ENTRYPOINT_AUDIT.md`, `RESEARCH_LOG.md`, `logs/integrity_setup.log`, `logs/verifier_driver.log`, `logs/minimal_replay.log`, `logs/computational_replay.log`, `logs/independent_simulation_comparison.log`, `logs/bundle_and_detached_source_checks.log`, `logs/certificate_containment.log`, and the shipped PDF audit summaries. Checkable reproductions are `independent_checks.py`, `certificate_containment.py`, `computational_replay.py`, `bundle_checks.py` and `mutation_artifacts/*.json`. Scratch copies and downloaded dependencies should not be published as new research findings.

## Artifact links

- [Command ledger](/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_full_referee_2026-09-05/software/COMMANDS.tsv)
- [Entrypoint-by-entrypoint semantic inventory](/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_full_referee_2026-09-05/software/ENTRYPOINT_AUDIT.md)
- [Mutation and containment reproducer](/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_full_referee_2026-09-05/software/certificate_containment.py)
- [Added-negative-term counterexample](/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_full_referee_2026-09-05/software/mutation_artifacts/extra_negative_terms.json)
- [Minimal-aggregate false-PASS log](/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_full_referee_2026-09-05/software/logs/containment_minimal_symbolic_aggregate.log)
- [Full-tree rejection log](/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_full_referee_2026-09-05/software/logs/containment_full_symbolic_aggregate.log)
- [Portable manifest rejection log](/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_full_referee_2026-09-05/software/logs/containment_portable_manifest_gate.log)
- [Full non-TeX replay log](/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_full_referee_2026-09-05/software/logs/computational_replay.log)
- [Actual toolchain preflight log with disk warnings](/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_full_referee_2026-09-05/software/logs/pinned_toolchain.log)
