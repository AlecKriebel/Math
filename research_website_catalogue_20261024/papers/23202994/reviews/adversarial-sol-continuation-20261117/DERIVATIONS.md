# Row 190: adversarial reconstruction and pressure tests

Continuation, 2026-11-17. This is a mathematical source review, not a formal
proof check. The separate INITIAL remains the record of the original-first
attempt. Packaged opinions were exposed only after that INITIAL was frozen.
Here their favorable conclusions are hypotheses to test against actual proof
bodies. No other review family or current root findings were consulted.

## Exact target and dependency

Fix a real exponent s>2 throughout each limit. Put b=√3/2,
Λ=b^(-1/2){(j+k/2,kb):j,k∈Z}, and Z_s=Σ_(v≠0)|v|^(-s).
The determinant is b^(-1)b=1. Finite energies count ordered pairs and
assign +∞ to collisions. With a_N=N^(-1-s/2) E_s([0,1]^2,N), the target is
a_N→Z_s. Its second assertion is E_s(M,N)~Z_s A^(-s/2)N^(1+s/2) for each
fixed smooth compact embedded 2-manifold M of positive ordinary area A,
possibly with smooth boundary, using ambient Euclidean distance.

The imported input U compares every locally finite set C of centered-disk
density one with Λ, for the lower ordered-pair disk energy per particle and
every nonnegative smooth completely monotone function of squared distance.
For g(t)=t^(-s/2), (-1)^r g^(r)(t)=(s/2)_r t^(-s/2-r)>0. No factor of two,
no exponent s in place of s/2, and no per-area normalization is introduced.
Only the square-periodic instance of U is needed for this note. The proof of
U remains attributed to OpenAI at the exact saved pin; this review does not
claim an independent discovery of it.

## Finite bridge reconstructed without a uniform separation premise

For q distinct f_i in [0,L)^2, the motif C=F+LZ² has unique representations.
Its i-th outgoing row h_i is finite: for m=||k||∞≥2,
|f_i-f_j-Lk|≥L(m-1)≥Lm/2, and there are 8m translations. Thus the tail is
at most 8q(2/L)^s Σ_(m≥2)m^(1-s). This uses exactly s>2.

Side-L cells centered at f_i+Lk give
π(R-d)^2/L²≤n_i(R)≤π(R+d)^2/L², d=L√2/2. Hence n_i(R)/n_C(R)→1/q.
For a fixed outgoing displacement cutoff T, nonnegativity gives
Σ_i n_i(R-T)h_i^(T)≤S_R≤Σ_i n_i(R)h_i. First R→∞, then T→∞ proves
S_R/n_C(R)→q^(-1)Σ_i h_i. A finite motif may have arbitrarily close pairs:
its finitely many short denominators are positive, and no bound uniform in
the motif is needed for this fixed-configuration identity.

For N distinct x_i in the closed unit square take y_i=√N x_i and
L=(1+ε)√N, ε>0. For a nonzero translation with sup norm m,
|y_i-y_j-Lk|≥√N[(1+ε)m-1]≥ε√N m. The inter-cell outgoing energy per particle,
including i=j at nonzero translations, is therefore at most
I_(N,ε)≤8 ε^(-s) ζ_R(s-1) N^(1-s/2).
The within-cell part is precisely the finite normalized ordered energy.
The density is (1+ε)^(-2). Compress lengths by (1+ε)^(-1), giving density
one and multiplying per-particle energy by (1+ε)^s. Applying U to this one
fixed infinite configuration yields

a_N≥(1+ε)^(-s)Z_s−8 ε^(-s)ζ_R(s-1)N^(1-s/2).

The legal order is: disk radius→∞ at fixed N,ε; N→∞ at fixed ε; then ε↓0.
There is no uniform averaging assertion for the family of motifs. Setting
ε=0 would cause identifications of opposite boundary points and is not used.

