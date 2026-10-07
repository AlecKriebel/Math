# Independent mathematical review: random free-product quotients and property (T)

Problem 30006628; OWR-14299911-031; rank 924. Review date: 2026-10-06.

## Verdict and exact object accepted

**ACCEPT the frozen proof for its stated theorem.** I found no mathematical gap requiring a correction. The argument establishes property (T) with probability tending to one for the free-product density model with at least three fixed nontrivial finitely generated factors, fixed finite generating sets and ball radius, and fixed density strictly between 1/3 and 1. The limit runs through all positive integer relator lengths, rather than only multiples of three. This is an asymptotic assertion, not an assertion about every individual finite presentation or finite length.

The accepted proof is the 19,961-byte `PROOF.md` with SHA-256:

`3bed7a81c5562d793bc4991fe62e1c06703818a9046495a7fe96d0b38e1ac100`

It is contained in the 20,225-byte `RANDOM_PROPERTY_T_30006628_AUTHOR_SAFE_FREEZE.zip`, SHA-256:

`f5c4e06b7c535a98aa37520ff616b4b63b4bdd7eb100e461de733f7fd7192134`

The supplied 3,285-byte external manifest has SHA-256:

`46011dfd09c59dc52c561886c31b0e8ed0c823f5d5f446baf2c5aa35448fdaf0`

All twelve archive members were checked against that external manifest. The separately supplied proof was compared byte-for-byte with the archived proof. No original was edited, no correction patch is proposed, and no GitHub write was performed in this review.

This is an AI-authored mathematical review, not formal verification, human peer review, or journal acceptance. Its acceptance rests on the full argument below and the checked hypotheses of the cited theorems. The finite diagnostics are supplementary and cannot certify an asymptotic proof. I did not use another auditor's verdict as evidence for acceptance.

## 1. Source statement and scope

The primary OWR report, Problem 16 on printed pages 535-536, asks about property (T) above density 1/3 for free products of **at least three factors**. That is the target answered by the candidate. [OWR]

Definition 1.1 of *Random Quotients of Free Products*, arXiv:2502.08630v2, supplies the precise model: finite balls of nonidentity factor elements; syllable-normal-form words; distinct factors at successive syllables and at the cyclic boundary; and uniform sampling with replacement. The candidate's use of the integer part of the specified relator count is harmless. Its sample space is the collection of actual syllable words, not rotation classes, inverse classes, arbitrary spelling words, or independent uniformly selected factors. [FPD]

Question 1.9 in that preprint is written for a model allowing two factors. Acceptance here is **not** acceptance of that entire question. In fact, the same source's Remark 1.3 says the two-factor sample space is empty at odd lengths. For example, two infinite cyclic factors leave a free group of rank two at every odd length, so an unrestricted all-length extension to two factors cannot follow. The candidate explicitly avoids this issue.

The public arXiv landing page was inspected during this review and records v2 on September 28, 2026, with the comment that the paper is to appear in Transactions of the AMS. That bibliographic status is not a certification of the new candidate proof.

The claim keeps all factor alphabets fixed while the relator length tends to infinity. The proof does not establish a uniform rate as the number of letters or factors changes. No conclusion is asserted at the critical density 1/3.

## 2. Alphabet counting and the Perron spectrum

Let A be the adjacency matrix on the finite disjoint syllable alphabet, with an edge precisely between different factors. Because there are at least three nonempty parts, the graph is connected and nonbipartite. A nonnegative connected undirected graph with an odd cycle has primitive adjacency matrix. Its Perron eigenvalue lambda is therefore simple, and every other eigenvalue has absolute value strictly below lambda.

The candidate's stronger sign assertion is correct. On the codimension-one space of vectors with total coordinate sum zero,

    z^T A z = - sum_i (sum_{a in B_i} z_a)^2 <= 0.

Consequently A has at most one positive eigenvalue. Its Perron eigenvalue is positive, so all remaining eigenvalues are nonpositive. A three-vertex principal submatrix is the adjacency matrix of a triangle, giving lambda >= 2. The Perron vector is constant within each factor, because the corresponding rows of A are identical. In particular inversion of a letter preserves its Perron coordinate.

