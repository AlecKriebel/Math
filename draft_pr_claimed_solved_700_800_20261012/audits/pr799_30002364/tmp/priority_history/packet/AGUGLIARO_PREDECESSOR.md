# A prior construction entails the full negative answer

This is an independently authored deduction from actual primary bodies. It is not a claim that Agugliaro explicitly names Sugiyama's question. It addresses priority of the unrestricted negative answer, not the particular D4×C2 eightfold, its four extra codimension-two classes, or priority of identifying the conflict in DKZ Remark 3.5.

## Primary identity and version scope

Thomas Agugliaro, *Examples for the standard conjecture of Hodge type*, arXiv:2401.17445v1, submitted 30 January 2024 21:18:59UTC. Actual v1 PDF:373784bytes, SHA256742d68d9860d667b5d0bc55020ac46e0d9e737dad7a05470812d5bcb77de72f1. The same construction is in v2,13 November 2025, and the official final article: Doc.Math.31(2026),855–904, DOI10.4171/DM/1057, published 19 January 2026 according to the official EMS landing page. Final PDF:632935bytes, SHA2562df0c9380e037c977b8efed2f764456c490d1e89e5f81a088741e086b93eaa81.

Read v1 pp.7,10–15 and relevant definitions pp.4–6; final §§2,3,5 through the exotic-class arguments. These are printed page numbers for v1 and final, respectively. Final abstract/Theorem 1.1 and §5 were visually checked: both allow g≥4. The arXiv landing abstract currently says g≥5; that metadata is not substituted for the actual §5 boundary. Final text extraction renders ≥ as >; visual inspection resolves it.

The final source positions are: CM-scheme existence Theorem 2.16(p 862), local splitting and type Lemmas5.1,5.3(p 873), CM model Proposition 5.4(p 874), primitive Frobenius Lemma 5.5(p 874), signed symmetric action Proposition 5.7(p 875), norm relation Proposition 5.8(pp 875–876), Hodge imbalance Proposition 5.12(pp 876–877), number-field descent Remark 5.13(pp 877–878), and non-Lefschetz cohomological Tate classes Lemma 5.14(pp 878–880). The corresponding v1 positions are Theorem 2.10(p 5), Lemmas5.1,5.2 and Proposition 5.3(p 10), Lemma 5.4/Proposition 5.6(p 11), Proposition 5.8(pp 11–12), Proposition 5.11(pp 12–13), Remark 5.12(p 13), and Lemmas5.14,5.15(pp 13–15).

## Exact field, avoiding the source's existence sentence

Set p=5, Q0=Q(sqrt(-2)), and R=Q(a), where

    F(a)=0,  F(X)=X^4-10X^2+5X+2.

Q0 is imaginary; -2=3mod5 is nonsquare, so5 is inert and unramified in Q0. Earlier working messages mistakenly wrote sqrt(2); that invalid choice was corrected and is not used here.

F has four real roots: its signs at -4,-1,0,1,4 are +,-,+,-,+ (values78,-12,2,-2,118). Mod5 it is X^4+2, which has no root. A monic quadratic factorization would be (X²+uX+b)(X²-uX+d). The X coefficient forces u(d-b)=0. If u=0, d=-b and b²=3; otherwise d=b and b²=2. Neither2 nor3 is square mod5. Thus Fmod5 is irreducible and separable, and5 is inert and unramified in R.

Modulo13,

    F=(X-9)(X³+9X²+6X+7),

and the cubic has no root mod13. The reduction is squarefree. Consequently Gal(Rtilde/Q) contains a4-cycle and a3-cycle. Its order divides24 and is divisible by12; a subgroup of order12 in S4 is A4, which contains no4-cycle. The group is therefore S4. This uses only the standard squarefree-factorization/Frobenius theorem; the finite factors and group check are reproduced in verify_finite.py.

The completion R5 is unramified quartic. It contains the unique unramified quadratic extension Q0,5, so the local embedding hypothesis holds. E=Q0·R is a CM field of degree8; its normal closure has group C2×S4 because Rtilde is totally real and Q0 imaginary. All hypotheses of Agugliaro's §5 construction at g=4 are now explicitly met.

This bypasses final Proposition 3.2's insufficient group-generation shortcut. The printed degree g/2 is correct: its base is the quadratic completion Q0,p, so the absolute degree is g. I initially misread that notation after text extraction, then corrected it after root's adversarial flag and my own visual inspection of printed p. 869. Only the unsupported implication that a g-cycle and a transposition automatically generate Sg is identified here as a source defect. For the general existence claim one can add a distinct prime with factorization(g-1)+1, then use2-transitivity and a transposition; the explicit quartic above makes that repair unnecessary for the priority conclusion.

