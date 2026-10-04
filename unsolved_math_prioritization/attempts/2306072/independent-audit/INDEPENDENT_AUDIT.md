# Independent adversarial audit: Function Theory 6.72

## Verdict

**PASS for the complete mathematical counterexample in the frozen candidate.** No blocking mathematical defect was found. The proof establishes, using its stated classical inputs, that every global maximizer of

\[
\operatorname{Re}\{a_2+i10^{-24}(a_4-3a_3)\}
\]

has an actual omitted slit with nonmonotone continuous argument, nonmonotone signed outward radial angle, and nonmonotone ordinary unsigned radial angle. This addresses both global questions in the identified Problem 6.72. It is not merely a trajectory construction or a numerical optimization result.

The result remains an independently checked, unrefereed candidate. This audit does not certify historical priority, peer review, or a formalized proof. No remote write was performed, and the frozen public files were not edited. No mathematical revision is required by this audit.

Audit date: 2026-10-04 UTC.

## Frozen object and replay

- Problem ID: 2306072; rank 587; Hayman–Lingham Problem 6.72.
- PROOF.md SHA-256: `f01dd412bf207967018faa7e1b5a599630ed64830daa5874a0d6c1ce4e54e1c8`.
- SHA256SUMS.json SHA-256: `c5bf26bfcfbf3502b8430d130ec35ac58111e99fca21838a9263fe1092971a83`.
- Frozen manifest replay: all 10 listed public files passed.
- Author's finite verifier: all 56 exact checks passed.
- Separate audit arithmetic: all 23 supplemental exact checks passed; see `independent_checks.py` and `INDEPENDENT_CHECKS.json`.

Neither arithmetic program proves the analytic theorems or substitutes for the reasoning below.

## Primary-source and target checks

I independently rendered and visually inspected Duren's printed pp.352–355 from the source PDF, rather than relying solely on candidate quotations or OCR. I independently rendered and inspected Hayman–Lingham's printed p.143, PDF p.144. The source files match their declared hashes:

- Duren PDF: `099c6a5e7e7945fb06a4b858e6b81f3ad0bb7f4de2911f844048d2c180499ef0`.
- Hayman–Lingham PDF: `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.

Duren p.352 states the single analytic omitted arc, increasing modulus, and the equation with the exact sign and normalization used in the candidate:

\[
L\!\left(\frac{f^2}{f-w}\right)\frac{dw^2}{w^2}>0.
\]

Page 353 gives the nonvanishing of \(L(f^2)\) and the uniqueness of the trajectory ending at the simple pole at infinity. Page 354 explicitly parameterizes the actual arc from a finite endpoint to infinity. Page 355 uses the signed radial-angle convention and notes its limiting value at infinity. None of these statements is a sufficiency theorem for an arbitrary trajectory; the candidate correctly uses them only after obtaining an actual global maximizer.

The selected Hayman–Lingham page asks the two global monotonicity questions asserted in the candidate. Its historical update does not establish current openness or novelty.

Sources: [Duren (1981), ETH scan](https://www.e-periodica.ch/cntmng?pid=com-001%3A1981%3A56%3A%3A30&bot=1); [Hayman–Lingham (2018), arXiv version 2](https://arxiv.org/pdf/1809.07200v2).

The indexed primary text for Hibschweiler (1995) reports eventual monotonicity. Full PDF retrieval remained unavailable during this audit; it is not an essential premise. A separate local-series check below establishes compatibility without relying on its inaccessible proof. No source PDF or scan image is included with these audit deliverables.

## 1. Actual global maximizers and uniformity: PASS

A finite linear combination of coefficient maps is a continuous complex-linear functional on \(H(D)\). Compactness of normalized \(S\) gives a maximizing function. The comparison with the identity and the Koebe function gives real functional values 0 and 2, respectively, so the real part is genuinely nonconstant. The maximizing function therefore meets the support-point theorem's hypothesis.

For each maximizer separately, the coefficient bounds give

\[
\operatorname{Re}a_2\ge 2-13\varepsilon,
\qquad |a_2-2|^2\le 52\varepsilon,
\qquad 1-|a_2|^2/4\le13\varepsilon.
\]

The odd-root construction is legitimate: \(f(z)/z\) never vanishes in the disk, so its normalized analytic square root exists. The function \(g(z)=z\sqrt{f(z^2)/z^2}\) is odd and injective. Equality of two values gives equality of their squared arguments under \(f\); the remaining opposite-point case is excluded by oddness and the unique zero at zero. Thus its reciprocal exterior map meets the area theorem's hypotheses.

The exterior coefficient of order \(\zeta^{-3}\) is \(3a_2^2/8-a_3/2\), with area-theorem weight 3. It follows that

\[
|a_3-3a_2^2/4|<5\eta,
\qquad |a_3-3|<29\eta.
\]

The exact identity

\[
A+2=2(a_3-3)+(a_2-2)(a_2-4)
\]

gives the stated 106\(\eta\) bound, and \(B-3=3(a_2-2)\) gives 24\(\eta\). All estimates are uniform over every maximizer. No unique maximizing selection, coefficient differentiability in \(\varepsilon\), or stability assumption about the maximizer is used.

The standard compactness, coefficient, and area theorems are explicit external mathematical inputs; their full historical proofs have not been reconstructed by this audit.

## 2. Finite-tip gate: PASS

The same exterior map equals \(\zeta H(\zeta^{-2})\), so the tail weights in (7) are exactly \(2n-1\). The two Cauchy–Schwarz estimates in (8) and (9) have the correct powers and summation ranges. For \(r=2/3\), the bounds \(16/135<1/4\) and \(56/25<9/4\) are correct.

At \(z_*=-2/3\), the derivative formula

\[
f'=(H-2z_*H')/H^3
\]

has reference numerator \(1/3\), not \(5/3\). The numerator error is bounded by \((5+40/3)\eta<19\eta\). Dividing by \((3/2)^3\) gives less than \(6\eta\); the remaining reciprocal-cube contribution is less than \(2\eta\). The function-value error is less than \(2\eta\).

One numerical detail is implicit but valid: the factor \(7/2\) in the reciprocal-square estimate follows from (8), since

\[
|H+H_0|\le10/3+5\eta<7/2.
\]

The weaker separately displayed bound \(|H|<2\) alone would not give that factor, but (8), which is explicitly available at that step, does. This is a nonblocking expository detail, not a false inequality or missing hypothesis.

The direction of the boundary-distance estimate (11) is correct. If \(B(f(z),d)\) lies in the image domain, compose the inverse on that disk with the disk automorphism sending \(z\) to zero. Its derivative at the center has modulus \(d/((1-|z|^2)|f'(z)|)\), and Schwarz's lemma bounds that by 1. Consequently the distance is at most the conformal radius.

At \(z_*\), the unperturbed bound is \(6/25+1/25=7/25\). The error is less than \((2+40/9)\eta<7\eta\). Since the omitted arc is closed and its modulus increases from its tip, this implies

\[
|w_{\rm tip}|<7/25+7\eta<3/10.
\]

No boundary convergence of the conformal map has been presumed. In particular, locally uniform closeness to Koebe has not been incorrectly converted into endpoint convergence.

## 3. Differential and natural coordinate: PASS

Expanding at \(z=0\), with \(w\ne0\), gives

\[
\frac{f^2}{f-w}=-\frac{f^2}{w}-\frac{f^3}{w^2}-\frac{f^4}{w^3}+O(z^5).
\]

The resulting coefficient extraction in (13) is correct, including all minus signs. Specifically,

\[
a=L(f^2)=1+i\varepsilon A,\quad
b=L(f^3)=i\varepsilon B,\quad
c=L(f^4)=i\varepsilon.
\]

Under \(w=-v^{-2}\), direct substitution gives

\[
Q(w)dw^2=4(a-bv^2+cv^4)dv^2.
\]

Thus the sign and the double-cover normalization both agree with the primary source. In the coordinate \(u=1/w\), the differential is

\[
(-a/u-b-cu)du^2,
\]

which has a simple pole at infinity because \(a\ne0\).

On the closed radius-3 disk, the perturbation of \(P\) is smaller than 1. Its square root can be chosen with positive real part and is analytic on a neighborhood of that disk. Therefore

\[
|p-1|=|P-1|/|p+1|\le111\varepsilon
\]

and \(|G(v)-v|\le333\varepsilon\). For each \(|t|<2\), Rouché applies on \(|v|=3\), with a strict error margin. It yields exactly one root of \(G(v)=t\) in the disk, not merely at least one. Since \(G'\ne0\), the local inverses patch uniquely to a holomorphic \(V\). Evenness of \(p\) gives oddness of \(G\) and \(V\).

For positive real \(t\), \(V(t)\ne0\), \(V'(t)\ne0\), and \(W=-V^{-2}\) is a regular positive trajectory. Moreover \(W(t_1)=W(t_2)\) would imply \(V(t_1)=\pm V(t_2)\); injectivity and oddness of \(V\) then imply \(t_1=t_2\) for positive parameters. Hence the parametrized segment cannot hide a self-intersection or reverse its orientation.

## 4. Identification with the actual omitted slit: PASS

This is the critical distinction between the candidate and an invalid formal-trajectory argument.

The maximizer already supplies an actual slit \(\Gamma\) with the same differential. The trajectory \(W\) tends to its simple pole at infinity. The cited unique-trajectory theorem therefore identifies their germs there.

One can also see the local uniqueness directly in this natural coordinate. Lift a sufficiently distant tail of \(\Gamma\) through \(w=-v^{-2}\). The trajectory condition makes \(\operatorname{Im}G(v)\) constant. Its limiting value is zero because \(v\to0\) at infinity. Thus \(G(v)\) is real. The positive and negative real branches give the same \(w\)-arc, since \(V\) is odd. There is only one geometric germ.

For continuation, suppose agreement first ceased at a finite parameter \(t_*\le7/4\). Closedness of \(\Gamma\) puts \(W(t_*)\) on the actual omitted arc. It is finite and satisfies

\[
|W(t_*)|>25/81>3/10>|w_{\rm tip}|.
\]

It is therefore an interior point of the slit, not its endpoint. At that point \(Q\) is regular and nonzero, because \(P\ne0\) and \(V\ne0\). Local uniqueness of regular trajectories extends agreement past \(t_*\), a contradiction. This proves inclusion of the whole tested segment in \(\Gamma\).

The positive radius gap is exactly \(25/81-3/10=7/810\). Its size is independent of any unproved endpoint continuity. The parameter moves inward from infinity, so the outward tangent is \(-W'\). This conclusion does not require an unproved sufficiency characterization of support-point slits.

## 5. Analytic inverse errors and exact signs: PASS

The identity for the square-root remainder is exact:

\[
\sqrt{1+x}-1-x/2=-x^2/[2(\sqrt{1+x}+1)^2].
\]

The selected branch makes the denominator's modulus at least 1 before squaring. The resulting 162\(\varepsilon\eta\) bound for \(p\), followed by integration, gives the 486\(\varepsilon\eta\) bound for the remainder in \(G\). The derivative of \(d\) is bounded by 55 on the radius-3 disk. Both \(t\) and \(V(t)\), as well as their straight connecting segment, lie there. The inversion error therefore costs no more than \(55\cdot333\varepsilon^2=18315\varepsilon^2\), giving 487\(\varepsilon\eta\).

For \((1+x)^{-1/2}\), Taylor's integral remainder is valid in the entire complex disk \(|x|\le1/4\). The asserted constant 2 is conservative: squaring the required derivative bound reduces to the exact inequality \((3/8)^2(4/3)^5<4\). The coefficient error costs 161\(\varepsilon\eta\), the quadratic Taylor term costs 24642\(\varepsilon^2\), and replacing \(P_0(V)\) by \(P_0(t)\) costs 20979\(\varepsilon^2\). These give the stated 162\(\varepsilon\eta\) derivative remainder.

The passage to \(Z=tV'/V\) is not a formal division of truncated series. Multiplying the claimed approximation by \(V\) leaves the exact error numerator

\[
tR_{V'}-R_V-i\varepsilon q(V-t).
\]

With \(|V|>1/2\), the two error contributions are bounded by

\[
1541\varepsilon\eta+4662\varepsilon^2<2000\varepsilon\eta.
\]

The endpoint polynomial values are exactly \(3/5\) and \(-441/640\). The full proved error leaves respectively a margin greater than \(\varepsilon/2\) and smaller than \(-\varepsilon/2\) for \(\operatorname{Im}Z\). Since \(q\) is real on this interval, the same estimate gives \(\operatorname{Re}Z>0\). The signs do not depend on floating-point arithmetic or the unknown extremal coefficients.

## 6. Both geometric conclusions and conventions: PASS

For any continuous lift of argument along the actual segment,

\[
\theta'(t)=\operatorname{Im}(W'/W)=-2\operatorname{Im}Z(t)/t.
\]

The derivative is negative at 1 and positive at \(7/4\). Smoothness at these regular interior slit points then rules out both nondecreasing and nonincreasing argument. Changing the lift by an integer multiple of \(2\pi\) changes neither derivative.

The signed outward radial angle is

\[
\beta=\arg((-W')/W)=\arg Z.
\]

The factor relating the two ratios is a positive real number. The positive-real-part estimate gives the intended local branch. The support-slit radial-angle bound selects a consistent signed branch along the whole tail. Oddness and the nonzero linear coefficient of \(V\) imply \(tV'/V\to1\), so \(\beta\to0\) at infinity. The positive value at 1 and negative value at \(7/4\), together with that initial limit, rule out either monotonic direction on the entire slit.

Finally, continuity gives an interior zero between these two signed values. Therefore the ordinary unsigned outward angle \(|\beta|\) is positive at both ends of this compact subarc and zero inside it. It cannot be monotone. Reversing a chosen tangent orientation changes the usual vector angle to its supplement and does not restore monotonicity. The conclusion is consequently robust to the conventional ambiguities in the second question.

## 7. Compatibility with eventual monotonicity: PASS

The frozen proof needs no eventual-monotonicity theorem for its counterexample. There is also an independent exact local check. Expanding the actual natural coordinate for the fixed maximizer yields

\[
V(t)=a^{-1/2}t+\frac{b}{6a^{5/2}}t^3+O(t^5),
\qquad Z(t)=1+\frac{b}{3a^2}t^2+O(t^4).
\]

Since \(b=i\varepsilon B\), the leading imaginary coefficient is

\[
\frac{\varepsilon}{3}\operatorname{Re}(B/a^2).
\]

The candidate's bounds imply \(|A|<3\), \(|a-1|<3\varepsilon\), and

\[
|a^{-2}-1|<7\varepsilon,\qquad
|B/a^2-3|<25\eta.
\]

Hence \(\operatorname{Re}(B/a^2)>0\). The actual radial angle is increasing with inward \(t\) sufficiently near zero, and the actual argument has a fixed derivative sign there. The reversal proved farther inward is fully compatible with eventual monotonicity near infinity. The qualitative polynomial display in Section 7 is not being used to extend an interval-specific error estimate down to zero.

## Defects, clarifications, and scope

**Blocking defects found: none.**

**Required mathematical revisions: none.**

Two optional exposition improvements would make already valid steps more explicit:

1. At the reciprocal-square estimate in Section 4, record \(|H+H_0|\le10/3+5\eta<7/2\), so the origin of the factor \(7/2\) is immediately visible.
2. Expand the continuation paragraph into a first-exit/closedness argument, as above, if writing for readers less familiar with quadratic differentials.

Neither point changes a constant, assumption, conclusion, or frozen verdict. The modest source-access limitation for Hibschweiler has no effect on the proof because that work is background rather than an essential input. The actual standard analytic dependencies were identified and checked for applicability. The candidate makes no justified claim to uniqueness of a maximizer or to a closed form, and neither is needed.

Recommendation: retain the candidate's provisional `claimed_solved`, `1/5` characterization if the surrounding workflow requires a status label, with the independent audit recorded separately. Do not convert this audit into a claim of expert peer review or historical priority.
