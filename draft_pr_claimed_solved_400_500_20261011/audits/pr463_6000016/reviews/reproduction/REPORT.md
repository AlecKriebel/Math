# Independent reproduction and consistency audit: PR 463

Review identity: `/root/pr463_reproduction`. Problem 6000016 / AMR-059-0016, “Stability of Hessian Metrics.” Frozen eligible head: `982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649`. Audit performed 12 October 2026 UTC.

**PASS for mathematical consistency and reproduction of the frozen result. No mathematical blocker or required source repair was found.** The argument excludes every smooth positive-definite Hessian metric on each nonzero fiber of the stated affine-torus family. The computations reproduce exactly and the independently authored controls reject deliberately corrupted mathematics and evidence. This report is an AI verification, not human peer review, a literature-priority certificate, a paper-readiness review, or permission to publish.

The initial hypothesis was saved in `INITIAL_HYPOTHESIS.md` before reading the historical audit verdict or any new peer conclusion. All fourteen original frozen artifacts were subsequently read; the duplicate historical author rerun was also parsed and byte-compared. No original artifact was modified. Verification used the existing pinned Python interpreter read-only. All temporary source copies, mutated programs and malformed result files were confined to this review's `private_cases` and removed after each run. There were no service writes, network requests, PR actions, original proof-search attempts, or changes to another effort.

## 1. Claim, hypotheses, and success criterion

On the fixed smooth torus `R²/Z²`, let the global frame be `X=∂x`, `Y=∂y`. The hypothesis to verify is that

\[
D^t=D^0+t\,dx\otimes dx\otimes Y,\qquad t\in\mathbb R,
\]

is a smooth family of complete torsion-free flat connections; the central fiber admits a positive-definite Hessian metric; and every noncentral fiber admits none. This gives a negative answer to the unrestricted stability assertion as identified in the frozen source gate.

“Hessian” here means a smooth positive-definite metric locally equal to the Hessian of a potential in affine coordinates. A global potential is not required. The quantifier is over all smooth metrics, without translation invariance, diagonal form, parallelism, proximity to the central metric, or a prescribed dependence on the parameter. Completeness and preservation of a volume form are additional verified properties, not hypotheses needed for Stokes. The claim does not extend to indefinite metrics, noncompact covers, the separately stated hyperbolic case, or fixed linear holonomy.

The success criterion is the analytical contradiction for arbitrary such metrics, plus independent checking of the connection/developing/holonomy/geodesic identities, immutable-source accounting, exact reproducibility in both optimization modes, and meaningful controls that fail through actual program entrypoints. Finite symbolic counts alone cannot establish the arbitrary-metric quantifier or the positivity/integration step.

## 2. Full frozen-input and historical-binding accounting

`SOURCE_RECEIPT.json` identifies exactly PR 463 and problem 6000016 at the head above. Its selected queue row agrees byte-for-byte with `selected_queue_row.md` and has status exactly `claimed_solved`, turns `1/5`. This is a frozen eligibility attestation; the parent workflow must still check live eligibility before service writes.

Every listed source path, byte count and SHA-256 was independently checked. The complete on-disk inventory is exactly those **14 files**, with no extra artifact omitted from this review. Their exact records are in `reproduction_normal.json`, under `integrity.frozen_files`. All remained unchanged after both driver runs.

The following advertised historical references were checked against actual bytes:

| Historical object | Path references | Verification |
| --- | ---: | --- |
| `FROZEN_AUTHOR_MANIFEST.json` | 6 | All present; exact SHA-256 and byte counts |
| `audit/AUDIT_MANIFEST.json` file list | 4 | All present; exact SHA-256 and byte counts |
| `PUBLICATION_MANIFEST.json` | 13 | All present; exact SHA-256 and byte counts |
| Audit standalone frozen-author-manifest and frozen-proof fields | 2 | Both actual source objects present; exact hashes |

Thus **25 references** were verified. They include repeated references to the same files; they are not 25 distinct payloads. **No missing or unattested historical reference was found in this packet.** The publication manifest legitimately omits itself from its internal list; its actual bytes are independently bound by the external 14-file source receipt. The audit manifest's `author_files_unchanged` field is an actual Boolean `true`, with its factual content rechecked rather than inferred from the flag.

Important frozen digests:

