# Actual canonical mountains obstruct the sharp local-reroot window certificate

Shared PASS4, row 1778 / 30005770, 14 October 2026. This is an all-size obstruction to a particular quantitative proof route. It is not a uniform-probability counterexample and does not bound the true finite-window gaps from above.

## 1. The rate being tested

Use e(x,y)=(x+y)log(x+y)-x log x-y log y, with zero values interpreted continuously. Put

    H(r)=e(1,r)=(1+r)log(1+r)-r log r.

The accepted first-frontier exponent is

    gamma=log C(1/lambda),     0<gamma<=log 2,
    C(z)=(1-sqrt(1-4z))/(2z).

The sharp profile-minimax certificate obtained from all the accepted single-incoming-edge reroot penalties is

    V_K=inf_{x_j>=0, sum_(j=1)^K x_j=1}
           max_(1<=j<=K) [gamma*x_j-e(x_(j-1),x_j)],
    x_0=0.                                                  (1)

The other PASS4 lane proves positivity and the exact recurrence evaluating V_K, and proves delta_K=log(lambda/g_K)>=V_K. This note does not need that recurrence: its obstruction holds for V_K as defined in (1), and therefore for every weaker certificate d_K<=V_K.

Crucially, V_K is a lower certificate for the true delta_K. Failure of V_K to pay the boundary entropy does not imply failure of delta_K.

## 2. An upper bound on what these local penalties can certify

For every K>=1,

    V_K<=gamma/(2^K-1).                                    (2)

Proof. In (1) use x_j=2^(j-1)/(2^K-1). The first penalty is gamma/(2^K-1). For j>=2, x_(j-1)=x_j/2, so

    gamma*x_j-e(x_(j-1),x_j)
        =x_j[gamma-H(1/2)]<0,

because

    H(1/2)-log 2=(1/2)log(27/16)>0.                         (3)

Thus the maximum for this test profile is exactly its first penalty, proving (2). In particular, optimizing tangents or the entire local profile minimax cannot remove exponential summability from this certificate family. Equation (2) is not an upper bound on delta_K.

## 3. Infinite normalized profile: every center-containing window fails

Consider the genuine normalized mass profile on the integer line

    p_j=(1/3)2^(-|j|),     j in Z.                          (4)

It has total mass one and a heavy central cell p_0=1/3. For W=[-u,v], u,v>=0, of length K=u+v+1, its mass and boundary entropy are

    M=(1/3) sum_(j=-u)^v 2^(-|j|),
    E=(1/3) H(1/2)[2^(-u)+2^(-v)].                          (5)

This includes u=0 or v=0: the outside neighbor of the central endpoint still has half its mass. Since the sum in (5) is at most K, AM-GM gives

    E/M >= [2H(1/2)/K] 2^(-(K-1)/2).                       (6)

Meanwhile AM-GM applied to 1,2,...,2^(K-1) gives

    2^K-1>=K 2^((K-1)/2),
    V_K<=gamma/(2^K-1)<[2H(1/2)/K]2^(-(K-1)/2).            (7)

Combining (6)-(7), every such window has

    M V_K-E<0.                                             (8)

Thus a positive internal loss for every fixed K, even the exact best loss from (1), need not overcome the exact two-boundary entropy in any center-containing window.

## 4. Every bounded window, including one-sided choices

A finite window in (4) that does not contain index zero lies entirely on one side. Let a be its endpoint closest to zero. Its outside inward neighbor has mass 2a, and its total mass satisfies M<2a. Therefore

    E/M >=e(a,2a)/M>H(1/2)>log 2>=gamma>=V_K.               (9)

No center-containing restriction is needed: (8) holds for every finite window of the infinite profile.

This is a normalized summable profile, not a claim that one finite permutation has infinitely many cells. The next section supplies actual finite canonical avoiders with the required fixed-window quantifiers.

## 5. Exact finite canonical realization and quantifiers

For m>=1, use increasing normalized states with sizes

    2,4,...,2^m,2^(m-1),...,4,2.                            (10)

For an edge from increasing I_a to increasing I_b, with a>=2, choose the shuffle

    first upper point, all lower points, remaining upper points.

The lower maximum is bracketed by an increasing pair in the upper cell, giving the greedy witness. A cross-cell 1324 would need two lower points with an upper point between them; the lower points form a consecutive block, so this is impossible. Cases with only one lower point would require a 213 in the upper cell, and cases with only one upper point a 132 in the lower cell; increasing cells exclude these. The accepted pair-local exact kernel reconstructs a unique actual 1324-avoider pi_m with precisely the canonical cell chain (10). This is the same rigorously accepted construction as PASS3; the new result is its exact all-window entropy comparison.

Its size and central fraction are

    n_m=3*2^m-4,
    p_center=2^m/n_m>1/3,
    p_center ->1/3.                                        (11)

Fix any proposed window bound B>=1. Choose m>B. For every center-containing window of at most B cells, both outside neighbors are present. Relative to the center its masses and neighbors are exactly proportional to those in (4); common scaling cancels in E/M. Hence (6)-(8) hold exactly, not only asymptotically.

For every window of at most B cells lying wholly on one side, its outside inward neighbor has twice the inward endpoint mass, and its total mass is less than twice that endpoint. Equation (9) holds even if its outer end is the end of the finite staircase. Thus for every m>B and every nonempty window W in pi_m with actual width K<=B,

    M(W) V_K-E(W)<0.                                      (12)

This defeats every finite family of candidate lengths, every location-selection rule, and every shorter cap certificate d_L<=V_L with L>=K: V_L is nonincreasing because zero-padding a profile in (1) cannot increase its maximum, so the score is no larger. The heavy-cell obstruction can be fixed at epsilon=1/3. In particular, no universally bounded window rule achieves a positive margin using only these certified losses.

The whole finite staircase does have E=0 and positive internal certificate. Its length 2m-1 is unbounded, so it is unavailable to any fixed B in (12). Passing to growing windows would require coefficient control uniform in their length; fixed-K asymptotics do not provide it.

## 6. What follows and what does not

- This extends the accepted PASS3 one-neighbor obstruction to the exact block-boundary criterion, evaluated with the sharp accepted local-reroot gap certificate.
- The obstruction is not only abstract: every fixed-width test is realized by actual canonically gridded 1324-avoiders.
- Each pi_m has an increasing cell of asymptotic mass 1/3, so its increasing-pair density has liminf at least 1/9. This is a deterministic non-anti-diagonal sequence.
- No positive probability, non-exponential count, or asymptotic mass under uniform Av_n(1324) is established. These witnesses may be exponentially rare.
- No bound delta_K<=V_K is proved or claimed. Better intrinsic estimates for g_K, or other actual-profile probability information, could still make adaptive windows work.
- In particular, the companion theorem using divergence of sum_K delta_K remains a valid unresolved sufficient route. The universal fixed-alpha target remains unresolved.

## Inputs

The canonical encoding and increasing-state bridges are the accepted PASS2 EXACT_GREEDY_TRANSFER.md and PASS3 GRADED_CELL_OBSTRUCTION.md. The first-frontier exponent is in PASS3 WEIGHTED_OPERATOR_BOUNDARY.md. The independent PASS4 gap lane supplies the quantitative lower certificate based on (1). All new inequalities here are elementary and all-size; finite checks are regression evidence only.
