# Independent adversarial audit: analytic and smooth-flow mechanism

**Verdict: PASS within the analytic scope below. No analytic gap or
counterexample found.** The construction in the pinned `PROOF.md` gives actual
orientation-preserving smooth diffeomorphisms on a one-holed torus, equal to
identity on a common boundary collar, and satisfying the braid relation exactly.
It extends smoothly with compact support to any oriented ambient surface once
the labeled one-holed-torus model is identified with the prescribed neighborhood.
The conclusion about the *prescribed twist mapping classes* also needs the
separate capping/central-offset argument in §§1,4 of the manuscript; this analytic
review does not substitute for its independent topological audit.

Pinned proof SHA-256:
`f00fb3ff79fbbe02b35c62ff8269d4bd49a01120e980bfc8ea33361fd6cca16d`.
Supplied PR head: `e1a11feef98ed0fde22375c983e30b72b268d265`.
This reviewer did not open the old `MATHEMATICAL_AUDIT.md` conclusions. The
derivations below were made directly from the proof, and the supplied manifest
and bibliography were treated as data rather than mathematical authority.

## 1. Exact target, dependencies, and success criteria

The bounded target is to validate §§2–3 and the smooth-transfer portion of §5:

1. Construct a globally defined smooth torus diffeomorphism `h`, isotopic to
   identity through maps fixing 0 and commuting with the antipodal involution.
2. Prove `h=P` on a *specified neighborhood*, including enough control to
   identify `h^-1` at the arguments needed for the conjugacy.
3. Prove `x=q`, `y=h r h^-1` obey `x²=y³=iota` globally and are actual prescribed
   rotations throughout one common invariant disk.
4. Prove the cutoff rotations `f_theta` form a globally commuting smooth flow,
   including their inverses and the complement of the disk.
5. Prove actual-map identities `X²=Y³`, `ABA=BAB`, `(AB)^6=f_(2pi)`, and a common
   identity disk, without identifying a mapping class or sampling an ODE.
6. Restrict to the punctured model, conjugate to a compact neighborhood, and
   extend by identity with no smoothness loss or support at the boundary.

The standard analytic theorem used is smooth existence, uniqueness, smooth
dependence, and invertibility for a smooth time-dependent vector field on a
compact smooth manifold over a compact time interval. No empirical assumption,
numerical approximation, branched-cover regularity, or limiting flow is needed.
The surface is oriented and the target pair has a one-holed-torus regular
neighborhood. The separate topological audit must verify exact twist classes,
twist handedness, the capping kernel, and the two-chain relation.

## 2. Cutoff and global path-flow: no singular denominator

Write `E(u)=exp(-1/u)` for `u>0`, and `E(u)=0` for `u<=0`. Repeated derivatives
from the right are polynomials in `u^-1` times `exp(-1/u)` and tend to zero at
0. Thus `E` is smooth and flat at 0. For `a<b`,

`K_(a,b)(s)=E(b-s)/(E(b-s)+E(s-a))`.

At least one of `b-s`, `s-a` is positive for every real `s`; otherwise one would
have `s>=b` and `s<=a` simultaneously. The denominator therefore never vanishes.
Both endpoint joins are smooth because the denominator remains positive there
and the vanishing numerator term is flat. The profile equals 1 for `s<=a` and
0 for `s>=b`, with values in [0,1]. Dependence on `|z|²` rather than the polar
radius removes any possible nonsmoothness of the radial coordinate at 0.

For `c=sqrt(3)/2-1` and `d(t)=1+c t`, the path and its velocity matrix are

```
P_t = [[1,-t/2],[0,d(t)]],
(dP_t/dt) P_t^-1 = [[0,-1/(2d(t))],[0,c/d(t)]].
```

Since `sqrt(3)/2 <= d(t) <= 1` for `0<=t<=1`, the displayed matrix has no time
singularity. It extends smoothly a little beyond the closed time interval.
Multiplying by `kappa(|z|²)` gives a smooth field in the embedded radius-1/4
coordinate disk. It is identically zero on the open annular region outside
radius 1/16, well before the coordinate boundary. Extension by zero to the
torus is consequently smooth, not merely a continuous patching.

