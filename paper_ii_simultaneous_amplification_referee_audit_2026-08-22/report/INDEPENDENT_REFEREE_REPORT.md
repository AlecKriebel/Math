# Independent referee report

**Manuscript:** *A fitness-independent family of simultaneous amplifiers beyond relative fitness 3/2*
**Package date:** 2026-08-22
**Audit date:** 2026-08-22 (America/Los_Angeles)
**Audit basis:** complete manuscript/source reading, independent mathematics, source inspection before execution, canonical replay/rebuild, fault injection, and alternative exact and finite-state calculations.

## Recommendation

**valid after minor corrections**

The main theorem is supported. I found one genuine but localized error in two unstopped pendant waiting-time displays: the expectations can be infinite on the positive-probability extinction event. The later proof already uses the corresponding stopped time, and the preceding comparison proves the stopped estimate needed downstream. Correcting the stopping boundary changes no asymptotic rate, graph choice, response function, or theorem statement.

The verifier package also has a high-impact reliability defect: all 58 mathematical checks are bare Python `assert` statements, so optimized Python can erase them and still print `PASS`. A disposable mutation test reproduced that false pass. The canonical run had optimization disabled, every encoded identity was independently checked, and the mathematical proof was not inferred from program output; therefore this software flaw does not undermine the theorem. It must nevertheless be corrected in a revised referee package.

## Scope, independence, and evidence handling

- I treated the manuscript, comments, expected output, manifests, hashes, provenance statements, and research logs as claims rather than evidence.
- I made a byte-preserving disposable copy and did all execution and mutation testing there. The delivered copy passed a post-run manifest check unchanged.
- I read all 20 PDF pages and all 1,615 LaTeX lines, including declarations, limitations, and references. Page-by-page visual inspection found no clipping, overlap, missing glyph, broken figure, or illegibility.
- I read every delivered shell/Python entry point, every project import, the dependency file, build scripts, release script, and four certifiers before running them.
- No person was contacted, no file was uploaded, and no external system was changed. Network use was limited to the configured Python package index, Tectonic resources needed for the rebuild, the stated Git remote for the optional tag check, and read-only primary-source literature checks.
- The complete command ledger is `../logs/commands.tsv`; the corresponding combined stdout/stderr record is `../logs/full_transcript.log`. These files include diagnostic mistakes, expected fault-injection failures, corrected reruns, exit statuses, and environment probes rather than only successful commands.

## Package and environment record

### Identity and completeness

| Item | Independent result |
|---|---|
| Whole-package manifest | Pass: all 29 listed payloads match; the payload set is exact; all nodes are regular files. |
| Detached archive checksum | Pass: `ce62bfbdb22681ba48b2a04653155b2e06f52659f140c13f5e0220db365b9250`. |
| Archive structure | Pass: exactly 19 unique, sorted, safe regular members; no absolute paths, traversal, links, devices, or duplicate names. |
| Internal manifest | Pass: it covers exactly the other 18 members and every digest matches. |
| Fresh extraction | Pass: byte-identical to the delivered extracted tree. |
| PDF identity | Pass: convenience and archived PDFs are byte-identical, SHA-256 `f68142b3d99b95f83ca6ba4688539cb9e0fdb88ed96809aef5316ed22a59888f`. |
| Rebuild | Pass: the canonical release route reproduced both archive and PDF byte-for-byte. |
| Local tag | Annotated tag `simultaneous-amplification-beyond-three-halves-v2.0.1` peels to `2302d7c6ae17fc061a985da322df6d0600b66672`. |
| Remote tag | The remote annotated tag object `abad2dd24cceae62fde4b69a2ad95510e24350b2` peels to the same commit. |
| Tag/tree binding | Pass: all 17 repository-backed archive files match the named commit's blobs and executable modes. The synthesized metadata/manifest agree with the committed builder. |
| Residual provenance limitation | The annotated tag is unsigned; remote transport/account integrity, rather than an independently verifiable signer key, authenticates it. |

### Runtime environment

| Component | Observed value |
|---|---|
| Operating system | macOS 26.5.2, build 25F84; Darwin 25.5.0 |
| Architecture | arm64, Apple T6000 |
| Shell | zsh on the normal user account |
| Python | CPython 3.14.6 at `/opt/homebrew/bin/python3` |
| SymPy / mpmath | 1.14.0 / 1.3.0 in disposable virtual environments |
| Tectonic | 0.16.9 |
| Poppler | 26.08.0 (`pdfinfo`, `pdftoppm`) |
| Git | 2.38.2 |
| `PYTHONOPTIMIZE` in canonical run | Unset |

