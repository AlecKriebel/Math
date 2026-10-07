# Independent adversarial audit of the central family-126 argument

**Audit checkpoint:** 2026-10-06 22:16:59 America/Los_Angeles (2026-10-07 05:16:59 UTC).
**Assigned audit completion:** 100%. **Overall TSP resolution/publication completion:** not estimated by this component reviewer; parent maintains those checkpoints.
**Verdict:** No material mathematical gap or counterexample found in the needed central exponential proof. The source-to-exact-matching consequence also checks. This is a mathematical reconstruction and adversarial audit, with supplemental rational/numerical checks, not formal verification or conventional human peer review.

## Reviewed claim and scope

Pinned input is the copy of family 126 at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, under `sources/family126`. The tested claim is: one absolute constant c>0 works so that, for each fixed 0<rho<1, all sufficiently large even n have real PSD rank at least 2^(cn) for the matrix

\[
A_n(\rho)_{U,M}=|M\cap\delta(U)|-1+\rho,
\]

with every odd subset U and every perfect matching M of K_n. The threshold may depend on rho, while c must not. Real PSD rank counts the matrix order of one real symmetric PSD cone, allows arbitrary real factors, and requires exact entries.

I read the project brief; manuscript-specific README/citation; `main.tex`; `refs.bib`; and the entirety of `introduction.tex`, `local-averaging.tex`, `splitting.tex`, `fourier-smoothing.tex`, `parity.tex`, and `matching.tex`. These are every proof section used by the main theorem and exact-lift corollary. The independent appendix `matching-smoothing.tex` is not used by the main proof and was not audited. The TSP face reduction, TSP padding, DP upper bound, and priority/publication package are outside this component audit.

Central source hashes are recorded in `upstream_adversary_checks.json`. I only read the upstream clone, including its `lean/docs/126.md`; I made no Git changes, publication operations, or contact with individuals.

## 1. Local averaging: the asymptotic contraction is justified

References: `local-averaging.tex:12-54`, `:94-189`, `:191-257`.

The local restrictions consist of fixed d terminal bits and g chosen complete internal pairs, where h=(k-d)/2 and g=(w-s)/2. Parity makes g integral. The formula

\[
g=h/2+d/4+\delta/2-s/2,\qquad \delta=w-k/2\in\{0,1\}
\]

gives |g-h/2|<=d/4+1/2. For fixed d, all supports therefore exist once k is sufficiently large, uniformly over both charges and all terminal assignments. No assumption about a typical assignment is needed.

**Uniform marginal.** Permuting vertex names acts transitively on the w-subsets, preserves the uniform law of ordered distinct terminals plus an internal matching, and carries each restriction law to the corresponding restriction law. Thus the average restriction law is exactly uniform.

