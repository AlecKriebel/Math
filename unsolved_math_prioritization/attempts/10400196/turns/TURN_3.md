# Turn 3: the odd-Chern extension and the actual lifting freedom

**Original unrestricted target remains unresolved.** This turn avoids assuming connected-sum additivity in the lifting problem itself. It extends the canonical positive theorem to a substantially larger rational-homology domain and isolates which part of the residual problem is topological rather than an arbitrary scalar branch choice.

## 1. Canonical spin origin for every odd-order Chern class

Let M be an oriented rational homology three-sphere, with no assumption that |H1(M)| is odd. Suppose the Chern class c(sigma) of the chosen Spin^c structure has odd order, including the zero class. Decompose the finite group H²(M;Z) canonically into its 2-primary and odd-primary subgroups.

There is a unique element a_odd in the odd-primary subgroup satisfying

    2 a_odd=c(sigma).

Define sigma0=sigma-a_odd using the affine H² action. The Chern map is affine over multiplication by two, so c(sigma0)=0. Deloup–Massuyeau's spin/Spin^c exact sequence identifies the image of Spin(M) with the zero-Chern structures. Moreover, for a rational homology sphere, H¹(M;Z)=0, and the Bockstein H¹(M;Z/2)→H²(M;Z)[2] is an isomorphism. Thus the map Spin(M)→Spin^c(M) is injective. There is a unique spin structure s_sigma inducing sigma0.

This spin structure is determined by sigma, even though M may have many spin structures. It does not come from picking one of them arbitrarily. Both the primary decomposition and the inverse of multiplication by two on its odd subgroup are canonical and commute with induced cohomology isomorphisms.

Let q0=q_(s_sigma). The unique element a in G=H1(M;Z) satisfying

    q_sigma(x)-q0(x)=b(a,x)

has odd order: by the affine embedding, it is the Poincare-dual image of a_odd, up to the fixed convention sign. Homogeneity makes q0(a) an odd-order element of Q/Z. The sign convention epsilon and canonical eta from Turn2 therefore still apply.

**Theorem 3.1.** For every rational homology Spin^c three-sphere with odd-order Chern class, including arbitrary even-primary first homology, the formula

    R_oddChern(M,sigma)
      = epsilon R(M,s_sigma)-8 eta(q0(a)) in Q/16Z

is canonical under orientation-preserving diffeomorphisms, reduces to the Gauss–Brown invariant, is additive under connected sum within this class, and has degree exactly one for Spin^c Y-surgeries. It agrees with epsilon R on every spin-induced structure in this rational-homology class and with Turn2 on every odd-order-H1 example.

**Proof.** The canonical spin-origin construction proves well-definedness and naturality. The quadratic completion and phase identity are exactly those of Turn2, now applied to the odd-order element a in a possibly even-order group. Connected sums preserve the odd-order Chern condition and split the uniquely defined spin origin and correction. Under a Spin^c Y-surgery, the canonical cohomology isomorphism transports c(sigma), its odd half, and the compatible spin structure. Hence it transports q0, q_sigma and a. The correction is unchanged by each Y-surgery, while the spin Rochlin term has zero second alternating difference. Thus the invariant has degree at most one. Integral homology spheres are included, and the same Poincare/S3 calibration as Turn2 proves that it is not degree zero. ∎

The extension covers, for example, every Spin^c structure on a rational homology sphere whose 2-primary first-homology summand has exponent two: doubling kills that summand, so every Chern class has odd order. The unresolved rational-homology structures are precisely those with a nonzero 2-primary Chern component, which require some higher 2-power torsion in H1.

## 2. Why that spin-origin mechanism stops at higher 2-power torsion

For a Spin^c structure with a nonzero 2-primary Chern component, subtracting an odd-primary class cannot make its Chern class zero. The preceding canonical spin origin is therefore unavailable. This is a real restriction of the construction, not merely a failure to choose a convenient notation.

