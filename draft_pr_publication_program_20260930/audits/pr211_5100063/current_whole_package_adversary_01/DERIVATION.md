# Independent reconstruction and attempted falsification

The claim and attack mechanisms were frozen before the candidate proof and old verdicts were read. This reconstruction uses the six-page note as the object being challenged, the primary canonical-coordinate theorem and standard Jacobi identities. Prior PASS labels are not premises. It establishes the mathematical implication below; it is not formal proof-assistant verification.

## Physical object, parameter coverage and normalization

Write alpha,beta for caustic semiaxes, c for the ORIGINAL focal distance, k=c/alpha, k'=beta/alpha. Stachel's published Theorem4.3, printed1614, gives

    P(w)=(-a sn(w),b cn(w)), a=alpha dn(v)/cn(v), b=beta/cn(v),
    delta=2v=4K tau/N, 0<v<K, gcd(tau,N)=1.

This covers every strict confocal elliptical pair: cn(v)=beta/b determines a unique v in (0,K), then confocality supplies a. The real parametrization is injective modulo4K, so least period is precisely the order of delta modulo4K. Reversal covers the complementary turns. Thus no convex-orbit restriction is smuggled into the star cases. Mpmath takes k^2 as its parameter. The adjacent primary paper's erroneous real dn sign is unused; dn has real period2K.

Set h=sn(v), C=cn(v), d=dn(v), t=h^2, q=C^2=1-t. Directly solve the two original tangent equations at P(u-v),P(u+v). Their coefficient determinant is

    2h C dn(u)/(a b (1-k^2 t sn(u)^2)),

which is strictly positive for real u. Cramer's rule yields

    Q(u)=(-A sn(u),B cn(u)), A=alpha d^2/q, B=alpha k'/q.

Since d^2-C^2=k'^2t>0, A>a and B>b. Hence Qx^2/a^2+Qy^2/b^2>1 at every real u. Original foci lie inside the original ellipse, so inversion is always defined. No ordering of A and B is needed: A<B is allowed and occurred in36 of my72 numerical families.

Area is the signed cyclic determinant sum. Translating every inverse vertex by minus its focus leaves its COMPLETE shoelace sum unchanged, because the translation terms telescope. Thus use I(u)=(Q(u)-f+)/D(u). Continuing D bilinearly, without complex conjugation, is the meromorphic continuation of the actual real Euclidean squared distance. Put

    U=1-2k^2t+k^2t^2, V=1-2t+k^2t^2, W=1-k^2t^2.

Expansion of Q gives

    D(u)=alpha^2/q^2 (1+k sn(u))(U+kV sn(u)).

With s=sn(u), H=1-k^2t s^2, addition gives

    s_+-s_- = 2h cn(u)dn(u)/H,
    s_++s_- = 2sCd/H,
    s_-s_+ = (s^2-t)/H.

Using these identities in the actual inverse determinant gives

    e(u)=det(I(u-v),I(u+v))/2
        =C0 dn(u) H/[(d+kC s)^2(L0+kL1 s)],
    L0=(U^2-k^2V^2t)/d, L1=(V^2-U^2t)/C,
    C0=B h d q^4/(alpha^3 C).

The raw half-determinant before dividing by the two distances is alpha B h d dn(u)(d+kC s)/(C H). The product of the two distances is alpha^4(d+kC s)^3(L0+kL1 s)/(q^4 H^2). This verifies the potentially dangerous q^4 factor and half-edge factor. In symbolic_check.py I independently reconstruct these products from the addition expressions and reduce eight residuals in a square-root quotient ring over Q(k,t,s); all eight residuals are exactly zero. Cleared-denominator CAS identities do not prove domain nonvanishing; the next inequalities do.

## Real nonvanishing and complete complex fibers

Addition of2v and v gives

    Z=W^2-4k^2t^2 q d^2=W^2(1-k^2t sn(2v)^2)>0,
    L0=Z dn(3v), L1=Z cn(3v),
    L0^2-k^2 L1^2=k'^2 Z^2>0.

Real dn is positive, so L0>|kL1|. Also d^2-k^2C^2=k'^2>0. Both denominator factors of e are positive on the real axis, as are dn,H,C0. Therefore e(u)>0 for every real u. L1 cannot vanish for an odd least period: its only possible interior zero in0<3v<3K is3v=K, forcing N=6tau.

Let p=iK' and r=3K+p. The sn torus has periods4K,2p and degree2. e itself has periods4K,4p and ANTI-period2p; these two tori must not be confused. The quarter shift

    sn(K+p+z)=dn(z)/(k cn(z))

shows the fiber d+kC sn(u)=0 consists of exactly r+v,r-v modulo4K,2p. Its value -d/(kC) has magnitude greater than1/k, so the fiber is noncritical and both roots are simple. The squared factor permits double poles.

