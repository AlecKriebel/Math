# Hostile independent submission-readiness audit: Paper II v2.0.2

**Audit date:** 2026-08-22

**Recommendation:** **READY** for scientific submission / independent referee review.

**Completion:** **100% of the assigned offline, nonvisual scope.**  The main agent reserved page-image inspection; I read the complete 21-page PDF text and all 1,660 lines of the revised LaTeX.  External authentication and human declarations remain inherently outside an offline audit.

## 1. Scope and evidence convention

I treated the manuscript, response letter, research logs, expected output, manifests, and source comments as claims.  I did not use the network, modify the delivered copy or source repository, contact anyone, upload, push, or release anything.  Every shell command is in `logs/full_transcript.log` and `logs/commands.tsv` under an `agent-v202-adv-*` label.

Abbreviations used below:

- `D` = `/Users/alec/Documents/Math/paper_ii_simultaneous_amplification_submission_recheck_v2_0_2_2026-08-22/delivered_copy`
- `P` = `D/source_and_certificates/universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold`
- `T` = `P/main.tex`
- `R` = `/Users/alec/Documents/Math-universal-amplification/universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold/submission/REFEREE_RESPONSE_2026-08-22.md`

Severity terminology: **blocking** means not ready; **minor** means a real correction that should normally be made but does not undermine the result; **low/optional** means a nonblocking documentation defect or improvement; **informational** records a limitation already correctly scoped.

## 2. Executive result

I found **no blocking, major, or mathematical defect** in v2.0.2.  The response letter's six accepted dispositions are borne out by the revised proof, source, package, and executed clean-room replay.  The only new concrete defect I found is a **low-severity broken documentation cross-reference** in the newly added wheel provenance note.  It does not affect proof, replay, package identity, or the correctly repeated reproducibility boundary, so it does not justify reopening the frozen scientific version.

The stopped-time repair is rigorous, including the exact `(h,ell)=(1,m)` target and every later use of equation (26).  I found no remaining statement of an infinite unconditional pendant-hitting expectation and no analogous unstopped expectation elsewhere in the manuscript.

## 3. Findings

### F-01 — Low/optional documentation defect: archived wheel note points to an omitted file

**Evidence.** `P/vendor/README.md:24-27` says the external document-tool boundary is described in `submission/ENVIRONMENT.md`.  The public 23-member source archive deliberately excludes the whole `submission/` directory, and the target is absent from both `D/source_and_certificates/` and the inner tar.  Logged check: `agent-v202-adv-broken-crossref-confirm`.

**Impact.** The cross-reference works in the development repository but is broken in the artifact where `vendor/README.md` is actually delivered.  No reproducibility information is lost: the same boundary is stated in `P/README.md:51-62`, `D/README_FIRST.md:75-82`, `D/VERSION.md:20-23`, `D/source_and_certificates/BUNDLE_METADATA.txt:13-15`, and `T:1515-1519`.

**Suggested correction.** In a future documentation-only version, point to `../README.md` (or another file actually retained in the archive).  I regard this as nonblocking.

### I-01 — Informational provenance layering: the final response-letter identity paragraph is post-tag

`R:57-60` names commit `03e94e...`, tag `...v2.0.2`, and tag object `be3946...`.  Those four lines were added in wrapper commit `0dcb450a...`, whose direct parent is the tagged scientific commit `03e94e...`; they are not themselves in the scientific tag.  This is expected because the final tag object could only be recorded after creating the tag.  The response letter is a submission-handoff file, not one of the 21 Git-bound scientific blobs, and the delivered neutral package omits it.

The values themselves are correct: local tag-object inspection peels `be3946...` to `03e94e...`; `verify_git_binding.py` matches all 21 archived blobs and modes; the delivered wrapper tree is byte-identical to the repository wrapper; and the outer tar is byte-identical to the committed wrapper tar (independently computed SHA-256 `2216c6a31545b38d9ca89c9d43c5a309bfcc6c2c1f7ab63ea5fabc171116e1d2`).  This layering must not be described as authenticating the post-tag response letter, but neither the letter nor package makes that stronger claim.

### I-02 — Informational neutrality caveat: transparent, not psychologically blind

The package excludes the response letter, hostile-audit ledgers, submission correspondence, and saved successful output.  The neutral prompt explicitly allows all five verdicts and says author conclusions/logs/hashes are claims, not evidence (`D/REFEREE_PROMPT.md:3-9, 192-217`; `D/README_FIRST.md:50-53`).  The file-set search found no forbidden response/submission/audit material in the delivered tree or inner archive.

