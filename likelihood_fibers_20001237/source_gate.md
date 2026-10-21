# Source and scope gate: AIM-COMPUTATION-0075

Checked 21 October 2026. This is an authored source/status audit, not a new research result or a solution claim.

## Decision

The source is recovered: AIM *Computational Algebraic Statistics*, Question 60 attributed to Sullivant, under working-session graphical-model questions. The official PDF is dated 27 March 2004; the item is on PDF page 12 of 13. The official HTML agrees. The question asks about sufficient statistics for general log-linear models whose likelihood-equation solution space fails to be zero-dimensional. Hoşten proposes examining parameter-dependent elimination leading coefficients.

The generated title is a specialization, not the historical title or a restatement of the whole question. The historical statement has an ambiguous duplicated-variable quantifier; any repair would be interpretive. It does not fix complex versus real data, affine versus projective conventions, or boundary treatment. The corpus's “partially_solved,” “proved,” and “PARTIAL-PROGRESS” labels describe a machine-generated attempt and are not evidence of accepted mathematical status.

Primary source: https://aimath.org/WWN/compalgstat/compalgstat.pdf and https://aimath.org/WWN/compalgstat/articles/html/2a/ . Public source verification metadata accompanies this audit.

## Three different families must not be conflated

Let u=(u11,u12,u21,u22), N=sum(u), r=u11+u12, c=u11+u21. The independence variety is the Segre quadric p11 p22−p12 p21=0 in projective P³. Its usual likelihood open excludes each p-coordinate and p+=sum(p). Data live projectively in P³_u or affinely in C⁴_u; sufficient-statistic coordinates can be (N,r,c). A nonzero u may have (N,r,c)=0, so projectivizing the statistics loses an important kernel stratum.

1. The generated expected-count family uses a matrix q with sum N, first-row sum r, first-column sum c, and determinant zero. With q=(t,r−t,c−t,N−r−c+t), its determinant is Nt−rc. This correctly yields one reduced affine point if N≠0; no point if N=0 and rc≠0; an affine line if N=0 and rc=0. Thus its positive-dimensional locus is V(N,rc). These lines have a dense cell-torus open; removing cell zeros does not remove them. This calculation is elementary and is not evidence of novel progress on the general question.

2. The normalized likelihood critical family instead sets p+=1. On the independence likelihood open, p=(ab,a(1−b),(1−a)b,(1−a)(1−b)) with a,b not 0 or 1. Direct differentiation gives score numerators r−Na and c−Nb, with nonzero denominators a(1−a), b(1−b). Hence at N=0 the valid critical fiber is empty unless r=c=0; in that latter case the whole two-dimensional model open is critical. For example, u=(1,−1,−1,1) is nonzero projective data and the likelihood is identically 1 on independence. This is a direct consistency audit, not a novelty claim. At N≠0 there is one valid critical point exactly when r(N−r)c(N−c)≠0.

3. The projective likelihood correspondence is the closure of valid critical pairs. Its special fibers can contain boundary points; they cannot be identified with valid open fibers or with the expected-count compactification without checking restriction and specialization. The substitution q=Np is invertible only for N≠0. In particular, the usual normalization exclusion p+≠0 does NOT itself exclude data N=u+=0. Inverting N adds a data-space restriction. The generated report's caution about this distinction is essential, not optional.

## Positive data, zero strata, and discriminants

For N>0 with nonnegative observations, the independence estimate is p_ij=(row_i column_j)/N² and expected counts are q_ij=(row_i column_j)/N. It is interior if every row and column margin is positive; otherwise the extended MLE lies on the boundary. A zero individual observation need not force any zero margin. Consequently a sampling zero, a structural/model zero, a coordinate-zero critical point, and a positive-dimensional complex fiber are different events. The case N=0 in the nonnegative cone forces the entire observed table to be zero and cannot represent a nonzero sample. The complex checkerboard example has negative entries and supplies no counterexample to statistical uniqueness.

The generic ML degree of independence is 1, long established. It does not imply that every nongeneric complex fiber is a single point. Likewise data discriminants can encode ramification, disappearance to infinity, or changes in real/positive root counts; their vanishing is not an exact synonym for positive-dimensional fibers. The ML data singular locus concerns critical points approaching a singular model locus, also a different condition. Primary references: https://arxiv.org/abs/1310.4197 , https://arxiv.org/abs/1501.00334 , https://arxiv.org/abs/1509.09225 .

## What is already algorithmic, and current literature

For a fixed finite polynomial family with explicit excluded factors D, adjoining zD−1 encodes the valid open without assuming saturation commutes with specialization. Comprehensive Gröbner stratification can classify empty, finite, and positive-dimensional fibers. This is standard algebraic machinery, not a new general theorem supplied by the corpus. Fiber-dimension loci are constructible for finite-presentation families; proper families have upper-semicontinuous fiber dimension, hence closed jump loci. An arbitrary compactification can add special components and does not automatically solve the open-fiber question. See https://stacks.math.columbia.edu/tag/05F6 and https://stacks.math.columbia.edu/tag/0D4I .

Barnhill, Cobb, and Faust construct the toric likelihood ideal by adding 2×2 minors of A[u p] to I_A and saturating by p0⋯pn p+. They give explicit Gröbner bases for complete and joint independence. This directly undercuts any suggestion that the 2×2 independence likelihood ideal or product-margin formula is novel. The current publisher record is ISSAC 2026, pages 21–28, published 12 July 2026: https://doi.org/10.1145/3815436.3815479 . The checked full arXiv version is v3, 16 November 2024: https://arxiv.org/html/2312.08501v3 .

Rodriguez–Tang study data-discriminants, and Tang–de Wolff–Zhao develop elimination algorithms exploiting factors involving the data sum; these are relevant algorithmic prior art, not proofs that their discriminant is exactly the AIM jump locus. https://arxiv.org/abs/1810.05620 . Kahle–Schenck–Sturmfels–Wiesmann's *The Likelihood Correspondence* is now published (7 July 2026), https://doi.org/10.1007/s10208-026-09755-9 ; its general correspondence framework likewise should not be advertised as a model-by-model classification of these fibers without a precise theorem match.

## Status wording safe to use

“Historical general question recovered; standard algorithms and later likelihood-correspondence literature address its framework. The generated 2×2 expected-count calculation is correct in its explicitly stated affine family, but is not a classification of normalized likelihood critical fibers at zero total, and novelty is unestablished. No solution of the general AIM question or verified present-day open-status certification follows from this record.”

The finite literature check did not locate a theorem advertised as a complete structural classification for every log-linear A. That negative search is not proof that the question remains open. No claim of new research or problem resolution is warranted. A future mathematical task would first need a fixed A, a precise data parameter space and valid critical family, and a comparison with the known toric correspondence results.
