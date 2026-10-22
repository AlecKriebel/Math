# Synchronous reflected-Brownian couplings: partial identities and exact obstructions

Problem 9500005 / AMR-094-0005. Primary-source check: 8 October 2026.

## Result and scope

Neither part of Burdzy's Problem 5 is resolved here. The work proves several elementary identities and sufficient criteria, and identifies the missing probabilistic steps in five approaches. There is no claimed counterexample, convergence theorem for the disk exterior, or novelty claim. In particular, controlled deterministic trajectories and an auxiliary jump process below are not evidence of a positive-probability Brownian nonconvergence event.

### Normalization

Let D be a connected open planar set with smooth boundary, and write n for its inward unit normal. Fix deterministic x,y in the closure of D and a standard two-dimensional Brownian motion B, with covariance t times the identity. The normally reflected processes satisfy

    X_t = x + B_t + ∫_0^t n(X_s) dL^X_s,
    Y_t = y + B_t + ∫_0^t n(Y_s) dL^Y_s.

Each regulator starts at zero, is continuous and nondecreasing, and increases only on the boundary. This equation fixes the regulator normalization; no extra factor of 1/2 is inserted. Processes take values in the closure. Define ρ_t=|X_t−Y_t| and

    q_D(x,y) = P_{x,y}(limsup_{t→∞} ρ_t > 0).

The bounded question asks for a bounded smooth D and a nontrivial starting pair with q_D(x,y)>0. The exterior question uses D={z:|z−c|>R}, R>0. The author states the starting points in the closure, without an explicit distinct-pair quantifier inside each subquestion. Equal starting points give X=Y by pathwise uniqueness and q=0. We therefore keep x≠y explicit; a positive answer must specify whether it covers some or every distinct pair. This report proves neither version for the exterior. The diagonal observation is not offered as a resolution of the intended question.

Positive limsup is the complement of convergence to zero, since ρ is nonnegative. It is not the same as a positive lower bound for every time, positive liminf, or failure to meet in finite time. All probability statements concern the shared driving Brownian motion. The intended smooth class is not replaced by convex domains or by polygonal domains.

Translation, rotation, and Brownian scaling reduce a disk of radius R and center c to the unit disk, while transforming the starting pair. Indeed, (X_{R²t}−c)/R has driving motion B_{R²t}/R and regulator L^X_{R²t}/R. Thus the event is scale invariant. This does not identify different starting pairs.

## 1. Literature and inspection limits

