# Independent mathematical audit: problem 4500001

## 1. Disposition and exact acceptance boundary

**Accept the substantive partial classifications under the explicitly stated
continuous convex-corner convention, with the narrow correction in Section 10.
Do not accept a full solution.**

The original audit required this correction before publication; the original
uncorrected manuscript was not accepted as-is. This public edition applies the
exact required replacement to the separately sealed proof and retains the full
mathematical review, defect and witness below. The audit was AI-assisted and
is unrefereed; acceptance is not external human peer review, journal acceptance
or formal proof-assistant certification.

This edition binds [PROOF.md](PROOF.md): 27,673 bytes; SHA-256 `d2836eb9944690cd91cce0ddbd2740ca82104878e77f6d9eaf581b16c5bb786b`. [CORNER_CORRECTION.md](CORNER_CORRECTION.md) records the exact replacement and its complete counterexample.

The original audit checked the manifest and all twelve listed authored files against their recorded byte counts and hashes. The complete authored proof, verification implementation and source audit were inspected. The exact originating scope was checked against the full five-page 2015 primary article. Relevant 2012 Sections 6–8 were read in full, with the earlier corner convention, leaf construction, 14/4 example and decomposition theorem also checked.

The publication proof preserves all accepted arguments and expands the three already audited rational examples by explicit substitution in the audited permutation, singular-strip and reversal formulas. These additions expose the finite derivations that were previously represented by a reference to verification output; they introduce no new parameter family or region-count claim. The correction witness's reversal pairing is likewise written out directly. Exact arithmetic checks of those expository substitutions were performed during edition preparation; the original mathematical test programs were not rerun.

Accepted, with all trajectories understood to be complete and regular under the
main convention:

- The direction-retaining weighted return map and least collision-period formula.
- A finite, complete rational-parameter region and period decomposition.
- The complete quarter-rotation line, including its irrational complementary region.
- The exact periodic set, threshold, period and periodic-region count for rational
  outer rotation and irrational inner rotation. This is not a count of all
  nonperiodic components on that line.
- The full 14/4 decomposition on the stated open irrational-capable band.
- The rational-independence nonperiodicity/minimality argument and the all-period
  obstruction for the later-source Cayley counterexample.
- The finite-word certificate as a logically complete, unbounded characterization
  of periodic cylinders, not a terminating algorithm for the general problem.
- The correction of the one specified translation in the inspected 2012 v1 PDF.

One optional-convention statement in the original manuscript was false as
literally written: deleting all convex-corner trajectories can change the
number of oriented cylinders. It does
not undermine any of the above results under the main convention. The exact
defect, witness and minimal replacement are supplied separately. Publication of
the uncorrected frozen text is not cleared by this audit.

No novelty, worldwide current-openness, general confocal normalization, or
arbitrary finite-arc-table result is established. The original arithmetic
classification question remains partial.

## 2. Source scope, physical inspection and normalization

The source table is a large right half-disc and a smaller left half-disc, joined
by two collinear radial segments, up to rigid motion. The caustic is strictly
inside the smaller disc. With radii `R1>R2>r>0`, the correct normalization is

    a = arccos(r/R1)/pi, b = arccos(r/R2)/pi, 0<b<a<1/2.

The source period counts all boundary bounces, including straight segments. The
2015 examples are 12/7, 5/6, 13/21 and a mixed period-6 example. Its Question 2
asks for both periodic and nonperiodic boundary regions and their periods;
Question 3 expands to other finite-arc tables. A finite experiment or a necessary
integer relation is not sufficient to answer Question 2.

The original 2015 source has five pages, 69–73. Its page 71 was physically
inspected, including the region diagram and all four requested examples. The
2012 manuscript has 24 pages. Its pages 18 and 19 were physically inspected to
verify all three signed-IET permutations and the disputed lower-sign formula.
The manuscript's genus-three construction and Sections 6–8 rule out a
genus-one or Cayley-sufficiency shortcut.

