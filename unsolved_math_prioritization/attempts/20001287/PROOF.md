# Spherical simplex volume products: a classical functional-inequality deduction

## Status and attribution

This note gives an affirmative answer to the exact inequality in H. Koenig's AIM Mahler-duality Problem 23, in every ambient dimension. It is a direct application of the classical Prékopa–Leindler inequality for the geometric mean. Fradelizi–Meyer [FM, Proposition 1] supplies both the inequality and its equality characterization; Lehec [L, Lemma 8 and the proof of Theorem 9] supplies the positive-orthant and dual-cone formulations. **No new-resolution or priority claim is made.** A paper explicitly advertising this application as the resolution of AIM Problem 23 has not been located.

## 1. Exact statement and conventions

Let `n >= 2`, let `C` be a full-dimensional pointed simplicial cone in `R^n`, and put `Q = C ∩ S^{n−1}`. Write

\[
 C^*=\{y:\langle x,y\rangle\geq0\text{ for every }x\in C\},
 \qquad Q^\circ=C^*\cap S^{n-1}.
\]

The original PDF uses **non-strict** `≥ 0`. This corrects the strict inequality in the machine-extracted record. The conventional negative polar is `−C*` and has the same spherical volume. Replacing the closed spherical dual by its interior also leaves the volume unchanged in this nondegenerate case.

Let `σ` denote ordinary spherical `(n−1)`-volume, let `s_{n−1}=σ(S^{n−1})`, and define

\[
 \omega(C)=\frac{\sigma(C\cap S^{n-1})}{s_{n-1}}.
\]

### Theorem

\[
 \omega(C)\omega(C^*)\leq4^{-n},
 \qquad
 \sigma(Q)\sigma(Q^\circ)\leq s_{n-1}^{,2}4^{-n}.
\]

Equality holds if and only if `C` is an orthogonal image of the positive orthant. Consequently the extremizing spherical simplex has pairwise orthogonal generating rays. The theorem also holds for `n=1` with counting measure on `S^0`.

Here `n` is the ambient dimension, and the spherical simplex has dimension `n−1`, with `n` rays and `n` facets. If one interprets “determined by n hyperplanes” to include a degenerate convex chamber, the inequality is trivial: either the cone or its dual lies in a proper linear subspace and hence has zero spherical volume. The proof below treats the nondegenerate case.

## 2. Gaussian and Gram-matrix reduction

Choose an invertible matrix `A` whose columns generate `C`. Then

\[
 C=A\mathbb R_+^n,\qquad C^*=A^{-T}\mathbb R_+^n,
 \qquad G=A^TA>0.
\]

For a positive-definite symmetric matrix `B`, define

\[
 I(B)=\int_{(0,\infty)^n}\exp(-x^TBx/2)\,dx.
\]

A standard Gaussian has uniform spherical direction, independently of its radius. Changing variables in its cone probabilities therefore gives

\[
 \omega(C)=(2\pi)^{-n/2}|\det A|I(G),\qquad
 \omega(C^*)=(2\pi)^{-n/2}|\det A|^{-1}I(G^{-1}).
\]

In particular,

\[
 \omega(C)\omega(C^*)=(2\pi)^{-n}I(G)I(G^{-1}). \tag{1}
\]

If `q(B)` is the positive-orthant probability of a centered Gaussian with covariance `B`, the same product is `q(G)q(G^{-1})`. The covariance and precision matrices are reversed in the individual factors; their product is unaffected.

## 3. The complete inequality

For positive vectors `x,y`, the exact identity

\[
 x^TGx+y^TG^{-1}y-2x^Ty
 =(y-Gx)^TG^{-1}(y-Gx)\geq0 \tag{2}
\]

implies, with `f(x)=exp(−x^TGx/2)`, `g(y)=exp(−y^TG^{-1}y/2)`, and `h(z)=exp(−|z|²/2)`,

\[
 f(x)g(y)\leq e^{-x^Ty}
 =h(\sqrt{x_1y_1},\ldots,\sqrt{x_ny_n})^2. \tag{3}
\]

For completeness, apply ordinary Prékopa–Leindler at parameter `1/2` after the coordinatewise logarithmic substitution. Set

