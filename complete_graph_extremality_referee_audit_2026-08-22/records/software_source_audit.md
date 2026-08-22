# Software source audit

Date: 2026-08-22 (America/Los_Angeles)

Scope: frozen disposable referee package at
`/Users/alec/Documents/Math/complete_graph_extremality_referee_audit_2026-08-22/work/package`

Completion: **100% of the requested static source audit**. I read the package
instructions and identity files, the package verifier, all shell/build/replay
entry points, the project Makefile, every Python program invoked by the replay,
and every delivered Python helper reached by project imports. I used text-only
inspection (`find`, `rg`, `nl`, `sed`, and `wc`). I did **not** execute a
delivered script/program, compile one, or import a delivered module.

The complete command/import topology is in `records/invocation_graph.md`.

## Bottom line

The package is suitable for a **conditional** execution audit: the mandatory
shell path normally propagates failures, theorem-bearing calculations use exact
arithmetic, the triangle and two stated weighted-K4 families have strong
derivation-to-certificate cross-checks, and the symmetric Hessian verifier
covers its stated finite integer ranges without gaps.

It is not safe to execute under an arbitrary inherited environment. The
scientific verifiers and even bootstrap version checks rely heavily on bare
Python `assert`; `PYTHONOPTIMIZE` is not cleared. With optimization enabled,
most checks disappear while PASS messages remain. Before execution, use an
unoptimized interpreter and sanitize at least `PYTHONOPTIMIZE`, `PYTHONPATH`,
and `MAKEFLAGS`.

The replay is a certificate checker, not a standalone computer proof of every
manuscript quantifier. Several all-order claims are computationally checked
only on finite orders and depend on manuscript analytic reductions for the
remaining orders. Some PASS/PROVED print strings are broader than the
assertions actually executed.

## Findings requiring attention

### SA-1 — High: Python optimization removes certification

`submission/bootstrap_replay.sh` tests Python and distribution versions with
assertions (`bootstrap_replay.sh:10-13,23-34`). Nearly every scientific verifier
also encodes its success conditions as bare assertions (for examples,
`derive_certificate.py:163-186`,
`verify_true_inverse_rank_symmetric_phase.py:204-349`, and
`verify_paper_claims.py:67-296`). Neither bootstrap nor replay clears
`PYTHONOPTIMIZE`, and no program checks `sys.flags.optimize`.

Under `python -O` or an effective `PYTHONOPTIMIZE` setting, environment checks,
algebraic identities, positivity checks, range checks, and most cross-checks
are compiled away. Programs can still reach unconditional PASS/PROVED prints.

Required mitigation: unset `PYTHONOPTIMIZE`, confirm
`sys.flags.optimize == 0` in Python 3.14.6, and require a zero process exit code
rather than judging success from printed PASS lines.

### SA-2 — Medium: two advertised imported-helper audits are not run

`CLAIM_CODE_MAP.md:23-31` says three modules are reached as imports, but the
substantive reachability is narrower:

- `verify_marked_lift.py:24` imports and calls
  `verify_resolvent_identities.solve` at `verify_marked_lift.py:28-29`.
- `verify_marked_lift.py:25` imports only
  `verify_direct_flow_screen.matrix_from_edges`, used as a construction utility
  at lines 491-495, 520-524, and 551-555.
- Loading `verify_direct_flow_screen.py` imports four functions from
  `verify_fisher_route.py` (`verify_direct_flow_screen.py:17-22`), but none is
  called by the marked-lift path.

The `__main__` guards mean replay does not execute the finite direct-flow screen
at `verify_direct_flow_screen.py:99-114`, the Fisher/witness suite at
`verify_fisher_route.py:773-804`, or the resolvent helper's standalone examples
at `verify_resolvent_identities.py:151-170`. The imported `solve()` itself is
exercised. Import reachability must not be reported as execution of those
guarded audit suites.

### SA-3 — Medium: all-order antisymmetric coverage is not discharged by code

