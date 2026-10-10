# KOU-21.114: proved reductions and construction obstructions

These are self-contained elementary arguments except where an external theorem is explicitly identified. They do not solve the uniform derived-length question. The arguments are authored reconstructions; no novelty is asserted.

For a finite group X, write X'=[X,X], a(X)=|X/X'|, X^(0)=X, and X^(i+1)=(X^(i))'. A group is weakly ab-maximal when a(H)≤a(X) for every subgroup H≤X. Derived length is the least d with X^(d)=1. A nontrivial abelian group has derived length 1. The nilpotency class of a nontrivial group is the least c with γ_(c+1)(X)=1, where γ_1(X)=X and γ_(i+1)(X)=[γ_i(X),X].

## 1. Structural reductions and their actual limit

### 1.1 Quotients

Every quotient of a finite weakly ab-maximal group is weakly ab-maximal.

Proof. Let N be normal in G and N≤H≤G. The derived subgroup of H/N is H'N/N. Hence

    a(H/N) = a(H) / |N : N∩H'|.

Because H'≤G', the denominator is at least |N:N∩G'|. Apply a(H)≤a(G) and the same formula to G/N. This gives a(H/N)≤a(G/N), as required. ∎

### 1.2 Direct products

A×B is weakly ab-maximal if and only if A and B are weakly ab-maximal.

Proof. The forward direction follows from 1.1. Conversely let H≤A×B, K=H∩(A×1), and L the image of H in B. The homomorphism H/H'→L/L' is surjective; its kernel is the image of K and has order |K:K∩H'|≤|K:K'|. Thus

    a(H) ≤ a(K)a(L) ≤ a(A)a(B) = a(A×B).

The middle inequality uses K≅a subgroup of A and L≤B. ∎

External input: Lisi–Sabatini, *On groups with large verbal quotients*, Theorem 1.2, proves that every finite weakly ab-maximal group is nilpotent. The original proof, including its reduction and imported theorems, is not independently reproved here. Combining that theorem with 1.2 reduces the target to finite p-groups. The derived length of a finite direct product is the maximum of the derived lengths of its factors, because commutators and every derived term are computed coordinatewise.

### 1.3 Minimal quotient obstruction for any proposed bound

Fix d≥1. If some finite weakly ab-maximal p-group has derived length greater than d, choose such a group P of minimum order. Then P has a unique minimal nontrivial normal subgroup Z0, and

    |Z0|=p,  Z0≤Z(P),  P^(d)=Z0,  dl(P)=d+1,

and Z(P) is cyclic.

Proof. Every nontrivial normal subgroup N gives a smaller weakly ab-maximal quotient P/N, by 1.1. Minimality implies (P/N)^(d)=1 and therefore P^(d)≤N. As P^(d)≠1, two nontrivial normal subgroups cannot have trivial intersection. Consequently there is a unique minimal normal subgroup Z0. In a finite p-group, a minimal normal subgroup has order p and is central: the conjugation action on that subgroup has a nonidentity fixed point by the class equation, and a central subgroup of order p is normal. Minimality of the normal subgroup then identifies it with this central subgroup. As P^(d)≤Z0 and is nontrivial, equality follows. Its commutator subgroup is trivial, giving dl(P)=d+1. Every order-p subgroup of Z(P) is normal, so there is only one. A finite abelian p-group with a unique order-p subgroup is cyclic, as follows at once from its decomposition into cyclic factors. ∎

This proposition does not rule out such groups as d varies. It identifies an unresolved family that a proof must exclude or a counterexample must construct.

### 1.4 A bound depending on the abelianization size

Let P be weakly ab-maximal, |P/P'|=p^a, and P≠1. Then

    |P| ≤ p^(a(a+1)),
    dl(P) ≤ ceil(log_2(a(a+1)+1)).

This is only an elementary parameter-dependent bound, not the absolute bound asked for.

Proof. Choose an abelian normal subgroup A maximal with respect to inclusion, and let |A|=p^b. It is nontrivial because the center of a nontrivial finite p-group is nontrivial. We first show C_P(A)=A. Put C=C_P(A), which is normal in P. If C>A, the nontrivial normal subgroup C/A of the p-group P/A meets Z(P/A) nontrivially, by the same conjugation class equation. Choose an order-p subgroup of this intersection and a representative x in C. Then A⟨x⟩ is abelian, properly contains A, and is normal in P, contradicting maximality. Thus conjugation embeds P/A in Aut(A).

The group A has a generating set of at most b elements. An automorphism is determined by the images of those generators, so |Aut(A)|≤|A|^b=p^(b²). Since A is abelian, weak ab-maximality gives b≤a. Therefore |P|≤p^(b+b²)≤p^(a+a²).

