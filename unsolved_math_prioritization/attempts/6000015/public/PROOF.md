# Stein tangent bundles: polyhedral quotients and the remaining gap

Problem 6000015 / AMR-059-0015, item 5(a) of Furuhata–Matsuzoe–Urakawa (1998), printed p.126.

## Outcome and conventions

**Partial result. The unrestricted original question is not resolved.** We prove the convex-domain question for every open polyhedral domain containing no complete affine line, including noncompact quotients. We also prove the translation-quotient case, a weak plurisubharmonic exhaustion result for compact hyperbolic quotients, and an explicit failure of a proposed metric-norm construction. None is a counterexample to the original question. No novelty or historical-priority claim is made.

A Hessian manifold here has a torsion-free flat real connection D and a positive-definite smooth metric g which locally equals D²φ. Completeness means Riemannian completeness of g, not affine geodesic completeness. In affine coordinates x and tangent-fiber coordinates y, the specified complex coordinates on TM are z=x+iy. An affine coordinate change x↦Ax+b induces z↦Az+b. We use the Levi matrix u_{i\bar j}=∂²u/(∂z_i∂\bar z_j).

The primary question asks whether this particular complex manifold TM is Stein for every complete Hessian manifold. Its particular convex-domain question allows any discrete affine group Γ acting freely and properly discontinuously on a convex domain Ω with no complete line. It imposes no compactness or homogeneity condition.

The only general complex-analysis criterion used in the new arguments is the classical Levi-problem characterization: a complex manifold admitting a smooth strictly plurisubharmonic exhaustion is Stein. Also used are the classical Steinness of convex domains in C^n and of open Riemann surfaces. These are background theorems, not new results here.

## 1. The lifted metric is exact Kähler and complete

Define the affine-horizontal/vertical metric and two-form on TM by

h = g_ij(x)(dx_i dx_j + dy_i dy_j),
ω = Σ g_ij(x) dx_i ∧ dy_j.

The formulas are intrinsic under the affine coordinate changes above. Define the global one-form

λ = −g_ij(x)y_j dx_i.

It is intrinsic because, at (x,y), it evaluates on a tangent vector ξ to TM as −g_x(y,dπ(ξ)). The Hessian symmetry ∂_k g_ij=∂_i g_kj gives

dλ = −(∂_k g_ij)y_j dx_k∧dx_i − g_ij dy_j∧dx_i = ω.

Thus h is Kähler and ω is exact. In particular TM contains no positive-dimensional compact complex submanifold: if C has complex dimension k>0, the positive volume ∫_C ω^k would equal ∫_C d(λ∧ω^{k−1})=0. This statement about smooth compact submanifolds is enough here; no singular-cycle theorem is needed.

If g is complete, then h is complete. Indeed π decreases lengths. A finite-h-length path therefore has a base path of finite g-length, whose tail lies in a relatively compact affine chart about its limiting base point. On that chart, g is uniformly comparable with a Euclidean metric. The h-length controls the total variation of both x and y, so y also converges to a finite vector. The path has a limit in TM. The finite-length divergent-path characterization of Riemannian completeness proves the assertion. Equivalently the same argument applies to a Cauchy sequence, using sufficiently short connecting paths whose projections remain in this chart.

These facts do not construct a global strictly plurisubharmonic exhaustion. Exactness dλ=ω is not itself an equation ω=i∂\bar∂u with a global proper u.

## 2. A complete Hessian torus defeats the squared-norm ansatz

On R² let

φ(x₁,x₂) = (x₁²+x₂²)/2 − (1/4)cos x₁ cos x₂,
g = D²φ.

Although φ is not periodic, its Hessian is invariant under (2πZ)² and descends to the affine torus M=R²/(2πZ)². Its matrix is

[[1+(1/4)cos x₁ cos x₂, −(1/4)sin x₁ sin x₂],
 [−(1/4)sin x₁ sin x₂, 1+(1/4)cos x₁ cos x₂]].

The two eigenvalues are 1+(1/4)cos(x₁+x₂) and 1+(1/4)cos(x₁−x₂); both lie in [3/4,5/4]. Hence g is positive definite and complete on the compact torus.

Let ρ(x,y)=g_x(y,y). At x=(0,0), y=(t,0), in the complex tangent direction v=∂/∂z₂, direct differentiation gives

∂ρ(v)=0,
L_ρ(v,\bar v)=(5/2−t²/4)/4=5/8−t²/16.

