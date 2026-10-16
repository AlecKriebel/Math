# Origin-pedal times origin-antipedal area: k403,a

**5100020 / AMR-050-0020. First-turn full candidate, independent review pending.** The proof gives the exact odd-period source invariant. Classical canonical coordinates and Jacobi identities, and the earlier campaign origin-pedal mechanism, are credited. No historical-priority claim is made.

## 1. Exact theorem and real domain

Let E be an ellipse with semiaxes a>=b>0 and center O. Fix a strictly nested nondegenerate confocal elliptical caustic. Let a billiard family have least period N>=3 odd, and winding tau with gcd(N,tau)=1. Primitive star traversals are allowed. Let A_O be the signed area of the perpendicular feet from O to consecutive **original orbit** supporting lines. Let A*_O be the signed area of consecutive intersections of the lines through the original orbit vertices P_i perpendicular to P_i−O. Then

                             A_O A*_O is constant.                           (1)

Both polygons are unprimed. They are not the corresponding constructions from the outer tangent polygon or inner caustic-contact polygon. This is arXiv2004.12497v11 Table5 p7 and the unchanged row in the final companion Table5 p348. All areas use the source's signed cross-product convention. Every antipedal intersection is finite in this setting, as proved below. Zero signed areas are allowed because (1) is a product, not a quotient. Hyperbolic or collapsed caustics and parity obtained only by repeating an orbit are not asserted.

Translate O to zero. Reversing the orientation reverses both signed areas and leaves their product unchanged. We may therefore take 0<tau<N/2.

## 2. Canonical coordinates and elementary Jacobi facts

First assume a>b. Write alpha>beta>0 for caustic semiaxes, k=sqrt(alpha²−beta²)/alpha and k'=beta/alpha. All Jacobi functions have modulus k. Let K,K' be its real and complementary complete elliptic integrals, p=iK', and choose

v=2K tau/N, delta=2v,
a=alpha dn(v)/cn(v), b=beta/cn(v),
P(w)=(-a sn(w), b cn(w)),     P_i=P(w+i delta).                              (2)

These are Stachel's published Theorem4.3 and equation4.9, with the least-period condition explicit. They give a²−b²=alpha²−beta² and N delta=4K tau. In particular 0<v<K.

We use the standard Jacobi identities, tabulated in DLMF22.4 and22.8. The functions sn,cn,dn have simple poles at

                         2rK+(2s+1)p,     r,s integers.

The zeros of dn are K+p and their translates by2K and2p. Their half-period transformations are

sn(z+2K)=-sn z,  cn(z+2K)=-cn z,  dn(z+2K)=dn z;
sn(z+2p)=sn z,   cn(z+2p)=-cn z,  dn(z+2p)=-dn z.                            (3)

Sn is odd, cn and dn even. The shifts by p include sn(p+z)=1/(k sn z), cn(p+z)=-i dn z/(k sn z), dn(p+z)=-i cn z/sn z. These also fix pole/zero multiplicities used below. Scalar products in the complex continuation are bilinear sums of coordinate products, without complex conjugation.

Put s=sn v, c=cn v, d=dn v and

D(u)=1−k²s²sn²u.

The addition formulas give the chord identity

B(u):=det(P(u−v),P(u+v))=2ab s c dn(u)/D(u).                                 (4)

For real u, dn(u)>0 and D(u)>=1−k²s²>0, so B(u)>0. Thus consecutive real vertex vectors are never parallel, and all lines P_i dot X=|P_i|² defining the origin antipedal have unique finite consecutive intersections. The original chord is also a genuine line, so its pedal foot exists.

Modulo the real and imaginary congruences2K and2p, the complete divisor information for B is as follows:

- Simple poles at u=p+v and p−v, where exactly one endpoint P(u−v) or P(u+v) has a simple pole
- Simple zeros at u=K+p, where the two finite endpoints coincide
- Simple zeros at u=p, where the two finite endpoints are opposite.

The last item is essential: dn has a simple pole there but D has a double pole, giving a simple zero of their quotient. At K+p, D=c² is nonzero. The roots D=0 are p±v; they are simple because the p-shift formulas and 0<v<K make the relevant derivatives nonzero. At these roots dn is finite and nonzero. This exhausts the possible poles and zeros in (4). Endpoints at the two zero types are finite since v is strictly between0 andK.

## 3. A two-pole cyclic elliptic function

Set ell=2K/N and

                         S(w)=sum_(j=0)^(N−1) dn(w+j delta).                  (5)

Because N is odd and gcd(N,tau)=1, the residues j delta modulo2K exhaust the subgroup of orderN, and delta/ell=2tau is relatively prime toN. Thus S has periods ell and4p and anti-period2p. It is even by reindexing j to−j. On the compact torus

                         X=C/(ell Z+4p Z),

