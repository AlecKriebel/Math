> Scope update, 14 September 2026: this is the original d=4 pilot contract.
> Its physical definitions and A-F targets remain in force. The new
> `GENERAL_STATEMENT_CONTRACT.md` and current `COVERAGE.md` supersede its original
> exclusions where General modules now contain uncompiled proof candidates.
> Neither contract records kernel acceptance.

# Statement contract: cyclic Bell Lean pilot

Established 2026-09-14, before writing proof candidates. **This is a contract,
not a certificate of completed formalization.** Consult COVERAGE.md and actual
compiler receipts for status.

## 1. Canonical source and dependency identity

Canonical manuscript: `cyclic_bell_exact_values_and_randomness/main.tex`.
Observed Git blob SHA-1: `bbd0667c934d5a34dd9c8ced50df91515cb1308c` (80,538 bytes).
Repository `main` at intake: `9f857fc6680a35ed0388e7eec48330d46606a5ba`.
The repository manifest reports manuscript SHA-256
`82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`.
That SHA-256 has **not** yet been independently recomputed in this environment;
the build runner must recompute it, rather than trust the manifest.

The TeX source is authoritative. The public PDF was not successfully retrieved
in this cloud session; no PDF inspection is claimed. Relevant TeX source ranges
read through the connected GitHub tool were 270–1170, 1675–1785, and the source
convention appendix near the end, together with the opening framework.

Target pins: Lean `leanprover/lean4:v4.19.0` (compiler commit
`6caaee842e9495688c1567e78c0e68dbb96942aa`) and Mathlib
`c44e0c8ee63ca166450922a373c7409c5d26b00b`. The existing qubit project uses
these versions. Its certification report records a completed local check;
its older umbrella-file comment about an uncompiled draft is stale. Neither
that report nor its qubit-specific theorems certify this new development.

## 2. Physical model and quantifiers

For universal finite-dimensional targets, local spaces are **arbitrary**
`C^(Fin nA)` and `C^(Fin nB)`, where nA,nB are positive integers. They are not
restricted to four. Inner products are conjugate-linear in the first argument:
`<u,v> = sum_j conjugate(u_j) v_j`. Coordinate tensor space has indices
`(Fin nA × Fin nB)`, with
`(R tensor S)_(i,j),(k,l) = R_(i,k) S_(j,l)`.

A mixed state is a positive-semidefinite Hermitian matrix rho with trace one.
A pure state is a vector psi with sum |psi_i|^2=1 and density psi psi^dagger.
Proving a universal pure-state result does not silently establish the mixed-
state contract: a checked spectral-decomposition or purification bridge is
required. The explicit witness has local dimensions exactly four and pure
state Phi4=(1/2) sum_j |j,j>.

A four-outcome PVM consists of four Hermitian idempotents, pairwise orthogonal,
summing to identity. Zero projectors are allowed in arbitrary strategies.
The explicit target projectors are rank one. A validity structure may contain
these physical conditions but must **not** contain the Bell bound, attainment,
maximality, the claimed target distribution, or a conclusion equivalent to any
of them.

For a mixed state, Born probability is
`Re trace(rho (M_a tensor N_b))`. For a pure state it is
`Re sum_i conjugate(psi_i) ((M_a tensor N_b) psi)_i`.
The reduction to the modulus square of a rank-one joint amplitude is a theorem,
not the definition of the general Born probability. A coordinate matrix model
of C^n with the Euclidean inner product represents a finite-dimensional
Hilbert space; the pilot does not claim a separately formalized isometric
transport theorem for every abstract finite-dimensional Hilbert-space type.

## 3. Index, complex, and measurement conventions

Outcomes are `Fin 4`, identified with 0,1,2,3. Alice inputs are 0,1 for family I
and 0,1,2,3 for family F. Bob inputs are 0,1,2,3,4. The designated pair is
**Alice 1, Bob 4**, using the manuscript's zero-based labels.

Set omega=i. The observable encoding is

    A = sum_a i^a M_a,
    M_a = (1/4) sum_(k=0)^3 i^(-a*k) A^k.

It is not the adjoint encoding. The general PVM-to-unitary and fourth-power
relations must be proved, or explicit PVMs must be shown to encode the claimed
matrices. `transpose` swaps indices with no conjugation; `adjoint` swaps and
conjugates; entrywise conjugation does not swap. Operator real part is
`(T+T^dagger)/2`, while scalar real part is `Complex.re`. A bar over a named
Bell functional means augmentation, not entrywise conjugation.