Compactness of the torus supplies the complete evolution from time 0 through
time 1. In particular every `h_t` is a smooth bijection with a smooth inverse
given by evolution back to time 0. One must not identify this inverse with
`h_(-t)` for an arbitrary nonautonomous field; the manuscript does not do so.
The Jacobian determinant of the evolution is
`exp(integral div(W_s)(h_s(z)) ds)>0` in oriented local coordinates. The
evolution is therefore orientation preserving. The field vanishes at 0 and
off the support disk, so those points are fixed for the whole interval.

The standard torus antipodal map preserves the coordinate disk, and the field
is odd there: `W_t(-z)=-W_t(z)`. Outside the disk the extended field is zero and
the antipodal image also lies outside. Hence the vector field is globally
equivariant under the antipodal involution. Uniqueness applied to the two
evolutions starting at `z` and `-z` yields `h_t iota=iota h_t` everywhere. No
radiality of `h_t` is asserted or required.

## 3. The exact local formula and its inverse

The Frobenius bound in the proof is valid for every time, not only at its
endpoints:

`||P_t||_F² = 1+t²/4+d(t)² <= 1+1/4+1 = 9/4`.

Thus `||P_t|| <= 3/2 < 2`. If `|u|<=1/64`, then
`|P_t u| <=3/128 <1/32` for the *entire* trajectory. Throughout this trajectory
the cutoff is 1, and

`d(P_t u)/dt = (dP_t/dt)P_t^-1(P_t u)=W_t(P_t u)`.

It has the required initial point because `P_0=I`. Uniqueness gives
`h_t(u)=P_t u` there, and in particular `h(u)=Pu`. This proves the local formula
using an exact candidate trajectory and a uniform enclosure. There is no
inference from closeness of computed trajectories.

The independent exact matrix check gives

```
P^-1 = [[1,1/sqrt(3)],[0,2/sqrt(3)]],
||P^-1||_F² = 8/3 <4,
||R||_F² = 3 <4,
P R P^-1 = [[1/2,sqrt(3)/2],[-sqrt(3)/2,1/2]].
```

For `|z|<=1/512`, let `u=P^-1 z`. The bound `|u|<2/512=1/256<1/64` ensures
`h(u)=Pu=z`. Since the *global* map `h` is injective and onto, this proves the
identity `h^-1(z)=P^-1z`; it is not a heuristic inversion of an unspecified
local formula. Next,

`|R u| <4/512 =1/128 <1/64`,

so `h(Ru)=PRu` as well. Consequently
`y(z)=h r h^-1(z)=PRP^-1z` throughout the entire common disk. The argument of
the linear torus map `r` is small, and its image has norm below 1/64, so these
coordinates do not cross a lattice identification. There is no hidden wrap
around the torus. The verifier also establishes the stronger exact identity
`||R P^-1||_F²=8/3`, but the manuscript's looser product estimate already suffices.

The matrix `Q` is clockwise pi/2 rotation. The displayed conjugate of `R` is
clockwise pi/3 rotation. They preserve the radius-1/512 disk and every
concentric smaller disk setwise, including their boundaries.

## 4. Common finite power: an actual global identity

Exact matrix multiplication yields `Q²=R³=-I`, `Q⁴=R⁶=I`. Thus `x²=iota` on
the whole torus. By conjugacy,

`y³=h r³ h^-1=h iota h^-1=iota`.

The last equality uses the established global equivariance of the path-flow.
It does not follow merely from `h=P` near 0. This verifies the most important
global analytic dependency before any cutoff correction is introduced.

## 5. Radial cutoff maps: all smoothness and commutation details

Let `lambda=K_((1/2048)^2,(1/1024)^2)`. In the common disk, the map is the
Cartesian formula

`f_theta(z) = cos(theta lambda(|z|²)) z + sin(theta lambda(|z|²)) Jz`,

