# PR110: independent algebraic adversarial review

## Result and exact scope

**No required or optional mathematical finding was identified.** The submitted
telescoping coefficient is correct. Its sign, its zero within the allowed
parameter interval, and its divergence at excluded boundary caustics do not
invalidate the proof. The ordinary positive focal antipedal distances are finite
for every edge of every admitted closed orbit. Their two sums are equal, and
their ratio is therefore 1.

This clearance concerns problem 5100032 / AMR-050-0032 and the complete original
`PROOF.md` authenticated at PR110 head
`3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35` (6990 bytes,
SHA256 `8478d2a792944c5fb9e8a53324e0c6bce8eba317de29c31a6fcbd6ca0205709d`).
It covers a nondegenerate closed Poncelet billiard orbit in a strictly nested
confocal **ellipse pair**, including self-intersecting orbits on a consistent
oriented tangent branch. It is conditional on closure; it does not claim that
every caustic parameter produces an N-periodic family for every N.

I read the complete original proof and source record before deriving the
identities. I did not read the submitted independent review, its reviewer code
or results, any other agent's mathematical review, or root mathematical
conclusions. I did not execute or import the author's verifier. The original
blob manifest was consulted only for provenance, not as mathematical evidence.
My mechanism uses an outward unit chord normal, the caustic support function,
and a direct solution of the two antipedal perpendicular equations. It is a
verification of the candidate rather than a fresh search for an unfinished
proof. Original effort remains 2/5; fresh central proof-search turns are zero.

This is not a novelty or priority clearance. No statement about the absence of
earlier proofs, or about the problem remaining open in 2026, follows from this
review. No native, Git, branch, remote, publication, tracker or external-contact
operation was performed.

## Primary statement and construction