The manuscript claims positivity for every `n>=3`
(`sections/04_local_hessian.tex:107-111`). The dedicated verifier evaluates its
rank recurrence only for `n=3..40` and its independent full-active check only
for `n=3..7` (`verify_antisymmetric_hessian.py:148-157`), then prints
`PROVED ANALYTICALLY ... every n>=3` at line 157.

The all-order argument is manuscript work, not mechanically quantified by this
program. A referee must validate the coupling/recurrence proof in
`appendices/A_sector_certificates.tex:247-328`; executable output alone does not
close `n>=41`.

### SA-4 — Medium: general directed strong selection is spot-checked

The theorem quantifies over every `n>=3` and every positive complete directed
support (`sections/02_model_results.tex:100-111`). The literal directed solve
is independent and orientation-sensitive
(`verify_directed_db_strong.py:32-70`), but `main()` checks only two directed
three-vertex matrices and one directed four-vertex matrix (`:148-168`), plus a
column-uniform control and one column-scaling check (`:175-203`). The predicted
coefficient and sum-of-squares formulas are supplied at `:83-112`; extraction
from the literal solve independently confirms them only on those examples
(`:130-145`).

`verify_paper_claims.py:174-210` likewise checks the incoming-column identity on
one four-vertex matrix and its equality case, not symbolically. The universal
quantifier rests on `sections/05_strong_selection.tex:42-126`. The software is
exact regression/orientation evidence, not an exhaustive computer proof.

### SA-5 — Medium/low: versions are pinned, artifacts and import state are not

`paper_db_extremality/requirements.txt:1-3` pins versions but supplies no wheel
or sdist hashes; `bootstrap_replay.sh:19-21` installs without
`--require-hashes`. Reproduction trusts the configured package index.
`PYTHONPATH` is not cleared. Make recipes override it with `PYTHONPATH=.` for
most Make goals (`Makefile:8-24`), but direct programs at `replay.sh:31-52`
inherit the caller's value. Use a trusted index/cache and unset `PYTHONPATH`.

The README discloses possible pip and Tectonic network/cache access
(`README_FIRST.md:51-56`). PDF byte comparison catches rendering differences
but does not pin downloaded Python or Tectonic resource artifacts.

### SA-6 — Medium/low: inherited Make flags can weaken failure behavior

Shell scripts use `set -eu` and normally propagate failure, but `replay.sh:29`
does not clear `MAKEFLAGS`. An inherited ignore-errors option can weaken recipe
handling. Unset `MAKEFLAGS`, or verify it contains no ignore-errors setting,
and preserve Make's final status.

### SA-7 — Low: internal integrity does not authenticate the Git commit

`verify_referee_package.py` explicitly checks package file-set equality and
hashes (`:50-72`), archive sidecar and safe sorted regular members (`:75-103`),
internal manifest hashes and byte-identical extracted files (`:104-127`), and
PDF identity (`:129-140`). These explicit raises are immune to `-O`.

It does not compare the supplied tree against Git object
`3652cfda20a3edad1b4e9ca75a4e5536f6f7f5ba`; it only checks that README and
VERSION contain the same 40-hex string (`:141-152`). It also does not validate
VERSION's statement that 68 members were byte-checked against that commit
(`VERSION.md:7`). Treat the commit as provenance metadata unless independently
verified against a trusted repository.

### SA-8 — Low: paper-level guards are consistency checks

`verify_paper_claims.py` is an integration audit, not an independent proof:

- formal-source checks are substring assertions (`:213-237`);
- the symmetric binding checks a hardcoded digest against a file and the same
  digest printed in the appendix (`:18-21,240-252`), proving version consistency
  rather than correctness;
- tangent decomposition is exercised on one chosen `n=5` tangent (`:120-171`);
- active-law and phase-space normalization is enumerated only for `n=3..5`
  (`:67-117`);
- curvature-sign conversion is checked at one rational specialization
  (`:285-296`).

These are useful regression guards, but hardcoded values should not be counted
twice as independent theorem evidence.

### SA-9 — Low: unused legacy Make target is not standalone-archive-safe

The unused `paper1` target at `Makefile:29-31` enters `paper/` and copies from a
legacy path absent from the archive. Running `make paper1` would fail after the
certificate goals. The mandatory replay deliberately requests individual
goals (`replay.sh:27-29`); `build.sh` is the correct document entry point.

