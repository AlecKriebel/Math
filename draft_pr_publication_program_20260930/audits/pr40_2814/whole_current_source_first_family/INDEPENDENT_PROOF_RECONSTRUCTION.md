# Independent operative proof reconstruction and boundaries

This reading reconstructs the three supplied primary proofs and their interfaces.
It imports standard geometric/dynamical inputs explicitly rather than presenting
a recursive proof of those inputs. The complete Luo-Markovic v1 (13 pages), Xia
v1 (11 pages) and published Kuhlmann2006 (12 pages) were read. Literal K3/AIM
targets and K3 Chapter3 conventions were read before artifact interpretations.
PDF byte identities and visual clarification pages are separately bound.

## Closed manifolds: Luo-Markovic2608.29761v1

Standing scope is a fixed closed hyperbolic n-manifold, n>=3. Orientability is
not imposed. For a closed geodesic of length in (r-epsilon,r+epsilon), define
non-collared to mean that points at ambient distance<delta have ambient distance
unequal to intrinsic circle distance. A self-intersection or nontrivial iterate
is non-collared for every delta>0. Hence delta-collared implies an embedded
primitive geodesic. Conversely a fixed simple closed geodesic has a sufficiently
small embedded collar by compactness and positive local injectivity radius.
Closed geodesic counting means periodic orbits, not all shifted circle maps.
Counting orientation twice only multiplies finite constants and does not create
extra geometric images.

The proof's quantitative chain is:

1. A (r,epsilon,delta)-tight unit vector is almost periodic at time r, and has a
   close basepoint return between two middle times in [r/10,9r/10] separated by
   at least i_M. The independent upper bound ignores almost-periodicity.
2. Let L_r^delta contain vectors with one basepoint return of distance<=delta
   at a time between i_M and r. A delta-net has O(delta^-n) points. Each such
   return lifts to a nontrivial pointed loop near one net point, with length
   <=r+3delta<2r. Lifted geodesic arcs have endpoints within O(delta), so
   fellow-travel and their initial vectors lie in an O(delta) Bowen ball.
3. A length-l pointed-loop Bowen ball has Liouville measure at most
   C delta^(2n-1) exp(-(n-1)l). Pointed-loop orbit counting in length shells
   implies sum exp(-(n-1)l)<=Cr. Multiplying by the net count gives
   Lambda(L_r^delta)<=C delta^(n-1)r.
4. For a tight vector choose close times s<t and k=floor(s/delta). Since
   k delta<=s, t-k delta>=i_M. Shifting by k delta places it in L_r^(2delta).
   The union over O(r/delta) choices, and flow invariance, yield
   Lambda(K_r,epsilon^delta)<=C delta^(n-2)r^2.
5. A non-collared closed geodesic of length near r has two close points with
   intrinsic shorter-circle separation>=i_M. Starting at the midpoint of their
   longer complementary arc puts both times within [L/4,3L/4], hence within
   [r/10,9r/10] for large r; small time shifts preserve this. Its tangent vector
   is almost-periodic since |L-r|<epsilon. A Bowen ball of fixed small epsilon
   follows the same periodic orbit with exponentially small middle-time errors.
   For delta=r^-kappa the exponential error is eventually smaller than delta;
   the ball lies in K_r,3epsilon^(3delta) associated to that geodesic. It has
   volume>=C exp(-(n-1)r).
6. The near-periodic closing map sends these Bowen balls to unique closed
   geodesic free-homotopy classes. Distinct fibers are disjoint. Therefore
   number(non-collared)<=C exp((n-1)r) delta^(n-2)r^2.
7. Margulis counting gives number(all length-near-r geodesics)>=
   C exp((n-1)r)/r for every fixed sufficiently small epsilon>0. The ratio is
   <=C delta^(n-2)r^3=C r^(3-(n-2)kappa), which tends to zero when
   kappa>3/(n-2). For dimension3 this requires kappa>3. Many primitive
   embedded images then occur in arbitrarily far length shells, proving
   infinitely many images rather than iterations of finitely many images.

