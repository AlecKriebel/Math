# Final hostile-but-fair adversarial falsification

Date: 2026-08-22 (America/Los_Angeles)

Scope: the frozen disposable referee package in `work/package`, the complete
30-page manuscript, the theorem/quantifier ledger, every current audit report,
and the official and optimized replay records in `records/COMMANDS.log`.

Method: every conclusion was treated as a hypothesis.  This pass used static
text inspection only and did **not** execute a delivered program or import a
delivered module.  It assessed the already-recorded executions and the
independently written checker as evidence.  No package payload was modified.

## Final verdict

**No new mathematical defect, counterexample, missing population range,
orientation reversal, phase-order error, sign/factor error, endpoint gap,
equality-class error, citation-hypothesis mismatch, or theorem/code
contradiction was found.**

The manuscript's mathematical claims are fully supported within the audited
scope.  The overall package verdict should nevertheless be **valid after minor
corrections**, because the delivered replay is not fail-closed under Python
optimization.  This defect has high impact on the meaning of a PASS transcript
but a small remediation: reject optimized mode and replace load-bearing bare
assertions with explicit nonzero-exit checks.  The clean official replay was
run with optimization disabled, so the flaw does not invalidate the evidence
from that particular run.

The strongest verified mathematical result is Theorem 1 in its full directed
form: for every fixed `n>=3`, the complete normalized kernel has zero first
variation and strictly negative fixation Hessian at fitness two in every
nonzero loopless row-zero direction.  The standard, antisymmetric-balanced,
and (when present) symmetric-balanced sectors are all positive for every
required order.  The sharp fixed-structure strong-selection expansion,
fixed-graph closure, triangle theorem, and the two stated symmetric `K4`
families are also independently supported.

## Evidence base reviewed

The following were read in full:

- `records/paper_extracted.txt` (the complete 30-page manuscript);
- `report/THEOREM_LEDGER.md`;
- `records/PACKAGE_IDENTITY.md`;
- `records/software_source_audit.md` and `records/invocation_graph.md`;
- `records/fitness_two_local_audit.md`;
- `records/strong_selection_low_order_audit.md`;
- `records/independent_crosschecks.md`; and
- the official and optimized replay entries in `records/COMMANDS.log`.

The source identity is fixed by archive SHA-256
`b1b7b7c4c9393ee4fa85eeacd54cefc4bcc94a3eca759d500c9ee6a362eddd2b`
and PDF SHA-256
`a6bda621b764ca8ee86658f6b68de0245790b84315eb77a6cc7ca45f7953bd2d`;
all 68 source-derived archive files were independently matched byte-for-byte
to local Git commit `3652cfda20a3edad1b4e9ca75a4e5536f6f7f5ba`
(`records/PACKAGE_IDENTITY.md:7-18,34-35`).

The independent checker in `records/independent_crosschecks.py` imports no
delivered module and has SHA-256
`019a599899fa223995ea61ca476e5e841e55bcea3605203f81b593d67f92d578`.
Its exact transcript ends with status 0 in
`records/independent_crosschecks.log`.

## Findings by severity

### AF-1 — High impact on certification, minor remediation: optimized replay can falsely pass

This is the only adverse finding that changes the package verdict.

The bootstrap's interpreter and dependency checks are bare assertions at
`phase5_exact_threshold/paper_db_extremality/submission/bootstrap_replay.sh:10-13`
and `:23-34`.  The theorem-bearing programs likewise use bare assertions; key
examples are
`verify_true_inverse_rank_symmetric_phase.py:204-349`,
`verify_physical_standard_phase.py:231-349`, and
`paper_db_extremality/verify_paper_claims.py:67-296`.  Static counting found
406 leading bare assertions across 20 delivered Python files
(`records/independent_crosschecks.md:239-245`).  Neither bootstrap nor replay
rejects `PYTHONOPTIMIZE`, and no mandatory program checks
`sys.flags.optimize` (`records/software_source_audit.md:40-55`).

The failure mode is not hypothetical:

- `records/COMMANDS.log:30004-30010` runs with `PYTHONOPTIMIZE=1`, erases an
  explicit `assert False`, prints `PASS_AFTER_ERASED_ASSERT`, and exits 0.
- `records/COMMANDS.log:30012-30198` runs the full delivered replay with
  `PYTHONOPTIMIZE=1`; it reaches the final package PASS and exits 0 even though
  the theorem-bearing assertions were compiled away.

