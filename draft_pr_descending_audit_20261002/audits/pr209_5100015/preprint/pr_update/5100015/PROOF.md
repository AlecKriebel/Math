# The outer center-pedal area product, k303,b

Current mathematical presentation, 16 October 2026. Full strict-ellipse theorem; classical and exact contemporary work credited. No novelty, first-proof or historical-independence claim.

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

## 7. Current scope, credits and review status

Reversal changes both signed areas' signs. A fixed d-fold traversal multiplies both areas by d and their product by d²; a listed period not divisible by four has primitive divisor not divisible by four. Nondegenerate one/two-bounce strict-ellipse orbits are impossible. Circles follow separately by rigid rotation of fixed-step regular stars. Hyperbolic, focal, collapsed, arbitrary-reference-point and unsigned filled-lobe assertions are not included.

The odd trace lemma is classical: Khare-Lakshminarayan-Sukhatme, arXiv:math-ph/0207019v1 (2002), AppendixA Eq86, product dn=C_q U_q with C_q=product cs²(2Kj/q), gives U_q(z)U_q(z+K)=(k')^q/C_q². Generalized Landen formulas of Khare-Sukhatme (2003/2004) provide another old route. The complete explicit constant is coefficient(21) times r²(k')^q/C_q². The analytic proof above is a reproof of prior elliptic-function facts, not a new identity or method.

Akopyan-Schwartz-Tabachnikov, arXiv:2001.02934v2, Theorem4 proof and Lemma3.1/Remark3.2, already give the unit-velocity/center-foot mechanism and skew hodograph; Bialy-Tabachnikov, arXiv:2001.08469v2, Theorem4.1, gives the actual-foot telescope. This proof makes the same-caustic canonical phase and signed-area normalization explicit. Stachel's canonical theorem, Jacobi identities, conic polarity, and the established complex Poncelet/pole-cancellation method are credited. Chavez-Caliz's Theorem6 concerns the different original/outer area product; an explicit auxiliary-family bridge to trace constancy is in the supplement.

A. Ferudun, *Outer-Pedal Area Products in Elliptic Billiards*, v1.1, DOI10.5281/zenodo.23088516, Theorem2/Section6, proves the exact complete target, including odd and2mod4 lengths and signed repetitions. v1.0 (DOI10.5281/zenodo.23087221) only gives the primitive even arbitrary-point result and hence its centered even subset. The bounded priority audit authenticates earlier GitHub server receipt of this unchanged candidate tree than either Zenodo record, but does not establish historical public availability, exclude earlier website posting, or certify independent non-derivation. Historical ordering and novelty remain undetermined. No exclusive/currently-open/first theorem claim is made.

Original conjecture: Reznik-Garcia-Koiller arXiv2004.12497 (2020; v11Table4p6), published *Fifty New Invariants*, AMJ7(2021),341-355, Table4p346, DOI10.1007/s40598-021-00174-y. The2021 source-year is the journal edition. Source Section2 specifies signed areas and Section3.4 the outer polygon.

Three new mathematical/source families, two priority families, exact original-checker replays and actual Cartesian physical controls have been checked. Finite high-precision diagnostics are not universal or interval proofs. Extensive AI use supported discovery, derivation, source investigation, programming, writing and internal adversarial review. This is unrefereed; no independent human peer review or formal proof verification is claimed. Required whole-package reviews and actual publication outcomes are recorded separately, not self-certified by this dated preparation snapshot.

All23 original files and dated inherited reviews remain byte-exact under history/original_submission_20261016/. Current presentation manifests bind current files; historical manifests and historical receipts bind that archive, not this edited proof. The original author budget remains one of five substantive turns.
