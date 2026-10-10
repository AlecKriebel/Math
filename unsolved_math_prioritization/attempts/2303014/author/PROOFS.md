# Subharmonic circle-minimum extremals: reconstructed partial results

Problem ID 2303014; Hayman–Lingham Problem 3.14 (Baernstein).
Reconstruction date: 2026-10-05 UTC. This is a new authored proof packet,
not a recovered copy or an independent audit of the interrupted packet.
The general positive-mean boundary-data problem remains unresolved here.

## 1. Scope and precise classes

Let D={z:|z|<1}, T=∂D, and let F be a real L1(T,dθ) function. Write

H(z)=P[F](z)=(1/(2π))∫_{−π}^{π} ((1−|z|²)/|e^{it}−z|²) F(e^{it}) dt,
m=H(0), F+=max(F,0), F−=max(−F,0).

The source asks for the largest value at a fixed interior point subject to
subharmonicity, boundary data F, and a nonpositive infimum on every circle
centered at 0. Its wording does not specify the boundary topology. We therefore
make no claim that either class below is the unique intended interpretation.

Define A_F to consist of finite, continuous, subharmonic functions u on D such that:

1. u≤P[F] throughout D;
2. lim_{r↑1}u(re^{it})=F(e^{it}) for almost every t;
3. min_{|z|=r}u(z)≤0 for every 0<r<1.

Define W_F by dropping condition 1, retaining the other conditions. Continuity
is only inside D. No continuity at every point of T is assumed. In particular,
when F=c>0 the extremizers below have one exceptional boundary point.
A requirement u∈C(cl D), u|T=c>0 would make the feasible class empty: uniform
continuity forces u>c/2 on all circles sufficiently close to T.

Continuity at 0 and condition 3 imply u(0)≤0. Thus P[F] is infeasible in A_F
when m>0, since it is strictly positive on a sufficiently small disk.

## 2. A slit operator for arbitrary nonnegative L1 data

For G≥0 in L1(T), define a boundary function g on the w-unit circle as follows.
On its right semicircle set g(ξ)=G(ξ²). On its left semicircle impose

g(−conj ξ)=−g(ξ),  Re ξ>0.

Endpoint values are immaterial. Let h=P[g] on the w-disk. Define S[G] on the
z-disk by h(√z) on D\(−1,0], using the square root with positive real part,
and define S[G]=0 on (−1,0].

### Proposition 2.1

S[G] is finite, continuous and subharmonic on D; harmonic off the slit;
0≤S[G]≤P[G]; and it has radial boundary trace G almost everywhere.

Proof. Reflection invariance of the Poisson kernel gives
h(−conj w)=−h(w), hence h=0 on the imaginary diameter. Pairing the two
semicircles in its Poisson integral gives, for Re w>0,

h(w)=(1/(4π))∫_{−π}^{π} [P_w(e^{it/2})−P_w(−e^{−it/2})] G(e^{it}) dt,

where P_w(ξ)=(1−|w|²)/|ξ−w|². If ξ=e^{it/2}, then

|−conj ξ−w|²−|ξ−w|²=4 Re w Re ξ≥0.

The bracket is nonnegative. It is positive when Re w>0 and −π<t<π,
so h≥0 on the right half-disk. As an ordinary harmonic function on the
full w-disk, h is smooth there and h(0)=0. Thus h(w)=O(|w|) near 0.
The zero extension S[G] is consequently continuous across the slit, including
its tip 0. It is locally harmonic off the slit. At every slit point its value
is zero while it is nonnegative everywhere, so it satisfies the local submean
inequality there. These facts prove subharmonicity on all of D.

For the majorization, put Q(ξ)=G(ξ²) on the full w-circle. The elementary
Poisson-composition identity P[Q](w)=P[G](w²) follows first from Fourier
polynomials and then by L1 approximation (the Poisson kernels are bounded
at each fixed interior point). On the right semicircle g=Q; on the left
g≤0≤Q. Hence h≤P[Q]. Substituting w=√z proves S[G]≤P[G], and the bound
holds on the slit as well.

The a.e. radial limit theorem for the disk Poisson integral, followed by the
angle change t↦t/2, proves the asserted trace. The slit endpoint is only one
exceptional angle. This proves the proposition. ∎

### Corollary 2.2: nonemptiness and explicit lower bounds

