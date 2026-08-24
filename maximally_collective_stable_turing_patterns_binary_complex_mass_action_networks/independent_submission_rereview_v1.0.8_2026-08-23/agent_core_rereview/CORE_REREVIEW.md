# Independent v1.0.8 rereview: algebraic/core mathematics

## Bottom line

**The assigned algebraic core remains independently verified in v1.0.8.** I
found no false statement, new gap, or mathematical defect introduced by the
tag change.  No central hypothesis, quantifier, endpoint, conclusion, or
headline claim changed: extracting all proposition, lemma, theorem, and
corollary environments from `main.tex` gives a byte-for-byte identical result
for v1.0.7 and v1.0.8.

The two revised linear-algebra passages are correct.  The `b=2a` SCC paragraph
now states the missing structural observation that the deleted edge belongs to
neither long cycle.  The new three-by-three Schur remainder is the actual Schur
complement and has determinant `2 a^2 b`, including the direct `m=3` case.

The new `verify_generic_cubic_recurrence.py` is a substantive exact
all-dimensional algebraic bridge, not a finite regression: with symbolic `m`
and a formal harmonic sum, it verifies the printed kernel identities,
zero-mode and second-harmonic recurrences, boundary solve, interior sum,
cubic contraction, and scaled-family gauge contraction.  It closes the
specific **software-evidence** limitation noted in the v1.0.7 audit, where full
cubic contractions were checked only in finitely many dimensions.  It does not
replace the human derivation of the local recurrences or the separate
denominator/sign proofs, and its `PASS` line must not be described as a proof
of the nonlinear theorem by itself.

This conclusion is restricted to the assigned algebraic/core rereview.  The
new Fredholm, sectorial, and branch-stability exposition at main lines 744--808
and supplement lines 947--1015 belongs to the functional-analytic audit.

## Source identity and comparison basis

- Target: tag `maximally-collective-stable-turing-v1.0.8`, commit
  `b4607c4cc9fe6931cedbbd0c5cd7e6e68a704f9f`.
- Read-only target snapshot:
  `independent_submission_rereview_v1.0.8_2026-08-23/source_snapshot/`.
- Baseline: the complete independent v1.0.7 core review and reaction-level
  reconstruction in
  `independent_referee_audit_v1.0.7_2026-08-22/agent_core_math/`.
- SHA-256 hashes of the snapshot copies of `manuscript/main.tex`,
  `manuscript/supplement.tex`,
  `proof_audit/all_spectrum_localization.tex`, and
  `independent_verifier/verify_generic_cubic_recurrence.py` exactly match their
  v1.0.8 tag blobs.
- I did not rely on `FEEDBACK_DISPOSITION`, stored logs, or prior `PASS`
  markers.  I compared the full tag diff, reread every modified core passage
  and its current cross-references, read all 309 lines of the new verifier, and
  used the prior full reading for unchanged manuscript sections.

The load-bearing mathematical source changes are:

1. SCC clarification: `manuscript/main.tex:304-308`,
   `manuscript/supplement.tex:93-97`, and
   `proof_audit/all_spectrum_localization.tex:31-34`.
2. Explicit core Schur remainder: `manuscript/main.tex:354-361`,
   `manuscript/supplement.tex:105-124`, and
   `proof_audit/all_spectrum_localization.tex:67-85`.
3. New exact cubic bridge:
   `independent_verifier/verify_generic_cubic_recurrence.py:1-309`, aggregated
   by `independent_verifier/verify_symbolic_certificates.py:19-38`.

The other manuscript changes add functional-analytic detail and update release
metadata.  No exact algebraic table or central formula was changed.

## 1. Revised SCC exhaustion at `b=2a`

The current graph convention and proof are at
`manuscript/main.tex:260-309` and `manuscript/supplement.tex:65-103`.
For the Jacobian entry convention `X_j -> X_i` when `A_{ij}` is nonzero, the
only coefficient that can vanish for positive `a,b` is

```text
A_{m1}=2a-b,
```

so at `b=2a` precisely the edge `X1 -> Xm` is deleted.  The two long cycles are

```text
X1 -> X2 -> ... -> X_{m-1} -> X1,
X2 -> X3 -> ... -> Xm -> X2.
```