## Claim-to-assertion map and coverage

### Forward dB chain, absorption, and baseline

Manuscript: `sections/02_model_results.tex:3-33` and
`sections/05_strong_selection.tex:6-22`.

- `src/exact_markov.py:65-121` builds transitions from explicit parent/target
  loops and asserts exact row normalization; `:124-169` builds all `2^n` rows,
  solves all transient equations, and averages singleton states.
- `src/exact_markov.py:178-192` supplies complete-graph closed forms.
- `tests/test_exact_markov.py:19-45` checks both rules at complete `n=2,3,4`,
  row sums on a weighted triangle, and complete `n=4` lumpability.
- `verification/verify_obstruction.py:56-145` independently constructs and
  solves the chain without importing `src.exact_markov`; its main exhausts all
  subset states of supplied complete graphs `n=2,3,4` (`:213-219`).

Assessment: exact for the declared symmetric-weight helper. Its validator
requires symmetry (`exact_markov.py:24-52`), so it is not directed evidence.
For symbolic inputs it rejects known-negative entries but can admit an entry of
undecidable sign (`:37`); current theorem calls use positive symbols or exact
positive rationals.

### Complete-support directed strong selection

Manuscript: `sections/02_model_results.tex:100-111` and proof
`sections/05_strong_selection.tex:42-126`.

Code assertions are the literal directed solve
(`verify_directed_db_strong.py:32-70`), target-column defect and coefficient
identity (`:83-112`), example coefficient extractions (`:130-168`),
column-uniform/wrong-row negative control (`:175-188`), and incoming-column
scaling invariance (`:190-203`).

Orientation is correct. The manuscript defines `P[target][source]` from raw
`W[source][target]` (`sections/02_model_results.tex:3-14`). The verifier stores
raw `W[source][target]`, sums sources for fixed target (`:47-59`), and forms
defects within target columns (`:87-93`). The deliberately wrong row defect is
nonzero on a column-uniform chain that exactly ties the baseline (`:175-188`).
Coverage remains finite, as detailed in SA-4.

### Noncomplete support and fixed-graph closure

Manuscript: `sections/02_model_results.tex:113-136` and
`sections/05_strong_selection.tex:128-163`.

Software evidence is illustrative: `tests/test_exact_markov.py:47-55` checks a
three-vertex path, and `verification/verify_obstruction.py:176-179,220-226`
checks the support-degree limit on `path4` and `star4`. The directed strongly
connected noncomplete case explicitly invokes an external theorem in the
manuscript (`sections/05_strong_selection.tex:130-132`); condensation-DAG and
general undirected support arguments are also manuscript deductions. Replay
does not mechanically establish the full corollary.

### Positive weighted triangles

Manuscript: theorem at `sections/02_model_results.tex:141-147`; certificate at
`sections/06_low_order.tex:7-68`.

- `phase2_triangle/derive_certificate.py:23-61` builds the generic six-state
  system over positive symbolic weights; `:156-170` solves it and compares the
  result to the claimed rational formula.
- It relates the cleared denominator to a strictly diagonally dominant
  M-matrix determinant (`:161-179`) and checks explicit square identities that
  establish `A,D,E>=0` and strictness (`:121-153,181-186`).
- `crosscheck_exact_solver.py:36-57` compares all six transient values with the
  generic eight-subset-state implementation, though it imports both the manual
  derivation and shared solver.
- `audit/independent_triangle_audit.py:23-62` has a third direct state
  construction, checks the homogeneous formula/SOS identities symbolically
  (`:124-187`), edge and near-uniform limits (`:190-220`), and deterministic
  exact cases (`:223-282`).

This certificate is not circular: the difference is derived from a literal
generic linear system before comparison to a separately encoded formula, and
positivity is reduced to explicit square identities. The domain `a,b,c>0`,
`r>1`, and equality only at uniform weights matches the code assumptions. The
excluded endpoint `r=1` is visibly a zero factor.

### Two symmetric weighted-K4 families

