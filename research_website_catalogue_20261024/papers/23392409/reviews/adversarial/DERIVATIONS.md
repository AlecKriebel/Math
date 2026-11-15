# Independent proof and exact-test freeze, before native/foreign science

The proof below certifies the manuscript's explicit Euclidean construction independently of its supplied checker/certificate. At this freeze the external definition/remark bodies and selected native program/results have not been read. Their convention/credit/reproducibility interfaces remain a separate, explicit gap to complete.

## 1. Validated arithmetic kernel

Every validity decision in `independent_gram_check.py` uses integer or Fraction arithmetic. For a nonnegative rational q and S=2^256, let k=isqrt(floor(q*S^2)). Then k^2<=q*S^2<(k+1)^2, unless the lower endpoint is exact. Thus k/S and (k+1)/S enclose sqrt(q); exact endpoints are retained when applicable. Applying this monotone enclosure three times encloses q^(1/8). The implementation additionally verifies nonnegative endpoints and the final exact rational inequalities lo^8<=q<=hi^8, including interval arguments via their endpoints.

Addition, negation and four-corner multiplication enclose all possibilities. Division is used only when its denominator interval excludes zero. Squares use zero as the lower bound precisely when the input crosses zero. Repeated powers use these outward operations. Lost dependence widens an enclosure; it cannot exclude the actual value. All boundary algebraic parameters are fixed unique roots throughout the calculation.

The explicit false controls reject a negative radical argument, a denominator crossing zero, an invalid interval order, a collinear focus Gram system, a noncrossing-embedding claim for the actual crossed boundary, and a wrong third-face constant. Arithmetic checks also cover signed multiplication, zero-crossing squares, zero/exact/rational/large radical arguments. No assertion disabled by optimization is used for validity.

## 2. Independent boundary isolation

For each T(q,h,ell), use t=1/2-r and V=r^2+h^2+1/4. Binomial expansion gives

(V+r)^8-(V-r)^8 = 16V^7r+112V^5r^3+112V^3r^5+16Vr^7.

The coefficients are twice the odd binomial coefficients of order eight. This polynomial is odd, strictly positive and strictly increasing for r>0, with positive derivative at zero. The actual ell values 1,lambda,1-lambda are positive, q is nonzero and h is nonzero. Hence every equation |q|^16*P(r)=ell has exactly one real root, that root is positive, and the corresponding t is unique. Exact endpoint signs enclose each r in(0,4); 160 dyadic bisections retain strict opposite polynomial signs. This is a centered positive-polynomial construction, avoiding subtraction of two huge near-equal values in the direct t expression.

Rational point coordinates from these three root intervals fall strictly inside every boundary box printed in the manuscript. A3's y coordinate equals b exactly. All15pairwise squared-distance enclosures have positive lower bound, and all20boundary-triple oriented-area enclosures exclude zero. The even determinant is exactly0.00132672; the odd determinant lies strictly in(6.37,6.39). The full rational enclosures and root endpoint evaluations are in `INDEPENDENT_RESULTS.json`.

## 3. Gram lift and count

For independent B,C, put alpha=B.B,beta=B.C,gamma=C.C,Delta=alpha*gamma-beta^2>0. For r1=alpha+u-v and r2=gamma+u-w, the unique coordinate lift has

|X|^2 = (gamma*r1^2-2beta*r1*r2+alpha*r2^2)/(4Delta).

Thus the Gram residual defined in the initial reconstruction equals the paper's norm residual, without implementing its coordinate expression. At a zero all three squared distances are the prescribed nonnegative eighth roots; taking eighth powers gives the exact original powered-distance equations. Conversely every real solution gives s=|X|^16 and this lift. Distinct s give distinct centers. Strict concavity gives the additional monotone x(s) injection and x(s)<b/2 at every finite s.

The independent exact enclosures lie strictly inside:

| s | G(s) |
|---|---|
|9/10000|(0.38,0.39)|
|11/10000|(-0.28,-0.27)|
|13/10000|(0.51,0.52)|
|1/2|(-0.91,-0.90)|
|1|(9,10)|
|10^16|(-4.766,-4.765)|

