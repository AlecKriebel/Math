# Turn 4: fourth-power closure and its squarefree obstruction

Substantive author turn **4/5**, 2026-10-02. The attempt to combine the prime constructions gives a closure operation preserving all required knot properties, together with an exact limitation of that operation. The full arbitrary-n conjecture is still unresolved.

## 1. Balanced two-terminal networks

Use T(N),S(N) as in turn3. A network is balanced if T(N)=S(N). The following construction realizes every square as its common count.

For an integer q≥2, let A_q be a path of q edges, so (T,S)=(1,q). Let B_q be q−1 parallel edges with one additional series edge, so (T,S)=(q−1,q). Put A_q and B_q in parallel. The resulting network C_q has

    T(C_q)=1·q+(q−1)q=q²,    S(C_q)=q·q=q².      (12)

It has2q edges and every edge/vertex lies on a simple terminal-to-terminal path. Its two-terminal plane dual has the same pair (q²,q²) and the same path property. For q=1, take C_1 to be a single edge.

## 2. Fourth-power closure with explicit symmetry hypothesis

Suppose an embedded loopless graph G has no bridges or cut vertices and has an orientation-preserving plane duality pairing distinct edges e and f. Assume that the duality on this pair is involutive in the natural primal-dual identification, so that paired dual-network replacement is equivariant. These are the explicit dualities of the two- and four-spoke wheel constructions used here; no such involution is asserted for every self-dual graph or every alternating achiral knot.

Replace e by C_q and f by its two-terminal plane dual. The same ribbon-duality argument as in turn3 preserves plane self-duality. The terminal-path argument there preserves connectedness without cut vertices, loops or bridges. The substitution formula(7) contributes exactly q² for each replaced edge, whether or not that base edge is in a spanning tree. Therefore

    τ(new G)=q⁴ τ(G).                            (13)

For odd q and odd τ(G), the alternating medial diagram is again a prime alternating achiral knot. The inserted ribbons are exchanged by the extended duality, so they supply distinct paired edges for further applications. Thus the construction may be iterated; equivalently the fourth-power factors may be combined.

This operation is not connected sum. In particular its preservation of primeness follows from the explicit absence of cut vertices, rather than from a false multiplicativity claim for prime knots.

## 3. A paired-duality realization of every primitive sum of two squares

The two-spoke wheel consists of a hub o, two rim vertices v_0,v_1, the two spokes, and two distinct parallel rim edges r_0,r_1. Its two interior faces are F_0,F_1 and its outer face is U. The identification o↦U, v_i↦F_i is a plane duality pairing spoke s_i with r_i. The cyclic orders agree; equivalently it is the two-spoke version of the ribbon duality in turn1. It has no loops, bridges or cut vertices.

Substitute a primitive network with counts(u,v) in s_0 and its dual in r_0; leave the other pair as single edges. The weighted two-vertex Laplacian, or direct enumeration of the five base trees, gives

    τ = u²+(u+v)².                              (14)

Indeed, for rational spoke weights a,b and reciprocal paired rim weights the prefactor-ab tree polynomial is a²b²+(a+b)²; put (a,b)=(u/v,1) and multiply by v² as in turn3. Every primitive positive sum A²+B² with 0<A<B is obtained by u=A,v=B−A. Its odd values therefore give paired-duality graph realizations. This rederives the already-known rational achiral-knot case in a form compatible with (13); no new primitive-case theorem is claimed.

## 4. Consequences for the original realization problem

### All prime-power versions of the5p² ray

For every odd prime p and every integer e≥0, there is a prime alternating achiral knot with determinant

    5p^{2e}.                                    (15)

For p≡3 mod4 and odd e, start with turn3's determinant5p² and apply (13) with q=p^{(e−1)/2}. For even e, start with determinant5, the two-spoke wheel with u=v=1, and take q=p^{e/2}. These include e=0 by q=1.

For p≡1 mod4, the known primitive sum-of-two-squares case supplies determinant5p², again in the paired form(14). To check the required primitivity explicitly, write p=a²+b² with coprime a,b by the classical sum-of-two-squares theorem. The real and imaginary parts of (2+i)(a+ib)² have squared norm5p². A common prime divisor must be p or5. For p≠5 the matrix with determinant5 giving multiplication by2+i is invertible modulo p, and a²−b²,2ab cannot both vanish modulo p. Divisibility of both coordinates by5 is excluded because5p² has exactly one factor5. Thus the representation is primitive. For p=5, use125=2²+11². The coordinates are nonzero and have different absolute values because their norm is odd and not a square. Order their positive absolute values to apply(14). Then use the same odd/even e argument.

### A broader credited-primitive extension

Let n be an odd sum of two squares for which every prime ℓ≡3 mod4 occurs to an exponent divisible by4. Write

    n=q⁴h,

where q contains precisely those bad-prime factors and h has no prime divisor3 modulo4. If h>1, the classical primitive representation theorem gives coprime nonzero A,B with h=A²+B². For clarity, this is the standard Gaussian-integer consequence of choosing one of each conjugate prime factor; it is prior arithmetic, not a new result. Formula(14) followed by(13) realizes n. If h=1, then n=q⁴ is a perfect square, covered by the credited prior square theorem of Stoimenow; the excluded value1 is still excluded. This deduction does not cover a bad-prime exponent congruent to2 modulo4 in a general primitive core.

## 5. A sharp obstruction to squarefree balanced multipliers in this route

A two-terminal series-parallel network made from single edges by series and parallel composition cannot have

    T=S=g>1

when g is squarefree. This includes, but is not limited to, the prime common-count obstruction already implicit in the prior arborescent discussion.

To prove it, use the last binary composition, with positive counts(T_1,S_1),(T_2,S_2). In the parallel case,

    S_1 S_2=g,   T_1 S_2+S_1 T_2=g.

Squarefreeness implies gcd(S_1,S_2)=1. Reduction modulo S_1 and S_2 shows S_i divides T_i. Since all counts are positive, T_i≥S_i, making the second expression at least2g, a contradiction. In the series case,

    T_1 T_2=g,   T_1 S_2+S_1 T_2=g,

and the same argument with T,S interchanged gives a contradiction. The base single edge has g=1. This proves the claim for every such network, without an edge-number bound.

Thus the balanced-network method supplies arbitrary fourth-power factors, but cannot use a squarefree multiplier g to multiply the determinant by g² within the series-parallel class. A more general non-series-parallel balanced network, a different determinant-changing operation, or a direct construction may still work. No obstruction to a prime alternating achiral knot is inferred from this network obstruction.

## 6. Remaining gap

We now cover the entire5p^{2e} prime-power ray and the stated fourth-power extension of the primitive class. General n=q²h with a mixed squarefree bad-prime part q and arbitrary primitive core h remains uncovered. In particular, multiplying two of the prime-ray examples by connected sum is not an admissible repair. The original target remains unresolved4/5. The final turn will test a more general construction rather than claiming multiplicative closure that has not been proved.