S has exactly two simple poles at p and3p. At p only one index contributes a pole modulo2K; its residue is nonzero. Periodicity identifies all translated poles, and the anti-period gives the opposite residue at3p. No cancellation can remove these poles.

Evenness and the two period characters force S(p+ell/2)=0: negating that argument and then adding ell+2p returns it, changing the value's sign. The same holds at3p+ell/2. Neither is a pole. The equality of total zero and pole orders on a compact torus shows that these are precisely its two simple zeros. Consequently

                     S(w)S(w+ell/2) is constant.                            (6)

The product has no poles after its zero/pole divisors cancel, hence is a holomorphic function on a compact torus. This is a classical elliptic-function argument. On the real axis S is positive.

We will also use this immediate uniqueness fact: a meromorphic function on X with at most simple poles at p,3p and anti-period2p is a scalar multiple of S. Match the residue at p, use the anti-period to match the other residue, and subtract. The remainder is holomorphic and therefore constant; its anti-period makes that constant zero. The same holds after a fixed argument shift.

## 4. Exact rational formula for the antipedal area

For complex vectors P,Q write H(P)=P dot P and, where det(P,Q) is nonzero, define

F(P,Q)=[H(P)H(Q)−(H(P)+H(Q))(P dot Q)/2]/det(P,Q).                            (7)

If R_i is the intersection of the lines P_i dot X=H(P_i) and P_(i+1) dot X=H(P_(i+1)), the signed area of the antipedal polygon is

                          U(w)=sum_i F(P_i,P_(i+1)).                        (8)

Here is a direct proof not involving square-root normalizations. Let J(x,y)=(-y,x), h_i=H(P_i), c_i=det(P_i,P_(i+1)), and d_i=P_i dot P_(i+1). Then

R_i=P_i+[(h_(i+1)−d_i)/c_i] J P_i,
R_(i−1)=P_i−[(h_(i−1)−d_(i−1))/c_(i−1)] J P_i.

These satisfy both relevant line equations. Taking det(R_(i−1),R_i), summing and dividing by two gives (8), with the two contributions from each edge combining into (7). The identity is algebraic and remains true for the meromorphic continuation. It does not require a convex derived polygon or a nonzero derived area.

The symmetries of F are

F(Q,P)=-F(P,Q),     F(-P,-Q)=F(P,Q).

A simultaneous reflection diag(1,-1) of both arguments reverses F, since it preserves dot products and reverses determinants. It follows from (2)–(3) and cyclic reindexing that U is periodic2K and delta, hence periodicell, and anti-periodic2p. It is meromorphic on X.

## 5. All antipedal poles, including the parity-sensitive type

There are three issues to check in the cyclic sum (8).

### 5.1 Coincident finite endpoints give removable singularities

At a zero of B with midpoint u=K+p, P(u+v)=P(u−v). To see this, use the parity/shift identity P(2(K+p)−z)=P(z). If P,Q are nearby finite vectors, the numerator in (7) equals

[(H(P)+H(Q)) H(P−Q)−(H(P)−H(Q))²]/4.                                      (9)

When Q−P=O(z), this is O(z²). The denominator has a simple zero by(4), so the singularity is removable. No assumption about the nonvanishing of an individual complex squared norm is required.

### 5.2 Opposite finite endpoints give possible simple poles

At midpoint u=p, one has P(p−v)=-P(p+v). Formula(4) gives a simple zero of the denominator; both endpoints are regular. Hence (7) has at most a simple pole there, which generally is genuine. Discarding this pole would be wrong.

In the cyclic variable w these possible poles have classes p−v−j delta and3p−v−j delta. Since v=tau ell for odd N, they coincide on X with p and3p. This is the precise place odd period enters the antipedal argument. For even period, the midpoint classes may be distinct from the vertex classes; no all-parity proportionality is claimed.

### 5.3 Double poles at vertices cancel between adjacent edges

At w=p−i delta, the vertex P_i has a simple pole and its two neighbors are regular. The denominator of each incident F term has a simple pole by(4). Its numerator has order at most three, so a single term has at most a double pole.

Set the pole vertex to P(p+z), and let

G(z)=F(P(p+z),P(p+delta+z)).

From (3) and parity, P(p−z)=-P(p+z), and
P(p−delta+z)=-P(p+delta−z). The two incident edge terms therefore sum exactly to

                             G(z)−G(−z).                                  (10)

The even negative Laurent powers cancel. Since G has order at most two, (10) has order at most one. The argument applies at every translated pole. For odd N, the vertex-pole indices are distinct modulo the real period2K, so no incident term has two pole endpoints. The possible opposite-endpoint term from5.2 at the same quotient phase still has only a simple pole and is already covered.

By the complete divisor classification(4), there are no other possible singularities. Thus U has only the two allowed simple-pole classes p,3p on X. The uniqueness fact after(6) proves

                             U(w)=c_* S(w).                                (11)