The current [author problem page](https://sites.math.washington.edu/~burdzy/open_mathjax.php), Problem 5, retains both questions and attributes a two-hole necessary condition for a bounded example to BCJ. This is a current statement by the author, not an independently audited theorem for every smooth boundary.

Burdzy–Chen–Jones, [arXiv:math/0501486v1](https://arxiv.org/abs/math/0501486), Theorems 1.1–1.2, prove synchronization for at most one hole and exponential decay when their geometric exponent Λ(D)>0. Their assumptions include boundedness, C4 boundary, uniformly finitely many points with any prescribed normal, and finitely many curvature zeros with nonzero cubic term. Problem 2.1 remains open; negative Λ implying positive limsup is Conjecture 2.2. Proposition 2.3 gives Λ=0 for the disk exterior; Problem 2.6 asks about its convergence. The bounded positive-exponent theorem therefore cannot decide that exterior case. Lemma 3.1 supplies arbitrarily close approach under its setting, which alone does not give convergence.

The publication is Illinois Journal of Mathematics 50 (2006), 189–268, [DOI](https://doi.org/10.1215/ijm/1258059475). The publisher endpoint returned HTML rather than PDF. Only the arXiv text's stated assumptions were checked; removal of its technical assumptions in another version has not been verified.

Burdzy–Chen, [Coalescence of synchronous couplings](https://digital.lib.washington.edu/bitstreams/730b9465-55ca-42cf-9ebd-9acf1aad56cf/download), Theorem 1.1, proves convergence for bounded polygonal and lip domains. An introductory sentence announces a future positive/negative answer for smooth domains. The later BCJ paper instead leaves the counterexample problem open, so that earlier announcement is not a verified solution. Polygonal approximation also does not justify exchanging a domain limit with t→∞.

The bounded search included both authors' publication listings and exact-title, disk-exterior, nonconvergence, and recent-year queries. No complete resolving theorem was located. This is not certification that no such theorem exists. The retrieved BCJ PDF was inspected at its normalization, main statements, Section 2, Lemma 3.1 statement and relevant distance-bound passage; its full long proof was not independently audited. BC was inspected at its introduction and main theorem. Full source bodies are excluded from this packet; SOURCE_METADATA.json identifies retrieved bytes and access limits.

## 2. Approach 1: direct boundary geometry

### Proposition 1. Exact distance identity and a one-sided bound

For any continuous solutions of the same normal Skorokhod equation, including deterministic continuous driving paths, Z=X−Y has locally finite variation and

    d|Z|² = 2 Z·n(X) dL^X − 2 Z·n(Y) dL^Y.                 (2.1)

If D satisfies a uniform exterior-ball condition of radius r>0, then

    |Z_t|² ≤ |Z_0|² exp((L^X_t+L^Y_t)/r).                (2.2)

The conclusion also holds between any two fixed times with corresponding regulator increments.

Proof. The common driving path cancels, giving dZ=n(X)dL^X−n(Y)dL^Y. The finite-variation chain rule proves (2.1); there is no Brownian quadratic-variation term. For a boundary point u, the open ball with center u−r n(u) and radius r is disjoint from D. For v in the closure of D,

    |v−u+r n(u)|² ≥ r²,
    (u−v)·n(u) ≤ |u−v|²/(2r).

Apply this inequality at each reflecting particle in (2.1) and use the Stieltjes Gronwall inequality for the continuous increasing measure d(L^X+L^Y)/r. This proves (2.2), including the zero-distance case. ∎

This is an upper-growth bound, not a lower bound preventing synchronization. In a convex domain both terms in (2.1) are nonpositive, but that special geometry does not cover the target.

### Explicit smooth two-hole controls

Consider

    D = B(0,10) \ (closed B(0,1) ∪ closed B((4,4),1/2)).

Its three disjoint circular boundary components give a bounded connected smooth domain with two holes. On 0≤t≤1, let the common deterministic driver be b_t=(−t,0).

Starting at x=(1,0), y=(−2,0), the exact Skorokhod solutions are

    X_t=(1,0),   L^X_t=t,
    Y_t=(−2−t,0),   L^Y_t=0.

Their separation is 3+t, which increases. Every displayed point remains in the closure of D, X's normal is (1,0), and Y touches no boundary.

With x=(1,0), y=(3/2,0), on 0≤t≤1/2 the solutions are X_t=(1,0), Y_t=(3/2−t,0), L^X_t=t, L^Y_t=0. The separation is 1/2−t. After t=1/2 they may be continued together at (1,0), with both regulators increasing at rate one.

Thus the same admissible smooth geometry allows deterministic expansion and contraction. Neither displayed driver is a Brownian sample-path event of positive probability. Even finite-time support arguments would need an additional, uniform infinite-horizon mechanism before answering Problem 5. No such mechanism is established. Approach 1 is incomplete.

## 3. Approach 2: a radial correction to logarithmic separation

This approach works directly with the disk exterior, D={z:|z|>R}. Write r_X=|X| and r_Y=|Y|. For real a define, off the diagonal,

    F_a(X,Y)=log|X−Y|−a(log|X|+log|Y|).

### Proposition 2. Exact stopped Itô decomposition

Before collision, and with the usual compact stopping away from the diagonal,

    dF_a = −a (X/r_X² + Y/r_Y²)·dB
           + [(1−2a)ρ²+R²−r_Y²]/(2Rρ²) dL^X
           + [(1−2a)ρ²+R²−r_X²]/(2Rρ²) dL^Y.           (3.1)

All individual boundary coefficients are nonpositive for every admissible pair if and only if a≥1/2. Consequently F_a is a local supermartingale off the diagonal for a≥1/2. The assertion is local; no integrability at collision or infinity is presumed.

Proof. On {r_X=R}, n(X)=X/R and

    (X−Y)·n(X) = (ρ²+R²−r_Y²)/(2R).

The analogous Y contribution has r_X in place of r_Y. Since ρ has finite variation, dividing the squared-distance differential by 2ρ² gives d logρ. In dimension two, log|z| is harmonic away from zero. Itô's formula therefore gives

    d log r_X = (X/r_X²)·dB + (1/R)dL^X,

and the same equation for Y. Subtraction gives (3.1). If a≥1/2, its boundary numerators are nonpositive because r_X,r_Y≥R. If a<1/2 and x,y are distinct boundary points, either coefficient equals (1−2a)/(2R)>0. This proves the sharp algebraic threshold for nonpositive boundary derivatives. Standard localization makes the martingale integral and finite-variation terms integrable, proving the local-supermartingale statement. ∎

### Why this does not prove convergence

F_{1/2} is not a coercive measure of Euclidean separation on an unbounded domain. At x=(r,0), y=(r+1,0), the separation is exactly one while

    F_{1/2}(x,y)=−(1/2)log(r(r+1)) → −∞.

Moreover, a local supermartingale unbounded below need not converge to a finite limit; bounded-stop inequalities alone do not supply the required global convergence statement. One must control excursions to large radii, repeated visits near the boundary, and the singular coefficients as ρ→0. These controls have not been proved here. The stopped identity and its sharp sign threshold are valid partial results, not an answer to part (ii). Approach 2 is incomplete.

## 4. Approach 3: conformal inversion

One might try to transfer the exterior problem to a convex disk. The obstruction is that a conformal map preserves individual planar Brownian motions only with a position-dependent clock and rotation; it need not preserve a synchronous pair.

### Proposition 3. The inverted pair is generally not synchronous

Use complex notation and φ(z)=R²/z. Let U=φ(X), V=φ(Y). These lie in the punctured closed disk of radius R and satisfy

    dU=−R²/X² dB − U/R dL^X,
    dV=−R²/Y² dB − V/R dL^Y.                         (4.1)

The reflection coefficients are evaluated only when their regulator increases. Each Cartesian component of the martingale part of U−V has quadratic variation

    ∫_0^t R⁴ |X_s−Y_s|² |X_s+Y_s|²
                 / (|X_s|⁴ |Y_s|⁴) ds.              (4.2)

Its cross bracket is zero. In particular, the difference generally has a nonzero martingale component, unlike the finite-variation difference of a synchronous pair.

Proof. Both real coordinates of a holomorphic map are harmonic, so Itô's formula has no interior drift. On |X|=R,

    φ'(X)n(X)= (−R²/X²)(X/R)=−U/R,

the unit inward normal for the image disk. The complex multiplier for the difference's martingale part is R²(1/Y²−1/X²). Complex multiplication by a number h gives the covariance matrix |h|² times the identity for standard planar Brownian motion. Factoring X²−Y² proves (4.2). ∎

At x=2R and y=3R on the real axis, the integrand is strictly positive. Its exceptional zeros at x=y or x=−y do not make the construction synchronous in general. Individual image clocks are ∫R⁴/|X_s|⁴ ds and ∫R⁴/|Y_s|⁴ ds; they need not agree. Independently changing these clocks changes simultaneous time comparisons. Convex-disk synchronous contraction therefore cannot simply be imported. Approach 3 yields this exact obstruction, but no replacement comparison theorem and no answer to part (ii).

## 5. Approach 4: an off-diagonal stationary measure

The following is a precise sufficient criterion for a bounded-domain counterexample. It is stated for a Feller pair semigroup on the compact space K=closure(D)×closure(D); this is the usual smooth bounded reflected-flow setting. The abstract proposition includes that hypothesis explicitly.

### Proposition 4. A stationary occupation criterion

Let P_t be a Feller Markov semigroup on a compact metric space K, and let g:K→[0,M] be continuous. Suppose the pair state has g(x,y)=|x−y|².

(a) If an invariant probability μ has ∫g dμ>0, then some deterministic starting pair satisfies

    P(limsup_{t→∞} |X_t−Y_t|>0)>0.

(b) If, for some starting pair z and some sequence T_k→∞,

    liminf_k (1/T_k) ∫_0^{T_k} E_z[g(Z_s)] ds > 0,      (5.1)

then such an invariant probability exists.

Proof of (a). Start Z with distribution μ. At all integer n, E_μ g(Z_n)=c:=∫g dμ>0. Applying Fatou to the bounded nonnegative variables M−g(Z_n) gives

    E_μ[limsup_n g(Z_n)] ≥ c>0.

Thus the event of positive limsup has positive probability under μ. Disintegrating over the starting state yields a deterministic state with positive probability. Positive limsup along integers implies positive limsup over all times. ∎

Proof of (b). Let μ_T=(1/T)∫_0^T Law_z(Z_s) ds. Compactness gives a weakly convergent subsequence. For continuous f and fixed u≥0, the semigroup property gives

    |∫P_u f dμ_T − ∫f dμ_T| ≤ 2u||f||∞/T.

Feller continuity permits passage to the weak limit, proving invariance. Continuity of g and (5.1) give ∫g dμ>0. ∎

Compactness alone does not ensure that ∫g dμ>0: a diagonal stationary distribution always exists when a single reflected Brownian motion has its uniform stationary distribution. The missing step is a quantitative off-diagonal occupation bound or a construction of an off-diagonal invariant measure.

### A failed stationary candidate can be rejected exactly

The product of two uniform marginals need not be invariant for synchronous dynamics. On the unit disk, choose

    u(x_1,x_2)=x_1(3−x_1²−x_2²),
    f(x,y)=u(x)u(y).

The normal derivative of u vanishes on the circle, so f satisfies the two normal boundary conditions. The interior synchronous generator is

    A=(1/2)Δ_x+(1/2)Δ_y+Σ_i ∂_{x_i}∂_{y_i}.

For U uniform on the unit disk, symmetry and its elementary second moments yield

    E u(U)=0,  E∇u(U)=(2,0).

Consequently, under the product uniform measure,

    ∫Af = |E∇u(U)|² = 4 ≠ 0.

A stationary measure must integrate Af to zero for this smooth Neumann test function. Hence the product candidate is not stationary. This calculation is a counterexample to a candidate-measure shortcut, not to the original convergence problem.

Finally, positive limsup does not by itself furnish (5.1). For example, a continuous scalar function having triangular peaks of height one and half-width 2^(−n−3) at times n has limsup one but finite total integral. Its time-averaged square tends to zero. This scalar example only shows that the proposed implication needs extra process-specific reasoning; it is not asserted to be a reflected-Brownian trajectory. Approach 4 is incomplete for the bounded target and does not cover the noncompact exterior.

## 6. Approach 5: critical excursion balance

This last approach examines the zero first-order balance for a circular obstacle. The calculation below gives exact integrals and an auxiliary stochastic model. It does not identify that model with the finite-distance reflected coupling.

Put

    ν(dθ)=dθ/[4π sin²(θ/2)],  0<θ<2π,
    h(θ)=log|cosθ|.

The singular points with cosθ=0 have zero ν-measure. For p>−1, define the convergent improper integral

    J(p)=∫ (|cosθ|^p−1) ν(dθ).

### Proposition 5. Exact first two log-jump integrals

For p>−1,

    J(p)=−(2p/π) ∫_0^{π/2} cos^p θ dθ.                 (6.1)

It follows that

    ∫h dν=−1,       ∫h² dν=2 log 2.                    (6.2)

Proof. Reflect the integral first around π and then pair θ with π−θ. The identity

    csc²(θ/2)+sec²(θ/2)=4 csc²θ

gives

    J(p)=(2/π) ∫_0^{π/2} (cos^p θ−1)csc²θ dθ.

Integrate by parts with antiderivative −cotθ. The lower boundary term vanishes because cos^p θ−1=O(θ²). The upper term vanishes for p>−1 because cotθ=O(π/2−θ). The result is (6.1). Near p=0, differentiation under the integral is justified by integrability of fixed powers of |log cosθ| at π/2 and by their quadratic vanishing at θ=0. The standard integral C=∫_0^{π/2}log cosθ dθ equals −(π/2)log2: symmetry gives the same integral for log sinθ; adding and substituting 2θ gives 2C=C−(π/2)log2. Differentiating (6.1) now proves (6.2). ∎

This independently checks the cancellation of circular curvature and the circular boundary kernel: integrating the loss 1 over a boundary of length 2π offsets total curvature −2π. It agrees with BCJ's stated Λ=0; it is not a new sign theorem for other obstacles or a justification for applying their bounded-domain decay theorem to an infinite-area domain.

### An explicitly auxiliary centered jump process

Let N(ds,dθ) be a Poisson random measure with intensity ds ν(dθ), and define

    S_ℓ = ∫_(0,ℓ] ∫ (−h(θ)) N(ds,dθ),
    M_ℓ = ℓ−S_ℓ.

Although ν has infinite total mass, (6.2) gives finite ∫|h|dν and finite ∫h²dν. Thus nonnegative truncations define S_ℓ with finite expectation, hence finite value almost surely for every finite ℓ; the centered truncations converge in L². Standard Poisson-integral expectation and variance identities, first for truncations and then by these limits, give

    E M_ℓ=0,       Var(M_ℓ)=2ℓ log2.                    (6.3)

These are exact properties of the newly defined auxiliary process only. Its clock has not been identified with the coupling's clock, and its jump increments have not been proved to describe finite separation. Tangent projections or a linearization at a fixed time would also require error control uniform over unbounded time and through arbitrarily close approaches. That is the missing nonlinear stochastic step.

Even a proved rate statement logρ_t/t→0 would not settle convergence: ρ_t=exp(−√t) and ρ_t=1 have the same limiting rate but different convergence to zero. No inference from criticality, from (6.3), or from finite-time deterministic expansion to positive limsup is made. A negative geometric exponent for another smooth domain would additionally require the stochastic implication identified as conjectural in the inspected primary source. Approach 5 is incomplete.

## 7. Verification and remaining questions

The five distinct approaches are boundary geometry, radial stopped Lyapunov correction, conformal inversion, stationary off-diagonal occupation, and critical excursion balance. None supplies a complete proof or counterexample for either original part. Only the explicitly proved partials above are retained.

The executable checker uses only the Python standard library and exact rational arithmetic. It checks boundary coefficient identities and signs on a declared finite family, sharp-threshold witnesses, rational inversion factorization, the controlled-path equations and membership conditions, disk-moment algebra rejecting the product invariant candidate, and a finite exact family of even-power integral identities. These checks can catch algebraic or normalization errors; they do not prove stochastic convergence, an infinite-horizon probability, a literature status, or a continuous-parameter theorem. The analytic proofs above, rather than the sampled checks, establish the propositions.

For a definitive bounded positive answer, an explicit bounded smooth D and nontrivial initial pair must be accompanied by a proof that q_D(x,y)>0. A definitive negative answer needs convergence for every admissible D and pair, with the exact smoothness scope stated. For the disk exterior, a proof must keep the shared Brownian driver and original time, handle unbounded excursions and the critical balance, and state its initial-pair quantifier. None of these conclusions is claimed here.

## References

- K. Burdzy, My favorite open problems, Problem 5, [current author page](https://sites.math.washington.edu/~burdzy/open_mathjax.php).
- K. Burdzy, Z.-Q. Chen, P. Jones, Synchronous couplings of reflected Brownian motions in smooth domains, Illinois J. Math. 50 (2006), 189–268, [DOI](https://doi.org/10.1215/ijm/1258059475); inspected [arXiv v1](https://arxiv.org/abs/math/0501486).
- K. Burdzy, Z.-Q. Chen, Coalescence of synchronous couplings, Probab. Theory Related Fields 123 (2002), 553–578; inspected [author manuscript](https://digital.lib.washington.edu/bitstreams/730b9465-55ca-42cf-9ebd-9acf1aad56cf/download).
