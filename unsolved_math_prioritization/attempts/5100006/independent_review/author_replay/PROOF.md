# A cyclic elliptic-function norm proves focal-product invariant k114

**5100006 / AMR-050-0006. Complete proof candidate, two approaches; independent review pending.** No novelty or human peer-review claim.

## 1. Exact theorem and prior inputs

Let the outer ellipse have semiaxes a>b>0 and foci f_+=(c,0), f_−=(−c,0), c²=a²−b². Fix a strictly nested confocal elliptical caustic with semiaxes alpha>beta>0, so alpha²−beta²=c². Suppose its billiard family has least period N congruent to2 modulo4. Then each ordinary focal-distance product

    product_(i=0)^(N−1) |P_i−f_+|,
    product_(i=0)^(N−1) |P_i−f_−|

is constant over the Poncelet family, and the two constants are equal.

This is k114 in Reznik–Garcia–Koiller, arXiv:2004.12497v11, Table2 on printed p.5, also in the published companion *Fifty New Invariants*. Its introductory definition is the nondegenerate confocal-ellipse pair. We retain that scope: no hyperbolic caustic or degenerate two-bounce orbit. Simple and star polygons of even least period are included. Repeating an admissible polygon preserves constancy, but an odd-period polygon repeated twice is not silently reclassified as a primitive even one. N=2 does not occur for a finite nondegenerate nested elliptical caustic. A circle has coincident foci at its center and constant product a^N directly.

The proof uses Stachel's published canonical parametrization, *On the motion of billiards in ellipses*, European Journal of Mathematics8 (2022),1602–1622, Theorem4.3 and equation4.9, DOI10.1007/s40879-021-00524-2. This is Theorem2 in the author preprint arXiv:2105.03624. The modulus is the **caustic** eccentricity, not the outer ellipse eccentricity. The complex pole-cancellation strategy is classical in elliptic-billiard invariants; compare Akopyan–Schwartz–Tabachnikov, arXiv:2001.02934. The particular norm calculation below is written out, with no assertion that it was previously unknown.

## 2. Canonical parameter and ordinary distances

Put k=c/alpha in(0,1), K=K(k) and K'=K(sqrt(1−k²)). All Jacobi functions below use modulus k, rather than parameter k². Stachel's parametrization is

    P(u)=(−a sn(u,k), b cn(u,k)).                            (1)

There is a fixed v in(0,K) such that one oriented billiard step sends u to u+2v, with

    a=alpha dn(v,k)/cn(v,k),   b=beta/cn(v,k).              (2)

For a primitive N-periodic orbit,

    v=2K tau/N,   gcd(tau,N)=1,   0<tau<N/2,                (3)

where tau is the turning number. Reversing the orbit does not change the product, so this orientation loses nothing.

Write N=2m. Our hypothesis makes m odd, and (3) makes tau odd and coprime to m. After m steps the parameter changes by2mv=2K tau. Standard Jacobi shifts give P(u+2K tau)=−P(u). Thus the opposite vertices pair exactly.

For any real point (x,y) on the outer ellipse, its focal distances are a−cx/a and a+cx/a, both positive. With x=−a sn u, their product is

    F(u)=a²−c² sn²u.                                       (4)

Pairing the N vertices into m opposite pairs therefore gives the original one-focus product as

    R(u)=product_(j=0)^(m−1) F(u+2jv).                     (5)

The same expression is obtained for the other focus. No square-root branch has been introduced: (5) is an equality of positive real products.

## 3. The complete divisor of F

