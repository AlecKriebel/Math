# Independent adversarial review: empty tails and scope of PR #1135

**Decision: mathematical PASS for the full negative answer to the displayed expected-moment comparison. No candidate mathematical repair is needed.** This review concentrates on the independent empty-tail mechanism, normalization, the all-n implications, and the boundary checks. It also reconstructs the three-point result as a crosscheck. It is an internal AI-assisted review, not human peer review, a priority audit, or proof-assistant certification.

The frozen head is `e809a9c40f4ccdaced6f45f10b1dc8b7725a2119`, problem 30000052 / OWR-723-005. The current distributed [PROOF.md](../../inputs/PROOF.md) has 7,682 bytes and SHA-256 `1b37d4296730dfcc7a22e3f5b8d149687357e926058a7ed6de844814da404e58`. The older 7,673-byte proof mentioned in the acceptance history is explicitly a different original edition. I have not conflated their identities. [INPUT_PINS.json](INPUT_PINS.json) independently records all ten current input files. The input manifest's nine entries agree with the current distributed files. No original file was changed.

## 1. Original target and admissible parameters

I freshly retrieved the [official EMS report](https://ems.press/content/serial-article-files/45858), extracted its text, and visually inspected printed pp. 697–699 (physical PDF pages 25–27). Its 445,532 bytes have SHA-256 `2f02cd5834ed1a868d95a20be9d172ade3b35e76caf8c9ff8ab6a3adaf6f3d3e`, matching the recorded source. The source is Erich Novak, reporting joint work with Aicke Hinrichs, *New bounds for the star discrepancy*, Oberwolfach Report 13/2004, pp. 696–699, [DOI](https://doi.org/10.4171/OWR/2004/13). [SOURCE_FETCH.json](SOURCE_FETCH.json) records the fresh retrieval; all source bodies, text and renders remain ignored private files.

Printed p. 697 defines normalized anchored Lp discrepancy and discusses even p. Printed p. 698 asks whether its p-th power averaged over independent continuous generator and shift is at most the iid average. It imposes no rational-generator or primality restriction. Printed p. 699 also asks a separate existence/upper-bound question for selected lattices. The candidate explicitly confines its negative answer to the displayed averaging comparison. This is the correct scope; the argument establishes no negative answer to the separate existence question or to a comparison of expected norms.

For clarity, in dimension one put

\[
 t_j=\{jz+\Delta\},\quad 0\le j<n,
 \qquad D_p(t)^p=\int_0^1\left|\frac1n\sum_{j=0}^{n-1}
 \mathbf1_{[0,x)}(t_j)-x\right|^p\,dx.
\]

The joint density of z and Delta on the unit square is one. Thus integrating over a subregion gives its **unconditional contribution** to the expectation; it must not be divided by the region's area. The points remain indexed, including on exceptional collision parameters.

## 2. Empty tails: complete geometry

Fix n>=3. Apart from its boundary, define

\[
 T_+=\{0<z<1/(n-1),\quad 0<\Delta<1-(n-1)z\}.
\]

For every index 0<=j<n,

\[
 0<\Delta\le\Delta+jz\le\Delta+(n-1)z<1.
\]

Therefore no modular reduction changes any point, and the smallest and largest points are Delta and Delta+(n-1)z. When 0<x<Delta, the empirical count is exactly zero and the discrepancy's fourth power is x^4. When Delta+(n-1)z<x<1, the count is exactly n and its normalized value is one, so the fourth power is (1-x)^4. The intervening integral is nonnegative. Hence

\[
 D_4(t)^4\ge\frac{\Delta^5+
 [1-\Delta-(n-1)z]^5}{5}.
\]

This calculation is where the indexed 1/n normalization matters: on the last empty tail, n/n=1. There is no missing n^-4 factor in this bound.

For the second region write z=1-w and use

\[
 T_-=\{0<w<1/(n-1),\quad (n-1)w<\Delta<1\}.
\]

Since jz+Delta=j+Delta-jw, its fractional part is Delta-jw throughout this region. The points strictly descend, all lie between zero and one, and their extreme values are Delta-(n-1)w and Delta. Their two tail contributions are

\[
 \frac{[\Delta-(n-1)w]^5+(1-\Delta)^5}{5}.
\]

The transformation (z,Delta) -> (1-z,1-Delta) maps the two open triangles to one another, has Jacobian of absolute value one, and exchanges the two tails. Their contributions are equal.

For n>=3 the ascending generator interval is (0,1/(n-1)), and the descending interval is (1-1/(n-1),1). These intervals are disjoint; at n=3 their closures meet at 1/2, but their interiors do not. Consequently there is no double counting. All triangle edges are finite unions of line segments, which have two-dimensional Lebesgue measure zero. Some closed-edge parameters really do cause a wrap, for example Delta+(n-1)z=1; none is silently treated as a nonwrapping interior point. The integral and expectation are unaffected by discarding them.

As an extra boundary control, the full triangles are also disjoint for n=2: then they are separated by Delta=1-z and partition the square up to their boundary. Their **generator projections** overlap in that case, so the n>=3 argument using only generator intervals should not be reused at n=2. The candidate makes no such misuse. Its n>=3 statement suffices.

## 3. Exact integral and all-n consequence

Use a=Delta, b=(n-1)z and c=1-a-b on T+. The image is the unit simplex a,b,c>0 and dz dDelta=da db/(n-1). Thus one triangle contributes

\[
\begin{aligned}
 I_n&=\frac1{5(n-1)}\int_0^1\int_0^{1-b}
          [a^5+(1-a-b)^5]\,da\,db\\
 &=\frac1{15(n-1)}\int_0^1(1-b)^6\,db
 =\frac1{105(n-1)}.
\end{aligned}
\]

The last formula is equivalently obtained by the simplex monomial identity

\[
 \int_{a,b\ge0,\ a+b\le1}a^r b^s\,da\,db
 =\frac{r!s!}{(r+s+2)!}.
\]

Adding the disjoint regions and using nonnegativity elsewhere gives the universal bound

\[
 \boxed{\ \mathbb E D_4(M_n^{z,\Delta})^4
       \ge \frac2{105(n-1)}\quad(n\ge3).\ }
\]

For an additional consistency check, the same tail calculation with any positive even p yields 4/[(p+1)(p+2)(p+3)(n-1)]. No assertion concerning all odd exponents is needed for the source's even-p question.

Here is an independent derivation of the iid comparison. For N~Binomial(n,x), let a=x(1-x). The fourth centered Bernoulli moment is a-3a^2. In a fourth power of a sum of independent centered variables, only the single-index and paired-index terms survive. There are n single-index terms and 3n(n-1) paired terms. Accordingly

\[
 \mathbb E(N/n-x)^4
 =\frac{n(a-3a^2)+3n(n-1)a^2}{n^4}.
\]

Integrating a and a^2 gives 1/6 and 1/30, respectively, so

\[
 J_n:=\mathbb E D_4(M_n^{\rm iid})^4=\frac{3n-1}{30n^3}.
\]

At n=4 the tail lower bound is 2/315, J_4=11/1920, and

\[
 \frac2{315}-\frac{11}{1920}=\frac5{8064}>0.
\]

Thus the n=4 argument alone completely disproves the proposed universal comparison. It does not merely exhibit one exceptional generator, because the integrated triangles have positive measure.

In fact this bound proves strict reversal for **every integer n>=4**. Its ratio to iid is

\[
 \frac{2/[105(n-1)]}{J_n}
 =\frac{4n^3}{7(n-1)(3n-1)}.
\]

The ratio exceeds one exactly when 4n^3-21n^2+28n-7>0. Writing k=n-4 gives the explicit certificate

\[
 4n^3-21n^2+28n-7=4k^3+27k^2+52k+25>0\quad(k\ge0).
\]

The ratio lower bound is asymptotic to 4n/21. Consequently the fourth moment has a lower bound of order 1/n, while the iid fourth moment is asymptotic to 1/(10n^2). This is a **lower-bound comparison**, not a claim that the full lattice moment has an exact 1/n asymptotic, nor a statement about the expected norm. At n=3 the tail bound is 1/105<4/405 and is insufficient; the candidate correctly provides another proof there. The n=2 extension's bound 2/105 is also below its iid value 1/48, as it must be.

## 4. Independent three-point crosscheck

Let u=t_0 and v=t_1. These are independent uniforms and t_2={2v-u}. For 0<=x<=1/2 and 0<=u,v<x, a negative value of 2v-u has fractional part at least 1-x>=x; a nonnegative value is below one off boundary events. Thus triple inclusion is the ordinary strip 0<=2v-u<x inside the x by x square. For each fixed u, its v interval is [u/2,(u+x)/2], of length x/2. Hence q(x)=P(all three<x)=x^2/2.

Every pair is independent, as also proved in the next section. If N is the count and P_k=P(N=k), total probability together with E N=3x, E binom(N,2)=3x^2 and P_3=q gives

\[
 (P_0,P_1,P_2,P_3)=
 (1-3x+\tfrac52x^2,\ 3x-\tfrac92x^2,\ \tfrac32x^2,\ \tfrac12x^2)
\]

on the lower half interval. Substituting these probabilities gives

\[
 F(x):=\mathbb E(N/3-x)^4
 =x^4-\frac{10}{9}x^3+\frac8{27}x^2+\frac{x}{27}.
\]

Replacing (z,Delta) by (-z,-Delta) modulo one preserves its product uniform law and reflects all three points. For each fixed x, endpoint equalities have probability zero, and the centered count changes sign at the reflected endpoint 1-x. Thus F(1-x)=F(x). This is a law statement; no conditioning or assumption of triple independence is used. Bounded measurability permits Tonelli/Fubini, and

\[
 2\int_0^{1/2}F(x)\,dx=\frac{19}{1620}.
\]

The iid formula above gives 4/405. As a direct sign check, the integrand difference on the lower half interval is

\[
 F(x)-F_{\rm iid}(x)=\frac29x^2(1-2x)^2\ge0,
\]

and its doubled integral is 1/540. The ratio of the moments is 19/16. These exact identities corroborate the smaller counterexample without relying on the triangle bound or a numerical estimate.

## 5. Whole-law and second-moment boundary claims

For arbitrary distinct indices j,k, conditional on z the point t_j is a translate of the independent uniform shift. Thus (t_j,z) has product uniform law. Conditional on t_j, z remains uniform; multiplication by the nonzero integer k-j preserves circle measure. Therefore t_k={t_j+(k-j)z} is uniform conditional on t_j. Coordinatewise this proves that every indexed pair is an independent uniform pair in every dimension d. This does not prove independence of triples or larger sets.

For a box [0,x) of volume v=product_r x_r, pairwise independence gives

\[
 \mathbb E\left(\frac1n\sum_j\mathbf1_{[0,x)}(t_j)-v\right)^2
 =\frac{v(1-v)}n.
\]

This is also the iid variance. Since the integrals of v and v^2 over the d-dimensional endpoint cube are 2^-d and 3^-d,

\[
 \boxed{\ \mathbb E D_2(M_n^{z,\Delta})^2
 =\mathbb E D_2(M_n^{\rm iid})^2
 =\frac{2^{-d}-3^{-d}}n\quad(n,d\ge1).\ }
\]

For n=1 the only point is the uniform shift. For n=2 the map from (z,Delta) to (t_0,t_1) has inverse Delta=t_0, z={t_1-t_0}. Conditional uniformity proves product uniform law for the complete ordered pair, in every coordinate. Hence the two ensembles have the same **whole** law for n<=2, and all measurable discrepancy functionals agree whenever their expectations exist. This justifies the smallest-possible-point-count statement. It asserts neither that every exponent fails for n=3 nor that an expected norm comparison follows from a fourth-moment comparison.

Collisions for fixed n,d occur when a nonzero indexed difference times z is integral in each coordinate; these exceptional sets have measure zero. They need not be deleted: indexed normalization always remains 1/n. Likewise every fixed endpoint event t_j=x has probability zero; for a fixed point set the finitely many box endpoints form a null set of x. Closed versus half-open parameter cubes do not change the expectations.

## 6. Exact independently authored verification

[verify_tail.py](verify_tail.py) is newly written for this review and imports no candidate or previous-audit code. It uses only Python's standard library and exact Fraction arithmetic, with explicit exceptions rather than assertions. It has no writable output path: the caller captures its JSON output.

The program checks the simplex monomial expansion and the integrated two-tail formula, all-n polynomial positivity certificate, deterministic modular point coordinates on 1,620 configurations in both triangle interiors including n=2, and lower-tail values against the exact full deterministic discrepancy integral. The ascending-point exclusion from the descending open interior explicitly tests its actual generator `step > 1-1/(n-1)` together with `Delta > (n-1)*(1-step)`, so the diagnostic directly matches its label. It independently recomputes iid moments from the complete binomial sum using integer beta integrals for 1<=n<=64. It reconstructs the n=3 polynomial and margin, tests the exact two-point torus inverse on 289 rational pairs, and checks the linear Fourier kernel used by the pairwise-independence proof on 11,016 controls. The all-parameter assertions are supplied by the proofs above; these finite controls do not by themselves establish continuous independence or universal inequalities.

Each successful run records 57,837 requirement evaluations, including deliberately rejected false identities. Normal and optimized Python runs produce byte-identical JSON files: [normal](CHECK_RESULTS.normal.json), [optimized](CHECK_RESULTS.optimized.json). [RUN_RECEIPT.json](RUN_RECEIPT.json) records the commands, versions, byte equality and explicit forced-failure tests. The 17 adverse controls cover triple independence, the wrong Jacobian, a missing triangle, omitted normalization, extending the lower-half q formula, invalid tail-only inference at n=3, removal of the descending Delta restriction, invalid domains, and substituting a fixed generator for the full average. A separate --force-failure invocation exits nonzero in both modes. No check is disabled by optimization.

The supplementary exact full n=4 value 139/17280 in the inherited audit is not needed for, and is not newly certified by, this tail-family program. This review independently certifies the sufficient n=4 lower bound and every argument in the candidate's standalone proof.

## 7. Outcome and remaining scope

The strict counterexamples, all-n/d p=2 equality, and n<=2 equality of whole ensemble laws all survive the adversarial checks. The n=4 geometric proof alone resolves the displayed comparison negatively, and the exact n=3 computation establishes minimal point count. There is no mathematical concern requiring repair in these claims.

No global priority decision was attempted. No publication-readiness decision, Zenodo action, tracker action, PR mutation, or external communication was performed. This mathematical PASS permits the parent review to proceed to its independent priority stage; it does not certify novelty or external peer review.