This means an arbitrary PASS transcript is not itself a certificate.  It does
**not** invalidate the official run: its sanitized preflight explicitly found
Python 3.14.6, `optimize=0`, and no relevant environment overrides
(`records/COMMANDS.log:29125-29131`), and the official replay then ran from
`:29133` through the byte-identical PDF result and status 0 at `:29723-29725`.

Required correction:

1. reject `sys.flags.optimize != 0` with an explicit exception or nonzero exit;
2. unset or reject `PYTHONOPTIMIZE` before creating and invoking the venv; and
3. convert theorem-bearing assertions to explicit checks that cannot be
   removed by `-O`.

The impact is high because it concerns whether checks occurred; the editorial
remediation is minor because it does not change a theorem, proof, certificate,
or expected value.

### AF-2 — Minor coverage-description issue: imported diagnostic mains are inert

The mandatory route reaches the unit suite and all **17 named top-level
verifier/cross-check programs** (`records/invocation_graph.md:66-129`).  No
load-bearing top-level verifier is skipped.

However, import reachability is narrower than execution:

- `verify_marked_lift.py:24` imports
  `verify_resolvent_identities.solve`, which is actually called at `:28-29`.
- `verify_marked_lift.py:25` imports only
  `verify_direct_flow_screen.matrix_from_edges`, used at `:491-495`,
  `:520-524`, and `:551-555`.
- importing `verify_direct_flow_screen.py` imports four Fisher helpers at
  `verify_direct_flow_screen.py:17-22`, but the marked-lift program calls none
  of them.

Consequently the direct-flow main at
`verify_direct_flow_screen.py:99-114`, the Fisher/witness main at
`verify_fisher_route.py:773-804`, and the resolvent module's standalone examples
at `verify_resolvent_identities.py:151-170` do not run; their guards are at
`verify_direct_flow_screen.py:117-118` and
`verify_fisher_route.py:807-808` (`records/invocation_graph.md:149-171`).

The direct-flow and Fisher suites are finite/legacy diagnostics for routes to
the **open** global fitness-two problem, not dependencies of any manuscript
theorem.  `verify_marked_lift.py` itself labels the universal marked collision
inequality/global `r=2` maximality open, and the manuscript does the same at
`records/paper_extracted.txt:1578-1583`.  The used `solve()` and
`matrix_from_edges()` utilities are exercised.  This is therefore a labeling
clarification, not a proof gap.

### AF-3 — Minor robustness issues beyond the clean run

The launcher also inherits `PYTHONPATH` and `MAKEFLAGS`; dependencies are
version-pinned but not artifact-hash-pinned, and Tectonic may obtain cached or
network resources (`records/software_source_audit.md:109-128,425-438`).  The
official audit mitigated these risks with an empty environment, isolated
HOME/cache/tmp paths, a declared package index, exact version gates, and a
byte-identical PDF comparison.  Future replay instructions should sanitize
these variables and preferably use hash-pinned artifacts.  No mismatch was
seen in the frozen official run.

The unused legacy `make paper1` target points to an omitted tree
(`Makefile:29-31`) but is never called by the mandatory route.  This is a
maintenance issue only.

## Adversarial mathematical analysis

### 1. Model orientation, normalization, and phase order

The model consistently uses raw `W[source][target]` and normalized
`P[target][source]`; equation (2.1) is the governing convention.  The
independent orientation sentinel multiplied incoming columns and obtained
exactly unchanged kernels and fixation, while deliberately normalizing source
rows changed the answer (`records/independent_crosschecks.md:62-78`).  The
directed strong-selection examples and the cited Tkadlec model use the same
orientation (`records/strong_selection_low_order_audit.md:68-95`).  No hidden
transpose or reversibility assumption survived these checks.

The rectangular phase typing is also consistent.  The empty-cache space
`Z_n`, nonempty-cache space `Y_n`, `K=RA` on `Y_n`, and `M=AR` on `Z_n` are
defined at `records/paper_extracted.txt:384-401`.  The stationary transports
and collision order are explicit at `:431-480`.  Four nonsymmetric directed
kernels independently satisfied

`n*rho_dB(P,2)*(nu H)=1`

exactly (`records/independent_crosschecks.md:80-99`).  Thus the marked/current
proof does not silently exchange sample-then-retarget with
retarget-then-sample, lose the singleton empty-cache boundary, or introduce an
extra factor two.

### 2. Hessian sign, normalization, and complete tangent coverage

The tangent decomposition in (4.8)-(4.10) has dimensions

`n-1`, `n(n-3)/2`, and `(n-1)(n-2)/2`,

which sum to `n(n-2)`; the symmetric sector is genuinely absent at `n=3`
(`records/paper_extracted.txt:544-566`).  The representations are pairwise
nonisomorphic and multiplicity-free, so no cross-sector form is omitted.

