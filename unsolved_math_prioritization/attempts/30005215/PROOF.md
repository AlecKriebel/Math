# Low-memory norm estimation with asymmetric oracle access

## Verdict, scope, and credit

Both finite-dimensional norm-estimation questions have an affirmative answer.
This is a credited exposition of existing random-plane methods, not a claim of
new resolution. Jonas Bresch, Dirk A. Lorenz, Felix Schneppe, and Maximilian
Winkler treat the single-operator problem in [1] and the mismatch problem in [2].
Their stated results match the two questions in Lorenz's Oberwolfach contribution
[3]. The complete argument below uses compact one- or two-dimensional
maximization and avoids exceptional step-size denominators.

The model is exact real arithmetic, finite-dimensional Euclidean input/output
spaces, and exact linear-map evaluations. Storage refers to a constant number of
input/output vectors, excluding the black boxes' internal storage. The estimates
converge almost surely and can be improved incrementally. No dimension-independent
iteration bound, floating-point certification, or deterministic finite-time
upper bound is asserted. In particular, a current lower estimate must not be
silently substituted for an upper bound in a step-size guarantee.

The original report opens with general Hilbert-space optimization, but its
numerical oracle questions and covariance construction concern implementable
vectors. The theorem here explicitly covers the finite-dimensional formulation
used in [1,2]. It does not assert a theorem for arbitrary infinite-dimensional
Hilbert spaces or convergence of every step-size schedule in the report's
suggested stochastic-gradient iteration.

## 1. The theorem

Let d,m be positive integers. Suppose A,V: R^d -> R^m are linear. We have oracles
F(v)=Av and G(u)=V^T u; we have no oracle for A^T or V.
Set B=A-V for analysis only. Then there is an algorithm using O(d+m) real-number
storage, one new call to each available oracle per nondegenerate iteration after
initialization, and scalar/constant-size linear algebra, producing nonnegative
values s_k such that

    0 <= s_k <= s_(k+1) <= ||B||_2,
    s_k -> ||B||_2 almost surely.

Setting G=0 gives an answer for ||A|| using only A. A specialized version uses
one new A call per iteration and maximizes ||Av|| directly (Section 5).

For a zero-dimensional input or output the operator norm is zero; return zero.
Henceforth assume d,m >= 1.

## 2. Oracle-accessible algorithm

For unit u in R^m and v in R^d define

    b(u,v) = <u,F(v)> - <G(u),v> = <u,Bv>.

Choose any initial unit vectors u_0,v_0, evaluate F(v_0),G(u_0), and reverse u_0
and its cached image if necessary so b(u_0,v_0) >= 0. Let s_0=b(u_0,v_0).

At step k:

1. If m>=2, sample w uniformly on the unit sphere in u_k^perp. If d>=2,
   independently sample x uniformly on the unit sphere in v_k^perp. Fresh
   samples are independent of the past conditional on the current vectors.
   Projecting a standard Gaussian onto the relevant tangent space and
   normalizing generates these laws; the zero projection is a null event and
   can be resampled. In dimension one omit the corresponding tangent vector.
2. Let U=[u_k,w] and Q=[v_k,x], omitting nonexistent second columns. The columns
   of each matrix are orthonormal. These matrices have at most two columns.
3. Form the at-most-2-by-2 matrix C with entries

       C_ij = <U_i,F(Q_j)> - <G(U_i),Q_j>.

   Cached images supply the old columns; F(x) and G(w) supply the new ones.
4. Maximize p^T C q over unit coefficient vectors p and q. Set p,q to a top
   left/right singular-vector pair with p^T C q=||C||_2>=0, and set

       u_(k+1)=Up,  v_(k+1)=Qq,  s_(k+1)=||C||_2.

   Update the cached images by linear combinations:

       F(v_(k+1)) = sum_j q_j F(Q_j),
       G(u_(k+1)) = sum_i p_i G(U_i).

