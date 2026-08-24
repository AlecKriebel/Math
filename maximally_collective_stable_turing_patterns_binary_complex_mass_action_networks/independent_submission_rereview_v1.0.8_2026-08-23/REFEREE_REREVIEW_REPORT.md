# Independent pre-submission referee rereview of v1.0.8

**Manuscript:** *Exact Diffusion Design for Maximally Collective Stable Turing
Patterns in Binary-Complex Mass-Action Networks*

**Audit date:** 2026-08-23 (America/Los_Angeles)

**Immutable target:** tag `maximally-collective-stable-turing-v1.0.8`, commit
`b4607c4cc9fe6931cedbbd0c5cd7e6e68a704f9f`

**Snapshot aggregate SHA-256:**
`436fb12e206edb864acbb017f2260fea61425996bbbec0ac21418e2231f3ef87`

This is an author-requested, independent pre-submission audit. It is not a
formal review commissioned by SIADS. Instructions and conclusions found in the
package were treated as objects of review, not as directions or established
facts. No manuscript, source, certificate, or release file in the audited tag
was edited.

## A. Executive verdict

**Technical-validity category: VALID AFTER MINOR CORRECTIONS.**

**Journal recommendation: minor revision.**

**Immediate submission disposition: HOLD — do not upload the present v1.0.8
bundle.**

The central mathematical results are valid. I found no false theorem, failed
endpoint, missing theorem hypothesis, invalid equality case, or unresolved
all-dimensional proof bridge. The revised SCC argument, the three-by-three
Schur remainder, the generic cubic recurrence calculation, and the fixed-mass
Fredholm/sectorial stability interface withstand independent reconstruction.
The functional-analytic portions are valid conditional on the cited standard
Crandall--Rabinowitz, Henry, and Kato theorems, whose concrete hypotheses are
present and were checked.

The minor-correction qualifier is caused by three local reproducibility defects
in the immutable release: its top-level manifest lists 570 absent
scratch files; two claimed TeX lock fields are not enforced; and a detached
supplement validation build stops one LaTeX pass too early and therefore
accepts stale table-of-contents page numbers. There is also one cosmetic
missing subscript. None changes a hypothesis, conclusion, dimension range,
endpoint convention, or headline claim.

