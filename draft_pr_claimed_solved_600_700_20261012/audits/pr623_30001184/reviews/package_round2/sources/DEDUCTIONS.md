# Independent deductions from the primary sources

## Hypotheses and success criteria

The reviewed claim is about a **general unital conditional-expectation dilation** `(A, theta, i, p)` of a Markov semigroup `T` on `B`: `i p` is a conditional expectation, and `p theta_t i = T_t`. The target is whether `A = C*(theta_r(i(B)): r >= 0)` alone ensures that the dynamics descends through the **fixed GNS representation of p** and subsequently extends to all adjointable operators. Success for this review means checking the exact original target, deriving the finite-image obstruction without assuming the desired conclusion, and constructing the earlier BFH corollary using explicit endpoint continuity rather than unsupported continuity on all bounded continuous clock functions.

## Finite-image obstruction, independently reconstructed

Let `(E, xi)` be the GNS correspondence of `p` and `pi:A -> B^a(E)` its left action. Suppose `I=ker(pi)` is invariant under every `theta_t` and `C=pi(A)` is finite dimensional.

1. `beta_t(pi(a)) = pi(theta_t(a))` is well defined by invariance, unital, multiplicative, adjoint preserving, and a semigroup. For each represented element, point-norm continuity follows from `||pi(theta_t(a)-theta_u(a))|| <= ||theta_t(a)-theta_u(a)||`. Finite dimension converts this to operator-norm continuity of `beta_t`.
2. Choose `h>0` such that `S_h = integral_0^h beta_u du` is invertible; this is possible because `S_h/h -> Id`. The semigroup law gives `beta_t S_h = integral_t^(t+h) beta_v dv`. Continuity of the integrand yields the right derivative at zero, `delta = (beta_h-Id) S_h^(-1)`.
3. Differentiating `beta_t(cd)=beta_t(c)beta_t(d)` and `beta_t(c*)=beta_t(c)*` at zero shows `delta(cd)=delta(c)d+c delta(d)` and `delta(c*)=delta(c)*`.
4. Write `j=pi i`. It is faithful: `j(b)=0` implies `b=p(i(b))=<xi,j(b)xi>=0`. The unital expectation gives `i(b)xi=xi b`, since the squared module norm of their difference is `p(i(b*)i(b))-b*b=0`. This also follows from the multiplicative domain of `p` on `i(B)`.
5. `pbar(c)=<xi,c xi>` is a UCP `B`-bimodule map relative to `j` with `pbar j=Id`. Thus `T_t=pbar beta_t j`. Its generator satisfies
   `L(bd)=pbar(delta(j(b)j(d)))=L(b)d+bL(d)` and preserves adjoints.

No Hamiltonian representation or quantum channel dilation theorem is used to establish this proposition. It is an elementary deduction for conditional expectations, as claimed by the paper.

For any projection `q` in `B`, a derivation must obey `q L(q) q=0`: apply Leibniz to `q^2=q` and multiply on both sides by `q`. This is the relevant falsifiable boundary check.

## Explicit BFH clock corollary

Use the BFH amplitude-damping example (v2, Section 2, equations (1)–(3), printed/PDF pp.3–4), followed by its clock construction (Definition 4.1 p.9; Theorem 4.4, proof Step 2 and equation (11), p.12).

Let `H_flip` on `C^2_bath tensor C^2_system` interchange `|01>` and `|10>` and vanish on `|00>, |11>`. BFH's coefficient is

`g(x)=1/(2 sqrt(exp(|x|)-1))`, for `x != 0`.

Its integral is

`G(x)=sign(x) arccos(exp(-|x|/2))`, `G(0)=0`.

This is checked by differentiation separately on both half lines and continuity at zero. Its limits are `G(+infinity)=pi/2`, `G(-infinity)=-pi/2`. Consequently

`W(x)=exp(-i G(x) H_flip)`

extends continuously to the two-endpoint compactification `X=[-infinity,+infinity]`. Define

