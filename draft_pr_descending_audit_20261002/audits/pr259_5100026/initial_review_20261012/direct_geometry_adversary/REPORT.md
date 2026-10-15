# PR259 independent direct-geometry adversary report

Target: 5100026 / k407. Authentic submitted head:
`0524ed734ee8185681d030af98088259134a6af7`.
Family: physical specular ray tracing and Cartesian tangent/normal intersections.
Review completion estimate: 100% of this family's assigned audit, not of a
historical novelty or publication assessment.

**Finding:** no mathematical defect found in the submitted theorem for strict
nondegenerate confocal elliptical caustics and even **least** period, including
coprime stars. The proof's real geometry, complex singularity coverage, residue
cancellation and exceptional N=4 treatment survive this audit. A literal
extension to any even-length list is false: an exactly certified triangle
repeated twice supplies a counterexample. The submitted theorem already
distinguishes these scopes correctly.

The two focus means are negatives of each other. This does not impose a fixed
direction relative to a chosen focus: the mean about the positive focus can
have either sign among primitive even families. The submitted proof makes no
direction inequality. My initial plan used negativity as an extra hypothesis;
it was falsified by my frozen controls. An earlier progress message had
inaccurately described those controls as supporting it; the correction is
preserved in RESEARCH_LOG.md.

## Exact claim, assumptions and success criterion

Original ellipse E has a>b>0, original focus M=(sqrt(a^2-b^2),0), and strict
confocal caustic with parameter 0<lambda<b^2. P_i follow the physical
specular billiard law. R_i is the intersection of the original ellipse
tangents at P_i,P_{i+1}. U_i is the intersection of consecutive lines through
R_i perpendicular to R_i-M. The quantity is sum U_i/N, not an area centroid.
For genuine even least period N>=4, with winding tau coprime to N, the exact
claim is finiteness of every real U_i, phase invariance of the arithmetic
mean, its location on the original focal axis, opposite-focus negation and
the N=4 value zero. Reversal and repeats of an even least-period orbit preserve
the mean. Hyperbolic and degenerate caustics are outside this theorem; the
circle is a separate centrally symmetric special case.

Success means a checkable all-period argument consistent with actual Euclidean
geometry. Numerical agreement alone cannot achieve it. This report assesses
the submitted analytic argument and supplies independently derived exact and
numerical geometry controls.

## Independence and evidence provenance

At 2026-10-12 11:39:06 UTC I froze INDEPENDENT_PLAN.md, SHA256
`ba36e7b14e4f16f4205621770f08abb96094e2f0c17d6d3abb649ad440bbeed9`.
Before that freeze I read only the assignment, applicable AGENTS.md, input
file names, and the permitted submitted SOURCE_GATE.md, SOURCES.md,
metadata.json and README.md. An overbroad first file inventory exposed many
unrelated file names and was truncated; it exposed no mathematical contents.
I had not read PROOF.md, author/reviewer verification helpers, old review
verdicts, or other new-family derivations.

At 11:44:16.054772 UTC, PRE_PROOF_INDEPENDENCE_FREEZE.json froze the
independent physical ray script, 75 broad even families, nine high-precision
stability families, eight odd controls, rational N4 witness, and exact odd
triangle counterexample before reading the submitted proof/code.

After this freeze I read the entire submitted PROOF.md and the two author
verification scripts, browsed primary source definitions and standard Jacobi
facts, and created separate post-exposure checks. No submitted helper is
imported by any family script. No old reviewer verdict/code or new-family
derivation was read. Root subsequently suggested the star k=.63,N8,tau3 and
its approximate positive mean as an adversarial sign control; that stimulus
is explicitly recorded. Root later mentioned parameters of its different
exact odd witness, but those parameters and its proof were not used in this
family's already-frozen exact witness.

## Independently verified Cartesian geometry

The pre-freeze formulas use P(theta)=(a cos(theta),b sin(theta)) and
g^2=a^2 sin^2(theta)+b^2 cos^2(theta). With forward unit tangent
T=(-a sin(theta),b cos(theta))/g and outward unit normal
H=(b cos(theta),a sin(theta))/g, the outgoing unit ray is

