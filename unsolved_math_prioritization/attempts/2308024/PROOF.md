# Character space of a weighted rational completion

## Theorem and scope

Let $X\subset\mathbb C$ be a nonempty compact set. Let $M_n>0$, for $n\geq0$, satisfy

$$
M_0=1,\qquad M_{j+k}\geq {j+k\choose j}M_jM_k,
\qquad \sum_{j=0}^{\infty}\frac{M_j}{M_{j+1}}<\infty.
$$

Let $\mathcal R_X$ be the algebra of rational functions having no pole on $X$, viewed as rational functions (equivalently, their germs near $X$), rather than identifying functions merely because their values on a finite set agree. Define

$$
\|r\|_{X,M}=\sum_{n=0}^{\infty}\frac{\|r^{(n)}\|_X}{M_n}.
$$

This is a finite, submultiplicative norm. The character space of its Banach algebra completion $A$ is canonically homeomorphic to $X$: every nonzero complex-linear multiplicative functional on $A$ is evaluation at a unique point of $X$, extended continuously from $\mathcal R_X$.

The same conclusion holds for any well-defined unital Banach function algebra on $X$ containing these rational functions densely, with continuous point evaluations and the indicated rational norm. No assertion that the abstract completion injects into $C(X)$ is required.

This is an elementary reconstruction of the established rational-density naturality argument, not a novelty claim. For the traditional Dales–Davie rational-closure setting, see Abtahi–Honary, Theorem 4.1 and the beginning of Section 4, and Feinstein–Kamowitz, p.2; the historical attribution in those papers is to Dales–Davie (1973).

## The weight limit

Put $r_j=M_j/M_{j+1}$. For fixed $N\geq0$, write

$$
S_N=\sum_{j=N}^{\infty}r_j,
\qquad C_N=\prod_{j=0}^{N-1}r_j=\frac1{M_N}.
$$

The empty product is one. Since all weights are positive, $S_N>0$; summability gives $S_N\to0$. For $n>N$, the arithmetic–geometric mean inequality gives

$$
\frac1{M_n}=C_N\prod_{j=N}^{n-1}r_j
\leq C_N\left(\frac{S_N}{n-N}\right)^{n-N}.
$$

Consequently,

$$
\left(\frac{n!}{M_n}\right)^{1/n}
\leq C_N^{1/n}S_N^{(n-N)/n}
\frac{(n!)^{1/n}}{(n-N)^{(n-N)/n}}.
$$

For fixed $N$, the final quotient tends to $e^{-1}$. Indeed, Stirling's formula gives $(n!)^{1/n}\sim n/e$, and $(n-N)^{(n-N)/n}/n\to1$. Thus

$$
\limsup_{n\to\infty}\left(\frac{n!}{M_n}\right)^{1/n}
\leq\frac{S_N}{e}.
$$

Letting $N\to\infty$ proves

$$
\boxed{\lim_{n\to\infty}(n!/M_n)^{1/n}=0.}
$$

This argument does not assume log-convexity or monotonicity of the ratios. The binomial weight inequality is not needed for this step.

## Finiteness and definiteness of the norm

Every $r\in\mathcal R_X$ is holomorphic on an open neighborhood of the compact set $X$. Choose $\delta>0$ so that all closed discs of radius $\delta$ centered on $X$ lie inside one compact subset of that neighborhood. If $C$ bounds $|r|$ there, Cauchy's estimate gives

$$
\|r^{(n)}\|_X\leq C n!\delta^{-n}.
$$

The root limit above and the root test show that $\|r\|_{X,M}<\infty$.

In particular, for $\lambda\notin X$ and $d=\operatorname{dist}(\lambda,X)>0$,

$$
s_\lambda(z)=\frac1{z-\lambda}\in\mathcal R_X,
\qquad
\|s_\lambda\|_{X,M}
\leq\frac1d\sum_{n=0}^{\infty}\frac{n!}{M_nd^n}<\infty.
$$

If $\|r\|_{X,M}=0$, choose $x\in X$. Every derivative of $r$ at $x$ is zero. Its Taylor expansion vanishes on a disc, so the rational function is identically zero. This proves definiteness, including when $X$ is finite. Homogeneity and the triangle inequality follow term by term.

The binomial weight inequality and Leibniz's formula give

$$
\frac{\|(fg)^{(n)}\|_X}{M_n}
\leq\sum_{j=0}^{n}
\frac{\|f^{(j)}\|_X}{M_j}
\frac{\|g^{(n-j)}\|_X}{M_{n-j}}.
$$

Summing the nonnegative terms proves $\|fg\|_{X,M}\leq\|f\|_{X,M}\|g\|_{X,M}$. The unit has norm one. Multiplication therefore extends to the completion $A$, making it a commutative unital Banach algebra. The coordinate element $u(z)=z$ is in $\mathcal R_X$, with norm $\|u\|_X+1/M_1$.

## Automatic continuity and identification of the characters

Let $\chi:A\to\mathbb C$ be a nonzero complex-linear multiplicative functional, without initially assuming continuity. Then $\chi(1)=1$. If $|\chi(a)|>\|a\|$, the element $a-\chi(a)1$ is invertible by the norm-convergent Neumann series. Applying $\chi$ to its algebraic inverse identity gives a contradiction. Hence

