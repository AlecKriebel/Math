# Complete law from the historical finite-pile construction

UTC started: 2026-10-15T03:56:27Z. Completion estimate: 75% of this scoped audit.

This is a checkable derivation made during this audit. It is **not** a claim that the displayed formulas below appeared verbatim in an earlier publication. It uses the construction already stated in Aldous–Diaconis's 1993 notes, printed36–37, and the finite RSK/pile-top facts stated in the same notes, printed2–3 and9–10, and in the 1999 survey, printed418–419. Exact source byte pins are in SOURCE_AUTHENTICATION.json.

## 1. The joint rank law is finitely specified

For a uniform permutation of {1,...,n}, let B(n,i) denote its i-th final patience pile top, infinity if absent. Deleting labels above q leaves all labels at most q in exactly the same piles. One proves this directly: an insertion above q can never displace a pile top at most q, while inserting a label at most q acts on the low-label pile tops just as it would if the high labels were absent.

Consequently, for b=(1=b_1<...<b_k=N),

    p_B(b) := P(B(1)=b_1,...,B(k)=b_k)
            = A(b)/N!,                                               (H1)

where

    A(b)=#{pi in S_N: the complete final pile-top row of pi is b}.

At deck size N=b_k there can be no further pile top to the right of N, so the condition is precisely equality of the full row, not an unspecified condition on infinitely many ranks. The probability remains the same for every later deck size by the compatibility just proved. Thus (H1) is an exact finite formula, requiring neither a limiting computation nor an unknown stationary function. It is inefficient but fully executable.

Under finite RSK the insertion tableau P has its first row equal to the final pile-top row. For a shape lambda of size N with first row length k let

    C_lambda(b)=#{standard Young tableaux of shape lambda with first row b}.

The recording tableau Q can be any of f^lambda standard tableaux. Hence

    A(b)=sum_{lambda partition N, lambda_1=k} f^lambda C_lambda(b).      (H2)

The hook formula gives f^lambda=N!/product_c hook(c). C_lambda(b) is a finite integer with an explicit recurrence: start at the empty diagram, successively add a legal corner labeled t=1,...,N, allow an addition to the first row exactly when t belongs to {b_1,...,b_k}, and count paths ending at lambda. This does not hide a new probabilistic law inside C.

## 2. Explicit rank-tail certificate

Let L_N be the LIS length of a uniform permutation of size N. Compatibility gives

    P(B(k)>N)=P(L_N<k)
             =(1/N!) sum_{lambda partition N, lambda_1<k} (f^lambda)^2. (H3)

This is already an explicit finite quantity from the classical one-time RSK formula. For k>=2 an elementary bound is

    P(B(k)>N) <= min(1,(k-1)^(2N)/N!).                                 (H4)

Indeed, if LIS<k, patience sorting partitions the permutation into at most q=k-1 decreasing piles. Encode each position by its pile color and each value by its pile color. Given both words, each colored subsequence must be decreasing, which reconstructs the permutation uniquely. There are at most q^(2N) pairs. For fixed k the right side tends to zero by the ratio test. For k=1, B(1)=1 deterministically. This independently proves all finite ranks exist almost surely, not merely convergence of their individual atom masses.

## 3. Exact stationary mixture

Let Gamma(1)<Gamma(2)<... be the times of an independent rate-one Poisson process. The 1993 stationary representation is

    (X_1,...,X_k) =d (Gamma(B(1)),...,Gamma(B(k))).                      (H5)

To identify it independently with the specified process, put a unit PPP in the positive quadrant, set L(x,s) equal to its increasing-chain length in (0,x]x(0,s], and set Z_i(s)=inf{x:L(x,s)>=i}. The pile-top identity gives these Z as the nearest-right left-jump Hammersley particles from the empty boundary. Setting

    Y_i(t)=e^t Z_i(e^t)

gives positive drift dY_i/dt=Y_i. The event transformation (u,v)->(uv,log v) has unit Jacobian, hence still unit PPP intensity. The area-preserving scaling (u,v)->(a u,v/a) preserves the PPP and shifts the logarithmic trajectory, so Y is strictly stationary. At t=0, the spatial PPP is Gamma and its independent vertical marks induce the coherent uniform permutations defining B. Thus (H5) is the exact simultaneous stationary law of the target, with finite-prefix projection and no boundary immigration in that projection.