### Command and exit-status summary

Every command and status is in the two logs named above. The substantive execution record is:

| Operation | Result | Exit status / evidence |
|---|---|---|
| Independent outer, detached, and internal manifest checks | Pass | 0 |
| Safe-member and byte-identical fresh-extraction audit | Pass | 0 |
| Local and remote tag resolution; 17 blob/mode comparisons | Pass after one corrected diagnostic command | 0 on corrected run |
| PDF metadata extraction and 20-page rendering | Pass | 0 |
| Page-by-page visual inspection | Pass | All 20 rendered pages inspected |
| Prescribed `BOOTSTRAP_PYTHON=/opt/homebrew/bin/python3 ./run_all_referee_checks.sh` | Pass | 0; approximately 21.7 seconds |
| All delivered certifiers in canonical replay | Pass | 0 |
| Deterministic archive and PDF rebuild comparisons | Pass | 0; exact hashes above |
| Independent standard-library cross-checks | Pass | 0 |
| Independent response/root/quantifier calculation | Pass in exact-dependency venv | 0 |
| Independent small-chain stochastic calculation | Pass | 0 |
| Mutated expected identity, ordinary interpreter | Correctly failed | 1, expected |
| Same mutation/replay with `PYTHONOPTIMIZE=1` | Incorrectly passed | 0, reproducing CODE-01 |

Non-substantive nonzero records are retained in the logs. They include absent optional contact-sheet tools followed by successful page-by-page inspection; unset-environment probes; base interpreters lacking the pinned symbolic dependencies followed by the successful disposable-venv run; an expected normal fault-injection failure; and two malformed diagnostic invocations immediately corrected. None represents an uncompleted required check.

## Central theorem and quantifier ledger

The theorem's quantifiers are:

\[
\exists\{G_t\}_{t\ge1}\;\forall r\in(1,R_{\rm hyb})\;\exists t_0(r)\;
\forall t\ge t_0(r):
\rho_{\rm Bd}(G_t,r)>\rho_{\rm Bd}(K_{|G_t|},r)
\text{ and }
\rho_{\rm dB}(G_t,r)>\rho_{\rm dB}(K_{|G_t|},r).
\]

The graph sequence, including its least-dyadic cut, is chosen before fitness is quantified. The sufficiently-large threshold may depend on the fixed fitness. The endpoint is not claimed. The population scales are `C=t^4`, `q=t`, `m=floor(lambda_* t)`, `eta=q/C=t^-3`, and `n=C+m+2q`; hence `m/q -> lambda_*` and the normalized gain scale is `Theta(n^-3/4)`. I found no fitness-dependent graph choice or illicit exchange of the weak-cut, population, and fixed-fitness limits.

## Theorem-by-theorem validation