Separately, the journal bundle says that it is provisional and is in fact not
upload-ready. It needs SIADS-compliant layout or the SIAM review template,
line numbering, visible keywords and MSC codes, a Supplementary Materials
index, a PDF cover letter, approved declarations, and refreshed DOI metadata.
Those are submission-preparation blockers, not mathematical defects. The
[current SIADS author instructions](https://epubs.siam.org/journal/siads/instructions-for-authors)
and [SIAM AI policy](https://epubs.siam.org/artificial-intelligence) should be
checked again on the day of upload.

## B. Claim-by-claim findings

The independent dependency map is in `THEOREM_DEPENDENCY_MAP.md`. Line numbers
below refer to the preserved `source_snapshot/`.

| Principal result | Exact claim boundary and dependencies | Classification and finding |
|---|---|---|
| Proposition 2.1 (`manuscript/main.tex:191-220`; Supplement `:31-63`) | Indexed binary-complex network, rank `m`, two-dimensional steady-flux kernel, positive flux cone, semipositive conservation covector, and `im Gamma_m=c^perp`, for `m>=3`. | **Independently verified.** Reconstructed from the reaction list and checked exactly in small dimensions. The all-dimensional rank and cone statements follow from the printed deductive minors/balances, not sampling. |
| Proposition 2.2 (`main.tex:222-253`) | All and only positive-equilibrium mass-action Jacobians are `A_m(a,b)H` with `a,b>0` and positive diagonal `H`; inverse rate construction included. | **Independently verified.** The derivative identity and inverse realization are exact. No omitted equilibrium or positivity condition was found. |
| Lemma 3.1 (`main.tex:260-309`; Supplement `:65-103`) | Exhaustive SCC classification for every proper induced subsystem, including direct `m=3` and exceptional `b=2a`. | **Independently verified.** At `b=2a`, only `X_1 -> X_m` disappears and that edge belongs to neither long cycle. Independent enumeration for `m=3,...,8` corroborated the general path argument. |
| Theorem 3.2 (`main.tex:311-362`; Supplement `:105-124`) | Every smaller nonempty principal subsystem is Hurwitz; the `m`-species `X` core has a positive real eigenvalue; first instability occurs at order `m=n-1`. | **Independently verified.** The long-cycle modulus bounds, boundary-triad Routh gap, SCC reduction, and Schur complement were checked. The displayed core remainder has determinant `2a^2b`, including the empty-interior `m=3` case. |
| Corollary 3.3 (`main.tex:364-371`) | The topology attains the maximal stable-pattern order and, with the later construction, a stable Turing branch. | **Verified conditional on the cited general-matrix endpoint and on Theorem 6.1.** The network-specific realization is independently verified. The historical maximality statement is citation-dependent. |
| Theorem 4.1 (`main.tex:379-428`) | Under the stated signed-principal-minor hypotheses, a positive diffusion-ray threshold exists iff the order-`(n-1)` sum is negative; the threshold is unique, the zero is ordinarily algebraically simple, and the positive-real eigenvalue occurs on the exact stated band. | **Independently verified.** Coefficient signs, strict monotonicity, endpoint behavior, ordinary algebraic simplicity, and the band argument are deductive. The theorem does not claim exclusion of later nonreal instability. Equality or a missing strict hypothesis does not supply a positive threshold. |
| Proposition 5.1 (`main.tex:445-492`) | Complete table of all one-species omission minors for the network family. | **Independently verified.** Exact independent principal-block calculations in several dimensions match the table; the general signs follow from the printed determinant reductions. |
| Theorem 5.2 (`main.tex:503-549`) | Necessary-and-sufficient stationary diffusion law and unique ray threshold on the homogeneously stable realization domain. | **Independently verified under its stated homogeneous-stability hypothesis.** The law follows from the complete omission table and Theorem 4.1. It concerns stationary crossings and does not exclude arbitrary wave instability. |
| Theorem 5.3 (`main.tex:558-596`) | Fixed-`H` and unit-equilibrium contrast infima, topology-wide contrast-product lower bound, equality/nonattainment statements, and sharpness as an infimum. | **Independently verified.** Denominators, strict inequalities, equality exclusions, and limiting sequences were checked. The scope is this topology and stationary crossings, not a global Pareto frontier over networks. |
| Theorem 6.1 (`main.tex:627-808`; Supplement `:237-482,947-1015`) | Exact unit-equilibrium diffusion, homogeneous stability, first-mode isolation, critical kernels and transversality, unique gauge-fixed `w_0` and `w_2`, all-`m` negative cubic coefficient, positive local stationary branches, and local exponential stability in the fixed-mass `H^1` phase space. | **Independently verified**, with the center-manifold/semigroup conclusion **verified conditional on cited standard results**. The exact matrix, kernel, contraction, recurrence, denominator, and shifted-polynomial sign steps pass. A reaction-level reconstruction matched the cubic numerator at `m=3,4,5,8,12`; the formal recurrence and finite-sum identity supply the all-dimensional bridge. The Fourier range/kernel/cokernel, `k^-2` inverse, Fredholm index, sectoriality, positivity, and complementary spectral continuation were reconstructed deductively. |
| Theorem 7.1 (`main.tex:844-1046`) | Inclusive scaled interval, physical equilibrium/rate/diffusion realization, homogeneous and spatial certificates, transformed adjoint, transversality, gauge correction, positivity and stability, fixed contrast product, unique within-family minimum, and `Theta(sqrt(m))` endpoint. | **Independently verified**, with local nonlinear stability **conditional on the same standard functional-analytic results**. Both certified endpoints, `m=3`, `m=4`, and the small complementary gap near `m=149` were inspected. The optimum is within the stated family; no constant-optimal or global Pareto-frontier claim is proved or made. |
| Equation (61) (`main.tex:1061-1071`; Supplement `:882-945`) | An exact `m=3` near-threshold example with positive cubic coefficient. | **Computationally reproduced and proof-checked.** It is a finite rational counterpoint and is correctly not promoted to a universal nonlinear obstruction. |
| Proposition 8.1 (`main.tex:1093-1113`) | Local robustness for each fixed `m,L`, restricted to the positive-equilibrium realization manifold, with one scalar diffusion multiplier retuned. | **Verified conditional on standard implicit-function and spectral-perturbation results.** Simplicity, nonzero multiplier derivative, diffusion positivity, low-mode gaps, high-mode ellipticity, cubic continuity, and branch-gap continuity are supplied. It does not cover arbitrary perturbations or a dimension-uniform radius. |
| Figures and simulations (`computation/simulations.py`; `figures/*.py`) | Numerical illustrations and refinement evidence. | **Computationally reproduced only.** They were not used as proof of existence, stability, asymptotics, or an all-dimensional assertion. |

### Central independent controls

- Reconstructed stoichiometric, Jacobian, Hessian, omission-minor, and Fourier
  matrices from the reaction definitions rather than importing project helper
  constructors.
- Exhaustively enumerated proper principal sets and SCCs for `m=3,...,8` at a
  generic positive point and at `b=2a`.
- Checked exact kernels, adjoint kernels, conservation gauges, transversality,
  and scaled transformations at `m=3,4,7`; independently solved the harmonic
  corrections and cubic contractions at `m=3,4,5,8,12`.
- Tested both scaling endpoints and numerical complementary spectra at
  `m=3,4,149`. The closest sampled noncritical margin was about `7.34e-4` at
  `m=149`: small but positive, as allowed by the fixed-dimension local theorem.
- Re-expanded the shifted sign polynomials and checked denominator positivity,
  equality cases, `m=3`, `m=4`, endpoint inclusions, and outside-domain
  degeneracies (`m=2`, `a=0`, `b=0`, nonpositive `H,D`, and weakened strict
  minor hypotheses). None furnishes a counterexample within the claimed
  domain.

Finite enumerations, random/spectral probes, and simulations were treated as
falsification evidence only. The all-dimensional claims rest on the explicit
recurrences, finite-sum identities, determinant arguments, and sign
certificates.

## C. Code and reproducibility findings

### Preservation and manifests

- The tagged source snapshot contains 1,064 files totaling 18,941,206 bytes.
- The 210-entry portable public manifest passed before execution.
- All seven hashes in `release/BUNDLE_SHA256.txt` passed.
- The 1,633-entry top-level release manifest failed: 1,063 present files have
  correct hashes, no present file mismatches, and 570 listed files are absent.
  Every absent path is an ignored v1.0.7 audit/scratch path. This is staging
  contamination, not current-file tampering, but it invalidates that baseline.
- The journal source ZIP is valid and byte-identical to the staged 11-file
  source tree. Its SHA-256 is
  `256a44bdba2489cb7b682b2c708260a172af4d6ebd0054a2f318815693b69638`.

### Executed campaign

| Current or historical stage | Exit / runtime | Finding |
|---|---:|---|
| Current v1.0.8 full portable public replay, clean copy | `0` / 72.55 s; independent duplicate `0` / 71.69 s | All eight stages, fixed shipped baseline, regenerated exact-artifact comparison, distinct self-consistency manifest, and `PUBLIC_REPLAY_PASS`. |
| Current v1.0.8 minimal replay, clean copy | `0` / 42.31 s | Exact aggregate, generic cubic bridge, endpoint checks through `m=200`, finite spectral regression, and `MINIMAL_VERIFIER_PASS`. This is a packaging duplicate, not new proof. |
| All current direct verifier entrypoints | `39/39` pass / 87.39 s | Every source entrypoint ran normally. The original request expected 38; v1.0.8 has 39 because the generic cubic verifier was added. |
| All current entrypoints under optimized Python | `39/39` expected rejection / 0.96 s | Every entrypoint fails closed; no assertion-dependent false `PASS` survives `-O`. |
| Mutation/regression suite | `0` / 8.88 s | 25 tests passed. Independent profile, manifest, cubic-coefficient, assertion-mode, TeX-lock, and build-pass controls were also exercised. |
| Full PDF semantic audit | `0` / 1.45 s | Passed producer, page, embedded-font, and extractor-robust semantic probes. |
| Manuscript and stale-claim audits | `0` / 0.10 s and `0` / 0.47 s | 82 labels, 29 citations, 201 abstract words; 652 files checked for stale claims. |
| Clean journal source build with correct pass count | `0` / 6.50 s | Main and supplement each 19 pages; no undefined references/citations, fatal errors, overfull boxes, or unembedded fonts. Extracted layout text equals the submitted PDFs; creation metadata differs. |
| Top-level release-manifest check | `1` / 0.23 s | Fails on the 570 absent paths. |
| Top-level v1.0.8 lineage replay | `2` / 2.79 s | Five documented historical ZIPs were unavailable; no later stage is counted as checked. Even with them, the bad manifest would stop the baseline gate. |
| Embedded v1.0.7 `RUN_COMPLETE_AUDIT.sh`, disposable copy | `1` / about 94 s | Outer and inner hashes and the historical minimal replay pass; its full replay stops at the known v1.0.7 PDF false-negative (`supplement PDF lacks unambiguous Latin near-threshold parameter`). This archived wrapper is not a current v1.0.8 validator; v1.0.8's repaired PDF audit passes above. |

The full command ledger is `COMMANDS.tsv`; the per-entrypoint ledger and raw
logs are under `agent_software_rereview/`.

### What the 39 entrypoints genuinely check

The complete line-specific semantic table is in
`agent_software_rereview/SOFTWARE_REREVIEW.md`. In summary:

- Thirty-three nonaggregate, nonfloating entrypoints use exact
  symbolic/rational algebra, exact finite regression, provenance, or freshness
  checks, often in combination. Many share formula modules or duplicate `dd_`
  and non-`dd_` layers and therefore are not epistemically independent.
- Four are fail-fast aggregate runners and add orchestration coverage, not a
  new mathematical assertion.
- Only `verify_branch_stability.py` and
  `verify_exchange_of_stability.py` use floating-point eigensolvers and stated
  tolerances. Their finite spectra are regression evidence only.
- `verify_generic_cubic_recurrence.py:21-304` is a substantive symbolic
  all-`m` recurrence-to-closed-form check. It imports only SymPy and verifies
  the boundary systems, recurrences, determinant, product sum, contraction
  `R_m+C_m hfrak`, and scaled gauge term. It still types formulas printed in
  the paper; it does not reconstruct reactions, establish the domain and
  denominator signs, or prove the PDE theorem. Its pass is not a theorem proof.
- The table, certificate, and PDF freshness checks regenerate their objects
  from named source formulas. Hard-coded expected expressions make some checks
  consistency tests, but none of the inspected central comparisons is vacuous.
  Independent reaction-level calculations mitigate shared-transcription risk.

Aggregate scripts use fail-fast child execution, failing children propagate,
assertion mode is explicitly guarded, sign checks establish domains and
denominators in the accompanying proof, and no load-bearing runtime stage
uses the network. Stored outputs were used only to identify provenance and
expected artifact scope.

### Regenerated artifacts

The clean portable replay regenerated all primary exact data/tables, finite
JSON instances, all 49 simulation files, nine figure files, six manuscript
files, integrated-design output, and stale-audit output. All were byte-identical
to the supplied artifacts. Expected differences were confined to test runtime
text, correctly updated provenance labels, and the deliberately new separate
self-consistency manifest.

The journal PDFs rebuilt with the correct pass count have layout text identical
to the submitted PDFs. PDF bytes differ only through creation metadata. In the
top-level detached validation loop, however, two supplement passes leave stale
TOC page numbers (for example S5/S6/S7/S9 appear as 3/4/6/17 instead of
4/5/7/18). A third pass produces the canonical PDF byte for byte.

## D. Defects and exact repairs

| ID | Classification | Defect and evidence | Required exact repair | Effect on claims |
|---|---|---|---|---|
| R1 | **Minor reproducibility** | `release/sha256_manifest.txt` lists 570 absent prior-audit scratch files; `release/create_release_manifest.sh --check` exits 1. The generator at `release/create_release_manifest.sh:17-29` uses unrestricted `find .`. | Generate the manifest from a sorted, NUL-safe tracked-file or explicit release allowlist, excluding the manifest itself; test it against a fresh `git archive`; rebuild affected bundle hashes; publish a new immutable version rather than moving the v1.0.8 tag. | Release-integrity/replay claim only. No hypothesis, conclusion, or headline changes. |
| R2 | **Minor reproducibility/software** | `environment/check_toolchain.sh:78-85` skips `FORMAT` and `LATEX`; impossible values still emit `TOOLCHAIN_LOCK_PASS`. | Enforce those two rows against the probe logs (the tested local correction skips only `ENGINE|BIBER`) and add negative tests for every special lock field. | Tightens an existing environment claim; no mathematical change. |
| R3 | **Minor reproducibility/submission** | `release/one_command_replay.sh:211-220` uses two supplement passes and accepts stale TOC page numbers. | Add a third supplement pass, preferably loop until auxiliary files stabilize, and compare semantic text or TOC state to the canonical artifact. | Build-validation/presentation only; no mathematical change. |
| M1 | **Cosmetic** | Supplement `manuscript/supplement.tex:981` writes `Delta` where the defined scaled diffusion matrix is `Delta_m`. | Replace `\Delta` with `\Delta_m`. | No hypothesis, estimate, or conclusion changes. |
| S1 | **Expository/submission-preparation blocker** | The generic 0.82-inch-margin article has an approximately 6.86-by-9.36-inch text area, no review line numbers, no visible keywords/MSC codes, no Supplementary Materials index, and no PDF cover letter. The bundle itself admits this at `submission/journal/README.md:1-62`. | Use SIAM's current review template or meet the current alternative layout rules; add continuous line numbering, approved keywords and MSC codes, a supplementary index with description/justification, and a final PDF cover letter; rebuild and visually inspect portal-generated PDFs. | Journal presentation only. |
| S2 | **Minor metadata/reproducibility** | v1.0.8 source says its DOI is pending, but the exact DOI now resolves as `10.5281/zenodo.22074358`. Funding, competing-interest, and AI wording remain marked for author confirmation. | Prefer a corrected immutable v1.0.9 and cite its exact DOI consistently. If v1.0.8 is retained, replace every pending marker with the exact v1.0.8 DOI. Obtain human approval for all declarations. Under current SIAM AI policy, include the required responsibility sentence; for one author use “The author assumes responsibility for all content.” | Metadata/declarations only. |

No fatal, major, or minor mathematical defect was found. No silent repair was
made. The clean disposition is a new immutable release after R1--R3 and M1,
followed by regeneration of all submission artifacts and metadata.

## E. Scope, confidence, and strongest uncertainty

The entire mathematical result is valid within its stated scope: the indexed
topology, `m>=3`, positive-equilibrium mass-action realizations, positive
diagonal species scalings and diffusions, stationary crossings, and local
fixed-mass branches. This review does not establish arbitrary wave-instability
optimality, results for other networks, a global Pareto frontier, a global
basin, stability far from onset, or a dimension-uniform branch radius. The
paper's limitations accurately exclude those conclusions.

I did not reprove the general Crandall--Rabinowitz, Henry, Kato, or cited
historical maximality theorems. Their concrete application hypotheses were
checked. Five historical lineage archives were unavailable, so the top-level
lineage replay is not checked. The immutable top-level manifest would fail even
if those archives were supplied. No journal portal-generated PDF was available
for inspection.

Confidence is approximately **98% for the algebraic claims**, **95% for the
functional-analytic application conditional on the standard citations**, and
**high for the observed software behavior**. The strongest remaining
mathematical uncertainty is shared transcription between printed formulas and
some typed certificate expressions. Independent reaction/Hessian controls in
multiple dimensions and separate generic recurrence/sign derivations reduce
that concern substantially; it is not an identified proof gap. The strongest
practical uncertainty is whether the final, reformatted journal bundle remains
synchronized after the required edits.

## Submission-readiness checklist

Before upload:

1. Apply R1--R3 and M1 in a new version; do not mutate or move the v1.0.8 tag.
2. Regenerate and check every manifest and all seven bundles from a clean
   archive; rerun the full current portable replay, minimal replay, all 39
   entrypoints normally and under `-O`, all 25 tests, and the document audits.
3. Reformat for SIADS review, add line numbering, keywords, MSC codes, and the
   Supplementary Materials index; produce the cover-letter PDF.
4. Approve funding, competing-interest, authorship, availability, and AI
   declarations. Use the current SIAM-required responsibility wording.
5. Insert the exact DOI for the corrected immutable release everywhere,
   rebuild the source ZIP and PDFs, and inspect the journal portal's generated
   PDFs before final submission.

## Audit completion checklist

- [x] Outer and inner hashes verified before execution, including the embedded
  historical packet and current portable/bundle manifests.
- [x] Main manuscript and supplement read completely.
- [x] Independent theorem-dependency map constructed.
- [x] Central claims checked against exact hypotheses, domains, endpoints, and
  scope.
- [x] All-dimensional proofs separated from finite evidence.
- [x] Load-bearing verifier and replay source inspected before outputs were
  trusted.
- [x] Circularity, duplicate checks, and shared typed formulas sought
  explicitly.
- [x] Exact arithmetic separated from floating-point evidence.
- [x] Current full portable and minimal replays completed in clean copies.
- [x] All 39 current entrypoints, tests, mutations, and audits run.
- [x] Tables and representative formulas traced to definitions.
- [x] Small-dimensional reconstructions performed independently.
- [x] `m=3`, `m=4`, both scaling endpoints, `m=149`, `m=200`, and equality
  cases inspected.
- [x] Counterexamples and outside-domain failures actively sought.
- [x] Simulations treated only as numerical evidence.
- [x] Functional-analytic stability assessed separately.
- [x] Every incomplete or failed stage disclosed.
- [x] Technical validity separated from journal recommendation and upload
  readiness.
- [x] No conclusion inferred solely from stored logs or passing software.
- [!] The top-level v1.0.8 lineage replay was not completed because five
  external historical archives were unavailable and the supplied baseline
  manifest fails. The embedded v1.0.7 complete wrapper was executed and
  stopped at its known archived PDF-audit defect; neither is called a pass.

## Companion evidence

- `INTEGRITY_AND_REPLAY.md`: hashes, environment, executions, and artifact
  comparisons.
- `PACKAGE_INVENTORY.md`: package contents and dependency boundary.
- `THEOREM_DEPENDENCY_MAP.md`: independently reconstructed proof map.
- `DEFECT_DISPOSITION.md`: v1.0.7-to-v1.0.8 disposition and new findings.
- `agent_core_rereview/CORE_REREVIEW.md`: algebraic and generic-cubic audit.
- `agent_pde_rereview/PDE_REREVIEW.md`: functional-analytic audit.
- `agent_software_rereview/SOFTWARE_REREVIEW.md`: complete 39-entrypoint
  semantic table and reproducibility audit.
- `COMMANDS.tsv` and `agent_software_rereview/COMMAND_RESULTS.jsonl`: command
  ledgers.