Write |P|=p^N. Each nontrivial term in the lower central series strictly decreases in a finite nilpotent group; therefore its class is at most N. The standard commutator inclusion [γ_i(P),γ_j(P)]≤γ_(i+j)(P), obtained inductively from the commutator identities, gives P^(j)≤γ_(2^j)(P). Thus P^(j)=1 when 2^j>N. Taking j=ceil(log_2(N+1)) and using N≤a(a+1) proves the claimed bound. ∎

The parameter a is unbounded even within abelian groups. None of these inequalities produces an absolute constant.

## 2. Cyclic holomorphs: unbounded class still has derived length two

This family and its weak ab-maximality are already in Lisi–Sabatini, Section 3.1. The proof below handles p=2 and odd p uniformly.

Let p be prime and n≥2. Write N additively as Z/p^nZ. Let K be the subgroup of its units congruent to 1 modulo p, and let

    P=N⋊K,   (x,u)(y,v)=(x+uy,uv).

For odd p, K is the Sylow p-subgroup of Aut(N). For p=2 it is the full unit group. In both cases |K|=p^(n-1). Then

    |P|=p^(2n-1),  |P/P'|=p^n,
    γ_i(P)=p^(i-1)N for 2≤i≤n+1,
    class(P)=n,  dl(P)=2,

and P is weakly ab-maximal.

Proof of the structural claims. Both N and K are abelian, so P'=[N,K]. Every u∈K has u−1 divisible by p, while the unit 1+p belongs to K and gives exactly the image pN. Thus P'=pN. Commuting p^jN with K gives p^(j+1)N by the same argument. This proves the lower-central formula and class. P' is nontrivial abelian for n≥2, so derived length is exactly two. The order and abelianization claims follow from |N|=p^n and |K|=p^(n-1).

Proof of weak ab-maximality. Take H≤P, put A=H∩N, and let R≤K be the image of H under projection. Suppose |A|=p^s. If R=1 then H≤N and a(H)≤p^n. Otherwise choose

    t=min { v_p(u−1) : u∈R, u≠1 }.

Then 1≤t<n. Since N is abelian, conjugation by a lift of u acts on A as multiplication by u; hence [A,H]=[A,R]≤H'. The minimum valuation implies [A,R]=p^tA, so

    a(H) ≤ |H:[A,H]| = |R| p^min(s,t).

All units in R are 1 modulo p^t, a set of exactly p^(n−t) units modulo p^n. Thus |R|≤p^(n−t), and the last displayed expression is at most p^n=a(P). ∎

No binomial-coefficient divisibility shortcut is needed here. In particular the argument does not presume the Sylow automorphism group to be cyclic when p=2.

### 2.1 Weak ab-maximality is not subgroup-closed

For p=2,n=3 the group P=C8⋊Aut(C8) is weakly ab-maximal with a(P)=8. Its subgroup D=C8⋊⟨−1⟩ is dihedral of order 16. Its commutator subgroup is 2C8 of order 4, so a(D)=4. The rotation subgroup C8 has abelianization order 8. Therefore D is not weakly ab-maximal. ∎

This gives a concrete obstruction to an induction that silently treats arbitrary subgroups of a weakly ab-maximal group as weakly ab-maximal.

## 3. Complete obstruction for regular p-group wreath products

Let A and B be nontrivial finite p-groups, with B acting regularly on itself. The regular wreath product W=A wr B is weakly ab-maximal if and only if A≅B≅C2.

