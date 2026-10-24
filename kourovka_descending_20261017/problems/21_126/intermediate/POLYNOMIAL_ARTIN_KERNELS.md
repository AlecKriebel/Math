# Polynomial upper bounds for finitely presented integral Artin kernels

October 24, 2026 UTC. **Derived class obstruction; not a solution of Kourovka 21.126. No originality or priority claim.** This note extends the attempted zero-weight construction beyond an independent dead set. It supersedes the *remaining-gap statement* at the end of INDEPENDENT_ZERO_DIRECTIONS.md: the gap there is repaired here by adding dead vertices one at a time, rather than treating all their stable letters simultaneously over one fixed base.

## Statement

Let Γ be finite, φ:A(Γ)→Z a nonzero integral character, and H=ker φ. Write S for its nonzero-weight vertices and D for its zero-weight vertices, with d=|D|. If H is finitely presented, then

    δ_H(n)≼n^a_d,     a_d=(9·3^d−1)/2.

This deliberately nonsharp polynomial bound follows from the construction below. In particular neither the superexponential nor the strongly intermediate branch of 21.126 can be realized by a finitely presented integral Artin kernel. This says nothing about arbitrary subgroups of such a kernel, or arbitrary finitely presented subgroups of RAAGs.

## Exact graph hypotheses supplied by an established theorem

Meier–Meinert–VanWyk, *Higher generation subgroup sets and the Σ-invariants of graph groups*, Comment. Math. Helv. 73 (1998), 22–44, Corollary A(i), characterizes finite presentation of H. Its n=2 case, expanding the recursive definition of 1-Z-acyclic domination, gives precisely:

(A) the living flag complex L_S is simply connected;
(B) each dead vertex z has a nonempty connected living link S_z=lk_Γ(z)∩S;
(C) each edge between dead vertices has a common living neighbor.

Indeed 0-acyclicity of each living link means connectedness, including nonemptiness, and 0-acyclic domination in the full link says each dead neighbor has a living neighbor in that link. The latter is condition (C). The primary source's Corollary A and preceding definition were inspected directly in sources/mmv1998.txt, printed p.24. Casals-Ruiz–Kazachkov–Roy, *Presentation of kernels of rational characters of right-angled Artin groups*, DOI 10.1112/blms.70090 (2025), Theorem 3.2, independently states this same finiteness criterion and provides explicit presentations. Its result is used only as corroboration; the cited original Corollary A supplies the implication needed here.

The proof below is also a standalone sufficient theorem under (A)–(C). It does not require using the converse criterion during the construction.

## Lemma 1: cubic ambient distortion with a connected dominating living part

Suppose a finite graph Λ has a nonempty connected living subgraph T, all weights on T are nonzero, all other weights vanish, and every dead vertex has a living neighbor. Then K=ker ψ is finitely generated and

    Dist_K^{A(Λ)}(n)≼n³.

Proof. Normalize the live weights to have gcd one, invert negative-weight generators, and choose a fixed live word t of height one. Let K_0 be the kernel of ψ restricted to A(T). The connected version of rectangular height pushing (INDEPENDENT_ZERO_DIRECTIONS.md, section 1) gives a finite generating set for K_0 and

    |k|_(K_0) ≤ C(|k|_(A(T))+1)².

For each dead vertex z let d_z be the gcd of the weights on its living neighbors. It is positive. Choose a word v_z, supported on those neighbors, with height d_z. Let z_i=t^i z t^(−i), 0≤i<d_z. These, together with the finite generating set of K_0, generate K.

For explicit length control, start with an ambient word w=s_1…s_n representing k∈K. Let q_j=ψ(s_1…s_j), with q_0=q_n=0. Then |q_j|≤Mn, where M bounds generator weights. The exact Schreier product identity is

    w=∏_(j=1)^n [ t^(q_(j−1)) s_j t^(−q_j) ].

A factor from a live letter is a height-zero live word of ambient length O(n), hence has K_0-length O(n²). For a dead letter z^ε, write its prefix height q=i+ℓd_z with 0≤i<d_z and set h=t^q v_z^(−ℓ) t^(−i)∈K_0. The corresponding factor equals h z_i^ε h^−1. Here |ℓ|=O(n+1), so h has ambient live length O(n+1), and K_0-length O((n+1)²). There are n factors. Thus |k|_K=O((n+1)³), proving both finite generation and the stated distortion bound.

