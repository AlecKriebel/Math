# The center-pedal area product for the outer polygon, k303,b

**5100015 / AMR-050-0015. Full candidate, author turn1; separate independent review pending.** This is an AI-assisted proof candidate with credited classical inputs; historical novelty is not certified.

## 1. Exact claim and conventions

Let E have equation x²/a²+y²/b²=1, a>b>0, and let its fixed confocal elliptical caustic C have semiaxes alpha>beta>0, with

    lambda=a²−alpha²=b²−beta²,  0<lambda<b².

Let P be a primitive N-periodic billiard orbit tangent to C, where **N is not divisible by4**. This includes odd periods and periods congruent to2 modulo4. In traversal order let R_i be the intersection of the tangents to E at P_i and P_(i+1). The outer polygon P' consists of the R_i. Its side through P_i is the tangent to E at P_i. Let Q_i be the orthogonal projection of the fixed ellipse center O onto that tangent line. Write

    A'=area(R),   A'_O=area(Q),
    area(W)=(1/2)sum_i det(W_i,W_(i+1)).                         (1)

Then A'A'_O is constant as the orbit's initial point varies through its fixed-caustic Poncelet family.

This is precisely k303,b in Table4 of both Reznik–Garcia–Koiller's arXiv:2004.12497v11, p.6, and its published *Fifty New Invariants*, Arnold Math.J.7(2021), p.346. Both list the product A'A'_M, N not0mod4 and M=O. Areas are signed, and feet are taken on the side lines of the outer tangent polygon, not on the original billiard chords or on the caustic. Star polygons retain their traversal indexing. No centroid, angle or nonzero-pedal-area hypothesis is needed.

The source uses a noncircular confocal pair of ellipses. Hyperbolic or degenerate caustics are not silently included. If a listed orbit repeats an admissible primitive one, the extension by repetition is addressed in Section7.

## 2. Canonical coordinates and the area trace

Use Stachel's published canonical parametrization, Theorem4.3/(4.9). Set

    k=sqrt(alpha²−beta²)/alpha,  k'=beta/alpha,
    K=K(k),  K'=K(k'),
    v=2tauK/N in(0,K),  gcd(tau,N)=1,
    a=alpha dn(v)/cn(v),   b=beta/cn(v).                       (2)

All Jacobi functions have modulus k, not parameter k². Choose orientation so0<tau<N/2; reversing it changes the signs of both signed areas and preserves their product. The orbit vertices are

    P_i=P(u+2iv),   P(z)=(-a sn(z),b cn(z)).                    (3)

The side contact is B(u+(2i+1)v), where

    B(z)=(-alpha sn(z),beta cn(z)).                            (4)

This contact-phase statement is also directly verified from the addition formulas: both P(z−v) and P(z+v) satisfy the caustic tangent equation

    −sn(z)X/alpha + cn(z)Y/beta =1.

Define

    f(t)=sn(t)cn(t)/dn(t),    T(u)=sum_(i=0)^(N−1)dn(u+2iv).   (5)

The denominator dn(t) is nonzero for real t. For any fixed A,B and points H(z)=(-A sn(z),B cn(z)), Jacobi addition gives

    det(H(z−t),H(z+t))
      =2AB sn(t)cn(t)dn(z)/(1−k²sn²(z)sn²(t))
      =AB f(t)[dn(z−t)+dn(z+t)].                             (6)

The second equality is the sum of the two dn addition formulas. Taking half the sum of (6) over the cyclic edges proves

    area(P(u+2iv))=ab f(v)T(u).                              (7)

Cyclic reindexing gives T(u+2v)=T(u), since2Nv=4tauK is a period of dn.

We also need the ordered edge-vector polygon D_i=P_(i+1)−P_i. Expanding determinants gives

    area(D)=2area(P)−(1/2)sum_i det(P_i,P_(i+2)).

Apply (6) with t=2v to the last sum and reindex by two. This works even when stepping by two splits the indices into two cycles; it is an identity of sums, not a simplicity assertion. Hence

    area(D)=ab[2f(v)−f(2v)]T(u).                             (8)

