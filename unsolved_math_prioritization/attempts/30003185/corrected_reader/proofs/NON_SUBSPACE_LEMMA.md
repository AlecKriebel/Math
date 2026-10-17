**Integrated reader status.** Accepted supporting non-subspace lemma, incorporated into the full class-generation proof. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# Constant-class generation: non-subspace part

13 October 2026. Authored deduction from inspected primary-source theorems. This is an intermediate lemma; the subspace part is separate.

Let J=Sp_e(q) or Ω(V), with q odd, e≥16, and let S=J/Z(J). These are quasisimple and simple respectively in this dimensional range. Let x∈J be a natural involution with both eigenspace dimensions in [e/3,2e/3]. Its image x̄ is a nonidentity involution in S.

For any maximal subgroup M of S that is non-subspace in Burness's Definition 1, Burness's Theorem 1 and Corollary 1 give

  |x̄^S ∩ M|/|x̄^S| < |x̄^S|^(−1/2+1/e+ι),

where, in these families and dimensions, 0≤ι≤1/(e−2). Thus the exponent is at most −1/3. The natural dimension is the parameter e in these ranges; the exceptional smaller-dimensional isomorphisms in his Definition 2 do not apply.

A strong Ω-class is a full O-class: the centralizer contains reflections realizing all determinant/spinor cosets, since the two nondegenerate eigenspaces have dimension at least three. The accepted order-product bounds give

  |x^J| ≥ (21/128)q^(rs) in Ω, and |x^J| ≥ (7/8)q^(rs) in Sp,

where r+s=e and rs≥2e²/9. Projection to S has fibers of size at most |Z(J)|≤2. Consequently

  |x̄^S| ≥ (21/256)q^(2e²/9) > (1/16)q^(2e²/9) ≥ q^(e²/5).

The last inequality holds uniformly for q≥3 and e≥16. Therefore

  |x̄^S ∩ M|/|x̄^S| ≤ q^(−e²/15).                         (NS1)

Take 192 mutually independent representatives from any prescribed sequence of 192 strong J-classes. Their projective images are independently uniform on the corresponding S-classes; this follows from the conjugacy-equivariant surjection, whose fibers all have the same size. By (NS1), the probability all images lie in a specified M is at most q^(−192e²/15).

Liebeck–Pyber–Shalev, Theorem 1.1, gives max(S)≤C r^(−2/3)|S| for an absolute C and Lie rank r. Since r≥1 and S is a quotient of a subgroup of GL_e(q), this is less than C q^(e²). A union bound over all non-subspace maximal subgroups gives

  P(all images lie in some non-subspace maximal M) ≤ C q^(−59e²/5).  (NS2)

For all sufficiently large e, uniformly q≥3, this is at most (1/2)q^(−e). The dimension threshold is absolute. No numerical value of C is asserted.

## Inspected primary sources

- T. C. Burness, *Fixed point ratios in actions of finite classical groups, I*, Journal of Algebra 309 (2007), 69–79, DOI https://doi.org/10.1016/j.jalgebra.2006.05.024 . The author-hosted manuscript at https://seis.bristol.ac.uk/~tb13602/docs/fpr1.pdf was retrieved; Definitions 1–2 on manuscript p.2, Theorem 1, Table 1, and Corollary 1 on p.3 were read and rendered. These statements explicitly cover simple projective even-dimensional orthogonal and simple odd-dimensional Ω groups, and PSp. Its main theorem is proved across parts II–IV, as specified in the paper; this deduction uses the stated theorem, not a new proof of those results.
- M. W. Liebeck, L. Pyber, and A. Shalev, *On a conjecture of G. E. Wall*, Journal of Algebra 317 (2007), 184–197. The author-hosted manuscript at https://www.ma.imperial.ac.uk/~mwl/WALL.PDF was retrieved. Theorem 1.1 on manuscript p.2 was read and rendered. It counts actual maximal subgroups, not only their conjugacy classes.

Source PDFs, extracted text, and renders are private inspection evidence and are excluded from any public authored deliverable.