No relation among dead vertices was used. Their commuting relations can only identify words; the displayed rewriting is an exact identity in the given RAAG.

## Lemma 2: adding one dead vertex

Let Γ' be an induced subgraph containing every living vertex, and let z be a new dead vertex. Put B=A(Γ'), G=ker(φ|_B), Λ=lk(z)∩Γ', K=ker(φ|_(A(Λ))). Assume G is finitely presented and K is finitely generated. Let d_z>0 be the gcd of live weights in Λ. Choose t∈A(S) of height one. Then

    ker(φ|_(A(Γ'∪{z})))
      ≅ ⟨ G, z_i (0≤i<d_z) | [z_i,t^i K t^(−i)]=1 ⟩.

Proof. A(Γ'∪{z}) is the identity HNN extension of B centralizing A(Λ). The residue/Britton argument in INDEPENDENT_ZERO_DIRECTIONS.md, section 3, applies with B in place of A(S). The height representative t still lies in B. Surjectivity is the same formula using a height-d_z word v_z∈A(Λ): for q=i+ℓd_z, t^q z t^(−q)=h z_i h^−1 with h=t^q v_z^(−ℓ)t^(−i)∈G. For injectivity, an ambient Britton pinch forces t^(−i) g t^j∈A(Λ), whence d_z divides j−i, so i=j; the remaining condition is exactly membership in t^i K t^(−i). This contradicts reducedness. The argument works with either stable-letter sign and negative heights.

If K has ambient distortion at most n³ in A(Λ), its fixed conjugates in G have distortion at most n³. Indeed A(Λ) is a full parabolic in B and hence isometrically embedded for standard word metrics, and finite generators of G have bounded B-length. Conjugation by a fixed t^i contributes only an additive constant.

## Induction and area bound

Order the d dead vertices arbitrarily, and let G_j be the kernel for the induced graph on S plus its first j dead vertices. The living part remains fixed throughout.

By (A) and WEIGHTED_HEIGHT_QUARTIC.md, G_0 is finitely presented with δ_(G_0)≼n^4.

At step j+1, consider the link Λ of the new dead vertex z in the previous induced graph. Its living subgraph is S_z, which is nonempty and connected by (B). Every dead vertex y in Λ is an earlier dead neighbor of z, so (C) supplies a living vertex adjacent to both y and z. That vertex lies in the living part of Λ and is adjacent to y there. Thus the living part of Λ dominates Λ. Lemma 1 shows its height kernel K is finitely generated and has cubic ambient distortion. Lemma 2 expresses G_(j+1) as finitely many identity HNN extensions of G_j over cubically distorted subgroups.

Apply the complete filling estimate proved in INDEPENDENT_ZERO_DIRECTIONS.md, section 2:

    δ_(G_(j+1))(n) ≼ n·δ_(G_j)(n+n³)+n⁴+δ_(G_j)(n).

If δ_(G_j)≼n^a_j with a_j≥4, this gives a_(j+1)=3a_j+1. Each step has a finite presentation because K is finitely generated and the stable letters are finite in number. Solving the recurrence from a_0=4 gives

    a_j=(9·3^j−1)/2.

This proves the theorem.

## Boundary and interpretation checks

- If d=0, the bound is exactly the already established quartic bound for fixed nonzero weighted kernels.
- A singleton living graph is allowed. The live kernel may be trivial; the bounds remain valid upper estimates.
- The nonzero character may have image rZ; rescaling to Z does not change its kernel or zero set.
- At each associated link the gcd can differ from the whole graph's gcd. Divide the restricted character by this link gcd when invoking Lemma 1; its kernel does not change.
- Negative weights are removed by individual generator inversion. Dead adjacency and link conditions are unchanged.
- The proof uses homotopical disk fillings, not homological FP_2 conclusions.
- A large fixed exponent, or exponents unbounded across different finite graphs, do not create one group with superpolynomial Dehn function.

## Consequence for the research mechanism

The attempted rank-one coabelian construction has been reduced to a polynomial class under the exact finite-presentation criterion. To find an intermediate witness by kernel methods one must now leave integral rank-one Artin kernels, for example considering more general coabelian targets or nonnormal subgroups. Those cases are not settled by this note. No complete witness to 21.126 has been obtained.