**Kernel normalization and trace.** If J is the joint probability of two independently restricted cuts conditional on the same local data and N=binom(k,w), the ordinary matrix for K=T* T is N J. Its trace squared is N² sum J(a,a')². Both the joint law and the independent uniform law are uniform within each intersection class. Writing their masses on |a intersect a'|=w-2j as P_j and Q_j gives

\[
P_j=\frac{\binom gj\binom{h-g}j}{\binom hg},\quad
Q_j=\frac{\binom w{2j}\binom{k-w}{2j}}{\binom kw},\quad
\operatorname{tr}(K^2)=\sum_j\frac{P_j^2}{Q_j}.
\]

The support inequality follows from w=2g+s and k-w=2(h-g)+(d-s). The restriction law may omit intersection classes, but these have density zero and cause no missing summand.

The independent central-binomial estimate is binom(k,w)/binom(h,g)²=O_d(sqrt(h)). The displayed identity involving binom(u,j)²/binom(2u,2j) is exact, including the endpoints. After bounding the two denominator factors from below, the residual sum is bounded by

\[
C^2(h+1)\sum_{j=0}^{g_*}\frac1{(j+1)(g_*-j+1)}
=\frac{2C^2(h+1)}{g_*+2}\sum_{j=1}^{g_*+1}\frac1j,
\]

where g*=min(g,h-g)=h/2+O_d(1). Therefore tr(K²)=O_d(sqrt(k) log(k+2))=o(k).

**Multiplicity.** The elementary invariant-subspace argument is sound. Choose k/2 disjoint transpositions. An occurring mixed sign pattern has at least k/2 conjugate patterns, giving at least that dimension. If every occurring pattern is all plus or all minus, each product of two chosen transpositions acts trivially. Conjugating shows the same for any two disjoint transpositions. The displayed five-label identity generates three-cycles, so the alternating group fixes the subspace pointwise. It acts transitively on the present subset slice, and hence only constant functions can be fixed. This contradicts orthogonality to constants.

Consequently the maximal nonconstant eigenvalue mu satisfies (k/2)mu²<=tr(K²)-1, so mu=O_d(k^(-1/4)sqrt(log(k+2))) tends to zero. Entrywise summation gives exactly the same constant for arbitrary finite matrix dimensions. Conditioning on other cells is legitimate if it fixes the function before the current independent local data are sampled.

**Attack result.** Small cells can have mu=1, e.g. k=6,d=2,b=0,s=0. This is reproduced by the supplemental calculation and is consistent with the sufficiently-large-k hypothesis. It is not a counterexample to the lemma. The proof must never be used with an arbitrary small cell size.

## 2. Orthogonal splitting: no dimension loss is hidden

References: `splitting.tex:11-89`.

For P the nonnegative spectral projection of A-B and Q=I-P, the common off-diagonal block A_12=B_12 gives

\[
\operatorname{tr}(AB)
=\operatorname{tr}(A_{11}B_{11})+\operatorname{tr}(A_{22}B_{22})+2\|A_{12}\|_F^2
\ge \|PBP\|_F^2+\|QAQ\|_F^2.
\]

The first two inequalities use A_11>=B_11 and B_22>=A_22 in PSD order. They do not require simultaneous diagonalization of A and B.

For more than two inputs, first separate A_1 from B=sum_{j>=2}A_j and recursively split their Q-compressions. The misplaced terms involving the first label cost at most tr(A_1 B). For distinct j,j'>=2,

\[
\operatorname{tr}(A_j Q A_{j'} Q)
=\|A_j^{1/2}Q A_{j'}^{1/2}\|_F^2
\le2\operatorname{tr}(A_jA_{j'})+2\operatorname{tr}(A_jP A_{j'}P).
\]

The total extra P-overlap is at most ||PBP||_F²<=tr(A_1 B). This gives the claimed induction with C_L=2^(L-1) for the **ordered** overlap sum. The constant is huge but finite and has no dependence on matrix order.

## 3. Product smoothing: the tagged stack repairs the usual square-root trap

References: `fourier-smoothing.tex:42-98`, `:121-342`.

I checked the full inductive construction, including dependence on remaining inputs. At stage i, each branch has r columns but a common row order R_i that may be enormous. Fourier coefficients are concatenated horizontally over L^i characters with old weights. Let U(x) be this concatenation before the next coordinate average, and Z(x)=U(x)^T U(x). Then ||Z(x)||_F²=||U(x)U(x)^T||_F².

The new square-root stack uses disjoint row blocks indexed by both y' and x:

\[
H'(y_{\le i},y)_{(y',x)}
=1_{y'=y}\sqrt{\pi_y^m(x)}H_q^{(i)}(y_{\le i};x,x_{>i+1}).
\]

This retains the exact average of squares. The y' label is essential: it kills terms involving distinct y values in the inner product of Fourier coefficient matrices. A direct multiplication gives precisely

\[
V_z^T V_{z'}=L^{-2}\sum_y\chi_z(y)\chi_{z'}(y)T_y Z(m).
\]

For z=z', Jensen and the uniform marginal bound its squared norm by L^(-2) E_x||Z(x)||_F². For z!=z', character orthogonality removes the common mean, and the local matrix variance bounds it by theta L^(-2) E_x||Z(x)||_F². There is no lost L factor in either expression: L^(-2) sum_y equals L^(-1) E_y.

Split the PSD row Gram matrices A_z=V_z V_z^T using the previous lemma. Left multiplication by the projections preserves the sum of squares and commutes with processed-variable Fourier transforms, because those projections depend only on the parameter history and unprocessed inputs. They can depend arbitrarily on an unprocessed x, but never on its as-yet-unsampled local parameter. Thus each variance application is to a fixed function under an independent uniform current parameter. This avoids an illicit adaptive-conditioning assumption.

The new weighted Gram is sum_z lambda^(1_{s!=z})P_s A_z P_s. Cauchy-Schwarz with L terms, splitting, and the diagonal/off-diagonal overlap counts give the factor

\[
1+(L-1)\lambda^2 C_L\theta\le2
\]

under L lambda² C_L theta<=1. This is a bound for the fourth-order Gram potential, not a falsely dimension-independent bound for its trace.

The final trace conversion uses rank(C_q)<=r L^t from the number of columns, independently of the enlarged row dimension. A second Cauchy-Schwarz over L^t branches gives weighted Fourier mass <=L^t sqrt(r) B 2^(t/2). All dimensions and all character counts agree.

## 4. Expander and parity functional: no circular consistency assumption

References: `parity.tex:15-91`, `:93-284`.

For a candidate set of size w<=l in the union of 100 random bipartite matchings, a failed cut bound first forces a,b in [.45w,.55w]. At least .95da prescribed images must lie in a specified b-subset. Sampling without replacement gives probability at most (b/l) to their number; the entropy bound supplies at most exp(.21da) possible exception sets. Combining with binom(2l,w) yields the displayed coefficient 41.75 on log(w/l). Independently evaluated, the constant term log(2e)+45(.21+.95 log(.55)) is approximately -14.41438, strictly less than -8. The sum of exp(-8w) over positive w is approximately 0.000335575<1. Therefore the probability argument supplies connected multigraphs for every required sufficiently large even t. Parallel edges are distinguished throughout and cause no simplification error.

For a character of block degree <=2D, its selected free incidences map to an edge set of size <=2Dd. If this is a cut, expansion gives a uniquely determined side of cardinality <=2D/beta<=t/5. The crucial point is **local** sign consistency only on the low-degree moment matrix. Equal-cut-coset pairs have a small cut side. For three indices, the symmetric difference of the three sides has empty cut and size <=3t/5<t; connectedness forces it to be empty. Thus every triple of moment signs has product one, and every coset block is exactly sigma sigma^T. No globally consistent assignment to the inconsistent parity system is assumed or needed.

When an edge incidence lies in the last position, replacing it by all d-1 free incidences toggles that vertex star and contributes the charge sign. For the two ends of an edge, their original incidence image is empty, so after all such replacements the image is delta(T). T has at most two vertices and is the selected small side for sufficiently large t. Its charge sign cancels the replacement phase. Every edge-sign product receives functional value one, hence every disagreement receives value zero. The constant gets value one, so D(f_epsilon)=-epsilon. The bound |D(h)|<=L^t||h||_infinity follows from at most L^t Fourier coefficients of absolute value <=||h||_infinity.

The finite supplemental parity check uses K_10,10 with d=10,t=20,beta=1/2,D=1, for which 2D/beta=t/5. It exactly checks all 10,221 degree-one characters, their 10,121 moment blocks, and all 100 edge disagreement values, including 20 last-incidence replacements. These are adapted small-instance constants, explicitly **not** a computation of the source's d=100 asymptotic theorem.

## 5. Matching realization and exponential contradiction

References: `matching.tex:13-39`, `:41-218`.

Normalization is valid after compressing to the span of column-factor images. The convex hull of column factors contains a positive definite average, so its determinant maximizer J is positive definite. The log-determinant directional derivative toward each column gives tr(J^(-1)G_m)<=r. Opposite congruences preserve all trace pairings. Row traces become convex combinations of row entries, hence are at most B. There is no precision, symmetry, or matrix-commutativity assumption.

The cell matching uses one distinct terminal per auxiliary incidence. Parallel auxiliary edges therefore use distinct vertices of K_n. All remaining vertices have even count and are matched outside the cut. The cut union has odd cardinality by its prescribed cell weights. Its internal pairs do not cross, and its auxiliary pairs cross exactly on bit disagreements. Thus the average row factor pairs with the actual matching column to yield f(y) exactly.

Choose lambda first with lambda^tau>=64 L^4, then fix even k so that L lambda² C_L theta_d(k)<=1. The local lemma allows this because d,L,lambda,C_L are fixed, despite their enormous values. These choices are independent of n and rho. Let t be the largest even integer with kt<=n, so kt<=n<k(t+2), and suppose r<=2^t.

After smoothing, truncate each branch at distance D=floor(tau t). A discarded integral distance is strictly larger than tau t. With ||G||_op<=r, Cauchy-Schwarz over at most L^t frequencies per branch, and the weighted Fourier estimate,

\[
\sum_q\|(H_q-K_q)G^{1/2}\|_F^2
\le n\left(\frac{4L^2}{\lambda^\tau}\right)^t
\le n(4L)^{-2t}.
\]

The factor 4^t uses r^(3/2)2^(t/2)<=2^(2t), exactly from r<=2^t. The full stack has norm sqrt(f(y))<=sqrt(n). Therefore the difference between squared norms is bounded uniformly by 2n(4L)^(-t)+n(4L)^(-2t).

Multiplying each retained branch by its real center character moves every entry to block degree <=D and leaves squares unchanged. Hence D(f_*)>=0 while D(f)=-epsilon. Its error after applying the functional is at most 2n4^(-t)+n(16L)^(-t), which tends to zero because k is fixed and n<k(t+2). For fixed epsilon=1-rho>0 this contradicts the functional values at sufficiently large n. Finally t>=n/(2k) for sufficiently large n, giving rank_psd A_n(rho)>2^t>=2^(n/(2k)). This confirms the uniform exponent and the allowed rho-dependent threshold.

The endpoint rho=1 is correctly excluded: the diagonal edge factorization has order binom(n,2). Nothing in the argument incorrectly claims an exponent uniform in a varying rho_n approaching one.

## 6. Exact unshifted matching consequence

References: `introduction.tex:74-114`. Primary cone-factorization source checked on 2026-10-06: [Gouveia, Parrilo, Thomas, arXiv:1111.3164v2](https://arxiv.org/pdf/1111.3164), Theorem 2.4, Corollary 2.6, and Theorem 3.3. Those statements give factorization from proper lifts and remove properness for nice cones, including real PSD cones.

An unshifted PSD factorization of order r gives a shifted one of order r+1 by F'_U=diag(F_U,rho), G'_M=diag(G_M,1). Consequently fixing rho=1/2 gives rank_psd A_n(0)>=2^(cn)-1>=2^(cn/2) for large even n. This is an exact entry calculation; no approximate robustness assertion is transferred.

There is also a direct lift-to-odd-cut factorization derivation that avoids facet redundancy. Restrict a lift to the least face containing its feasible section. For PSD cones, that face has order r'<=r and the section contains a positive definite matrix on the common support: a finite sum of feasible matrices spanning the support, rescaled to a convex average, supplies one. Write its affine slice as A(Z)=b. Pull a tight odd-cut slack back to c+<C,Z>. Its minimum is zero. Slater duality supplies y with F=C-A*(y)>=0 and <b,y>=-c. Thus on the slice c+<C,Z>=tr(FZ). Choose G_M as a feasible preimage of each matching. This yields A_n(0)_{U,M}=tr(F_U G_M) without increasing cone order. Hence every exact affine lift has order at least rank_psd A_n(0). Degree equations and non-full-dimensionality cause no issue in this derivation.

The source's alternate facet-slack explanation is likewise sound: every redundant tight valid inequality on a polytope is a nonnegative combination of facet slacks modulo affine equations. Singleton odd cuts produce zero rows and are harmless. Its affine-to-linear translation absorption is valid since a non-point bounded image cannot arise from a slice containing zero; such a slice would be linear and its cone intersection a cone. A functional identically one on the remaining affine slice then absorbs the translation.

## 7. Reproducibility, strongest verified result, and limitations

Run `agent_notes/upstream_adversary_checks.py` with Python and NumPy (recorded version 2.3.5). The script writes `upstream_adversary_checks.json`, carrying reviewed central source hashes. It performs:

- Exact local-marginal and trace-formula checks by enumerating every ordered terminal list and internal matching for eleven small parameter choices.
- Three seeded, noncommuting 2-by-2 matrix instances of the complete binary two-stage tagged stack and spectral splitting construction. Maximum observed overlap-identity error is below 4e-16 and square-identity error below 4e-15. Potential and weighted Fourier-mass bounds pass.
- A three-input noncommuting PSD orthogonal-splitting check.
- The exact full degree-one parity moment-block and edge-disagreement check described above.

The rational checks are exact for their enumerated instances; the matrix checks are floating-point supplemental tests only. Neither finite computation proves the asymptotic bound; the proof reconstruction above is the relevant justification.

**Strongest verified result:** The source's explicit proof supports an absolute c>0 exponential exact real PSD-rank lower bound for every fixed 0<rho<1, and its scalar-block argument plus lift factorization supports an exponential exact real PSD-lift lower bound for the perfect matching polytope. No material unsupported assertion was found in this dependency chain.

**Exact remaining obstruction in this component:** None identified. This audit does not certify the TSP reduction or the novelty/publication claims. It also does not furnish a Lean proof of the exponential result. The actual scope file `lean/docs/126.md` says the linked formalization gives only superpolynomial unshifted/lift statements; I did not run Lean builds or treat comparator declarations as proofs. A later substantive source change requires a fresh audit against its changed hashes.
