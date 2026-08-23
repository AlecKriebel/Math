# Independent post-submission referee report

## Manuscript

*Exact Diffusion Design for Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks*

Audited release: `full_referee_validation_packet_v1.0.7`, tag
`maximally-collective-stable-turing-v1.0.7`, commit
`963594192a494421de6c5984c24d4a41e682da3f`, exact-version DOI
`10.5281/zenodo.22062080`.

Audit date: 2026-08-22, America/Los_Angeles.

The packet's `REFEREE_PROMPT.md`, `START_HERE.md`, review maps, proof aids,
stored certificates, and `PASS` files were treated as author-supplied evidence
and navigation, not as instructions superseding the human request and not as
proof. No author conclusion or stored output was presumed correct.

## A. Executive verdict

### Technical-validity category

**VALID AFTER MINOR CORRECTIONS**

### Journal recommendation

**Minor revision.**

### Basis

The mathematical headline survives independent reconstruction. I found no
false theorem, counterexample in the stated domain, missing central
hypothesis, invalid endpoint, finite-to-all-dimensional proof gap, or defect
that changes the title claim. The network topology, realization family,
all-spectrum localization, diffusion-ray theorem, omission-minor law, sharp
stationary contrast results, unit and equilibrium-scaled stable-pattern
families, cubic signs, fixed-mass local stability, and retuned robustness are
valid with their stated scope. The PDE conclusions are conditional on standard
Crandall--Rabinowitz, sectorial center-manifold, Kato perturbation, and Henry
linearized-stability results; I checked the hypotheses needed here.

The corrections are local and nonmathematical: the advertised full replay
fails its own PDF text probe even in the documented TeX/Biber generation; the
TeX/Python environment is not fully pinned and the archived PDFs use a
different producer from the scripted route; some direct verifier entrypoints
can print false `PASS` under optimized Python despite the README; and several
nominally all-dimensional or independent verifier layers are actually finite,
hard-coded, duplicated, or aggregate checks. None changes a theorem
hypothesis, conclusion, dimension range, endpoint, or headline.

My calibrated confidence is **very high (about 97%)** in the exact
mathematics and **high (about 93%)** in the complete local PDE conclusion,
conditional on the cited standard functional analysis. Reproducibility
confidence is lower because the unmodified all-in-one command does not reach
its completion marker.

## Preservation, provenance, and inventory

Before execution, the packet was copied to separate `source_snapshot/` and
`working_packet/` directories. The source snapshot was not executed or
modified. All replay and mutation work occurred in disposable copies.

| Item | Finding |
|---|---|
| Outer manifest | 263/263 entries matched before execution, exit 0. The manifest itself is not self-covered; SHA-256 `9cce0ed2d5f63efd121e92eb846f5bc404351aa1bf327c6af51afc9e4277c43c`. |
| Inner manifest | 198/198 entries matched before execution, exit 0. |
| Independent package aggregate | 264 files, 2,580,258 bytes; path-and-content aggregate SHA-256 `ae955f478dabf85cc3731b57cfa4aebe631d7977df04bdc5e39b271d112aebf5`. |
| Release provenance | Local tag resolves to the declared commit. Every inner-manifest file matches the tagged `public/repository/` subtree; zero missing and zero hash mismatches. |
| Reading PDFs | `paper/main.pdf` and `paper/supplement.pdf` are byte-identical to the repository manuscript PDFs. |
| Package contents | 264 files: manuscript/supplement, proof aids, exact and numerical data, 38 verifier entrypoints, tests, generators, figures, stored outputs, review maps, and orchestration. See `PACKAGE_INVENTORY.md`. |
| Private/missing inputs | No private path, missing mathematical input, runtime network call, or undocumented historical archive is needed by the portable replay. The `/mnt/data/` occurrence is a rejection sentinel. |
| Independence of minimal replay | `minimal_verifier/` is source-identical to `repository/independent_verifier/` except for README/replay files. It is a packaging duplicate, not an independent implementation. |
| Unpinned dependencies | Python requirements use lower bounds only; there is no wheel/solver/BLAS lock. The TeX distribution and packages are unpinned. |

Host details and exact dependency versions are in `ENVIRONMENT.md`. The
default host Python was CPython 3.9.6 with the recorded scientific stack except
`pypdf`; the host initially lacked `pdflatex`. Disposable `pypdf==6.10.0` and
official TinyTeX bundles were used for explicitly labeled reruns, without a
system-wide install.

