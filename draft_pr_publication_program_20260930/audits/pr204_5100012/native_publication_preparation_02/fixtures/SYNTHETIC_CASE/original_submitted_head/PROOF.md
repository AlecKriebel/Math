# The origin-pedal area product in an elliptic billiard

**5100012 / AMR-050-0012 / k203,b. Complete author-turn-1 candidate; separate review pending.** No historical-priority or human-peer-review claim.

## 1. The exact source theorem

Let an ellipse E with semiaxes a>b>0 have a strictly nested nondegenerate confocal elliptical caustic C with semiaxes alpha>beta>0. Let a Poncelet billiard family have least period N>=3 and turning number tau, gcd(N,tau)=1. Let A be its **signed** area. From the common center O, drop perpendiculars to its consecutive sidelines, and let A_O be the signed area of the ordered pedal polygon. Then

    A A_O is constant over the family if N is odd or divisible by4.   (1)

These are exactly N not congruent to2 modulo4, the range in k203,b. Primitive star orbits are included. Orthogonal projections are to the full side lines, as in the usual pedal construction. Hyperbolic or collapsed caustics are not part of the source's confocal-ellipse setting. Repetition does not change an orbit's least period or permit relabeling an excluded primitive parity.

Both [arXiv2004.12497v11](https://arxiv.org/abs/2004.12497v11), Table3 printedp6, and the [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Table3 printedp346, state A A_M for M=O and this same parity. Section2 defines polygon areas by signed cross-product sums. This result is distinct from k203,a, which concerns every fixed M when N is divisible by4.

## 2. Published canonical coordinates and the side contacts

Write k=sqrt(alpha^2-beta^2)/alpha in (0,1), k'=beta/alpha, and K,K' for the real and complementary complete elliptic integrals. Jacobi functions have modulus k. By Stachel's [published Theorem4.3 and equation4.9](https://doi.org/10.1007/s40879-021-00524-2), choose 0<v<K so that

    P(w)=(-a sn w,b cn w),
    a=alpha dn(v)/cn(v),    b=beta/cn(v),
    delta=2v=4K tau/N,    0<tau<N/2.                       (2)

Changing orientation if necessary does not change the product of the two signed areas. The vertices are P(w+j delta), j=0,...,N-1. The coprimality condition is the least-period condition and permits primitive stars.

The chord through P(u-v) and P(u+v) is the caustic tangent

    n(u) dot X=1,    n(u)=(-sn(u)/alpha,cn(u)/beta).        (3)

Indeed the contact point (-alpha sn u,beta cn u) satisfies (3). Substituting either endpoint and the Jacobi addition formulas gives 1: the numerator after cancellation is sn^2(u)dn^2(v)+cn^2(u)=1-k^2sn^2(u)sn^2(v), the addition denominator. This verifies the contact phase without assuming that a side midpoint equals the contact point.

The perpendicular foot from the origin to (3) is therefore

    Q(u)=n(u)/(n(u) dot n(u))
        =(-alpha k'^2 sn(u)/dn^2(u), beta cn(u)/dn^2(u)).  (4)

For real u its denominator is positive. In the complex continuation, the dot product is the bilinear sum of squares, with no complex conjugation. It is the meromorphic extension of the real projection formula.

Define

    S(w)=sum_(j=0)^(N-1) dn(w+j delta),
    T(u)=1/2 sum_(j=0)^(N-1)
              det(Q(u+j delta),Q(u+(j+1)delta)).           (5)

The cyclic sum closes because N delta=4K tau. The actual pedal area is

    A_O(w)=T(w+v).                                        (6)

## 3. The orbit area is a cyclic dn sum

Put h=sn v and C_v=cn v. The cross-product addition identity is

    det(P(u-v),P(u+v))
      =2ab h C_v dn u/(1-k^2 h^2 sn^2 u).                 (7)

Meanwhile

    dn(u-v)+dn(u+v)
      =2dn(v)dn(u)/(1-k^2 h^2 sn^2 u).                    (8)

Summing (7)/2 over the side mid-phases w+v+j delta and using (8), every vertex dn term occurs twice. Hence

    A(w)=C_A S(w),    C_A=ab sn(v)cn(v)/dn(v)>0.           (9)

In particular A is positive for the chosen orientation. This remains true for the signed area of a primitive star; no simple-polygon area assumption has been made.

## 4. The two-pole cyclic function

Let

    m=N if N is odd,    m=N/2 if N is even,
    ell=2K/m,    p=iK'.                                  (10)

The residues of j delta modulo2K form the group of order m. More explicitly delta/ell equals2tau for odd N and tau for even N; the relevant integer is coprime to m. The sum S has periods ell,4iK', anti-period2iK', and is even. Period ell follows from its invariance under delta and2K by Bezout; evenness follows by reindexing j to -j.

The standard Jacobi facts used here are in [DLMF22.4](https://dlmf.nist.gov/22.4): dn has real period2K, imaginary period4iK', anti-period2iK', and simple poles at 2rK+(2s+1)iK'. Its basic zeros are K+iK', with the corresponding translates. Addition identities are in [DLMF22.8](https://dlmf.nist.gov/22.8).

On the compact torus

    X=C/(ell Z+4iK' Z),                                  (11)

S has exactly two simple poles, at p and3p. At p, precisely N/m summands contribute a pole; their arguments differ by real periods2K, so all have the same nonzero residue. They do not cancel. Anti-periodicity gives the other simple pole with the opposite residue. There are no other possible poles.

At z=p+ell/2, evenness, real periodicity and anti-periodicity give S(z)=-S(z), since -z+ell+2iK'=z. Thus z is a zero; it is not a pole. The same holds at3p+ell/2. These two distinct zeros exhaust the zero divisor, because an elliptic function has equally many zeros and poles counted with multiplicity. Each is simple. Therefore

    div(S)=[p+ell/2]+[3p+ell/2]-[p]-[3p],
    S(w)S(w+ell/2) is constant.                           (12)

The last assertion follows by canceling divisors on X and compactness. Its constant is positive on the real line because every real dn value is positive.

## 5. The pedal sum has only simple poles

We establish the key fact without evaluating any residue explicitly:

    T(u)=C_T S(u+K) for a real constant C_T.               (13)

The constant may be zero; that causes no problem for (1).

First, (4) is meromorphic. At a common pole of sn,cn,dn, each numerator has at most a simple pole and dn^2 has a double pole, so Q extends holomorphically and vanishes there. Its only possible poles are the zeros of dn: r=K+iK' and its translates. They are at most double. The zeros of dn are simple; the values of sn and cn there are finite and nonzero.

Crucially, Q is even about r. The parity and shifts of Jacobi functions give

    sn(2r-z)=sn z,    cn(2r-z)=cn z,    dn(2r-z)=-dn z,
    Q(2r-z)=Q(z).                                        (14)

Consequently the Laurent expansion of Q(r+epsilon) has only even powers, starting at epsilon^-2, and no epsilon^-1 term.

Consider a phase where Q(u+j delta) has a pole, and set u+j delta=r+epsilon. The two incident summands of T combine exactly as

    1/2 det(Q(r+epsilon),
            Q(r+delta+epsilon)-Q(r-delta+epsilon)).       (15)

The neighbor values are holomorphic there: 0<delta<2K rules out a real pole-to-pole shift. At epsilon=0 their difference is zero by (14), so this second vector is O(epsilon). The first is O(epsilon^-2). Thus the apparent double pole in the **summed area** has order at most one. For even N, repeated pole indices separated by m contribute copies of this argument; they are not adjacent, and no term has two pole endpoints. The N4 case m=2 is covered: both neighbors remain holomorphic, even when their value is zero.

All other summands are holomorphic. The same conclusion holds at every pole translate. Therefore T has at most simple poles at r-j delta and r+2iK'-j delta.

It remains to verify the torus and character, rather than presume them. From (4),

    Q(u+2K)=-Q(u),
    Q(u+2iK')=J Q(u),    J=diag(1,-1), det J=-1.          (16)

Determinants therefore make T periodic2K and anti-periodic2iK'. Reindexing its cyclic sum makes it periodicdelta, hence periodicell. It is consequently meromorphic on X, with its only permitted simple poles at r and r+2iK'.

S(u+K) has exactly those two simple poles on X: p-K and r differ by2K, a multiple of ell. Choose C_T to match the residue of T to that of S(u+K) at r. This is possible because the latter residue is nonzero. Their anti-periods match the residues at the second pole automatically. The difference is now holomorphic on the compact torus X, so it is constant; its anti-period forces that constant to be zero. This proves (13). For real u the quotient is real, because S(u+K)>0 and T is a real signed area.

Notice that this argument used a cancellation **between the two adjacent area terms**. Bounding the poles of each term separately would not give (13).

## 6. Exact parity calculation and conclusion

Combining (6), (9) and (13) gives

    A(w)A_O(w)=C_A C_T S(w)S(w+K+v).                     (17)

It remains to identify this phase shift on the reduced torus.

- If N is odd, m=N and (K+v)/ell=N/2+tau, a half-integer
- If N is divisible by4, m=N/2 is even and tau is odd, so (K+v)/ell=(m+tau)/2 is a half-integer
- If N=2 modulo4, m and tau are odd and the same expression is an integer

In the first two cases K+v equals ell/2 moduloell. Equation (12) therefore proves (1). The excluded parity is not silently included: there (17) is proportional to S(w)^2, and this proof does not assert that product to be invariant. It instead shows the central-pedal area is proportional to the orbit area, without making a ratio assertion at a possible zero denominator.

No division by A_O occurs anywhere, so a zero value of C_T is allowed. Reversal changes the signs of both ordered areas and leaves their product unchanged. The source's signed-area convention is thus respected. For a circular billiard, all regular primitive star polygons and their central pedals rotate rigidly, giving the corresponding conclusion directly without the complex argument.

## 7. Verification, credit and relation to k203,a

The proof rests on the published canonical parametrization, standard Jacobi meromorphic facts, explicit real algebra, local Laurent cancellation and compactness. Exact finite controls check algebraic formulas, pole-orbit multiplicities, parity and the formal local cancellation. Separate numerical checks use actual chord projections and signed shoelace areas, including odd periods, N4, stars and wrong-parity controls. These are diagnostics, not substitutes for the universal proof.

Complex elliptic-function methods for billiard invariants predate this work; see Akopyan-Schwartz-Tabachnikov, [Billiards in ellipses revisited](https://arxiv.org/abs/2001.02934). The canonical input is credited to Stachel. No exhaustive novelty search or historical-first claim is made.

A parallel author working on k203,a supplied its own centrally symmetric arbitrary-M reduction. The present origin-only proof does not assume that reduction. The two-pole mechanism developed here was shared with that author as an **author contribution** for a possible general-M extension, not as an independent review. Any such neighboring result needs a separate review by an uninvolved reviewer. The current candidate proves exactly k203,b, including its additional odd-period cases, and does not substitute k203,a for the target.
