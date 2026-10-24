# Normal subgroup upper bound

Status: derived partial result using established theorems; not a solution of 21.126 and not asserted original. Prepared October 24, 2026 UTC.

**Proposition.** If N is a finitely presented normal subgroup of a right-angled Artin group A, then δ_N ≼ exp(n).

The claim concerns intrinsic filling in N. It does not say that arbitrary finitely presented subgroups satisfy this bound, and it does not exclude superpolynomial subexponential Dehn functions even in the normal subclass.

## External inputs

1. Casals-Ruiz–Lopez de Gamiz Zearra, *On finitely generated normal subgroups of right-angled Artin groups and graph products of groups*, [arXiv:2206.12182v2](https://arxiv.org/abs/2206.12182v2), Corollary 2.6, printed pp8–9: if M is a finitely generated **full** normal subgroup of a finite-graph RAAG B, then B/M is finite-by-abelian (also abelian-by-finite). “Full” means nontrivial intersection with every directly indecomposable standard direct factor. We use the finite-by-abelian conclusion, not merely virtual abelianness.
2. Llosa Isenrich, *From the second BNSR invariant to Dehn functions of coabelian subgroups*, [arXiv:2404.12334v2](https://arxiv.org/abs/2404.12334v2), Corollary 1.3, printed p2: a finitely presented kernel of a homomorphism from an automatic group onto a finitely generated abelian group has δ(n)≤C^n for some C>1.
3. RAAGs are automatic; finite-index passage preserves finite presentation and the coarse Dehn equivalence class. These are standard inputs, also explicitly used in the cited papers and Bridson2013 Proposition7.1.

## Proof, including removal of the fullness assumption

N has a finite generating set. The union of the supports of its generators is a finite vertex set S, and N lies in the induced RAAG A(S). Since N is normal in A, it is normal in A(S). Thus reduce to finite defining graphs.

Write A=A_1×⋯×A_k using the standard directly indecomposable join factors. If N∩A_i=1, the projection p:A→∏_{j≠i}A_j restricts to an injective homomorphism on N: its kernel on N is exactly N∩A_i. Its image p(N) is normal because p is surjective. It is finitely presented because it is isomorphic to N. Drop this factor and repeat. There are finitely many factors. Either N=1, whose Dehn function lies in the linear coarse class, or this produces a RAAG B and a full finitely presented normal subgroup M of B isomorphic to N.

Let π:B→Q=B/M. By input1 the group Q is finite-by-abelian. Equivalently, [Q,Q] is finite: a finite normal subgroup with abelian quotient contains [Q,Q], and conversely [Q,Q] itself then supplies such a finite normal subgroup. Put K=π^{-1}([Q,Q]). Then M≤K and K/M=[Q,Q] is finite, so M has finite index in K. Moreover K is the kernel of B→Q/[Q,Q], whose target is finitely generated abelian. Since M is finitely presented, its finite extension K is finitely presented. Input2 applies to B and K, giving δ_K≼exp. Finite-index invariance gives δ_N≃δ_M≃δ_K≼exp. □

## Scope and falsification cases

- N may fail to be full, be central, have finite index, be trivial, or have quotient with torsion. The proof treats these cases explicitly. It never assumes the quotient itself is torsion-free or abelian.
- If the ambient graph is infinite, the normality argument after finite support is valid only because N was normal in the whole ambient group; N is then invariant under every element of A(S).
- Dropping a factor is an isomorphism on N, not an assertion that N lies in the product of the remaining original factors.
- Finite extension K need not be a RAAG. Input2 only requires that its **ambient B** is automatic and that K is a finitely presented coabelian kernel.
- The theorem cannot be applied merely because N is normal in some arbitrary subgroup G≤A. In particular virtually compact special Rips groups G are usually proper subgroups of A; the theorem about normal subgroups of A does not transfer to normal subgroups of G.

This closes a direct normal-kernel super-exponential construction route. The remaining candidate would have to be nonnormal in every RAAG embedding, or answer the intermediate branch, neither of which is established here.
