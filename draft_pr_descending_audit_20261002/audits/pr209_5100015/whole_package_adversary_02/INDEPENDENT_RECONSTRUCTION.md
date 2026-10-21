# Reconstruction before previous whole-package verdicts

This analysis was written after freezing the actual package and independently reading the current proof and primary passages, before opening whole_package_adversary_01 or ROOT_REVIEW01_RESOLUTION. Initial planned mechanism and time remain in INITIAL_MECHANISM.md. Finite diagnostics are supporting checks, not the universal proof.

## Claim, exact construction and exhaustive real domain

For fixed a>b>0 and 0<lambda<b², alpha²=a²-lambda, beta²=b²-lambda, use the given orbit's trajectory ordering. Its outer vertices are intersections of consecutive boundary tangents; its center feet belong to these same tangent lines. The determinant areas, rather than filled lobe areas, are essential. The source is a pair of ellipses, not an arbitrary hyperbolic/focal caustic. Its centered target has no problematic arbitrary-point repeated-list extension.

Let k²=(alpha²-beta²)/alpha². There is a unique real v in (0,K) with cn(v)=beta/b. Then dn²(v)=a² beta²/(b² alpha²), so a=alpha dn(v)/cn(v) and b=beta/cn(v). P(z)=(-a sn(z),b cn(z)) covers E once in 4K. Addition gives the caustic tangent equation through P(z-v), P(z+v). Conversely the two tangents from a point of E to the strictly interior convex C exhaust the admissible chord choices. The billiard reflection preserves a consistently chosen orientation. Hence, after reversal if necessary, every such family has step 2v; closure gives 2Nv=4tau K, and least period makes gcd(tau,N)=1. Because C contains the origin strictly, no admissible chord crosses the origin and the chosen step is less than a half turn: 0<tau<N/2. This reconstructs the applicability of Stachel's canonical theorem, rather than assuming only sampled families exist.

## Direct line geometry, phase and all area factors

Write n(z)=(-sn(z)/a,cn(z)/b). The exact foot is Q=n/(n·n). Its denominator a²-(a²-b²)sn²(z) is at least b²>0 for real z. Intersecting the two endpoint tangent equations yields

R(z)=(-a dn(v)sn(z)/cn(v), b cn(z)/cn(v)),

where z is the chord midpoint parameter. Equivalently R=diag(a²/alpha²,b²/beta²)B(z), the ordinary pole of the caustic tangent relative to E. Thus the actual outer list is a linear image of the same orbit at phase u+v, with determinant scale ab/(alpha beta). Parallel endpoint tangents would imply antipodal endpoints, impossible for a tangent chord to the strictly interior C.

Addition of the two dn formulas gives, with f(t)=sn(t)cn(t)/dn(t),

det(P(z-t),P(z+t))=ab f(t)[dn(z-t)+dn(z+t)].

Consequently area(P)=ab f(v)T(u), and expanding four terms in each determinant of successive edge vectors gives area(Delta P)=ab[2f(v)-f(2v)]T(u). The second formula is an identity of full cyclic sums; it never presumes that skip-by-two visits one connected cycle.

For w=K-v, cn(w)=k' sn(v)/dn(v)>0 and dn(w)=b/a. Directly adding P(z+w)+P(z-w), and using P(z-2K)=-P(z), gives

Q(z)=diag(b/a,1)[P(z+K-v)-P(z+K+v)]/(2cn(w)).

Its determinant is b/(4a cn²(w)); the common negative edge-vector sign preserves planar determinant area. Therefore

A'=(a²b²/(alpha beta))f(v)T(u+v),

A'_O=b²[2f(v)-f(2v)]T(u+K-v)/(4cn²(w)).

T has period 2v by cyclic reindexing, so the latter trace can be shifted by +2v. There is no division by either area, and no unproved zero-area exception.

## Universal parity and residue argument

Set r=gcd(N,2), q=N/r. The shifts 2jv modulo 2K form the subgroup {2Kj/q}, each with multiplicity r, independently of coprime winding. Thus T=rUq. The condition 4 does not divide N is exactly q odd.

The standard dn periods are 2K and 4iK', with sign reversal under 2iK'. Poles are simple at iK'+2mK+2niK'. For odd q the q distinct subgroup-translated poles never coincide with a translated zero: a collision would require K in the odd real subgroup. At iK', Res(dn)=-i and dn(iK'+t)=-i cs(t). Pairing t with 2K-t gives

Res(product dn)/Res(Uq)=(-i)^(q-1) product_{j=1}^{q-1} cs(2Kj/q)=product_{j=1}^{(q-1)/2} cs²(2Kj/q)=Cq.

Subgroup translation and imaginary antiperiodicity transfer this ratio to every pole. The difference product(dn)-Cq Uq is therefore entire elliptic and constant; antiperiodicity forces the constant to zero. Multiplying by the K shift and using dn(t+K)=k'/dn(t) yields Uq(z)Uq(z+K)=(k')^q/Cq². This is the cited old cyclic identity; it is not new mathematics or independent priority evidence.

The native proof's alternative reflected-zero argument is also complete: evenness plus half-period signs gives dn(K+iK'+t)=-dn(K+iK'-t). The odd subgroup avoids K, so every term there is finite and opposite subgroup terms cancel, including the zero self-paired term. Each possible simple pole of Uq has a zero in its complementary K-shift. Conversely each possible pole of the second factor has a zero in the first. Thus all product poles are removed. Repeated summands multiply a residue, never its pole order.

The explicit invariant is

 a² b⁴ f(v)[2f(v)-f(2v)] r²(k')^q / [4alpha beta cn²(K-v) Cq²].

All real denominators: alpha,beta,a,b>0; dn(t)>=k'>0; cn(v)>0; cn(K-v)>0; addition denominators >=1-k²>0; normal norm positive; each Cq factor has argument in (0,K) and is finite nonzero. There is no omitted denominator from geometric line intersection. Multiplying length scales gives length^4, as required.

## Boundary cases and limits

Stars retain cyclic trajectory order throughout. Reversal negates both signed areas. A d-fold traversal multiplies both sums by d and product by d²; if its listed length avoids 4, its least period does too. Strict interior elliptical caustics preclude genuine period one or two. The q=1 trace identity is valid although no such primitive billiard is included.

At k=0 the separate circular geometry has A'=NR²tan(v) and A'_O=NR²sin(v)cos(v), hence product N²R^4 sin²(v). The elliptic formula has this continuous limit because Uq becomes q and Cq becomes 1/q. Limits with beta=0 or lambda=0 are outside the theorem, so no unsupported endpoint extension is used.

Period four really fails on a common admissible caustic: for axes (2,1), lambda=4/5, the axis diamond and the normal-bisected rectangle have (A',A'_O)=(8,4) and (10,5). Both satisfy forward specular reflection and actual segment tangency. Products 32 and 50 differ. No denominator failure is needed to produce this obstruction; the odd-subgroup trace argument simply no longer holds. Circles remain constant in this excluded class by rotation, consistent with the weaker statement that a general 4-divisible family is not asserted.

## Attribution hypotheses checked separately

Exact theorem comparison uses Ferudun version 1.1 Theorem 2 and Section 6, with full odd and twice-odd/list repetition scope; version 1.0 is a narrower primitive even arbitrary-point result. Earlier KLS cyclic identity, KS Landen transformation, AST foot/velocity and skew hodograph, BT telescope, Stachel canonical coordinates and CC complex methods are mechanisms requiring express credit. No absence search can establish firstness, novelty or historical independent non-derivation. The snapshot's own chronology assertions require byte-bound receipt checks; future release operations remain outside this review.