Section 1 of the 2012 source defines reversal at a convex right-angle corner as
a limiting continuation, counted as two bounces. Reflex-corner reflection has
no such well-defined limit. These are exactly the main conventions used by the
authored result. Hashes, byte counts, URLs and inspection scope are recorded in
[SOURCE_METADATA.json](SOURCE_METADATA.json); source bytes and images are excluded from this edition.

## 3. Independent geometric derivation

Set `r=1` and let `alpha_i=pi*rho_i`. For an anticlockwise unit tangent contact
normal `n(theta)=(cos(theta),sin(theta))`, the forward tangent line meets the
full radius-`Ri` circle at angle `theta+alpha_i`. The reflection changes the next
contact normal to `n(theta+2alpha_i)`. This follows either from the equal-angle
law or from `v -> v-2(v dot p)p/Ri^2` at the collision point `p`.

Put `theta0=pi/2-2alpha1+alpha2`. On the anticlockwise sheet use
`theta=theta0+2pi*x`; on the clockwise sheet use its reflection in the horizontal
axis. The first smaller-circle collision lies on the smaller left semicircle
exactly when

    pi/2 < theta+alpha2 < 3pi/2.

In the chosen coordinates this is `a-b<x<a-b+1/2`, exactly branch B.
Outside B, the only circular collision before the next contact is on the larger
circle. The additional upper straight-segment collision occurs exactly for
`0<x<a-b`, branch A. Its order switches at

    theta=pi/2-alpha1, equivalently x=(a-b)/2.

Below that value the circular collision precedes the straight one; above it the
straight collision precedes the circular one. At equality the events coalesce at
the convex right-angle vertex. The product of the two reflections reverses
velocity and has the same limiting contact map on both sides.

A vertical-line reflection sends the contact normal `theta` to `pi-theta` and
changes angular direction. Composing it with the outer-circle collision gives
`pi-theta-2alpha1` in both possible orders. Re-expressing in the clockwise
coordinate gives `x+a+1/2 mod 1`. On C only the outer circular reflection occurs.
Thus the three shifts are independently recovered as

    A: a+1/2, with direction flip and weight 2;
    B: b,     with no flip and weight 1;
    C: a,     with no flip and weight 1.

Reflection of the entire construction in the horizontal axis gives the same
coordinate map on the other sheet. Every complete trajectory meets the contact
section, and every nonsingular contact state determines its next segment
sequence uniquely. There is no omitted angular-direction state.

The three true singular input coordinates are `0,d,d+1/2`, with `d=a-b`.
They correspond to the three incoming separatrix directions distributed across
the reflex vertices on each sheet. The convex value `d/2` is not a discontinuity
under the main convention. Artificial cuts caused by reducing modulo 1 are also
not singular. An orbit meeting a reflex vertex in either time direction is
excluded; an arbitrary half-open formula is not permission to continue it.

As an exact additional check, the audit ray tracer uses rational Pythagorean
radii, rational unit contact normals and exact quadratic intersections. It
chooses the physically first boundary hit, applies the Euclidean reflection law,
and looks for the next tangent contact. Branch prediction uses exact orientation
predicates between rational unit vectors, without angles, floating point or
tolerances. All 2,460 cases pass, including 134 exact reflex-singular cases and
42 exact convex-corner cases. This is corroboration of the derivation, not a
substitute for its all-parameter inequalities.

The physical projection formulas in the authored note also follow: circle hits
have the angles just derived; a tangent line with normal `theta` meets the
y-axis at `y=1/sin(theta)`. Before/after the outer reflection this yields the two
A formulas. At `d/2`, each gives `y=R1`, so the formulas meet at the correct
convex vertex. The clockwise formulas are horizontal reflections. Their
endpoints are singular or auxiliary endpoints as specified, not new hidden
open dynamical regions.

## 4. The printed source sign error is independently established

