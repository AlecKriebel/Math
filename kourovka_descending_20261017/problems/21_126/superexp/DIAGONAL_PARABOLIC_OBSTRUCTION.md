# A diagonal obstruction valid for arbitrary RAAG embeddings

Status: independently derived construction filter; a fresh adversarial proof audit passed. See review/DIAGONAL_PARABOLIC_AUDIT.md and the reviewed-input receipt for scope and exact versions. No claim of literature originality, solution of 21.126, or obstruction to every possible embedding of the Brady–Tran ambient groups is made.

## Statement

Let A be a finite-graph RAAG, P≤A a parabolic subgroup (a conjugate of a standard full subgroup), and α,β:H→A homomorphisms such that the two images commute elementwise. Suppose

    α(h)β(h) ∈ P    for every h∈H.

Then α([H,H])≤P and β([H,H])≤P.

Consequently, if j:H×H→A is injective and H is nonabelian, no parabolic subgroup P can satisfy

    j(H×H) ∩ P = j(ΔH),     ΔH={(h,h):h∈H}.

This consequence concerns the *same* embedding j and every parabolic P. It does not require j to be convex-cocompact. For abelian H the commutator conclusion is vacuous; the diagonal Z in Z² can indeed become a standard factor under a change of basis, so the nonabelian hypothesis cannot be dropped.

## Primary structural inputs

Use the convention C_A(U)={a∈A:[a,u]=1 for all u∈U}. For a vertex set E, write

    E^⊥={v: v commutes with every vertex of E},

where v itself commutes with v. Thus E^⊥ is an inclusive orthogonal complement, and L(S)=S^⊥\S is the usual external link. Empty sets have E^⊥=VΓ.

Duncan–Kazachkov–Remeslennikov, *Parabolic and quasiparabolic subgroups of free partially commutative groups*, J. Algebra 318(2) (2007), 918–932, DOI 10.1016/j.jalgebra.2007.08.032, arXiv:math/0702431, gives:

1. Theorem 3.12 and Definitions 3.1–3.2: after conjugation, any centralizer C_A(U) is a canonical quasiparabolic group

       C_A(U)=B×A(Y),    B=⟨w₁⟩×⋯×⟨w_k⟩,

   where the w_i are cyclically reduced root blocks, their pairwise disjoint supports S_i commute across different blocks, each |S_i|≥2 in standard form, and Y⊆L(S), S=⋃S_i. The empty block family B=1 is allowed.

2. The centralizer formula for w=w₁⋯w_k (recalled in their preliminary discussion and used in the proof of Theorem 3.12) is

       C_A(w)=B×A(L(S)).

3. Proposition 2.6 and especially Lemma 2.7: an intersection of parabolic subgroups is parabolic. When one intersectand is the standard subgroup A(K), the intersection is a conjugate of a standard subgroup of A(K) by an element of A(K). This last internal-conjugator assertion is explicit in Lemma 2.7, not an assumed arbitrary-subgroup inheritance.

The primary PDF was downloaded and these exact statements were read. The proof below spells out the new application rather than treating an aggregator description as a theorem.

## Proof

Put U=α(H), V=β(H). Since U and V commute, V≤C_A(U). Apply structural input 1 and conjugate all the data simultaneously so that

    C_A(U)=B×A(Y)

has the displayed standard form. In particular

    V≤B×A(Y).

Every element of U commutes with every element of C_A(U), so U≤C_A(C_A(U)). Centralizing B is equivalent to centralizing w=w₁⋯w_k, by structural input 2. Also

    C_A(A(Y))=A(Y^⊥),

because centralizing all standard generators y∈Y is exactly membership in the intersection of their standard-star centralizers. The blocks in B commute with every vertex of Y. Thus the product decomposition of C_A(w) gives

    C_A(C_A(U)) = B × A(T),     T=L(S)∩Y^⊥,

and hence U≤B×A(T). If k=0, take S=∅, B=1, and L(S)=VΓ, so the same formula remains valid.

Let C=Y∩T. Since Y⊆L(S), this equals Y∩Y^⊥, precisely the vertices that are central in A(Y). It is a clique, and every vertex of C commutes with all of Y∪T. Put Y₀=Y\C and T₀=T\C. These sets are disjoint, and every vertex of Y₀ commutes with every vertex of T₀, because T⊆Y^⊥. Every vertex of S commutes with every vertex in Y∪T. Therefore the following is an actual standard parabolic subgroup with its join-product decomposition:

    K=A(S) × A(Y₀) × A(T₀) × A(C).

There is no assertion that A(S) is abelian: only its subgroup B is abelian. The two images satisfy

    U≤B × A(T₀) × A(C),
    V≤B × A(Y₀) × A(C).

Taking commutators kills both the B and A(C) coordinates, so

    [U,U]≤A(T₀),     [V,V]≤A(Y₀).

Both U and V lie in K. Put R=P∩K. By structural input 3, R is a parabolic subgroup of K with conjugator lying in K. Every such subgroup splits across the displayed direct factors: a standard full subgroup is the product of its restrictions to the four vertex sets, and conjugation by an element of K acts in each direct factor separately. Consequently, if x∈A(T₀), y∈A(Y₀), and xy∈R, then x,y∈R.

For h,k∈H, apply the hypothesis to γ=[h,k]. It gives

    α(γ)β(γ)∈P∩K=R.

The first factor belongs to A(T₀), the second to A(Y₀), by the commutator observation. The factorwise property of R therefore gives α(γ),β(γ)∈P. Such commutators generate H′, proving both claimed containments.

For the consequence, write α(h)=j(h,1), β(h)=j(1,h). If H is nonabelian choose 1≠c∈H′. Then j(c,1)∈P∩j(H×H), but it does not belong to j(ΔH): injectivity would force (c,1)=(h,h), so h=1 and c=1, a contradiction.

## Finite-index robustness for non-virtually-abelian H

Suppose H is not virtually abelian and j:H×H→A is injective. Let J≤H×H have finite index. No parabolic P can have R=P∩j(J) commensurable with j(ΔH).

Indeed, finite index of J supplies a finite-index subgroup H₀≤H with H₀×H₀≤J (intersect the two coordinate intersections, or take the core). Commensurability would supply a finite-index K≤H₀ with j(ΔK)≤P. Apply the theorem to the restrictions of the two coordinate homomorphisms to K. It gives j(K′×1)≤P∩j(J)=R. The subgroup K is nonabelian since H is not virtually abelian, so K′ contains a nonidentity element. RAAGs are torsion-free; hence j(K′×1) is infinite. Its intersection with j(ΔH) is trivial, so R∩j(ΔH) cannot have finite index in R, contrary to commensurability.

This only excludes a proposed finite-index *parabolic-intersection* model of the diagonal. It is not an obstruction to arbitrary virtual RAAG embeddings of a larger amalgam.

## Relevance and exact limit

The factor-diagonal chaining of Brady–Tran uses nonabelian diagonal groups. A suggested algebraic repair was to embed each product H×H into a RAAG so that its diagonal became its intersection with a parabolic, allowing the normal-form RAAG gluing mechanism of PARABOLIC_DOUBLE_ROUTE.md. The theorem rules out that particular repair for every such embedding, even a highly distorted embedding.

This does not prove that the complete factor-diagonal amalgam fails to embed into a RAAG. An embedding need not arise by a parabolic amalgam, and virtual special combination results can use different mechanisms. It also does not rule out non-diagonal constructions or supply a universal exponential bound for RAAG subgroup Dehn functions. The mathematical outcome is a precisely scoped negative filter, not a resolution of Kourovka 21.126.