For a fundamental parallelogram P⊂[-D,D]² of area one, the cells meeting
[D,t-D]² have representatives in [0,t]². Thus #Λ∩[0,t]²≥(t-2D)². Taking
t=√N+2D supplies at least N sites; any exact-N subset has each outgoing row
bounded by Z_s. Rescaling into the unit square proves
a_N≤Z_s(1+2D/√N)^s. This upper bound does not use U. An exact crop count is
unnecessary, and removing sites cannot increase the positive energy.

## Main imported proof: analytic interfaces actually checked

Read the actual pinned main TeX, macros, sections 1–7, and the scalar
appendix through its complete nonmatrix scalar route. Later field-energy
and conditional floor-matrix appendices are not premises of the positive
energy theorem consumed here. Read the actual numeric, scalar, and input
binding programs completely; none was executed in this continuation.

The sine product uses nodes 12Z+{0,1,3,4,7,9}. The squared-radius coordinate
b|x|² contains every triangular shell. For determinant-one basis M,
M^(-T)=JMJ^(-1), so A*=JA and radial direct/dual contacts have identical radii.
In the cardinal formula P(s)[C+Σ(c_n/(s-n)²+d_n/(s-n))], cancellation uses
both P(n)=0 and P'(n)=0. Integrating the exponential differences gives finite
spectral measures with variation ≤25|C|+36Σ(|c_n|+|d_n|), independent of n.
This uniformity, rather than an unmentioned weighted coefficient norm,
justifies all entire derivatives and Schwartz seminorms after Gaussian damping.

The actual complex Gaussian parameter is γ=b(h-it), Re γ=bh>0. Its
dimension-two transform is γ^(-1)e^(-π|ξ|²/γ). Substitution gives exactly
λ=i/[b(t+ih)] and z=-B/(t+ih)-ih, B=b^(-2). The transformed real part is
uniformly positive on the compact frequency interval. Fourier involution is
applied to actual radial Schwartz functions, not to a composition of folded
contour profiles. The source explicitly makes this distinction.

The Fejér rule is exact to degree 383 and has positive weights summing to one.
The analytic density integrands are bounded by 10^83 on disks twice the real
interval radius; uniformity includes every scaled derivative order. Cauchy's
tail, applied to both positive functionals, gives 4·10^83·2^(-384)<10^(-31).
Consequently the finite arrays approximate the exact integrals with a proved
error; finite spatial samples are not substituted for the integrals.

The full positive-node operator norm can be 4000. The proof does not require
it to be a contraction. Its finite paired block has inverse norm <40, while
all distant outputs have norm δ=1.1·10^(-14). The tail Schur complement is
within δ(1+40·4000)=1.760011·10^(-9)<1 of identity on the full unweighted ℓ¹
space. Reference residuals include dropped target jets, quadrature error,
and D^512, rather than just a finite fit. Their finite and tail bounds give
a full-list correction <2·10^(-8), with unchanged extra coordinates.

Near nodes, the proof deletes each value and slope before estimating the
quotient. Exact corrected slack jets then permit multiplication by (s-m)².
The error allowances .00011+.000001+.000001 are below the Bernstein margin
.001; the parameter boxes contain the whole Gaussian-data curve, including
unbounded k. In particular the last box uses fixed left endpoint K=6 for
target Taylor bounds. At the tail, the low rational piece is >.002 and the
remaining function has genuine double zeros and second derivative <.0002.
Log-concavity of P(s)/(s-m)² supplies P≥.68(s-m)². The resulting comparison
.68·.002>.0001 closes all later gaps. This uses the full infinite correction.

The main finite-array inequalities have been inspected in the formulas and
programs; their author-run records are secondary execution evidence only.
This continuation's own single execution checks the separate atomic route.

## Atomic proof and the fresh native route

The entire actual 2473-line atomic TeX and 389-line checker were read. Its
periodic residues modulo 36 omit the artificial node 24 used by the main
route, and h=.34,H=.54 distinguish the constructions. The rational tail
columns have a node-uniform spectral variation bound <119. The finite
csc²/cot columns are Laurent polynomials; folding counts the zero atom once
and positive atoms twice. The complex Gaussian prefactor and the divided
Fourier waves were checked against the same genuine transform identity.

