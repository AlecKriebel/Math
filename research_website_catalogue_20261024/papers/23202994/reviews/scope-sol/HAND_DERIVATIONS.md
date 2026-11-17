# INITIAL independent analytic reconstruction

This file was written from the original manuscript, fresh outer-PDF text/pixels and original metadata only. No cited primary, package audit, README, scientific code or peer/root scientific finding has been read. All imported results below are premises awaiting independent verification. These calculations do not certify the imported theorem.

## 1. Exact normalization and lattice

Put b=sqrt(3)/2 and B=b^(-1/2)[[1,1/2],[0,b]]. Then det(B)=b^(-1)b=1, so Lambda=B Z^2 has number density one. For k=(j,l),

    |Bk|^2 = b^(-1)(j^2+j l+l^2).

The quadratic form is positive definite: j^2+j l+l^2=(j+l/2)^2+3l^2/4. The six pairs (1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1) have value one. Thus the shortest distance is b^(-1/2), and their contribution to Z_s is 6 b^(s/2). This is a normalization check, not a numerical evaluation of Z_s or proof of optimality.

Since B is invertible, |Bk| >= c ||k||_infinity for some c>0. The integer shell ||k||_infinity=m contains (2m+1)^2-(2m-1)^2=8m points. Consequently

    0 < Z_s <= 8 c^(-s) sum_(m>=1) m^(1-s) < infinity,  s>2.

Every finite energy is ordered: E_ord=sum_(i!=j)|x_i-x_j|^(-s)=2 E_unord. The outgoing row of an infinite lattice therefore contributes Z_s, with no factor 1/2. A source theorem using unordered energy must be converted before importing its lower bound.

## 2. Periodic averaging without an averaging-convention substitution

Let F={f_1,...,f_q} be distinct in [0,L)^2 and C=F+L Z^2. Different representatives give disjoint cosets, including when a point lies on a lower face. Every row

    h_i = sum_((j,k)!=(i,0)) |f_i-f_j-Lk|^(-s)

is finite. For m=||k||_infinity>=2, choose a coordinate attaining m. Coordinate differences of representatives have magnitude <L, so the Euclidean denominator is at least L(m-1)>=Lm/2. The tail is bounded by 8q(2/L)^s sum_(m>=2)m^(1-s). Near shells are a finite collection of nonzero denominators. This also shows that the periodic configuration is uniformly discrete, although no uniform lower separation across different finite input configurations is needed.

For each coset let n_i(R)=#((f_i+LZ^2) intersect B_R), and put d=L sqrt(2)/2. The side-L cells centered at its points tile the plane. The union of cells with centers in B_R contains B_(R-d), up to irrelevant boundaries, and is contained in B_(R+d). Hence

    pi(R-d)^2/L^2 <= n_i(R) <= pi(R+d)^2/L^2,
    n_i(R)=pi R^2/L^2+O(R/L+1),
    n_i(R)/sum_j n_j(R) -> 1/q.

Write S_R for the ordered energy with both endpoints in B_R. For a fixed displacement cutoff T and truncated full rows h_i^(T),

    sum_i n_i(R-T) h_i^(T) <= S_R <= sum_i n_i(R) h_i.

The lower inequality retains rows whose initial point lies in B_(R-T); every retained endpoint then lies in B_R. The upper inequality completes outgoing rows. Divide by n_C(R), send R to infinity at fixed T, and then let T tend to infinity. Nonnegative sums and monotone convergence give

    lim_(R->infinity) S_R/n_C(R) = q^(-1) sum_i h_i.

This is an ordinary finite limit. It has been derived for the exact centered-disk convention, rather than inferred from a square or Palm average. Translation of the origin affects only the elementary boundary count, not the limiting periodic average.

## 3. Density and energy scaling

For lambda>0, n_(lambda C)(R)=n_C(R/lambda). Thus

    density(lambda C)=lambda^(-2) density(C),
    H_s(lambda C)=lambda^(-s) H_s(C).

The denominator of the energy average is n_C(R/lambda), not the disk area. Scaling therefore introduces lambda^(-s), with no extra lambda^(-2) factor in the per-particle energy. This is a sensitive interface check.

## 4. Minimal external premise and the finite lower bound

Define U_per(s) as follows: every distinct q-point F in [0,sqrt(q))^2, periodically extended by sqrt(q) Z^2, has ordered centered-disk energy per particle at least Z_s. Only the more restricted compressed positive-gap subclass below is actually needed. The manuscript asserts a stronger theorem for all locally finite centered-density-one configurations. Neither that assertion nor U_per(s) has been verified against a primary source in this INITIAL.

