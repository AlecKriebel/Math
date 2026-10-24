# Arithmetic approach to Kourovka21.135

Checkpoint: **2026-10-24T18:06:00Z**. Discovery completion estimate: **12%** for this approach, reflecting useful reductions and exact barriers rather than a probability of success. Status: **partial results only; no full resolution, originality claim, or publication candidate**.

The target concerns arbitrary finite G,H with the same irreducible complex degree **multiset**, with R(G)=1. Throughout, D is that multiset, m(d) its multiplicity, n=Σm(d)d², L=lcm{d:m(d)>0}, and δ=n/L. These are determined by D. Frobenius divisibility makes δ a positive integer for an actual finite-group spectrum. Write

    M_p(D)=Σ_{p∤d}m(d)d²,     α_p(D)=M_p(D)/n.

## 1. Itô divisibility isolates the possible minimal abelian normals

**Lemma1.** Every abelian normal subgroup A of a group H with spectrum D has |A| dividing δ.

**Proof.** Itô's theorem says d divides [H:A] for every irreducible degree d. Hence L divides [H:A], and δ=|A|([H:A]/L). This uses divisibility, not merely the bound d≤[H:A].

Consequently δ=1 implies R(H)=1. Indeed, any nontrivial solvable normal subgroup contains a nontrivial H-minimal normal subgroup N, necessarily elementary abelian of order p^a. More explicitly, take the last nontrivial term of its derived series, a characteristic abelian normal subgroup, then a nontrivial H-minimal subgroup within that term. Lemma1 rules it out.

This implication does not require R(G)=1 in advance. It is a standard consequence of Itô's1951 theorem, not a claim of a new theorem. Since irreducible degrees of a direct product are products,

    L(A×B)=L(A)L(B),       δ(A×B)=δ(A)δ(B).

The equality follows prime by prime by taking maximum valuations. Thus arbitrary products of groups with δ=1 have the same elementary positive answer. In particular δ(PSL2(q))=1 for all prime powers q≥4: for q even, L=lcm(q,q−1,q+1)=q(q²−1); for odd q>5 the three degrees q,q−1,q+1 occur and their lcm is q(q²−1)/2. The exceptional q=5 has degrees1,3,3,4,5 and the same equality.

**Primary dependency:** N. Itô, *On the degrees of irreducible representations of a finite group*, Nagoya Math. J.3(1951),5–6, DOI10.1017/S0027763000012162. Its theorem is stated for maximal abelian normal subgroups; extending any A to such a subgroup gives the version used here. A local primary PDF and its checksum are in sources/manifest.json.

## 2. Central elementary abelian normals leave stronger numerical traces

Let N=C_p≤Z(H). By Schur's lemma each irreducible representation is scalar on N, with one central character λ∈Irr(N). For every λ,

    Σ_{χ∈Irr(H|λ)}χ(1)² = n/p.                         (2.1)

For example, the central idempotent (1/p)Σ_{z∈N}λ(z)⁻¹z has image of dimension n/p in C[H], while its simple matrix blocks have dimensions χ(1)². Equivalently use the induced character λ^H and Frobenius reciprocity.

If N≤H′, determinants of every representation are trivial on N. Thus λ(z)^χ(1)=1, and for λ nontrivial this forces p|χ(1). It follows that:

1. All p-prime degrees belong to the trivial central-character block, so M_p≤n/p.
2. Every nontrivial block has weight n/p and uses only p-divisible degrees. Therefore gcd{d²:p|d} divides n/p. In particular p³ divides n. If there are no p-divisible degrees then a nontrivial block is impossible outright.
3. The number n/p−M_p must be representable as a sum of p-divisible degree squares, using each degree at most its multiplicity. This is a necessary condition for the trivial block, not a sufficient condition for a group or for all other blocks.

If N is not contained in H′, its intersection with H′ is trivial because |N|=p. Some linear character η of H is faithful on N: characters of the subgroup NH′/H′ of the finite abelian group H/H′ extend to that group. Tensoring by η permutes Irr(H), preserves degree, and cycles the central character through p distinct values. Every orbit has length divisible by p, hence

    p divides m(d) for every d.                          (2.2)