\[
 F(u)=e^{\sum u_i}f(e^{u_1},\ldots,e^{u_n}),\quad
 K(v)=e^{\sum v_i}g(e^{v_1},\ldots,e^{v_n}),
\]

and define `H` in the same way from `h`. The Jacobians give

\[
 \sqrt{F(u)K(v)}\leq H((u+v)/2),\qquad
 \int_{\mathbb R^n}F=I(G),\quad
 \int_{\mathbb R^n}K=I(G^{-1}).
\]

All functions are positive and integrable; no log-concavity assumption on `F` or `K` is needed for Prékopa–Leindler. Hence

\[
 I(G)I(G^{-1})\leq
 \left(\int_{(0,\infty)^n}e^{-|z|^2/2}\,dz\right)^2
 =\left(\frac\pi2\right)^n. \tag{4}
\]

Substitution into (1) proves the claimed bound `4^{−n}`. The orthant attains it because each Gaussian orthant has mass `2^{−n}`.

## 4. Equality and the precise external input

For the equality characterization we use [FM, Proposition 1], not a guessed strictness criterion in (2). Apply that proposition to the unconditional extensions

\[
 f_1(x)=\exp(-|x|_{\rm coord}^TG|x|_{\rm coord}/2),\quad
 f_2(x)=\exp(-|x|_{\rm coord}^TG^{-1}|x|_{\rm coord}/2),\quad
 f_3(x)=e^{-|x|^2/2},
\]

where `|x|coord=(|x_1|,...,|x_n|)`. They are positive, continuous, integrable, and unconditional. Its pointwise hypothesis on the positive orthant is precisely (3). These extensions need not be log-concave; the proposition only requires measurability.

Equality in (4) is equivalent to equality for their whole-space integrals, since each integral gains the factor `2^n`. The equality part of [FM, Proposition 1] then gives a positive diagonal matrix `D` and `d>0` such that

\[
 f_1(x)=d\exp(-|Dx|^2/2)\quad\text{almost everywhere}.
\]

The continuous functions agree everywhere. Taking `x=0` yields `d=1`. On the open positive orthant, comparison of quadratic polynomials now gives `G=D²`, so `G` is diagonal. Conversely a positive diagonal `G` gives equality by one-dimensional Gaussian factorization. Finally, `A^TA` diagonal means that the generating columns of `A` are pairwise orthogonal; positive rescaling of individual columns does not change the cone. This proves exactly the orthogonal-orthant equality characterization.

The Gaussian `f_3` also satisfies the proposition's multiplicative midpoint-concavity condition: `∑(x_i²+y_i²) >= 2∑x_iy_i`. Thus all stated equality hypotheses are met.

## 5. Scope checks

- Orthogonal, rather than arbitrary invertible, images of the orthant are the equality cases. Spherical volume is not invariant under a general linear transformation.
- No sign restriction on the off-diagonal entries of `G` was imposed. Every positive-definite Gram matrix is covered.
- The cone's boundary has Gaussian and spherical measure zero, justifying use of open orthants in integrals.
- The theorem is about simplicial cones. For comparison, the self-dual circular cone of half-angle `π/4` in `R^3` has product `((2−√2)/4)^2 > 1/64`. Thus the same bound would be false for arbitrary convex cones.
- The original source asserts the case `n=3`; the argument proves every `n` under the usual spherical-simplex interpretation and also deals with degenerate convex chambers as above.

## References

[FM] M. Fradelizi and M. Meyer, *Some functional forms of Blaschke–Santaló inequality*, Math. Z. 256 (2007), 379–395. Proposition 1, page 5 of the inspected arXiv version. https://arxiv.org/abs/math/0609553 ; https://doi.org/10.1007/s00209-006-0078-z

[L] J. Lehec, *Partitions and functional Santaló inequalities*, Arch. Math. 92 (2009), 89–94. Lemma 8 on page 4 and dual-cone application on page 5 of the inspected arXiv version. https://arxiv.org/abs/1011.2119 ; https://doi.org/10.1007/s00013-008-3014-0

[AIM] *Mahler's conjecture and duality in convex geometry: Problems*, Problem 23 (H. Koenig), printed page 4. https://aimath.org/WWN/mahlerduality/mahlerduality.pdf
