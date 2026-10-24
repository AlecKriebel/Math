# Fresh delta audit: different-character doubles after finite-index passage

Reviewer: `/root/p21126_superexp/double_adversary`; UTC: 2026-10-24T21:35:36.264716+00:00. Exact input: `../FINITE_INDEX_CHARACTER_DOUBLE.md`, hashed in FINITE_INDEX_CHARACTER_RECEIPT.json.

**Outcome: PASS after explicitly stating the finite-type surface-fiber hypothesis.** I independently reconstructed every finite-index passage, the unchanged aligned fiber product, the character extension on that product, and the finite-index subgroup of the ACTUAL double. No substantive objection remains. This strengthens the previous partial filter; it does not solve 21.126 or certify novelty.

## Initial hypothesis repair

The first candidate said only 'surface-by-cyclic groups'. I requested explicit finiteness of the surface fibers because the proof needs G finitely generated to have finitely many fixed-index subgroups and needs G finitely presented to present the double. The final input specifies finitely generated, finitely presented fundamental groups of compact surfaces. Then

    G=(Σ1×Σ2)⋊Z

is finitely generated and finitely presented, by a finite semidirect-product presentation. Its finite-index subgroup G0 is finitely presented. No assertion about arbitrary infinite-type surface fibers is approved. The final status paragraph and audit link match this repaired input.

## 1. Reconstructing the ambient finite-index product

Let C be the core of G0 in G. It has finite index. Since G is normal in E, each E-conjugate of C is a subgroup of G with the same index. A finitely generated group has only finitely many subgroups of that index, by its permutation representations on the finite coset set. Thus the intersection K of ALL E-conjugates of C is a finite intersection, is normal in E, has finite index in G, and is contained in G0. Normality in E, not merely normality in G, is proved here.

The quotient E/G is Z because h1−h2 is onto. Therefore E/K is an extension of Z by the finite group F=G/K. Choose any t mapping to1. The homomorphism n↦t^n is injective, so this extension really splits as F⋊Z. The induced automorphism of the FINITE F has finite order r≥1. Reducing the stable exponent modulo r defines a genuine homomorphism

    F⋊Z → F⋊(Z/rZ).

It is injective on F, since the action factors through Z/rZ. The preimage E0 in E of its kernel has finite index and intersects G exactly in K. For trivial action r=1, the finite quotient is simply F and this conclusion remains correct. No residual-finiteness hypothesis on E is needed for this step.

For any finite-index E0≤Γ1×Γ2, the coordinate intersections Γ1′={a:(a,1)∈E0} and Γ2′={b:(1,b)∈E0} have finite index in their factors, and their product is contained in E0. Hence

    G1=G∩(Γ1′×Γ2′)

has finite index in G and lies in E0∩G=K≤G0. It therefore also has finite index in G0. No assumption that the original G0 is normal, or itself a product kernel in a finite-index ambient, has been used.

## 2. Height alignment and all-character extension

The height image of each finite-index Γi′ is liZ with li≥1. Its kernel is Σi′=Γi′∩Σi. Choosing zi with height li gives an exact splitting Γi′=Σi′⋊〈zi〉. Let L be the lcm of the two li and put ai=zi^{L/li}. The subgroup Λi=Σi′⋊〈ai〉 has finite index in Γi′ and height image LZ.

This replacement DOES NOT shrink G1. If (g1,g2) belongs to G1, its common height belongs to both l1Z and l2Z, hence is qL. Writing gi=si zi^{qL/li} places each coordinate in Λi. The reverse inclusion is immediate. Consequently

    G1=G∩(Λ1×Λ2)=(Σ1′×Σ2′)⋊〈(a1,a2)〉.

The two conjugation automorphisms need not agree. An arbitrary character ψ on G1 has restrictions λi to each independent Σi′, and c=ψ(a1,a2). Applying ψ to the separate conjugation relations makes λi invariant under conjugation by its corresponding ai. Thus λi extends to Λi with value0 on ai, and

    ψ̃(b1,b2)=λ̃1(b1)+λ̃2(b2)+c h1(b1)/L

