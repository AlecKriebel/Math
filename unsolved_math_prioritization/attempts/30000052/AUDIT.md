# Independent audit: a counterexample to the random generalized-lattice comparison

## Decision

**ACCEPT_FULL_NEGATIVE.** The frozen candidate proves that the universally quantified expected-moment comparison in problem 30000052 / OWR-723-005 is false. For independently continuous uniform generator and shift, the example with n = 3, d = 1, p = 4 has expected normalized anchored fourth moment 19/1620, whereas the corresponding iid moment is 4/405 = 16/1620. The strict excess is 1/540, and the ratio is 19/16. The separately supplied n = 4 empty-tail argument is also valid and independently sufficient to refute the universal comparison.

No mathematical correction is required. The audited original has minor inline TeX delimiter errors; this separately identified edition repairs only those proof delimiters. The frozen original remains unchanged. ACCEPTANCE.json distinguishes the original and distributed document identities.

This is an independent AI-assisted mathematical audit. Acceptance is not external human peer review, proof-assistant certification, or certification of historical novelty. The analytic proof stands without the supplementary code.

## 1. Exact input and source identification

The audit is tied to the frozen original proof of 7,673 bytes with SHA-256 `7fbb3d20d27cc709ef84fc8106c06472335f892321815921e71019e01e110c7d`. Its identity and the full frozen author inventory were verified before acceptance. The distributed PROOF.md has delimiter-only editorial repairs, with its separate identity recorded in ACCEPTANCE.json and MANIFEST.json.

The exact original question is Erich Novak's contribution, reporting joint work with Aicke Hinrichs, *New bounds for the star discrepancy*, in *Discrepancy Theory and Its Applications*, Oberwolfach Report 13/2004, printed pp. 696–699. The definition is on p. 697 and the proposed comparison is displayed on p. 698. Sources: [report DOI](https://doi.org/10.4171/OWR/2004/13), [official PDF](https://ems.press/content/serial-article-files/45858).

The source PDF is 445,532 bytes, SHA-256 `2f02cd5834ed1a868d95a20be9d172ade3b35e76caf8c9ff8ab6a3adaf6f3d3e`. The original PDF context on PDF pages 24–27 was read, and PDF pages 25–26 were independently inspected as rendered images. A fresh extraction from the PDF was also compared with the frozen context. The source PDF and inspection history were authenticated against their recorded identities.

The source definition is

\[
\operatorname{disc}_p(t)^p=
\int_{[0,1]^d}\left|\prod_{r=1}^d x_r-
\frac1n\sum_{j=0}^{n-1}\mathbf1_{[0,x)}(t_j)\right|^p\,dx.
\]

The source then integrates over the entire product cube of generator and shift, with

\[
t_j=\{jz+\Delta\},\quad 0\le j<n,
\qquad (z,\Delta)\in[0,1]^{2d}.
\]

Thus the generator and shift are independent continuous uniforms. The source supplies no restriction to rational generators, no conditioning on distinct or well-spread points, no fixed-generator average, and no primality requirement on n. Its discussion specifies even p. The counterexample's n = 3, d = 1, p = 4 is admissible. Reversing the sign inside the absolute value is immaterial. The comparison concerns the expectation of the p-th power, not the expectation of the norm itself.

The final sentence on p. 699 also discusses a different existence/upper-bound problem for well-chosen lattices. The counterexample refutes the displayed averaging comparison; it does not disprove that separate existence problem.

## 2. Pairwise independence, and the exact dependence that remains

Let u = t_0 = Delta and v = t_1 = {z + Delta}. Conditional on Delta, addition by Delta preserves uniform circle measure. It follows that u and v are independent uniforms and

\[
t_2=\{2v-u\}.
\]

For any distinct indices j and k, t_j is uniform and independent of z: conditional on z it is a translate of the uniform shift. The map z to {(k-j)z} preserves uniform circle measure, including when |k-j| is greater than one. Conditional on t_j, therefore, t_k = {t_j + (k-j)z} is uniform. This proves uniform pairwise independence. Coordinatewise the same argument gives independent uniform vector pairs in any dimension.

