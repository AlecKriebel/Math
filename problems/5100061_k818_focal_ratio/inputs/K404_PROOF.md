# k404: the focal antipedal-to-pedal area ratio

**5100022 / AMR-050-0022. Full source-target candidate, substantive author turn 1. Independent review pending.** The canonical parametrization and pedal-trace mechanism are credited below; no novelty or priority claim is made.

## 1. Exact target and theorem

Fix an ellipse E with semiaxes a>b>0 and a strictly nested nondegenerate confocal elliptical caustic. Let P_j be a family of primitive periodic billiard orbits of least period N, including all star winding classes. Assume N=2 modulo 4. Orient traversal so that its turning number satisfies 0<tau<N/2 and gcd(tau,N)=1; reversal will negate all signed areas and leave the asserted quotient unchanged.

Fix either original focus F. The pedal polygon has vertices q_j, the perpendicular feet from F onto the original orbit's consecutive side lines. The antipedal polygon has vertices

    U_j = L_j(F) intersection L_(j+1)(F),
    L_j(F) = {X : (P_j-F)·(X-P_j)=0}.                 (1)

Thus its sides pass through the original vertices perpendicular to their focal rays. Neither construction is made from the outer tangent polygon or the inner contact polygon. Area always means the signed shoelace area in traversal order.

**Theorem.** All intersections (1) are finite. The focal pedal area A_F is strictly positive in the chosen orientation, including for the permitted primitive stars. There is a real family-dependent constant gamma such that

    A_F^* = gamma A_F                                (2)

throughout the family. Hence the literal source quotient A_F^*/A_F is defined and constant everywhere in this strict elliptic-caustic ensemble. The same constant applies to the two foci. It may be zero; no nonvanishing assertion for the antipedal numerator is needed.

Both source editions state precisely this ratio and parity: Reznik–Garcia–Koiller, arXiv:2004.12497v11, Table 5 p. 7; and the published *Fifty New Invariants*, Arnold Mathematical Journal 7 (2021), Table 5 p. 348. The signed-area convention is source equation (1), and §3.5 allows self-intersecting antipedals. Section 1 concerns least period: an artificial repetition is not used to convert another primitive parity into the requested one. Repeating an orbit that already satisfies the theorem scales both areas equally and preserves its ratio.

## 2. Credited canonical coordinates

Scale the caustic's major semiaxis to 1; uniform scaling does not change the area ratio. Set

    0<k<1,   b0=sqrt(1-k²),   K=K(k),   K'=K(b0),
    v=2K tau/N in (0,K),    delta=2v,
    t=sn(v),   C=cn(v),   D=dn(v),
    a=D/C,     b=b0/C,      F+=(k,0), F-=(-k,0).

All Jacobi functions use modulus k, rather than the software parameter k². Stachel, *On the motion of billiards in ellipses*, European Journal of Mathematics 8 (2022), 1602–1622, Theorem 4.3 and equation (4.9), gives

    P(w)=(-a sn(w), b cn(w)),
    P_j(w)=P(w+j delta),                              (3)

with caustic contact parameter u=w+v+j delta and contact point

    B(u)=(-sn(u), b0 cn(u)).                          (4)

Write N=2m. Then tau is odd and gcd(tau,m)=1. In particular

    m delta = 2K tau = 2K modulo 4K.

Thus opposite orbit vertices and contact points are paired by central inversion. Any cyclic area function of (3) has real periods delta and 2K; consequently it has period

    h=2K/m.                                          (5)

This uses the integer Bezout identity for tau and m, not an assumption that a single sampled orbit represents a whole family.