In the lower-sign case `1/2+b-2a<0`, page 19 of the inspected arXiv:1206.0163v1 prints the shift
`a-1/2` on `[-1/2-a,a-b-1)`. Its image is

    [-1, 2a-b-3/2).

But the printed positive interval `[1/2-a,a-b)` with shift `a-3/2` has exactly
that same image. Both intervals have positive length `2a-b-1/2`. The alleged
IET is therefore noninjective throughout this parameter regime, not merely at
an endpoint or one floating-point test.

The exact interior witness `a=3/10`, `b=1/14` uses inputs `-79/100` and
`21/100`. Both printed outputs are `-99/100`. The disputed interval is
`[-4/5,-27/35)`; the positive input is also strictly interior to its branch.
The geometric return map instead gives outputs `1/100` and `-99/100`.

The corrected negative shift is `a+1/2`, whose image is
`[0,2a-b-1/2)`. For the witness, this is `[0,1/35)`, exactly the missing range.
It is also the shift forced by the source's independently printed destination
order `F,D,C,E,B,H,G,A` and its length vector. The audit reconstructs every
translation from cumulative interval lengths and this order, rather than
copying either the author's corrected map or the erroneous source translations.

The exact witness, the interval-overlap argument, the physical source pixels,
the printed permutation, and the independent geometric derivation all agree.
The correction is accepted only for the inspected arXiv v1 location. Nothing
here asserts that a later publication or another version has the same error.

## 5. Orientation, minimal collision periods and rational regions

For a primitive base cycle of length `q` with `k` A visits, the orientation
cocycle is `k mod 2`. The oriented return has `q` contacts if `k` is even and
`2q` if `k` is odd. Its bounce count is respectively `q+k` or `2(q+k)`.
This is a least period: an earlier billiard-state return would yield an earlier
return of the oriented caustic contact. A contact count, a base-circle period,
and a boundary collision count cannot be substituted for one another.

For rational `a,b`, every shift and all true breakpoints lie on the `1/L` grid,
where `L=lcm(2,den(a),den(b))`. Each cell is translated to another cell with
the same transverse offset. Hence the cell permutation and its orientation
lift close for every interior point, and the displayed period bound is safe.
Regular auxiliary endpoints obey the same continuous map. Singular ones are
excluded instead of being assigned an artificial periodic continuation.

The author's singular closure and component merging are correct. An independent
way to see their completeness is especially useful. The right images of the
three true breakpoints are the same set as their left images:

    {a, a+1/2, 2a-b+1/2} modulo 1.

At every other endpoint, left and right images agree. Consequently the union
of the three breakpoint cycles of the right-continuous finite permutation is
already closed under both one-sided maps and their inverses. Its complement
consists of maximal nonsingular strips. The return permutes these strips by
translations of equal-width intervals. Cycles of signed strips are exactly the
maximal oriented cylinders. This independently recovers the author's graph
algorithm without treating each auxiliary grid cut as a physical separatrix.

Reversal at a contact is

    J(x,s)=(2a-b-1/2-x mod 1,1-s).

It reverses the flow. The two fixed-caustic outgoing choices at a smooth
boundary point trace the same trajectory in opposite time directions. Thus
reversal pairing is the required identification for boundary regions; a
J-invariant cylinder remains one boundary region. The accepted rational output
is a region classification, not merely a list of sampled orbit lengths.

The independently reconstructed signed-strip decomposition agrees exactly with
the author implementation on 1,225 rational pairs: singular coordinates, every
signed cell in every maximal component, contact lengths, bounce counts and
boundary-region periods agree. There are 419,664 additional signed-map
comparisons across all three source regimes. Required examples give:

- `(1/3,1/4)`: boundary periods `[7,12]`, three oriented cylinders. The period-12
  family has six outer, four inner and two straight reflections.