I read all 1,217 lines of `main.tex` and all 971 lines of `supplement.tex` and
rendered and visually inspected every page of the 18-page main PDF and
18-page supplement. All fonts are embedded; I found no clipping, overlap,
missing page, or unreadable table. The independent theorem map is
`THEOREM_DEPENDENCY_MAP.md`; it was constructed before consulting the supplied
review maps for comparison.

## B. Claim-by-claim findings

Evidence labels below mean what they say: deductive proof and independent exact
algebra are not conflated with finite regression, floating-point sampling,
simulation, provenance, or citation dependence.

| Result | Exact scope and conclusion type | Classification and basis | Source |
|---|---|---|---|
| Proposition 2.1, Eqs. (10)--(13) | Every integer `m>=3`; binary-complex topology, rank `m`, two-dimensional flux kernel, positive flux cone, semipositive conservation law. Algebraic. | **Independently verified.** Reaction matrices were reconstructed from the indexed complexes; rank/kernel/conservation were proved by balances and checked exactly for `m=3,4,5,6,7`. The empty `m=3` chain is handled correctly. | `main.tex:145-220`; `supplement.tex:31-63`. |
| Proposition 2.2, Eq. (16) | All and only positive-equilibrium Jacobians are `A_m(a,b)H`, `a,b>0`, `H` positive diagonal. Algebraic realization. | **Independently verified.** Both the mass-action derivative factorization and inverse rate construction were derived directly. No hidden realizability constraint was found. | `main.tex:222-253`. |
| Lemma 3.1 | Every nonempty principal set of order below `m`; exhaustive SCC list, including `m=3` and `b=2a`. Graph-theoretic. | **Independently verified.** The all-`m` path-forcing proof is complete. Exhaustive exact enumeration for `m=3,...,9`, generic and `b=2a`, found no omitted class. The deleted edge belongs to neither long cycle. | `main.tex:260-307`; `supplement.tex:65-101`. |
| Theorem 3.2, Eqs. (17)--(20) | All positive realizations; every smaller nonempty principal block Hurwitz; first unstable principal order exactly `m=n-1`; instability is positive-real at the full `X` core. Spectral. | **Independently verified.** Long-cycle modulus inequalities, all boundary-triad blocks, the 14-term Routh gap, and the signed core determinant were reconstructed. A 39,380-case and a separate 76,560-case numerical search found no counterexample but was not used as proof. | `main.tex:309-359`; `supplement.tex:97-108`. |
| Corollary 3.3 | Endpoint construction for every `n>=4` and existence of one stable-pattern realization. Algebraic/contextual/nonlinear. | The construction is **independently verified**; the historical general-matrix comparison is **verified conditional on a cited standard result**; the stable-pattern clause is **verified conditional on Theorem 6.1 and its cited standard PDE results**. Satnoianu's indexed abstract supports activator-subsystem orders through `n-1`. | `main.tex:361-372`. |
| Theorem 4.1, Eqs. (21)--(25) | Arbitrary real `n x n` matrix satisfying the exact signed-minor hypotheses; iff threshold, uniqueness, ordinary algebraic simplicity, and exact positive-real-eigenvalue band; no post-band wave exclusion. Algebraic spectral theorem. | **Independently verified deductively.** The principal-minor expansion and strict monotonicity in both ray parameter and real spectral parameter are valid. An exact counterexample after removing the positive order-`(n-1)` sum confirms that hypothesis is substantive. | `main.tex:376-425`; `supplement.tex:110-149`. |
| Proposition 5.1, Eqs. (26)--(29) | Complete order-`m=n-1` omission-minor table for every `m>=3`, `a,b,H>0`. Algebraic. | **Independently verified.** Sparse cycle covers, the triad determinant, and the two restricted nullvectors yield one negative, two zero, and all interior positive minors. Exact direct determinants matched for `m=3,...,7`. | `main.tex:442-489`; `supplement.tex:151-187`. |
| Theorem 5.2, Eq. (31) | `(a,b,H)` in the stated homogeneous relative-stability set and `D>0`; necessary-and-sufficient **stationary** diffusion law, unique simple ray threshold, exact positive-real band. Spectral/stationary. | **Independently verified under the stated hypothesis.** The simple conservation zero supplies the positive order-`m` sum; Theorem 4.1 then applies exactly. Equality gives no nonzero threshold, confirming strictness. No arbitrary-wave claim is made. | `main.tex:491-553`. |
| Theorem 5.3, Eqs. (32)--(35) | Fixed stable `H`, unit case, topology-wide product lower bound; nonattained sharp infima for stationary crossings. Algebraic optimization. | **Independently verified.** All inequalities, strictness, equality exclusions, and the unit sharpness sequence are exact. Scope is this topology and stationary crossings, not biological cost or a global Pareto frontier. | `main.tex:555-593`. |
| Theorem 6.1, Eqs. (36)--(48) | Every fixed `m>=3`; selected unit-equilibrium PDE; homogeneous stability, isolated simple first mode, transverse crossing, negative cubic, two positive locally exponentially stable branches in fixed-mass `H^1`. Spectral/local nonlinear. | **Verified conditional on standard cited PDE theorems.** I independently rebuilt the 35/77-term modulus certificates and equality loci, kernels, adjoint, transversality, Fourier factors, unique `w_0,w_2`, and the all-dimensional cubic bridge `N_m=R_m+C_m \mathfrak h_m`, where `\mathfrak h_m:=\sum_{j=1}^{m-2}(91m-181-j)^{-1}` is the harmonic sum. Fixed-mass Fredholm index zero, reflection oddness, exchange of stability, sectoriality, `H^1->L^2` smoothness, and the spectral gap satisfy the standard hypotheses. | `main.tex:595-772`; `supplement.tex:205-465,795-855,930-940`. |
| Stable contrast bounds, Eqs. (42),(60) | Unit-equilibrium nonlinear stable infimum bounded below and above; exact infimum left open. | **Independently verified modulo Theorem 6.1.** The lower bound is the stationary law; the selected stable design is the upper bound. No exact nonlinear optimum is claimed. | `main.tex:618-655,1019-1026`. |
| Theorem 7.1, Eqs. (49)--(59) | Every fixed `m>=3` and every `L` in the inclusive certified interval; physical scaled realization, stable local branch, exact contrast product and within-family optimum; exponent `1/2` only for stationary crossings of this topology. Spectral/local nonlinear/asymptotic. | **Verified conditional on the same standard PDE results.** Physical rescaling, transformed adjoint/mass covector, separate 22/84-term certificates, inclusive endpoints, gauge correction, cubic sign, positivity, exact contrasts, fixed product, unique `L_0` minimum, and `Theta(sqrt m)` scaling were independently checked. No constant-optimal or global Pareto claim is made. | `main.tex:774-1006`; `supplement.tex:467-777,816-843`. |
| Near-threshold Eq. (61) | One `m=3` affine path, `0<epsilon<=10^-3`; positive cubic; explicitly not universal. Exact finite-dimensional control. | **Computationally reproduced and proof-checked.** Exact elimination and rational remainder bounds support the stated sign and scope. | `main.tex:1027-1035`; `supplement.tex:875-928`. |
| Proposition 8.1 | Fixed `m,L`; small perturbations within the positive-equilibrium realization manifold, diffusion ratios, and interval length, with one retuned scalar multiplier; no uniform radius. Local robustness. | **Verified conditional on standard smooth spectral/center-manifold theory.** Simple-eigenvalue IFT, finite low-mode continuation, diffusion-dominated high-mode bound, and openness of the cubic/branch gaps establish exactly the stated codimension-one result. | `main.tex:1053-1073`; `supplement.tex:942-953`. |
| Numerical figures | `m=3,5,8` illustrations only. Floating-point. | **Numerically reproduced within declared tolerance, not used as proof.** All 15 full simulations passed; regenerated values differed at solver scale. | `main.tex:1088-1104`; `supplement.tex:955-969`. |