The Jacobi identities used below are the standard addition, period, pole and quarter-period identities in [DLMF §22.4](https://dlmf.nist.gov/22.4) and [§22.8](https://dlmf.nist.gov/22.8). The earlier campaign pedal-trace argument in k203,a / [PR203](https://github.com/AlecKriebel/Math/pull/203), with shared input from [PR204](https://github.com/AlecKriebel/Math/pull/204), and its k204 / 5100013 specialization supply the method used in §6. The exact focal specialization is reproduced here, rather than importing an all-M conclusion without checking its domain. These are author inputs, not independent review of this target.

## 3. Direct focal antipedal formula and all possible poles

We first use F=F+. For a chord with midpoint parameter u, put

    s=sn(u), c=cn(u), d=dn(u),
    L=1-k² t² s²,
    E0=1-2k²t²+k²t⁴.

Solving the two actual antipedal line equations through P(u-v) and P(u+v) gives

    U_x(u) = -[E0 s+k(C²-D²s²)]/(C² L),
    U_y(u) = c[2b0²-E0(1+ks)]/(b0 C² L).             (6)

Here U_j(w)=U(w+v+j delta). Formula (6) is a meromorphic identity, with removable expressions filled by continuation when necessary.

For a direct derivation, the midpoint and half-difference of the two original endpoints are

    M=(-sD²/L, b0 c/L),
    H= -Dt d/(C L) · (c,b0 s).

The chord normal n=(-s,c/b0) satisfies n·M=1 and n·H=0. The antipedal intersection is

    U=2M-F+eta n,
    eta=(|H|²-|M-F|²)/(1+ks).

Use c²=1-s², d²=1-k²s², C²=1-t², D²=1-k²t² and b0²=1-k². Simplification cancels the apparent factor 1+ks and yields (6). The exact checker substitutes the original endpoint formulas into both line equations. It also verifies the determinant

 det(P(u-v)-F,P(u+v)-F)
        =2b0 D t d(1+ks)/(C L).                    (7)

For real u every factor in (7) is nonzero, and L>0. Equivalently, a caustic tangent chord cannot pass through its interior focus. Thus all real intersections are finite, with no assumption about simplicity of the derived polygon.

For complex u the only possible nonremovable poles in (6) are zeros of L. On the lattice generated by 2K and 2iK', these are

    u=iK'+v,  iK'-v.                               (8)

They are simple: sn(u)=±1/(kt), while cn(u) and dn(u) are nonzero because 0<t<1 and 0<k<1. Completeness also follows because sn² has one double pole and hence L has two zeros counted with multiplicity on this lattice. The identity sn(iK'+z)=1/(k sn z) locates them.

At a common pole of sn,cn,dn, the numerator in U_x has order at most two and the denominator order two. The same holds for U_y, since it is cn times a linear function of sn. Those apparent poles are removable. There are no others. In particular each U_j(w) has at most simple poles, and the area

    B_F(w)=(1/2) sum_j det(U_j(w),U_(j+1)(w))        (9)

has at most double poles. By (8), their only possible locations are

    w=iK'-j delta   modulo 2K,2iK'.                (10)

The two endpoint families in (8) coincide after the cyclic index shift because delta=2v. On the quotient with real period h, (10) is one pole location and its 2iK' translate.

## 4. Symmetry forces the double-pole coefficients to vanish

The following are exact meromorphic identities, obtained from the line construction (1) with the bilinear dot product after complexification.

1. Central inversion sends P(w) to P(w+2K), interchanges the foci and preserves signed area. Since shifting by 2K cyclically relabels the even orbit,

       B_(F+)(w)=B_(F-)(w),   B_F(w+2K)=B_F(w).

2. Reflection in the y-axis sends P(w) to P(-w), interchanges the foci and reverses traversal order. Reflection and traversal reversal each negate signed area. More explicitly, antipedal index j becomes -j-1. Hence

       B_F(-w)=B_(-F)(w)=B_F(w).                    (11)

3. The Jacobi imaginary shift gives sn(w+2iK')=sn(w) and cn(w+2iK')=-cn(w). It reflects the original polygon in the x-axis, fixes either focus and keeps the cyclic order. Thus

       B_F(w+2iK')=-B_F(w).                         (12)

These formulas first hold where all intersections are defined and then extend meromorphically. In particular the area is elliptic with periods h and 4iK'.

At p=iK', (11)–(12) imply

    B_F(p+z)=-B_F(p-z).                             (13)

So its Laurent expansion about p contains only odd powers. Section 3 bounds its pole order by two; (13) therefore eliminates the only possible double-pole term. Real-period translates and (12) treat all points in (10). Every possible pole of B_F is at most simple. No assumption that a residue or an area is nonzero has been made.

## 5. The antipedal area is a multiple of the original-area trace

Define

    S(w)=sum_(j=0)^(N-1) dn(w+j delta).              (14)

It has periods h and 4iK' and changes sign under 2iK'. On that quotient it has exactly two simple poles, at iK' and its 2iK' translate. Its residue at the first is nonzero: in the original sum precisely j=0 and j=m have poles there; they are equal terms because dn has period 2K. Their residues add rather than cancel.

Consequently a scalar b_F can match the residue of B_F at iK' with that of b_F S. The anti-period (12) matches the other residue automatically. The difference is holomorphic on the compact period torus and therefore constant; anti-periodicity forces that constant to be zero. This proves

    B_F(w)=b_F S(w).                                (15)

It includes b_F=0. Evaluation at any real phase shows b_F is real, and §4 shows it is identical for the two foci.

For reference, the original orbit area is

    A(P(w))=a b t C/D · S(w).                       (16)

Indeed, the determinant of the edge centered at u is 2ab t C dn(u)/L, while dn(u-v)+dn(u+v)=2D dn(u)/L. Summing half the edge determinants proves (16). On the real axis S(w)>0 and the coefficient in (16) is positive.

Sections 3–5 prove the proportionality of focal antipedal and original areas for any primitive even period under these hypotheses. Only the requested 2-modulo-4 specialization is needed below. No assertion about arbitrary antipedal centers or adjacent source rows is inferred.

## 6. The focal pedal trace and the required parity

The tangent line to the caustic at B(u) has equation n(u)·X=1, where n=(-s,c/b0). Its foot from F+ is

    q(u)=F+ + (1-n·F+)n/(n·n)
         = ((k-s)/(1-ks), b0 c/(1-ks)).              (17)

This is the actual side-line pedal foot. For complex parameters dot products are bilinear, not Hermitian. Put

    T_F(u)=(1/2)sum_j det(q(u+j delta),
                          q(u+(j+1)delta)).
    A_F(w)=T_F(w+v).                               (18)

The possible poles of q occur where sn(u)=1/k, hence at a subset of the dn-zero translates r=K+iK' modulo 2K,2iK'. They have order at most two. Common poles of sn and cn in (17) are removable. Near r the quarter-period identities are

    sn(r+z)=dn(z)/(k cn(z)),
    cn(r+z)=-i b0/(k cn(z)).

Both are even in z, so q(r+z) is even. Neighboring terms at r±delta are regular: 0<delta<2K prevents coincidence of their dn-zero locations with r. At a singular vertex the two incident area summands combine to

    (1/2) det(q(r+z),
              q(r+z+delta)-q(r+z-delta)).           (19)

The second vector is odd and holomorphic in z. Multiplication by the even, at-most-double-pole first vector leaves at most a simple pole. The same argument applies at every translate. Nonadjacent singular terms, if present, add rather than multiply, so cause no larger order.

As with the antipedal, even-period cyclic relabeling gives real period h, and reflection in the x-axis under 2iK' gives an anti-period. Thus on the torus with periods h,4iK', T_F has at most the two simple poles of S(u+K). The same residue-matching argument proves

    T_F(u)=p_F S(u+K).                              (20)

The opposite focus has the same area by central inversion, and hence the same constant p_F. This is the focal specialization of the credited pedal-trace method, with pole orders and phase conventions checked directly.

Now use the exact source parity. Since m=N/2 and tau are both odd,

    K+v = ((m+tau)/2) h,

an integer multiple of h. Combining (18)–(20) yields

    A_F(w)=p_F S(w).                               (21)

For the excluded primitive periods divisible by four this phase-alignment argument does not hold; one may not erase the parity restriction from the ratio.

## 7. Positive denominator, including primitive stars

The focus F lies strictly inside the caustic. Write the perpendicular foot from it to the tangent at u as

    q_F(u)-F = rho(u) n_hat(u),    rho(u)>0,

where n_hat is the outward unit normal. Positivity follows from 1-n(u)·F>0 and n(u)·n(u)>0.

The lifted angle psi(u) of n_hat is strictly increasing, and psi(u+2K)=psi(u)+pi. Indeed n(u)=(-sn u,cn u/b0), whose determinant with its derivative equals dn(u)/b0>0. Since 0<delta<2K,

    0 < psi(u+delta)-psi(u) < pi.

Every consecutive determinant relative to F is therefore strictly positive:

 det(q_F(u)-F,q_F(u+delta)-F)
   =rho(u)rho(u+delta) sin(psi(u+delta)-psi(u)) > 0.

Their half-sum is the signed area; translating the shoelace polygon by F does not change it. This proves A_F(w)>0 even for a star traversal, because the argument uses the canonical contact step delta, not convexity of the orbit. Closure handles the last edge by the same lifted angle. In particular p_F>0 in (21).

Finally (15) and (21) give (2) with gamma=b_F/p_F. This division is justified on the whole real family. No antipedal area is divided by, and its possible zeros create no pole in the target quotient.

## 8. Scope, attribution and diagnostics

The proof covers both original foci, all primitive star winding classes of the requested parity, and strict noncircular confocal ellipse pairs. Circular billiards and degenerate or hyperbolic caustics are not silently added. Reversal and repetitions of already-admissible primitive orbits behave as stated in §1.

The known canonical parametrization, standard Jacobi identities, compact-torus residue argument and earlier campaign pedal-trace work are credited. The direct antipedal calculation and symmetry reduction are presented as a source-matched construction without a novelty claim.

The supplied checker proves symbolic algebra identities for (6), (7), (17), checks exact period arithmetic for a range of primitive indices, and separately performs high-precision real and complex diagnostics using actual line intersections and perpendicular projections. Floating diagnostics do not prove the all-period theorem. The analytic pole completeness, pole order, symmetry and denominator arguments above are the proof and require independent review.
