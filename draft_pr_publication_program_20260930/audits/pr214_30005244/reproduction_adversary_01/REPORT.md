# PR214 independent computational and package reproduction

Verdict within the assigned finite scope: no mandatory mathematical or package-reproduction issue was found. All seven unchanged published programs pass on the actual available runtime. Independently authored Cartesian, geometric-integral, rational-constant and defective-projection checks also pass. This finding is not a substitute for Root's independent proof and priority review.

## Exact inputs and independence

Root explicitly authorized own-body mathematical reading after authenticating the original/current native custody. I authenticated Root's 3365-byte custody acceptance with SHA-256 `529fbbb3ca2b850e530434b7d10f2d356e58a7e2c18a1349bc45fff08343075e`.

The exact published verification ZIP is 764472 bytes with SHA-256 `5cbd35e7c4b30d3d7e90a953cffb689b03bc957e60c4aa6905b0a60e38c069d7`. Its 187 entries are regular files, totaling 1335262 uncompressed bytes. Before exclusive extraction to an owned directory I rejected traversal/absolute names, duplicate names, links, encryption and unreasonable sizes or compression ratios. All 186 rows of the archive's `PACKAGE_FILES.json` independently match the extracted bytes. The root manuscript is exactly 34975 bytes/SHA-256 `5d1145a052135d34997614be42142f9b63ef76730ca9992e045d52548747dd7e`; it is not the distinct frozen historical manuscript.

I read the root manuscript, package and verification instructions, wrapper and all seven mathematical programs completely. I did not read earlier narrative adversarial reports, verdicts or conclusions. Expected JSON files were used solely for the prescribed replay comparison. The four original program bodies were also compared directly against Root's authenticated original native snapshots; all four are byte-identical. `SOURCE_READ_MANIFEST.json`, `EXTRACTED_PINS.json`, `NATIVE_SCRIPT_IDENTITY.json` and `ZIP_INVENTORY.json` preserve the finite input scope.

## Unchanged inherited replay

The actual runtime was Python 3.11.8, NumPy 2.4.2 and SymPy 1.14.0 on arm64 macOS; independently authored stress checks additionally used mpmath 1.3.0 at 100 decimal digits. These differ from the archived instructions' recorded Python 3.14.6/NumPy 2.3.4 replay, giving a successful additional runtime observation rather than an assertion of runtime identity.

`replay_unchanged.py` copies each fully read program unchanged into a separate owned working directory and invokes the actual Python interpreter with `-E -B -P`. It makes no installations or network calls and never mutates the extracted published bodies. It captures exact stdout/stderr, return status, elapsed time, command, working directory and script bytes/hash for every invocation. The published wrapper was fully read and its seven-program behavior and expected-field comparison were reproduced by this auditable runner; the wrapper itself was not executed. No dependency implementation audit is claimed.

| Program | Actual reported/checkable result | Exit/stderr |
|---|---:|---|
| Original `verify.py` | 301 reported exact assertions | 0 / empty |
| Original inherited `independent_check.py` | 625 reported exact assertions | 0 / empty |
| Original `verify_scope.py` | 482 reported exact assertions | 0 / empty |
| Original inherited `independent_scope_check.py` | 748 reported exact assertions | 0 / empty |
| `ball_exact_controls.py` | 1244 entries, every `pass` true; coefficient `-7831/15000` | 0 / empty |
| `kernel_controls.py` | 427 complete shells through squared radius 512; identities/scaling pass; numerical tables produced | 0 / empty |
| `spectral_illustration.py` | Five defective-cluster rows and all program assertions pass | 0 / empty |

The first four outputs match every archived expected JSON field, using the documented absolute/relative `1e-12` tolerance only for floating values. The sum 2156 is the programs' own reported count, not 2156 independently formulated mathematical obligations. The 1244 and 427 counts likewise describe finite computational evidence. Exact symbolic/rational assertions and illustrative floating tables remain distinct. `replay/REPLAY_RESULTS.json` and per-program binary stdout/stderr are the actual execution evidence; the full ball output and kernel output are retained separately.

## New independently authored checks

`independent_checks.py` imports no submitted mathematical program. Its final run performs 27 exact/symbolic checks plus one asserted observation about a separately labelled floating-point stress experiment. This is a finite coverage count, not proof coverage.

