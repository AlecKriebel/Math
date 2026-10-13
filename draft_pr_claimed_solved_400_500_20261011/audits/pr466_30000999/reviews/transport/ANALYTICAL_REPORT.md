# Independent transport and normalization audit — PR 466 / problem 30000999

## Result and scope

**Verdict: the mathematical claims in the frozen `PROOF.md` pass this independent analytical route. No mandatory mathematical correction was found.** In particular, Theorem 2 is valid for every integer ambient dimension n >= 3, every fixed real 1 <= p < infinity, and every fixed 0 < a < 1. Its proof does not require p to be an integer. The quantitative lower bound is asymptotic to a positive constant times k^((n-2)/(2p)) along positive even integers k.

This audit reconstructs transport from a smooth ODE and its volume Jacobian, rather than invoking a dynamic optimal-transport formula. The harmonic transform and normalized moments are rederived directly from Gaussian moments. I read only the frozen proof before writing `INITIAL_HYPOTHESIS.md`; I did not consult prior audits, peers' conclusions, or the frozen author's computation scripts/results. The numerical checks here are independently written and are not a proof of any universal claim.

The strongest verified result is exactly the finite-p, even, smooth, uniformly positive density obstruction, together with the unrestricted antipodal counterexample and the even-circle isometry. No remaining mathematical gap was found for these stated claims. This audit does not establish historical priority, a present open-problem status, optimality of the displayed divergence exponent, or human review.

## 1. Target, conventions, and primary-source scope check

Let S = S^(n-1) in R^n, n an integer >= 2, with normalized surface probability sigma and intrinsic metric d(x,y)=arccos(x dot y). For each unit u, let sigma_u be normalized surface probability on S intersect u-perp; for n=2 it assigns probability 1/2 to each of two points. Define

    Ff(u) = integral f(x) d sigma_u(x),
    integral f d(Rmu) = integral Ff dmu.