The second factor has fiber r+3v,r-3v. Generically these are two simple roots. A collision requires6v=4K in0<6v<6K; equivalently3v=2K, and coprimality then gives only N=3,tau=1. This is also the only critical value of that second fiber: equality of the magnitude of dn(3v)/(k cn(3v)) with1/k requires sn(3v)=0. The two denominator fibers cannot meet, since that would force2v or4v to be a multiple of4K with0<v<K.

In the triangular case L0=Z,L1=-Z, the second factor is Z(1-k sn(u)). At b=K+p it has a quadratic zero, whereas dn(u) has a simple zero. Here H=q is nonzero, and d+kC sn(b)=d+C is nonzero. In local coordinate z=u-b,

    dn(u)=i k' z+O(z^2),
    1-k sn(u)=-k'^2 z^2/2+O(z^3).

Thus e has a SIMPLE pole, with residue -2i C0 q/[Z k'(d+C)^2]. This explicitly checks that the critical fiber does not leave a hidden double pole.

At a common pole of sn,cn,dn, the numerator and denominator of e each have order3; the denominator's leading coefficient is nonzero because k,C,L1 are nonzero. Every such point is removable. At finite points away from the listed denominator roots e is holomorphic. These facts exhaust possible poles, including common Jacobi poles and the only coalescent fiber.

Parity and correct periods give

    sn(2r-u)=sn(u), dn(2r-u)=-dn(u), e(2r-u)=-e(u).

Consequently the quadratic Laurent coefficients at r+v,r-v are opposite. This is a local identity, not a sampled cancellation.

## Universal cyclic cancellation and nonzero residue

Define F(u)=sum(j=0..N-1)e(u+j delta), L=4K/N and R=r+v. The element delta has order N modulo4K. At every translated first-fiber pole exactly one occurrence of each of the two quadratic coefficients appears, because those fibers differ by delta. They cancel. The other fiber positions differ from R by delta and -2delta and were already at most simple. For N=3 the second fiber was treated as one critical root, not counted twice. There are no other pole classes.

F has periods4K and delta. Bezout gives period L. It retains anti-period2p. On X=C/(L Z+4p Z), there are therefore at most two simple poles, R and R+2p. If both were removable, compactness would make F constant and its anti-period would make F zero. This contradicts the strictly positive real sum. Anti-periodicity pairs the candidate poles, so each is an actual simple pole. In particular the nonzero-residue conclusion holds for EVERY admissible N,k,tau, without a numerical lower bound or a hidden genericity assumption.

Reindexing the reflection makes F odd about r. Since2R=2r+delta, F is also odd about R. The holomorphic fixed classes R+L/2 and R+L/2+2p are zeros. They are distinct and do not meet the two poles. A nonzero meromorphic function on a compact torus has equal total zero and pole order, so these are exactly two simple zeros. Translation by L/2 exchanges the complete zero and pole divisors. Consequently F(u)F(u+L/2) has no poles on X and is constant.

The outer polygon phase may be Q(w+j delta); its inverse area is F(w+v). Since Q(u+2K)=-Q(u), the inverse list at f- is the central reflection of the f+ inverse list at phase shifted2K. This preserves signed area. Since N is odd,

    2K=NL/2=L/2 modulo L.

Therefore the actual two-focus signed-area product is F(w+v)F(w+v+L/2), the constant just proved. The positivity, complete fibers, cancellation, nonzero-residue argument and opposite-focus shift close the universal proof. A finite match was not substituted for any of these steps.

## Boundary and falsification controls

Reversal reverses each cyclic determinant sum and changes both signs. A fixed r-fold repetition multiplies each sum by r and its product by r^2; it does not create a new least period. Spatial scaling by lambda multiplies each unit-inverse area by lambda^-2 and the product by lambda^-4. Changing both inversion radii to rho multiplies each inverse area by rho^4 and the product by rho^8. At k=0 both foci coincide and a separate rigid-rotation calculation gives B=N sin(2pi tau/N)/(2R_outer^2). The compact-torus proof need not extend to that degenerate torus.

Even periods do not have2K congruent to L/2. The independently replayed exact controls exhibit same-caustic even examples where the product changes. Strict k in(0,1), v in(0,K) and beta>0 are used in the inequalities and must not be dropped at collapsed, hyperbolic, grazing or coincident-ellipse boundaries. No uniform numerical conditioning at those boundaries is claimed.

My Cartesian checker generates only the ellipse PAIR using the canonical closure values. From a freely chosen eccentric-angle phase, it constructs a caustic tangent by an affine unit-circle tangent construction, then propagates by the physical Cartesian reflection law. It independently solves the two original tangents, performs the center-inclusive inversions and sums signed determinants. It uses neither the proposed Q formula nor e to generate the tested areas. Across72 families and288 phases at90digits, max RELATIVE product spread was1.367677133e-88 and relative closure1.299974186e-88;36 families had reversed outer axes. Reversal and fresh scaled geometry agreed. These are noninterval diagnostics. The exact algebra controls and the universal written argument provide their proper context.
