# Independent mathematical audit of Function Theory Problem 7.28

## Decision and provenance

**Accepted: both alternatives imply holomorphicity under the stated continuity hypothesis. No correction patch is required.** The affirmative result already appears in Qiteng Guo and Ao Xiao, [An Infinitesimal Circular Morera Theorem](https://arxiv.org/abs/2608.04540v1), submitted 5 August 2026. Theorem 1.1 addresses the limiting condition and Corollary 1.2 addresses exact local vanishing. This is verification of an existing result, with no novelty claim.

The complete six-page preprint, including all proof steps, was inspected. The public arXiv record was checked on 6 October 2026 and lists v1; journal acceptance or publication was not established. The 2018 update to [Hayman and Lingham, Research Problems in Function Theory](https://arxiv.org/abs/1809.07200v2), Problem 7.28 on printed page 168, is historical evidence rather than a current obstruction to acceptance.

The original five-file author archive was reviewed without altering its bytes. Its SHA-256 is 71fea7845b03ca825e1e4c34524b6b3ab312d5433480eb159c757a0aa3200fa2 (6,273 bytes). Its manifest SHA-256 is b1bd22260ecff4940ee4069ae493e5c21dfbb508a570b00968c37e7adcc0d786. The independent conclusions below do not rely on the author's pass labels. The original package's pending independent-review labels describe its frozen author-stage snapshot; this separate report supplies the completed review without rewriting that snapshot.

## Exact scope and quantifiers

Let D be an open plane domain and f a continuous complex-valued function on D. For a in D and r>0 with the closed disk contained in D, define

J_f(a,r) = integral over |z-a|=r of f(z) dz,

with positive orientation, and define the circular average

M_u(a,r) = (1/(2 pi)) integral from 0 to 2 pi of u(a+r exp(it)) dt.

The hypothesis tested in the harder alternative is: for every a and every eta>0, there exists delta(a,eta)>0 such that |J_f(a,r)| <= eta r^2 for every admissible 0<r<delta(a,eta). The center is fixed before the radius bound is selected. Uniformity over centers, a common radius bound, differentiability, or an almost-everywhere substitute is never assumed.

In the exact-vanishing alternative, each center has its own strictly positive threshold, and every sufficiently small positive radius satisfies J_f(a,r)=0. The source problem includes its endpoint radius; shrinking that threshold gives exactly the strict-radius hypothesis used by the corollary. Conversely, a strict local threshold gives a smaller inclusive threshold, so the endpoint convention has no effect. All arguments stay inside compact disks in D. Circles that surround holes but do not bound disks in D play no role.

The theorem uses all sufficiently small radii at each center. It does not assert the conclusion from selected center-dependent sequences of radii. The radial integration step below would not be justified from such a weakened assumption.

## Independent check of the distributional primitive

Use the Wirtinger operators partial = (partial_x-i partial_y)/2 and bar-partial = (partial_x+i partial_y)/2. The relevant kernel is K(z)=1/(pi conjugate(z)); using 1/(pi z) instead would solve the wrong differential equation.

Here is a direct sign and normalization check. For a compactly supported smooth test function phi, omit the disk of radius epsilon in the distributional pairing -integral K partial(phi) dA. In polar coordinates the integrand reduces to

-(1/(2 pi)) [partial_r phi - (i/r) partial_t phi] dr dt.

The angular derivative has integral zero. Integrating the radial derivative yields the angular average of phi(epsilon exp(it)), with positive sign, which tends to phi(0). The contribution of the omitted disk is O(epsilon) because partial(phi) is bounded and 1/|z| is locally integrable. Thus partial K = delta_0 as distributions, with exactly the displayed factor pi.

Choose V with compact closure in D, then W with closure(V) contained in W and compact closure(W) in D. Choose a smooth compactly supported cutoff chi in D that equals one near closure(W). Set g=chi f, extended by zero, and F=K*g. The integral exists everywhere because g is bounded and compactly supported. For evaluation points x and x+h in a fixed compact set, the continuity estimate is bounded by ||g||_infinity times the L1 norm of the difference between a translate of K and K on a fixed larger compact set. Local L1 translation continuity makes that bound tend to zero. Hence F is continuous. Distributional differentiation of a convolution with a compactly supported factor gives partial F=g, and therefore partial F=f on W.

This constructs only a local weak primitive and presupposes neither classical differentiability of f nor simple connectivity of D.

## Independent check of the circular identity

For smooth F, in polar coordinates about a,

partial F = exp(-it)/2 [partial_r F - (i/r) partial_t F],

dz = i r exp(it) dt.

After multiplication, the angular derivative contributes one half of a full-period derivative and has integral zero. The radial term gives

J_{partial F}(a,r) = i pi r (d/dr) M_F(a,r).

Since M_F(a,r) tends to F(a) as r tends to zero, integration gives

M_F(a,R)-F(a) = -(i/pi) integral from 0 to R of J_f(a,s)/s ds.  (1)

This is valid at the weak regularity actually available. Choose a closed disk of radius R1>R still inside W and a cutoff equal to one near that larger disk. Mollify the cutoffs of F and f with the same compactly supported approximate identity. On a neighborhood of the closed radius-R disk, the distributional equation becomes partial F_epsilon=f_epsilon; the derivative of the cutoff makes no contribution there. Both smooth approximations converge uniformly on that smaller closed disk. For every 0<s<=R,

|J_{f_epsilon}(a,s)-J_f(a,s)|/s <= 2 pi ||f_epsilon-f||_infinity.

The error after integration over s in (1) is therefore at most 2 R ||f_epsilon-f||_infinity, including the prefactor 1/pi. It tends to zero. Before multiplication by that prefactor, the bound is 2 pi R ||f_epsilon-f||_infinity, as in the author report. The left-hand side converges by uniform convergence of F_epsilon.

The lower endpoint is harmless even without the main hypothesis: subtract f(a) under the circular integral to obtain |J_f(a,s)|/s <= 2 pi omega_f(a,s), where omega_f is a local continuity modulus. This is bounded near zero and tends to zero. Thus the improper integral is absolutely convergent. The proof has not applied classical Cauchy-Green directly to a merely continuous f and has not assumed that circlewise differentiation of a weak primitive is classically valid before mollification.

## From pointwise circular control to harmonicity

Fix a single center a. Its hypothesis bounds the modulus of J_f(a,s) by eta s^2 for all sufficiently small s. Identity (1) gives

|M_F(a,R)-F(a)| <= eta R^2/(2 pi)

for all sufficiently small R. Consequently each real component of F satisfies M_u(a,R)-u(a)=o(R^2) at every center. Only the radius is integrated. No limit is interchanged with an integral over centers, and no uniform center bound is introduced.

The external mean-value input is [Kuznetsov, Mean value properties of harmonic functions and related topics](https://arxiv.org/abs/1904.08312v2), Theorem 1.6. Its dimension range is m>=2, including the planar case. Its L is the spherical average, not the ball average: in dimension two its normalization is (2 pi r)^(-1) times the arclength integral, equal to M_u as defined here. The theorem assumes continuity and a pointwise full-radius limit at every center. It does not require a uniform limit. The symbol, range and quantifiers were checked against the rendered PDF.

For independence from that citation, the planar implication has the following complete argument. On any closed disk B(c,R) within the domain, let h be the Poisson extension of the continuous boundary values of a real continuous u satisfying the asymptotic mean condition. The Poisson extension is harmonic inside and continuous up to the boundary. Put w=u-h; w is zero on the boundary and has the same asymptotic mean defect, because every sufficiently small mean defect of h is zero.

For epsilon>0 consider v(z)=w(z)+epsilon |z-c|^2. At every interior point a, its circular mean defect is o(r^2)+epsilon r^2 and hence strictly positive for all sufficiently small r. If v had a local maximum at a, all such sufficiently small circular averages would be at most v(a), a contradiction. Its global maximum exists on the compact closed disk and must therefore lie on its boundary, where its value is epsilon R^2. It follows that

w(z) <= epsilon (R^2-|z-c|^2).

Letting epsilon decrease to zero gives w<=0. Apply the same argument to -w to obtain w>=0. Thus u=h throughout the disk and is harmonic. The small radius is selected only after choosing a hypothetical interior maximizing point; the argument does not covertly require a radius valid at every point. There is no assumption that u itself has a classical Laplacian.

## Finishing the proof and controls

Both real components of F are harmonic, so F is smooth and bar-partial(partial F)=Delta F/4=0. Hence partial F is holomorphic. The original f agrees with partial F as a distribution and thus almost everywhere; their continuous difference must vanish everywhere. Since V was arbitrary, f is holomorphic throughout D. Exact local vanishing implies the limiting condition, completing both alternatives.

The control F(z)=|z|^2 gives partial F=conjugate(z), J_{partial F}(a,r)=2 pi i r^2, and M_F(a,r)-F(a)=r^2. It verifies the sign and every constant in (1), at any center. The same f shows that replacing little-o by big-O would be false. A continuous function that is holomorphic gives zero circular integrals on every compactly contained disk by Cauchy's theorem, so the conclusion is consistent in the reverse direction.

No step requires a bounded ambient domain, a smooth ambient boundary, or simple connectivity. The local closed disks provide every compactness and boundary-continuity condition actually used. The proof covers the original problem's two alternatives without an additional hypothesis or missing regularity argument.

## Package decision and limits

The immutable author archive passes exact namespace, regular-file mode, non-executable inventory, CRC, byte count, UTF-8, JSON and externally pinned hash checks. Independent validation was repeated under isolated normal and optimized Python and after relocation, with nineteen malformed fixtures rejected in each run. These tests concern integrity and safe static inspection; they are not a formal proof checker. No executable payload is delivered.

This independent package contains authored audit prose and bounded verification metadata only. It contains no third-party paper, extracted source text, dataset contents or private coordination material. The mathematical decision is acceptance as an existing affirmative preprint result. No patch, remote publication, repository state change, or assertion of journal acceptance is part of this review.