where `J` is counterclockwise pi/2 rotation. This formula is smooth at the
origin and everywhere else. Near the origin, `lambda=1` and it is an ordinary
rotation. For radii at least 1/1024 it is the identity on an open neighborhood
of the boundary of the radius-1/512 coordinate disk, so extension by identity
is smooth. Endpoint flatness is already supplied by the cutoff proof.

Radius is preserved exactly. Hence applying `f_phi` does not change the value
of `lambda` in the subsequent application of `f_theta`, giving

`f_theta f_phi=f_(theta+phi)`, `f_theta^-1=f_(-theta)`.

Both sides are smooth global maps. The parameter gives an isotopy from
identity, so these are orientation-preserving diffeomorphisms. Equivalently,
away from 0 the polar-coordinate differential is triangular with determinant
1; the Cartesian formula handles 0.

For either `g=x` or `g=y`, global commutation follows by two exhaustive cases.
If `z` is in the common disk, all maps in the two compositions are the specified
constant-angle or radius-dependent rotations, which commute and stay in the
disk. If `z` is outside, disk preservation and global bijectivity imply that
`g(z)` is outside as well. Thus `f_theta(z)=z` and `f_theta(g(z))=g(z)`, so the
compositions agree there. The boundary is handled by the same local rotation
formula (or by continuity). In particular no point outside can be transported
into the cutoff support. This is a genuine global proof, stronger than a
check of the formula on the transition annulus.

## 6. Exact cancellations, powers, and common identity collar

Set `X=f_(pi/2) x`, `Y=f_(pi/3) y`. The preceding global commutation and group
law imply

```
X² = f_pi x² = f_pi iota,
Y³ = f_pi y³ = f_pi iota.
```

For `|z|<=1/2048`, the counterclockwise corrections cancel the clockwise local
rotations pointwise. Thus both maps are literally identity on this entire
disk, as are their inverses. Remove the open radius-1/4096 disk. Its complement
`N` is preserved because the removed disk is pointwise fixed and the maps are
bijections. The annulus `1/4096 <= |z| <1/2048` is a common open boundary collar
on which both restrictions and all their products/inverses are identity.

For `A=Y^-1 X`, `B=X^-1 Y²`, the complete algebra, composing right to left, is

```
AB = Y^-1 X X^-1 Y² = Y,
ABA = Y Y^-1 X = X,
BAB = X^-1 Y² Y^-1 X X^-1 Y² = X^-1 Y³ = X.
```

Only the final equality uses `Y³=X²`. No illicit commutation of `X` and `Y`
occurs. The sixth power is

`(AB)^6=Y^6=f_(6pi/3) y^6=f_(2pi)`.

The right side is generally a nonidentity map in the transition annulus.
It is identity on both constant-profile sides because those rotations are
integer full turns. Its relative-boundary annular winding has absolute value
one. The sign and its comparison to the chain relation belong to the separate
mapping-class audit. This proof correctly does not simplify `f_(2pi)` to
identity globally.

Simultaneously inverting `A,B` preserves the braid relation by taking the
inverse of both sides of `ABA=BAB`. It also preserves the common identity
collar. This analytic normalization is valid if the separate twist-sign audit
requires the simultaneous inverse.

## 7. Transfer and boundary cases

Given the orientation-preserving smooth identification `j:N->M` of the labeled
regular-neighborhood model, conjugation preserves smooth invertibility,
orientation, the braid identity, and a common identity collar of `partial M`.
Extension by identity is smooth because on an *open* neighborhood of that
boundary both definitions are already the same identity map. The inverse
extends by the identical construction. There is no derivative matching problem
and no singular point requiring a smoothing theorem.

As `M` is compact and a boundary collar is fixed, the closure of the nonidentity
locus is a compact subset of `int(M)`. Hence support is compact in the stated
interior. This works in an ambient noncompact surface too, provided the compact
regular neighborhood is disjoint from its marked points, punctures, and
boundary. A sufficiently small choice has exactly that property. Negative
Euler characteristic of the ambient surface does not alter the local analytic
construction. The auxiliary torus is not the final ambient answer.

