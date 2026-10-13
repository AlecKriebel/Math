# Tail generation by ordinary shifted moments

## Reader edition and material method credit

The proof below was independently accepted without a mathematical correction. Its original argument is retained verbatim apart from the final review-status sentence. The full [analytic acceptance](ACCEPTANCE.md) explains the scope and adversarial checks.

The coefficient-stabilization method is prior art. Dykema–Köstler–Williams, Lemma 5.1.8, the proof of Theorem 5.1.10, and Remark 5.1.11 already contain the finite-word coefficient argument and bounded extension. Weihua Liu, *Extended de Finetti theorems for boolean independence and monotone independence*, [arXiv:1505.02215v1](https://arxiv.org/pdf/1505.02215v1), §6.2, Lemma 6.8, printed p.33, gives a closely related past/future coefficient identity using Kaplansky approximation. Liu's setting is bilateral spreadability with a non-degenerated normal state and its specified generation hypothesis; it is not silently substituted for the present setting. His later publication is [Trans. Amer. Math. Soc. 370 (2018), 1959–2003](https://doi.org/10.1090/tran/7034); the publisher PDF was inaccessible, so the lemma numbering here refers to inspected arXiv v1.

The deduction presented here uses the future algebra for each finite family of initial-copy test vectors to obtain bounded WOT density of ordinary canonical moments in the general DKW setting. This is a description of the deduction, not a historical-priority claim. Prior quantum-symmetric cases, source versions, and the bounded literature-search limits are recorded in [Sources](SOURCES.md).

## Statement and scope

Let A be any unital C*-algebra, let 𝔄 be its universal unital free product over the positive integers, and let ψ be a state on 𝔄 invariant under all finite permutations of the copies. Write (π,H,ξ) for its GNS representation, π_j for the j-th copy, M=π(𝔄)'', and

T = ⋂_{N≥1} W*(π_j(A): j>N).

(The indexing j>N has the same intersection as j≥N.) Let Q=C*(T∪π(𝔄)). Let F:Q→T be the canonical conditional expectation of Dykema–Köstler–Williams, Theorem 5.1.10(iv). Let D be the least unital C*-subalgebra of T closed under all the F-valued copyword operations in their Definition 5.3.1, with repeated indices allowed.

Then D''=T in B(H). In fact the stronger assertion holds:

T is the weak-operator closure of F(π(𝔄)).

For every t∈T there is a net x_λ∈π(𝔄) with ||x_λ||≤||t|| and F(x_λ)→t in the weak operator topology. Thus the first stage of ordinary copyword moments already generates T as a von Neumann algebra; the higher recursive stages in the definition of D are unnecessary for this particular generation conclusion.

No separability, trace, faithfulness, factoriality, quantum symmetry, or normal extension of F to M is assumed.

## Source facts used

The needed established facts are in Kenneth J. Dykema, Claus Köstler, and John D. Williams, *Quantum symmetric states on free product C*-algebras*, arXiv:1305.7293v3, §§5.1 and 5.3:

1. Finite permutations σ induce ψ̂-preserving automorphisms β̂_σ of M, with β̂_σ(π_j(a))=π_{σ(j)}(a), implemented by unitaries U_σ fixing ξ (Definition 5.1.2).
2. The shift α on π(𝔄), and its extension to Q, is isometric and satisfies α(π_j(a))=π_{j+1}(a) (Lemma 5.1.9).
3. F(x)=WOT-lim_{k→∞} α^k(x) for x∈Q, and F is contractive with range T (Theorem 5.1.10).
4. D is a norm-closed unital C*-subalgebra of T containing F of every finite copyword (Definition 5.3.1, by setting every inserted D element equal to 1).

Source: https://arxiv.org/abs/1305.7293v3 and https://arxiv.org/pdf/1305.7293v3 . These are existing results, not claims of the present argument. Theorem 7.3 and Table 1 already establish D''=T for quantum symmetric states, including nonfaithful states. The argument below addresses the general symmetric-state case.

## Lemma: exact agreement on an initial-copy subspace

For N≥1, put

B_N=C*(π_j(A):1≤j≤N),
C_N=C*(π_j(A):j>N),
H_N=closure(B_N ξ),

and let P_N be the orthogonal projection of H onto H_N. Then, for every x∈C_N,

P_N F(x) P_N = P_N x P_N.                                      (1)

### Proof

First suppose x is a finite linear combination of finite copywords, all of whose indices belong to a finite set S⊂{N+1,N+2,…}. Fix k≥1. The map i↦i+k is an injection from S to S+k and extends to a permutation σ of the finite set S∪(S+k). Extend this permutation to ℕ by the identity off S∪(S+k). In particular, σ fixes every index 1,…,N.

For completeness, any bijection between two subsets S and S+k of the same finite ambient set extends to a permutation of that set: complete it by an arbitrary bijection from the complement of S to the complement of S+k. Alternatively, close the finite chains i↦i+k into cycles. Hence overlaps between S and S+k cause no difficulty. Repeated indices in a word are carried to the same shifted index on every occurrence.

It follows that β̂_σ(x)=α^k(x), whereas β̂_σ fixes B_N pointwise and U_σξ=ξ. Thus, for y,z∈B_N,

⟨α^k(x)yξ,zξ⟩
=ψ̂(z*α^k(x)y)
=ψ̂(β̂_σ(z*xy))
=ψ̂(z*xy)
=⟨xyξ,zξ⟩.                                                    (2)

Let k→∞ and use the canonical weak-operator-limit formula for F. This proves the same equality with F(x) in place of α^k(x).

Finite-copy polynomials from indices>N are norm dense in C_N. Contractivity of F and norm continuity of the matrix coefficients therefore give the equality for every x∈C_N. Finally B_Nξ is dense in H_N, so the equality extends to arbitrary pairs of vectors in H_N. This is precisely (1). ∎

## Proof of the theorem

Fix t∈T and let r=||t||. If r=0 there is nothing to prove. The increasing union ⋃_N H_N is dense in H, because every finite copyword uses finitely many indices and ξ is cyclic for π(𝔄). Consequently P_N→1 strongly.

Let a weak-operator neighborhood of t be specified by finitely many pairs of vectors (η_l,ζ_l), 1≤l≤m, and an error ε>0. Choose N so large that, simultaneously for all l,

2r ( ||η_l−P_Nη_l|| ||ζ_l||
     + ||P_Nη_l|| ||ζ_l−P_Nζ_l|| ) < ε/2.                     (3)

This is possible because P_N→1 strongly. Since t∈T⊂C_N'', Kaplansky density supplies x∈C_N, ||x||≤r, such that, simultaneously for all l,

|⟨(x−t)P_Nη_l,P_Nζ_l⟩| < ε/2.                               (4)

Only weak-operator density of the norm ball is needed; Kaplansky gives the stronger strong-operator density. The algebra C_N is contained in π(𝔄), since the image of a C*-homomorphism is norm closed and contains all the copy images. Put d=F(x). Then ||d||≤r. By (1), the expression in (4) equals

|⟨(d−t)P_Nη_l,P_Nζ_l⟩|.

Since ||d−t||≤2r, splitting the original vectors into their P_N components and remainders yields

|⟨(d−t)η_l,ζ_l⟩|
≤ 2r ( ||η_l−P_Nη_l|| ||ζ_l||
       + ||P_Nη_l|| ||ζ_l−P_Nζ_l|| )
   + |⟨(d−t)P_Nη_l,P_Nζ_l⟩|
< ε.

Thus every weak-operator neighborhood of t meets F(C_N), and in particular meets F(π(𝔄)), with the uniform bound ||d||≤||t||. Directing these neighborhoods by reverse inclusion gives the asserted bounded approximating net. Conversely F(π(𝔄))⊂T and T is weak-operator closed. Hence

closure_WOT(F(π(𝔄))) = T.                                    (5)

Finally F(π(𝔄))⊂D: finite copywords map into D by Definition 5.3.1 with every inserted element equal to 1; their linear span is norm dense in π(𝔄), F is bounded, and D is norm closed. Therefore (5) gives T⊂D''. The reverse inclusion follows from D⊂T and the fact that T is a von Neumann algebra. Hence D''=T. ∎

## Why the nonnormal-expectation obstruction does not apply

No weak-operator limit is passed through F. For a fixed N, formula (1) identifies only the matrix coefficients with both vectors in H_N, and only for inputs from C_N. Kaplansky approximation is performed in C_N''. The output F(x) is compared with t using (1) and a uniform norm bound; it is never asserted that F(x) converges to F(t) by continuity of F.

In Weihua Liu's Example 5.2.1 in the same source, M=B(ℓ²({0,1,…})), π_n(a)=e_{0n}+e_{n0}, T=Ce_{00}+C(1−e_{00}), and

F(x)=e_{00}xe_{00}+τ(x)(1−e_{00})

on the unitized compact operators, where τ is its scalar quotient character. F has no normal extension. Nevertheless F(π_n(a²))=e_{00}, since π_n(a²)=e_{00}+e_{nn}, so already F(π(𝔄)) linearly spans T. This is consistent with (5).

The argument also does not identify T with the finite-permutation fixed-point algebra, which can be larger (the source's Example 5.1.4).

## Attribution and status

This is an authored proof argument, separate from the cited third-party source. The general target is Question 5.3.5 of Dykema–Köstler–Williams and Question 2 in Ken Dykema's *Tail algebras, amalgamated free products and KMS states*, OWR 40/2016, printed p.2335, https://doi.org/10.4171/OWR/2016/40 . The earlier duplicate formulation is in OWR 28/2015, printed p.1619, https://doi.org/10.4171/OWR/2015/28 . The quantum-symmetric special case is prior work, as credited above.

The original proof received independent analytic acceptance on 13 October 2026 without a mathematical amendment. This attributed reader retains that argument; the acceptance is not journal acceptance, and novelty remains unverified.
