# Fresh adversarial mathematical review

Audit date: 2026-08-08

Object reviewed: `cyclic_bell_exact_values_and_randomness/main.tex`

Method: line-by-line reconstruction from the merged manuscript, followed by independent replay of the preserved exact and numerical artifacts.  Earlier project reviews were treated as leads, not as proof.

## Verdict

**Central mathematical verdict: PASS.**  The exact first-family bound, its commuting-operator strengthening, the conditional phase-permutation construction, the all-dimensional nonuniform maximizers for \(d\geq4\), the second-family extension, and the Bell-value-only randomness conclusion are supported by complete analytic arguments as presently stated.

**Scope verdict: PASS.**  The manuscript now distinguishes the exact scalar equality set from a classification of the full maximizing face, distinguishes a scalar Bell constraint from a fixed full behavior, states only a lower bound on worst-case guessing probability, and restricts the low-setting obstruction to the routes actually proved.

**Release verdict: PASS subject to ordinary final replay.**  After any final manuscript edits, the unified verifier, PDF build, links, metadata, redirect, and hash checks must be rerun.  This internal audit is not external peer review.

## 1. Exact-value theorem

### 1.1 Normalization

The audited operator is

\[
 \mathcal I_d=\sum_{y=0}^{d-1}
 \operatorname{Re}\!\left[(A_0+\omega^yA_1)B_y\right],
 \qquad \omega=e^{2\pi i/d}.
\]

Its sharp value in this convention is

\[
 M_d=2\csc\!\left(\frac{\pi}{2d}\right).
\]

The first augmentation adds one term bounded by one and therefore has value \(M_d+1\).  This agrees with the source operator definition, its reduced-value equation, and the stated small-dimensional augmented value.  A localized printed extra factor \(d\) beside a source conjecture is correctly treated as a neutral normalization discrepancy rather than used rhetorically.

### 1.2 Polar identity and kernels

For \(C=V|C|\), with the canonical partial isometry, the manuscript uses

\[
 P=|C^\dagger|^{1/2}-V|C|^{1/2}B.
\]

Expansion gives

\[
 P^\dagger P=|C^\dagger|+|C|-CB-B^\dagger C^\dagger.
\]

The two potentially dangerous steps are valid:

- \(|C^\dagger|^{1/2}V=V|C|^{1/2}\) holds for the canonical polar partial isometry, including the kernels;
- \(|C^\dagger|^{1/2}V|C|^{1/2}=C\), while the support projection produced in the quadratic term acts as the identity on the support of \(|C|\).

No inverse of \(|C|\), no full-support hypothesis, and no unitary extension of \(V\) is used in the proof.  The polar objects lie in \(W^*(C)\), so they commute with the Bob algebra.  I found no missing adjoint, reversed polar phase, or left/right functional-calculus error.

### 1.3 Scalar extremum

The trigonometric reduction gives

\[
 \sum_y|1+\omega^yz|\leq2\csc(\pi/(2d)),
 \qquad |z|=1,
\]

and the exact equality set is

\[
 z^d=(-1)^{d-1}.
\]

The parity split and endpoint cases check out for \(d=2\) and \(d=3\), as well as general even and odd \(d\).  There are exactly \(d\) distinct equality roots.

### 1.4 Functional calculus and commuting operators

Writing \(U=A_0^\dagger A_1\) and \(M_y=I+\omega^yU\), normality of \(M_y\) gives the correct left/right absolute values.  Continuous functional calculus yields

\[
 F_d(U)=\sum_y|I+\omega^yU|\leq M_dI.
\]

Summing the polar identities then yields the claimed operator inequality.  The argument uses only \([A_x,B_y]=0\) and takes place on an arbitrary Hilbert space; it never invokes a tensor-factor trace identity for the upper bound.  Thus the \(q_c\) bound is genuinely analytic.  The explicit finite strategy supplies \(q\)-attainment, and the standard inclusions give equality of \(q,q_a,q_c\).

Finite direct-sum matrix tests are useful regression evidence, but they do not test nonspatial commuting representations and are not the reason the \(q_c\) statement is accepted.

### 1.5 Equality warning

The operator statement

\[
 F_d(U)=M_dI\iff U^d=(-1)^{d-1}I
\]