The backward existence input was also checked directly: Tate, Bourbaki Exposé 352 (November 1968; printed 1971), §4 Lemma 4 and proof, printed pp. 102–103, realizes an arbitrary CM field/type over the integers of a number field after finite extension. The proof explicitly constructs a polarizable complex torus, descends to a number field, and uses potential good reduction. This closes the distinction between a merely p-adic model and an abelian variety over Qbar with actual good reduction. The official Numdam source is https://numdam.org/item/SB_1968-1969__11__95_0.pdf ; its byte identity and limited reading scope are in the ledgers.

## The all-powers Hodge premise, proved explicitly

The source supplies a CM abelian scheme with #Phi_v=1 and #Phi_vbar=3. Its generic fiber descends to Qbar. To see exactly what this condition means, enumerate the four real embeddings by1,2,3,4 and the two Q0 signs by±. An unramified Frobenius at5 acts as (c,(1234)), since5 is inert in Q0 and R. One local fiber of embeddings is

    Hv={(+,1),(-,2),(+,3),(-,4)}.

A CM type chooses one element from each conjugate pair. The condition #Phi∩Hv=1 gives a sign vector f∈{±1}^4 with three signs of one kind and one of the other, hence sum f=±2. This also follows from the determinant Hodge types(3,1),(1,3) in source Proposition 5.12 (v1Proposition5.11). It is a nonconstant vector with nonzero sum. For example Phi={(+,1),(+,2),(-,3),(+,4)} gives f=(1,1,-1,1).

The S4 action permutes these four coordinates without independent sign changes. For indices i,j of opposite signs, f-(ij)f=±2(e_i-e_j). Conjugates span the trace-zero subspace; averaging f supplies a nonzero constant vector. Thus the rational span of all conjugates of f is Q^4. This is full centered Hodge rank4, and weight-inclusive rank5.

Here is the all-powers step, rather than a one-power substitute. For every n, H¹(A^n) over a splitting field consists of n copies of each of the eight embedding eigenlines. A wedge monomial has a multiplicity-difference vector d∈Z^4 between conjugate embeddings. A rational Hodge class is invariant under all conjugate Hodge cocharacters, so each contributing monomial has d orthogonal to every conjugate of f. Full rank forces d=0. Every such balanced monomial can be paired into degree-two monomials from conjugate embeddings, which are Hodge classes. Degree-two rational Hodge classes are divisors by Lefschetz(1,1). The multiplication map from the algebra generated by them is surjective after extension of coefficients, hence over Q by faithful scalar extension. This proves that every Hodge class on every A^n is divisor-generated.

For geometric simplicity, full Hodge rank gives the full CM torus, whose H¹ commutant is the field E. The rational endomorphism algebra, a faithful subalgebra of this commutant containing E, equals E. A nonsimple abelian variety has a nontrivial rational idempotent from an isogeny decomposition; a field has none. Thus the generic fiber is simple and its type primitive. CM dimension is4 since[E:Q]=8.

## Special fiber and the cohomological conclusion

The abelian scheme in the source supplies actual good reduction, not merely an abstract Weil-number candidate. Its slopes are1/4 and3/4, each with multiplicity4. In E the two primes over5 have degree4; their Honda–Tate division-algebra invariants are4·(1/4)=1 and4·(3/4)=3, both0modZ, so the endomorphism division algebra is commutative. The same primitive-Frobenius argument applies to every positive power of Frobenius, so the special fiber is geometrically simple with geometric endomorphism algebra E, in agreement with the source's theorem over Fbar_p.

After a finite residue extension, Proposition 5.8 supplies the relation ∏_{i=1}^4 pi_i=q², where the pi_i are the four conjugates over Q0. The two conjugate eigenline wedges in H⁴ therefore give Tate classes. They are not divisor products: the divisor classes have balanced conjugate-pair weights; these wedges use one side of all four pairs. Source final Lemma 5.14 and v1Lemma5.15 explicitly make this a statement about l-adic cohomological Tate and Lefschetz classes; it is not merely about numerical cycles or the standard conjecture. The finite signed-permutation calculation gives H⁴ Tate dimension8 and divisor-product dimension6. This count is a supporting inference; the source's explicit non-Lefschetz assertion already suffices.

The predecessor therefore meets the complete premise of the universal forward implication and violates its conclusion already on the first power of a reduction. A short, explicit deduction from a prior published construction suffices to defeat a claim that the unrestricted negative answer is new. It does not establish who first recognized that deduction, that Agugliaro stated the Sugiyama answer, or priority of the candidate's distinct eightfold.
