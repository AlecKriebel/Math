# No uniform inverse Wasserstein bound for equator averaging

Problem 30000999 / OWR-2042-008. Research note, 3 October 2026.

## Status and scope

The answer to the stated all-probability-measures question is **no**. Antipodal point masses already disprove it. The parity obstruction is classical; no novelty or historical priority is claimed. We additionally give a self-contained quantitative obstruction on smooth, positive, antipodally symmetric densities for every finite Wasserstein order and sphere dimension at least two. This stronger statement is useful if one repairs the original question by imposing evenness.

This is AI-assisted, unrefereed work. It is not a claim of human verification. Source attribution and the limits of the literature search are recorded in SOURCE_GATE.md.

## 1. Exact convention

Let n >= 2, let S = S^{n-1} be the unit sphere in R^n, and use its intrinsic geodesic distance d(x,y) = arccos(x dot y). Let sigma be normalized spherical surface measure. For u in S put E(u) = S intersect u-perp, and let sigma_u be normalized surface measure on E(u). When n = 2, sigma_u is the equal-weight measure on the two points of E(u).

Define the function transform and its measure dual by

    (F f)(u) = integral_{E(u)} f(x) d sigma_u(x),
    integral f d(R mu) = integral F f d mu.

Equivalently, R mu = integral sigma_u d mu(u), a probability measure on S. This is equator averaging, not the Euclidean hyperplane Radon transform or the sliced-Wasserstein transform. The order is 1 <= p < infinity, and

    W_p(mu,nu)^p = inf_gamma integral d(x,y)^p d gamma(x,y),

where gamma ranges over probability couplings. Compactness makes every such measure have finite p-th moment. No support restriction or antipodal symmetry is assumed in the original question. For n = 1 the equator is empty and this normalized transform is not defined; we make no assertion for that case.

## 2. Complete counterexample to the stated question

**Theorem 1.** For every n >= 2 and every 1 <= p < infinity, there is no finite C such that

    W_p(mu,nu) <= C W_p(R mu,R nu)

for all probability measures on S^{n-1}.

**Proof.** Fix u in S. Since E(u) = E(-u), the defining dual identity gives

    R delta_u = sigma_u = sigma_{-u} = R delta_{-u}.

The only coupling of delta_u and delta_{-u} is delta_{(u,-u)}, so

    W_p(delta_u,delta_{-u}) = d(u,-u) = pi,
    W_p(R delta_u,R delta_{-u}) = 0.

The proposed estimate would assert pi <= 0. This proves the claim. The same example also works for p = infinity, although that order is outside the cited report's stated range. QED.

