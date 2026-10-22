# Independent reconstruction and attempted falsification

Reconstructed from the frozen theorem/manuscript before reading peer or Root
mathematical acceptance conclusions. This is a written mathematical check,
not a proof-assistant certificate. Locators refer to manuscript.tex SHA256
71e45462370c5314a2e43cc43678571931f8dc177536637e24cea050034b496e.

## Domain and geometric identification (lines 42-110)

Put alpha^2=a^2-lambda, beta^2=b^2-lambda and c^2=a^2-b^2. The strict
domain gives alpha>c>0,beta>0,k=c/alpha in (0,1). Every such pair has a
unique v in (0,K) with cn(v)=beta/b. Substituting dn^2=1-k^2 sn^2 yields
alpha dn(v)/cn(v)=a, so the canonical relations omit no pair. Stachel's
published Theorem4.3/Eq4.9, printed1614, supplies the billiard step2v at
arbitrary initial phase. Real phase injectivity modulo4K makes least N
equivalent to a reduced fraction delta/(4K)=tau/N. Reversal arranges
0<tau<N/2. No convexity restriction is introduced; admitted primitive stars
are included.

Consecutive contacts are distinct and not antipodal, so adjacent boundary
tangents meet finitely. A collapsed outer side would require three distinct
tangents through one point, impossible for a nonsingular conic. The actual
outer side V_(j-1)V_j is exactly the tangent at P_j, including the cyclic cut.

For P=(-as,bt),s^2+t^2=1, the tangent is n.X=1 with n=(-s/a,t/b).
Perpendicular projection F+(1-n.F)n/(n.n), together with
n.n=(a-cs)(a+cs)/(a^2 b^2), gives

    Q_+=(a(c-as)/(a-cs), abt/(a-cs)).

The real denominator is positive and Q.Q=a^2. Direct projection from the
other focus gives Q_-(w)=-Q_+(w+2K). Global negation preserves area, hence
B_-=T(w+2K). This identifies side-LINE feet at the ORIGINAL foci rather
than chord-polygon feet. My exact Cartesian checks construct actual outer
intersections independently and recover the different products for these
two objects:12544/25 versus7225344/390625 in both H,V.

## Exhaustive poles and the adjacent singular edge (lines 113-167)

Let p=iK',r=K+p. Q has periods4K,4p; shift2p reflects its y coordinate.
Common simple sn/cn poles are removable in its component ratios. Other
poles solve sn(w)=a/c=dn(v)/(k cn(v)). The quarter-period identities give
r-v,r+v on the sn torus(4K,2p). They are distinct; cn=-ib/c and dn has
opposite nonzero values there, so the denominator roots are simple. The
degree-two map sn exhausts them. The full vector torus adds their translates
by2p, and there are no further poles.

The numerator at both first-row roots is(-ab^2/c,-iab^2/c); denominator
derivatives have opposite signs. Residues are consequently R,-R. The roots
differ by delta, so an area edge really has TWO singular endpoints. Its
double coefficient det(R,-R) vanishes. Every other incident edge has one
singular endpoint and at most a simple pole. Coprimality gives exactly two
singular indices, adjacent modulo N, with no copy from the other imaginary
row at the same phase. N delta=4K tau is a true vector period at the cut.

For N=3, the two other edges share their regular vertex C; this creates no
new double pole. Expanding Q0=R/e+A,Q1=-R/e+B gives simple area coefficient
det(R,A+B-2C)/2 and zero double coefficient. My symbolic code verifies this
identity. Finite exact checks cover17,413 cuts in469 primitive grids up to
N55; the modular argument above is universal. A repeated six-entry triangle
is separately detected as nonprimitive.

## Reduced torus and complementary zeros (lines 169-217)

T has periods delta and4K. Bezout yields L=4K/N. On C/(L Z+4p Z), its
only possible poles are b0+p,b0+3p,b0=K-v, each at most simple. The full
vector is never incorrectly assigned period2p.

Q(w+2p)=JQ(w),J=diag(1,-1), implies T(w+2p)=-T(w).
Q(2K-w)=JQ(w) combines reflection with cyclic reversal, whose two minus
signs cancel. Since2v=delta is a trace period,F(z)=T(b0+z) is even.
At z=p+L/2, evenness and L-periodicity give F(-p+L/2)=F(p+L/2), while
antiperiodicity gives its negative. This is a regular point, so it is a zero;
3p+L/2 is another zero. Each possible pole of F(z)F(z+L/2) is canceled by
a zero of its other factor. The at-most-simple bound is essential here.
The product is holomorphic on a compact torus and constant.

If F has no poles it is constant and the antiperiod forces F=0. There is no
division or hidden nonzero-area assumption. For odd N,2K=(N/2)L is L/2
modulo L, proving B_+B_-=constant for all admitted primitive stars.
Even primitive N gives equal focal areas, not constancy of their square.
My exact genuine N4 phases at a^2=4,b^2=1,lambda4/5 give products16,25.
The incorrect source square is already distinguished in the frozen paper.
An s-fold repeat multiplies each area by s, for any integer s, even when
the resulting list has even length. Reversal negates both areas. The circle
is a separate direct rotation argument; k=0 is not inserted into the strict
pole formulas. Hyperbolic, collapsed and grazing caustics are not promoted.

## Auxiliary bicentric/Landen proof (lines 227-260 and sealed bridge)