Manuscript: `appendices/B_k4_certificate.tex:54-147`; limited scope is explicit
at `sections/06_low_order.tex:70-74`.

- `derive_lumped_certificates.py:22-106` builds the generic two-class quotient
  directly from dB updating.
- The `1+3` result compares a solved symbolic rational function with the
  factored certificate and checks positive coefficients (`:118-146,194-202`).
- For `2+2`, it derives the numerator, symmetrizes it, substitutes
  `xy=g^2`, `x+y=2g+d` with `g>0,d>=0`, and compares all `d` coefficients to
  the certificate (`:203-231`). The equality split is complete: `d=0,g!=1` is
  handled by `C0`; `g=1,d>0` by positive higher coefficients. The derived
  reduced denominator is coefficientwise positive (`:233-252`).
- `crosscheck_full_chain.py:88-100` checks symbolic strong lumpability against
  the full 16-state transition structure. Full 14-transient-state solves are
  checked at four rational specializations (`:101-129`).

Coverage matches exactly the two declared invariant families and does not
purport to classify every weighted K4.

### Fair-geometric dual, collision, and marked/active identities

Manuscript: `sections/03_duality_collision.tex`; local-Hessian use at
`sections/04_local_hessian.tex:1-60`.

- `verify_r2_determinant.py:14-49` builds the active kernel and matrix-tree
  cofactors. Its generic triangle calculation checks a centered certificate and
  distinguishes collision from promotion (`:51-124`). Its docstring explicitly
  says it does not prove an all-order determinant sign (`:1-7`).
- `verify_complete_refresh_forest.py:52-120` proves the symbolic order-three
  Bernstein certificate. The `n=4,5` checks are small deterministic random
  screens (`:223-255`) explicitly labelled finite evidence (`:1-6`).
- `verify_marked_lift.py:28-80` uses the imported resolvent solve to construct
  the posterior midpoint. It separately builds row-stochastic marked/active
  kernels (`:83-136`), rank flux, harmonic, and handoff identities (`:240-313`),
  and checks Perron/forward-active factorization on P3 (`:344-464`).
- It records exact counterexamples to stronger domination/semigroup statements
  (`:491-569`) and prints the universal collision/global statement as open
  (`:572-578`).

The line-341 label “universal two-step sum-of-squares identity” is broader than
runtime enumeration: comparison with the hardcoded formula is on three raw
kernels and four `t` values (`:316-341`). Universal validity is an algebraic
manuscript identity, not an exhaustive input check.

The inert direct-flow and Fisher helper mains are **not load-bearing for a
stated theorem**. `verify_direct_flow_screen.py:1-8` labels its work finite
validation, and its main (`:99-114`) concerns the direct `L<=V` route. The
Fisher main (`verify_fisher_route.py:773-804`) records route identities and
counterexamples. Those concern the open global collision route, consistent
with `verify_marked_lift.py:578` and the open global statement at
`sections/07_implications_reproducibility.tex:69-73`. Their nonexecution removes
diagnostics, not a certificate used to prove the paper's local theorem.

### Tangent decomposition and Hessian integration

Manuscript: `sections/04_local_hessian.tex:62-161`.

`verify_paper_claims.py:120-171` checks row/column sums, symmetry types,
reconstruction, and dimensions on one genuinely directed `n=5` tangent;
`:67-117` checks active normalization and phase typing for `n=3..5`;
`:255-282` checks standard-sector phase/embedding/Frobenius constants for
`N=2,3,4`; and `:285-296` checks curvature-sign conversion. These are exact
finite consistency checks. The general irreducible decomposition, vanishing
first variation, and local-neighborhood Taylor argument remain manuscript
proofs.

### Standard Hessian sector

The manuscript ledger is exact `2<=N<=9`, analytic tail `N>=10`
(`sections/07_implications_reproducibility.tex:86-92`).

- `verify_physical_standard_phase.py:53-143` reconstructs the signed quotient,
  rewards, Schur complement, and direct/reduced equality.
- It independently constructs the physical two-feature operator and checks
  conjugacy/normalization (`:146-228`) for invoked `N=2..12` (`:414-417`).
