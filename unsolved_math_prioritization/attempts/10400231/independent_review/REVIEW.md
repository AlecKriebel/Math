# Independent review: the prescribed-pair Alexander-polynomial counterexample

**Verdict: PASS_COMPLETE_LITERAL_COUNTEREXAMPLE.** No mandatory mathematical correction was found. The submitted proof refutes the sufficiency direction of the literal prescribed-pair conjecture in Ohtsuki–Turaev Conjecture 12.26. This is an independent adversarial AI audit, not human peer review. Priority has not been established.

Reviewed artifact: `COUNTEREXAMPLE.md`, SHA-256
`483bc7e3dccd4d6d262d36341becdf05bfa22f7d52e721eae4f51ecdc0fb95e5`.

## 1. Exact source and convention

The complete [published problem collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed p. 542 (PDF p. 170), was checked both as text and as a rendered page. The conjecture prescribes the isomorphism type of a rank-one finitely generated abelian group H, together with a Laurent polynomial in **Z[H/Tors H]**. It asks for a closed connected oriented three-manifold with that first integral homology group and Alexander polynomial. Its two displayed conditions are reciprocity with an even exponent and evaluation at one equal, up to sign, to the order of the torsion group.

The following remark states the known cases H=Z and H=Z⊕Z/n. It does not restrict the question to cyclic torsion. The proposed H=Z⊕(Z/2)^3 and Δ=t+6+t^−1 are consequently inside the literal scope. The source prescribes the group, not merely the number eight.

The polynomial convention was independently checked against [Massuyeau's complete author preprint](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/massu.pdf), Definition 3.5 and equation (3.2): it is the order of the first homology of the maximal free-abelian cover, over the integral Laurent UFD, up to its units ±t^k. For rank one this is precisely the cover in the candidate. The order is the gcd of the maximal presentation minors, without discarding integer content. Refined torsion with finite-group variables, rational normalization, and a division by t−1 are different constructions and are not substituted here.

[Alcaraz's full preprint](https://arxiv.org/abs/1406.2042), §4.2, supplies the familiar cut-surface context. Its polynomial-realization theorem with prescribed first Betti number does not prescribe the torsion group and does not contradict the candidate. The present audit independently rederives the integral statements rather than importing a rational Seifert-matrix computation.

## 2. Independent reconstruction of the topology

Write H₁(M;Z)=Z⊕T, and let φ be the primitive projection to Z. The following argument checks the central topological burden.

### Connected primitive surface

An integral degree-one cohomology class is represented by a map to S¹. A regular fiber is an embedded, oriented, possibly disconnected surface representing its Poincaré dual. Here H₂(M;Z)=Z, by integral Poincaré duality and the universal coefficient theorem. Since the total fiber class is nonzero, at least one connected component has nonzero class. A connected oriented embedded surface in a closed oriented three-manifold is null-homologous if it separates; conversely a nonseparating such surface admits a closed curve crossing it exactly once, obtained by joining its two sides through its connected complement. Its homology class is therefore primitive. In the rank-one group H₂(M;Z), this component represents the required generator up to sign. Reorient it if necessary.

This independently establishes precisely the connected nonseparating F needed here. It avoids assuming that arbitrary divisible codimension-one classes have connected representatives. Standard smoothing or triangulation in dimension three places this argument in the category of the source without adding a smoothness restriction.

### Ranks after cutting

Cut along a collar of F, of genus g, and call the connected complement X. Its two boundary components are F₊ and F₋. With their markings from F, the difference of their fundamental classes is the boundary of the relative fundamental class of X. Thus the difference map H₂(F;Q)→H₂(X;Q) in the re-gluing sequence is zero. Exactness makes H₂(X;Q)→H₂(M;Q) injective, so b₂(X)≤1.

The boundary pair sequence gives the reverse inequality: the one-dimensional image of H₃(X,∂X;Q) in H₂(∂X;Q)=Q² leaves a one-dimensional quotient injecting into H₂(X;Q). Therefore b₂(X)=1. Doubling X gives χ(X)=χ(∂X)/2=2−2g, and b₀(X)=1, b₃(X)=0 imply b₁(X)=2g.

This determines only the free rank. It does **not** assert that H₁(X;Z) is torsion-free. Write its full decomposition as Z^(2g)⊕⊕ⱼZ/dⱼ.

### Infinite-cover sequence over the integers

Ordinary singular chains in the infinite cyclic cover have finite support. The graph-of-spaces Mayer–Vietoris sequence therefore uses direct sums over the copies of X and F, giving, over R=Z[t,t^−1],

    H₁(F;Z)⊗R → H₁(X;Z)⊗R → H₁(M̃;Z)
      → H₀(F;Z)⊗R —(1−t)→ H₀(X;Z)⊗R.

The first map is i₊−t i₋ after choosing the deck generator. The last map is injective, since both spaces are connected and R is a domain. Hence the whole Alexander module is the cokernel of the first map. No extra generator survives from H₀. A possible kernel on the left, controlled by higher homology, does not add relations to that cokernel.

Present H₁(X;Z)⊗R by 2g+r generators and its r constant torsion relations dⱼeⱼ. The surface homology has 2g free generators, and their images add exactly 2g columns. This is a square (2g+r)-row presentation. In a suitable arrangement its block form is

    A(t) = [ B(t)   0 ]
           [ C(t)   D ],       D=diag(d₁,…,dᵣ).

Thus all cut-manifold torsion is retained. Altering lifts in C by multiples of D is a column operation. In particular det A=(∏dⱼ)det B; dropping D would wrongly discard integer content. The empty genus-zero and zero-torsion cases use the ordinary empty determinant convention.

### Exact specialization

Right exactness of the cokernel construction gives

    coker A(1) = H₁(X;Z)/(i₊−i₋)H₁(F;Z).

The ordinary **integral** re-gluing sequence identifies this quotient with the kernel of H₁(M;Z)→H₀(F;Z)=Z. That connecting map records signed crossings of F, hence equals φ up to sign. It is surjective and its kernel is exactly T. Consequently coker A(1)=T, including its full group structure.

No flatness assertion about evaluation at one is needed: cokernels commute with this tensor product by right exactness. Potential Tor terms elsewhere in a tensor-product sequence do not change the displayed cokernel calculation.

## 3. Alexander order, finite modules, and extra-factor attacks

Since coker A(1) is finite, det A(1)≠0 and its absolute value is |T|. Therefore det A(t) is nonzero, the square map is injective over the fraction field, and the presented module is R-torsion. Its zeroth Fitting ideal is the principal ideal generated by the sole maximal minor det A(t). By the integral order definition, Δ_M is this determinant up to ±t^k.

This step is essential. For an arbitrary finitely presented R-module, the order alone need not determine the size or rank of its specialization: for example R/(p,t−1) has order gcd(p,t−1)=1 but coinvariants Z/p. That rectangular presentation cannot invalidate the proof because the topology supplies an actual square presentation of the entire module. The proof does not replace the module by a pseudo-isomorphic one or by its localization. There is no discarded finite module, unseen gcd of several maximal minors, rational integer factor, or removable t−1 factor. Indeed a t−1 factor in this determinant would already contradict det A(1)≠0.

## 4. Independent algebra and the contradiction

Let r_p=dim_Fp(T⊗Fp). Reduction of A(1) has nullity r_p. Constant invertible row and column operations over Fp bring that evaluation to diag(I,0). Apply these same operations to the Laurent matrix. Every entry in each of the last r_p rows vanishes at t=1, so each row contains a factor t−1. Hence

    ord_(t=1)(det A mod p) ≥ r_p.

The zero polynomial is assigned infinite order. Laurent powers cause no issue: evaluation at one has kernel (t−1), and ±t^k is a unit there. Replacing the deck generator by its inverse also preserves the order. This independently proves the candidate's necessary condition.

For T=(Z/p)^3 the required order is at least three. But

    t[t+(p³−2)+t^−1] = (t−1)²+p³t,

which modulo p has order exactly two. The polynomial is symmetric and evaluates to p³, so both conditions of the source hold while the necessary condition fails. In particular p=2 gives the advertised counterexample. This settles the literal sufficiency assertion for prescribed pairs. It does not assert a classification of all realizable pairs.

## 5. Reproducibility and independent diagnostics

The submitted verifier was replayed beside the exact frozen artifact. All **8,967 author assertions** passed, and `verification.json` reproduced byte for byte (SHA-256 `4be4174d11c27b2185485a3d4abfb89902acf1fd724dccd45399a182f40bf1f9`).

The separately written checker uses subset dynamic programming for integer polynomial determinants and exact expansion at t=1. Its **13,154 independent assertions** include:

- every linear 2×2 polynomial matrix over F₂ and F₃;
- 3,584 three-dimensional matrix controls with exhaustive constant terms over F₂;
- 300 integral torsion-block presentations, including changes of torsion lifts;
- 100 genuine torus-bundle matrix examples, with Smith-group p-ranks and specialized determinants checked independently;
- the candidate family at eleven primes and unit-shift invariance.

The finite diagnostics test algebra and normalization; they do not prove the existence of the cut surface or either Mayer–Vietoris identification. Those topological claims are justified in Sections 2–3 above. Source hashes and the replay dependencies are retained separately for reproducibility.

## 6. Scope of the verdict

No mandatory revision of the frozen mathematical artifact is required. The counterexample concerns closed connected oriented three-manifolds with ordinary integral H₁ and the free-abelian Alexander polynomial. It requires no irreducibility, fiberedness, hyperbolicity, or surgery-model restriction. It does not refute the already-known cyclic-torsion cases or a different question prescribing only the order of T.

Targeted current primary-source searches did not establish priority for this elementary obstruction. Neither the author nor this review should claim that the result is new, nor that this AI audit is human peer review. Subject to those qualifications, the complete literal counterexample passes.
