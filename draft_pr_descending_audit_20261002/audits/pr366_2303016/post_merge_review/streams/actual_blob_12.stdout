# Turn 1: a direct energy proof of the thin-point conclusion

Problem2303016 / AMR-022-3016, Hayman–Lingham Problem3.16. Complete candidate for the requested direct proof, with two precise sharpness statements. The method is a Newtonian specialization/reconstruction of the capacitary strategy in Hedberg–Wolff, *Thin sets in nonlinear potential theory* (1983), pp.173–174. No novelty or priority claim is made.

## 1. Normalization and foundational inputs

Put s=n−2>0 and use the Newtonian kernel k(x,y)=|x−y|^(−s), with infinite diagonal value. For a compact set K define

    cap(K) = 1 / inf{ I(mu) : mu is a probability measure supported on K },
    I(mu) = double_integral k(x,y) dmu(x)dmu(y),

with1/infinity=0 and cap(empty)=0. Changing this capacity by a fixed positive dimensional factor does not affect the question's finiteness condition or polar conclusion.

We use the standard foundational facts that Newtonian capacity is a Choquet capacity on Borel sets, and that a Borel set has capacity zero exactly when it is polar. Thus a nonpolar Borel set contains a compact subset carrying a finite-energy probability measure. This is the measure-theoretic Choquet capacitability theorem, not the fine-topological Choquet property that itself implies Kellogg. These general capacity/measure facts are explicitly retained as background; they are not Kellogg's theorem, the Wiener regularity criterion, or a Dirichlet-boundary result. The arguments below prove all special equilibrium-potential estimates they use.

Weak compactness of probabilities on a compact set and lower semicontinuity of the nonnegative kernel give an energy-minimizing probability mu when0<cap(K)<infinity. Write J=I(mu). If D=diam(K), then

    J >= D^(−s) > 0,                                (1.1)

since distances between points of K are at most D. Positive capacity excludes D=0. Compact sets have finite capacity by this same bound.

The potential is U_mu(x)=integral |x−y|^(−s) dmu(y).

## 2. The equilibrium property needed here, without a q.e. theorem

For any Borel A with mu(A)>0, the probability nu=mu|_A/mu(A) has finite energy. Minimality under the variation(1−t)mu+t nu gives

    integral U_mu dnu >= J.

All cross energies in this variation are finite because nu is bounded by a constant multiple of mu. Hence

    integral_A U_mu dmu >= J mu(A)

for every such A. It follows that U_mu>=J mu-almost everywhere. Since integral U_mu dmu=J, in fact

    U_mu=J mu-almost everywhere.                     (2.1)

No assertion about exceptional boundary points has been used.

Let S=supp(mu) and G={x in S:U_mu(x)=J}. Then G is dense in S: every relatively open nonempty portion of the support has positive mu-mass. The potential is lower semicontinuous by Fatou's lemma. Approximating any x in S by points of G therefore gives

    U_mu(x)<=J, x in S.                              (2.2)

## 3. A global weak maximum bound from nearest support points

Set C=2^s. We claim

    U_mu(x)<=C J for every x in R^n.                 (3.1)

Section2 handles x in S. If x lies outside S, let d=dist(x,S)>0 and choose a nearest point y in S. For epsilon>0 choose y_epsilon in G with |y_epsilon−y|<epsilon. For every z in S,

    |y_epsilon−z| <= |y_epsilon−x|+|x−z|
       <= d+epsilon+|x−z|
       <= (2+epsilon/d)|x−z|.

After raising to the negative s power and integrating,

    U_mu(x) <= (2+epsilon/d)^s U_mu(y_epsilon)
             = (2+epsilon/d)^s J.

Let epsilon decrease to0. This proves(3.1). It is a deliberately non-sharp bound and does not import a potential maximum principle, Frostman's q.e. statement, or Kellogg's theorem.

For a compact A contained in K, put m=mu(A). If m>0, the restricted measure satisfies

    I(mu|_A) <= C J m.

Its normalized probability is admissible in the energy definition of cap(A), so

    cap(A) >= m²/I(mu|_A) >= m/(C J).

For m=0 the same final inequality is immediate. Thus

    mu(A) <= C J cap(A)                              (3.2)

for every compact A contained in K.

## 4. Measurability of the exceptional set

For the given compact E, put

    c(x,r)=cap(E intersect closed B(x,r)), r>0,
    W_E(x)=integral_0^1 c(x,r) r^(−s−1) dr,
    T={x in E:W_E(x)<infinity}.

The map(x,r)↦c(x,r) is upper semicontinuous. If(x_j,r_j)→(x,r), then for every epsilon>0 and sufficiently large j,

    E intersect closed B(x_j,r_j)
       is contained in E intersect closed B(x,r+epsilon).

Capacity is continuous along decreasing compact sets, so taking limsup and then epsilon→0 gives the assertion. For clarity, compact continuity follows directly from the energy definition: choose minimizing probabilities on a decreasing sequence of compact sets; a weakly convergent subsequence is supported on their intersection, and lower semicontinuity of energy yields the reverse inequality to monotonicity. The case when the limiting capacities are zero is immediate.

