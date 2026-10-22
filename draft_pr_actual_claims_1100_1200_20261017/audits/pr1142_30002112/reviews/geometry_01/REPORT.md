# Independent adversarial geometry review of PR 1142

**Verdict: PASS for the assigned geometric existence mechanism.** No material
mathematical defect was found, and no repair is required in that mechanism.
This is a review of the exact supplied proof bytes, not a claim of formal
verification, historical originality, or an independent rereading of the
original Oberwolfach problem. The complete negative conclusion also depends
on the other scope and spectral-counting checks outside this assignment.

Target: problem 30002112 / OWR-12005-004; assigned PR head
`c29139d2c2a98f1a0284d0dc794c88f51c680a0c`. The head identifier comes from the
assignment, not a checkout/GitHub query. Independently verified base
PROOF.md: 10,412 bytes, SHA-256
`c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658`.

## Exact claim and falsification criteria

The claim reviewed is: for every fixed integer m >= 2 and all S,L,r > 0,
there exists a smooth compact connected closed hypersurface H embedded in
the open ball B(0,r) in R^(m+1), with area **exactly** S and intrinsic first
positive Laplace-Beltrami eigenvalue greater than L. The closedness condition
is made explicit here because it is needed for the cavity application and
is delivered by the construction.

The review sought a failure in at least one of these points: unrestricted
normalized gap in the needed embedding dimension; connected/closed or
orientable topology; embedding versus immersion; the C0 approximation
quantifier; strict shortness; global injectivity after smoothing; spectral
min-max domains; exact area restoration; a simultaneous ball/gap tolerance;
or a hidden uniformity assumption as m, topology, S, L, r, or q vary.

The mechanism is mathematical existence from established theorems, not an
empirical model. Its checkable artifacts are the universal arguments below,
the frozen independent core, exact source pins, and narrowly scoped exact
algebra diagnostics. No finite computation is evidence for the existence
of a Nash embedding.

## Independence, exposure, and source scope

The route and intended negative claim were disclosed in the task. I did not
independently discover the route. I first read the whole supplied PROOF.md
and SOURCE_DEPENDENCIES.json, then freshly obtained the primary PDFs and
checked the requested statements. Before reading any old audit, acceptance,
status, root report, or concurrent report, I wrote INDEPENDENT_CORE.md at
2026-10-17 23:15:30 UTC. Its SHA-256 is
`6c925b47634c36d8ab3092884456d98a227b2eb9c8907d30ff2327b9a766203d`.
Those other audit/report contents remain unread throughout this review.

A directory inventory exposed their filenames. The base proof itself says
an old internal audit accepted it, and the dependency JSON records old
inspection limits. Those statements were visible but were not mathematical
evidence or adopted conclusions. READ_RECEIPT.json records every nonself
semantic read and all own artifact pins. It excludes its own hash; the
receipt digest is transmitted separately to the parent.

The two decisive primary statements were verified as follows. CDE Theorem
1.4 supplies connected closed embedded examples with unbounded normalized
gap; its second part allows S^m in codimension one for m >= 3, while its
surface part allows varying orientable topology. Full Section 5 verifies the
intended C1-to-smooth route. DLS Theorem 1.2 supplies arbitrary C0 accuracy
in every ambient dimension N >= m+1, and explicitly retains embedding when
starting with an embedding. These statements match the actual uses.

I inspected CDE's connected/closed/indexing convention on printed p. 1,
Theorem 1.4 on p. 6, and all of Section 5 on pp. 14-15. I inspected DLS's
shortness definition and Theorem 1.2 with immediate context on pp. 2-4.
Rendered CDE pp. 6, 14, 15 and DLS p. 4 were visually checked, resolving
the relevant arrows, powers, regularity, and embedding clause. The rest of
the papers was not comprehensively audited. In particular, original
Colbois-Dodziuk, Buser-Burger-Dodziuk, Nash, Kuiper, and Hirsch texts were
not separately retrieved or reproved. The generalized smooth
Jordan-Brouwer separation theorem is a named standard input. The smoothing
step is also justified directly below rather than relying only on the
unretrieved Hirsch reference.