Imported inputs: compact positive injectivity radius; discrete torsion-free
quotient/unique geodesic tightening; almost-periodic hyperbolic chain closing;
stable/unstable product structure and Bowen volumes; elementary hyperbolic
fellow-travel estimates; orbit counting and Margulis geodesic asymptotics.
The papers cited for those tools have not been recursively proved here. The
local volume exponents and the combination above were independently checked.
Uniform smallness thresholds can always depend on the fixed compact manifold.

Literal-proof constant qualifications, without a claimed theorem refutation:
LM p12 applies the fellow-travel lemma with a displayed C(10 i_M), while its
return arcs only have a positive lower length near i_M. Use a lower bound such
as i_M/2 and shrink delta accordingly; also require c delta<=delta_1 in the
Bowen estimate by choosing delta_0<=delta_1/c. The p7 interval [r/4,4r/4]
can be sharpened to [L/4,3L/4] from the midpoint choice. The floor-union count
has floor(r/delta)+1 terms, bounded by 2r/delta after shrinking delta. These are
constant/interval clarifications in the reconstruction, not counterexamples or
new mathematical results. They must not be silently represented as exact source
text. No orientation argument or orientable-cover descent is needed.

## Orientable cusps: published Kuhlmann2006

The published theorem explicitly assumes orientability, complete curvature-1,
noncompact finite volume and a rank2 torus cusp. Normalize two tangent lifts of
a maximal horocusp to H_0 and H_infinity, with H_infinity at height1. Two distinct
preimages A_0 and B_0 of the bumping point occur in a fixed cusp parallelogram;
if they coincided in that normalized orbit, the associated deck isometry would
fix a point of H^3, contradicting free discrete torsion-free action.

Write the cusp translations as lattice vectors u,v and B_0=x_0 u+y_0 v,
with x_0,y_0 in [0,1), not both zero. Choose the basis so y_0>0. Elements a^p g
have axes whose ideal endpoints approach0 and B_p=B_0+p u; their cusp-boundary
intersection endpoints C_p,D_p likewise approach A_0,B_p. The short outside-
cusp arc contracts to the bumping point and therefore lies in a neighborhood
where the covering map is injective. The long arc is inside the embedded cusp;
only cusp-group identifications can identify its points.

The projected long segment has transverse v-coordinate difference approaching
y_0, strictly between0 and1. Choose coordinate errors smaller than a fixed
fraction of min(y_0,1-y_0). If two points on it differed by a nonzero lattice
vector, their v-coordinate difference would be an integer of magnitude<1,
hence zero. Then their difference is parallel to u, impossible because the
segment has nonzero transverse coordinate. The long arc is embedded. Its
interior is inside the cusp and the short arc's interior outside, so the combined
curve is simple. Cusp height and long-arc length diverge, yielding infinitely
many distinct primitive images. All axes in the two-parameter family need not
be embedded; the proof uses a chosen one-parameter subfamily.

The manuscript's Euclidean-error notation is read in fixed lattice coordinates:
a fixed linear change of basis bounds each coordinate error by a constant times
the Euclidean error. Shrink the threshold by that constant. This avoids assuming
an orthonormal cusp basis. Torsion-free cusp/horoball geometry, finite-volume
cusp structure and the local covering injectivity are imported geometric facts.
Kuhlmann alone does not cover the nonorientable finite-volume target.

## All3-dimensional cusps: Xia2110.14376v1

The toral-cusp part reproduces the transverse-coordinate mechanism in any
n>=3 with a full translation cusp; higher-dimensional non-toral cusps are not
covered by that argument. In dimension3, compact flat cusp sections are tori
or Klein bottles. The orientation-preserving cusp case uses the torus argument
even if the ambient manifold is nonorientable. For a Klein cusp put generators
s(x,y)=(x+alpha,-y), t(x,y)=(x,y+beta), alpha,beta>0. They generate translations
(2k alpha,m beta) and glides (x+(2k+1)alpha,-y+m beta); glide axes lie at
half-integer multiples of beta. The relation is s t s^-1=t^-1 (equivalently
 t s t=s), not commutativity.

