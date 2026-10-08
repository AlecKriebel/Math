# Alexander interpolation and the parameter-dimension gap

## Scope and result

This is an authored mathematical audit for the ANR question about homeomorphism groups. It makes no claim to settle Kirby KP-5.4 and no claim of novelty. All constructions below are proved directly. The final fragmentation implication is conditional, with its hypotheses stated explicitly.

The main result is a concrete failure of one tempting proof scheme: for every spatial dimension n >= 2, ordered barycentric interpolation obtained from the Alexander contraction has genuinely linear worst-case dependence on the number of vertices. There are vertices converging uniformly to the identity whose interpolated values remain distance at least 1/2 from the identity. Thus this interpolation cannot simply be combined with arbitrary locally finite partitions of unity to prove the ANR assertion. This failure occurs even in spatial dimension 2, so it is not evidence that the disk homeomorphism group fails to be an ANR.

In contrast, the same construction gives a fully explicit extension argument for bounded-multiplicity parameter covers, and hence for finite-dimensional metrizable parameter spaces. The spatial dimension n and the parameter dimension m are different quantities throughout.

## 1. Notation and elementary topology

Let D^n be the closed Euclidean unit ball, let e be its identity map, and set

    G_n = Homeo(D^n rel boundary).

Composition is written hk = h composed with k. Equip G_n with

    d(h,k) = sup_{x in D^n} |h(x)-k(x)|.

This is the compact-open topology because the domain is compact. Composition and inversion are continuous in this topology. For inversion, if h_j -> h uniformly, write y = h_j(x); then

    |h_j^{-1}(y)-h^{-1}(y)|
      = |x-h^{-1}(h_j(x))|
      <= omega_{h^{-1}}(d(h_j,h)),

where omega_{h^{-1}} is a uniform continuity modulus. Composition continuity follows in the same way. Also

    d(ha,ka) = d(h,k)

for every a in G_n, because a is onto. The metric d need not be complete; completeness is not used. The equivalent metric

    D(h,k) = max(d(h,k), d(h^{-1},k^{-1}))

may be used when simultaneous forward-and-inverse control is wanted.

## 2. The Alexander contraction has exact one-step estimates

For 0 < t <= 1 define

    alpha_t(h)(x) = t h(x/t)   if |x| <= t,
                 = x          if |x| >= t,

and put alpha_0(h) = e. Boundary-fixing makes the two formulas agree.

### Lemma 1

The map (h,t) -> alpha_t(h) is continuous G_n x [0,1] -> G_n. Each alpha_t is a group homomorphism, and

    alpha_s alpha_t = alpha_{st},
    alpha_t(h)^{-1} = alpha_t(h^{-1}),
    d(alpha_t(h), alpha_t(k)) = t d(h,k),
    D(alpha_t(h), alpha_t(k)) = t D(h,k).

In particular alpha_1 is the identity and alpha_0 is the constant map at e.

Proof. On the radius-t ball this is conjugation by the dilation x -> tx; outside that ball it is the identity. These observations prove the group and semigroup identities. Taking a supremum over the radius-t ball gives the exact metric identity for t > 0; t = 0 is immediate. The inverse identity then gives the D identity.

For joint continuity away from t = 0, extend u_h(x) = h(x)-x by zero outside D^n. This extension is continuous because u_h vanishes on the boundary. The formula is

    alpha_t(h)(x) = x + t u_h(x/t).

Uniform continuity of u_h on compact sets, together with uniform convergence of u_{h_j} to u_h, proves continuity for t > 0. At t = 0 use the uniform bound

    d(alpha_t(h),e) <= 2t

for all h. This also applies to inverses. QED.

Define the global equiconnection

    lambda(h,k,t) = alpha_t(kh^{-1})h.

Then lambda(h,k,0) = h, lambda(h,k,1) = k, and lambda(h,h,t) = h. Right invariance of d gives the stronger exact identity

    d(lambda(h,k,t),h) = t d(k,h).                 (1)

Consequently every d-ball about h contracts to h inside itself by reversing t in lambda(h,k,t). This is a local-contractibility statement, not an ANR proof.

## 3. Compatible interpolation on finite simplices

For ordered vertices h_0,...,h_m and barycentric coordinates p_0,...,p_m, define I_m recursively. Let I_0(h_0;1) = h_0. For m > 0 put r = 1-p_0. If r = 0 set I_m = h_0. Otherwise put

    J = I_{m-1}(h_1,...,h_m; p_1/r,...,p_m/r),
    I_m(h_0,...,h_m;p) = lambda(h_0,J,r).

