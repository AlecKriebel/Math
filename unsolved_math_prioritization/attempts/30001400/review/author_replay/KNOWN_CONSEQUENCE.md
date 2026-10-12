# Fixed-dimensional multiple-copy closure follows from a published majorization theorem

**Status:** Complete credited consequence of an existing published theorem; separate adversarial source/proof review is pending. No historical-priority or new-discovery claim is made. One validation/reduction family is recorded.

## 1. The precise closure question

Fix \(d\ge1\) and positive probability vectors \(x,y\in\mathbb R^d\). Write \(a\prec b\) for ordinary majorization, with \(a\) the more mixed vector. Write
\[
 x\prec_M y\quad\Longleftrightarrow\quad
 x^{\otimes n}\prec y^{\otimes n}\text{ for some integer }n\ge1,
\]
and \(x\prec_Cy\) when \(x\otimes z\prec y\otimes z\) for a finite probability catalyst \(z\). For real \(p\), put \(N_p(x)=\sum_i x_i^p\).

The original contribution [1, pp. 2999–3001] asks whether the following three conditions characterize the closure of the multiple-copy order **with every approximating vector still in the same dimension d**:
\[
\begin{aligned}
 N_p(x)&\le N_p(y) &&(p\ge1),\\
 N_p(x)&\ge N_p(y) &&(0\le p\le1),\\
 N_p(x)&\le N_p(y) &&(p\le0).
\end{aligned}
\tag{1}
\]
The answer is **yes**, as a consequence of Mu–Pomatto–Strack–Tamuz [2, published online supplement, Proposition 8].

**Theorem.** Conditions (1) are equivalent to the existence of positive probability vectors \(x_k\in\mathbb R^d\), with \(\|x_k-x\|_1\to0\), such that \(x_k\prec_M y\) for every k. If x is nonuniform, the explicit perturbations
\[
 x_\varepsilon=(1-\varepsilon)x+\varepsilon u_d,
 \qquad u_d=(1/d,\ldots,1/d),\quad0<\varepsilon<1,
\tag{2}
\]
have the stronger property that, for each fixed \(\varepsilon\),
\[
 x_\varepsilon^{\otimes n}\prec y^{\otimes n}
 \quad\text{for every sufficiently large }n.
\tag{3}
\]
The threshold in (3) may depend on \(\varepsilon,x,y\); no uniform threshold is asserted.

The source already had closure theorems allowing dimension d+1, or unbounded dimension, with fewer power-sum conditions. Neither is used as a replacement for the fixed-dimension question here. The original catalytic fixed-dimension closure characterization is credited to Turgut in [1].

## 2. The exact later theorem being used

For a positive probability vector a define, using natural logarithms,
\[
 H_a(p)=\frac{\log N_p(a)}{1-p}\quad(p\ne1),\qquad
 H_a(1)=-\sum_i a_i\log a_i.
\]
The endpoint and derivative conventions are
\[
 H_a(0)=\log d,\quad H_a(+\infty)=-\log\max_i a_i,\quad
 H_a(-\infty)=-\log\min_i a_i,
\]
\[
 H_a'(0)=\log d+\frac1d\sum_i\log a_i.
\tag{4}
\]
The derivative is with respect to p. Positivity makes these expressions finite and the derivative well-defined.

Mu–Pomatto–Strack–Tamuz, *From Blackwell Dominance in Large Samples to Rényi Divergences and Back Again*, Econometrica 89 (2021), 475–506, prove in **Proposition 8 of the published supplement, Section L, pp. 18–19**:

For equal finite support sizes and unequal maxima and minima, the conditions
\[
\begin{aligned}
 H_\mu(p)&<H_\nu(p) &&(0<p\le+\infty),\\
 H_\mu(p)&>H_\nu(p) &&(-\infty\le p<0),\\
 H_\mu'(0)&<H_\nu'(0)
\end{aligned}
\tag{5}
\]
are equivalent to \(\mu^{\otimes n}\) majorizing \(\nu^{\otimes n}\) for every sufficiently large n. In the notation of this package, that conclusion is \(\nu^{\otimes n}\prec\mu^{\otimes n}\).