For arbitrary real F∈L1(T),

u_F(z)=S[F+](z)−P[F−](z)

belongs to A_F. On the slit it is −P[F−]≤0; all other properties follow from
Proposition 2.1. In particular, A_F is nonempty and its pointwise supremum is
finite, bounded above by H.

For a unit complex number η, apply the same construction to
G_η(ξ)=F+(ηξ), and put

u_{F,η}(z)=S[G_η](conj η z)−P[F−](z).

Its slit is {−rη:0≤r<1}. Hence, with M_F(z)=sup_{u∈A_F}u(z),

sup_{|η|=1}u_{F,η}(z) ≤ M_F(z) ≤ H(z).

These are competitor bounds, not a proof that radial slits are optimal for
nonconstant F.

## 3. Weak a.e. boundary trace alone gives no finite answer away from 0

### Proposition 3.1

For every real F∈L1(T) and every z0≠0 in D,

sup_{u∈W_F}u(z0)=+∞.

Proof. Set r0=|z0|, η=z0/r0, and use u_{F,η} from Corollary 2.2.
For A>0 define

d_η(z)=P_z(η)−P_z(−η),   u_A(z)=u_{F,η}(z)+A d_η(z).

The dipole d_η is harmonic in D and has radial limit zero except at the two
boundary atoms ±η. On the negative η-radius,

d_η(−rη)=−4r/(1−r²)<0.

Thus u_A(−rη)≤0 for every r and u_A∈W_F. At z0,

d_η(z0)=4r0/(1−r0²)>0,

so u_A(z0) tends to infinity with A. ∎

This is a boundary-class warning, not a resolution of a majorized version of
the source problem. At z0=0 continuity still gives the upper bound zero;
no formula for the center supremum for all signed F is asserted here.

## 4. Nonpositive mean: a complete solution within A_F

### Proposition 4.1

If m≤0, then M_F(z0)=P[F](z0) at every z0∈D. The unique maximizer at any
one prescribed point is u=P[F].

Proof. The harmonic function H has circle average m on every centered circle,
so its minimum there is at most m≤0. Its standard a.e. radial trace is F.
Thus H∈A_F. The majorization condition gives u(z0)≤H(z0) for every competitor.
If equality holds at one interior point, u−H is a subharmonic function bounded
above by zero with an interior maximum; the strong maximum principle gives
u−H≡0. ∎

## 5. Positive constant data: sharp solution within A_c

Write b(r)=(4/π) arctan√r for 0≤r<1.

### Projection input (credited classical theorem)

For a compact set K in the closed disk of radius R and a starting point a
with −R<a<0, the probability of hitting K before disk exit is at least the
corresponding probability of hitting its circular projection
K*={|z|:z∈K} on the positive radius, starting at a. This is the R1=0 case of
Øksendal, “Projection estimates for harmonic measure,” Theorem 1, printed
p.192. No connectedness hypothesis is imposed on K. Rotating K and the
starting point gives the comparison from an arbitrary starting point.
If K contains boundary points, including them in the stopping set is harmless.

### Lemma 5.1: a bounded-disk estimate

Suppose u is continuous and subharmonic on a neighborhood of the closed disk
of radius R, u≤C there with C>0, and every centered circle of radius at most
R contains a point at which u≤0. Then for |z|<R,

u(z)≤C b(|z|/R).

Proof. The conclusion is immediate if u(z)≤0. Otherwise let
K={w:|w|≤R, u(w)≤0}. This is compact. Continuity at 0 and the circle condition
imply 0∈K, and K*=[0,R]. Stop Brownian motion started at z upon first hitting
K or the outer circle. The stopped subharmonic process is bounded because
u is continuous on the closed disk. The submartingale inequality therefore
gives

u(z)≤C Pr_z(exit the disk before hitting K).

The projection theorem bounds this escape probability by that in the disk
slit along [0,R], with starting point −|z|. After rotation and scaling, it
is the harmonic measure of the outer circumference in D\(−1,0], at |z|/R.
The square root maps this domain to the right half-disk. The harmonic
function equal to 1 on the semicircle and 0 on the imaginary diameter is

h_1(w)=(4/π) Re arctan w.

It is bounded between 0 and 1 and has those boundary values away from the
two corners. Evaluation at w=√(|z|/R) gives b(|z|/R). ∎

