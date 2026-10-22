# Constructive quasi-isometry search for Kourovka 21.145

Author of this research notebook: independent work in Alec Kriebel's project (ORCID https://orcid.org/0009-0001-9320-500X).

## Scope and success criteria

The two targets are (a) a quasi-isometry between the finitely generated group $F$ and $F\times\mathbb Z$, and (b) a quasi-isometry between $F$ and $F\times F$. The product metric here is the sum of standard word metrics. A successful construction must give a well-defined map, uniform two-sided distance bounds, and a uniform coarse-surjectivity radius. A product subgroup embedding alone cannot settle either question.

This notebook deliberately develops explicit constructions before consulting any other approach team's verdicts. It records only this route. No external communication, branch changes, commits, or pushes were made by its author.

## 2026-10-17 20:49 UTC checkpoint

Discovery completion estimate: **5%** for each target. Status: no quasi-isometry construction established.

Primary references checked:

* [Cleary–Taback, *Geometric quasi-isometric embeddings into Thompson's group F*, NYJM 9 (2003), 141–148](https://nyjm.albany.edu/j/2003/9-11p.pdf): Theorem 2.1 gives $N(w)-2\le |w|\le4N(w)-4$ for reduced tree pairs, and Theorem 3.4 gives product subgroup embeddings. Their introduction explicitly discusses Bridson's $F\times\mathbb Z$ question. These are embeddings, not a coarse-surjectivity assertion.
* [Belk–Brown, *Forest diagrams for elements of Thompson's group F*](https://pi.math.cornell.edu/~kbrown/papers/Forest.pdf): Theorem 4.2.2 expresses word length as caret count plus weights on spaces. This makes pointer normalization plausible, but it supplies no product metric estimate for such a normalization.
* [Burillo–Cleary–Stein, *Metrics and embeddings of generalizations of Thompson's group F*](https://arxiv.org/abs/math/9809185): reduced tree size is comparable to word length. No additional metric equivalence is assumed below.

## Conventions for checkable constructions

Multiplication is composition, $fg=f\circ g$. Set

$$x_0(t)=\begin{cases}t/2&0\le t\le1/2,\\t-1/4&1/2\le t\le3/4,\\2t-1&3/4\le t\le1,\end{cases}$$

and let $x_1$ be the right-half clone of $x_0$: identity on $[0,1/2]$, and $x_1(t)=1/2+x_0(2t-1)/2$ on $[1/2,1]$. These are the usual two generators up to the standard composition convention.

Write $L(f)=f\oplus1$ and $R(f)=1\oplus f$ for left/right affine clones. The map

$$J_2:F\times F\longrightarrow F,\qquad J_2(a,b)=a\oplus b$$

has image $H=\operatorname{Stab}_F(1/2)$. The map

$$J_1:F\times\mathbb Z\longrightarrow F,\qquad J_1(a,n)=a\oplus x_0^n$$

is likewise an injection; its image is a subgroup of $H$. Both are the familiar product embedding mechanism, not a new result.

## Construction family A: fixed root splitting

**Mechanism.** Split a reduced tree pair at the root; read its two subpairs as coordinates in $F\times F$. Equivalently, use $J_2^{-1}$.

**Exact gap.** This is defined directly only on $H$. In a general tree pair, source and target left subtrees need not have the same number of leaves. Refinement cannot repair the underlying obstruction $f(1/2)\ne1/2$. Treating every pair as two independent subpairs is therefore not a map on all of $F$.

**Quantitative failure of coarse surjectivity.** For an interior dyadic rational $q$, write $\delta(q)$ for its reduced denominator exponent: $q=m/2^{\delta(q)}$, $m$ odd. Directly from the displayed generators and their inverses,

$$\delta(s(q))\le\delta(q)+1\quad(s\in\{x_0^{\pm1},x_1^{\pm1}\}).$$

For depths at least three this follows immediately from slope/intercept formulas; the finitely many dyadics of depths one and two are checked separately. Consequently a word of length $r$ sends $1/2$ to a dyadic of depth at most $r+1$.

For $g_n=x_0^{-n}$ and every $h\in H$, the element $u=g_n^{-1}h=x_0^n h$ satisfies

$$u(1/2)=2^{-(n+1)},\qquad |u|\ge n.$$

Taking $h=1$ gives the reverse inequality, so

$$\boxed{d_F(x_0^{-n},H)=n.}$$

Thus neither fixed-block product embedding is coarsely onto. The same ray also rules out any proposed image contained in this fixed point stabilizer. This is an elementary rejection certificate, not an obstruction to arbitrary nonhomomorphic quasi-isometries.

## Construction family B: Cantor–Bernstein / Hilbert-hotel absorption

**Mechanism.** There are injections both ways: $I_2(f)=(f,1)$ and $J_2$ for the square, or $I_1(f)=(f,0)$ and $J_1$ for the cyclic product. Since $J_iI_i=L$, apply the ordinary set-theoretic Cantor–Bernstein construction and hope it respects distance.

For either target $Y_i$, define

$$A_0=F\setminus J_i(Y_i),\qquad A_{k+1}=L(A_k),\qquad A=\bigcup_{k\ge0}A_k,$$

and the actual bijection

$$B_i(f)=\begin{cases}I_i(f)&f\in A,\\J_i^{-1}(f)&f\notin A.\end{cases}$$

The second branch is defined because $f\notin A_0$ implies $f\in J_i(Y_i)$. The standard disjoint-chain argument establishes bijectivity. This is a concrete globally onto candidate, unlike a bare product embedding.

**Falsification, with exact distances.** Let $h_n=x_1^n=R(x_0^n)$, $n\ge1$, and $f_n=h_nx_0$. Then $d_F(h_n,f_n)=1$. The element $h_n$ lies in $J_i(Y_i)$, while every $A_k$ with $k\ge1$ is supported in $[0,2^{-k}]$. Since $h_n$ has nontrivial support in the right half, $h_n\notin A$. Meanwhile

$$f_n(1/2)=h_n(1/4)=1/4,$$

so $f_n\notin H$, hence $f_n\in A_0$. Therefore

$$B_2(h_n)=(1,x_0^n),\quad B_2(f_n)=(x_1^nx_0,1),$$

and

$$B_1(h_n)=(1,n),\quad B_1(f_n)=(x_1^nx_0,0).$$

The right endpoint slope character $\chi(f)=\log_2 f'(1^-)$ takes both generators to $1$, so it is $1$-Lipschitz for word length. It proves $|x_0^n|=n$ and $|x_1^nx_0|=n+1$, matching the displayed words. Thus for **both** candidates,

$$\boxed{d_{Y_i}(B_i(h_n),B_i(f_n))=2n+1\quad\text{while}\quad d_F(h_n,f_n)=1.}$$

**Status: blocked.** The canonical Cantor–Bernstein bijection is not even bornologous. Mutual undistorted embeddings do not license this gluing. Reopening requires a materially new construction that smooths these partition boundaries uniformly; relabeling the existing copies gives no progress.

## Pending independent construction families

1. Endpoint-height / forest-pointer normalization: factor $f=kx_0^n$ by an endpoint character and compare with a product metric. Uniform conjugation bounds must be checked, not inferred from element sizes.
2. Moving-cut splitting: choose a transporter taking $1/2$ to $f(1/2)$, then split. Need uniform control of the section cocycle under multiplication by each generator, and an account of the entire dyadic orbit coordinate.
3. Variable-depth cloning or recursive binary redistribution: any candidate must survive the adjacent pair $x_1^n,x_1^nx_0$ above and must not erase unbounded motion of the cut.