There is a small exact model showing why one cannot repair the mechanism by a fully affine-and-conjugation-natural choice of spin origin on every torsor. Let the Spin^c torsor be Z/4 with conjugation j→-j and fixed-point (spin) subset {0,2}. Suppose a retraction r to this subset fixes0 and2, commutes with conjugation, and is equivariant under translation by the order-two element2. Conjugation gives r(1)=r(3), because it fixes both possible output points. Translation gives r(3)=r(1)+2. These contradict each other.

This is only an obstruction to that specific functorial choice mechanism. Translation by a 2-torsion cohomology class is not automatically induced by a diffeomorphism of a fixed three-manifold. Consequently this model is not a nonexistence theorem for a diffeomorphism invariant and does not add an unstated naturality axiom to Question10.21. It indicates exactly where a construction using more than a selected spin origin would be required.

## 3. Classification of degree-one scalar lifts, without additivity

Let X be a class of Spin^c three-manifolds closed under the surgeries being used, on which the finite Gauss phase B:X→Q/8Z is canonically defined and is of degree zero. This includes the torsion-Chern domain. Fix for this paragraph any section s:Q/8Z→Q/16Z and put F0=s∘B. Since B is unchanged by each Y-surgery, F0 is degree zero, regardless of whether the scalar section is additive.

**Proposition 3.2.** Every lift F:X→Q/16Z of B has a unique expression

    F=F0+8d,

where d:X→Z/2 is a diffeomorphism invariant. The lift F has degree at most one if and only if d does. It has degree zero if and only if d does.

**Proof.** The kernel of reduction Q/16Z→Q/8Z is exactly {0,8}, so the expression and uniqueness are pointwise. For a cube of disjoint Y-surgeries, the alternating sum of F0 is zero. The alternating sum of F is therefore the injection of the alternating sum of d under Z/2→Q/16Z, 1↦8. Since that injection is injective, either finite-type relation vanishes exactly when the other one does. The same reasoning with a single Y-graph gives the degree-zero assertion. ∎

Thus the weak scalar-lift problem by itself has no obstruction: the actual content of an intended refinement must specify which order-one Z/2 correction is required by naturality or normalization. Proposition3.2 does not compute the degree-one invariant space and is not a substitute for solving that topological problem.

For clarity, even “degree exactly one” alone does not remove the weakness. Define d to be R(M)/8 modulo2 when M is an integral homology sphere and zero otherwise. The quotient R/8 is defined there, since the Rochlin value is0 or8. First homology is unchanged by every Y-surgery, so each surgery cube lies wholly in one of these two domains. The spin degree-one theorem then proves that d has degree at most one, and the Poincare/S3 comparison proves exact degree one. A scalar branch F0 with s(0)=0 would therefore produce a degree-one lift F0+8d.

We do **not** promote this piecewise construction to a solution of the intended question. It simply appends known homology-sphere information to a degree-zero phase branch and lacks the natural compatibility expected of a Rochlin-type refinement. Its defects are explicit, not a philosophical objection. For the section represented in [0,8), the two RP3 phases yield values1 and7, whereas orientation reversal negates the classical values1 and15. Fourfold connected sums of the negative-phase RP3 have Brown value4, so the branch gives4 while additivity of the single value7 would require12 modulo16. It also fails agreement with the classical spin invariant in these cases. These are properties a meaningful proposed lift must state and verify rather than silently presume.

## 4. Scope after this turn

The canonical construction now treats all rational homology spheres whose selected Spin^c Chern class has odd order, including all spin-induced structures and the entire exponent-two 2-primary case. It is genuinely order one and needs no arbitrary phase section. It remains a restricted positive theorem.

For the higher 2-primary Chern case, the affine spin-origin shortcut fails. For general non-torsion Chern classes, the original finite phase still needs a precise definition or extra data; Turn1's explicit section dependence and Turn2's conditional additive obstruction remain applicable. Neither is a blanket rejection of all possible nonadditive invariants.

The next substantive turn should examine a presentation-independent higher-2-primary correction or a genuine diffeomorphism/surgery obstruction, with explicit finite-type and spin-normalization requirements. If the source cannot justify those requirements, they must be kept as separately scoped targets. No arbitrary branch or conditional no-go is counted as an original solution.