| Claim or proof component | Status | Independent reasoning or check | Location | Finding |
|---|---|---|---|---|
| Main theorem and `R_sim >= R_hyb > 3/2` | Supported after MATH-01 | All analytic dependencies, exact algebra, compact-uniform response transfer, and graph-independent quantifiers check; MATH-01 supplies the stopped form actually used. | Theorem 3, PDF p. 5; proof p. 18; `main.tex:324-336,1348-1357` | MATH-01 only |
| Model and complete-graph baselines | Verified | Direct derivation of labelled Bd/dB rates; exact birth-death products reproduce both same-order complete-graph formulas for multiple `n`. | PDF pp. 2-3, Eqs. (1)-(6); `main.tex:141-199` | None |
| Definition and quantifier order | Verified | One family is selected independently of `r`; fixed-`r` eventuality and the open endpoint are used consistently. | Definition 1, PDF p. 3; `main.tex:191-199` | None |
| Effective graph construction | Verified | Finite, loopless, undirected, connected for every positive dyadic cut; all stated edges positive; scales and module counts agree. Finite absorption systems are rational functions with positive denominators; compact convergence and exact real-algebraic comparison make the least dyadic choice effective. | Lemma 2, PDF pp. 3-4; `main.tex:203-225,276-322` | No complexity bound is claimed or needed |
| Strong orbit lumping | Verified | The weight-preserving automorphism group acts transitively on each `(h,i,u,v,ell)` fibre and transports ordered replacement events with equal rates for both rules. A distinct rational instance also passed exact orbit-row comparison. | Lemma 4, PDF p. 5; `main.tex:341-366` | Supplied nine-vertex enumeration is corroboration, not the general proof |
| Weak-cut trace | Verified | At zero cut, every fast mixed state is transient; the row-oriented reduction is `A+B(I-Q_0)^{-1}C_0`, representing one weak introduction followed by exact local absorption. Nonsingular finite macro interiors and compact continuity give uniform convergence. | Proposition 5, PDF pp. 5-6; `main.tex:368-441` | No independent-lineage substitution |
| Early establishment | Verified | Re-derived stopped embedded-walk odds and `O(K^2/C)+O(r^{-K})` errors for `K=ceil(A_0 log C)`. | Lemma 7, PDF pp. 7-8; `main.tex:499-543` | None |
| Completion and core confinement | Verified | Conditional intensities, exponential supermartingales, compensator count, nested strips, and polynomial-horizon escape prefactor check uniformly in hidden hub/leaf states. | Lemma 8, PDF pp. 8-9; `main.tex:544-660` | None |
| Bd cleanup | Verified after local stopping correction | Renewal monotonicity, effective pendant up/down bias, deficit drift, hub-survival integral, conditional block success, and strong-Markov geometric recursion check. The recursion needs no independence. | Lemma 9, PDF pp. 9-12; `main.tex:662-859` | MATH-01 at Eqs. (25)-(26) |
| dB cleanup | Verified | With `T=beta_0 log C`, the two errors are `O(C^{1/4-beta_0})` and `O(C^{-kappa beta_0})`; the displayed choices give `O(C^{-B_0-2})`. The deactivation integral is `O((R_0/kappa+m)/C)=O(C^{-3/4})`, with no harmful `T` factor. | Lemma 9, PDF pp. 12-13; `main.tex:861-895` | None |
| Pendant initialization | Verified | The graphical deletion/suppression coupling is attractive; Bd trial success/loss scales give `o(1)` loss before regeneration success, while dB hub activation before singleton-leaf death is `O(C^-1)`. | Lemma 9, PDF p. 13; `main.tex:897-932` | None |
| Reciprocal killed-Green estimate | Verified | Product odds, stopped Dynkin particle-time, exponential Green tail, and hub-change hazard give the stated bounds. | Lemma 10, PDF p. 13; `main.tex:934-995` | None |
| Reciprocal renewal | Verified | The dB immigration-death Lyapunov bound uses finite horizons in the correct order; the refined renewal inequality first yields `limsup Cx_{C,1} <= a exp(-theta L)` and then sends `L` to infinity, proving little-`o(C^-1)`. | Lemma 11, PDF pp. 14-15; `main.tex:997-1119` | None |
| Gate rates and global sweep | Verified | Direct event sums give all four directional rates and `Z_B=sigma(r^2-1)`, `Z_D=2r(r-1)/sigma`. Adverse reversals are retained; their union bound is `o(q/C)`. | Proposition 12, PDF pp. 16-17; `main.tex:1142-1247` | None |
| Response expansion | Verified | Independent first-order expansion accounts for center, pair, pendant, population denominator, and complete-graph baseline terms on the common `eta=q/C` scale. Denominators are positive. | Proposition 13, PDF p. 17, Eqs. (41)-(44); `main.tex:1249-1290` | None |
| Sextic feasibility and tangency | Verified | Independent exact arithmetic gives the feasibility gap, convex minimizer, discriminant sextic, Sturm variations `(4,4,3)`, exact endpoint signs, and monotonicity. | Lemma 14, PDF pp. 17-18; `main.tex:1292-1346` | None |
| Fixed-response optimality | Verified within stated scope | The obstruction applies to fixed positive pair-pendant response parameters, not singular/size-dependent choices or all graph families; the text states this limitation. | Proposition 15, PDF p. 18; `main.tex:1359-1382` | None |
| Rational specialization | Verified | Exact margins at `r=3/2` are `232/17361` and `65/12123`; the algebraic threshold and strict endpoint comparison check. | Corollary 16, PDF pp. 18-19; `main.tex:1384-1416` | None |
| Final diagonal transfer | Verified | For fixed interior `r`, eventually `r in I_t`; the dyadic scaled error is at most `1/t`, while both separated scaled gains tend to positive constants. | Theorem proof, PDF p. 18; `main.tex:1348-1357` | None |

## Independent numerical and exact cross-checks

These calculations did not import delivered verifier code.