`d=sqrt(1-lambda/g^2) T - sqrt(lambda)/g H`.

The caustic tangency follows from the support relation for a unit line normal
n=(-d_y,d_x):

`lambda=a^2 n_x^2+b^2 n_y^2-(n dot P)^2`.

The next ellipse intersection is found from the quadratic along the ray;
subsequent directions are propagated by the physical reflection formula.
The caustic parameter is solved by physical winding closure at one phase,
then held fixed while the starting phase changes. Tangent intersections use
the original equations `(P_x/a^2,P_y/b^2) dot R=1`. Antipedal lines use
`(R-M) dot U=|R|^2-M dot R`. No Jacobi parametrization entered these initial
controls.

The independent REAL_GEOMETRY_LEMMA.md supplies an exact Euclidean proof of
real finiteness for every strict elliptical-caustic orbit and every strictly
interior M, regardless of parity. Consecutive outer vertices R,S are finite,
distinct and lie on one original ellipse tangent. M cannot lie on this
tangent. Therefore R-M,S-M cannot be dependent. In unit tangent coordinates,

`det(R-M,S-M)=(s-r)(P-M) dot H != 0`.

This proof does not establish phase invariance. Central symmetry of an even
least-period orbit separately gives C(-M)=-C(M) by reindexing its antipodal
outer vertices and negating the normal intersections.

For the exact N4 control a=5,b=3,c=4, lambda=225/34, the original diamond
has outer vertices (5,3),(-5,3),(-5,-3),(5,-3). Its antipedal about (4,0)
is (-4,6),(-6,0),(-4,-6),(14,0), with arithmetic mean zero. The submitted
general rectangle argument is stronger than this particular control and
was independently checked below.

## Exact repeated-odd counterexample and source scope

Set a=5,b=3,c=4, D=sqrt(481), t=(D-9)/16, s=sqrt(1-t^2)>0. The points

`(5,0), (-5t,3s), (-5t,-3s)`

form an actual least-period-three billiard orbit with strict elliptical
caustic `lambda=225(D-17)/128`. All boundary, unit-direction, common-caustic
and specular-reflection identities reduce exactly to zero modulo
`16t^2+18t-25=0`, `s^2+t^2=1`; the intended real root satisfies .8<t<.82.
The central reflection is another phase of the same caustic family.

Their original-positive-focus vertex means are respectively

`Gplus_x=[5+9(1+t)/(1-t)-10/t]/3 ≈ 25.83024650637936`,

`Gminus_x=[-5-(1+t)/(1-t)+10/t]/3 ≈ -0.68552816595785`,

with y=0. Their difference is `20(2t-1)/(3t(1-t))>0`.
Repeating either orbit twice gives nominal listed N=6 and leaves its mean
unchanged. All intersections are finite. Thus an even listed count does
not imply phase invariance. See EXACT_WITNESSES.md for the derivation,
nonzero denominator bounds and caustic inequalities; exact_controls.py and
exact_cartesian_witnesses.json provide the exact arithmetic receipt.

