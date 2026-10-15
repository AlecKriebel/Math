# A determinantal counterexample to the augmented-image condition

**Target:** 30001234 / OWR-3471-008, Takagi’s Question 8 in OWR 21/2009.  
**Status:** complete counterexample candidate; independent adversarial review pending.  
**Attribution:** elementary argument for the stated question; no novelty or human peer-review claim.

## 1. The exact condition being tested

In [the original report](https://ems.press/content/serial-article-files/46224), Proposition 5 starts on printed p. 1137 and continues on p. 1138. It uses nonzero nonnegative integral exponent vectors \(a_i,b_i\), nonzero coefficients \(\gamma_i\), and the augmented matrix
\[
 A=\begin{pmatrix}a_1&\cdots&a_r&b_1&\cdots&b_r\\ I_r&I_r\end{pmatrix}.
\]
The constraints are **nonstrict**:
\[
 P=\{z=(\mu,\nu)\in\mathbb Q_{\ge0}^{2r}:Az\le\mathbf1\},
 \qquad c(z)=\sum_{i=1}^r(\mu_i+\nu_i).
\]
Let \(F\) be the set of optimal rational solutions. The rendered hypothesis is
\[
 A(\mu,\nu)^{\mathsf T}\ne A(\mu',\nu')^{\mathsf T}
\]
“for all other optimal solutions” \((\mu',\nu')\ne(\mu,\nu)\), for some optimal \((\mu,\nu)\). Thus the question is whether
\[
 \exists z\in F\quad\forall z'\in F\setminus\{z\},\quad Az'\ne Az. \tag{1}
\]
Question 8, printed p. 1139, asks whether this always holds for a monomial-free binomial ideal with a minimal binomial generating system. The same formulation occurs in Shibuta–Takagi, arXiv:0810.1278v3, Proposition 2.1 and Question 2.2. No regular-sequence, dimension-three, irreducibility or primeness hypothesis is imposed by Question 8.

Condition (1) must be distinguished from both uniqueness of the optimizer and uniqueness of the optimal image vector. It asks for an optimizer whose **fiber under \(A\) contains no second optimizer**. In this LP, if a feasible \(z'\) has \(Az'=Az\) for an optimizer \(z\), then it is automatically optimal: \(c(z)\) is the sum of the last \(r\) coordinates of \(Az\). Therefore replacing “other optimal solutions” in (1) by “other feasible solutions” would give an equivalent condition. By contrast, \(A(F)\) being a singleton is an entirely different assertion.

## 2. The ideal and its hypotheses

Let \(k\) be any field of characteristic zero and work in
\[
 S=k[x_1,x_2,x_3,y_1,y_2,y_3].
\]
Set
\[
\begin{aligned}
 f_1&=x_1y_2-x_2y_1,\\
 f_2&=x_2y_3-x_3y_2,\\
 f_3&=x_3y_1-x_1y_3,
\end{aligned}
\qquad \mathfrak a=(f_1,f_2,f_3). \tag{2}
\]
These are the three two-by-two minors of a generic two-by-three matrix, with one sign chosen to give a cyclic orientation. All coefficients \(\gamma_i\) in the source notation are one. Every monomial has degree two, is squarefree, and has a nonzero exponent vector. The two monomials in each generator have no common factor.

**No monomial belongs to \(\mathfrak a\).** Evaluation at the point where all six variables are one annihilates every generator. A nonzero scalar multiple of any monomial evaluates to a nonzero scalar. Hence it cannot lie in \(\mathfrak a\).

**The three generators are minimal.** The ideal is homogeneous and generated in degree two. The six monomials occurring in (2) are pairwise distinct, so \(f_1,f_2,f_3\) are linearly independent over \(k\). If \(\mathfrak m\) is the homogeneous maximal ideal, their classes form a basis of \(\mathfrak a/\mathfrak m\mathfrak a\): the degree-two part has dimension three, and all higher-degree elements of \(\mathfrak a\) are in \(\mathfrak m\mathfrak a\). Therefore at least three generators are necessary, even after localization at \(\mathfrak m\). This is not a counterexample produced by adding redundant generators.

The example is even prime, although primeness is unnecessary for Question 8. Here is a direct verification. Define
\[
 \phi:S\longrightarrow k[s,t,z_1,z_2,z_3],\qquad
 x_i\longmapsto sz_i,\quad y_i\longmapsto tz_i.
\]
The generators lie in its kernel. Two monomials \(x^\alpha y^\beta\) and \(x^{\alpha'}y^{\beta'}\) have the same image exactly when
\[
 \alpha+\beta=\alpha'+\beta',\qquad |\alpha|=|\alpha'|.
\]
If \(\alpha\ne\alpha'\), choose indices \(j,i\) with \(\alpha_j>\alpha'_j\) and \(\alpha_i<\alpha'_i\). The first monomial contains \(x_jy_i\), since \(\alpha_j\ge1\) and \(\beta_i=(\alpha_i'+\beta_i')-\alpha_i\ge1\). Replace \(x_jy_i\) by \(x_iy_j\) using one of the relations (2). This decreases \(\sum_i|\alpha_i-\alpha'_i|\) by two. Induction identifies the two monomials modulo \(\mathfrak a\). Grouping any polynomial in \(\ker\phi\) by its image monomials now proves \(\ker\phi=\mathfrak a\). The quotient embeds in a polynomial ring, so \(\mathfrak a\) is prime.

## 3. The complete optimal face

Order the variables of \(S\) as \((x_1,x_2,x_3,y_1,y_2,y_3)\), and the LP coordinates as \((\mu_1,\mu_2,\mu_3,\nu_1,\nu_2,\nu_3)\). The prescribed augmented matrix is exactly
\[
 A=\begin{pmatrix}
 1&0&0&0&0&1\\
 0&1&0&1&0&0\\
 0&0&1&0&1&0\\
 0&0&1&1&0&0\\
 1&0&0&0&1&0\\
 0&1&0&0&0&1\\
 1&0&0&1&0&0\\
 0&1&0&0&1&0\\
 0&0&1&0&0&1
 \end{pmatrix}. \tag{3}
\]
The first six rows come from the monomial exponents; the last three are \((I_3\ I_3)\). They are all retained.

**Theorem.** The optimum of this LP is three. Its full set of rational optimizers is
\[
 F=\{z(t)=(t,t,t,1-t,1-t,1-t):t\in\mathbb Q\cap[0,1]\}. \tag{4}
\]
Moreover
\[
 Az(t)=\mathbf1_9\qquad\text{for every such }t. \tag{5}
\]
Consequently (1) fails for every optimizer, answering Question 8 negatively.

**Proof.** The last three inequalities of (3) give \(c(z)\le3\). Every point in (4) is nonnegative and has image \(\mathbf1_9\), so it is feasible and has objective three. Thus the optimum is three.

Conversely, at any optimum each of the last three inequalities is an equality:
\[
 \nu_i=1-\mu_i\qquad(i=1,2,3).
\]
The first three inequalities then imply
\[
 \mu_1\le\mu_3,\qquad\mu_2\le\mu_1,\qquad\mu_3\le\mu_2.
\]
They force all three \(\mu_i\) to be one number \(t\). Nonnegativity of \(\mu_i\) and \(\nu_i\) gives \(0\le t\le1\). This proves (4), and substitution gives (5).

For every rational \(t\), a distinct rational parameter can be chosen: take zero when \(t\ne0\), and one when \(t=0\). Thus every optimizer has a distinct optimizer with the same augmented image. In fact the entire nontrivial optimal segment is one fiber of \(A\). This is the negation of the precise source condition (1), not merely evidence that the optimizer is nonunique. \(\square\)

The calculation also makes the linear-algebra obstruction transparent:
\[
 \ker A=\mathbb Q(1,1,1,-1,-1,-1),\qquad\operatorname{rank}A=5.
\]
This kernel statement follows already from the three bottom equations and the three cyclic top equations. The optimal set has a unique **image vector**, but has no optimizer with a singleton image fiber. These two uses of the word “unique” have opposite implications in this example.

## 4. Literature and what this answer does not require

The ideal (2) is the familiar binomial edge ideal of the triangle and a classical determinantal ideal. Neither the ideal nor the underlying determinantal theory is new. The proof above is only an explicit elementary answer to the stated LP-fiber question; it makes no priority claim.

Later work must be compared with the actual LP. LaClair’s *Invariants of binomial edge ideals via linear programs*, J. Algebraic Combinatorics 62 (2025), article 16, uses a **modified** linear program, with additional vertex-subset constraints. For the full three-vertex set one of those constraints bounds the total edge weight by two. It excludes (4), which has total weight three. That later program is therefore not the same feasible polytope as Proposition 5. Remark 3.15 explicitly discusses the upper bound obtained by removing the additional subset constraints. Its existence and the known determinantal-threshold calculations are relevant prior context, not evidence that (3) satisfies the original condition. [Published article](https://doi.org/10.1007/s10801-025-01439-x); [primary preprint](https://arxiv.org/abs/2304.13299).

Blanco–Encinas gives a broader procedure for computing thresholds of binomial ideals, including coefficient dependence. It likewise does not turn the original singleton-fiber assertion into a general theorem. [Primary preprint](https://arxiv.org/abs/1405.3942); Manuscripta Mathematica 155 (2018), 141–181, DOI [10.1007/s00229-017-0929-4](https://doi.org/10.1007/s00229-017-0929-4).

No log canonical threshold, multiplier ideal or positive-characteristic comparison is needed to establish the counterexample: (2) and (3)–(5) suffice. In particular, this does not contradict the conditional theorem of Shibuta–Takagi or its regular-sequence/space-curve applications. The candidate fails that theorem’s explicitly stated hypothesis.

A bounded primary-source search did not locate an explicit earlier answer to the numbered LP-fiber question. It did locate substantial related prior theory, and does not establish novelty. The exact mathematical counterexample should not be described as a new determination of a determinantal threshold or a new general algorithm.

## 5. Verification boundary

The accompanying exact checker reconstructs (3) from the binomial exponents, computes the rational rank and kernel, verifies optimal primal and dual certificates, enumerates the small polytope’s vertices using exact arithmetic, and checks the segment/image formulas. It also checks bounded instances of the monomial straightening used in the primeness argument and the coefficient cancellation in \(f_1f_2f_3\).

The unrestricted proofs of minimality, absence of monomials, primeness and the complete optimal-face description are written above. They are not inferred from sampling or from floating-point LP output. One substantive cyclic-minor construction attempt was used. Separate adversarial review must precede publication as a claimed complete result.

## Primary source locations

- Takagi, *Computations of log canonical thresholds*, OWR 21/2009, printed pp. 1136–1139; Proposition 5 on pp. 1137–1138 and Question 8 on p. 1139: https://ems.press/content/serial-article-files/46224. The precise condition and question were visually checked on rendered pp. 1138–1139.
- Shibuta–Takagi, *Log canonical thresholds of binomial ideals*, [arXiv:0810.1278v3](https://arxiv.org/abs/0810.1278v3), Proposition 2.1 on p. 6 and Question 2.2 on p. 8. Published as Manuscripta Mathematica 130 (2009), 45–61, DOI [10.1007/s00229-009-0270-7](https://doi.org/10.1007/s00229-009-0270-7). The complete primary preprint was available; the publisher’s full text was subscription-only in this audit.