The target reverse estimate is W_p(mu,nu) <= C W_p(Rmu,Rnu), with W_p^p equal to the infimum of the probability-coupling d^p cost. The literal published setup has this normalized dual transform on spherical probability measures and finite orders p in [1,infinity); the reverse question follows its forward contraction discussion. The report's passage does not impose evenness or a support restriction. This is a source-scope check, not an interpretation of the author's unstated intention. See Stephens, printed p. 1763, PDF page index 56, in the [official Oberwolfach report](https://ems.press/content/serial-article-files/46174).

The important dimensions are different and correctly used in the proof:

| Object | Dimension/convention |
|---|---|
| Original Euclidean space | n |
| Original sphere | n-1 |
| Equator's Euclidean linear space u-perp | n-1 |
| Equator as a sphere | n-2 |
| Remaining Gaussian coordinates after x_1,x_2 | n-2 |
| Beta parameter | alpha=(n-2)/2 |

For n=1 the equator is empty and its normalized probability is undefined. Excluding it is necessary and correct.

## 2. The unrestricted obstruction and elementary Lipschitz test

For every u, E(u)=E(-u), so R delta_u=R delta_(-u). The only coupling of the two point masses sends u to -u and has distance pi at every point. Thus W_p(delta_u,delta_(-u))=pi for every finite p, while the output distance is zero. The same observation works for the usual essential-supremum W_infinity cost. This proves the literal unrestricted negative answer without any transport regularity assumption.

If A(x)=-x, Ff(u)=Ff(-u), hence R(A_#mu)=Rmu and Rmu equals the transform of the evenized measure (mu+A_#mu)/2. Any inverse modulus satisfying omega(0)=0 fails on the unrestricted class.

For a smooth counterexample to injectivity, rho_+=1+a x_1 and rho_-=1-a x_1 are smooth probability densities for 0<a<1. Odd-function cancellation on every equator gives F x_1=0. The coordinate x_1 is 1-Lipschitz in the intrinsic metric, because its tangent gradient has norm sqrt(1-x_1^2)<=1. Rotation symmetry and sum_j x_j^2=1 give integral x_1^2 d sigma=1/n. Therefore every coupling satisfies

    integral d(x,y) dgamma >= integral x_1 d(mu_+-mu_-)=2a/n.

The resulting lower W_1 bound has the correct factor 2 and correct probability normalization. No assertion of Kantorovich-dual attainment is needed.

## 3. Density action and self-adjointness

The incidence probability M(du,dx)=sigma(du) sigma_u(dx) is O(n)-invariant. O(n) acts transitively on the compact space of ordered orthogonal unit pairs: complete an orthogonal pair to an orthonormal basis and map one basis to another. On a compact homogeneous space, the invariant probability is unique: averaging a continuous function over Haar probability on O(n) gives the same value starting at any pair, so every invariant probability has the same integral of that function.

Swapping the two coordinates preserves O(n)-invariance and hence M. Thus, for continuous f,g,

    integral g(u) Ff(u) d sigma(u)
      = integral f(x) Fg(x) d sigma(x).

Setting g=rho gives R(rho sigma)=(F rho)sigma. Taking rho=1 gives R sigma=sigma, since F1=1. This justifies the density transform and transport target, rather than assuming the function and measure transforms coincide by notation.

## 4. Harmonic, tangent gradient, and equator eigenvalue

Fix a positive even integer k=2m and put z=x_1+i x_2, H_k=Re z^k, r=|z|. The polynomial is homogeneous of degree k. Its Euclidean gradient in the first two coordinates is

    grad_R H_k = (k Re z^(k-1), -k Im z^(k-1), 0, ..., 0).

The two second derivatives cancel, so Delta_R H_k=0. Euler's homogeneous identity is x dot grad_R H_k=kH_k. Restricting to the unit sphere gives

    grad_S H_k=grad_R H_k-kH_k x,
    |grad_S H_k|^2=k^2(r^(2k-2)-H_k^2) <= k^2 r^(2k-2).

This identity proves the claimed gradient bound globally, including r=0, without using polar coordinates at their singular set. The Euclidean polar Laplacian applied to R^k H_k(x/R) gives

    Delta_S H_k=-k(k+n-2)H_k.

The bound |H_k|<=r^k<=1 follows from the real part. Its mean is zero by plane rotation through pi/k, which changes its sign. Even k gives H_k(-x)=H_k(x). Its value at e_1 is 1, so it is not the zero function.

For the transform eigenvalue, first take uniform X on a unit sphere in a d-dimensional Euclidean space. Write a standard Gaussian vector G=R X, where direction and radius are independent. For real v,

    E[(v dot G)^(2m)]=(2m-1)!! (v dot v)^m,
    E[R^(2m)]=product_(j=0)^(m-1)(d+2j).

Dividing gives

    E[(v dot X)^(2m)]
      = (2m-1)!! (v dot v)^m / product_(j=0)^(m-1)(d+2j).

Both sides are polynomials in the coordinates of v. A polynomial identity holding for all real coordinates extends to complex coordinates. The dot product remains bilinear: replacing it by a Hermitian product here would invalidate the argument.

For the equator use d=n-1, w=e_1+i e_2, and P=I-u u^T. Since X lies in u-perp, w dot X=(Pw) dot X. The complex bilinear calculation is

    (Pw) dot (Pw)=w dot w-(w dot u)^2=-(w dot u)^2.

Taking the real part of the moment formula therefore gives, at every u,

    FH_(2m)(u)=lambda_(2m) H_(2m)(u),
    lambda_(2m)=(-1)^m product_(j=0)^(m-1)(2j+1)/(n-1+2j).

Every factor has positive denominator. For n>=2, its absolute value is <=1 and it is nonzero. For n>=3, the first factor is <=1/2 and every subsequent factor is strictly less than one, so |lambda_k|<=1/(n-1)<=1/2 for all selected k. The proof uses only the weaker bound <=1, which is sufficient.

With alpha=(n-2)/2>0,

    |lambda_(2m)|
      = Gamma(alpha+1/2) Gamma(m+1/2)
        / [sqrt(pi) Gamma(m+alpha+1/2)].

The product and gamma formula have the same sign-free normalization; there is no missing surface-area factor.

## 5. Radial and angular moments, including the smallest dimension

Let G_j be independent standard Gaussians. Then U=G_1^2+G_2^2 has Gamma shape 1, V=sum_(j=3)^n G_j^2 has Gamma shape alpha=(n-2)/2, and U,V are independent with equal scale. Changing variables to s=U/(U+V) and T=U+V shows that s has normalized density alpha(1-s)^(alpha-1) on (0,1). Thus r^2 has Beta(1,alpha) law. The plane angle theta is uniform and independent of r, by plane rotational symmetry of the Gaussian law.

For every real q>=0,

    M(q)=integral r^q d sigma
        =alpha integral_0^1 s^(q/2)(1-s)^(alpha-1) ds
        =Gamma(alpha+1) Gamma(q/2+1)/Gamma(q/2+alpha+1).

In particular M(0)=1, as required for normalized sigma. The angular mean of cos^2(k theta) is 1/2 for every nonzero integer k. Therefore

    integral H_k^2 d sigma=M(2k)/2,
    integral |grad_S H_k|^p d sigma <= k^p M(p(k-1)).

This calculation allows arbitrary real p>=1; p(k-1) is a nonnegative real exponent. At the smallest stated ambient n=3, alpha=1/2. The beta density has an integrable endpoint singularity and all displayed moments remain finite and positive. At n=2, alpha=0 would fail this beta-density derivation; the proof correctly uses a separate circle argument instead.

## 6. Input distance: test function and inequality direction

Put rho_k=1+aH_k, 0<a<1. Its mean is one, and it is smooth, even, and in [1-a,1+a]. The tangent gradient bound makes f=H_k/k globally 1-Lipschitz: integrate its derivative along a minimizing spherical geodesic.

For every probability coupling gamma of rho_k sigma and sigma,

    integral d dgamma
      >= integral (f(x)-f(y)) dgamma
       = a integral H_k^2 d sigma / k
       = a M(2k)/(2k).

For real p>=1, Holder on a probability space gives integral d <= (integral d^p)^(1/p). Taking the infimum over all couplings thus gives

    W_p(rho_k sigma,sigma) >= W_1(rho_k sigma,sigma)
                            >= a M(2k)/(2k).                 [INPUT]

The lower bound is strictly positive. This establishes the needed direction and does not mistake an arbitrary coupling for an optimizer.

## 7. Independent Jacobian reconstruction of the output coupling

Set b=a lambda_k and L=k(k+n-2)>0. The density action from Section 3 makes the output (1+bH_k)sigma. For t in [0,1] set

    eta_t=1+t bH_k,
    v_t=b grad_S H_k/(L eta_t).

The sharper lower bound eta_t>=1-|b|>0 holds. The bound eta_t>=1-a used in the proof is valid as well. The field is smooth in time and position and tangent to the compact sphere, so its ODE

    d Phi_t(x)/dt=v_t(Phi_t(x)),    Phi_0(x)=x

has a smooth global flow on [0,1]. It is a diffeomorphism at each t, with inverse obtained by solving the ODE backwards over a finite interval.

Let J_t(x)>0 be the volume Jacobian of Phi_t relative to spherical surface measure. Normalizing surface measure by its total area does not change this Jacobian. The Jacobian ODE is

    d J_t(x)/dt=(div_S v_t)(Phi_t(x)) J_t(x),    J_0(x)=1.

The continuity identity has the correct sign:

    partial_t eta_t+div_S(eta_t v_t)
      =bH_k+(b/L)Delta_S H_k=0.

Differentiating the full density-Jacobian product gives

    d[eta_t(Phi_t(x)) J_t(x)]/dt
      =[partial_t eta_t+grad_S eta_t dot v_t+eta_t div_S v_t](Phi_t(x)) J_t(x)
      =[partial_t eta_t+div_S(eta_t v_t)](Phi_t(x)) J_t(x)
      =0.

Its initial value is one. Hence eta_t(Phi_t(x)) J_t(x)=1 for every x,t. The change-of-variables formula then implies

    integral g(Phi_t(x)) d sigma(x)=integral g(y) eta_t(y) d sigma(y).

Consequently Phi_t#sigma=eta_t sigma, and gamma=(id,Phi_1)#sigma is a probability coupling of sigma and the claimed output. No unsupported uniqueness theorem for weak continuity equations is required.

## 8. Cost estimate for every real finite p

For each starting point x, the intrinsic endpoint distance is at most the length of its flow curve:

    d(x,Phi_1(x)) <= integral_0^1 |v_t(Phi_t(x))| dt.

For every real p>=1, convexity of s^p and interval length one give

    d(x,Phi_1(x))^p <= integral_0^1 |v_t(Phi_t(x))|^p dt.

For p=1 the convexity step is equality; the endpoint-distance/length bound may still be strict. Integrating against sigma and using the Jacobian-derived pushforward yields

    W_p((1+bH_k)sigma,sigma)^p
      <= integral_0^1 integral |v_t(y)|^p eta_t(y) d sigma(y) dt
       = |b|^p L^(-p) integral_0^1 integral |grad_S H_k|^p eta_t^(1-p) d sigma dt
      <= |b|^p L^(-p)(1-a)^(1-p) integral |grad_S H_k|^p d sigma.

The last direction is correct: 1-p<=0, so raising the lower bound eta_t>=1-a to this power gives an upper bound. For p=1 the density factor is exactly one. All integrands are nonnegative and bounded for fixed n,k,a,p, so there is no interchange or finiteness problem.

Using Section 5 and taking the p-th root gives

    W_p((1+bH_k)sigma,sigma)
      <= a |lambda_k| (1-a)^(-(p-1)/p)
         M(p(k-1))^(1/p)/(k+n-2).                         [OUTPUT]

The factor k in the gradient bound cancels one factor k in L; the remaining denominator is k+n-2. Probability normalization is used both in time Jensen and in the initial coupling, with no omitted factors.

The denominator in the ratio is strictly positive for every selected k. An explicit confirmation, stronger than simply invoking separation by the Wasserstein metric, is to apply Section 6's test with f=sign(b)H_k/k:

    W_p((1+bH_k)sigma,sigma) >= |b|M(2k)/(2k)>0,

because a>0, lambda_k!=0, and M(2k)>0.

## 9. Asymptotics and absence of a localization cancellation

For fixed real constants c,d, the gamma ratio Gamma(z+c)/Gamma(z+d) is asymptotic to z^(c-d) as real z tends to infinity. This follows by subtracting the two fixed-shift Stirling expansions; the remaining multiplicative error tends to one. See [NIST DLMF 5.11.12](https://dlmf.nist.gov/5.11#E12).

Write A=Gamma(alpha+1) and B=Gamma(alpha+1/2)/sqrt(pi). With k even tending to infinity and fixed n,p,

    M(2k) ~ A k^(-alpha),
    |lambda_k| ~ B 2^alpha k^(-alpha),
    M(p(k-1))^(1/p) ~ A^(1/p) (p/2)^(-alpha/p) k^(-alpha/p).

The factor from localized input mass cancels the transform eigenvalue's k^(-alpha), but the gradient's L^p moment contributes a further k^(-alpha/p) in the denominator. Therefore [INPUT]/[OUTPUT] gives

    W_p(rho_k sigma,sigma)/W_p(R(rho_k sigma),sigma)
      >= (k+n-2)/(2k) (1-a)^(1-1/p)
          M(2k)/[|lambda_k| M(p(k-1))^(1/p)]
       ~ C_(n,p,a) k^(alpha/p),

where the explicit constant is

    C_(n,p,a)
      = sqrt(pi) Gamma(alpha+1)^(1-1/p) p^(alpha/p) (1-a)^(1-1/p)
        / [2^(1+alpha+alpha/p) Gamma(alpha+1/2)].

Every factor in C_(n,p,a) is strictly positive and finite under the theorem's hypotheses. Since alpha>0 and p is fixed and finite, alpha/p>0. The right-hand side diverges, proving Theorem 2 for all such real p. This is a lower bound on the actual ratio, not an asymptotic equality for the actual optimal-transport distances.

A transparent normalization check is n=4, p=1: alpha=1, |lambda_k|=1/(k+1), M(2k)=1/(k+1), and M(k-1)=2/(k+1). The exact lower-ratio expression is (k+2)(k+1)/(4k), asymptotic to k/4, which agrees with the displayed C.

## 10. Boundary cases and quotient interpretation

### Amplitude and finite-order endpoints

- a=0 produces equal input/output measures and a 0/0 ratio; it is correctly excluded.
- a=1 loses strict positivity of the input and makes the published coarse factor (1-a) unsuitable. It is correctly excluded. The actual output flow remains regular for n>=3 because |lambda_k|<=1/2; this is an optional possible extension, not needed for the theorem.
- For every fixed 0<a<1, the bounds are uniform in k as claimed. No uniform conclusion as a tends to one is required.
- p=1 works with eta_t^(1-p)=1 and exponent alpha>0.
- Noninteger real p causes no algebraic or analytical difficulty: it appears only in positive real powers, Holder/Jensen, and gamma moments with positive arguments.
- p may be arbitrarily large but must be fixed before k tends to infinity. The proof is not uniform in p. Taking p=infinity replaces the positive exponent alpha/p by zero, and this argument cannot establish an even-density W_infinity obstruction. The frozen proof correctly excludes that claim.

### Circle case

For n=2, choose J as rotation by pi/2. The equator at u consists of Ju and -Ju, so Rmu=(J#mu+(-J)#mu)/2. If mu is even, (-J)#mu=J#mu, hence Rmu=J#mu. For any two even probabilities mu,nu, applying J simultaneously to a coupling preserves d and the d^p cost; applying J^(-1) supplies the converse inequality. Thus W_p(Rmu,Rnu)=W_p(mu,nu) for all finite p. The same two directions preserve the essential-supremum cost for W_infinity. The reverse constant is exactly one (unless the class is reduced to a singleton). The n>=3 restriction in Theorem 2 is therefore substantive.

### Antipodal/projective caveat

The last sentence of the frozen proof is correct as an informal limitation statement, but the word "equivalence" can denote different quotients. A precise natural interpretation uses q:S->RP^(n-1), with quotient metric d_Q([x],[y])=min(d(x,y),d(x,-y)). For even spherical probabilities mu,nu,

    W_p^S(mu,nu)=W_p^Q(q#mu,q#nu).

One direction follows by projecting any sphere coupling. For the converse, take a quotient coupling, choose measurable representatives x,y, choose a sign epsilon so d(x,epsilon y)=d_Q([x],[y]), and lift the pair to (x,epsilon y) and (-x,-epsilon y) with probability 1/2 each. This lift has the unique even marginals over the given quotient measures and exactly the same cost. Representatives and the sign can be chosen measurably by a coordinate-based section and the condition x dot y>=0; ties have equal costs. This proves the equality for finite p and also infinity.

The even H_k test descends to this quotient and is still 1-Lipschitz there, since it is even and its sphere Lipschitz estimate can be applied with both y and -y. The flow also descends because v_t(-x)=-v_t(x). Thus the even-density obstruction persists for the natural projective formulation. Merely quotienting whole measures by the two-element operation mu->A#mu does not identify all measures with the same evenization; no injectivity claim for that different quotient follows from the point-mass example alone. The frozen proof does not assert such a claim.

## 11. Falsification attempts and reproducibility artifacts

The independent checker `check_transport.py` uses only Python's standard library, writes only `numerical_checks.json` in this review folder, and imports none of the frozen author's code or output. It passed:

- Six exact integer-coefficient polynomial cases for Laplace harmonicity, the Euler identity, and |grad_R H_k|^2=k^2(x_1^2+x_2^2)^(k-1).
- Forty exact-product/rational versus gamma-normalization cases for moments and eigenvalues across n=3,4,5,10.
- Forty asymptotic parameter cases across n=3,4,5,10; p=1,1.25,sqrt(2),pi,31.5; and a=0.5,0.999, with even k up to 65536.
- Sixty independently integrated flow trajectories for n=3,5, k=2,4,8, amplitudes 0.8 and 0.999, including stationary poles, off-equator starts, and equatorial starts. Maximum density-Jacobian product error was 5.33e-15; maximum sphere-norm error was 4.22e-15.
- 240 trajectory endpoint/action inequalities including real noninteger p.

These computations are finite diagnostics of algebra, sign, and normalization. The universal statement rests on Sections 2–10, not on finite cases, discretization accuracy, or extrapolation.

## 12. Issue classification and exact remaining gap

### Mandatory issues

**None found within the stated mathematical scope.** No counterexample, reversed inequality, missing dimensional factor, hidden integer-p assumption, circular transport assertion, vanishing-denominator issue, or failed finite-order endpoint was found.

### Optional improvements

1. **Make the Jacobian step explicit in Section 3.5.** Adding the identity eta_t(Phi_t(x))J_t(x)=1 and its derivative would make the existing correct transport construction more directly checkable without a reader appealing to a continuity-equation uniqueness theorem.
2. **Define the intended antipodal equivalence.** If the final caveat means the natural projective metric quotient, the equality between projective W_p and spherical W_p on even measures can be stated or referenced. This improves precision; it is not needed for the written Theorem 2.
3. **Give an explicit positive denominator test.** The bound W_p((1+bH_k)sigma,sigma)>=|b|M(2k)/(2k)>0 follows from the same test function already used for the input. It supplements the existing correct statement that a nonzero density difference has positive Wasserstein distance.

No mathematical gap remains for the literal negative answer or the finite-p even smooth-density theorem. Optimal ratio asymptotics, uniformity in p, an even-density infinity theorem, support/derivative/bandwidth restrictions, inverse Hölder/modulus questions, and historical originality remain outside this verified result. This review gives no opinion on their truth or on current literature status.

## Public artifact policy

Only the exact relative files listed in `PUBLIC_MANIFEST.json` are public review artifacts. The manifest is a positive whitelist, with file sizes and SHA-256 hashes. `private_sources/` is excluded wholesale; any foreign source copies or temporary materials belong there. No foreign PDF or source text was downloaded into the public artifact set, and no private or invalid fixture was selected. The audited source was read in place and was not changed. No Git, index, branch, remote, release, cloud, or outreach action was performed by this review.
