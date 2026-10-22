# Independent adversarial audit: 2306047 / rank 685

## Verdict

**PASS for partial work, exhausted after five approaches. No full solution.**

No blocking mathematical defect was found in the frozen authored partials. The original 48 controls replayed successfully and reproduced their stored result byte-for-byte. An independently written audit script passed 55 additional checks. Every frozen input remained unchanged.

The strongest unconditional audited result is the strict bound

\[
A_2<\frac{2+\sqrt{13}}3.
\]

The two strategy counterexamples and the coefficient limit for the explicitly specified analytic candidate are also valid. The candidate's membership in the admissible class remains dependent on the inspected Hayman–Lingham report; this audit did not independently establish that membership. No sharp coefficient maximum, novelty, or exhaustive current literature status is certified.

## Binding and method

- Target: 2306047, AMR-022-6047, rank 685.
- Frozen manifest SHA-256: `cf78e841bb4c939d8dadefd05f76447a6a5b18629748290a047c9fb03996f932`.
- All seven file byte counts and hashes listed in that manifest were independently matched.
- The existing control script was copied to a temporary location before execution, because it writes its result beside itself. The frozen directory was never used as its output destination.
- The mathematical arguments below were checked independently of the supplied computation. Finite tests are supporting controls, not substitutes for the analytic arguments.
- No helpers were delegated and no remote writes were made.

## 1. Target and source audit

The relevant class consists of normalized holomorphic functions on the **open unit disk**, with both the function and its first derivative injective there. Coefficients may be complex. The question concerns sharp coefficient maxima for the complete class, rather than an assertion that all maxima equal one.

The definition and Problem/Update 6.47 were independently inspected in the local primary PDF, including the rendered problem/update pages. The primary arXiv abstract and PDF were also opened through the web tool. The displayed integral for the reported candidate agrees with the package's series after choosing the logarithm analytic at zero. The rendered convex-subclass coefficient expression is inconsistent with the displayed example's actual coefficients; the package properly avoids using it as a proved sharp theorem.

Source: W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, printed pages 114 and 135–136. [Primary record](https://arxiv.org/abs/1809.07200v2), [PDF](https://arxiv.org/pdf/1809.07200v2).

The locally inspected PDF has 1,706,228 bytes and SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`, matching the frozen metadata. This is a check of the local source bytes; the web PDF open was not a fresh byte-for-byte download verification.

The Barnard–Suffridge DOI and an official Project Euclid full-article route were retried and returned retrieval errors. The original proof was not inspected in this audit. Search results concerning real-coefficient or typically-real subclasses were not promoted to results for the unrestricted class. Bounded searches cannot certify that the problem remains open today.

## 2. Derivative normalization and compactness

If `f'` is holomorphic and injective, then its derivative at the origin cannot vanish. Thus `2a_2=f''(0)` is nonzero, and `h=(f'-1)/(2a_2)` is normalized schlicht. Its coefficient of degree `n-1` equals `n a_n/(2a_2)`. The coefficient theorem therefore gives

\[
|a_n|\leq\frac{2(n-1)}n|a_2|.
\]

Normalization by the extremal number `A_2` instead of the particular coefficient `a_2` is not justified for an arbitrary function. The package uses the correct normalization.

The compactness step needed to obtain a strict supremum bound is valid. A sequence in the normalized schlicht class has a subsequential locally uniform limit still in that class. Derivatives converge locally uniformly too. A locally uniform limit of holomorphic injective derivatives is either injective or constant. In the constant case the normalization forces `f'=1`, hence `f(z)=z`. Consequently the class enlarged by the identity is compact.

The identity cannot maximize any coefficient under consideration: `z/(1-z)` belongs to the original class and has every coefficient equal to one. To check derivative injectivity directly, equality of `(1-z)^(-2)` and `(1-w)^(-2)` implies either `z=w` or `z+w=2`; the latter is impossible inside the disk. Since each coefficient functional is continuous, its maximum on the enlargement is achieved away from the identity.

The original class is genuinely nonclosed. For example, `f_j(z)=z+z^2/(4j)` has an injective affine derivative and a derivative with positive real part on the disk, while `f_j` converges locally uniformly to the excluded identity. This confirms that adding the identity is a substantive part of the argument.

## 3. Weak bound and equality exclusion

Let `a=|a_2|`. The exterior area theorem gives `|a_3-a_2^2|≤1`. The second coefficient estimate for the normalized derivative gives `|a_3|≤4a/3`. Therefore `a^2≤1+4a/3`, yielding the stated constant `C=(2+sqrt(13))/3`.

The equality argument survives complex phases. A rotation can make `a_2=a>0` without changing admissibility. If `a=C`, equality holds throughout the triangle-inequality chain. Both summands must then have the positive-real direction, forcing `a_3=4a/3` and the second coefficient of `h` to equal 2. The equality case of the second coefficient theorem gives the unrotated Koebe function.

The package's brief area-theorem derivation of that equality case is legitimate. For normalized univalent `h`, the analytic odd branch `H(z)=sqrt(h(z^2))` exists because `h(z^2)/z^2` is nonvanishing. It is univalent: equality of two values implies equality after squaring, then the only possible alternative is opposite arguments, ruled out by oddness unless both vanish. The first exterior coefficient of `1/H(1/zeta)` is `-b_2/2`. If `|b_2|=2`, its squared modulus exhausts the area bound; every other negative Laurent coefficient vanishes. Solving for `H` gives the asserted Koebe form.