- `(1/4,1/6)`: boundary periods `[5,6]`, three oriented cylinders. Treating all
  auxiliary grid cuts as singular wrongly gives five cylinders; the independent
  algorithm detects and rejects this overcount.
- `(1/3,1/5)`: boundary periods `[13,21]`, four oriented cylinders.

These checks support the finite proof; the finite proof, rather than the number
of test pairs, establishes the claim for every rational pair. PROOF.md now gives the complete finite strip/cycle and reversal derivations of these same three examples, so none of their period or region claims depends on omitted verification output.

## 6. Quarter-rotation line and rational/irrational threshold

### Entire `a=1/4` line

For `d=1/4-b`, A maps `(0,d)` onto `(3/4,1-b)` and C maps back. The primitive
base word is AC, so the oriented collision period is 6. The remaining section
pieces are `(d,3/4)` and `(1-b,1)`. Collapsing the omitted gaps by the stated
piecewise translation gives a circle of length `ell=1/2+2b`; the return advances
by `b` modulo `ell`. These identities apply away from the appropriate singular
orbits. The conjugacy is not a license to continue the physical corner orbits
through a removed cut.

If `b` is irrational, `b/ell` is irrational: a rational value `r` would imply
`b=r/(2-4r)`, with the impossible zero-denominator case checked separately.
Thus every complete complementary orbit is nonperiodic and dense on its
orientation sheet. Its two sheets are time-reversed partners. If `b=u/v`, the
rotation ratio is `2u/(v+4u)`, whose reduced denominator is
`(v+4u)/gcd(2u,v)`. No A visits occur there, so this is also its collision period.
Together these give the complete stated two-boundary-region classification.

The source mixed parameter `1/sqrt(30)` satisfies `0<b<1/4`, so its period-6
region and nonperiodic complementary region follow from the conjugacy without
an orbit cutoff.

### Rational `a=p/q`, irrational `b`

An oriented closed orbit with `m` outer and `n` inner reflections satisfies
`ma+nb` integral, because its total straight-reflection count is even. Hence
irrational `b` forces `n=0`. This necessity rules out every proposed periodic
orbit touching the inner semicircle, regardless of length.

For outer-only motion, reduction modulo `1/2` gives `y -> y+a`. Exactly one
outer state lies over a regular reduced coordinate: `x=y` for `y<d`, and
`x=y+1/2` for `y>d`. Its next state remains outer precisely when
`y` avoids `[1/2-b,1/2)`. With `g=gcd(q,2)`, the reduced rotation has order
`Q=q/g` and orbit spacing `h0=1/(2Q)`.

The translated holes cover the circle if `b>=h0`; at equality any limiting
survivors are endpoints, not regular periodic trajectories. If `b<h0`, the
survivor is exactly the `Q` intervals

    (j*h0,(j+1)*h0-b), 0<=j<Q.

Let `K=2p/g`. Then `a=K*h0`, `d=K*h0-b`, and exactly K survivor strips lie in A.
The permutation of strips is transitive since `gcd(K,Q)=1`. For odd q, K is even
and the period is `Q+K=q+2p`; for even q, K=p is odd and orientation doubling
gives the same `q+2p`. In the former case there are two reversal-paired phase
cylinders; in the latter, one J-invariant cylinder. There is exactly one periodic
boundary region when the survivor exists. All other complete trajectories are
nonperiodic by the inner-visit obstruction.

This proves both directions of the threshold and exhausts the periodic set.
It does not classify the number of minimal components in the complement.
Conversely, irrational a and rational b force `m=0` for a closed orbit, whereas
a trajectory cannot stay in B indefinitely: B advances by the positive b and
has no wrap before it exits. Thus that reversed mixed case has no periodic
regular trajectories, but a general region-count formula is not supplied.

## 7. Complete open 14/4 band

Take `a+b=1/2`, `1/6<b<1/4`, `d=1/2-2b>0`, `e=3b-1/2>0`.
Starting with `(0,d)`, direct branch substitution gives ACBBBC, with starts

    0, 1-b, d, 1/2-b, 1/2, 1/2+b.