All small maximizations are over compact spheres. They exist even when C=0,
has rank one, has repeated singular values, or the optimum corresponds to an
infinite slope in a tangent chart. No division by a projected determinant or
off-diagonal entry is used. To make the stochastic process completely defined,
use any fixed Borel tie-breaking rule: for example take q in the top eigenspace
of C^T C by projecting the first coordinate vector with a nonzero projection
and normalizing with positive first nonzero entry; if ||C||>0 set p=Cq/||C||,
and if C=0 choose both first coordinate vectors.

There are only a fixed number of length-d and length-m vectors and a constant-size
matrix. Thus the storage is O(d+m)=O(max(d,m)), independent of the number of
iterations. The algorithm does not assemble A,V,B, or a growing sketch.

## 3. A uniform random-plane approximation lemma

For n>=2 and 0<delta<1 let

    p_n(delta) = P(||X-z||<delta),

where X is uniform on S^(n-2) and z is any fixed point of that sphere. Rotation
invariance makes this probability independent of z, and it is positive: for
n=2 the sphere is the two-point set S^0 and the probability is 1/2; for n>=3
an open spherical cap has positive surface measure. Set p_1(delta)=1.

**Lemma.** Fix any unit a,t in R^n. Let P=span(a,X), where X is uniform on
the unit sphere of a^perp (and let P=R when n=1). With probability at least
p_n(delta), P contains a unit vector t' satisfying ||t'-t||<delta, or t'=t.
The lower bound is uniform in both a and t.

**Proof.** For n=1 there is nothing to prove. For n>=2 write

    t = alpha a + beta z,
    alpha=<a,t>,  beta=sqrt(1-alpha^2).

If beta=0, t=+/-a is already in P for every sample. Otherwise z is a fixed
unit vector in a^perp. On the event ||X-z||<delta, let t'=alpha a+beta X.
Orthogonality gives ||t'||^2=alpha^2+beta^2=1, and

    ||t'-t||=beta||X-z||<delta.

This event has probability p_n(delta). This proves the claim. QED.

## 4. Complete convergence proof for the mismatch algorithm

Orthonormality and the defining identity give

    max_(||p||=||q||=1) p^T Cq
      = max_(u in range(U), v in range(Q), ||u||=||v||=1) <u,Bv>.

The old pair is feasible. Every feasible value is bounded above by ||B||.
Thus the algorithm is well-defined and 0<=s_k<=s_(k+1)<=||B||.

If ||B||=0, all values are zero and the conclusion holds. Suppose M=||B||>0.
Finite-dimensional compactness gives unit t in R^d with ||Bt||=M. Set
r=Bt/M; then ||r||=1 and <r,Bt>=M.

Fix 0<epsilon<1 and delta=epsilon/4. At every iteration, conditional on the
entire past, apply the lemma to target r in the output space and target t in
the input space. Independence of w and x shows that, with conditional
probability at least

    p = p_m(delta) p_d(delta) > 0,