Neither uses `X1 -> Xm`.  Consequently their vertex sets, edge sets, and
characteristic-equation derivations remain valid at the exceptional
hypersurface.  Any other non-singleton SCC in a proper induced set lies in the
boundary triad `{X1,Xm,Z}`.  Deleting an edge cannot merge SCCs; any split
component is still a principal subgraph of that triad.  This is the exact
observation omitted from the shorter v1.0.7 prose, and the revised statement is
deductively complete.

The base case is not hidden in the chain argument.  At `m=3`, the two complete
long cycles are the pairs `{X1,X2}` and `{X2,X3}`, while every other
non-singleton component is a pair in `{X1,X3,Z}`
(`manuscript/main.tex:277-282`; `manuscript/supplement.tex:73-76`).  The deleted
edge is `X1 -> X3`, again in neither pair.

Independent corroboration reconstructed `A_m(a,b)` from the reaction list and
enumerated every induced set of size below `m` for `m=3,...,8`, both at a
generic positive point and at `b=2a`.  No SCC outside the claimed three classes
occurred.  This enumeration is finite corroboration only; the preceding path
argument is the all-dimensional proof.

**Classification:** Lemma 3.1, independently verified (deductive, with exact
finite exhaustive corroboration).  The revision repairs an expository
omission without changing any hypothesis or conclusion.

## 2. New three-by-three Schur remainder

The added calculation is at `manuscript/supplement.tex:105-124`.  After
factoring the positive column scalings `prod_i h_i`, order the boundary
variables as `(X1,X2,Xm)` and the interior variables as
`(X3,...,X_{m-1})`.  For `m>=4`, the interior block is

```text
E = -a I + a L,
```

where `L` has ones on the first subdiagonal.  Hence

```text
det(E)=(-a)^(m-3),
E^(-1)=-(1/a)(I+L+...+L^(m-4)),
```

and its bottom-left entry is `-1/a`, exactly as printed.  Only the last
interior column and first interior row couple to the boundary.  The Schur
complement is therefore

```text
[ -(a+b)   -a       -b      ]
[ -a       -a        2a     ]
[ 2a-b      2a      -(4a+b) ]
```

with determinant `2 a^2 b`.  Thus

```text
det(A_X)=(-a)^(m-3) 2a^2b,
(-1)^m det(J_X)=-2a^(m-1)b prod_i h_i < 0.
```

For `m=3`, the interior block is empty and the displayed matrix is the original
three-species `X` block, so the same determinant formula holds without an
empty-block ambiguity.  Direct symbolic Schur complements for `m=3,...,8`
matched the displayed matrix exactly.

This validates the final step of Theorem 3.2 at
`manuscript/main.tex:311-362`: the characteristic polynomial of the full
`X` block is negative at zero and positive for large positive real lambda, so
it has a positive real eigenvalue.  Together with the unchanged long-cycle
modulus inequalities and boundary-triad Routh--Hurwitz proof
(`manuscript/main.tex:328-352`), every smaller nonempty principal subsystem is
Hurwitz and the first possible instability order remains `m=n-1`.

**Classification:** Theorem 3.2, independently verified.  The added calculation
is correct proof detail; it changes neither theorem nor formula.

## 3. Semantic audit of `verify_generic_cubic_recurrence.py`

### What it genuinely checks

The program imports only SymPy and no project construction helper
(`independent_verifier/verify_generic_cubic_recurrence.py:11-18`).  It works in
the rational function field in formal `m` and `hfrak`, not in a loop over a
finite dimension list (`:62-66`).  Its checks divide into the following
nontrivial layers:

- `:21-59`: defines the affine chain factor, the boundary determinant
  polynomial, and the claimed terminal numerator `R_m+C_m*hfrak`.
- `:68-123`: verifies every displayed boundary and generic interior identity
  for the critical right and left vectors and independently reduces
  `ell^T r` and `ell^T D r`.
- `:125-186`: verifies the closed zero-mode formula, all four boundary rows,
  the conservation gauge, and the generic interior affine recurrence.
- `:188-223`: verifies the complete four-by-four second-harmonic boundary
  system, its determinant, its printed boundary solution, and the generic
  four-factor recurrence.
- `:224-292`: reduces the only dimension-dependent interior sum by the exact
  formulas for `sum 1`, `sum j`, and `sum j^2`; rebuilds the zero-mode and
  second-harmonic contractions; and proves their sum equals the separately
  encoded `R_m+C_m*hfrak` identically.
