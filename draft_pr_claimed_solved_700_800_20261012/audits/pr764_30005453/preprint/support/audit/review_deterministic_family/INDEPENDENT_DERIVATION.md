# Independent deterministic derivation

Written before reading historical audit or acceptance conclusions. Exact input is bound in INPUT_BINDING.json.

## Claim, assumptions and falsification target

For a countable simple graph without isolates, 1 <= degree <= D and 0 < p_v <= P, and beta=alpha/(1-alpha)>0, the candidate asserts unique positive z satisfying

    z_v sum_{w~v}(z_v+z_w)^beta = p_v.

It also asserts that every coordinatewise positive complete classical trajectory

    b'_v=(1-alpha)(p_v / sum_{w~v}(b_v+b_w)^beta - b_v)

with a common finite upper bound is this z, even when inf p_v=0. These are the actual new deterministic steps being checked. Boundary equilibria and the exact bundled source target must be considered separately.

## Existence: independent argument

On finite F, zero exterior data give a finite C2 interior strictly convex energy: sum over edges meeting F of (z_u+z_v)^(beta+1)/(beta+1) minus sum p_v log z_v. Positive degrees ensure coercivity: the edge energy is at least (1/2)/(beta+1) sum_{v in F} z_v^(beta+1). For beta+1>1 this dominates the finite sum of logarithms. In a bounded sublevel set, -p_v log z_v tends to infinity at any zero coordinate while the other finite summands remain bounded below. Thus a minimizer is interior. Its gradient gives T_v(z)=p_v/z_v. The log Hessian is positive definite; the edge Hessians are positive semidefinite, so the minimizer is unique for each F.

The equations yield z_v^(beta+1) <= p_v/degree(v) <= P and hence z_v <= B=P^(1/(beta+1)). All neighbors are then <=B, including the zero exterior values, giving z_v >= p_v/[degree(v)(2B)^beta]. Each fixed coordinate has its own strictly positive lower bound once included. Countability yields a subsequence converging in every coordinate, not in sup norm. Local finiteness permits passage through T_v, and the fixed-coordinate lower bound survives. This proves infinite-volume existence. No monotonicity of finite-volume minimizers, summability of p, finite total energy, boundary uniqueness, or compactness in the uniform topology is used.

## Uniqueness: independent approximate-extremum calculation

Two positive solutions are both bounded by B, including solutions not assumed bounded initially. Let M=sup |z-y|>0. One orientation has supremum M; choose z_v-y_v > M-epsilon in that orientation. Since all neighbor differences are >=-M, each edge-sum difference is >-epsilon. A uniform modulus omega of x^beta on [0,2B] gives T_v(z)-T_v(y) >=-D omega(epsilon). Also z_v>M-epsilon and T_v(z)>=z_v^beta. Thus

    0=(z_v-y_v)T_v(z)+y_v(T_v(z)-T_v(y))
      >=(M-epsilon)^(beta+1)-BD omega(epsilon).

The last expression is strictly positive for small epsilon, contradiction. This works for 0<beta<1 despite the derivative singularity at zero: omega(epsilon)=epsilon^beta suffices. For beta>=1 take omega(epsilon)=beta(2B)^(beta-1)epsilon. No lower rate bound enters.

## Limiting trajectories: independent compactness check

Given the stochastic preliminaries' coordinate bounds and exact asymptotic edge representation, every fixed coordinate of a(s) is uniformly bounded and eventually uniformly Lipschitz on shifted compact intervals, with constants depending on that coordinate. A diagonal over countable vertices and integer compact intervals gives a complete locally uniform coordinatewise limit. An error r_e(t)->0 automatically converges uniformly for t in [exp(s_n-j),exp(s_n+j)] since its lower endpoint tends to infinity. Finite incident sums and fixed strictly positive lower coordinate bounds permit continuous passage through the reciprocal denominator in the integral equation. Hence the limit is a classical complete positive trajectory. This step does not require a common positive lower bound or uniform spatial martingale control.

## Rigidity: independent derivation and attempted falsification

Let b be a positive complete trajectory bounded above by K0>=B and d=b-z. M=sup_{v,s}|d_v(s)| is finite. Suppose M>0. For epsilon<M/4 choose delta=BD omega(epsilon)/(M/2)^beta<M/4, where omega is on [0,2K0].

If d_v>=M-epsilon, then every edge-sum difference is >=-epsilon and b_v>M/2. Thus T_v(b)>=T_v(z)-D omega(epsilon), T_v(b)>=(M/2)^beta, and

    R_v(b)-z_v=z_v(T_v(z)-T_v(b))/T_v(b) <= delta.

Consequently d'_v<=c(delta-M+epsilon)<=-cM/2. If d_v<=-M+epsilon, each edge-sum difference is <=epsilon and z_v>M/2. Since T_v(b)<=T_v(z)+D omega(epsilon),

    R_v(b)-z_v >= -z_v D omega(epsilon)/(T_v(z)+D omega(epsilon)) >= -delta,

giving d'_v>=cM/2. A coordinate within epsilon of the absolute supremum exists by definition. In the upper case it stays in the upper strip for all preceding times: a finite left endpoint would require crossing upward through the lower strip boundary, while the derivative is uniformly negative at that boundary and inside. Backward integration forces it above M, impossible. The lower case similarly forces it below -M. Therefore M=0.

I looked for failure from an unattained spatial/time supremum, vanishing p_v, nonuniform lower bounds, beta<1, beta>1, and backward strip crossing. None invalidates this argument. In disconnected single-edge components with rates tending to zero, the symmetric scalar equation has b^(beta+1)=p/2^beta+C exp(-s), since c(beta+1)=1. A nonzero C either loses positivity backward (C<0) or loses boundedness backward (C>0); thus it cannot be a counterexample to the complete-trajectory lemma. This is a useful limiting-case diagnostic rather than a proof of all graphs.

## Provisional deterministic verdict

Sections 2, 6 and 7 supply checkable mechanisms and do not transfer the difficulty to an unsupported equivalent uniqueness or convergence claim. The positive theorem is mathematically plausible with no deterministic gap found. This is provisional pending independent controls and the exact original-source scope: the author explicitly corrects a literal nonnegative-uniqueness claim and may therefore not resolve a bundled source assertion as a positive theorem without framing the correction honestly.