- Proof: `783f927e0e1bcc309547ad58371a64aeb4428553bfc329df22c980a2b8f0bdb0`.
- Author checker: `76839bdc7a403d3552f6d1bfbe717d903524455a86b6a8f9ea0ade43b58c122a`.
- Audit checker: `a91b60e80a5b72d2565621632225fa230e30f293474f6ffde0d887430543ddf8`.
- Author manifest: `376b54e387e261f5dfdde1058ecf6c2fc889823a54fead31350584716848c896`.
- Publication manifest: `075a5fa8b15cf4e5bd1fd8a9fd32a8ff2f2a7086d4e3dceb79e4026489c62d71`.

## 3. Reproduction and optimized-Python assessment

Both original programs were read in their entirety before running them from an unrelated working directory, with copied inputs outside the original snapshot. The actual programs are `check_exact.py` and `audit/check_audit.py`; there is no separate file called `authorcheck_exact.py` in the frozen inventory.

The historical result objects do **not** contain 41 or 61 Boolean success fields. They contain status strings, integer counts, and ordered lists of check names. This distinction matters: a count or a truthy payload is not an independent proof that each identity was checked. Each original helper actually evaluates a symbolic residual and explicitly raises `AssertionError` if it is nonzero; a name is appended only after the test succeeds.

AST inspection finds **zero `assert` statements** in either historical program. Explicit `raise AssertionError(...)` statements remain effective under Python `-O`. The independent runner additionally propagates `PYTHONOPTIMIZE=1` to the historical audit's nested author subprocess in its optimized runs.

| Program | Normal and optimized result | Stdout bytes | Stdout SHA-256 |
| --- | --- | ---: | --- |
| Author checker | Exact 41-name list; exit 0; empty stderr | 1,363 | `f5ef9ddfd0786fde75c53bb338d7d759162aa44f6f86d9f91af41789fb818d25` |
| Audit checker | Exact 61-name list; exit 0; empty stderr | 2,532 | `fd5dd563121a6da7d398728eeae1951410f844bd7f0fd10a41d6bcaa937b9286` |

Each stdout is byte-for-byte identical to the corresponding frozen result JSON. The historical `author_rerun.json` is also byte-for-byte identical to the author's frozen result. The 61 audit controls comprise 22 integrity/reproduction controls and 39 algebraic/boundary controls; these are not 61 separate mathematical theorems.

The independent driver uses duplicate-key rejecting JSON parsing, exact key sets, strict integer types excluding Booleans and floats, exact ordered check-name inventories, unique names, correct status, and nonempty textual scope fields. Thus it does not accept a merely truthy value or a fabricated name/count. Byte equality to the frozen output also binds the exact historical scope text. It does not upgrade that text into an independently established source or priority claim.

Both complete runs of `reproduce.py`, with and without `-O`, produce the same **35,715-byte** result, SHA-256 `830e5e221a257dfd50a01550a2764bcf8ab72f19306b0c1156fc327d182abfb5`. The runner makes no writes to source inputs. It needs Python with SymPy for subprocesses; the tested versions are Python 3.14.6, SymPy 1.14.0, mpmath 1.3.0.

## 4. Independently verified analytical argument

### 4.1 Global affine connection and completeness

Although `x,y` themselves are not global real-valued functions on the torus, `dx,dy,X,Y` are globally defined, translation-invariant tensors. Hence adding `t dx⊗dx⊗Y` to the standard connection is legitimate on the fixed quotient. Symmetry of its two covariant input slots gives zero torsion.

The only nonzero coefficient is `Γʸₓₓ=t`. In the quotient frame the connection matrices are

\[
K_x=\begin{pmatrix}0&0\\t&0\end{pmatrix},\qquad K_y=0.
\]

Their coefficients are constant, their traces vanish, and every product `K_i K_j` vanishes. Thus curvature vanishes and `dx∧dy` is parallel. These facts hold for every real parameter, not only a sampled set.

On the cover, the coframe `(dx,dy+t x dx)` is the exact differential of

\[
F_t(x,y)=(x,y+t x^2/2).
\]

Its Jacobian is invertible with determinant one, and its inverse map is `(u,v)↦(u,v-t u²/2)`. Computing `J⁻¹∂_iJ` recovers the matrices above. This proves the connection is the pullback of the ordinary affine connection. The inverse is defined on all of the affine plane; completeness is not inferred merely from flatness or volume preservation.

Independently, for any real initial positions and velocities, the lifted geodesic is

\[
x(s)=x_0+a s,\qquad y(s)=y_0+b s-t a^2s^2/2.
\]

It exists for all real `s`, satisfies both geodesic equations and the initial data, and develops to an affine straight line. Quotienting a globally defined lifted geodesic gives a complete torus geodesic.

### 4.2 Descent, holonomy, and deformation parameter

Conjugating every integer translation `(m,n)` by `F_t` yields

