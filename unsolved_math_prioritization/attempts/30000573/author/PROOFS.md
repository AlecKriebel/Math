# Proofs and the remaining gap

All vector spaces are Hausdorff. Indices start at 0; a Fréchet space is a complete metrizable locally convex space. The product and weighted-shift results below hold over R and C. The root-of-unity construction in §5 and the cited unconditional-decomposition theorem use C. The source's one-sentence question does not itself spell out a field, so a complex theorem is not silently asserted for arbitrary real spaces.

## 1. Assumptions that cannot be omitted or conflated

A hypercyclic operator has a countable dense orbit, hence its underlying space must be separable. Nuclearity already implies separability for a Fréchet space E: choose an increasing defining sequence of seminorms p_j. For each j, nuclearity supplies a stronger seminorm q whose canonical map from the q-completion to the p_j-completion is nuclear. Such a map has separable range closure, because its nuclear expansion uses countably many range vectors. Its range is dense in the p_j-completion, which is consequently separable. E embeds topologically into the countable product of these separable Banach completions. That product is second countable; so is its subspace E; every second-countable space is separable.

An infinite-dimensional nuclear Fréchet space is not normable. Otherwise its topology comes from a Banach norm. Nuclearity then makes the identity a nuclear, and hence compact, Banach-space operator (factor the canonical nuclear map through an equivalent stronger norm). A compact identity forces finite dimension.

A **continuous norm** is weaker than normability: it is a continuous seminorm with zero kernel, but need not generate the topology. The explicit space in §4 has a continuous norm p_0 and is not normable. Neither nuclearity nor separability gives a Schauder basis. Nothing below assumes such a basis on an arbitrary E.

## 2. Approach 1: direct coding on countable products

**Theorem 2.1.** If E is a nonzero separable Fréchet space, the backward shift B on Y=E^N, given by (Bx)_j=x_(j+1), is a continuous linear mixing and chaotic operator.

**Proof.** Continuity follows coordinate by coordinate in the product topology. For nonempty open U,V in Y, choose nonempty basic cylinders U_0⊂U and V_0⊂V prescribing the first a and b coordinates. For every n≥a, their prescribed blocks occupy disjoint positions 0,...,a-1 and n,...,n+b-1. Fill those two blocks by permitted values and the other coordinates by zero. The resulting x lies in U and B^n x lies in V. This proves mixing.

To give a dense orbit directly, take a countable dense set D⊂E and list every nonempty finite word over D. Concatenate the list into an infinite sequence z. Each basic cylinder contains a finite word over D, and some shift of z begins with exactly that word. Thus the orbit of z is dense. For any prescribed finite initial block, periodically repeat that block (or a longer block containing it). The resulting sequence lies in Y and is periodic under B. Such sequences meet every basic cylinder. Therefore periodic points are dense. □

If E is nuclear, Y is nuclear. Indeed, a continuous seminorm on the product is dominated by finitely many coordinate seminorms. Strengthen each of those finitely many seminorms to obtain nuclear canonical maps in E. Their finite direct sum yields the requisite nuclear map for the product seminorm. Y is Fréchet by countability of the product and complete factor spaces. For E≠0, Y is infinite-dimensional and has no continuous norm: any continuous seminorm vanishes on the subspace supported outside some finite initial block.

**Gap.** This proves existence on E^N, not E. Arbitrary E is not identified with its countable power. A complemented copy of E in E^N does not by itself inherit a chaotic operator.

## 3. Approach 2: factor transfer, and a sharp obstruction

**Lemma 3.1 (dense-range intertwining).** Let A:Y→X be continuous linear with dense range and suppose AS=TA for continuous linear operators S,T. If S is hypercyclic, so is T; if periodic points of S are dense, those of T are dense.

**Proof.** If y has dense S-orbit, its image orbit A(S^n y)=T^n Ay is dense in X: every nonempty open V⊂X has nonempty open inverse image A^(-1)(V), using dense range. If S^q y=y then T^q Ay=Ay. Applying the same open-set argument to a dense set of periodic points proves the second assertion. □

**Theorem 3.2 (product-shift factor no-go).** Let E be a locally convex space and let X admit a continuous norm p. If A:E^N→X is continuous linear and AB=TA, with B the product backward shift and T continuous linear, then A=0.

**Proof.** Continuity of p∘A gives a finite initial block 0,...,L-1 and coordinate seminorm bounds such that p(Ax) is bounded by a constant times their maximum. In particular, p(Ax)=0 whenever that block is zero, so Ax=0 by definiteness of p. Thus A depends on the first L coordinates. Let i_j:E→E^N insert a vector in coordinate j. We have Ai_j=0 for j≥L. Since Bi_j=i_(j-1) for j≥1, the intertwining identity gives

    Ai_(L-1) = ABi_L = TAi_L = 0.