Therefore c is Borel measurable, and nonnegative parameter integration makes W_E and every truncated/tail integral Borel. Thus T is Borel and the Borel-capacitability input from Section1 applies.

## 5. Localize a hypothetical positive-capacity exceptional set

Suppose, for contradiction, that T is nonpolar. Take a compact K_0 contained in T with positive capacity and a finite-energy probability rho on K_0. At every x in K_0,

    integral_0^delta c(x,r) r^(−s−1) dr →0 as delta→0.

Let epsilon=1/(4Cs). The increasing Borel sets

    T_j={x in K_0: integral_0^(1/j) c(x,r) r^(−s−1) dr <= epsilon}

cover K_0. Some T_j has positive rho-mass. Fix such a j and delta=1/j. Cover R^n by countably many small closed cubes of diameter at most delta/4. Some T_j intersected with a cube has positive rho-mass. Inner regularity of rho supplies a compact subset K of that intersection with rho(K)>0.

The normalized restriction of rho to K still has finite energy, so cap(K)>0. Moreover,

    diam(K)<=delta/4,
    integral_0^delta c(x,r) r^(−s−1) dr <=1/(4Cs)
          for every x in K.                         (5.1)

This uniform small-tail localization is the essential step. It is justified by measurable exhaustion and inner regularity, not an unproved uniformity assertion on all thin points.

## 6. The contradiction by layer cake

Let mu be the energy-minimizing probability on K and J=I(mu). Tonelli's theorem and the elementary identity

    t^(−s)=s integral_t^infinity r^(−s−1) dr

give, for every x,

    U_mu(x)=s integral_0^infinity mu(closed B(x,r)) r^(−s−1) dr.  (6.1)

Open versus closed balls does not change this radial integral; the same identity follows pointwise before integrating in y, including the infinite diagonal case.

For x in K and r<=delta, apply(3.2) to K intersect closed B(x,r), and then monotonicity with K contained in E:

    mu(closed B(x,r)) <= C J c(x,r).

For r>delta use only total mass1. Equations(5.1) and(6.1) imply

    U_mu(x) <= C J s integral_0^delta c(x,r) r^(−s−1) dr + delta^(−s)
             <= J/4 + delta^(−s).

By(1.1) and diam(K)<=delta/4,

    delta^(−s) <= J (diam(K)/delta)^s <= J/4^s <= J/4.

Thus U_mu(x)<=J/2 for every x in K. This contradicts U_mu=J mu-almost everywhere and J>0. Therefore cap(T)=0, and T is polar.

This proves the exact original integral-finiteness conclusion directly from capacity energy, with no appeal to harmonic boundary regularity or the Wiener equivalence.

## 7. Precise critical-power sharpness

For every x,r, the diameter bound gives

    c(x,r)<=cap(closed B(x,r))<=2^s r^s.

If the denominator power n−1=s+1 is weakened to n−1−eta for any eta>0, then

    integral_0^1 c(x,r) r^(−s−1+eta) dr <= 2^s/eta

at **every** point of every compact E. Taking E to be a ball gives a positive-capacity exceptional set. A ball has positive capacity because normalized volume measure has finite Newtonian energy: the kernel exponent s=n−2 is strictly below the ambient dimension n and its local radial integral is proportional to integral_0^2 r dr.

Thus the denominator exponent is critical. More generally any nonnegative weight a(r) with integral_0^1 a(r) dr/r finite makes the weighted criterion finite everywhere by the same bound, so no polar conclusion survives for that class of weakenings. This does not assert that every smaller, nonintegrable weight fails; the source's optional “best possible” clause is not promoted to an unformulated all-gauge theorem.

## 8. Sharpness of the exceptional-set size

Every compact polar set P has cap(P intersect closed B)=0, so all its points satisfy the criterion. The exceptional set therefore need not be empty, finite or countable.

For an explicit uncountable example take a line segment of length1 in R^n, n>=3. Every probability rho on that segment has infinite energy. Indeed, for d=|x−y|<=1,

    d^(−s)>=d^(−1)>=sum_{k>=0} 2^(k−1) 1_{d<=2^(−k)}.

Partition the segment into2^k intervals. The rho-product mass of same-interval pairs is the sum of squared interval masses, at least2^(−k). Integrating the displayed kernel bound yields a contribution at least1/2 for every k, hence infinite energy. Atoms simply give infinite diagonal energy as well. Thus the segment has zero capacity and is polar, while every one of its uncountably many points satisfies W_E=0.

## 9. Credit and audit limits

Hedberg–Wolff's general proof for Borel sets uses a small-capacity-integral compact subset and its capacitary measure to obtain an energy contradiction. This packet gives the explicit Newtonian version, with a proved non-sharp potential bound and measured localization. Its elementary sharpness examples are not novelty claims.

The only unreproved capacity-theoretic foundations are Borel capacitability and the equivalence of Newtonian capacity zero with polarity, together with routine measure compactness/regularity. These are not the requested conclusion in disguise and do not use Kellogg or the Wiener criterion. Independent review must verify that separation as well as every estimate above. The source-method candidate is frozen after this one substantive turn; no further author search before review.