More generally, if A(x) = -x, then R A_#mu = R mu and

    R mu = R((mu + A_#mu)/2).

Consequently no inverse modulus omega with omega(0) = 0 can hold on the unrestricted class. Smoothness and strict positivity alone do not repair injectivity: for any 0 < a < 1, the distinct probability densities 1 + a x_1 and 1 - a x_1 have identical transforms. Their W_1 distance is at least 2a/n, by testing the 1-Lipschitz function x_1, whose squared sigma-average is 1/n. The equality of transforms follows either from antipodal pushforward or odd-function cancellation.

## 3. Even, smooth, positive densities still have no Lipschitz inverse

**Theorem 2.** Fix n >= 3, 1 <= p < infinity, and 0 < a < 1. There are even C-infinity probability densities rho_k on S, all satisfying

    1-a <= rho_k <= 1+a,

such that, for mu_k = rho_k sigma,

    W_p(mu_k,sigma) / W_p(R mu_k,sigma) -> infinity.

In particular, evenness and uniform positive lower and upper density bounds do not restore the proposed uniform reverse inequality. The denominator below is nonzero for each k. No uniform bound on derivatives of rho_k is assumed.

### 3.1 Symmetry and the density action

The probability measure sigma(du) sigma_u(dx) on the set of orthogonal pairs (u,x) is symmetric under exchanging u and x. To see this, it is the unique O(n)-invariant probability on that homogeneous space; exchanging the coordinates preserves invariance. Therefore F is self-adjoint with respect to sigma and

    R(rho sigma) = (F rho) sigma,       R sigma = sigma.

### 3.2 Explicit harmonic and its equatorial eigenvalue

For an even positive integer k = 2m define

    H_k(x) = Re (x_1 + i x_2)^k,        r = sqrt(x_1^2 + x_2^2).

This real polynomial is homogeneous of degree k and harmonic in R^n. Its restriction to S obeys

    -Delta_S H_k = k(k+n-2) H_k,
    |H_k| <= r^k <= 1,
    |grad_S H_k| <= k r^{k-1} <= k.

The Laplace eigenvalue follows by inserting a degree-k homogeneous harmonic function into the Euclidean polar-coordinate Laplacian. Its mean is zero: rotation in the (x_1,x_2)-plane by pi/k sends H_k to -H_k and preserves sigma. Because k is even, H_k(-x) = H_k(x).

The exact eigenvalue of equator averaging is

    F H_{2m} = lambda_{2m} H_{2m},
    lambda_{2m} = (-1)^m product_{j=0}^{m-1} (2j+1)/(n-1+2j).

Here is a direct derivation, avoiding a representation-theoretic assumption. If X is uniform on the unit sphere of a d-dimensional Euclidean space, its polynomial moment is

    E[(v dot X)^{2m}] = [(2m-1)!! / product_{j=0}^{m-1}(d+2j)] (v dot v)^m.

For real v, rotate it to a coordinate axis and compute the one-coordinate beta moment (or compare Gaussian moments and the radial Gaussian moment). Both sides are polynomial in v, so the identity also holds for complex v with the bilinear, not Hermitian, dot product.

For the equator use d = n-1, w = e_1 + i e_2 and v = (I - u u^T)w. Since w dot w = 0,

    v dot v = -(w dot u)^2.

Taking real parts proves the displayed formula for all u. The product is nonzero and has absolute value at most 1. With alpha = (n-2)/2 > 0,

    |lambda_{2m}| = Gamma((n-1)/2) Gamma(m+1/2)
                       / [sqrt(pi) Gamma(m+(n-1)/2)]
                  asymptotic to [Gamma((n-1)/2)/sqrt(pi)] m^{-alpha}.

The asymptotic follows directly from Stirling's formula for the ratio of gamma functions. These are the classical Funk-transform eigenvalues, derived here for this explicit family.

### 3.3 Exact radial moments

For n >= 3, r^2 under sigma has the Beta(1,alpha) distribution, alpha = (n-2)/2. For example, this follows by dividing the sum of squares of two independent standard Gaussians by the sum of squares of n of them. Hence, for q >= 0,

    M(q) := integral r^q d sigma
          = Gamma(alpha+1) Gamma(q/2+1) / Gamma(q/2+alpha+1).

Conditionally on r, the polar angle in the first two coordinates is uniform. Thus for k >= 1,

    integral H_k^2 d sigma = M(2k)/2,
    ||grad_S H_k||_{L^p(sigma)} <= k M(p(k-1))^{1/p}.

For fixed positive c, Stirling's formula gives M(c k + O(1)) asymptotic to Gamma(alpha+1)(c k/2)^{-alpha}.

### 3.4 Input distance lower bound

Set rho_k = 1 + a H_k. The preceding properties establish evenness, positivity, normalization and the fixed density bounds. The function H_k/k is 1-Lipschitz for the intrinsic metric, since its tangent gradient is at most 1. Every coupling gamma of mu_k and sigma satisfies

    integral d(x,y) d gamma >= integral (H_k/k) d(mu_k-sigma)
                            = a M(2k)/(2k).

On a probability space the L^p norm dominates the L^1 norm, so

    W_p(mu_k,sigma) >= W_1(mu_k,sigma) >= a M(2k)/(2k).          (1)

This uses only the elementary Lipschitz test inequality, not attainment of the Kantorovich dual problem.

### 3.5 Output upper bound by an explicit smooth flow

Write b = a lambda_k and L = k(k+n-2). Since F H_k = lambda_k H_k,

    R mu_k = (1+b H_k) sigma.

For 0 <= t <= 1 put

    eta_t = 1 + t b H_k,
    v_t = b grad_S H_k / (L eta_t).

The denominator is at least 1-a > 0, so v_t is a smooth, globally defined, time-dependent vector field on the compact sphere. Moreover,

    partial_t eta_t + div_S(eta_t v_t)
      = b H_k + (b/L) Delta_S H_k = 0.

The flow Phi_t of v_t therefore sends sigma to eta_t sigma: this follows from the change-of-variables/Jacobian equation, or uniqueness for the smooth continuity equation. The map x -> (x,Phi_1(x)) is a coupling of sigma and R mu_k. By the length bound on endpoint distance and Jensen's inequality in t,

    W_p(R mu_k,sigma)^p
      <= integral_S integral_0^1 |v_t(Phi_t(x))|^p dt d sigma(x)
       = integral_0^1 integral_S |v_t(y)|^p eta_t(y) d sigma(y) dt
      <= |b|^p L^{-p} (1-a)^{1-p} integral_S |grad_S H_k|^p d sigma.

This includes p = 1, for which Jensen is equality and the density power is zero. Using the gradient moment bound gives

    W_p(R mu_k,sigma)
      <= a |lambda_k| (1-a)^{-(p-1)/p}
             M(p(k-1))^{1/p}/(k+n-2).                         (2)

Because lambda_k is nonzero and H_k is nonzero, R mu_k differs from sigma, so the denominator in the theorem is positive.

### 3.6 Diverging ratio

Combining (1) and (2),

    W_p(mu_k,sigma) / W_p(R mu_k,sigma)
      >= [(k+n-2)/(2k)] (1-a)^{(p-1)/p}
            M(2k) / [|lambda_k| M(p(k-1))^{1/p}].              (3)

As k tends to infinity through even integers, M(2k) and |lambda_k| are positive constants times k^{-alpha}, while M(p(k-1))^{1/p} is a positive constant times k^{-alpha/p}. The right side of (3) is therefore asymptotic to a strictly positive constant times

    k^{alpha/p} = k^{(n-2)/(2p)} -> infinity.

This proves Theorem 2. The exponent is a sufficient lower bound for this construction; no optimal asymptotic for the actual Wasserstein ratio is asserted. QED.

## 4. Circle boundary case and limits

For n = 2, if J denotes rotation by pi/2, then

    R mu = (J_#mu + (-J)_#mu)/2.

If mu is even, (-J)_#mu = J_#mu and R mu = J_#mu. Consequently R is an isometry on the even probabilities of S^1 for every p in [1,infinity], with reverse constant 1. The distinction n >= 3 in Theorem 2 is necessary. Theorem 1 still rules out the unrestricted circle problem.

The even-density theorem here is only for finite p. No W_infinity even-density conclusion is asserted. The construction does not settle restricted-support, finite-bandwidth, uniformly derivative-bounded, Hölder-inverse or optimal-modulus variants. Passing to antipodal equivalence removes the point-mass obstruction but cannot by itself provide a uniform same-order Lipschitz inverse in the n >= 3 even-density setting just proved.

## References

1. Benjamin K. Stephens, contribution “Measuring the Geodesic Radon Transform with Mass Transport,” in *Calculus of Variations*, Oberwolfach Report 31/2008, printed pp. 1762–1764. [Report DOI](https://doi.org/10.4171/OWR/2008/31). [Official report PDF](https://ems.press/content/serial-article-files/46174). The question and exact transform are on p. 1763.
2. Michael Quellmalz, *The Funk–Radon transform for hyperplane sections through a common point*, Analysis and Mathematical Physics 10, 38 (2020), [DOI 10.1007/s13324-020-00383-2](https://doi.org/10.1007/s13324-020-00383-2). Sections 2.2.2 and 4 identify the normalized classical transform and its odd nullspace; the introduction and Section 6 discuss the classical Sobolev smoothing degree and credit prior work. This reference supports the classical context, not a claimed previously published exact Wasserstein theorem.
