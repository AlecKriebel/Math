# Literature-derived negative resolution at n = 8

Problem 30003042 / OWR-14213-008. This AI-assisted reconstruction preserves the complete setup, generic-index bridge, parameter-specific implication, and computational-dependency explanation of the accompanying [AUDIT.md](AUDIT.md). The source labels [O], [A], [K-pre], [K-journal], [KM], and [DKM] are defined there with public citations and exact inspection scopes.

The conclusion is e₈ ∈ γ⁵K(X over F(SB(C₀(φ)))) for an instance with dim φ = 17 and ind C₀(φ) = 256 over F. This contradicts the original nonmembership claim. This report has no external human review or formal certification; the underlying index theorem is published, and its Maple-dependent computation was not independently rerun.

## 2. Exact original setup

The following information is present in [O] p. 226 and carried into [A] §4:

1. F is a field of arbitrary characteristic, and φ is a nondegenerate quadratic form of odd dimension 2n+1. In characteristic 2, nondegeneracy is the quadratic-form convention used by these sources, not the impossible requirement that an odd-dimensional alternating polar form be nonsingular.
2. X is the orthogonal Grassmannian of n-dimensional totally isotropic subspaces of φ.
3. A = C₀(φ) has maximal index 2ⁿ. Since its degree is 2ⁿ, A is a division algebra.
4. S is the ordinary Severi–Brauer variety SB(A), and the field in the target is K = F(S). This kills the Clifford invariant by a function-field extension; it does not assert that φ itself is split over K.
5. The class e_n is the K-theoretic special Schubert class corresponding to a point on the split quadric. Over K it is understood through the splitting-field identification of K-theory. An actual rational Schubert subvariety or a rational point on the original anisotropic quadric is not being assumed.
6. The target excludes e_n from γ^(n+1−floor((n+1)/2))K(X_K) for all n ≥ 8.

At n = 8 these conditions say dim φ = 17, ind C₀(φ) = 256, S = SB(C₀(φ)), and e₈ is supposed not to lie in γ⁵K(X_K). The full original statement [O], Conjecture 3, and [A], Conjecture 4.7, have the same class, field, threshold, and range of n.

The scalar 18 used in the index theorem is the dimension of an auxiliary even form. It is not the dimension of the original odd form. Also, the later papers use m for an isotropic-subspace dimension, whereas Conjecture 3.3 of [A] uses m for the dimension of the whole quadratic form. The following argument uses d for the latter and r for the former to avoid this collision.

## 3. The two generic constructions and the needed bridge

### 3.1 The model required by the 2016 proof

Take an even nondegenerate form ψ over F with dimension d = 2n+2, trivial discriminant, and division half-Clifford algebra C⁺(ψ) of degree 2ⁿ. Set A = C⁺(ψ), S = SB(A), and K = F(S).

Then q = ψ_K has trivial discriminant and Clifford invariant, hence belongs to I_q^3(K). The text following [A], Corollary 1.6, calls forms constructed this way “generic” for its purposes and states that such models exist over an extension of any chosen base field. This is a deliberately broader convention than fixing a generic fiber of GL(N) → GL(N)/Spin_d.

For any nondegenerate codimension-one subform φ of ψ, [A] pp. 3–4 records

- dim φ = 2n+1;
- C₀(φ) ≅ C⁺(ψ) = A;
- a component X of the maximal Grassmannian of ψ is isomorphic to the maximal Grassmannian of φ.

Thus this construction gives exactly the original φ, X, A, S and K, with maximal Clifford index over F. Its suitability does not disappear merely because the Clifford algebra becomes split over K: that is the intended construction.

### 3.2 What the later exact-index result says

For a generic Spin₁₈-torsor, [K-pre] §6 and [K-journal] pp. 751–752 determine the indices of the Grassmannians of totally isotropic r-planes:

- 2ʳ for r = 1, 2, 3;
- 8 for r = 4, 5;
- 16 for r = 6, 7, 8, 9.

In particular, the fourth index is 8. The Grassmannians use vector-space dimensions: the first is the projective quadric, and the fourth parametrizes isotropic 4-planes, equivalently projective 3-spaces on that quadric. There is no projective-versus-affine off-by-one error.

### 3.3 Why the later result applies to the earlier model