The maximally entangled identity is
`<Phi4|R tensor S|Phi4> = trace(R S^T)/4`. Thus the target Fourier expression
uses **a+b**, not a-b. Outcome inversion b -> -b preserves parity at d=4,
so the parity table alone cannot detect a mistaken transpose convention.
Observable encodings must also be inspected. The amplitude normalization is
1/2, the maximally entangled trace factor is 1/4, and the unnormalized
four-term Fourier probability has factor 1/64.

## 4. Exact Bell functionals

### First family: `eq:Id`, `cor:first-augmented`

    I4 = sum_(y=0)^3 Re[A0 tensor By + i^y (A1 tensor By)]
    Ibar4 = I4 + Re[A0 tensor B4].

There is no extra factor 1/4. The target upper value is
`2 / sin(pi/8) + 1`. An alternative expression is
`2 sqrt(4 + 2 sqrt 2) + 1`, but its equality to the trigonometric expression
must itself be proved. The normalization follows `rem:normalization` and the
displayed operator, not the source paper's isolated printed denominator typo.

### Second family: `eq:lambda`, `eq:second-functional`

    eta = exp(pi i/4)
    lambda_l = (-1)^(l-1) eta^(l(l-1)) / (4 sin(pi(l-1/2)/4))
    Bhat_l = sum_(y=0)^3 i^(l*y) By
    F4 = sum_(l=0)^3 Re[conjugate(lambda_l) (Al tensor Bhat_l)]
    Fbar4 = F4 + Re[A0 tensor B4].

The numerator at l=0 is -1, as is the sign of the sine denominator.
Let s=sin(pi/8), c=cos(pi/8). The four coefficients specialize to

    (1/(4s), 1/(4s), -i/(4c), -i/(4c)).

An algebraic coefficient implementation must prove the trigonometric bridge,
positivity/nonvanishing of the denominators, and normalization. The source
SOS `eq:second-sos` specializes to

    4 I - F4 = (1/8) sum_l P_l^dagger P_l,
    P_l = 4 lambda_l I - Al tensor Bhat_l.

Dependencies include `sum_l |lambda_l|^2=1` and
`sum_l Bhat_l^dagger Bhat_l=16 I`. The augmented gap adds
`(1/2) (I-A0 tensor B4)^dagger (I-A0 tensor B4)`.
Cross-party commutation follows from tensor placement; **same-party
commutation must not be assumed**.

## 5. Explicit witness

Source labels: `eq:first-strategy`, `eq:final-swap`, `app:d4`.
Let X|j>=|j+1 mod 4>, zeta=exp(pi i/8), and kappa=(0,1,3,2).

    A0 = X
    A1 = X diag(zeta^2,zeta^6,zeta^14,zeta^10)
    B4 = X
    By = entrywise-conjugate(X diag(zeta^(e_yj))).

Rows e_y are `(1,3,15,13)`, `(3,13,1,15)`, `(13,15,3,1)`, `(15,1,13,3)`.

For the target bases (`eq:q-sequence`, `eq:target-table`):

    q = (1,zeta^2,-1,zeta^6)
    u_b(j) = (1/2) i^(-b*j)
    v_a(j) = q_j u_a(j)
    M_a = v_a v_a^dagger; N_b = u_b u_b^dagger.

Then X u_b=i^b u_b and A1 v_a=i^a v_a. These eigenvalue statements and
PVM encodings, not just the table, fix outcome labels. In algebraic coordinates,
put h=sqrt(2)/2, q=(1,h+ih,-1,-h+ih), and the A1 weights are
`(h+ih,-h+ih,h-ih,-h-ih)`. The correspondence with the exponential phases
requires the usual positive sqrt/trigonometric identities; it is not an
unproved axiom or an arbitrary choice of a square root.

For the second family (`eq:second-A`, `thm:second`),

    Dl = eta^(-l*l) X diag(i^(-l*kappa_j)),
    Al = entrywise-conjugate(Dl).

This gives four Alice settings and shares A0,A1 with the first family. Reusing
a two-setting Alice tuple without this extension would not define family F.

## 6. Intended endpoints and their dependency contracts

