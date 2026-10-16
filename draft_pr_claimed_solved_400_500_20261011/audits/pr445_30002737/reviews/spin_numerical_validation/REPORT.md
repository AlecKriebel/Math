# Published spin-cocycle integral: independent numerical validation

**Independent pre-peer result, 2026-10-12T21:15:00Z. Completion estimate: 85%.**

The existing strict numerical inequality in Frank–Mañibo, *Spin substitutions*, published Example 10/Table 1 (PDF page 32; printed page 5430; DOI `10.3934/dcds.2022105`), is certified for both published choices N=12 and N=13. This is a finite computational validation of an existing example. It makes no claim about the prospective PR445 candidate, weighted combs, spectral reclassification, or new originality.

Let

\[
 B(x)=\begin{pmatrix}1&i\\ e^{2\pi ix}&-e^{2\pi ix}\end{pmatrix},\qquad
 P_N(x)=B(x)B(2x)\cdots B(2^{N-1}x),\qquad
 I_N=\frac1N\int_0^1\log\|P_N(x)\|_F^2\,dx.
\]

The published definition of the Fourier cocycle specifies this forward order. Its Example 10/Table 1 reports 0.688005 for N=12 and 0.682035 for N=13, with errors below 0.001. Those reports are evidence, not inputs to the acceptance test. The supplied published PDF's SHA256 was independently checked; see `SOURCE_CHECK.json`. No source PDF or foreign executable is part of this review's public files.

## Exact certified conclusion

At 65,536 cells and scale R=2^100, the programs produce:

| N | Certified upper bound for I_N (display only) | Certified positive margin below log 2 (display only) |
|---|---:|---:|
| 12 | 0.6880448396098113 | 0.005102340950133975 |
| 13 | 0.6820639600445100 | 0.01108322051543537 |

The comparison uses integer numerators, not these decimal displays. For N=13,

\[
 I_{13}\le\frac{736627539868258100115635444363832284}
 {65536\cdot13\cdot1267650600228229401496703205376}
 < \frac{878668439483319573618263538022}
 {1267650600228229401496703205376}\le\log2.
\]

The strict integer margin, after multiplying both sides by `M*N*R`, is
`11969853181466710380769305597695012`. The complete N=12 integers and a second N=13 run at R=2^80 under optimized Python are in their certificate JSON files. The optimized runs pass explicit runtime guards, which do not depend on Python `assert` statements.

## Certificate derivation and arithmetic control

1. **Exact polynomial cocycle.** Put z=exp(2πix). Starting from the identity and q=1,2,4,..., multiplication on the right by B(z^q) gives
   `(a,b,c,d) -> (a+z^q b, i a-z^q b, c+z^q d, i c-z^q d)`.
   Since q is larger than the previous degree, this is coefficient concatenation. All coefficients are exact Gaussian integers of modulus zero or one. For N=13 each entry has length L=8192. The independent sum of their squared coefficient moduli is 16384.

2. **Exact Fourier coefficients.** Write S(x)=||P_N(x)||_F²=Σ_k c_k exp(2πikx). Each c_k is the sum of the four entry autocorrelations. Real and imaginary parts are obtained by convolution modulo p=998244353, with zero padding to 2L. The code checks p is prime by exhaustive trial division through its integer square root. It checks primitive-root conditions for the complete prime factorization p−1=2^23·7·17. Every real/imaginary true coefficient has magnitude at most 4L<p/2, so its signed residue recovers the exact integer uniquely. Padding prevents cyclic aliasing. For N≤16 this uniqueness bound also covers the determinant convolution.

   Sanity checks include c_0=2^(N+1), c_(−k)=conjugate(c_k), and vanishing odd-frequency coefficients. A separate exact convolution verifies `det P_13(z)=(64+64i) z^8191`, hence |det|²=8192, as prescribed by `det B(z)=−(1+i)z`. Small N=1,...,6 autocorrelations are independently recomputed by quadratic integer sums and compared coefficient by coefficient to the NTT output.

3. **Analytic cell means and Jensen.** Partition the torus into M equal cells centered at j/M, wrapping the cell at zero. Its exact mean is
   `A_j = Σ_k c_k sinc(π k/M) exp(2π i k j/M)`, where sinc(t)=sin(t)/t and sinc(0)=1. S(x)≥2|det P_N|>0, so logarithms and Jensen apply on every cell. Therefore `I_N <= (1/(N M)) Σ_j log A_j`. No quadrature remainder for log S is assumed or omitted: Jensen is the integration upper bound.

4. **Outward sinc arithmetic.** All represented endpoints are integers divided by R. Addition, subtraction, multiplication and division round lower endpoints down and upper endpoints up with exact integer operations. A π interval comes from the classical Machin identity `π=16 atan(1/5)−4 atan(1/239)`. Each alternating arctangent series is bounded by its first omitted term. For each k, the code evaluates `sinc(t)=Σ_(j≥0) (−1)^j t^(2j)/(2j+1)!` through j=20, adding an outward bound for the next term. The guard t²<1 ensures term magnitudes decrease. The separate elementary bound sinc(t)≤1 is also applied. These interval operations enclose each Fourier input coefficient; dependency is harmless because it only enlarges intervals.