Fix N>=1, epsilon>0 and a distinct X={x_i} in [0,1]^2. Set y_i=sqrt(N)x_i and L=(1+epsilon)sqrt(N). The positive gap puts every representative strictly below each upper face of the fundamental square, even when X uses the boundary. Its density is N/L^2=(1+epsilon)^(-2). Periodic averaging gives

    H_s(F+LZ^2) = N^(-1-s/2) sum_(i!=j)|x_i-x_j|^(-s) + I_(N,epsilon),
    I_(N,epsilon) = (1/N) sum_(i,j=1)^N sum_(k!=0)|y_i-y_j-Lk|^(-s).

The cross sum includes i=j at nonzero translations. For ||k||_infinity=m>=1, a coordinate with magnitude m gives

    |y_i-y_j-Lk| >= sqrt(N)((1+epsilon)m-1) >= epsilon sqrt(N)m.

There are 8m translations in that shell. All N^2 choices of i,j are retained, so

    0 <= I_(N,epsilon)
       <= (1/N) N^2 8 epsilon^(-s) N^(-s/2) sum_(m>=1)m^(1-s)
       = 8 epsilon^(-s) zeta_R(s-1) N^(1-s/2).

No separation/occupancy assumption on X entered this bound. Compress by lambda=(1+epsilon)^(-1); the period becomes sqrt(N), the number of representatives stays N, and density becomes one. Conditional on U_per(s),

    Z_s <= (1+epsilon)^s [a(X)+I_(N,epsilon)],
    a_N >= (1+epsilon)^(-s) Z_s
           -8 epsilon^(-s) zeta_R(s-1) N^(1-s/2).

The direction is correct: the inter-box term is subtracted from the lower bound after applying the density-one theorem. For fixed epsilon and fixed s>2, the error tends to zero as N tends to infinity, then epsilon tends down to zero. The disk radius already tended to infinity for each fixed finite configuration. No interchange of a liminf and an infinite mixture is used here.

## 5. Matching upper bound independent of U_per

Choose a bounded area-one fundamental parallelogram P for Lambda with P contained in [-D,D]^2. If z lies in [D,t-D]^2 and in the cell v+P, then v=z-p lies in [0,t]^2. Area comparison of the tiling implies

    #(Lambda intersect [0,t]^2) >= (t-2D)^2,  t>=2D.

For t_N=sqrt(N)+2D, this crop has at least N points. Choose exactly N of them. Its total ordered energy is at most N Z_s, because each finite outgoing row is a sub-sum of one full lattice row. After shrinking by 1/t_N,

    a_N <= Z_s (1+2D/sqrt(N))^s.

This proves limsup a_N<=Z_s without any imported universal-optimality theorem. It does not prove the matching lower bound. Choosing a subset, rather than asserting a crop with exactly N sites, avoids a lattice-counting gap.

## 6. A checkable conditional quantitative corollary

This is an independent manipulation of the manuscript's all-N/all-epsilon finite inequality, not a claimed new asymptotic expansion. Let

    alpha=(s-2)/(2(s+1)) > 0,  epsilon_N=N^(-alpha).

Convexity gives (1+epsilon)^(-s)>=1-s epsilon. Also

    1-s/2+alpha s = -alpha.

Therefore, conditional on U_per(s),

    a_N >= Z_s - [s Z_s+8 zeta_R(s-1)] N^(-alpha).

The independent lattice upper bound is Z_s+O_(s,D)(N^(-1/2)). The rate alpha tends to zero as s decreases to 2 and to 1/2 as s tends to infinity. Thus the original fixed-s result has no uniform critical-s guarantee. These rough inequalities do not produce a second-order coefficient and are not transferred to arbitrary surfaces by an asymptotic-only manifold theorem.

## 7. Why the upstream lower bound is the central unresolved difficulty

The periodic input cannot be promoted to an independent proof merely by restating it. In fact, for the fixed-s square problem it is equivalent to the planar lower asymptotic through elementary periodic cropping.

Assume liminf_N a_N>=Z_s. For a fixed density-one periodic configuration F+LZ^2, let C_T=C intersect [0,T]^2 and N_T=#C_T. Coset cell counting gives N_T=T^2+O(T) and proportions tending to 1/q. Completing rows gives

    E(C_T) <= sum_i n_i(T) h_i = N_T[H_s(C)+o(1)].

Shrink by 1/T into the unit square:

    a_(N_T) <= (T^2/N_T)^(s/2)[H_s(C)+o(1)] -> H_s(C).

