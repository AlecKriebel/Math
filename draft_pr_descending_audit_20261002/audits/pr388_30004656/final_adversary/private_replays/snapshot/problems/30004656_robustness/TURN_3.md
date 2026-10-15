# Turn 3: a sphere-domain rank floor with explicit uniform constants

Third substantive turn; original unresolved. This reconstructs the credited BLN undercomplete projection mechanism on the source's actual sphere-restricted Lipschitz domain, allows nonsmooth and data-dependent nonlinearities, and records a fixed-accuracy version with explicit constants. The fiber-transport observation also appears in Shmalo2026 §8; that source is credited. This is not a new unrestricted n-versus-width law or a historical novelty claim.

## 1. A deterministic sphere-fiber estimate

Let P be an orthogonal projection of rank r<d, and suppose f(x)=g(Px) on S^{d-1}. Write L=Lip_{S^{d-1}}(f), possibly infinite. For u,v in the range of P with norms at most1/2, choose one fixed unit z in ker P and lift them to

    x(u)=u+sqrt(1-||u||²)z,   x(v)=v+sqrt(1-||v||²)z.

They lie on the sphere and have projections u,v. The difference of their square-root coordinates is at most ||u-v||/sqrt3: rationalize the difference, use that both square roots are at least sqrt3/2, and bound | ||u||²-||v||² |≤(||u||+||v||)||u-v||≤||u-v||. Hence

    |g(u)-g(v)|≤(2/sqrt3)L ||u-v||.                       (1)

There is no derivative assumption on g, and no segment outside the sphere is used to estimate L. This correct domain bridge is the reason a global-norm proof is not simply relabeled as a sphere-norm proof.

## 2. A single event controlling every data-dependent projection

Let x_i be iid uniform on S^{d-1}, d≥2, and y_i independent random signs. Assume n≥8d. With probability at least

    1-exp(-n/4)-2exp(-n/32),                              (2)

the following two properties hold:

    ||sum_i x_i x_i^T||_op ≤8n/d;                         (3)
    each sign occurs at least3n/8 times.                 (4)

The label assertion is Hoeffding's inequality. Here is a self-contained net proof of(3). For a unit u and integer m≥0, the standard spherical moment identity gives

    E[d<u,x>²]^m = d^m(2m-1)!!/[d(d+2)...(d+2m-2)]
                  ≤(2m-1)!!.

At m=0 both sides are1. The identity follows, for example, by writing a standard Gaussian as its independent radius times a uniform direction and comparing even moments. Summing the nonnegative moment series yields E exp(d<u,x>²/4)≤sqrt2. Independence and exponential Markov therefore give

    P(sum_i <u,x_i>² ≥4n/d) ≤ exp[-n+(n/2)log2].

A1/4-net of the unit sphere has at most9^d points. For a positive semidefinite matrix, its operator norm is at most twice the maximum quadratic form on this net, by approximating a maximizing unit vector and bounding the quadratic-form difference by2·(1/4)||A||. Thus the failure probability of(3) is at most9^d exp[-n+(n/2)log2]≤exp(-n/4) when n≥8d. The elementary estimates log9<3 and log2<3/4 suffice for the final inequality.

On(3), for every rank-r orthogonal P, including those chosen after seeing both inputs and labels,

    sum_i ||Px_i||² =trace(P sum_i x_i x_i^T) ≤8nr/d.     (5)

No union bound over an adaptive projection family is inserted later.

## 3. Approximate interpolation and low projection points

Suppose the empirical squared error of f is at most1/256. At most n/16 observations can have |f(x_i)-y_i|>1/4, by Markov's inequality.

First assume 1≤r≤d/512. By(5), at most32nr/d≤n/16 observations have ||Px_i||>1/2. Pair min(n_+,n_-) opposite-label observations arbitrarily, without reuse. By(4) there are at least3n/8 pairs. Removing all pairs with an inaccurate or high-projection endpoint removes at most n/8 pairs. At least n/4 good pairs remain.

Each good pair (i,j) has |f(x_i)-f(x_j)|≥3/2. Applying(1) gives

    ||P(x_i-x_j)|| ≥3sqrt3/(4L) ≥1/L.

On the other hand, since the pairs have disjoint endpoints,

    sum_pairs ||P(x_i-x_j)||² ≤2 sum_i ||Px_i||² ≤16nr/d.

The good pairs therefore give n/(4L²)≤16nr/d, or

    L²≥d/(64r).                                          (6)

If L is infinite the conclusion is automatic. If r=0, f is constant on the sphere; on(4) its minimum empirical squared error is at least15/16, so it cannot meet the stated accuracy.

For r>d/512, at least one opposite-label pair has both endpoint errors at most1/4, again by(4) and the n/16 error count. Their chord distance is at most2, so L≥3/4. Since d/r<512 this implies

    L ≥ [3/(32sqrt8)] sqrt(d/r).                         (7)

The same weaker constant also follows from(6) in the small-rank case. Thus(7) holds on the single event(2) for every projection-factorized function meeting the accuracy threshold, every rank1≤r≤d, and every choice of P or g after observing the data.

## 4. Neural-network consequence and limits

A width-k two-layer network without a separate affine skip depends only on the span of its k first-layer weight vectors, so r≤min(k,d). Biases and output weights do not change this span. Thus(7) gives

    Lip_{S^{d-1}}(f) ≥ [3/(32sqrt8)] sqrt(d/k)             (8)

for every empirical-error≤1/256 network, uniformly over all real weights and biases. The activation may be different at each unit or data-dependent, since the proof only uses the factorization. With an affine skip, replace k by k+1, or use the exact span rank including its slope vector.

When n is comparable to d, (8) has the source's sqrt(n/k) order, with a constant depending on the upper bound for n/d. When n≫d, it leaves the essential missing sqrt(n/d) factor. The conclusion does not require polynomial parameter bounds, but it also does not solve the overcomplete high-dimensional regime. The credited Shmalo projection-capacity refinements address other small-width windows; no claim of surpassing all those results is made here.

The finite exact checker verifies the sphere-lift inequality algebra, spherical moment comparison and all constant/counting implications. These checks are supplementary to the analytic uniform event proof. Original unresolved3/5.
