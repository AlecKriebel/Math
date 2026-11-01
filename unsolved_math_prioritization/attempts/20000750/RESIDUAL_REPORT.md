# Alternative GPY weights: five residual approaches and an architecture audit

Row 1898; problem ID 20000750. Authored analysis, 21 October 2026. Status: partial progress, no new prime-gap bound or optimality theorem. No publication or queue edit.

## Scope and prior art

The original AIM Problem 15 asks about changing single-divisor coefficients, particularly a prime-local product times a smooth cutoff, traditional sieve weights, and upper/lower mixtures. It is not the problem of re-solving the radial Maynard variational problem. The recovered research is mathematically useful but does not evaluate the prime-local family's arithmetic moments.

Farkas–Pintz–Révész, https://arxiv.org/abs/1306.2133, already solve the one-variable optimization. Polymath, https://arxiv.org/abs/1407.4897, printed page 46 gives the radial maximum 4k(k−1)/j_(k−2,1)^2 < 4 and cites that work. Maynard, https://arxiv.org/abs/1311.4600, printed pages 17–18 and equation (7.2), supplies the larger variational space and operator. These are prior results, not claimed discoveries. The web search on 21 October reconfirmed Farkas–Pintz–Révész; it did not establish a classification of the precise product-local family. Negative search evidence is not nonexistence evidence.

Throughout finite calculations, R>1, D consists of squarefree integers d<R, x_p=log(p)/log(R), y_d=log(R/d), and
u_d=mu(d) Q(y_d) product_(p|d) f(x_p).
Explicit truncation to d<R avoids an ambiguity in the informal formula: Q(log^+(R/d)) by itself does NOT impose support unless Q(0)=0. If needed use Q(0)=0 and extend the cutoff by zero for support and continuity. Smoothness of the zero extension would additionally require flatness at 0; finitely many prescribed positive-node values can instead be realized by disjoint smooth bumps supported away from 0. Fix a finite interval X of N consecutive integers and q(n)>=0. Write A=Phi^T Phi, B=Phi^T diag(q) Phi, Phi_(n,d)=1_(d|product_i(n+h_i)). Set a=u^T A u>0 and rho=u^T B u/a. All results below are exact finite statements; asymptotic uniformity is a separate requirement.

## Approach 1. Remove a prime-local gauge and expose the finite-level overfitting obstruction

For every real c, replacing f(x) by exp(cx)f(x) multiplies the coefficient by exp(c log(d)/log(R)). This is absorbed EXACTLY by replacing Q(y) by exp(−c+cy/log(R))Q(y). Thus this one-parameter variation changes no coefficient at all. Conversely changing only f by exp(cx) is simply a cutoff change, not an independent prime-local improvement. In infinitesimal form h(x)=cx yields sum_(p|d) h(x_p)=c log(d)/log(R). Searches that count this as a new direction duplicate the Q direction.

A more fundamental finite-level obstruction: for any prescribed real coefficients c_d on D there is a polynomial Q with Q(log(R/d))=mu(d)c_d, and with Q(0)=0 if requested. The interpolation nodes are distinct and positive. With f=1 this gives exactly lambda_d=c_d on D. Consequently, absent uniform degree/derivative bounds or an R-independent normalized profile, the smooth-cutoff family already represents EVERY finite squarefree coefficient vector. Finite numerical improvement therefore cannot demonstrate a useful uniform product-local asymptotic improvement. This does not impose an extra requirement on the original question; it identifies why a finite computation alone does not answer its quantitative asymptotic purpose. Nonsquarefree entries remain zero and are excluded from this statement.

## Approach 2. Test the actual curved product family, not an unauthorized linear enlargement

Put f_epsilon(x)=f(x)exp(epsilon h(x)) for smooth real h, keeping Q fixed. Then lambda_d(epsilon)=u_d exp(epsilon H_d), H_d=sum_(p|d) h(x_p). Write v_d=u_d H_d, z_d=u_d H_d^2, and K=B−rho A. Direct differentiation gives

R'(0)=2 u^T K v/a,
R''(0)=2(v^T K v+u^T K z)/a − 8(u^T A v)(u^T K v)/a^2.

Proof: differentiate N(epsilon)−rho D(epsilon), using its value zero at the origin, and the quotient by D(epsilon). The derivatives are 2uKv and 2vKv+2uKz, while D'(0)=2uAv.

If uKv !=0, one sign of epsilon gives a strict improvement WITHIN the product family. If uKv=0 and vKv+uKz>0, both sufficiently small nonzero signs give an improvement. At an interior local maximum the first quantity must vanish for every allowed h and the second must be nonpositive. These are rigorous falsifiable necessary conditions; satisfying them is not sufficient for global optimality.

The recovered exact two-plane theorem is correct for span{u,v}; but a sum of two product-local coefficients is generally NOT a single product-local coefficient. Even at stationarity, the straight-plane criterion cannot be substituted for the curved criterion: uKz is absent from the former.

Concrete exact algebraic counterexample to that substitution: A=I_3, u=(1,1,1), H=(0,1,2), v=(0,1,2), z=(0,1,4), r=(1,−2,1), w=(−1,0,1), and
K=(r u^T+u r^T)/3 − ww^T/4, B=5I_3+K.
Here uKu=0, Ku=r, uKv=0, vKv=−1, uKz=2. The two-plane {u,v} has no gain above rho=5, yet R''(0)=2/3>0 along u_d exp(epsilon H_d). B is positive definite: ||(r u^T+u r^T)/3||=sqrt(2) and ||ww^T/4||=1/2, so lambda_min(B)>=5−sqrt(2)−1/2>0. This is an abstract Gram-geometry diagnostic, NOT a claim that these matrices arise from a GPY arithmetic sample. Smooth h can interpolate specified values at finitely many prime nodes, but that alone does not realize prescribed A,B arithmetically.