### Theorem 5.2

For c>0 and z0∈D,

M_c(z0)=c b(|z0|).

Proof. Every u∈A_c is bounded above by c. For |z0|<R<1, Lemma 5.1 gives
u(z0)≤c b(|z0|/R). Let R↑1. Conversely,

v(z)=c S[1](z)=(4c/π) Re arctan√z

on the slit disk, extended by zero on (−1,0], is in A_c by Proposition 2.1.
If z0≠0 rotate its slit to lie opposite z0. This gives v(z0)=c b(|z0|).
At z0=0 its value is zero, which is the upper bound already proved.
The theorem makes no uniqueness claim for constant-data maximizers. ∎

This is a classical projection-theorem consequence. No novelty or priority
claim is made for this special case.

### Corollary 5.3: a general-data upper bound

For z≠0, let H=P[F], and for |z|<R<1 set
C_R=max(0,max_{|w|=R}H(w)). Then

M_F(z)≤min(H(z), inf_{|z|<R<1} C_R b(|z|/R)).

Indeed H≤C_R on the closed R-disk by the maximum principle, and u≤H. Apply
Lemma 5.1 if C_R>0. If C_R=0, u≤0 already. This bound is not claimed sharp
for general F.

## 6. Exact obstructions to tempting shortcuts

### Proposition 6.1: nonconvexity and failure of maximum closure

For c>0, take two constant-data slit extremizers with different slit directions.
Each is nonnegative and has as its zero set precisely its own slit. On any
circle of positive radius their zeros are disjoint. Their arithmetic mean
is therefore strictly positive everywhere on that circle, as is their
pointwise maximum. Both violate the circle-minimum condition.
Thus A_c is neither convex nor closed under pointwise maxima. Ordinary
Perron-envelope arguments cannot simply assume either closure property.

In fact its pointwise supremum is the radial function c b(|z|), by Theorem 5.2.
That supremum is positive on every circle of positive radius and is itself
infeasible. A pointwise extremal value need not be represented by a single
function simultaneously extremal at all points.

### Proposition 6.2: finite radial sampling cannot certify feasibility

Fix finitely many sample radii r_j∈(0,1), choose a∈[max r_j,1), and let c>0.
The smooth function

q_a(z)=c (|z|²−a²)/(1−a²)

is subharmonic, bounded above by c in D, and has boundary value c everywhere.
It is nonpositive on every sampled circle. But it is positive on every circle
with a<r<1. Its Laplacian is 4c/(1−a²)>0. Thus even all-angular checking at
any finite collection of radii cannot certify the continuum constraint.

## 7. What remains unresolved

The packet does not find the sharp value or all optimizers for arbitrary
positive-mean, nonconstant F in A_F. It does not prove equivalence between
A_F and any particular intended class in the printed problem. It does not
remove interior continuity from the positive-constant proof. It does not
establish historical novelty or current literature completeness.

The historical run was reported as five attempted approaches with the general
target unresolved. Its missing proof bytes, reported check count, and
interrupted review are not evidence validating this new packet. This packet
requires a fresh independent proof audit against its own manifest.

## References and inspection scope

1. W. K. Hayman and E. F. Lingham, Research Problems in Function Theory
   (New Edition), arXiv:1809.07200v2, printed p.65, Problem/Update 3.14.
   https://arxiv.org/pdf/1809.07200v2 . The complete entry and adjacent context
   were read; PDF page 66 was visually inspected. The 2018 update reports
   no progress to the authors; this is not a claim about the literature in 2026.
2. B. Øksendal, Projection estimates for harmonic measure, Arkiv för Matematik
   21 (1983), 191–203, Theorem 1 at p.192 and its proof through p.193.
   https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7393-11512_2006_Article_BF02384309.pdf .
   The theorem statement was visually inspected; the proof was read in extracted
   text. Only its planar compact-set projection theorem is used.
3. G. F. Lawler, harmonic-measure lecture notes, Section 7.1.
   https://www.math.uchicago.edu/~lawler/harmonicpaper.pdf . Its connected-set
   formulation was inspected as a cross-check but is not used for the
   potentially disconnected contact set in Lemma 5.1.

No source PDFs, extracted source text, screenshots, dataset contents, or private
coordination records are included in this authored packet.