No order-p assumption on η is needed for this orbit argument. If additionally m(1)=p, η itself has order p and H=N×ker(η).

These are deductions from the ordinary character theory described above. They do not reconstruct character kernels or the normal lattice from D.

## 3. A perfect-group certificate and a restricted infinite family

The number m(1)=|H/H′| is read from D. Suppose m(1)=1. A minimal abelian normal N=C_p^a satisfies p^a|δ by Lemma1, and conjugation gives a homomorphism H→GL_a(p). Its image is perfect. If GL_a(p) is solvable, the image is trivial. Then N is central and its H-minimality forces a=1.

Thus the following is a valid sufficient certificate:

    For every p|δ, all GL_a(p) with1≤a≤v_p(δ) are solvable,
    and M_p>n/p.

Then R(H)=1. The solvability condition holds if v_pδ≤1 for arbitrary p, or if p=2 or3 and v_pδ≤2. GL1(p) is cyclic; GL2(2) and GL2(3) are solvable. Larger ranks are not covered automatically. Empty prime support (δ=1) gives Lemma1 directly.

For A7, hook lengths give

    D(A7)={1,6,10,10,14,14,15,21,35},
    n=2520, L=210, δ=12,
    M2=1892, α2=473/630;
    M3=1818, α3=101/140.

Both M2>n/2 and M3>n/3. The only possible ranks are a≤2 at2 and a≤1 at3. This recovers a positive answer for A7 by elementary arithmetic. Full simple-group recognition already gives this case, so no priority claim is made.

More generally, **every degree-multiset twin of A7×PSL2(2^f), f≥2, has trivial solvable radical**. To verify the unbounded family, put q=2^f≥4, S=PSL2(q). Its degrees and multiplicities are

    1 once, q once, q−1 repeated q/2 times,
    q+1 repeated (q−2)/2 times.

It has δ(S)=1, and

    α2(S)=1−q/(q²−1)≥11/15,
    α3(S)=(q+3)/(2(q+1))>1/2     if q≡1 mod3,
    α3(S)=1/2+1/(q(q−1))>1/2    if q≡−1 mod3.

For products, α_p is multiplicative, because a product degree is p-prime exactly when both factors are. Therefore δ(A7×S)=12 and

    α2(A7×S)≥(473/630)(11/15)=5203/9450>1/2,
    α3(A7×S)>(101/140)/2=101/280>1/3.

The perfect-group certificate proves the claim for every f≥2. The finite checks q=4,…,1024 corroborate these formulas; they are not the proof of the infinite quantifier. This remains a restricted result and does not settle21.135. Its originality has not been established, and existing product recognition results may already imply it.

## 4. The mass test by itself fails: an exact affine barrier

Let V=F4² additively, S=SL2(4)=PSL2(4)≅A5, and H=V⋊S. Then H is perfect: S is perfect and [V,S]=V, since V is a nontrivial irreducible F2S-module. For irreducibility, S is transitive on the15 nonzero vectors, so a nonzero invariant subspace must contain all of them. The radical is exactly V: its image in the simple quotient S is solvable normal and hence trivial, while V itself is solvable normal.

The dual action is transitive on the15 nontrivial characters of V; the alternating F4-bilinear determinant form composed with the field trace gives a nondegenerate invariant F2-pairing identifying V with its dual. A stabilizer has order4 and is C2². A stabilized λ extends to V⋊S_λ by λ(v,s)=λ(v). Its four twists by Irr(S_λ) induce four characters of degree15. Together with the inflated A5 characters this gives

    D(H)={1,3,3,4,5,15,15,15,15}.

Thus |H|=960, δ=16, m(1)=1 and M2=944>480, yet R(H)=V≠1. The missing hypothesis in the mass-only criterion is the exclusion of noncentral rank4 minimal normal modules. This is not a counterexample to21.135: no radical-free group with this degree multiset is supplied.

The exact script enumerates all60 determinant-one matrices over F4, verifies both natural and dual orbit sizes15, and verifies that the order4 dual stabilizer is abelian of exponent2. The character induction argument is a proof dependency in addition to those finite checks.

## 5. Multiplicity gcd does not detect radical-freeness

A tempting universal assertion is that a radical-free group must have gcd_d m(d)=1. It is false.

