# Turn4: quantitative nonlinear hyperbolic localization

AI-assisted proof attempt; independent review pending. This is a sufficient local condition, not a necessary characterization for arbitrary f.

Let E=E_s⊕E_u be a finite-dimensional real vector space, with the maximum of chosen norms on the two summands. Let A=A_s⊕A_u, with A_u invertible and
||A_s||≤ρ, ||A_u^(-1)||≤ρ, 0<ρ<1.
A zero-dimensional summand is permitted. On a region U let f(x)=Ax+g(x), where
||g(x)−g(y)||≤ε||x−y|| for x,y∈U.
Choose ρ<θ<1 and put
K=(1+ρθ)/(θ−ρ)+(θ+ρ)/(1−ρθ).
Assume εK<1.

For any two trajectories x_0,...,x_T and y_0,...,y_T remaining in U, with endpoint distances at most D, the following finite-horizon estimate holds:
||x_t−y_t||≤D/(1−εK) [θ^t+θ^(T−t)], 0≤t≤T.

Proof. Write z_t=x_t−y_t and r_t=g(x_t)−g(y_t), so ||r_t||≤ε||z_t||. Variation of constants in stable and unstable coordinates gives
z_t^s=A_s^t z_0^s+sum_(k<t) A_s^(t−1−k)r_k^s,
z_t^u=A_u^(-(T−t))z_T^u−sum_(k=t)^(T−1) A_u^(-(k−t+1))r_k^u.
Only the unstable linear block is inverted; f need not be invertible. With a_t=||z_t|| and w_t=θ^t+θ^(T−t), each component and therefore their maximum obeys
 a_t≤D w_t+ε[sum_(k<t)ρ^(t−1−k)a_k+sum_(k≥t)^(T−1)ρ^(k−t+1)a_k].
The two geometric sums applied to w_k have coefficients at most
 C_1=1/(θ−ρ)+ρ/(1−ρθ) on θ^t,
 C_2=θ/(1−ρθ)+ρθ/(θ−ρ) on θ^(T−t).
Their sum is K, so the bracket is at most K w_t max_k(a_k/w_k). Taking the finite maximum yields M≤D+εKM and proves the bound. All sums remain valid at endpoints and T=0.

## Feasible-set consequence
Suppose every observed cell P_t is contained in U, and diam(P_0),diam(P_T)≤D in this norm. By turn1, every pair in Q_t extends to full admissible trajectories; applying the bound gives
diam(Q_t)≤D/(1−εK)[θ^t+θ^(T−t)].
Thus central feasible sets shrink exponentially as both distances to the endpoints grow. Norm equivalence translates this to an explicit Euclidean bound after its fixed comparison constant is included.

If E_u=0, the simpler direct estimate gives ||z_t||≤(ρ+ε)^t||z_0||. For ρ+ε<1, diam(Q_T)≤(ρ+ε)^T D. If E_s=0, the equation z_(t+1)=Az_t+r_t gives
||z_t||≤ρ||z_(t+1)||+ρε||z_t||,
so diam(Q_0)≤[ρ/(1−ρε)]^T D provided ρε<1 and ρ/(1−ρε)<1. This is an inverse-Lipschitz trajectory estimate and does not assume a globally defined inverse map.

## A concrete C1 condition at the source's fixed point
Let f be C1 near a fixed point x*, and suppose Df(x*) has no eigenvalue of modulus1. The finite-dimensional stable/unstable generalized eigenspaces admit norms with the displayed block bounds for someρ<1 (chooseρ strictly larger than the stable spectral radius and the inverse unstable spectral radius). In translated coordinates set A=Df(x*) and g(x)=f(x*+x)−x*−Ax. On a sufficiently small convex norm ball, continuity of Df gives Lip(g)≤ε for any prescribed positiveε. Chooseθ and then εK<1. Therefore the displayed finite-horizon bound applies whenever all observed cells, and hence both feasible trajectories, lie in that ball.

This proves the suggested hyperbolic central localization without invoking an informal claim that a finite feasible set is literally a stable/unstable manifold neighborhood. No assertion is made for observations that leave the controlled neighborhood, nonhyperbolic center directions, arbitrary coarse partitions, or numerical computation of an exact nonlinear image. Hyperbolic/dichotomy and geometric-series methods are classical; no novelty certification is made.