The full published main article and supplement were recovered, and the exact proposition, its proof, and the supporting main Theorem 1 were read. This is a use of a credited published theorem, not a claim to have reconstructed all of its large-deviation proof independently. The same proposition appears in the full author manuscript on pp. 56–57.

Two conditions must not be omitted: the derivative inequality at zero and the strict extreme-coordinate comparisons that ensure the theorem's genericity hypothesis. Merely invoking a positive-order Rényi rate formula, or merely replacing strict inequalities by weak ones in this theorem, would not prove the required statement. The perturbation below supplies every missing strict inequality.

## 3. Necessity of the power-sum inequalities

If \(a^{\otimes n}\prec y^{\otimes n}\), convexity of \(s\mapsto s^p\) for \(p<0\) or \(p>1\), and concavity for \(0<p<1\), give the corresponding inequalities for the power sums of the tensor products. Since
\[
 N_p(a^{\otimes n})=N_p(a)^n>0,
\]
taking n-th roots gives (1) for a. At p=0 and p=1 equality follows from the common dimension and normalization. Convexity can be applied directly to a bistochastic matrix representing majorization; no catalyst or limit theorem is needed.

Now let \(x_k\to x\) in the fixed dimension, with \(x_k\prec_My\). For each fixed real p, positivity of x makes \(N_p\) continuous near x. Passing to the limit yields (1). If one instead permits zero entries in the approximants' convention, they cannot occur here: the last majorization inequality forces \(\min(x_k)^{n_k}\ge\min(y)^{n_k}>0\).

## 4. A fixed-dimensional perturbation supplies all strict conditions

Assume (1). Taking logarithms and dividing by \(1-p\), with the correct sign, gives
\[
 H_x(p)\ge H_y(p)\quad(p>0),\qquad
 H_x(p)\le H_y(p)\quad(p<0).
\tag{6}
\]
The p=1 value follows by continuity. Taking p to positive or negative infinity also gives
\[
 \max x\le\max y,\qquad\min x\ge\min y.
\tag{7}
\]
At p=0 both entropies equal \(\log d\). The nonnegative difference in (6) for positive p implies its right derivative is nonnegative; analyticity near zero therefore yields
\[
 H_x'(0)\ge H_y'(0).
\tag{8}
\]

If x is uniform, then \(x\prec y\) already, so the constant sequence \(x_k=x\) proves the assertion. This includes d=1. Indeed the top k coordinates of a decreasing probability vector y have sum at least k/d.

Suppose now that x is nonuniform. Fix \(0<\varepsilon<1\) and use (2). For \(p>1\) or \(p<0\), strict convexity gives \(N_p(u_d)<N_p(x)\), and hence
\[
 N_p(x_\varepsilon)
 \le(1-\varepsilon)N_p(x)+\varepsilon N_p(u_d)<N_p(x).
\]
For \(0<p<1\), strict concavity reverses these two inequalities. Consequently
\[
 H_{x_\varepsilon}(p)>H_x(p)\quad(0<p<\infty),\qquad
 H_{x_\varepsilon}(p)<H_x(p)\quad(-\infty<p<0).
\tag{9}
\]
At p=1 the first assertion uses the same argument for the strictly concave Shannon entropy. Strict concavity of \(\log\), summed over coordinates, gives
\[
 \sum_i\log(x_\varepsilon)_i>\sum_i\log x_i,
 \qquad H_{x_\varepsilon}'(0)>H_x'(0).
\tag{10}
\]
Finally, nonuniformity implies \(\max x>1/d>\min x\), so
\[
\begin{aligned}
 \max x_\varepsilon&=(1-\varepsilon)\max x+\varepsilon/d<\max x\le\max y,\\
 \min x_\varepsilon&=(1-\varepsilon)\min x+\varepsilon/d>\min x\ge\min y.
\end{aligned}
\tag{11}
\]
Thus the strict comparisons extend to both infinite endpoints, and both extreme-coordinate genericity conditions hold.

Apply the published proposition with **\(\mu=y\), \(\nu=x_\varepsilon\)**. Equations (6), (8), (9), (10), and (11) give every condition in (5), in the correct direction. Both vectors have the same support size d, and all coordinates are positive. The conclusion is exactly (3).

