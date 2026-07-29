# Track B — independent dimension-six constructor/falsifier

Status: `NUMERICAL_EVIDENCE` except where an exact lemma is explicitly marked
`PROVED`.

This track deliberately does not assume the support, Pauli algebra, or
two-reflection form of the published \(d=4\) witness.  Its numerical work is
only a candidate generator and falsifier.  A nonzero residual, even at a
stationary point and across many seeds, is not evidence that \(d=6\) is
impossible.

## Exact exclusion: real signed-permutation involutions

**Lemma (`PROVED`).** There is no trace-zero real signed-permutation matrix
\(H\) in any local dimension \(d>0\) satisfying
\[
 H_{12}H_{23}H_{12}-H_{23}H_{12}H_{23}
 =\frac13(H_{12}-H_{23}).
\]

Indeed, all four matrices in the identity have integral entries.  After
multiplying by \(3\), every entry on the left is divisible by \(3\), whereas
every entry of \(H_{12}-H_{23}\) belongs to
\(\{-2,-1,0,1,2\}\).  Hence \(H_{12}=H_{23}\).  Taking the partial trace over
the third tensor factor, and separately over the first, gives
\[
 dH=I_d\otimes\operatorname{Tr}_2H,
 \qquad
 dH=\operatorname{Tr}_1H\otimes I_d.
\]
Thus \(H\) lies in both \(I_d\otimes M_d\) and \(M_d\otimes I_d\), whose
intersection consists only of scalar matrices.  Trace zero then forces
\(H=0\), contradicting \(H^2=I\).

This removes one precisely defined sparse family, including all involutive
signed set-theoretic candidates.  It says nothing about complex monomial
phases or nonmonomial sparse matrices.

The proof is exhaustive for its stated family: a real signed-permutation
matrix has exactly one entry in \(\{\pm1\}\) in every row and column, and
every product appearing in the cubic identity is again signed-permutation.

## Numerical search space

The program `scripts/d6_riemannian_search.py` minimizes the exact defining
residual over the Grassmann orbit of Hermitian involutions of signature
\((18,18)\).  Thus Hermiticity, involutivity, and trace zero are maintained
geometrically rather than imposed by penalties.  Both the full real and full
complex Grassmannians are tested.

The following independent symmetry families are also tested.  Write a local
basis vector of \(\mathbb C^2\otimes\mathbb C^3\) as \((a,r)\), with
\(a\in\mathbb Z_2\) and \(r\in\mathbb Z_3\).

- `z3_sum`: \(H\) preserves \(r_i+r_j\pmod3\); three blocks of size \(12\).
- `z3_difference`: \(H\) preserves \(r_i-r_j\pmod3\); three blocks of size
  \(12\).
- `z2_parity`: \(H\) preserves \(a_i+a_j\pmod2\); two blocks of size \(18\).
- `z2_z3`: both sum charges are preserved; six blocks of size \(6\).
- `local_4plus2`: for an unrelated decomposition
  \(\mathbb C^6=\mathbb C^4\oplus\mathbb C^2\), \(H\) preserves each ordered
  pair sector.  The blocks have sizes \(16,8,8,4\).  This tests a genuine
  sector-preserving extension with nontrivial mixed-sector operators, not an
  invalid direct sum on \(V\otimes V\).
- `h4_block`: within the preceding family, initialize the \(4\otimes4\)
  sector at the published exact \(d=4\) matrix while randomizing all three
  other sectors.
- A separate unrestricted complex batch adds the nonnegative discovery
  penalty
  \[
  10\bigl(\|\operatorname{Tr}_1H\|_F^2+
           \|\operatorname{Tr}_2H\|_F^2\bigr).
  \]
  This deliberately searches only toward the standard branch; it is kept
  separate and cannot test arbitrary nonstandard solutions.

### Reduced heterogeneous shifted ansatz

A second search does not optimize a \(36\times36\) matrix at all.  Put
\(A=\mathbb C^2\) and \(B=\mathbb C^3\), and seek a signature-\((6,6)\)
Hermitian involution
\[
K\in\operatorname{End}(A\otimes B\otimes A)
\]
satisfying the exceptional cubic relation for
\[
K_1=K\otimes I_{B\otimes A},\qquad
K_2=I_{A\otimes B}\otimes K
\]
on the \(72\)-dimensional alternating five-factor space.  Adding a spectator
\(B\) and regrouping \(B_i\otimes A_i\) into six-dimensional local sites
turns such a \(K\) into an ordinary \(d=6\) solution.  This reduces the
Grassmann search from signature \((18,18)\) in size \(36\) to signature
\((6,6)\) in size \(12\).