In particular, the periodic finite columns repeat their jets at n+36l. After
dividing by the tail damping, their coefficient contribution is
e^(-πηm)(c_n,d_n−πηc_n). It is an own-side contribution and is subtracted
in both sum and difference systems. The n=0 fixed column is included. This
term is not silently omitted from the tail. There is no analogous repetition
for a single-pole rational column.

For X=B/(k²+t²), the absolute jet envelope has logarithmic derivative in X
at most 1/X−πkn. The elementary inequality
(k²+25/36)/B<3k<πkn holds for k=h,H and n≥1. Hence the right frequency
endpoint bounds each whole continuous tail interval. Periodic Q_n,D_n and
the complete initial tail period [25,61) give the geometric denominator
1−e^(-36E_b). All denominators are positive. This is analytic continuum
coverage, not inferred from the finitely many frequency values in the checker.

Write Bop for tail-to-finite, D for tail-to-tail, A for repetitions and C
for finite-to-tail transform. The proved bounds are ||Bop||<340,
||D||<3·10^(-8), ||C||+||A||<β=3·10^(-10). Finite inverses have bounds
N_+=17,N_-=5. The exact tail Schur operator differs from identity by less than
3·10^(-8)+340βN_±. At N_+=17 this is .000001764; at N_-=5 it is .00000054.
Both are strictly below one. The full ℓ¹ inverse therefore exists. This is
the needed infinite argument; a finite inverse alone would be insufficient.