For t=4 this is −3/8, while ρ=20. For every C² function H on an interval containing 20 with H'(20)>0,

L_{H∘ρ}(v,\bar v)=H'(20)(−3/8)+H''(20)|∂ρ(v)|² < 0.

Therefore no C² reparametrization with derivative everywhere strictly positive makes H(ρ) plurisubharmonic on all of TM. Adding any fixed C² base function also cannot cure ρ itself: its contribution in this direction is independent of t, whereas 5/8−t²/16 tends to −∞.

This is solely a failure of the ansatz. The actual TM is C²/(2πZ)²≅(C*)², hence Stein. Its complex structure does not change with the chosen Hessian metric.

## 3. Every line-free polyhedral quotient is Stein

### Theorem 3.1

Let Ω be a nonempty open full-dimensional polyhedron in R^n containing no complete affine line. Let Γ≤Aff(R^n) preserve Ω and act freely and properly discontinuously. Then (Ω+iR^n)/Γ, and thus T(Ω/Γ), is Stein. No compactness assumption is needed.

### Proof

Write Ω={x:ℓ_j(x)>0, 1≤j≤N}, using one nonredundant defining affine form per facet, positive on Ω. Write ℓ_j(x)=a_j·x+b_j. The vectors a_j span R^n: if a_j·v=0 for every j, any x∈Ω would satisfy x+Rv⊂Ω, contrary to the line-free hypothesis.

Every affine automorphism of Ω permutes its facets. The kernel Γ₀ of the resulting homomorphism Γ→S_N is a normal subgroup of finite index. For each γ∈Γ₀ there are unique c_j(γ)>0 such that

ℓ_j(γx)=c_j(γ)ℓ_j(x).

To justify this equality, the two nonconstant affine functions vanish on the same facet hyperplane, so they are proportional; positivity on Ω fixes the sign. Each c_j is a multiplicative character. Put

τ(γ)=(log c₁(γ),...,log c_N(γ))∈R^N,
Λ=τ(Γ₀), V=span_R Λ.

The homomorphism τ is injective. If all c_j=1, spanning of the a_j implies first A_γ=I and then b_γ=0. Moreover Λ is discrete. If τ(γ_m)→0, then c_j(γ_m)→1. In the identities

a_j A_{γ_m}=c_j(γ_m)a_j,
a_j·b_{γ_m}=(c_j(γ_m)−1)b_j,

choose n independent rows a_j; these equations imply A_{γ_m}→I and b_{γ_m}→0. Proper discontinuity on Ω then forces γ_m=identity for all sufficiently large m. An additive subgroup with zero isolated is discrete. Thus Λ is a lattice in V, so V/Λ is compact.

Let H={ζ∈C:Re ζ>0} and S={w∈C:|Im w|<π/2}. The holomorphic map

L:C^n→C^N, L(z)=(ℓ₁(z),...,ℓ_N(z))

is an affine embedding with closed affine image A, because the linear part has rank n. If D=Ω+iR^n, then

L(D)=A∩H^N.

The componentwise principal logarithm is a biholomorphism H^N→S^N. It identifies D with the closed complex submanifold

Y={w∈S^N:(e^{w₁},...,e^{w_N})∈A}.

Under this identification Γ₀ acts by w↦w+τ(γ). Hence D/Γ₀≅Y/Λ, a closed complex submanifold of Z=S^N/Λ. Closedness holds because Y is closed and invariant, and the complement of its image has the invariant open preimage S^N\Y. Local evenly covered neighborhoods prove the submanifold assertion.

Let P:R^N→V^⊥ be the orthogonal projection. For w=u+iv∈S^N define

F(w)=||Pu||² + Σ_{j=1}^N[−log cos v_j].

F is smooth, nonnegative, and Λ-invariant. Its Levi matrix is

(1/2)P + (1/4)diag(sec²v₁,...,sec²v_N),

which is positive definite. It descends to a strictly plurisubharmonic function on Z.

It is an exhaustion on Z. A sublevel bounds Pu and bounds every v_j away from ±π/2. The remaining component of u lies in V and can be moved into a compact fundamental parallelepiped for Λ. Thus each sublevel is represented in a compact subset of S^N; its closedness makes it compact. Restricting to the closed submanifold Y/Λ gives a smooth nonnegative strictly plurisubharmonic exhaustion f of D/Γ₀.

Finally the finite group G=Γ/Γ₀ acts freely and holomorphically on D/Γ₀. The function