Proof. Let m=|B|, a=a(A), and b=a(B). The base is A^m and has abelianization order a^m. The abelianization of W is A/A'×B/B', of order ab. Here is a direct verification: internal commutators in each base coordinate kill (A')^m; commutators with the regular top action identify all base coordinates in the abelianized base. The remaining base quotient is A/A', via the product of the coordinate images. Together with projection to B/B' this gives a surjective map with exactly the described commutator kernel.

If W is weakly ab-maximal, its base therefore requires

    a^(m−1) ≤ b ≤ m.

A nontrivial finite p-group has a≥p≥2. If m≥3, then 2^(m−1)>m: the inequality starts at m=3 and is preserved on increasing m because doubling outgrows an increment of one. Consequently m=2, B=C2, and a≤2. Thus p=2 and a=2.

A finite p-group with cyclic abelianization is cyclic. Indeed, choose x whose coset generates the abelianization. Then P=⟨x⟩P'. If ⟨x⟩ were proper, it would be contained in a maximal subgroup M. Every maximal subgroup of a finite p-group is normal of index p, so P'≤M, giving P≤M, a contradiction. Thus A is cyclic and a(A)=2 forces A=C2.

Conversely C2 wr C2 is D8, the order-eight dihedral group. Its abelianization has order 4, and every proper subgroup has order at most 4, so it is weakly ab-maximal. ∎

In particular W1=Cp and W_(r+1)=W_r wr Cp cannot supply unbounded derived length within this class. Already W2 fails for p≥3; W3 fails for p=2. More precisely a(W_r)=p^r, while the base of W_r, r≥2, has abelianization p^(p(r−1)). The latter exceeds the former whenever p(r−1)>r. The equality case p=r=2 is the single allowed nontrivial wreath product.

For W3=(C2 wr C2) wr C2, the base D8×D8 has order 64 and abelianization order 16; the ambient order is 128 and ambient abelianization order 8. The checker directly confirms derived length 3, so this tempting candidate does reach the next derived length but fails the defining inequality.

## 4. Full unitriangular groups are excluded

For every finite field F_q and every n≥4, UT_n(F_q) is not weakly ab-maximal.

Proof. Projection to the first superdiagonal gives the abelianization F_q^(n−1). To check its kernel is the commutator subgroup, write x_ij(c)=I+cE_ij. Every x_ij(c) with j−i≥2 is

    [x_i,j−1(c), x_j−1,j(1)] = x_ij(c)

for the commutator convention used here. These elementary matrices generate exactly the matrices whose first superdiagonal vanishes. Thus the ambient abelianization has order q^(n−1).

Set k=floor(n/2). Matrices I+X with X supported only on positions i≤k<j form an abelian subgroup: the product XY of any two such strictly upper matrices is zero, so multiplication is just addition. Its order is q^(k(n−k)). For n=2r≥4, r²>2r−1 because (r−1)²>0. For n=2r+1≥5, r(r+1)>2r because r(r−1)>0. Hence k(n−k)>n−1, and the subgroup violates weak ab-maximality. ∎

The exact control UT_4(F_2) has order 64, abelianization order 8, and an abelian rectangular subgroup of order 16. Exhaustive subgroup enumeration independently identifies the maximum subgroup-abelianization order. This infinite-family obstruction excludes full unitriangular groups, not all their subgroups, sections, or other matrix groups.

## 5. Enlarging the center does not repair the wreath obstruction

Ordinary direct-product padding cannot turn a non-weakly-ab-maximal group into a weakly ab-maximal one, by 1.2. This remains true for a broad central-product repair of the bad wreath examples.

Let G and E be finite groups with identified central subgroups Z_G≅Z_E of prime order p, both contained in the respective commutator subgroups. Let Δ be the central order-p subgroup used to identify them, and put Q=(G×E)/Δ. If H≤G satisfies Z_G≤H', then its image S=(H×E)/Δ satisfies

    a(Q)=a(G)a(E),  a(S)=a(H)a(E).

Thus a(H)>a(G) implies a(S)>a(Q).

Proof. As Δ≤G'×E', the derived subgroup of Q is (G'×E')/Δ, so the factor p cancels between total and derived orders. The same argument applies to H×E because Δ≤H'×E'. The two formulas follow. ∎

For W=(C2 wr C2) wr C2, write D8=C2 wr C2 and let z generate Z(D8)=D8'. The element (z,z) in the base is central in W. Its subgroup Z has order 2 and lies in the derived subgroup of the base H=D8×D8. The violation a(H)=16>a(W)=8 therefore survives every central product of the displayed type, including amalgamation with an extraspecial 2-group along its derived center. The exact checker verifies that the entire center of W has order two and is contained in H'.

This does not exclude all possible central extensions or central products. It pinpoints why this specific inflation strategy cannot repair the regular-wreath candidate.

## Certification and logical boundary

The Python checker constructs the groups from their multiplication formulas, checks every associativity triple, enumerates all subgroups for nine indicated small groups, and computes subgroup derived subgroups by generating all elementwise commutators. It also checks two additional wreath witnesses by exact tables. No floating-point arithmetic or external group database is used.

Subgroup enumeration starts from {1} and repeatedly adjoins one element. One representative from each left coset xH is enough because ⟨H,xh⟩=⟨H,x⟩ for h∈H. Every subgroup has a finite generating list, so induction on its length shows that the enumeration is complete. Duplicate subgroups are identified by their full element sets. Each produced subgroup is independently checked for multiplication closure and regenerated from its stored generators. The certificate is regenerated exactly on replay.

The computations verify finite controls and expose false generalizations. The all-parameter results above are proved by the written arguments, not inferred from a finite sample. None establishes an absolute bound for the derived length of every weakly ab-maximal p-group, and none constructs such groups of unbounded derived length.