5. **Certified roots and FFT rounding.** Roots of unity are enclosed using exact square-root bisection via integer `isqrt` and the positive half-angle identities, starting from cos(π/2)=0 and sin(π/2)=1. Binary products of these enclosed roots generate every needed rotation. A fixed-point center is selected for each, and its Euclidean error is bounded by twice the maximum coordinate error. No floating trigonometric function is used. For N=13/M=65536/R=2^100, the uniform root error numerator is `14478`.

   The FFT uses fixed-point complex products with integer flooring. Each such product has Euclidean rounding error below 2/R. Put C=Σ_k(|Re c_k|+|Im c_k|)=1619032, a bound on any exact partial transform's magnitude because |sinc|≤1. If E/R bounds the current Euclidean error and e/R bounds a root's error, each butterfly has error at most
   `((2+e/R) E + e C + 2)/R`.
   The code rounds the updated numerator upward at each stage. This follows by bounding the approximate root's norm by 1+e/R, comparing its product with the exact partial transform, and then bounding both additions/subtractions. Initially E is twice the maximum Fourier-input coordinate error. After all stages the certified error numerator is `1536169203185453`, or less than 1.212e−15 in each cell mean. Each exact A_j is thus at most `(computed_real_j+E)/R`.

   Imaginary output enclosures contain zero. The exact global mean c_0 is inside the sum of all real enclosures. The determinant lower bound is checked against every upper cell-mean enclosure. The minimum upper cell mean is approximately 189.9549, comfortably positive.

6. **Certified logarithms and strict comparison.** For every rational upper cell mean v≥1, extract an integer exponent so v=2^e t with 1≤t<2. Then u=(t−1)/(t+1) lies in [0,1/3), and
   `log t = 2 Σ_(j≥0) u^(2j+1)/(2j+1)`.
   Upward fixed-point powers and divisions through 40 terms bound the partial sum above. The remaining positive tail is at most `3*u^(81)/81`, because `2/(1−u²)<3`; its numerator is rounded upward. The upper bound for log 2 uses the same method at u=1/3. The lower bound uses downward arithmetic and the positive partial sum alone. Positive exponent e uses the upper log2 bound. Summing these integer upper logarithms and comparing against `M*N*lower_log2` certifies the desired strict inequality.

## Direct decimal reproduction

An independent direct forward matrix-product midpoint calculation, using ordinary complex floating arithmetic, was run at M=65,536 and M=262,144. At the finer grid it gives:

| N | Direct empirical integral | Published decimal | Absolute difference |
|---|---:|---:|---:|
| 10 | 0.7037020356284376 | 0.703953 | 0.0002509644 |
| 11 | 0.6951620137968294 | 0.695342 | 0.0001799862 |
| 12 | 0.6879966061006004 | 0.688005 | 0.0000083939 |
| 13 | 0.6818863548699248 | 0.682035 | 0.0001486451 |

The printed decimals do not match to their last digits; all differences are within the paper's stated 0.001 tolerance. These reproductions and their apparent convergence are explicitly **noncertifying**. This review certifies the strict integral inequalities using upper bounds. It does not furnish a two-sided certificate for the paper's entire table or its claimed absolute error bound.

## Source-convention gauge check

The exact finite identity `W^T=C W C^-1`, for `W=[[1,i],[1,−1]]` and the unitary `C=diag(1,i)`, is checked by Gaussian-integer arithmetic. C commutes with D(z)=diag(1,z). Thus `D(z)W^T=C(D(z)W)C^-1`, and the same conjugation holds for every forward cocycle product. Its Frobenius norm is identical pointwise. This resolves this finite transpose convention only; it does not evaluate any prospective candidate claim.

## Reproduction, records and boundaries

From `/Users/alec/Documents/Math`, run:

```
python3 draft_pr_claimed_solved_400_500_20261011/audits/pr445_30002737/reviews/spin_numerical_validation/run_records.py
```

The runner preserves each actual argument vector, working directory, timestamps, stdout, stderr, and exit code in `RAW_RUN_RECORDS.json`. It executes independent exact small-N checks, N=13, N=12 under `python -O`, N=13 at 80 bits under `python -O`, both direct floating reproductions, and three intentional negative-input checks under `python -O`. Every expected success and failure occurred. These negative cases are retained records, not exploratory failures of the method. There were no failed exploratory certificate runs.

Only Python's standard library is needed; the recorded interpreter is Python 3.14.6. Core certificate arithmetic uses arbitrary-precision integers. Floating division is used only after acceptance to produce explanatory displays and timings. There were no external communications, Git operations, PR/queue actions, releases, DOI operations, or paper edits. All review files are original validation artifacts; the only use of the supplied primary source was read-only inspection and hashing.

**Strongest verified result:** both existing finite inequalities I_12<log2 and I_13<log2 have checkable, reproducible integer certificates. **Remaining gap at this checkpoint:** fresh adversarial review of the certificate's analytic bounds and implementation. The table's full absolute-error assertion is outside this strict-upper-bound certificate.
