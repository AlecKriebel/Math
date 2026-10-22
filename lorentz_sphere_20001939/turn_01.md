# Attempt 1 of 5: a global simple-eigenvalue obstruction

## Target and verdict

The target is the existence of two smooth, nonproportional, projectively equivalent indefinite metrics on the entire smooth three-sphere. No completeness assumption is available. This attempt does not resolve that question. It proves a topological obstruction stronger than merely excluding an everywhere-simple spectrum: a compatible tensor cannot have even one globally isolated simple real eigenvalue.

## Setup

For projectively equivalent metrics g and gbar in dimension three, put

L = |det(gbar)/det(g)|^(1/4) gbar^(-1) g.

Then L is g-self-adjoint and satisfies

(∇_X L)Y = (1/2)[dτ(Y)X + g(X,Y) grad_g τ],  τ = tr L.

A constant multiple of the identity is the trivial case. The normalization and compatibility equation are standard; see Bolsinov–Matveev, https://arxiv.org/abs/1301.2492, equations (2), (4), and (5).

## Proposition: globally isolated simple eigenvalues are impossible

Let M be a closed connected three-manifold with finite fundamental group. Suppose L is a compatible tensor for a pseudo-Riemannian metric g. There cannot exist a smooth real eigenvalue λ:M→R that has algebraic multiplicity one at every point.

Proof. Let χ(t)=det(tI-L)=(t-λ)q(t), where q is monic of degree two. Polynomial division makes the coefficients of q smooth. The condition q(λ)≠0 holds everywhere. Let E=ker(L-λI); it is a smooth line bundle. Its g-orthogonal complement F is the other primary summand, and both summands are nondegenerate. The projectors P_E,P_F are smooth and polynomial in L with smooth coefficients; in particular P_E=q(L)/q(λ).

Define a global pseudo-Riemannian metric h by declaring E perpendicular to F and setting

h|E = g|E / q(λ),
h|F(u,v) = g((L|F-λI)^(-1)u,v).

The inverses exist. The splitting lemma for compatible metrics gives local product coordinates in which h is a direct product h_E(x)⊕h_F(y), and E is its first factor. This assertion does not require eigenvalues within F to remain distinct: its hypothesis is the relatively prime factorization (t-λ)q. Thus E is a nondegenerate parallel line for the Levi-Civita connection of h. This is precisely the two-factor splitting construction, not an assertion that E is parallel for g.

Lift h and E to the finite universal cover N. It is compact and simply connected. The metric on the parallel line has holonomy in O(1)={±1}. On a simply connected base its flat line connection has trivial holonomy, so it admits a nonzero global h-parallel field V. The one-form α=h(V,·) is parallel, hence closed and nowhere zero. Since N is simply connected, α=df. But a real smooth function on compact N has an extremum, at which df=0. Contradiction. ∎

The splitting input is Bolsinov–Matveev, Theorem 3, https://arxiv.org/abs/0904.0535. The only imported geometric theorem in the proposition is this splitting lemma; its local product conclusion, including nonsemisimple complementary blocks, is the essential hypothesis. A global de Rham decomposition or geodesic completeness is neither asserted nor needed.

## Consequence for the proposed S^3 pair

Bolsinov–Matveev's Corollary 1.13 excludes a nonreal eigenvalue for a pair on S^3: a closed three-manifold with such an eigenvalue would be finitely covered by T^3. Hence write the continuous ordered eigenvalues as λ1≤λ2≤λ3.

Both collision sets must be nonempty:

C12={p:λ1(p)=λ2(p)} ≠∅,
C23={p:λ2(p)=λ3(p)} ≠∅.

Indeed, if C12 were empty, λ1 would be a smooth globally simple real eigenvalue; if C23 were empty, λ3 would be one. The proposition excludes each possibility. In particular an everywhere-simple Levi-Civita ansatz cannot give an example.

## Failed extension and remaining gap

The two collision sets need not intersect on purely topological grounds. A proof that they intersect, or that the signature prevents their compatible realization, has not been obtained. At collisions the spectral projector used above can become singular, so the closed one-form cannot simply be extended across them. This is a real missing step rather than a technicality. Nontrivial Jordan blocks and transitions among algebraic types remain allowed.

## Credit and novelty

The obstruction is a short application of the established splitting lemma plus compactness and finite fundamental group. It is recorded as a verified deduction, not a claim of a new theorem in the literature. The cached prior attempt did not contain this global simple-eigenvalue obstruction or the two mandatory collision sets.