`scripts/d6_shifted_k_search.py` tests the unrestricted real and complex
spaces, as well as preservation of qutrit charge, outer-qubit parity, and
their joint grading.  It also tests the decomposition
\(B=\mathbb C^2\oplus\mathbb C\), both from random starts and with the known
\(8\times8\) generalized \(d=4\) operator inserted exactly in the
\(A\otimes\mathbb C^2\otimes A\) block.  This factorization is an ansatz:
failure here cannot exclude an ordinary solution without a spectator factor.

Many unrestricted descents terminate at involutive braid solutions for which
\(K_1K_2K_1=K_2K_1K_2\) but the exceptional linear term is nonzero.  These
have objective \(12\), residual \(\sqrt{12}\), and
\(\operatorname{Tr}(K_1K_2)=18\).  A separate predeclared batch therefore
adds the discovery penalty
\(\lvert\operatorname{Tr}(K_1K_2)\rvert^2\), which vanishes on the known
exceptional \(d=4\) generalized operator.  This is a heuristic branch
selector, not an extra condition in any theorem claimed here.

The first shifted batch completed 92 distinct \(K\)-runs:

| shifted family | runs | best residual | worst residual |
|---|---:|---:|---:|
| unrestricted complex, initial batch | 5 | 3.46410161514 | 8.00000000000 |
| unrestricted real | 3 | 7.01315473462 | 8.08166323844 |
| qutrit charge | 3 | 3.46410161514 | 9.23283993124 |
| outer parity | 3 | 3.46410161514 | 6.00581172862 |
| charge and parity | 3 | 3.46410161514 | 3.46410161514 |
| middle \(2+1\), seeded with known \(K_8\) | 5 | 6.02549064154 | 6.02549064154 |
| unrestricted complex, 50-seed batch | 50 | 3.46410161514 | 8.00000000000 |
| unrestricted complex with overlap penalty | 20 | 5.99803403648 | 8.00000000000 |

No shifted run approached zero.  The 50-seed unpenalized batch landed eleven
times at objective \(12\).  The saved representative at seed `26073047` has
cubic part norm `5.96e-10`, exceptional residual
\(\sqrt{12}\), overlap trace \(18\), and operator-Schmidt singular values
\(\sqrt3,\sqrt3,\sqrt3,\sqrt3\) across either outer split.  It is therefore
a numerical involutive braid solution, not an exceptional candidate.

More precisely, write \(A=K\otimes I_6\) and \(B=I_6\otimes K\).  For the
saved representative,
\[
\|ABA-BAB\|_F=5.96\times10^{-10},\qquad
\operatorname{Tr}(AB)=18,
\]
and \((AB)^3=I\) to `5.97e-10`.  Its spectrum clusters as
\[
\operatorname{spec}(AB)=
\{1^{(36)},e^{2\pi i/3\,(18)},e^{-2\pi i/3\,(18)}\}.
\]
The exceptional residual consequently tends to
\(-\tfrac13(A-B)\), with singular values \(1/\sqrt3\) (multiplicity 36)
and \(0\) (multiplicity 36).  Algebraically, any exact limiting point with
these properties has
\[
\left\|-\frac13(A-B)\right\|_F^2
=\frac19(72+72-2\cdot18)=12.
\]
This explains the repeated \(\sqrt{12}\) basin.  It is a different
involutive-Yang--Baxter stratum and supplies no lower bound for the
exceptional problem.

Every block is initialized with equal positive and negative signature.  This
is a choice inside each structured family, so these runs do not exhaust all
possible signature allocations among blocks.

The update is unitary conjugation
\[
H\longmapsto e^{tK}He^{-tK},
\qquad
K=\frac{DH-HD}{4},
\]
where \(D\) is a projected Riemannian search direction.  It therefore keeps
the signature fixed without an involution penalty.  The objective and its
analytic gradient use dense matrices on the \(216\)-dimensional three-site
space.  Nonlinear conjugate-gradient directions use Armijo backtracking.