The three-point law is not an iid triple. For 0 <= x <= 1/2, set q(x) = P(t_0 < x, t_1 < x, t_2 < x). Under u,v in [0,x), the quantity 2v-u lies between -x and 2x. A negative value has fractional part at least 1-x, hence cannot lie in [0,x), except for irrelevant endpoints. A nonnegative value is below one, again apart from the limiting boundary. Consequently the inclusion condition is exactly

\[
0\le2v-u<x
\]

up to null sets. For fixed u in [0,x], v ranges from u/2 to (u+x)/2. This interval lies inside [0,x] and has length x/2. Its area is

\[
q(x)=x^2/2\quad(0\le x\le1/2).
\]

In particular q(1/4) = 1/32, whereas an iid triple has inclusion probability 1/64. Pairwise independence does not permit replacement of q by x^3.

For completeness, reflection and inclusion-exclusion also give the full probability:

\[
q(x)=
\begin{cases}
x^2/2,&0\le x\le1/2,\\
1/2-2x+(5/2)x^2,&1/2\le x\le1.
\end{cases}
\]

Indeed, the probability that all three points lie in [x,1) is 1-3x+3x^2-q(x), and reflection identifies it with q(1-x). The two expressions agree at 1/2. Extending x^2/2 all the way to one would be an error; neither the manuscript nor the accepted calculation does this.

## 3. Count distribution and fourth moment

Let N_x count indexed points in [0,x), and let P_k = P(N_x = k). Uniform marginals, uniform pairs, and the definition of q give

\[
\mathbb EN_x=3x,\qquad
\mathbb E\binom{N_x}{2}=3x^2,\qquad
P_3=q.
\]

These equations, with total probability one, uniquely give

\[
(P_0,P_1,P_2,P_3)=
(1-3x+3x^2-q,\;3x-6x^2+3q,\;3x^2-3q,\;q).
\]

On the lower half interval this is

\[
(1-3x+\tfrac52x^2,\;3x-\tfrac92x^2,
\;\tfrac32x^2,\;\tfrac12x^2).
\]

The entries sum to one and are nonnegative throughout that interval. An independent reconstruction via falling factorial moments gives

\[
\begin{aligned}
\mathbb EN_x^2&=3x+6x^2,\\
\mathbb EN_x^3&=3x+18x^2+6q,\\
\mathbb EN_x^4&=3x+42x^2+36q.
\end{aligned}
\]

Expanding (N_x/3-x)^4 therefore yields, before substituting q,

\[
F(x)=x^4-\frac23x^3+\frac2{27}x^2+\frac{x}{27}
+\frac49(1-2x)q(x).
\]

For x <= 1/2 this becomes exactly the manuscript's polynomial

\[
F(x)=x^4-\frac{10}{9}x^3+\frac8{27}x^2+\frac{x}{27}.
\]

Simultaneous reflection t_j to {-t_j} preserves the joint law, because (z,Delta) to ({-z},{-Delta}) preserves product Lebesgue measure. At a fixed x, reflection exchanges the count with 3-N_(1-x) outside endpoint events of probability zero. Thus the centered discrepancy changes sign and F(1-x) = F(x). The integrand is measurable, nonnegative, and bounded, so Tonelli/Fubini interchanges expectation and the x integral without any extra hypothesis. The result is

\[
2\int_0^{1/2}F(x)\,dx
=2\left(\frac1{160}-\frac5{288}+\frac1{81}+\frac1{216}\right)
=\frac{19}{1620}.
\]

A particularly direct independent verification of the strict margin compares with the iid triple, for which q_iid(x) = x^3. On the lower half interval,

\[
F(x)-F_{\rm iid}(x)
=\frac49(1-2x)(x^2/2-x^3)
=\frac29x^2(1-2x)^2.
\]

The reflected difference is nonnegative everywhere and positive except at the finitely many zeros. Its full integral is

\[
\frac49\int_0^{1/2}x^2(1-2x)^2\,dx
=\frac49\cdot\frac1{240}
=\frac1{540}.
\]