Repeating this step yields Ai_j=0 for 0≤j<L. Finite dependence now gives A=0 on the whole product. The case L=0 is immediate. □

This is stronger than observing that first-coordinate projection fails to intertwine. It rules out every continuous linear dense-range factor of the full shift into a nonzero continuous-norm target. The last input coordinate i_L is essential; a finite matrix truncation that deletes this boundary equation can create spurious intertwiners. The controls explicitly test that issue.

**Gap.** Nuclear spaces can have a continuous norm, so this route cannot solve the target class. Other source dynamics or other topologies may admit intertwiners; the theorem does not exclude them.

## 4. Approach 3: weighted shifts on a nuclear test space

Put

    X = {x=(x_n): p_k(x)=Σ_(n≥0)|x_n| 2^(k·2^n)<∞ for every integer k≥0}.

**Lemma 4.1.** X is an infinite-dimensional nuclear Fréchet space with an unconditional Schauder basis (e_n), a continuous norm p_0, and a nonnormable topology.

**Proof.** It is the projective intersection of weighted ℓ1 spaces. A sequence Cauchy in every p_k has compatible limits in those complete spaces, giving completeness; the countable seminorm family gives metrizability. Finite truncations converge in every p_k, absolutely and independently of order, establishing the unconditional basis. Nuclearity follows from the inclusion from the (k+1)-completion to the k-completion: on normalized coordinate vectors its nuclear coefficients are 2^(-2^n), whose sum is finite. The norm p_0 is continuous and definite. If X were normable, an increasing defining family would have some p_m dominating every p_k up to constants. But p_(m+1)(e_n)/p_m(e_n)=2^(2^n) is unbounded, a contradiction. □

**Theorem 4.2.** Every continuous weighted backward shift W on X, with (Wx)_r=w_(r+1)x_(r+1), satisfies W^n x→0 for every x∈X. Weights may be real or complex, and zeros are allowed.

**Proof.** Continuity gives m≥0 and C≥1 with p_0(Wx)≤C p_m(x). On e_j, j≥1, this implies |w_j|≤C·2^(m·2^j). Therefore

    |w_(r+1)...w_(r+n)| ≤ C^n 2^[m(2^(r+n+1)-2^(r+1))]
                            ≤ C^n 2^(2m·2^(r+n)).

For k≥0 and n≥1, using 2^r≤2^(r+n) and r+n≥n,

    p_k(W^n x)
    ≤ C^n Σ_(r≥0) |x_(r+n)| 2^[(k+2m)2^(r+n)]
    ≤ C^n 2^(-2^n) p_(k+2m+1)(x).

The scalar factor tends to zero: if c≥log_2 C, its base-2 logarithm is at most cn-2^n→-∞. Thus W^n x→0 in all defining seminorms. □

A nonzero periodic vector would have a constant subsequence W^(qn)x=x contradicting convergence to zero. There is also no dense orbit: a convergent orbit together with its limit is compact, whereas a Hausdorff infinite-dimensional topological vector space is not compact; alternatively project onto any nonzero coordinate functional, where the orbit is a convergent scalar sequence and hence not dense in the scalar field.

**Attribution and scope.** This X is precisely the topology of the lacunary example in Charpentier–Grosse-Erdmann–Menet, Example 3.8: the weights 2^k are cofinal among positive real growth parameters. Their no-hypercyclic-weighted-shift conclusion is credited prior literature. The displayed strong-stability estimate is proved here without claiming priority. Their Proposition 4.2 also characterizes weighted-shift existence for infinite-type power-series spaces. These facts say nothing negative about arbitrary continuous operators on X. In fact X belongs to the already positively treated complex unconditional-basis class.

**Gap.** A general construction cannot restrict itself to continuous weighted backward shifts, even when a nuclear basis is available.

## 5. Approach 4: dense periodic eigenvectors are not enough

We try to repair the shift by adding a diagonal operator. On the complex space X of §4 set

    λ_0=-1;  λ_n=exp(2πi/2^(n+2)) for n≥1;
    w_n=2^(-4^n) for n≥1;
    (Tx)_j=λ_j x_j + w_(j+1)x_(j+1).

The λ_j are pairwise distinct roots of unity. The diagonal part is an isometry for each p_k. The weighted shift is continuous because 0<w_n≤1 and p_k(Wx)≤p_k(x). Thus T is continuous.

**Proposition 5.1.** Periodic points of T are dense, but T is not hypercyclic.