Extend u to the complex plane. The standard Jacobi identities and pole data used here are in NIST DLMF22.4, Tables22.4.1 and22.4.3:

    sn(u+2K)=−sn u,       sn(u+2iK')=sn u,
    sn(z+K+iK')=dn z/[k cn z].                             (6)

The poles of sn are simple and occur at2rK+(2s+1)iK'. Hence F is an elliptic function for

    Lambda=2K Z+2iK' Z,

with precisely one double pole on C/Lambda, at p=iK'. The coefficient c² is nonzero, so this pole is not removable. There are no other poles on that torus.

From (2), (6), and c²=k² alpha²,

    F(K+iK'±v)
      = a²−c² dn²(v)/[k² cn²(v)]
      = a²−alpha² dn²(v)/cn²(v)=0.                         (7)

The two points p+K+v and p+K−v are distinct modulo Lambda because0<v<K. They are not p modulo Lambda. An elliptic function has as many zeros as poles counted with multiplicity, so the two displayed distinct zeros exhaust the zero divisor and are each simple. In divisor notation,

    div(F)=[p+K+v]+[p+K−v]−2[p].                          (8)

This accounts for every zero and pole; a finite sample of orbit products would not establish (8).

## 4. Cancellation of the cyclic norm divisor

Let delta=2v. Translation by delta on C/Lambda has order m, since delta=2K tau/m and gcd(tau,m)=1. Also mv=K tau and tau is odd, so K is congruent to mv modulo2K. As m is odd, both integers

    h_+=(m+1)/2,   h_−=(m−1)/2

exist, and

    p+K±v congruent to p+h_± delta modulo Lambda.           (9)

For R in (5), the poles lie at p−j delta, j=0,...,m−1, each of order2. The first zero in (8), translated through all factors, lies at p+(h_+−j)delta; those m points are a permutation of the same pole set. The second zero gives a second copy of that same set. Thus each order-two pole is canceled with exactly two simple zeros and

    div(R)=0.

Consequently R extends to a holomorphic function on the compact connected torus C/Lambda and is constant. Its real values are positive and finite by (4), so the constant is positive. Equation(5) proves the claimed focal-product invariance for the whole family.

For example, its value can always be written without choosing a moving orbit as

    R(0)=a² product_(j=1)^(m−1) [a²−c² sn²(2jv,k)].        (10)

No claim of a simpler universal closed expression is needed for constancy.

## 5. Checks, parity and credit

The proof's parity restriction has a concrete role: for N divisible by4, m is even and the zero shifts K±v are half-integer rather than integer multiples of delta. The cancellation argument does not apply. We make no assertion about the separately assigned area/half-angle invariants k107 or k108. Their angle conventions are irrelevant here; Stachel's exterior angle must not be substituted for the source's internal angle.

The verifier checks the rational lattice permutation and multiplicities for every tested primitive rotation with N=2 modulo4, the algebraic zero relation, positivity and confocal-axis identities, and two exact six-bounce focal-product expressions. Supplementary high-precision Jacobi evaluations are explicitly labeled numerical diagnostics; they are not the proof. Sections3–4 establish constancy at all periods and all phases.

The antipodal pairing and ordinary focal-distance normalization agree with the earlier k405/k603 campaign work, which is credited in the source manifest. The required pairing here also follows directly from the published parameter shifts, so no unreviewed sibling result is used. The earlier k405 review's symmetric six-bounce coordinates are reused only as controls. A targeted literature check found Stachel's canonical parametrization and other product invariants, and the older complex-method paper, but did not establish priority for k114. No first-discovery claim is warranted.

The author preprint prints an incorrect sign in its dn(u+2K) shift line; the proof uses the DLMF shift table and only the correctly stated sn/cn shifts and equation(2). This harmless adjacent typo is not used as an identity.

The inherited native runtime was used without changes; its exact model identifier was not exposed. Independent adversarial review is required before any claimed-result PR.

### Primary sources

- Original invariant: https://arxiv.org/abs/2004.12497v11
- Published companion: https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf
- Stachel published canonical parametrization: https://doi.org/10.1007/s40879-021-00524-2
- Full author preprint: https://arxiv.org/abs/2105.03624
- Jacobi periods, poles and shifts: https://dlmf.nist.gov/22.4
- Prior complex proof method: https://arxiv.org/abs/2001.02934
- Earlier distinct campaign results: https://github.com/AlecKriebel/Math/pull/110 and https://github.com/AlecKriebel/Math/pull/140