It is unnecessary to prove that q = ψ_K is literally the same generic torsor as in [K-pre]. The appropriate consequence of [DKM], Proposition 2.1, is sufficient.

Let G be a split reductive group, P a parabolic subgroup, E_gen a generic G-torsor, and E any G-torsor. The proposition places the image of CH(E_gen/P) in the split Chow ring inside the image of CH(E/P). In top codimension, these images are respectively

ind(E_gen/P) Z ⊆ ind(E/P) Z.

Therefore ind(E/P) divides ind(E_gen/P). The direction matters: the generic index is a universal upper bound under divisibility. The proposition is valid for a split reductive group generally, not only for odd spin groups; [DKM] pp. 8–9 explicitly relates the even forms of trivial discriminant and Clifford invariant to Spin torsors.

Apply it to G = Spin₁₈, P defining the fourth Grassmannian, and q = ψ_K. Then

ind OG₄(q) divides 8.

This already contradicts the value 2^floor(18/4) = 16 demanded for this very model by [A], Conjecture 3.3. The exact value for an arbitrary member of the broader 2016 class is not required; the upper bound is enough. No assertion that every arbitrary nongeneric 18-dimensional form has index exactly 8 is made.

An alternative bridge follows the route of [K-pre] §6: a 17-dimensional subform has trivial even Clifford algebra, up to the harmless similarity normalization for its discriminant; its fourth Grassmannian has index dividing the generic Spin₁₇ value 8. Its inclusion in the 18-dimensional form implies the same bound for OG₄(q). [DKM] p. 2 verifies that similarity does not change these Grassmannians. The argument above using Spin₁₈ directly is simpler.

## 4. Reconstructing the parameter-specific implication

The following expands the actual paragraph on [A] p. 12 at d = 18. It also explains why a failure at d = 18 produces a failure at n = 8 rather than only an unspecified failure of the universal statement.

Let ψ, F, A, S, K and q = ψ_K be as in §3, with d = 18 and n = 8. Set r = floor(d/4) = 4. The published upper bound gives ind OG₄(q) | 8.

### 4.1 Transferring a linear-space class on the quadric

Let Y be the projective quadric of ψ, so dim Y = 16. Every closed point of OG₄(q), with residue field L, provides a totally isotropic 4-plane over L. Consequently Y_L contains a projective 3-space. Its structure-sheaf class l₃ belongs to T¹³K(Y_L), where T denotes the topological filtration, since 16−3 = 13.

The finite pushforward K(Y_L) → K(Y_K) preserves topological codimension. Under the split K-theory identification used in [A] p. 12, its value on l₃ is [L:K] l₃. The requisite rational K-classes and compatibility are part of the standard quadric/twisted-flag K-theory facts used in that published proof; their existence is not an assertion that these linear spaces are geometrically defined over K.

Because the index divides 8, integral combinations of such degrees give 8. Summing the corresponding transfers therefore yields

8l₃ ∈ T¹³K(Y_K).

This formulation avoids an unnecessary inference that there must be a field extension of degree exactly 8. The index is a gcd; a zero-cycle of degree 8, or a finite integral combination of degrees, suffices. Equivalently one can use the degree not divisible by 16 singled out in [A] and the usual power-of-two splitting degrees.

### 4.2 Extracting the point class without division by 8

The K-theoretic relation invoked on [A] p. 12 specializes to

8l₃ = l₀ + h¹⁵ + 2h¹⁴ + 4h¹³,

where h is the class of a hyperplane section. This is consistent with iterating 2l_j = l_(j−1) + h^(16−j), for j = 1, 2, 3. It is an integral identity, not a rational-coefficient cancellation.

Each hyperplane term on the right belongs to T¹³: its exponent is at least 13. Subtracting those terms gives

l₀ ∈ T¹³K(Y_K).

### 4.3 The incidence correspondence and the important dimension shift

Use the even form ψ, not the odd φ, for this step. Let X be a component of its maximal Grassmannian, so its tautological isotropic subspaces have dimension 9. Let Z = P(T) be the incidence variety of an isotropic line inside such a 9-plane. Its projections are

Y ← Z → X,

written g and f, respectively. The fibers of f are P⁸, so dim Z−dim X = 8. Pullback by the smooth incidence projection g preserves the topological-filtration index, and proper pushforward by f lowers it by at most 8. The K-theoretic version of [A], equation (1.2), discussed on p. 11, identifies f_*g^*(l₀) with e₈. Thus

