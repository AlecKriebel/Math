# An exact least-period criterion for focal-distance products

**5100006 / AMR-050-0006 / k114. Published research note, 11 October 2026.** Alec Kriebel, independent researcher, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). AI-assisted and unrefereed. Publication: [https://doi.org/10.5281/zenodo.23306203](https://doi.org/10.5281/zenodo.23306203). Fresh whole-package R2 passed after the R1 reference repair.

## 1. Exact theorem and source interpretation

Let the boundary E and caustic C have semiaxes a>b>0 and A>B>0, with a>A, b>B and a²-b²=A²-B²=c²>0. Fix a periodic billiard family tangent to C, with **least period n**, vertices P_j and foci F_±=(±c,0). Define the ordinary positive Euclidean products

    D_n^± = product(j=0,...,n-1) |P_j-F_±|.

**Theorem.** Each product is independent of phase if and only if n=2 modulo 4. All admissible primitive star windings and both orientations are included. For every even n the two focal products agree at each phase. An r-fold traversal, r≥1, has product (D_n^±)^r and has exactly the same constancy status. A circle is a separate case: both foci coincide with its center and every listed product equals a^N.

For a return length N=2 modulo 4, the least period divides N and is either odd or 2 modulo 4. Hence the listed product is constant precisely when that least period is even. An unrestricted return-length reading is partly false, as the exact example in Section 5 shows. Hyperbolic and degenerate caustics are outside the theorem.

This resolves the least-period interpretation of the experimentally recorded k114 entry in [Reznik–Garcia–Koiller, Table 2](https://arxiv.org/abs/2004.12497v11); the [2021 version of record](https://doi.org/10.1007/s40598-021-00174-y) retains the entry as unproved. Historical source and review files are distinguished in README.md and SOURCE_RESOLUTION.md.

## 2. Complete real geometric bridge

Put k=c/A in (0,1), K=K(k), K'=K(sqrt(1-k²)); all Jacobi functions use **modulus k**. [Stachel, Theorem 4.3 and (4.9), p.1614](https://doi.org/10.1007/s40879-021-00524-2) gives

    P(u)=(-a sn u,b cn u),
    a=A dn(v)/cn(v), b=B/cn(v), 0<v<K,
    P_j(u)=P(u+j delta), delta=2v.                         (1)

The fixed pair determines v uniquely by cn(v)=B/b. Confocality gives the other axis relation.

The real geometric bridge can also be checked directly. At Q(U)=(-A sn U,B cn U), the caustic tangent is

    -x sn U/A + y cn U/B = 1.

Jacobi addition places both P(U-v) and P(U+v) on it: substitution gives

    [dn²(v) sn²(U)+cn²(U)]/[1-k² sn²(U) sn²(v)] = 1.       (2)

Their endpoints are distinct. The contact Q lies strictly inside E, so it is inside the actual chord. The two caustic tangent directions d at P=(x,y) satisfy dᵀMd=0, where

    M = [[B²-y², xy], [xy, A²-x²]].

For the outer normal nu=(x/a²,y/b²) and perpendicular t=(-y/b²,x/a²),

    nuᵀ M t = xy c²/(a²b²) [1-x²/a²-y²/b²] = 0,
    det M = A²B² [1-x²/A²-y²/B²] < 0.

Thus reflection across the normal interchanges the two inward tangent rays, which is the elastic billiard law. These two tangents exhaust the choices from every boundary point. The real Jacobi amplitude increases strictly by 2pi over 4K, so P is bijective modulo 4K and covers every real phase; reversal chooses the opposite step.

Real injectivity gives the exact least-period condition

    delta=4K tau/n, gcd(tau,n)=1, 0<tau<n/2,               (3)

where tau is the positive turning number. Star turns tau>1 are allowed. Neither n=1 nor n=2 occurs with 0<v<K. Elementary ellipse algebra gives

    |P(u)-F_±|²=(a±c sn u)².

Since a>c, each real factor is at least a-c>0. Consequently the actual ordinary distance functions are

    g_±(u)=a±c sn u,
    D_n^±(u)=product(j=0,...,n-1) g_±(u+j delta).          (4)

No signed-distance or complex-square-root convention is used.

## 3. Full Jacobi-sine divisor and the iff criterion

Use the sine torus

    T = C/(4K Z+2iK' Z), p=iK'.

This lattice is used for sn and g_±; no identical complex lattice for the full vertex map P is assumed. [NIST DLMF 22.4](https://dlmf.nist.gov/22.4) gives two simple poles of g_+, at p and p+2K, and

    sn(p+K±v)=dn(v)/(k cn(v))=a/c,
    sn(u+2K)=-sn u.

Thus g_+ has zeros q_±=p-K±v. They are distinct and nonpolar because 0<v<K. The coefficient c≠0 prevents pole removal. Equal total zero and pole degree on a torus implies that these two zeros are simple and exhaustive.

Let H=<delta> on T, of order n. Subtract p and normalize real offsets by 4K. By gcd(tau,n)=1, H becomes {j/n modulo 1}. The two zeros differ by delta; translated through all n factors they form one double-zero coset z+H, with

    z=-1/4+tau/(2n).

The pole cosets are H and 1/2+H. This describes the complete product divisor, with multiplicities.

If n is odd, the two pole cosets are disjoint. Neither zero coset meets them, since

    nz=(-n+2tau)/4,
    n(z-1/2)=(-3n+2tau)/4

have odd numerators and are not integers. The product retains 2n simple poles.

If n is even, tau is odd and 1/2 belongs to H. The pole cosets coincide, giving n double poles. The double-zero coset cancels them exactly when

    nz=(-n+2tau)/4 is an integer,

which is equivalent to n=2 modulo 4. In that case the full divisor vanishes, so the product extends holomorphically to the compact connected torus and is constant. If n=0 modulo 4, it retains n double poles.

All products are holomorphic near the real phase line. A product retaining poles cannot be constant on that line: the identity theorem would then make its meromorphic extension constant. By (4) and the complete real parametrization, this is nonconstancy among actual physical family members. This proves both directions for g_+.

Finally g_-(u)=g_+(u+2K). Its product has the same classification. When n is even, 2K belongs to H, so cyclic relabeling proves D_n^+=D_n^- at every phase. Equivalently, (n/2)delta=2K tau and P(u+2K tau)=-P(u) pair the vertices antipodally. For n=2m=2 modulo 4, one positive constant evaluation is

    D_n^± = product(j=0,...,m-1) [a²-c² sn²(2jv)] > 0.

Each bracket is at least b².

## 4. Repetition and boundary cases

An r-fold traversal enumerates the same n vertices r times, giving (D_n^±)^r. The power map x→x^r is injective on positive reals, so repetition preserves constancy in both directions. The criterion is about least period, even when the listed return length lies in a different residue class.

For a circle, every focal distance equals its radius a, proving the separate a^N formula directly. The endpoints v=0 (coalescing boundary and caustic), v=K, and B=0 (degenerate caustic and k=1) are not included. No hyperbolic, separatrix or degenerate two-bounce extension is claimed.

## 5. Exact doubled-triangle counterexample

Take a=√15, b=√7, c=√8, A²=135/16 and B²=7/16. The strict confocal pair has a²-A²=b²-B²=105/16. Let

    T=((a,0),(-3a/4,7/4),(-3a/4,-7/4)).

Its vertices lie on E and its sides are x=-3a/4=-A and x±ay=a. They touch C because A²+a²B²=a². At the upper off-axis vertex, the inward unit rays (a/4,-1/4) and (0,-1) sum to five times the inward normal (a/20,-1/4). Symmetry verifies the other vertices. Therefore T and its central reflection are primitive three-bounce members of the same physical family.

At F_+=(c,0), their ordinary primitive products are

    (a-c)(a+3c/4)²=15a/2+3c,
    (a+c)(a-3c/4)²=15a/2-3c.

Twice traversing each triangle gives return length six, but the products differ by

    (15a/2+3c)²-(15a/2-3c)²=90ac=180√30>0.

Thus return length alone cannot replace least period.

## 6. Attribution and verification limits

The observation belongs to Reznik–Garcia–Koiller; the canonical parameter, Jacobi identities and meromorphic pole-removal method are established inputs. Method precedents include [Schwartz (2015)](https://doi.org/10.1016/j.geomphys.2014.07.024) and [Akopyan–Schwartz–Tabachnikov](https://doi.org/10.1007/s40879-020-00426-9). No first-priority, new parametrization or new-method claim is made. The bounded audit's uninspected Dragović–Gajić 2023 sections remain disclosed in SOURCE_RESOLUTION.md.

The active verify.py is the package's explicit standard-library exact checker. Its finite divisor inventories, both focal signs, repeats and exact physical controls support this analytic all-period proof; they do not prove the Jacobi identities, certify numerical error bounds or replace the universal deduction. Historical independent_review/author_replay files concern the archived primitive theorem and are not reviews or receipts for this strengthened PROOF.md. See README.md.
