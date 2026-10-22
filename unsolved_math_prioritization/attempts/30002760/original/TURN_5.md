# Approach 5: parabolic residual control and time-space allocation

## Aim and disposition

Attempt to lift stationary approximation results to evolution equations. Energy stability and optimal allocation of independent spatial budgets can be proved, but neither controls an unrefined temporal error. The remaining time-space approximation-class problem is explicit.

## Proposition 5.1 (energy residual estimate)

Let V be a real Hilbert space densely and continuously embedded in H, identified in the Gelfand triple V subset H subset V'. Let a(t;.,.) be measurable and bounded on V uniformly in t, with a(t;v,v)>=||v||_V^2. Suppose u and a continuous reconstruction U belong to L^2(0,T;V) intersect H^1(0,T;V'), and u'+A(t)u=f. Put e=u-U and r=f-U'-A(t)U in L^2(0,T;V'). Then for every t in [0,T],

||e(t)||_H^2 + integral_0^t ||e||_V^2
<= ||e(0)||_H^2 + integral_0^t ||r||_{V'}^2.

Proof. The Gelfand-triple energy identity gives (1/2)d||e||_H^2/dt=<e',e>. Since e'+Ae=r, coercivity and dual Cauchy-Schwarz imply
(1/2)d||e||_H^2/dt+||e||_V^2 <= ||r||_{V'}||e||_V
<= (1/2)||r||_{V'}^2+(1/2)||e||_V^2.
Integrate after multiplying by two. The identity can first be proved for smooth time approximations, then passed to the stated Sobolev class by density and continuity of the H-valued traces. In particular,

sup_t ||e(t)||_H^2 + integral_0^T||e||_V^2
<= 2[||e(0)||_H^2+integral_0^T||r||_{V'}^2].

For homogeneous-boundary convection-diffusion, a skew convection term contributes zero to a(v,v), so it does not enter the displayed constant. The V norm may itself depend on epsilon (for example sqrt(epsilon)||gradient v||); this is not a uniform comparison with an unweighted H^1 norm. A discontinuous time approximation requires a reconstruction or separate jump terms before applying this proposition. Distributional jumps are not silently treated as L^2 residuals.

## Proposition 5.2 (exact allocation benchmark)

Let M>=1, p>0, b_i>0, and a total real budget N>0. For positive allocations n_i with sum n_i=N,

sum_i b_i n_i^-p >= N^-p [sum_i b_i^(1/(p+1))]^(p+1).

Equality is attained at n_i=N b_i^(1/(p+1))/B, B=sum_i b_i^(1/(p+1)). To prove the lower bound, apply Hölder with conjugate exponents p+1 and (p+1)/p to
B=sum_i (b_i n_i^-p)^(1/(p+1)) n_i^(p/(p+1)).
Raise the resulting inequality to power p+1 and rearrange. Direct substitution proves equality. This establishes the global minimum, without relying only on a stationary-point calculation.

Rounding each optimum upward gives integer allocations of total at most N+M and no larger error. More usefully, if an integer budget L>=2M is prescribed, apply the real optimizer at N=L-M and round upward. The resulting positive integers sum to at most L, and their error is at most 2^p B^(p+1)L^-p. This remains only a fixed-M allocation statement; when the number of time intervals varies, its cost must be included.

For a fixed temporal partition, if independent squared spatial-error contributions are bounded by b_i n_i^-2s, take p=2s. The theorem then identifies the best allocation in this particular separable upper-bound model. The b_i, exponent, independence and absence of transfer/temporal terms are hypotheses; the theorem does not certify them for arbitrary evolving meshes.

## Proposition 5.3 (a fixed time step defeats spatial-only convergence)

Take a time-independent coercive operator A:V -> V' and a nonzero phi in V. Set u(t)=t^2 phi on [0,1], u(0)=0 and f(t)=2t phi+t^2 Aphi, where H is embedded into V'. Exact spatial solution of one backward-Euler step of length one gives U_1 in V satisfying

(U_1,v)_H+a(U_1,v)=2(phi,v)_H+a(phi,v), for all v in V.

The exact endpoint is phi. Therefore w=U_1-phi is the unique solution of
(w,v)_H+a(w,v)=(phi,v)_H.

It cannot be zero: otherwise the right-hand side would vanish for all v, including v=phi. Thus even exact spatial resolution leaves a nonzero temporal endpoint error. Any convergent spatial finite-element sequence for this fixed time-discrete problem approaches U_1, not u(1). For the exact scalar instance H=V=R, A=1 and phi=1, U_1=3/2 while u(1)=1; the squared endpoint error is 1/4.

This is a counterexample to the specific claim that arbitrarily good spatial solves on a fixed time grid force convergence to the parabolic solution. It does not obstruct properly time-adaptive methods.

## Remaining gap and credit

Energy estimates, Hölder allocation, and backward-Euler consistency are classical. These proofs are reconstructed diagnostics, without novelty claims. The remaining target needs a defined space-time refinement family and norm, temporal and spatial residual reliability/efficiency, controlled mesh-transfer and test-space costs, and global rate optimality over that family. Recent time-adaptive and minimal-residual papers resolve important narrower questions but cannot be substituted for all these requirements; see SOURCE_SCOPE.md.
