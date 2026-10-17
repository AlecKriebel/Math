# Stabilizers and the exact compactification obstruction

## 1. No stabilizer prime 5 for imaginary-quadratic GL₂

Let F be imaginary quadratic and let G be a finite subgroup of GL₂(F). Every prime divisor of |G| is 2 or 3.

Indeed, if a prime ℓ divides |G|, Cauchy's theorem gives a nonidentity matrix of order ℓ. In characteristic zero it is diagonalizable and has a primitive ℓth-root eigenvalue ζ. Its characteristic polynomial over F has degree two, so [F(ζ):F]≤2 and [Q(ζ):Q]≤4. Hence ℓ≤5. If ℓ=5, the unique quadratic subfield of Q(ζ₅) is Q(√5), which is real. Consequently F∩Q(ζ₅)=Q and [F(ζ₅):F]=4, a contradiction.

For any arithmetic component Γ_r occurring in the paper, finite point stabilizers of its action on hyperbolic three-space are finite subgroups of GL₂(F). For completeness, determinant units have complex absolute value one; the stabilizer of a positive Hermitian form, after imposing that determinant condition, lies in a compact unitary group. Its intersection with the discrete arithmetic group is finite. The scalar kernel consists of roots of unity and is also of order divisible only by 2 and 3. This applies at small levels without assuming the level injects O×.

Let R=Z[1/6]. For a proper cellular action on a contractible model, subdivide so that cell stabilizers act without inversions. The equivariant homology spectral sequence has first page consisting of sums of H_t(G_σ,R), where G_σ is a finite cell stabilizer. These groups vanish for t>0, since |G_σ| is invertible in R. The remaining row is the cellular chain complex of the coarse quotient. Thus group homology and coarse quotient homology agree over R. This construction is natural for finite-index correspondences and conjugation, so their Hecke actions agree under the usual transfer convention. The same applies to the Borel–Serre model.

This removes **only a geometric stabilizer reason** for inverting 5. It does not remove the Z[1/30] coefficient requirement of the trace-fixed motivic complex used to construct the source cocycle in §3.2. No Z[1/6]-valued specialized cocycle has been constructed here.

## 2. The obstruction is a particular boundary homomorphism

Keep every class-group component r∈I. Let Y=Y₁(N), M=X₁^BS(N), D=∂M, and let X=X₁(N) be obtained by collapsing each connected boundary component to its own cusp. For any coefficient ring R, the relative homology sequence, or the homology sequence of this pushout, gives

H₁(D,R) → H₁(M,R) → H₁(X,R) → 0.

The last surjectivity follows because the map H₀(D,R)→H₀(C,R) to the separate cusp points is an isomorphism. Also M is homotopy equivalent to Y. Hence, for any R-module A and homomorphism f:H₁(Y,R)→A, conditions (1) and (2) below are equivalent for every coefficient ring R. If 6 is invertible in R, as for the intended R=Z[1/6], they are also equivalent to (3):

1. f factors through H₁(X,R).
2. f vanishes on the image of H₁(D,R).
3. The class corresponding to f restricts to zero on every cusp stabilizer, after the group/coarse comparison above.

The factorization, when it exists, is unique. This is an exact criterion, not only a sufficient spectral criterion.

At levels satisfying the source’s assumptions, including injectivity of O×→(O/N)×, for the already constructed auxiliary map of the paper write

b_{c,N} = cΠ_N ∘ [H₁(D,Z[1/30])→H₁(Y,Z[1/30])].

The unresolved parabolicity assertion is b_{c,N}=0. Where an unaugmented p-adic map Π_N^χ is available, define b_N^χ in exactly the same way. Its comparison relation is

(Nc²−R_N(c)) b_N^χ = b_{c,N}^χ.

When χ≠ω² an auxiliary c can be chosen with the factor invertible, so auxiliary and unaugmented boundary vanishing are equivalent. Theorem 4.3.5 already supplies the entire p-part when (p)∤N² or p∤h, including the relevant exceptional component when it vanishes. Corollary 4.3.6 assembles that existing result over Z[1/30] under its stated class-number condition. None of these auxiliary-removal statements itself proves b=0.

## 3. An explicit remaining cusp lemma

Choose, for every component r and cusp x, a matrix τ_x∈GL₂(F) taking ∞ to x. Put

Λ_{x,r} = {z∈F : γ_{x,r}(z)=τ_x [[1,z],[0,1]] τ_x⁻¹ ∈ Γ₁(N)_r}.

It is a rank-two Z-lattice. The cusp stabilizer modulo this unipotent lattice is a finite subgroup of O××O×. After inverting 6, its positive-degree homology vanishes and H₁ of the cusp stabilizer is a quotient of Λ_{x,r}⊗R. Therefore it suffices to prove the following exact identity on two Z-basis elements of Λ_{x,r}, for every r and every cusp x:

cΘ_{r,N}(γ_{x,r}(z)) = 0 in K₂(O′(N))⊗Z[1/30].                 (P)

Here cΘ_{r,N} is specifically the specialized, descended cocycle of the paper, §§3.4 and 4.1, restricted to Γ₁(N)_r; it is a homomorphism on that group because its coefficient action is trivial there. The identity can equivalently be checked through its defining CM specialization, with the descent comparison of Proposition 4.1.4 included. It must not be asserted merely in an extension field with an undetected p-primary restriction kernel.

The input to that specialization is the trace-fixed class whose Gersten residue is

(γ*−1) μ_r* (cϑ_r),

with cϑ_r and the moving matrix μ_r exactly as in (3.4). Thus (P) is a concrete residue/specialization calculation, not a request to find an arbitrary abstract homology map. Proving (P) without the residual-character exclusions would remove the compactification obstruction for the corresponding already-constructed coefficients, even if boundary cohomology itself does not vanish.

For an eventual R=Z[1/6] construction, the identical topological criterion and cusp test apply, but its R-valued motivic cocycle first has to exist. This report does not infer its existence from the geometric comparison.

## Sources

- Lecouturier–Sharifi–Shih–Wang, arXiv:2504.19125v1, §§3.2,3.4,4.1,4.3,5.1–5.2, especially (3.4), Proposition 4.1.4, Theorem 4.3.5, Corollary 4.3.6, and Lemma 5.2.1: https://arxiv.org/pdf/2504.19125v1
- Distinct author-hosted manuscript, same sections; pp.37,39–41 for geometric/cohomological comparison and pp.35–36 for the broader auxiliary removal: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf

The elementary no-order-five proof and the direct pushout description are provided above. They do not extend the source's motivic theorem to p=5.
