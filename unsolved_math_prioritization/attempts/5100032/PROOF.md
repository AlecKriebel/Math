# A telescoping proof of focal antipedal invariant k603

**ID 5100032 / AMR-050-0032. Status:** complete proof candidate for the source's confocal-ellipse setting; independent review pending. Two substantive approaches used. No novelty or human peer-review claim.

## Exact theorem and source scope

Let the outer ellipse be

    E: x^2/a^2+y^2/b^2=1,       a>b>0,

with foci f_+=(c,0), f_-=(-c,0), c=sqrt(a^2-b^2). Let the inner caustic be the strictly nested confocal ellipse

    E_lambda: x^2/(a^2-lambda)+y^2/(b^2-lambda)=1,
    0<lambda<b^2.

Let P_1,...,P_N be a closed nondegenerate Poncelet billiard orbit between these two ellipses. For each edge P_i P_(i+1) and each focus f, let Q_f,i be the intersection of the lines through its endpoints perpendicular to P_i-f and P_(i+1)-f. Set q_f,i=|Q_f,i-f|. Then

    sum_i q_(+,i) = sum_i q_(-,i),                            (1)

so their ratio is1 for every such orbit, independently of N and the member of the Poncelet family.

This is invariant k603 in [Reznik–Garcia–Koiller, arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), Section3.5, Section3.7 and Table7, also Table7 in [the published companion](https://amj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf). The source introduction explicitly defines its elliptic billiard as a pair of confocal ellipses. Its antipedal construction is the intersection of the perpendicular supporting lines at consecutive polygon vertices, and q is an ordinary nonnegative distance. We do not substitute pedal feet, side lengths, areas or signed distances.

The proof covers simple and star Poncelet orbits following one oriented tangent branch of an elliptical caustic. It does not assert a hyperbolic-caustic or degenerate two-bounce extension. Those are not the nondegenerate confocal-ellipse pair defined in this source. Repeated traversal of a closed orbit simply repeats all summands. The circle limit has coincident foci and equality is immediate. No claim is made that either individual sum is itself constant.

## 1. A distance formula for antipedal vertices

Let A,B,f be noncollinear, put r=|A-f|, s=|B-f|, and let alpha be the angle between A-f and B-f. Translate f to the origin. The antipedal intersection Q satisfies

    Q dot (A-f)=r^2,       Q dot (B-f)=s^2.

Solving in an orthonormal basis with A-f=(r,0) gives

    |Q-f|^2=(r^2+s^2-2rs cos(alpha))/sin^2(alpha)
            = |A-B|^2/sin^2(alpha).

If h is the perpendicular distance from f to the line AB, the triangle area identity gives h=rs|sin(alpha)|/|A-B|. Therefore

    |Q-f|=rs/h.                                              (2)

This is a positive-distance identity, not a signed formula.

## 2. Consistent orientation and chord coordinates

Orient the Poncelet orbit so the inner ellipse lies to the left of every directed edge. Such a choice is consistent: at a vertex outside a strictly convex caustic the two distinct tangent lines give the incoming and outgoing billiard edges; continuing along the other tangent preserves the chosen side. Reversing the entire orbit handles the other direction. This is also the usual orientation of the Poncelet tangent map. Since the origin lies inside the caustic, it lies strictly to the left of each edge.

Parameterize one such edge as

    A=(a cos(s-delta), b sin(s-delta)),
    B=(a cos(s+delta), b sin(s+delta)),       0<delta<pi/2.

Indeed the directed central angle is in(0,pi), since det(A,B)>0. Set

    C=cos(s), S=sin(s), U=cos(delta), V=sin(delta),
    D=sqrt(C^2/a^2+S^2/b^2),       e=c/a.

The chord line has equation

    x C/a + y S/b = U.                                      (3)

Tangency to E_lambda gives its support-function identity

    U^2=(a^2-lambda)C^2/a^2+(b^2-lambda)S^2/b^2
       =1-lambda D^2,
    V^2=lambda D^2.                                         (4)

Moreover

    U^2-e^2 C^2=(b^2-lambda)D^2>0.                          (5)

Since U>0, both H_+=U-eC and H_-=U+eC are positive. Consequently the distances of the two foci to the chord are h_+=H_+/D and h_-=H_-/D. In particular the chord does not pass through either focus. Formula(2) is valid and every antipedal intersection is finite.

## 3. The per-edge telescoping identity

The focal distances of a point (a cos t,b sin t) are a-c cos t and a+c cos t. For sigma in{+1,-1}, write H_sigma=U-sigma eC. The product of the two endpoint distances from focus f_sigma is

    R_sigma=(a-sigma c cos(s-delta))
             (a-sigma c cos(s+delta))
           = a^2 H_sigma^2 + b^2 V^2.                       (6)

Using(2), (4) and (5), rationalize the last term to obtain

    q_sigma=D R_sigma/H_sigma
       =D [a^2 H_sigma + b^2 lambda D^2/H_sigma]
       =D [(a^2+b^2 lambda/(b^2-lambda)) U
             + sigma (-ac+(c/a)b^2 lambda/(b^2-lambda)) C].  (7)

Subtracting the sigma=-1 expression from sigma=+1 gives

    q_+ - q_- = (2c/a) D C [-a^2+b^2 lambda/(b^2-lambda)].   (8)

On the other hand the vertical displacement of the directed chord is

    y_B-y_A=2b C V=2b sqrt(lambda) D C.                      (9)

Thus every edge of the orbit satisfies

    q_+ - q_- = Gamma (y_B-y_A),                             (10)
    Gamma = c/(ab sqrt(lambda))
              [-a^2+b^2 lambda/(b^2-lambda)].

Crucially Gamma depends only on the fixed ellipses, not on the edge or its position. It may have either sign; this does not affect the positivity of the separate distances established above.

## 4. Closure and the invariant

Sum(10) over the cyclic sequence of orbit edges. Since P_(N+1)=P_1,

    sum_i (q_(+,i)-q_(-,i))
       =Gamma sum_i (y_(i+1)-y_i)=0.

All q values are positive and finite: in(2), the endpoint focal distances, the nonzero chord length and the focal height are positive. In particular the denominator sum is nonzero. This proves(1) and the claimed ratio1 for every admissible N. No low-period symmetry, numerical approximation or independent constancy of either sum is used.

## Verification and limits

`verify.py` uses rational Pythagorean ellipse axes and rational half-angle parameters. It solves the two antipedal line equations exactly, verifies their positive norms against(6)–(7), checks tangency and the focal-height identity, and checks(10) after removing common square roots. It tests 1,447 valid chords with 17,364 exact assertions. These are algebraic controls; the written argument proves the identity and closure for all real admissible parameters and all N.

The initial source audit and direct per-edge derivation are the two approaches recorded. No current primary general-N proof of this exact invariant was located in the targeted literature search, but novelty is not established. The argument is confined to the source's nested confocal ellipses and nonsingular antipedal construction. No external outreach or publication outside the authorized repository is implied.

Work used the inherited native runtime without model or reasoning-setting changes; its exact model identifier was not exposed to this worker.
