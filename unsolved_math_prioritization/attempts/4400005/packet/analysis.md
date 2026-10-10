# Ledrappier's time-one invariant-measure question

## Disposition

**Already solved in the literature.** The answer is affirmative for every closed Riemannian manifold of constant negative sectional curvature, of dimension at least two. In fact the same conclusion holds in variable strictly negative curvature. A measure can be chosen nonatomic, ergodic for the time-one map, and of entropy zero. It can be chosen to fail invariance already at time one-half.

This is a literature-resolution audit and a short deduction from existing theorems, not a new-result or priority claim. The directly matching corollary of Quas and Soo (2012) is stated for surfaces. The all-dimensional conclusion below uses the later theorem of Burguet (2020) together with the dimension-independent specification fact documented by Thompson and Tian. No surface theorem is silently promoted to arbitrary dimension.

## Exact target and conventions

Let N be a nonempty compact smooth Riemannian manifold without boundary with constant sectional curvature -c^2, c>0, and dimension d>=2. Write X=T^1N for its unit tangent bundle and g_t:X->X for unit-speed geodesic motion. The target is a Borel probability mu on X satisfying (g_1)_*mu=mu and (g_t)_*mu != mu for at least one real t. All time parameters refer to the given metric; no rescaling of the metric or replacement of time one is performed.

The source uses the customary abbreviation 'geodesic flow on N'; the measure actually lives on T^1N. Its full real flow convention excludes an ordinary manifold with boundary and exiting geodesics. Dimension one is not an intended negative-sectional-curvature case. If N is disconnected, apply the connected case to one component and extend the measure by zero on the others. The target imposes no absolute continuity, entropy lower bound, full support, or rational closed-geodesic hypothesis.

The primary locator is the November 22, 2010 Pingree problem list, printed page 3, Francois Ledrappier item 1. The catalogue URL was attempted first and returned HTTP 403; the pinned record was then matched against the primary PDF by text and visual inspection. The exact source transcription remains outside this packet.

## Imported facts and their precise scope

1. **Specification of the sampled geodesic flow.** Thompson, arXiv:0807.2123v1, Definition 1.5 (page 4) and section 4.3 (page 20), expressly applies fixed-gap discrete specification to time-t maps of geodesic flows on compact connected negatively curved Riemannian manifolds. This includes every dimension and t=1. Tian, *Advances in Mathematics* 288 (2016), section 7.3, printed page 515, repeats the general mixing-Anosov time-map statement and cites Thompson. The underlying geometric inputs are Anosov hyperbolicity, mixing, and Bowen's flow specification theorem. These classical inputs are used as published results, not reproved here.
2. **Universality.** Burguet, arXiv:1901.00666v1, Theorem 1.2 (page 3), proved for a compact metric space and homeomorphism of finite topological entropy, almost-Borel embeds every aperiodic Borel system of strictly lower Borel entropy when the target has almost weak specification. The article was published in *Ergodic Theory and Dynamical Systems* 40 (2020), 2098-2115, DOI 10.1017/etds.2019.7. We use Theorem 1.2, rather than the nearby corollary whose shortened terminology can be confusing.
3. **Direct surface resolution.** Quas and Soo, *Journal of Modern Dynamics* 6 (2012), Corollary 4 (page 430), gives a time-one ergodic invariant probability not invariant under the geodesic flow for every compact negatively curved surface. Their Theorem 1 is surface universality. The published text and its square-root argument were inspected. This corroborates the result for surfaces; it is not the dimension-independent premise in step 1.

Here fixed-gap discrete specification means: for every epsilon>0 there is L(epsilon) such that any finite collection of integer-time orbit intervals with all successive gaps at least L can be epsilon-shadowed at those prescribed times by one orbit. A constant gap function is sublinear, hence gives Burguet's almost weak specification. If one definition uses local-time orbit origins and the other absolute-time origins, replace each prescribed point by its image or preimage at the starting time. Since g_1 is invertible, these formulations agree. Intervals beginning at negative times are translated by a common integer.

This is not the weaker flow gluing property allowing freely chosen transition times merely bounded above. That property alone does not justify Burguet's hypothesis. Nor is the shadowing point required to be periodic for g_1; imposing that would be wrong for metrics with no rational-length closed geodesics.

## Complete deduction from the imported theorems

### 1. The target has finite positive topological entropy

Set F=g_1 on a connected component X. It is a smooth diffeomorphism of a compact manifold, hence Lipschitz for a suitable Riemannian distance, with a finite Lipschitz constant K. Covering-number bounds in dimension D=dim X imply finite topological entropy: an ordinary ball of radius epsilon K^{-(n-1)} controls its first n iterates, so spanning numbers grow at most exponentially in n.

Positivity follows directly from the specification property, without a curvature-normalization formula. Choose two different points x_0,x_1 with distance delta>0 and an error epsilon<delta/3. Fix an integer q greater than the specification gap. For every binary word of length m, prescribe the corresponding x_0 or x_1 at the times 0,q,...,(m-1)q. Specification supplies a tracing point. Tracing points from two different words are separated at one of these times by at least delta-2epsilon>epsilon. Therefore there are at least 2^m distinct (mq,epsilon)-separated points. This gives h_top(F)>=log(2)/q>0. If nondegenerate intervals are required, prescribe intervals of length one and increase q by one; the same argument works.

### 2. An explicit entropy-zero aperiodic source

Let Z_2 be the inverse limit of the cyclic groups Z/(2^k Z), and let S(z)=z+1. Equip Z_2 with its Borel sigma-algebra and normalized Haar measure m.

