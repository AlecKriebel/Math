# Fresh adversarial review of the published spin integral certificate

Completed UTC: 2026-10-12T21:25:39.641873+00:00. Review completion estimate: **100% for the delegated N=13 certificate review**.

**Disposition: accept the sealed finite N=13 strict upper-bound certificate within its stated scope.** The review found no mathematical blocker or required code repair for that inequality. It did find a concrete limit of the runtime guards: an invalid point-sampling replacement can pass them, so the reviewed analytic derivation and controlling code hash are essential parts of the certificate. An initially inactive fault-control prediction failed and is preserved below.

The only accepted claim is

\[
I_{13}=\frac1{13}\int_0^1\log\|B(x)B(2x)\cdots B(2^{12}x)\|_F^2\,dx<\log2,
\qquad B(x)=\begin{pmatrix}1&i\\e^{2\pi ix}&-e^{2\pi ix}\end{pmatrix}.
\]

This is a validation of Frank–Mañibo's already published Example 10/Table 1, DOI 10.3934/dcds.2022105. It is not an original proof search, prospective-candidate review, priority certificate, proof of an infinite family, or independent proof of the spectral theorem and its substitution hypotheses. The producer also reports N=12; this review freshly reproduced N=13 and makes no separate fresh-execution acceptance claim for N=12.

## Independence and immutable inputs

`INITIAL_CHECKPOINT.md` was sealed at 2026-10-12T21:13:41.923899+00:00 before any producer implementation, report, result, or raw record was read. Its SHA-256 is `1c44eea34f762fd56303c582f77606f8cab93967c1e0ed332516f86441e326ed`. The exact source was independently reconstructed from the supplied published primary PDF/text, then the relevant displayed equations were visually checked on PDF pp.28–29 and 32. The primary PDF hash was `7e4a477cbfc7c43e3384a5c082d30617418c9fd9b027921103664bd27b390954`.

The producer announced FINAL_READY_PRE_PEER at 2026-10-12T21:16:14.886239+00:00. Only then was its complete code read. The reviewed controlling code is `certify_integral.py`, SHA-256 `027dc38ea76f1a4e69d8976a4845caefc4429e48b551afa7c327dc243b3dac20`. The report/result hashes match the communicated seal. Complete controlling code, reports, and raw records were saved in the ignored private fixture area, outside this review's positive public manifest. `SEALED_INPUT_RECEIPT.json` binds those copies and checks each producer certificate's stdout against its saved certificate JSON. All nine producer raw records parse consistently with their stated exit statuses; their three successful certificate stdout objects equal the corresponding certificate files.

## Exact recurrence, source order and modular recovery

Right multiplication by the source's next factor gives

\[
(a,b,c,d)\mapsto(a+z^{2^n}b,\;ia-z^{2^n}b,\;c+z^{2^n}d,\;ic-z^{2^n}d).
\]

At stage n the old degree is at most 2^n−1, so concatenation in the code implements that exact right multiplication with disjoint old/shifted supports. All coefficients are Gaussian integer units or zero. The independent generic matrix-polynomial multiplication in `independent_reference.py` matches every entry of the producer's polynomial for N=1,…,6, rather than merely testing the producer's recurrence against its own autocorrelation. N=0 and the quarter-root boundary structure were also represented in that reference.

A second, materially distinct exact mechanism checks **all 16,383 signed-frequency coefficients for N=13**. Put W=[[1,i],[1,−1]], D(z)=diag(1,z), and G_n=A_n A_n*. The source-forward identity A_n(x)=D(z)W A_(n−1)(2x) gives

\[
G_n(x)=D(z)W G_{n-1}(2x)W^*D(z)^*.
\]

`gram_crosscheck.py` applies this recurrence directly to Gaussian Laurent-polynomial dictionaries and takes the trace. It uses no modular transform, convolution, coefficient concatenation, or floating arithmetic. Its entire N=13 coefficient dictionary matches the NTT output, including zero imaginary coefficients and correct negative-frequency conjugation. The common coefficient hash is `3d3550f4233ca4f00b26cb86befd13f54aeff043e46b099fff5bad3a47bbb5f4`; the independently computed coefficient L1 norm is 1,619,032. The Gram recurrence also agrees with generic quadratic autocorrelation at every coefficient for N=1,…,6.