No division by a polygon area has occurred.

## 3. The outer polygon is an affine-scaled phase shift

Put E_0=diag(a²,b²) and C_0=diag(alpha²,beta²). The line of the side P_iP_(i+1), tangent at B_i=B(u+(2i+1)v), is X^t C_0^(-1)B_i=1. Its pole with respect to E is the intersection R_i of the endpoint tangents, so

    R_i=E_0 C_0^(-1)B_i
       =diag(a/alpha,b/beta)P(u+(2i+1)v).                    (9)

There is no infinite real R_i: parallel endpoint tangents would require antipodal endpoints, whose center-crossing chord cannot be tangent to C. Consecutive endpoints are distinct in a nondegenerate billiard orbit. Taking determinants in (9) and using (7),

    A'(u)= [a²b²/(alpha beta)] f(v)T(u+v).                  (10)

This is elementary conic polarity and a fixed linear area scale, valid in traversal order for simple and star polygons alike.

## 4. The center-pedal polygon is a scaled edge-vector polygon

The tangent to E at P(z) is n(z)·X=1 with

    n(z)=(-sn(z)/a,cn(z)/b).

Since O=0, its perpendicular foot is n(z)/(n(z)·n(z)), or

    Q(z)=(-a b² sn(z), a² b cn(z))
          /[a²−(a²−b²)sn²(z)].                             (11)

The real denominator is positive. Set w=K−v in(0,K). Quarter-period formulas give

    sn(w)=cn(v)/dn(v),
    cn(w)=k' sn(v)/dn(v)>0,
    dn(w)=k'/dn(v)=b/a.                                   (12)

In the addition formulas for P(z+w)+P(z−w), the denominator is

    D(z)=1−k²sn²(z)sn²(w)
        =[a²−(a²−b²)sn²(z)]/a².                           (13)

The sum itself is

    (−2a sn(z)cn(w)dn(w)/D(z),
       2b cn(z)cn(w)/D(z)).

Combining (11)–(13), and using P(z−2K)=−P(z), proves the pointwise identity

    Q(z)=L[P(z+K−v)−P(z+K+v)],
    L=diag(b/a,1)/(2cn(w)),  det L=b/[4a cn²(w)].           (14)

Thus the center-pedal polygon is the image under −L of the edge-vector polygon of the phase-shifted orbit with initial parameter u+K−v. The global minus sign does not change signed area in two dimensions. Equation(8) now gives

    A'_O(u)= [b²/(4cn²(w))][2f(v)−f(2v)]T(u+K−v).          (15)

The same cyclic indexing is used in (10) and (15). In particular, this step does not replace the center pedal by a caustic-contact polygon.

## 5. Odd-order cyclic dn trace lemma

**Lemma.** Let0<k<1 and q be a positive odd integer. Define

    U(z)=sum_(j=0)^(q−1)dn(z+2Kj/q).

Then U(z)U(z+K) is independent of z.

**Proof.** The standard Jacobi data are: dn is even; its periods are2K and4iK'; it changes sign under2iK'; and all its poles are simple, at

    iK'+2rK+2s iK',  r,s in Z.                             (16)

These are exactly the DLMF22.4 period/pole/shift facts. The sum U is elliptic with these periods and may have only simple poles at the shifts of (16) by the finite subgroup H={2Kj/q} modulo2K.

Set c=K+iK'. Evenness and the two half-period signs give the meromorphic identity

    dn(c+t)=−dn(c−t).                                     (17)

Because q is odd, H does not contain K modulo2K. Therefore no summand of U(c) is a pole: c+h could be congruent to an iK' pole only if h were K modulo2K. Pairing h with−h in the subgroup, (17) gives U(c)=0, including the self-paired h=0 term.

For every possible pole p of U, subgroup periodicity and imaginary anti-periodicity imply U(p+K)=0. At such p, the product U(z)U(z+K) has a removable singularity, since the pole order is at most one. Conversely, at any possible pole z=p−K of the second factor, the first equals U(p−K)=U(p+K)=0 by the real period2K. These exhaust all possible poles of the product.