Continuity on each of the five disjoint finite intervening intervals gives at least one root in each. The independent code retains opposite endpoint signs through80rational bisections per interval. These refinements are not uniqueness claims. The resulting five x-coordinate boxes are disjoint and increasing; all lie strictly left of b/2.

As a second tail mechanism, concavity bounds the two tiny radical differences at10^16 and gives the paper's direct rational x/y boxes. Their squared norm minus100 is strictly in(-4.766,-4.765). The rational limiting norm identity39007985196121/409600000000 is checked exactly. This tail proof does not rely on subtracting rounded large roots or treating infinity as a center.

## 4. Incoming existence for the same boundary

The independently isolated fixed boundary defines L=|B-A5|^16-|B-A3|^16 and M=|A1|^16-|A3|^16. Both have strict positive lower bounds. Apply the same Gram lift after translation by A3, with B'=A5-A3 and C'=A1-A3. The Gram determinant is strictly positive. All radical arguments stay positive on[1/100,11/1000], so the actual residual of these fixed constants is continuous.

Independent enclosures give H(1/100) strictly in(0.00037,0.00038) and H(11/1000) strictly in(-0.00081,-0.00080). An actual root therefore exists. The entire image of the retained parameter interval is enclosed strictly inside(0.1677,0.1717) x(-0.0036,-0.0026). Coordinate evaluation uses Gram dual vectors with their common u coefficient combined first. This is an independent expression structure retaining a shared-variable dependence, not a choice of new boundary values.

The whole incoming box is strictly right of b/2, so it is separate from all five selected outgoing boxes. Every incoming-boundary squared-distance interval is positive. Every selected incoming/outgoing box has strict nonzero oriented area with each of the15boundary-pair lines:90exact line tests in total. Therefore every selected center is distinct from every boundary vertex, and no three vertices of any selected face are collinear. These are direct finite conditions for these particular witnesses, not a claim about every solution of the polynomial equations.

## 5. Exact face identities and fixed-boundary quantifiers

The unique boundary-root equations imply the exact six edge powers(a,f,f+lambda,g,g+1-lambda,a+1). Their alternating sums agree. Define r1=r3+a-f and r5=r3+g-f-lambda from the incoming lift, and qB=qA+lambda,qC=qA+1 from the outgoing lift. Substitution gives all three incoming and all three outgoing face identities.

The independent checker represents each side as an integer coefficient vector in seven formal generators(a,f,g,lambda,1,r3,qA). All six differences are identically zero. A deliberately changed third-face constant is rejected. No equality is inferred from a numerical enclosure merely containing zero. No flip-existence theorem or repeated numerical re-selection of a boundary is needed.

Consequently one fixed algebraic sextuple supports the incoming witness and all five outgoing witnesses simultaneously. Boundary roots are algebraic by their nonconstant rational polynomials and unique isolating intervals. The lower-bound count does not assume exact root counts, simplicity, or uniqueness of an incoming center.

## 6. Crossing and precise limitation

The four independently certified orientation signs are(-,+,+,-), for the two specified boundary segments. Each pair has strict opposite signs; neither collinearity nor endpoint contact can explain them. Hence the boundary has a strict interior crossing. No center choice makes that fixed boundary a proper embedding. The raw Euclidean construction is thus verified, but its claimed connection to the cited crossing-permitted realization convention still requires direct primary-interface reading after this freeze.

The five displayed decimal center approximations, if used later, are only reader orientation; they do not decide signs or validity. The exact rational boxes are the checkable artifact. No exact total, universal maximum, alpha<1 result, historical firstness or current open-status conclusion is drawn.

## 7. Reproduction and remaining gap at this freeze

Actual independent normal and optimized runs both exit0 with empty stderr and byte-identical complete131777byte output. The code imports only the standard library and no supplied program, expected certificate, foreign scientific text or peer/root result. All target conditions above were decided by rational interval or exact coefficient identities.

The original native checker/certificate, actual primary definition/remark/question and weighted-distance credit interfaces remain unread at this freeze. Their audit and the sole-owner bounded native replay are next. These are explicitly separate requirements before the final scientific disposition. Root130 remains CLOSED and scientific findings remain withheld.
