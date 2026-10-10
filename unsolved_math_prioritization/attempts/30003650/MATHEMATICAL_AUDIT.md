# Independent mathematical audit: maximum finite CP-plus-rank

## Decision and exact scope

**Accept the theorem and fixed-ordinary-rank refinement. Accept the combined two-question target only as partial. No mathematical correction is required.**

For every positive integer n, the candidate proves p_n^+ = p_n, where p_n is the largest ordinary CP-rank of a nonzero completely positive n by n matrix and p_n^+ is the largest finite strictly-positive-factor rank. For every 1 <= r <= n it also proves P_(n,r)^+ = P_(n,r), with both maxima restricted to matrices of exact ordinary rank r. These are attained maxima. Singular matrices are included.

The candidate does not determine the maximum gap g_n in general. It does not give explicit numerical values of p_n for all n, prove equality of the two ranks for every individual matrix, or certify worldwide literature priority. This is a mathematical review of the supplied argument, not a formal proof-assistant certificate.

The reviewed proof has SHA-256 a2486250c2ddd7dc0e75cbf7275c59628a7b24f1f227e6432890369de96bacdb (11,301 bytes). The reviewed result summary has SHA-256 c0ef452c249188664e375b608188721b5de2276a78d4873bfa12ec8e0533f94b (2,521 bytes). Both were read completely and are authenticated by the candidate's 26-file inventory.

## 1. Definitions and finite minima

The convention A = BB^T requires an n by p factor B. Each column is an n-vector. Entrywise positive means every entry is strictly positive, rather than merely a positive-semidefinite Gram matrix or an entrywise positive Gram matrix. A positive Gram matrix alone does not suffice to invoke the negative-congruence argument: its hypothesis is an actual finite positive factor.

For any nonzero matrix in the relevant domain, the set of admissible positive integer column counts is nonempty. The well-ordering principle supplies a minimal column count. No closedness assertion for strictly positive factors is needed to obtain this minimum. A minimal nonnegative factor has no zero column, since deleting such a column leaves the Gram matrix unchanged and lowers its column count. A strictly positive factor already has no zero column.

The exclusion of the zero matrix is consistent with the original questions and avoids empty-factor conventions. The proof remains correct for n = 1: alpha = 1 and any allowed t <= 1/2 gives a positive scalar inverse.

## 2. Finite bounds and attainment without compact rank strata

The vector space of symmetric n by n matrices has dimension N = n(n+1)/2. If a finite conic rank-one decomposition has more than N nonzero terms, those rank-one matrices are linearly dependent. Pick a nontrivial dependence with a positive coefficient. Subtract its largest allowed nonnegative multiple from the current positive weights. At least one weight becomes zero, no weight becomes negative, and the represented matrix is unchanged. Repetition leaves at most N terms. Square-root rescaling preserves nonnegativity and, when applicable, strict positivity of the retained nonzero vectors.

Consequently ordinary CP-ranks form a nonempty subset of {1,...,N}. A largest realized integer exists. This is an attained maximum by the definition of that finite set of realized values, not an assertion of compactness of a matrix domain.

The same argument applies on each exact-rank stratum. It is nonempty, as a diagonal matrix with r positive diagonal entries has rank r. Although an exact-rank stratum is generally not closed, its realized CP-ranks still have an attained largest integer. This resolves a possible but unnecessary compactness concern.

## 3. Closed bounded-CP-rank sets

Fix k >= 1 and suppose A_m has a nonnegative factor with at most k columns and converges in the Euclidean space of symmetric matrices. Pad with zero columns to obtain n by k factors D_m. The exact identity

||D_m||_F^2 = trace(D_m D_m^T) = trace(A_m)

bounds D_m in a fixed finite-dimensional space. A convergent subsequence exists; its limit D is nonnegative. Matrix multiplication is continuous, so the limiting matrix is DD^T. Hence F_k = {A: cp(A) <= k} is closed. For k = 0 the claim is the singleton F_0 = {0}.

