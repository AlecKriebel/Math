# Source-author technical review packet

This is a technical comparison document, not an email, endorsement request,
authorship proposal, or claim that external review has occurred.

## One-page theorem comparison

| Topic | Originating paper (arXiv:2606.21362v3) | Version 1.1 conclusion |
|---|---|---|
| Bell families | Introduced both cyclic families and their displayed operators | Adopts those definitions with explicit Hermitian/adjoint conventions |
| First general bound | Proved $\beta_q\le d\sqrt2$ | Fully credited; the new polar proof strengthens it to $2\csc(\pi/(2d))$ |
| First lower bound and conjecture | Supplied a canonical strategy of value $2\csc(\pi/(2d))$ and conjectured equality | Rechecks the source strategy and proves equality for $q,qa,qc$ |
| Low-dimensional evidence | Reported matching NPA bounds through $d=6$: $1+AB$ for $d=3,4$, level 2 for $d=5,6$ | Gives the corresponding exact radicals and checks agreement with the reported decimals |
| First augmentation | Defined it; the formula printed beside Conjecture 2 has an isolated normalization discrepancy | Uses the displayed operator, whose exact maximum is $M_d+1$ |
| Attained finite-dimensional tensor-product exact maximizers of the first augmented family | No complete maximizing-face classification | Proves that every such maximizer has every equality root with equal multiplicity on $K=\operatorname{supp}\rho_A$, hence $d\mid\dim K$ |
| Phase ordering | Canonical ordering supplied | Gives a conditional paired-permutation orbit preserving all complex first harmonics; does not claim exhaustiveness |
| Alternative maximizers | Not identified in the source | Constructs nonuniform exact maximizers of both augmented families for every $d\ge4$ |
| Second reduced value | Proved value $d$ by an SOS | Credits and uses that complete SOS, including its commuting-operator reading |
| Second-family conventions | Main/SOS and appendix formulas differ by consistent Bob adjunction | Keeps the main/SOS convention; treats the appendix convention as Bob outcome inversion $b\mapsto-b$ |
| Canonical full behavior | Numerical guessing analysis fixes the complete canonical distribution; selected rigidity/self-testing results are also given | Explicitly not contradicted |
| Conjecture 2 scalar implication | Maximal violation of the first augmentation is stated to certify $2\log_2d$ bits at $(1,d)$ | For the displayed operator, disproves $\langle\overline{\mathcal I}_d\rangle=M_d+1\Rightarrow G=1/d^2$ for $d\ge4$ |
| Exact $d=4$ witness | Canonical table studied | Root-swapped table has probabilities $1/32,3/32$, $G=3/32$, and displayed-realization entropy $5-\log_2 3$ bits |

## Normalization and operator conventions

For the first family, version 1.1 treats the displayed Hermitian operator as
authoritative. Its reduced and augmented values are

\[
M_d=2\csc\!\left(\frac{\pi}{2d}\right),
\qquad M_d+1.
\]

This agrees with the source's reduced equation, canonical lower strategy, and
stated $d=3$ augmented value. The extra $d$ in the denominator printed beside
Conjecture 2 is recorded neutrally as a localized normalization or
typographical discrepancy and is not used rhetorically.

For the second family, version 1.1 follows the source main-text convention
with $B_y$ and the source-v3 SOS, with prefactor $1/(2d)$. The alternative appendix
convention consistently replaces every Bob observable by its adjoint. This is
Bob outcome inversion, preserving the maximum, the table's nonuniformity, the
guessing probability, and entropy. The two conventions cannot be mixed term
by term.

## Bell value versus complete behavior

The source's Appendix B.1 numerical program constrains the complete canonical
probability distribution before optimizing Eve. The version 1.1 witness
constrains only the same scalar maximum, although it also preserves the full
matrix of complex first-harmonic correlators. Its higher Fourier data and
target table differ.

The precise relationship is therefore:

\[
\boxed{
\langle\overline{\mathcal I}_d\rangle=M_d+1
\not\Longrightarrow
G(AB\mid1,d,E)=1/d^2
\quad(d\ge4).}
\]

This leaves logically possible—and does not criticize—the source conclusion
that the fixed complete canonical behavior has $G=1/d^2$. Version 1.1 does
not show that the canonical strategy lacks maximal randomness and does not
determine the exact worst-case guessing probability over the maximizing face.

