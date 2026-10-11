# An explicit Steinberg quotient that is not a rational SL₂-character

## Statement and conventions

Let k be an algebraically closed field of characteristic 3 and G = SL₂(k). Identify the character lattice of the diagonal torus diag(t,t⁻¹) with ℤ, using t ↦ t as the fundamental weight. Write z for its formal exponential. Then

\[
\frac{\operatorname{ch}T(4)}{\operatorname{ch}\mathrm{St}}
=z^2+z^{-2},
\]

and this is not the character of any finite-dimensional rational G-module. In the convention t(λ) = ch T((p−1)ρ+λ)/ch St, this is t(2), since p = 3 and ρ = 1.

Here Sym means the symmetric-power quotient, not the divided-power functor. For SL₂ with the usual highest-weight convention,

\[
\nabla(n)\cong\operatorname{Sym}^n E,
\qquad
\Delta(n)\cong\nabla(n)^*,
\]

where E is the natural module. One way to see the first identification is ∇(n) = H⁰(ℙ(E),O(n)) = Symⁿ(E*) and the determinant pairing E ≅ E*. This identifies Symⁿ(E) with Symⁿ(E*), not automatically with (Symⁿ(E))*; the latter distinction matters when n! is not invertible. The same conventions are stated explicitly in [Martin, §1.1, p. 2](https://arxiv.org/pdf/1705.06980v3#page=2) and [Doty–Henke, Lemma 1.1 proof, p. 3](https://arxiv.org/pdf/math/0205186v1#page=3).

The only general tilting-theoretic fact needed below is the standard uniqueness, up to isomorphism, of the indecomposable tilting module T(n) with highest weight n. Tilting means that both a ∇-filtration and a Δ-filtration exist. We prove indecomposability directly, so do not need the direct-summand closure theorem for the main argument.

## 1. Construction and self-duality

Take a basis x,y of E and set

\[
V=\operatorname{Sym}^2E,
\qquad a=x^2,\quad b=xy,\quad c=y^2.
\]

The weights of a,b,c are 2,0,−2. The lower root subgroup, denoted ℓ(t), acts by x ↦ x+ty, y ↦ y, hence

\[
a\mapsto a+2tb+t^2c,\qquad b\mapsto b+tc,\qquad c\mapsto c.
\]

The upper subgroup u(t) acts by x ↦ x, y ↦ y+tx, hence

\[
a\mapsto a,\qquad b\mapsto b+ta,\qquad c\mapsto c+2tb+t^2a.
\]

Every nonzero G-submodule of V contains a torus weight vector. Starting with a or c, these formulas generate all three basis vectors; starting with b first gives c. Here k is infinite and 2 is nonzero, so coefficients of the displayed polynomial orbit belong to its span. Thus V is simple. It is also ∇(2).

An invariant symmetric bilinear form B on V is given in this characteristic by

\[
B(a,c)=B(c,a)=B(b,b)=1
\]

and zero on the remaining basis pairs. Its determinant is −1, and the displayed upper/lower formulas verify its invariance. Weight sums verify torus invariance. These subgroups generate SL₂, so V is self-dual. Consequently V is both ∇(2) and Δ(2), hence V = T(2) = St.

Set

\[
W=\operatorname{Sym}^2V
\]

with ordered basis a²,ab,ac,b²,bc,c² and respective weights 4,2,0,0,−2,−4. The pairing

\[
C(v_1v_2,w_1w_2)
=B(v_1,w_1)B(v_2,w_2)+B(v_1,w_2)B(v_2,w_1)
\]

is well-defined, symmetric and G-invariant. Its nonzero basis entries, besides their symmetric counterparts, are

\[
C(a^2,c^2)=2,\quad C(ab,bc)=1,\quad
C(ac,ac)=1,\quad C(b^2,b^2)=2.
\]

All four blocks are nondegenerate, so W ≅ W*. Equivalently one may use the degree-two symmetrizer (1+τ)/2 in V⊗V. That argument is legitimate precisely because 2 is invertible; it does not use a degree-four symmetrizer.

## 2. Both filtrations

Multiplication of degree-two polynomials gives a G-equivariant surjection

\[
m:W\longrightarrow\operatorname{Sym}^4E.
\]

Its basis images are x⁴,x³y,x²y²,x²y²,xy³,y⁴, so it is surjective and

\[
\ker m=kq,\qquad q=ac-b^2.
\]

The vector q is fixed by both root groups and by the torus. Thus

\[
0\longrightarrow\nabla(0)\longrightarrow W\longrightarrow\nabla(4)\longrightarrow0
\]

is a good filtration. Taking the ordinary linear dual gives

\[
0\longrightarrow\Delta(4)\longrightarrow W^*\longrightarrow\Delta(0)\longrightarrow0.
\]

Since W ≅ W*, this is also a Weyl filtration of W. Therefore W is tilting. No assertion that Sym⁴E is self-dual is used.

## 3. Invariants and nonsplitting

A G-invariant vector must lie in the weight-zero space, so has the form r ac+s b². Its image under ℓ(t) differs from itself by

\[
(r+s)(2tbc+t^2c^2).
\]

Therefore r+s=0, and the converse follows from invariance of q. Hence Wᴳ = kq.

For an invariant functional f:W→k, torus invariance forces f to vanish on all nonzero weight spaces. Put f(ac)=u and f(b²)=v. Expanding the image of a² under ℓ(t) gives

\[
\ell(t)a^2=a^2+4tab+(2ac+4b^2)t^2+4t^3bc+t^4c^2.
\]

Its t² coefficient implies 2u+4v=0. In characteristic 3 this is v=u. In particular f(q)=0 for every invariant functional. A retraction onto kq would give an invariant functional nonzero on q, so kq is not a direct summand. The functional with f(ac)=f(b²)=1 and the remaining basis values zero is indeed invariant, as a check on the calculation.

## 4. Elementary indecomposability

The same orbit expansion simplifies in characteristic 3 to

\[
\ell(t)a^2=a^2+tab-t^2q+t^3bc+t^4c^2.
\]

The five coefficient vectors a²,ab,−q,bc,c² are linearly independent. Since k is infinite, the span of this polynomial orbit contains all of them: a linear functional vanishing on all orbit values yields the zero polynomial and therefore vanishes on every coefficient.

Suppose W=A⊕D were a nontrivial decomposition into rational G-submodules. The weight-4 space is the single line ka², so after interchanging A and D we have a²∈A. The orbit calculation forces dim A≥5 and q∈A. Since dim W=6, dim D=1.

Every one-dimensional rational SL₂-module is trivial. Indeed its restriction to either root subgroup defines an algebraic homomorphism Gₐ→Gₘ, which is trivial because the units in k[t] are constant; the root subgroups generate SL₂. Consequently D⊂Wᴳ=kq⊂A, contradicting A∩D=0.

Thus W is indecomposable. It is tilting with highest weight 4, so W≅T(4).

The frozen candidate's alternative argument is also valid: a tilting module's indecomposable summands are tilting; the summand with highest weight 4 has a Δ(4) filtration factor and dimension at least 5; any complementary summand would be one-dimensional and trivial, which §3 rules out. The direct argument above removes those additional structure-theorem dependencies.

## 5. Formal character division

Counting the actual torus weights gives an identity in ℤ[z,z⁻¹], not in characteristic-3 coefficients:

\[
\operatorname{ch}T(4)=z^4+z^2+2+z^{-2}+z^{-4}
=(z^2+1+z^{-2})(z^2+z^{-2}).
\]

Since ch St=z²+1+z⁻², the displayed quotient follows. As an independent established-character check, [Doty–Henke, Lemma 1.1(b), p. 3](https://arxiv.org/pdf/math/0205186v1#page=3) implies ch T(4)=χ(4)+χ(0) at p=3, agreeing with this construction.

## 6. Excluding every rational G-module

Suppose a finite-dimensional rational G-module M had character z²+z⁻². Then its only torus weight spaces would be M₂ and M₋₂, each one-dimensional. Let e,f,h be the standard basis of sl₂ with [e,f]=h. Torus conjugation has weights +2 and −2 on e and f, so differentiation of the rational G-action gives

\[
eM_m\subset M_{m+2},\qquad fM_m\subset M_{m-2}.
\]

These are exact integer torus characters, not their residue classes modulo 3. For m∈{2,−2}, none of the target weights 4,0,−4 is present. Hence e=f=0 on M, and therefore h=[e,f]=0. But h acts on M₂ by the differential of t↦t², namely multiplication by 2≠0 in k. This is a contradiction.

The exact-weight argument is essential: replacing torus weights by their differential eigenvalues modulo 3 would lose information. Frobenius-twisted rational modules do not evade the contradiction, because their weights are multiples of 3 and our proposed weight 2 has nonzero differential.

## Conclusion and limits

This is an ordinary-rational-G-module obstruction, already for type A₁ in good characteristic. It does not deny that the quotient is a torus character, a virtual G-character, or a geometric character. Indeed t(2)=ch St−ch k in the Grothendieck group. The construction verifies standard rank-one representation theory; no novelty or first-counterexample claim is made. It neither proves nor refutes the general geometric realization at bad primes.