1. I formed the nine Cartesian derivatives of `exp(i k sqrt(x²+y²+z²))/(4π sqrt(x²+y²+z²))` directly, then checked the claimed full matrix at two nonaxial points, `(2/3,-1/3,2/3)` and `(1,2,-2)`, with unrestricted symbolic complex `k`. This verifies the matrix signs and factors without relying only on axial radial/transverse formulas. Three independent diagonal/off-diagonal entries of the near-field expansion are checked from those Cartesian derivatives, recovering both `-k²(I+eeᵀ)/(8πr)` and `-i k³ I/(6π)` signs. The off-origin trace is `-2 k² g_k`.
2. Exact checks cover the dynamic dimensionless identity `h³ K_k(hv)=K_(hk)(v)` for positive rational `h=2/7`, conjugation `K_(-conj(k))=conj(K_k)` at pure imaginary, genuinely complex and zero frequencies, and exact vanishing of the dynamic correction at zero frequency.
3. I derived the unit-ball overlap volume from two spherical caps: `V(d)=π(4+d)(2-d)²/12` for `0≤d≤2`. Integrating `4π d^(p+2) V(d)` gives the pair-volume normalization and exact integrals for powers `p=-2,-1,2`. Thus the actual quadratic kernel has `||C2||_HS²=3/8<1`, and the manuscript's pointwise quartic remainder majorant has squared Hilbert–Schmidt constant `6/5<4`. These independently support, and are stronger than, the manuscript's stated coarse constants. They are auxiliary validation identities; no new discovery claim is made. The same overlap calculation gives constant-mode compression `P C2|V=-4I/15`.
4. The harmonic gap is checked as an identity for every integer `ell≥2`: `mu_ell-1/15=(ell-2)/(5(2ell+1))≥0`. Its accumulation gap is `1/6-mu_ell=1/[2(2ell+1)]`. This avoids treating a finite degree loop as a universal gap proof. Exact rational arithmetic at `k=1/10000` gives a graph-estimate trace upper bound even more negative than the published coarse upper bound `-(7831/15000) k³`, confirming its margin.
5. A separate exact 3×3 defective block with eigenvalue `2i` and a moving static coordinate has the nonorthogonal rank-two Riesz projector `I-(A-2iI)²/(1-2i)²`. Exact checks establish idempotence, commutation, rank via trace and the generalized-eigenspace relation. This gives a materially different check from contour quadrature and does not assume orthogonal projections or semisimplicity.

`INDEPENDENT_CHECKS_RESULT.json` and `INDEPENDENT_EXECUTION.json` contain the final results and source/runtime/output pins. Final exit status is zero with empty stderr. Two failures in my own initial check harness were corrected and preserved transparently: an incorrect factor in my own accumulation-gap identity, and an unsimplified SymPy trace equality. Neither was a defect in the published manuscript or source. The history is described in `ISSUES.json`, `HARNESS_CORRECTION.json` and `harness_run_02_failed/`.

## Nonblocking numerical limitation

A deliberately adversarial small-argument test exposes complete cancellation in the raw double-precision remainder expressions: with `k=1e-4` and `r=1e-6` or `1e-8`, direct subtraction returns zero radial/transverse remainders. Independent 100-digit differentiation gives, for example at `r=1e-8`, approximately `-0.07957747` radially and `-0.03978874` transversely. Relative error is 1.0. A moderate-separation baseline agrees to about `1.8e-14` relative error.

This does not contradict the analytic expansion or the published finite tables, whose parameters are resolved and whose purpose is expressly illustrative. No script numerically certifies the explicit ball pole or existential support index. Accordingly this is observation N1, not a mandatory repair or theorem counterexample. These raw routines should not be promoted to a general-purpose small-argument kernel evaluator without a separately verified stable implementation.

## Mathematical and audit limits

I read the complete final proof and found no contradiction between its stated kernel normalization, its numerical constants and this reproduction evidence. The finite checks do not establish strong static convergence, Hilbert–Schmidt mesh convergence, harmonic completeness, Fredholm continuation, norm convergence of Riesz projections, a finite effective mask index or historical priority. The manuscript explicitly labels these as analytical arguments, credits its static/spectral ingredients and makes a qualified priority claim. Root remains responsible for the complete proof/primary-source and priority audits and the final adoption decision.

No Git commands, package installations, native provider/ref/PR changes, tracker edits, global-five changes, stable writer-lock actions, outside communication or additional agents were used. Every output is confined to this assigned directory. No external mathematical endorsement or human peer review is asserted.