The independent literal active-resolvent calculation reconstructed `K_0`,
`Delta`, `G`, the stationary law, and `R_2` without using a delivered expected
implementation.  It obtained zero first variation and all eight displayed
Frobenius-normalized values at `n=3,4,5`, exactly matching (4.12)
(`records/independent_crosschecks.md:101-130`).  This specifically tests the
standard embedding norm, symmetric factor two, antisymmetric norm, and
physical sign.

From

`1/(n rho_epsilon)=c_0+epsilon^2 R_n^(2)(delta)+O(epsilon^3)`,

inversion gives the fixation second derivative

`-2 m_n^2 R_n^(2)(delta)/n`,

as stated at `records/paper_extracted.txt:220-238`; there is no missing factor
two or sign reversal.  A separately solved directed mixed-sector example also
matched the exact forward-chain second-order coefficient
(`records/fitness_two_local_audit.md:82-114`).

The positive-kernel hypothesis loses no tangent direction because `J_n` is an
interior point and every fixed tangent remains positive for sufficiently small
two-sided epsilon (`records/paper_extracted.txt:240-245`).  Fixed-`n` negative
definiteness plus analyticity supplies a uniform remainder on a small
fixed-`n` ball.  It does not supply a radius uniform in `n`, and the manuscript
does not claim one.

### 3. Finite certificates and analytic endpoints

Every required order is covered without overlap ambiguity or a missing
endpoint:

- standard: exact `2<=N<=9`, analytic and strict for `N>=10`;
- antisymmetric: analytic for every `N>=2`;
- symmetric: exact solves `3<=N<=39`, all 248 exact margins
  `40<=N<=287`, and analytic discriminant certificate `N>=288`.

The local audit checked the standard endpoint bound, antisymmetric strict
coupling, symmetric Schur sign/debt, the `N=40` exact minimum, and the large
order leading-sign/discriminant implications
(`records/fitness_two_local_audit.md:140-196`).  The manuscript explicitly
separates the finite and analytic obligations at
`records/paper_extracted.txt:1411-1460`; it does not extrapolate samples to all
orders.

The executable antisymmetric recurrence stops at `n=40` and the literal active
check at `n=7` (`verify_antisymmetric_hessian.py:148-157`).  Its printed
"every n" sentence is broader than the loop alone, but the all-order result is
the manuscript coupling/recurrence proof in
`appendices/A_sector_certificates.tex:247-328`.  That proof was independently
audited and no transferred or circular gap was found.

The finite symmetric range ultimately trusts exact Python/FLINT solves.  A
second independent solver did not repeat all 37 orders `3<=N<=39`, although
literal active/orbit computations agree at small orders and the delivered
solver exhausts the range exactly.  This is the residual computer-assisted
trust boundary, not an identified mathematical failure.

### 4. Strong-selection quantifiers and support boundaries

Theorem 2 explicitly fixes both `n` and positive complete-support `W` before
`r` tends to infinity (`records/paper_extracted.txt:262-272`).  Direct
first-step differentiation gives pair extinction coefficient

`(a_ij+a_ji)/[n(n-2)]`

and the column sum-of-squares identity (5.15)-(5.16)
(`records/paper_extracted.txt:666-749`).  Four nonsymmetric literal chains
reproduced `E_dir/[n^2(n-2)]` exactly
(`records/independent_crosschecks.md:132-148`).  The `O(r^-2)` term may depend
on the fixed weighting; no uniformity toward a zero-weight face is asserted.

The support cases are exhaustive:

1. positive complete support is Theorem 2;
2. strongly connected noncomplete support is the cited Tkadlec theorem; and
3. reducible support is handled by the source-SCC bound (5.17).

The source-SCC direction is correct: a source component has no incoming parent
edge, so an initially resident source cannot be invaded.  The resulting bound
and the undirected adjacent-pair limiting argument were independently derived
(`records/strong_selection_low_order_audit.md:97-128`).

The fixed-structure quantifiers are stated explicitly at
`records/paper_extracted.txt:158-170` and `:1574-1583`.  No step interchanges
`n` and `r`, gives a uniform `r_0`, or excludes a growing amplifier family.

### 5. Boundaries and equality classes

- `n=2`: the normalized loopless kernel space is a singleton, so every
  admissible positive weighting ties; the singular `1/(n-2)` theorem begins at
  `n=3`.
- `n=3`: the symmetric tangent dimension is zero; standard and antisymmetric
  sectors exhaust the tangent space.
