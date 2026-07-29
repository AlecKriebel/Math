# Independent audit of checkpoint 2

**Date:** 2026-07-28 PDT

**Scope:** the dimension-six falsifier, additive/heterogeneous construction
lemmas, coherence/parity audit, and cyclic Gaussian-functional no-go.

## Verdict

I found no mathematical defect in the exact claims at their stated scopes.
In particular, none of these tracks proves or claims global nonexistence at
\(d=6\). The finite ansatz exclusions, symbolic identities, exact
leg-commutant calculation, optimizer derivatives, run summaries, and
calibrations all replayed.

I did find one concrete archive-overwrite bug and one limitation in the
historical source trace. The overwrite behavior is fixed. The limitation is
now disclosed in `notes/track_d6_falsifier.md`; it affects only the
reproducibility description of exploratory numerical failures, not an exact
theorem.

## Exact and numerical replays

All commands below were run from `exceptional_ybe_spectrum/`.

### Exact certificates

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/search_gaussian_functional_d6.py
```

Outcome: all 20 sign assignments were exhausted in exact
\(\mathbb Q(i\sqrt3)\) arithmetic and there were zero survivors. Runtime was
27.18 seconds.

I also independently represented the twisted algebra faithfully on
\(\mathbb C^6\), using
\[
u=\operatorname{diag}(1,q,\ldots,q^5),\qquad
v e_j=e_{j+1},
\]
and custom exact `Fraction` pairs \(a+b(i\sqrt3)\), rather than SymPy or the
script's tensor-word dictionary. All 20 involutions had nonzero residual.
The two alternating assignments each gave 12 nonzero matrix entries, as
expected from the two nonzero group-algebra words reported by the primary
calculation.

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/verify_track_additive_scalar_gluing.py
```

Outcome: the seven displayed nonzero entries in table (MC) agree exactly,
and all assertions pass.

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/verify_track_additive_graph_flip_qutrit.py
```

Outcome: all \(4\cdot2^6=256\) qutrit
graph-phase/global-flip cases were exhausted. Every endpoint obstruction was
nonzero and every common residual-polynomial gcd was exactly \(1\).

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/verify_track_additive_su2_ansatz.py
```

Outcome: \(H^2=I_{12}\), \(\operatorname{Tr}H=0\), and the cubic residual
has 644 nonzero entries, including the exact entry \(13/8\).

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/verify_track_additive_s4_central.py
```

Outcome: the two central rank-six \(S_4\)-equivariant projectors have exact
residual entry \(-5/12\) and \(5/12\), respectively.

The numerical companion
`scripts/explore_track_additive_s4_symmetry.py` reproduced all 20
deterministic BFGS starts at seed 7 and the reported best squared residual
`64.0`. It is correctly labeled `NUMERICAL_EVIDENCE`.

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/coherence_leg_commutant_d4.py
```

Outcome:
\[
\dim\mathcal C_L=4,\quad \dim Z(\mathcal C_L)=1,\qquad
\dim\mathcal C_R=4,\quad \dim Z(\mathcal C_R)=4,\qquad
\dim\mathcal M_1=1.
\]
For finite-dimensional unital \(*\)-subalgebras of \(M_4\), these data do
give \(\mathcal C_L\cong M_2(\mathbb C)\) and
\(\mathcal C_R\cong\mathbb C^4\).

The complete majority/transposition enumeration was replayed into
`/tmp/d6_majority_audit.json`:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/d6_majority_transposition_search.py \
  --output /tmp/d6_majority_audit.json
```

Outcome: 64 words, 5,791 commuting triples, 2,220 triples admitting an
eligible \(E\), 291,840 signed candidates, 109,440 distinct trace-zero
\(H\)'s, and zero survivors. The canonical ordered-residual digest was
again
`3ed7f63a6d801d55cb068674f790bec1a8ea27b6ab50309b554b0fec92e7c756`.
The whole JSON file hash changed because `elapsed_seconds` is intentionally
non-deterministic; every substantive field, including the complete best
certificate, matched.

The independent dense reconstruction

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/verify_d6_majority_transposition_best.py \
  --certificate /tmp/d6_majority_audit.json
```