e₈ ∈ T^(13−8)K(X_K) = T⁵K(X_K).

Using the rank-8 tautological bundle of the odd-dimensional Grassmannian at this point would give the wrong relative dimension. The published argument first uses the rank-9 bundle for ψ and only then identifies its component with the Grassmannian of φ. This accounts for the exact parameter shift.

### 4.4 Turning topological membership into gamma membership

Since C₀(φ) = A has maximal index 256 over F and K = F(SB(A)), [A], Theorem 4.3, applies to the original odd-dimensional model. It identifies the topological and gamma filtrations on K(X_K). Equivalently, its even-component version is stated in Remark 4.5. Therefore

e₈ ∈ γ⁵K(X_K).

Finally,

n + 1 − floor((n+1)/2) = 8+1−4 = 5.

This is exactly the prohibited term. The arithmetic generalizes in the proof as

d = 2n+2,  r = floor(d/4) = floor((n+1)/2),

d−r−1−n = n+1−floor((n+1)/2).

Thus the published implication is pointwise in the dimension parameter. A purely formal contrapositive of “all Conjecture 4.7 instances imply all Conjecture 3.3 instances” would not by itself identify n = 8; the inspected proof does.

## 5. Computational and mathematical dependency scope

The negative resolution depends on the published index bound 8. Its provenance is transparent:

1. [K-pre], Theorem 3.6, describes the generic odd-spin Chow ring modulo torsion using its tautological Chern subring and one additional class.
2. Theorem 4.1 turns a divisibility calculation in a free integral Chow ring into the Grassmannian index. With n = 8 and r = 5, its auxiliary parameter is l = 3.
3. In §5, the author reports a Maple 2021 computation using the Chow ring package version 4.0. It shows that the cube of the relevant integral class is not divisible by 2²³. In the theorem's notation, this gives a deficiency at least 24−22 = 2, hence an upper bound 2^(5−2) = 8 for the fifth Spin₁₇ Grassmannian.
4. Appendix A specifies the weight substitutions, the type-C₈ parabolic with the package's reversed root numbering, the integral class, its Schubert expansion, and a nonzero parity result after normalization. The 128 normalization contributes 2²¹ to the cube; the printed normalized cube divided by 2 has a nonzero reduction modulo 2, consistent with exact valuation 22 for the original cube. These are descriptions and arithmetic interpretation of the paper's outputs, not outputs reproduced in this audit.
5. Monotonicity gives the fourth Spin₁₇ index at most 8. The paper uses known highest-index information and elementary splitting arguments for the matching lower bound. Section 6 passes to Spin₁₈ and obtains the displayed exact fourth/fifth values 8.
6. [KM] p. 5 explicitly summarizes the dimension-17 and dimension-18 deviations and expressly says their determination involved computer computations. It cites [K-pre] rather than supplying a new independent computation.

For the disproof itself, the upper bound 8 is enough. The exact-index lower bound, the rest of the Spin₁₈ list, the Spin₁₉ computations, and the general asymptotic bounds in [KM] are not necessary to the contradiction.

The independently checked portions here are the source identities and versions; exact target match; parameter and field matching; generic-index divisibility direction; application to the maximal-Clifford-index model; the integer arithmetic and codimension shifts in the existing implication; and the published final-preprint/journal agreement on the input value. The background K-theory, Chow-theory, and quadratic-form results cited inside these papers remain literature dependencies. No claim is made to have reproved Panin's theorem, the Chow-ring presentation, Totaro's theorem, or the underlying characteristic-free quadratic-form theory.

No Maple, Chow ring package, or other source-author program was downloaded or executed. No independent finite Schubert-ring computation or proof-assistant verification was performed. The software used locally only downloaded, hashed, extracted, and rendered sources and assembled this audit.

## Scope of this reconstruction

The inference is an existential negative resolution at n = 8 in the original maximal-Clifford-index and Severi–Brauer function-field setup. It does not classify all n or establish an optimal replacement threshold. The complete source-version comparison, inspection history, characteristic discussion, and mathematical cautions remain in [AUDIT.md](AUDIT.md). This is credited literature-derived coverage, with no new index theorem or novelty claim.