Take \(\varepsilon_k=1/(k+1)\). All \(x_k=x_{\varepsilon_k}\) stay in \(\mathbb R^d\), satisfy \(x_k\prec_My\), and obey
\[
 \|x_k-x\|_1=\varepsilon_k\|u_d-x\|_1\longrightarrow0.
\]
This proves sufficiency and the theorem. \(\square\)

## 5. A check on the probability-experiment translation

For completeness, the published proposition associates to a positive vector a the binary experiment with distributions a and \(u_d\). With \(D_\alpha\) denoting Rényi divergence, direct substitution gives
\[
 D_p(a\|u_d)=\log d-H_a(p)\quad(p>0),
\]
\[
 D_{1-p}(u_d\|a)
 =\frac{1-p}{p}\bigl(\log d-H_a(p)\bigr)\quad(p<0),
 \qquad D_1(u_d\|a)=-H_a'(0).
\tag{12}
\]
Thus (5) compares both states' divergences, including the order-one value in the reversed experiment. The extreme log-likelihood ratios are \(\log(d\max a)\) and \(\log(d\min a)\); (11) supplies their strict separation. On n copies the two experiments still have equal finite cardinality \(d^n\). A stochastic channel preserving the uniform distribution on that cardinality is bistochastic, so Blackwell dominance gives ordinary majorization with the orientation used above. This explains why neither a support-size change nor an omitted negative-order condition is harmless.

The unperturbed equal-max/min boundary cases need not satisfy the generic theorem directly. The proof does not apply it there. It applies it separately to every positive uniform perturbation, which is precisely what the requested closure permits.

## 6. Attribution and limits

This is a fixed-dimensional closure consequence of the published 2021 theorem, with an elementary smoothing argument. The underlying eventual-majorization theorem and all difficult large-sample analysis are credited to Mu, Pomatto, Strack, and Tamuz. The earlier catalytic and dimension-changing closure results remain credited to Turgut and Aubrun–Nechita. Whether this exact corollary was separately recorded earlier was not established, so no priority claim is made.

The full final main paper and published supplement were obtained. The supplement contains a prose slip saying that \(H_\mu(0)\) is the support size; its displayed definition gives the logarithm of that size, as in (4). Equality of support sizes and every formula used in Proposition 8 are unaffected. This package consistently uses \(H_a(0)=\log d\).

Finite exact controls check the perturbation, tensor power sums, bistochastic orientation, and endpoint algebra. They do not replace the published eventual-majorization theorem or verify an unbounded continuum of orders by sampling. No effective copy bound, exact unperturbed equivalence between catalytic and multiple-copy orders, or new discovery is claimed.

## References

1. Guillaume Aubrun, *Entanglement Catalysis*, Oberwolfach Report 56/2009, pp. 2999–3001, Theorems 1–3 and the following question. [Full original report](https://ems.press/content/serial-article-files/46257), DOI [10.4171/OWR/2009/56](https://doi.org/10.4171/OWR/2009/56).
2. Xiaosheng Mu, Luciano Pomatto, Philipp Strack, and Omer Tamuz, *From Blackwell Dominance in Large Samples to Rényi Divergences and Back Again*, Econometrica 89 (2021), 475–506. DOI [10.3982/ECTA17548](https://doi.org/10.3982/ECTA17548). [Published main text](https://par.nsf.gov/servlets/purl/10292858); [published supplement, Section L, Proposition 8, pp. 18–19](https://www.econometricsociety.org/publications/econometrica/2021/01/01/blackwell-dominance-large-samples-r%C3%A9nyi-divergences-and-back/supp/ecta200239-sup-0001-onlineappendix.pdf); [complete author manuscript](https://tamuz.caltech.edu/papers/law_order.pdf).
3. Asger Kjærulff Jensen, *Asymptotic Majorization of Finite Probability Distributions*, IEEE Trans. Inf. Theory 65 (2019), 8131–8139, DOI [10.1109/TIT.2019.2922627](https://doi.org/10.1109/TIT.2019.2922627), [primary preprint](https://arxiv.org/abs/1808.05157). Its unequal-support/rate result alone is not the fixed-dimension conclusion needed here; the later supplement expressly treats the missing equal-support case.