## Analytic-gradient check

The Euclidean residual gradient is computed on the \(216\)-dimensional
three-site space, pulled back by partial traces, projected to the selected
commutant, and then projected to the Grassmann tangent space.  A finite
difference check is run before production searches.

For the \(d=6\), complex, `z2_z3` check at seed `26072800`, the analytic
directional derivative was `-3.1754097580015985`.  Difference quotients at
steps \(10^{-4},10^{-5},10^{-6}\) differed from it by
`3.42e-5`, `3.43e-6`, and `2.14e-7`, respectively.

## First numerical batch (2026-07-28)

The calibration run in the unrestricted complex \(d=4\) space reached
residual Frobenius norm `8.73240822329e-11` after 87 iterations from seed
`26072804`.  This confirms that the implementation can recover a solution in
a dimension where one is known, although it does not establish any
completeness property of the optimizer.

An independent reduced-code calibration inserts the published three-qubit
\(K_8\) formula directly.  It gives Hermiticity error zero, involution error
`6.30e-16`, and shifted cubic residual `6.89e-16`.

Seventeen predeclared \(d=6\) runs were then completed.  No run reached the
candidate-save threshold `1e-6`.  The smallest residuals were:

| family | seed | residual Frobenius norm |
|---|---:|---:|
| complex `z3_difference` | 26072842 | 5.36166439394 |
| complex `local_4plus2`, seeded with \(H_4\) | 26072882 | 6.01085854264 |
| complex `local_4plus2`, seeded with \(H_4\) | 26072881 | 6.01457553022 |
| complex `local_4plus2`, random | 26072872 | 6.01525690988 |
| complex `z2_parity` | 26072851 | 6.09646857830 |
| unrestricted complex | 26072811 | 6.09661136651 |

The remaining eleven residuals ranged from `6.09778306299` to
`16.9036888137`.  The final involution errors were all below `9e-14`.
Several line searches shrank to roundoff-scale steps near nonzero stationary
points, so these runs principally map local minima of this particular
objective.  They are not a statistically meaningful nonexistence test.

The three separate partial-trace-penalty runs ended at exceptional residuals
`6.31428680832`, `6.32370045340`, and `6.31426180999`.  Their two
partial-trace deviations were between `0.4055` and `0.4697`, so the soft
penalty did not reach the exactly standard submanifold.

## Reproducibility

- Seed manifest: `results/d6_seed_manifest.json`
- Raw JSON-lines output: `results/d6_riemannian_runs.jsonl`
- Python: `/Users/alec/Documents/Math/.venv/bin/python`
- Thread controls:
  `OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`
- Machine recorded by each run in its `start` event.
- NumPy and SciPy versions recorded by each run.
- Raw hashes: `results/d6_falsifier_hashes.txt`.

The seed manifest was written before the corresponding production runs.
Production candidate directories retain only matrices below their declared
thresholds.  One explicitly labeled non-solution stationary matrix is kept
separately under `results/d6_shifted_stationary/` for basin diagnosis.

### Independent-audit provenance correction

An independent replay on 2026-07-28 exposed that both search programs
formerly overwrote an existing candidate archive without warning. The
replay replaced
`results/d6_shifted_candidates/k8_shift4_real_none_known_seed26072900.npz`;
its SHA-256 changed from
`292ad889928587315d83c528de9979ead7aade77a087f0ed8eeb73914c3c03ed`
to
`cf0630b2a4a813307be318b7a23ad14a9bfa11ed68acb69ebff51eaeaf12f3d2`.
The replacement matrix agrees entrywise with the deterministic published
\(K_8\) formula. Every diagnostic field shared with the original JSON-lines
record is identical; the replacement has a different elapsed time and adds
the subsequently introduced field `overlap_trace: 0.0`.

Both programs now preserve an existing archive by default and require the
explicit flag `--overwrite-candidate` to replace it.

The audit also found a narrower source-provenance limitation. The first 18
unpenalized full-space `start` records omit `partial_trace_penalty`, and the
first 74 shifted `start` records omit `overlap_trace_penalty`, whereas the
source snapshot taken later records those zero-valued defaults
unconditionally. Thus at least a logging-schema revision occurred between
those runs and the recorded source hash. The seeds, spaces, iteration
counts, environments, raw outputs, objective values, analytic-gradient
checks, and independent calibrations remain recorded, but those initial
exploratory runs should not be described as byte-for-byte source-replayable.
No exact theorem or nonexistence claim depends on them.

