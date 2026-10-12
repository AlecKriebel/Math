# The missing boundary range in the printed Dyck-path formula

## Result and scope

The inequality system printed in Conjecture 1 of Valentina Kiritchenko's contribution to Oberwolfach Report 46/2019, p. 2895, does not define the asserted Newton-Okounkov body when (n=2). The defect is in the literal boundary range. This observation does not disprove an intended corrected conjecture, and it does not supply a full corrected formula in higher rank.

The relevant source is the [official Oberwolfach PDF](https://ems.press/content/serial-article-files/46825), PDF page 27, printed p. 2895. Its range and superscripts/subscripts were checked in a rendered page, rather than inferred from text extraction alone.

## 1. What the printed system says in the smallest rank

In the source notation the weight at stage (r) is

\[
\Lambda_r=(\lambda_r^r,\ldots,\lambda_n^r).
\]

The source pads the missing earlier entries by \(\lambda_a^b=\lambda_b^b\) for \(a<b\). It uses coordinates \(u_m^l\), with \(l,m\geq1\) and \(l+m\leq n\). Besides their nonnegativity, the displayed path inequalities are

\[
\sum_{(l,m)\in D}u_m^l
\leq \sum_{s=1}^{j}(\lambda_k^s-\lambda_{i+j}^s),
\qquad 1<k\leq j<n,\quad 1\leq i\leq n-j,
\]

where the endpoint is \(u_j^i\).

Set \(n=2\). There is exactly one coordinate, \(x=u_1^1\). There are no integers \(k,j\) satisfying \(1<k\leq j<2\): the last inequality forces \(j\leq1\), whereas the first two force \(j\geq2\). Thus no upper inequality is present, regardless of how the paths themselves are defined. The literal solution set is

\[
P_{\mathrm{printed}}=\{x\in\mathbb R:x\geq0\}=[0,\infty).
\]

## 2. The actual variety, line bundle, and valuation

The notation imported from [Kiritchenko, arXiv:1801.00334v1](https://arxiv.org/abs/1801.00334v1), Sections 2.1-2.2, takes \(G=GL_n(\mathbb C)\) and the word

\[
(s_1)(s_2s_1)\cdots(s_{n-1}\cdots s_1).
\]

For \(n=2\) the word is \((s_1)\). Its Bott-Samelson variety is the single projective-line fiber over a point, hence

\[
X_{\overline w_0}=R_{(1)}\cong GL_2/B_2\cong\mathbb P^1.
\]

Use a dominant weight \(\Lambda_1=(a,b)\), with \(a\geq b\), and put \(d=a-b\). In the source's positive line-bundle convention, \(L_{\Lambda_1}\cong\mathcal O_{\mathbb P^1}(d)\). In particular, \((a,b)=(1,0)\) gives \(\mathcal O(1)\), which is very ample. This sign and degree convention is checked independently in [Brion, Lectures on the geometry of flag varieties](https://arxiv.org/abs/math/0410240v1), Proposition 1.4.3 and the paragraph following Definition 1.4.4 (printed/PDF pp. 16-17): the first fundamental weight gives the Plucker pullback of \(\mathcal O(1)\), and degrees on a simple Schubert curve are weight differences.

In dimension one the source's lowest-term valuation \(v_0\) is order of vanishing at its translated Schubert point \(p\). Choose homogeneous coordinates \([X:Y]\) with \(p=[1:0]\), local coordinate \(t=Y/X\), and normalizing section \(s_0=X^d\), which is nonzero at \(p\).

## 3. Direct computation, without a general Minkowski-sum theorem

For every integer \(m\geq1\), a nonzero section of \(\mathcal O(md)\), divided by \(s_0^m=X^{md}\), is a nonzero polynomial in \(t\) of degree at most \(md\). Its valuation is its smallest occurring exponent. Therefore

\[
\{v_0(s/s_0^m):0\ne s\in H^0(\mathbb P^1,\mathcal O(md))\}
=\{0,1,\ldots,md\}.
\]

Both inclusions are explicit: a polynomial of degree at most \(md\) cannot vanish to higher order; and the section \(X^{md-r}Y^r\) has valuation \(r\) for every \(0\leq r\leq md\). The Newton-Okounkov body is consequently

\[
\overline{\operatorname{conv}}\!\left(
\bigcup_{m\geq1}\{0,1/m,\ldots,md/m\}\right)=[0,d].
\]

The containment in \([0,d]\) and the presence of its two endpoints already prove the equality. For \(d=1\), the actual body is \([0,1]\). The point \(2\) belongs to the printed half-line and not to this body, establishing the literal failure.

A different normalizing section translates this bounded interval. It cannot turn it into an unbounded half-line. Thus the normalization issue does not rescue the printed system.

## 4. The limited repair certified here

Replacing the strict lower endpoint \(1<k\) by \(1\leq k\) would include \(i=j=k=1\) when \(n=2\). The corresponding one-coordinate path bound is

\[
0\leq u_1^1\leq\lambda_1^1-\lambda_2^1,
\]

which is exactly the interval computed above. This certifies the missing rank-one boundary inequality. It does not certify that this single typographic change is sufficient in arbitrary rank. The equality of any proposed repaired higher-rank path system with the intended Newton-Okounkov body remains a separate mathematical question.