### Lemma 2

Each I_m is jointly continuous in its vertices and coordinates. Deleting a zero barycentric coordinate and its vertex leaves the result unchanged. If all vertices equal q, the result is q. For every q in G_n,

    d(I_m(h_0,...,h_m;p),q)
       <= (2m+1) max_i d(h_i,q).                 (2)

Proof. Induct on m. The only apparent continuity issue is r -> 0, but (1) gives

    d(I_m,h_0) = r d(J,h_0) <= 2r,

uniformly in the remaining vertices and normalized weights. If p_0 = 0, r = 1 and lambda(h_0,J,1) = J. Other zero-coordinate deletions follow by induction. The diagonal identity follows similarly.

For (2), let delta = max_i d(h_i,q). By induction d(J,q) <= (2m-1)delta. Therefore

    d(I_m,q)
      <= d(h_0,q) + r d(J,h_0)
      <= delta + r((2m-1)delta+delta)
      <= (2m+1)delta.

QED.

For later use let S_j = p_j+...+p_m, so S_0 = 1 and S_{m+1} = 0. The group and semigroup identities in Lemma 1 give

    I_m = E_m E_{m-1} ... E_0,
    E_j = alpha_{S_{j+1}}(h_j)^{-1} alpha_{S_j}(h_j).       (3)

This follows by induction when all relevant tails are positive, and by continuity on the remaining faces. Formula (3) is an equality in the potentially noncommutative group G_n; its displayed order matters.

## 4. A complete bounded-parameter-dimension extension proof

### Lemma 3

Let X be metrizable, let A be a nonempty closed subset, and let f:A -> G_n be continuous. Suppose the standard small-ball cover of X minus A described below has a locally finite open refinement of multiplicity at most m+1. Then f extends continuously over all of X.

In particular this applies when X has finite covering dimension at most m, by the usual bounded-order refinement characterization of covering dimension for metrizable spaces.

Proof. Choose a compatible metric rho on X. For each x outside A put r_x = dist(x,A) > 0 and let

    B_x = B_rho(x,r_x/4).

Choose a locally finite refinement {V_i} of multiplicity at most m+1, and choose x_i with V_i subset B_{x_i}. Choose a_i in A such that

    rho(a_i,x_i) < 2r_{x_i}.

Take a locally finite partition of unity {phi_i} subordinate to {V_i}, so phi_i(y)>0 implies y in V_i. Give the index set any fixed total order. For y outside A, list the finitely many positive coordinates in that order and define F(y) using the corresponding I_k, the vertex values f(a_i), and the weights phi_i(y). Define F = f on A.

The zero-coordinate deletion property proves compatibility. Local finiteness and the joint continuity of I_k prove continuity away from A, including where a weight becomes zero.

Fix a in A. If phi_i(y)>0, then rho(y,x_i)<r_{x_i}/4, whence

    dist(y,A) > 3r_{x_i}/4,
    rho(a_i,y) < 9r_{x_i}/4 < 3 dist(y,A),
    rho(a_i,a) < 4rho(y,a).

Thus, as y -> a, every active a_i tends uniformly to a. Continuity of f implies that max over active i of d(f(a_i),f(a)) tends to zero. At most m+1 coordinates are active, so (2), with the upper bound 2m+1, gives F(y) -> f(a). This proves continuity on A. If A is empty, the constant identity map is an extension. QED.

The final use of a uniform bound on the number of active vertices is the exact point that does not survive for an arbitrary metrizable X. An arbitrary locally finite partition has finitely many active coordinates at each point, but these numbers need not be uniformly bounded as that point approaches A.

## 5. The missing dimension-free estimate is false for this interpolation

Here the distinction is sharper than an unproved estimate: the particular interpolation I_m above cannot satisfy that estimate.

### Theorem 4: radial-twist amplification

For every n >= 2 and every positive integer N there exist h_0^(N),...,h_N^(N) in G_n and p^(N) in Delta^N such that

    max_j D(h_j^(N),e) <= pi/(2N),
    d(I_N(h_0^(N),...,h_N^(N);p^(N)),e) >= 1/2.       (4)

Proof. Let R_theta rotate the first two coordinates through angle theta and fix the other coordinates. For a continuous real-valued function phi on [0,1] with phi(1)=0, define

    h_phi(x) = R_{phi(|x|)}x.