The original arXiv v11 paper's Table 5 identifies k407 as the outer-antipedal
vertex centroid, even N, with M either original focus and unspecified value.
Its title is *Eighty New Invariants*. Its definitions distinguish vertex and
signed-area centroids. I found no literal primitive/gcd/repeated-list
qualification in its searchable text. This does not settle the convention
intended by N-periodic. [arXiv v11, Section 3.5/Table 5](https://arxiv.org/pdf/2004.12497v11)

The final *Fifty New Invariants* has the same target in Section 3.5 and Table 5
on printed pp.347–348, and permits self-intersecting antipedals. Its searchable
text likewise yielded no literal primitive/gcd qualification. The exact
counterexample shows why the least-period convention must be explicit when
stating the mathematical result. The submitted theorem supplies that
qualification. [Final paper](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf)

## Full submitted proof audit

| Step | Assessment and exact reason |
|---|---|
| Canonical parametrization | Stachel Theorem4.3/(4.9) matches the caustic eccentricity modulus, outer axes and step 2v; gcd(N,tau)=1 is explicit there. Both ordinary and star winding are admitted. |
| Actual outer polygon | Solving the original tangents at P(u-v),P(u+v) yields R=(-a d/c sn(u), b/c cn(u)), matching equation(1). This does not replace the outer polygon by a confocal billiard. |
| Real determinant | Delta=2B s d D(a+kS)/D0 has positive factors for real phase; a>k and D0>0. The independent convex-tangent lemma supplies an alternative proof. |
| Common complex torus | The common lattice 4K,4iK' is legitimate. The real dn period is 2K. The bilinear complex dot product is the correct meromorphic continuation. |
| dn zeros | Endpoints coincide, remain finite and give a simple determinant zero. Both Cramer numerators vanish; quotient singularities are removable. |
| Midpoint Jacobi poles | Endpoint arguments are regular; D(a+kS)/D0 has a finite nonzero limit. No unlisted singularity persists here. |
| Focal roots | At S=-a/k, the common original tangent passes through M and is isotropic, making both q dot q zero. The simple-zero cancellation is sound. It depends on ORIGINAL foci. |
| Exceptional overlap | s^2 a^2=1 reduces to k^2 x^2-2x+1=0. The unique x in (0,1) is 1/(1+k'), corresponding to v=K/2. Coprimeness then forces N=4,tau=1. |
| Endpoint poles | Exactly one endpoint is singular because 0<2v<2K. D0 zeros are simple and the determinant has a simple pole away from N4. Cramer numerator order is at most two, so U has at most a simple pole. |
| Exhaustion | Outside Jacobi poles, the explicit determinant factorization permits only dn zeros, focal roots and endpoint poles. The sn degree-two map on its own torus, doubled for the common lattice, accounts for all endpoint classes. |
| Cyclic pole bookkeeping | Primitive even tau is odd; a real delta orbit has exactly two R pole indices j,j+N/2. Their four incident edge indices are distinct for N>=6. This is a universal modular argument, not a finite index experiment. |
| Residue cancellation | With fixed leading L, the residue solves L dot V=L dot L and (Q-M) dot V=0, hence V=-(L dot L)J(Q-M)/det(L,Q-M). Neighbor values Q,-Q and opposite leading -L yield the stated quartet cancellation. There are no higher pole orders to leave untested. |
| Holomorphic constancy | Removing every pole makes each coordinate holomorphic on a compact torus; it is constant. This is the universal step and is not inferred from numerical controls. |
| Axis and focus symmetry | Focal-axis reflection reverses order within the fixed-caustic family; unordered pair intersections preserve the sum. Central symmetry negates focus and centroid. No direction inequality follows. |
| General N4 | Half-period outer vertices lie on one circle and have antipodal pairs, hence form a rectangle circumscribed about E. Direct edge-normal solutions give the submitted mean formula; the support identities h^2-m^2=l^2-n^2=b^2 make it zero, with nonzero real denominators. |
| Circle, reversal, repeats | Even primitive circular orbits pair antipodally and have independent normals. Reversal/repeats of even least period preserve the arithmetic sum. Odd repeats are correctly excluded. |

Stachel supplies the standard canonical coordinates and explicitly includes
coprime turning numbers in Theorem4.3 on printed p.1614. The paper prints an
incorrect antiperiod sign for dn near p.1613; the submitted proof uses the
correct real period and therefore does not inherit that error.
[Stachel, published article](https://doi.org/10.1007/s40879-021-00524-2),
[primary repository reading copy](https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf)

The addition formulas and real/imaginary shifts used in this audit are
confirmed by NIST's Jacobi references, including dn(u+2K)=dn(u) and
dn(u+2iK')=-dn(u). [DLMF22.4](https://dlmf.nist.gov/22.4),
[DLMF22.8](https://dlmf.nist.gov/22.8)

## Quantitative controls and their limits

| Independent control | Coverage | Largest scaled phase variation | Other checks |
|---|---|---|---|
| Pre-proof broad ray tracing | 75 primitive even families, 450 phase runs, a/b=1.0001,1.2,5/3,3,10; N4 through N30 and many coprime stars | 1.06e-38 at 70 digits | Caustic residual <=2.12e-68; closure <=2.94e-53; no determinant failure. |
| Pre-proof stability | 9 families, 54 phase runs, a/b through100; N4,N12/tau5,N30/tau13 | 5.51e-87 at 140 digits | Minimum scaled normal determinant 2.21e-15; caustic residual <=7.50e-137; closure <=1.52e-110. |
| Pre-proof odd controls | 8 families,48 phases, both ordinary and star odd least periods | Not invariant; differences can be large | All traced closures and caustic checks retained; repeating each orbit twice preserves its mean. |
| Post-proof checks | Five canonical stimuli; three physically reclosed phases each; complex local and complete sum neighborhoods | Complete pole residual <=6.51e-48 at120 digits, eps through1e-36 | Actual outer formula error <=3.63e-121; determinant error <=4.34e-121; physical/canonical vertex error <=3.51e-119. |

High-winding elongated cases are ill-conditioned: the strict caustic approaches
its excluded degeneration and consecutive normals can become nearly parallel.
The loss of digits is preserved in the diagnostics and improves at higher
precision. These are high-precision arithmetic checks, not interval-certified
computations or universal proofs. The exact controls and reviewed analytic
argument carry the exact conclusions.

The root-suggested star k=.63,N8,tau3 independently re-solves to the same
physical caustic and gives x=+1.780146638544216006266687370922135277466 at
three phases. Forty broad N>4 families had negative x and thirty had positive
x. Every N4 case remains consistent with zero. This falsifies the extra
direction-sign hypothesis while supporting the theorem's actual symmetries.

## Boundary, failure and reproducibility declarations

Strictness matters: lambda=0 collapses the two boundary tangency endpoints;
lambda=b^2 degenerates the elliptical caustic. Original-axis degeneracy
b=0 and hyperbolic caustics are outside scope. The positive determinant
argument need not have a uniform lower bound as an excluded limit is
approached. N4 complex overlaps are handled directly, rather than imported
through the N>=6 local argument. Generic M can leave additional complex
poles and does not have the asserted invariance; no such extension is made.

No mathematical test failed. Operational diagnostics are preserved: initial
system Python lacked mpmath; the preexisting workspace environment supplied
mpmath1.3.0 and SymPy1.14.0 on Python3.9.6. The initial inventory truncation
and the erroneous initial interpretation of a direction sign are recorded.
No package installation, contact, Git/index/ref operation, or provider write
occurred. All family mutations stayed in this folder; publication decisions
belong to Root/human. Existing frozen inputs are read-only and hash checked.

Run scripts in a copy of this folder to avoid overwriting frozen dated
receipts. With Python, mpmath and SymPy available:

```
python exact_controls.py
python direct_controls.py --mode broad --dps 70
python direct_controls.py --mode stability --dps 140
python direct_controls.py --mode odd --dps 90
python post_freeze_geometry_audit.py
python build_manifest.py
```

The script receipts record executable, versions, precision, start/end time,
commands and script SHA256. The numerical script's output and progress logs
are complete; no selected-only successful subset replaces failed cases.
The final MANIFEST.json pins family artifacts and verifies every frozen
submitted body's hash against INTAKE.json. It excludes Python caches and
itself. No external source PDF/full text is present in the public artifact
selection; the report contains only locators and brief attribution.

Strongest verified result: the exact scoped primitive-even theorem survives
this audit, supported by independent direct geometry and exact boundary
controls. Remaining mathematical gap in that scoped theorem: none identified.
Remaining source qualification: retain and explain even least period; a
literal even-count extension is false. No priority, novelty, publication or
claimed-solved tracker verdict is made by this family.
