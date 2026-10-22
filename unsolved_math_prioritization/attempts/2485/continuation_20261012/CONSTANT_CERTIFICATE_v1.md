# Self-contained rational certificate for the positive sieve margin

12 October 2026. This authored supplement supplies the finite arithmetic details for equation (20) of *A square-root overhead bound for the actual Erdős–Selfridge minimum*. It leaves the original proof unchanged. No executable or data file is required to state or check this certificate.

For the parameters c=8/5 and z=4, the required positive quantity is

\[
\Delta=4\log4+\frac{16}{5}\log\frac{164}{39}
-2\log\frac{13}{3}-2\pi-8\arctan\frac19.
\tag{1}
\]

This follows by inserting the explicitly evaluated integrals from the proof and combining logarithms. Machin's identity
\(\pi=16\arctan(1/5)-4\arctan(1/239)\) converts the remaining pi term into arctangents with rational arguments.

For positive rational q, set v=(q-1)/(q+1) and define the rational number

\[
L_{40}(q)=2\sum_{j=0}^{39}\frac{v^{2j+1}}{2j+1}.
\]

For rational 0<t<1, define

\[
A_{40}(t)=\sum_{j=0}^{39}\frac{(-1)^j t^{2j+1}}{2j+1}.
\]

The finite rational certificate is

\[
\begin{split}
D_{40}={}&4L_{40}(4)+\frac{16}{5}L_{40}(164/39)
-2L_{40}(13/3)\\
&-32A_{40}(1/5)+8A_{40}(1/239)-8A_{40}(1/9),
\end{split}
\]

with the exact rational inequalities

\[
\frac{402355317}{10^{10}}<D_{40}<\frac{402355318}{10^{10}}.
\tag{2}
\]

Equation (2) is a finite rational calculation: substitute the six displayed finite sums, multiply by their positive common denominator, and compare integers. Both comparisons have been separately reproduced by exact rational arithmetic; no floating-point estimate is being used as the premise.

For completeness the remainder is also explicitly bounded. The logarithm series gives

\[
\left|\log q-L_{40}(q)\right|
\le\frac{2|v|^{81}}{81(1-v^2)}.
\]

For the three logarithm arguments used above, |v| is at most 5/8. The sum of the absolute logarithm coefficients is 46/5. The alternating-series bound gives
\(\left|\arctan t-A_{40}(t)\right|\le t^{81}/81\).
For the three arctangent terms, t is at most 1/5 and the sum of the absolute coefficients is 48. Therefore

\[
|\Delta-D_{40}|\le
\frac{46}{5}\frac{2(5/8)^{81}}{81(1-(5/8)^2)}
+\frac{48}{81\cdot5^{81}}
<\frac1{10^{15}}.
\tag{3}
\]

The final comparison in (3) involves positive rational numbers only. Combining (2) and (3) proves, in particular,

\[
0.0402355<\Delta<0.0402356,
\]

so the strict negative exponent margin in the Bonferroni proof is certified. The resulting asymptotic coefficient is c-1+A/2=13/5 with A=4.

The only transcendental identities used in this certificate are the logarithm and arctangent power series and Machin's identity. The latter can be checked by the tangent addition formula: if alpha=arctan(1/5), then tan(2alpha)=5/12 and tan(4alpha)=120/119; consequently tan(4alpha-arctan(1/239))=1, and the angle lies in (0,pi/2), so it equals pi/4.