The fixed constants cancel in the plus residual, and their difference is
.012 in the minus residual. With d=8.2·10^(-8),
d'_+=10^(-26)+6β, d'_-=d'_++ .012·1.3·10^(-7), the errors satisfy
t_±≤(d'_±+βN_±d)/(1−3·10^(-8)−340βN_±),
u_±≤N_±(d+340t_±). Averaging the two sides gives individual tail error
<3·10^(-9) and finite error <10^(-5). Requiring each plus/minus bound to
meet the individual bound would be the wrong test; the source uses the average.

For tail curvature, logarithmic differentiation gives the upper derivative
3/(2X)−πhs. Since 3(h²+25/36)/(2B)<3h<πh, the right endpoint is maximal for
s≥1, whereas t=0 is maximal at s=0. Thus the endpoint envelope comparisons
propagate over every frequency, and damping makes them uniform for larger s.
The deleted Taylor remainder after degree20 starts at derivative23 and uses
ratio |y|d/24<1. The checker and text agree on these indices.

On the first right half-cell the Gaussian rational lower bound cannot be
replaced by zero. Multiplying by v²+4zv+6z²>0 gives a cubic in z/Z. Its four
Bernstein coefficients are the four exceptional tests, the first carrying a
factor v. At v=0 it may vanish, but actual z>0 gives weight to the other
positive coefficients. The containing polytope varies its first coordinate
z independently; no affine interpolation of the physical exponential curve
is asserted. The ≤.003 error decreases every relevant coefficient by at most
.003·3.5, below the supplied margins. This treats z→0 without ever taking
the singular value z=0 as a physical Gaussian.

For the far signs remove only the direct constant ±.006P, keeping its
transform in the curvature estimate. The remaining curvature allowances are
3.01·.00465+800·3·10^(-9)+.006·.002=.0140109<.018 on [14.5,23], and
3.01·.000023+800·3·10^(-9)+.006·.002=.00008363<.000324 later.
The sine-product barriers are respectively 3 and .054 times squared
distance to the chosen nearest node. At the junctions choose node16 at14.5
and21 at23; the whole joining segment stays within the region where its
curvature bound holds. Exact jets settle the node itself. Thus no final
unbounded radius interval is left to extrapolation from finite tests.

Native execution: the exact README command python3 -I
verification/check_certificate.py was run once in a fresh local copy, with
assertions enabled and no installs, modifications, or retries. The input
tree's four files and two child directories were fully guarded before and
after. Exit0, empty literal streams, 3.228441457991721 seconds. The code
implements outward integer intervals, zero-excluding reciprocal operations,
integer-square-root enclosures, complex rectangles and a proved exponential
Taylor allowance. Gauss–Jordan may reset entries to 0/1 only when algebraic
elimination identities establish those exact values. All pivots are checked.
Its 659 Bernstein row minima, parameter polytope, and finite envelopes cover
the stated finite certificate, not the analytic steps just reconstructed.

## Density and positive mixtures: independent logical checks

The main positive Fourier form compares μ_R=Σ_(x∈C_R)δ_x with area measure on
B_((1+ε)R). Its cross error is ≤N_R∫_(|z|≥εR)|f(z)|dz=o(N_R), uniformly in
all point positions. The area self-term divided by its area tends to ∫f by
overlap dominated convergence. Cauchy–Schwarz gives the diagonal-included
bound (1+ε)^(-2)fhat(0); then ε↓0 and subtraction of exactly N_R f(0)
yield the needed ordered bound. This survives arbitrarily large local
clusters. The atomic Fourier-cutoff proof instead uses |M_R|≤N_R, a
Schwartz cutoff tail, Plancherel, and N_R~πR²; it has the same density scope.

For α<1, put β=1/α. The complement
f_α=G_α−β fhat_β has transform β(G_β−f_β)≥0 and slack β fhat_β≥0.
Radiality and A*=JA exchange the contact sets. The factor is β in dimension
two, not β^(1/2). Poisson summation is applied only to the lattice and only
after Schwartz decay has been established.

The main shifted-moment proof keeps total measure mass g(ε), handles v=0
and v=1, and chooses its weak subsequence before the real exponent. Its
uniform power estimate |v^(t_n)−v^t|≤(t_n−t)/(et) is valid for t>0.
For every arbitrary radius sequence, Fatou is applied to nonnegative
normalized Gaussian sums, then Tonelli sums the lattice. At v=1 the finite
sum is N_R−1→∞; v=0 gives0. Finally g≥g(ε+·), and monotone convergence
removes ε only on the lattice side. No interchange with the configuration
liminf is needed. The atomic Laplace construction gives a second proof,
with locally finite measures whose Laplace tails obey Ce^(-sT/2); it also
preserves the constant-potential atom. Neither proof requires a measurable
choice of Gaussian auxiliary functions.

## Corrected Hardin–Saff interface, including the real auxiliary pitfall

The actual retrieved math-ph/0311024v3 PDF matches its deposited SHA256 and
has the four-page addendum headed November23,2018 followed by the original
paper; the arXiv version banner says15Dec2004. These are distinct metadata,
not evidence of a2018 first disclosure. Definition(19), Theorem2.4, its proof,
the relevant union lemmas, and the complete hypersingular addendum argument
were inspected. The threshold is s>d. Its additional smooth manifold
without-boundary condition belongs to s=d and is not imported here.

The source's unrestricted neighborhood lemma is false for unbounded G:
in R² adjoin to a fixed positive-area compact K tiny open balls centered at
2^(2^n)e_1, with total area <δ. Choosing any fixed finite number of centers
arbitrarily far out makes all mutual distances arbitrarily large, so the
infimum finite energy is0 despite the claimed positive lower bound from K.
The proof's assertion dist(clG,Atilde\V)>0 also requires compactness.
This is an explicit boundary counterexample to the unrestricted auxiliary
wording, not to the theorem as used by the reviewed note.

The note expressly restricts its use to a compact regular thickening, so the
counterexample does not enter the retained chain. To check that restriction:
cover every compact parameter piece by finitely many closed cubes inside its
open bi-Lipschitz domain, and take their image union Atilde. It is compact.
For a component containing the center, the image of the cube's intersection
with a preimage ball gives a uniform lower area bound cr², including corners.
For the upper bound sum finitely many image bounds; a component intersecting
the ambient r-ball is contained in a 2r-ball about one of its own points.
Finite union and finitely many Lipschitz constants give uniform regularity.
Every relative neighborhood closure is then compact, so its distance from
the complementary closed set is positive.

In that compact setting, choose k above the LIMSUP energy of K. Monotonicity
gives an eventual upper bound kN^(1+s/d) for the larger closure. Deleting
points with nearest distance <ρN^(-1/d) loses ≤kρ^sN points; disjoint regular
balls for good points farther than νρN^(-1/d) from K lose at most
2δN/[c0(νρ)^d]. Moving retained points into K changes each distance by at most
2ν times the original and preserves distinctness. Hence

g_under(G)≥(1−2ν)^s[1−kρ^s−2δ/(c0(νρ)^d)]_+^(1+s/d) g_under(K).

Set ρ=ν=δ^(1/(4d)): every loss tends to0. Closure and open-set infima agree
by approximating a fixed distinct finite configuration through the dense
open set. Smooth boundary charts extend locally into an open parameter ball;
if Dφ stays within half the smallest singular value of Dφ(0), integration
along straight segments gives a lower Lipschitz bound as well as an upper
one. Compact half-chart pieces therefore satisfy definition(19). This
justifies boundary and chart interfaces without requiring a closed surface.

## Boundary, finite-size, and quantifier attacks

* N=1 has zero within-cell energy, but periodization still has nonzero
  self-image rows. Omitting those rows would invalidate the inequality.
* Finite N is not asserted to obey a_N≥Z_s. At N=2 opposite square corners
  yield a_2≤2^(-s), far below the limiting constant. This does not contradict
  a leading asymptotic with an explicit finite gap error.
* At s=2 the shell sum diverges and N^(1-s/2) ceases to decay. The theorem
  does not include s=2 or a joint s→2,N→∞ limit. For large fixed s the gap
  constants can grow rapidly; no uniform large-s rate is claimed.
* The six nearest lattice vectors have length b^(-1/2), so
  Z_s≥6b^(s/2). The squared-distance normalization and scaling match this
  six-neighbor check. Rescaling a surface by λ multiplies both the asserted
  coefficient A^(-s/2) and the exact energy by λ^(-s).
* Arbitrarily close motif pairs are allowed: the inter-cell estimate is
  uniform while the fixed motif's own finite rows need not be small.
* Centered density is sufficient for the LP step. Translation invariance of
  the energy for arbitrary highly clustered nonperiodic sets is not silently
  assumed. The periodic row formula itself works for every motif translate.
* A fixed disconnected compact surface has finitely many components, and
  distinct components have positive separation. Its cross-energy is O(N²),
  lower order because s>2. Minimizing Σ A_i^(-s/2)N_i^(1+s/2) allocates
  N_i/N→A_i/ΣA_i and gives total area. No assertion is made for a sequence
  of surfaces with separation shrinking with N.
* Empty sets, collapsed sets, positive-area nonsmooth sets outside the chart
  class, intrinsic distances, uniqueness, microscopic crystallization, and
  subleading terms are outside the target. The stated positive area and
  fixed smooth embedded surface hypotheses remove those degenerate attacks.

## Result of this family

The original finite bridge and upper crop survive the attacks above. The
complete atomic analytic route plus its freshly reproduced exact finite
certificate supplies the imported U with the required measure, density,
dimension, and pair conventions. The main positive-energy route was also
read in its needed proof bodies; its finite execution was not rerun here.
The corrected compact application of Hardin–Saff supplies the stated surface
transfer. No material unresolved gap in the retained target chain was found.
The unrestricted auxiliary lemma pitfall is explicitly avoided in the
original note and is recorded above so it cannot be silently generalized.

Strongest supported claim: the exact fixed-s>2 square constant and its stated
ambient-distance compact-surface consequence as an attributed corollary of
the pinned imported theorem and corrected classical theorem. This is neither
a new independent proof of universal optimality nor a claim of formal
verification or first priority. A full Lean/Comparator/axiom run and a fresh
main Arb run were not performed. No repair or extension was attempted.
The root controls final disposition and publication. follow_up: null.