- Complete-graph Bd and dB fixation formulas were checked for several orders and rational fitnesses.
- A different hybrid graph (`C=4`, one pair, one pendant, `sigma=2/5`, `epsilon=1/17`, `r=7/4`) gave exact equality of every labelled aggregate row within each orbit fibre under both update rules.
- A standard-library rational Sturm calculation found zero roots of the sextic in `(1,3/2)` and one in `(3/2,151/100)`, with
  `P(3/2)=1/64` and `P(151/100)=-39866792399/10^12`.
- Bisection gave
  `R_hyb=1.5028569127905696267...`,
  `sigma_*=0.13067728228704837686...`, and
  `lambda_*=0.75080648303188049230...`.
- Exact gate/response calculations reproduced both rational margins above.
- An independently implemented 512-state finite chain reproduced the 108 orbit fibres for each rule, both center intensity tables on 256 states, and monotone convergence to the separated weak-cut trace at `epsilon=10^-1,...,10^-4` for a separate small graph.

## Claim-to-code coverage and execution

| Program | Intended claim | Source-audit result | Execution result | Exact coverage limitation |
|---|---|---|---|---|
| `certificates/verify_leading_algebra.py` | Sextic/root/tangency identities | Exact SymPy algebra and Sturm logic; 11 bare asserts | Pass canonically | Checks encoded algebra only; CODE-01 under optimization |
| `certificates/verify_hybrid_lumping.py` | Finite labelled/orbit aggregation | Exhaustive 512 masks and 108 fibres at one rational nine-vertex instance; one loop assert | Pass canonically | Tests orientation/aggregation at one instance, not arbitrary-size lumpability or asymptotics |
| `certificates/verify_hybrid_coefficients.py` | Gate, response, rational, and phase identities | Exact symbolic/rational arithmetic; 21 bare asserts | Pass canonically | Reduced leading rates are inputs; does not derive stochastic portal asymptotics |
| `verify_paper_claims.py` | Integration/marker and duplicate algebra audit | 25 bare asserts; marker checks correctly recognized as textual regression checks | Pass canonically | Not a proof checker; no semantic theorem or stochastic verification |
| `verify_referee_package.py` | Package/archive consistency | Fail-closed explicit exceptions; safe regular members and bytes checked | Pass | Does not bind a Git tree/signature or extracted executable modes |
| `run_all_referee_checks.sh` | End-to-end replay/rebuild | Safe guarded temporary tree, strict tool gates, `set -eu`, and byte comparisons | Pass; exact rebuild | Does not reject optimized Python; inherits CODE-01 |
| `bootstrap_replay.sh` / `replay.sh` | Dependency bootstrap and four-certifier sequence | Failures propagate under ordinary execution; version gates themselves use asserts | Pass | Downloads version-pinned but not hash-pinned artifacts; optimization can erase checks |
| `build.sh` / `release_bundle.sh` | PDF/archive rebuild | Deterministic route succeeded; deletion target is scoped to rendered pages | Pass; byte-identical | Release archive builder calls bare `python3`, not the selected bootstrap interpreter |
| Independent audit programs | Alternative finite chains, response algebra, rational Sturm and archive safety | Separate implementations; standard library except exact response script in the pinned venv | Pass | Corroboration at finite samples; analytic infinite claims were checked by derivation, not extrapolation |

## Findings

### MATH-01 — Minor mathematical correction — unstopped pendant expectations can be infinite

**Location:** Lemma 9, PDF p. 10, Eqs. (25)-(26); `main.tex:728-755`, especially `eq:leaf-wait` and `eq:leaf-hitting-time`.

The manuscript defines successive pendant-count change times and states an unconditional conditional inter-change mean bound, followed by

\[
\sup_{R\le 2\delta c}\mathbb E\tau_{\ell=m}=O(Cm).
\]

As written, this is false. From, for example, `R=1`, resident hub, and `ell=0`, a finite sequence of resident replacement events reaches global extinction with positive probability before another pendant change or before `ell=m`. At extinction those events never occur, so the relevant time is infinity on a positive-probability event and its expectation is infinite.

The required replacement is local. Define

\[
\tau_\uparrow=\inf\{s:R_s\ge2\delta c\},\qquad
\Sigma=\inf\{s:(h_s,\ell_s)=(1,m)\text{ or }R_s\ge2\delta c\}.
\]

Stop each phase at the next pendant change **or** `tau_up`; assign upper-strip exit the terminal top level in the adapted pendant comparison. The preceding worst-rate committor calculation still gives uniformly favorable up-or-exit/down odds greater than one. Optional stopping of the bounded truncated level process gives `O(m)` actual pendant changes before `ell=m` or exit, and the phase calculation gives `O(C)` conditional mean time per outcome. If a block begins at `(h,ell)=(0,m)`, activation, loss, or exit has bounded mean; activation/exit ends the block and a loss restarts from `m-1`. Hence