- `:294-304`: uses the same generic contraction to verify the scaled-family
  gauge term `S_m`.

The important summation step is transparent.  With

```text
T_i = K_{i-3}K_{i-2}K_{i-1}K_i/(K_{-1}K_0K_1K_2),
```

one has

```text
T_i/(K_{i-1}K_i)
 = K_{i-3}K_{i-2}/(K_{-1}K_0K_1K_2).
```

For `i=3,...,m-1`, summing the remaining product of two affine factors gives

```text
(m-3)(24571m^2-97470m+96662)/3,
```

which the program verifies symbolically at `:224-235`.  The remaining
reciprocal terms are exactly the formal harmonic sum.  This is a valid generic
recurrence-to-closed-form proof schema; it does not extrapolate from `m<=N`.

The special case `m=3` is sound.  Then `T_{m-1}=T_2=1`, the last interior
coordinate equals the second coordinate, and the interior tail is empty once
`hfrak=1/K_1` is substituted.  A direct reaction-level solve below matched the
closed form exactly at `m=3` and `m=4`.

### What it does not check

The executable alone is not a self-contained proof of the theorem:

- It copies the printed local matrix, vector, correction, and target formulas;
  it does not reconstruct them from the indexed reactions.  Its comparison is
  not vacuous—the contraction and the terminal polynomial are assembled by
  distinct expressions—but a coordinated transcription error could be shared
  with the manuscript.
- The formal symbol is declared positive but the code does not establish the
  application domain `m>=3`, actual identity
  `hfrak=sum_{j=1}^{m-2}1/K_j`, or positivity of every denominator.
- It proves the numerator identity, not its all-dimensional sign.  The needed
  nonvanishing/positivity certificates remain at
  `manuscript/supplement.tex:353-361` and `:434-482`.
- It does not prove the center-manifold or PDE stability conclusions.

These are scope boundaries, not gaps in the manuscript.  The reaction-wise
formula for `B`, the correction equations, and the recurrence are printed at
`manuscript/supplement.tex:308-400`; the generic numerator and sign argument
are at `:402-482`.  I independently reconstructed the Hessian directly from
the reaction sources and products, solved the gauge-fixed `w_0` and unique
`w_2` over the rationals, and matched `R_m+C_m*hfrak_m` at
`m=3,4,5,8,12`.  A separate formal calculation reproduced the generic
four-factor recurrence and affine product sum without importing the new
verifier.  I also shifted and re-expanded `Q_m`, `P_R`, `P_C`, the cleared
lower-bound polynomial `L_m`, and the harmonic-bound numerator proving
`ell^T r<0`; every required coefficient is strictly positive.  These finite
direct solves are corroboration, while the local recurrence, formal sum, and
shifted sign identities are the deductive all-dimensional bridge.

### Execution and mutation controls

- Python 3.9.6 with SymPy 1.14.0: exit 0 in approximately 0.66 seconds,
  printing `GENERIC_CUBIC_RECURRENCE_PASS`.
- Optimized Python (`-O`): exit 1 with the required assertion-mode message.
- Replacing the terminal closed form in memory by the claimed value plus one:
  rejected by `AssertionError`.
- Independent reaction/Hessian control script: exit 0 in approximately 0.92
  seconds in its initial run (0.99 seconds after adding the independent shifted
  sign-certificate reconstruction); details are in
  `INDEPENDENT_CONTROL_RESULTS.md`.

The system `/opt/homebrew/bin/python3` (3.14.6) lacks SymPy and therefore failed
with `ModuleNotFoundError`.  This records the need to use the declared/project
dependency environment; it is not evidence against the identity.

**Classification:** the recurrence-to-closed-form identity and gauge
contraction are exact computer algebra with an independently checked deductive
schema.  This is materially stronger than finite regression, but a passing
program alone is evidence only for the identities listed above.

## 4. Theorem-by-theorem effect of the tag change

