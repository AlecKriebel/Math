# Positive congruence removes the extra column in the maximal CP-plus-rank bound

## Scope and conclusions

For an integer n >= 1, let CP_n be the cone of real symmetric matrices A admitting A = BB^T with B entrywise nonnegative. The factor B is n by p. Define cp(A) as the least such p and cp^+(A) as the least p for which B is entrywise strictly positive. We consider nonzero matrices with finite cp^+(A), including singular matrices. Write

- p_n = max { cp(A) : 0 != A in CP_n };
- p_n^+ = max { cp^+(A) : 0 != A and cp^+(A) < infinity };
- g_n = max { cp^+(A) - cp(A) : 0 != A and cp^+(A) < infinity }.

The main result proved here is

**Theorem. For every n >= 1, p_n^+ = p_n.**

This equality also holds separately on every fixed ordinary-matrix-rank stratum. The proof does not assume positive definiteness, and does not extend an ambient-interior continuity theorem to boundary points.

This determines the second CP-plus extremum in terms of the ordinary maximum p_n. It does not compute the still difficult ordinary CP-rank maximum as an explicit integer for every n. In particular, the established ordinary values give p_n^+ = 1, 2, 3, 4, 6 for n = 1, 2, 3, 4, 5 respectively.

The first extremum g_n is **not determined in general by this note**. The bounds and exact small-order conclusions proved or explicitly attributed below are only partial results for that separate question.

## 1. Elementary facts used in the proof

### Lemma 1: finiteness and attainment of the ordinary maximum

Every nonzero A in CP_n has cp(A) <= N := n(n+1)/2. Consequently p_n is a well-defined attained positive integer.

Proof. Start from any finite decomposition A = sum_i v_i v_i^T, v_i >= 0, omitting zero vectors. If it has more than N terms, its rank-one symmetric matrices are linearly dependent. For coefficients c_i, not all zero, satisfying sum_i c_i v_i v_i^T = 0, reverse the signs if necessary so that some c_i > 0. More generally, for current positive weights w_i, choose t = min_{c_i>0} w_i/c_i. Replacing w_i by w_i - t c_i preserves the represented matrix, keeps all weights nonnegative and sets at least one weight to zero. Remove zero weights and repeat. Absorb the square roots of the remaining weights into the vectors. There are at most N remaining terms. The nonempty set of possible cp-ranks is thus a subset of the finite set {1,...,N}, and its largest element is attained. The same reduction preserves strict positivity of retained vectors when the starting vectors are strictly positive. QED.

### Lemma 2: closedness of bounded CP-rank sets

For each integer k >= 0, F_k := { A : cp(A) <= k } is closed in the Euclidean space of real symmetric n by n matrices, with F_0 = {0}.

Proof. Let A_m in F_k converge to A. Choose n by k matrices D_m >= 0 with A_m = D_m D_m^T, padding shorter factors with zero columns. Their squared Frobenius norms satisfy ||D_m||_F^2 = trace(A_m), hence are bounded. A subsequence converges to a nonnegative n by k matrix D. Continuity gives A = DD^T, so A in F_k. This argument includes singular limits. QED.

It follows that if cp(A) = p < infinity, there is a neighborhood of A disjoint from F_(p-1). Therefore cp cannot decrease under sufficiently small perturbations that remain completely positive.

### Lemma 3: a strictly positive inverse

Let e be the n-vector of ones and J = ee^T. For 0 < t < 1/n, put T_t = I - tJ. Since J^2 = nJ,

T_t^(-1) = I + [t/(1-nt)]J.

In particular, T_t is invertible and T_t^(-1) is entrywise strictly positive. Every nonzero nonnegative vector d is therefore sent to a strictly positive vector T_t^(-1)d. Also S_t := I + tJ is invertible and entrywise strictly positive for every t > 0.

## 2. A boundary-inclusive perturbation theorem

### Theorem 4: both ranks can be made equal without changing ordinary rank