All six intervals have length d and lie in the stated branches. Their shifts
close exactly. The nonzero intermediate displacements lie strictly between 0
and 1, proving primitive base period 6. One A visit forces collision period 14.

Starting with `(2d,2d+e)` gives BBCC, with starts

    2d, 1-3b, 1-2b, 3/2-3b.

These four length-e intervals likewise satisfy all branch inequalities and close
with no intermediate return. Their collision period is 4. In increasing order
the ten intervals have types P,P,Q,P,Q,P,Q,P,P,Q. Consecutive endpoints agree,
the first begins at 0, and the last ends at 1. Equivalently their total length
is `6d+4e=1`; here the endpoint identities, not just the measure sum, establish
disjoint exhaustive coverage. The remaining finite endpoint trajectories are
corner separatrices. The P cycle lifts once; the Q cycle lifts on both sheets
and those two cylinders pair under reversal. Thus there are exactly two
boundary regions, of periods 14 and 4.

The arguments use strict inequalities holding throughout the open band, so
irrational parameters require no finite approximations. The endpoints `b=1/6`
and `b=1/4` make e or d vanish and are not covered by this band theorem.
The earlier source's square-root parameters lie strictly inside the band and
therefore give its 14/4 example.

## 8. Generic minimality, all-period obstruction and word certificates

If `1,a,b` are Q-independent, the closed-orbit relation is impossible. A
one-sided chain joining true singular contacts would also give an integer
relation: the endpoint a,b coefficient differences are `(0,0)`, `(1,-1)` or
`(-1,1)`, while a nonempty chain adds nonnegative outer/inner counts with
positive sum. None can cancel. Thus there is no reflex saddle connection.
The connected genus-three leaf and the source's measured-foliation
decomposition theorem then give one minimal component. This inference uses
the theorem's saddle-connection boundary assertion; it does not assume a torus.

For any periodic orbit, a run of B visits increases the coordinate by b inside
an interval of length 1/2 without wrap. Its length is at most
`M=ceil(1/(2b))`. Splitting a cyclic word at its outer visits gives `n<=Mm`,
with `m>=1`. At the later-source parameters

    a=5/11+1/(22pi), b=5/11-1/(220pi),

the irrational coefficient forces `n=10m`, while `1/4<b<1/2` implies `M=2`.
The contradiction is independent of period. The printed relation `a+10b=5`
is therefore an explicit negative control against sufficiency of a Cayley-type
relation. The source's stronger minimality result uses its modified Keane
condition; the authored note accurately distinguishes it from the new
visit-count nonperiodicity proof.

The word certificate uses exactly the three open branch intervals and cumulative
translations reduced by integers. Its intersection inequalities ensure every
symbol and every wrap, while zero total displacement closes the orbit. Every
regular periodic contact has a neighborhood with the same finite word; hence
it supplies a positive-width certificate. A first zero-displacement prefix gives
the primitive contact return; the orientation/weight rule gives the true period.
Bounds `0<=N_j<=j` hold because each increment lies in `(0,1)` and the initial
coordinate lies in `(0,1)`. This verifies the logical characterization.
There is no stopping bound for absence of a further word. The proof correctly
does not use failed finite searches as evidence of all-parameter completeness.

## 9. True remaining gap

The unresolved original task is a terminating arithmetic decomposition for the
remaining irrational, rationally dependent parameters, including the location
and number of nonperiodic components. The current results leave:

- Minimal-component counts for general mixed rational/irrational lines, even
  when the existence and entirety of the periodic set are settled.
- Periodic-set and period classification for other positively dependent
  irrational pairs outside the complete families above.
- Region-count information for dependent irrational pairs where an elementary
  nonnegative-coefficient obstruction already rules out periods.