| Result and current location | v1.0.8 core classification | Effect of v1.0.8 |
|---|---|---|
| Proposition 2.1, flux cone/rank/conservation (`main.tex:191-220`) | Independently verified in v1.0.7 from the reaction list; unchanged | None |
| Proposition 2.2, complete positive-equilibrium Jacobian family (`main.tex:239-253`) | Independently verified; unchanged | None |
| Lemma 3.1, SCC exhaustion (`main.tex:260-309`) | Independently reverified | Exposition strengthened at `b=2a`; no claim change |
| Theorem 3.2, all-spectrum localization and first instability order (`main.tex:311-362`) | Independently reverified | Correct Schur elimination printed; no claim change |
| Theorem 4.1, principal-minor diffusion ray (`main.tex:379-428`) | Independently verified deductively in v1.0.7; statement and proof unchanged | None |
| Proposition 5.1, complete omission table (`main.tex:445-492`) | Independently verified; unchanged | The negative omission receives a more explicit upstream determinant derivation |
| Theorem 5.2, exact stationary diffusion law (`main.tex:503-549`) | Independently verified under the stated homogeneous-stability hypothesis; unchanged | None |
| Theorem 5.3, sharp contrast/product infima (`main.tex:558-596`) | Independently verified; unchanged | None |
| Theorem 6.1, unit design (`main.tex:627-808`) | Linear algebra and cubic sign independently verified; PDE stability remains citation/functional-analysis dependent | Generic cubic software bridge added; theorem statement unchanged |
| Theorem 7.1, scaled trade-off (`main.tex:844-1046`) | Algebraic family, endpoints, contrast product/optimum/asymptotics retained as independently verified; nonlinear stability assessed elsewhere | Gauge contraction receives generic symbolic corroboration; theorem unchanged |
| Proposition 8.1, robustness (`main.tex:1093-1112`) | Outside this algebraic rereview | No statement change |

The v1.0.7 outside-domain controls remain applicable because none of the
relevant hypotheses changed: omitting the positive order-`(n-1)` sum destroys
the post-threshold spectral conclusion; equality in the diffusion criterion
does not give a nonzero threshold; omitting homogeneous stability permits a
multiple conservation zero; `m=2` is a different reaction topology; and
`a=0`, `b=0`, or nonpositive `H,D` cause rank/minor degeneracies.  They confirm
the necessity and scope of the stated hypotheses and are not counterexamples
to v1.0.8.

Likewise, all equality and endpoint conclusions audited in v1.0.7 remain
unchanged: `m=3`, `m=4`, both scaled-family endpoints, the coefficientwise
modulus equality case, the current `m=149` endpoint regression, the
nonattained strict contrast infima, and the square-root asymptotic exponent.
The tag diff contains no altered coefficient, endpoint, or asymptotic formula
in those results.

## Defects, repairs, and evidentiary cautions

**No fatal, major, minor mathematical, expository, or core reproducibility
defect was found in the v1.0.8 changes.**

The `b=2a` and Schur additions are best classified as expository proof
strengthening.  They repair no false claim and change neither a hypothesis nor
a conclusion.  The generic cubic checker repairs a prior software-evidence
limitation: the supplied executable layer now contains an all-dimensional
symbolic bridge instead of relying on representative full-matrix contractions.
The underlying manuscript identity was already supported by its recurrence
proof, so this does not alter the headline mathematical claim.

Two cautions should remain explicit in the final referee report:

1. “Standalone” means that the new script imports no project helper.  It is
   not epistemically independent of the formulas it copies from the
   manuscript, and its `PASS` marker is not an independent theorem proof.
2. Finite exact direct solves and the old `verify_cubic_sign.py` remain
   regression/falsification evidence only.  The all-dimensional conclusion
   rests on the generic local recurrence, exact finite-sum identity, boundary
   determinant nonvanishing, and shifted-positive sign certificates.

## Confidence and strongest remaining uncertainty

Confidence is **high** for the algebraic core and high that v1.0.8 introduces
no mathematical regression.  The strongest possible residual concern in the
new cubic executable is shared transcription between the printed local
equations and the hard-coded checker; reaction-level direct reconstructions in
five dimensions, including `m=3`, and independent inspection of the generic
local equations substantially mitigate it.  It is not an unresolved proof
bridge.

No conclusion here upgrades the separate functional-analytic and
reproducibility audits.  Subject to those independent components, the
v1.0.8 algebraic/core findings support the same validity assessment as the
v1.0.7 review, now with stronger exposition and a genuine generic cubic
computer-algebra check.