- S is an invertible homeomorphism preserving m. A singleton has measure at most 2^{-k} for every k, so m is nonatomic.
- The reduction modulo 2^k is a single cyclic permutation. Any S-invariant probability must assign 2^{-k} to each residue cylinder. The cylinders generate the Borel sigma-algebra, so m is the unique invariant probability. It is consequently ergodic.
- If S^n z=z then every 2^k divides the integer n, so n=0. Thus S is aperiodic on every point, not just almost everywhere.
- In the usual 2-adic metric, S is an isometry. At any fixed accuracy the residue classes modulo 2^k give a finite spanning family valid for all orbit lengths. Hence h_top(S)=0 and therefore h_m(S)=0. Its Borel entropy, the supremum over invariant probabilities, is zero as well.

### 3. A no-square-root lemma with an explicit obstruction

Define f(z)=(-1)^{z mod 2}. It is a nonzero real-valued function satisfying f composed with S = -f and f^2=1.

Suppose R were an invertible m-preserving measurable transformation with R^2=S modulo null sets. Then R commutes with S modulo null sets, since both RS and SR equal R^3. Consequently f composed with R is also a real -1 eigenfunction of S.

Every such real eigenfunction h is a constant multiple of f: h/f is S-invariant, hence almost everywhere constant by ergodicity. Thus f composed with R=a f for a real constant a. As R preserves m, their L^2 norms are equal, so a=1 or a=-1. Applying R twice now gives f composed with R^2=f, contradicting f composed with S=-f. No measure-preserving square root exists.

One must retain the word real and the fact that R is a transformation: multiplication by i is a square root of -1 as a complex linear operator, but it cannot act on this real eigenfunction as a Koopman operator. One must also retain ergodicity, which makes this eigenline one-dimensional.

### 4. Embed and transport the obstruction

Since h_bor(S)=0<h_top(F), Burguet's Theorem 1.2 provides an invariant full Borel subset Z_0 of Z_2 and an injective Borel map Psi:Z_0->X with Psi composed with S = F composed with Psi. Replace Z_0 by its intersection over all integer S-iterates if needed. The image A is Borel by the Borel injective-image theorem for standard Borel spaces, and Psi has a Borel inverse on A.

Define mu=Psi_*m. Equivariance proves F_*mu=mu. The measurable conjugacy transfers ergodicity, nonatomicity, and zero entropy from (Z_2,m,S) to (X,mu,F).

If (g_(1/2))_*mu=mu, then g_(1/2) defines an invertible measure-preserving automorphism of (X,mu) whose square is F. On A intersected with all integer g_(1/2)-translates of A, a conull invariant set, transport that automorphism using Psi^{-1}. This gives an m-preserving square root of S, contradicting step 3. Thus (g_(1/2))_*mu != mu. In particular mu is not invariant under the full flow. This completes the target deduction.

## Other routes and failure controls

### Periodic-orbit route

A closed geodesic of rational length ell=p/q in lowest terms gives an immediate finite g_1-orbit of size p. Its uniform atomic measure is g_1-invariant and cannot be invariant under the full nonstationary circle flow. For example, a sufficiently small nonzero shift moves its finite support. The route does not resolve an arbitrary fixed metric: its length spectrum need not contain a rational number. Changing scale to make one orbit have length one changes the specified time-one problem. This route is valid only under the extra rational-length premise.

### Averaging and rigidity route

For every g_1-invariant mu, the averaged probability bar_mu=integral_0^1 (g_t)_*mu dt is flow-invariant; translation of the integration interval and its period-one integrand prove this. The equality bar_mu=mu is an additional condition, not a consequence of that formula. On a circle with period one, averaging a point mass gives normalized length measure and loses the original point mass. Rigidity of smooth or maximal-entropy measures cannot be applied to the zero-entropy singular measures produced above.

### Symbolic-factor route

Quas-Soo's suspension theorem is attractive, and strong symbolic coding is available in arbitrary negative curvature. But a finite-to-one coding alone does not automatically preserve an embedded system's no-root obstruction after pushforward. Injectivity on its particular measure, or an appropriate full-support argument, must be verified. The present proof avoids this issue by applying universality directly to F. This route is recorded as an unnecessary detour, not as a second proof.

### General universality route

This is the successful all-dimensional route. The explicit fixed-gap hypothesis, strict positive entropy inequality, aperiodic source, and measurable embedding are all checked above. There is no small-boundary-property assumption and no countability assumption on F-periodic points in Burguet's theorem.

### Direct prior-resolution route

The surface corollary already disposes of the common surface formulation. It alone leaves the manifold wording uncovered, which is why the separate all-dimensional deduction was needed. The full result here follows from established theorems and earns no novelty claim. These five route families record the investigation; the successful prior-resolution route terminates further proof searching within the campaign budget.

## Related-source caution

The neighboring Pingree item attributed to Thouvenot is a broader suspension universality question. Do not automatically mark it solved from this audit: roof regularity, positivity, topological weak mixing, and the precise measure-theoretic coding hypotheses must be checked on its own statement. Arithmetic roofs can introduce an eigenvalue obstruction. No neighboring queue row is modified by this packet.

## Verification limits

The included exact Python controls check finite cyclic no-root obstructions, odd-cycle positive controls, rational periodic-orbit samples, and failures of overbroad assertions. They do not numerically construct the measure on a specified manifold, certify the imported universality theorem, or replace an independent mathematical review. The construction is non-explicit at its measurable embedding step, exactly as permitted by the existence question.