At $d=4$, the explicit trivial-Eve witness has
$G=3/32$ and $H_{\min}=5-\log_2 3$. The latter is an exact entropy for that
displayed realization and therefore an upper bound on value-only worst-case
entropy, not the optimized value itself.

## Three proof points most worth checking

1. **Commuting polar bound.** Verify the strong-limit placement of the
   canonical polar partial isometry in Alice's bicommutant, cross-party
   commutation, kernel support identities, scalar equality set, finite source
   attainment, and source-observable Fourier identification.
2. **Two equality layers.** Verify support cancellation for nonfaithful
   $\rho_A$, polar stabilization on $K$, the adjacent reflection and rank
   count, keeping support rigidity restricted to attained finite-dimensional
   tensor-product exact maximizers of the first augmented family.
   Separately verify both
   product-one conditions for the sufficient paired phase orbit, the target
   DFT, final-two autocorrelation, and exact $d=4$ table and entropy.
3. **Second-family SOS and randomness logic.** Verify
   $\widehat B_\ell=d\lambda_\ell D_\ell$, $D_\ell^d=I$, Alice's conjugation,
   the source-v3 SOS prefactor $1/(2d)$, and the all-Bob-adjoint outcome
   inversion. Then check that
   the explicit nonuniform maximum refutes only the normalized scalar-value
   implication and leaves the fixed canonical full-behavior calculation
   outside its scope.

## Secondary results retained from the third historical paper

These results support the distinction between scalar data and operator-valued
privacy conditions but are not dependencies of the cyclic counterexample.

- The prior-art binary $2\times2$ benchmark has $q=qa=qc=3\sqrt3$; its two-
  square SOS and on-state Fourier argument imply
  $\sigma_E^{ab}=\rho_E/4$ at the target pair for every attaining finite-
  dimensional tensor-product strategy.
- The private-MUB composition lemma is a positive sufficient criterion. A
  private reference PVM, perfect Bob matching, and a state-supported MUB
  sandwich imply $\sigma_E^{a,\pi(b)}=\rho_E/d^2$. It is not claimed necessary
  and does not itself construct a low-setting Bell functional.
- The higher-dimensional $2\times2$ and $2\times3$ certification problems
  remain open at the scopes stated in the manuscript.

## Source item to merged disposition

| Source item | Version 1.1 treatment |
|---|---|
| Family definitions | Adopted and credited |
| $d\sqrt2$ analytic bound | Credited and sharpened |
| Canonical lower strategies | Adopted, credited, and exactly rechecked |
| NPA evidence through $d=6$ | Credited and matched to exact radicals |
| First-value conjecture | Proved, including the commuting-operator value |
| Second-family SOS | Adopted from source-v3 with prefactor $1/(2d)$ and credited |
| Fixed-canonical-behavior numerical randomness | Explicitly not contradicted |
| Conjecture 2 scalar-value implication | Disproved for the displayed operator for every $d\ge4$ |
| Source $d=3$ second-family self-test | Explicitly outside the counterexample dimensions |

## Possible collaborative extensions

- Determine whether supported rigidity, admissible phase permutations, direct
  sums, and irrelevant ancillas generate every attained finite-dimensional
  tensor-product exact maximizer of the first augmented family.
- Separately characterize the $qa$ and $qc$ maximizing faces.
- Determine the exact worst-case guessing probability and min-entropy at the
  scalar maximum.
- Resolve the first-family $d=2,3$ maximizing faces.
- Classify phase orders up to local isometries and output relabelings.
- Add a minimal set of higher Fourier terms that restores value rigidity.
- Prove robust self-testing or randomness for a modified low-setting family.

## Shortest focused replay

```sh
cd cyclic_bell_exact_values_and_randomness
python3 verification/verify_merged.py
python3 verification/verify_rigidity.py
python3 verification/verify_exact_benchmarks.py
python3 verification/verify_private_mub_binary.py
python3 ../cyclic_randomness_counterexample/verify_exact.py
python3 ../minimum_bell_randomness/verify_second_family_d4_exact.py
```

For the complete build, integrity, and website replay, run `./reproduce.sh`.
The theorem-to-artifact map gives precise manuscript and verifier locations.