The NTT derivation is sound independently of this full check: transform length 2L exceeds convolution degree 2L−2; its phase shifts the reversed polynomial by L−1; the real and imaginary convolutions are separate; and every signed coefficient is bounded by 4L. With L=8192 and p=998244353, 4L<p/2 gives unique signed recovery. The code exhaustively checks primality and the generator's orders against the complete factorization p−1=2^23·7·17. All intermediate operations are Python arbitrary-precision integer operations, so native integer overflow is absent. The determinant convolution has the same safe uniqueness bound and returns (64+64i)z^8191.

Product reversal is pointwise sensitive: independently, N=2 gives source S_2(x)=8−4cos(4πx), while the reversed product gives 8−4cos(2πx). The code uses the source order. Its narrower transpose convention is valid: W^T=CWC^−1 for C=diag(1,i), C commutes with D(z), and the same unitary conjugation applies to every forward factor and hence the whole forward product. This identity does not authorize factor reversal.

## Analytic enclosure and integration audit

The following deductions justify the general arithmetic mechanism; finite sanity checks supplement them.

- The determinant gives |det A_13|²=8192, hence S_13(x)≥2√8192>180 everywhere. Thus every exact cell mean is positive and every logarithm is legitimate. The code's rational lower bound 2 isqrt(8192)=180 is sufficient. Its check against each upper mean endpoint is a sanity check, not the proof of positivity. A separate positive approximate lower endpoint is unnecessary because the exact determinant supplies the uniform positive lower bound.
- On cells centered at j/M and wrapping at zero, the exact mean is m_j=Σ_k C_k sinc(πk/M)exp(2πikj/M). The coefficient indexing `k % M`, positive-sign FFT, and conjugate negative frequencies implement this formula. Distinct frequencies cannot collide because M≥4L.
- Integer interval multiplication considers all four endpoint products; subtraction reverses endpoints; positive division rounds outward. Integer `isqrt` returns the lower square-root endpoint and the upper endpoint is incremented exactly when its square is too small. Half-angle intervals use the correct reversed subtraction endpoints and positive square-root branches. The roots start at the exact fourth root i; binary products generate every required positive-sign twiddle. The coordinate center error times two bounds Euclidean error.
- The Machin arctangent alternating remainders are enclosed by their first omitted terms. The sinc recurrence encloses each exact Taylor term, t²<1 ensures decreasing terms, and the next term bounds the tail. Applying sinc≤1 is valid and supplies the coefficient L1 bound on all exact FFT partial transforms.
- If E/R bounds each current complex error and e/R bounds a twiddle's error, a butterfly has error at most (2+e/R)E/R+eC/R+2/R. This includes both input errors, the root-error/input-error interaction, the exact partial-transform amplitude bound C, and both coordinate floor-roundings. The implemented upward integer recurrence therefore bounds every stage. No transform normalization or rounding factor is omitted.
- Concavity gives ∫log S≤M^−1Σ_j log m_j. The code uses upper endpoints (computed_real_j+E)/R and monotonicity of log in the correct direction. It does not claim a trapezoidal or midpoint integration error for log S.
- For v≥1, exact bit-length normalization gives v=2^e t with e≥0 and 1≤t<2. The positive atanh series at u=(t−1)/(t+1) has upper-rounded powers and divisions. Its tail bound is valid even for the permitted one-ulp overshoot: u≤1/3+2^−80<1/2 implies 2/(1−u²)<3. Downward partial sums at floor(R/3)/R give a lower log2 bound. The integer inequality, not printed decimals, decides acceptance.

`rational_crosscheck.py` separately uses exact Fraction series and remainders to enclose π and log2, and confirms that the producer's intervals contain those independent bounds. It checks sinc at k=0,1,2,4095,8190,8191 and nine logarithm arguments including 1, 1+ulp, 2−ulp, 2, determinant-scale values and a large power boundary. These finite checks support the general derivation; they are not its replacement.

## Fresh executions and exact threshold

`RAW_ADVERSARIAL_RECORDS.json` retains each actual argument vector, cwd, timestamps, stdout, stderr, exit status, and controlling-file hash. Fresh normal and Python -O N=13 runs at M=65536 and R=2^100 match every stable producer certificate field, including