- `symbolic_certificates()` checks all-order polynomial identities and residual
  factorizations (`:231-349`). Every barrier is rebuilt with exact matrices for
  `N=6..15` (`:352-421`), and exact phase values are checked for `N=2..9`
  (`:398-428`).

There is no range gap: finite values end at 9 and the appendix's symbolic sign
argument starts at 10. Code checks the identities; the integer-domain sign
interpretation remains part of the appendix proof.

### Symmetric-balanced Hessian sector

- `verify_true_inverse_rank_symmetric_phase.py:255-277` exactly solves every
  integer `N=3..39`, checks phase identity on `N=3..8`, and checks every phase
  margin for `N=40..287`.
- `:280-349` audits the discriminant/coefficient certificates for `N>=288`.
- The intended ranges `3..39`, `40..287`, and `>=288` meet with no gap;
  `N=2` is the zero-dimensional symmetric sector at `n=3`
  (`sections/04_local_hessian.tex:84-86`).
- `verify_hessian_sectors.py:205-225` separately constructs orbit-reduced
  active-chain values for all three sectors at `n=3..12`.

The two-channel system (`verify_true_inverse_rank_symmetric_phase.py:74-109`)
and debt polynomials (`:280-326`) are transcribed from the appendix. This is not
wholly circular because the finite solves, phase identity, and separate active
chain values cross-check them; derivation from the full operator and the
discriminant sign logic are still manuscript obligations.

### Antisymmetric-balanced and regular-sector checks

`verify_antisymmetric_hessian.py:31-76` computes the rank solution and positive
recurrence; `:102-132` compares a canonical direction with the full active
chain. Runtime ranges are finite as recorded in SA-3.

`verify_local_complete_hessian.py` independently starts from a rank/cut
reduction, checks exact `n=4,5` values (`:192-202`), exact total bounds for
`n=6,7,8` (`:203-215`), and coefficientwise certificates for `n>=9`
(`:224-347`). Its ranges meet without gaps for its declared `n>=4` claim. The
M-matrix comparison and derivation of the hardcoded cut factors come from
`LOCAL_COMPLETE_HESSIAN_THEOREM.md`, not from a full subset-chain rebuild.

### Phase-3 examples

`phase3_asymptotic/verify_lumping.py:64-85` exhausts all `2^n` states for each
supplied partition, but `main()` checks one two-class and one windmill graph at
only `r=7/3`, under both rules (`:139-147`). `CLAIM_CODE_MAP.md:13` correctly
says no Paper I theorem depends on them.

## Enumeration, exactness, sharing, and circularity

- Literal state builders exhaust every state for each supplied graph. Triangle
  generic elimination covers all positive symbolic triangle weights after
  scale normalization. Both K4 orbit partitions are checked symbolically
  against the full 16-state structure. The symmetric verifier exhausts every
  integer order in its finite bands, including endpoints.
- Sample-only evidence includes the directed coefficient examples, complete
  baseline/lumping at small `n`, forest samples at `n=4,5`, antisymmetric
  recurrence through `n=40`, full antisymmetric active checks through `n=7`,
  and three-sector active values through `n=12`.
- The unexecuted direct-flow main would enumerate raw alphabets of `4^3` at
  `n=3` and `3^6` at `n=4`, filter connected graphs, then sample 48 exact
  `n=5` graphs (`verify_direct_flow_screen.py:80-104`). This is finite even if
  run.
- Theorem checks use `Fraction`, SymPy exact expressions/rational functions, or
  Flint `fmpq`. Fixed-seed random screens retain exact rational arithmetic.
  Float conversions are human-readable output only. Fisher's Decimal entropy
  diagnostics (`verify_fisher_route.py:450-505`) are not theorem assertions and
  its main is not reached.
- Unit tests, triangle crosscheck, and K4 crosscheck share
  `src/exact_markov.py`. Triangle's main derivation and hostile audit do have
  separate state constructions; `verification/verify_obstruction.py` is also
  independent. K4's crosscheck imports its expected quotient, so independence
  is in transition construction rather than certificate transcription.
- The active kernel is independently reimplemented in several source files.
  Standard and symmetric phase verifiers do not import one another; small-order
  values also meet the active-sector verifier.
