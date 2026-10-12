# The sharp convexity radius in Hayman Problem 6.22

**2306022 / AMR-022-6022. Known result; source-status correction.**

The exact universal radius is

$$R=\sqrt{2\sqrt3-3}=0.6812500386\ldots.$$

This is a classical result, attributed to Thomas H. MacGregor (1963, Theorem 1) in current primary literature. The full published Singh–Goel paper (1971, Theorem 4.2) independently supplies the same sharp result. The proof below is a self-contained specialization of the classical Schwarz–Pick method, not a new discovery. Separate adversarial review is pending.

## 1. Exact source and historical scope

[Hayman–Lingham, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed pp. 122–123, Problem 6.22 asks for the convexity radius of normalized univalent functions in the unit disk $\mathbb D$ satisfying

$$\operatorname{Re}\frac{zf'(z)}{f(z)}\ge\frac12,
\qquad f(0)=0,\quad f'(0)=1.$$

Equivalently, for a holomorphic $P$ with $P(0)=1$ and $\operatorname{Re}P>0$, it asks when the real part of

$$\frac{P(z)+1}{2}+\frac{zP'(z)}{P(z)+1}$$

is positive throughout a circle $|z|=r$. The 2018 update says that no progress had been reported to the editors. That editorial report does not establish that the problem was then unresolved.

The radius here is the largest **uniform** radius for the entire stated class. Individual functions can have a larger radius; for example, $f(z)=z$ is convex throughout $\mathbb D$.

The historical evidence is as follows.

1. Thomas H. MacGregor, *The radius of convexity for starlike functions of order $1/2$*, Proceedings of the American Mathematical Society **14** (1963), 71–76, [DOI](https://doi.org/10.1090/S0002-9939-1963-0150282-6). The title and publication details are corroborated by the [journal issue record](https://www.jstor.org/stable/i335921). The full 1963 paper was **not retrieved** in this audit, so a line-by-line verification of that paper is not claimed.
2. V. Singh and R. M. Goel, *On radii of convexity and starlikeness of some classes of functions*, Journal of the Mathematical Society of Japan **23** (1971), 323–339. The [full published paper](https://www.jstage.jst.go.jp/article/jmath1948/23/2/23_2_323/_pdf) was retrieved. Its definition (1.1) is exactly the normalized class starlike of order $\beta$. Theorem 4.2, pp. 330–331, gives the sharp radius. At $\beta=1/2$, its equation (4.9) becomes
   $$-\tfrac12(r^4+6r^2-3)=0,$$
   and its formula (4.11) gives $R^2=2\sqrt3-3$. Its extremal (4.6) becomes $z(1-2az+z^2)^{-1/2}$, the family used below. The relevant derivative estimate is its Lemma 2, p. 325. The proof below verifies the needed specialization directly rather than importing the general-order optimization.
3. B. Bhowmik and S. Biswas, [arXiv:2606.20872v1](https://arxiv.org/abs/2606.20872v1), submitted 18 June 2026, p. 3, explicitly uses this exact radius and attributes it to MacGregor's Theorem 1, reference [11]. That paper studies a different convolution problem. Its new convolution assertions are not dependencies here, and no journal publication is claimed for it.

Thus the imported open-status classification should be corrected to **already_solved**, with classical attribution. The earlier campaign's Problem 6.64 concerns coefficient sufficient conditions for alpha-convexity and is a distinct target; none of its results are needed below.

## 2. The theorem

Let $f$ satisfy the source hypotheses. Then $f$ maps $\{z:|z|<R\}$ conformally onto a convex domain. No larger radius has this property for every such $f$.

More precisely, every admissible $f$ satisfies

$$\operatorname{Re}\left(1+\frac{zf''(z)}{f'(z)}\right)>0
\qquad (|z|<R).\tag{1}$$

For the extremal function in Section 4, equality occurs at the real point $z=R$, and the expression is negative at real points immediately beyond $R$.

We use the classical analytic criteria for normalized starlike and convex maps: positivity of $\operatorname{Re}(zf'/f)$ implies starlikeness and univalence, and a locally univalent normalized map is convex on a disk exactly when $\operatorname{Re}(1+zf''/f')>0$ there. These criteria also underlie the source's stated equivalence.

## 3. Universal lower bound

Put $q=zf'/f$, with the removable value $q(0)=1$. Univalence ensures that $f$ has no other zero and $f'$ has no zero. The harmonic minimum principle upgrades $\operatorname{Re}q\ge1/2$ to strict inequality, since $q(0)=1$. Therefore

$$w=1-\frac1q=\frac{P-1}{P+1}$$

is a holomorphic map from $\mathbb D$ into itself, with $w(0)=0$, and

$$q=\frac1{1-w},\qquad
1+\frac{zf''}{f'}=q+\frac{zq'}q
=\frac{1+zw'}{1-w}.\tag{2}$$

Fix $z\ne0$, write $r=|z|$ and $\rho=|w(z)|\le r$. Schwarz–Pick applied to the holomorphic function $w(\zeta)/\zeta$ gives

$$|zw'(z)-w(z)|\le\frac{r^2-\rho^2}{1-r^2}.\tag{3}$$

The possible constant unimodular case of $w(\zeta)/\zeta$ satisfies (3) with both sides zero. Thus (3) needs no strict self-map qualification for that quotient.

Writing $\delta=zw'-w$ in (2), and using $|1-w|\le1+\rho$, gives

$$\begin{aligned}
\operatorname{Re}\frac{1+zw'}{1-w}
&=\frac{1-\rho^2}{|1-w|^2}
  +\operatorname{Re}\frac\delta{1-w}\\
&\ge\frac{(1-r^2)(1-\rho^2)-(r^2-\rho^2)|1-w|}
{(1-r^2)|1-w|^2}\\
&\ge\frac{(1+\rho)\bigl[\rho^2-(1-r^2)\rho+1-2r^2\bigr]}
{(1-r^2)|1-w|^2}.\tag{4}
\end{aligned}$$

All denominators are positive. The remaining quadratic has the exact decomposition

$$\rho^2-(1-r^2)\rho+1-2r^2
=\left(\rho-\frac{1-r^2}{2}\right)^2
 +\frac{3-6r^2-r^4}{4}.\tag{5}$$

The last term is positive for $0\le r<R$, because $R$ is the unique positive solution of $r^4+6r^2-3=0$. This proves (1) for nonzero $z$; its value at zero is $1$. In particular, for every $r<R$ the real part has a positive minimum on the compact circle $|z|=r$, exactly as requested in the source.

## 4. Sharpness and an admissible extremal

Set

$$\rho_*=2-\sqrt3,\qquad
 a=\frac{\rho_*}{R}=\sqrt{\frac2{\sqrt3}-1},\qquad 0<a<1.$$

Define

$$f_*(z)=\frac{z}{\sqrt{1-2az+z^2}},\tag{6}$$

where the analytic square root is chosen to be $1$ at zero. The two zeros of the quadratic are $a\pm i\sqrt{1-a^2}$, both on the unit circle, so this branch is well-defined and nonzero throughout $\mathbb D$. Hence $f_*$ is holomorphic and normalized. Direct differentiation gives

$$\frac{zf_*'(z)}{f_*(z)}
=\frac{1-az}{1-2az+z^2}
=\frac1{1-w_*(z)},
\qquad
w_*(z)=\frac{z(a-z)}{1-az}.\tag{7}$$

The factor $(a-z)/(1-az)$ is a disk automorphism, so $|w_*(z)|<1$ for $z\in\mathbb D$. The identity

$$\operatorname{Re}\frac1{1-w}-\frac12
=\frac{1-|w|^2}{2|1-w|^2}>0$$

shows that $f_*$ is starlike of order $1/2$, and in particular is univalent. This verifies every source hypothesis, not just the derivative at the proposed extremum.

One further differentiation gives

$$1+\frac{zf_*''(z)}{f_*'(z)}
=\frac{B(z)}{(1-az)(1-2az+z^2)},
\qquad B(z)=1-az+(a^2-2)z^2+az^3.\tag{8}$$

Using $aR=\rho_*$, $R^2=1-2\rho_*$ and $\rho_*^2-4\rho_*+1=0$, we obtain

$$B(R)=0,\qquad R B'(R)=-6\rho_*<0.\tag{9}$$

For real $0<z<1$ the denominator in (8) is positive: $1-az>0$ and $1-2az+z^2=(z-a)^2+1-a^2>0$. Consequently (8) is negative at all real points in some interval immediately to the right of $R$. Every larger disk contains such a point, and $f_*$ is not convex on that disk.

This proves sharpness and completes the exact source problem. The boundary value zero does not contradict convexity on the open disk $|z|<R$.

## 5. Verification and limits of the audit

`python verify.py` uses exact SymPy algebra and rational controls to check the change of variables, derivative estimate identities, completed square, extremal normalization, boundary zero, negative derivative, and specialization of Singh–Goel's published formula. Finite controls support the written proof; they do not replace its all-function argument.

The historical conclusion is credited known mathematics. The 1963 full text remains an access limitation; the full 1971 primary theorem, its relevant proof ingredients, the direct specialization above, and the 2026 explicit attribution are available. No new result, historical-priority claim, official correction to the source, or human peer review is asserted.