\[
U=736627539868258100115635444363832284,\quad
L_2=878668439483319573618263538022,\quad
R=1267650600228229401496703205376.
\]

The exact acceptance calculation is

\[
I_{13}\le\frac{U}{65536\cdot13\cdot R}\;<\;\frac{L_2}{R}\;\le\;\log2.
\]

The positive integer margin is `11969853181466710380769305597695012`. The displayed upper value 0.68206396004451 is generated only after acceptance by division of those integers; it is not itself an exact rational or acceptance premise. The propagated FFT error numerator is `1536169203185453`; the root error numerator is `14478`; both fresh executions match them. No `assert` statement carries an acceptance guard.

## Targeted controls and preserved failure history

The final targeted controls were actual Python -O child runs of saved private mutants, with exact single-replacement descriptions and mutant hashes in `MUTATION_RECEIPTS.json`.

| Control | Actual result | Interpretation |
|---|---|---|
| NTT generator 3→1 | exit 1, generator guard | Modular-root invalidity rejected |
| Active twiddle index0 imaginary coordinate shifted by R/10 without changing its bound | exit 1, imaginary-enclosure guard | Used-root corruption rejected |
| FFT error numerator reset to zero | exit 1, imaginary-enclosure guard | Missing propagated error rejected |
| sinc multiplier replaced by 1 | exit 0, internally CERTIFIED | Runtime guards do not establish the cell-mean/Jensen premise |

The last mutant is analytically invalid despite passing guards. For N=2, the zero-centered cell's true mean is 8−4sinc(2π/M)>4=S_2(0), since sin t<t for 0<t<π. A point sample therefore cannot serve as this cell's mean upper bound. This is a checkable counterexample to the altered integration mechanism; it is not a counterexample to the sealed code, which uses outward sinc intervals. No claim is made that guards detect arbitrary altered executables.

The first control harness expected a rejection after perturbing root index1. That prediction was wrong: the altered program exited 0 and every stable certificate field was unchanged. Root index1 is used only in the final FFT stage, where the bit-reversed odd-frequency block is exactly zero; earlier stages use root indices divisible by two. This fault was inactive. The harness exited 1 on its expectation mismatch and stopped; `attempt1_runner.py`, `attempt1_raw_records.json`, `attempt1_mutation_receipts.json`, and `ATTEMPT1_CONTROL_ANALYSIS.json` preserve the complete history. The repaired control targets active index0.

Across the two retained harness attempts and the separate rational-check child there were **13 actual child executions: 9 exits 0 and 4 intentional mutated-program exits 1**. There was **one failed control prediction and one consequent harness failure**, both preserved. There were **zero failed runs of the unmodified sealed certificate**. In the completed final harness, three invalid arithmetic mutations were rejected and one invalid analytic mutation passed internal guards but was independently rejected by the exact cell-mean argument.

## Findings, required repairs and exact remaining gaps

There is **no mathematical blocker and no required repair for I_13<log2 under the sealed controlling code**. The accepted proof remains conditional on Python's specified exact integer semantics, the mathematical source criterion, and the explicitly derived error mechanism. It is not a formally machine-checked proof of the interpreter or the entire spectral theory.

The concrete informational finding is that internal sanity guards are not a complete mathematical verifier: the sampling mutant passes. Any certificate reuse must bind the reviewed full code hash and analytic derivation, as this review does. No code change is needed to repair the actual integration premise.

No certified two-sided enclosure for the published decimal 0.682035, its entire Table 1, or its stated absolute-error tolerance is supplied by this strict upper-bound certificate. The producer's floating reproductions are explicitly noncertifying and were not adopted as mathematical evidence for acceptance. No fresh N=12 execution was requested in this review. Singular-continuous classification, candidate novelty, priority and bibliographic sufficiency remain outside scope.

No external communications, Git changes, branch changes, PR/queue actions, DOI/release actions, or paper edits were made. All writes were restricted to this review's folder and its ignored private fixtures. `PUBLIC_FILES.json` is a positive SHA-256 manifest of this review's original artifacts; it excludes the saved producer/source bytes.