No positive definiteness of A_m or of the limit is used. This is ordinary sequential compactness of a bounded sequence of factors, not compactness of a family of strictly positive factors. If cp(A) = p, then A lies in the open complement of F_(p-1). Therefore every sufficiently small completely positive perturbation of A has CP-rank at least p. The inequality direction is correct: ordinary CP-rank cannot drop near the fixed matrix.

## 4. Negative congruence and positive pullback

Let A = BB^T with B > 0 and B of minimal positive width q. Let e be the n-vector of ones, J = ee^T, s_j the sum of column j of B, and

alpha = min_(i,j) B_ij/s_j.

Every s_j is positive; there are finitely many entries; thus alpha > 0. For each j the n ratios sum to 1, so alpha <= 1/n. If 0 < t <= alpha/2, then

B_ij - t s_j >= B_ij/2 > 0,

and 0 < t < 1/n. Thus T = I - tJ maps this particular positive factor to a positive factor. It is neither asserted nor needed that T maps the whole nonnegative cone to itself.

Since J^2 = nJ, direct multiplication gives

T^(-1) = I + [t/(1-nt)]J.

The coefficient is strictly positive. All off-diagonal entries of this inverse are positive, as are its diagonal entries; for n = 1 its sole entry is positive. For every nonzero nonnegative vector d, its coordinate sum is positive and

T^(-1)d = d + [t/(1-nt)](sum_i d_i)e > 0.

Set C = TAT^T. The factor TB proves cp^+(C) <= q. Let C = DD^T be a minimal nonnegative factorization. C is nonzero because T is invertible, and no column of D is zero by minimality. Every column of T^(-1)D is therefore strictly positive. Its Gram matrix is exactly A, not an approximation. The inequalities are

q = cp^+(A) <= cp(C) <= cp^+(C) <= q.

They force equality throughout. This argument applies for every parameter in the explicit positive interval, with no continuity theorem for cp^+ and no interior assumption. In particular, it applies to every singular positive-factor matrix. It immediately yields cp^+(A) <= p_n.

The positive-factor minimum is only needed for the sharpened equality cp(C) = cp^+(C) = q. For the global upper bound one could start with any finite positive factor, since a minimal nonnegative factor of C would still pull back to a positive factor of A of width at most p_n. There is no circular appeal to the existence of a maximum of cp^+.

## 5. Positive congruence and attained lower extremum

Let A = DD^T have minimal nonnegative width p. For t > 0, S = I+tJ is entrywise positive and invertible: its eigenvalues are 1 on e-perpendicular and 1+nt on the span of e. Every column of D is nonzero. It follows that SD is strictly positive, so

cp(SAS^T) <= cp^+(SAS^T) <= p.

The matrices SAS^T tend to A as t decreases to zero. Section 3 supplies cp(SAS^T) >= p throughout some sufficiently small positive interval. Both ranks consequently equal p in that interval. This is an actual family of positive-factor witnesses, rather than merely a limiting value which might not be attained.

Taking A to realize p_n proves p_n^+ >= p_n. Together with the upper bound this gives equality, and the same construction proves attainment of the positive maximum. Both congruences are invertible, so rank(TAT^T) = rank(SAS^T) = rank(A). Taking an ordinary maximum inside a fixed rank-r stratum and applying the two arguments inside that same stratum proves P_(n,r)^+ = P_(n,r).

For r < n, these witnesses are singular positive-semidefinite matrices and cannot be in the ambient interior of the completely positive cone. The proof deliberately retains them, rather than identifying finite positive factorization with ambient interior membership.

## 6. Gap statements and their limits

A nonzero finite positive factorization makes every entry of A strictly positive. The attributed low-rank and low-order equality theorem therefore applies to the candidate's entire domain, including its singular part. The source-dependent consequences used are listed with exact locators in the source metadata.

The retained gap conclusions are g_1 = g_2 = g_3 = 0; 0 <= g_4 <= 1; and 1 <= g_n <= p_n-3 for n >= 5. For an individual rank-r matrix, cp(A) >= r and cp^+(A) <= P_(n,r), giving the stated bound P_(n,r)-r. When A is positive definite, r=n and the weaker global bound cp^+(A)-cp(A) <= p_n-n follows. The latter is not exported to singular matrices.