**Proof of periodic density.** For each N, define a finite-support vector v^(N), zero above N, by

    v_j^(N) = (Π_(t=j+1)^N w_t) (Π_(t=0)^(j-1)(λ_N-λ_t)), 0≤j≤N.

Empty products are 1. Then

    (λ_N-λ_j)v_j^(N) = w_(j+1)v_(j+1)^(N)  (j<N),

so Tv^(N)=λ_N v^(N). Its Nth coordinate is the nonzero product Π_(t<N)(λ_N-λ_t). Hence v^(0),...,v^(N) span the first N+1 coordinate vectors by triangularity. All those eigenvectors are periodic, and any finite sum is periodic after taking the least common multiple of their periods. Their span contains every finite sequence, which is dense in X. □

**Proof of non-hypercyclicity.** Define c_0=1 and

    c_n = w_n c_(n-1)/(-1-λ_n), n≥1.

For n≥1 the argument of λ_n lies in (0,π/4], so Re λ_n≥0 and |-1-λ_n|≥1. Therefore |c_n|≤1. The formula f(x)=Σ_n c_n x_n defines a continuous complex-linear functional with |f(x)|≤p_0(x), and f(e_0)=1. On each coordinate vector,

    f(Te_0)=-f(e_0),
    f(Te_n)=λ_n c_n+w_n c_(n-1)=-c_n  (n≥1).

Density of finite sequences and continuity imply f∘T=-f on X. Thus the scalar image of any orbit is contained in {f(x),-f(x)}, a finite set. Since f is nonzero and hence onto C, a dense orbit in X would map densely into C, which is impossible. □

This example provides a fully explicit failed general strategy: even a dense union of root-of-unity eigenspaces does not guarantee hypercyclicity. The credited de la Rosa–Frerick–Grivaux–Peris constructions make much more careful choices to obtain the required orbit behavior. Their unconditional-decomposition mechanism cannot simply be installed on a general nuclear space without proving the needed projections, convergence, and continuity estimates.

**Gap.** The construction obtains periodic density but fails the dense-orbit half of chaos. No adjustment of its parameters producing chaos in the arbitrary basis-free target class has been established.

## 6. Approach 5: scalar-plus-small perturbations

**Lemma 6.1.** If a continuous operator T has a nonzero continuous eigenfunctional f, namely f∘T=λf, it is not hypercyclic.

**Proof.** A dense orbit would project densely onto the scalar field, but its projection is {λ^n f(x):n≥0}. If f(x)=0 it is constant. Otherwise, when |λ|≤1 it is bounded, and when |λ|>1 it misses a neighborhood of zero. Thus it is never dense. The same argument covers R and C. □

**Proposition 6.2.** On an infinite-dimensional Hausdorff locally convex space E, no operator T=λI+F with F continuous and finite rank is hypercyclic.

**Proof.** The finite-dimensional range R=F(E) is closed and is a proper subspace. There is a nonzero continuous linear functional f annihilating R: take a nonzero functional on the nonzero Hausdorff locally convex quotient E/R and compose with the quotient map, or apply the Hahn–Banach separation theorem. Then f∘T=λf. Lemma 6.1 applies. □

This elementary obstruction does not automatically extend from finite-rank to arbitrary compact perturbations by this proof: a compact operator can have dense range, leaving no annihilating functional. The stronger literature theorem, reported by Bonet in RACSAM 104 (2010), Theorem 2(2), excludes chaos for a nonzero scalar multiple of the identity plus a compact operator on a Fréchet space. Theorem 2(1) separately excludes hypercyclicity for a compact operator. Here compact means that some zero-neighborhood has relatively compact image. In a Montel Fréchet space, an operator mapping some zero-neighborhood to a bounded set is compact. A continuous operator need not have that neighborhood-to-bounded-set property. In particular, nuclearity of E does not say all its endomorphisms are compact in this sense.

**Gap.** Making a biorthogonal series sufficiently small to be a scalar-plus-compact construction cannot establish chaos. Removing that smallness requires fresh control of continuity and orbit approximation. No such basis-free construction is proved here, and no scalar-plus-compact representation theorem for all endomorphisms of a candidate nuclear E is proved either.

## 7. What remains unresolved

The five approaches above either prove a genuine positive subclass result or expose an exact obstruction to a candidate route. None decides the original arbitrary nuclear Fréchet existence question. The written all-parameter proofs, rather than the accompanying finite computations, establish the scoped conclusions. The real-field problem is not collapsed into the complex-field literature theorem. No new theorem resolving any unhandled full class, and no new-priority claim for the auxiliary statements, is made.