- `r=1`: the complete formula is interpreted continuously and the low-order
  differences contain `r-1`; strict equality classifications are correctly
  limited to `r>1`.
- Zero support: Theorem 2 deliberately excludes it; strongly connected
  missing-edge supports and reducible supports are handled separately.
- Triangle equality: the exact centered sum-of-squares is strict away from
  equal positive edge weights.
- `G_13`/`G_22`: the square-root coordinates cover all positive parameters up
  to the stated symmetry, and equality reduces exactly to `x=1` or
  `x=y=1`.  No unrestricted six-edge `K4` classification is claimed.

These endpoints were also tested on literal exact subset chains, including
near-zero and connected zero-support controls
(`records/strong_selection_low_order_audit.md:203-278` and
`records/independent_crosschecks.md:150-173`).  No boundary equality was
misreported.

### 6. Citation dependency

Corollary 3 materially depends on Tkadlec et al. (2020) for the strongly
connected noncomplete-support case; the manuscript does not present that
external proof as an internal certificate.  The cited source was checked
against its model and proof.  Its main text states the directed/weighted
noncomplete theorem at `work/independent_refs/Tkadlec2020_main.txt:366-380`,
and the supplement supplies the theorem and `2N^2` bound at
`work/independent_refs/Tkadlec2020_S1.txt:354-382`.  Its no-self-loop,
strong-connectivity, uniform initialization, target-first dB update, edge
orientation, and advantageous-fitness hypotheses match the manuscript
application (`records/strong_selection_low_order_audit.md:68-95`).

The supplement has an internal results-list numbering typo (calling this
Theorem 2 rather than the published main-text Theorem 1), but its statement and
proof are unambiguous.  This is not a citation defect.

### 7. Low-order algebra and proof/code alignment

The triangle certificate was independently regenerated from all six transient
equations, with an M-matrix denominator and exact centered sums of squares
(`records/strong_selection_low_order_audit.md:130-155`).  Both symmetric `K4`
families were independently regenerated from their lumped transitions and
cross-checked against literal 14-transient-state chains; the 123-term `P_22`
denominator and all `g,d,t` coefficients matched
(`records/strong_selection_low_order_audit.md:157-193`).  These hardcoded
expressions are checked against independently derived rational functions and
are not circular transcriptions.

The official replay reaches every theorem-bearing top-level program.  Some
programs begin from manuscript-derived quotient/recurrence formulas, so they
check algebra, finite ranges, and signs rather than independently derive the
reduction.  The manuscript supplies the analytic reductions; independent
literal chains test orientation, phase order, and normalization.  This division
of labor is legitimate and disclosed.

## Strongest verified result

For every fixed `n>=3` and every nonzero `delta` with zero diagonal and zero
row sums,

`R_n^(2)(delta)=nu_0 Delta G Delta G(H-c_0 1)>0`.

The standard, antisymmetric-balanced, and symmetric-balanced sector scalars
cover all existing irreducible tangent components and are positive on their
complete order ranges.  Hence

`D rho_dB(J_n,2)[delta]=0`

and

`D^2 rho_dB(J_n,2)[delta,delta]
 = -(2m_n^2/n)R_n^(2)(delta)<0`.

Finite-dimensional analyticity upgrades this to a strict nondegenerate local
maximum in an `n`-dependent neighborhood in the full directed normalized
kernel space.  Independently, every fixed positive complete-support weighting
has the sharp incoming-column sum-of-squares strong-selection deficit; the
cited noncomplete theorem plus the verified reducible closure proves the
fixed-finite universal-amplifier obstruction.

## Exact remaining gaps and nonclaims

No unresolved gap was found inside a stated theorem.  The exact residual
limitations are:

1. The replay must be hardened against optimization before an arbitrary PASS
   transcript can be accepted as a certificate.
2. The exact symmetric orders `3<=N<=39` rely on the delivered FLINT solver;
   there is no second independently authored solver for all 37 orders.
3. Exact computation assumes correct CPython, SymPy, and python-flint rational
   arithmetic, and the current install artifacts are version- but not
   hash-pinned.
4. The direct-flow/Fisher guarded diagnostic mains do not execute, but they are
   not theorem dependencies.
5. Global fitness-two maximality, an explicit or population-uniform local
   radius, interchange of `n` and strong-selection limits, unrestricted
   weighted `K4` classification, and growing-family classification remain open
   exactly as disclosed at `records/paper_extracted.txt:1566-1583`.

Subject to item 1's small replay correction, the proof, finite certificates,
official replay, and independent exact calculations support the same stated
mathematical conclusions.