The stochastic matrix P[a,b] = A[a,b] r_b/(lambda r_a) is similar to A/lambda, and is reversible for the strictly positive measure r_a^2. Thus its nonprincipal eigenvalues belong to (-1,0]. Writing rho for the negative of its least eigenvalue gives rho < 1. That strict inequality is indispensable in the two unequal-length residues.

The number of reduced words of length t with endpoints a,b is exactly (A^(t-1))[a,b], including t=1 with A^0. The number of cyclically reduced syllable words is exactly trace(A^ell). These identities use the free-product normal-form theorem and count the specified sample space without any extra factor for rotation or inversion. Symmetric-matrix diagonalization yields the stated uniform Perron asymptotics, since the alphabet is fixed.

**Finding:** Section 2 is valid, including the probability denominator and the needed strict spectral margin.

## 3. Inverse-fixed words, reversal, and retained samples

For an even reduced length, equality of a word and its inverse forces its middle two syllables to be inverses. They would belong to the same factor, contrary to reduction. Thus there are no inverse-fixed even-length blocks.

For length 2s+1, an inverse-fixed block is determined by its first s syllables and its middle letter, which must have order two. This bounds the number removed by a constant times lambda^s. It does not require that each factor be torsion-free, nor does it presume any particular number of involutions. Compared with the positive leading endpoint count of order lambda^(t-1), this is exponentially negligible, uniformly over the finitely many endpoint classes. Every class is therefore eventually nonempty.

For completion counts, summing over all reduced h-blocks gives A^(h+1). Removing the inverse-fixed blocks changes any entry by at most their total number. This proves the required uniform asymptotic for T_h.

The exact symmetry of T_h deserves attention. Inverting a retained word exchanges its endpoint factors. Since adjacency depends only on the factor and inversion preserves factors, the bijection w -> w^(-1) exchanges the constraints defining T_h(p,q) and T_h(q,p). Thus the symmetry claimed in the proof is exact, even when not every letter is self-inverse. It also follows directly that T_h depends only on the factors of p and q.

A sample is discarded or retained using only that sample. This deterministic thinning does not destroy independence between samples. The argument does not claim that all sampled relators are retained, nor does it replace the sampling law by a conditional uniform law. Discarded samples are represented by zero matrices, and the exact denominator stays Z_ell.

**Finding:** The treatment of arbitrary factor torsion, inverse-fixed blocks, and reversal is valid.

## 4. The triangular group and its finite-index image

The block-length patterns (L,L,L), (L,L,L+1), and (L,L+1,L+1) cover all residues. Taking one formal generator for each inverse pair in the retained block alphabet is legitimate because inverse-fixed words have been removed. Different reduced lengths cannot represent the same element of the original free product. The presentation need not retain relations internal to the factor groups: it maps onto the subgroup generated by the block images in the desired quotient.

Each retained relator yields a formal length-three relation. If two adjacent formal letters canceled, the corresponding adjacent blocks would be inverse normal forms. The meeting syllables would then lie in the same factor. That is forbidden at all three cyclic boundaries of the original sampled word. Thus every triangular relator is cyclically reduced and the associated link has no loops.

Here is a direct verification of the deterministic index argument. Let H_0 be generated by the retained length-L blocks. For letters a,b choose a factor C distinct from both their factors. For even L, any reduced suffix v of length L-1 starting in C makes both av and b^(-1)v admissible retained L-blocks. For odd L >= 5, choose v with first and last factors both C. A four-letter factor pattern C,D,E,C exists with three distinct factors. Appending D,C adds two syllables while preserving reduction and the endpoint factor C, giving every needed even suffix length. Both full blocks have different first and last factors, so neither equals its inverse. In either case,

    (av)(b^(-1)v)^(-1) = ab.

Thus H_0 contains every product of two alphabet letters. The subgroup K generated by these products is normal, since for any letter c,

    c(ab)c^(-1) = (ca)(bc^(-1)) in K.

All quotient images of letters are equal and have square equal to the identity. Because the alphabet generates the whole free product, its quotient by K has order at most two. Hence H_0 has index at most two, and its image in the sampled quotient does also. The construction holds for all sufficiently large lengths, which is sufficient for the claimed limit.

This avoids a potentially invalid transfer between random models on arbitrary factors and on free factors. No such transfer is needed here. The abstract triangular group maps onto a subgroup of index at most two of the desired random quotient for **every realization**, before any probability estimate.