`u_t(x)=W(x) W(x+t)*`,
`alpha_t(F)(x)=u_t(x) F(x+t) u_t(x)*`.

The cocycle identity follows by cancellation. Translation fixes both endpoints and is jointly continuous on `R x X`, so this is a point-norm continuous automorphism group on `C(X,M_4)`: compact time intervals times compact `X` provide uniform continuity of each orbit. This endpoint argument is the additional step needed here. Strong continuity of BFH's Hilbert-space group alone does **not** imply point-norm continuity on all `C_b(R)`.

Put `B=M_2`, `i(b)(x)=I_bath tensor b`, and `A=C*(alpha_r(i(B)):r>=0)`. Then `A` is unital, separable (rational forward times suffice), and forward invariant. The restrictions `theta_t=alpha_t|A` are injective unital endomorphisms. Let `Jv=|1>_bath tensor v`, and set `p(F)=J*F(0)J`. Then `p` is UCP, `p o i=Id_B`, and its bimodule identity shows `i p` is a conditional expectation. The bath convention agrees with BFH Section 2's pure state `|1><1|`; relabeling bath levels gives the Step 1 convention.

For `t>=0`, put `a=cos(G(t))=exp(-t/2)` and `c=sin(G(t))=sqrt(1-exp(-t))`. In the ordered bath/system basis `|00>,|01>,|10>,|11>`, the only nontrivial block of `W(t)` is

`[[a,-i c],[-i c,a]]`

on `|01>,|10>`. Its initial bath columns are

`W(t)J|0> = a|10>-i c|01>`, `W(t)J|1>=|11>`.

Direct compression gives, for `b=[[b00,b01],[b10,b11]]`,

`p alpha_t i(b) = [[a^2 b00+c^2 b11, a b01],[a b10,b11]]`.

These are the Heisenberg dual maps of BFH's displayed amplitude-damping channel, so they form its norm-continuous Markov semigroup. In particular, for `q=diag(1,0)`, `T_t(q)=exp(-t)q` and `L(q)=-q`. Therefore `q L(q) q=-q != 0`.

The GNS correspondence is finite dimensional: the algebraic GNS map `F tensor b -> F(0)Jb` lands in `M_(4,2)` with inner product `Z*Y`; its inner product is precisely `b* p(F*G) d`. Completion of its image remains finite dimensional. Left multiplication by evaluation gives the actual GNS action on this image, so its represented algebra is finite dimensional. Equality of the representation kernel with the whole evaluation kernel is not required for this argument.

If this kernel were invariant at **every** time, the finite-image obstruction would force `L` to be a derivation, contradicting `L(q)=-q`. Thus the BFH construction, restricted to the forward-generated algebra and with the endpoint continuity check supplied, already yields a negative generation-only example at **some** positive time. This argument does not supply failure at every positive time or the paper's explicit positive witnesses; those are the separate refinement of the displayed `M_2/C^2` example.

## Source-scope boundaries

OWR p.498 defines the general dilation using only `p theta_t i=T_t`; p.543 explicitly asks first for preservation of the GNS kernel and then extension. The print error `p:B -> A` on p.542 is resolved by p.498 and both arrows on p.543. The forward-generation sentence is a proposed sufficient example of being sufficiently small, not a specified universal definition of every possible minimality condition.

Shalit–Skeide arXiv v3 Appendix R(i), pp.211–212, distinguishes general dilation, the additional condition `p theta_t=T_t p` (strongness), and corner compression (weakness). A nontrivial unital dilation cannot also be weak: `i(1)=1_A` would make its corner all of `A`. The paper's witness `p(a_s)=0`, `p theta_s(a_s)!=0` checks that its specific example is not strong. The literature does not require a general expectation to be faithful or normal.

Skeide–Sumesh v2 Section 5, especially p.34, asks whether represented left actions admit an endomorphism on all adjointable operators. The present result concerns the fixed GNS action of the given general dilation. It does not deny existence of another dilation, answer arbitrary stronger minimality hypotheses, or prove a normal von Neumann counterexample.