For the bound involving p_n-3, split the cases explicitly: if cp(A) <= 2 then the gap is zero; otherwise cp(A) >= 3 and the new maximum theorem gives the bound. For n=4, p_4=4. For n>=5, p_n>n and the attributed gap-one witness gives the lower bound. For each n the nonempty set of realized gaps consists of bounded nonnegative integers, so the maximum g_n itself exists and is attained, even though its value is not determined here.

Row duplication preserves both factor ranks: extending a factor by the same repeated row gives one inequality, and restricting any factor of the enlarged Gram matrix to its original n rows gives the opposite inequality. Thus each gap at order n is realized at order n+1. This does not identify the maximum gap.

Crucially, the negative perturbation generally changes cp(A) to cp^+(A). Its success therefore does not prove cp(A) = cp^+(A) for the original matrix, nor solve the gap extremum by transforming it into a zero-gap witness.

## 7. Independent diagnostics and adversarial review

The audit used a new Python Fraction implementation of matrix arithmetic and forward-elimination rank. It imports neither candidate code nor SymPy. It replayed the 108 supplied records, including 84 rank-deficient cases, and checked another 385 exactly rational cases over orders 1 through 10: 330 negative-congruence cases at three distinct admissible fractions of alpha and 55 positive-congruence cases. Of the additional cases, 315 are singular. The new cases include redundant positive columns and nonnegative factors with zero entries. Row-duplication and principal restriction were also checked exactly.

Ten adverse controls reject or directly demonstrate the failures of singular, oversized, zero and negative parameters; zero and negative purported positive-factor entries; singular-map rank loss; oversized-map negativity; persistence of a zero column under a positive map; and loss of the positive-pullback argument when the inverse has the wrong sign. Ordinary Python, -O, and -OO give identical audit results. The proof does not rely on Python assertions.

These checks validate finite algebra, parameter handling and bookkeeping. They do not decide minimal CP-rank of arbitrary matrices, establish a universal extremum by enumeration, or certify nonexistence after unsuccessful optimization. Universal acceptance rests on Sections 1-5, not the numerical sample.

## 8. Source handling, notation and novelty

The original two questions were verified in the complete Dickinson contribution in Oberwolfach Report 52/2017, printed pages 3082-3083. The displayed p by n factor paired with BB^T is dimensionally inconsistent; the candidate's n by p convention repairs it consistently with the vector-sum definition. The original is preserved unchanged. [Original report](https://ems.press/content/serial-article-files/46715).

The complete BDS author manuscript is dated November 4, 2014 and corresponds to the 2015 journal article. Corollary 3.4 (p.4) supplies equality for n<=3 or cp<=2. Theorem 5.1(3)-(6), (11) and its proof (pp.7-8) supply the previous maximum bounds, ordinary values, and gap-one witnesses. Theorem 4.9 is interior-only. The paragraph before Lemma 5.2 explicitly leaves the all-order maximum equality open there. The audit verified these pages visually and read the complete relevant arguments; it does not label this manuscript the journal PDF. [Author manuscript](https://api.newton.ac.uk/website/v0/events/preprints/NI14088), [journal record](https://doi.org/10.1016/j.laa.2015.05.021).

The Lai-Yoshise paper uses the consistent column convention. Its conditional stationary-point conclusion and explicit algorithmic limitation do not certify factor nonexistence. It is not a mathematical dependency of the new extremum theorem. [Published paper](https://doi.org/10.1007/s10589-022-00417-4).

A bounded public search also inspected later primary-paper pages concerning the 5 by 5 cone and a 2026 factorization algorithm. This audit did not identify a prior all-order inverse-positive-congruence theorem in the inspected material. Neither this search nor the older manuscript's open-question statement proves that the result is new today. Acceptance is mathematical, with worldwide priority and exhaustive current-literature status expressly uncertified.
