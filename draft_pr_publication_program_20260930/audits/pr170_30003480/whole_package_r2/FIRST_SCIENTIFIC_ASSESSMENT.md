# Independent first scientific assessment

UTC checkpoint: 2026-10-12T13:27:11.141889+00:00. Completion estimate for this whole-package review: 45%. This is a substantive initial derivation, sealed before any prior review, gate, preparation record, proposal directory, support index, manifest or support archive was opened. The accompanying input ledger fixes the exact candidate and primary-source bytes. No earlier verdict or parent synthesis was consumed.

## Claim, domain and success criterion

The object is the determinant image of real binary tensors of Frobenius norm at most one, including the origin and rank-deficient tensors. The universal claim is: for every integer n>=3, no real polynomial in the n determinant coordinates alone has its nonnegativity set equal to G_n relative to either C_n=[0,1/4]^n or H_n={d in C_n: d_i<=sum_{j!=i}d_j}. A proof must exclude arbitrary degree and arbitrary coefficients, not merely the source's proposed polynomial. It need not exclude Boolean combinations, quantified auxiliary variables, or finite conjunctions. The current paper expressly makes the single-polynomial claim; I do not promote any broader basic-closedness claim here.

Fresh acquisition of Seigal's publisher-typeset paper confirms Definition 1.2 on p352 uses the closed norm-at-most-one ball. Theorem 1.3 on p353 gives H_n; the visually inspected p354 defines Q2 as one half times the product over all 2^n sign vectors, rather than a half-sign product or a square root of that product. Conjecture 1.5 states n>=4 with cube bounds. The relevant OWR contribution uses the same ball and points to that conjecture. The candidate addresses the correct source domain, including zero faces.

## Independent normalization derivation and attacks

For a unit real tensor, choose the real Schmidt basis in mode i. Write T=sqrt(a)e0 tensor u+sqrt(1-a)e1 tensor v with u,v orthonormal and 0<a<=1/2. On the remaining factors, P_j are projections onto the smaller-eigenvalue eigenvectors, and N=sum P_j. In the product eigenbasis, N counts selected coordinates; its sole zero eigenvector is w, the product of the complementary vectors. Consequently N>=I-ww^T. With p=|<w,u>|^2 and q=|<w,v>|^2, Bessel gives p+q<=1 and

sum_{j!=i} lambda_j >= a(1-p)+(1-a)(1-q) >= a(2-p-q) >= a.

The a=0 case is immediate. Degenerate eigenvalues cause no issue: any orthonormal eigensystem works and the spectral counting assertion remains exact. This is the published HSS ingredient, recast in projection notation, not a new physical or empirical assumption.

For a nonzero ball tensor, put s=||T||_F^2. Its smaller unnormalized Gram eigenvalue at determinant d is a_s(d)=(s-sqrt(s^2-4d))/2, with s>=2sqrt(max d). Dividing the tensor by sqrt(s) gives determinants d/s^2, not d/s. The normalized polygon inequality therefore implies the same polygon inequality for a_s(d_i).

One cannot simply increase the norm while preserving determinants. Instead suppose lambda(d_i)=a_1(d_i)>sum a_1(d_j). Then d_i>d_j for every j!=i. For positive d_j<d_i,

d/ds log(a_s(d_j)/a_s(d_i)) = 1/sqrt(s^2-4d_i)-1/sqrt(s^2-4d_j)>0.

To check the derivative independently, log(a_s(d))=log(2d)-log(s+sqrt(s^2-4d)); its derivative is -1/sqrt(s^2-4d). Thus each ratio at an allowed s<=1 is no larger than its trace-one ratio, and their sum is strictly below one. Zero numerators stay zero. The endpoint s=2sqrt(d_i) is obtained by continuity; if d_i=1/4 then s=1 is the only allowed trace. The origin is separate. This proves ball necessity without assuming sphere and ball coincide, and handles all endpoint cases used by the paper.

For n=3 the given weights are nonnegative by triangles, sum to one, and have w0>=1/4 because each t_i<=1/2. The support {000,011,101,110} contains no pair differing in exactly one bit, so every one-mode off-diagonal Gram entry is zero. The bit-one sums are w2+w3=t1, w1+w3=t2, w1+w2=t3. The diagonal spectra are therefore (1-t_i,t_i), including t_i=0 and t_i=1/2. The construction is real and unit norm. This proves exact three-factor sufficiency, rather than an inference from complex realizability or tensor sampling. Fresh HSS text supplies the odd-parity equivalent after flipping all bits; fresh Bravyi Section 2 explicitly supplies even-parity realizability. DSL's published Theorems 1.4--1.5 give a further prior real singular-value criterion, not a novel ingredient of this note.

## Multiplicity and generic residual analysis

Let h(t)=(t_i(1-t_i)) and F=P composed with h. On D=(0,1/2)^3, h is a diffeomorphism and exact feasibility is the triangle region. F is a polynomial and is invariant under t1 -> 1-t1 on all real t, not only on D. On the open boundary patch L=t1-t2-t3=0 with t2,t3>0 and t2+t3<1/2, the other triangle conditions remain strict locally. A valid defining polynomial is nonnegative on L<0 and strictly negative on L>0. Continuity implies F=0 on the patch. In affine coordinates (L,t2,t3), vanishing on an open subset forces the constant coefficient in L to be the zero polynomial, so L divides F.