\[
(u,v)\mapsto(u+m,v+n+t m u+t m^2/2).
\]

The composition law is addition in `Z²`; the quadratic term is essential for the cross term `t m p`. The action is a smooth conjugate of ordinary integer translations, hence free, properly discontinuous and cocompact for every real `t`. There is no integrality requirement on `t`. A developing map need not descend to a self-map of the original Euclidean torus; this equivariance is the correct descent condition.

Parallel transport along an `x`-loop has matrix `[[1,0],[-t,1]]` in the quotient frame, inverse to the corresponding deck linear part `[[1,0],[t,1]]` in developing coordinates. This independently checks the sign convention and shows that the linear holonomy changes at nonzero parameter. Therefore this is not a fixed-linear-holonomy example.

The connection family is genuinely smooth on the fixed compact torus: `D^t-D^0=tS` for a fixed smooth tensor `S`, so it tends to zero in every `C^k` seminorm. Fixed coordinate neighborhoods with lifted charts and the maps `F_t` give affine transition functions varying smoothly in `t`. Developing maps converge in `C∞` on every compact subset of the cover; uniform convergence on the entire noncompact cover is not asserted or needed. At `t=0`, the standard positive metric is locally the Hessian of `(x²+y²)/2`, with no need for a global potential.

The original audit discusses the nonsmooth period expression involving the real cube root. It is irrelevant to the ordinary affine-deformation topology just verified. If a smooth cubic reparameterization is desired, `t=s³` gives the same exact obstruction on every nonzero fiber and a smooth connection family. This report verifies that substitution mathematically; it does not independently certify the literature's period-coordinate statement.

### 4.3 All-metric Codazzi identity and Stokes obstruction

Let an arbitrary smooth metric on the torus have coefficient matrix `[[A,B],[B,C]]` in the global quotient frame. Its coefficients lift to smooth functions periodic in both `x` and `y`. In particular, they are not coefficients in developing coordinates. For a positive-definite metric, `C=g(Y,Y)>0`, since `Y` is nowhere zero.

Local affine Hessian potentials imply symmetry of `Dg` in its first two slots by commutation of third partial derivatives. This necessary identity is tensorial, so it may be evaluated in the quotient frame. Direct differentiation gives

\[
(D_Xg)(Y,X)=\partial_xB-tC,\qquad
(D_Yg)(X,X)=\partial_yA.
\]

Thus every candidate Hessian metric must satisfy

\[
\partial_xB-\partial_yA=tC.
\]

There is no invariance or ansatz restriction on `A,B,C`. No sufficiency of Codazzi is needed: one necessary condition already contradicts positivity. The other independent component is `∂xC-∂yB=0`, consistent but unnecessary for the contradiction.

The globally defined one-form `α=g(X,·)=A dx+B dy` therefore satisfies

\[
d\alpha=tC\,dx\wedge dy.
\]

Stokes on the compact torus without boundary yields `0=t∫C dx dy`. Equivalently, the integrals of the two periodic derivatives cancel opposite unit-square boundary values. Continuity and strict positivity on the compact torus give a positive minimum of `C`, so its integral is strictly positive. Consequently `t=0`. This excludes **every** smooth positive-definite Hessian metric for **every real nonzero** parameter, including negative parameters and arbitrarily small parameters. This is the quantified analytical proof; the finite identities are supplements.

## 5. Independent derivations and boundary cases

`independent_identities.py` supplies **43 exact identities** derived through the affine coframe, arbitrary pulled-back potentials, parallel-transport equation, affine-line geodesics, and the arbitrary-metric exterior-derivative expression. The script does not import either historical checker. Normal and optimized outputs agree exactly, with SHA-256 `1da0af18405bf66ec5b620ee7d08f701f24a3a44a1808b04316538c72d9d72e5`. Its own guards explicitly raise exceptions.

The following boundary checks substantiate the limits of the claim:

- **Local positive metric, noncompact cover.** Pulling back the Euclidean Hessian metric gives `dx²+(dy+t x dx)²`, positive definite with determinant one. Its coefficient `B=t x` changes by `t` under `x↦x+1`, so for nonzero parameter it fails to descend. Its derivative integral is the uncanceled boundary term `t`; this explains precisely why the compact global Stokes obstruction does not apply locally.
- **Indefinite global metric.** The metric `2 dx dy` descends and is locally Hessian for every parameter. Its affine-coordinate potential is `uv-t u³/3`; pulling its Hessian back yields exactly that constant metric. Its determinant is `-1` and `C=0`, so positivity fails. This falsifies any extension of the theorem to indefinite metrics.
- **Central parameter.** At zero, the standard positive metric is locally Hessian and the obstruction vanishes. No claim of nonexistence is made there.
- **Signed and cubic parameters.** The symbolic obstruction is checked for positive and negative rational substitutions and for `t=s³`; the analytical equality handles all real parameters. The finite substitutions are diagnostics rather than the proof of the universal parameter statement.
- **Periodic derivative illustration.** A general finite Fourier example has zero derivative integral. The report's Stokes/periodicity proof, rather than that finite family, handles arbitrary smooth coefficients.

