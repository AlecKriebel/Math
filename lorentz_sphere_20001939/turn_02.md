# Attempt 2 of 5: global Jordan-type rigidity via a Riccati identity

## Target and verdict

Attempt 1 forces spectral collisions, but permits a single size-three Jordan block at every point. This attempt eliminates that possibility by a complete-vector-field argument. Together with the other algebraic cases, it proves that a hypothetical nonproportional pair on S^3 must change algebraic type somewhere. It does not rule out those transitions.

## Lemma: an everywhere size-three block has constant eigenvalue

Let g have Lorentz signature (-,+,+) on a closed connected three-manifold, and let L satisfy the compatibility equation. Suppose L has one real eigenvalue λ=tr(L)/3 and one size-three Jordan block at every point. Then λ is constant and ∇L=0.

Proof. Put N=L-λI. Pointwise there is a basis (e1,e2,e3) such that

N e1=0, N e2=e1, N e3=e2,
g(e1,e3)=g(e2,e2)=1,
g(e1,e1)=g(e1,e2)=g(e2,e3)=g(e3,e3)=0.

The simultaneous canonical frame is unique up to changing all three signs. To see uniqueness, a matrix commuting with the single Jordan block is aI+bN+cN². Preservation of g and g-self-adjointness of this polynomial imply (aI+bN+cN²)²=I. Comparing coefficients gives a=±1 and b=c=0. The frames therefore form a smooth double cover. Work on that cover if necessary; it is still compact, and e1,e2,e3 are now global smooth vector fields. Write θ1,θ2,θ3 for their dual coframe and α=θ3=g(e1,·).

Differentiating tr(L²)=3λ² using compatibility gives dλ∘L=λ dλ. Therefore dλ∘N=0, so

dλ=f α,  f=e3(λ),  grad_g λ=f e1.

Compatibility, with tr L=3λ, reads

∇_X N = (3/2)[X⊗dλ + grad_g λ⊗X^flat] - dλ(X)I.

Let B=N²=e1⊗α. Because N grad_g λ=0 and dλ∘N=0,

∇_X B = (3/2)[NX⊗dλ + grad_g λ⊗(NX)^flat] - 2dλ(X)N.

Write X=a e1+b e2+c e3. Then NX=b e1+c e2 and N=e1⊗θ2+e2⊗α. Substitution yields

∇_X B = 3 f b(e1⊗α) - (f c/2)(e2⊗α+e1⊗θ2).

Since B=e1⊗g(e1,·), differentiating it and comparing the symmetric rank-one factors gives

∇_X e1 = (3/2) f θ2(X)e1 - (1/2) f α(X)e2,
∇_X α = (3/2) f θ2(X)α - (1/2) f α(X)θ2.

Antisymmetrizing the second equation gives dα=2f θ2∧α. Now d(dλ)=d(fα)=0. Evaluating on (e2,e3) gives the Riccati identity

e2(f)=-2f².

The vector field e2 is complete because the covering manifold is compact. Along any integral curve, u(t)=f(γ(t)) solves u'=-2u². A nonzero initial value u0 would give u(t)=u0/(1+2u0 t), which blows up at finite positive or negative time. This contradicts smoothness of f along a complete curve. Therefore f=0 identically. Hence dλ=0, d tr L=0, and compatibility yields ∇L=0. ∎

No affine-geodesic completeness was used: completeness here concerns a smooth vector field on a compact manifold, an entirely different fact.

## Constant algebraic type is impossible for a nontrivial S^3 pair

By algebraic type we mean the number of distinct eigenvalues together with the sizes of their Jordan blocks, not the numerical eigenvalues. Assume a hypothetical pair has constant algebraic type on S^3.

- Nonreal spectrum is excluded by Bolsinov–Matveev, Corollary 1.13.
- With at least two real eigenvalues, dimension three supplies a globally simple branch. When there are two eigenvalues it is the multiplicity-one branch; with three, take the smallest. Attempt 1 excludes it.
- With one eigenvalue and geometric multiplicity at least two, Bolsinov–Matveev, Theorem 1.4, makes L parallel.
- With one eigenvalue and geometric multiplicity one, the lemma above makes L parallel.

A parallel g-self-adjoint tensor on a closed Lorentzian three-manifold with finite fundamental group is scalar. For clarity, the needed elementary argument is: multiple primary factors give a nondegenerate parallel line; a single factor gives L=λI+N. For nonzero nilpotent N, the nonzero highest power B has B²=0 and rank one (the Witt index is one). The induced bilinear form q(Bx,By)=g(x,By) is well-defined, nondegenerate and parallel on im B. Thus that line's holonomy is {±1}, and on the compact simply connected cover there is a nonzero parallel vector. Its dual is an exact nowhere-zero one-form, impossible by compactness. This also verifies the affine-rigidity step used in the cached partial report.

Therefore a nonproportional pair cannot have constant algebraic type.

## Failed extension

The canonical frame in the lemma may cease to exist or become unbounded where N² vanishes. Compactness of the base does not bound a frame defined only on an open Jordan-block stratum. The Riccati blow-up argument cannot be applied through that boundary without a proved extension theorem. Such a theorem is not established here.

## Credit and novelty

The canonical algebraic normal form and compatibility equation are standard; see Bolsinov–Matveev, https://arxiv.org/abs/1301.2492, Proposition 3.1. The displayed Riccati computation is given in full so the deduction can be checked independently. It is not asserted to be historically new.