## Universal argument and attempted attacks

### 1. The starting metric exists in every stated dimension

Use the first positive eigenvalue, denoted lambda below to avoid an index
convention mismatch. For the given S and L, CDE provides an abstract smooth
connected closed manifold M, a smooth hypersurface embedding of M, and a
smooth metric g0 with

    lambda(g0) * area(g0)^(2/m) > 2 L S^(2/m).

One may simply use the induced smooth metric of a supplied CDE example;
there is no need to independently infer an additional intrinsic existence
theorem. Put g = b^2 g0, b = (S/area(g0))^(1/m). The exact scaling identities
are area(g)=b^m area(g0)=S and lambda(g)=b^-2 lambda(g0)>2L.

For m=2 the genus is allowed to change with the target. No fixed-genus
unbounded-gap assertion is used. In particular, the argument does not
interpret the source's hyperbolic surface discussion as an assertion that
unscaled hyperbolic lambda itself tends to infinity. For m>=3 choose the
underlying manifold to be S^m, which has the required smooth hypersurface
embedding. There is no nonorientable closed hypersurface obstruction in
either case. Constants and smoothing tolerances need only work for this
one target at a time.

### 2. Strict shortness and the small-ball condition are simultaneous

Let e0:M->R^(m+1) be any smooth embedding supplied by the choice of M.
On the compact g-unit tangent bundle define

    K = max |de0(v)|^2,   R = max_M |e0|.

These are finite and K>0. Choose t>0 with t^2 K<1 and tR<r/8. The map
e=t e0 is a smooth embedding, its pullback metric is strictly less than g,
and its image is inside B(0,r/8). Thus no short-map existence problem has
been substituted for the original problem. Apply the precise DLS theorem
with N=m+1 and uniform error less than r/8. It gives a C1 **embedding** f
with f^*g_Eucl=g and f(M) inside B(0,r/4).

An immersion-only theorem would not suffice; that is not the cited theorem.
Likewise, mere existence of some C1 isometric embedding with uncontrolled
position would not suffice; the cited uniform approximation conclusion is
exactly what supplies ball containment. The argument uses the combined
Nash-Kuiper result, including Kuiper's codimension-one case, rather than
claiming Nash's original codimension-two result alone proves this step.

### 3. Smoothing retains both immersion and global injectivity

For completeness, smooth C1 approximation can be obtained componentwise:
choose a finite smooth partition of unity subordinate to precompact
coordinate charts; extend the compactly supported chart pieces of each
coordinate of f by zero; convolve with smooth approximate identities; pull
back and sum. For sufficiently small convolution radii these are globally
defined smooth maps f_j converging to f in C1.

That approximation alone would not imply embedding without a stability
argument. Near p, select a linear projection P:R^(m+1)->R^m such that
D(Pf)(p)=A is invertible. Shrink a convex coordinate ball until
||A^-1 D(Pf)-Id||<1/4. For all sufficiently C1-close F, the same norm for
PF is less than 1/2. Integration along straight coordinate segments then
gives

    |A^-1(PF(x)-PF(y))| >= |x-y|/2.

This proves local injectivity and full differential rank on that ball.
Take finitely many smaller balls covering M. A Lebesgue number gives a
distance delta>0 so every sufficiently near pair lies in one such chart.
On the compact set of pairs separated by at least delta, injectivity of f
gives a positive minimum eta of |f(x)-f(y)|. A perturbation with
||F-f||_C0 < eta/3 retains separation on those pairs. Combining these two
arguments proves that all sufficiently C1-close f_j are embeddings, not
just immersions. Compactness then makes the image an embedded closed
hypersurface.

Uniform first-derivative convergence also yields

    h_j = f_j^*g_Eucl -> f^*g_Eucl = g

uniformly as quadratic forms on the same smooth abstract manifold. No
second derivative, curvature, or uniform lower reach bound is required.
The final smooth hypersurfaces can have arbitrarily large curvature.