- A finite certificate that an unbounded word search has exhausted all
  periodic cylinders, together with a finite minimal-region certificate.

Rational arithmetic cannot simply be replaced by floating-point arithmetic:
irrational endpoint orbits need not close. A single integer relation does not
resolve these gaps. Other finite-arc domains are a separate extension, and the
confocal analog is not independently reproved here. These limits match a
substantive partial result, not a resolution of the originating Question 2.

## 10. Required correction: optional strict-corner statement

The original main-convention paragraph additionally said that excluding all corner
orbits leaves the periods and open periodic/minimal regions unchanged. The
claim about the decomposition is too strong. At the source pair `(1/4,1/6)`,
delete the convex-contact orbit at `x=1/24`; its four signed contact states are

    (1/24,0), (19/24,1), (1/24,1), (19/24,0).

The ambient period-6 cylinder has transverse interval `(0,1/12)`. The removed
orbit is the middle transverse value and cuts it into two cylinders. Therefore
the main-convention oriented periods `[5,5,6]` become `[5,5,6,6]` under strict
exclusion. Their reversal-paired boundary periods remain `[5,6]` in this
example, with the exceptional bouncing points removed. Every remaining orbit
keeps its original period.

The independent strip algorithm reproduces both counts exactly after adding
the convex orbit as a deleted cut. This is not an issue with a finite numerical
corner tolerance. [CORNER_CORRECTION.md](CORNER_CORRECTION.md) preserves the minimal replacement that
clearly confines all subsequent component counts to the main convention and
requires separate checks under strict exclusion.

**Original publication gate:** apply that correction and provide a fresh seal.
The frozen text was not unconditionally accepted as-is. This edition applies
the exact replacement to PROOF.md and seals that corrected proof separately;
the frozen author and audit packages remain unchanged. The correction changes
no accepted main-convention formula or result and does not enlarge the scope.
The complete counterexample remains in this audit and CORNER_CORRECTION.md.
The latter also writes out the reversal calculation justifying its already
audited boundary pairing. All subsequent region formulas and oriented-cylinder
counts use continuous convex-corner continuation; strict exclusion requires
separate component checks. The general irrational dependent classification
remains unresolved.

## 11. Verification evidence and exclusions

The author's full verifier passed in normal and optimized Python, with equal
substantive results. These runs were invoked through `run()` and their outputs
written only to the audit directory; the frozen files were not regenerated.
The independent program also passed in both modes and gives matching outputs
after deleting the mode field. All checks use explicit conditional failures,
so Python optimization does not remove them.

Independent evidence includes exact Euclidean geometry, all three source
permutation regimes, maximal-strip versus grid-component comparison, exact
required examples, and negative controls for the printed sign, omitted angular
orientation, omitted straight reflections, artificial auxiliary-cut splitting,
Cayley sufficiency and the optional corner-convention claim.

Finite tests are labeled corroboration throughout. All accepted universal
statements rest on the geometric or arithmetic arguments above. The original audit seal covered its reports, code, replay outputs and public-source metadata. This proof-only edition preserves the complete mathematical review and recorded aggregate checks, but distributes no programs, raw outputs or datasets. All finite checks in the original audit are historical supplementary evidence, not universal proofs. Edition preparation rechecked frozen byte identities, the exact required correction and publication integrity, and checked the newly explicit finite substitutions independently; it did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection or literature search. Copied source PDFs/text/images, private coordination material and repository/queue snapshots are excluded.

## Primary references

- Vladimir Dragović and Milena Radnović, *Periods of Pseudo-Integrable Billiards*,
  Arnold Mathematical Journal 1 (2015), 69–73,
  https://doi.org/10.1007/s40598-014-0004-0 .
- Vladimir Dragović and Milena Radnović, *Pseudo-integrable billiards and
  arithmetic dynamics*, arXiv:1206.0163v1 (1 June 2012),
  https://arxiv.org/abs/1206.0163v1 .