### Key independent derivations and adversarial controls

- The `m=3` and `m=4` source, stoichiometric, and Jacobian matrices are printed
  in `SMALL_DIMENSION_RECONSTRUCTIONS.md`. They were not imported from project
  helpers.
- Every omission minor was independently enumerated in several dimensions.
- The all-dimensional cubic bridge was derived from the `w_2` recurrence:
  `w_{i-1}-w_i=4w_i/K_i+sigma` and
  `T_i/(K_{i-1}K_i)=K_{i-3}K_{i-2}/(K_{-1}K_0K_1K_2)` reduce the contraction to
  the printed polynomial sum plus the harmonic sum `\mathfrak h_m`; the
  symbolic difference from `R_m+C_m \mathfrak h_m` is identically zero.
- The 35-, 77-, 22-, and 84-term modulus polynomials were rebuilt from their
  defining boundary factors. Equality cases were checked using pure-axis
  anchors, including the `E22` coefficient boundary `U=0` (outside the certified
  physical scaling interval); they were not inferred from nonnegative
  coefficients alone.
- Exact outside-domain controls confirm necessity rather than reveal defects:
  dropping the positive order-`(n-1)` sum breaks Theorem 4.1's post-threshold
  exclusion; equality in Eq. (31) gives no nonzero threshold; `T(H)=1` gives a
  double zero and lies outside the stable set; a naive `m=2` continuation has
  the wrong reaction count/rank and no conservation kernel.