This sign convention is derived here. The displayed transformation on printed36 of the unfinished1993 draft uses x e^t in its counting function, which is inconsistent with positive drift under the usual Hammersley convention; it also places an infinite initial condition at t=0 despite using e^t. These draft defects are not used as evidence for a new law, and are not imported into this derivation.

For 0<x_1<...<x_k, put b_0=0,x_0=0. Conditional on b, independent exponential increments give the density

    g_b(x)=e^(-x_k) product_{i=1}^k
           (x_i-x_{i-1})^(b_i-b_{i-1}-1)/(b_i-b_{i-1}-1)! .            (H6)

The mixture p_k(x)=sum_b p_B(b) g_b(x) gives a positive all-coordinate density. It is a probability mixture since (H3) tends to zero. The mixture, plus (H1) or(H2), has no unspecified joint rank input.

For simultaneous survival queries at sorted thresholds 0<a_1<...<a_m and indices r_j<=k, conditional on b the Poisson-count identity gives

    K_b=P(Gamma(b_{r_j})>a_j for all j)
       =e^(-a_m) sum_{d_1,...,d_m>=0; sum_{h<=j}d_h<b_{r_j} for all j}
          product_j (a_j-a_{j-1})^d_j/d_j!,                            (H7)

where a_0=0. This is a finite sum because the last constraint bounds the total count. Therefore

    S_N=sum_{b: b_k<=N} p_B(b) K_b,
    S_N <= P(X_{r_j}>a_j for all j) <= S_N+P(L_N<k).                    (H8)

At rational thresholds S_N is e^(-a_m) times a rational; the exponential itself admits the usual explicit factorial-tail rational enclosure. Formula(H8) is a certified approximation to every joint event, built entirely from the old representation and finite deck counts. No numerical stability assumption or unproved limiting Markov property is needed.

## 4. Why this yields the candidate nested-shape formula automatically

Condition instead on the spatial Poisson strip counts d_j, and put n_j=sum_{h<=j}d_h, n=n_m. By(H5), the query is B(r_j)>n_j for every j. Conditional on the n spatial ranks, their independent marks give one uniform permutation of {1,...,n}. By compatibility, B(r_j)>n_j is exactly the event that the subword of values at most n_j has LIS at most r_j-1.

For completeness, insertion tableaux have the requisite value-restriction property: inserting a value above q only changes entries above q; inserting a value at most q has exactly the same action on the subtableau of entries at most q as insertion into that subtableau. This follows row by row from the bump-the-first-larger rule. Induction over the input word proves that P restricted to values at most q is the insertion tableau of the value-restricted subword. Thus its shapes lambda^(j) form a nested chain and satisfy lambda^(j)_1<=r_j-1.

For a fixed chain at the prescribed sizes, the number of P tableaux is

    product_j f^(lambda^(j)/lambda^(j-1)),

and Q can be any of f^(lambda^(m)) tableaux. Since RSK is a bijection, its conditional probability is that product times f^(lambda^(m))/n!. Multiplication by

    e^(-a_m) product_j (a_j-a_{j-1})^d_j/d_j!

gives exactly the candidate's positive nested-shape weights after replacing standard/skew tableau counts by their exponential specializations. This is the same counting as the candidate with P and Q exchanged by RSK symmetry. It explicitly handles all distinct thresholds and repeated/nonmonotone indices; no independent product of one-time LIS distributions is substituted.

The threshold formula is therefore a complete, automatic consequence of an already-stated stationary mapping plus coherent finite RSK, not merely a resemblance to old ingredients. The factorial-determinant specialization is a further classical evaluation of these finite skew counts. This proof does not establish that a prior author displayed this formula as an answer to Aldous's later question, and it does not turn the qualitative explicitness criterion into an objective historical acceptance fact.

## 5. Independent validation and limits

coherent_rank_check.py imports no campaign code. It exhaustively enumerates all permutations through n=8 and, independently, all standard tableaux by Young-lattice corner addition. It verifies weighted first-row histograms via the hook formula, every complete shape dimension, 255 prefix compatibility equalities, the known second-rank formula, and the finite color-tail inequalities. COHERENT_RANK_CHECK.json records the results. These finite checks support implementation and convention consistency; the arguments above establish the general statements.

The central priority distinction is now precise: the earlier construction specifies the law in a mathematically complete sense, and ordinary finite enumeration with explicit tails makes it effectively computable. A new determinant presentation can improve explicitness substantially, but this audit cannot certify historical firstness or that the problem's author would accept this qualitative form.