The scalar c_* is real by evaluation on the real axis and may be zero. This conclusion is restricted to the odd-period setting used above.

## 6. The origin-pedal factor, restated self-contained

This section restates the previously reviewed campaign mechanism from5100012/k203,b ([PR204](https://github.com/AlecKriebel/Math/pull/204)), with its classical canonical-coordinate and Jacobi inputs credited. It is not an independent new derivation of that earlier campaign claim and no new priority is asserted.

The chord through P(u−v),P(u+v) is the caustic tangent

n(u) dot X=1,      n(u)=(-sn(u)/alpha, cn(u)/beta).

Substitution of the two endpoints using addition formulas verifies the equation; the contact point (-alpha sn u,beta cn u) lies on it. Its origin foot is

Q(u)=n(u)/(n(u) dot n(u))
    =(-alpha k'^2 sn(u)/dn²(u), beta cn(u)/dn²(u)).                           (12)

For real u this denominator is positive. Define

T(u)=(1/2)sum_j det(Q(u+j delta),Q(u+(j+1)delta)).

The actual original-orbit pedal area is A_O(w)=T(w+v).

At common poles of sn,cn,dn, Q is holomorphic and vanishes. Its only possible poles are the zeros of dn at r=K+p and translates, with order at most two. Parity and shifts give

sn(2r−z)=sn z, cn(2r−z)=cn z, dn(2r−z)=-dn z,
so Q(2r−z)=Q(z).

Hence Q(r+z) is even. At a pole vertex the two incident area terms combine as

(1/2)det(Q(r+z), Q(r+delta+z)−Q(r−delta+z)).

The first vector is O(z^(-2)); the second is O(z) because the neighboring values agree at z=0 and are regular. Neighbors cannot also be poles since0<delta<2K. Thus T has at most simple poles, not double ones.

Moreover Q(u+2K)=-Q(u), while Q(u+2p)=diag(1,-1)Q(u). Its cyclic area is therefore2K-periodic, delta-periodic and2p-antiperiodic, just as required. On X its only possible simple poles are r,r+2p. The shifted S(u+K) has exactly those poles with that anti-period, because p−K and p+K differ by2K. The same uniqueness argument yields

                         T(u)=c_p S(u+K),                                 (13)

with real c_p, possibly zero.

## 7. Product, circular case and all domain qualifications

Equations(11) and(13) give

A_O(w) A*_O(w)=c_p c_* S(w+v+K) S(w).

Since (v+K)/ell=tau+N/2 is a half-integer for odd N, real periodicity and(6) prove(1). No division by a polygon area is used. In particular, if either scalar vanishes, the product is the constant zero and the argument remains valid.

When the outer ellipse is a circle of radiusR, the family consists of rotations of the regular primitive N-star with step angle theta=2pi tau/N in(0,pi). The origin pedal is a rotated regular star of radiusR cos(theta/2), and the antipedal is a rotated regular star of radiusR/cos(theta/2). Their signed area product is

                          (N² R^4/4) sin²(theta),

which is constant; cos(theta/2)>0 ensures finite intersections. This also handles the circular limit without a degenerate complex torus argument.

All real intersections in the noncircular theorem are finite by(4), and all origin feet by(12). These facts do not imply derived signed areas or centroid denominators are nonzero; no centroid or quotient is claimed. Least odd period and strict elliptical caustic are retained. The additional opposite-endpoint poles in5.2 explain why simply extending this proof to even periods would be invalid.

The analytic theorem, rather than numerical tests, establishes the invariant. Reproducible exact algebra/lattice controls and separately labeled high-precision geometric diagnostics accompany this candidate. Independent review must verify the source identity, support-line area formula, complete pole divisor, incident cancellations and parity bookkeeping before any result promotion.

## 8. Exact even-period negative control, outside the theorem

The odd restriction cannot be discarded in this statement. Take a²=5,b²=3 and the four-periodic confocal caustic with lambda=a²b²/(a²+b²)=15/8, hence alpha²=25/8,beta²=9/8. The axis diamond with vertices(±a,0),(0,±b), in cyclic order, and the rectangle with vertices(±alpha,±beta) are in the same primitive convex four-periodic family. The diamond chords are tangent because alpha²/a²+beta²/b²=1; the rectangle sides are x=±alpha,y=±beta. The reflection law holds at the axes by symmetry and at the rectangle corners because alpha/a²=beta/b². All relevant intersections are finite.

For the diamond, its origin-pedal rectangle has area4a³b³/(a²+b²)² and its antipedal rectangle has area4ab. Their product is225/4. For the other orbit, its pedal diamond has area2alpha beta and its antipedal diamond has area2(alpha²+beta²)²/(alpha beta); their product is289/4. Thus even this convex, finite, positive-area four-periodic family has a varying product. This is a negative control on an excluded extension, not a counterexample to the odd source target. It is consistent with the additional midpoint pole class that survives for even period in Section5.2.