- Both certified scaled endpoints were checked at `m=3,4`. At `m=149`, the
  unit-profile critical data and generic formulas were checked exactly, while
  competing-mode endpoint sweeps were numerical. The superseded outside-domain
  `m=149,L=1/21` value has the expected unstable complex pair, confirming the
  need for the repaired interval.

Full exact and numerical details are in `INDEPENDENT_CHECK_RESULTS.md`,
`agent_core_math/CORE_MATH_FINDINGS.md`, and
`agent_nonlinear_pde/NONLINEAR_PDE_FINDINGS.md`.

## C. Code and reproducibility findings

### Commands and outcomes

The machine-readable command ledger is `COMMANDS.tsv`; the detailed software
ledger is `agent_software_repro/COMMAND_RESULTS.jsonl`.

| Command/stage | Exit | Runtime | Finding |
|---|---:|---:|---|
| Outer and inner `sha256sum -c` | 0/0 | `<1 s` each | 263/263 and 198/198 matched before execution. |
| Literal `bash RUN_COMPLETE_AUDIT.sh` in the host environment | 2 | `0.00 s` | Stopped at `missing required command: pdflatex`; no work root and no stage executed. **Not a pass.** |
| Same wrapper with current disposable TeX Live 2026 after installing declared LaTeX packages | 1 | about `119 s` | Ran through repository stage 8, then failed PDF audit: 19-page supplement plus two extraction/layout probes. |
| Same wrapper with full disposable TeX Live 2022.08/Biber 2.18 | 1 | about `114 s` | Ran through repository stage 8, then failed only the Latin-`u` PDF probe. |
| Same wrapper with full disposable TeX Live 2022.04/**Biber 2.17**, matching the recorded Biber generation | 1 | about `135 s` | Ran all substantive minimal/full-replay stages and document builds; failed only `supplement PDF lacks unambiguous Latin near-threshold parameter`. **No completion marker.** |
| Patched PDF audit in the last disposable copy only | 0 | `1.13 s` | Replacing the literal phrase check with `with\s*u\s+the\s+Latin\s+letter` passed. Packet source remained unchanged. |
| Minimal verifier replay | 0 | `43.28 s` | `MINIMAL_VERIFIER_PASS`; duplicate implementation, not independent proof. |
| `python RUN_ALL_VERIFIERS.py repository` | 0 | `89.05 s` | All 38 entrypoints exited zero under assertions-enabled Python. |
| Pytest suite | 0 | `7.76 s` (`22 passed in 7.30 s`) | All supplied coefficient, endpoint, Fourier, source-value, and stale-profile mutations rejected. |
| Independent central exact checker | 0 | `26.50 s` | Reactions, SCCs, omissions, kernels, contractions, modulus equality, 76,560 falsification blocks, and endpoints through `m=149`. |
| Independent core checker rerun | 0 | `69.38 s` | Exact core reconstruction, 39,380 additional blocks, and outside-domain counterexamples. |
| Independent nonlinear/PDE checker final | 0 | `90.81 s` | Generic cubic bridge/signs, kernels/gauges, endpoints, and `m=149` regressions. |
| Manuscript/stale-claim audits | 0/0 | `0.12/0.12 s` | Passed source-level checks. |
| Numerical-provenance audit, supplied/regenerated | 0/0 | `0.37 s` each | Max relative refinements `1.6247e-8` and `1.4095e-8`, below `2e-8`. |
| PDF audit, host Python | 1 | `0.04 s` | Missing `pypdf`; **not a pass**. With disposable `pypdf==6.10.0`, supplied PDFs passed in `1.03 s`. |
| Exact JSON/table/sign generators | 0 | `0.43/0.27/0.29 s` | Exact artifacts regenerated byte-identically. |
| Six network and two scaled-family exporters | 0 | `1.40/0.59 s` | All JSON outputs byte-identical. |
| Full `simulations.py --jobs 3` | 0 | `8.15 s` | All 15 non-quick configurations passed; numerical output reproduced within tolerance, not bytewise. |
| Three Matplotlib figure generators | 0 | `1.47/1.70/1.12 s` | Completed; extracted text matched, with expected metadata/numerical raster differences. |
| Tectonic fallback, network/supplement/main | `0/0/1` | `2.76/3.18/3.93 s` | Supplemental only, not the advertised route. Main failed because local Biber 2.22 rejected the Tectonic BCF version. |
| Independent topology/cubic mutations | 1/1 | `<1 s` each | Both mathematically material mutations rejected. |
| Forced child exit 7 | 1 | `0.36 s` | Outer 38-runner propagated failure immediately. |
| `PYTHONOPTIMIZE=1` direct entrypoints | 0 | `0.98 s` | Three assertion-only scripts printed false `PASS`; orchestrated runners correctly rejected optimized mode. |
| Manifest mutation/control | expected fail then pass after rewrite | `0.4 s` | Old manifest rejected the mutation; replay-style manifest regeneration then self-certified the changed tree. |

### What all 38 entrypoints genuinely check

The complete line-by-line 38-row inventory is in
`agent_software_repro/SOFTWARE_REPRO_FINDINGS.md`. The concise classification
is:

| Entrypoints | Genuine evidentiary role |
|---|---|
| `dd_verify_contrast_bounds`, `verify_contrast_bounds`, `verify_stable_contrast`, `dd_verify_stable_contrast` | Finite exact evaluations of hard-coded selected-profile formulas; not general optimization proofs. |
| `dd_/verify_critical_profile`, `dd_/verify_harmonic_corrections`, `dd_/verify_cubic_sign` | Finite exact kernel/correction/contraction regressions at selected dimensions; cubic signs also check literal shifted polynomials. Full reaction-to-formula bridge is finite and shared. |
| `dd_/verify_diffusion_criterion`, `dd_/verify_order_m_minors`, `verify_network_one_bad_minor` | Finite exact matrix/minor checks, plus a symbolic `m=3` case; not the arbitrary-`m` iff/band proof. |
| `dd_/verify_mode_isolation`, `frontier_verify_mode_certificates` | Exact regeneration of 35/77/22/84-term certificate polynomials and equality anchors; determinant connection to actual matrices is finite, with the all-`m` chain bridge in the paper. |
| `verify_all_spectrum` | Symbolic triad Routh gap plus finite SCC/core determinant enumeration; not the all-dimensional graph proof. |
| `verify_principal_minor_diffusion_ray` | Exact finite mutation-sensitive examples; its source correctly disclaims being a substitute for the general proof. |
| `verify_family`, `verify_realization_space`, `frontier_verify_family` | Strong finite exact topology/rank/Jacobian/physical-scaling checks. |
| `frontier_verify_determinant_identity`, `frontier_verify_normal_form`, `frontier_verify_pareto`, `frontier_verify_pareto_curve` | Finite exact scaled determinant, normal-form, endpoint, and curve regressions. |
| `frontier_verify_cubic_bound`, `frontier_verify_exposition_identities`, `frontier_verify_mode_certificates` | Exact symbolic scalar/certificate and transcription-freshness checks, but several formulas are separately hard-coded copies. |
| `frontier_verify_master_certificate` | JSON/internal consistency against expected metadata; not reconstruction from reactions. |
| `frontier_verify_near_threshold` | Exact finite residual/formal-series checks; the key `m=3` polynomial is hard-coded. |
| `verify_current_numerical_provenance` | Independent finite reaction/Hessian reconstruction and exact finite solves against stored rows; one of the stronger finite-data checks. |
| `verify_branch_stability`, `verify_exchange_of_stability` | Finite floating-point spectral regression with stated tolerances; not nonlinear/PDE proof. |
| `verify_improved_profile`, `verify_mode_certificates`, `verify_pareto_family`, `verify_symbolic_certificates` | Fail-fast aggregates of children; no additional independent logic. |

Only the branch/exchange entrypoints use numerical eigensolvers; the
polynomial, rational, kernel, and minor scripts otherwise use exact SymPy or
`Fraction` arithmetic. Eight `dd_`/ordinary pairs are duplicate or nearly
duplicate layers, and four entrypoints are aggregates. The literal count 38 is
therefore coverage, not 38 independent implementations.

### Regenerated-artifact comparison

- Exact JSON, table, sign-certificate, network-instance, and scaled-instance
  artifacts regenerated byte-for-byte.
- Stored `integrated_designs.txt` has an extra successful `m=200` row that the
  current replay no longer requests. Stored `stale_claim_audit.txt` describes a
  larger historical tree. Both are provenance mismatches, not theorem evidence.
- Of 49 simulation files, 37 changed bytewise. The largest final amplitude
  difference was about `3.24e-9`, profile difference about `5.86e-9`, and
  transient difference about `4.28e-8`; all documented tolerance checks passed.
- All three Matplotlib PDFs changed bytes. The tradeoff figure was pixel
  identical at 200 dpi; the two simulation figures had small data/tight-box
  differences. Extracted text matched.
- Supplied manuscript PDFs report `xdvipdfmx`/Tectonic production, whereas the
  replay invokes `pdflatex`. The supplied PDFs are therefore not byte products
  of the stated engine route.

## D. Defects and exact repairs

No fatal, major, or minor mathematical defect was found.

| ID | Class | Defect/evidence | Exact repair | Effect on claims |
|---|---|---|---|---|
| D1 | **Reproducibility, minor but required** | The exact recorded TeX generation runs all substantive stages but fails `audit_pdfs.py:284,291`: pypdf extracts `withu the Latin letter` from the visibly correct source phrase. Current TeX also changes page count/layout probes. The unmodified wrapper never prints its completion marker. | Pin the complete TeX distribution/packages/engine, not only Biber; reconcile the scripted engine with the archived PDF producer; replace the literal phrase check by `re.search(r"with\s*u\s+the\s+Latin\s+letter", supplement, re.I)` (independently demonstrated to pass). If page count is intended as invariant, pin the layout stack; otherwise test content rather than page count. | No hypothesis, conclusion, endpoint, or headline change. |
| D2 | **Software/reproducibility, minor** | At least 21 direct entrypoints lack their own assertion-mode guard. Three reproduced false `PASS` under `PYTHONOPTIMIZE=1`, contradicting `independent_verifier/README.md:32-33`. Orchestrated paths are safe. | Add a shared explicit `if not __debug__: raise SystemExit(...)` guard to every public entrypoint, or narrow the README claim to guarded orchestration. | No mathematical change. |
| D3 | **Reproducibility/evidentiary description, minor** | Full cubic/harmonic contractions are checked only at six dimensions against hard-coded formulas; `dd_` twins share helpers; branch stability is finite floating regression. Aggregate `PASS` counts can overstate independent/all-dimensional evidence. | Add the generic recurrence-to-`R_m+C_m\mathfrak h_m` symbolic checker from this audit, label finite loops as regression, label duplicate/aggregate entrypoints, and rename/document branch stability as spectral regression. | No theorem change; strengthens evidence only. |
| D4 | **Reproducibility, minor** | `repository/replay.sh:109-111` rewrites its manifest from the regenerated tree and verifies that new manifest. This establishes self-consistency, not equality with the release baseline. Mutation reproduced the distinction. | Preserve the downloaded manifest separately and compare regenerated semantic/exact artifacts against it before writing a new manifest; label the final check as self-consistency. | No mathematical change. |
| D5 | **Expository** | The fixed-mass Fredholm/sectorial argument in Theorem 6.1 is compressed. It is correct, but the zero-mode restriction, nonzero Fourier modes, high-mode inverse bound, and restricted sectoriality should be explicit. | Add the four-part Fourier/Fredholm paragraph given in `agent_nonlinear_pde/NONLINEAR_PDE_FINDINGS.md`. | No hypothesis, conclusion, or headline change. |
| D6 | **Reproducibility/cosmetic** | Extra `m=200` and larger-tree stored logs, unused JSON schema, and release DOI metadata lag can be mistaken for current replay output. | Label all stored outputs with producing command/version and current-vs-historical status; update exact DOI metadata. | No mathematical change. |

Optional exposition improvements are to state explicitly that the `b=2a`
deleted edge lies in neither long cycle and to show the three-by-three remainder
in the full-`X` determinant elimination. These are clarity improvements, not
proof repairs.

## E. Scope, confidence, and remaining uncertainty

### What is proved or verified

The full mathematical result is valid within the manuscript's express scope:

- one indexed binary-complex classical mass-action topology for every `m>=3`;
- topology-wide localization over all positive equilibrium realizations;
- exact necessary-and-sufficient **stationary** diffusion crossing law for
  homogeneously stable realizations `(a,b,H)\in\mathfrak S_m`;
- local nonlinear positive stable branches for the selected unit and scaled
  profiles;
- a topology-specific stationary product lower bound and a within-family
  square-root design, not a global Pareto optimum.

### What was not claimed and was not inferred

I did not infer arbitrary-data global boundedness, far-from-onset attraction,
dimension-uniform robustness, arbitrary wave-instability exclusion, a result
for other networks, biochemical plausibility, an exact nonlinear contrast
infimum, constant-optimality, or a global Pareto frontier. Simulations remain
illustrations.

I did not reprove the general Crandall--Rabinowitz, Henry, or Kato theorems.
Their use was checked at the level appropriate for a referee: Banach/sectorial
spaces, smoothness, Fredholm index, one-dimensional kernel and cokernel,
transversality, reflection equivariance, isolated spectral projection,
complementary gap, and `H^1` Nemytskii regularity are present. The original
Crandall--Rabinowitz paper and the Henry monograph have the cited scope; the
classification is therefore “verified conditional on a cited standard
result,” not “computer verified.”

### Strongest remaining uncertainty

The strongest remaining mathematical uncertainty is ordinary reliance on the
cited local semilinear theory, not an identified hypothesis gap. The strongest
package uncertainty is the failed all-in-one completion marker and mismatch
between the archived PDF producer and scripted engine. Those are why the
verdict is not `VALID AS STATED`.

## Completion checklist

- [x] Outer and inner hashes verified before execution.
- [x] Main manuscript and supplement read completely.
- [x] Independent theorem-dependency map constructed.
- [x] Central claims checked against exact hypotheses and scope.
- [x] All-dimensional proofs separated from finite evidence.
- [x] Every load-bearing verifier/generator/audit/replay source inspected before output was trusted.
- [x] Circular/self-comparison and shared-hard-code checks sought explicitly.
- [x] Exact arithmetic separated from floating-point evidence.
- [ ] Full unmodified all-in-one replay completed: **no**. It fails at the final PDF semantic probe even in the documented TeX/Biber generation; all earlier substantive stages run. A one-line disposable regex repair passes the PDF audit.
- [x] Minimal replay completed.
- [x] All 38 verifier entrypoints run.
- [x] Exact tests, supplied and independent mutations, source/manuscript/stale/numerical audits run.
- [x] PDF audit run on supplied PDFs; regenerated-document PDF failure disclosed and diagnosed.
- [x] Tables and representative formulas traced to definitions.
- [x] Small-dimensional reconstructions performed independently.
- [x] Endpoint, exceptional-dimension, high-`m`, and equality cases checked.
- [x] Counterexamples actively sought inside and outside stated domains.
- [x] Simulations treated only as numerical evidence.
- [x] Functional-analytic stability argument assessed separately.
- [x] Every incomplete or failed stage disclosed.
- [x] Technical validity separated from journal recommendation.
- [x] No conclusion inferred solely from stored logs or passing software.

## External standard-result checks

- M. G. Crandall and P. H. Rabinowitz, “Bifurcation from Simple Eigenvalues,”
  *Journal of Functional Analysis* 8 (1971), 321--340:
  https://www.sciencedirect.com/science/article/pii/0022123671900152
- D. Henry, *Geometric Theory of Semilinear Parabolic Equations*, Springer LNM
  840: https://link.springer.com/book/10.1007/BFb0089647
- T. Kato, *Perturbation Theory for Linear Operators*, Springer:
  https://link.springer.com/book/10.1007/978-3-642-66282-9
- R. A. Satnoianu, M. Menzinger, and P. K. Maini, indexed abstract supporting
  subsystem orders through `n-1`: https://pubmed.ncbi.nlm.nih.gov/11196582/
- A. Anma, K. Sakamoto, and T. Yoneda, three-component steady/wave comparison:
  https://www.jstage.jst.go.jp/article/kodaimath/35/2/35_215/_article/-char/en