**Finding:** The group-theoretic bridge is complete. It applies even when the factors are infinite, have torsion, or are not finitely presented.

## 5. Exact expected-link kernel and multiplicities

The candidate's link convention has edges {u^(-1),v}, {v^(-1),w}, {w^(-1),u}. Applying inversion to every vertex gives exactly the convention in Definition 2.12 of Kotowski-Kotowski. It preserves the spectrum.

Fix x of length t and y of length u. An oriented corner in which the first block is x^(-1) and the second is y is legal at their common boundary precisely when their first endpoint factors differ, giving A[f(x),f(y)]. The remaining block has length h = ell-t-u and must satisfy the two remaining boundary conditions. Its number of allowed choices is T_h[l(x),l(y)], using the exact symmetry checked above.

For a reversed edge orientation, the roles of the first two blocks are reversed; the same factor condition and symmetric completion count result. This also works when the types differ and the fixed cuts are not preserved by a cyclic rotation: one counts each corner at its own fixed position. For a specified corner and specified blocks, every allowed completion determines exactly one original syllable word.

The oriented type counts are:

    ell = 3L:       C = [6]
    ell = 3L+1:     C = [[2,2],[2,0]]
    ell = 3L+2:     C = [[0,2],[2,2]].

These count six oriented incidences per retained triangle, rather than three independent edges. They give exactly

    Ebar[x,y] = (N_ell/Z_ell) c_tu A[f(x),f(y)] T_(ell-t-u)[l(x),l(y)].

This identity remains correct when several corners or repeated sampled relators produce the same undirected edge: multiplicities add. For x=y its adjacency factor is zero, consistent with the absence of loops. For y=x^(-1), any parallel edges are counted normally.

Summing over destination words and inserting the endpoint asymptotics gives the exponent ell-t+1 in the expected degree. Specifically, the factors from destination length and completion length give lambda^(ell-t); summing A[a,c]r_c gives one more factor lambda r_a; and the other endpoint sum is sum_f r_f^2 = 1. This yields the candidate's formula, including its factor h_t = sum_u c_tu.

Since N_ell is comparable to lambda^(d ell), the minimum expected degree is bounded below by a fixed positive constant times lambda^(d ell-ceil(ell/3)). The number of vertices is at most a fixed constant times lambda^ceil(ell/3). Therefore minimum expected degree grows exponentially, whereas log of the number of vertices grows only linearly.

**Finding:** The exact kernel, degree exponent, multiplicities, and model probability normalization are correct.

## 6. Endpoint compression and all residue spectra

All vertices with the same block type and endpoint letters have identical rows in the mean walk. Its image lies in the space of endpoint-class-constant functions. The induced finite matrix has entries equal to the per-vertex transition multiplied by the destination class size. The remaining eigenvalues of the full mean walk are zero. Reversibility follows either from the original symmetric adjacency matrix or from detailed balance with class-size times expected-degree weights.

For each residue, the number of labels is fixed once the alphabet is fixed. The limiting transition is

    Q[t,u] P[a,c] r_f^2,

independent of the previous last letter b. The final-coordinate transition is the rank-one Markov matrix R[b,f]=r_f^2. Thus the limit is Q tensor P tensor R, exactly as claimed.

The equal-length type matrix is [1]. The unequal-length type matrices have eigenvalues 1 and -1/2. Combining these with the spectrum of P and the spectrum {1,0} of R gives:

- a simple principal eigenvalue 1 in every residue;
- nonprincipal eigenvalues at most zero in the equal-length limit;
- nonprincipal eigenvalues at most rho/2 in either unequal-length limit.

In particular, the positive products of two negative eigenvalues are included. Ignoring them would give an incorrect estimate, but the candidate does not ignore them. Since rho < 1, their upper bound is strictly below 1/2.

For extra confirmation of the reversible limit, its stationary weight at (t,a,b) is proportional to h_t r_a^2 r_b^2. Indeed, the type balance is h_t Q[t,u] = c_tu = c_ut. All those weights are strictly positive. This also makes clear why unequal class sizes do not introduce an omitted lambda factor in Q.