F cannot be the zero polynomial because D contains infeasible points. If F=L^m A with exact m, A restricted to L=0 is a nonzero polynomial. Its zero set cannot contain an open patch, so a boundary point exists with A nonzero. At that point the sign change forces m odd. This avoids a hidden assumption that an arbitrary residual is nonzero at a preselected rational point.

Reflection maps L to -(t1+t2+t3-1)=-L'. Since reflection is a polynomial ring automorphism fixing F, exact divisibility in both directions gives exactly the same multiplicity m for L'. The patch near (1/3,1/3,1/3) on L'=0 lies within D and strictly within all triangles. Exact multiplicity again gives a point in this patch where the residual is nonzero. There F has the sign of a nonzero continuous residual times (L')^m; nonnegativity on a full neighborhood forces m even. Thus no polynomial exists. No global factorization or simultaneous avoidance of all possible factors is needed beyond these two residual restrictions.

For the hull version, at t=(b+c,b,c) the three determinant slacks are 2bc, 2c(1-b-c), 2b(1-b-c), all strictly positive. On sum t_i=1 they are 2t_jt_k. These conditions place both patches in the strict interior of H3 and allow both local sides to remain there. To exclude a zero F for this version independently, t=(5/16,1/8,1/8) has t1>t2+t3 but h(t)=(55,28,28)/256 in strict H3. The smallest hull slack is 1/256>0. Therefore a zero F would include an explicit infeasible point of the allowed hull.

## All-n slices and exceptions

For a real flattening M, det(MM^T)=0 is equivalent to rank(M)<=1 because MM^T is positive semidefinite. A nonzero tensor with that property factors as S tensor u in the chosen factor. Replace u by u/||u|| and S by ||u||S. Then every remaining Gram matrix and the total norm are exactly preserved, as contraction in the removed unit factor contributes sum u_a^2=1. Repeated peeling therefore proves G_n intersect {d4=...=dn=0}=G3 times zero, including the zero tensor separately. Conversely tensoring by unit vectors realizes every such point. The corresponding hull face is exactly H3 times zero: inequalities in appended zero coordinates impose no additional constraint. Restriction of an alleged P_n then gives an alleged three-variable polynomial; an identically zero restriction is already excluded by the infeasible point above. This proof establishes the closed-domain theorem for all n>=3. It does not establish the all-positive higher-dimensional-domain variant from the competitor.

For n=2, the two determinant values agree. A diagonal real matrix with squared singular values t and 1-t realizes every d=t(1-t) in [0,1/4]; -(d1-d2)^2 suffices in C2. For n=1 any 2-by-1 flattening has zero determinant, giving {0}. These exceptions fit the claimed threshold.

## Exact positive witness and printed-source warning

With r=(49,36,36,1)/100 and d=r^2, the full-sign product and determinant-triangle product have the manuscript's rational values. The deposited checker baseline was run on the exact manuscript/checker bytes, producing 46,274 finite checks; this is corroboration of the arithmetic, not the universal proof. Every coordinate lies strictly between zero and 1/4. The largest determinant is 2401/10000=0.2401, and the sum of the other determinants is 0.2593, so all H4 slacks are positive. The polynomial difference is 2589624828909/4768371582031250>0.

Since h(t)=t(1-t) increases on [0,1/2], d1>h(2/5), d2=d3<h(1/6), and d4<h(1/100). Therefore lambda(d1)>2/5 whereas sum of the remaining lambdas<103/300<2/5. Ball necessity excludes this strictly positive tuple at every allowed trace. The witness refutes the printed conjecture with exactly its Q2 convention. For GHZ, d=(1/4)^3 gives Q1=1/64 and Q2=9/512 and the printed secondary left side equals 1/4>3/16. This verifies the displayed inequality warning; it does not undermine the independently used convex-hull theorem or the marginal criterion.

## Prior ingredients, overlap and chronology limits

Sinn's freshly acquired Lemma 4.2(b) gives an earlier general boundary/interior obstruction for regular sets and their regular complements, reaching basic closedness under its hypotheses. The paper appropriately credits that principle and supplies its elementary determinant-specific symmetry argument. I have not proved or promoted a finite-conjunction extension for this manuscript.

Ferudun's independently reacquired nine-page paper contains Theorem 1.4 on p3 and its proof in Section 5, pp7--8: an all-positive strict-hull domain for every n>=3. The facet/interior hyperplane parity argument is equivalent after r=1-2t. His statement is stronger than the present closed-face transfer for n>3. The paper must therefore credit direct overlap rather than merely the marginal background. The candidate does this in abstract, body and metadata. He gives a different rational positive witness, plus additional semialgebraic descriptions; those are not claimed here.

The dates in the receipt and the document are qualified appropriately: author-controlled commit dates cannot certify historical publication visibility, and dated records cannot certify mutual authorship independence or exclusive firstness. The formal preprint is October 12. No pre-October-2 novelty conclusion is justified solely by negative literature searching. Fresh source chronology readback is being retained privately, and the full package phase will verify exact public summaries against it.

## Initial conclusion and remaining work

No substantive mathematical counterexample or proof gap was found in the stated single-polynomial theorem, ball normalization, hull strengthening, exact slice or positive witness. The argument is deductive and checkable; the finite controls are properly subordinated to it. The main remaining tasks are archive/member identity, exact control reruns including semantic mutations in ordinary and optimized execution, all-page PDF inspection, proposal/history/package consistency, and evidence/exclusion/credit audit. These are not yet completed at this first seal. Initial verdict: scientifically sound within its stated closed-domain scope, with overlapped stronger published preprint explicitly credited; package approval remains open.