| Milestone | Manuscript claim | Required conclusion and dependencies |
|---|---|---|
| A | `thm:exact`, `cor:first-augmented` at d=4 | Ibar4 is at most `2/sin(pi/8)+1` for every allowed mixed state and PVM tuple at arbitrary positive local dimensions. Requires a genuine arbitrary-dimension first bound and augmented-term bound. Formalizing the scalar lemma alone does not prove A. |
| B | `eq:first-strategy`, `app:d4` | Normalized Phi4 and **all** required projective measurements with the specified observable encoding. A target-only pair is partial B, not full B. |
| C | `thm:biased`, `app:d4` | Evaluation of the actual Ibar4 on the valid witness equals the bound. Attainment arithmetic alone does not imply maximality without A. |
| D | `eq:target-table`, `eq:d4-table` | Actual Born probabilities are 1/32 for even a+b and 3/32 otherwise; nonnegative, normalized, local marginals 1/4, all entries <=3/32, an entry equals 3/32, and 3/32>1/16. Requires physical target-projector validity, state normalization, Born reduction, and phase/encoding correspondence. |
| E | `sec:randomness` | An allowed **maximizing** first-family strategy has a nonuniform target distribution. Always guessing a particular odd-sum pair with trivial Eve succeeds with 3/32; no worst-Eve optimization is asserted. Requires A+B+C+D. |
| F | `lem:lambda-normalization`, `eq:second-sos`, `thm:second` | Actual second-family coefficients, global SOS and arbitrary-local-dimension mixed-state bound 5, complete valid witness attaining 5, and D. A conditional identity or a witness-only calculation is insufficient. F does not establish the first-family Conjecture-2 counterexample. |

A later first-family route may follow `lem:polar`, `lem:scalar` and functional
calculus; the canonical partial isometry and its kernel must be handled.
A different valid finite-dimensional proof is allowed if its hypotheses match A.

## 7. Exclusions and trust rules

Initially outside the pilot: all-dimensional weighted-cycle and autocorrelation
mechanisms; `thm:support-rigidity` and the passage from saturation through
support cancellation, invariance, polar kernels, and reflection ranks; qa/qc
identifications; arbitrary-Hilbert-space commuting-operator theorems; robustness;
complete maximizing faces; exact worst-case adversarial guessing probability;
canonical private randomness; binary and low-setting auxiliary results.

Only an actually executed pinned Lean check with a clean project rebuild and
recorded `#print axioms` output can establish completed formal coverage.
No `sorry`, `admit`, `sorryAx`, custom mathematical axioms, `native_decide`, unsafe
proof evaluation, or imported external solver verdict may certify an endpoint.
The permitted standard foundations are `propext`, `Classical.choice`, and
`Quot.sound`, with the actual dependency subset disclosed per endpoint.

Unfinished experiments are excluded from the candidate library's standard
import graph. The candidate library itself remains **uncertified until run**.
A self-audit is not an independent-agent audit. No separate agent was available
in the current tool environment, so no independent-agent review is claimed.


## Continuation amendment — 14 September 2026, source-only scope

The user requested maximum source completion without attempting Lean execution.
The contract's endpoints A–F and physical definitions are unchanged. Explicit
proof scripts now cover all of them at d=4. This is a source-disposition statement,
not certification; all acceptance and transitive-axiom reports remain pending.

A now uses the finite polynomial identity documented in `FIRST_FAMILY_SOS.md`:
with k=√2, s=sin(π/8), alpha=(cos(π/8)+s)/2, beta=(s-cos(π/8))/2,
P(T)=sI+2alpha*T+sT² and Q(T)=beta*I+alpha*T+alpha*T²+beta*T³.
For T_y=i^y U, U=A0†A1, the first reduced gap is
(s/2) sum_y(F_y†F_y+k G_y†G_y), where
F_y=(I+T_y)A0†-P(T_y)B_y and G_y=T_y A0†-Q(T_y)B_y.
The augmented gap adds the independent aligned half-square. Unitarity and the
required U/B_y commutation are derived from arbitrary-dimensional physical PVMs.
The constant is proved equal to 2/sin(π/8). No polar/CFC or equality-spectrum
hypothesis is supplied by the caller. This replaces the proof route only, not
its d=4 conclusion or dimensional quantifiers.

Both upper bounds use direct mixed-state trace positivity, not an unproved
pure-to-mixed reduction. The scalar upper-bound import closure contains no
concrete witness module. `ScalarData.lean` isolates the exact constants and
source coefficients; `Phases.lean` separately bridges the explicit target
coordinates. The d=4 source includes inverse PVM encoding and generic Born
nonnegativity/normalization, complete measurement families, literal source D_l
Fourier compression, and actual trivial-Eve sandwich/partial-trace identities.

The named endpoint candidates are `CyclicBell.D4.first_counterexample`,
`CyclicBell.D4.second_counterexample`, and `CyclicBell.D4.main_d4_counterexamples`.
`IsFirstMaximizer` and `IsSecondMaximizer` compare against all finite-dimensional
competitors and are proved for the witness, not assumed in a validity predicate.
A complete statement/axiom inventory is part of the standard build.

No all-dimension d theorem, abstract-Hilbert-space basis transport, arbitrary-
Hilbert-space qc theorem, supported-multiplicity theorem, canonical privacy,
or worst-case adversarial optimization is added to the formalization scope.
A self-audit and an alternate exact word-algebra check were performed; neither
is represented as an independent-agent review or a Lean proof.
