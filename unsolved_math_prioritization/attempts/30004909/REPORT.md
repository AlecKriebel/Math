# A same-ground-set matroid-rank obstruction

Problem 30004909 / OWR-8415356-020. Mathematical verification completed 9 October 2026.

## Result and scope

There is no dimension-independent constant for the two-sided approximation by a single ordinary matroid rank function in the displayed formulation of László Végh's question in Oberwolfach Report 53/2021, printed p. 2946 (PDF page 54). The elementary family

\[
f_n(S)=\sqrt{|S|},\qquad S\subseteq [n],
\]

forces any admissible approximation factor to satisfy \(\alpha\ge n^{1/6}\). This already answers the universal-constant question negatively. A rational-valued family below gives the stronger lower bound \(\alpha\ge n^{1/4}/\sqrt2\) along square ground-set sizes, by the same basis/full-set argument.

The constant is required to be independent of both the function and the finite ground-set size. The approximant is the rank of one matroid on that same ground set. No claim is made about approximation by sums of ranks, weighted ranks, an expanded ground set, or a different intended question. This is an independently checked argument for the displayed formulation, not a claim of research priority or of a new literature discovery.

## 1. Precise target

The property being disproved is

\[
\exists\alpha>0\ \forall\text{ finite }V\ \forall f\ \exists\text{ matroid }M\text{ on }V\ \forall S\subseteq V:
\quad \frac{r_M(S)}{\alpha}\le f(S)\le\alpha r_M(S),
\tag{1}
\]

where \(f:2^V\to\mathbb R_{\ge0}\) is monotone and submodular, \(f(\varnothing)=0\), and \(f(\{i\})=1\) for every \(i\in V\). The source explicitly displays the denominator \(\alpha\) on the left. It is essential to retain it. The source's word “constant” is read dimension-independently here; it does not separately write a quantifier over \(V\).

For a matroid \(M=(V,\mathcal I)\), the rank is

\[
r_M(S)=\max\{|I|:I\subseteq S,\ I\in\mathcal I\}.
\]

Thus \(R=r_M(V)\) is the size of a basis \(B\), and \(r_M(B)=|B|=R\). These are the only structural facts about matroids used in the lower bounds.

## 2. Square-root family: a complete counterexample proof

**Theorem.** Let \(n\ge1\), and set \(f_n(S)=\sqrt{|S|}\) on \(V=[n]\). The function meets every hypothesis in (1). If a matroid rank \(r\) on \(V\) satisfies (1) for this function and some \(\alpha>0\), then \(\alpha\ge n^{1/6}\).

**Proof.** Nonnegativity, monotonicity, \(f_n(\varnothing)=0\), and singleton normalization are immediate. For \(k\ge0\), the successive cardinality increment is

\[
d_k=\sqrt{k+1}-\sqrt{k}
=\frac{1}{\sqrt{k+1}+\sqrt{k}},
\]

which is nonincreasing in \(k\). To check the full submodular inequality directly, take \(A,C\subseteq V\), put \(t=|A\cap C|\), \(a=|A\setminus C|\), and \(c=|C\setminus A|\). Then

\[
f_n(A)-f_n(A\cap C)=\sum_{j=0}^{a-1}d_{t+j}
\ge\sum_{j=0}^{a-1}d_{t+c+j}
=f_n(A\cup C)-f_n(C).
\]

Empty sums are zero. Rearrangement proves submodularity, including all degenerate cases.

Suppose now that (1) holds. For every \(i\in V\), its upper inequality gives

\[
1=f_n(\{i\})\le\alpha r(\{i\}).
\]

A matroid singleton rank is zero or one, so all elements are nonloops, \(\alpha\ge1\), and \(R=r(V)\ge1\). Choose a basis \(B\). The lower inequality in (1), evaluated at \(B\), gives

\[
\frac{R}{\alpha}\le\sqrt R,
\qquad\text{hence}\qquad R\le\alpha^2.
\]

The upper inequality, evaluated at \(V\), then gives

\[
\sqrt n\le\alpha R\le\alpha^3.
\]

Consequently \(\alpha\ge n^{1/6}\), as claimed. For any proposed universal \(\alpha>0\), choosing an integer \(n>\alpha^6\) contradicts this bound. Therefore (1) is false. \(\square\)