This is a boundary-fixing homeomorphism: it preserves radius, and its inverse is h_{-phi}. Such homeomorphisms commute, and

    D(h_phi,e) = d(h_phi,e) <= ||phi||_infinity.

For s>0 and |x|<=s,

    alpha_s(h_phi)(x) = R_{phi(|x|/s)}x.             (5)

Take p_j = 1/(2N) for 0<=j<N and p_N = 1/2. Then

    S_j = 1-j/(2N),  0<=j<=N.

Fix r = 1/4 and a_N = pi/(2N). For each 0<=j<N choose a continuous piecewise-linear phi_j:[0,1] -> [-a_N,a_N] with

    phi_j(0) = phi_j(1) = 0,
    phi_j(r/S_j) = a_N,
    phi_j(r/S_{j+1}) = -a_N.

These interpolation nodes are distinct and lie strictly between 0 and 1, since 1/2 <= S_{j+1}<S_j<=1. Set h_j^(N)=h_{phi_j} for j<N and h_N^(N)=e. The first assertion of (4) follows immediately.

Every factor in (3) preserves the radius r. By (5), its action on the radius-r sphere, for j<N, is rotation through angle

    phi_j(r/S_j) - phi_j(r/S_{j+1}) = 2a_N.

The j=N factor is the identity. Therefore their product rotates the first coordinate vector x=re_1 by angle 2Na_N=pi. It sends re_1 to -re_1, a Euclidean displacement of 2r=1/2. This proves the second assertion of (4). QED.

### Consequences and exact limits

1. The following dimension-free local stability assertion is false for I_m at q=e: for every epsilon>0 there exists delta>0 such that, for every m and every set of vertices in the delta-ball about q, the whole interpolated simplex lies in the epsilon-ball about q. Take epsilon<1/2 in (4).

2. Let A_m be the supremum of d(I_m,q)/max_i d(h_i,q), over nonconstant data, weights, and centers. For n>=2, (2) and (4) imply

       m/pi <= A_m <= 2m+1.

   Thus the linear dependence on simplex dimension is real, not merely an artifact of the upper-bound proof.

3. This does not show G_n is not an ANR. It rules out this specific universal interpolation as an uncontrolled, dimension-independent extension operator. A different interpolation, a target-adapted cover, or a different extension method remains possible. In particular the counterexample also exists when n=2.

4. The source of amplification is uncontrolled spatial oscillation of the vertex homeomorphisms. Small uniform displacement alone permits the twist angle to reverse across arbitrarily narrow radial intervals. Bounded parameter dimension prevents arbitrarily many such increments from accumulating in this construction.

### A literal discontinuous-extension example for the canonical rule

The preceding calculation can be realized on a compact metrizable parameter space. Let X be the disjoint union of Delta^N for N>=1, together with a point a. Give Delta^N its sup-coordinate metric divided by N, put dist(a,Delta^N)=1/N, and put the distance between distinct components Delta^N and Delta^M equal to 1/N+1/M. This is a metric, and X is compact: each component is compact and the components converge to a in diameter and distance.

Let A consist of a and all simplex vertices. It is closed. Define f(a)=e and, on the vertices of Delta^N, use h_j^(N). Estimate (4) proves that f:A -> G_n is continuous. But extending on each simplex by the canonical I_N makes the points p^(N) -> a have images distance at least 1/2 from e. That canonical extension is discontinuous. This is a failure of the rule, not a claim that f has no other extension.

## 6. A genuinely sufficient dimension-free replacement

For comparison, suppose there were another family of continuous finite-simplex operations J_m on G_n, compatible with deleting zero coordinates and equal to the common vertex on constant data, with the following property:

    For every q and epsilon>0 there is delta>0 such that,
    simultaneously for every m, all vertices within delta of q
    have all J_m values within epsilon of q.                 (USC)

Then G_n would be an absolute extensor for all metrizable spaces, hence an AR and an ANR. Indeed, repeat Lemma 3 using an arbitrary locally finite refinement and subordinate partition of unity; metric paracompactness provides these without a multiplicity bound. The same estimate rho(a_i,a)<4rho(y,a) makes all active vertex images lie in the one delta-ball required by (USC). This proves continuity at A regardless of how many coordinates are active. No additional argument is needed away from A.