Entrywise convergence in fixed dimension implies spectral convergence. Equivalently, one may conjugate by the convergent positive stationary weights to obtain convergence of real symmetric matrices. The limit's isolated eigenvalue 1 remains the unique principal eigenvalue eventually. The extra zero eigenvalues in the full walk do not reduce the Laplacian gap below the stated bound.

The proposed gamma = 1/2 + (1-rho)/4 leaves a positive margin below the worst limiting gap 1-rho/2. Taking the largest of the three residue-dependent length thresholds gives a common eventual bound.

**Finding:** The mean spectral gap is proved uniformly over the three residues for each fixed alphabet. There is no omitted equal-length assumption.

## 7. Matrix concentration with dependent corner edges

This is the essential probabilistic step, and the independence requirement is satisfied at the correct level. The three corner edges of a sampled triangle are generally dependent. The proof packages them into one matrix L_j, the unnormalized Laplacian contributed by that sample. Samples, and therefore the matrices L_j, are independent.

Every L_j is positive semidefinite and is a sum of three edge Laplacians, each of norm two. Its norm is at most six, even when edges coincide. Discarded samples give zero. Every L_j kills the constant vector. After deterministic normalization by the expected degrees,

    X_j = Dbar^(-1/2) L_j Dbar^(-1/2),

the summands remain positive semidefinite, have norm at most 6/delta_ell, and all kill the same deterministic vector z=Dbar^(1/2)1. The orthogonal complement of z is invariant because the matrices are self-adjoint. Their restrictions therefore meet the hypotheses of Tropp's matrix Chernoff inequality. The expectation sum on that subspace has smallest eigenvalue at least gamma. [Tropp]

With R=6/delta_ell, the lower-tail exponent from Remark 5.3 is epsilon^2 gamma delta_ell/12. The dimension is M_ell-1, so the candidate's prefactor M_ell is a valid weakening. Using gamma in place of a possibly larger true minimum expectation eigenvalue only weakens the threshold and bound. The estimate is consequently valid without independent matrix entries or edges.

The scalar degree bound also uses the right sample size. Each occurrence of a block puts one endpoint at that block and one endpoint at its inverse, in the two neighboring corners. Since these are distinct formal vertices, a fixed vertex can receive at most one incidence from each of the three block occurrences. Its degree contribution is at most three. Scalar Chernoff applied after division by three gives the stated exponent epsilon^2 delta_ell/9. A union bound over vertices needs no independence between their degrees.

Both failure probabilities go to zero because exponential expected-degree growth dominates the linear logarithm of the matrix dimension. The proof works at every fixed d>1/3, however small its distance from 1/3, by choosing sufficiently large ell.

**Finding:** Section 6 supplies actual random-matrix concentration, not merely a calculation of expected spectrum. No false edge-independence hypothesis is used.

## 8. Actual normalization, connectivity, and the spectral criterion

On the concentration event, the candidate first obtains coercivity on the hyperplane f^T Dbar 1 = 0. If the actual graph were disconnected, its Laplacian kernel would have dimension at least two, and would contain a nonzero vector in that hyperplane. This contradicts coercivity. Thus the actual graph is connected; since it has more than one vertex eventually, all actual degrees are positive.

It is valid to compare the two degree matrices using only the upper bound D <= (1+epsilon)Dbar. On the chosen hyperplane,

    (f^T L f)/(f^T D f) >= (1-epsilon)gamma/(1+epsilon).

The generalized Courant-Fischer formula for the second eigenvalue maximizes this minimum over all codimension-one subspaces. It is therefore legitimate to select the Dbar-centered hyperplane. It need not equal the D-centered hyperplane. This is not an invalid substitution of orthogonality conventions.

The stated condition epsilon < (2gamma-1)/(2gamma+1) is exactly the algebraic condition making the last ratio greater than 1/2. Hence the actual link is connected and has normalized Laplacian gap greater than 1/2 with probability tending to one.

I checked Definition 2.12 and Theorem 2.13 against the cited Kotowski-Kotowski v2 PDF itself, including a rendered view of its page 7. The definition explicitly allows multiple edges, disallows loops for cyclically reduced relators, and uses the degree-normalized Laplacian. The candidate satisfies those requirements. Repeated relation occurrences may be kept as repeated triangular cells without changing the presented group; their corner incidences are counted with multiplicity. The theorem applies to this finite triangular presentation. [KK]