Since N_T tends to infinity, Z_s<=H_s(C). This is U_per(s). Together with the positive-gap derivation, it identifies the exact unsupported premise if the primary theorem has not been checked. A stand-alone primary-free solution route is BLOCKED at this equivalent central lower-bound statement. A cited consequence route can reopen only upon material independent evidence for the exact imported theorem/interface; this does not make the manuscript's explicit attribution a hidden proof.

## 8. Potential-class interface and a conditional singular-kernel workaround

The original uses g(t)=t^(-s/2) and the derivative identity

    (-1)^r g^(r)(t)=(s/2)_r t^(-s/2-r)>0, t>0.

That algebra is correct, but the actual primary theorem's domain must be read: squared distance versus distance, allowance of a singularity at zero, decay/integrability and complete monotonicity conventions matter. No primary was opened here.

If direct singular kernels are excluded but bounded positive Gaussian mixtures are included, there is a possible fully one-sided bridge. For t=s/2 and 0<a<b<infinity define

    g_(a,b)(r^2) = Gamma(t)^(-1) integral_a^b u^(t-1) exp(-u r^2) du.

Substitution v=u r^2 gives the full integral r^(-s). Each truncated kernel is smooth, bounded at zero, completely monotone in r^2 and rapidly decaying. Pointwise g_(a,b)(r^2)<=r^(-s), so every finite-disk energy and its liminf satisfy H_s(C)>=H_(a,b)(C). If the actual upstream theorem applies to these mixtures, then

    H_s(C) >= H_(a,b)(C) >= sum_(v in Lambda\{0})g_(a,b)(|v|^2).

Monotone convergence on the lattice as a decreases to zero and b increases to infinity yields Z_s. There is no illicit exchange of the configuration liminf with the parameter integral. This is an interface contingency to check after RESUME, not evidence that the actual theorem has been proved or has these hypotheses.

## 9. Surface interface, units and boundary

The second external premise HS(s,2) is the corrected theorem identifying the leading energy on the admitted compact two-rectifiable class with C_(s,2)/H^2(M)^(s/2), in ordered ambient-Euclidean conventions. Its exact definition, theorem statement and addendum have not been opened.

The elementary geometric inclusion is plausible and reconstructible: a smooth embedded surface, including a smooth boundary point, is locally a smooth graph over a plane or half-plane. Extend the boundary chart to a full open planar neighborhood and shrink to retain rank two. A nonsingular coordinate projection and bounded derivatives give a bi-Lipschitz chart on a smaller neighborhood. Compactness supplies finitely many compact pieces in such open chart domains. This is the class the note attributes to definition(19); that attribution must still be checked in the actual theorem.

For compact K_j contained in an open chart domain G_j, finite closed cubes contained in G_j can cover K_j. Their bi-Lipschitz images form a compact finite union of regular sets. This supplies a compact ambient relative-neighborhood setting. It does not, by itself, verify where and with which extra hypotheses the cited addendum's neighborhood lemma is used. That exact step remains a primary-interface check, not an assumed repaired proof.

Under HS(s,2) and the conditional square result,

    E_s(M,N)/N^(1+s/2) -> Z_s A^(-s/2).

If M is dilated by lambda, its area becomes lambda^2 A and its energy is multiplied by lambda^(-s); the formula has exactly that homogeneity. A radius-r sphere has area4pi r^2, so the predicted coefficient is r^(-s) Z_s/(4pi)^(s/2), consistent with exact chordal scaling. No intrinsic-distance conclusion is needed or independently asserted.

## 10. Boundary and limiting-case audit

- N=1: the within-cell ordered energy is zero; nonzero-translation self images remain in the cross term. The lower comparison is conditional on the imported input and retains its error.
- Boundary points of X: epsilon>0 prevents periodic aliases even at opposite upper/lower faces. Epsilon=0 is not admissible for this construction.
- Collisions: assigned +infinity; distinct finite configurations exist. The compact-product lower-semicontinuity argument supplies minimizers without any separation theorem.
- s=2 or below: the periodic shell tail need not converge; the proof intentionally stops. Neither a critical logarithmic normalization nor an infinite coefficient is substituted.
- s varying with N: all constants and the vanishing error depend on fixed s>2; no uniform joint limit is claimed.
- Area zero: excluded before using A^(-s/2). Smooth compact positive-area surfaces are the stated scope.
- Ordered/unordered conventions: the claimed constant is Z_s for ordered pairs and Z_s/2 for unordered pairs.
- Finite minimizer geometry: equality of leading minimum values does not establish crystallization, uniqueness or a subleading expansion.

The strongest INITIAL evidence is a checkable conditional reconstruction and a precise separation of elementary deductions from the two unverified external interfaces. No unconditional main-theorem clearance, primary-proof verification, computation replay, formal proof or priority certificate is issued here.