The principal replay commands, run from `exceptional_ybe_spectrum/`, are:

```text
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
/Users/alec/Documents/Math/.venv/bin/python \
scripts/d6_riemannian_search.py --dimension 6 --field <field> \
--symmetry <family> --initial <initial> --seed <manifest-seed> \
--max-iterations <recorded-count> --output <new-replay-log>.jsonl

OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
/Users/alec/Documents/Math/.venv/bin/python \
scripts/d6_shifted_k_search.py --seed <manifest-seed> --field <field> \
--symmetry <family> --max-iterations <recorded-count> \
--output <new-replay-log>.jsonl

OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
/Users/alec/Documents/Math/.venv/bin/python \
scripts/d6_majority_transposition_search.py \
--output <new-replay-certificate>.json
```

Replay into a new path: both JSON-lines programs append to their requested
log, while the finite exact search records a new runtime field on each run.
Using the canonical raw-output paths would mutate the archived record.

Every `start` event records the exact iteration count, field, symmetry,
initialization, seed, dependency versions, and platform.  The shifted raw
file contains one intentional deterministic replay of seed `26073047`, used
to save its non-solution stationary matrix for structural diagnosis.

## Exact finite majority/transposition search (2026-07-28)

`scripts/d6_majority_transposition_search.py` exhausts a separate finite
qubit–qutrit ansatz.  On each qutrit use the algebra generated by a fixed
transposition \(T\), and on each qubit use the Pauli words.  It enumerates
commuting triples \(A,B,C\), every word \(E\) anticommuting with the triple,
all inequivalent signs in the majority reflection
\[
M=\frac{-s_AA-s_BB-s_CC+s_As_Bs_CABC}{2},
\]
and both signs in
\[
H=\sqrt{\frac23}M\mathbin{\pm}\frac1{\sqrt3}E.
\]

Concretely, the 64 words are
\[
(Q_1\otimes T^{e_1})\otimes(Q_2\otimes T^{e_2}),
\quad
Q_i\in\{I,X,Y,Z\},\quad e_i\in\{0,1\}.
\]
Replacing \(T\) simultaneously by another qutrit transposition gives a
locally conjugate ansatz.  Distinct fixed transpositions on the two local
legs are not included.  The program tests all unordered nonidentity commuting
triples and all common anticommuting words.  It fixes \(s_A=1\) without loss:
reversing all three signs sends \(M\) to \(-M\), while \(H\mapsto-H\)
preserves the cubic equation and both signs of \(E\) are enumerated.
Trace zero is checked independently in the \(\sqrt3\) and \(\sqrt6\)
components.

The tensor-word calculation is exact.  After scaling the cubic residual by
216, every coefficient is stored as a Gaussian-integer multiple of
\(\sqrt3\) and \(\sqrt6\).  The completed search found:

- 64 available tensor words;
- 5,791 commuting triples;
- 2,220 triples with at least one eligible \(E\);
- 291,840 signed candidates, all trace zero;
- 109,440 distinct trace-zero \(H\) expressions;
- **zero exact solutions**.

The ordered residual digest is
`3ed7f63a6d801d55cb068674f790bec1a8ea27b6ab50309b554b0fec92e7c756`.
The complete raw certificate, including the smallest-support nonzero
residual, is in `results/d6_majority_transposition_exact.json`.
The separately implemented dense reconstruction
`scripts/verify_d6_majority_transposition_best.py` checks the smallest-support
entry directly as a \(216\times216\) matrix.  It obtains involution error
`1.26e-15`, a nonzero residual norm `13.8564`, and agreement with the printed
exact coefficient certificate to `1.03e-12`.

This is an exact negative theorem only for this explicitly stated finite
majority/transposition ansatz.  It neither excludes other
two-reflection constructions nor bears on the full \(d=6\) problem.

## Interpretation rule

Only an exact algebraic witness, independently verified, will count as a
positive result.  These experiments can reveal candidate support, symmetries,
or algebraic numbers.  They cannot certify nonexistence.