### 4. Metric comparison legitimately controls the spectral gap

Suppose c>=1 and c^-1 g<=h<=c g. The eigenvalues of h relative to g lie
in [c^-1,c], hence the volume densities compare by c^(+/-m/2). Inverse
forms compare by the same two factors c^-1 and c. For every u in H1,

    c^(-1-m/2) E_g(u) <= E_h(u) <= c^(1+m/2) E_g(u),
    c^(-m/2) ||u||_g^2 <= ||u||_h^2 <= c^(m/2) ||u||_g^2.

For nonzero u, division gives c^(-m-1) R_g(u)<=R_h(u)<=c^(m+1) R_g(u).
These conservative constants are sufficient; sharpness is not claimed.
Uniform equivalence means the full Sobolev spaces have identical elements
and equivalent norms. Apply the full-space min-max formula over subspaces
of dimension k to get the same inequalities for every numbered eigenvalue,
including zeros and multiplicities. Constants are included in those spaces.

This matters: the mean-zero condition depends on the volume measure. For
example, on a flat two-torus let h=(1+(1/2)cos x)g and u=cos x. The
g integral is zero, while the h integral divided by area(g) is 1/4. Thus one
cannot silently use the same metric-dependent mean-zero subspace for both
Rayleigh minima. The supplied proof correctly avoids this trap.

For the present application g and h_j are smooth; f need only be C1.
There is no need to assign a classical rough-image Laplace operator to
f(M). Uniform convergence h_j->g and positivity of g permit comparison
constants c_j->1. Thus their areas converge to S and their first positive
eigenvalues converge to lambda(g)>2L.

### 5. Exact area correction preserves a quantitative gap and ball margin

Let S_j=area(h_j), a_j=(S/S_j)^(1/m), and H_j=a_j f_j(M). It follows
algebraically that area(H_j)=S **exactly**, not just asymptotically. Under
the preceding comparison with g of area S,

    c^(-1/2) <= a_j <= c^(1/2),
    lambda(H_j) = a_j^-2 lambda(h_j),
    c^(-m-2) lambda(g) <= lambda(H_j) <= c^(m+2) lambda(g).

The extra factor c from area correction has been included. A fully explicit
all-dimension tolerance is available: set n=m+2 and c=1+1/(4n). Then

    c^n = sum_{k=0}^n binom(n,k)/(4n)^k
        <= sum_{k=0}^n (1/4)^k < 4/3 < 2.

Consequently any sufficiently close smooth approximant satisfying this c
has lambda(H_j)>(3/2)L. Also c<=17/16 for m>=2, so a_j<=sqrt(c)<2.
By additionally taking ||f_j-f||_C0<r/12, obtain f_j(M) inside B(0,r/3)
and H_j inside B(0,2r/3), a strict subset of B(0,r).

All these conditions are finitely many simultaneous open error bounds.
The sequence converges in C1, so a single sufficiently large j meets them
all. There is no exchange of an infinite family of limits and no need for
one smoothing index uniform over q. This supplies the precise claimed
S,L,r existence result in every fixed m>=2.

### 6. The geometry supports the cavity use

The general smooth hypersurface form of Jordan-Brouwer applies to the
connected closed embedded H, not only to a sphere. It yields a bounded
complementary component U and an unbounded component E, both with boundary
H. Every point of norm at least r reaches infinity along the exterior of
the ball without meeting H; thus U is inside B(0,r). Smoothness of H gives
a smooth boundary for U.

For the proof's r=1/2, the inner and outer boundary components are separated
by a positive distance. The complement inside the unit ball is connected:
any point of E inside radius 3/4 can follow an E-path toward infinity until
its first crossing of that sphere; that stopped path stays inside the unit
ball. All points of the annulus 1/2<|x|<1 connect within the same annulus.
Hence removing the closed bounded cavity leaves a connected smooth domain
with exactly the two indicated boundary components. Orientation has no
effect on the intrinsic scalar Laplacian. No bounding-volume lower bound
for U or geometric regularity beyond smoothness is being assumed.

