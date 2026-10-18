# Independent full scoped-partial review: 30001781

## Verdict and binding version

**PASS_SCOPED_PARTIALS_ORIGINAL_UNSOLVED_5_OF_5.** No mathematical correction is required to the five frozen arguments. The original general-row conjecture remains unresolved. This verdict does not certify historical novelty, establish the conditional weak–strong comparison, or promote a transcription-error counterexample to an answer to the original.

The verdict binds author FROZEN_MANIFEST.json SHA-256 `2b0cd7b17d683dc313f2b052f1b9f2617d6b86f60fde11405d15b1b38795ca88`, RESULT.md `efc85d8c58523d527d6ffd139a8f46042706dd9724f4902513f06dd553d55a2e`, and TURN_5.md `dba3206a27b026f46a051e467d3ce9c4b2aa0ba7df26a1190234dfe2fe4b3922`. All38 bound author files and six full primary PDFs match, as do every historical manifest and all five replayed receipts. The separate standard-library checker passes53,069 exact controls with no floating-point diagnostics. Analytic proofs were audited separately from those finite tests.

There is a minor bibliographic correction, recorded in SOURCE_AUDIT.md: the OWR report's title is *Random Matrices, Geometric Functional Analysis and Algorithms*. RESULT.md incorrectly calls it *Asymptotic Geometric Analysis*. The actual contribution, report number, page range and mathematical target are correct. The frozen files stay unchanged; this supplement supplies the correction transparently. The2024 paper's exact title likewise ends in *variables*, not *matrices*.

## 1. Exact original target

I read the complete Litvak contribution on OWR24/2011 pp.1343–1344 and visually checked both pages. The rows are independent isotropic log-concave vectors in R^N, initially coordinatewise unconditional, and their laws need not coincide. The matrix statistic is the maximum Euclidean operator norm over k-row, m-column submatrices. Padding supports gives the equivalent sparse bilinear supremum.

The two factors are sqrt(m) times log(3N/m), and sqrt(k) times log(3n/k). The logs are outside the square roots. The report asks whether unconditionality can be removed. It gives qualitative high-probability language, not a fully specified new tail convention. The2012 published Theorem4.2 provides the precise additive-tail benchmark used by the author under its own stronger hypotheses.

The exponential-entry computation correctly refutes only the malformed imported scale. In particular, at k=m=1 the maximum of nN independent variance-one Laplace magnitudes has CDF `(1-exp(-sqrt(2)u))^(nN)`. For n=N=d, any threshold of order sqrt(log d) is insufficient; this says nothing against the actual order-log d source bound. The false arbitrary-norm Chevet extension is also correctly kept separate from the more specific maximal-submatrix question.

## 2. Turn1: common coisometric images

The whole latent matrix Gamma is an isotropic unconditional log-concave vector: independence combines the row laws into a product, and the centered cross-row covariances vanish. Thus the exact full-matrix hypotheses of the final Chevet Theorem3.1 and Corollary3.2 apply. No assertion of unconditionality for Gamma T* is used.

For the column body K=T* conv U_m(N), TT*=I makes T* an isometric embedding, so R(K)=1. The row polar body has radius one as well. The coordinate radii are at most one, giving sigma=1 and sigma-prime≤1. The two exponential widths really are E||T E_D||_(m) and E||E_n||_(k); their dimensions are not silently substituted.

The marginal subexponential estimate for each coordinate of T E_D is dimension-free. For a unit coefficient vector, the Laplace MGF is a product of `(1-s²a_j²/2)^(-1)`. A sufficiently small fixed s bounds its logarithm by a constant times s² sum a_j². Chernoff and the deterministic top-m tail-count identity then bound the squared width by C m log²(3N/m). Dependence between the transformed coordinates is immaterial; the tail-count expectation is a sum of marginal integrals.

The D>N issue is explicitly closed rather than ignored. For fixed D, K+epsilon B_2^D is a valid symmetric convex body. Its radius and width converge to the required limits. The epsilon=1 supremum is integrable by the same source theorem, allowing dominated convergence. For tails, the author compares the strict event at a limiting deviation t with the regularized event at t'<t, then passes epsilon down and t' up. This avoids an unjustified limiting event at an atom and removes the latent-dimension error before stating the dimension-free result.