f_G(p)=Σ_{g∈G} f(gp)

is smooth, strictly plurisubharmonic, G-invariant, and proper: its sublevels lie in those of the identity summand f, all summands being nonnegative. It descends through the finite covering to a smooth strictly plurisubharmonic exhaustion of D/Γ. The Levi criterion proves Steinness. ∎

### A shorter compact-base construction

In the same polyhedral setting define

Ψ(z)=Σ_j[log|ℓ_j(z)|−logℓ_j(Re z)].

Every summand is nonnegative, and positive rescaling of ℓ_j changes nothing. Consequently Ψ is invariant under the whole Γ, including its facet permutations. Since ℓ_j(z) never vanishes on D, log|ℓ_j(z)| is pluriharmonic, and

L_Ψ(v,\bar v)=(1/4)Σ_j |a_j·v|²/ℓ_j(x)²>0 for v≠0.

Spanning of the a_j makes Ψ tend to infinity when ||y||→∞ locally uniformly in x. If Ω/Γ is compact, this is already an exhaustion on the quotient. If the base is noncompact, Ψ is not proper, since it vanishes on its entire zero section. The ambient-strip construction above supplies the missing control.

## 4. Translation quotients and dimension one

### Proposition 4.1

Let Ω⊂R^n be any open convex domain, and let Λ⊂R^n be a discrete subgroup of translations preserving Ω. Then (Ω+iR^n)/Λ is Stein.

### Proof

Let V=span_R Λ, of dimension r. For λ∈Λ and x∈Ω, convexity and invariance under all integer translates imply x+tλ∈Ω for every real t: place t between two integers and use the connecting segment. Iterating over a basis of Λ gives Ω+V=Ω. Choose a linear complement W, and put Ω₀=Ω∩W. This is a nonempty open convex domain in W and Ω=V+Ω₀. Complexifying the direct-sum decomposition gives

(Ω+iR^n)/Λ ≅ (V_C/Λ)×(Ω₀+iW).

A real linear lattice basis extends complex linearly, identifying V_C/Λ with C^r/Z^r≅(C*)^r through coordinatewise exponentials e^{2πiz_j}. The other factor is a convex domain in C^{n−r}; it is Stein. Products of Stein manifolds are Stein (sum proper nonnegative strictly plurisubharmonic exhaustions, or use product proper embeddings). ∎

This includes the trivial-group case. In the line-free convex-domain subquestion, however, a nonzero translation cannot preserve Ω, so this proposition addresses an additional class of the general Hessian problem rather than enlarging its line-free group class.

For every connected one-dimensional affine manifold M without boundary, TM is a connected noncompact Riemann surface. Noncompactness follows because a fiber over a point is a closed copy of R; it could not be closed in a compact total space. The classical open-Riemann-surface theorem makes TM Stein. Completeness is unnecessary in this dimension.

## 5. A continuous plurisubharmonic exhaustion for compact hyperbolic bases

This section removes the finite-facet assumption at the price of losing strictness.

Let Ω⊂R^n be any open convex domain containing no complete line. Let P(Ω) be the collection of nonzero real affine functions ℓ positive on Ω. Write ℓ(x)=a_ℓ·x+b_ℓ. Set

N_Ω(x,y)=sup_{ℓ∈P(Ω)} |a_ℓ·y|/ℓ(x),
U_Ω(x+iy)=(1/2)log(1+N_Ω(x,y)²).

### Proposition 5.1

N_Ω is a continuous, affine-invariant fiber norm, locally uniformly equivalent to the Euclidean norm in y. The function U_Ω is continuous and plurisubharmonic. It is invariant under every affine automorphism of Ω. If Ω/Γ is compact, it induces a continuous plurisubharmonic exhaustion of T(Ω/Γ).

### Proof

Fix x₀∈Ω. Normalize all forms by ℓ(x₀)=1. Their gradients comprise

K={a∈R^n:1+a·(u−x₀)≥0 for all u∈Ω}.

This set is closed. If B(x₀,r)⊂Ω, testing along ±a/||a|| shows ||a||≤1/r. Thus K is compact. Each displayed normalized affine function is actually strictly positive on Ω: a nonzero affine function nonnegative on an open set cannot vanish at an interior point. (When a=0 it is the constant 1.) Consequently K parametrizes exactly the normalized forms in P(Ω).

For x in a sufficiently small ball about x₀, the denominators 1+a·(x−x₀) are uniformly positive for a∈K. Hence