the sampled planes contain unit r',t' with errors at most delta. On that event,

    |<r',Bt'>-<r,Bt>|
      <= |<r'-r,Bt'>| + |<r,B(t'-t)>|
      <= M (||r'-r|| + ||t'-t||)
      <= 2 M delta.

Consequently the maximum selected by the algorithm satisfies

    s_(k+1) >= M(1-2delta) > M(1-epsilon).

It does not matter whether the selected maximizer itself lies in the target
caps; it is its objective value that is compared with their feasible value.

Let E_k={s_k < M(1-epsilon)}. Monotonicity makes E_(k+1) a subset of E_k.
The conditional bound just obtained gives

    P(E_(k+1) | history through step k) <= (1-p) 1_(E_k).

Taking expectations and iterating,

    P(E_N) <= (1-p)^N P(E_0) <= (1-p)^N -> 0.

Since E_k decreases, almost surely the algorithm eventually reaches
M(1-epsilon). Apply this to epsilon=1/j for all integers j>=2. A countable
intersection of probability-one events still has probability one. On that event,
the bounded nondecreasing sequence s_k approaches M arbitrarily closely and
therefore converges to M. QED.

The factor is 1-p_m p_d: the favorable event requires both independent plane
approximations. It is not (1-p_m)(1-p_d).

This argument requires no spectral gap, simplicity, nonzero projected determinant,
or absence of stationary initial points. It covers rank deficiency, repeated
singular values, B=0, and either ambient dimension equal to one. It proves norm
convergence; no assertion that the actual singular vectors converge is needed.

## 5. Specialized one-oracle variant

For a current unit v, sample unit x in v^perp (omit it when d=1). Set
Q=[v,x], and form the Gram matrix H=(AQ)^T(AQ), which has size at most two.
Take a unit top eigenvector q of H, set v_new=Qq, and report sqrt(lambda_max(H)).
Its value is the largest ||Az|| over unit z in range(Q). Cache Av_new as a
linear combination of Av and Ax. The method uses one new A evaluation and
O(d+m) storage per iteration. Zero matrices and tied eigenvalues cause no
problem because the compact maximum always exists.

For d=1, ||A||=||A(1)|| is obtained immediately. For d>=2 choose a maximizing
unit target t. The lemma says with conditional probability at least p_d(delta)
there is a feasible t' with ||t'-t||<=delta. Hence

    ||At'|| >= ||At||-||A(t'-t)|| >= ||A||(1-delta).

The identical decreasing-event argument proves almost sure convergence to
||A||. This is the compact random-plane form of the Rayleigh-quotient method
of [1]. In a nondegenerate tangent chart, its update is exactly an optimal
line search in v+tau*x, up to the immaterial sign of the new unit vector.

## 6. Source-proof cautions and why the argument is self-contained

The prior articles deserve credit for formulating and solving these oracle
problems. This packet does not certify every statement in them or claim an
error in an unseen later publisher revision. In the inspected version
arXiv:2503.21361v2:

- Proposition 2.11 (p.12) includes the assertion bc-ad != 0 almost surely for
  the four entries C=[[a,c],[b,d]]. For B=rs^T nonzero, C=(U^T r)(s^T Q)
  has rank at most one for every U,Q; therefore bc-ad=0 identically. Non-singular
  initial vector pairs do not remove this example. For instance use
  B=diag(1,0,0), u=v=(3/5,4/5,0), w=x=(-4/5,3/5,0):
  a=9/25, b=c=-12/25, d=16/25, and ad-bc=0. The failure is the general
  nonvanishing claim, not a counterexample to existence of a norm algorithm.
- The complement-of-product event estimate in its Theorem 2.26 proof
  (equation (30), pp.20-21) uses a product of failure factors where simultaneous
  success supplies 1-p_m p_d. The proof above explicitly uses the latter.

The 2-by-2 SVD formulation and direct target-cap proof remove these dependencies.
No outcome here rests solely on a paper's abstract or generated catalogue label.
The provided verification script also checks the rank-one identity exactly.

## References

[1] J. Bresch, D. A. Lorenz, F. Schneppe, M. Winkler, *Matrix-free stochastic
calculation of operator norms without using adjoints*, arXiv:2410.08297v3,
3 December 2025. Algorithm 1; Section 2.2, especially Theorem 2.19 and
Remarks 2.21-2.23. Publisher DOI: 10.1137/25M1772277.
https://arxiv.org/abs/2410.08297v3
https://doi.org/10.1137/25M1772277

[2] Same authors, *Computing adjoint mismatch of linear maps*,
arXiv:2503.21361v2, 9 March 2026. Algorithm 1; Sections 2.1-2.4, especially
Theorem 2.26 and Remarks 2.27-2.28. Publisher DOI: 10.1016/j.cam.2026.117853.
https://arxiv.org/abs/2503.21361v2
https://doi.org/10.1016/j.cam.2026.117853

[3] D. A. Lorenz, *Adjoint mismatch*, in *Mathematical Imaging and Surface
Processing*, Oberwolfach Report 38/2022, printed pp.2250-2252, published
14 June 2023. DOI: 10.4171/OWR/2022/38.
https://ems.press/journals/owr/articles/11101919