Take G=PSL2(16)⋊C2 where the involution acts by the field automorphism x↦x^4. Then

    D(G)={1^2,16^2,17^6,30^4,34^2},
    |G|=8160, L=4080, δ=2, gcd_d m(d)=2.             (5.1)

Here an exponent is multiplicity, not a group power. G has trivial radical: any solvable normal subgroup centralizes its simple socle, and the centralizer of that socle inside its automorphism group is trivial.

For a direct verification of the multiplicities, characters of PSL2(q) of degree q+1 are parametrized by nonzero indices j modulo q−1 identified under sign, while degree q−1 uses indices modulo q+1 identified under sign. The field automorphism acts as multiplication by4. Modulo15 there are three fixed sign-pairs and two length2 orbits. Modulo17 there are four length2 orbits and no fixed pair. Each invariant character has two extensions; each length2 orbit induces one character of twice the base degree. This gives (5.1), including the invariant trivial and Steinberg characters.

This is a stronger arithmetic barrier than merely having a common multiplicity factor. Dividing all multiplicities in(5.1) by2 produces

    D0={1,16,17^3,30^2,34},       Σ_D0 d²=4080=L(D0).

Every degree divides4080; all the elementary order and degree-divisibility tests pass. As an associative algebra, C[G]≅C[C2]⊗B where B has the displayed matrix blocks. None of this proves that B=C[K] for a finite group K.

In a degree twin H of G, Lemma1 forces any minimal abelian normal subgroup to be a central C2. The derived-central case is excluded already by the necessary quotient-block equation:

    4080−(2+6·17²)=2344,
    2344≠256a+900b+1156c
       for 0≤a≤2, 0≤b≤4, 0≤c≤2.

The exact script exhausts these45 choices. The other central case is allowed by the common factor2 in multiplicities. Because m(1)=2, that case would imply H≅C2×K with D(K)=D0. Any such K would itself have trivial radical by δ(D0)=1. Showing that D0 cannot be realized by a group needs additional structural input; treating B as a group algebra simply assumes away this gap. The already known recognition theorem for almost simple PSL2-socle groups rules out such an H, but arithmetic normalization alone does not.

For comparison, PSL2(512)⋊C3 with field action x↦x^8 has

    {1^3,512^3,511^12,513^9,1533^84,1539^84},

also radical-free and with multiplicity gcd3. In this case δ=1. Dividing multiplicities by3 fails Frobenius divisibility because1539 does not divide the resulting total order. Thus the512 example is a weaker tensor-root barrier than the16 example.

**Primary dependency:** D. L. White, *Character Degrees of Extensions of PSL2(q)*, author manuscript dated July25,2011, §4 and Lemmas4.5,4.7–4.8, gives the character families, invariance criteria and cyclic-quotient extension method. The exact script independently enumerates the stated finite parameter orbits and checks order sums; it does not recompute the full character table directly from matrix representations. Its local PDF receipt is in sources/manifest.json.

## 6. Defect-zero theory controls the socle, not all of G

The valuation v_pδ(G) equals

    v_p|G|−max_{χ∈Irr(G)}v_pχ(1),

the smallest p-defect among ordinary irreducible characters. It vanishes exactly when a p-defect-zero character exists.

**Lemma2.** If N◁G then δ(G) divides [G:N]δ(N).

**Proof.** Every θ∈Irr(N) occurs in the restriction of some χ∈Irr(G), for instance by decomposing θ^G and reciprocity. Clifford's theorem gives χ(1)=e[G:I_G(θ)]θ(1). Hence θ(1)|χ(1), so L(N)|L(G). Now

    [G:N]δ(N)=|G|/L(N)=δ(G)(L(G)/L(N)).

For a radical-free G the socle N is a direct product of nonabelian simple groups. Granville–Ono Corollary2 says that every nonabelian simple group has a p-defect-zero character for p≥5. Tensoring these characters gives a p-defect-zero character of N. Thus

    δ(N) has no prime divisors outside{2,3},
    v_pδ(G)≤v_p[G:N] for every p≥5.                    (6.1)