N_Ω(x,y)=max_{a∈K}|a·y|/[1+a·(x−x₀)]

is finite and continuous. Homogeneity and the triangle inequality are immediate. It is positive on y≠0: if all positive supporting forms annihilated y, every x+ty would satisfy every affine halfspace containing Ω, hence would lie in Ω. Here use the separation representation of an open convex set as the intersection of its containing open affine halfspaces, which follows from separation of each exterior or boundary point from Ω. This would produce a complete line, forbidden by hypothesis. Compactness of the unit sphere and continuity now give positive lower and finite upper norm bounds locally uniformly in x.

For each ℓ∈P(Ω), its complexification is nonvanishing on D=Ω+iR^n, and

u_ℓ(z)=log|ℓ(z)|−logℓ(Re z)
       =(1/2)log(1+(a_ℓ·y/ℓ(x))²)

is smooth plurisubharmonic, with Levi matrix a_ℓa_ℓ^T/(4ℓ(x)²). Since U_Ω=sup_ℓ u_ℓ is continuous and locally bounded, it is plurisubharmonic. For completeness, on any holomorphic disk the submean inequality for each u_ℓ is bounded above by the average of U_Ω; taking the supremum at the center gives the submean inequality for U_Ω. No unjustified interchange of a supremum and an integral is needed.

Pullback by an affine automorphism permutes the collection P(Ω), and its derivative acts on y. The quotient ratios, N_Ω, and U_Ω are therefore invariant. The local norm bounds show that U_Ω→∞ along unbounded fibers uniformly over compact base-coordinate sets. A compact quotient base has a finite collection of relatively compact affine charts; over each, a fixed sublevel has bounded fiber coordinates. The union of the corresponding compact closed disk-bundle pieces is compact. Thus the descended sublevels are compact. ∎

### Strictness really fails for this envelope

Take Ω=(0,∞)². An affine function positive on Ω has nonnegative coefficients a₁,a₂,b, not all zero. Its ratio is bounded by max(|y₁|/x₁,|y₂|/x₂), and the two coordinate forms attain that bound. Consequently

U_Ω(z)=(1/2)log(1+max(y₁²/x₁²,y₂²/x₂²)).

Near z=(1+2i,1), the first ratio strictly dominates. There U_Ω=log|z₁|−log x₁ and is independent of z₂. Its Levi form has a nonzero null direction throughout that neighborhood. The fact that this particular domain is Stein does not make this particular exhaustion strict.

## 6. The unclosed part of the original problem

Shimizu (1985) already gives an affirmative result for compact locally homogeneous hyperbolic affine manifolds. His general construction produces a strictly plurisubharmonic function away from a possible analytic divisor; compactness makes it exhaustive there. It cannot simply be read as a proof for the whole tangent bundle. The present finite-facet proof is independent of zero-freeness of that holomorphic kernel.

The universal question still requires a global holomorphically convex/Stein argument for arbitrary complete Hessian bases, or a counterexample. In the line-free convex formulation, the concrete missing step after Section 5 is to replace its generally degenerate invariant envelope by a smooth strictly plurisubharmonic exhaustion for arbitrary nonpolyhedral Ω and Γ, while also controlling escape in the base when Ω/Γ is noncompact. No such replacement is established here. The exact Kähler form in Section 1, the finite-facet proof, and the weak exhaustion in Section 5 do not imply that step.

## References

- H. Furuhata, H. Matsuzoe, H. Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, Interdisciplinary Information Sciences 4(2) (1998), 125–127, item 5(a). [Primary PDF](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en).
- S. Shimizu, *Complex analytic properties of tubes over locally homogeneous hyperbolic affine manifolds*, Tohoku Math. J. 37 (1985), 299–305. [DOI](https://doi.org/10.2748/tmj/1178228643), [primary PDF](https://www.jstage.jst.go.jp/article/tmj1949/37/3/37_3_299/_pdf/-char/en).
- H. Grauert, *On Levi's problem and the imbedding of real-analytic manifolds*, Ann. of Math. 68 (1958), 460–472. Standard strict-exhaustion criterion; cited in Shimizu's reference [4].
- H. Behnke and K. Stein, *Entwicklung analytischer Funktionen auf Riemannschen Flächen*, Math. Ann. 120 (1949), 430–461. Standard open-Riemann-surface theorem.

The proofs and symbolic controls were developed with AI assistance and have not received human peer review. Exact computations check displayed formulas, not universal Steinness or completeness of the literature search.