Let 0 != A in CP_n and p = cp(A). For all sufficiently small t > 0,

cp(S_t A S_t^T) = cp^+(S_t A S_t^T) = p.                 (1)

If q = cp^+(A) is finite, then for all sufficiently small t > 0,

cp(T_t A T_t^T) = cp^+(T_t A T_t^T) = q.                 (2)

All matrices in these two families have the same ordinary rank as A.

Proof of (1). Choose a minimal nonnegative n by p factor D of A. Each of its columns is nonzero; a zero column would contradict minimality. Since S_t is strictly positive, S_t D is strictly positive. Thus

cp(S_t A S_t^T) <= cp^+(S_t A S_t^T) <= p.

As t decreases to zero, S_t A S_t^T tends to A. Lemma 2 gives the opposite lower bound p for all sufficiently small t > 0. Since S_t is invertible, ordinary rank is unchanged.

Proof of (2), including a uniform positive parameter bound. Choose a minimal strictly positive n by q factor B of A. For each column j put s_j = sum_(i=1)^n B_ij, and define

alpha = min_(1<=i<=n, 1<=j<=q) B_ij/s_j > 0.

For every column the ratios sum to one, so alpha <= 1/n. Every t with 0 < t <= alpha/2 satisfies t < 1/n and

(T_t B)_ij = B_ij - t s_j >= B_ij/2 > 0.

Put C = T_t A T_t^T = (T_t B)(T_t B)^T. This supplies a strictly positive q-column factor of C and proves cp^+(C) <= q.

Now choose a minimal nonnegative factor D of C and omit zero columns (there are none in a minimal factor). Every column of T_t^(-1)D is strictly positive by Lemma 3, and

A = (T_t^(-1)D)(T_t^(-1)D)^T.

Consequently q = cp^+(A) <= cp(C). Combining the bounds gives

q <= cp(C) <= cp^+(C) <= q,

which proves (2). Invertibility of T_t proves rank preservation. No interior hypothesis was used. QED.

The same argument using any finite strictly positive factor, not necessarily a minimal one, already proves cp^+(A) <= p_n: the matrix C is completely positive, and any minimal factor of C pulls back to a strictly positive factor of A.

## 3. The maximum and its fixed-rank refinement

### Corollary 5: p_n^+ = p_n

The upper bound follows at once from (2): cp^+(A) = cp(C) <= p_n whenever cp^+(A) is finite. For the lower bound take A_0 in CP_n with cp(A_0) = p_n, which exists by Lemma 1. Theorem 4(1) gives, for all sufficiently small t > 0, a matrix S_t A_0 S_t^T with both ranks equal to p_n. It is nonzero, has a finite strictly positive factor, and has the same ordinary rank as A_0. Thus the upper bound is attained. QED.

In particular, the lower-bound construction is not a limit with only an unattained extremal value. Closedness of F_(p_n-1) excludes a decrease of CP-rank throughout a sufficiently small positive interval of t.

For 1 <= r <= n define

P_(n,r) = max { cp(A) : A in CP_n, rank(A) = r },

and define P_(n,r)^+ by maximizing finite cp^+(A) on the same ordinary-rank stratum. The first set is nonempty, for example by a diagonal matrix with r positive entries; Lemma 1 makes its maximum finite and attained. Positive congruence as in (1) shows the second set is nonempty. Rank preservation in (1) and (2) proves

**P_(n,r)^+ = P_(n,r) for every 1 <= r <= n.**

This is a statement on exact rank strata, not an identification of the boundary with the interior. For r < n all these strictly positive-factor matrices are singular and remain on the boundary of CP_n.

## 4. What remains of the rank-gap question

Let g_n be as defined above. The established results and the new maximum theorem give:

- g_1 = g_2 = g_3 = 0. The n=1 claim is immediate. For n=2,3, use Bomze-Dickinson-Still, Corollary 3.4, since a nonzero matrix with a strictly positive factor has all entries strictly positive.
- 0 <= g_4 <= 1. Indeed p_4^+ = 4, and Corollary 3.4 also gives cp^+(A)=cp(A) whenever cp(A)<=2. Any nonzero gap thus has cp(A)>=3.
- For every n>=5, 1 <= g_n <= p_n-3. The upper bound uses precisely the same cp(A)<=2 equality and Corollary 5. For the lower bound, Bomze-Dickinson-Still, Theorem 5.1(11), provides an interior matrix with cp(A)=n and cp^+(A)=n+1, since p_n>n for n>=5.
- More specifically, a rank-r matrix in the domain satisfies cp^+(A)-cp(A) <= P_(n,r)-r.
- For positive-definite matrices the bound is cp^+(A)-cp(A) <= p_n-n. This is not asserted as a boundary-inclusive bound.

These bounds do not assert that the endpoints for n>=4 are attained. In particular, this note does not decide whether g_4 is zero or one, or determine g_n for n>=5. A finite numerical search for factors cannot establish nonexistence of a shorter positive factor, and is not used to claim an extremal gap.

One further elementary fact is that g_n is nondecreasing. Given a matrix A with factor B, repeat any one row of B to obtain an (n+1)-row factor. This operation is a fixed row-duplication congruence on A. It preserves both ranks: extending either a nonnegative or a positive factor gives the upper inequalities, while restricting to the original n principal rows and columns gives the lower inequalities. Thus every finite gap at order n also occurs at order n+1. This fact does not resolve the missing maximum.

## 5. Source comparison and limitations

The original two questions appear in Peter J. C. Dickinson's contribution to Oberwolfach Report 52/2017, printed pp. 3082-3083. Its display combines a p by n factor with BB^T, which is dimensionally inconsistent. We use the vector-sum definition from Bomze-Dickinson-Still: n-vectors are columns of an n by p factor in A=BB^T. Their manuscript also uses the consistent transposed convention, a p by n matrix V with A=V^T V.

Bomze-Dickinson-Still's Theorem 5.1 proves p_n <= p_n^+ <= p_n+1 and an interior CP-plus maximum equal to p_n; its Theorem 4.9 is restricted to the interior. The present proof supplies the additional boundary-inclusive argument by strictly positive invertible congruence. It does not silently enlarge the domain of either cited theorem. Their Corollary 3.4 and Theorem 5.1 are the sources for the low-order and gap facts quoted above. The n=5 ordinary maximum 6 is stated in their proof of Theorem 5.1.

Lai-Yoshise's 2022 paper uses exactly the n by p column-factor convention. Its algorithmic stationary-point guarantees and experiments do not determine either extremum; in particular, unsuccessful local optimization is not a proof of nonexistence of a factor. None of its numerical conclusions is needed for Theorems 4 or 5.

The proof of p_n^+=p_n and its fixed-rank refinement is self-contained above. A bounded literature check is not a worldwide novelty certificate. The combined two-question target is only partially resolved here because the maximum gap is still undetermined in general. No explicit formula for all ordinary maxima p_n is claimed.

## References

1. P. J. C. Dickinson, with I. M. Bomze and G. Still, "The structure of completely positive matrices according to their CP-rank and CP-plus-rank," in *Copositivity and Complete Positivity*, Oberwolfach Report 52/2017, pp. 3082-3083. Full report: https://ems.press/content/serial-article-files/46715
2. I. M. Bomze, P. J. C. Dickinson and G. Still, "The structure of completely positive matrices according to their CP-rank and CP-plus-rank," *Linear Algebra and its Applications* 482 (2015), 191-206. https://doi.org/10.1016/j.laa.2015.05.021. The inspected complete author manuscript is dated November 4, 2014: https://api.newton.ac.uk/website/v0/events/preprints/NI14088
3. Z. Lai and A. Yoshise, "Completely positive factorization by a Riemannian smoothing method," *Computational Optimization and Applications* 83 (2022), 933-966. https://doi.org/10.1007/s10589-022-00417-4