\[
\sup_{R\le\delta c}\mathbb E\Sigma=O(Cm).
\]

Every later use at `main.tex:782-785,802-809,824-854` is already stopped at `(h,ell)=(1,m)` or the upper strip and charges strip exit separately through core confinement. Thus the corrected estimate proves exactly what the block recursion needs. No theorem statement or scale changes.

### CODE-01 — High verifier reliability; small remediation — optimized Python erases all mathematical checks

**Locations:**

- `certificates/verify_leading_algebra.py:15-66` — 11 asserts;
- `certificates/verify_hybrid_lumping.py:159` — the sole assert inside the exhaustive loop;
- `certificates/verify_hybrid_coefficients.py:16-106` — 21 asserts;
- `verify_paper_claims.py:32-154` — 25 asserts;
- `bootstrap_replay.sh:9-12,23-29` — assertion-based version gates;
- `replay.sh:1-21` and `run_all_referee_checks.sh:1-76` — no optimization rejection.

Python removes `assert` statements under `-O` or `PYTHONOPTIMIZE`. Each certifier prints its success message after the assertions. In a disposable replay copy with an impossible injected assertion, ordinary `./replay.sh` exited 1, while

```sh
PYTHONOPTIMIZE=1 ./replay.sh
```

exited 0 and printed every `PASS` line. An independent mutation of the expected Bd margin behaved the same way. The canonical run was not optimized and independently checked results agree with it, so this is not evidence of a wrong calculation; it is a soundness failure in the certificate harness.

**Required correction:** replace every verification-critical assert with an explicit conditional that raises a nonzero exception, explicitly reject `sys.flags.optimize != 0`, and rerun the fault-injection test. Isolated mode and a sanitized environment are additional hardening, not substitutes for explicit checks.

### CODE-02 — Medium software/provenance limitation, independently resolved here — standalone verifier does not bind Git identity

**Location:** `verify_referee_package.py:23-24,149-161`; `BUNDLE_METADATA.txt:1-14`.

The standalone verifier checks that hard-coded commit/tag strings occur in metadata; it does not reconstruct the Git tree or resolve a tag. Independent local/remote resolution and 17 exact blob/mode comparisons resolved the claimed source binding for this audit. The remaining limitation is the unsigned tag. A stronger handoff should include and verify a signed tag or a separately authenticated source attestation.

### REPRO-01 — Medium reproducibility limitation — dependency artifacts are not frozen offline

**Location:** `bootstrap_replay.sh:18-21`; `requirements.txt:1-2`; `README_FIRST.md:3,61-66`.

SymPy 1.14.0 and mpmath 1.3.0 are version-pinned, but their wheels/sdists and hashes are not included. Tectonic resources are also external. The base interpreter lacked these packages, so the authorized canonical run downloaded them from the configured index. The run succeeded and exact product hashes detect divergent results, but the delivered bytes alone are not an offline-hermetic build despite the opening “self-contained” description. Vendor hash-pinned distributions and a pinned Tectonic resource bundle for a stronger archival package.

### REPRO-02 — Medium portability limitation — archive rebuild ignores `BOOTSTRAP_PYTHON`

**Location:** `run_all_referee_checks.sh:5,16,53`; `release_bundle.sh:17-19`; `bundle_manifest.py:155-165`.

The bootstrap honors the selected Python 3.14.6 interpreter, but the release script invokes bare `python3` for the deterministic archive builder. On this host bare `python3` was the required interpreter and the archive matched exactly. On a host that needs the documented `BOOTSTRAP_PYTHON` escape hatch, archive bytes could be generated by another implementation/version or the command could be absent. Pass the selected interpreter through or invoke the created venv interpreter explicitly.

### CODE-03 — Low integrity-scope limitation — standalone verifier omits extracted modes

**Location:** `verify_referee_package.py:62-81`; `bundle_manifest.py:136-141`; `run_all_referee_checks.sh:54-58`.

The standalone verifier checks nodes and bytes but not permission bits. The full rebuild-and-compare route does catch mode changes through tar metadata, and delivered modes match. Extending the standalone verifier to check expected executable modes would remove the gap.

## Proof-software consistency