is justified by the exact scalar zero set.  For a single maximizing vector, however, the SOS gives only annihilation by its displayed factors.  The manuscript correctly declines to infer a global polynomial identity or a full equality-face classification from those vector conditions.  This distinction is load-bearing.

## 2. Attaining strategy

The Weyl strategy and polar Bob operators were reconstructed.  The weighted-cycle product proves the order-\(d\) relation; its characteristic polynomial proves the full simple root-of-unity spectrum.  The maximally-entangled trace identity produces equality term by term.  The added observable is aligned and contributes exactly one.  Dimension-dependent signs and conjugations agree with the chosen no-dagger Bob convention.

## 3. Conditional phase-permutation mechanism

The theorem is valid as a sufficient result under all three stated ingredients:

1. every labeled \(z_j\) maximizes the scalar function;
2. \(\prod_jz_j=1\);
3. for every coefficient index, the selected polar phases satisfy \(\prod_js_{rj}=1\).

The product conditions are not decorative: they are what make the weighted shifts order \(d\).  Permuting complete labeled pairs preserves them.  The trace expressions for first harmonics are symmetric sums and therefore permutation-independent, while higher powers can retain the cyclic ordering.

The theorem does not cover arbitrary phase choices or claim necessity.  A deliberately broken root product failed the order-\(d\) relation in a hostile replay, as expected.  No counterexample was found inside the theorem's hypotheses.

## 4. Nonuniform exact maximizers

For the cyclic roots \(z_k=e^{\pi i(2k+\delta_d)/d}\), the polynomial identities

\[
 \prod_kz_k=1,
 \qquad \prod_k(1+\omega^yz_k)=2,
 \qquad \prod_ks_{y,k}=1
\]

verify admissibility.  Direct diagonalization gives

\[
 p_\kappa(a,b\mid1,d)=\frac{|\widehat q_{-(a+b)}|^2}{d^3},
 \qquad q_{j+1}=z_{\kappa_j}q_j.
\]

Parseval proves probability normalization and uniform marginals.  For the final-two swap,

\[
 R_2=(z_{d-1}-z_{d-2})(z_{d-3}-z_0),
 \qquad |R_2|=4\sin(\pi/d)\sin(3\pi/d)>0
\]

for every \(d\geq4\), so the target joint table cannot be uniform.  The mean-zero/Fourier estimate yields exactly the displayed guessing lower bound.  The proof does not assert that this swap is worst over the maximizing face.

The exact \(d=4\) replay over \(\mathbb Q(\zeta_{16})\) gives \(1/32\) and \(3/32\) on alternating output sums and \(G=3/32>1/16\).  For \(d=2,3\), every permutation in this construction is flat; the manuscript correctly leaves those dimensions unresolved rather than extrapolating.

## 5. Second augmented family

Expanding

\[
 P_\ell=d\lambda_\ell I-A_\ell\widehat B_\ell
\]

with Fourier orthogonality and \(\sum_\ell|\lambda_\ell|^2=1\) gives

\[
 dI-\mathcal F_d=\frac1{2d}\sum_\ell P_\ell^\dagger P_\ell.
\]

The factor \(1/(2d)\), conjugation of \(A_\ell\), and Fourier orientation were independently rechecked.  The geometric sum gives \(\widehat B_\ell=d\lambda_\ell D_\ell\), including its phase; the parity exponent makes \(D_\ell^d=I\).  Every complete SOS factor therefore annihilates \(|\Phi_d\rangle\), proving saturation of a genuine global upper bound rather than merely vanishing of selected candidate equations.  The same \(A_1\) weighted cycle reproduces the first-family target table.

The exact \(d=4\) implementation independently expands the second-family SOS and agrees with the first-family projector calculation.

## 6. Randomness logic

The explicit behavior has maximum scalar value and \(\max_{a,b}p(a,b)>1/d^2\).  Even with trivial Eve, always guessing a most likely pair gives a guessing probability above the maximal-randomness benchmark.  This is sufficient to prove that the scalar value does not certify \(2\log_2d\) private bits across the full maximizing face.

It does not follow that the canonical full behavior fails to certify maximal randomness.  The phase-permuted behavior changes higher Fourier data and is excluded when the entire canonical distribution is fixed.  The manuscript states this distinction prominently.  The endpoint corollary is now logically correct because it quantifies all strategies with deficit **at most** \(\varepsilon\); the exact biased maximizer is feasible for every such tolerance.