The retained chronological `RESEARCH_LOG.md` does summarize earlier favorable and unfavorable audits (`P/RESEARCH_LOG.md:96-105, 188-224, 226-245`).  That could anchor a human reader, but it is openly disclosed and includes the later counterexample that overturned an earlier clean verdict.  Thus the handoff is epistemically neutral, although a maximally outcome-blinded variant would also omit the research log.  This is not a correctness or readiness defect.

## 4. Exact issue-closure audit against the response letter

| Response item | Status | Independent evidence and boundary |
|---|---|---|
| MATH-01: unstopped pendant waiting times (`R:11-30`) | **Closed** | Revised Lemma 9, `T:680-795`; PDF pp. 9-11, equations (24)-(26).  Full derivation below. |
| CODE-01: optimized Python / bare assertions (`R:32-45`) | **Closed** | AST scan found zero `ast.Assert` nodes in every delivered Python file and every relevant source Python file.  All entry points have explicit optimization guards.  The clean bootstrap's direct, optimized, early-mutation, late-mutation, and shell-propagation tests passed.  Direct `-O` tests of both outer verifiers and the private submission validator failed nonzero without success sentinels. |
| CODE-02: unsigned Git identity (`R:47-60`) | **Correctly limited** | Tag object, peeled commit, 21 blob/mode comparison all match.  Package and response repeatedly state that this does not authenticate signer, hosting account, checkout, or authorship (`D/README_FIRST.md:68-71,84-87`; `D/VERSION.md:20-23`). |
| REPRO-01: offline Python dependencies (`R:62-75`) | **Closed** | Both pure-Python wheels are included; hashes match requirements and wheel bytes; metadata gives mpmath 1.3.0 and SymPy 1.14.0; upstream license files are retained.  The clean runner installed them with package-index access disabled.  The PDF tool boundary remains explicitly non-hermetic. |
| REPRO-02: selected interpreter (`R:77-82`) | **Closed** | Source inspection shows one resolved Python is passed from bootstrap through replay and archive construction.  The complete delivered runner succeeded under Python 3.14.6 and reproduced both final hashes. |
| CODE-03: executable modes (`R:84-91`) | **Closed** | Package verifier checked expected `0644`/`0755` modes, safe regular members, and extracted byte/mode equality.  Independent outer-tar comparison found 35 sorted, unique, safe regular files exactly matching the 35 delivered files and modes. |

### 4.1 Rigorous re-derivation of the stopped-time repair

The relevant definition is

`tau_up = inf{s >= 0 : R_s >= 2 delta c}` (`T:680-681`).

1. **Stopped committor.** For fixed pendant count `ell`, the worst-rate two-hub-state committor is extended to value one on upper-strip exit (`T:695-708`).  Its explicit forms at `T:711-714` are increasing in `H_+` and `U_ell` and decreasing in `H_-`; direct differentiation confirms every sign.  Interior core jumps leave the function unchanged, while a boundary-crossing core jump contributes `rate*(1-p_h) >= 0`.  Hence it is subharmonic for the full stopped generator.

2. **Uniform favorable odds.** For `1 <= ell < m`, the from-resident-hub odds are

   `H_+ U_ell / [V_ell(H_-+U_ell)]`.

   The mutant-hub odds are larger.  Substitution of the stated worst rates gives equation (24), uniformly bounded below by `r_-^2/(1+2 delta)*(1-o(1)) > 1` (`T:719-729`).  At `ell=0` there is no downward pendant move.

3. **Expected stopped outcomes.** Define `xi = tau_{ell=m} wedge tau_up`, successive pendant-change-or-exit times `sigma_j`, and assign an exit the terminal trace level `m` (`T:731-742`).  If the up-or-exit/down odds are at least `beta>1`, then with `epsilon=(beta-1)/(beta+1)`,

   `hat_ell_{j wedge N} - epsilon (j wedge N)`

   is a bounded-above stopped submartingale.  Optional stopping at `N wedge k` gives `epsilon E(N wedge k) <= m`; monotone convergence gives `EN <= m/epsilon` (`T:743-753`).  There is no missing absorption event: from `R<2 delta c`, any path to global mutant extinction must cross the upper boundary, while for `ell<m` global fixation cannot occur before a pendant change.  Thus the stopped outcome occurs almost surely.

4. **Calendar time.** Before the upper exit, resident-hub phases have activation-or-loss intensity bounded below; mutant-hub phases with `ell<m` have deactivation-or-gain intensity at least one.  The outcome probability per phase is at least `c_0/C` (`T:755-768`).  At `ell=0`, the resident phase has no loss but ends by activation/exit and is grouped with the following mutant phase (`T:769-774`).  Core jumps neither pause these hazards nor change `(h,ell)`.  Therefore each phase has uniformly bounded conditional mean duration and the number of phases per outcome has conditional mean `O(C)`, proving equation (25) and `E xi=O(Cm)` (`T:775-782`).