This applies to arbitrary radical-free overgroups, including those permuting isomorphic socle factors. It bounds the remaining primes by the socle quotient, rather than pretending G itself is a product. In the standard embedding G/N into the product of outer automorphism groups followed by factor-permutation groups, such p can come from field/other outer automorphisms or permutation actions.

**No universal restriction to primes2,3 is valid.** For every odd prime p≥5, put q=p^p and

    G_p=PSL2(q)⋊C_p

with the order-p field action x↦x^p. Then δ(G_p)=p. Indeed δ(PSL2(q))=1, so Lemma2 gives δ(G_p)|p. In the source group the only p-divisible irreducible degree is the Steinberg degree q, whose valuation is p. That character is field-invariant and extends; every character over it has degree q. Every other base degree is p-prime, and cyclic-index-p Clifford theory only multiplies it by1 orp. Hence the largest p-valuation of a G_p degree is p, whereas v_p|G_p|=p+1. Therefore δ(G_p)=p exactly. These are radical-free almost simple groups. Direct products G_p^k show that the p-valuation of δ is unbounded for every such p.

This construction is theoretical, not a claim that a huge character table was computed. It blocks a universal small-prime or bounded-exponent route. It also shows why the full arbitrary-overgroup quantifier cannot be reduced to the Granville–Ono simple-group list alone.

**Primary dependency:** A. Granville and K. Ono, *Defect zero p-blocks for finite simple groups*, Trans. Amer. Math. Soc.348(1996),331–347, DOI10.1090/S0002-9947-96-01481-X, Corollary2. Only its p≥5 assertion is used; the exact2,3 exception lists are not needed here. Source receipt is in sources/manifest.json. The G_p calculation additionally uses White's PSL2 character degree and field-invariance formulas.

## 7. Attempts, outcomes, and exact unresolved gap

| Mechanism | Strongest justified output | Status / remaining gap |
|---|---|---|
| Itô/lcm divisibility | Any abelian normal order divides δ; δ=1 gives a complete restricted answer | General source groups have δ>1; δ can have arbitrarily large primes and exponents |
| Central character masses and determinants | Numerical necessary conditions, including M_p≤n/p and exact quotient-block subset tests | Higher-rank noncentral elementary abelian normals escape; ASL2(4) falsifies the overstrong mass-only claim |
| Perfectness + small linear actions | Complete restricted certificate, including all A7×PSL2(2^f), f≥2 | Non-solvable GL_a(p) actions remain, and character data do not identify their kernels |
| Multiplicity normalization / tensor root | Explicit radical-free spectrum with multiplicity gcd2 and fully integral normalized order/divisibility data | An associative matrix algebra need not possess a finite group basis; realizing the root spectrum is unsupported |
| Defect-zero control via socle | δ(G)|[G:Soc(G)]δ(Soc(G)); primes≥5 inδ originate in the socle quotient | The quotient can contain arbitrary field-action primes, so this is a reduction, not a uniform exclusion |

The route is **blocked** whenever it asks, without additional evidence, for one of: all radical-free groups have δ=1; gcd multiplicities of a radical-free group is1; every p′-mass excess excludes any normal p-subgroup; numerical normalization of a group spectrum yields another group spectrum; or all radical-free groups possess p-defect-zero characters for p≥5. Explicit constructions above refute each applicable overstrong premise or locate its missing group-basis input.

The strongest new-to-this-session contribution is the combination of numerical certificates and exact barrier examples. Their priority has not undergone a full originality audit, and none solves the actual arbitrary-group question. No result is marked solved_verified or published.

## Reproduction and scope

Run `python3 verify_arithmetic.py`; the JSON output is recorded as exact_results.json. It uses only the Python standard library and integer/rational arithmetic. There is no floating-point computation. The output checks A_n spectra by hook lengths for5≤n≤32, all stated finite parameter orbits, q=4,…,1024 examples of the proved infinite family, the45-choice central block obstruction for PSL2(16)⋊C2, and the finite affine action.

The script assumes standard ordinary character classification/restriction formulas for A_n and PSL2(q), and Clifford theory. It verifies the arithmetic consequences and finite actions, rather than independently proving those external theorems. Its successful execution is no substitute for the symbolic proofs above. No GAP or Sage executable was present in this environment, and no such independent package run is claimed.
