# Bülles–Arapura transfer audit

## Checkpoint and status

2026-10-06 21:31 PDT (2026-10-07 04:31 UTC). Independent primary-source audit by the transfer agent. Conditional-transfer completion estimate: 95%; unconditional universal target estimate from this route: 0%. The latter means this route supplies no proof of its required universal K3-product input. Nothing below certifies that upstream input, any new mathematical novelty, or publication readiness. No external individual was contacted; no git operations or publication were performed.

**Strongest conclusion:** conditional on the rational Hodge conjecture for every finite mixed product of the relevant projective K3 bases, the rational Hodge conjecture holds in every codimension on every finite product of moduli spaces satisfying the actual hypotheses of Bülles Theorem 0.1. The proof is an algebraic correspondence pull-push argument, given below with all degrees specified. The upstream mixed-product conjecture is the exact remaining central gap.

## Primary-source inventory and imported statements

All sources were fetched on 2026-10-06 PDT from the current arXiv endpoints; version histories were checked through arXiv abstract pages. Local PDFs and text extractions are under `sources/downloads/bulles*`.

1. **Bülles, arXiv:1806.08284v1**, submitted 2018-06-21; only version listed. [Primary text](https://arxiv.org/html/1806.08284v1), [PDF](https://arxiv.org/pdf/1806.08284v1). Theorem 0.1, PDF p.1, treats a complex projective K3 or abelian surface with a Brauer class, and a smooth projective moduli space of Gieseker-stable twisted sheaves or of stable objects for a generic Bridgeland stability condition. Its rational Chow motive is a summand of a finite sum of twisted motives of powers of the underlying surface, with positive exponents bounded by the moduli dimension. Section 2.1, pp.5–7, uses a relative-Ext diagonal formula, GRR, and closure of correspondences factoring through surface powers under intersection products. Remark 2.1 records the Bridgeland extension. Section 3.1, p.11, describes algebraic twisted Chern characters by formal roots after killing the Brauer class and extension using locally free resolutions. These are theorem/proof inputs, not a Hodge conjecture theorem for the bases.

2. **Arapura, arXiv:math/0102070v5**, revised 2002-08-26. [Primary text](https://arxiv.org/html/math/0102070v5), [PDF](https://arxiv.org/pdf/math/0102070v5). Proposition 4.6, PDF p.19, transfers Hodge statements when algebraic correspondences have Künneth components generating the target's cohomology ring and suitable powers of the source satisfy the conjecture. Theorem 5.7(3), pp.21–22, applies this to an abelian or K3 surface's projective torsion-free sheaf moduli when its stable and semistable loci coincide and all surface powers satisfy the relevant conjecture. Its proof cites Markman's cohomology generators from a quasi-universal sheaf. Theorem 5.4, pp.20–21, gives the Hilbert-scheme transfer assuming the surface powers through exponent n. This text supplies an independent ordinary-sheaf transfer route; it does not contain an unconditional theorem for arbitrary K3 products, nor the full twisted/Bridgeland scope of Bülles.

3. **Markman, arXiv:math/0009109v4**, revised 2001-04-21. [Primary text](https://arxiv.org/html/math/0009109v4), [PDF](https://arxiv.org/pdf/math/0009109v4). Theorem 1 initially assumes universal families. Lemma 4, pp.6–11, is a geometric Chern-class lemma for a three-term locally free complex: its two outer cokernel conditions concern line bundles supported on a smooth codimension-m locus; the virtual rank is m−2; for even m its top Chern class is that locus. Section 3, pp.12–13, replaces a nonexistent universal family with a normalized rational Chern character obtained from a semi-universal family, an auxiliary bundle, and a Brauer–Severi bundle. Remark 3(1) uses polynomial dependence on line twists to extend invariance from integral to rational divisor twists. The non-fine treatment uses the normalized character rather than the raw multiplicity-bearing Ext complex.

4. **Marian–Zhao, arXiv:1711.10045v3**, revised 2020-02-28. [Primary text](https://arxiv.org/html/1711.10045v3), [PDF](https://arxiv.org/pdf/1711.10045v3). Its pp.2–4 explain the stable-complex diagonal formula: objects in the same stability heart have the required Ext amplitude; duality and stability give the diagonal line-bundle conditions; Markman's three-term-complex lemma applies. The main stated zero-cycle theorem assumes primitive Mukai vector and a v-generic stability condition. Its non-fine discussion uses a Brauer–Severi space carrying a universal family and suitable smooth generically finite sections. This validates the mechanism referenced by Bülles Remark 2.1; its main zero-cycle theorem's scope should not be silently enlarged.

PDF SHA256:

- Bülles: `2a5687aa5720e06ef1c37e8567ec99d993ee70b110069b4288425a6046079cb7`
- Arapura: `b9a642086a7a3e26a0a71fa29b1abc17ceb880c3a5ec43dce18e34a11034525f`
- Markman: `7681e31a6bf90ec16340421b5b9d1727fc8f9af81f8055af9f487644ce03dd3f`
- Marian–Zhao: `ef5412f859b011acf67fbb5d92ba904d10df40b78a1c745ef6338dc06b915c75`

## Exact applicability

Fix finitely many complex projective K3 surfaces S_a, with repetitions permitted, and classes α_a in Br(S_a). For each a, let M_a have fixed discrete invariants, normally a Mukai vector v_a, and be one of:

- a **smooth projective** moduli space of Gieseker-stable α_a-twisted sheaves for its chosen polarization;
- a **smooth projective** moduli space of σ_a-stable objects in D^b(S_a,α_a), with σ_a generic for the fixed moduli problem.

Here generic stability means the appropriate v-relative wall condition; it does not mean the surface is very general in its moduli space. Bülles's statement does not separately impose primitivity of v. It also does not prove that every choice of v, polarization, or stability condition produces a smooth projective stable moduli space. A primitive vector and a v-generic condition are a customary way to secure eligibility in standard constructions, but are not a license to omit the actual smoothness/projectivity/stability hypotheses. For a nonprimitive vector, genericity alone need not remove strictly semistable objects. Stable loci that are merely open in a singular projective semistable moduli space are not covered unless the stable moduli space in question is itself projective.

No extension to singular moduli, arbitrary symplectic resolutions, arbitrary deformations of K3^[n] type, integral Hodge classes, or the generalized Hodge conjecture is inferred here. Components can be handled separately and then added. Fine moduli are not required, but their absence must be treated as below.

## A cycle certificate without ambiguous twist signs

For one positive-dimensional eligible M of dimension m, Bülles supplies finitely many smooth projective Y_j=S^{k_j}, k_j≤m, and rational cycles

    γ_j ∈ CH^{e_j}(M×Y_j)_Q,
    δ_j ∈ CH^{d_j}(Y_j×M)_Q,
    e_j+d_j−dim(Y_j)=m,
    Σ_j δ_j∘γ_j = [Δ_M] in CH^m(M×M)_Q.

The composition convention is

    δ∘γ = (p_13)_*((p_12)^*γ · (p_23)^*δ)

on M×Y×M. It lowers the sum of codimensions by dim Y, giving the displayed identity of degrees. Homogeneous pieces of any initially inhomogeneous certificate can be extracted, retaining only terms of total degree m.

**Printed sign issue:** Bülles §1 defines Hom((X,p,a),(Y,q,b)) using CH^{dim X+b−a}. His §2.1 writes n_j=d_j−2k_j for δ_j:h(S^{k_j})(n_j)→h(M). With that stated Hom convention, the correct value is n_j=2k_j−d_j. Then e_j=m+n_j also agrees with the γ direction. This changes no existence statement because arbitrary integer twists are allowed, but it matters when identifying source Hodge degrees. Use the explicit cycle certificate, or the corrected convention, throughout.

## Independent derivation of the conditional transfer

Let X be any smooth projective variety of dimension D with such a certificate through smooth projective Y_j of dimension N_j. For

    ξ ∈ H^{2p}(X,Q) ∩ H^{p,p}(X),

define

    q_j = p+e_j−D = p−(d_j−N_j),
    η_j = (γ_j)_*ξ.

An algebraic correspondence of codimension e_j on X×Y_j shifts cohomology degree by 2(e_j−D) and Hodge bidegree by (e_j−D,e_j−D). Consequently

    η_j ∈ H^{2q_j}(Y_j,Q) ∩ H^{q_j,q_j}(Y_j).

If q_j<0 or q_j>N_j, this cohomology group is zero and the term is discarded. Otherwise, HC(Y_j) provides z_j∈CH^{q_j}(Y_j)_Q with cl(z_j)=η_j. Define

    z = Σ_j (δ_j)_*z_j.

The codimension of each summand is

    q_j+d_j−N_j = p,

so z∈CH^p(X)_Q. Functoriality of the cycle class map and the certificate give

    cl(z) = Σ_j (δ_j)_*(γ_j)_*ξ = (Δ_X)_*ξ = ξ.

Thus HC transfers from these source varieties to X in every codimension. This proof needs only a diagonal identity in cohomology, although Bülles supplies one in the rational Chow group. No finite-dimensional-motive conjecture, algebraicity of a separately chosen Hodge splitting, or semisimplicity argument is needed.

For X=∏_{a=1}^r M_a, expand the external product of the individual certificates. For a tuple b=(j_1,...,j_r), set

    Y_b=∏_a S_a^{k_{a,j_a}},
    Γ_b=⊠_a γ_{a,j_a},       Δ_b=⊠_a δ_{a,j_a},
    E_b=Σ_a e_{a,j_a},       F_b=Σ_a d_{a,j_a},
    D=Σ_a dim M_a,           N_b=Σ_a 2k_{a,j_a}.

The product compatibility of correspondence composition gives

    Σ_b Δ_b∘Γ_b = [Δ_X],
    E_b+F_b−N_b=D.

Apply the preceding construction with

    q_b=p+E_b−D=p−(F_b−N_b).

The source varieties are **mixed** products of the K3 bases. The assumption that HC holds for each S_a^k separately does not imply HC for Y_b by itself: new rational Hodge tensors can occur between different factors. HC on all these mixed Y_b is precisely the required assumption. For each fixed X only finitely many Y_b occur; exponents of each source occurrence are bounded by dim M_a. The blanket hypothesis “HC for every finite mixed product of the relevant bases” covers all X simultaneously.

## Independent repair of the non-fine and twisted-family bookkeeping

This subsection is a derivation explaining the omitted normalization. It is not a new claimed theorem or an additional unverified K3-product input.

### Algebraic twisted characters without a B-field

Choose a locally free α-twisted sheaf A of positive rank s on S, as supplied by an Azumaya representative of the Brauer class. End(A) is an ordinary algebraic vector bundle of rank s² and is self-dual. For any perfect α-twisted E on T×S, let

    b = sqrt(ch End(A)),      constant term of b=s,
    q_A(E) = ch(E⊗A^∨)/b.

Pullback of A and b to T×S is understood. The numerator is the Chern character of an **untwisted** perfect complex. Formal division and the root are finite operations in the rational Chow ring because the ideal of positive codimension is nilpotent. Hence q_A(E) is an ordinary rational algebraic cycle class even when E has rank zero. It is additive on perfect complexes.

Let ∨ denote the usual sign involution on Chern-character components. Since End(A) is self-dual, b^∨=b. For two families with the same α twist,

    q_A(E)^∨ q_A(F)
      = ch(A⊗E^∨) ch(A^∨⊗F) / ch End(A)
      = ch(End(A)⊗E^∨⊗F) / ch End(A)
      = ch(E^∨⊗F).

Everything in this identity after tensor cancellation is untwisted. Therefore the ordinary GRR formula for relative RHom factors into rational algebraic classes from the two M×S factors exactly as in the fine untwisted case. This eliminates any temptation to use a transcendental B-field exponential as an algebraic correspondence.

### Remove quasi-universal multiplicities before taking Chern classes

Let F be a quasi-universal family on M×S, carrying only the fixed α twist from S. Locally on M it is E_i⊗V_i^*, where E_i is a universal family and V_i has fixed positive rank ρ. The V_i carry the common scalar descent obstruction. The bundles

    W_i=V_i^{⊗ρ}⊗(det V_i)^*

glue to an ordinary vector bundle W on M. Define

    Q = q_A(F) · ch(W^*)^{−1/ρ}.

The root is chosen with constant term ρ for ch(W^*)^{1/ρ}, because W has rank ρ^ρ. Thus all coefficients remain rational. This is the normalized character needed in the diagonal formula. Dividing q_A(F) just by the scalar ρ does not, by itself, justify the top-Chern-class identity.

Let p:P→M be the associated Brauer–Severi bundle, with fiber P^{ρ−1}; it carries a universal family Ẽ on P×S. Write

    h = c_1(O_P(ρ))/ρ.

The auxiliary bundle Ṽ(1) on P satisfies

    p^*F = Ṽ(1)^*⊗Ẽ,
    p^*W = Ṽ(1)^{⊗ρ}⊗O_P(−ρ).

Taking the specified root yields the unambiguous normalization identity

    p^*Q = q_A(Ẽ) exp(−h).

**Source presentation issue:** the printed Markman §3 formula for its intermediate α uses a plus sign on the formal hyperplane character, while its immediately preceding two bundle identities force the minus sign above. The normalization equation involving W is internally sufficient to fix the sign; do not quote the intermediate sign as a convention-free formula.

On P×P the diagonal locus is Z=P×_M P, a smooth locus of codimension m. The relative Ext complex of Ẽ from the two factors has virtual rank m−2. Stability and K3 Serre duality give the line-bundle support conditions in Markman's geometric Lemma 4. For m positive and even,

    c_m(−Ext^!_π(Ẽ,Ẽ)) = [Z] = (p×p)^*[Δ_M].

Twisting either universal family by an arbitrary line bundle from P preserves those conditions and this class. The expression is polynomial in the two first-Chern-class twist parameters. Constancy for all integer twists by O_P(ρ) implies constancy for rational twists by a Vandermonde argument over Q. In particular, the exp(−h) factors above can be removed from the top-Chern-class computation.

Define the rational character on M×M

    C = −π_*((Q_12)^∨ Q_23 · td(S)).

Its pullback is the character of the universal relative Ext complex, multiplied by exp(h_1−h_2); rational twist invariance therefore gives

    (p×p)^*c_m(C) = (p×p)^*[Δ_M].

Here c_m(C) is the universal Newton polynomial in the positive-codimension components of C. Pullback is injective in rational Chow groups: p_*(h^{ρ−1})=1, and the analogous product formula recovers any class via the projection formula. Consequently

    c_m(C)=[Δ_M] in CH^m(M×M)_Q.

This argument uses ordinary algebraic Chow classes throughout. For Bridgeland objects the universal families are perfect complexes, the same calculation uses their derived duals, and the amplitude/line-bundle conditions are the stable-complex mechanism described by Marian–Zhao. The existence of the moduli gerbe, a Brauer–Severi cover, and such universal perfect families is part of the eligible moduli setup already used by the cited transfer theorem; no claim about a moduli problem lacking these structures is intended.

### Recover the bound on surface powers

For each n≥1, the codimension-n component C_n is a finite sum of compositions through one copy of S:

    C_n = −Σ_{u+v=n+2} B_v∘A_u,

where A_u and B_v are the homogeneous pieces of Q^∨sqrt(td S) and Qsqrt(td S). The shift +2 is dim S, not dim M.

The polynomial c_m(C) is weighted-homogeneous of weight m, giving each C_n weight n. Every monomial has at most m factors C_n. Intersection products of l correspondences each factoring through S factor through S^l, by taking external products and pulling back along the diagonal at both endpoints. Thus c_m(C)=[Δ_M] factors through finitely many S^k with 1≤k≤m. Splitting into homogeneous γ and δ gives the cycle certificate used above.

## Arapura cross-check and displayed-degree caution

Arapura's ordinary-sheaf theorem provides an independent cohomological route: Markman's algebraic universal-character components generate cohomology; multiply such correspondences using the target diagonal; then use exactness of Hodge classes for a surjection of polarizable Hodge structures to lift classes. The explicit diagonal certificate above makes that final lifting step especially transparent and keeps it algebraic.

For a general correspondence C∈CH^i(Y×N), its action shifts degrees by 2(i−dim Y). For an n-fold external product pulled back along the target diagonal, the shift is

    2(Σ i_j − n dim Y).

Arapura Proposition 4.6's displayed formula uses Σ i_j−n, the curve value. In the surface application it must be Σ i_j−2n. The displayed finite counting bound also needs attention if odd-degree generators are present in the abstract setup. In the K3 application, source cohomology is even, positive target generator degrees are even, and at most dim N such generators enter any monomial of degree at most 2 dim N. Theorem 5.7(3) assumes all powers of the base, so neither display issue affects that theorem's transfer conclusion. They are further reasons to present the independent degree-correct proof rather than copying the displayed map.

## Boundary and falsification checks

- **Zero-dimensional M:** the printed Bülles range 1≤k≤dim M is empty, and Markman Lemma 4 assumes m≥2. Treat a smooth projective zero-dimensional space directly as a finite disjoint union of points. Its Hodge classes are the point basis in H^0; all are algebraic. No positive-power certificate is necessary.
- **Empty M:** both cycle and cohomology groups vanish; any product containing an empty factor is vacuous.
- **No factors:** the empty product is Spec C, whose HC is trivial.
- **Outside degrees:** p<0 or p>dim X gives a zero target group. Likewise q_b outside [0,dim Y_b] contributes zero and requires no impossible source cycle.
- **Hilbert schemes:** for n≥1, S^[n] is the ordinary fine stable ideal-sheaf example with v=(1,0,1−n) and dim=2n. For n=0 it is a point. For n=1 it is S itself. Arapura's Hilbert-specific reduction needs powers only through n; Bülles's general certificate bound through 2n is sufficient but less sharp.
- **Identity example:** for M=S, γ=δ=Δ_S has e=d=2 and q=p, verifying the sign and degree convention directly.
- **No closure shortcut:** “HC(S) and HC(T), therefore HC(S×T)” is invalid without control of mixed Hodge tensors. The proof assumes HC on its actual source products.
- **No integral upgrade:** normalization and correspondences contain denominators; no torsion or integral-cycle theorem follows.
- **No finite-dimensionality requirement:** the proof uses the split diagonal, not Kimura finite dimensionality. Finite dimensionality is a different conditional corollary in Bülles.
- **No upstream promotion:** the construction transports a base result if established; it does not prove algebraicity of a new Hodge tensor on a K3 product.

An explicit falsification check for the raw quasi-universal formula is available in dimension two. Take M=S as the moduli of length-one skyscraper sheaves, with universal family U=O_Δ. Markman's dimension-two calculation has Ext^1=0 and Ext^2 a line bundle on the diagonal. Thus the virtual complex W=−Ext^! has c_1(W)=0 and c_2(W)=[Δ_S]. Replace U by U⊕U, a perfectly valid quasi-universal family of multiplicity two. The raw relative Ext complex becomes four copies, so c_2(4W)=4[Δ_S], not [Δ_S]. This checks that a multiplicity correction is necessary; the displayed raw formula in Bülles cannot be read literally for an arbitrary quasi-universal family. The normalized character/cover argument repairs this without changing Theorem 0.1's transfer conclusion.

## Exact remaining gap and novelty assessment

Let A be the assertion HC in every codimension for every finite mixed product of complex projective K3 surfaces. Let B be the original universal assertion for every finite product of eligible K3 stable moduli, including all Hilbert schemes. The transfer proves A⇒B. Since S=S^[1] is an eligible target factor, B⇒A. Therefore A and B are equivalent as universal assertions.

This makes the obstruction exact: a merely conditional invocation of Bülles cannot resolve the original target, because it relocates it to an equivalent universal K3-product assertion. The transfer mechanism is established literature; its mixed-product elaboration is a formal consequence and should not be promoted as novel research without a separate independently verified new input. The normalized calculations above repair presentation details and make the proof checkable, but no claim of priority or novelty for those corrections is made.

**Route status:** transfer is viable and essentially complete as a conditional theorem; unconditional transfer-only route is blocked at the equivalent universal K3-product input. Reopen that route only for a materially new verified proof of that input or a meaningful restricted hypothesis on the bases.

## Independent review of root manuscript

2026-10-06 21:34 PDT checkpoint. Conditional-transfer proof completion estimate: 100%; exact auxiliary-source normalization audit: 95%; unconditional universal target remains 0% from this route. Reviewed `manuscript/CONDITIONAL_TRANSFER.md` independently for statement, stable/generic scope, cycle degrees, product signs, exponent bounds, and boundary cases. Its conditional theorem and its pull-push proof are correct as written. It explicitly treats Bülles's splitting as the published input and does not depend on the raw quasi-universal Ext formula, the printed twist sign, or Arapura's displayed dimension shift. The nonnegative exponent formulation remains valid with repeated bases because the individual indexed source occurrences can be kept separate before their identical factors are combined. No necessary manuscript correction was found. The only unresolved requirement for the original universal assertion is the independently unvalidated universal mixed-K3-product input, and the documentation should preserve that status.