## 7. Setting-complexity statements

The one-input proposition passes: the explicit conditional-product hidden variable is local, and coherently flagging the deterministic response tuple gives a finite pure projective realization from which Eve guesses perfectly.  Zero-probability sectors can use zero projectors or harmless padding.

The Fourier-phase ideal-table and perfect-anchor formulas pass, but concern the specified bases.  The computational-MUB proposition's corner-block proof passes and excludes only a coefficientwise separately bounded spectral route.  It does not rule out a joint SOS, another MUB, a different self-test, or a general \((2,3,d,d)\) construction.  The manuscript maintains this scope.

The binary \(d=2\) SOS is correct but known prior art and is appropriately treated as calibration rather than a new theorem.

## 8. Hostile and regression replay

The following commands were replayed from the preserved packages:

```sh
(cd cyclic_bell_exact_values_and_randomness && PYTHONDONTWRITEBYTECODE=1 python3 verification/verify_merged.py)
(cd cyclic_bell_tsirelson_bound && PYTHONDONTWRITEBYTECODE=1 python verify_certificate.py)
(cd cyclic_bell_tsirelson_bound && PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v)
(cd cyclic_randomness_counterexample && PYTHONDONTWRITEBYTECODE=1 python verify_exact.py)
(cd cyclic_randomness_counterexample && PYTHONDONTWRITEBYTECODE=1 python test_cases.py)
(cd minimum_bell_randomness && PYTHONDONTWRITEBYTECODE=1 python verify_second_family_d4_exact.py)
(cd minimum_bell_randomness && PYTHONDONTWRITEBYTECODE=1 python second_family_discovery.py)
(cd minimum_bell_randomness && PYTHONDONTWRITEBYTECODE=1 python test_cases.py)
(cd minimum_bell_randomness && PYTHONDONTWRITEBYTECODE=1 python satwap_ideal_audit.py)
(cd minimum_bell_randomness && PYTHONDONTWRITEBYTECODE=1 python verify_binary_2x2.py)
```

Results:

- canonical hostile suite: 13,395 scalar grid points through \(d=20\), a genuinely nonunitary polar partial isometry, 125 canonical/reversed/random prime-and-composite first-family strategies, exhaustive \(d=2,3\) flatness, final-two witnesses through \(d=20\), three deliberately inadmissible/failing cases, 125 second-family strategies, and 15 exact-rational one-input behaviors: **PASS**;
- exact-value package: 5 exact closed forms, 11 product instances, 21 polar checks including 15 singular cases, 10 global-certificate checks, 8 direct-sum commuting checks over 16 blocks, all 77 equality roots for \(d=2,\ldots,12\), all 77 Bob observables, Bell residual below \(1.3\times10^{-14}\), and 8 unit tests: **PASS**;
- exact first-family \(d=4\) cyclotomic certificate: **PASS**;
- canonical and final-two-swap regressions for \(d=2,\ldots,12\), including prime and composite dimensions and exhaustive root orderings at \(d=2,3\): **PASS**;
- independent second-family \(d=4\) cyclotomic SOS: **PASS**;
- second-family numerical dimensions \(3,\ldots,12\): **PASS**;
- setting regressions, standard-table audit, and binary exact SOS: **PASS**.

The all-dimensional and commuting-operator claims remain analytic theorems, not extrapolations from this list.

## 9. Defects found and disposition

1. An earlier endpoint-robustness phrasing was vulnerable to an exact-deficit reading.  The merged manuscript now says the bound must hold for strategies whose deficit is **at most** \(\varepsilon\); the proof then works.
2. The historical equal-supported-multiplicity proposition appears correct but is not a full-face classification and is not needed centrally.  Its omission, if retained, must be explicit in the changelog/merge report.
3. The historical private-MUB composition lemma is a valid secondary design observation.  Its omission for focus must likewise be recorded rather than silent.
4. A broad all-dimensional minimum-setting claim is unsupported by the scoped appendical obstructions and has correctly not been imported.
5. The powers-based repair attempt remains a failed approach, not a theorem.

No load-bearing mathematical claim had to be removed after being reconstructed.  The strongest defensible theorem is exactly the scoped chain recorded as CBR-005, CBR-009, CBR-012, CBR-014/015, and CBR-016/018 in `CLAIMS_LEDGER.md`.