The displayed two-dimensional rotation genuinely destroys coordinate unconditionality: the two L1 values are13/5 and3. Isotropy and log-concavity survive the coisometry. All these claims retain the common-map restriction; they do not cover unrelated T_i.

## 3. Turn2: asymmetric Dirichlet rows

For a centered matrix B, conditional Jensen applied to the convex function N^p gives E N(B)^p≤E N(B-B')^p. The maximal selected-submatrix statistic is indeed a norm for k,m≥1. Independent scalar differences, normalized by sqrt(2), produce the unconditional latent matrix needed for Turn1. Only central symmetry is asserted for a general symmetrized dependent-coordinate row; the stronger scalar independence step is used precisely where available.

For alpha_ij=c_i alpha_j≥1, the common null vector is proportional to the coordinate square roots of alpha_j and is independent of i. The stated common U therefore kills each mean after diagonal rescaling. Direct covariance multiplication gives I_N. The affine map from the simplex is injective: the kernel of U diag(alpha_i)^(-1/2) is span(alpha_i), whose intersection with the tangent hyperplane sum h_j=0 is zero. This proves full-dimensional log-concavity of the image; density exponents alpha_ij−1≥0 are essential and retained.

The Gamma change of variables has Jacobian s^(D−1), and the density factors into Gamma(a_i,1) for S_i and the Dirichlet density for P_i. Thus S_i is independent of P_i, hence of X_i, but not of the unnormalized Gamma coordinates. The proof uses only the valid independence. Different rows remain independent under the construction.

The exact identity Y_i=S_i X_i/sqrt(a_i(a_i+1)) and deterministic coefficient d_i=sqrt((a_i+1)/a_i) yield E[d_i Y_i | all X]=X_i. In particular the product of coefficients is S_i/a_i, whose conditional mean is one. Since a_i≥D≥2, max d_i≤sqrt(3/2). Jensen and deterministic diagonal-row multiplication transfer all moments from the already controlled latent scalar matrix to A. This works for every sample size n and needs no event controlling all random denominators.

The all-real-p bound follows from the source tail integral. The reverse moment-to-tail conversion is valid after increasing the baseline multiple: large deviations use p proportional to t, while the p=1 bound gives a fixed probability below one for the bounded small-t interval. A sufficiently small universal c yields exp(-c min(t²,t)). This is a tail above a multiple of Lambda, not concentration about the exact mean.

The isotropic regular-simplex example has vertex squared radius N(N+2), covariance identity and no central symmetry for N≥2. It really extends beyond the symmetric exact-latent laws of Turn1. Arbitrary row-specific weight ratios or orientations would change U and are not included.

## 4. Turn3: flat tests and the deterministic obstruction

For a fixed unit column direction, the row projections are independent centered variance-one log-concave scalars. Their uniformly controlled moments imply the Bernstein MGF regime `|theta| max|u_i|≤c`, with quadratic variance sum u_i². For a normalized flat s-support vector, this gives the stated min(t²,t sqrt(s)) exponent.

The signs, row supports and half-nets contribute at most exp[ s log(2en/s)+m log(5eN/m) ] tests. A union bound at a sufficiently large multiple of sqrt(H+v)+(H+v)/sqrt(s), followed by the linear-functional net factor two, gives the claimed uniform bound. When s≥m, m/sqrt(s)≤sqrt(m), so both entropy contributions simplify to the stated sharp scale. That simplification is not valid for all s<m; the packet explicitly retains the larger term there.

The harmonic vector has Euclidean norm sqrt(H_k) but every flat signed test is at most two. Pairing a putative flat-atom expansion with this vector gives the lower bound sqrt(H_k)/2 on total coefficient mass. The layer-cake representation and Cauchy–Schwarz give the complementary O(sqrt(log k)) upper bound. The elementary inequality `(sqrt(s)-sqrt(s-1))²≤1/s` is in the correct direction. This is a deterministic obstruction to a dimension-free atomic reduction, not an admissible random-matrix counterexample or a lower bound on what stochastic chaining could achieve.

## 5. Turn4: all profiles for one column

The independent, nonidentically distributed exceedance argument is sound. For the ell-th largest absolute projection, an ell-subset union bound gives binomial(n,ell) times a common exponential tail to the ell-th power. Choosing t_ell=C[log(en/ell)+v/ell] leaves a summable exp(-2ell-2v) bound. This is a union over order statistics, not a false claim of independence among the order statistics themselves.

The logarithmic square sum is bounded using the decreasing integrable function log²(1/x), whose integral on (0,1) is2; sum ell^-2≤2 handles the additive v term. The resulting top-k norm bound includes every coefficient profile through Euclidean duality on each row support. This directly closes the nonflat issue for a fixed column direction without reusing the failed flat-atom domination.

A union over coordinate columns gives the sharp m=1 order. For general m, the half-net has exp(H_m) points, where H_m=m log(5eN/m). The map y↦Ay is linear into the normed space whose norm is the top-k Euclidean norm. Hence its operator norm is at most twice the net maximum, giving the claimed general elementary bound. The row-dominated regime is correctly conditional on H_m≤C_2 b_k with a fixed numerical C_2. Constants may depend on that specified C_2. The general column-entropy term is too large and is explicitly not presented as an improvement on the2014 theorem.

## 6. Turn5: the precise k=1 reduction

The Q/T/M equivalence is correct for any family of nonnegative random variables with associated a≥1; no log-concavity is needed for the equivalence itself. The constants must be uniform in the family member and sample size, exactly as stated.

For Q⇒T, n=floor(exp(t)) is at least exp(t)/2. The event with the larger threshold C_Q(a+1+t) has probability at least1/2 for the iid maximum. Writing its exact probability as (1-q)^n handles atoms correctly because q uses strict exceedance. It implies q≤log(2)/n. Absorbing the added1 into a+t uses a≥1 and yields the advertised tail. T⇒Q is a union bound and needs no independence; it also proves the nonidentical-row consequence when each row has the same uniform tail bound.

Markov establishes M⇒T, with the t<1 range handled explicitly by enlarging the threshold. Tail integration and Minkowski establish T⇒M for all real p≥1. One can verify the elementary Gamma estimate without an integer restriction by comparing the Lp norm of an exponential variable to the Lceil(p) norm, which is at most ceil(p)≤2p.

For k=1, A_(1,m) is exactly the maximum of the row top-m norms. The top-m norm is the support function of conv U_m, so the dual unit ball is precisely that body. It lies in the Euclidean unit ball; isotropy plus scalar log-concave moment bounds control every one-dimensional functional by Cp. Thus the stated weak–strong comparison, if available with a universal constant, would imply M. It is not proved in the packet, and no source-era conjecture label is turned into a present-status theorem.

I checked Latała's Conjecture12 and its nearby theorems. The ell_r statement retains its r factor and embeddings retain distortion; the coordinate-maximum theorem assumes isotropy of that whole vector. The collection of all sparse projections need not meet that hypothesis. Even the conditional one-row consequence leaves an exponentially large family of row coefficient profiles when k>1, so it cannot by itself close the full target. The remaining gap is correctly stated.

## 7. Source hierarchy, tests and publication boundary

The final2012 Chevet theorem and tail corollary were read in full, including their proof and parameter definitions. The pinned2014 author manuscript's exact Theorem5.1 and lambda formula were checked both textually and visually. The2014 general-row result retains the extra sqrt(loglog(3m)), max(N,n), and tail denominator sqrt(log(3m)) exactly as the packet records. The final2024 comparison still assumes unconditionality in the relevant result. These citations support the scoped arguments; the limited literature search does not prove worldwide openness.

All five receipts replay byte-identically in separate copies:12,911;3,374;30,449;14,132;999 controls. The independent53,069 controls reconstruct additional rational coisometries, fractional-shape Gamma/Dirichlet joint moments, conditional scaling, tail-count inequalities, nonidentical exceedance probabilities, maximum CDFs with atoms, top-k support identities and a distinct dyadic flat-test obstruction. Their finite character is explicit.

The author has completed five substantive turns. The appropriate original status is **unsolved5/5**, accompanied by these scoped positive results and reductions. Publish the frozen public author files plus this portable review/citation correction; omit PDFs, extracted text, page images and replay copies. Parent retains publication authority.