Consequently the triangular group has property (T). Its block-image subgroup is a quotient, and the whole target group is a finite extension of that subgroup. Quotient stability and finite-index equivalence of property (T), stated in Remarks 2.10 and 2.11 of the same source, complete the proof.

**Finding:** The final probabilistic-to-group-theoretic implication is valid, including actual rather than expected normalization, loops, multiple edges, and finite-index transfer.

## 9. Supplementary independent diagnostics

A separate checker was written for this review. It exhaustively constructs cyclic syllable words and counts the actual link at the individual-word-vertex level, rather than only at the compressed endpoint-class level.

It checked 23 cases with factor alphabet sizes (1,1,1), (2,1,1), and (3,2,1), both all-self-inverse and mixed paired inversion where applicable, and lengths covering all three residues. Across these cases it examined 431,578 cyclic words and verified 50,652 individual entries of the exact expected-link kernel. It also checked total oriented edge mass, exact completion reversal, absence of loops, the per-sample degree bound, and 190 samples producing parallel edges. All twelve frozen archive members and the original proof were checked against the supplied pins.

The checker passed under both ordinary Python and Python with optimizations enabled. Its two JSON outputs are byte-identical. These are finite exact diagnostics. They do not prove Perron convergence, tail estimates, the spectral criterion, or the asymptotic property-(T) conclusion. Those steps were reviewed mathematically in Sections 2-8 above.

## 10. Literature and publication boundaries

The adjacent Ashcroft result concerns uniform random elements in word-metric annuli of non-elementary hyperbolic groups; it is not identified without proof with the exact cyclic syllable sample space here. The September 2026 Oppenheim preprint concerns the Gromov model along relator lengths divisible by four. Neither is used as a proof dependency of the candidate. Their relevant statement pages were inspected, and their PDF hashes were checked. [Ashcroft] [Oppenheim]

A narrow live literature check did not identify a prior resolution of this exact statement. This review does not establish exhaustive novelty. Its mathematical acceptance is separate from any novelty or publication decision. The target problem's live webpage was not independently accessible in this review; the actual primary OWR statement supplies the scope.

The safe review bundle contains this authored mathematical report, the independent checker and its outputs, and public bibliographic and verification metadata only. It contains no source PDF, extracted source text, dataset contents, private personal information, or private coordination material.

## Public references

[OWR] *Median Geometry and Applications*, Oberwolfach Reports 23 (2026), Report 8, pp. 487-540; Problem 16, pp. 535-536. https://doi.org/10.4171/owr/2026/8 . Public PDF: https://ems.press/content/serial-article-files/53603 .

[FPD] E. Einstein, S. Krishna M S, M. Montee, T. Ng, M. Steenbock, *Random Quotients of Free Products*, arXiv:2502.08630v2. Definition 1.1, Remark 1.3, Question 1.9. https://arxiv.org/abs/2502.08630v2 . Current landing page: https://arxiv.org/abs/2502.08630 .

[KK] M. Kotowski, M. Kotowski, *Random groups and Property (T): Zuk's theorem revisited*, arXiv:1106.2242v2; Journal of the London Mathematical Society 88 (2013), 396-416. Definition 2.12, Theorem 2.13, Remarks 2.10-2.11. https://arxiv.org/abs/1106.2242v2 ; https://doi.org/10.1112/jlms/jdt024 .

[Tropp] J. A. Tropp, *User-friendly tail bounds for sums of random matrices*, arXiv:1004.4389v7; Foundations of Computational Mathematics 12 (2012), 389-434. Corollary 5.2 and Remark 5.3. https://arxiv.org/abs/1004.4389v7 ; https://doi.org/10.1007/s10208-011-9099-z .

[Ashcroft] C. J. Ashcroft, *Property (T) in random quotients of hyperbolic groups at densities above 1/3*, arXiv:2202.12318v2. Theorems A and B. https://arxiv.org/abs/2202.12318v2 .

[Oppenheim] I. Oppenheim, *Property (T) for random groups in the density model with d > 1/4*, arXiv:2609.21255v1. Definition 1.1 and Theorem 1.2. https://arxiv.org/abs/2609.21255v1 .