gave involution error \(1.26\times10^{-15}\), residual norm
`13.856406460551009`, and certificate-reconstruction error
\(1.02\times10^{-12}\).

### Optimizer checks and raw-run summaries

The full-space analytic-gradient check reproduced the recorded convergence:

```text
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
/Users/alec/Documents/Math/.venv/bin/python \
scripts/d6_riemannian_search.py --dimension 6 --field complex \
--symmetry z2_z3 --initial random --seed 26072800 \
--max-iterations 1 --gradient-check
```

The absolute finite-difference errors at steps
\(10^{-4},10^{-5},10^{-6}\) were respectively
`3.42e-5`, `3.43e-6`, and `2.14e-7`.

I independently finite-differenced the shifted search gradient, including
an overlap-trace penalty of `0.7`, at a new complex `charge_parity` point.
The errors at the same steps were `4.42e-5`, `4.43e-6`, and `4.96e-7`.

The deterministic shifted \(d=4\) calibration again gave cubic residual
`6.891614306094705e-16` and involution error
`6.296050253958239e-16`.

Parsing the raw logs independently gave:

- 21 full-space runs: one \(d=4\) calibration, 17 unpenalized \(d=6\)
  runs, and three partial-trace-penalized \(d=6\) runs;
- the stated best unpenalized \(d=6\) residual
  `5.361664393944234`;
- 92 distinct shifted \(K_{12}\) runs, plus the \(K_8\) calibration;
- one intentional duplicate shifted start for seed `26073047`;
- exactly 11 objective-12 landings in the 50-seed batch;
- the stated shifted-family minima and maxima.

Direct reconstruction of the stored \(d=4\) numerical candidate gives
residual `8.732408223294123e-11`. Direct reconstruction of the stored
shifted stationary point gives exceptional residual \(\sqrt{12}\), braid
residual `5.96e-10`, and \(\operatorname{Tr}(K_1K_2)=18\), agreeing with
the note.

## Derivation and scope audit

### Dimension-six falsifier

- The signed-permutation proof is valid: after multiplying by three,
  entrywise integrality forces \(H_{12}=H_{23}\), and the two partial
  traces then force \(H\) to be scalar.
- The Grassmann updates preserve Hermiticity, signature, and involutivity.
  The symmetry masks define the stated restricted submanifolds. Equal
  signature was imposed separately inside each block, and the note
  correctly says that other blockwise allocations were not exhausted.
- The repeated \(\sqrt{12}\) basin calculation follows exactly from a
  limiting involutive braid solution with
  \(\operatorname{Tr}(K_1K_2)=18\). It is not presented as a lower bound.
- In the majority/transposition search, the 64 one-site-pair words are
  linearly independent, and the common anticommuting reflection makes the
  majority construction an involution. Separating the \(\sqrt3\) and
  \(\sqrt6\) trace components is exact because their ratio is irrational.
- The dense majority verifier checks the reported best nonzero residual,
  not independent exhaustive coverage of all 109,440 expressions. Thus a
  publication-level use of this finite no-go as a principal theorem would
  still benefit from a second exhaustive implementation with different
  core logic. This does not invalidate the present exact computation.

### Additive and heterogeneous constructions

- The heterogeneous blocking order and rank formula
  \(\operatorname{rank}P_K=a^2b/2\) are correct.
- The pure tensor-product spectrum argument is correct for the stated
  normal two-eigenvalue factors.
- The scalar-cross matrices on the `AAB/ABA/BAA` orbit give the complete
  mixed-color equations in that ansatz. I separately checked the scalar
  \(T=xI\) case: the off-diagonal equations still force \(s=t=0\) when
  \(c,u\ne0\), after which the remaining equations force the whole operator
  to be scalar.
- The controlled-middle parity proof validly uses only the known
  two-dimensional half-rank emptiness. It excludes odd middle dimension
  only within the controlled ansatz.