$$
|\chi(a)|\leq\|a\|\qquad(a\in A).
$$

Thus every such character is continuous, independently of any semisimplicity assumption.

Set $\lambda=\chi(u)$. If $\lambda\notin X$, the finite-norm rational element $s_\lambda$ satisfies

$$
(u-\lambda1)s_\lambda=1.
$$

Applying $\chi$ would give $0=1$. Therefore $\lambda\in X$.

Write an arbitrary $r\in\mathcal R_X$ in reduced form $p/q$, where $q$ has no zero on $X$. Since $1/q\in\mathcal R_X$,

$$
\chi(r)=\frac{p(\lambda)}{q(\lambda)}=r(\lambda).
$$

For $x\in X$, the evaluation $\varepsilon_x(r)=r(x)$ satisfies $|\varepsilon_x(r)|\leq\|r\|_{X,M}$. It therefore has a unique continuous linear extension to $A$; the extension is multiplicative by continuity of multiplication and is nonzero because it takes the unit to one. Since $\chi$ and $\varepsilon_\lambda$ agree on the dense subalgebra $\mathcal R_X$, they agree throughout $A$.

This argument uses rational density and all outside resolvents; it does not assume that polynomials are dense.

The maximal ideal space is understood in the standard equivalent sense of the character space of a commutative complex unital Banach algebra. This identification does not require semisimplicity.

## Topology and the possible radical

The restriction map $\mathcal R_X\to C(X)$ is contractive and thus extends to a continuous algebra homomorphism $J:A\to C(X)$. If $r_k\to a$ in $A$, then $r_k|_X\to J(a)$ uniformly and

$$
\varepsilon_x(a)=J(a)(x).
$$

For each $a\in A$, this is a continuous function of $x$. The map $x\mapsto\varepsilon_x$ is therefore continuous for the weak-star topology on the character space. It is injective because $u$ separates points, and surjective by the preceding argument. A continuous bijection from compact $X$ to this Hausdorff space is a homeomorphism.

In a commutative unital Banach algebra the Jacobson radical is the intersection of the kernels of all characters. Hence the proved character identification gives exactly

$$
\operatorname{rad}A=\ker J.
$$

The kernel need not vanish. For example, take $X=\{0\}$ and $M_n=(n!)^2$. These weights satisfy both hypotheses, since the binomial ratio is the square of the required binomial coefficient and $M_n/M_{n+1}=1/(n+1)^2$. The coordinate element has $\|u\|=1$, but $J(u)=0$. Also $\|u^n\|=1/n!$, so it is a nonzero quasinilpotent element. The sole character is nevertheless $\varepsilon_0$. Thus a statement about the character space does not imply that the completion is a semisimple algebra of value functions on $X$.

## Function algebra and empty set conventions

For an actual Banach function algebra with the stated dense rational subalgebra and continuous point evaluations, the character argument applies directly; its functions are already distinguished by values. In particular, it applies to the norm closure of the rationals inside a complete Dales–Davie algebra on a perfect compact set. It supplies no density theorem for the full Dales–Davie algebra.

The nonempty condition above is solely the unital normed-algebra convention. If one includes $X=\varnothing$, explicitly defines the supremum of each nonnegative derivative modulus over $\varnothing$ to be zero, and takes the quotient by the resulting zero seminorm, the completion is the zero algebra. It has no nonzero characters, so its character space is $\varnothing$, as required. This convention is not implicit in the nonempty proof.

## Sources and attribution

- W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*, arXiv:1809.07200v2, Problem 8.24, PDF pp.196–197, printed pp.195–196. [Versioned primary source](https://arxiv.org/pdf/1809.07200v2). The text explicitly specifies rational approximation in the weighted norm. Its phrase “poles of X” is read as the evident correction “poles off X”.
- M. Abtahi and T. G. Honary, *Properties of certain subalgebras of Dales–Davie algebras*, Glasgow Math. J. 49 (2007), 225–233, particularly pp.226–228 and 231. [Publisher DOI](https://doi.org/10.1017/S0017089507003576). Their rational closure theorem has explicit perfectness and completeness hypotheses; Section 4 attributes the nonanalytic case to Dales–Davie.
- J. F. Feinstein and H. Kamowitz, *Compact homomorphisms between Dales–Davie algebras*, author version, pp.1–2. [Author PDF](https://www.maths.nottingham.ac.uk/plp/pmzjff/Papers/pdf/FK4.pdf). It records rational-density naturality in the nonanalytic case.
- H. G. Dales and A. M. Davie, *Quasianalytic Banach function algebras*, J. Functional Analysis 13 (1973), 28–50. [DOI](https://doi.org/10.1016/0022-1236(73)90065-7). Historical attribution here is verified through the preceding two papers; the 1973 full text was not inspected for this audit.

## Review status

This proof and the separate mathematical audit are AI-assisted. They have not undergone external human peer review and are not formally certified or verified by a proof assistant. Acceptance here records the stated AI-assisted mathematical audit verdict, not journal acceptance. No novelty or priority is claimed. [ACCEPTANCE.json](ACCEPTANCE.json) binds the verdict to this exact proof, the [audit report](ACCEPTANCE_REPORT.md), and the source metadata.
