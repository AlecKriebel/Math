# Independent geometric/topology adversary: PR57

The pinned candidate passes this family's universal mathematical audit. For
every finite integer r≥0, on each of the plane and sphere, its sequences lie in
the exact normalized source domain, have smooth complete strictly positive
curvature, converge in the metric C^r topology, and fail inverse continuity in
the source's C^{r+1} diffeomorphism topology. No mathematical counterexample or
unsupported geometric realization step was found. This is an AI audit of an
unrefereed candidate; priority remains unconfirmed.

Target: 30003354 / OWR-15208-008. Pinned original head supplied by ROOT and
authenticated by the original preparer:
`4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29`. The exact original CANDIDATE.md is
12596 bytes, SHA256
`7f358fb1aaa73dc3cfd06c798c10f6afed65ee430b622b84b90f0554dd440e62`.
All candidate locators below refer to that 204-line file in
`../original_preparation_family/original/CANDIDATE.md`.

## Independence and source scope

I previously audited PR56. For PR57 I first read the literal source_record and
candidate, followed by the official question and primary topology passages.
`INITIAL_SCOPE_AND_DERIVATION.md` records the first universal derivation at the
14:23:05 UTC checkpoint, before reading historical reviewer/checker bodies or
another fresh family's findings. None of those bodies or findings was used in
this audit. Later source-preparer authentication/accounting was read solely to
bind the pinned artifacts and distinguish the prior fields and proof budget.
That preparer's evidence is not this agent's Git authentication or ROOT custody.