No numerical approximations, tolerance thresholds, unit choices, statistical assumptions, or stability-sensitive floating-point calculations enter the argument or its controls.

## 6. Actual rejecting controls and their limits

Each complete driver run performs **98 actual subprocess rejection controls**, with each invalid case tested in normal and optimized Python. Both whole driver modes perform the same controls, yielding 196 successful rejection executions overall. Invalid code and payload files are private temporary fixtures, not publication artifacts. Public result JSON contains case names, optimization mode, actual exit code and observed error class; it does not contain the mutated source or fabricated results.

| Entry tested | Executions per driver run | Invalid inputs |
| --- | ---: | --- |
| Author checker with private mathematical mutation | 16 | Wrong connection sign/slot, missing developing factor, missing holonomy quadratic term, wrong holonomy linear sign, wrong geodesic sign, wrong Codazzi sign, wrong central potential |
| Audit checker with private mathematical mutation | 8 | Wrong connection sign, missing holonomy quadratic term, wrong Codazzi sign, wrong geodesic sign |
| Original audit checker against altered private frozen inputs | 8 | Modified proof, checker, result file, or author manifest |
| Strict evidence-validator CLI | 66 | False/wrong status, Boolean/float/string/wrong counts, missing/duplicate/renamed/reordered/nonstring checks, extra/missing fields, empty scope, duplicate JSON keys, malformed JSON, Boolean audit author count |

The first 32 cases fail through the actual historical checker entrypoints with nonzero exit and `AssertionError`. The 66 schema cases fail through `reproduce.py --validate-result ...` with exit code **4** and `InvalidEvidence`. Valid author and audit results are also accepted through that same validator CLI in both modes, preventing a vacuous reject-everything control. These tests prove that the tested invalid payloads are rejected; they do not prove immunity to every imaginable malicious program or strengthen the mathematical theorem.

The historical programs are pinned mathematical artifacts, not generic untrusted-JSON validators. Their original result-count checks do not independently enforce every schema detail, but exact pinned source/result hashes and successful full replays bind the correct actual result. The new strict driver adds explicit schema protection without rewriting historical evidence.

## 7. Strongest verified result and exact remaining gap

The strongest verified mathematical result is the complete nonexistence theorem for arbitrary smooth positive-definite Hessian metrics on every nonzero fiber of this complete volume-preserving affine-torus family, together with smooth convergence to the positive Hessian central fiber. There is **no remaining mathematical or reproduction gap within that formulation**.

The family is explicitly credited in the frozen proof to Baues–Goldman. This audit does not claim a new family, first resolution, continued openness, or historical novelty of the obstruction. Independent reading of the primary source and an in-depth current priority search are separate tasks of the parent workflow and its other approach families. I have not treated the historical source-inspection prose as a new visual inspection by this reviewer. A future paper and verification package require their own fresh complete-package reviews; this mathematical audit does not approve those uncreated materials.

Author accounting remains the original **1/5**. This effort made no additional original proof-search attempt, edited no historical snapshot, and executed no administrative publication or merge step.

## 8. Reproduction instructions

Use Python with SymPy available. From any working directory, run the absolute path to this review's `reproduce.py`, supplying `--python /path/to/python-with-sympy` if the runner's own interpreter lacks SymPy. Running the same command with `python -O` must produce the identical recorded driver JSON. The review expects the original adjacent source snapshot and external source receipt; it does not fetch missing evidence.

The stand-alone `independent_identities.py` needs only Python and SymPy, reads no repository source, writes nothing, and can be run normally or with `-O`. Its records are `independent_normal.json` and `independent_optimized.json`. The full driver records are `reproduction_normal.json` and `reproduction_optimized.json`. `RUN_ENVIRONMENT.json` records tested dependency versions, without shipping an environment or private interpreter path.

`PUBLIC_OUTPUT_WHITELIST.json` is a positive SHA/size list of this review's authored evidence. Its own hash is reported externally to avoid circular self-binding. It excludes private sources, private cases, environments, caches, foreign PDFs, page images, source extracts, malformed payload files, and credentials.