No nonorientable-surface statement is validated here: the hypothesis used in
the theorem is an oriented surface (or, equivalently for the construction, an
oriented one-holed-torus neighborhood with compatible twist choices). The
original question uses right twists in a mapping-class-group context, and the
manuscript explicitly describes its usual oriented interpretation.

## 8. Adversarial controls and reproducibility

`verify_exact.py` is an independent standard-library checker. It uses exact
rational arithmetic and an explicitly implemented quadratic field
`Q(sqrt(3))` for matrix equalities and norm squares. It also reduces group words
in `C4 *_(C2) C6` with an independent central additive cutoff-angle parameter.
This universal calculation checks the exact algebra assuming the analytically
proved commutation; it cannot certify that a particular smooth flow has that
property. Results are saved in `RESULTS.json`.

The adverse controls are mechanisms that would genuinely invalidate shortcuts:

- **A full cutoff turn is not globally identity.** In the transition annulus
  continuity supplies a radius where `lambda=1/2`, at which `f_(2pi)` is a
  half-turn. The formal checker retains this nontrivial parameter.
- **The correction angles matter.** Replacing the correction for `y` by pi/2
  makes its near-origin corrected map a counterclockwise pi/6 rotation, while
  corrected `x` remains identity. Then near 0 the putative two braid words are
  identity and pi/2 rotation, so the actual relation fails. The exact checker
  independently detects the mismatched powers and braid words.
- **Support alone does not prove global commutation.** A four-point permutation
  example has `f` supported in `D={0,1}`, identity outside, and `g` carrying
  that set to its complement. It fails commutation. The manuscript avoids
  this failure by proving disk preservation before making its global claim.
- **Local linearization alone does not prove the global common power.** Without
  oddness/equivariance, `h iota h^-1` need not equal `iota`. The cutoff field
  actually has the required global symmetry. No stronger property, such as
  `h` itself being radial, is presumed.
- **A merely local inverse is insufficient.** The explicit input norm bounds
  and global injectivity were checked separately. Both `P^-1z` and
  `RP^-1z` remain strictly inside the region of known equality; all radius
  inequalities retain substantial slack at their closed endpoints.

The checker ran successfully with Python 3, without third-party packages,
floating-point arithmetic, ODE samples, generated large files, or external
contacts. The analytic arguments remain independently checkable from this
report without executing the checker.

## 9. Primary-source scope check and limitations

Freshly inspected [publisher PDF](https://ems.press/content/serial-article-files/46762?nt=1),
physical page 53 / printed 2527, confirms that Problem 9 asks for lifts of two
respective right Dehn twists about essential curves crossing once to actual
homeomorphisms, then to once and r-times continuously differentiable
homeomorphisms satisfying the braid equality. Its ambient condition is
negative Euler characteristic. The smooth construction, conditional only on
the separately audited identification of twist classes, addresses these
regularity questions on the manuscript's oriented-surface scope. Both maps and
inverses are smooth, so either common interpretation of differentiable
homeomorphism is covered. It does not promise all additional relations of the
ambient mapping-class image or a section of its entire mapping class group.

The source PDF was separately fetched into memory for a byte hash, not saved
to disk. Its 562604 bytes have SHA-256
`0bd596abb171c94b1ff9352fba8f2a2cf91e12dd29180590ce2425054ea17de7`, agreeing
with the pinned source metadata. The original page was also opened via the
browser's PDF screenshot facility; no screenshot file was retained.

No priority search, novelty certification, human peer review, formal proof
assistant certification, or re-audit of the historical literature is claimed.
Mann–Tshishiku is explicitly credited in the supplied manuscript; this reviewer
does not infer priority from the present analytic success. No external outreach,
PR modification, git commit, push, publication, or release was performed.

**Strongest independently verified result:** the smooth-flow/radial-cutoff
mechanism establishes exact compactly supported smooth braid lifts on the
one-holed-torus model and smooth transfer. **Remaining gap within this
analytic mechanism: none found.** **Dependency outside this report:** verify
the exact prescribed mapping classes by the independent topological audit.