## Approach 3. Evaluate denominator moments with explicit CRT error; isolate the prime numerator deficit

Let nu(m) be the number of residues a modulo m with product_i(a+h_i)=0 mod m. For squarefree m, CRT gives nu(m)=product_(p|m) nu(p). Each residue occurs N/m with absolute error at most 1 in X, hence
|A_de−N nu([d,e])/[d,e]| <= nu([d,e]).
For any real vectors c,t this yields the rigorous bilinear bound
|c^T(A−A0)t| <= sum_(d,e) |c_d t_e| nu([d,e]),
A0_de=N nu([d,e])/[d,e].
No equidistribution assumption is used. The same estimate is usually too crude in the interesting growing-R regime, which precisely marks the missing uniform analysis rather than hiding it.

For the prime-indicator score q(n)=sum_i 1_prime(n+h_i), the numerator can also be expressed exactly:
B_de=sum_i sum_(a mod m:P(a)=0 mod m) #{p prime: p−h_i in X, p ≡ a+h_i mod m}, m=[d,e].
Non-coprime residue classes must not be replaced by the usual 1/phi(m) main term: their prime counts are exceptional primes dividing m. Define discrepancies for the coprime classes and retain exceptional classes exactly. A uniform weighted bound on these discrepancies is the arithmetic ingredient absent from a mere six-moment certificate.

If rigorous entrywise intervals |A−A0|<=EA and |B−B0|<=EB are obtained, a candidate c has a certified ratio >T whenever
c^T(B0−T A0)c > sum_(d,e)|c_d c_e|(EB_de+|T|EA_de),
and c^T A c>0 is certified separately. This is an exact finite sufficient certificate, not an asymptotic estimate or a claim that an available distribution theorem achieves its margin. It prevents an uncertified floating-point eigenvalue or neglected error term from being reported as arithmetic improvement.

## Approach 4. Traditional weights: distinguish square-mixtures from mixtures of squares

For any fixed collection of divisor sums L_j, every signed linear combination inside a square remains nonnegative. Optimizing (sum c_j L_j)^2 is the known generalized-eigenvalue problem. In contrast, for nonnegative coefficients alpha_j, the ratio of the mixture W=sum alpha_j L_j^2 is a denominator-weighted average of the individual ratios, and cannot exceed their maximum (omit zero-denominator terms). Thus simply averaging nonnegative traditional weights supplies no strict advantage over the best component. Cross terms inside one square are the only potential source of improvement within this elementary comparison.

For a candidate v and baseline u, Gram-orthogonalize v_perp=v−(uAv/a)u. If b=v_perp A v_perp=0, it changes no divisor sum on X. Otherwise the larger eigenvalue of [[rho,s],[s,t]], s=uBv_perp/sqrt(ab), t=v_perp Bv_perp/b, exceeds rho exactly when s!=0 or t>rho. This is standard, recovered prior mathematics. It supplies a rejection certificate for a SPECIFIED traditional component, not an impossibility theorem over all traditional sieve constructions, and its maximizing combination need not stay inside a more restricted original parametric family.

## Approach 5. Upper/lower mixtures: sharp uniform contamination budget

Write W=W_+−W_- with W_+,W_->=0. For any surplus g,
sum gW <= sum g_+ W_+ + sum (−g)_+ W_-.
Thus sum gW > C_-, C_-=sum(−g)_+W_-, ensures a point with g>0 and W_+>0. No estimate of C_- has been furnished by the residual construction.

For a prime-count target of at least m primes among k shifts, take g=q−(m−1), 1<=m<=k, with 0<=q<=k. Then C_- <= (m−1) sum W_-. Hence sum gW > (m−1)sum W_- is an elementary sufficient certificate. The coefficient m−1 is uniformly sharp given only the range of q: take one point with q=0 and W_-=1,W_+=0. Then sum gW=m−1 but no target point exists. The strict inequality is essential. This sharpness is a worst-case algebraic obstruction, not a proof that arithmetic configurations realize the worst case or that Chen-type methods cannot improve it. A viable mixture must exploit extra distribution/structure to lower the actual contamination.

## Radial escape audit and remaining target

For F(t)=G(S), G continuous, H(x)=integral_x^1 G, the full operator is LF=sum_i H(S−t_i). The equivalence LF radial iff G constant is valid only after explaining why an almost-everywhere radial identity extends to the continuous representatives on fibers. A complete repair and independent checks are supplied in INDEPENDENT_REVIEW.md. There is no nonzero continuous radial eigenfunction for k>=2. The Rayleigh residual is nonzero and gives a strict two-plane gain, but it lives in the larger Maynard space, not automatically in the original prime-local single-divisor family.

The five approaches above produce exact diagnostics, obstructions, and error-controlled finite certificates. None supplies uniform arithmetic moments for a genuinely new f,Q choice, proves an improved finite-k asymptotic constant from such a choice, globally optimizes traditional sieves, or controls a Chen-style mixture's arithmetic negative contribution. Classification must remain partial. Novelty of these elementary identities is not asserted.