- Triangle/K4 hardcoded certificates are checked against directly derived
  rational functions and are not circular. Several Hessian programs instead
  begin from manuscript-derived quotient/recurrence formulas; their value is
  checking algebra, signs, and finite ranges, not independently deriving the
  reduction.

## Failure propagation and suppressed errors

Positive findings:

- `run_all_referee_checks.sh`, bootstrap, replay, all, and build scripts use
  `set -eu` at line 2.
- Package-integrity failures use explicit exceptions. Linear-solver pivot
  failure propagates. The replay dependency probe suppresses diagnostics
  (`replay.sh:17`) but exits 2 (`:18-21`). `pdftoppm` diagnostics are redirected
  (`build.sh:20-22`) but a nonzero status propagates. Outer `cmp` is decisive
  (`run_all_referee_checks.sh:49-52`).
- No `try/except` converting scientific failure to success, `contextlib.suppress`,
  `|| true`, or `set +e` occurs on the mandatory path.

The optimizer issue is nevertheless decisive: with assertions removed, the
package verifier, unittest methods, dependency import probe, incidental
computation errors, and PDF comparison still operate, but the scientific
certificate assertions and exact interpreter/package-version assertions do
not. It is therefore entirely possible for the overall command to exit 0 under
optimization while most intended checks never occurred.

## Build and package notes

- `build.sh:10-22` fixes epoch/time zone, compiles, installs, inspects, and
  renders the PDF; outer bytewise comparison is stronger than a visual check.
- Tectonic and Poppler versions are exact-checked
  (`run_all_referee_checks.sh:18-32`); Make is checked only for presence.
- `Makefile:6` has a different document epoch from `build.sh:10`, but its
  legacy paper target is unused. Mandatory build uses the latter value, matching
  bundle metadata.
- Release tools are outside mandatory replay. Statically,
  `bundle_manifest.py:114-206,209-255` uses sorted members, normalized metadata,
  atomic replacement, and post-write verification. Its internal parser is
  looser than the delivered package verifier, but the latter rechecks the
  delivered archive strictly.

## Readiness verdict and exact execution preconditions

**Static audit complete; conditionally ready, but do not execute until all
items below are satisfied.**

1. Resolve `BOOTSTRAP_PYTHON` to Python **3.14.6**.
2. **Unset `PYTHONOPTIMIZE`** and independently confirm that interpreter reports
   `sys.flags.optimize == 0`.
3. **Unset `PYTHONPATH`** for the whole bootstrap/replay.
4. **Unset `MAKEFLAGS`** (at minimum ensure no ignore-errors option is present).
5. Resolve trusted executables for Make, Tectonic **0.16.9**, and Poppler
   `pdfinfo`/`pdftoppm` **26.08.0**.
6. Accept that pip will install `sympy==1.14.0`, `python-flint==0.9.0`, and
   `mpmath==1.3.0` without artifact hashes; use a trusted configured index/cache.
7. Accept possible pip/Tectonic network or cache access and provide sufficient
   temporary disk/memory for exact symbolic solves and PDF rendering.
8. Preserve the complete transcript and top-level exit status. PASS strings
   alone are not a success criterion.

The mandatory replay reaches the unit suite and all **17 named top-level
verifier/cross-check programs**. It does not execute the guarded mains of
`verify_direct_flow_screen.py`, `verify_fisher_route.py`, or
`verify_resolvent_identities.py`; only the latter's `solve()` and the direct
screen's `matrix_from_edges()` are substantively used. The first two mains are
open-route diagnostics, not load-bearing theorem verifiers.

## Static-audit conclusion

No static evidence of malicious behavior, person-to-person communication,
exception swallowing, floating-point theorem extrapolation, or a hidden global
maximality assertion was found. The source is traceable and generally
fail-fast under a clean, unoptimized environment. Exact remaining software
risks are assertion elision, inherited environment state, nonexecution of
helper diagnostic mains, finite executable coverage for the general directed
and antisymmetric claims, and reliance on manuscript-derived reductions for
several Hessian certificates.

