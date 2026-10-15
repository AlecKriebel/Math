# ROOT preliminary mathematical reconstruction — PR170

UTC: 2026-10-12. Case remains at mathematical audit stage; priority has not begun.

## Exact hypothesis

For the image G_n of the closed Frobenius unit ball of real binary tensors under mode Gram determinants, the candidate asserts that no real polynomial P in the n determinant coordinates defines G_n by P>=0 even relative to C_n=[0,1/4]^n or its stated convex hull H_n, for n>=3. This is an all-polynomial nonexistence assertion, not a rejection only of Seigal's proposed formula. The original published conjecture concerns n>=4; n=3 serves as the obstructing face. Finite checks cannot certify this quantification.

## Independent reconstruction

A normalized real tensor gives trace-one positive semidefinite two-by-two mode marginals. Let their smaller eigenvalues be a_i. Fix i and Schmidt-expand as sqrt(a_i)|0>u+sqrt(1-a_i)|1>v with u,v orthonormal. In the remaining factors, the sum N of smaller-eigenvector projectors dominates I minus the projector onto the product w of their larger-eigenvectors. With p=|<w,u>|² and q=|<w,v>|², Bessel gives p+q<=1. The remaining eigenvalue sum is at least a_i(1-p)+(1-a_i)(1-q)>=a_i(2-p-q)>=a_i. This proves the credited polygon necessity, including a_i=0 separately.

For trace s=||T||² in (0,1], the smaller eigenvalue is A_s(d)=(s-sqrt(s²-4d))/2. If the trace-one polygon inequality fails at coordinate i, monotonicity of A_1 implies d_i>d_j for every j different from i. For each positive d_j, derivative of log(A_s(d_j)/A_s(d_i)) is 1/sqrt(s²-4d_i)-1/sqrt(s²-4d_j)>0 on the interior feasible trace interval. Thus reducing s from 1 cannot remove that failure. Zero d_j contributes zero; s=2sqrt(d_i) follows by continuity. The d_i=1/4 case forces s=1. This correctly prevents the closed-ball normalization from supplying additional determinant points beyond the trace-one polygon description.

In three factors, nonnegative weights
w_0=1-(a_1+a_2+a_3)/2,
w_1=(a_2+a_3-a_1)/2,
w_2=(a_1+a_3-a_2)/2,
w_3=(a_1+a_2-a_3)/2
sum to one; w_0>=1/4. The even parity support makes every mode Gram matrix diagonal, with bit-one mass a_i. Hence the exact image G_3 in determinant coordinates is obtained by d_i=a_i(1-a_i) from the closed eigenvalue triangle polytope in [0,1/2]^3. This explicit real construction does not rely on a disputed formula for G_3 in the later paper.

Pull back any purported P to F(a)=P(a_1(1-a_1),a_2(1-a_2),a_3(1-a_3)). On the open half-cube it distinguishes the triangle region. A genuine boundary patch on L=a_1-a_2-a_3=0 has inside/outside on opposite sides, forcing F to vanish identically on that plane. Exact divisibility uses polynomial identity on an open plane patch. F cannot be identically zero because a nonempty open outside region requires F<0. Its exact L-multiplicity m is finite; the residual factor is nonzero somewhere on any open patch of L. Near such a point the outside strict negativity and inside nonnegativity force m odd. This does not assume strict positivity everywhere inside.

The global polynomial identity F(1-a_1,a_2,a_3)=F(a_1,a_2,a_3) maps L to minus L'=a_1+a_2+a_3-1 and preserves exact multiplicity, even though the affine involution does not preserve the half-cube. That is sufficient: polynomial identity is global. An open patch of L' around (1/3,1/3,1/3) is strictly inside the triangle region and the half-cube. A nonzero residual at a point of this patch makes odd multiplicity change sign within the image, contradicting nonnegativity. Thus m must also be even.

For the H_3 claim, the determinant triangle gaps on the first patch are 2bc, 2c(1-b-c), 2b(1-b-c), positive for b,c>0 and b+c<1/2. On the second patch sum a_i=1 they are 2a_ja_k>0. Both patches and sufficiently small crossings stay in the interior of H_3. The contradiction therefore persists relative to H_3.

A vanishing mode Gram determinant is equivalent to rank at most one of that real mode flattening. A nonzero tensor consequently factors in that mode. Absorbing length into the remaining tensor and taking a unit vector in the peeled factor preserves total norm and every other Gram matrix. Iteration proves the exact closed face G_n intersect {d_4=...=d_n=0}=G_3 times zero. The corresponding H_n face is H_3 times zero. Restricting P_n to this face inherits the contradiction; an identically zero restriction would wrongly include all of the face, so cannot evade it.

## Outstanding verification and limits

The full polynomial argument appears sound after this reconstruction. Remaining tasks before a math gate: independent complete family audits/controls; ROOT reproduction with false variants; visual confirmation of source formulas/domain and the rational n4 values; accurate treatment of the printed source's GHZ discrepancy. The original source's n>=2 convention makes the n=1 aside merely an extension, not an original claim.

The source record mislabels the OWR report as2018; the report itself is20/2017. This bibliographic correction must be propagated if a package is made. No historical/current priority conclusion follows from correctness or accessibility of the cited papers. Nothing has been published, merged or promoted for PR170.

## Assessment provenance

ROOT inspected only the original candidate, original problem/source metadata, and freshly acquired primary material before drafting these deductions; author verifier, review verdicts and sibling review files have not been read. An unsolicited summary from the multiplicity family, reporting its independently sealed provisional support and a finite outside example, arrived before this note was saved. ROOT's reconstruction above had already been carried out in analysis, but was not sealed beforehand; this note is not claimed as a chronologically blind sealed ROOT assessment. No sibling-specific example or conclusion is needed as an input to this derivation. Each scientific family's separately sealed first mathematical assessment remains the evidence of family independence.
