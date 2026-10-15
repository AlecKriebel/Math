# Additional independent separated-mode check

This check was undertaken after the initial independent proof reconstruction was recorded and after the historical supporting records were opened. It is supplementary to, and does not retrospectively replace, the pre-verdict reconstruction.

A point mass at angular coordinate η has Fourier boundary data δ(y−η)=(1/2π)Σ exp(in(y−η)). Solving a_n''−n²a_n=0 with a_n(0)=1, a_n(1)=0 gives

Pη(x,y)=(1−x)/(2π)+(1/π)Σ_{n≥1}[sinh(n(1−x))/sinh n]cos(n(y−η)).

This determines the same cylinder Poisson solution. Its derivatives converge on interior compact sets; differentiation in x gives constant −1/(2π) and coefficients −n cosh(n(1−x))/sinh n. At A with η=π, the angular cosine is (−1)^n. An independent implementation uses Machin's π formula (16 arctan(1/5)−4 arctan(1/239)), direct sinh/cosh mode coefficients, and 140/180 digit Decimal arithmetic. It verifies the image density against 1200 Fourier terms and reproduces the x derivative and gradient coefficient. The independently implemented Green sum uses a stable atanh expansion of log(1+t), rather than subtracting nearly equal logarithms.

The computed coefficient c is approximately 0.0003249863618574431472. The sharp minimum of the four-competitor linear support gap on the unit circle is (1−c)b/sqrt(1+b²), approximately 0.4052164889908448753. To verify that formula, write α=|u|, β=|v|, α²+β²=1, choosing u≤0. The gap is max(α,bβ)−cα. On the branch α≥bβ it increases with α; on the branch α≤bβ it decreases with α. Its minimum occurs at α=b/sqrt(1+b²). This sharpened value is an optional diagnostic comparison: the paper proves the sufficient weaker bound 1/10 by exact inequalities.

Severe tangential tests use s=10^−300 and η−π from 10^−5 to 10^−40, at an interior point. The final ratio-limit discrepancy is approximately 2.67·10^−40, consistent with the tangential offset. This is a sample test, while the uniform Taylor derivation proves unrestricted convergence.

The first 180-digit run of my new harness rejected an overly small comparison allowance because I had included the Fourier tail but omitted the finite image tail. Including both analytic tails repaired the harness; no paper formula or supplied diagnostic changed. This is recorded as a reviewer-computation correction, not a counterexample. Precision-stability checks pass. Decimal rounding is not enclosed by certified interval arithmetic, and neither numerical implementation proves a radius or the continuum theorem. The analytic derivation remains decisive.
