# Independent full-claim derivation

This final derivation closes the ten families frozen in INITIAL_RECONSTRUCTION.md. That original remains unchanged. The proof concerns every admitted least period, caustic, phase and primitive winding, rather than the finite test ranges. No numerical assertion is a proof premise.

## Real billiard and ordinary lengths

Assume a>b>0, A>B>0, a>A, b>B and a²−b²=A²−B²=c²>0. Put k=c/A, k'=B/A and use Jacobi modulus k, with K=K(k), K'=K(k'). There is a unique v∈(0,K) with cn(v)=B/b. Confocality gives a=A dn(v)/cn(v). The canonical parametrization is P(u)=(-a sn(u),b cn(u)), and successive vertices have step δ=2v. The actual Stachel Theorem 4.3 and equation (4.9), printed1614/physical13, state precisely these data after changing his modulus letter m to k. His m denotes the modulus, not the software parameter k².

The caustic tangent at Q(U)=(-A sn(U),B cn(U)) is −x sn(U)/A+y cn(U)/B=1. On substituting P(U±v), the addition formulas reduce its left side to

    [dn²(v) sn²(U)+cn²(U)]/[1−k² sn²(U) sn²(v)] = 1.

The denominator is positive for real U. Strict nesting makes Q(U) the interior point of the actual chord. The direction-tangency quadratic at (x,y) is dᵀMd=0, where

    M = [[B²−y², xy], [xy, A²−x²]].

For outer normal ν=(x/a²,y/b²) and tangent t=(-y/b²,x/a²), expansion gives

    νᵀMt = xy c²/(a²b²) · (1−x²/a²−y²/b²)=0,
    det M = A²B²(1−x²/A²−y²/B²)<0.

Thus normal and tangent diagonalize an indefinite direction form. Reflection interchanges the two distinct tangent lines; taking the inward directions gives elastic reflection. This is a physical billiard, not merely an arbitrary inscribed polygon. The rational algebra controls check this bridge independently in399 cases.

On the real axis, |P(u)−F±|²=(a±c sn(u))². Since a>c and |sn(u)|≤1, these are ordinary positive Euclidean lengths g±(u)=a±c sn(u). No sign, complex square root, or squared-distance reinterpretation is needed. The real boundary parametrization is injective modulo4K. Hence exact vertex period n is equivalent to δ=4Kτ/n with gcd(τ,n)=1, 0<τ<n/2. Reversal replaces δ by−δ without changing its cyclic subgroup. This includes every admitted primitive star winding. Periods1 and2 are excluded by0<δ<2K.

## Complete divisor, including its multiplicities

Work on T=C/(4KZ+2iK'Z). Official DLMF22.4 Table1 and Table3 give the periods, the simple poles p=iK' and p+2K of sn, and the identities

    sn(z+2K)=−sn(z),
    sn(p+z)=1/(k sn(z)),
    sn(K±v)=cn(v)/dn(v).

Consequently g+ has zeros q±=p−K±v. They are distinct, nonpolar points because0<v<K. Its two poles remain simple because c≠0. An elliptic function has equally many zeros and poles counted with multiplicity, so these two roots exhaust the zero divisor and each is simple. This degree argument is necessary; two candidate roots alone would not establish the full divisor. Since g−(u)=g+(u+2K), the second focus follows by translation.

Let H=⟨δ⟩, of exact order n. The divisor of D_n^+(u)=∏_(j=0)^(n−1)g+(u+jδ) is a sum of translated point divisors. Subtract p and divide the real coordinate by4K. The two zero sets are the same coset because q+−q−=δ. Thus there is a double-zero coset z+H with

    z=−1/4+τ/(2n).

The pole cosets are H and1/2+H. If n is odd they are disjoint and simple. Neither meets the zero coset, because nz=(−n+2τ)/4 and n(z−1/2)=(−3n+2τ)/4 are nonintegers with odd numerator. There remain2n simple poles and n double zeros.

If n is even, τ is odd and1/2∈H. The poles form n double poles. Cancellation is complete exactly when nz∈Z, namely when n≡2 mod4. If n≡0 mod4, the zero and pole cosets are disjoint and n double poles remain. This arithmetic proves the classification for all coprime n,τ. The finite point-divisor sums independently corroborate it but do not establish the universal statement.

A zero divisor makes the product holomorphic on the compact connected torus and therefore constant. When poles remain it is nonconstant. The real line has no poles and lies in a holomorphic neighborhood; constancy on any open real-phase interval would force global meromorphic constancy by the identity theorem, contradicting the retained poles. Thus complex nonconstancy proves physical phase variation. The translated g− has exactly the same classification. For even n,2K∈H, so both focal products agree at each phase, independently of whether that common function varies.

For n=2m≡2 mod4, antipodal pairing gives the positive value, evaluated at phase0,

    D_n^± = ∏_(j=0)^(m−1)[a²−c² sn²(2jv)].

Its units are length^n. Scaling the configuration by s>0 multiplies it by s^n and cannot affect phase constancy.

## Repetitions and boundaries

An r-fold traversal repeats each positive factor r times, so D_(rn)^±=(D_n^±)^r. The positive-power map is injective; therefore constancy depends on least period n, regardless of listed length. If a return length N is2 mod4, its divisor n is odd or2 mod4. In that particular return-length class constancy is equivalent to even least period. This statement includes every positive integer repetition count.

For c=0 the foci coincide with the center and all vertex distances equal a, giving a^N. This separate circular assertion is correct. Its c=0 removal of every sn pole prevents using the noncircular divisor criterion there. The limits B→0 (k→1), v→K, v→0, a caustic touching the boundary, hyperbolic caustics and degenerate two-bounce paths are excluded. No uniform positive oscillation lower bound in these limits is asserted; ordinary floating-point inability to resolve small variation does not contradict the pole proof.

## Exact physical falsifiers

The target's triangle has a²15,b²7,c²8,A²135/16,B²7/16 and vertices (a,0),(-3a/4,±7/4). They lie on the outer ellipse. The sides x=−A and x±ay=a are caustic tangents because A²+a²B²=a². At the upper vertex the inward unit directions are(a/4,−1/4),(0,−1), whose sum is5(a/20,−1/4), a positive multiple of the inward normal. Axis reflection and symmetry handle the other vertices. Central negation shifts the phase by2K in the same family. The two positive F+ products are15a/2±3c. Twice traversing them produces unequal six-event products with difference90ac=180√30>0. This verifies the paper's counterexample to the unrestricted return-length interpretation, and also defeats an unjustified odd-period equality between foci.

An independently reconstructed four-bounce comparison works for every a>b>0. Put s²=a²+b², A=a²/s, B=b²/s. The axis diamond(a,0),(0,b),(-a,0),(0,-b) and axis-parallel rectangle(±A,±B) share that strict confocal caustic. The identity A²/a²+B²/b²=1 gives both inscribedness/tangency relations. Axis symmetry proves the diamond reflection law. At a rectangle corner the normal components have equal magnitude A/a²=B/b²=1/s, so the horizontal and vertical rays reflect correctly. The focal products are respectively

    a²b² and 4a⁴b⁴/(a²+b²)²,

with positive difference a²b²(a²−b²)²/(a²+b²)². For a2,b1 they equal4 and64/25. Thus even-period pointwise equality between foci cannot be confused with invariance. The same fixture is present in the subsequently read native checker; its appearance there does not retroactively make this a new target-independent family. The broader all-axis formula and physical reconstruction were frozen before native code was read.

## Closure of the initial exact-gap table

| Mechanism | Final evidence | Remaining mathematical gap |
|---|---|---|
| Geometry/category/modulus | Focal identity, tangent/reflection derivation, actual Stachel Thm4.3 | None found in stated domain |
| Primitive order/star/orientation | Real injectivity, cyclic subgroup proof, direct signed-step controls | None found |
| Complete divisor | Actual DLMF periods/shifts, elliptic degree and multiplicities | None found |
| Universal parity criterion | Coset arithmetic above;982 finite primitive-pair corroborations | None found; finite corroboration is not the proof |
| Real-phase necessity | Pole retention plus identity theorem | None found |
| Focal equality/value |2K subgroup permutation and antipodal pairing | None found |
| Repetitions/circle/limits | Positivity/injectivity,380 finite return cases and circle controls | None found; excluded singular cases remain excluded |
| Physical counterexamples | Exact radical triangle and28 four-bounce configurations | None found |
| Primary attribution | Actual RGK/Stachel/DLMF and prior pole-removal bodies read | Bibliographic coverage is bounded; no firstness certification |

No narrowing, repair, or replacement theorem is proposed.
