# A credited finite orbitwise evaluation certificate

**Target:** UnsolvedMath ID 30001568 / OWR-4426-005, rank 432.  
**Status:** complete candidate applicability certificate, author turn 1; awaiting genuinely independent review.  
**Scope:** exact finite evaluation, with one invariant scalar computation per input orbit representative. No complexity or novelty claim.  
**Date:** 2026-10-03.

## 1. Target and attribution

The source is Matthias Köppe's contribution to *Mini-Workshop: Exploiting Symmetry in Optimization*, Oberwolfach Report 38/2010, pp. 2266–2268, DOI [10.4171/OWR/2010/38](https://doi.org/10.4171/OWR/2010/38). Its question is how to evaluate an already orbitwise rational generating function without losing the useful symmetry. In the counting application the combined function belongs to a bounded polytope, even though its individual binomial-denominator terms are singular at the all-ones point. The source does not impose a particular complexity bound.

This certificate supplies a finite evaluator by applying established multivariate regularization. The analytic foundation is **Li Guo, Sylvie Paycha, and Bin Zhang**, *A conical approach to Laurent expansions for multivariate meromorphic germs with linear poles*, Pacific Journal of Mathematics **307** (2020), 159–196: Definition 2.4, Theorem 2.11, and Corollary 4.16. These give polar germs relative to an inner product, a constructive decomposition, and uniqueness of the holomorphic part. Their *Locality Galois groups of meromorphic germs in several variables*, [arXiv:2301.02300](https://arxiv.org/abs/2301.02300), Example 5.4, explicitly composes this projection with evaluation at zero. The new text below is an applicability derivation and exact-arithmetic implementation, **not a claim of a new projection, regularization principle, or independent mathematical discovery**.

## 2. Finite input and exact conclusion

Let \(V=\mathbb Q^d\), with \(d\ge1\), and let \(G\) be a finite group of lattice-preserving affine maps
\[
g(v)=A_gv+t_g,\qquad A_g\in\mathrm{GL}_d(\mathbb Z),\quad t_g\in\mathbb Z^d.
\]
Linear symmetries are the special case \(t_g=0\). The induced action on a Laurent rational function sends a monomial \(z^a\) to \(z^{A_ga+t_g}\) and a binomial denominator exponent \(b\) to \(A_gb\); equivalently,
\[
(g\star R)(z)=z^{t_g}R(z^{A_g}),
\]
where \((z^{A_g})^a=z^{A_ga}\). This is a linear group action on functions; for affine symmetries it is not asserted to preserve multiplication.

The given orbit presentation has the form
\[
F(z)=\sum_{i=1}^{r}\alpha_i\sum_{g\in G/H_i}g\star R_i(z),
\qquad
R_i(z)=\frac{z^{a_i}}{\prod_{j=1}^{m_i}(1-z^{b_{ij}})}. \tag{1}
\]
Here \(\alpha_i\in\mathbb Q\), \(a_i,b_{ij}\in\mathbb Z^d\), every \(b_{ij}\ne0\), and \(H_i\) fixes \(R_i\). Usually \(H_i\) is its stabilizer. A subgroup of the stabilizer is also allowed if (1), including its repetitions, is the intended input. Set \(n_i=[G:H_i]\). No linear independence of the denominator vectors is assumed.

Required regularity: \(F\) is holomorphic at \(\mathbf1\). For the generating function of a bounded rational polytope this follows because the combined function is a finite Laurent polynomial. In the more general rational-function formulation, holomorphy is an input promise. The procedure computes the ordinary finite value \(F(\mathbf1)\), not a newly assigned value for a genuine pole.

The finite data are the group or its finite generating set, the orbit representatives and rational coefficients, the orbit multiplicities, and rational matrix/vector arithmetic. The formula also accepts a supplied common fixed point \(c\) and invariant positive definite rational form \(Q\), whose defining identities can be checked on generators. If multiplicities are not supplied, finite group/orbit enumeration computes them; this may be expensive.

**Candidate conclusion.** From these data the procedure below terminates using rational arithmetic and returns
\[
F(\mathbf1)=\sum_{i=1}^{r}\alpha_i n_i\,\mathcal E_{Q,c}(R_i). \tag{2}
\]
Only one \(\mathcal E_{Q,c}\) evaluation is required per representative. No singular orbit member is separately evaluated at \(\mathbf1\), and no single generic evaluation direction is selected.

## 3. An invariant rational metric and centering

A common rational fixed point is
\[
c=\frac1{|G|}\sum_{g\in G}g(0)=\frac1{|G|}\sum_{g\in G}t_g.
\]
Indeed, every \(h\) permutes the summands in this affine average, so \(A_hc+t_h=c\). A positive definite rational form on exponent vectors is
\[
Q(v,w)=\sum_{g\in G}(A_gv)^{T}(A_gw). \tag{3}
\]
It is positive definite because the identity term is positive on every nonzero vector. Reindexing \(g\mapsto gh\) proves \(Q(A_hv,A_hw)=Q(v,w)\). The matrix of \(Q\) is integral.

Full group enumeration is sufficient but is not logically required to construct these two auxiliary objects. With generators, solve \((A_s-I)c=-t_s\) by rational linear algebra. Solve the rational homogeneous equations \(A_s^TQA_s=Q\), \(Q=Q^T\), and enumerate rational matrices in that solution space until the leading principal minors are all positive. Formula (3) proves that this search terminates. This alternative is only a finite procedure, not an efficiency claim.

## 4. Published projection and its applicability

For \(v\in V\), write \(L_v(x)=v^Tx\), where \(x\) is a complex dual variable near zero. A meromorphic germ with rational linear poles can be written
\[
\frac{h(x)}{L_{v_1}(x)\cdots L_{v_M}(x)},
\]
with holomorphic rational-coefficient numerator. GPZ's polar subspace for \(Q\) is spanned by germs
\[
\frac{h(L_{w_1},\ldots,L_{w_k})}
{L_{u_1}^{s_1}\cdots L_{u_\ell}^{s_\ell}}, \tag{4}
\]
where the denominator forms are independent, all \(s_j>0\), and \(Q(w_i,u_j)=0\). Their direct-sum theorem gives
\[
\mathcal M=\mathcal M_{-,Q}\oplus\mathcal M_+,
\]
where \(\mathcal M_+\) denotes holomorphic germs. Let \(\pi_{+,Q}\) be the unique projection to \(\mathcal M_+\).

For a rational summand define its centered exponential germ
\[
\widehat R_c(x)=e^{-L_c(x)}R(e^{x_1},\ldots,e^{x_d}),
\qquad
\mathcal E_{Q,c}(R)=\bigl(\pi_{+,Q}\widehat R_c\bigr)(0). \tag{5}
\]
This germ lies in the stated domain: \(1-e^{L_b}=-L_b U(L_b)\), where \(U(t)=(e^t-1)/t\) is holomorphic with \(U(0)=1\). Each inverse \(U^{-1}\) is therefore holomorphic near zero. The numerator remains holomorphic with rational Taylor coefficients, even though \(a-c\) can be rational rather than integral. No globally defined fractional Laurent monomial is required.

### Equivariance

Let \((A\cdot f)(x)=f(A^Tx)\). It sends \(L_v\) to \(L_{Av}\). If \(A\) is a \(Q\)-isometry, it preserves both holomorphic germs and the polar subspace (4): independence, positive pole powers, and orthogonality are preserved. Uniqueness of the direct-sum decomposition consequently gives
\[
\pi_{+,Q}(A\cdot f)=A\cdot\pi_{+,Q}(f). \tag{6}
\]
The fixed-point identity gives, for every affine \(g\),
\[
\widehat{g\star R}_c(x)
=e^{L_{t_g-c+A_gc}(x)}\widehat R_c(A_g^Tx)
=\widehat R_c(A_g^Tx).
\]
Evaluating (6) at zero proves
\[
\mathcal E_{Q,c}(g\star R)=\mathcal E_{Q,c}(R). \tag{7}
\]
The invariant metric is essential to this justification. A generally chosen coordinatewise Laurent constant term cannot be substituted without proving the corresponding invariance.

## 5. Only a finite numerator jet is needed

Put \(T(t)=t/(e^t-1)=\sum_{k\ge0}B_k t^k/k!\), with \(B_1=-1/2\). For a seed with \(m\) denominator factors,
\[
\widehat R_c(x)
=(-1)^m\frac{e^{L_{a-c}(x)}\prod_{j=1}^m T(L_{b_j}(x))}
{\prod_{j=1}^m L_{b_j}(x)}. \tag{8}
\]
Let
\[
P_m(x)=(-1)^m\left[e^{L_{a-c}(x)}\prod_{j=1}^m T(L_{b_j}(x))\right]_m, \tag{9}
\]
where brackets denote the homogeneous degree-\(m\) part. The computation needs only Bernoulli numbers \(B_0,\ldots,B_m\), rational factorials, and the input linear forms. It returns
\[
\mathcal E_{Q,c}(R)
=E_Q\!\left(\frac{P_m}{\prod_jL_{b_j}}\right), \tag{10}
\]
where \(E_Q=\operatorname{ev}_0\circ\pi_{+,Q}\) on linear-pole germs. Section 6 computes the right-hand side by finite polynomial operations.

### Why truncation is exact

The finite reduction below decomposes a numerator \(h\), after choosing independent denominator coordinates \(y\) and \(Q\)-orthogonal coordinates \(w\), as
\[
h(y,w)=h(0,w)+\sum_j y_j h_j(y,w).
\]
The first quotient is polar; each remaining quotient has one fewer total denominator power. For a numerator vanishing to order \(r\), the divided differences \(h_j\) vanish to order at least \(r-1\). Thus a Taylor remainder vanishing to order \(m+1\), over \(m\) denominator factors, can only leave holomorphic terms vanishing at zero. Its evaluator is zero.

For a homogeneous numerator of degree \(q\), every reduction preserves the difference between numerator degree and total denominator degree. If \(q<m\), the numerator becomes constant while poles remain, and that remainder is polar. If \(q>m\), holomorphic terms produced when all poles are removed have positive degree and vanish at zero. Only \(q=m\) contributes. This also proves (10) without assuming continuity of the projection or exchanging it with an infinite sum.

For \(m=0\), the seed is a monomial, \(P_0=1\), and its evaluator is 1.

## 6. A terminating exact algorithm for the degree-zero fraction

The input is a homogeneous polynomial \(P\) of degree \(M\) and nonzero rational denominator forms of total degree \(M\). Coefficients are rational throughout.

### 6.1 Remove dependence among denominator forms

Combine proportional forms, retaining their scalar factors and multiplicities. If distinct remaining forms are dependent, choose a relation
\(L_p=\sum_{i\ne p}c_iL_i\). Use
\[
\frac1{L_p^{s_p}\prod_{i\ne p}L_i^{s_i}}
=\sum_{i\ne p,\ c_i\ne0}
\frac{c_i}{L_p^{s_p+1}L_i^{s_i-1}\prod_{j\ne p,i}L_j^{s_j}}. \tag{11}
\]
Repeat with that fixed relation until some nonpivot factor in it disappears. Along each branch its nonpivot exponent sum decreases by one, so this stage terminates. Rechoose a relation only after the support shrinks. There are finitely many supports, and total pole degree stays \(M\). This yields a finite rational linear combination of fractions with independent denominator supports. This is standard partial-fraction reduction, corresponding to the elementary step preceding GPZ Theorem 2.11.

### 6.2 Remove numerator dependence on the pole span

For an independent denominator support \(L_{u_1},\ldots,L_{u_k}\), let \(U\) be the span of \(u_1,\ldots,u_k\). Choose a rational basis \(w_1,\ldots,w_{d-k}\) of \(U^{\perp_Q}\). Then
\((y_1,\ldots,y_k,w'_1,\ldots,w'_{d-k})=(L_{u_1},\ldots,L_{u_k},L_{w_1},\ldots,L_{w_{d-k}})\)
is a rational coordinate system.

Expand \(P\) in these coordinates and write
\[
P=P_{\perp}+\sum_{j=1}^k y_jP_j,
\]
where \(P_\perp\) consists of monomials containing no \(y\)-variable. One deterministic choice assigns every other monomial to its first positive \(y\)-exponent and divides that monomial by that \(y_j\).

The fraction \(P_\perp/\prod_j y_j^{s_j}\) lies in the polar subspace, so discard it when computing \(E_Q\). For every \(P_j\), cancel one power of \(y_j\) and recurse. **Recompute the orthogonal complement whenever the support changes.** When no denominator remains, take the numerator's value at zero.

Every recursion reduces total denominator degree by one. Thus it terminates in at most \(M\) cancellation levels after (11), although the branching can be costly. Every discarded fraction is genuinely GPZ-polar, and every retained algebraic decomposition is an identity. Hence the returned scalar equals (10). Choices of coordinate complements or monomial assignment do not alter the answer, by uniqueness of the published holomorphic projection.

The forms \(L_{u_j}\) need not be mutually orthogonal. Merely taking the coefficient of \(y_1^{s_1}\cdots y_k^{s_k}\) in an arbitrary denominator-coordinate expansion is generally wrong. For example, with \(Q=\begin{pmatrix}2&1\\1&2\end{pmatrix}\), \(E_Q(x_1/x_2)=1/2\), rather than zero.

## 7. Why the orbit-weighted sum is the desired value

Centering and the published projection are linear. From (1), linearity and (7) give
\[
\mathcal E_{Q,c}(F)=\sum_i\alpha_i n_i\mathcal E_{Q,c}(R_i).
\]
By the holomorphy assumption, \(e^{-L_c(x)}F(e^x)\) is already a holomorphic germ. Its projection is itself, and its value at zero is \(F(\mathbf1)\). This proves (2).

For the stated lattice-point generating function, that value is exactly the number of lattice points. Intermediate orbit contributions can be fractional or negative. They are regularized contributions, not separate ordinary limits or counts. Although they can depend on the invariant metric, the final sum does not.

## 8. Transparent examples and author checks

For the segment \([0,N]\), reflection acts affinely as \(v\mapsto N-v\). Take \(c=N/2\), \(Q=1\), and seed \(1/(1-z)\). Formula (9) gives its value \((N+1)/2\). The two-member orbit contributes \(N+1\).

For \(\{(x,y)\ge0:x+y\le N\}\), the six affine permutations of the barycentric coordinates give \(c=(N/3,N/3)\) and the invariant form \(Q=\begin{pmatrix}2&1\\1&2\end{pmatrix}\). The seed \(1/((1-z_1)(1-z_2))\) has a three-member orbit and evaluates to \((N+1)(N+2)/6\); multiplying by three gives the familiar triangular count. This exercises nonorthogonal poles and affine centering.

The accompanying `orbitwise_evaluator.py` implements (8)–(11) and the recursive reduction. `AUTHOR_TESTS.json` records exact rational checks for segments, cubes, affine triangles, dependent/repeated/proportional poles, a binomial rewrite, and covariance under both a group isometry and a nonorthogonal lattice-basis change. These are author diagnostics, not independent review and not the proof of the general assertion.

## 9. Exact limits of the certificate

- It establishes a **finite, symmetry-invariant orbit-representative procedure** for the stated data and ordinary removable-value problem. It does not establish polynomial-time complexity, practical speedup, small memory use, or good dependence on dimension, pole count, coefficient bit size, orbit sizes, or group-generator input.
- Group/metric preprocessing and partial fractions may be expensive. Given orbit multiplicities and a verified invariant metric, the evaluation stage nevertheless operates once per representative.
- A generic-vector obstruction is not needed and would not refute this method.
- Genuine nonremovable poles, infinite groups, or a presentation not stable under the asserted group are outside the hypotheses. In particular, an unbounded polyhedron can lack the ordinary value requested; choosing a renormalized total in that situation would be a different target.
- This is credited applicability of known machinery. There is no novelty claim. It is a complete candidate for the source's unquantified finite-evaluation reading, not a final repository status or a certification of the source's unstated practical aspirations.

## 10. Independent review request

Please audit the exact source match, the GPZ domain and direct-sum theorem, affine-action centering, invariant metric convention, finite-jet truncation, termination and correctness of both reductions, use of stabilizer multiplicities, all boundary cases, and whether any remaining claim exceeds standard prior credit. Rebuild the diagnostic code from the frozen packet. Distinguish a proof defect from a missing complexity result that the source did not explicitly demand. Any genuine missing hypothesis should be stated rather than silently supplied.