I inspected the authenticated private originals of
[Reznik–Garcia–Koiller, arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11)
and [the 2021 published article](https://doi.org/10.1007/s40598-021-00174-y).
The arXiv title is *Eighty New Invariants in the Elliptic Billiard*; the published
title is *Fifty New Invariants of N-Periodics in the Elliptic Billiard*. Their
introductions define the billiard setting using two confocal ellipses. Section
3.5 defines antipedal vertices by consecutive perpendicular supports through
the original polygon vertices. Section 3.7 defines the starred q quantities
as ordinary Euclidean distances from the corresponding focus. Table 7's k603
row specifies the ratio of their sums, value 1, for all N. The original source
record's additional area and pedal notation supplies background definitions,
not extra requested conclusions for k603.

The relevant complete pages were read in extracted text: arXiv pp.1,6–9 and
published pp.341,347,349. I visually inspected arXiv Figure 3 on p.7 and the
published Table 7/Section 3.7 on p.349. The visual table confirms that the sums
refer to starred distances, not squared norms, side lengths or pedal feet.
The figure uses the standard antipedal support-line construction. The prose's
informal use of rays does not impose a new one-sided half-line convention.

The source record's phrase “confocal caustic” could be broader if isolated from
its cited source. The full primary introduction resolves that scope: this
review does not substitute a hyperbolic caustic theorem for the cited
ellipse-pair question. Both full PDFs remain private with the root. My temporary
copyrighted page renders are removed after inspection; extraction/render
process receipts and body hashes are retained without redistributing the
copyrighted primary bodies.

## Independent antipedal distance derivation

Translate a focus f to the origin. Let the line through two distinct endpoints
A and B have positive focal height h and orthonormal normal/tangent coordinates

    A-f = h n + alpha tau,     B-f = h n + beta tau,
    |n|=|tau|=1, n dot tau=0, alpha != beta.

Write Q-f = x n + y tau. The perpendicular line through A imposes

    h x + alpha y = h^2 + alpha^2,

and the line through B imposes the analogous equation with beta. Subtraction
and substitution give

    y = alpha + beta,     x = (h^2-alpha beta)/h.

Consequently

    |Q-f|^2 = (h^2-alpha beta)^2/h^2 + (alpha+beta)^2
             = (h^2+alpha^2)(h^2+beta^2)/h^2.

Taking the positive square root yields

    |Q-f| = |A-f| |B-f| / h.

There is no implicit signed distance in this step. For arbitrary f one would
use the absolute height; the ellipse-pair geometry below proves h>0 for both
foci. The antipedal determinant is (beta-alpha)h, so h>0 and A!=B also prove
existence and uniqueness of a finite intersection.

## Independent support-coordinate derivation

Let a>b>0, c^2=a^2-b^2, 0<lambda<b^2, and put

    M=diag(a^2,b^2),    n=(u,v),    u^2+v^2=1,
    H^2=a^2 u^2+b^2 v^2,          kappa=b^2-lambda>0.

The caustic support in outward direction n is

    rho=sqrt((a^2-lambda)u^2+(b^2-lambda)v^2)
        =sqrt(H^2-lambda)>0.

The chord line is n dot X=rho. Give it tangent direction tau=(-v,u), so the
origin and the complete caustic are strictly to the left of the directed chord.
Its ellipse midpoint and half-length are

    X0 = rho M n/H^2,       ell = ab sqrt(lambda)/H^2,
    A = X0-ell tau,         B = X0+ell tau.

To check this without the submitted half-angle calculation, substitute
X=X0+t tau into X dot M^(-1)X=1. The cross term vanishes because
X0 dot M^(-1)tau=rho n dot tau/H^2=0. The remaining terms are
rho^2/H^2 + t^2 H^2/(a^2b^2)=1, which gives t=±ell. Thus the chord is nonzero
because lambda>0.

For f_sigma=(sigma c,0), sigma=±1, the signed outward support height is

    h_sigma=rho-sigma c u.

The two heights satisfy the especially simple identity

    h_+ h_- = rho^2-c^2u^2
             = H^2-lambda-(a^2-b^2)u^2
             = b^2-lambda = kappa>0.

Since rho>0, this also gives rho>|cu|, hence h_+>0 and h_->0 individually.
It proves that both foci are on the inner side of every caustic tangent chord,
and that neither focus is on such a chord. In particular no absolute-value
branch can change within the permitted parameter range.

A point X=(x,y) on the outer ellipse has focal distance

    |X-f_sigma| = a-sigma c x/a >0.

Its square is the actual Euclidean squared norm, by the ellipse equation; the
unsquared expression is positive because |x|<=a and a>c. Let R_sigma be the
product of these distances at A and B. From the midpoint and half-length above,

    R_sigma = a^2 - 2 sigma c rho a^2u/H^2
                 + c^2 rho^2 a^2u^2/H^4
                 - c^2 b^2 lambda v^2/H^4
             = [a^2 h_sigma^2+b^2 lambda]/H^2.

For a checkable expansion of the last equality, subtract its right side and
multiply by H^4. Using rho^2=H^2-lambda, the difference becomes

    lambda [a^2H^2-a^2c^2u^2-c^2b^2v^2-b^2H^2]
      =lambda c^2[H^2-a^2u^2-b^2v^2]=0.

The independently established ordinary distance formula therefore gives

    q_sigma = [a^2 h_sigma+b^2 lambda/h_sigma]/H^2.

Since 1/h_sigma=(rho+sigma cu)/kappa,

    q_sigma = [(a^2+b^2lambda/kappa)rho
               + sigma c(-a^2+b^2lambda/kappa)u]/H^2.

Subtracting and using the actual chord's vertical displacement yields

    q_+ - q_- = 2cu[-a^2+b^2lambda/kappa]/H^2,
    y_B-y_A   = 2ab sqrt(lambda)u/H^2,

and thus

    q_+ - q_- = Gamma (y_B-y_A),
    Gamma = c[-a^2+b^2lambda/(b^2-lambda)]/(ab sqrt(lambda)).

This equals the submitted coefficient exactly. The derivation does not divide
by u or by the vertical displacement, so horizontal chords (u=0) and the zero
coefficient case are fully included. Gamma is dimensionless and invariant
under scaling all lengths by the same positive factor, while both distances
and the displacement scale by that factor.

## Orientation and closure

The formula fixes the common convention that the caustic lies to the left.
At each outer vertex the two caustic tangent chords are distinct. Traversing
one toward the vertex and leaving along the other preserves this same side
of the caustic. A usual elliptical Poncelet tangent-map orbit therefore has
this convention on every edge after possibly reversing the whole orbit.
Self-intersections between different edges change neither that local side
choice nor the computation. The calculation does not assume a simple polygon,
one turn around the origin, low N, or opposite-vertex symmetry.

For a cyclic sequence with P_(N+1)=P_1,

    sum_i(q_+,i-q_-,i)
      =Gamma sum_i(y_(i+1)-y_i)=0.

Every summand q_sigma is positive and finite, so the denominator sum is
strictly positive. The ratio conclusion follows without establishing that
either separate sum is invariant. Repeated traversal merely repeats the
summands. Reversing the orbit does not change the two sums; it changes the
oriented displacement convention, so it is essential to fix that convention
before applying the local coefficient. The submitted proof does so.

## Sign, zero and excluded limits

Gamma changes sign at

    lambda0 = a^2 b^2/(a^2+b^2),      0<lambda0<b^2.

Below it Gamma is negative, above it positive. At lambda0 it is zero and the
two focal antipedal distances are equal **edge by edge**. There is no need to
divide by Gamma in the proof. Positivity of each q_sigma follows from the
unrationalized height expression independently of this sign change.

For fixed eccentric axes, as lambda tends to 0 from above,
Gamma behaves as -ac/(b sqrt(lambda)). The edge displacement shrinks at rate
sqrt(lambda), so its product with Gamma has a finite limit. For a fixed normal,
q_sigma tends to a^2(H-sigma cu)/H^2>0. At lambda=0 the chord collapses and the
two antipedal equations coincide; a uniquely defined vertex is lost. The
submitted strict inequality excludes this case correctly.

As lambda tends to b^2 from below, Gamma behaves as cb^2/[a(b^2-lambda)].
For u!=0 one height tends to zero, and one focal antipedal distance diverges.
For u=0, both heights are sqrt(b^2-lambda), and both distances diverge together
at order 1/sqrt(b^2-lambda). No uniform finite boundary limit is asserted.
At the degenerate caustic itself some antipedal intersections fail to exist
because an edge passes through a focus. This is outside the admitted ellipse
pair, not an unhandled interior singularity.

The necessity of the parameter restriction can be exhibited exactly. On the
ellipse a=5,b=3,c=4 take A=(3,-12/5), B=(3,12/5). It corresponds formally to
lambda=16>b^2, so the height at the positive focus is -1. The actual positive
distances are q_+=169/25 and q_-=1369/175. Using the unmodified signed-height
formula would instead give -169/25 at the first focus. It therefore does not
prove a hyperbolic-caustic extension. The submitted theorem expressly excludes
that extension, and this negative control does not contradict it.

In the circle case a=b=R, c=0 the foci coincide. For 0<lambda<R^2 each edge
has rho=sqrt(R^2-lambda) and q_+=q_-=R^2/rho. Equality is immediate and no
singular eccentricity division is used. This statement is a coincident-focus
circle limit; simultaneous movement to a degenerate caustic need not have a
finite distance limit.

## Purposeful exact execution evidence

`independent_exact_controls.py` contains an independently written rational
quadratic-field implementation using the Python standard library only. It
solves the two perpendicular equations directly and checks squared norms;
positivity then identifies the ordinary norm. No floating-point search,
numerical tolerance, author code or reviewer code is used.

Fifteen deliberately chosen admissible cases cover both axis normals, all four
mixed-normal quadrants, both nonzero coefficient signs, its zero, a near-outer
and a near-degenerate caustic, uniform scaling, and coincident-focus circles.
They check actual outer endpoints, actual caustic tangency, positive focal
heights, both endpoint focal norms, product identities, the direct intersection
determinants, positive antipedal norms, rationalization and the displacement
identity. Negative controls reject the wrong coefficient sign, a missing
factor two, replacing distances with squared distances, both degenerate
boundaries, and the invalid signed-height continuation described above.

Normal execution used actual PID1080, from
2026-10-06T09:17:12.426337+00:00 to
2026-10-06T09:17:12.472209+00:00, exit0. Optimized execution used actual PID1081,
from 2026-10-06T09:17:12.473086+00:00 to
2026-10-06T09:17:12.522217+00:00, exit0. **Each passed 699 explicit checks,
15 curated admissible cases and 33 detected negative controls.** The explicit
exception-based checks remain enabled under -O. The two result payloads are
identical after removing their truthful PID/optimization metadata.

Exact argv, clean environment, resolved binary pin, UTC intervals, full
18341-/18340-byte stdout payloads, empty stderr streams, exits and stream
SHA256 hashes are retained in `EXACT_CONTROL_PROCESS_RECEIPTS.json` and the
adjacent mode-specific files. The interpreter body is SHA256
`b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf`.
The general-real proof above, rather than the finite controls, establishes the
identity for all allowed parameters and closure for arbitrary admitted N.

## Strongest verified result and remaining gap

The strongest verified mathematical result is the complete stated k603
identity for every nondegenerate closed orbit in the specified strictly
nested confocal ellipse pair, with ordinary positive distances and consistent
orientation, plus the coincident-focus circle equality. There is no remaining
mathematical gap within that theorem. No required repair or optional change
is requested by this mechanism's audit.

This mathematical clearance does not establish novelty or priority. A fresh
priority audit, publication preparation, full-package adversarial rounds and
any final integration remain the root's separate workflow. This review does
not authorise or attest to their completion. Hyperbolic or degenerate caustic
extensions are outside the primary scope reviewed here.