The focal projectivity T_+(x,y)=(a^2(x+c)/(a^2+cx),a^2 y/(a^2+cx)) agrees
with the focal foot on E. Its denominator is positive on the closed interior.
It maps E to the radius-a circle. With A=a^2,B=b^2,U=A-lambda,V=B-lambda,
the image caustic has coefficients

    ux=A^2/U-c^2, vy=B^2/V, ell=c A lambda/U, C=-A^2 V/U.

They satisfy vy-ux=c^2 lambda^2/(UV)>0 and ell^2+C(vy-ux)=0; the image
is a displaced ellipse with a focus at zero, not an incircle. Polarity
q.R=A uses homogeneous line(R_x,R_y,-A), and matrix adjugation gives a
circle centered d=-c lambda/V of radius R_b=sqrt(U)B/V. My independent
generic symbolic calculation verifies that full equation and its negative
center. Projectivity without the additional polarity or an area calculation
would not establish an area invariant.

Zero is inside the image caustic since its preimage(-c,0) is strictly inside
the original caustic. Each forward image chord leaves zero on its left,
including stars. Consecutive circle angles have positive increment less
than pi. Thus positive tangent lengths t_j=a tan(epsilon_j) are valid and
direct signed determinants give

    A(R)=a sum(t_j), B_+=a^3 sum(t_j/(a^2+t_j^2)).

These are signed formulas and do not use filled-star areas. Direct tangent
intersection at midpoint z gives V(z)=(-a^2/alpha sn z,b^2/beta cn z).
Its focal projective image satisfies

    (R_x-d)/R_b=(k-sn z)/(1-k sn z),
    R_y/R_b=k' cn z/(1-k sn z).

For m_b=4k/(1+k)^2,K_b=(1+k)K,u=(1+k)(z-K)/2, differentiating
f=sqrt((1-k)/(1+k))dn(z)/(1-k sn(z)) gives
f''=((1+k)^2/4)((2-m_b)f-2f^3),f(K)=1,f'(K)=0. ODE uniqueness gives
f=dn(u|m_b), fixing the phase. The circle coordinates give
t_j=t_M dn(u_j|m_b),t_M^2=(R_b+|d|)^2-a^2, with step sigma=2K_b tau/N.
The positive root is justified by the geometry, not assumed for stars.

The local dn addition formula summed over both shifts u+/-sigma yields

    B_+=a^3 t_M/(R_b^2-d^2) sum_j dn(u+j sigma|m_b),
    B_+/A(R)=a^2/(R_b^2-d^2).

Specifically,dn(sigma)=(R_b-|d|)/(R_b+|d|) and
a^2+t_M^2dn^2(u)=(R_b+|d|)^2(1-m_b sn^2(u)sn^2(sigma)). Both shifted
sums equal the original because N sigma is a true dn period. Denominators
are positive. My five numerical families check the direct circle, contact
ratio and dn area trace with actual projected feet.

Fourier filtering independently normalizes the old arbitrary-order identity:
the absolutely uniformly convergent real dn series has constant pi/(2K)
and harmonic coefficients(2pi/K)q^h/(1+q^(2h)). The N equally spaced sum
kills harmonics except multiples of N. If m_N has nome q_b^N, this gives

    sum_j dn(u+2jK_b/N|m_b)
       =(N K_N/K_b)dn((N K_N/K_b)u|m_N).

K_N=K(m_N) uses parameter syntax; with the manuscript's modulus convention
it is K(sqrt(m_N)). The sealed bridge's ambiguity is explicitly resolved by
CURRENT_CONVENTIONS_AND_CORRECTIONS.md. Coprimality reorders the sum. The
focus switch u->u+K_b becomes a reduced half-period for odd N, so the
classical dn half-period product proves the same constant. KS2004 Eq7 and
Section2.1, read in preserved primary extraction, print the arbitrary-order
identity. Its old analytic origin is credited; the additional geometric
application neither proves nor refutes historical novelty on its own.

## Opposite-focus inversion proof (lines 262-278 and sealed transfer)

The translated inverse about F_- is R_-=(c-a sn w,b cn w)/(a-c sn w)^2,
so pointwise Q_+=a(a-c sn w)R_-. This multiplier varies with phase and
does NOT by itself multiply polygon area by a constant.

The correct mechanism is the shared meromorphic space. The outer area has
the two possible simple poles and imaginary antiperiod proved above. The
full F62 primary gives the corresponding inverse bound: isotropic negative
Laurent coefficients first bound order by two; reversal removes that even
term. In the shared space, residue at one possible pole determines the
function, since antiperiodicity fixes the other residue and a pole-free
member is constant and then zero. The inverse area is a nonzero spanning
member: each directed original edge leaves the focus strictly on its left,
so each inverse determinant is positive on real forward trajectories.
Matching residues gives B_+=gamma D_- without division through zeros.
Focus exchange gives the SAME gamma for B_-=gamma D_+. My exact H,V
calculations recover gamma2016/5 and inverse product1/324. F22 Remark6.6
now also prints the comparison and credits the deposit. No causal history
or priority certificate is inferred from this attribution.

## Outcome

No unsupported central step or counterexample was found for the exact
strict-domain theorem. The main proof requires neither auxiliary proof nor
positivity. Controls discriminate chord versus outer-side geometry, odd least
period versus even primitive period, opposite versus same focus in transfer,
correct polarity sign, and primitive versus repeated lists. The universal
conclusion rests on the written argument, not these finite computations.