The manuscript and `CLAIM_CODE_MAP.md` are candid about the certificate boundary. The finite lumping program checks one rational nine-vertex instance; the symbolic programs check already-encoded exact algebra; the marker program is not described as a proof checker; and the weak-cut and stochastic asymptotics remain analytic. I found no manuscript conclusion that silently relies on a program outside that stated boundary.

The proof and canonical outputs support the same formulas. The software does not, by itself, support the infinite-size theorem, and I have not credited it with doing so. CODE-01 means that a raw `PASS` transcript is not trustworthy unless optimization is known to be disabled; this audit established that fact for the canonical run and independently re-derived the load-bearing results.

## Literature and positioning check

The literature check was contextual rather than evidence for the proof. Primary sources support the manuscript's broad positioning: Svoboda et al. report a previous fitness-independent simultaneous interval only up to `r<1.2`; Tkadlec et al. establish strong restrictions on death-Birth amplification, including weighted graphs; and Brewster et al.'s 2026 mixed-update model is mathematically distinct from requiring both pure Bd and pure dB inequalities on one family. A targeted search found no public paper with the same pair-pendant construction or the claimed `1.502856...` threshold. This is not an exhaustive priority search.

- Svoboda et al., PLOS Computational Biology (2024): https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1012008
- Tkadlec et al., PLOS Computational Biology (2020): https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1007494
- Brewster et al., ITCS 2026: https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/html/LIPIcs.ITCS.2026.29/LIPIcs.ITCS.2026.29.html

## Unresolved assumptions and limitations

- The tag is unsigned, so I cannot independently authenticate a signer; I did independently verify local/remote resolution and every repository-backed archive blob.
- Downloaded SymPy/mpmath artifacts and the Tectonic resource bundle were not supplied or source-audited. Their versions were checked, and all mathematical outputs were independently cross-checked where they were used.
- The revised manuscript/package containing MATH-01 and CODE-01 fixes does not yet exist, so I could validate the repairs but could not replay the revised artifact.
- The targeted literature search was not an exhaustive novelty or priority search.
- No endpoint claim at `r=R_hyb`, uniformity as `r` approaches 1, singular/size-dependent response optimization, or explicit bound on the least dyadic exponent is made; I did not treat these excluded scopes as gaps.
- There is no machine-formal proof. The arbitrary-size and asymptotic statements were assessed by independent derivation, with finite programs used only as corroboration.

No required mathematical, source-inspection, execution, or alternative-cross-check task remains unperformed.

## Supporting audit artifacts

- `../work/THEOREM_LEDGER.md` — full hypothesis, scale, uniformity, dependency, and quantifier ledger.
- `../independent_checks/stochastic_math_audit.md` — line-by-line stochastic derivation and stopped-time repair.
- `../independent_checks/response_quantifier_audit.md` — independent exact response, sextic, rational-edge, and final-quantifier audit.
- `../independent_checks/package_code_audit.md` — package/source inventory, Git binding, code audit, canonical run, and mutation tests.
- `../independent_checks/adversarial_reconciliation.md` — hostile attempt to falsify the repair and load-bearing interfaces.
- `../independent_checks/independent_cross_checks.py`, `../independent_checks/stochastic_math/audit_small_chains.py`, and `../independent_checks/response_math/independent_response_audit.py` — independent check programs.
- `../logs/commands.tsv` and `../logs/full_transcript.log` — every recorded command, status, version query, calculation, and transcript.

## Required revision checklist

1. Replace the two unstopped displays in Lemma 9 with the stopped `tau_up`/`Sigma` formulation above and make the already-used downstream stopping boundary explicit.
2. Replace all verification-critical Python asserts with explicit exceptions, reject optimized mode explicitly, and include a mutation/failure-propagation regression test.
3. Route the selected bootstrap interpreter into the archive builder.
4. Clarify that the package is network-reproducible with version-pinned dependencies, not offline self-contained; preferably vendor hash-pinned artifacts.
5. Optionally strengthen standalone verification of Git identity/signature and executable modes.

## Final rationale

The only mathematical error is a missing stop in two intermediate expected-time statements, with a direct stopped-time repair supported by the immediately preceding estimates and matching every downstream use. Independent derivations validate the model, orbit lumping, weak-cut trace, stochastic scales, reciprocal little-`o` bounds, gate sweep, response algebra, sextic optimization, rational case, and diagonal quantifiers. The canonical package replay completed and reproduced both deliverables exactly. The optimized-assert flaw is serious for certificate trust but easy to remediate and did not carry this review's mathematical conclusion. The appropriate disposition is therefore the recommendation stated at the beginning.