## Diagnostics and reproduction

Run, from the repository root:

    python3 draft_pr_actual_claims_1100_1200_20261017/audits/pr1142_30002112/reviews/geometry_01/diagnose_geometry_constants.py
    python3 -O draft_pr_actual_claims_1100_1200_20261017/audits/pr1142_30002112/reviews/geometry_01/diagnose_geometry_constants.py

Both were run under Python 3.14.6 and exited 0. Their saved JSON outputs
are byte-identical, SHA-256
`9fdb39b60297b1066ae749181a7cb2c5f843f9f333c96f6d9a559240943aabf9`.
All failure checks use explicit require(), so optimized Python retains them.

The exact fractions diagnostics cover 620 smooth flat-torus metric pairs,
4,960 genuine Fourier-function Rayleigh comparisons, 620 combined
area-normalization eigenvalue checks, 450 finite positive-quadrature
coefficient checks, 255 rational tolerance checks for m=2,...,256, and the
explicit smooth mean-zero control example above. The quadrature data are
clearly labeled algebra models, not actual smooth metrics or numerical
spectral solutions. The transcript digest is
`f2f5e62a09de5ecb43a9d88c14e2dee3a17167a729302e02576378e1d67768a0`.

These checks found no counterexample. They are limited diagnostics for
constants and scaling; the universal proofs above supply the all-m and
all-S,L,r statements. There is no constructed numerical Nash embedding,
implementation mutation-testing claim, or attempt to infer existence from
finite examples.

## Source identities and version pins

| Source | Version/location inspected | SHA-256 of PDF |
| --- | --- | --- |
| Colbois-Dryden-El Soufi, *Bounding the eigenvalues of the Laplace-Beltrami operator on compact submanifolds* | [arXiv:0909.5346v1](https://arxiv.org/abs/0909.5346v1), submitted 2009-09-29; printed pp. 1, 6, 14-15 | `a2bc60b7f1b00009ef39ac1260ee6b9cb4a3464d3617f0f3944a9aee5fa6bb35` |
| De Lellis-Szekelyhidi, *John Nash's nonlinear iteration* | [Author-hosted PDF](https://www.math.ias.edu/delellis/sites/math.ias.edu.delellis/files/contr_vol_Nash_11.pdf), Definition 1.1/Theorem 1.2 and context; printed pp. 2-4 | `22ca78b5750848189dee869f3fc8895c0b935c4af5316450132164aba87e0ddc` |

CDE's unversioned PDF download was compared byte-for-byte with the explicit
v1 URL and is identical. Its PDF creation metadata is 2021-08-01, which is
a compilation date and is not a new arXiv version or result date. The DLS
PDF has 31 pages and metadata date 2016-05-11; no version number or original
publication date is inferred from that metadata. CDE has 17 PDF pages.
Text extraction/rendering used Poppler 26.08.0. Original files, exact text
derivatives, rendered critical pages, and their pins are retained in this
review's private sources/tmp subdirectories.

## Findings, exact gap, and disposition

Material findings: **none**. Severity/repairability: not applicable. The
strongest verified result is precisely the universal prescribed-small-ball,
exact-area, arbitrarily-large-first-positive-gap lemma, with sufficient
regularity and topology for the proposed cavity construction, conditional
only on the explicitly named established existence/topology theorems.

There is no unsupported equivalent reformulation or blocked route left
inside this mechanism. Direct reproof of the historical metric and
Nash-Kuiper theorems, a full novelty search, and the original problem-scope
gate are outside this review and are not claimed complete. Those are
inspection limits, not gaps silently filled by finite computation.

All writes are confined to geometry_01. No other shard reports were read;
no subagents, external outreach, Git mutations, PR/Zenodo/tracker writes,
or releases were performed. Completion estimate: **100% of this assigned
geometry review**, subject to the stated external theorem dependencies.
