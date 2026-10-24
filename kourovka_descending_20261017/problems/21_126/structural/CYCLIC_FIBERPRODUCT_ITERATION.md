# Cyclic diagonal fibre products: exact iteration and filling bounds

Prepared October 24, 2026 UTC. These are derived structural filters, not a solution of 21.126 or a claim of new literature priority.

## The group produced by iteration

Let 1→N→G→Z→1 be an extension. Choose t mapping to 1. This extension splits because Z is free on one generator, so G=N⋊_φ Z, where φ(n)=tnt^{-1}. For m≥1 define

P_m={(g_1,…,g_m)∈G^m: π(g_1)=⋯=π(g_m)}.

Then there is an explicit isomorphism

(N^m)⋊_{(φ,…,φ)} Z → P_m,
((n_1,…,n_m),k) ↦ (n_1t^k,…,n_mt^k).

It is a homomorphism by the semidirect multiplication rule; uniqueness of the common height k and the n_i proves injectivity and surjectivity. Taking the symmetric fibre product of P_m with P_ℓ over their common height map gives P_{m+ℓ}. Thus iterating this operation increases the number of copies of N. It does not insert another independent monodromy layer.

## Direct area estimate

**Lemma.** Suppose N is finitely presented and δ_N(n)≤C(n+1)^d for some d≥1. Then every P_m is finitely presented and has δ_{P_m}≼exp. More precisely, if the iterates of φ and φ^{-1} have word lengths ≤D(n+1)^r on a finite generating set of N, then δ_{P_m} is polynomially bounded.

Fix a finite presentation ⟨X|R⟩ for N. A finite presentation for N^m consists of m copies X_i of X, copies of R, and the finitely many cross commutators [x_i,y_j] for i≠j. Its Dehn function has a polynomial upper bound: move letters to factor order at cost O(n²) and fill the null word in each N factor, giving O(n²+∑δ_N(n_i))≤C'(n+1)^{max{2,d}}. Write q=max{2,d}.

Adjoin t and the finitely many relators t x_i t^{-1}=Φ_i(x), where Φ_i(x) is a chosen word for φ(x) in the same factor. This presents (N^m)⋊Z. The inverse conjugation rules may be included as finitely many redundant relators; finite enlargement does not change the Dehn class. Let L≥2 bound the lengths of all chosen forward and inverse image words.

Take a null word w of length n. Move the t letters to the right without first applying any relators of N^m, obtaining U t^k. Since w is null, k=0. During collection every original N letter has been conjugated by a height h with |h|≤n. Applying the chosen image substitutions gives a representative of that conjugate of length ≤L^n. The number of conjugation relator applications is bounded by C_0 n² L^n (an intentionally loose bound). Thus |U|≤nL^n and U=1 in N^m. Fill it with ≤C_1(nL^n+1)^q cells. This proves an exponential upper bound; no lower bound is asserted.

For polynomial iterate growth the raw substitution words may still have exponential lengths before free reduction. Instead, choose for each generator and each |h|≤n a shortest representative V_{h,x} of φ^h(x), of length ≤D(n+1)^r. The equality

 t V_{h,x} t^{-1}=V_{h+1,x}

can be filled using at most O(|V_{h,x}|) conjugation cells followed by a filling in N of a null word of length O((n+1)^r). The latter area is O((n+1)^{rd}) for the presentation of N, because both sides lie in the same N factor. Repeating this at most n times for each of at most n original letters gives a polynomial collection cost O(n²((n+1)^r+(n+1)^{rd})). The final word has length O(n(n+1)^r) and fills in N^m at polynomial cost. The h<0 case uses the inverse rules. Hence the second claim also holds.

The polynomial part does not assume that polynomial **reduced** iterate length bounds raw syntactic substitution size; the extra N fillings are essential.

## Application and central gap

If G is hyperbolic and N is finitely presented, Llosa Isenrich2404.12334v2 Theorem1.1 supplies the polynomial upper bound for δ_N. Consequently every P_m above has Dehn function at most exponential, even if the extension monodromy is exponentially growing and even if one iterates the symmetric cyclic fibre-product operation finitely many times. If G virtually embeds into a RAAG, P_m also virtually embeds into a product of RAAGs and hence into a RAAG after finite-index passage. This validates the embedding half but excludes a super-exponential witness from this **specific** operation.

This does not cover general Rips fibre products, whose kernels are merely finitely generated, or arbitrary fibre products over noncyclic quotients, or asymmetric iterated extensions. It does not exclude an intermediate Dehn function when only the exponential upper bound is known. Polynomial monodromy gives a polynomial upper bound, but the converse “exponential monodromy forces exponential Dehn function” is not asserted; already a single free-by-cyclic group can have quadratic Dehn function despite exponentially growing monodromy.

The proposed positive iteration route is therefore blocked without a materially new operation or an intrinsic lower-bound mechanism beyond repeating the same height constraint.