This confirms both the sign and the exact claimed excess, without subtracting two approximate values.

## 4. The iid formula

For independent Bernoulli(x) variables B_i, let Y_i = B_i-x and a=x(1-x). Then E Y_i = 0, E Y_i^2 = a, and E Y_i^4 = a-3a^2. In the fourth-power expansion only the all-equal and two-pairs index patterns survive. The coefficient of the latter is 6 binomial(n,2) = 3n(n-1). Hence

\[
\mathbb E\left(\frac1n\sum_iY_i\right)^4
=\frac{n(a-3a^2)+3n(n-1)a^2}{n^4}.
\]

Integrating a and a^2 gives 1/6 and 1/30, respectively, so

\[
\mathbb E\operatorname{disc}_4(U_1,\ldots,U_n)^4
=\frac{3n-1}{30n^3}.
\]

At n = 3 this is 4/405. At n = 4 it is 11/1920. At n = 1,2 the values are 1/15 and 1/48, respectively. The n^-4 normalization in the central-moment expansion is essential and has been retained.

## 5. Independent verification of the second counterexample

For n >= 3, the ascending triangle is

\[
0\le z\le1/(n-1),\qquad 0\le\Delta\le1-(n-1)z.
\]

Apart from null boundaries, the n points have no wraparound and lie in [Delta, Delta+(n-1)z]. The discrepancy equals -x below the first point and 1-x above the last point. Integrating just these two nonnegative fourth-power contributions gives

\[
\frac{\Delta^5+(1-\Delta-(n-1)z)^5}{5}.
\]

Integrating over Delta first gives (1-(n-1)z)^6/15, and integrating over z gives 1/[105(n-1)]. For the descending triangle write z = 1-w, with 0 <= w <= 1/(n-1) and (n-1)w <= Delta <= 1. The points now range from Delta-(n-1)w to Delta, and the same tail integral and total contribution result.

The triangles have disjoint interiors for n >= 3: their generator intervals meet only at a boundary when n = 3, and are separated when n > 3. Their boundaries can be discarded without changing the integral. No contribution from the rest of the parameter square is negative. Therefore

\[
\mathbb E\operatorname{disc}_4(M_n^{z,\Delta})^4
\ge\frac{2}{105(n-1)}.
\]

At n = 4,

\[
\frac2{315}-\frac{11}{1920}=\frac5{8064}>0.
\]

This proves the second counterexample without knowing the full lattice moment. As an adverse check, at n = 3 the analogous lower bound 1/105 is less than 4/405, so this lower bound alone does not establish the three-point result. The manuscript correctly supplies a separate exact calculation for n = 3.

## 6. Null sets, indexing, second moments, and minimality

For distinct j,k, collisions require (k-j)z to be an integer in every coordinate. For fixed n,d this is a finite union of null parameter sets. Nevertheless, the counting definition is indexed: a collision is not a reason to replace the normalization or condition the sample. The proof consistently keeps all n indices. Uniform marginals make the event t_j=x (and t_j=0) null for any fixed x. For a fixed configuration, box-boundary equalities occur on a null set of integration endpoints. These observations justify the half-open interval convention and the reflection step. Values z=1, Delta=1, or endpoints of parameter triangles also form null sets. Replacing [0,1) by [0,1] does not alter the expectation.

For any anchored box B_x in dimension d, its volume is v = product x_r. Pairwise independence gives

\[
\mathbb E\left(\frac1n\sum_j\mathbf1_{B_x}(t_j)-v\right)^2
=\frac{v(1-v)}n.
\]

Since the integrals of v and v^2 are 2^-d and 3^-d, respectively,

\[
\mathbb E\operatorname{disc}_2(M_n^{z,\Delta})^2
=\frac{2^{-d}-3^{-d}}n,
\]

exactly as in the iid ensemble. This equality addresses all n,d, not only the numerical controls in dimension one.