- In the qutrit graph-phase/global-flip calculation, substituting
  \(t=y/x\) and \(x^2=(1+t^2)^{-1}\) gives exactly the four displayed
  polynomial coefficient matrices. A common complex mixing angle exists
  only if their entry polynomials have a nonconstant gcd; the endpoint
  checks cover \(x=0\) and \(y=0\).
- The diagonal \(SU(2)\) rank equation has exactly the two complementary
  solutions listed; no continuous multiplicity-space parameter remains at
  rank six.
- The \(S_4\) character decomposition
  \(2V_3\oplus2V_{3'}\) gives precisely two central rank-six points and a
  \(CP^1\times CP^1\) noncentral branch. The former are rejected exactly;
  the latter has only the explicitly non-probative numerical search.
- The Clifford/qutrit parity, ice-rule, monomial, and reducing-sector
  arguments are valid with the restrictions stated in the note.

### Coherence and parity

- The one-sided tower construction works for every \(d=2s\); its branching
  calculation is exact and correctly shows that central ranks, \(K_0\),
  and one-sided inclusions cannot force \(2\mid s\).
- The Frobenius--Schur and real Brauer arguments are correctly rejected:
  an ordinary localization is not a rigid tensor functor, and the problem
  is over \(\mathbb C\).
- The quaternionic-algebra block sizes give no fixed-level parity
  obstruction. This part relies on Rowell's stated structure of \(Q_n\)
  and the known restriction of its coefficient trace to the Hecke
  subalgebra; I checked the dimension arithmetic but did not independently
  rederive Rowell's algebra theorem.
- The leg-commutant signature explains only the published stabilization
  family. The note explicitly avoids promoting it to a universal
  four-divisibility theorem.

### Gaussian functional ansatz

The Fourier parametrization is complete once the ansatz is fixed:
\(U^6=I\), equal multiplicity of the six roots, and \(H=f(U)\). The twisted
group algebra is faithful because \(q\) is a primitive sixth root, so its 36
words form a basis of \(M_6(\mathbb C)\). The no-go therefore holds exactly
for this cyclic Gaussian-functional family and says nothing about general
Gaussian combinations or arbitrary \(d=6\) matrices.

## Provenance defects and repairs

1. **Candidate overwrite.** A calibration replay silently overwrote
   `k8_shift4_real_none_known_seed26072900.npz`. The old SHA-256 was
   `292ad889928587315d83c528de9979ead7aade77a087f0ed8eeb73914c3c03ed`;
   the replacement SHA-256 is
   `cf0630b2a4a813307be318b7a23ad14a9bfa11ed68acb69ebff51eaeaf12f3d2`.
   Its matrix equals the deterministic formula entrywise. All diagnostic
   fields shared with the original raw final event agree exactly; the new
   archive differs in elapsed time and adds `overlap_trace: 0.0`.

2. **Repair.** Both numerical scripts now preserve an existing archive and
   emit `candidate_preserved`. Replacement requires the explicit
   `--overwrite-candidate` flag. This behavior was tested in temporary
   candidate directories and against the retained \(K_8\) archive.

3. **Replay paths.** The written replay commands formerly pointed at the
   canonical append-only JSON-lines logs and at the canonical exact JSON.
   They now require fresh replay paths, preventing accidental mutation.

4. **Historical source linkage.** The first 18 unpenalized full-space
   starts omit a field that the later source snapshot logs
   unconditionally; likewise for the first 74 shifted starts. At least a
   logging-schema change therefore occurred between those exploratory runs
   and the source-hash snapshot. Their parameters and outputs remain useful,
   but byte-for-byte replay from a contemporaneously hashed source cannot
   be certified.

5. **Formatting.** Accidental Markdown trailing spaces in the additive and
   coherence notes were removed. The scalar-gluing verifier's docstring was
   corrected to say that it spot-checks representative odd ranks while the
   written parity proof covers all odd dimensions.

## Bottom line

Checkpoint 2 is mathematically sound as a collection of exact restricted
no-go results, structural delimitations, and explicitly non-probative
numerical falsification. It does not settle \(d=6\) or the dimension
spectrum. Its main remaining verification gap is a genuinely independent
exhaustive implementation of the 109,440-case majority/transposition
search if that restricted theorem later becomes publication-critical.