5. **Exact target `(1,m)`, not merely `ell=m`.** If initially `h=1,ell=m`, the target is already hit.  If initially `h=0,ell=m`, activation, pendant loss, or upper exit has bounded mean; pendant loss wins with probability `O(C^-1)` (`T:782-786`).  Activation reaches `(1,m)`; exit reaches the alternative stop.  After a loss, the trace restarts at `m-1`, and its only way to return to `ell=m` is a gain event while `h=1`.  Therefore the return really is `(h,ell)=(1,m)`.  This proves the displayed supremum for `Sigma`, equation (26), over all allowed `h,R,ell` (`T:787-795`).  In the construction `m=floor(lambda_* t)>=1` for `t>=2`, so the vacuous `m=0` big-O boundary does not arise.

6. **Every later use of equation (26).** The only references are `T:824`, `T:846`, `T:864`, and `T:879-883`.

   - At `T:824`, Markov on `E Sigma=O(Cm)` over a `C^2` block gives failure `O(m/C)=o(1)`, since `m=o(C)`; core confinement charges the alternative upper exit.
   - At a regeneration time `S_j`, `R<=delta c`, so the strong Markov property and the state-uniform supremum give the conditional bound `E(Sigma_j-S_j | F_{S_j}) <= KCm` exactly as claimed at `T:843-848`.  No independence assumption is used.
   - At `T:863-877`, it is combined only with separately stopped cleanup, return, and nested-strip estimates to obtain uniform conditional block success/escape/duration bounds.
   - At `T:879-883`, the conditional mean `O(Cm)` is used with Markov and `D_*=B_0+4`; because `Cm=O(C^{5/4})`, the requested polynomial tail is more than sufficient.

### 4.2 Search for analogous infinite expectations

I enumerated every occurrence of `mathbb E`, expected/mean time, and hitting-time notation in the revised manuscript.  The remaining expectations are all one of:

- bounded stopping at finite count boundaries (`T:527-529`, `T:951-957`);
- finite-horizon entry counts controlled by a compensator (`T:629-635`);
- explicitly upper-exit-stopped deficit/cleanup times (`T:650-658`, `T:806-819`, `T:837-898`);
- killed Green integrals stopped at extinction or a macro boundary (`T:974-1034`);
- a finite-horizon immigration-process maximum (`T:1088-1109`); or
- a pure-death pendant particle-time integral after reactivation is suppressed (`T:1111-1117`).

I found no remaining unconditional expectation that can be infinite on a positive-probability absorption path.

## 5. Global submission claims

### 5.1 No changed theorem or new mathematical overclaim

The scoped v2.0.1-to-v2.0.2 diff has 26 changed files.  In `main.tex`, changes are confined to the stopped pendant proof and data/code availability/tag wording.  The theorem statement, graph scales and weights, effective diagonal, response functions, sextic, rational specialization, and quantifier order are byte-unchanged.  This supports `R:101-102`.

The revised manuscript states the quantifier order explicitly (`T:102-120,191-199,324-336`), restricts response optimality to fixed positive parameters (`T:1400-1422,1489-1498`), disclaims an endpoint theorem/universal upper bound, and notes that the gain is asymptotically small with no useful finite-size threshold (`T:1500-1505`).  I found no claim of uniformity as `r downarrow 1`, no amplification claim at `r=R_hyb`, and no claim that the finite programs prove stochastic asymptotics.

### 5.2 Declarations

The manuscript declarations at `T:1507-1562` are internally consistent with `submission/DECLARATIONS.md`: no empirical data, offline exact-certificate replay after Python is supplied, external PDF tools/resources, no new DOI, no funding, no competing interests, author responsibility, ethics not applicable, and substantive AI assistance.  The archive and executed runner substantiate the technical availability statements.

Funding, interests, contribution, authorship responsibility, and permission statements remain human attestations and cannot be proved from files.  The private submission handoff correctly labels them for human approval.  One administrative token, `[[POSTAL_ADDRESS]]`, intentionally remains in private cover-letter/metadata files and is excluded from the public scientific/referee archive; it must be filled by the author before an actual portal submission.

### 5.3 References

The LaTeX contains 12 distinct citation keys and 12 bibliography items; the sets are identical, with no missing or uncited entry.  The complete PDF rebuild reported no undefined citation/reference, and the PDF text contains the declarations and bibliography.  DOI/title accuracy and literature completeness were not checked online under the no-network mandate.  The manuscript and response appropriately call the search targeted rather than exhaustive and label prior project DOIs as unrefereed source/software releases.

### 5.4 Reproducibility scope and certificate boundary

The stated boundary is accurate:

- exact programs cover finite transition aggregation, exact symbolic/rational response identities, Sturm isolation, tangency, and rational margins;
- `verify_paper_claims.py` is only a marker/integration audit;
- general strong lumpability, weak-cut perturbation, establishment, cleanup, reciprocal invasion, population errors, and global sweep remain analytic arguments;
- Python, Tectonic, Poppler, and Tectonic resources are externally provisioned, while only the two Python libraries are vendored for offline installation.

AST import inspection found only standard-library imports plus SymPy; mpmath is SymPy's pinned dependency.  Wheel metadata and retained licenses are consistent with the documentation.  Without an external trusted source, the word “unmodified” in `vendor/README.md` remains a provenance assertion, not something internal hashes alone can prove.

### 5.5 Identity, hashes, and package binding

All current identity records agree:

- scientific commit `03e94e877ce10d9d459fd284bd652934cde08bb3`;
- annotated unsigned tag object `be3946c051c7f7e2073d6adf81bca31ae750251a`;
- tag `simultaneous-amplification-beyond-three-halves-v2.0.2`;
- source archive SHA-256 `d2145513f8abe295e9e7fab62f062fa9d0f7a6282de95e8155f3db4621485274`;
- PDF SHA-256 `4e86597bb0baff388e8ce7ccf6ffd808f86b5ea846acf6f2188b31016fd2572c`;
- 23 inner archive members = 21 repository blobs plus metadata and manifest;
- 21-page PDF;
- deterministic epoch `1787356800 = 2026-08-22T00:00:00Z`.

Historical v2.0.0/v2.0.1, 19-member, 20-page, and old commit markers occur only in dated chronological research-log entries, not current identity fields.  The outer tar has 35 sorted, unique, safe regular files and matches the delivered tree byte-for-byte and mode-for-mode.

## 6. Execution and adversarial tests

| Logged label | Result |
|---|---|
| `agent-v202-adv-package-verifier` | Exit 0: 34 payload hashes/modes, 23 inner members, extracted tree, convenience PDF, prompt, archive and PDF hashes all pass. |
| `agent-v202-adv-git-binding` | Exit 0: annotated unsigned tag and all 21 source blobs/modes match local checkout; tool prints authentication limitation. |
| `agent-v202-adv-submission-validator` | Exit 0: title, abstract, keywords, placeholders, provenance, dependency pins, and highlights pass. |
| `agent-v202-adv-full-clean-replay` | Exit 0: offline wheel install, exact algebra, 512-state/108-fibre lumping, coefficients, integration audit, fail-closed mutations, deterministic archive rebuild, and deterministic PDF rebuild all pass; rebuilt hashes equal delivered hashes. |
| `agent-v202-adv-citation-key-audit` | 12 cited keys = 12 bibliography keys; no missing or unused entries. |
| `agent-v202-adv-wheel-metadata-license` | Wheel hashes, names, versions, requirements, and retained license files match documentation. |
| `agent-v202-adv-all-python-assert-audit`, `agent-v202-adv-source-python-assert-audit` | Zero bare assertions. |
| `agent-v202-adv-outer-optimized-rejection`, `agent-v202-adv-private-validator-optimize` | Every additionally tested entry point rejects optimized Python nonzero. |
| `agent-v202-adv-independent-package-mutation` | Disposable `VERSION.md` mutation rejected nonzero before final package success. |
| `agent-v202-adv-outer-archive-binding` | 35/35 outer members safe, sorted, unique, byte- and mode-equal to delivered copy. |
| `agent-v202-adv-wrapper-tree-compare`, `agent-v202-adv-outer-archive-repo-compare` | Delivered wrapper tree and outer tar are byte-identical to repository wrapper artifacts. |

## 7. Unresolved but nonblocking external assertions

1. The tag is unsigned; local checkout, tag, wrapper, and manifests establish consistency, not signer, remote-hosting-account, or authorship authentication.
2. No network was used, so remote tag availability, PyPI-origin hashes, DOI metadata, current journal rules, and completeness of the literature search were not externally verified.
3. Funding, competing interests, author contribution/responsibility, permissions, and the private postal address require human confirmation.
4. I did not perform the assigned-to-main-agent raster visual inspection.  My complete PDF-text review and the clean deterministic build found no textual/reference defect.

These are either explicitly disclosed limitations or ordinary human submission gates; none contradicts the scientific claims.

## 8. Final recommendation

**READY.** The v2.0.2 proof repair closes the only mathematical counterexample exactly at the stopped time needed downstream; every use of equation (26) is valid; the verifier, interpreter, dependency, mode, provenance, and reproducibility fixes execute as described; the manuscript remains carefully scoped; and package/version hashes are consistent.  The broken `vendor/README.md` cross-reference is a low-severity documentation blemish, not a reason to reopen the scientific freeze.  Before actual portal submission, the human author should complete the explicitly reserved postal/declaration/venue confirmations.
