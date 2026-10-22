# Independent full review: 30003480, one-inequality descriptions of binary Gram loci

**Verdict: PASS_COMPLETE_SINGLE_POLYNOMIAL_IMPOSSIBILITY. No mandatory correction.**

Reviewed COUNTEREXAMPLE.md SHA-256:
\[
\texttt{da019dd76c0ea7bdf789df23410cf85b75f5a30af11ffe7646d1654c7261c5a8}.
\]

The candidate proves that, for every \(n\ge3\), no single additional real-polynomial nonnegativity condition describes the closed-unit-ball Gram locus inside the source cube. The same is true inside its known convex hull. This answers the stated one-polynomial conjecture negatively, including its requested \(n\ge4\) range. The positive rational four-factor certificate independently refutes the particular proposed formula.

Recommended campaign status: **claimed_solved, 2/5**. The result has passed a separate AI mathematical audit. Historical priority and human peer review remain unestablished.

## 1. Exact original domain and question

I inspected the complete Seigal contribution in [OWR 20/2017, printed p.1226](https://ems.press/content/serial-article-files/46684), including its rendered page. The domain is the closed Frobenius **unit ball** of real binary tensors. The contribution proposes one polynomial nonnegativity condition and explicitly points to Conjecture 1.5.

I also read the relevant definitions and statements in the [published 2018 paper](https://seigal.github.io/seigal2018gram.pdf), visually checking printed p.354. Conjecture 1.5 asserts \(Q_1\ge Q_2\) together with the cube bounds \(0\le d_i\le1/4\), for \(n\ge4\). The candidate therefore does not create an easier ambient-space interpretation: its impossibility concerns exactly one **additional** polynomial inequality after granting the cube inequalities, and remains valid after granting all the convex-hull inequalities.

The determinant coordinates scale to fourth order with tensor amplitude, while their common Gram trace is the squared norm. The submitted proof keeps these quantities distinct. It does not replace the real unit ball by unnormalized tensors or silently assume a norm-one representative.

## 2. Polygon necessity and the unit-ball reduction

The [Higuchi–Sudbery–Szulc paper](https://arxiv.org/abs/quant-ph/0209085v2), whose full three-page text I checked, proves the credited marginal-eigenvalue polygon theorem. The included necessity argument is valid: after the first Schmidt split, the sum of the other minor-eigenvalue projections dominates the complement of one product vector. Bessel's inequality gives \(p+q\le1\), and the smaller Schmidt weight \(a\le1/2\) gives the stated lower bound by \(a\). This applies to real tensors without invoking complex realizability.

For a ball tensor of squared norm \(s\), the marginal eigenvalue is
\[
a_s(d)=\frac{s-\sqrt{s^2-4d}}2,
\]
with \(s\ge2\sqrt{\max d_i}\). Dividing the tensor by \(\sqrt s\) and multiplying the normalized polygon inequalities back by \(s\) is correct.

The normalization argument is essential and succeeds. If the unit-trace polygon inequality fails at index \(i\), then \(d_i>d_j\) for every other index. For positive \(d_j\),
\[
\partial_s\log\!\frac{a_s(d_j)}{a_s(d_i)}
=\frac1{\sqrt{s^2-4d_i}}-\frac1{\sqrt{s^2-4d_j}}>0.
\]
Thus the sum of these ratios at an allowed \(s\le1\) is no larger than its already invalid value at \(s=1\). Zero \(d_j\) terms contribute zero. The lowest allowed \(s\) is included by continuity; if \(\max d_i=1/4\), the only allowed norm is already \(s=1\). The zero tensor is separate and valid. Hence every ball tensor satisfies the determinant-to-unit-trace polygon condition used in the proof.

For three factors, the even-parity construction has nonnegative weights summing to one, with \(w_0\ge1/4\). Its mode marginals are diagonal and have the prescribed smaller eigenvalues. This gives an actual **real norm-one tensor**, proving sufficiency and the exact three-factor ball characterization. The construction is explicitly credited to the earlier polygon theorem, up to flipping all bits.

## 3. The universal polynomial obstruction

The pullback map \(t_i\mapsto t_i(1-t_i)\) is a diffeomorphism from \((0,1/2)^3\) to the open cube, with Jacobian \(\prod_i(1-2t_i)>0\). Any proposed polynomial definition therefore gives a nonzero polynomial \(F\) invariant under each involution \(t_i\mapsto1-t_i\).

On the true boundary patch \(L=t_1-t_2-t_3=0\), with positive \(t_2,t_3\) and sum less than \(1/2\), the other triangle inequalities are strict. The defining sign condition forces vanishing on this patch, hence divisibility by \(L\). At a point where the residual factor is nonzero, the polynomial changes sign between the feasible and infeasible sides, so the exact multiplicity of \(L\) is odd. Such a residual-nonzero point exists because otherwise another factor \(L\) would divide \(F\).

The first-coordinate involution sends this factor to the negative of
\(L'=t_1+t_2+t_3-1\), preserving its exact multiplicity. A patch of \(L'=0\) near \((1/3,1/3,1/3)\) lies strictly inside all triangle inequalities and the parameter cube. On both sides of that patch, \(F\) must be nonnegative. At a residual-nonzero point, its multiplicity must consequently be even. This is the required contradiction.

No finite sampling establishes this conclusion. It follows from polynomial divisibility on an open hyperplane patch, exact multiplicity, and the polynomial symmetry. A zero pullback cannot evade the argument: it would include all points of the relevant domain, which contains infeasible points.

The strengthened convex-hull version is also valid. At the true patch, all three determinant-triangle margins are the strictly positive quantities displayed in the candidate. At the internal conjugate patch, they are \(2t_jt_k>0\). Thus complete neighborhoods of both crossing patches remain inside the granted convex hull. The same sign argument applies there.

As an independent algebraic diagnostic, I factored the source's three-factor \(Q_1-Q_2\) after this substitution. The factorization is exactly
\[
-\tfrac12(u-v-w)(u-v+w)(u+v-w)(u-v-w+1)
(u-v+w-1)(u+v-w-1)(u+v+w-2)(u+v+w-1).
\]
It displays the same true and interior conjugate planes. This calculation supports the source checks but is not used to replace the argument for an arbitrary polynomial \(P\).

## 4. Higher-factor slices and boundary cases

For real matrices, a zero Gram determinant is equivalent to flattening rank at most one. A nonzero tensor with that property factors in the corresponding mode. Making the factor a unit vector preserves the remaining tensor norm and all other mode Gram matrices. Iterating proves the exact zero-determinant slice identity; the zero tensor gives no exception.

Restricting any proposed \(n\)-variable defining polynomial to that face would define the three-factor locus. A polynomial vanishing identically on the face would instead include its entire cube or hull slice, which is impossible. The source uses the closed cube, so the face restriction is within its stated domain. The argument needs no higher-factor real-realizability theorem.

The small-\(n\) exceptions are correct. For \(n=2\), the Gram locus is the diagonal segment in the cube, defined by the nonnegativity of \(-(d_1-d_2)^2\). For \(n=1\), the Gram determinant vanishes. These cases do not affect the original \(n\ge4\) conjecture.

## 5. Independent rational counterexample and printed-source issue

I recalculated the full sign product for the proposed four-factor formula by pairing opposite sign choices. At
\[
d=(2401/10000,\;81/625,\;81/625,\;1/10000)
\]
the cube and all determinant-triangle bounds are strict, and the exact difference is
\[
Q_1-Q_2=\frac{2589624828909}{4768371582031250}>0.
\]
The rational comparisons to \(t(1-t)\) give
\(\lambda(d_1)>2/5\) while the sum of the other three smaller eigenvalues is less than \(103/300<2/5\). The necessary ball condition therefore excludes this point. There is no numerical-radical uncertainty.

The caution about the printed Theorem 1.4 is also verified narrowly. Its displayed secondary direction on p.354 is indeed the one reproduced by the candidate. The unit GHZ tensor has all three determinants \(1/4\); its first-region values are \(Q_1=1/64<Q_2=9/512\), and the secondary pair expression is \(1/4>3/16\). Thus that **printed display** fails this direct test. The candidate correctly avoids using it, does not silently repair it, and does not infer that unrelated results in the paper are false.

## 6. Reproduction, source status and publication

All **8,363** submitted assertions replayed with a byte-identical receipt. The independent checker passes **1,589** exact assertions, including symbolic normalization and Jacobian identities, the complete source-polynomial factorization, 125 rational norm-one tensors, prescribed marginal weights, two-sided crossing patches inside the hull, non-coordinate rank-one tensor slices through six modes, the rational four-factor certificate and the GHZ display test. An initial structural comparison of differently factored Jacobian expressions was normalized algebraically in the independent checker; no author proof changed.

Run from this review directory:
\[
\texttt{(cd author\_replay \&\& python verify.py)},\qquad
\texttt{python independent\_checks.py}.
\]
The first checker requires its replay directory as the working directory. Both regenerate deterministic receipts.

A bounded current-primary-source search located the published conjecture and the author's current bibliography, but did not establish a later resolution or a historical-priority conclusion. The polygon theorem and real realization remain credited prior mathematics. This verdict certifies the supplied proof and source match, not first discovery.

The frozen candidate is suitable for one result PR with the eight enumerated review files. Preserve the exact polynomial-coordinate and closed-domain scope, source-display caution, earlier-theorem credit, and the AI-reviewed/unrefereed and priority-unconfirmed qualifications. No mathematical correction is required.