The short outside arc embeds as before. Let C,D be the long arc's intersections
with the height1 horosphere, and P=(C+D)/2 its projected midpoint. Cusp-group
elements preserve height. Two distinct points of a semicircle at equal height
are symmetric about its center, so if a glide identifies them, their projected
midpoint must lie on a glide axis: P_y in (beta/2)Z. This exact equal-height
restriction is essential: looking only at projected segment crossings is not
a valid test for a glide-induced self-intersection.

Xia's exhaustive coordinate cases supply robust avoidance margins:

- Different x-coordinates of A_0,B_0 in a width-alpha domain: translate far in
  y. Projected x-width remains nonzero and<alpha. Nonzero translations require
  x-displacement>=2alpha or zero; glides require at least alpha. Both fail,
  with the zero-x translation ruled out by nonverticality.
- Same x and y-coordinates symmetric about0: write A=(0,-a), B=(0,a), with
  0<a<beta/2. Use t^n s. Endpoint x-width approaches alpha, hence is<2alpha
  and nonzero, ruling out translations. The midpoint y approaches n beta/2-a,
  whose distance from (beta/2)Z is min(a,beta/2-a)>0. Small endpoint errors
  preserve this distance and rule out all glides by the equal-height condition.
- Same x and y-coordinates not symmetric about0: use s^(2n). The transverse
  y-difference is nonzero and<beta, ruling out translations as in the torus
  argument. The midpoint y=(A_y+B_y)/2 stays off (beta/2)Z because A,B lie
  in [-beta/2,beta/2) and have nonzero sum. Small errors preserve that gap,
  ruling out glides. A=B is excluded by the bumping-point/free-action setup.

These cases cover all positions of the two distinct bumping preimages. Long
lengths diverge as translation parameters diverge, so embedded images are
infinitely many, not repeated traversals. The finite-volume noncompact case
has a virtually rank2 cusp and is non-elementary; those standard structure
facts are imported rather than recursively certified.

Xia's p5 inequalities constrain locations of existing fixed points; alone they
do not establish existence of two fixed points. A direct reconstruction supplies
it: a normalized boundary isometry has form F(x)=B+Qx/|x|^2 with Q orthogonal.
For R=|B| sufficiently large, F is a contraction on the ball B(B,2/R), since
|x|>=R-2/R and derivative norm<=1/(R-2/R)^2<1; its displacement from B is
<=1/(R-2/R)<2/R. The inverse is a contraction on B(0,2/R) by the same bounds.
The two disjoint balls yield distinct fixed points, one near B and one near0.
The free discrete group excludes elliptic axis-fixing rotations, giving an axial
loxodromic (possibly orientation-reversing) isometry. Its axis has large cusp
excursion. This explains the axis existence used in the construction; it is an
independent reconstruction of the paper's elementary step, not an assertion
that the original inequalities alone prove it.

## Scope conclusion and falsifiable boundaries

Combining these imported primary results covers the literal3-dimensional
finite-volume target: closed by LM and noncompact orientable/nonorientable by
Xia, with published Kuhlmann as the orientable-cusp result. This is a literature
coverage reconstruction conditional on the explicitly imported standard inputs.
It gives no project theorem, novelty credit, new DOI or extra research response.
A raw dated open classification cannot override a later pinned primary proof.
Conversely an arXiv theorem is not a new theorem authored by this project.

Finite volume and dimension3 are essential boundaries of this coverage. H^3 is
a complete infinite-volume hyperbolic3-manifold with no closed geodesic: a
geodesic lifts to a line with no periodic points. A torsion-free rank1 cyclic
loxodromic quotient H^3/<g> is infinite-volume and has a single primitive closed
axis image; powers only iterate it. A thrice-punctured hyperbolic surface has no
nonperipheral simple closed geodesic, showing that the blanket cusped statement
cannot be shifted down to dimension2. Variable negative curvature, manifolds
with boundary, incomplete metrics and orbifolds are not supplied by these proofs.
No finite parameter sample certifies the universal cusp or asymptotic theorem;
finite controls can only challenge local transformations/algebra/exponent signs.