### Sharpness for this particular family

For every integer \(1\le R\le n\), the uniform matroid \(U_{R,n}\) has rank \(r(S)=\min\{|S|,R\}\). Its smallest valid two-sided factor for \(f_n\) is exactly

\[
\max\!\left\{\sqrt R,\frac{\sqrt n}{R}\right\}.
\tag{2}
\]

Indeed, for \(1\le k\le R\), the ratios \(r(S)/f_n(S)\) and \(f_n(S)/r(S)\) are \(\sqrt k\) and \(1/\sqrt k\). For \(R\le k\le n\), they are \(R/\sqrt k\) and \(\sqrt k/R\). Their maxima are precisely those in (2). The basis and full-set argument gives the same lower bound for every matroid of total rank \(R\), so minimizing (2) over integer \(R\) gives the optimum among all matroids on \([n]\).

In particular, for \(n=m^3\), the choice \(R=m\) realizes factor \(\sqrt m=n^{1/6}\). This establishes sharpness only for the square-root family, not for the entire class of normalized submodular functions.

## 3. Rational-valued strengthening by the same method

**Lemma.** Let \(m\ge1\) be an integer and \(|V|=m^2\). Define

\[
g_m(\varnothing)=0,\qquad
g_m(S)=1+\frac{|S|-1}{m}\quad(S\ne\varnothing).
\]

This is a normalized, nonnegative, monotone, rational-valued submodular function. Every matroid rank on \(V\) satisfying the two inequalities in (1) with \(f=g_m\) has

\[
\alpha^2+\alpha\ge m,
\qquad
\alpha\ge\frac{\sqrt{1+4m}-1}{2},
\qquad
\alpha\ge\sqrt{m/2}=|V|^{1/4}/\sqrt2.
\tag{3}
\]

**Proof.** Let \(u(S)=\min\{|S|,1\}\), the rank of the rank-one uniform matroid. Then

\[
g_m(S)=\left(1-\frac1m\right)u(S)+\frac1m|S|.
\]

Both \(u\) and cardinality are monotone submodular, and the coefficients are nonnegative. Hence \(g_m\) is monotone submodular; its remaining stated properties follow immediately.

As above, singleton normalization and the upper comparison force \(\alpha\ge1\) and \(R=r(V)\ge1\). At a basis \(B\), the lower comparison is

\[
\frac R\alpha\le\frac{m+R-1}{m},
\quad\text{so}\quad
m\le\alpha+\frac{\alpha(m-1)}R.
\]

At the full ground set, the upper comparison is

\[
m+1-\frac1m=g_m(V)\le\alpha R.
\]

In particular \(R\ge m/\alpha\). Substitution yields, with no case split or division by \(m-\alpha\),

\[
m\le\alpha+\frac{\alpha(m-1)}R
\le\alpha+\frac{\alpha^2(m-1)}m
\le\alpha+\alpha^2.
\]

Solving this quadratic inequality gives the middle bound in (3). Since \(\alpha\ge1\), also \(\alpha+\alpha^2\le2\alpha^2\), giving the last bound. \(\square\)

## 4. Source and attribution

- László Végh, *Open problem: Approximating submodular functions by matroid rank functions*, in *Combinatorial Optimization*, Oberwolfach Report 53/2021, printed p. 2946; [official report PDF](https://ems.press/content/serial-article-files/46931), [DOI](https://doi.org/10.4171/OWR/2021/53).
- Michel X. Goemans, Nicholas J. A. Harvey, Satoru Iwata and Vahab Mirrokni, *Approximating Submodular Functions Everywhere*, [author-hosted paper](https://www.cs.ubc.ca/~nickhar/papers/SubmodularEverywhere/SubmodularEverywhere.pdf). Its Problem 1 concerns approximants obtained with polynomially many oracle queries; the approximant is not required to be a single matroid rank. Its lower bounds are not being claimed as this proof or used to infer the negative answer above.

A bounded primary-literature search on 9 October 2026 did not locate an exact prior presentation of the elementary obstruction. This is not an exhaustive novelty certification. The proof is self-contained and the report makes no priority claim. The two families use a single mathematical approach: compare the approximant on one basis and on its whole ground set.