This is a sufficient route, not a claimed necessary characterization of ANR by this particular global J_m format. Theorem 4 proves only that the Alexander-derived I_m is not such a family.

## 7. Conditional finite-fragmentation reduction

### Lemma 5

Let G be a separable metrizable topological group and G_1,...,G_r topological subgroups, with their subspace topologies. Suppose there are an open identity neighborhood U in G and continuous maps

    sigma_i:U -> G_i

such that sigma_1(g)...sigma_r(g)=g for all g in U. If each G_i is an ANR, then U is an ANR. Consequently G is an ANR by the local-to-global theorem for metrizable ANRs.

Proof. Let P=product_i G_i and p:P -> G be multiplication. Let sigma=(sigma_1,...,sigma_r), so p sigma=id_U. The set W=p^{-1}(U) is open in P. The map

    R:W -> sigma(U),  R(z)=sigma(p(z))

is a retraction, and sigma is a homeomorphism U -> sigma(U), with inverse the restriction of p. Finite products of ANRs, their open subsets, and their retracts are ANRs. Hence U is an ANR. Its translates give an open ANR cover of G; apply the local-to-global theorem. QED.

The finite product, open-subspace, and retract facts can also be proved directly with neighborhood extensions. For example, extend finitely many component maps over neighborhoods, intersect those neighborhoods, and shrink by the inverse image of U after multiplying.

For a compact manifold without boundary, a subgroup consisting of homeomorphisms supported in a coordinate closed n-ball B is homeomorphic to G_n: restrict to B in one direction, and extend by the identity in the other. Here “supported in B” means fixing the complement of the interior of B pointwise. Consequently continuous finite local fragmentation into such factors, together with the additional assertion that G_n is an ANR, would imply that Homeo(M) is an ANR.

This paragraph does not assert a fragmentation theorem without checking its exact hypotheses. Merely producing a factorization for each g is not enough: its factors must vary continuously with g on one neighborhood U. Also, for manifolds with boundary, ordinary interior balls cannot cover the boundary. Boundary-adapted factors and their own ANR hypotheses must be supplied rather than silently replaced by G_n.

## 8. A disk-product sanity check

Restriction to the boundary has an explicit section

    c:Homeo(S^{n-1}) -> Homeo(D^n),
    c(b)(ru)=r b(u),  c(b)(0)=0.

The section is continuous, as is restriction. Every self-homeomorphism of the ball preserves its boundary. Thus

    Homeo(D^n) -> G_n x Homeo(S^{n-1}),
    h -> (h c(h|boundary)^{-1}, h|boundary)

is a homeomorphism with inverse (g,b) -> g c(b). In particular G_n is a retract of Homeo(D^n). If Homeo(D^n) were known to be an ANR, G_n would be one too; conversely G_n and Homeo(S^{n-1}) both being ANRs would imply that Homeo(D^n) is an ANR. This is a product decomposition, not a proof that either unknown factor is an ANR.

## 9. Source dependencies and unresolved conclusions

Sections 1–6 and 8 are direct proofs. They require only elementary properties of compact metric mapping spaces, Euclidean rotations, metric paracompactness and partitions of unity. The finite-covering-dimension corollary in Section 4 uses the standard bounded-order open-refinement characterization of covering dimension; the core lemma states the needed covering hypothesis explicitly.

Section 7 uses the standard ANR closure properties and the local-to-global theorem. A primary reference for the latter is Olof Hanner, “Some theorems on absolute neighborhood retracts,” Arkiv för Matematik 1 (1951), 389–408, Theorems 3.2–3.3, printed pp. 392–394. Hanner's original article explicitly works in the separable metrizable category, which covers the compact-manifold homeomorphism groups here. The primary PDF was inspected through its statement and proof:

https://webhomes.maths.ed.ac.uk/~v1ranick/papers/hanner.pdf

https://doi.org/10.1007/BF02591376

No assertion about the current published status of KP-5.4 is proved by these calculations. That requires the separate current-source audit. The exact mathematical output here is:

- a rigorously proved finite-dimensional parameter-extension construction;
- an explicit, order-sharp obstruction to dimension-free use of that canonical construction;
- a sufficient replacement property whose proof would provide the missing arbitrary-metrizable extension;
- a finite-fragmentation reduction whose continuous factor maps and factor ANR assumptions must actually be established.

Neither contractibility, strict contraction of individual metric balls, finite-dimensional parameter extension, nor a merely pointwise fragmentation proves the requested ANR assertion.