Integration at zero now uniquely forces the stated `P_a`. For this function, the conjugate-pair collision argument below excludes every `a>2/(pi-2)`. Exact inequalities establish `C>9/5>2/(pi-2)`. Equality at `C` is therefore impossible.

Importantly, pointwise exclusion alone would prove only `A_2≤C`. The separately established attainment theorem upgrades it to `A_2<C`. This logical bridge is present and sound. An explicit numerical improvement below `C` is not supplied or certified.

## 4. Local versus global injectivity

For the disk-holomorphic branch

\[
P_a(z)=z+2a\bigl((1-z)^{-1}+\log(1-z)-1\bigr),
\]

one has `P_a'=1+2a z/(1-z)^2`. The Koebe collision identity factors by `(z-w)(1-zw)`, and `zw=1` cannot occur in the disk. Thus the derivative is globally injective on this domain for nonzero `a`.

At `a=9/5`, the only zeros of `P_a'` are `-4/5±3i/5`, both on the boundary. Hence the primitive is locally injective throughout the disk. This says nothing sufficient about its global injectivity.

For points `ir`, the imaginary part of the primitive is

\[
J_a(r)=r+2a\left(\frac r{1+r^2}-\arctan r\right).
\]

It is positive near zero and negative at `r=1` whenever `a>2/(pi-2)`. The branch is continuous at `i`, so the intermediate-value step yields an interior zero. Real Taylor coefficients then give the same primitive value at two distinct points `ir` and `-ir`.

The added audit recomputed the claimed collision bracket `19/20<r<49/50` using a different exact enclosure for pi: the tangent-addition identity `atan(1/2)+atan(1/3)=pi/4` and alternating-series remainders. Both endpoint signs pass. The collision, local injectivity, and derivative injectivity are therefore compatible, exactly as the package claims.

No assertion about the sufficiency of the complementary parameter range is supported. `P_a` is a disk-holomorphic logarithmic primitive, not an entire example.

## 5. Symmetrization counterexample and domain guards

For the specified entire function `E`, independent differentiation confirms `E'(0)=1`, `E''(z)=exp(2iz)/10`, and `a_2=1/20`. The package's uniform bound implies positive real part of `E'` on the disk. The segment-integral proof of injectivity uses the convexity of this domain and is valid.

Equality of two derivative values forces `z-w` to be an integer multiple of pi. The disk diameter is smaller than pi, so the derivative is injective on the disk. Its periodicity explicitly shows that it is **not** injective on the whole complex plane. Entire analyticity must not be conflated with entire-plane univalence.

The conjugate average is `T(z)=z+(1-cos(2z))/40`. Its derivative has a critical point at `pi/4`, strictly inside the disk. There is also a direct two-point collision: `T'(pi/4+1/10)=T'(pi/4-1/10)`, and both arguments are in the disk. This independently confirms the failure without relying solely on the necessary nonvanishing-derivative condition for injectivity.

The average itself remains univalent: its derivative is the average of `E'(z)` and `conjugate(E'(conjugate(z)))`, both with positive real part. Both functions retain the same positive real second coefficient. The example disproves preservation of the class by this averaging operation. It does not prove that no real extremizer exists.

## 6. Convex control

For `G=-z/3-(4/3)log(1-z)`, differentiation gives the stated Möbius derivative and coefficients `4/(3n)`. The derivative has no pole or zero in the disk. Its image is a half-plane. In the analytic convexity criterion, the two terms `z/(1-z)` and `z/(3+z)` each have real part strictly greater than `-1/2` inside the disk. Thus the criterion is strictly positive and establishes convexity of `G`.

This verifies only this example and the transcription discrepancy. It does not independently prove the historical sharp theorem for a whole convex subclass.

## 7. Published candidate: what is and is not established

The logarithmic integral defining the reported derivative expands to exactly the odd power series `Q` in the frozen package. Independent recurrence calculations for the exponential coefficients reproduce the three displayed coefficients, including the positive value `3/2+1/pi` at degree two.

The coefficient-limit proof is valid and does not require candidate univalence. The coefficient sequence of `Q` is absolutely summable. The space of absolutely summable power series is a Banach algebra, so `exp Q` also has absolutely summable coefficients. In fact its norm is bounded by `exp(pi/4)`.

Multiplication by `(1+z)/(1-z)^2`, followed by integration, produces exactly the triangular weighted sum in the package. Every weight is bounded by 2, and each fixed-index weight converges to 2. Dominated convergence for the absolutely summable coefficient sequence applies. It yields

\[
\lim a_n(F)=2\exp\left(\frac{2\,\mathrm{Catalan}}\pi\right)
=3.583245624139186849\ldots.
\]

The source's membership assertion is an additional input before this becomes a lower asymptotic bound for the extremal numbers. A coefficient limit for one function cannot imply that its coefficients maximize the unrestricted class. The package keeps these statements separate.

## 8. Disposition and publication boundary

Recommended disposition: exhausted partial work, five approaches used, full target unsolved **in this package**. There are no mandatory mathematical revisions for that disposition. Do not describe it as a solved problem, an independently reverified Barnard–Suffridge proof, an established optimal bound, or a proof of the problem's current global open status.

The supplied source-dependence and bibliographic-access limitations should remain attached to any use of the results. Dataset provenance and remote repository search history are frozen metadata, not independently reaudited live facts here.

This audit's safe directory contains authored mathematics, authored code, results, hashes, byte counts, and public source metadata only. It contains no external PDF, reproduced source text, dataset records, or private coordination files.