The product is consequently holomorphic on the compact torus with periods2K and4iK', and hence constant. For real z, dn(z)>0, so neither trace nor the resulting real constant vanishes. This completes the lemma. No numerical pole cancellation or assertion about an unexamined principal part is needed. ∎

## 6. Apply the parity condition and finish

Let

    q=N/gcd(N,2),   r=N/q.

Since gcd(tau,N)=1, the shifts2iv modulo the real period2K run through the subgroup H of order q, each exactly r times. Thus

    T(z)=r U(z).                                          (18)

The condition N not0mod4 is exactly that q is odd: q=N for odd N, and q=N/2 for N=2mod4. The lemma therefore proves

    T(z)T(z+K)=T(0)T(K),                                  (19)

independent of z, for every admissible simple or star winding number.

Multiply (10) and (15). The cyclic period2v gives T(u+K−v)=T(u+K+v), so

    A'(u)A'_O(u)
      = C(E,C,v) T(u+v)T(u+v+K)
      = C(E,C,v) T(0)T(K),                                (20)

where the phase-independent coefficient is explicitly

    C(E,C,v)=a² b⁴ f(v)[2f(v)−f(2v)]
               /[4alpha beta cn²(K−v)].                  (21)

All displayed real denominators are nonzero under(2). Equations(20)–(21) prove the full required constancy, including the odd-period part not present in the parallel k303,a target.

## 7. Boundaries, attribution and verification scope

- Primitive stars are included because the only arithmetic requirement is gcd(tau,N)=1 with0<tau<N/2. Neither a spatial re-sorting of vertices nor convex-polygon area is used.
- A repeated traversal of a primitive orbit multiplies both signed areas by its repetition count, hence the product by its square. Moreover, if a listed length N is not divisible by4, its primitive divisor N_0 cannot be divisible by4 either. Thus repeated orbits satisfying the literal listed-period condition follow from the primitive theorem by this scaling; no parity gap is hidden.
- N=2 is impossible with a finite outer ellipse and strictly interior nondegenerate elliptical caustic. The two-bounce chord would pass through O. The source assumes a>b; the separate circular case consists of rigid rotations of fixed-step regular stars and follows directly.
- The proof is specifically for M=O. No arbitrary-M assertion or the separate k303,a proof is needed. Hyperbolic or degenerate caustics, clamped projection to finite segments, and unsigned areas of filled star lobes are different questions.
- Stachel's canonical theorem, classical Jacobi addition/period facts and elementary conic polarity are credited inputs. The dn-trace lemma is proved here as a classical elliptic-function argument, not claimed as a new special-function identity.
- The complete mechanism was saved in TURN1_DERIVATION_CHECKPOINT.md before this author read the parallel k203,a candidate during an assigned review. That candidate independently uses the same universal dn-area identity and a different two-pole proportionality argument. This overlap is disclosed; neither it nor the parallel k303,a candidate supplies an unproved step here. A reviewer uninvolved in this author derivation is required before promotion.
- A bounded exact-target/source search did not locate a published full k303,b proof. This is not a guarantee of historical novelty. Exact algebra and finite/high-precision controls support the written analytic proof and must not be represented as proving all phases by numerical sampling.

## Primary references

1. Reznik, Garcia, Koiller, *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, arXiv:2004.12497v11, Table4 p.6 and Sections2/3.4: https://arxiv.org/pdf/2004.12497v11
2. Same authors, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Math.J.7(2021),341–355, Table4 p.346: https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf
3. H. Stachel, *On the motion of billiards in ellipses*, European J.Math.8(2022),1602–1622, Theorem4.3/(4.9), p.1614: https://doi.org/10.1007/s40879-021-00524-2 and https://link.springer.com/content/pdf/10.1007/s40879-021-00524-2.pdf
4. NIST DLMF22.4, especially Tables22.4.1–22.4.3 (periods, simple poles, quarter shifts): https://dlmf.nist.gov/22.4
5. NIST DLMF22.8.1–22.8.3 (addition theorems): https://dlmf.nist.gov/22.8