When n = 1 the only point is uniform. When n = 2 the entire ordered point pair is iid uniform, coordinatewise, so the complete ensemble laws agree in all dimensions. Every measurable discrepancy functional with a defined expectation therefore agrees for these two point counts. The candidate's claim that three is the smallest possible point count for a counterexample is correct. It does not claim that every even exponent or every dimension exhibits a reversal.

## 7. Independent exact recomputation

The audit's exact computation does not import or call the candidate verifier and does not reuse its polygon-clipping calculation. It integrates the shift first using order statistics. For sorted points s_1 <= ... <= s_n and even p, the deterministic identity is

\[
\operatorname{disc}_p^p
=\frac1{p+1}\sum_{j=1}^n
\left[(s_j-(j-1)/n)^{p+1}-(s_j-j/n)^{p+1}\right].
\]

For fixed rational z, the Delta interval is cut only where a point wraps through one. Inside each open subinterval the sorted points are Delta+c_j, with fixed rational c_j. The displayed polynomial integrates exactly in Delta by its elementary antiderivative.

As z varies, the ordering and wrap-cut arrangement can change only when (j-k)z is an integer. Partitioning [0,1] at these rational points gives intervals on which the shift-integrated answer is a polynomial of degree at most p+2. The audit reconstructs that polynomial by exact rational interpolation at p+3 interior points, verifies it at additional distinct rational points, and integrates it exactly. The degree bound and the complete breakpoint set justify this method; it is not numerical quadrature or a statistical estimate.

For n = 3, p = 4, the shift-averaged polynomial on 0 <= z <= 1/2 is

\[
H(z)=\frac1{15}-\frac{56}{81}z+\frac{76}{27}z^2
-\frac{16}{3}z^3+4z^4.
\]

The upper-half polynomial is H(1-z). Each half integral is 19/3240, recovering 19/1620. For n = 4 the generator partition is 0, 1/3, 1/2, 2/3, 1; exact integration yields 139/17280, which exceeds the sufficient lower bound 2/315 and exceeds the iid value by 1/432. This exact n = 4 value is supplementary; the accepted analytic counterexample does not depend on it.

A separate exact sliced-area calculation keeps every modular band for the triple-inclusion event and performs 495 rational-parameter checks throughout [0,1], including 0, 1/2, and 1. It verifies the count polynomial and reflection as well. The iid values are independently recomputed by integrating the complete binomial sum with integer beta integrals. Second-moment controls n = 1,2,3,4 and fourth-moment controls n = 1,2 all agree. Normal and optimized Python outputs are identical. The original author checker was also replayed separately and reproduced its mathematical results.

These checks corroborate the elementary proof. They are not prerequisites for accepting the probability, moment, reflection, or triangle arguments above.

## 8. Adverse checks, attribution limits, and acceptance scope

The audit specifically rejects the following tempting substitutions: treating pairwise independence as triple independence; extending the lower-half q formula to x=1; using a fixed zero generator in place of the full generator average; applying the three-point empty-tail bound as if it already exceeded iid; and dropping the fourth-power normalization. The exact calculations distinguish all these cases.

A separate integrity verifier authenticates the audit manifest from an external digest, verifies strict file inventory, hashes and byte counts, and rejects duplicate JSON keys, nonfinite constants, malformed sizes, unsafe paths, symlinks, missing members, and unlisted members. Independent adverse controls exercise corrupted and re-pinned copies without modifying any audited input. Explicit exceptions are used so optimization cannot disable checks.

The source and literature review was bounded. Broad lattice search hits concern different mathematical questions, including lattice group generators, lattice circles, Wills inequalities, and packing bounds; their conclusions do not settle this expected-moment comparison. Neither a dated open-status label nor absence of a search hit proves global openness or novelty. SOURCE_REVIEW.md records the inspected sources and retrieval limits.

**Accepted scope:** a complete negative answer to the original displayed universal expected-p-th-moment comparison, with the correct continuous law and normalized anchored discrepancy; correct second-moment and n <= 2 consistency statements; correct independent n = 4 geometric counterexample. **No claim:** exhaustive literature novelty, a result about the expectation of the norm rather than its p-th power, failure of carefully chosen lattice generators, or a solution to the separate existence/upper-bound problem.