is an INTEGRAL homomorphism extending ψ. Both normalized heights hi/L are integer-valued on Λi. This verifies the claimed all-character extension after the chosen aligned passage, without claiming extension to the ORIGINAL E. Nontrivial twists in the chosen zi, different surface groups, and different monodromies cause no exception.

## 3. The actual double image and its finite-index subgroup

The primitive χ on G0 gives χ(G1)=kZ for some k≥1, because G1 has finite index. Therefore χ1=χ|G1/k is integral and onto, and it extends to Λ1×Λ2 by the previous calculation. Let F′=ε^{-1}(kZ). This has index k in F2, is finitely generated free, and ε1=ε|F′/k is integer-valued and onto (u^k has value1).

The reviewed normal-double fold/quotient injection identifies D0 with the EXACT fiber product

    {(g,w)∈G0×F2:χ(g)=ε(w)}.

This equality uses onto χ and does not require a splitting of G0 over N beyond the lift of the infinite cyclic quotient. Intersecting this actual image with the finite-index ambient subgroup G1×F′ gives a finite-index subgroup D′≤D0. Division of the equality by k gives precisely

    D′={(g,w)∈G1×F′:χ1(g)=ε1(w)}.

There is no assertion that the smaller vertexwise amalgam G1*_{N∩G1}G1 has finite index in D0. The proof correctly uses the intersection in the PRODUCT MODEL of the actual double instead. That distinction repairs the previously dangerous finite-index shortcut.

In Λ1×Λ2×F′, the first displayed equation hi/L difference=0 forces the pair of surface-by-cyclic coordinates into EXACTLY G1, by height alignment. The second displayed equation then becomes χ1(g)=ε1(w), because χ̃1 restricts to χ1. Thus ker Ψ is exactly D′, not a larger subgroup or merely a containing coabelian group. Both coordinates of Ψ are homomorphisms to Z, so the target is finitely generated abelian.

## 4. Intrinsic filling theorem and finite presentability

Each Λi is a finite-index subgroup of the given automatic Γi; finite-index passage preserves synchronous automaticity. F′ is finitely generated free. The finite direct product Λ1×Λ2×F′ is therefore automatic and finitely presented. This is an automatic AMBIENT group; neither G0 nor D′ is being incorrectly presumed automatic.

G0 is finitely presented as noted above, and N is finitely generated by hypothesis. The amalgam D0 is finitely presented using two finite presentations of G0 and finitely many identifications of N-generators. No finite presentation of N is needed. Its finite-index subgroup D′ is consequently finitely presented.

I directly inspected the cached primary Llosa Isenrich arXiv:2404.12334v2, Corollary1.3, printedp.2. It applies to a finitely presented kernel of a homomorphism from a finitely presented synchronous or asynchronous automatic group to a finitely generated abelian group; it does not require surjectivity of that homomorphism. The required finitely presented kernel here is D′, not N. It gives the intrinsic exponential Dehn upper bound for D′. Finite-index invariance of the Dehn equivalence class then gives the same growth upper bound for D0. No extrinsic distortion estimate or ambient filling is substituted for this intrinsic theorem.

## Falsification attempts and limits

I checked nonnormal G0, trivial finite conjugation action r=1, trivial F, unequal height indices li, k=1, arbitrary surface monodromy twists, degenerate compact surface factors, and N not finitely presented. The repaired proof covers each. The finite-index construction does not assume that χ itself extends to E, and does not require every finite-index subgroup of G to have its own initial product-kernel description.

The conclusion is restricted to one different-character double after arbitrary finite-index passage in the ORIGINAL surface-product model. No theorem that every later iterated doubled subgroup has this structure is proved. Failing the extension condition in another model would still not supply a super-exponential lower bound. No resolution, publication readiness, human peer review, or originality is certified.