The [official OWR question](https://ems.press/doi/pdf/10.4171/OWR/2017/3), printed
p.149 (private layout lines 716–738), fixes 0,1 on the plane and 0,1,∞ on the
sphere. It asks about this parametrization and expects the integer case to fail.
The workshop is dated 2017; the curated citation's parenthetical 2018 does not
alter the mathematical target.

[Banakh–Belegradek](https://arxiv.org/pdf/1510.07269), printed pp.3–4,17–20
(layout lines 90–120,149–165,707–778,815–854), uses smooth objects with
compact-open derivative topologies. The diffeomorphism factor has one more
derivative. Its plane/sphere normalized maps are continuous bijections; the
positive homeomorphism assertion concerns noninteger regularity. The
[published Belegradek–Hu erratum](https://link.springer.com/content/pdf/10.1007/s00208-015-1354-1.pdf),
printed p.711 (layout lines 23–39), corrects the earlier integer assertion to a
Hölder statement with precisely that extra derivative. Thus candidate lines
9–25 identify the correct endpoint question. It is not a claim that the spaces
admit no other homeomorphism, nor a counterexample to the C^∞/Hölder results.

Full PDFs were successfully acquired for private reading, including the full
published two-page erratum. Selected passages of the other two works were read
in extracted text and six rendered pages were inspected. Their entire proofs
and the current literature were not comprehensively audited. Receipts and
selected locators are public packet inputs; complete PDFs/text/PNGs remain
private and are not necessary for the ROOT closure helper.

## 1. Exact inverse components and admissible gauge

Consider two decompositions of the same metric, with normalized maps f and ψ.
In their conformal coordinates F=ψ∘f^{-1} pulls one scalar multiple of the
Euclidean/round metric to another. Therefore D F is conformal at every point.
Positive orientation gives the Cauchy–Riemann equations, so F is a global
orientation-preserving conformal automorphism. On the plane such an
automorphism is az+b; fixing 0 and 1 forces a=1,b=0. On the sphere it is a
Möbius transformation; fixing three distinct marked points forces identity.
The scalar factors then agree pointwise. Consequently every explicitly
constructed normalized decomposition is the actual inverse image of its metric.

The source fixes values at marked points. It imposes no derivative gauge such
as Df(0)=I. Adding that condition would change the target and would improperly
exclude the r=0 construction. Even if identity-component membership were
required, the examples satisfy it: interpolate the twist angle, or use
f_t=id+t w with ||Dw||∞<1. All these paths fix the marked points. The sphere
extension is identity on a neighborhood of infinity. Candidate lines 13,39,
48–60,89,125–129 pass these normalization and uniqueness checks.

## 2. Complete strictly positive backgrounds

For g*=e^{-2b}|dz|², curvature is e^{2b}Δb. On the plane,

    b=½log(1+|z|²),   Δb=2/(1+|z|²)²,   K=2/(1+|z|²)>0.

For an escaping curve, its length bounds the absolute variation of
asinh|z| from below, which diverges. This establishes completeness without a
hidden compactness assumption. On the sphere,

    b=log(1+|z|²)−log2,   Δb=4/(1+|z|²)²,   K=1.

This is the smooth round metric, hence complete by compactness. On either
fixed coordinate support disk Δb and K have positive minima. Strict positive
curvature means pointwise K>0; the plane example does not assert a uniform
positive global lower bound. Thus no compactness consequence of such a bound
is being invoked. These computations verify candidate lines 31–39.

## 3. The zero endpoint is a genuine global construction

Set θ_n(t)=θ₀η(log(R/t)/n), with θ₀ not a multiple of 2π and R=1/4,
and φ_n(z)=e^{iθ_n(|z|)}z. It is constant rotation for |z|≤Re^{-n}
and identity for |z|≥R, so it is smooth at 0 and at the support boundary.
Its inverse subtracts the angle at the same radius. In radial/azimuthal
orthonormal frames its differential is a rotation times

    S=[[1,0],[q,1]],   q=tθ_n'(t),   |q|≤|θ₀| ||η'||∞/n.

The radial background factor is unchanged by φ_n. Hence the relative pulled
metric is S^T S=[[1+q²,q],[q,1]], which tends uniformly to identity.
This proves compact-open C^0 convergence in every smooth coordinate chart;
the perturbation has fixed compact support and is identity near infinity.
The onto isometry φ_n preserves completeness and strict positive curvature.
The unique inverse components are (b,φ_n) on the plane and (0,φ_n) on the
sphere, while Dφ_n(0)=Rot(θ₀)≠I for all n. This is failure exactly in C^1,
with no dependence on a coordinate singularity of the polar frame: the map is
linear near 0. Candidate lines 43–60 pass in full.

## 4. Global logarithmic maps and actual metric realization, r≥1

Fix an arbitrary finite integer r≥1, ρ=e^{-n}, ε=1/n,
s=(|z|²+ρ²)^{1/2}, and w=εχz^{r+1}log s, f=id+w. Constants may depend on
r and the fixed cutoff but not on n. Direct differentiation or homogeneous
rescaling in (x,y,ρ) gives |D^j log s|≤C_j s^{-j} for j≥1.
Leibniz gives

    |D^k(z^{r+1}log s)|≤C s^{r+1-k}(1+|log s|),  0≤k≤r+1.

Since s^r(1+|log s|) is uniformly bounded on the support,
||Dw||∞≤C_r ε. In particular the inverse equation z=y−w(z) is a strict
contraction on all of R², for each y, once n is large. The inverse function
theorem and the path id+t w prove global smooth invertibility and positive
orientation. Since f is identity outside R, injectivity and surjectivity imply
f maps the disk onto itself: an interior point could not map to an exterior
point, since the latter is already its own preimage. Thus f^{-1} also equals
identity outside R. This justifies the global sphere extension and compact
support assertions; local near-identity estimates alone were not substituted
for onto realization. Candidate lines 64–89 pass.

On the inner disk,

    f_{bar z}=εz^{r+2}/(2s²),   |D^k f_{bar z}|≤C_r ε s^{r-k},  k≤r.

Cutoff terms have O(ε) derivatives on the fixed annulus. The f_z C^r norm is
bounded because its highest-order possible logarithm is canceled by εn=1,
while |f_z|≥1/2 for large n. Repeated reciprocal differentiation now gives
uniform C^r bounds for 1/f_z, so μ=f_{bar z}/f_z tends to zero in C^r.
This is the estimate in candidate lines 95–105; it does not assert smallness
of the f_z C^r norm itself.

For a real smooth compact correction a, define h=log|f_z| and

    g=e^{-2(b+a)}|dz+μdbar z|²,
    U=(b+a+h)∘f^{-1}.

The pointwise identity df=f_z(dz+μdbar z) gives, exactly,

    g=f*(e^{-2U}|dw|²).

Therefore it constructs the source-domain representation, rather than inferring
one from a formal Beltrami coefficient. The metric is positive definite with
relative eigenvalues (1±|μ|)². Bounded a and |μ|≤1/2 imply a global uniform
comparison with the complete plane background. Hence g is complete and the
conformal target is complete by the onto isometry f. Moreover U=b outside R.
In particular its logarithmic growth is α(U)=1, consistent with the plane
source's completeness/growth restriction. On the sphere u=U−b is zero outside
R and extends smoothly to infinity. Once the curvature sign below is proved,
u belongs to the precise nonnegative-curvature source set on either surface.
Candidate lines 115–129 contain no gap between estimates and realization.

At 0 the exact jet satisfies

    ∂_x^{r+1}(f−id)(0)=ε(r+1)!logρ=−(r+1)!.

Any derivative hitting log s leaves positive polynomial degree and vanishes
there. Thus the actual normalized diffeomorphism cannot approach identity in
C^{r+1}; this is not just a large unnormalized-coordinate derivative.

There is also a stronger independent function-component check. For r≥2, the
Taylor expansion at 0 is f=z−z^{r+1}+terms of degree≥r+3. Consequently
h=−(r+1)Re(z^r)+terms of degree>r, and f^{-1} has identity jet through order r.
Since the background has zero first derivative at 0, its composition changes
no jet through order r. Thus

    ∂_x^r(U−b)(0)=−(r+1)!.

For r=1, J(0)=I, Db(0)=0, Da(0)=0 for the radius correction below, and
Dh(0)=(-2,0); therefore ∂_x(U−b)(0)=−2. These exact fixed-n statements do
not require uniform Taylor remainders in n. They give failure also in the
function C^r component. This strengthening is not needed for candidate
lines 107–111, whose diffeomorphism jet already proves the theorem.

## 5. All endpoints r≥2

Set a=0. Since μ→0 in C^r and r≥2, the realized positive metrics converge
in C² on the fixed compact support. Curvature is continuous in the metric's
positive two-jet. The background's strict positive minimum on that disk
therefore proves positive curvature there for all sufficiently large n.
Outside it the metric is exactly the background. Completeness and actual
inverse identification have already been established. This verifies candidate
line 133 for each arbitrary r≥2, without a finite-r extrapolation.

## 6. Critical r=1: correct operator and uniform sign proof

The ordinary Jacobian J has target-component rows and domain-variable columns.
For v real and F=f^{-1}, direct chain rule gives

    L v=[Δ_w(v∘F)]∘f=A^{ij}v_{ij}+B^i v_i,
    A=J^{-1}J^{-T},
    B^i=−(J^{-1})_{ia}(∂_{jk}f_a)A^{jk}.

The last identity follows by twice differentiating f∘F=id and summing the
target Laplacian indices. The order of the two inverse factors matters, and B
cannot in general be dropped. Neither feature depends on f being conformal.

Put ℓ=1+|log s| on |z|≤R/2. Direct logarithmic differentiation for r=1 gives

    |J−I|≤Cε,   |D²f|≤Cεℓ,   |D³f|≤Cε/s.

For D³f the quadratic polynomial has no third derivative, so every surviving
term differentiates the logarithm. Since |f_z|≥1/2, differentiation of
log|f_z| gives

    |Dh|≤Cεℓ,
    |D²h|≤C(ε/s+ε²ℓ²)≤C'ε/s.

The final bound is uniform because sℓ² is bounded, including the shrinking
core s=ρ. Also |A−I|≤Cε, A≥I/2, and |B|≤Cεℓ. With b and its first two
derivatives bounded, these inequalities yield

    L(b+h)≥Δb−C₀ε/s.

For example the B Dh term is O(ε²ℓ²), again bounded by Cε/s; the drift on
Db is O(εℓ), bounded by Cε/s. Thus no uncontrolled core logarithm remains.

The radius Hessian has radial eigenvalue ρ²/s³ and tangential eigenvalue 1/s.
It is positive semidefinite, |Ds|≤1, and Δs≥1/s. Hence

    Ls≥1/(2s)−Cεℓ≥1/(4s)

uniformly once n is large, since sℓ is bounded. Choose one fixed K>4C₀ and
a=Kεχs. On the inner disk,

    L(b+h+a)≥Δb+(K/4−C₀)ε/s>0.

Meanwhile ||a||C¹≤C_K ε→0. On the fixed closed annulus R/2≤|z|≤R,
all derivatives through the required orders of f−id,h,a are O_K(ε): its
radius is bounded away from 0, independently of n. Thus L(b+h+a) tends
uniformly there to Δb, whose minimum is positive. The cutoff is smooth and
flat where it meets the constant outer region; outside R all expressions
equal the background. This proves global positivity after one finite discard
of n, including both sides of both boundaries.

The exact curvature is e^{2U}ΔU, with ΔU(f(z))=L(b+h+a)(z). Therefore
this controls actual Gaussian curvature, not a linearized proxy. The metric
converges in C¹ because μ,a do. It remains complete, and its unique inverse
components have the nonzero fixed jet described above. This independently
verifies candidate lines 139–198 on both surfaces.

## 7. Controls that can detect geometric shortcuts

Five exact rational Taylor-algebra controls were run, independently of the
author's checker. They supplement the preceding universal argument.

* For J=[[2,1],[0,3]] and v=x²+3xy+2y², direct composition has Laplacian
  2/3. J^{-1}J^{-T} gives 2/3; the reversed factor order gives 5/9.
* For f(x,y)=(x+x²,y), the inverse first coordinate has jet t−t², so B_x(0)
  is −2 although J(0)=I. Dropping drift would be wrong.
* For the uncorrected r=1 metric, write z=ρξ on the inner disk and
  G(ξ)=1−2ρξ. Then

      f_z(ρξ)=G(ξ)+ερ M(ξ),
      M(ξ)=ξlog(1+|ξ|²)+ξ²barξ/[2(1+|ξ|²)].

  On a fixed neighborhood of ξ=-1, G stays nonzero. Expanding
  log|G+ερM| in the C² ξ norm, and using the harmonicity of log|G|, gives

      Δ_z h(-ρ)=-(7/2)ε/ρ+O(ε+ε²).

  The exact value Δ_ξ Re M(-1)=-7/2 is checked by rational jets. At this
  point J−I=O(ρ), D²h=O(1+ε/ρ), and B,Dh,Db,D²b are bounded, so

      L(b+h)(-ρ)=-(7/2)ε/ρ+O(1)<0

  for all large n. Thus the same construction with a=0 really fails the
  curvature domain at r=1. This falsifies that shortcut, not the corrected
  candidate.
* At ξ=-1, Δ_ξ sqrt(1+|ξ|²)=3/(2sqrt2). Consequently the corrected
  leading curvature is

      [-7/2+3K/(2sqrt2)] ε/ρ+O_K(1).

  K<7sqrt2/3 is insufficient at this point; K>7sqrt2/3 makes this leading
  point positive. Equality is not decided by the leading term. This local
  threshold is not a sufficient global K bound: the universal proof uses
  K>4C₀ and the separate annulus argument.
* The exact critical conformal-factor first jet is Dh(0)=(-2,0), while
  Db(0)=Da(0)=0. It survives the normalized inverse coordinate change.

A further integral obstruction identifies why the positive background is
essential. If one tried b=0 globally with f identity outside compact support
and compact a,h, then U would be compactly supported. Nonnegative curvature
would require ΔU≥0. Its integral is zero by the divergence theorem, forcing
ΔU=0 everywhere and then U=0 by harmonic uniqueness/maximum principle.
The resulting metric would be a pullback of the flat metric and could not
have strict positive curvature. The candidate uses the complete positive
cigar instead, and passes this obstruction. No finite computation is needed
for this integral control.

## Evidence, limits and strongest conclusion

The first attempted exact-control operator failed before controls ran because
SymPy was absent: collector PID 91695, owned child PID 91703,
14:30:48.876759–14:30:48.901496 UTC, exit 1. Its exact source and full 277-byte
stderr are preserved under captures/geometric_controls. It is an environment
failure and contributes zero successful controls. A separate standard-library
Fraction operator then passed all five exact controls: collector PID 93641,
child PID 93651, 14:33:16.190900–14:33:16.219553 UTC, exit 0, full stdout 1556
bytes and empty stderr. The primary-reading operator was child PID 91565 of
collector 91557, 14:30:34.593685–14:30:41.243193 UTC, exit 0; its nine owned
Poppler children all exited 0. Every actual run has prelaunch operator and
collector snapshots, true owned PID/time/argv, full streams and byte hashes.
No author/historical checker was read or replayed. No ROOT helper has been
executed by this family.

The original proof-attempt budget is 1/5, not this family's diagnostic count.
This audit adds no substantive discovery turn, native claim, queue mutation,
Git/remote/publication action, paper or DOI. The original draft proposes
claimed_solved 1/5; that is an archived original field, not fresh native status.
The preparer records raw prior report key ABSENT, SQL report non-NULL TEXT
"{}", and flat original upstream_report field ABSENT; those are distinct
typed observations. Its authenticated original science count is 17; no
historical control count has been adopted as this family's fresh evidence.

Confidence is high in the mathematical conclusion for the exact pinned
candidate and target topology. The strongest verified result is a universal
counterexample construction, not merely passing finite tests. Remaining limits
are priority/current-literature completeness, human/refereed review, and ROOT's
independent custody and downstream acceptance decisions. This family has found
no remaining mathematical gap to transfer to those decisions.
